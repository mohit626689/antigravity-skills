---
name: acq
description: |
  Client Acquisition hub (playbook engine + shared business registry). Use when the user types '/acq', asks for the
  acquisition pipeline status, wants to create a NEW offer/playbook ("I want to sell X to businesses that have problem Y"),
  record a reply / opt-out / meeting / won / lost, suppress a business, resolve duplicate records, or check whether a
  business may be contacted. Works next to the GEO skills without changing them. Related skills: acq-find (see the
  problem), acq-offer (build the sample solution), acq-outreach (message + approval + send).
---

# acq: evidence-first client acquisition

One workflow, many offers. Each offer is a **playbook** (a JSON file). Every playbook runs the same steps:

```
find → see the problem (evidence) → qualify → build a sample solution → write message → HUMAN approval → gated send → track replies
```

All playbooks share ONE registry, so a business is contacted about one thing at a time, never by several
campaigns. GEO's sent emails are read from the GEO ledger automatically and count as contact.

Engine: `python3 /Users/shivpratap/.gemini/config/skills/acq/acq.py <command>` (shortened to `acq` below; always run
the full command). Data: `/Users/shivpratap/Desktop/AI Skills/Client Acquisition/`.

## Hard rules (never break, even if asked mid-task)

1. **Never touch the GEO skill**: no edits, moves or re-runs of anything under `~/.gemini/config/skills/geo*`,
   `Desktop/AI Skills/GEO`, `Shiv Second Brain/scripts`, the GEO ledger or the GEO sheet.
2. **You (the Antigravity agent) are the only LLM.** Do not add calls to any LLM API. The engine is deterministic.
3. **Never edit `config/settings.json` `sending_enabled`, `config/policy.json`, or `registry.db` directly.** Only the user
   changes them. Never bypass the engine with your own SMTP/browser sending.
4. **Never run `acq send ... --live`** unless the user said, in this conversation, to send those exact draft ids.
5. **Only state what the evidence says.** Findings come from `acq show <business>`. Anything else is a hypothesis
   and must be worded as one ("may", "could"). No invented numbers, reviews, results or urgency.
6. If a command says BLOCKED, report the reasons to the user. Do not look for a workaround.
7. **Never open Airbnb, VRBO, Booking.com or Expedia pages with the browser or any tool.** Their terms forbid bots
   and automated access, and messaging hosts through them commercially. The user views those sites themselves and
   tells you what they saw. Never download their photos, copy their text, or look up private individuals' contact details.
   Contact only businesses, through channels the business itself publishes.

## Commands you will use from this hub

| Need | Command |
|---|---|
| First-time setup / import GEO history | `acq init` |
| Pipeline overview | `acq status` |
| Everything about one business | `acq show <domain or #id>` |
| May we contact them? | `acq gate <business> --playbook <id> --channel email --to <addr>` |
| They replied / booked / said no | `acq outcome <business> replied|meeting|won|lost|not_interested|opt_out|bounced [--note ..] [--email ..]` |
| Do-not-contact | `acq suppress <value> --kind email|domain|phone|business --reason "..."` |
| Possible duplicates | `acq review list` then `acq review resolve <id> --same-as <id>` or `--distinct` |
| Country missing | `acq set-country <business> US` |
| Unresolved send | `acq touch list --pending` then `acq touch resolve <id> --sent|--failed` (ask the user what actually went out) |
| GEO protection check | `acq baseline verify` (must print "GEO files unchanged") |
| Before the user runs /geo-message | `~/.gemini/config/skills/geo/.venv/bin/python3 ~/.gemini/config/skills/acq/acq.py guard-geo` |
| Pull non-email GEO sends + replies from the sheet | `~/.gemini/config/skills/geo/.venv/bin/python3 ~/.gemini/config/skills/acq/acq.py import geo --sheet` (add `--dry-run` first) |
| Export to CSV | `acq export` |

## Creating a new playbook (new offer)

When the user describes an offer ("people with photo-only listings → I make them a video"):

1. Ask only what you cannot infer: who exactly, where to find them **legally** (Google Places, their own sites, a CSV
   they collect; NOT scraping platforms that forbid it, such as Airbnb), what observable problem proves the need,
   what a willingness-to-pay signal is, what sample you will make, which channels.
2. Copy `playbooks/_template.json` to `playbooks/<id>.json` and fill it in. Each problem must be **observable** with a
   check type (`element`, `link`, `text`, `count`, `jsonld_type`, `https`) or a `manual` check with a source URL.
   Willingness-to-pay signals (e.g. Meta Ad Library) go in `qualify.signals`. They raise priority but are never proof.
3. Run `acq playbook validate <id>` and fix every error.
4. Show the user the playbook summary and wait for their OK before running it.

Existing playbooks: `acq playbook list`.

## Policy the gate enforces (config/policy.json, edited only by the user)

90-day cooldown after any message on any topic; an unanswered pitch is not re-pitched automatically; at most 1
follow-up 3-21 days after the pitch; max 3 messages per business per year; 5 emails per 24h shared with GEO; no
new pitch while a conversation is active; opt-outs, bounces and "not interested" are permanent; US only; records
flagged for duplicate review are blocked until resolved. These are the user's starting values, not legal advice.
