#!/usr/bin/env python3
"""acq: evidence-first client acquisition engine (shared by the acq, acq-find, acq-offer, acq-outreach skills).

Run `python3 ~/.gemini/config/skills/acq/acq.py -h` for commands. Nothing is ever sent without:
validation -> a human approval (native dialog) -> sending_enabled=true -> the shared eligibility gate.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from acqlib import baseline, checks, discover, geo_bridge, outreach, playbooks, samples, sheets  # noqa: E402
from acqlib import policy as gate  # noqa: E402
from acqlib.config import data_paths, ensure_data_dirs, load_env, load_policy, load_settings  # noqa: E402
from acqlib.db import connect  # noqa: E402
from acqlib.registry import OUTCOMES, Registry  # noqa: E402
from acqlib.web import Fetcher  # noqa: E402


def die(msg, code=1):
    print(f"❌ {msg}")
    sys.exit(code)


def open_registry():
    settings, pol = load_settings(), load_policy()
    paths = ensure_data_dirs(settings)
    return Registry(connect(paths["db"]), settings, pol)


def need(reg, ref):
    bid = reg.find(ref)
    if not bid:
        die(f"no business matches '{ref}' (use #id, domain, profile URL or email)")
    return bid


def table(rows, headers):
    rows = [[("" if v is None else str(v)) for v in r] for r in rows]
    widths = [min(60, max(len(h), *(len(r[i]) for r in rows))) if rows else len(h) for i, h in enumerate(headers)]
    print("  ".join(h.ljust(w) for h, w in zip(headers, widths)))
    for r in rows:
        print("  ".join(v[:w].ljust(w) for v, w in zip(r, widths)))


# ------------------------------------------------------------------------------------------- commands
def cmd_init(a):
    reg = open_registry()
    paths = data_paths(reg.settings)
    if not baseline.latest(paths["baseline"]):
        print(f"GEO baseline created: {baseline.create(reg.settings, paths['baseline'])}")
    own = geo_bridge.suppress_own_domains(reg)
    n_audit = geo_bridge.import_audit_index(reg)
    n_ledger = geo_bridge.sync_ledger(reg)
    print(f"Registry: {paths['db']}")
    print(f"Imported from GEO (read-only): {n_audit} audited businesses, {n_ledger} new sent emails from the ledger")
    print(f"Suppressed own domains: {', '.join(own) or 'none'}")
    print("Optional: pick up LinkedIn/Instagram/form sends + replies from the GEO sheet with\n"
          "  ~/.gemini/config/skills/geo/.venv/bin/python3 ~/.gemini/config/skills/acq/acq.py import geo --sheet")


def cmd_import(a):
    reg = open_registry()
    if a.source != "geo":
        die("only 'geo' is supported")
    if a.sheet:
        stats = geo_bridge.import_sheet(reg, dry_run=a.dry_run)
        print(("[DRY RUN] " if a.dry_run else "") + json.dumps(stats))
    else:
        print(f"audit index: {geo_bridge.import_audit_index(reg)}  ledger (new): {geo_bridge.sync_ledger(reg)}")


def cmd_guard_geo(a):
    reg = open_registry()
    geo_bridge.sync_ledger(reg)
    rows = geo_bridge.guard_rows(reg)
    if not rows:
        print("✅ No GEO READY_TO_SEND row conflicts with the registry.")
        return
    print("⚠️  Do NOT send these with /geo-message (set them aside in the sheet yourself):")
    for dom, why in rows:
        print(f"  {dom}: " + "; ".join(why))


def cmd_baseline(a):
    s = load_settings()
    paths = ensure_data_dirs(s)
    if a.action == "create":
        print(baseline.create(s, paths["baseline"]))
        return
    ref = baseline.latest(paths["baseline"])
    if not ref:
        die("no baseline yet: run `acq baseline create`")
    r = baseline.verify(s, ref)
    ok = not (r["changed"] or r["missing"])
    print(("✅ GEO files unchanged" if ok else "❌ GEO files differ from baseline") + f" ({r['checked']} files, {ref.name})")
    for k in ("changed", "missing", "added"):
        for p in r[k][:50]:
            print(f"  {k}: {p}")
    if not ok:
        sys.exit(2)


def cmd_playbook(a):
    if a.action == "list":
        for pid in playbooks.list_ids():
            pb = playbooks.load(pid)
            print(f"{pid:24} {pb['name']}  →  {pb['offer']['title']}")
    elif a.action in ("show", "validate"):
        if not a.ref:
            die("give a playbook id or file")
        try:
            pb = playbooks.load(a.ref)
        except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
            die(str(e))
        if a.action == "validate":
            print(f"✅ {pb['id']} is valid ({len(pb['checks'])} checks)")
        else:
            print(json.dumps({k: v for k, v in pb.items() if k != "_path"}, indent=1, ensure_ascii=False))


def cmd_find(a):
    reg = open_registry()
    pb = playbooks.load(a.playbook)
    country = a.country or pb["target"].get("default_country")
    if a.urls or a.urls_file:
        urls = list(a.urls or [])
        if a.urls_file:
            urls += Path(a.urls_file).read_text().splitlines()
        cands, source = discover.from_urls(urls, country), "urls"
    elif a.csv:
        cands, source = discover.from_csv(a.csv, country), "csv"
        if not cands:
            print(f"ℹ️  {a.csv} has no host rows yet (header only, or rows without website/profile/listing links). "
                  "Add rows, or paste host notes in chat, then run this again.")
            return
    else:
        if pb.get("discovery", {}).get("source") != "google_places":
            die("this playbook has no google_places discovery; use --urls/--urls-file/--csv")
        if not a.location:
            die("--location is required for Google Places discovery")
        budget = discover.places_budget(reg.settings)
        print(f"Places budget this month: GEO {budget['geo']} + acq {budget['acq']} / {budget['limit']}")
        queries = [a.query] if a.query else pb["discovery"]["queries"]
        cands, source = [], "google_places"
        for q in queries:
            text = f"{q} in {a.location}"
            try:
                found = discover.places_search(reg.settings, text, max_pages=a.max_pages)
            except RuntimeError as e:
                print(f"⚠️  {e}")
                break
            print(f"  '{text}': {len(found)} results")
            cands += [discover.from_place(p) for p in found]
    stats = discover.ingest(reg, pb, cands, source, dry_run=a.dry_run)
    table(stats.pop("rows")[: a.show], ["business", "result", "note"])
    print(("[DRY RUN] " if a.dry_run else "") + json.dumps(stats))
    if not a.dry_run and stats["new_prospects"]:
        print(f"Next: python3 ~/.gemini/config/skills/acq/acq.py check {pb['id']}")


def cmd_check(a):
    reg = open_registry()
    pb = playbooks.load(a.playbook)
    fetcher = Fetcher(reg.settings)
    if a.business:
        bids = [need(reg, r) for r in a.business]
    else:
        stages = ("found", "needs_check") if a.recheck else ("found",)
        rows = reg.q(f"SELECT business_id FROM prospects WHERE playbook=? AND stage IN ({','.join('?' * len(stages))}) "
                     "ORDER BY id", (pb["id"], *stages))
        bids = [r["business_id"] for r in rows][: a.limit]
    if not bids:
        print("Nothing to check.")
        return
    summary = []
    for bid in bids:
        p = reg.prospect(bid, pb["id"])
        if p and p["stage"] in ("skipped", "contacted") and not a.force:
            summary.append((reg.label(bid), p["stage"], p["reason"]))
            continue
        res = checks.check_business(reg, fetcher, pb, bid)
        summary.append((reg.label(bid), res["stage"], res["reason"]))
        print(f"• {reg.label(bid)} → {res['stage']}: {res['reason']}")
    print()
    table(summary, ["business", "stage", "reason"])


def cmd_evidence(a):
    reg = open_registry()
    pb = playbooks.load(a.playbook)
    bid = need(reg, a.ref)
    try:
        playbooks.check_by_id(pb, a.check)
    except KeyError as e:
        die(str(e))
    status = "OBSERVED" if a.source_url else "HYPOTHESIS"
    eid = reg.add_evidence(bid, pb["id"], a.check, status, a.hit == "yes", a.note, source_url=a.source_url,
                           method="manual")
    print(f"E{eid} recorded as {status}" + ("" if a.source_url else " (no --source-url, so it cannot qualify a prospect)"))
    stage, reason, _ = checks.qualify(reg, bid, pb)
    print(f"{reg.label(bid)} → {stage}: {reason}")


def cmd_qualify(a):
    reg = open_registry()
    pb = playbooks.load(a.playbook)
    bid = need(reg, a.ref)
    stage, reason, pr = checks.qualify(reg, bid, pb)
    print(f"{reg.label(bid)} → {stage} (priority {pr}): {reason}")


def cmd_sample(a):
    reg = open_registry()
    pb = playbooks.load(a.playbook)
    bid = need(reg, a.ref)
    try:
        if a.action == "prepare":
            d = samples.prepare(reg, Fetcher(reg.settings), pb, bid, download_images=a.download_images)
            print(f"Brief: {d / 'brief.md'}\nJSON:  {d / 'brief.json'}")
        else:
            sid = samples.register(reg, pb, bid, file=a.file, link=a.link)
            print(f"Sample #{sid} registered for {reg.label(bid)}")
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        die(str(e))


def cmd_draft(a):
    reg = open_registry()
    if a.action == "create":
        pb = playbooks.load(a.playbook)
        bid = need(reg, a.ref)
        body = Path(a.body_file).read_text(encoding="utf-8") if a.body_file else (a.body or "")
        ev = [int(x.strip().lstrip("Ee")) for x in (a.evidence or "").split(",") if x.strip()]
        did, status, problems, dec = outreach.create_draft(
            reg, pb, bid=bid, channel=a.channel, recipient=a.to, subject=a.subject, body=body.strip(),
            evidence_ids=ev, kind=a.kind, parent_touch_id=a.parent, recipient_source=a.recipient_source)
        print(f"Draft #{did}: {status}")
        for p in problems:
            print(f"  ✗ {p}")
        if not dec.allowed:
            print(f"  gate: {dec}")
        if status == "draft":
            print(f"Next (a person): python3 ~/.gemini/config/skills/acq/acq.py approve {did}")
    elif a.action == "list":
        sql, params = "SELECT * FROM drafts WHERE 1=1", []
        if a.status:
            sql += " AND status=?"
            params.append(a.status)
        if a.playbook:
            sql += " AND playbook=?"
            params.append(a.playbook)
        rows = reg.q(sql + " ORDER BY id DESC LIMIT 100", params)
        table([(d["id"], reg.label(d["business_id"]), d["playbook"], d["kind"], d["channel"], d["recipient"],
                d["status"]) for d in rows], ["id", "business", "playbook", "kind", "channel", "to", "status"])
    elif a.action == "show":
        d = reg.q1("SELECT * FROM drafts WHERE id=?", (a.id,)) or die(f"draft #{a.id} not found")
        sample = reg.q1("SELECT * FROM samples WHERE id=?", (d["sample_id"],)) if d["sample_id"] else None
        print(outreach.preview(reg, reg.settings, load_env(reg.settings), d, sample))
        print(f"\nstatus: {d['status']}  problems: {d['problems']}")
    elif a.action == "reject":
        reg.conn.execute("UPDATE drafts SET status='rejected' WHERE id=? AND status IN ('draft','approved','invalid','blocked')",
                         (a.id,))
        print(f"draft #{a.id} rejected")


def cmd_approve(a):
    reg = open_registry()
    outreach.approve(reg, reg.settings, load_env(reg.settings), playbooks.load, a.ids)


def cmd_send(a):
    reg = open_registry()
    d = reg.q1("SELECT * FROM drafts WHERE id=?", (a.id,)) or die(f"draft #{a.id} not found")
    print(outreach.send(reg, reg.settings, load_env(reg.settings), playbooks.load(d["playbook"]), a.id, live=a.live))


def cmd_touch(a):
    reg = open_registry()
    if a.action == "list":
        sql = "SELECT * FROM touches" + (" WHERE state IN ('PENDING','UNKNOWN')" if a.pending else "")
        rows = reg.q(sql + " ORDER BY id DESC LIMIT 200")
        table([(t["id"], reg.label(t["business_id"]), t["playbook"], t["kind"], t["channel"], t["recipient"],
                t["state"], (t["sent_at"] or t["created_at"])[:16], t["source"]) for t in rows],
              ["id", "business", "playbook", "kind", "channel", "to", "state", "when", "source"])
    else:
        state = "SENT" if a.sent else "FAILED" if a.failed else "UNKNOWN"
        gate.resolve_touch(reg, a.id, state, message_id=a.message_id)
        print(f"touch #{a.id} → {state}")


def cmd_followups(a):
    reg = open_registry()
    rows = outreach.followups_due(reg, [a.playbook] if a.playbook else None)
    if not rows:
        print("No acq pitches awaiting follow-up.")
    for t, dec in rows:
        tag = "DUE" if dec.allowed else "not now"
        print(f"[{tag}] touch #{t['id']} {reg.label(t['business_id'])} {t['channel']} sent {t['sent_at'][:10]}")
        if not dec.allowed:
            for r in dec.reasons:
                print(f"     - {r}")
        else:
            print(f"     draft: acq draft create {t['business_id']} --playbook {t['playbook']} --kind followup "
                  f"--parent {t['id']} --channel {t['channel']} --to '{t['recipient']}' ...")


def cmd_outcome(a):
    reg = open_registry()
    bid = need(reg, a.ref)
    reg.record_outcome(bid, a.outcome, a.note, a.email)
    print(f"{reg.label(bid)}: {a.outcome} recorded")


def cmd_suppress(a):
    reg = open_registry()
    value = a.value
    if a.kind == "business":
        value = str(need(reg, a.value))
    try:
        norm = reg.suppress(a.kind, value, a.reason, "manual")
    except ValueError as e:
        die(str(e))
    print(f"suppressed {a.kind} {norm}: {a.reason}")


def cmd_review(a):
    reg = open_registry()
    if a.action == "list":
        rows = reg.q("SELECT * FROM businesses WHERE needs_review=1 AND merged_into IS NULL ORDER BY id")
        if not rows:
            print("Review queue is empty.")
        for b in rows:
            ids = ", ".join(f"{i['kind']}={i['value']}" for i in reg.identifiers(b["id"]))
            print(f"#{b['id']} {b['name']} [{b['city'] or ''}]  {ids}\n    → {b['review_note']}")
        return
    bid = need(reg, a.ref)
    if a.same_as:
        dst = need(reg, a.same_as)
        reg.merge(bid, dst)
        reg.mark_reviewed(dst, f"merged #{bid}")
        print(f"#{bid} merged into #{dst}")
    elif a.distinct:
        reg.mark_reviewed(bid)
        print(f"#{bid} confirmed as a separate business")
    else:
        die("give --same-as <id> or --distinct")


def cmd_set_country(a):
    reg = open_registry()
    bid = need(reg, a.ref)
    reg.set_country(bid, a.country)
    print(f"{reg.label(bid)} country = {a.country.upper()}")


def cmd_gate(a):
    reg = open_registry()
    bid = need(reg, a.ref)
    pb = playbooks.load(a.playbook) if a.playbook != "geo" else None
    req = bool(pb) and pb["sample"].get("type") != "none" and pb["sample"].get("required", True)
    print(gate.can_contact(reg, bid, playbook=a.playbook, channel=a.channel, recipient=a.to or "", kind=a.kind,
                           parent_touch_id=a.parent, require_sample=req))


def cmd_show(a):
    reg = open_registry()
    geo_bridge.sync_ledger(reg)
    bid = need(reg, a.ref)
    b = reg.business(bid)
    print(f"{reg.label(bid)}  status={b['status']}  country={b['country']}  city={b['city']}  website={b['website']}")
    if b["needs_review"]:
        print(f"  ⚠️  needs review: {b['review_note']}")
    print("Identifiers: " + ", ".join(f"{i['kind']}={i['value']}" for i in reg.identifiers(bid)))
    for s in reg.suppression_hits(bid):
        print(f"  ⛔ {s}")
    for p in reg.q("SELECT * FROM prospects WHERE business_id=?", (bid,)):
        print(f"\n[{p['playbook']}] stage={p['stage']} priority={p['priority']}  {p['reason'] or ''}")
        for e in reg.q("SELECT * FROM evidence WHERE business_id=? AND playbook=? AND current=1 AND check_id!='_contacts' "
                       "ORDER BY id", (bid, p["playbook"])):
            print(f"  E{e['id']} {e['check_id']}: {e['status']} hit={e['hit']} ({e['method']}) {e['summary'][:160]}")
        contacts = reg.q1("SELECT summary FROM evidence WHERE business_id=? AND playbook=? AND check_id='_contacts' "
                          "AND current=1", (bid, p["playbook"]))
        if contacts:
            c = json.loads(contacts["summary"])
            print("  contacts: " + "; ".join(
                [e["email"] for e in c.get("emails", [])] + [s["url"] for s in c.get("socials", [])] +
                [f"form on {f['page']}" for f in c.get("contact_forms", [])]))
    opps = reg.q("SELECT * FROM opportunities WHERE business_id=?", (bid,))
    if opps:
        print("\nOpportunities:")
        for o in opps:
            print(f"  [{o['playbook']}] {o['basis']:10} {o['status']:8} {o['title']}")
    tch = reg.q("SELECT * FROM touches WHERE business_id=? ORDER BY id", (bid,))
    if tch:
        print("\nContact history:")
        for t in tch:
            print(f"  #{t['id']} {(t['sent_at'] or t['created_at'])[:10]} {t['state']:7} {t['playbook']}/{t['kind']} "
                  f"via {t['channel']} → {t['recipient'] or ''} ({t['source']})")
    ds = reg.q("SELECT id, playbook, status, channel FROM drafts WHERE business_id=? ORDER BY id", (bid,))
    if ds:
        print("\nDrafts: " + ", ".join(f"#{d['id']} {d['playbook']} {d['channel']} {d['status']}" for d in ds))


def cmd_run(a):
    """One command: search → check → qualify until --target clients qualify, then update the playbook's sheet."""
    reg = open_registry()
    pb = playbooks.load(a.playbook)
    b = discover.places_budget(reg.settings)
    print(f"Places budget this month: {b['geo'] + b['acq']}/{b['limit']} used (GEO {b['geo']}, acq {b['acq']}); "
          f"this run may use up to {a.max_requests}.")
    state = discover.run_auto(reg, pb, Fetcher(reg.settings), location=a.location, target=a.target,
                              max_requests=a.max_requests, max_checks=a.max_checks)
    print(f"\nQualified in this run: {len(state['qualified'])}/{a.target}  "
          f"(sites checked {state['checked']}, searches {state['requests']})")
    if state["stopped"] and len(state["qualified"]) < a.target:
        print(f"Stopped early: {state['stopped'][:300]}")
        if "403" in state["stopped"] or "PERMISSION_DENIED" in state["stopped"]:
            print("→ Google refused the Places search: the API key has no permission for 'Places API (New)'.\n"
                  "  Fix (owner of the Google Cloud project): enable 'Places API (New)' and allow it in the key's API\n"
                  "  restrictions. Until then: find rental management companies with web search and import their\n"
                  "  websites: acq find " + pb["id"] + " --urls <site1> <site2> ... --country US, then run this again.")
    print()
    cmd_list(argparse.Namespace(playbook=pb["id"], stage=None, limit=50))
    print()
    cmd_sheet(argparse.Namespace(playbook=pb["id"], include_rejected=False))


