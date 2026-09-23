#!/usr/bin/env python3
"""
Company Domain & Tech Stack Inspector — Antigravity Skill Utility
Extracts infrastructure, cloud providers, CDN, security headers, analytics, 
and frontend framework signals using Python standard library.

Usage:
  python inspect_company_tech.py stripe.com
  python inspect_company_tech.py https://figma.com --json
"""

import sys
import os
import json
import re
import socket
import ssl
import subprocess
import argparse
import urllib.request
import urllib.parse
import urllib.error

def clean_domain(raw_url):
    """Normalizes URL/domain into hostname and full URL."""
    url = raw_url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or raw_url.strip()
    return hostname, f"https://{hostname}"

def query_mx_records(hostname):
    """Discovers mail providers (Google Workspace, M365, etc.) via dig or nslookup."""
    mail_provider = "Unknown"
    records = []
    try:
        cmd = ["dig", "+short", "MX", hostname]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip():
            records = [line.strip() for line in res.stdout.strip().split('\n') if line.strip()]
        else:
            # Fallback to nslookup
            cmd2 = ["nslookup", "-type=mx", hostname]
            res2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=5)
            if res2.returncode == 0:
                for line in res2.stdout.split('\n'):
                    if 'mail exchanger' in line.lower() or 'mx' in line.lower():
                        records.append(line.strip())
    except Exception:
        pass

    raw_mx = " ".join(records).lower()
    if "google" in raw_mx or "googlemail" in raw_mx or "aspmx" in raw_mx:
        mail_provider = "Google Workspace (Gmail Enterprise)"
    elif "outlook" in raw_mx or "microsoft" in raw_mx or "pphosted" in raw_mx:
        mail_provider = "Microsoft 365 / Exchange Online"
    elif "zoho" in raw_mx:
        mail_provider = "Zoho Mail"
    elif "proton" in raw_mx:
        mail_provider = "ProtonMail"
    elif records:
        mail_provider = f"Custom / Third-Party ({records[0].split()[-1] if records else 'Custom'})"

    return mail_provider, records

