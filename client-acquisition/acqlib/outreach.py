"""Drafts, human approval and gated sending.

The agent writes the message; this module decides whether it may exist (validation), whether a human approved it
(native macOS dialog or interactive terminal, which an agent cannot click through), and whether it may go out
right now (the shared gate + a PENDING touch written before sending).
"""
from __future__ import annotations

import getpass
import hashlib
import json
import mimetypes
import re
import smtplib
import subprocess
import sys
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

from . import identity, policy as gate

NUM_RE = re.compile(r"\d+(?:[.,]\d+)*")
URL_RE = re.compile(r"https?://\S+")


class BeforeSendError(Exception):
    """Failed before the server accepted the message: it definitely did not go out."""


def content_sha(channel, recipient, subject, body, sample_id) -> str:
    raw = json.dumps([channel, (recipient or "").lower(), subject or "", body, sample_id])
    return hashlib.sha256(raw.encode()).hexdigest()


def _numbers(text: str) -> set:
    return {n.replace(",", "") for n in NUM_RE.findall(URL_RE.sub(" ", text or ""))}


def _evidence_numbers(summary: str) -> set:
    """Numbers a message may quote from evidence: the finding itself, not the scope (page counts, dates, paths)."""
    s = re.split(r" across | on the \d+ (?:property )?page| checked on ", summary or "")[0]
    s = re.sub(r"\([≥≤][^)]*\)", " ", s)
    return _numbers(s)


def footer(settings, env) -> str:
    addr = env.get("POSTAL_ADDRESS", "").strip()
    if not addr:
        raise RuntimeError("POSTAL_ADDRESS is not configured (needed in every cold email footer)")
    who = " · ".join(x for x in (settings.get("sender_name"), settings.get("business_name")) if x)
    return f"\n\n--\n{who}\n{addr}\nNot relevant? Reply \"no thanks\" and I won't contact you again."


def render(draft, sample, settings, env) -> str:
    body = draft["body"]
    if sample and sample["link"]:
        body = body.replace("{sample_link}", sample["link"])
    if draft["channel"] == "email":
        body += footer(settings, env)
    return body