def cmd_sheet(a):
    import os
    import subprocess
    reg = open_registry()
    pb = playbooks.load(a.playbook)
    rows = sheets.rows_for(reg, pb, include_rejected=a.include_rejected)
    print(f"Sheet (CSV, {len(rows)} rows): {sheets.write_csv(reg, pb, rows)}")
    cfg = sheets.sheet_config(reg.settings, pb["id"])
    if not cfg["sheet_id"]:
        print("Google Sheet: not set up yet. Create an empty Google Sheet, share it with "
              "sheet-manager@geo-client-finder.iam.gserviceaccount.com as Editor, and put its link in "
              f"config/settings.json → sheets → {pb['id']} → sheet_id.")
        return
    try:
        import gspread  # noqa: F401
    except ImportError:
        py = reg.settings.get("gspread_python", "")
        if py and Path(py).exists() and not os.environ.get("ACQ_NO_REEXEC"):
            env = dict(os.environ, ACQ_NO_REEXEC="1")
            r = subprocess.run([py, "-B", str(Path(__file__).resolve()), "sheet", pb["id"]] +
                               (["--include-rejected"] if a.include_rejected else []), env=env, capture_output=True,
                               text=True, timeout=180)
            print("\n".join(l for l in r.stdout.splitlines() if l.startswith("Google Sheet")) or r.stderr[-500:])
            return
        print("Google Sheet: gspread not available (set gspread_python in settings.json)")
        return
    try:
        print(f"Google Sheet updated ({cfg['tab']} tab): {sheets.sync_google(reg, pb, rows)}")
    except Exception as e:
        print(f"Google Sheet: not updated ({type(e).__name__}: {str(e)[:300]})")


