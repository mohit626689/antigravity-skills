"""Find candidates: Google Places Text Search (shared free-tier budget with GEO), a URL list, or a CSV you collected.

Every candidate goes through the registry: duplicates collapse onto one business, and businesses that were already
contacted, suppressed or need review are recorded as 'skipped' instead of being worked again.
"""
from __future__ import annotations

import csv
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from . import identity
from .config import data_paths, load_env

PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
PLACES_FIELDS = ",".join([
    "places.id", "places.displayName", "places.rating", "places.userRatingCount", "places.websiteUri",
    "places.internationalPhoneNumber", "places.googleMapsUri", "places.businessStatus", "places.addressComponents",
    "nextPageToken",
])


# ------------------------------------------------------------------ Places budget (shared with GEO)
def _month() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def _read_usage(path) -> int:
    try:
        d = json.loads(Path(path).read_text())
        return int(d.get("requests", 0)) if d.get("month") == _month() else 0
    except Exception:
        return 0


def places_budget(settings) -> dict:
    own = data_paths(settings)["places_usage"]
    geo = settings.get("geo", {}).get("places_usage", "")
    used_acq, used_geo = _read_usage(own), (_read_usage(geo) if geo else 0)
    limit = int(settings.get("places_monthly_limit_combined", 900))
    return {"acq": used_acq, "geo": used_geo, "limit": limit, "remaining": max(0, limit - used_acq - used_geo)}


def _count_request(settings):
    own = data_paths(settings)["places_usage"]
    n = _read_usage(own) + 1
    own.parent.mkdir(parents=True, exist_ok=True)
    own.write_text(json.dumps({"month": _month(), "requests": n}))


def places_search(settings, query: str, max_pages: int = 2):
    key = load_env(settings).get("GOOGLE_PLACES_API_KEY")
    if not key:
        raise RuntimeError("GOOGLE_PLACES_API_KEY not found in env_files or environment")
    token, out = None, []
    for _ in range(max_pages):
        if places_budget(settings)["remaining"] <= 0:
            raise RuntimeError("monthly Places budget (GEO + acq) used up; stopping to avoid charges")
        body = {"textQuery": query, "pageSize": 20}
        if token:
            body["pageToken"] = token
        req = urllib.request.Request(PLACES_URL, data=json.dumps(body).encode(), method="POST", headers={
            "Content-Type": "application/json", "X-Goog-Api-Key": key, "X-Goog-FieldMask": PLACES_FIELDS})
        _count_request(settings)  # count before the call: a failed call may still be billed
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Places API HTTP {e.code}: {e.read()[:300].decode(errors='replace')}") from e
        out.extend(data.get("places", []))
        token = data.get("nextPageToken")
        if not token:
            break
    return out


def _component(place, kind, short=False):
    for c in place.get("addressComponents", []):
        if kind in c.get("types", []):
            return c.get("shortText" if short else "longText")
    return None


def from_place(p) -> dict:
    return {
        "name": (p.get("displayName") or {}).get("text", ""),
        "website": p.get("websiteUri"),
        "phone": p.get("internationalPhoneNumber"),
        "place_id": p.get("id"),
        "maps_url": p.get("googleMapsUri"),
        "rating": p.get("rating"),
        "reviews": p.get("userRatingCount"),
        "business_status": p.get("businessStatus"),
        "city": _component(p, "locality") or _component(p, "postal_town"),
        "region": _component(p, "administrative_area_level_1", short=True),
        "country": _component(p, "country", short=True),
        "source_url": p.get("googleMapsUri"),
    }


def passes_filters(c: dict, filters: dict) -> tuple:
    f = filters or {}
    if c.get("business_status") and c["business_status"] != "OPERATIONAL":
        return False, f"status {c['business_status']}"
    if f.get("require_website", True) and not c.get("website"):
        return False, "no website"
    r, n = c.get("rating"), c.get("reviews")
    if f.get("rating_min") is not None and (r is None or r < f["rating_min"]):
        return False, f"rating {r} < {f['rating_min']}"
    if f.get("rating_max") is not None and (r is None or r > f["rating_max"]):
        return False, f"rating {r} > {f['rating_max']}"
    if f.get("reviews_min") is not None and (n is None or n < f["reviews_min"]):
        return False, f"reviews {n} < {f['reviews_min']}"
    if f.get("reviews_max") is not None and (n is None or n > f["reviews_max"]):
        return False, f"reviews {n} > {f['reviews_max']}"
    if f.get("exclude_name_pattern") and re.search(f["exclude_name_pattern"], c.get("name", ""), re.I):
        return False, "excluded by name pattern"
    return True, ""


# ------------------------------------------------------------------ other sources
def from_urls(urls, country=None) -> list:
    out = []
    for u in urls:
        u = u.strip()
        if not u or u.startswith("#"):
            continue
        if identity.is_platform(u):  # a listing/profile link: identity only, never crawled
            out.append({"name": "", "website": "", "profiles": [u], "country": country, "source_url": u})
        else:
            out.append({"name": "", "website": u, "country": country, "source_url": u})
    return out


