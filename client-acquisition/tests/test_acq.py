"""Acceptance tests for the acq engine. Run: python3 -B -m unittest discover -s ~/.gemini/config/skills/acq/tests -v

No network, no real email: pages come from FakeFetcher and sending uses a fake transport.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL))
sys.dont_write_bytecode = True

from acqlib import checks, discover, identity, outreach, playbooks, samples, web  # noqa: E402
from acqlib import policy as gate  # noqa: E402
from acqlib.config import load_json, load_policy  # noqa: E402
from acqlib.db import connect  # noqa: E402
from acqlib.registry import Registry  # noqa: E402

NOW = datetime.now(timezone.utc)


class FakeFetcher:
    """Serves fixture HTML by URL. Unknown URLs behave like a DNS failure."""

    def __init__(self, pages):
        self.pages = pages

    def fetch(self, url):
        if url not in self.pages:
            return web.Page(url=url, error="URLError: name not resolved")
        status, html = self.pages[url]
        return web.Page(url=url, final_url=url, status=status, content_type="text/html; charset=utf-8", html=html,
                        error="" if status == 200 else f"HTTP {status}")

    def download(self, url, dest, **kw):
        return None


def site(images=10, video=False, tel=True, email="hello@sunnycabins.test", js_shell=False, links=True):
    imgs = "".join(f'<img src="/photos/cabin-{i}.jpg" alt="cabin {i}">' for i in range(images))
    vid = '<iframe src="https://www.youtube.com/embed/abc123"></iframe>' if video else ""
    nav = ('<a href="https://sunnycabins.test/gallery">Gallery</a><a href="https://sunnycabins.test/contact">Contact</a>'
           if links else "")
    body = (f"<h1>Sunny Cabins</h1><p>{'Lakeside cabins with fireplaces and hot tubs near the trail head. ' * 8}</p>"
            f"{nav}{imgs}{vid}" + (f'<a href="tel:+15125550100">Call</a>' if tel else "") +
            (f'<a href="mailto:{email}">Email us</a>' if email else ""))
    if js_shell:
        body = '<div id="root"></div><script src="/a.js"></script><script src="/b.js"></script>'
    return f"<html><head><title>Sunny Cabins</title></head><body>{body}</body></html>"


def manager_site(domain, gaps=True):
    """A rental manager's own website: homepage linking two property pages."""
    base = f"https://{domain}"
    nav = (f'<a href="{base}/properties/lake-house">Lake House</a><a href="{base}/properties/river-cabin">River Cabin</a>'
           f'<a href="mailto:stay@{domain}">Email</a>')
    intro = "<p>" + "We manage vacation homes across the valley with local care and fast replies. " * 10 + "</p>"
    home = f"<html><body><h1>{domain}</h1>{intro}{nav}</body></html>"
    if gaps:
        detail = lambda n: (f"<html><body><h1>Property</h1><p>Sleeps 6 · 3 bedrooms · 2 baths</p>{intro}" +
                            "".join(f'<img src="/img/p{i}.jpg">' for i in range(n)) + "</body></html>")
        return {base: (200, home), f"{base}/properties/lake-house": (200, detail(6)),
                f"{base}/properties/river-cabin": (200, detail(20))}
    full = (f"<html><body>{intro}<p>Sleeps 8, 4 bedrooms. Free parking for two cars. Self check-in with a keypad.</p>"
            '<iframe src="https://www.youtube.com/embed/x"></iframe>' +
            "".join(f'<img src="/img/q{i}.jpg">' for i in range(25)) + "</body></html>")
    return {base: (200, home), f"{base}/properties/lake-house": (200, full), f"{base}/properties/river-cabin": (200, full)}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="acq-test-"))
        self.ledger = self.tmp / "ledger.jsonl"
        self.ledger.write_text("")
        self.settings = {
            "data_dir": self.tmp / "data", "sending_enabled": False, "sender_name": "Test Sender",
            "business_name": "TestWorks", "env_files": [], "own_domains": ["mine.test"], "attachment_max_mb": 15,
            "geo": {"ledger": str(self.ledger), "audit_index": str(self.tmp / "none.json"),
                    "places_usage": str(self.tmp / "geo_usage.json")},
            "places_monthly_limit_combined": 900, "http": {},
        }
        self.policy = load_policy()
        self.reg = Registry(connect(self.tmp / "data" / "registry.db"), self.settings, self.policy)
        self.pb = playbooks.load("listing-video")
        self.env = {"POSTAL_ADDRESS": "1 Test St, Austin TX 78701"}

    def tearDown(self):
        self.reg.conn.close()

    def qualified_business(self, html=None, name="Sunny Cabins", domain="sunnycabins.test"):
        bid, _ = self.reg.upsert_business(name=name, website=f"https://{domain}", country="US", city="Austin",
                                          source="test")
        self.reg.ensure_prospect(bid, self.pb["id"])
        pages = {f"https://{domain}": (200, html or site()),
                 f"https://{domain}/gallery": (200, site()), f"https://{domain}/contact": (200, site())}
        res = checks.check_business(self.reg, FakeFetcher(pages), self.pb, bid)
        return bid, res

    def problem_evidence(self, bid):
        ev = self.reg.current_evidence(bid, self.pb["id"])
        return [ev["no_video"]["id"], ev["many_photos"]["id"]]

    def ready_draft(self, bid, link="https://drive.example.org/sample-1"):
        samples.register(self.reg, self.pb, bid, link=link)
        return outreach.create_draft(
            self.reg, self.pb, bid=bid, channel="email", recipient="hello@sunnycabins.test",
            subject="A short video from your cabin photos",
            body="Hi, I noticed your property pages show photos but no video. I made a short sample from your "
                 "own photos: {sample_link} Would a version for each property be useful?",
            evidence_ids=self.problem_evidence(bid))


