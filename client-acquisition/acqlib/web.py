"""Polite page fetching (robots.txt, per-host delay, size cap) and a standard-library HTML parser."""
from __future__ import annotations

import gzip
import re
import time
import urllib.error
import urllib.request
import urllib.robotparser
import zlib
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Optional
from urllib.parse import urljoin, urlsplit, urlunsplit

from . import identity

# Markers that only appear on bot-challenge pages, and weaker ones that count only with a 403/429/503.
# ("challenge-platform" and "captcha" also appear on normal pages: Cloudflare scripts, reCAPTCHA forms.)
BLOCK_STRONG = ("<title>just a moment...</title>", "cf_chl_opt", "cf-chl-bypass", "px-captcha", "are you a robot")
BLOCK_WEAK = ("challenge-platform", "captcha", "access denied", "attention required!")
SKIP_TEXT_TAGS = {"script", "style", "noscript", "template", "svg"}
ASSET_TLDS = {"png", "jpg", "jpeg", "svg", "webp", "gif", "js", "css", "woff", "woff2", "ico", "map", "avif"}
EMAIL_IN_TEXT = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}")
SOCIAL_HOSTS = {"instagram.com": "instagram", "facebook.com": "facebook", "linkedin.com": "linkedin",
                "tiktok.com": "tiktok", "youtube.com": "youtube", "x.com": "x", "twitter.com": "x"}


@dataclass
class Page:
    url: str
    final_url: str = ""
    status: int = 0
    content_type: str = ""
    html: str = ""
    error: str = ""
    blocked: bool = False
    robots_disallowed: bool = False

    @property
    def ok(self) -> bool:
        return self.status == 200 and "html" in self.content_type and not self.blocked and not self.error


@dataclass
class Parsed:
    title: str = ""
    elements: list = field(default_factory=list)   # (tag, {attr: value})
    text: str = ""
    links: list = field(default_factory=list)      # (absolute href, anchor text)
    images: list = field(default_factory=list)     # absolute image URLs in document order
    jsonld: list = field(default_factory=list)     # raw JSON-LD strings
    forms: list = field(default_factory=list)      # list of input descriptors per form
    script_count: int = 0


