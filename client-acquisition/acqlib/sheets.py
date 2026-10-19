"""Per-playbook client sheet: a view of the registry, written to a local CSV and (optionally) its own Google Sheet.

The registry stays the source of truth; each sync rewrites the sheet. It never writes to the GEO sheet.
"""
from __future__ import annotations

import csv
import json
import re

from . import identity, playbooks
from .config import data_paths

COLUMNS = ["Business", "Stage", "Priority", "Website", "City", "State", "Properties / listings",
           "Observed problems (evidence)", "Signals", "Email", "Instagram", "Facebook", "Other contact",
           "Listing links (view yourself)", "Sample", "Draft", "Last contact", "Next step", "Updated"]
HIDDEN_STAGES = ("skipped",)
NEXT = {"qualified": "make sample: /airbnb-sample", "sample_ready": "write message: /airbnb-message",
        "drafted": "approve + send: /airbnb-message", "contacted": "wait for reply / follow-up",
        "found": "check: /airbnb-client", "rejected": "-"}


def _short(summary: str) -> str:
    text = summary.split(": ", 1)[-1]
    if text.startswith(("yes (", "no (")) and text.endswith(")"):
        text = text.split("(", 1)[1][:-1]
    return text[:120]


def rows_for(reg, pb: dict, include_rejected=False) -> list:
    pid = pb["id"]
    signal_ids = set(pb["qualify"].get("signals", []))
    rows = []
    for p in reg.q("SELECT * FROM prospects WHERE playbook=? ORDER BY "
                   "CASE stage WHEN 'contacted' THEN 0 WHEN 'drafted' THEN 1 WHEN 'sample_ready' THEN 2 "
                   "WHEN 'qualified' THEN 3 WHEN 'needs_check' THEN 4 ELSE 5 END, priority DESC, id", (pid,)):
        if p["stage"] in HIDDEN_STAGES or (p["stage"] == "rejected" and not include_rejected):
            continue
        bid = p["business_id"]
        b = reg.business(bid)
        ev = reg.current_evidence(bid, pid)
        problems, signals, props = [], [], ""
        for cid, e in ev.items():
            if cid == "_contacts" or e["status"] != "OBSERVED" or e["hit"] != 1:
                continue
            try:
                c = playbooks.check_by_id(pb, cid)
            except KeyError:
                continue
            if cid == "multi_listing":
                props = _short(e["summary"])
            elif cid == "site_multi_property" and not props:
                m = re.match(r"(\d+) counted", e["summary"])
                props = f"{m.group(1)} properties on own site" if m else "2+ on own site"
            if c.get("problem") and cid not in signal_ids:
                text = _short(e["summary"]) if e["method"] == "manual" else c["problem"]
                problems.append(f"E{e['id']}: {text} (seen {e['observed_at'][:10]})")
            elif cid in signal_ids:
                signals.append(c["label"])
        cont = json.loads(ev["_contacts"]["summary"]) if "_contacts" in ev else {}
        socials = {s["network"]: s["url"] for s in cont.get("socials", [])}
        other = [f["page"] for f in cont.get("contact_forms", [])] + [s["url"] for s in cont.get("socials", [])
                                                                       if s["network"] not in ("instagram", "facebook")]
        listings = [f"https://www.{i['value']}" for i in reg.identifiers(bid)
                    if i["kind"] == "profile" and identity.automation_forbidden(i["value"])]
        sample = reg.latest_sample(bid, pid)
        draft = reg.q1("SELECT id, status FROM drafts WHERE business_id=? AND playbook=? ORDER BY id DESC LIMIT 1",
                       (bid, pid))
        last = reg.q1("SELECT sent_at, channel, playbook FROM touches WHERE business_id=? AND state='SENT' "
                      "ORDER BY sent_at DESC LIMIT 1", (bid,))
        nxt = NEXT.get(p["stage"], "-")
        if p["stage"] == "needs_check":
            nxt = p["reason"] or "verify"
        rows.append([
            b["name"], p["stage"], p["priority"], b["website"] or reg.primary_domain(bid) or "", b["city"] or "",
            b["region"] or "", props, "\n".join(problems), ", ".join(signals),
            ", ".join(e["email"] for e in cont.get("emails", [])), socials.get("instagram", ""),
            socials.get("facebook", ""), ", ".join(other[:2]), "\n".join(listings[:5]),
            (sample["link"] or sample["path"]) if sample else "", f"#{draft['id']} {draft['status']}" if draft else "",
            f"{last['sent_at'][:10]} {last['channel']} ({last['playbook']})" if last else "", nxt,
            p["updated_at"][:16].replace("T", " "),
        ])
    return rows


def write_csv(reg, pb: dict, rows) -> str:
    path = data_paths(reg.settings)["exports"] / f"{pb['id']}-clients.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLUMNS)
        w.writerows(rows)
    return str(path)


def sheet_config(settings: dict, pid: str) -> dict:
    cfg = dict(settings.get("sheets", {}).get(pid, {}))
    sid = (cfg.get("sheet_id") or "").strip()
    if "/d/" in sid:  # a pasted URL
        sid = sid.split("/d/", 1)[1].split("/", 1)[0]
    cfg["sheet_id"] = sid
    cfg.setdefault("tab", "Clients")
    return cfg


def sync_google(reg, pb: dict, rows) -> str:
    cfg = sheet_config(reg.settings, pb["id"])
    if not cfg["sheet_id"]:
        raise RuntimeError(f"no Google Sheet configured for {pb['id']} (settings.json → sheets)")
    if cfg["sheet_id"] == reg.settings.get("geo", {}).get("sheet_id"):
        raise RuntimeError("refusing to write: that is the GEO sheet. Use a separate sheet for this playbook.")
    import gspread  # GEO venv provides it

    client = gspread.service_account(filename=reg.settings["geo"]["service_account"])
    doc = client.open_by_key(cfg["sheet_id"])
    try:
        ws = doc.worksheet(cfg["tab"])
    except gspread.exceptions.WorksheetNotFound:
        ws = doc.add_worksheet(title=cfg["tab"], rows=max(100, len(rows) + 10), cols=len(COLUMNS))
    ws.clear()
    ws.update(range_name="A1", values=[COLUMNS] + [[str(v) for v in r] for r in rows], value_input_option="RAW")
    try:
        ws.freeze(rows=1)
        ws.format("1:1", {"textFormat": {"bold": True}})
    except Exception:
        pass
    return f"https://docs.google.com/spreadsheets/d/{cfg['sheet_id']}"