class TestIdentity(Base):
    def test_url_variants_are_one_domain(self):
        variants = ["https://www.SunnyCabins.test/", "sunnycabins.test", "http://sunnycabins.test:8080/book?x=1",
                    "https://book.sunnycabins.test/rooms", "HTTPS://SUNNYCABINS.TEST#top"]
        self.assertEqual({identity.domain_key(v) for v in variants}, {"sunnycabins.test"})
        self.assertEqual(identity.registrable_domain("https://shop.example.co.uk/x"), "example.co.uk")
        self.assertNotEqual(identity.domain_key("a.lovable.app"), identity.domain_key("b.lovable.app"))
        self.assertEqual(identity.domain_key("https://www.airbnb.com/rooms/123"), "")
        self.assertEqual(identity.profile_key("https://www.airbnb.com/rooms/123/"), "airbnb.com/rooms/123")
        self.assertEqual(identity.normalize_phone("(512) 555-0100", "US"), "+15125550100")
        self.assertEqual(identity.normalize_phone("555-0100", "GB"), "")

    def test_dedupe_across_formats(self):
        a, how_a = self.reg.upsert_business(name="Sunny Cabins", website="https://www.sunnycabins.test/", source="t")
        b, how_b = self.reg.upsert_business(name="Sunny Cabins LLC", website="sunnycabins.test/book", source="t")
        c, how_c = self.reg.upsert_business(name="SUNNY CABINS", phone="+1 512 555 0100", website="http://sunnycabins.test",
                                            source="t")
        d, how_d = self.reg.upsert_business(name="Sunny Cabins (Lake)", phone="512.555.0100", country="US", source="t")
        self.assertEqual((how_a, how_b, how_c, how_d), ("new", "matched", "matched", "matched"))
        self.assertEqual(len({a, b, c, d}), 1)
        self.assertEqual(self.reg.q1("SELECT COUNT(*) n FROM businesses")["n"], 1)

    def test_name_only_match_goes_to_review_not_merge(self):
        a, _ = self.reg.upsert_business(name="Acme Dental, LLC", website="acmedental.test", city="Austin", source="t")
        b, how = self.reg.upsert_business(name="ACME Dental", website="acme-dental-austin.test", city="Austin", source="t")
        self.assertNotEqual(a, b)
        self.assertEqual(how, "review")
        self.assertTrue(self.reg.business(b)["needs_review"])
        self.reg.merge(b, a)
        self.assertEqual(self.reg.find("acme-dental-austin.test"), a)

    def test_many_opportunities_one_business(self):
        bid, _ = self.reg.upsert_business(name="Sunny Cabins", website="sunnycabins.test", source="t")
        self.reg.add_opportunity(bid, "geo", "GEO readiness 51", "OBSERVED")
        self.reg.add_opportunity(bid, "listing-video", "No video", "OBSERVED")
        self.reg.add_opportunity(bid, "website-conversion", "No booking link", "OBSERVED")
        self.assertEqual(self.reg.q1("SELECT COUNT(*) n FROM opportunities WHERE business_id=?", (bid,))["n"], 3)


