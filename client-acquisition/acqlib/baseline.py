"""GEO protection: a checksum manifest of the existing GEO skill code, verified before and after acq work."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def _excluded(path: Path, excludes) -> bool:
    parts = set(path.parts)
    s = str(path)
    for ex in excludes:
        if "/" in ex:
            if ex in s:
                return True
        elif ex in parts or path.name == ex:
            return True
    return False


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def compute(paths, excludes) -> dict:
    files = {}
    for root in paths:
        root = Path(root)
        if not root.exists():
            continue
        if root.is_file():
            files[str(root)] = sha256_file(root)
            continue
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            dp = Path(dirpath)
            dirnames[:] = [d for d in dirnames if not _excluded(dp / d, excludes)]
            for name in filenames:
                fp = dp / name
                if _excluded(fp, excludes) or fp.is_symlink():
                    continue
                files[str(fp)] = sha256_file(fp)
    return files


def create(settings: dict, out_dir: Path) -> Path:
    files = compute(settings["baseline_paths"], settings.get("baseline_exclude", []))
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = out_dir / f"geo-baseline-{stamp}.json"
    path.write_text(json.dumps({"created": stamp, "file_count": len(files), "files": files}, indent=1))
    return path


def latest(out_dir: Path):
    found = sorted(out_dir.glob("geo-baseline-*.json"))
    return found[0] if found else None  # the FIRST baseline is the reference


def verify(settings: dict, manifest_path: Path) -> dict:
    ref = json.loads(Path(manifest_path).read_text())["files"]
    now = compute(settings["baseline_paths"], settings.get("baseline_exclude", []))
    return {
        "manifest": str(manifest_path),
        "checked": len(ref),
        "changed": sorted(p for p in ref if p in now and now[p] != ref[p]),
        "missing": sorted(p for p in ref if p not in now),
        "added": sorted(p for p in now if p not in ref),
    }
