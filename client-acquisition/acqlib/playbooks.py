"""Playbooks: one JSON file per offer. Same pipeline, different problem checks, sample and message rules."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .config import PLAYBOOK_DIR
from .policy import CHANNELS

CHECK_TYPES = {"element", "link", "text", "count", "jsonld_type", "https", "manual", "contact_available"}
SOURCES = {"google_places", "urls", "csv"}
SAMPLE_TYPES = {"video", "image", "mockup_page", "pdf_report", "document", "none"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,40}$")


def path_for(pid: str) -> Path:
    return PLAYBOOK_DIR / f"{pid}.json"


def list_ids() -> list:
    return sorted(p.stem for p in PLAYBOOK_DIR.glob("*.json") if not p.stem.startswith("_"))


def load(ref: str) -> dict:
    p = Path(ref)
    if not p.suffix:
        p = path_for(ref)
    if not p.exists():
        raise FileNotFoundError(f"playbook '{ref}' not found (have: {', '.join(list_ids()) or 'none'})")
    pb = json.loads(p.read_text(encoding="utf-8"))
    errors = validate(pb)
    if errors:
        raise ValueError(f"playbook {p.name} is invalid:\n  - " + "\n  - ".join(errors))
    pb["_path"] = str(p)
    return pb


def _regex_ok(pattern, where, errors):
    try:
        re.compile(pattern)
    except re.error as e:
        errors.append(f"{where}: bad regex {pattern!r} ({e})")


def validate(pb: dict) -> list:
    e = []
    pid = pb.get("id", "")
    if not ID_RE.match(pid):
        e.append("id must be lowercase letters, digits and dashes (e.g. 'listing-video')")
    if pid == "geo":
        e.append("id 'geo' is reserved for the existing GEO pipeline")
    for key in ("name", "offer", "target", "checks", "qualify", "sample", "message"):
        if key not in pb:
            e.append(f"missing '{key}'")
    if e:
        return e
    offer = pb["offer"]
    for key in ("title", "summary"):
        if not offer.get(key):
            e.append(f"offer.{key} is required")
    countries = pb["target"].get("countries") or []
    if not countries:
        e.append("target.countries is required (e.g. [\"US\"])")

    disc = pb.get("discovery", {})
    if disc and disc.get("source") not in SOURCES:
        e.append(f"discovery.source must be one of {sorted(SOURCES)}")
    if disc.get("source") == "google_places" and not disc.get("queries"):
        e.append("discovery.queries is required for google_places")
    if disc.get("filters", {}).get("exclude_name_pattern"):
        _regex_ok(disc["filters"]["exclude_name_pattern"], "discovery.filters.exclude_name_pattern", e)
    for key in ("path_pattern", "text_pattern"):
        if pb.get("detail_page", {}).get(key):
            _regex_ok(pb["detail_page"][key], f"detail_page.{key}", e)
    if pb.get("crawl", {}).get("page_keywords"):
        _regex_ok(pb["crawl"]["page_keywords"], "crawl.page_keywords", e)

    ids = set()
    for i, c in enumerate(pb["checks"]):
        where = f"checks[{i}] ({c.get('id', '?')})"
        cid = c.get("id", "")
        if not re.match(r"^[a-z0-9_]+$", cid) or cid.startswith("_"):
            e.append(f"{where}: id must be lowercase snake_case")
        if cid in ids:
            e.append(f"{where}: duplicate id")
        ids.add(cid)
        t = c.get("type")
        if t not in CHECK_TYPES:
            e.append(f"{where}: type must be one of {sorted(CHECK_TYPES)}")
            continue
        if not c.get("label"):
            e.append(f"{where}: label is required")
        if t in ("element", "count") and c.get("source") != "images":
            if not c.get("match"):
                e.append(f"{where}: 'match' selectors are required")
            for s in c.get("match", []):
                if not s.get("tag"):
                    e.append(f"{where}: every selector needs 'tag'")
                if s.get("pattern"):
                    _regex_ok(s["pattern"], where, e)
        if t in ("link", "text"):
            if not c.get("pattern"):
                e.append(f"{where}: 'pattern' is required")
            else:
                _regex_ok(c["pattern"], where, e)
        if t == "count" and c.get("min") is None and c.get("max") is None:
            e.append(f"{where}: count needs 'min' and/or 'max'")
        if t == "count" and c.get("exclude_pattern"):
            _regex_ok(c["exclude_pattern"], where, e)
        if t == "jsonld_type" and not c.get("types"):
            e.append(f"{where}: 'types' is required")
        if t in ("element", "link", "text", "jsonld_type", "https") and c.get("hit_if", "present") not in ("present", "absent"):
            e.append(f"{where}: hit_if must be 'present' or 'absent'")
        if t == "manual" and not c.get("instructions"):
            e.append(f"{where}: manual checks need 'instructions' (how a human verifies it, which URL to record)")

    q = pb["qualify"]
    if not q.get("all_of") and not q.get("any_of"):
        e.append("qualify needs all_of and/or any_of")
    for cid in qualify_ids(pb):
        if cid not in ids:
            e.append(f"qualify references unknown check '{cid}'")
    deciding = set(q.get("all_of", [])) | {cid for g in any_of_groups(pb) for cid in g}
    if not any(c.get("problem") for c in pb["checks"] if c.get("id") in deciding):
        e.append("at least one qualify.all_of/any_of check must describe a 'problem' (what the client gets help with)")
    for c in pb["checks"]:
        if c.get("page_pattern"):
            _regex_ok(c["page_pattern"], f"checks.{c.get('id')}.page_pattern", e)
        if c.get("pages") not in (None, "detail"):
            e.append(f"checks.{c.get('id')}.pages must be 'detail' when set")
        if c.get("pages") == "detail" and not pb.get("detail_page", {}).get("path_pattern"):
            e.append(f"checks.{c.get('id')} uses pages=detail but the playbook has no detail_page.path_pattern")
        if c.get("aggregate") not in (None, "sum", "min", "max"):
            e.append(f"checks.{c.get('id')}.aggregate must be sum, min or max")
    if pb.get("discovery", {}).get("source") == "google_places":
        for qtext in pb["discovery"].get("queries", []):
            if any(b in qtext.lower() for b in ("airbnb.com", "vrbo.com", "booking.com")):
                e.append(f"discovery query '{qtext}' targets a platform site; search for businesses instead")

    s = pb["sample"]
    if s.get("type") not in SAMPLE_TYPES:
        e.append(f"sample.type must be one of {sorted(SAMPLE_TYPES)}")
    if s.get("type") != "none" and not s.get("label"):
        e.append("sample.label is required (the honest caption shown with the sample)")

    m = pb["message"]
    for ch in m.get("channels", []):
        if ch not in CHANNELS:
            e.append(f"message.channels: unknown channel '{ch}' (use {', '.join(CHANNELS)})")
    if not m.get("channels"):
        e.append("message.channels is required")
    return e


def any_of_groups(pb: dict) -> list:
    """qualify.any_of is one group ["a", "b"] or several [["a", "b"], ["c", "d"]]: one check per group must hit."""
    raw = pb.get("qualify", {}).get("any_of", [])
    if not raw:
        return []
    return [raw] if all(isinstance(x, str) for x in raw) else [list(g) for g in raw]


def qualify_ids(pb: dict) -> list:
    q = pb.get("qualify", {})
    return list(q.get("all_of", [])) + [cid for g in any_of_groups(pb) for cid in g] + list(q.get("signals", []))


def check_by_id(pb: dict, cid: str) -> dict:
    for c in pb["checks"]:
        if c["id"] == cid:
            return c
    raise KeyError(f"playbook {pb['id']} has no check '{cid}'")