def cmd_list(a):
    reg = open_registry()
    geo_bridge.sync_ledger(reg)
    pb = playbooks.load(a.playbook)
    sql, params = "SELECT * FROM prospects WHERE playbook=?", [pb["id"]]
    if a.stage:
        sql += " AND stage=?"
        params.append(a.stage)
    rows = []
    for p in reg.q(sql + " ORDER BY priority DESC, updated_at DESC LIMIT ?", params + [a.limit]):
        ev = reg.current_evidence(p["business_id"], pb["id"])
        problems = [f"E{e['id']} " + re.sub(r"^(yes|no) \((.*)\)$", r"\2", e["summary"].split(": ", 1)[-1])[:50]
                    for cid, e in ev.items()
                    if cid != "_contacts" and e["hit"] == 1 and e["status"] == "OBSERVED"
                    and playbooks.check_by_id(pb, cid).get("problem")]
        drafts = reg.q("SELECT id, status FROM drafts WHERE business_id=? AND playbook=? ORDER BY id DESC LIMIT 1",
                       (p["business_id"], pb["id"]))
        sample = reg.latest_sample(p["business_id"], pb["id"])
        rows.append((reg.label(p["business_id"]), p["stage"], p["priority"], "; ".join(problems) or "-",
                     "yes" if sample else "-", f"#{drafts[0]['id']} {drafts[0]['status']}" if drafts else "-"))
    if not rows:
        print("No prospects" + (f" at stage {a.stage}" if a.stage else "") + ".")
        return
    table(rows, ["business", "stage", "prio", "observed problems (evidence)", "sample", "draft"])


