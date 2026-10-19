# acq: client acquisition playbooks

The GEO workflow idea (find → check → evidence → report → reach out), generalized: **one engine, many offers**.
Each offer is a playbook JSON file. The GEO skill itself is untouched; acq only reads GEO's ledger, audit index and
(optionally) sheet.

```
                 playbooks/*.json  (what problem, what proof, what sample, what message rules)
                          │
 acq-find   ─ find ─► registry ◄─ GEO ledger / audit index / sheet (read-only)
            ─ check ─► evidence (OBSERVED / UNVERIFIED / NOT_CHECKED, with page + date)
            ─ qualify (all_of problem checks observed; signals = priority)
 acq-offer  ─ sample prepare (brief + their own assets) → agent builds sample → sample register
 acq-outreach ─ agent writes message → draft create (validated) → approve (macOS dialog, human)
            ─ send: gate re-check → PENDING touch → SMTP / manual → SENT | FAILED | UNKNOWN
 acq        ─ outcome / suppress / review / status / export / baseline
```

## Layout

| Path | What |
|---|---|
| `~/.gemini/config/skills/acq/` | hub skill, engine (`acq.py`, `acqlib/`), `config/`, `playbooks/`, `tests/` |
| `~/.gemini/config/skills/acq-find/`, `acq-offer/`, `acq-outreach/` | step skills (SKILL.md only) |
| `~/Desktop/AI Skills/Client Acquisition/` | data: `registry.db`, `evidence/`, `samples/`, `exports/`, `baseline/` |

## Safety design

- **Antigravity is the only LLM.** The engine is standard-library Python with no LLM calls (a test enforces it).
  The agent writes messages and builds samples; the engine validates them.
- **One business, one record**: domain (registrable, platform-aware), platform profile, Places id, Maps URL, phone,
  email. A name+city match alone is never merged; it goes to `acq review`.
- **One conversation per business**: `policy.can_contact()` is the only path to a send. It covers suppression,
  cooldown across all topics, no re-pitch of unanswered businesses, follow-up limits, a yearly cap, the 24h email cap
  shared with GEO, no pitch while a conversation is active, allowed countries, duplicate-review holds, and
  unresolved-send holds.
- **No duplicate sends after a crash**: the gate check and a `PENDING` touch are written in one transaction before
  sending. A send that errors mid-way becomes `UNKNOWN` and blocks the business until a human resolves it.
- **Human gates**: drafts need approval in a native macOS dialog, which an agent cannot click.
  Email also needs `sending_enabled: true` in `config/settings.json` (off by default), plus `--live`.
- **Evidence honesty**: absence is only claimed for the pages checked, never on JS-rendered pages. Manual findings
  need a source URL to count. Drafts must cite observed problem evidence. Numbers must come from that evidence.
  Forbidden hype phrases are rejected. An unusable homepage means rejected, so it can never reach outreach.
- **GEO protection**: `acq baseline verify` compares 363 GEO files with the checksum taken before acq existed.

## Platforms that forbid automation (Airbnb, VRBO, Booking, Expedia)

Airbnb's Terms (11.1) forbid bots, scrapers and automated access, and using its messaging or members' personal
information to send commercial messages. The engine therefore never fetches these domains or their image CDNs,
and rejects them as outreach recipients. Listing links are stored only as identity (airbnb.com/.co.in/.co.uk count
as one listing). Observations come from the user's own browsing (research CSV or `acq evidence add`). Playbook
`str-listing-upgrade` targets multi-listing host businesses and contacts them only through their own channels.

## Known limits

- `normalize` uses a short public-suffix list; uncommon country domains may need adding to `identity.py`.
- Contact detection reads raw HTML; JavaScript-only sites need a human check in the browser (`acq evidence add`).
- Replies are not read automatically; record them with `acq outcome`.
- GEO's `/geo-message` does not consult the registry. Run `acq guard-geo` (GEO venv python) before using it.
- Google Places data has caching terms; acq stores the same fields GEO already stores.

## Test

```bash
python3 -B -m unittest discover -s ~/.gemini/config/skills/acq/tests -v
python3 -B ~/.gemini/config/skills/acq/acq.py baseline verify
```

## Roll back

Delete `~/.gemini/config/skills/acq*` and `~/Desktop/AI Skills/Client Acquisition/`. Nothing else was changed.
