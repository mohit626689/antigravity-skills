"""Registry operations: business identity/dedupe, prospects, evidence, opportunities, samples, suppression, outcomes."""
from __future__ import annotations

import sqlite3
from typing import Iterable, Optional

from . import identity
from .db import now_iso

OUTCOMES = {
    # outcome: (new business status or None, suppress business?, suppress the email given?)
    "replied": ("replied", False, False),
    "meeting": ("meeting", False, False),
    "won": ("client", False, False),
    "lost": ("lost", False, False),
    "not_interested": ("not_interested", True, True),
    "opt_out": ("opted_out", True, True),
    "do_not_contact": ("do_not_contact", True, True),
    "bounced": (None, False, True),
}


class Registry:
    def __init__(self, conn: sqlite3.Connection, settings: dict, policy: dict):
        self.conn = conn
        self.settings = settings
        self.policy = policy

    # ------------------------------------------------------------------ helpers
    def q(self, sql, params=()):
        return self.conn.execute(sql, params).fetchall()

    def q1(self, sql, params=()):
        return self.conn.execute(sql, params).fetchone()

    def event(self, bid, type_, note=None):
        self.conn.execute("INSERT INTO events (business_id, type, note, created_at) VALUES (?,?,?,?)",
                          (bid, type_, note, now_iso()))

    def resolve(self, bid: Optional[int]) -> Optional[int]:
        seen = set()
        while bid is not None and bid not in seen:
            seen.add(bid)
            row = self.q1("SELECT merged_into FROM businesses WHERE id=?", (bid,))
            if not row or row["merged_into"] is None:
                return bid
            bid = row["merged_into"]
        return bid

    def business(self, bid):
        return self.q1("SELECT * FROM businesses WHERE id=?", (bid,))

    def identifiers(self, bid):
        return self.q("SELECT kind, value, source FROM identifiers WHERE business_id=? ORDER BY kind", (bid,))

    def primary_domain(self, bid) -> str:
        row = self.q1("SELECT value FROM identifiers WHERE business_id=? AND kind='domain' ORDER BY created_at LIMIT 1",
                      (bid,))
        return row["value"] if row else ""

    def label(self, bid) -> str:
        b = self.business(bid)
        if not b:
            return f"#{bid}"
        dom = self.primary_domain(bid)
        return f"#{bid} {b['name']}" + (f" ({dom})" if dom and dom != b["name"] else "")

    # ----------------------------------------------------------------- identity
    def _candidate_ids(self, *, website, phone, emails, place_id, maps_url, country, profiles=()):
        ids = []
        for url in [website, *(profiles or ())]:
            if not url:
                continue
            d = identity.domain_key(url)
            if d and ("domain", d) not in ids:
                ids.append(("domain", d))
            p = identity.profile_key(url)
            if p and ("profile", p) not in ids:
                ids.append(("profile", p))
        if place_id:
            ids.append(("place", str(place_id).strip()))
        if maps_url:
            ids.append(("maps", str(maps_url).strip().lower()))
        if phone:
            ph = identity.normalize_phone(phone, country or "")
            if ph:
                ids.append(("phone", ph))
        for e in emails or ():
            ne = identity.normalize_email(e)
            if ne:
                ids.append(("email", ne))
        return ids

    def _add_identifier(self, bid, kind, value, source):
        self.conn.execute("INSERT OR IGNORE INTO identifiers (kind, value, business_id, source, created_at) "
                          "VALUES (?,?,?,?,?)", (kind, value, bid, source, now_iso()))
        owner = self.resolve(self.q1("SELECT business_id FROM identifiers WHERE kind=? AND value=?",
                                     (kind, value))["business_id"])
        if owner != bid:
            note = f"{kind} '{value}' already belongs to #{owner}"
            self.flag_review(bid, note)
            self.flag_review(owner, f"{kind} '{value}' also seen on #{bid}")

    def flag_review(self, bid, note):
        b = self.business(bid)
        if not b:
            return
        notes = [n for n in (b["review_note"] or "").split(" | ") if n]
        if note not in notes:
            notes.append(note)
        self.conn.execute("UPDATE businesses SET needs_review=1, review_note=?, updated_at=? WHERE id=?",
                          (" | ".join(notes), now_iso(), bid))

    def _fill(self, bid, name, website, city, region, country):
        b = self.business(bid)
        new_name = b["name"]
        # GEO-ledger imports only know the domain; replace a domain-looking placeholder with a real name.
        if name and (not b["name"] or ("." in b["name"] and " " not in b["name"] and " " in name)):
            new_name = name
        self.conn.execute(
            "UPDATE businesses SET name=?, website=COALESCE(website, ?), city=COALESCE(city, ?), "
            "region=COALESCE(region, ?), country=COALESCE(country, ?), updated_at=? WHERE id=?",
            (new_name, website or None, city or None, region or None, (country or "").upper() or None, now_iso(), bid))

    def upsert_business(self, *, name, website=None, phone=None, emails: Iterable[str] = (), place_id=None,
                        maps_url=None, city=None, region=None, country=None, source="manual", profiles=()):
        """Returns (business_id, how) where how is new | matched | review | conflict.

        Strong identifiers (domain, platform profile, place id, maps url, phone, email) match automatically.
        `profiles` are extra URLs for the same business: a host profile and its listing URLs, social pages.
        Name + city alone never merges: the new record is created and flagged for human review.
        """
        country = (country or "").upper() or None
        if website and identity.is_platform(website):   # a platform URL is a profile, never the business's own site
            profiles, website = [website, *(profiles or ())], None
        ids = self._candidate_ids(website=website, phone=phone, emails=emails, place_id=place_id,
                                  maps_url=maps_url, country=country, profiles=profiles)
        matched = set()
        for kind, value in ids:
            row = self.q1("SELECT business_id FROM identifiers WHERE kind=? AND value=?", (kind, value))
            if row:
                matched.add(self.resolve(row["business_id"]))

        if len(matched) == 1:
            bid = matched.pop()
            self._fill(bid, name, website, city, region, country)
            for kind, value in ids:
                self._add_identifier(bid, kind, value, source)
            return bid, "matched"

        if len(matched) > 1:
            ordered = sorted(matched)
            for b in ordered:
                self.flag_review(b, f"identifiers of one input match several records {ordered}")
            return ordered[0], "conflict"

        ts = now_iso()
        cur = self.conn.execute(
            "INSERT INTO businesses (name, website, city, region, country, created_at, updated_at) "
            "VALUES (?,?,?,?,?,?,?)",
            (name or identity.domain_key(website or "") or (identity.profile_key(profiles[0]) if profiles else "")
             or "unknown", website, city, region, country, ts, ts))
        bid = cur.lastrowid
        for kind, value in ids:
            self._add_identifier(bid, kind, value, source)
        how = "new"
        nk = identity.name_key(name or "", city or "")
        if nk:
            row = self.q1("SELECT business_id FROM identifiers WHERE kind='name_city' AND value=?", (nk,))
            if row:
                other = self.resolve(row["business_id"])
                self.flag_review(bid, f"same name and city as #{other}")
                how = "review"
            else:
                self._add_identifier(bid, "name_city", nk, source)
        self.event(bid, "created", f"source={source}")
        return bid, how

    def find(self, ref: str) -> Optional[int]:
        ref = (ref or "").strip()
        if not ref:
            return None
        if ref.lstrip("#").isdigit():
            bid = int(ref.lstrip("#"))
            return self.resolve(bid) if self.business(bid) else None
        if "@" in ref:
            row = self.q1("SELECT business_id FROM identifiers WHERE kind='email' AND value=?",
                          (identity.normalize_email(ref),))
            return self.resolve(row["business_id"]) if row else None
        for kind, value in (("domain", identity.domain_key(ref)), ("profile", identity.profile_key(ref))):
            if value:
                row = self.q1("SELECT business_id FROM identifiers WHERE kind=? AND value=?", (kind, value))
                if row:
                    return self.resolve(row["business_id"])
        rows = self.q("SELECT id FROM businesses WHERE lower(name)=lower(?) AND merged_into IS NULL", (ref,))
        return rows[0]["id"] if len(rows) == 1 else None

    def merge(self, src: int, dst: int):
        """Fold record `src` into `dst` (same real business)."""
        src, dst = self.resolve(src), self.resolve(dst)
        if src == dst:
            return
        c = self.conn
        c.execute("BEGIN IMMEDIATE")
        try:
            c.execute("UPDATE identifiers SET business_id=? WHERE business_id=?", (dst, src))
            for p in self.q("SELECT * FROM prospects WHERE business_id=?", (src,)):
                if self.q1("SELECT 1 FROM prospects WHERE business_id=? AND playbook=?", (dst, p["playbook"])):
                    c.execute("DELETE FROM prospects WHERE id=?", (p["id"],))
                else:
                    c.execute("UPDATE prospects SET business_id=? WHERE id=?", (dst, p["id"]))
            c.execute("UPDATE OR IGNORE opportunities SET business_id=? WHERE business_id=?", (dst, src))
            c.execute("DELETE FROM opportunities WHERE business_id=?", (src,))
            for table in ("evidence", "samples", "drafts", "touches", "events"):
                c.execute(f"UPDATE {table} SET business_id=? WHERE business_id=?", (dst, src))
            c.execute("UPDATE businesses SET status='merged', merged_into=?, needs_review=0, updated_at=? WHERE id=?",
                      (dst, now_iso(), src))
            self.event(dst, "merged", f"#{src} merged into #{dst}")
            c.execute("COMMIT")
        except Exception:
            c.execute("ROLLBACK")
            raise

    def mark_reviewed(self, bid: int, note: str = "confirmed distinct"):
        self.conn.execute("UPDATE businesses SET needs_review=0, review_note=NULL, updated_at=? WHERE id=?",
                          (now_iso(), bid))
        self.event(bid, "review_resolved", note)

    def set_country(self, bid: int, country: str):
        self.conn.execute("UPDATE businesses SET country=?, updated_at=? WHERE id=?",
                          ((country or "").upper() or None, now_iso(), bid))

    # ---------------------------------------------------------------- prospects
    def ensure_prospect(self, bid, playbook, *, stage="found", reason=None, source=None, source_url=None):
        row = self.prospect(bid, playbook)
        if row:
            return row, False
        ts = now_iso()
        self.conn.execute(
            "INSERT INTO prospects (business_id, playbook, stage, reason, source, source_url, created_at, updated_at) "
            "VALUES (?,?,?,?,?,?,?,?)", (bid, playbook, stage, reason, source, source_url, ts, ts))
        return self.prospect(bid, playbook), True

    def prospect(self, bid, playbook):
        return self.q1("SELECT * FROM prospects WHERE business_id=? AND playbook=?", (bid, playbook))

    def set_stage(self, bid, playbook, stage, reason=None, priority=None):
        self.ensure_prospect(bid, playbook, stage=stage, reason=reason)
        if priority is None:
            self.conn.execute("UPDATE prospects SET stage=?, reason=?, updated_at=? WHERE business_id=? AND playbook=?",
                              (stage, reason, now_iso(), bid, playbook))
        else:
            self.conn.execute("UPDATE prospects SET stage=?, reason=?, priority=?, updated_at=? "
                              "WHERE business_id=? AND playbook=?", (stage, reason, priority, now_iso(), bid, playbook))

    # ----------------------------------------------------------------- evidence
    def add_evidence(self, bid, playbook, check_id, status, hit, summary, *, source_url=None, run_file=None,
                     method="auto") -> int:
        self.conn.execute("UPDATE evidence SET current=0 WHERE business_id=? AND playbook=? AND check_id=? AND current=1",
                          (bid, playbook, check_id))
        cur = self.conn.execute(
            "INSERT INTO evidence (business_id, playbook, check_id, status, hit, summary, source_url, run_file, method, "
            "observed_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (bid, playbook, check_id, status, None if hit is None else int(bool(hit)), summary, source_url, run_file,
             method, now_iso()))
        return cur.lastrowid

    def current_evidence(self, bid, playbook) -> dict:
        rows = self.q("SELECT * FROM evidence WHERE business_id=? AND playbook=? AND current=1", (bid, playbook))
        return {r["check_id"]: r for r in rows}

    def add_opportunity(self, bid, playbook, title, basis, evidence_id=None):
        self.conn.execute(
            "INSERT OR IGNORE INTO opportunities (business_id, playbook, title, basis, evidence_id, created_at) "
            "VALUES (?,?,?,?,?,?)", (bid, playbook, title, basis, evidence_id, now_iso()))

    # ------------------------------------------------------------------ samples
    def add_sample(self, bid, playbook, *, path, link, label, sha256, size_bytes) -> int:
        cur = self.conn.execute(
            "INSERT INTO samples (business_id, playbook, path, link, label, sha256, size_bytes, created_at) "
            "VALUES (?,?,?,?,?,?,?,?)", (bid, playbook, path, link, label, sha256, size_bytes, now_iso()))
        return cur.lastrowid

    def latest_sample(self, bid, playbook):
        return self.q1("SELECT * FROM samples WHERE business_id=? AND playbook=? ORDER BY id DESC LIMIT 1",
                       (bid, playbook))

    # -------------------------------------------------------------- suppression
    def _norm_suppression(self, kind, value):
        if kind == "email":
            return identity.normalize_email(value)
        if kind == "domain":
            return identity.domain_key(value) or identity.registrable_domain(value)
        if kind == "phone":
            return identity.normalize_phone(value, "US") or value.strip()
        if kind == "business":
            return str(int(str(value).lstrip("#")))
        raise ValueError(f"unknown suppression kind {kind!r}")

    def suppress(self, kind, value, reason, source="manual"):
        norm = self._norm_suppression(kind, value)
        if not norm:
            raise ValueError(f"cannot normalize {kind} '{value}'")
        self.conn.execute("INSERT OR IGNORE INTO suppression (kind, value, reason, source, created_at) "
                          "VALUES (?,?,?,?,?)", (kind, norm, reason, source, now_iso()))
        return norm

    def suppression_hits(self, bid, recipient=None) -> list:
        hits = []

        def check(kind, value):
            if not value:
                return
            row = self.q1("SELECT reason FROM suppression WHERE kind=? AND value=?", (kind, value))
            if row:
                hits.append(f"suppressed {kind} {value}: {row['reason']}")

        check("business", str(bid))
        for ident in self.identifiers(bid):
            if ident["kind"] in ("domain", "email", "phone"):
                check(ident["kind"], ident["value"])
        if recipient and "@" in recipient:
            e = identity.normalize_email(recipient)
            check("email", e)
            dom = identity.email_domain(e)
            if dom and dom not in self.policy.get("freemail_domains", []):
                check("domain", identity.registrable_domain(dom))
        return hits

    # ----------------------------------------------------------------- outcomes
    def record_outcome(self, bid, outcome, note=None, email=None):
        if outcome not in OUTCOMES:
            raise ValueError(f"outcome must be one of {sorted(OUTCOMES)}")
        status, suppress_business, suppress_email = OUTCOMES[outcome]
        if status:
            self.conn.execute("UPDATE businesses SET status=?, updated_at=? WHERE id=?", (status, now_iso(), bid))
        if suppress_business:
            self.suppress("business", bid, outcome, "outcome")
        if suppress_email:
            emails = {identity.normalize_email(email)} if email else set()
            if outcome != "bounced":
                emails |= {r["recipient"] for r in self.q(
                    "SELECT DISTINCT recipient FROM touches WHERE business_id=? AND channel='email' AND recipient IS NOT NULL",
                    (bid,))}
            for e in filter(None, emails):
                self.suppress("email", e, outcome, "outcome")
        self.event(bid, f"outcome:{outcome}", note)