def cmd_pdf(a):
    import shutil
    import subprocess
    src = Path(a.html).expanduser().resolve()
    if not src.is_file():
        die(f"{src} not found")
    out = Path(a.out).expanduser().resolve() if a.out else src.with_suffix(".pdf")
    chrome = next((c for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                               "/Applications/Chromium.app/Contents/MacOS/Chromium",
                               shutil.which("google-chrome") or "", shutil.which("chromium") or "") if c and Path(c).exists()),
                  None)
    if not chrome:
        die("Chrome/Chromium not found; open the HTML in a browser and use Print → Save as PDF")
    r = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--no-first-run",
                        f"--print-to-pdf={out}", src.as_uri()], capture_output=True, text=True, timeout=120)
    if not out.exists():
        die(f"PDF not created: {r.stderr[-400:]}")
    print(out)


def cmd_status(a):
    reg = open_registry()
    geo_bridge.sync_ledger(reg)
    s = reg.settings
    print(f"Registry: {data_paths(s)['db']}")
    print(f"Sending enabled: {s.get('sending_enabled')}   Businesses: {reg.q1('SELECT COUNT(*) n FROM businesses WHERE merged_into IS NULL')['n']}")
    rows = reg.q("SELECT playbook, stage, COUNT(*) n FROM prospects GROUP BY playbook, stage ORDER BY playbook, stage")
    if rows:
        table([(r["playbook"], r["stage"], r["n"]) for r in rows], ["playbook", "stage", "count"])
    t = reg.q("SELECT source, state, COUNT(*) n FROM touches GROUP BY source, state")
    print("Touches: " + (", ".join(f"{r['source']}/{r['state']}={r['n']}" for r in t) or "none"))
    pend = reg.q1("SELECT COUNT(*) n FROM touches WHERE state IN ('PENDING','UNKNOWN')")["n"]
    rev = reg.q1("SELECT COUNT(*) n FROM businesses WHERE needs_review=1 AND merged_into IS NULL")["n"]
    dr = reg.q("SELECT status, COUNT(*) n FROM drafts GROUP BY status")
    print(f"Unresolved sends: {pend}   Review queue: {rev}   Drafts: " +
          (", ".join(f"{r['status']}={r['n']}" for r in dr) or "none"))
    b = discover.places_budget(s)
    print(f"Places budget {b['geo'] + b['acq']}/{b['limit']} this month (GEO {b['geo']}, acq {b['acq']})")


