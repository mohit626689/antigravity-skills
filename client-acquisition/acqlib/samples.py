"""Sample solutions: a brief the Antigravity agent builds the sample from, and registration of the finished file."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from . import checks, identity
from .config import data_paths

IMAGE_EXCLUDE = re.compile(
    r"logo|icon|favicon|sprite|pixel|tracking|gravatar|badge|spinner|loader|placeholder|1x1|blank\.|\.svg(\?|$)|"
    r"maps\.googleapis|maps\.gstatic|facebook\.com/tr|doubleclick|google-analytics|googletagmanager|"
    r"ssl\.gstatic|/emoji/|wpforms|recaptcha", re.I)
EXT = {"image/jpeg": ".jpg", "image/jpg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif",
       "image/avif": ".avif"}
READY = ("qualified", "sample_ready", "drafted")


def sample_dir(reg, bid, pid) -> Path:
    key = reg.primary_domain(bid) or f"business-{bid}"
    d = data_paths(reg.settings)["samples"] / key / pid
    d.mkdir(parents=True, exist_ok=True)
    return d


def prepare(reg, fetcher, playbook: dict, bid: int, download_images: int = 0) -> Path:
    pid = playbook["id"]
    p = reg.prospect(bid, pid)
    if not p or p["stage"] not in READY:
        raise RuntimeError(f"{reg.label(bid)} is not qualified for {pid} (stage: {p['stage'] if p else 'none'})")
    b = reg.business(bid)
    ev = reg.current_evidence(bid, pid)
    run = checks.latest_run(reg, bid, pid) or {}
    out = sample_dir(reg, bid, pid)

    problems, observations = [], []
    for c in playbook["checks"]:
        e = ev.get(c["id"])
        if not e or e["status"] != "OBSERVED" or e["hit"] != 1:
            continue
        item = {"evidence_id": e["id"], "check": c["id"], "label": c["label"], "summary": e["summary"],
                "source_url": e["source_url"], "observed_at": e["observed_at"], "method": e["method"]}
        (problems if c.get("problem") else observations).append({**item, "problem": c.get("problem")}
                                                                if c.get("problem") else item)

    images = [u for u in run.get("images", []) if u.startswith("http") and not IMAGE_EXCLUDE.search(u)
              and not identity.automation_forbidden(u)]
    platform_refs = [f"https://www.{i['value']}" for i in reg.identifiers(bid)
                     if i["kind"] == "profile" and identity.automation_forbidden(i["value"])]
    downloaded = []
    if download_images and images:
        assets = out / "assets"
        assets.mkdir(exist_ok=True)
        for i, url in enumerate(images[: download_images * 2], 1):
            if len(downloaded) >= download_images:
                break
            tmp = assets / f"img-{len(downloaded) + 1:02d}"
            ctype = fetcher.download(url, tmp)
            if not ctype:
                continue
            final = tmp.with_suffix(EXT.get(ctype.split(";")[0].strip(), ".img"))
            tmp.rename(final)
            downloaded.append({"file": str(final), "source_url": url,
                               "sha256": hashlib.sha256(final.read_bytes()).hexdigest()})

    sample = playbook["sample"]
    brief = {
        "business": {"id": bid, "name": b["name"], "website": b["website"], "domain": reg.primary_domain(bid),
                     "city": b["city"], "region": b["region"], "country": b["country"]},
        "playbook": pid,
        "offer": playbook["offer"],
        "observed_problems": problems,
        "other_observations": observations,
        "hypotheses_not_verified": playbook.get("hypotheses", []),
        "sample": sample,
        "assets": {"image_urls_from_their_site": images[:40], "downloaded": downloaded},
        "contacts": run.get("contacts", {}),
        "platform_references_do_not_copy": platform_refs,
        "rules": [
            *(["Airbnb/VRBO/Booking links are references for the human only. Do not open them with Antigravity, do "
               "not download their photos, do not paste their text. Describe gaps in your own words."]
              if platform_refs else []),
            "Build the sample ONLY from the assets listed here (their own published material) or clearly synthetic "
            "placeholders. Never use other businesses' content or stock photos presented as theirs.",
            f"Show this label with the sample: \"{sample.get('label', '')}\"",
            "Keep the sample private: an unlisted link or an attachment. Never post it publicly.",
            "No invented facts, numbers, reviews, prices or results about the business.",
            "Anything in hypotheses_not_verified must be phrased as a possibility, never as a finding.",
        ],
        "register_with": f"acq sample register {bid} --playbook {pid} --file <path> [--link <unlisted url>]",
    }
    (out / "brief.json").write_text(json.dumps(brief, indent=1, ensure_ascii=False))
    md = [f"# Sample brief: {b['name']} ({pid})", "", f"**Offer:** {playbook['offer']['title']}", "",
          "## Observed problems (evidence)"]
    md += [f"- [E{x['evidence_id']}] {x['problem']}: {x['summary']} ({x['source_url']})" for x in problems] or ["- none"]
    md += ["", "## Not verified (say 'may', never state as fact)"]
    md += [f"- {h}" for h in playbook.get("hypotheses", [])] or ["- none"]
    if platform_refs:
        md += ["", "## Listing references (view yourself; never copy photos or text)"] + [f"- {u}" for u in platform_refs]
    md += ["", "## Sample to build", f"- Type: {sample.get('type')}", f"- Label: {sample.get('label')}",
           f"- Instructions: {sample.get('instructions', '')}", "", "## Assets from their site"]
    md += [f"- {d['file']}  ←  {d['source_url']}" for d in downloaded] or [f"- {u}" for u in images[:15]] or ["- none"]
    md += ["", "## Rules"] + [f"- {r}" for r in brief["rules"]] + ["", f"Register: `{brief['register_with']}`"]
    (out / "brief.md").write_text("\n".join(md))
    return out


def register(reg, playbook: dict, bid: int, file: str = None, link: str = None) -> int:
    pid = playbook["id"]
    p = reg.prospect(bid, pid)
    if not p or p["stage"] not in READY:
        raise RuntimeError(f"{reg.label(bid)} is not qualified for {pid} (stage: {p['stage'] if p else 'none'})")
    if not file and not link:
        raise ValueError("give --file and/or --link")
    sha = size = None
    if file:
        fp = Path(file).expanduser()
        if not fp.is_file():
            raise FileNotFoundError(file)
        sha = hashlib.sha256(fp.read_bytes()).hexdigest()
        size = fp.stat().st_size
        file = str(fp.resolve())
    if link and not re.match(r"^https?://", link):
        raise ValueError("--link must be an http(s) URL")
    if link and identity.registrable_domain(link) == reg.primary_domain(bid):
        raise ValueError("--link points at the prospect's own site; use your private/unlisted sample link")
    sid = reg.add_sample(bid, pid, path=file, link=link, label=playbook["sample"].get("label", ""), sha256=sha,
                         size_bytes=size)
    if p["stage"] == "qualified":
        reg.set_stage(bid, pid, "sample_ready", "sample registered")
    return sid
