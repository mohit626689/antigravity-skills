from __future__ import annotations

import json
import os
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = SKILL_DIR / "config"
PLAYBOOK_DIR = SKILL_DIR / "playbooks"


def load_json(path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_settings() -> dict:
    """settings.json, with ACQ_SETTINGS / ACQ_DATA_DIR overrides (used by tests)."""
    s = load_json(os.environ.get("ACQ_SETTINGS", CONFIG_DIR / "settings.json"))
    s["data_dir"] = Path(os.environ.get("ACQ_DATA_DIR", s["data_dir"]))
    return s


def load_policy() -> dict:
    return load_json(os.environ.get("ACQ_POLICY", CONFIG_DIR / "policy.json"))


def load_env(settings: dict) -> dict:
    """Read KEY=VALUE files read-only. Real environment variables win, then the first file that defines a key."""
    env: dict = {}
    for p in settings.get("env_files", []):
        if not os.path.exists(p):
            continue
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip("\"'")
            if v and k not in env:
                env[k] = v
    for k, v in os.environ.items():
        if v:
            env[k] = v
    return env


def data_paths(settings: dict) -> dict:
    d = Path(settings["data_dir"])
    return {
        "root": d,
        "db": d / "registry.db",
        "evidence": d / "evidence",
        "samples": d / "samples",
        "exports": d / "exports",
        "baseline": d / "baseline",
        "places_usage": d / "places_usage.json",
    }


def ensure_data_dirs(settings: dict) -> dict:
    p = data_paths(settings)
    for key in ("root", "evidence", "samples", "exports", "baseline"):
        p[key].mkdir(parents=True, exist_ok=True)
    return p