def cmd_export(a):
    reg = open_registry()
    out = data_paths(reg.settings)["exports"] / "businesses.csv"
    rows = reg.q("""SELECT b.id, b.name, b.website, b.city, b.region, b.country, b.status, b.needs_review,
                    (SELECT group_concat(playbook || ':' || stage, ' | ') FROM prospects p WHERE p.business_id=b.id) prospects,
                    (SELECT MAX(sent_at) FROM touches t WHERE t.business_id=b.id AND t.state='SENT') last_contact,
                    (SELECT COUNT(*) FROM touches t WHERE t.business_id=b.id AND t.state='SENT') messages,
                    (SELECT group_concat(title, ' | ') FROM opportunities o WHERE o.business_id=b.id) opportunities
                    FROM businesses b WHERE b.merged_into IS NULL ORDER BY b.id""")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(rows[0].keys() if rows else ["id"])
        for r in rows:
            w.writerow(list(r))
    print(out)


# ------------------------------------------------------------------------------------------- parser
def build_parser():
    p = argparse.ArgumentParser(prog="acq", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)

    sp.add_parser("init", help="create the registry, import GEO history (read-only)").set_defaults(fn=cmd_init)
    s = sp.add_parser("import", help="import from GEO (read-only)")
    s.add_argument("source", choices=["geo"])
    s.add_argument("--sheet", action="store_true", help="also read the Google Sheet (run with the GEO venv python)")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_import)
    sp.add_parser("guard-geo", help="list GEO READY_TO_SEND rows the registry says must not be sent").set_defaults(fn=cmd_guard_geo)
    s = sp.add_parser("baseline", help="GEO protection checksums")
    s.add_argument("action", choices=["create", "verify"])
    s.set_defaults(fn=cmd_baseline)

    s = sp.add_parser("playbook", help="list / show / validate playbooks")
    s.add_argument("action", choices=["list", "show", "validate"])
    s.add_argument("ref", nargs="?")
    s.set_defaults(fn=cmd_playbook)

    s = sp.add_parser("find", help="discover candidates for a playbook")
    s.add_argument("playbook")
    s.add_argument("--location")
    s.add_argument("--query", help="override the playbook's queries")
    s.add_argument("--urls", nargs="*")
    s.add_argument("--urls-file")
    s.add_argument("--csv")
    s.add_argument("--country", help="country for URL/CSV input (default: playbook target.default_country)")
    s.add_argument("--max-pages", type=int, default=1, help="Places result pages per query (20 each)")
    s.add_argument("--show", type=int, default=40)
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_find)

    s = sp.add_parser("check", help="see the problem: run the playbook's checks")
    s.add_argument("playbook")
    s.add_argument("--business", nargs="*")
    s.add_argument("--limit", type=int, default=10)
    s.add_argument("--recheck", action="store_true", help="include needs_check prospects")
    s.add_argument("--force", action="store_true", help="also check skipped/contacted prospects")
    s.set_defaults(fn=cmd_check)

    s = sp.add_parser("evidence", help="record a manual finding (e.g. Meta Ad Library)")
    s.add_argument("action", choices=["add"])
    s.add_argument("ref")
    s.add_argument("--playbook", required=True)
    s.add_argument("--check", required=True)
    s.add_argument("--hit", choices=["yes", "no"], required=True)
    s.add_argument("--source-url")
    s.add_argument("--note", required=True)
    s.set_defaults(fn=cmd_evidence)

    s = sp.add_parser("qualify", help="re-evaluate a prospect from current evidence")
    s.add_argument("ref")
    s.add_argument("--playbook", required=True)
    s.set_defaults(fn=cmd_qualify)

    s = sp.add_parser("sample", help="prepare a sample brief / register the finished sample")
    s.add_argument("action", choices=["prepare", "register"])
    s.add_argument("ref")
    s.add_argument("--playbook", required=True)
    s.add_argument("--download-images", type=int, default=0)
    s.add_argument("--file")
    s.add_argument("--link")
    s.set_defaults(fn=cmd_sample)

    s = sp.add_parser("draft", help="create / list / show / reject drafts")
    s.add_argument("action", choices=["create", "list", "show", "reject"])
    s.add_argument("ref", nargs="?", help="business (create)")
    s.add_argument("--id", type=int)
    s.add_argument("--playbook")
    s.add_argument("--channel", default="email")
    s.add_argument("--to")
    s.add_argument("--subject")
    s.add_argument("--body")
    s.add_argument("--body-file")
    s.add_argument("--evidence", help="comma-separated evidence ids, e.g. 12,15")
    s.add_argument("--kind", choices=["pitch", "followup"], default="pitch")
    s.add_argument("--parent", type=int)
    s.add_argument("--recipient-source")
    s.add_argument("--status")
    s.set_defaults(fn=cmd_draft)

    s = sp.add_parser("approve", help="HUMAN approval (native dialog)")
    s.add_argument("ids", nargs="+", type=int)
    s.set_defaults(fn=cmd_approve)

    s = sp.add_parser("send", help="send an approved draft (dry-run unless --live)")
    s.add_argument("id", type=int)
    s.add_argument("--live", action="store_true")
    s.set_defaults(fn=cmd_send)

    s = sp.add_parser("touch", help="list touches / resolve an unresolved send")
    s.add_argument("action", choices=["list", "resolve"])
    s.add_argument("id", nargs="?", type=int)
    s.add_argument("--pending", action="store_true")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--sent", action="store_true")
    g.add_argument("--failed", action="store_true")
    g.add_argument("--unknown", action="store_true")
    s.add_argument("--message-id")
    s.set_defaults(fn=cmd_touch)

    s = sp.add_parser("followups", help="acq pitches and whether a follow-up is allowed")
    s.add_argument("--playbook")
    s.set_defaults(fn=cmd_followups)

    s = sp.add_parser("outcome", help="record a reply / opt-out / result")
    s.add_argument("ref")
    s.add_argument("outcome", choices=sorted(OUTCOMES))
    s.add_argument("--note")
    s.add_argument("--email")
    s.set_defaults(fn=cmd_outcome)

    s = sp.add_parser("suppress", help="do-not-contact entry")
    s.add_argument("value")
    s.add_argument("--kind", choices=["business", "domain", "email", "phone"], required=True)
    s.add_argument("--reason", required=True)
    s.set_defaults(fn=cmd_suppress)

    s = sp.add_parser("review", help="duplicate review queue")
    s.add_argument("action", choices=["list", "resolve"])
    s.add_argument("ref", nargs="?")
    s.add_argument("--same-as")
    s.add_argument("--distinct", action="store_true")
    s.set_defaults(fn=cmd_review)

    s = sp.add_parser("set-country")
    s.add_argument("ref")
    s.add_argument("country")
    s.set_defaults(fn=cmd_set_country)

    s = sp.add_parser("gate", help="ask the gate whether a business may be contacted")
    s.add_argument("ref")
    s.add_argument("--playbook", required=True)
    s.add_argument("--channel", default="email")
    s.add_argument("--to")
    s.add_argument("--kind", default="pitch", choices=["pitch", "followup"])
    s.add_argument("--parent", type=int)
    s.set_defaults(fn=cmd_gate)

    s = sp.add_parser("show", help="everything known about one business")
    s.add_argument("ref")
    s.set_defaults(fn=cmd_show)
    sp.add_parser("status", help="pipeline overview").set_defaults(fn=cmd_status)
    s = sp.add_parser("list", help="prospects of one playbook with their observed problems")
    s.add_argument("playbook")
    s.add_argument("--stage")
    s.add_argument("--limit", type=int, default=50)
    s.set_defaults(fn=cmd_list)
    s = sp.add_parser("run", help="ONE COMMAND: find + check until N clients qualify, then update the sheet")
    s.add_argument("playbook")
    s.add_argument("--location", help="e.g. 'Gatlinburg, TN' (default: the playbook's default_locations in order)")
    s.add_argument("--target", type=int, default=5)
    s.add_argument("--max-requests", type=int, default=8, help="Places searches this run may use")
    s.add_argument("--max-checks", type=int, default=25, help="websites this run may check")
    s.set_defaults(fn=cmd_run)
    s = sp.add_parser("sheet", help="write the playbook's client sheet (CSV + its own Google Sheet if set up)")
    s.add_argument("playbook")
    s.add_argument("--include-rejected", action="store_true")
    s.set_defaults(fn=cmd_sheet)
    s = sp.add_parser("pdf", help="render an HTML sample to PDF with local headless Chrome")
    s.add_argument("html")
    s.add_argument("--out")
    s.set_defaults(fn=cmd_pdf)
    sp.add_parser("export", help="CSV export of the registry").set_defaults(fn=cmd_export)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.cmd == "draft" and args.action in ("show", "reject") and args.id is None:
        args.id = int(args.ref) if args.ref and args.ref.isdigit() else die("give --id <draft id>")
    if args.cmd == "draft" and args.action == "create":
        for req in ("ref", "playbook", "to"):
            if not getattr(args, req):
                die(f"draft create needs {'a business' if req == 'ref' else '--' + req}")
    if args.cmd == "touch" and args.action == "resolve" and (args.id is None or not (args.sent or args.failed or args.unknown)):
        die("touch resolve <id> --sent|--failed|--unknown")
    args.fn(args)


if __name__ == "__main__":
    main()
