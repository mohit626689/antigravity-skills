"""SQLite registry: the single source of truth for businesses, evidence, samples, drafts, touches and suppression."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS businesses (
    id            INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    website       TEXT,
    city          TEXT,
    region        TEXT,
    country       TEXT,
    status        TEXT NOT NULL DEFAULT 'new',      -- new|contacted|replied|meeting|client|lost|not_interested|opted_out|do_not_contact|merged
    needs_review  INTEGER NOT NULL DEFAULT 0,
    review_note   TEXT,
    merged_into   INTEGER REFERENCES businesses(id),
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS identifiers (
    kind        TEXT NOT NULL,                       -- domain|profile|place|maps|phone|email|name_city
    value       TEXT NOT NULL,
    business_id INTEGER NOT NULL REFERENCES businesses(id),
    source      TEXT,
    created_at  TEXT NOT NULL,
    PRIMARY KEY (kind, value)
);
CREATE INDEX IF NOT EXISTS ix_identifiers_business ON identifiers(business_id);
CREATE TABLE IF NOT EXISTS prospects (
    id          INTEGER PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES businesses(id),
    playbook    TEXT NOT NULL,
    stage       TEXT NOT NULL,                       -- found|skipped|checked|needs_check|rejected|qualified|sample_ready|drafted|contacted
    reason      TEXT,
    priority    INTEGER NOT NULL DEFAULT 0,
    source      TEXT,
    source_url  TEXT,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL,
    UNIQUE (business_id, playbook)
);
CREATE TABLE IF NOT EXISTS evidence (
    id          INTEGER PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES businesses(id),
    playbook    TEXT NOT NULL,
    check_id    TEXT NOT NULL,
    status      TEXT NOT NULL,                       -- OBSERVED|HYPOTHESIS|UNVERIFIED|NOT_CHECKED|ERROR
    hit         INTEGER,                             -- 1 condition true, 0 false, NULL unknown
    summary     TEXT NOT NULL,
    source_url  TEXT,
    run_file    TEXT,
    method      TEXT NOT NULL,                       -- auto|manual
    observed_at TEXT NOT NULL,
    current     INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS ix_evidence_lookup ON evidence(business_id, playbook, check_id, current);
CREATE TABLE IF NOT EXISTS opportunities (
    id          INTEGER PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES businesses(id),
    playbook    TEXT NOT NULL,
    title       TEXT NOT NULL,
    basis       TEXT NOT NULL,                       -- OBSERVED|HYPOTHESIS
    evidence_id INTEGER REFERENCES evidence(id),
    status      TEXT NOT NULL DEFAULT 'open',        -- open|pitched|closed
    created_at  TEXT NOT NULL,
    UNIQUE (business_id, playbook, title)
);
CREATE TABLE IF NOT EXISTS samples (
    id          INTEGER PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES businesses(id),
    playbook    TEXT NOT NULL,
    path        TEXT,
    link        TEXT,
    label       TEXT NOT NULL,
    sha256      TEXT,
    size_bytes  INTEGER,
    created_at  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS drafts (
    id              INTEGER PRIMARY KEY,
    business_id     INTEGER NOT NULL REFERENCES businesses(id),
    playbook        TEXT NOT NULL,
    kind            TEXT NOT NULL,                   -- pitch|followup
    parent_touch_id INTEGER REFERENCES touches(id),
    channel         TEXT NOT NULL,
    recipient       TEXT NOT NULL,
    recipient_source TEXT,
    subject         TEXT,
    body            TEXT NOT NULL,
    evidence_ids    TEXT,
    sample_id       INTEGER REFERENCES samples(id),
    status          TEXT NOT NULL,                   -- invalid|blocked|draft|approved|rejected|sent|cancelled
    problems        TEXT,
    content_sha     TEXT NOT NULL,
    approved_by     TEXT,
    approved_at     TEXT,
    created_at      TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS touches (
    id              INTEGER PRIMARY KEY,
    business_id     INTEGER NOT NULL REFERENCES businesses(id),
    playbook        TEXT NOT NULL,
    kind            TEXT NOT NULL,                   -- pitch|followup
    channel         TEXT NOT NULL,
    recipient       TEXT,
    topic           TEXT,
    state           TEXT NOT NULL,                   -- PENDING|SENT|FAILED|UNKNOWN
    idempotency_key TEXT NOT NULL UNIQUE,
    parent_touch_id INTEGER REFERENCES touches(id),
    draft_id        INTEGER REFERENCES drafts(id),
    message_id      TEXT,
    error           TEXT,
    source          TEXT NOT NULL,                   -- acq|geo-ledger|geo-sheet
    created_at      TEXT NOT NULL,
    sent_at         TEXT
);
CREATE INDEX IF NOT EXISTS ix_touches_business ON touches(business_id);
CREATE TABLE IF NOT EXISTS suppression (
    id         INTEGER PRIMARY KEY,
    kind       TEXT NOT NULL,                        -- business|domain|email|phone
    value      TEXT NOT NULL,
    reason     TEXT NOT NULL,
    source     TEXT,
    created_at TEXT NOT NULL,
    UNIQUE (kind, value)
);
CREATE TABLE IF NOT EXISTS searches (
    id          INTEGER PRIMARY KEY,
    playbook    TEXT NOT NULL,
    query_text  TEXT NOT NULL,
    results     INTEGER NOT NULL,
    searched_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_searches ON searches(playbook, query_text);
CREATE TABLE IF NOT EXISTS events (
    id          INTEGER PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id),
    type        TEXT NOT NULL,
    note        TEXT,
    created_at  TEXT NOT NULL
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_iso(text: str) -> datetime:
    dt = datetime.fromisoformat(text)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def connect(path) -> sqlite3.Connection:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=30, isolation_level=None)  # autocommit; explicit BEGIN where needed
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.executescript(SCHEMA)
    return conn