class TestEvidence(Base):
    def test_photo_only_site_qualifies_with_observed_evidence(self):
        bid, res = self.qualified_business()
        self.assertEqual(res["stage"], "qualified", res["reason"])
        ev = self.reg.current_evidence(bid, self.pb["id"])
        self.assertEqual((ev["no_video"]["status"], ev["no_video"]["hit"]), ("OBSERVED", 1))
        self.assertIn("Scope: these pages only", ev["no_video"]["summary"])
        opp = self.reg.q("SELECT basis, title FROM opportunities WHERE business_id=?", (bid,))
        self.assertIn("OBSERVED", {o["basis"] for o in opp})
        self.assertIn("HYPOTHESIS", {o["basis"] for o in opp})

    def test_site_with_video_is_rejected(self):
        _, res = self.qualified_business(html=site(video=True))
        self.assertEqual(res["stage"], "rejected")

    def test_js_rendered_absence_is_unverified_not_a_finding(self):
        pages = [(p, web.parse(p)) for p in [FakeFetcher({"https://x.test": (200, site(js_shell=True))}).fetch("https://x.test")]]
        qa, results = checks.evaluate(self.pb, pages)
        by = {r["check_id"]: r for r in results}
        self.assertEqual(by["no_video"]["status"], "UNVERIFIED")
        self.assertIsNone(by["no_video"]["hit"])
        bid, res = self.qualified_business(html=site(js_shell=True))
        self.assertEqual(res["stage"], "needs_check")

    def test_failed_site_never_reaches_outreach(self):
        bid, _ = self.reg.upsert_business(name="Dead Site", website="https://dead.test", country="US", source="t")
        self.reg.ensure_prospect(bid, self.pb["id"])
        res = checks.check_business(self.reg, FakeFetcher({}), self.pb, bid)
        self.assertEqual(res["stage"], "rejected")
        with self.assertRaises(RuntimeError):
            samples.register(self.reg, self.pb, bid, link="https://drive.example.org/x")
        d = gate.can_contact(self.reg, bid, playbook=self.pb["id"], channel="email", recipient="a@dead.test")
        self.assertFalse(d.allowed)
        self.assertTrue(any("not qualified" in r for r in d.reasons))

    def test_manual_signal_without_source_is_hypothesis(self):
        bid, _ = self.qualified_business()
        self.reg.add_evidence(bid, self.pb["id"], "runs_ads", "HYPOTHESIS", True, "I think they run ads", method="manual")
        _, _, priority = checks.qualify(self.reg, bid, self.pb)
        self.assertEqual(priority, 0)
        self.reg.add_evidence(bid, self.pb["id"], "runs_ads", "OBSERVED", True, "2 active ads",
                              source_url="https://www.facebook.com/ads/library/?q=sunny", method="manual")
        _, _, priority = checks.qualify(self.reg, bid, self.pb)
        self.assertEqual(priority, 1)


class TestDrafts(Base):
    def test_valid_draft(self):
        bid, _ = self.qualified_business()
        did, status, problems, dec = self.ready_draft(bid)
        self.assertEqual(status, "draft", (problems, dec.reasons))

    def test_unsupported_claims_are_rejected(self):
        bid, _ = self.qualified_business()
        samples.register(self.reg, self.pb, bid, link="https://drive.example.org/s")
        _, status, problems, _ = outreach.create_draft(
            self.reg, self.pb, bid=bid, channel="email", recipient="hello@sunnycabins.test", subject="Quick idea",
            body="Video is guaranteed to get you 40% more bookings. See {sample_link}", evidence_ids=self.problem_evidence(bid))
        self.assertEqual(status, "invalid")
        text = " ".join(problems)
        self.assertIn("guarantee", text)
        self.assertIn("40", text)

    def test_scope_numbers_do_not_back_claims(self):
        bid, _ = self.qualified_business()
        samples.register(self.reg, self.pb, bid, link="https://drive.example.org/s")
        ev = self.problem_evidence(bid)
        _, status, problems, _ = outreach.create_draft(
            self.reg, self.pb, bid=bid, channel="email", recipient="hello@sunnycabins.test", subject="Idea",
            body="Video could bring 3x the views. Sample: {sample_link}", evidence_ids=ev)
        self.assertEqual(status, "invalid")
        self.assertTrue(any("numbers not backed" in p and "3" in p for p in problems), problems)
        _, status, problems, _ = outreach.create_draft(
            self.reg, self.pb, bid=bid, channel="email", recipient="hello@sunnycabins.test", subject="Idea",
            body="I counted 10 photos on your pages but no video. Sample: {sample_link}", evidence_ids=ev)
        self.assertEqual(status, "draft", problems)

    def test_pitch_needs_observed_problem_evidence(self):
        bid, _ = self.qualified_business()
        samples.register(self.reg, self.pb, bid, link="https://drive.example.org/s")
        hyp = self.reg.add_evidence(bid, self.pb["id"], "runs_ads", "HYPOTHESIS", True, "guess", method="manual")
        for ev in ([], [hyp]):
            _, status, problems, _ = outreach.create_draft(
                self.reg, self.pb, bid=bid, channel="email", recipient="hello@sunnycabins.test", subject="Idea",
                body="I made a sample: {sample_link}", evidence_ids=ev)
            self.assertEqual(status, "invalid", problems)

    def test_recipient_must_be_published(self):
        bid, _ = self.qualified_business()
        samples.register(self.reg, self.pb, bid, link="https://drive.example.org/s")
        _, status, problems, _ = outreach.create_draft(
            self.reg, self.pb, bid=bid, channel="email", recipient="owner@gmail.com", subject="Idea",
            body="No video on your pages; sample: {sample_link}", evidence_ids=self.problem_evidence(bid))
        self.assertEqual(status, "invalid")
        self.assertTrue(any("not found on their site" in p for p in problems))


