"""Business identity: normalized keys so one business is one record however its URL, name or phone is written."""
from __future__ import annotations

import re
from urllib.parse import urlsplit

# Two-label public suffixes we are likely to meet. Not the full public-suffix list; extend when needed.
MULTI_SUFFIXES = {
    "co.uk", "org.uk", "ac.uk", "gov.uk", "me.uk", "com.au", "net.au", "org.au", "co.nz", "org.nz", "co.in",
    "net.in", "org.in", "firm.in", "com.br", "com.mx", "co.za", "com.sg", "co.jp", "com.tr", "com.cn", "com.hk",
    "co.il", "com.ar", "com.co", "com.my", "com.ph", "co.th", "co.id", "com.pk", "com.ng", "co.ke",
}

# Hosting platforms where each customer gets a subdomain: the full host identifies the business.
SHARED_HOSTS = {
    "lovable.app", "wixsite.com", "squarespace.com", "myshopify.com", "github.io", "netlify.app", "vercel.app",
    "webflow.io", "wordpress.com", "blogspot.com", "carrd.co", "godaddysites.com", "square.site", "business.site",
    "weebly.com", "framer.website", "framer.ai", "pages.dev", "herokuapp.com", "glitch.me", "site123.me",
    "jimdosite.com", "mystrikingly.com", "durable.co", "wix.com", "editorx.io", "hostinger.site", "web.app",
    "firebaseapp.com", "notion.site", "super.site",
}

# Sites where a URL is a profile/listing on someone else's platform, never the business's own domain.
PLATFORM_DOMAINS = {
    "facebook.com", "instagram.com", "linkedin.com", "google.com", "goo.gl", "g.page", "yelp.com", "airbnb.com",
    "vrbo.com", "booking.com", "tripadvisor.com", "tiktok.com", "x.com", "twitter.com", "youtube.com", "etsy.com",
    "thumbtack.com", "angi.com", "houzz.com", "nextdoor.com", "fiverr.com", "upwork.com", "zillow.com", "realtor.com",
    "pinterest.com", "threads.net", "whatsapp.com", "wa.me", "calendly.com", "vagaro.com", "booksy.com",
    "squareup.com", "fresha.com", "mindbodyonline.com", "linktr.ee",
}

# Platforms that appear under many country domains (airbnb.co.in, booking.de ...): matched by brand label.
PLATFORM_BRANDS = {"airbnb", "vrbo", "homeaway", "booking", "expedia", "tripadvisor", "facebook", "instagram",
                   "linkedin", "yelp", "zillow", "google"}
# Platforms whose terms forbid bots/scrapers and commercial messages through them. The engine never fetches these
# and never accepts them as an outreach channel.
NO_AUTOMATION_BRANDS = {"airbnb", "vrbo", "homeaway", "booking", "expedia"}

EMAIL_RE = re.compile(r"^[a-z0-9._%+'-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,}$")
_IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
_NAME_DROP = re.compile(
    r"\b(the|llc|l\.l\.c|inc|incorporated|co|corp|corporation|company|ltd|limited|pllc|pc|lp|llp|group)\b\.?")


def host_of(url: str) -> str:
    text = (url or "").strip().lower()
    if not text:
        return ""
    if "://" not in text:
        text = "http://" + text
    try:
        host = urlsplit(text).hostname or ""
    except ValueError:
        return ""
    host = host.strip(".")
    for prefix in ("www.", "m.", "mobile."):
        if host.startswith(prefix) and host.count(".") >= 2:
            host = host[len(prefix):]
    try:
        host = host.encode("idna").decode("ascii")
    except UnicodeError:
        pass
    return host


def registrable_domain(url: str) -> str:
    """'https://www.Shop.Example.co.uk/x' -> 'example.co.uk'. Shared-platform subdomains keep the full host."""
    host = host_of(url)
    if not host or "." not in host:
        return ""
    if _IP_RE.match(host):
        return host
    for shared in SHARED_HOSTS:
        if host == shared:
            return shared
        if host.endswith("." + shared):
            return host
    labels = host.split(".")
    if len(labels) >= 3 and ".".join(labels[-2:]) in MULTI_SUFFIXES:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def _brand(domain: str) -> str:
    return domain.split(".", 1)[0] if domain else ""


def is_platform(url: str) -> bool:
    d = registrable_domain(url)
    return bool(d) and (d in PLATFORM_DOMAINS or _brand(d) in PLATFORM_BRANDS)


def automation_forbidden(url_or_email: str) -> bool:
    """True for Airbnb/VRBO/Booking/Expedia URLs or addresses (any country domain)."""
    text = url_or_email or ""
    if "@" in text and "://" not in text:
        text = text.rsplit("@", 1)[1]
    return _brand(registrable_domain(text)) in NO_AUTOMATION_BRANDS


def domain_key(url: str) -> str:
    """The business's own website domain, or '' for platform profiles and shared-host roots."""
    d = registrable_domain(url)
    if not d or is_platform(url) or d in SHARED_HOSTS:
        return ""
    return d


def profile_key(url: str) -> str:
    """A listing/profile on a platform (airbnb.com/rooms/123, instagram.com/acme) as host+path."""
    if not is_platform(url):
        return ""
    text = url.strip()
    if "://" not in text:
        text = "http://" + text
    try:
        parts = urlsplit(text)
    except ValueError:
        return ""
    path = re.sub(r"/+$", "", parts.path or "").lower()
    d = registrable_domain(url)
    host = f"{_brand(d)}.com" if _brand(d) in PLATFORM_BRANDS else d  # airbnb.co.in/rooms/1 == airbnb.com/rooms/1
    return f"{host}{path}" if path else ""


def normalize_email(email: str) -> str:
    e = (email or "").strip().lower()
    if e.startswith("mailto:"):
        e = e[7:]
    e = e.split("?")[0].strip()
    return e if EMAIL_RE.match(e) else ""


def email_domain(email: str) -> str:
    e = normalize_email(email)
    return e.split("@", 1)[1] if e else ""


def normalize_phone(phone: str, country: str = "US") -> str:
    """E.164 ('+15125550100') or '' when the country code cannot be established. Never guesses +1 outside US/CA."""
    raw = (phone or "").strip()
    if raw.lower().startswith("tel:"):
        raw = raw[4:]
    if not raw:
        return ""
    has_plus = raw.startswith("+") or raw.startswith("00")
    digits = re.sub(r"\D", "", raw)
    if raw.startswith("00"):
        digits = digits[2:]
    if has_plus:
        return "+" + digits if 8 <= len(digits) <= 15 else ""
    if (country or "").upper() in ("US", "CA"):
        if len(digits) == 10:
            return "+1" + digits
        if len(digits) == 11 and digits.startswith("1"):
            return "+" + digits
    return ""


def name_key(name: str, city: str = "") -> str:
    n = (name or "").lower().replace("&", " and ")
    n = _NAME_DROP.sub(" ", n)
    n = re.sub(r"[^a-z0-9]+", " ", n).strip()
    c = re.sub(r"[^a-z0-9]+", " ", (city or "").lower()).strip()
    return f"{n}@{c}" if n else ""