def validate(reg, playbook, *, bid, kind, channel, recipient, recipient_source, subject, body, evidence_ids,
             parent_touch_id=None):
    """Returns (problems, sample_row). Problems make the draft 'invalid'; nothing invalid can be approved."""
    pid = playbook["id"]
    m = playbook["message"]
    pol = reg.policy
    problems = []
    text = f"{subject or ''}\n{body}"

    if channel not in m.get("channels", []):
        problems.append(f"channel '{channel}' is not allowed by this playbook ({', '.join(m.get('channels', []))})")
    limit = m.get("max_words", 150) if kind == "pitch" else m.get("followup_max_words", 70)
    words = len(re.findall(r"[A-Za-z0-9][\w'’-]*", body))
    if words > limit:
        problems.append(f"{words} words; limit is {limit}")
    if not body.strip():
        problems.append("empty message")
    low = text.lower()
    for phrase in pol.get("forbidden_phrases", []) + m.get("forbidden_phrases", []):
        if phrase.lower() in low:
            problems.append(f"forbidden phrase: '{phrase}'")
    for ph in set(re.findall(r"\{(\w+)\}", body)) - {"sample_link"}:
        problems.append(f"unfilled placeholder {{{ph}}}")
    if re.search(r"\[(?:[A-Z][A-Za-z ]{0,30}|name|business|city)\]", text):
        problems.append("template placeholder in [brackets] left in the message")
    if channel == "email":
        if not (subject or "").strip():
            problems.append("email needs a subject")
        elif re.match(r"^\s*(re|fwd?)\s*:", subject, re.I):
            problems.append("subject pretends to be a reply/forward")

    # evidence: every pitch rests on at least one observed problem on this business
    cited = []
    allowed_numbers = {str(x) for x in m.get("allowed_numbers", [])}
    allowed_numbers |= _numbers(playbook["offer"].get("title", "")) | _numbers(playbook["offer"].get("summary", ""))
    b = reg.business(bid)
    allowed_numbers |= _numbers(b["name"] or "")
    problem_checks = {c["id"] for c in playbook["checks"] if c.get("problem")}
    from .playbooks import qualify_ids
    usable_checks = problem_checks | set(qualify_ids(playbook))
    for eid in evidence_ids or []:
        e = reg.q1("SELECT * FROM evidence WHERE id=?", (eid,))
        if not e or reg.resolve(e["business_id"]) != bid or e["playbook"] != pid:
            problems.append(f"evidence E{eid} does not belong to this business/playbook")
            continue
        if not e["current"]:
            problems.append(f"evidence E{eid} is outdated (a newer check replaced it)")
        if e["status"] != "OBSERVED" or e["hit"] != 1:
            problems.append(f"evidence E{eid} is {e['status']}/hit={e['hit']}: only observed findings may be cited")
        if e["check_id"] not in usable_checks:
            problems.append(f"evidence E{eid} ({e['check_id']}) is not one of this playbook's qualifying checks")
        cited.append(e)
        allowed_numbers |= _evidence_numbers(e["summary"])
    if kind == "pitch":
        if not cited:
            problems.append("cite the observed problem(s) with --evidence <ids> (see `acq show`)")
        elif not any(e["check_id"] in problem_checks for e in cited):
            problems.append("none of the cited evidence is a problem check")
    unsupported = sorted(_numbers(text) - allowed_numbers)
    if unsupported:
        problems.append(f"numbers not backed by cited evidence or the playbook: {', '.join(unsupported)} "
                        f"(remove them, cite the evidence, or add to message.allowed_numbers)")

    # sample
    sample = None
    sample_required = playbook["sample"].get("type") != "none" and playbook["sample"].get("required", True)
    if kind == "pitch" and sample_required:
        sample = reg.latest_sample(bid, pid)
        if not sample:
            problems.append("this playbook requires a sample; register it first (`acq sample register`)")
        elif sample["link"]:
            if "{sample_link}" not in body and sample["link"] not in body:
                problems.append("include the sample link in the message as {sample_link}")
        elif channel != "email":
            problems.append(f"{channel} cannot carry an attachment: register the sample with --link")
        else:
            max_b = reg.settings.get("attachment_max_mb", 15) * 1024 * 1024
            if not sample["path"] or not Path(sample["path"]).is_file():
                problems.append("sample file is missing on disk")
            elif (sample["size_bytes"] or 0) > max_b:
                problems.append("sample file is larger than attachment_max_mb: register an unlisted --link instead")
    if "{sample_link}" in body and sample is None:
        sample = reg.latest_sample(bid, pid)
    if "{sample_link}" in body and not (sample and sample["link"]):
        problems.append("message uses {sample_link} but no sample link is registered")

    # never through a platform whose terms forbid commercial messages (Airbnb, VRBO, Booking, Expedia)
    if identity.automation_forbidden(recipient or "") or identity.automation_forbidden(recipient_source or ""):
        problems.append("recipient is on Airbnb/VRBO/Booking/Expedia: their terms forbid commercial messages through "
                        "the platform or using members' details from it. Use the business's own published channel.")
    # recipient must be a published contact (or you say where it came from)
    if channel == "email":
        e = identity.normalize_email(recipient)
        if not e:
            problems.append(f"'{recipient}' is not a valid email address")
        else:
            row = reg.q1("SELECT summary FROM evidence WHERE business_id=? AND playbook=? AND check_id='_contacts' "
                         "AND current=1", (bid, pid))
            published = {x["email"] for x in json.loads(row["summary"]).get("emails", [])} if row else set()
            if e not in published and not (recipient_source or "").strip():
                problems.append(f"{e} was not found on their site; pass --recipient-source '<where it is published>'")
    elif not (recipient or "").strip():
        problems.append("recipient (profile URL / form URL / number) is empty")
    if kind == "followup" and not parent_touch_id:
        problems.append("follow-up needs --parent <touch id>")
    return problems, sample


def create_draft(reg, playbook, *, bid, channel, recipient, subject, body, evidence_ids, kind="pitch",
                 parent_touch_id=None, recipient_source=None):
    pid = playbook["id"]
    problems, sample = validate(reg, playbook, bid=bid, kind=kind, channel=channel, recipient=recipient,
                                recipient_source=recipient_source, subject=subject, body=body,
                                evidence_ids=evidence_ids, parent_touch_id=parent_touch_id)
    require_sample = kind == "pitch" and playbook["sample"].get("type") != "none" and playbook["sample"].get("required", True)
    decision = gate.can_contact(reg, bid, playbook=pid, channel=channel, recipient=recipient, kind=kind,
                                parent_touch_id=parent_touch_id, require_sample=require_sample)
    status = "invalid" if problems else ("blocked" if not decision.allowed else "draft")
    sample_id = sample["id"] if sample else None
    from .db import now_iso
    did = reg.conn.execute(
        "INSERT INTO drafts (business_id, playbook, kind, parent_touch_id, channel, recipient, recipient_source, subject, "
        "body, evidence_ids, sample_id, status, problems, content_sha, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (bid, pid, kind, parent_touch_id, channel, recipient, recipient_source, subject, body,
         ",".join(str(i) for i in evidence_ids or []), sample_id, status,
         json.dumps(problems + ([] if decision.allowed else decision.reasons)),
         content_sha(channel, recipient, subject, body, sample_id), now_iso())).lastrowid
    if status == "draft":
        p = reg.prospect(bid, pid)
        if p and p["stage"] in ("qualified", "sample_ready"):
            reg.set_stage(bid, pid, "drafted", f"draft #{did}")
    return did, status, problems, decision