class TestGateAndSending(Base):
    def approve(self, did):
        return outreach.approve(self.reg, self.settings, self.env, playbooks.load, [did],
                                confirm=lambda d, t: True, out=lambda *a: None)

    def test_dry_run_live_switch_and_no_duplicate(self):
        bid, _ = self.qualified_business()
        did, status, *_ = self.ready_draft(bid)
        self.assertEqual(self.approve(did), [did])
        sent = []
        fake = lambda to, subj, text, att, name: sent.append((to, text)) or "<msg-1@test>"
        r = outreach.send(self.reg, self.settings, self.env, self.pb, did, live=False, transport=fake, out=lambda *a: None)
        self.assertIn("DRY RUN", r)
        self.assertEqual((sent, self.reg.q("SELECT * FROM touches")), ([], []))
        r = outreach.send(self.reg, self.settings, self.env, self.pb, did, live=True, transport=fake)
        self.assertIn("sending_enabled is false", r)
        self.settings["sending_enabled"] = True
        r = outreach.send(self.reg, self.settings, self.env, self.pb, did, live=True, transport=fake)
        self.assertTrue(r.startswith("SENT"), r)
        self.assertIn("drive.example.org/sample-1", sent[0][1])
        self.assertIn("1 Test St", sent[0][1])
        r = outreach.send(self.reg, self.settings, self.env, self.pb, did, live=True, transport=fake)
        self.assertEqual(len(sent), 1, r)

    def test_unapproved_draft_cannot_send(self):
        bid, _ = self.qualified_business()
        did, *_ = self.ready_draft(bid)
        self.settings["sending_enabled"] = True
        r = outreach.send(self.reg, self.settings, self.env, self.pb, did, live=True, transport=lambda *a: "x")
        self.assertIn("only approved drafts", r)
        outreach.approve(self.reg, self.settings, self.env, playbooks.load, [did], confirm=lambda d, t: False,
                         out=lambda *a: None)
        self.assertEqual(self.reg.q1("SELECT status FROM drafts WHERE id=?", (did,))["status"], "draft")

    def test_crash_mid_send_blocks_until_resolved(self):
        bid, _ = self.qualified_business()
        did, *_ = self.ready_draft(bid)
        self.approve(did)
        self.settings["sending_enabled"] = True

        def boom(*a):
            raise ConnectionResetError("lost connection after DATA")
        r = outreach.send(self.reg, self.settings, self.env, self.pb, did, live=True, transport=boom)
        self.assertIn("UNKNOWN", r)
        again = outreach.send(self.reg, self.settings, self.env, self.pb, did, live=True, transport=lambda *a: "x")
        self.assertIn("unresolved send", again)

    def test_failed_before_send_can_retry(self):
        bid, _ = self.qualified_business()
        did, *_ = self.ready_draft(bid)
        self.approve(did)
        self.settings["sending_enabled"] = True

        def auth_fail(*a):
            raise outreach.BeforeSendError("bad password")
        self.assertIn("FAILED", outreach.send(self.reg, self.settings, self.env, self.pb, did, live=True, transport=auth_fail))
        self.assertTrue(outreach.send(self.reg, self.settings, self.env, self.pb, did, live=True,
                                      transport=lambda *a: "<ok>").startswith("SENT"))
        self.assertEqual(self.reg.q1("SELECT COUNT(*) n FROM touches")["n"], 1)

    def test_other_playbook_cannot_pitch_same_business(self):
        bid, _ = self.qualified_business()
        did, *_ = self.ready_draft(bid)
        self.approve(did)
        self.settings["sending_enabled"] = True
        outreach.send(self.reg, self.settings, self.env, self.pb, did, live=True, transport=lambda *a: "<1>")
        conv = playbooks.load("website-conversion")
        self.reg.set_stage(bid, conv["id"], "qualified")
        self.reg.add_opportunity(bid, conv["id"], "No online booking path found", "OBSERVED")
        for days in (0, 120, 400):
            d = gate.can_contact(self.reg, bid, playbook=conv["id"], channel="email",
                                 recipient="hello@sunnycabins.test", now=NOW + timedelta(days=days))
            self.assertFalse(d.allowed, days)
        self.assertEqual(self.reg.q1("SELECT COUNT(*) n FROM opportunities WHERE business_id=? AND playbook=?",
                                     (bid, conv["id"]))["n"], 1)

    def test_followup_rules(self):
        bid, _ = self.qualified_business()
        did, *_ = self.ready_draft(bid)
        self.approve(did)
        self.settings["sending_enabled"] = True
        outreach.send(self.reg, self.settings, self.env, self.pb, did, live=True, transport=lambda *a: "<1>")
        tid = self.reg.q1("SELECT id FROM touches")["id"]
        kw = dict(playbook=self.pb["id"], channel="email", recipient="hello@sunnycabins.test", kind="followup",
                  parent_touch_id=tid)
        self.assertFalse(gate.can_contact(self.reg, bid, now=NOW + timedelta(days=1), **kw).allowed)
        self.assertTrue(gate.can_contact(self.reg, bid, now=NOW + timedelta(days=4), **kw).allowed)
        self.assertFalse(gate.can_contact(self.reg, bid, now=NOW + timedelta(days=30), **kw).allowed)
        ft, _ = gate.reserve_touch(self.reg, bid, topic="f", now=NOW + timedelta(days=4), **kw)
        gate.resolve_touch(self.reg, ft, "SENT")
        self.assertFalse(gate.can_contact(self.reg, bid, now=NOW + timedelta(days=10), **kw).allowed)
        self.reg.record_outcome(bid, "replied")
        self.assertFalse(gate.can_contact(self.reg, bid, now=NOW + timedelta(days=5), **{**kw, "parent_touch_id": tid}).allowed)

    def test_opt_out_and_email_suppression(self):
        bid, _ = self.qualified_business()
        samples.register(self.reg, self.pb, bid, link="https://drive.example.org/s")
        self.reg.record_outcome(bid, "opt_out", email="hello@sunnycabins.test")
        d = gate.can_contact(self.reg, bid, playbook=self.pb["id"], channel="email", recipient="hello@sunnycabins.test")
        self.assertFalse(d.allowed)
        other, _ = self.reg.upsert_business(name="Other", website="other.test", country="US", source="t")
        self.reg.set_stage(other, self.pb["id"], "qualified")
        d2 = gate.can_contact(self.reg, other, playbook=self.pb["id"], channel="email", recipient="HELLO@sunnycabins.test")
        self.assertTrue(any("suppressed email" in r for r in d2.reasons))

    def test_needs_review_and_unknown_country_block(self):
        bid, _ = self.reg.upsert_business(name="Nowhere", website="nowhere.test", source="t")
        self.reg.set_stage(bid, self.pb["id"], "qualified")
        d = gate.can_contact(self.reg, bid, playbook=self.pb["id"], channel="email", recipient="a@nowhere.test")
        self.assertTrue(any("country unknown" in r for r in d.reasons))