YES = {"yes", "y", "true", "1", "x"}
NO = {"no", "n", "false", "0"}
SPLIT = re.compile(r"[;|\s]+")


def _norm_key(k: str) -> str:
    return re.sub(r"[\s\-]+", "_", (k or "").strip().lower())


def from_csv(path, country=None) -> list:
    """Rows you collected yourself. Recognised columns (any order, extra columns ignored):

    company | name, website, host_profile_url, listing_urls (separated by ; or |), email, email_source, phone,
    instagram, facebook, linkedin, contact_form, city, state, country, source_url,
    and per manual check of the playbook: check_<id> (yes/no), note_<id> (what you saw), source_<id> (page URL).
    """
    out = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            r = {_norm_key(k): (v or "").strip() for k, v in row.items() if k}
            host = r.get("host_profile_url") or r.get("host_url") or r.get("profile") or ""
            listings = [u for u in SPLIT.split(r.get("listing_urls", "")) if u.startswith("http")]
            socials = {n: r.get(n) for n in ("instagram", "facebook", "linkedin") if r.get(n)}
            website = r.get("website") or r.get("url") or ""
            if not (website or host or listings):
                continue
            first_ref = (listings[:1] or [host or website or r.get("source_url", "")])[0]
            evidence = {}
            for k, v in r.items():
                if k.startswith("check_") and v.lower() in YES | NO:
                    cid = k[len("check_"):]
                    evidence[cid] = {"hit": v.lower() in YES, "note": r.get(f"note_{cid}", ""),
                                     "source": r.get(f"source_{cid}") or first_ref}
            email_src = r.get("email_source") or r.get("source_url") or website
            contacts = {
                "emails": ([{"email": r["email"].lower(), "page": email_src, "how": "csv"}]
                           if r.get("email") and email_src else []),
                "socials": [{"network": n, "url": u, "page": u} for n, u in socials.items()],
                "contact_forms": [{"page": r["contact_form"], "fields": 0}] if r.get("contact_form") else [],
                "phones": [],
            }
            out.append({
                "name": r.get("company") or r.get("business_name") or r.get("name") or "",
                "website": website, "profiles": [host, *listings, *socials.values()],
                "phone": r.get("phone"), "emails": [r["email"]] if r.get("email") else [],
                "city": r.get("city"), "region": r.get("region") or r.get("state"),
                "country": r.get("country") or country, "source_url": r.get("source_url") or host or website,
                "evidence": evidence, "contacts": contacts,
            })
    return out


def apply_research(reg, playbook: dict, bid: int, c: dict):
    """Store your recorded observations (manual checks) and contacts for a business, then re-qualify it."""
    from . import checks

    pid = playbook["id"]
    manual = {ch["id"]: ch for ch in playbook["checks"] if ch["type"] == "manual"}
    for cid, ev in (c.get("evidence") or {}).items():
        if cid not in manual:
            continue
        status = "OBSERVED" if ev.get("source") else "HYPOTHESIS"
        summary = f"{manual[cid]['label']}: {'yes' if ev['hit'] else 'no'}" + (f" ({ev['note']})" if ev.get("note") else "")
        reg.add_evidence(bid, pid, cid, status, ev["hit"], summary, source_url=ev.get("source") or None, method="manual")
    if any((c.get("contacts") or {}).values()):
        checks.merge_contacts(reg, bid, pid, c["contacts"], source_url=c.get("source_url"))
    elif not c.get("website") and not reg.business(bid)["website"]:
        # nothing of their own to contact and no site to look at: record "no channel" so the prospect is rejected
        # (do not go looking for a private person's contact details)
        checks.merge_contacts(reg, bid, pid, {}, source_url=c.get("source_url"))
    return checks.qualify(reg, bid, playbook)


