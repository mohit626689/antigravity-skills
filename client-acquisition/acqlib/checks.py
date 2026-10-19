"""See the problem: crawl a few pages of the business's own site, run the playbook's checks, record evidence.

Evidence rules:
  * Something FOUND is OBSERVED (with the page it was found on).
  * Something NOT found is OBSERVED only for the pages actually checked, and only when the raw HTML is
    trustworthy. On JavaScript-rendered pages it is UNVERIFIED (hit unknown): a human must confirm in a browser.
  * If the homepage is not a usable HTML page, nothing is checked and the prospect is rejected. No outreach.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from . import identity, web
from .config import data_paths

SKIP_EXT = re.compile(r"\.(pdf|jpe?g|png|gif|webp|svg|zip|mp4|mov|docx?|xlsx?)$", re.I)
DEFAULT_KEYWORDS = r"about|contact|gallery|photos|services|book|appointment|tour|portfolio"


def _sel_match(tag, attrs, sel) -> bool:
    if sel.get("tag") not in ("*", tag):
        return False
    attr = sel.get("attr")
    if not attr:
        return True
    val = attrs.get(attr.lower())
    if val is None:
        return False
    pattern = sel.get("pattern")
    return True if not pattern else bool(re.search(pattern, val, re.I))


def _describe(tag, attrs) -> str:
    keys = [k for k in ("src", "href", "property", "name", "type", "content") if attrs.get(k)]
    inner = " ".join(f'{k}="{attrs[k][:90]}"' for k in keys[:2])
    return f"<{tag}{' ' + inner if inner else ''}>"


def _path(url) -> str:
    p = urlsplit(url)
    return (p.path or "/") + (f"?{p.query}" if p.query else "")


def is_detail_page(playbook: dict, url: str, parsed) -> bool:
    """A single-property page (per playbook.detail_page), not a category/search page listing many properties."""
    spec = playbook.get("detail_page")
    if not spec:
        return False
    if not re.search(spec["path_pattern"], _path(url), re.I):
        return False
    if spec.get("text_pattern") and not re.search(spec["text_pattern"], parsed.text, re.I):
        return False
    if spec.get("max_property_links") is not None:
        targets = {h.split("#")[0].rstrip("/") for h, _ in parsed.links
                   if re.search(spec["path_pattern"], urlsplit(h).path, re.I)}
        targets.discard(url.split("#")[0].rstrip("/"))
        if len(targets) > spec["max_property_links"]:
            return False
    return True


def crawl(fetcher: web.Fetcher, website: str, playbook: dict):
    cfg = playbook.get("crawl", {})
    max_pages = max(1, int(cfg.get("max_pages", 5)))
    kw = re.compile(cfg.get("page_keywords") or DEFAULT_KEYWORDS, re.I)
    start = website if "://" in website else "https://" + website
    home = fetcher.fetch(start)
    if home.error and start.startswith("https://") and not home.status:
        home = fetcher.fetch("http://" + start[len("https://"):])
    pages = [(home, web.parse(home))]
    if not home.ok:
        return pages
    domain = identity.registrable_domain(home.final_url)

    def key(u):  # www./no-www, trailing slash and fragments are the same page
        sp = urlsplit(u)
        return identity.host_of(u) + ((sp.path or "/").rstrip("/") or "/") + (f"?{sp.query}" if sp.query else "")

    seen = {key(home.final_url), key(start)}
    prio = re.compile(cfg["priority_pattern"], re.I) if cfg.get("priority_pattern") else None
    first, rest = [], []
    for href, text in pages[0][1].links:
        if not href.startswith("http") or not web.same_site(href, domain) or SKIP_EXT.search(urlsplit(href).path):
            continue
        k = key(href)
        if k in seen:
            continue
        if prio and prio.search(urlsplit(href).path):
            seen.add(k)
            first.append(href)
        elif kw.search(urlsplit(href).path) or kw.search(text or ""):
            seen.add(k)
            rest.append(href)
    # detail pages the playbook cares about first (leaving room for contact/about pages), then the rest
    hop_reserve = 2 if playbook.get("detail_page") else 0
    budget = max_pages - hop_reserve
    n_first = min(len(first), max(1, budget - 3)) if rest else len(first)
    for href in first[:n_first] + rest + first[n_first:]:
        if len(pages) >= budget:
            break
        pg = fetcher.fetch(href)
        pages.append((pg, web.parse(pg)))
    fetched = {key(pg.url) for pg, _ in pages}
    have_detail = any(pg.ok and is_detail_page(playbook, pg.final_url, ps) for pg, ps in pages)
    if hop_reserve and have_detail:  # already on property pages: spend the reserve on more of them
        for href in [h for h in first if key(h) not in fetched][:hop_reserve]:
            pg = fetcher.fetch(href)
            pages.append((pg, web.parse(pg)))
    # second hop: category pages usually link to the single-property pages the checks need
    elif hop_reserve:
        path_re = re.compile(playbook["detail_page"]["path_pattern"], re.I)
        deeper = []
        for pg, ps in pages[1:]:
            for href, _ in ps.links:
                if (href.startswith("http") and web.same_site(href, domain) and path_re.search(urlsplit(href).path)
                        and key(href) not in seen):
                    seen.add(key(href))
                    deeper.append(href)
        deeper.sort(key=lambda h: -len([x for x in urlsplit(h).path.split("/") if x]))  # deepest paths first
        for href in deeper[:hop_reserve]:
            pg = fetcher.fetch(href)
            pages.append((pg, web.parse(pg)))
    return pages


def _jsonld_types(parsed) -> set:
    types = set()
    for raw in parsed.jsonld:
        types.update(re.findall(r'"@type"\s*:\s*"([A-Za-z]+)"', raw))
        for group in re.findall(r'"@type"\s*:\s*\[([^\]]*)\]', raw):
            types.update(re.findall(r'"([A-Za-z]+)"', group))
    return types


def evaluate(playbook: dict, pages, today: str = None):
    """Pure function: pages -> (qa, results). No network, no database."""
    today = today or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    home, _ = pages[0]
    ok = [(pg, ps) for pg, ps in pages if pg.ok]
    shells = [pg.final_url for pg, ps in ok if web.is_js_shell(ps)]
    qa = {
        "homepage_ok": home.ok,
        "homepage_status": home.status,
        "final_url": home.final_url or home.url,
        "pages": [{"url": pg.final_url or pg.url, "status": pg.status, "ok": pg.ok, "error": pg.error,
                   "js_rendered": pg.ok and web.is_js_shell(ps)} for pg, ps in pages],
        "pages_ok": len(ok),
        "js_rendered_pages": shells,
        "failed": None,
    }
    if not home.ok:
        why = home.error or f"status {home.status}, content-type '{home.content_type}'"
        qa["failed"] = f"homepage not usable: {why}"
        qa["transient"] = home.status in (408, 425, 429, 500, 502, 503, 504) or "timed out" in (home.error or "").lower() \
            or "timeout" in (home.error or "").lower()
    scope_paths = ", ".join(_path(pg.final_url) for pg, _ in ok) or "none"
    scope = f"{len(ok)} page(s) checked on {today} ({scope_paths})"

    results = []
    for c in playbook["checks"]:
        base = {"check_id": c["id"], "label": c["label"], "type": c["type"], "problem": c.get("problem"),
                "found": []}
        if c["type"] == "manual":
            results.append({**base, "status": "NOT_CHECKED", "hit": None,
                            "summary": f"Manual check, not done yet: {c['instructions']}"})
            continue
        if c["type"] == "contact_available":
            continue  # derived from known contacts at qualify time
        if qa["failed"]:
            results.append({**base, "status": "NOT_CHECKED", "hit": None, "summary": f"Not checked: {qa['failed']}"})
            continue

        page_pattern = c.get("page_pattern")
        if c.get("pages") == "detail":
            cpages = [(pg, ps) for pg, ps in ok if is_detail_page(playbook, pg.final_url, ps)]
            what = "single-property page"
        elif page_pattern:
            cpages = [(pg, ps) for pg, ps in ok if re.search(page_pattern, _path(pg.final_url), re.I)]
            what = f"page matching {page_pattern!r}"
        else:
            cpages, what = ok, "page"
        if not cpages:
            results.append({**base, "status": "NOT_CHECKED", "hit": None,
                            "summary": f"{c['label']}: no {what} among the checked pages"})
            continue
        c_shells = [pg.final_url for pg, ps in cpages if web.is_js_shell(ps)]
        noun = "property page(s)" if c.get("pages") == "detail" else "page(s)"
        c_scope = (f"{len(cpages)} {noun} checked on {today} ({', '.join(_path(pg.final_url) for pg, _ in cpages)})"
                   if (page_pattern or c.get("pages") == "detail") else scope)
        found = []
        t = c["type"]
        if t == "element":
            for pg, ps in cpages:
                for tag, attrs in ps.elements:
                    if any(_sel_match(tag, attrs, s) for s in c["match"]):
                        found.append((pg.final_url, _describe(tag, attrs)))
        elif t == "link":
            tp = c.get("text_pattern")
            for pg, ps in cpages:
                for href, text in ps.links:
                    if re.search(c["pattern"], href, re.I) or (tp and re.search(tp, text or "", re.I)):
                        found.append((pg.final_url, href[:140]))
        elif t == "text":
            for pg, ps in cpages:
                m = re.search(c["pattern"], ps.text, re.I)
                if m:
                    a, b = max(0, m.start() - 60), min(len(ps.text), m.end() + 60)
                    found.append((pg.final_url, "…" + ps.text[a:b] + "…"))
        elif t == "jsonld_type":
            wanted = set(c["types"])
            for pg, ps in cpages:
                hit_types = _jsonld_types(ps) & wanted
                if hit_types:
                    found.append((pg.final_url, "JSON-LD @type " + ", ".join(sorted(hit_types))))
        elif t == "https":
            if (home.final_url or "").startswith("https://"):
                found.append((home.final_url, "served over HTTPS"))
        elif t == "count":
            excl = re.compile(c["exclude_pattern"], re.I) if c.get("exclude_pattern") else None
            per_page = []
            for pg, ps in cpages:
                if c.get("source") == "images":
                    items = [(u, u) for u in ps.images]
                else:
                    items = [(attrs.get(c.get("unique_attr", "src"), "") or f"{pg.final_url}#{i}", _describe(tag, attrs))
                             for i, (tag, attrs) in enumerate(ps.elements)
                             if any(_sel_match(tag, attrs, s) for s in c["match"])]
                page_vals = []
                for key, desc in items:
                    if excl and excl.search(key):
                        continue
                    if key not in {v[0] for v in page_vals}:
                        page_vals.append((key, desc, pg.final_url))
                per_page.append((pg.final_url, page_vals))
            agg = c.get("aggregate", "sum")
            if agg in ("min", "max") and per_page:
                pick = (min if agg == "min" else max)(per_page, key=lambda x: len(x[1]))
                values = pick[1]
                c_scope = f"{_path(pick[0])} ({agg} of {len(per_page)} matching page(s), checked on {today})"
            else:
                values = []
                for _, page_vals in per_page:
                    for v in page_vals:
                        if v[0] not in {x[0] for x in values}:
                            values.append(v)
            n = len(values)
            mn, mx = c.get("min"), c.get("max")
            hit = (mn is None or n >= mn) and (mx is None or n <= mx)
            cond = " and ".join(x for x in (f"≥ {mn}" if mn is not None else "", f"≤ {mx}" if mx is not None else "") if x)
            summary = f"{n} counted ({cond} needed) across {c_scope}"
            if c_shells and not (hit and mx is None):
                # a low count on a JavaScript-rendered page proves nothing
                results.append({**base, "status": "UNVERIFIED", "hit": None, "value": n,
                                "summary": summary + "; some pages render with JavaScript, so the count may be low. "
                                           "Confirm in a browser."})
            else:
                results.append({**base, "status": "OBSERVED", "hit": hit, "value": n, "summary": summary,
                                "found": [(v[2], v[1]) for v in values[:5]]})
            continue

        present = bool(found)
        hit_if = c.get("hit_if", "present")
        hit = present if hit_if == "present" else not present
        if present:
            first = "; ".join(f"{_path(u)}: {d}" for u, d in found[:2])
            results.append({**base, "status": "OBSERVED", "hit": hit, "found": found[:5],
                            "summary": f"{c['label']}: found ({first})"})
        elif c_shells:
            results.append({**base, "status": "UNVERIFIED", "hit": None,
                            "summary": f"{c['label']}: not found in raw HTML of {c_scope}, but these pages render with "
                                       f"JavaScript ({', '.join(_path(u) for u in c_shells)}). Confirm in a browser."})
        else:
            results.append({**base, "status": "OBSERVED", "hit": hit,
                            "summary": f"{c['label']}: not found on the {c_scope}. Scope: these pages only."})
    return qa, results


def qualify(reg, bid: int, playbook: dict, qa_failed: str = None) -> tuple:
    """Decide the prospect stage from current evidence (auto + manual). Returns (stage, reason, priority)."""
    pid = playbook["id"]
    _derive_contact_checks(reg, bid, playbook)
    ev = reg.current_evidence(bid, pid)
    rules = playbook["qualify"]
    failed, unknown = [], []
    for cid in rules.get("all_of", []):
        e = ev.get(cid)
        if not e or e["hit"] is None or e["status"] != "OBSERVED":
            unknown.append(cid)
        elif not e["hit"]:
            failed.append(f"{cid}: {e['summary']}")
    from .playbooks import any_of_groups
    manual_ids = {c["id"] for c in playbook["checks"] if c["type"] == "manual"}
    clean = lambda e: e is not None and e["status"] == "OBSERVED" and e["hit"] == 0
    for group in any_of_groups(playbook):
        states = {cid: ev.get(cid) for cid in group}
        if any(e and e["status"] == "OBSERVED" and e["hit"] == 1 for e in states.values()):
            continue
        auto = [cid for cid in group if cid not in manual_ids]
        if all(clean(e) for e in states.values()):
            failed.append("none of " + ", ".join(group) + " observed")
        elif auto and all(clean(states[cid]) for cid in auto):
            pending = [cid for cid in group if cid in manual_ids and not clean(states[cid])]
            failed.append("nothing found automatically (" + ", ".join(auto) + "); record "
                          + "/".join(pending) + " observations to reconsider")
        else:
            unknown.append("one of " + "/".join(group))
    priority = sum(1 for cid in rules.get("signals", [])
                   if ev.get(cid) and ev[cid]["hit"] == 1 and ev[cid]["status"] == "OBSERVED")
    if qa_failed and qa_failed.startswith("temporary:"):
        stage, reason = "needs_check", qa_failed + " (run `acq check <playbook> --recheck` later)"
    elif qa_failed:
        stage, reason = "rejected", qa_failed
    elif failed:
        stage, reason = "rejected", "; ".join(failed)
    elif unknown:
        stage, reason = "needs_check", ("not verified yet: " + ", ".join(unknown) +
                                        " (check in a browser, then `acq evidence add`)")
    else:
        stage, reason = "qualified", "all required checks observed"

    current = reg.prospect(bid, pid)
    cur_stage = current["stage"] if current else None
    if cur_stage == "contacted" or (stage == "qualified" and cur_stage in ("sample_ready", "drafted")):
        reg.set_stage(bid, pid, cur_stage, reason, priority)
        stage = cur_stage
    else:
        reg.set_stage(bid, pid, stage, reason, priority)

    if stage in ("qualified", "sample_ready", "drafted"):
        for c in playbook["checks"]:
            e = ev.get(c["id"])
            if c.get("problem") and e and e["hit"] == 1 and e["status"] == "OBSERVED":
                reg.add_opportunity(bid, pid, c["problem"], "OBSERVED", e["id"])
        for h in playbook.get("hypotheses", []):
            reg.add_opportunity(bid, pid, h, "HYPOTHESIS")
    return stage, reason, priority


def check_business(reg, fetcher, playbook: dict, bid: int) -> dict:
    pid = playbook["id"]
    b = reg.business(bid)
    website = b["website"] or reg.primary_domain(bid)
    if not website or identity.is_platform(website):
        # Nothing to crawl (e.g. a host known only from Airbnb). Decide from manual evidence and known contacts.
        stage, reason, priority = qualify(reg, bid, playbook)
        return {"business": bid, "stage": stage, "reason": reason + " (no own website: page checks skipped)",
                "priority": priority}

    pages = crawl(fetcher, website, playbook)
    qa, results = evaluate(playbook, pages)
    domain = identity.registrable_domain(qa["final_url"]) or reg.primary_domain(bid)
    contacts = web.extract_contacts([(pg.final_url, ps) for pg, ps in pages if pg.ok], domain, reg.policy)
    images = []
    for pg, ps in pages:
        if pg.ok:
            for u in ps.images:
                if u not in images:
                    images.append(u)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = data_paths(reg.settings)["evidence"] / (domain or f"business-{bid}") / pid
    run_dir.mkdir(parents=True, exist_ok=True)
    run_file = run_dir / f"run-{stamp}.json"
    run_file.write_text(json.dumps({
        "business_id": bid, "business": b["name"], "playbook": pid, "playbook_version": playbook.get("version"),
        "checked_at": stamp, "qa": qa, "results": results, "contacts": contacts, "images": images[:80],
    }, indent=1, ensure_ascii=False))

    for r in results:
        if r["type"] in ("manual", "contact_available"):
            continue  # never overwrite a human's recorded finding; contact checks are derived
        src = r["found"][0][0] if r.get("found") else qa["final_url"]
        reg.add_evidence(bid, pid, r["check_id"], r["status"], r["hit"], r["summary"], source_url=src,
                         run_file=str(run_file))
    if not qa["failed"]:
        merge_contacts(reg, bid, pid, contacts, source_url=qa["final_url"], run_file=str(run_file))
    for e in contacts["emails"]:
        if e["on_business_domain"]:
            reg._add_identifier(bid, "email", e["email"], f"site:{pid}")

    failed = qa["failed"]
    if failed and qa.get("transient"):
        failed = f"temporary: {failed}"
    stage, reason, priority = qualify(reg, bid, playbook, failed)
    return {"business": bid, "stage": stage, "reason": reason, "priority": priority, "run_file": str(run_file),
            "results": results, "contacts": contacts}


def merge_contacts(reg, bid: int, pid: str, new: dict, *, source_url=None, run_file=None):
    """Union of already-known contacts (site crawl, CSV research) and new ones, stored as the `_contacts` evidence."""
    row = reg.q1("SELECT summary FROM evidence WHERE business_id=? AND playbook=? AND check_id='_contacts' AND current=1",
                 (bid, pid))
    old = json.loads(row["summary"]) if row else {}
    merged = {}
    for key, ident in (("emails", "email"), ("phones", "phone"), ("socials", "url"), ("contact_forms", "page")):
        seen, items = set(), []
        for item in old.get(key, []) + new.get(key, []):
            k = (item.get(ident) or "").lower()
            if k and k not in seen and not identity.automation_forbidden(k):
                seen.add(k)
                items.append(item)
        merged[key] = items
    reg.add_evidence(bid, pid, "_contacts", "OBSERVED", None, json.dumps(merged), source_url=source_url,
                     run_file=run_file)
    return merged


def _derive_contact_checks(reg, bid: int, playbook: dict):
    """contact_available checks: true when the business has a usable channel of its own (never Airbnb messaging)."""
    pid = playbook["id"]
    derived = [c for c in playbook["checks"] if c["type"] == "contact_available"]
    if not derived:
        return
    row = reg.q1("SELECT summary, source_url FROM evidence WHERE business_id=? AND playbook=? AND check_id='_contacts' "
                 "AND current=1", (bid, pid))
    ev = reg.current_evidence(bid, pid)
    for c in derived:
        if not row:
            status, hit, summary, src = "NOT_CHECKED", None, "No contact information collected yet", None
        else:
            cont = json.loads(row["summary"])
            channels = ([e["email"] for e in cont.get("emails", [])] + [s["url"] for s in cont.get("socials", [])] +
                        [f["page"] for f in cont.get("contact_forms", [])])
            status = "OBSERVED"
            hit = bool(channels)
            summary = (f"Business contact channel(s): {', '.join(channels[:4])}" if hit else
                       "No business contact channel found (platform messaging is not an allowed channel)")
            src = (cont.get("emails") or cont.get("socials") or cont.get("contact_forms") or [{}])[0].get("page") \
                or row["source_url"]
        cur = ev.get(c["id"])
        if cur and cur["summary"] == summary and cur["status"] == status:
            continue
        reg.add_evidence(bid, pid, c["id"], status, hit, summary, source_url=src)


def latest_run(reg, bid: int, pid: str):
    row = reg.q1("SELECT run_file FROM evidence WHERE business_id=? AND playbook=? AND run_file IS NOT NULL "
                 "ORDER BY id DESC LIMIT 1", (bid, pid))
    if row and row["run_file"] and Path(row["run_file"]).exists():
        return json.loads(Path(row["run_file"]).read_text())
    return None