class _Parser(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.p = Parsed()
        self._skip = 0
        self._text = []
        self._in_title = False
        self._in_jsonld = False
        self._jsonld_buf = []
        self._anchor = None
        self._form = None

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        self.p.elements.append((tag, a))
        if tag in SKIP_TEXT_TAGS:
            self._skip += 1
        if tag == "script":
            self.p.script_count += 1
            if "ld+json" in a.get("type", "").lower():
                self._in_jsonld = True
                self._jsonld_buf = []
        elif tag == "title":
            self._in_title = True
        elif tag == "a" and a.get("href"):
            self._anchor = [urljoin(self.base, a["href"].strip()), []]
        elif tag == "img":
            for key in ("src", "data-src", "data-lazy-src", "data-original"):
                if a.get(key) and not a[key].startswith("data:"):
                    self.p.images.append(urljoin(self.base, a[key].strip()))
                    break
            else:
                srcset = a.get("srcset") or a.get("data-srcset")
                if srcset:
                    self.p.images.append(urljoin(self.base, srcset.split(",")[0].strip().split(" ")[0]))
        elif tag == "source" and a.get("srcset") and "image" in a.get("type", "image"):
            self.p.images.append(urljoin(self.base, a["srcset"].split(",")[0].strip().split(" ")[0]))
        elif tag == "form":
            self._form = []
        elif tag in ("input", "textarea", "select") and self._form is not None:
            self._form.append((tag, a.get("type", ""), a.get("name", ""), a.get("placeholder", "")))

    def handle_endtag(self, tag):
        if tag in SKIP_TEXT_TAGS and self._skip:
            self._skip -= 1
        if tag == "script" and self._in_jsonld:
            self.p.jsonld.append("".join(self._jsonld_buf))
            self._in_jsonld = False
        elif tag == "title":
            self._in_title = False
        elif tag == "a" and self._anchor:
            self.p.links.append((self._anchor[0], " ".join("".join(self._anchor[1]).split())))
            self._anchor = None
        elif tag == "form" and self._form is not None:
            self.p.forms.append(self._form)
            self._form = None

    def handle_data(self, data):
        if self._in_jsonld:
            self._jsonld_buf.append(data)
            return
        if self._in_title:
            self.p.title += data
        if self._skip:
            return
        self._text.append(data)
        if self._anchor:
            self._anchor[1].append(data)

    def close(self):
        super().close()
        self.p.text = " ".join(" ".join(self._text).split())
        self.p.title = " ".join(self.p.title.split())
        return self.p


def parse(page: Page) -> Parsed:
    parser = _Parser(page.final_url or page.url)
    try:
        parser.feed(page.html or "")
    except Exception:  # malformed HTML: keep whatever was parsed
        pass
    return parser.close()


def is_js_shell(parsed: Parsed) -> bool:
    """A page whose content is rendered by JavaScript: absence of an element cannot be concluded from raw HTML."""
    return len(parsed.text) < 300 and parsed.script_count >= 2


class Fetcher:
    def __init__(self, settings: dict):
        h = settings.get("http", {})
        self.timeout = h.get("timeout_seconds", 20)
        self.max_bytes = h.get("max_bytes", 3_000_000)
        self.delay = h.get("delay_seconds", 1.0)
        self.ua = h.get("user_agent", "Mozilla/5.0")
        self._robots = {}
        self._last = {}

    def _wait(self, host):
        last = self._last.get(host)
        if last is not None:
            gap = time.monotonic() - last
            if gap < self.delay:
                time.sleep(self.delay - gap)
        self._last[host] = time.monotonic()

    def allowed(self, url) -> bool:
        parts = urlsplit(url)
        root = f"{parts.scheme}://{parts.netloc}"
        rp = self._robots.get(root)
        if rp is None:
            rp = urllib.robotparser.RobotFileParser()
            try:
                raw = self._get(root + "/robots.txt", text_only=True)
                rp.parse(raw.html.splitlines() if raw.status == 200 else [])
            except Exception:
                rp.parse([])
            self._robots[root] = rp
        return rp.can_fetch(self.ua, url) and rp.can_fetch("*", url)

    def _get(self, url, text_only=False) -> Page:
        page = Page(url=url)
        host = urlsplit(url).netloc
        self._wait(host)
        req = urllib.request.Request(url, headers={"User-Agent": self.ua, "Accept": "text/html,*/*;q=0.8",
                                                   "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                page.status = resp.status
                page.final_url = resp.geturl()
                page.content_type = (resp.headers.get("Content-Type") or "").lower()
                raw = resp.read(self.max_bytes + 1)[: self.max_bytes]
                enc = (resp.headers.get("Content-Encoding") or "").lower()
                if enc == "gzip":
                    raw = gzip.decompress(raw)
                elif enc == "deflate":
                    raw = zlib.decompress(raw)
                charset = resp.headers.get_content_charset() or "utf-8"
                page.html = raw.decode(charset, errors="replace")
        except urllib.error.HTTPError as e:
            page.status = e.code
            page.final_url = e.geturl() or url
            page.error = f"HTTP {e.code}"
            try:
                page.html = e.read(200_000).decode("utf-8", errors="replace")
            except Exception:
                pass
        except Exception as e:  # DNS, TLS, timeout
            page.error = f"{type(e).__name__}: {e}"
        low = page.html[:20000].lower()
        page.blocked = any(m in low for m in BLOCK_STRONG) or (
            page.status in (403, 429, 503) and any(m in low for m in BLOCK_WEAK))
        if page.blocked and not page.error:
            page.error = "blocked by a bot challenge"
        return page

    def fetch(self, url) -> Page:
        if identity.automation_forbidden(url):
            return Page(url=url, final_url=url, robots_disallowed=True,
                        error="not fetched: this platform's terms forbid automated access (record observations manually)")
        if not self.allowed(url):
            return Page(url=url, final_url=url, error="disallowed by robots.txt", robots_disallowed=True)
        return self._get(url)

    def download(self, url, dest, max_bytes=8_000_000, accept_prefix="image/") -> Optional[str]:
        """Save a file if it is the expected type and size. Returns the content type or None."""
        if identity.automation_forbidden(url) or any(
                b in url.lower() for b in ("muscache.com", "a0.muscache", "trvl-media", "bstatic.com")):
            return None  # never pull images from Airbnb/VRBO/Booking CDNs
        host = urlsplit(url).netloc
        self._wait(host)
        req = urllib.request.Request(url, headers={"User-Agent": self.ua})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                ctype = (resp.headers.get("Content-Type") or "").lower()
                if not ctype.startswith(accept_prefix):
                    return None
                data = resp.read(max_bytes + 1)
                if len(data) > max_bytes:
                    return None
            with open(dest, "wb") as f:
                f.write(data)
            return ctype
        except Exception:
            return None


def normalize_url(url: str) -> str:
    parts = urlsplit(url)
    path = parts.path or "/"
    return urlunsplit((parts.scheme, parts.netloc.lower(), path, parts.query, ""))


def same_site(url: str, domain: str) -> bool:
    return bool(domain) and identity.registrable_domain(url) == domain


def extract_contacts(parsed_pages, site_domain: str, policy: dict) -> dict:
    """Contact channels published on the business's own pages. Placeholders and asset names are discarded."""
    emails, phones, socials, forms = {}, {}, {}, []
    placeholder = set(policy.get("placeholder_email_domains", []))
    for url, p in parsed_pages:
        found = [(h[7:], "mailto") for h, _ in p.links if h.lower().startswith("mailto:")]
        found += [(m, "text") for m in EMAIL_IN_TEXT.findall(p.text)]
        for raw, how in found:
            e = identity.normalize_email(raw)
            if not e:
                continue
            dom = identity.email_domain(e)
            if dom in placeholder or dom.rsplit(".", 1)[-1] in ASSET_TLDS or e.startswith(("noreply@", "no-reply@")):
                continue
            emails.setdefault(e, {"email": e, "page": url, "how": how,
                                  "on_business_domain": identity.registrable_domain(dom) == site_domain})
        for h, _ in p.links:
            if h.lower().startswith("tel:"):
                ph = identity.normalize_phone(h, "US")
                if ph:
                    phones.setdefault(ph, {"phone": ph, "page": url})
            dom = identity.registrable_domain(h)
            if dom in SOCIAL_HOSTS and identity.profile_key(h):
                key = identity.profile_key(h)
                if key.count("/") >= 1 and not re.search(r"/(sharer|share|intent|plugins|dialog)", key):
                    socials.setdefault(key, {"network": SOCIAL_HOSTS[dom], "url": h, "page": url})
        for form in p.forms:
            kinds = {(t, typ) for t, typ, *_ in form}
            if ("textarea", "") in kinds or any(typ == "email" for _, typ in kinds):
                forms.append({"page": url, "fields": len(form)})
                break
    return {"emails": list(emails.values()), "phones": list(phones.values()), "socials": list(socials.values()),
            "contact_forms": forms}