class TestGeoBridge(Base):
    def write_ledger(self, entries):
        self.ledger.write_text("".join(json.dumps(e) + "\n" for e in entries))
        return hashlib.sha256(self.ledger.read_bytes()).hexdigest()

    def test_geo_contacted_business_is_skipped_and_blocked(self):
        ts = (NOW - timedelta(days=10)).isoformat()
        before = self.write_ledger([{"ts": ts, "domain": "sunnycabins.test", "to": "hello@sunnycabins.test",
                                     "msg_id": "<g1@x>", "kind": "pitch"}])
        stats = discover.ingest(self.reg, self.pb, discover.from_urls(["https://www.SunnyCabins.test/"], "US"), "urls")
        self.assertEqual(stats["skipped_known"], 1)
        bid = self.reg.find("sunnycabins.test")
        self.reg.set_stage(bid, self.pb["id"], "qualified")
        d = gate.can_contact(self.reg, bid, playbook=self.pb["id"], channel="email", recipient="hello@sunnycabins.test")
        self.assertFalse(d.allowed)
        self.assertTrue(any("contacted 10 day" in r for r in d.reasons))
        self.assertEqual(before, hashlib.sha256(self.ledger.read_bytes()).hexdigest(), "GEO ledger must not change")

    def test_daily_cap_counts_geo_sends(self):
        recent = (NOW - timedelta(hours=2)).isoformat()
        self.write_ledger([{"ts": recent, "domain": f"geo{i}.test", "to": f"a@geo{i}.test", "msg_id": f"<{i}>"}
                           for i in range(5)])
        bid, _ = self.qualified_business()
        samples.register(self.reg, self.pb, bid, link="https://drive.example.org/s")
        d = gate.can_contact(self.reg, bid, playbook=self.pb["id"], channel="email", recipient="hello@sunnycabins.test",
                             require_sample=True)
        self.assertTrue(any("daily email cap" in r for r in d.reasons), d.reasons)


