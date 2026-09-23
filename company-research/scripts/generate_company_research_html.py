#!/usr/bin/env python3
"""
Company Research & Battlecard — Executive HTML Dashboard Generator
Compiles markdown company research dossiers into interactive, publication-grade HTML reports.
Requires ZERO external dependencies (uses standard library only).

Usage:
  python generate_company_research_html.py --input COMPANY-RESEARCH-Company.md --output COMPANY-RESEARCH-Company.html
"""

import os
import sys
import re
import argparse
import html

def clean_inline(text):
    """Converts standard markdown formatting to safe HTML."""
    text = html.escape(text)
    # Bold italic
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # Code
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)

    # Verification Badges (Rakhim Ford Protocol)
    text = re.sub(r'🟢\s*(?:<code>)?\[VERIFIED FACT\](?:</code>)?', r'<span class="badge badge-verified">🟢 VERIFIED FACT</span>', text, flags=re.IGNORECASE)
    text = re.sub(r'🟢\s*(?:<code>)?\[CONFIRMED\](?:</code>)?', r'<span class="badge badge-verified">🟢 CONFIRMED</span>', text, flags=re.IGNORECASE)
    text = re.sub(r'🟡\s*(?:<code>)?\[HIGH CONFIDENCE(?: PATTERN)?\](?:</code>)?', r'<span class="badge badge-confidence">🟡 HIGH CONFIDENCE</span>', text, flags=re.IGNORECASE)
    text = re.sub(r'🟣\s*(?:<code>)?\[AI HYPOTHESIS(?: / TO VALIDATE)?\](?:</code>)?', r'<span class="badge badge-hypothesis">🟣 AI HYPOTHESIS</span>', text, flags=re.IGNORECASE)
    text = re.sub(r'🔴\s*(?:<code>)?\[DEBUNKED(?: / REVISED)?\](?:</code>)?', r'<span class="badge badge-debunked">🔴 REVISED</span>', text, flags=re.IGNORECASE)

    return text