def _recheck(reg, playbook, d):
    """Re-validate a stored draft exactly as it would be sent."""
    problems, sample = validate(reg, playbook, bid=reg.resolve(d["business_id"]), kind=d["kind"],
                                channel=d["channel"], recipient=d["recipient"], recipient_source=d["recipient_source"],
                                subject=d["subject"], body=d["body"],
                                evidence_ids=[int(x) for x in (d["evidence_ids"] or "").split(",") if x],
                                parent_touch_id=d["parent_touch_id"])
    if content_sha(d["channel"], d["recipient"], d["subject"], d["body"], d["sample_id"]) != d["content_sha"]:
        problems.append("draft content changed after it was created")
    if sample and d["sample_id"] and sample["id"] != d["sample_id"]:
        problems.append("a newer sample was registered after this draft; create a new draft")
    return problems, sample


def preview(reg, settings, env, d, sample) -> str:
    try:
        body = render(d, sample, settings, env)
    except RuntimeError as e:
        body = d["body"] + f"\n\n[footer missing: {e}]"
    head = [f"Draft #{d['id']} · {reg.label(d['business_id'])} · playbook {d['playbook']} · {d['kind']}",
            f"Channel: {d['channel']}  To: {d['recipient']}"]
    if d["subject"]:
        head.append(f"Subject: {d['subject']}")
    if sample:
        head.append(f"Sample: {sample['link'] or sample['path']}  (label: {sample['label']})")
    return "\n".join(head) + "\n" + "-" * 60 + "\n" + body


def macos_confirm(title: str, text: str) -> bool:
    """Native dialog. An agent driving a shell cannot click it; a person has to."""
    text = text[:1800].replace("\\", "\\\\").replace('"', '\\"')
    title = title.replace('"', "'")
    script = (f'display dialog "{text}" with title "{title}" buttons {{"Skip", "Approve"}} default button "Skip" '
              f'cancel button "Skip" giving up after 600 with icon caution')
    try:
        out = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=650)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
    return "button returned:Approve" in out.stdout and "gave up:true" not in out.stdout


def terminal_confirm(draft_id: int) -> bool:
    if not sys.stdin.isatty():
        return False
    return input(f"Type APPROVE {draft_id} to approve (Enter skips): ").strip() == f"APPROVE {draft_id}"


def approve(reg, settings, env, playbooks_by_id, draft_ids, confirm=None, out=print) -> list:
    approved = []
    for did in draft_ids:
        d = reg.q1("SELECT * FROM drafts WHERE id=?", (did,))
        if not d:
            out(f"draft #{did}: not found")
            continue
        if d["status"] != "draft":
            out(f"draft #{did}: status is '{d['status']}', only 'draft' can be approved")
            continue
        pb = playbooks_by_id(d["playbook"])
        problems, sample = _recheck(reg, pb, d)
        dec = gate.can_contact(reg, d["business_id"], playbook=d["playbook"], channel=d["channel"],
                               recipient=d["recipient"], kind=d["kind"], parent_touch_id=d["parent_touch_id"])
        text = preview(reg, settings, env, d, sample)
        out(text)
        if problems or not dec.allowed:
            out("NOT approvable:\n  - " + "\n  - ".join(problems + dec.reasons))
            continue
        ok = confirm(d, text) if confirm else (
            macos_confirm(f"Approve outreach draft #{did}?", text) if sys.platform == "darwin" else terminal_confirm(did))
        if not ok:
            out(f"draft #{did}: skipped (not approved)")
            continue
        from .db import now_iso
        reg.conn.execute("UPDATE drafts SET status='approved', approved_by=?, approved_at=? WHERE id=?",
                         (getpass.getuser(), now_iso(), did))
        approved.append(did)
        out(f"draft #{did}: APPROVED")
    return approved