class TestRentalHosts(Base):
    """str-listing-upgrade: hosts you researched yourself on Airbnb, contacted only through their own channels."""

    HEADER = ("company,website,host_profile_url,listing_urls,email,email_source,instagram,city,state,country,"
              "check_multi_listing,note_multi_listing,check_photo_gap,note_photo_gap,check_description_gap,"
              "note_description_gap\n")

    def setUp(self):
        super().setUp()
        self.pb = playbooks.load("str-listing-upgrade")

    def import_rows(self, rows):
        path = self.tmp / "hosts.csv"
        path.write_text(self.HEADER + "".join(r + "\n" for r in rows))
        return discover.ingest(self.reg, self.pb, discover.from_csv(path, "US"), "csv")

    def test_platform_country_domains_are_one_listing(self):
        self.assertEqual(identity.profile_key("https://www.airbnb.co.in/rooms/123?adults=2"),
                         identity.profile_key("airbnb.com/rooms/123/"))
        self.assertEqual(identity.domain_key("https://www.airbnb.co.uk/users/show/9"), "")
        self.assertTrue(identity.automation_forbidden("https://www.vrbo.com/123"))
        self.assertTrue(identity.automation_forbidden("someone@airbnb.com"))
        self.assertFalse(identity.automation_forbidden("https://lakestays.test"))

    def test_research_csv_builds_one_business_per_host(self):
        stats = self.import_rows([
            "Lake Stays Co,https://lakestays.test,https://www.airbnb.com/users/show/111,"
            "https://www.airbnb.com/rooms/1;https://www.airbnb.com/rooms/2,info@lakestays.test,https://lakestays.test/contact,,"
            "Austin,TX,US,yes,6 listings,yes,11 photos; no bathroom photo,no,",
            "Private Host,,https://www.airbnb.com/users/show/222,https://www.airbnb.com/rooms/3,,,,Austin,TX,US,"
            "yes,2 listings,yes,9 photos,yes,40-word description",
            "LAKE STAYS,,,https://www.airbnb.co.in/rooms/2?check_in=x,,,https://instagram.com/lakestays,Austin,TX,US,,,,,yes,"
            "no check-in info",
        ])
        self.assertEqual(stats["new_prospects"], 2)
        self.assertEqual(stats["already_in_playbook"], 1)
        lake = self.reg.find("https://www.airbnb.com/rooms/1")
        self.assertEqual(self.reg.find("lakestays.test"), lake)
        self.assertEqual(self.reg.find("https://www.airbnb.com/rooms/2"), lake)
        self.assertEqual(self.reg.prospect(lake, self.pb["id"])["stage"], "qualified")
        ev = self.reg.current_evidence(lake, self.pb["id"])
        self.assertEqual(ev["photo_gap"]["status"], "OBSERVED")
        self.assertEqual(ev["photo_gap"]["source_url"], "https://www.airbnb.com/rooms/1")
        self.assertEqual(ev["description_gap"]["hit"], 1)  # added by the 3rd row for the same host
        private = self.reg.find("https://www.airbnb.com/users/show/222")
        self.assertEqual(self.reg.prospect(private, self.pb["id"])["stage"], "rejected")  # no channel of its own

    def test_no_gap_observed_is_rejected(self):
        self.import_rows(["Tidy Homes,https://tidy.test,,https://www.airbnb.com/rooms/7,hi@tidy.test,https://tidy.test,,"
                          "Austin,TX,US,yes,3 listings,no,25 good photos,no,full description"])
        bid = self.reg.find("tidy.test")
        self.assertEqual(self.reg.prospect(bid, self.pb["id"])["stage"], "needs_check")  # own site not checked yet
        res = checks.check_business(self.reg, FakeFetcher(manager_site("tidy.test", gaps=False)), self.pb, bid)
        self.assertEqual(res["stage"], "rejected", res["reason"])

    def test_management_company_qualifies_from_its_own_site(self):
        bid, _ = self.reg.upsert_business(name="River Rentals", website="https://riverrentals.test", country="US",
                                          source="t")
        self.reg.ensure_prospect(bid, self.pb["id"])
        res = checks.check_business(self.reg, FakeFetcher(manager_site("riverrentals.test")), self.pb, bid)
        self.assertEqual(res["stage"], "qualified", res["reason"])
        ev = self.reg.current_evidence(bid, self.pb["id"])
        self.assertEqual(ev["site_multi_property"]["hit"], 1)
        self.assertEqual(ev["site_no_parking"]["hit"], 1)
        self.assertIn("/properties/", ev["site_no_parking"]["summary"])
        self.assertEqual(ev["site_few_photos"]["hit"], 1)  # signal only
        self.assertIn("min of 2", ev["site_few_photos"]["summary"])
        self.assertEqual(self.reg.prospect(bid, self.pb["id"])["priority"], 1)

    def test_rate_limited_site_is_retried_not_rejected(self):
        bid, _ = self.reg.upsert_business(name="Busy", website="https://busy.test", country="US", source="t")
        self.reg.ensure_prospect(bid, self.pb["id"])
        res = checks.check_business(self.reg, FakeFetcher({"https://busy.test": (429, "slow down")}), self.pb, bid)
        self.assertEqual(res["stage"], "needs_check")
        self.assertIn("temporary", res["reason"])

    def test_crawl_prefers_property_pages_and_skips_www_duplicates(self):
        base = "https://cove.test"
        links = "".join(f'<a href="{base}/properties/home-{i}">Home {i}</a>' for i in range(4))
        links += (f'<a href="https://www.cove.test/">Home</a><a href="{base}/about">About</a>'
                  f'<a href="{base}/contact">Contact</a><a href="{base}/property-management">Owners</a>')
        pages = {base: (200, f"<html><body>{site()}{links}</body></html>")}
        for i in range(4):
            pages[f"{base}/properties/home-{i}"] = (200, site().replace("<h1>", "<p>Sleeps 4, 2 bedrooms</p><h1>"))
        fetched = []
        ff = FakeFetcher(pages)
        orig = ff.fetch
        ff.fetch = lambda u: fetched.append(u) or orig(u)
        checks.crawl(ff, base, self.pb)
        self.assertNotIn("https://www.cove.test/", fetched)
        self.assertEqual(sum("/properties/" in u for u in fetched), 4)
        self.assertLessEqual(len(fetched), self.pb["crawl"]["max_pages"])

    def test_category_pages_are_not_property_pages_and_second_hop_finds_them(self):
        base = "https://peak.test"
        cat_links = "".join(f'<a href="{base}/rentals/cabin-{i}">Cabin {i}</a>' for i in range(20))
        intro = "<p>" + "Cabins in the Smokies with views and hot tubs for families and groups. " * 8 + "</p>"
        pages = {
            base: (200, f'<html><body>{intro}<a href="{base}/rentals/pet-friendly">Pet friendly</a>'
                        f'<a href="mailto:hi@peak.test">Email</a></body></html>'),
            f"{base}/rentals/pet-friendly": (200, f"<html><body>{intro}<p>Sleeps up to 12 guests</p>{cat_links}</body></html>"),
        }
        for i in range(20):
            pages[f"{base}/rentals/cabin-{i}"] = (200, f"<html><body>{intro}<p>Sleeps 6, 3 bedrooms, 2 baths</p>"
                                                       f'<img src="/c{i}a.jpg"><img src="/c{i}b.jpg"></body></html>')
        crawled = checks.crawl(FakeFetcher(pages), base, self.pb)
        details = [pg.final_url for pg, ps in crawled if pg.ok and checks.is_detail_page(self.pb, pg.final_url, ps)]
        self.assertNotIn(f"{base}/rentals/pet-friendly", details)
        self.assertTrue(details, "second hop should reach single-property pages")
        qa, results = checks.evaluate(self.pb, crawled)
        parking = {r["check_id"]: r for r in results}["site_no_parking"]
        self.assertIn("property page(s)", parking["summary"])
        self.assertNotIn("pet-friendly", parking["summary"])

    def test_linked_video_channel_counts_as_video(self):
        html = site().replace("</body>", '<a href="https://www.youtube.com/@peakcabins">YouTube</a></body>')
        pages = [(FakeFetcher({"https://v.test": (200, html)}).fetch("https://v.test"),)]
        pages = [(p[0], web.parse(p[0])) for p in pages]
        qa, results = checks.evaluate(self.pb, pages)
        self.assertEqual({r["check_id"]: r for r in results}["site_no_video"]["hit"], False)

    def test_page_pattern_without_matching_pages_is_not_checked(self):
        pages = {"https://plain.test": (200, site())}
        bid, _ = self.reg.upsert_business(name="Plain", website="https://plain.test", country="US", source="t")
        self.reg.ensure_prospect(bid, self.pb["id"])
        checks.check_business(self.reg, FakeFetcher(pages), self.pb, bid)
        ev = self.reg.current_evidence(bid, self.pb["id"])
        self.assertEqual(ev["site_no_parking"]["status"], "NOT_CHECKED")

    def test_one_command_run_stops_at_target_and_never_repeats_a_search(self):
        domains = ["alpha.test", "bravo.test", "charlie.test"]
        pages = {}
        for d in domains:
            pages.update(manager_site(d))
        calls = []

        def fake_search(text):
            calls.append(text)
            return [{"id": f"place-{d}", "displayName": {"text": d.split(".")[0].title() + " Stays"},
                     "websiteUri": f"https://{d}", "rating": 4.5, "userRatingCount": 40, "businessStatus": "OPERATIONAL",
                     "addressComponents": [{"types": ["country"], "shortText": "US", "longText": "United States"}]}
                    for d in domains]
        state = discover.run_auto(self.reg, self.pb, FakeFetcher(pages), location="Testville, TN", target=2,
                                  search_fn=fake_search, out=lambda *a: None)
        self.assertEqual(len(state["qualified"]), 2)
        self.assertEqual(len(calls), 1)
        self.assertEqual(self.reg.q1("SELECT COUNT(*) n FROM prospects WHERE stage='found'")["n"], 1)  # left for next run
        state2 = discover.run_auto(self.reg, self.pb, FakeFetcher(pages), location="Testville, TN", target=5,
                                   search_fn=fake_search, out=lambda *a: None)
        self.assertEqual(len(calls), 1 + (len(self.pb["discovery"]["queries"]) - 1))  # first query not repeated
        self.assertEqual(len(state2["qualified"]), 1)  # the unchecked one from run 1, checked first

    def test_client_sheet_is_separate_from_geo(self):
        from acqlib import sheets
        bid, _ = self.reg.upsert_business(name="River Rentals", website="https://riverrentals.test", country="US",
                                          source="t")
        self.reg.ensure_prospect(bid, self.pb["id"])
        checks.check_business(self.reg, FakeFetcher(manager_site("riverrentals.test")), self.pb, bid)
        rows = sheets.rows_for(self.reg, self.pb)
        self.assertEqual(len(rows), 1)
        row = dict(zip(sheets.COLUMNS, rows[0]))
        self.assertEqual(row["Stage"], "qualified")
        self.assertIn("parking", row["Observed problems (evidence)"])
        self.assertEqual(row["Email"], "stay@riverrentals.test")
        path = sheets.write_csv(self.reg, self.pb, rows)
        self.assertTrue(Path(path).read_text().startswith("Business,Stage"))
        self.reg.settings["geo"]["sheet_id"] = "GEO123"
        self.reg.settings["sheets"] = {self.pb["id"]: {"sheet_id": "https://docs.google.com/spreadsheets/d/GEO123/edit"}}
        with self.assertRaises(RuntimeError):
            sheets.sync_google(self.reg, self.pb, rows)

    def test_engine_never_fetches_airbnb(self):
        page = web.Fetcher({"http": {}}).fetch("https://www.airbnb.com/rooms/1")
        self.assertFalse(page.ok)
        self.assertIn("forbid automated access", page.error)
        self.assertIsNone(web.Fetcher({"http": {}}).download("https://a0.muscache.com/im/pictures/x.jpg",
                                                             self.tmp / "x.jpg"))
        cands = discover.from_urls(["https://www.airbnb.com/rooms/55"], "US")
        self.assertEqual(cands[0]["website"], "")

    def test_host_without_website_stays_qualified_after_check(self):
        self.import_rows(["Ridge Rentals,,https://www.airbnb.com/users/show/333,https://www.airbnb.com/rooms/8,,,"
                          "https://instagram.com/ridgerentals,Austin,TX,US,yes,4 listings,yes,no kitchen photo,,"])
        bid = self.reg.find("https://www.airbnb.com/rooms/8")
        self.assertEqual(self.reg.prospect(bid, self.pb["id"])["stage"], "qualified")
        res = checks.check_business(self.reg, FakeFetcher({}), self.pb, bid)
        self.assertEqual(res["stage"], "qualified")

    def test_cannot_message_through_airbnb(self):
        self.import_rows(["Ridge Rentals,,https://www.airbnb.com/users/show/333,https://www.airbnb.com/rooms/8,,,"
                          "https://instagram.com/ridgerentals,Austin,TX,US,yes,4 listings,yes,no kitchen photo,,"])
        bid = self.reg.find("https://www.airbnb.com/rooms/8")
        samples.register(self.reg, self.pb, bid, link="https://drive.example.org/upgrade")
        ev = self.reg.current_evidence(bid, self.pb["id"])["photo_gap"]["id"]
        _, status, problems, dec = outreach.create_draft(
            self.reg, self.pb, bid=bid, channel="instagram", recipient="https://www.airbnb.com/users/show/333",
            subject=None, body="Your listing has no kitchen photo. Sample: {sample_link}", evidence_ids=[ev])
        self.assertEqual(status, "invalid")
        self.assertFalse(dec.allowed)
        _, status, problems, _ = outreach.create_draft(
            self.reg, self.pb, bid=bid, channel="instagram", recipient="https://instagram.com/ridgerentals",
            subject=None, body="I came across your listings; one has no kitchen photo. I put together a short upgrade "
                               "sample: {sample_link} Would a refresh across your 4 listings help?", evidence_ids=[ev])
        self.assertEqual(status, "invalid")  # '4' is not in the cited photo evidence
        mid = self.reg.current_evidence(bid, self.pb["id"])["multi_listing"]["id"]
        _, status, problems, _ = outreach.create_draft(
            self.reg, self.pb, bid=bid, channel="instagram", recipient="https://instagram.com/ridgerentals",
            subject=None, body="I came across your listings; one has no kitchen photo. I put together a short upgrade "
                               "sample: {sample_link} Would a refresh across your 4 listings help?", evidence_ids=[ev, mid])
        self.assertEqual(status, "draft", problems)


