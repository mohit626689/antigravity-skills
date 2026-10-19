"""The outreach eligibility gate. Every playbook goes through can_contact(); nothing sends without reserve_touch()."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

from . import identity
from .db import now_iso, parse_iso

CONTACT_STATES = ("SENT", "PENDING", "UNKNOWN")
MANUAL_CHANNELS = ("contact_form", "instagram", "facebook", "linkedin", "whatsapp", "phone", "sms", "other")
CHANNELS = ("email",) + MANUAL_CHANNELS
READY_STAGES = ("qualified", "sample_ready", "drafted")


@dataclass
class Decision:
    allowed: bool
    reasons: list = field(default_factory=list)   # why it is blocked
    notes: list = field(default_factory=list)     # context that does not block

    def __str__(self):
        head = "ALLOWED" if self.allowed else "BLOCKED"
        lines = [head] + [f"  - {r}" for r in self.reasons] + [f"  · {n}" for n in self.notes]
        return "\n".join(lines)


def _days(now: datetime, iso: str) -> float:
    return (now - parse_iso(iso)).total_seconds() / 86400


def can_contact(reg, bid: int, *, playbook: str, channel: str, recipient: str, kind: str = "pitch",
                parent_touch_id: Optional[int] = None, require_sample: bool = False,
                now: Optional[datetime] = None, sync_geo: bool = True) -> Decision:
    from . import geo_bridge  # local import: geo_bridge imports registry helpers

    now = now or datetime.now(timezone.utc)
    pol = reg.policy
    if sync_geo:
        geo_bridge.sync_ledger(reg)

    reasons, notes = [], []
    bid = reg.resolve(bid)
    b = reg.business(bid)
    if not b:
        return Decision(False, [f"business #{bid} not found"])

    # identity / record state
    if b["needs_review"]:
        reasons.append(f"needs duplicate review: {b['review_note']} (run `acq review`)")
    if b["status"] in pol.get("blocked_statuses", []):
        reasons.append(f"business status is '{b['status']}'")
    country = (b["country"] or "").upper()
    if not country:
        reasons.append("country unknown (set it with `acq set-country`)")
    elif country not in [c.upper() for c in pol.get("allowed_countries", [])]:
        reasons.append(f"country {country} is not in allowed_countries")

    # channel / recipient
    if channel not in CHANNELS:
        reasons.append(f"unknown channel '{channel}'")
    if channel == "email":
        e = identity.normalize_email(recipient)
        if not e:
            reasons.append(f"'{recipient}' is not a valid email address")
        elif identity.email_domain(e) in pol.get("placeholder_email_domains", []):
            reasons.append(f"'{recipient}' is a placeholder address")
    elif not (recipient or "").strip():
        reasons.append("recipient (profile / form URL / number) is empty")
    if identity.automation_forbidden(recipient or ""):
        reasons.append("recipient is on Airbnb/VRBO/Booking/Expedia; contact the business through its own channels")

    reasons += reg.suppression_hits(bid, recipient if channel == "email" else None)

    touches = reg.q("SELECT * FROM touches WHERE business_id=? ORDER BY COALESCE(sent_at, created_at)", (bid,))
    unresolved = [t for t in touches if t["state"] in ("PENDING", "UNKNOWN")]
    if unresolved:
        ids = ", ".join(f"#{t['id']}" for t in unresolved)
        reasons.append(f"unresolved send(s) {ids}: check what actually went out, then `acq touch resolve`")
    sent = [t for t in touches if t["state"] == "SENT"]
    last = sent[-1] if sent else None
    if last:
        notes.append(f"last contact {last['sent_at'][:10]} via {last['channel']} ({last['playbook']}: "
                     f"{last['topic'] or last['kind']})")

    if kind == "pitch":
        if b["status"] in ("replied", "meeting") and pol.get("block_new_pitch_when_engaged", True):
            reasons.append("business is in an active conversation; add this opportunity to that conversation yourself")
        if last:
            days = _days(now, last["sent_at"])
            cooldown = pol.get("cooldown_days_any_touch", 90)
            if days < cooldown:
                reasons.append(f"contacted {days:.0f} day(s) ago; cooldown is {cooldown} days for any new topic")
            else:
                recontact = pol.get("recontact_unanswered_after_days")
                if b["status"] not in ("replied", "meeting"):
                    if recontact is None:
                        reasons.append("already pitched once without a reply; automatic re-contact is disabled "
                                       "(policy recontact_unanswered_after_days = null)")
                    elif days < recontact:
                        reasons.append(f"unanswered pitch {days:.0f} day(s) ago; re-contact allowed after {recontact}")
        p = reg.prospect(bid, playbook)
        if not p or p["stage"] not in READY_STAGES:
            reasons.append(f"not qualified for playbook '{playbook}' (stage: {p['stage'] if p else 'none'})")
        if require_sample and not reg.latest_sample(bid, playbook):
            reasons.append("playbook requires a sample, none registered (`acq sample register`)")

    elif kind == "followup":
        parent = reg.q1("SELECT * FROM touches WHERE id=?", (parent_touch_id,)) if parent_touch_id else None
        if not parent or reg.resolve(parent["business_id"]) != bid:
            reasons.append("follow-up needs --parent <touch id> of a pitch to this business")
        else:
            if parent["state"] != "SENT" or parent["kind"] != "pitch":
                reasons.append(f"parent touch #{parent['id']} is not a sent pitch")
            if parent["source"] != "acq":
                reasons.append("parent was sent by the GEO pipeline; follow up with /geo-message --track instead")
            if b["status"] in ("replied", "meeting"):
                reasons.append("they replied; answer personally instead of sending a follow-up")
            done = reg.q1("SELECT COUNT(*) n FROM touches WHERE parent_touch_id=? AND state IN ('SENT','PENDING','UNKNOWN')",
                          (parent["id"],))["n"]
            if done >= pol.get("max_followups_per_pitch", 1):
                reasons.append(f"follow-up limit reached ({done}/{pol.get('max_followups_per_pitch', 1)})")
            if parent["sent_at"]:
                age = _days(now, parent["sent_at"])
                if age > pol.get("followup_max_days", 21):
                    reasons.append(f"pitch is {age:.0f} days old; follow-up window is {pol.get('followup_max_days', 21)} days")
            if last and _days(now, last["sent_at"]) < pol.get("followup_min_days", 3):
                reasons.append(f"last contact was under {pol.get('followup_min_days', 3)} days ago")
    else:
        reasons.append(f"unknown kind '{kind}'")

    year = [t for t in sent if _days(now, t["sent_at"]) <= 365]
    if len(year) >= pol.get("max_touches_per_business_365d", 3):
        reasons.append(f"{len(year)} messages in the last 365 days (limit {pol.get('max_touches_per_business_365d', 3)})")

    if channel == "email":
        since = (now - timedelta(hours=24)).isoformat()
        n = reg.q1("SELECT COUNT(*) n FROM touches WHERE channel='email' AND state IN ('SENT','PENDING','UNKNOWN') "
                   "AND COALESCE(sent_at, created_at) > ?", (since,))["n"]
        cap = pol.get("daily_email_cap_combined", 5)
        if n >= cap:
            reasons.append(f"daily email cap reached: {n}/{cap} in the last 24h (acq + GEO)")
        else:
            notes.append(f"emails in last 24h (acq + GEO): {n}/{cap}")

    return Decision(not reasons, reasons, notes)


def idempotency_key(bid, playbook, kind, channel, recipient, parent_touch_id) -> str:
    raw = f"{bid}|{playbook}|{kind}|{channel}|{(recipient or '').strip().lower()}|{parent_touch_id or ''}"
    return hashlib.sha256(raw.encode()).hexdigest()


def reserve_touch(reg, bid, *, playbook, kind, channel, recipient, topic, draft_id=None, parent_touch_id=None,
                  require_sample=False, now=None):
    """Re-check the gate and write a PENDING touch in one write transaction.

    Returns (touch_id, Decision). touch_id is None when blocked. A crash after this point leaves a PENDING row,
    which blocks every further send to the business until a human resolves it, so no duplicate can go out.
    """
    from . import geo_bridge

    geo_bridge.sync_ledger(reg)
    c = reg.conn
    c.execute("BEGIN IMMEDIATE")
    try:
        d = can_contact(reg, bid, playbook=playbook, channel=channel, recipient=recipient, kind=kind,
                        parent_touch_id=parent_touch_id, require_sample=require_sample, now=now, sync_geo=False)
        if not d.allowed:
            c.execute("ROLLBACK")
            return None, d
        key = idempotency_key(bid, playbook, kind, channel, recipient, parent_touch_id)
        existing = reg.q1("SELECT * FROM touches WHERE idempotency_key=?", (key,))
        if existing and existing["state"] != "FAILED":
            c.execute("ROLLBACK")
            return None, Decision(False, [f"identical message already recorded as touch #{existing['id']} "
                                          f"({existing['state']})"])
        if existing:  # a previous attempt definitely failed: retry on the same row
            c.execute("UPDATE touches SET state='PENDING', error=NULL, draft_id=?, created_at=? WHERE id=?",
                      (draft_id, now_iso(), existing["id"]))
            tid = existing["id"]
        else:
            tid = c.execute(
                "INSERT INTO touches (business_id, playbook, kind, channel, recipient, topic, state, idempotency_key, "
                "parent_touch_id, draft_id, source, created_at) VALUES (?,?,?,?,?,?, 'PENDING', ?,?,?, 'acq', ?)",
                (bid, playbook, kind, channel, recipient, topic, key, parent_touch_id, draft_id, now_iso())).lastrowid
        c.execute("COMMIT")
        return tid, d
    except Exception:
        c.execute("ROLLBACK")
        raise


def resolve_touch(reg, touch_id, state, *, message_id=None, error=None):
    if state not in ("SENT", "FAILED", "UNKNOWN"):
        raise ValueError("state must be SENT, FAILED or UNKNOWN")
    t = reg.q1("SELECT * FROM touches WHERE id=?", (touch_id,))
    if not t:
        raise ValueError(f"touch #{touch_id} not found")
    sent_at = now_iso() if state == "SENT" else None
    reg.conn.execute("UPDATE touches SET state=?, message_id=COALESCE(?, message_id), error=?, sent_at=? WHERE id=?",
                     (state, message_id, error, sent_at, touch_id))
    if state == "SENT":
        reg.conn.execute("UPDATE businesses SET status='contacted', updated_at=? WHERE id=? AND status='new'",
                         (now_iso(), t["business_id"]))
        if t["draft_id"]:
            reg.conn.execute("UPDATE drafts SET status='sent' WHERE id=?", (t["draft_id"],))
        reg.conn.execute("UPDATE prospects SET stage='contacted', updated_at=? WHERE business_id=? AND playbook=?",
                         (now_iso(), t["business_id"], t["playbook"]))
        reg.conn.execute("UPDATE opportunities SET status='pitched' WHERE business_id=? AND playbook=? AND status='open'",
                         (t["business_id"], t["playbook"]))
    reg.event(t["business_id"], f"touch:{state}", f"touch #{touch_id} {t['channel']} {t['recipient'] or ''}")