def smtp_transport(env):
    def send(to, subject, text, attachment, sender_name):
        user, pwd = env.get("GMAIL_USER"), env.get("GMAIL_APP_PASSWORD")
        if not user or not pwd:
            raise BeforeSendError("GMAIL_USER / GMAIL_APP_PASSWORD not configured")
        msg = EmailMessage()
        msg["From"] = f"{sender_name} <{user}>" if sender_name else user
        msg["To"] = to
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain=user.split("@")[-1])
        msg["Reply-To"] = user
        msg["List-Unsubscribe"] = f"<mailto:{user}?subject=unsubscribe>"
        msg.set_content(text)
        if attachment:
            ctype = mimetypes.guess_type(attachment)[0] or "application/octet-stream"
            main, sub = ctype.split("/", 1)
            msg.add_attachment(Path(attachment).read_bytes(), maintype=main, subtype=sub,
                               filename=Path(attachment).name)
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30)
            server.login(user, pwd)
        except Exception as e:
            raise BeforeSendError(f"{type(e).__name__}: {e}") from e
        try:
            server.send_message(msg)
        finally:
            try:
                server.quit()
            except Exception:
                pass
        return msg["Message-ID"]
    return send


def send(reg, settings, env, playbook, draft_id, live=False, transport=None, out=print) -> str:
    """Returns a short outcome string. Dry-run unless live=True."""
    d = reg.q1("SELECT * FROM drafts WHERE id=?", (draft_id,))
    if not d:
        return f"draft #{draft_id} not found"
    if d["status"] != "approved":
        return f"draft #{draft_id} is '{d['status']}'; only approved drafts can be sent"
    problems, sample = _recheck(reg, playbook, d)
    if problems:
        return "refused, draft no longer valid:\n  - " + "\n  - ".join(problems)
    bid = reg.resolve(d["business_id"])
    require_sample = d["kind"] == "pitch" and playbook["sample"].get("type") != "none" and playbook["sample"].get("required", True)
    kw = dict(playbook=d["playbook"], channel=d["channel"], recipient=d["recipient"], kind=d["kind"],
              parent_touch_id=d["parent_touch_id"], require_sample=require_sample)
    if d["channel"] == "email":
        try:
            text = render(d, sample, settings, env)
        except RuntimeError as e:
            return f"refused: {e}"
    else:
        text = render(d, sample, settings, env)

    if not live:
        dec = gate.can_contact(reg, bid, **kw)
        out(preview(reg, settings, env, d, sample))
        return f"[DRY RUN] nothing sent. Gate: {dec}"

    if d["channel"] == "email" and not settings.get("sending_enabled"):
        return "refused: sending_enabled is false in config/settings.json (a human must switch it on)"

    topic = playbook["offer"]["title"]
    tid, dec = gate.reserve_touch(reg, bid, topic=topic, draft_id=draft_id, **kw)
    if not tid:
        return f"refused by gate:\n{dec}"

    if d["channel"] != "email":
        out(preview(reg, settings, env, d, sample))
        return (f"touch #{tid} reserved as PENDING. Send it yourself on {d['channel']} to {d['recipient']}, then run "
                f"`acq touch resolve {tid} --sent` (or --failed if you did not send it).")

    attachment = sample["path"] if sample and not sample["link"] else None
    send_fn = transport or smtp_transport(env)
    try:
        mid = send_fn(d["recipient"], d["subject"], text, attachment, settings.get("sender_name"))
    except BeforeSendError as e:
        gate.resolve_touch(reg, tid, "FAILED", error=str(e))
        return f"FAILED before sending (nothing went out): {e}"
    except Exception as e:
        gate.resolve_touch(reg, tid, "UNKNOWN", error=f"{type(e).__name__}: {e}")
        return (f"UNKNOWN: error while sending ({e}). Check Gmail Sent, then `acq touch resolve {tid} --sent|--failed`. "
                f"The business stays blocked until you do.")
    gate.resolve_touch(reg, tid, "SENT", message_id=mid)
    return f"SENT touch #{tid} to {d['recipient']} ({mid})"


def followups_due(reg, playbook_ids=None) -> list:
    rows = reg.q("SELECT * FROM touches WHERE state='SENT' AND kind='pitch' AND source='acq' ORDER BY sent_at")
    out = []
    for t in rows:
        if playbook_ids and t["playbook"] not in playbook_ids:
            continue
        dec = gate.can_contact(reg, t["business_id"], playbook=t["playbook"], channel=t["channel"],
                               recipient=t["recipient"] or "", kind="followup", parent_touch_id=t["id"])
        out.append((t, dec))
    return out