class TestSafetyProperties(unittest.TestCase):
    def test_no_llm_provider_in_engine(self):
        pattern = re.compile(r"anthropic|openai|generativelanguage|google\.generativeai|genai|api\.claude|mistral|cohere",
                             re.I)
        offenders = [str(p) for p in (SKILL / "acqlib").glob("*.py") if pattern.search(p.read_text())]
        offenders += [str(SKILL / "acq.py")] if pattern.search((SKILL / "acq.py").read_text()) else []
        self.assertEqual(offenders, [])

    def test_all_playbooks_valid(self):
        for pid in playbooks.list_ids() + ["_template"]:
            playbooks.load(pid)

    def test_engine_never_writes_geo_paths(self):
        settings = load_json(SKILL / "config" / "settings.json")
        geo_roots = [p for p in settings["baseline_paths"]] + list(settings["geo"].values())
        data_dir = settings["data_dir"]
        self.assertFalse(any(str(data_dir).startswith(str(r)) for r in geo_roots if isinstance(r, str) and r.startswith("/")))
        for p in (SKILL / "acqlib").glob("*.py"):
            src = p.read_text()
            for m in re.finditer(r"open\(([^)]*)\)", src):
                if "geo" in m.group(1).lower():
                    self.assertNotRegex(m.group(1), r"['\"](w|a)", f"{p.name} opens a GEO path for writing")


if __name__ == "__main__":
    unittest.main()