def inspect_domain(domain):
    hostname, base_url = clean_domain(domain)
    
    result = {
        "domain": hostname,
        "url": base_url,
        "resolved_ip": None,
        "mail_provider": "Unknown",
        "cdn_cloud": "Unknown",
        "web_server": "Unknown",
        "security_posture": {},
        "frontend_signals": [],
        "analytics_tooling": [],
        "raw_headers": {}
    }

    # 1. IP Resolution
    try:
        ip = socket.gethostbyname(hostname)
        result["resolved_ip"] = ip
    except Exception as e:
        result["resolved_ip"] = f"Unresolved ({e})"

    # 2. MX Mail Provider
    mail_prov, mx_recs = query_mx_records(hostname)
    result["mail_provider"] = mail_prov
    result["mx_records"] = mx_recs[:3]

    # 3. HTTP Request & Header Fingerprinting
    headers_to_send = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(base_url, headers=headers_to_send)
    html_content = ""

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            resp_headers = dict(resp.headers)
            result["raw_headers"] = {k.lower(): v for k, v in resp_headers.items()}
            # Read first 150KB of HTML for script/meta tag detection
            raw_bytes = resp.read(150000)
            html_content = raw_bytes.decode('utf-8', errors='ignore')
    except urllib.error.HTTPError as e:
        resp_headers = dict(e.headers)
        result["raw_headers"] = {k.lower(): v for k, v in resp_headers.items()}
    except Exception as e:
        result["error"] = str(e)
        return result

    headers = result["raw_headers"]

    # Detect Server & CDN/Cloud
    server = headers.get("server", "Hidden/Generic")
    result["web_server"] = server

    cdn_signals = []
    if "cf-ray" in headers or "cloudflare" in server.lower():
        cdn_signals.append("Cloudflare CDN & Edge")
    if "x-amz-cf-id" in headers or "cloudfront" in str(headers).lower():
        cdn_signals.append("AWS CloudFront / S3")
    if "x-served-by" in headers and "fastly" in str(headers).lower():
        cdn_signals.append("Fastly CDN")
    if "x-vercel-id" in headers or "vercel" in server.lower():
        cdn_signals.append("Vercel Edge Platform")
    if "x-github-request-id" in headers:
        cdn_signals.append("GitHub Pages")
    if "x-azure-ref" in headers:
        cdn_signals.append("Microsoft Azure Front Door")

    if cdn_signals:
        result["cdn_cloud"] = ", ".join(cdn_signals)
    elif server != "Hidden/Generic":
        result["cdn_cloud"] = f"Self-Hosted / Managed ({server})"

    # Security Posture
    result["security_posture"] = {
        "HSTS": "strict-transport-security" in headers,
        "CSP": "content-security-policy" in headers,
        "X-Frame-Options": headers.get("x-frame-options", "None"),
        "HTTPS-Enforced": base_url.startswith("https://")
    }

    # 4. Frontend & Analytics Pattern Matching
    if html_content:
        # Frameworks
        if "__NEXT_DATA__" in html_content or "/_next/" in html_content:
            result["frontend_signals"].append("Next.js (React)")
        elif "data-reactroot" in html_content or "react" in html_content.lower():
            result["frontend_signals"].append("React")
        if "__NUXT__" in html_content or "/_nuxt/" in html_content:
            result["frontend_signals"].append("Nuxt.js (Vue)")
        if "ng-version" in html_content:
            result["frontend_signals"].append("Angular")
        if "webflow.js" in html_content or "wf-page" in html_content:
            result["frontend_signals"].append("Webflow CMS")
        if "wp-content" in html_content:
            result["frontend_signals"].append("WordPress")
        if "cdn.shopify.com" in html_content:
            result["frontend_signals"].append("Shopify")

        # Analytics / GTM / Marketing
        if "googletagmanager.com/gtm.js" in html_content:
            result["analytics_tooling"].append("Google Tag Manager")
        if "google-analytics.com" in html_content or "gtag(" in html_content:
            result["analytics_tooling"].append("Google Analytics (GA4)")
        if "cdn.segment.com/analytics.js" in html_content:
            result["analytics_tooling"].append("Segment CDP")
        if "posthog" in html_content:
            result["analytics_tooling"].append("PostHog Product Analytics")
        if "mixpanel" in html_content:
            result["analytics_tooling"].append("Mixpanel")
        if "hotjar.com" in html_content:
            result["analytics_tooling"].append("Hotjar")
        if "js.hs-scripts.com" in html_content or "hubspot" in html_content:
            result["analytics_tooling"].append("HubSpot Marketing/CRM")
        if "widget.intercom.io" in html_content:
            result["analytics_tooling"].append("Intercom Messenger")
        if "js.driftt.com" in html_content:
            result["analytics_tooling"].append("Drift Conversational Marketing")
        if "datadoghq-browser" in html_content:
            result["analytics_tooling"].append("Datadog Real User Monitoring (RUM)")

    return result

def format_markdown_summary(data):
    """Outputs a clean markdown block ready to insert into company research dossiers."""
    lines = [
        f"### 🌐 Automated Tech & Infrastructure Fingerprint: {data['domain']}",
        "",
        "| Infrastructure Layer | Detected Technology / Provider |",
        "|---|---|",
        f"| **Productivity & Mail Suite** | {data['mail_provider']} |",
        f"| **Cloud & CDN Platform** | {data['cdn_cloud']} |",
        f"| **Web Server** | {data['web_server']} |",
        f"| **Frontend Framework(s)** | {', '.join(data['frontend_signals']) if data['frontend_signals'] else 'Server-Rendered / Custom'} |",
        f"| **Analytics & Marketing Stack** | {', '.join(data['analytics_tooling']) if data['analytics_tooling'] else 'Minimal or Server-Side Tracked'} |",
        f"| **Security Headers** | HSTS: {'✅' if data['security_posture'].get('HSTS') else '❌'} • CSP: {'✅' if data['security_posture'].get('CSP') else '❌'} • Frame Protection: {'✅' if data['security_posture'].get('X-Frame-Options') != 'None' else '❌'} |",
        f"| **Resolved IP Address** | `{data['resolved_ip']}` |",
        ""
    ]
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Inspect company tech stack and infrastructure footprint.")
    parser.add_argument("domain", help="Company domain or website URL (e.g. stripe.com or https://figma.com)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    info = inspect_domain(args.domain)

    if args.json:
        print(json.dumps(info, indent=2))
    else:
        print(format_markdown_summary(info))

if __name__ == "__main__":
    main()