# ------------------------------------------------------------------ ingest
def ingest(reg, playbook: dict, candidates: list, source: str, dry_run: bool = False) -> dict:
    from . import geo_bridge

    geo_bridge.sync_ledger(reg)  # GEO sends must be known before deciding who is "new"
    pid = playbook["id"]
    stats = {"seen": 0, "new_prospects": 0, "already_in_playbook": 0, "skipped_known": 0, "filtered": 0,
             "review": 0, "rows": []}
    filters = playbook.get("discovery", {}).get("filters", {})
    if source != "google_places":  # your own lists: only the name exclusions apply
        filters = {"require_website": False, "exclude_name_pattern": filters.get("exclude_name_pattern")}
    for c in candidates:
        stats["seen"] += 1
        ok, why = passes_filters(c, filters) if filters else (True, "")
        if not ok:
            stats["filtered"] += 1
            stats["rows"].append((c.get("name") or c.get("website"), "filtered", why))
            continue
        if dry_run:
            known = reg.find(c.get("website") or "") if c.get("website") else None
            stats["rows"].append((c.get("name") or c.get("website"), "would add", f"known as #{known}" if known else ""))
            continue
        bid, how = reg.upsert_business(name=c.get("name"), website=c.get("website") or None, phone=c.get("phone"),
                                       emails=c.get("emails", []), place_id=c.get("place_id"),
                                       maps_url=c.get("maps_url"), city=c.get("city"), region=c.get("region"),
                                       country=c.get("country"), source=f"{source}:{pid}",
                                       profiles=[u for u in c.get("profiles", []) if u])
        if how in ("review", "conflict"):
            stats["review"] += 1
        prior = reg.prospect(bid, pid)
        if prior:
            stats["already_in_playbook"] += 1
            note = prior["stage"]
            if (c.get("evidence") or c.get("contacts")) and prior["stage"] not in ("skipped", "contacted"):
                stage, reason, _ = apply_research(reg, playbook, bid, c)
                note = f"updated → {stage}: {reason}"
            stats["rows"].append((reg.label(bid), "already in playbook", note))
            continue
        touched = reg.q("SELECT playbook, channel, sent_at FROM touches WHERE business_id=? AND state IN "
                        "('SENT','PENDING','UNKNOWN')", (bid,))
        supp = reg.suppression_hits(bid)
        b = reg.business(bid)
        if touched or supp or b["status"] not in ("new",):
            why = supp[0] if supp else (f"already contacted by {touched[0]['playbook']} via {touched[0]['channel']}"
                                         if touched else f"status {b['status']}")
            reg.ensure_prospect(bid, pid, stage="skipped", reason=why, source=source, source_url=c.get("source_url"))
            stats["skipped_known"] += 1
            stats["rows"].append((reg.label(bid), "skipped", why))
            continue
        reg.ensure_prospect(bid, pid, stage="found", source=source, source_url=c.get("source_url"))
        stats["new_prospects"] += 1
        note = "needs duplicate review" if how in ("review", "conflict") else ""
        if c.get("evidence") or any((c.get("contacts") or {}).values()):
            stage, reason, _ = apply_research(reg, playbook, bid, c)
            note = f"{stage}: {reason}" + (f"; {note}" if note else "")
        stats["rows"].append((reg.label(bid), "found", note))
    return stats


# ------------------------------------------------------------------ one-command run
def run_auto(reg, playbook: dict, fetcher, *, location=None, target=5, max_requests=8, max_checks=25,
             research_days=30, out=print, search_fn=None) -> dict:
    """Find and check prospects until `target` qualify in this run.

    Limits: at most `max_requests` Places requests (shared monthly budget still applies) and `max_checks` site checks.
    A query already searched in the last `research_days` days is not paid for again.
    """
    from datetime import timedelta

    from . import checks

    pid = playbook["id"]
    disc = playbook.get("discovery", {})
    locations = [location] if location else list(disc.get("default_locations", []))
    if not locations:
        raise RuntimeError("give a location (this playbook has no discovery.default_locations)")
    search = search_fn or (lambda text: places_search(reg.settings, text, max_pages=1))
    since = (datetime.now(timezone.utc) - timedelta(days=research_days)).isoformat()
    state = {"qualified": [], "checked": 0, "requests": 0, "stopped": None}

    def check_found():
        rows = reg.q("SELECT business_id FROM prospects WHERE playbook=? AND stage='found' ORDER BY priority DESC, id",
                     (pid,))
        for r in rows:
            if len(state["qualified"]) >= target or state["checked"] >= max_checks:
                return
            res = checks.check_business(reg, fetcher, playbook, r["business_id"])
            state["checked"] += 1
            out(f"  • {reg.label(r['business_id'])} → {res['stage']}: {res['reason'][:150]}")
            if res["stage"] == "qualified":
                state["qualified"].append(r["business_id"])

    check_found()  # prospects found earlier but never checked come first (no new requests)
    for loc in locations:
        for q in disc.get("queries", []):
            if len(state["qualified"]) >= target or state["checked"] >= max_checks:
                break
            if state["requests"] >= max_requests:
                state["stopped"] = f"reached {max_requests} search requests for this run"
                break
            text = f"{q} in {loc}"
            if reg.q1("SELECT 1 FROM searches WHERE playbook=? AND query_text=? AND searched_at > ?", (pid, text, since)):
                continue
            if search_fn is None and places_budget(reg.settings)["remaining"] <= 0:
                state["stopped"] = "monthly Places budget (GEO + acq) used up"
                break
            try:
                found = search(text)
            except RuntimeError as e:
                state["stopped"] = str(e)
                break
            state["requests"] += 1
            reg.conn.execute("INSERT INTO searches (playbook, query_text, results, searched_at) VALUES (?,?,?,?)",
                             (pid, text, len(found), datetime.now(timezone.utc).isoformat()))
            stats = ingest(reg, playbook, [from_place(p) for p in found], "google_places")
            out(f"Search '{text}': {len(found)} results, {stats['new_prospects']} new, "
                f"{stats['skipped_known']} already known/contacted, {stats['filtered']} filtered out")
            check_found()
        if state["stopped"] or len(state["qualified"]) >= target or state["checked"] >= max_checks:
            break
    if not state["stopped"] and len(state["qualified"]) < target:
        state["stopped"] = ("checked the limit of sites for one run" if state["checked"] >= max_checks
                            else "no more new searches for these locations (all searched recently)")
    return state
