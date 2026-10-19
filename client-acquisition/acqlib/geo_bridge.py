"""Read-only bridge to the existing GEO pipeline. Opens GEO files for reading only; never writes to them.

- sync_ledger():  every email GEO sent (outreach_send_ledger.jsonl) becomes a touch, so no acq playbook
                  can pitch a business GEO already contacted. Called automatically before every gate decision.
- import_audit_index(): GEO-audited businesses + their GEO finding as an opportunity (not a touch).
- import_sheet() / guard_rows(): optional, needs gspread (run with the GEO venv python). Reads the Google
                  Sheet's Leads/Outreach tabs to pick up non-email sends, replies and NOT_INTERESTED rows.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import identity
from .db import now_iso, parse_iso

SHEET_SENT = {"SENT", "OPENED", "FOLLOW_UP_DUE", "FOLLOWED_UP"}
CHANNEL_MAP = {"email": "email", "linkedin": "linkedin", "instagram": "instagram", "contact form": "contact_form",
               "whatsapp": "whatsapp", "whatsapp manual": "whatsapp", "facebook": "facebook"}


def _geo(reg) -> dict:
    return reg.settings.get("geo", {})


def sync_ledger(reg) -> int:
    path = _geo(reg).get("ledger")
    if not path or not Path(path).exists():
        return 0
    added = 0
    with open(path, encoding="utf-8") as f:   # read-only
        lines = f.read().splitlines()
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        domain = identity.domain_key(e.get("domain", "")) or (e.get("domain") or "").lower()
        if not domain or not e.get("ts"):
            continue
        key = "geo-ledger:" + (e.get("msg_id") or f"{e['ts']}|{domain}|{e.get('kind', 'pitch')}")
        if reg.q1("SELECT 1 FROM touches WHERE idempotency_key=?", (key,)):
            continue
        bid, _ = reg.upsert_business(name=domain, website=f"https://{domain}", emails=[], source="geo-ledger")
        kind = "followup" if "follow" in str(e.get("kind", "")).lower() else "pitch"
        reg.conn.execute(
            "INSERT INTO touches (business_id, playbook, kind, channel, recipient, topic, state, idempotency_key, "
            "message_id, source, created_at, sent_at) VALUES (?, 'geo', ?, 'email', ?, 'GEO audit report', 'SENT', ?, ?, "
            "'geo-ledger', ?, ?)",
            (bid, kind, identity.normalize_email(e.get("to", "")) or e.get("to"), key, e.get("msg_id"), now_iso(),
             parse_iso(e["ts"]).isoformat()))
        reg.conn.execute("UPDATE businesses SET status='contacted', updated_at=? WHERE id=? AND status='new'",
                         (now_iso(), bid))
        added += 1
    return added


def import_audit_index(reg) -> int:
    path = _geo(reg).get("audit_index")
    if not path or not Path(path).exists():
        return 0
    with open(path, encoding="utf-8") as f:
        entries = json.load(f)
    n = 0
    for e in entries if isinstance(entries, list) else []:
        domain = e.get("domain")
        if not domain:
            continue
        bid, _ = reg.upsert_business(name=e.get("client_name") or domain, website=f"https://{domain}",
                                     source="geo-audit-index")
        score, status = e.get("geo_readiness"), e.get("composite_status", "")
        reg.add_opportunity(bid, "geo", f"GEO readiness {score} ({status}) on {e.get('date', '')}", "OBSERVED")
        n += 1
    return n


def suppress_own_domains(reg) -> list:
    done = []
    for d in reg.settings.get("own_domains", []):
        bid, _ = reg.upsert_business(name=d, website=f"https://{d}", source="own-domain")
        reg.suppress("business", bid, "own business / test site", "settings.own_domains")
        done.append(d)
    return done


# ---------------------------------------------------------------- Google Sheet (optional)
def _open_sheet(reg):
    try:
        import gspread  # available in the GEO venv
    except ImportError as exc:
        raise RuntimeError("gspread not installed. Run this command with the GEO venv python: "
                           "~/.gemini/config/skills/geo/.venv/bin/python3 ~/.gemini/config/skills/acq/acq.py ...") from exc
    g = _geo(reg)
    client = gspread.service_account(filename=g["service_account"])
    return client.open_by_key(g["sheet_id"])


def _cell(v) -> str:
    s = str(v or "").strip()
    if s.upper().startswith("=HYPERLINK("):
        parts = s.split('"')
        return parts[3] if len(parts) > 3 else (parts[1] if len(parts) > 1 else s)
    return s


def import_sheet(reg, dry_run=True) -> dict:
    """Read Leads + Outreach tabs (read-only API calls) and fold them into the registry."""
    doc = _open_sheet(reg)
    country = _geo(reg).get("default_country", "US")
    stats = {"leads": 0, "touches": 0, "replied": 0, "suppressed": 0}
    leads = doc.worksheet("Leads").get_all_records()
    outreach = doc.worksheet("Outreach").get_all_records()
    if dry_run:
        stats.update(leads=len(leads), outreach_rows=len(outreach),
                     sent_rows=sum(1 for r in outreach if str(r.get("Outreach Status", "")).upper() in SHEET_SENT))
        return stats
    for r in leads:
        site = _cell(r.get("Website") or r.get("Domain"))
        if not site:
            continue
        reg.upsert_business(name=_cell(r.get("Business Name")), website=site, phone=_cell(r.get("Phone")),
                            maps_url=_cell(r.get("Google Maps URL")) or None, city=_cell(r.get("City")),
                            region=_cell(r.get("State")), country=country, source="geo-sheet")
        stats["leads"] += 1
    for r in outreach:
        domain = identity.domain_key(_cell(r.get("Domain")))
        if not domain:
            continue
        bid, _ = reg.upsert_business(name=_cell(r.get("Business Name")) or domain, website=f"https://{domain}",
                                     country=country, source="geo-sheet")
        status = str(r.get("Outreach Status", "")).strip().upper()
        channel = CHANNEL_MAP.get(str(r.get("Active Priority Channel", "")).strip().lower(), "other")
        if status in SHEET_SENT or status in ("REPLIED", "NOT_INTERESTED"):
            # Email sends are already in the ledger; record non-email sends the ledger never saw.
            has_ledger = reg.q1("SELECT 1 FROM touches WHERE business_id=? AND source='geo-ledger'", (bid,))
            if channel != "email" or not has_ledger:
                key = f"geo-sheet:{domain}:{channel}"
                if not reg.q1("SELECT 1 FROM touches WHERE idempotency_key=?", (key,)):
                    sent_at = _sent_date_from_followup(r.get("Follow-up Due Date"))
                    reg.conn.execute(
                        "INSERT INTO touches (business_id, playbook, kind, channel, recipient, topic, state, "
                        "idempotency_key, source, created_at, sent_at) VALUES (?, 'geo', 'pitch', ?, ?, "
                        "'GEO audit report', 'SENT', ?, 'geo-sheet', ?, ?)",
                        (bid, channel, _cell(r.get("Active Target Destination")), key, now_iso(), sent_at))
                    stats["touches"] += 1
        if status == "REPLIED":
            reg.record_outcome(bid, "replied", "from GEO sheet")
            stats["replied"] += 1
        elif status == "NOT_INTERESTED":
            reg.record_outcome(bid, "not_interested", "from GEO sheet")
            stats["suppressed"] += 1
    return stats


def _sent_date_from_followup(v) -> str:
    """The sheet stores follow-up due = sent + 3 days. Unknown -> now (the conservative choice for cooldowns)."""
    s = str(v or "").strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            d = datetime.strptime(s, fmt).replace(tzinfo=timezone.utc) - timedelta(days=3)
            return d.isoformat()
        except ValueError:
            continue
    return now_iso()


def guard_rows(reg) -> list:
    """GEO Outreach rows still READY_TO_SEND whose business the registry says must not be contacted."""
    doc = _open_sheet(reg)
    out = []
    for r in doc.worksheet("Outreach").get_all_records():
        if str(r.get("Outreach Status", "")).strip().upper() != "READY_TO_SEND":
            continue
        bid = reg.find(_cell(r.get("Domain")))
        if not bid:
            continue
        others = reg.q("SELECT playbook, channel, sent_at FROM touches WHERE business_id=? AND state='SENT' "
                       "AND playbook != 'geo'", (bid,))
        hits = reg.suppression_hits(bid)
        if others or hits:
            why = hits + [f"contacted by playbook {t['playbook']} via {t['channel']} on {t['sent_at'][:10]}" for t in others]
            out.append((_cell(r.get("Domain")), why))
    return out