def parse_markdown_to_html(md_content):
    lines = md_content.split('\n')
    out = []
    i = 0
    in_table = False
    table_rows = []

    def flush_table(rows):
        if not rows:
            return ""
        html_t = ['<div class="table-container"><table>']
        is_head = True
        for row in rows:
            if re.match(r'^\s*\|?\s*[-:]+\s*\|', row):
                continue
            cells = [c.strip() for c in row.strip().strip('|').split('|')]
            if is_head:
                html_t.append('<thead><tr>' + ''.join(f'<th>{clean_inline(c)}</th>' for c in cells) + '</tr></thead><tbody>')
                is_head = False
            else:
                html_t.append('<tr>' + ''.join(f'<td>{clean_inline(c)}</td>' for c in cells) + '</tr>')
        html_t.append('</tbody></table></div>')
        return "\n".join(html_t)

    while i < len(lines):
        line = lines[i]

        # Table detection
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            in_table = True
            table_rows.append(line)
            i += 1
            continue
        elif in_table:
            out.append(flush_table(table_rows))
            in_table = False
            table_rows = []

        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Horizontal Rule
        if stripped in ('---', '***', '___'):
            out.append('<hr class="divider" />')
            i += 1
            continue

        # Title (# H1)
        if stripped.startswith('# '):
            title_text = clean_inline(stripped[2:])
            out.append(f'<h1 class="doc-title">{title_text}</h1>')
            i += 1
            continue

        # Section (## H2)
        if stripped.startswith('## '):
            h2_text = clean_inline(stripped[3:])
            is_battlecard = "battlecard" in h2_text.lower()
            is_delta = "delta" in h2_text.lower() or "section 0" in h2_text.lower()
            if is_battlecard:
                card_class = "section-h2 battlecard-h2"
            elif is_delta:
                card_class = "section-h2 delta-h2"
            else:
                card_class = "section-h2"
            out.append(f'<h2 class="{card_class}">{h2_text}</h2>')
            i += 1
            continue

        # Subsection (### H3)
        if stripped.startswith('### '):
            h3_text = clean_inline(stripped[4:])
            out.append(f'<h3 class="section-h3">{h3_text}</h3>')
            i += 1
            continue

        # Blockquote / Alert
        if stripped.startswith('>'):
            quote_text = re.sub(r'^>\s*(\[!.*?\])?\s*', '', stripped)
            if quote_text:
                out.append(f'<div class="callout-box"><strong>EXECUTIVE BRIEFING:</strong> {clean_inline(quote_text)}</div>')
            i += 1
            continue

        # Metadata (**Key:** Value)
        if stripped.startswith('**') and ':' in stripped and not stripped.startswith('**['):
            out.append(f'<div class="meta-row">{clean_inline(stripped)}</div>')
            i += 1
            continue

        # Bullets / Lists
        if stripped.startswith(('- ', '* ')) or re.match(r'^\d+\.\s', stripped):
            bullet_body = re.sub(r'^(-|\*|\d+\.)\s+', '', stripped)
            out.append(f'<div class="list-item"><span class="bullet-dot">•</span><div>{clean_inline(bullet_body)}</div></div>')
            i += 1
            continue

        # Paragraph
        out.append(f'<p class="para">{clean_inline(stripped)}</p>')
        i += 1

    if in_table and table_rows:
        out.append(flush_table(table_rows))

    return "\n".join(out)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Company Research Dossier & Battlecard • Antigravity Engine</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

  @page {
    size: letter;
    margin: 0.5in;
  }

  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  body {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #1E293B;
    background-color: #F8FAFC;
    margin: 0;
    padding: 32px 16px;
    font-size: 13.5px;
    line-height: 1.65;
  }

  .container {
    max-width: 960px;
    margin: 0 auto;
    background: #FFFFFF;
    padding: 48px 56px;
    border-radius: 14px;
    box-shadow: 0 4px 24px rgba(15, 23, 42, 0.06);
    border: 1px solid #E2E8F0;
  }

  .header-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #EFF6FF;
    color: #2563EB;
    border: 1px solid #BFDBFE;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 16px;
  }

  .action-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #2563EB;
    padding-bottom: 16px;
    margin-bottom: 28px;
  }

  .print-btn {
    background: #0F172A;
    color: #FFFFFF;
    border: none;
    padding: 8px 14px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s ease;
  }

  .print-btn:hover {
    background: #2563EB;
  }

  .doc-title {
    font-size: 26px;
    font-weight: 800;
    color: #0F172A;
    margin: 0 0 16px 0;
    letter-spacing: -0.5px;
  }

  .meta-row {
    font-size: 12.5px;
    color: #475569;
    margin-bottom: 4px;
  }

  .divider {
    border: none;
    border-top: 1px solid #E2E8F0;
    margin: 24px 0;
  }

  .section-h2 {
    font-size: 16px;
    font-weight: 700;
    color: #0F172A;
    margin: 28px 0 14px 0;
    padding-bottom: 6px;
    border-bottom: 1px solid #E2E8F0;
  }

  .battlecard-h2 {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    color: #1D4ED8;
    padding: 8px 14px;
    border-radius: 8px;
    margin-top: 20px;
  }

  .delta-h2 {
    background: #F0FDF4;
    border: 1.5px solid #86EFAC;
    color: #166534;
    padding: 8px 14px;
    border-radius: 8px;
    margin-top: 20px;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    vertical-align: middle;
  }

  .badge-verified {
    background: #ECFDF5;
    color: #047857;
    border: 1px solid #A7F3D0;
  }

  .badge-confidence {
    background: #FEF3C7;
    color: #B45309;
    border: 1px solid #FDE68A;
  }

  .badge-hypothesis {
    background: #FAF5FF;
    color: #7E22CE;
    border: 1px solid #E9D5FF;
  }

  .badge-debunked {
    background: #FEF2F2;
    color: #B91C1C;
    border: 1px solid #FECACA;
  }

  .section-h3 {
    font-size: 13.5px;
    font-weight: 700;
    color: #334155;
    margin: 18px 0 8px 0;
  }

  .para {
    margin: 0 0 12px 0;
    color: #334155;
  }

  .callout-box {
    background: #FFFBEB;
    border-left: 4px solid #F59E0B;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin: 14px 0;
    font-size: 12.5px;
    color: #92400E;
  }

  .list-item {
    display: flex;
    gap: 8px;
    margin-bottom: 6px;
    color: #334155;
  }

  .bullet-dot {
    color: #2563EB;
    font-weight: bold;
  }

  .table-container {
    width: 100%;
    overflow-x: auto;
    margin: 16px 0;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    text-align: left;
  }

  th {
    background: #0F172A;
    color: #FFFFFF;
    font-weight: 600;
    padding: 9px 12px;
    border: 1px solid #334155;
  }

  td {
    padding: 8px 12px;
    border: 1px solid #E2E8F0;
    vertical-align: top;
  }

  tr:nth-child(even) {
    background-color: #F8FAFC;
  }

  code {
    font-family: 'JetBrains Mono', monospace;
    background: #F1F5F9;
    color: #0F172A;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 11.5px;
  }

  a {
    color: #2563EB;
    text-decoration: none;
  }

  a:hover {
    text-decoration: underline;
  }

  @media print {
    body {
      background: #FFFFFF;
      padding: 0;
    }
    .container {
      box-shadow: none;
      border: none;
      padding: 0;
      max-width: 100%;
    }
    .action-bar button {
      display: none;
    }
  }
</style>
</head>
<body>
<div class="container">
  <div class="action-bar">
    <div class="header-badge">⚡ Antigravity Multi-Agent Intelligence Dossier</div>
    <button class="print-btn" onclick="window.print()">Export / Print PDF (Cmd+P)</button>
  </div>
  __BODY__
</div>
</body>
</html>
"""

def main():
    parser = argparse.ArgumentParser(description="Compile Company Research markdown into Executive HTML Dashboard.")
    parser.add_argument("--input", required=True, help="Path to input markdown file")
    parser.add_argument("--output", required=True, help="Path to output HTML file")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()

    body_html = parse_markdown_to_html(content)
    full_html = HTML_TEMPLATE.replace("__BODY__", body_html)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"✅ Successfully compiled Executive HTML Dashboard: {args.output}")

if __name__ == "__main__":
    main()
