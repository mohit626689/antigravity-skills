#!/usr/bin/env python3
"""
AI Restaurant Team — Professional PDF Report Generator

Generates a polished, multi-page restaurant audit PDF using ReportLab.
Output: RESTAURANT-REPORT.pdf (or --demo for RESTAURANT-REPORT-sample.pdf).

Usage:
  python3 generate_restaurant_pdf.py                        # Demo mode
  python3 generate_restaurant_pdf.py --demo                 # Demo mode (explicit)
  python3 generate_restaurant_pdf.py data.json              # From JSON
  python3 generate_restaurant_pdf.py data.json output.pdf   # JSON with custom output

Requires: reportlab>=4.0.0
"""

import sys
import json
import os
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, PageBreak, KeepTogether)
    from reportlab.graphics.shapes import Drawing, Rect, Circle, String, Line
except ImportError:
    print("Error: reportlab is required. Install with: pip install reportlab")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Color palette — Warm Restaurant Theme
# ---------------------------------------------------------------------------
COLORS = {
    "red": HexColor("#e74c3c"),               # Primary brand red
    "red_dark": HexColor("#c0392b"),          # Dark red
    "orange": HexColor("#f39c12"),            # Warm orange (accent)
    "orange_light": HexColor("#fad79a"),      # Light orange
    "green": HexColor("#27ae60"),             # Success green
    "green_light": HexColor("#2ecc71"),       # Lighter green
    "yellow": HexColor("#f1c40f"),            # Caution yellow
    "danger": HexColor("#c0392b"),            # Danger
    "navy": HexColor("#2c3e50"),              # Header navy
    "navy_light": HexColor("#34495e"),
    "gray": HexColor("#7f8c8d"),              # Muted gray
    "light_bg": HexColor("#fdf6ec"),          # Warm cream background
    "cream": HexColor("#fffaf2"),
    "text": HexColor("#2d2d2d"),              # Dark text
    "text_light": HexColor("#7f8c8d"),
    "border": HexColor("#e0d6c9"),
    "header_bg": HexColor("#c0392b"),         # Table header red
    "row_alt": HexColor("#fdf6ec"),
    "white": white,
    "black": black,
}


def score_color(score):
    if score >= 70:
        return COLORS["green"]
    elif score >= 55:
        return COLORS["orange"]
    elif score >= 40:
        return COLORS["yellow"]
    else:
        return COLORS["red"]


def score_grade(score):
    if score >= 85: return "A+"
    if score >= 70: return "A"
    if score >= 55: return "B"
    if score >= 40: return "C"
    if score >= 25: return "D"
    return "F"


def score_signal(score):
    if score >= 85: return "EXCELLENT"
    if score >= 70: return "STRONG"
    if score >= 55: return "AVERAGE"
    if score >= 40: return "BELOW AVERAGE"
    if score >= 25: return "POOR"
    return "CRITICAL"


def signal_color(score):
    if score >= 70: return COLORS["green"]
    if score >= 55: return COLORS["orange"]
    if score >= 40: return COLORS["yellow"]
    return COLORS["red"]


# ---------------------------------------------------------------------------
# Graphics — gauge, bar chart
# ---------------------------------------------------------------------------
def draw_score_gauge(score, size=160):
    """Restaurant Health Score circular gauge with color-coded ring."""
    d = Drawing(size + 20, size + 20)
    cx = size / 2 + 10
    cy = size / 2 + 10

    # Outer ring
    d.add(Circle(cx, cy, size / 2,
                 fillColor=COLORS["light_bg"], strokeColor=COLORS["navy"], strokeWidth=2))

    # Score ring (filled)
    color = score_color(score)
    inner_r = size / 2 - 10
    d.add(Circle(cx, cy, inner_r,
                 fillColor=color, strokeColor=None))

    # White center
    d.add(Circle(cx, cy, inner_r - 16,
                 fillColor=COLORS["white"], strokeColor=None))

    # Score text
    d.add(String(cx, cy + 4, str(int(score)),
                 fontSize=40, fillColor=COLORS["navy"],
                 textAnchor="middle", fontName="Helvetica-Bold"))

    d.add(String(cx, cy - 20, "/ 100",
                 fontSize=11, fillColor=COLORS["gray"],
                 textAnchor="middle", fontName="Helvetica"))

    return d


def create_bar_chart(categories, scores, width=470, height=200):
    """Horizontal bar chart for category scores."""
    d = Drawing(width, height)

    bar_height = 22
    gap = 14
    max_bar_width = width - 220
    start_y = height - 25
    label_x = 5
    bar_x = 190

    for i, (cat, score) in enumerate(zip(categories, scores)):
        y = start_y - i * (bar_height + gap)

        # Category label
        d.add(String(label_x, y + 6, cat[:28],
                     fontSize=9, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica"))

        # Background bar
        d.add(Rect(bar_x, y, max_bar_width, bar_height,
                   fillColor=COLORS["light_bg"], strokeColor=None, rx=3))

        # Score bar
        bar_width = max((score / 100) * max_bar_width, 2)
        color = score_color(score)
        d.add(Rect(bar_x, y, bar_width, bar_height,
                   fillColor=color, strokeColor=None, rx=3))

        # Score label
        d.add(String(bar_x + max_bar_width + 10, y + 6, f"{int(score)}/100",
                     fontSize=10, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica-Bold"))

    return d


def create_competitor_chart(names, scores, width=470, height=180):
    """Vertical bar chart comparing subject + competitors."""
    d = Drawing(width, height)

    bar_count = len(names)
    bar_width = (width - 60) / max(bar_count, 1) - 10
    max_height = height - 50
    base_y = 25

    max_score = max(scores) if scores else 50

    for i, (name, score) in enumerate(zip(names, scores)):
        x = 30 + i * ((width - 60) / max(bar_count, 1))
        bar_h = (score / max_score) * max_height if max_score > 0 else 0

        # Highlight first one (subject) in red, rest in gray
        color = COLORS["red"] if i == 0 else COLORS["navy"]

        d.add(Rect(x, base_y, bar_width, bar_h,
                   fillColor=color, strokeColor=None))

        # Score label
        d.add(String(x + bar_width / 2, base_y + bar_h + 4, str(int(score)),
                     fontSize=9, fillColor=COLORS["text"],
                     textAnchor="middle", fontName="Helvetica-Bold"))

        # Name label (rotated for readability)
        short_name = name[:14]
        d.add(String(x + bar_width / 2, base_y - 12, short_name,
                     fontSize=8, fillColor=COLORS["text"],
                     textAnchor="middle", fontName="Helvetica"))

    return d


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def get_styles():
    styles = getSampleStyleSheet()
    custom = {
        "title": ParagraphStyle("RTitle", parent=styles["Title"],
                                fontSize=30, textColor=COLORS["red"],
                                spaceAfter=6, fontName="Helvetica-Bold", leading=36),
        "name": ParagraphStyle("RName", parent=styles["Title"],
                               fontSize=24, textColor=COLORS["navy"],
                               spaceAfter=4, fontName="Helvetica-Bold", leading=30),
        "subtitle": ParagraphStyle("RSubtitle", parent=styles["Normal"],
                                   fontSize=14, textColor=COLORS["gray"],
                                   spaceAfter=6, fontName="Helvetica"),
        "heading": ParagraphStyle("RHeading", parent=styles["Heading1"],
                                  fontSize=20, textColor=COLORS["red_dark"],
                                  spaceBefore=14, spaceAfter=10,
                                  fontName="Helvetica-Bold"),
        "subheading": ParagraphStyle("RSub", parent=styles["Heading2"],
                                     fontSize=14, textColor=COLORS["navy"],
                                     spaceBefore=12, spaceAfter=6,
                                     fontName="Helvetica-Bold"),
        "body": ParagraphStyle("RBody", parent=styles["Normal"],
                               fontSize=10, textColor=COLORS["text"],
                               spaceAfter=6, fontName="Helvetica", leading=14),
        "body_small": ParagraphStyle("RBodyS", parent=styles["Normal"],
                                     fontSize=8, textColor=COLORS["text"],
                                     spaceAfter=4, fontName="Helvetica", leading=11),
        "signal": ParagraphStyle("RSignal", parent=styles["Title"],
                                 fontSize=24, textColor=COLORS["green"],
                                 spaceAfter=4, fontName="Helvetica-Bold",
                                 alignment=1),
        "grade_large": ParagraphStyle("RGrade", parent=styles["Title"],
                                      fontSize=18, textColor=COLORS["navy"],
                                      spaceAfter=6, fontName="Helvetica-Bold",
                                      alignment=1),
        "footer": ParagraphStyle("RFooter", parent=styles["Normal"],
                                 fontSize=7, textColor=COLORS["gray"],
                                 fontName="Helvetica", leading=10),
        "disclaimer": ParagraphStyle("RDisc", parent=styles["Normal"],
                                     fontSize=6.5, textColor=COLORS["gray"],
                                     fontName="Helvetica", leading=9,
                                     spaceBefore=8),
    }
    return custom


def standard_table_style(extra=None):
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), COLORS["header_bg"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["white"]),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLORS["white"], COLORS["row_alt"]]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if extra:
        cmds.extend(extra)
    return TableStyle(cmds)


DISCLAIMER_TEXT = (
    "DISCLAIMER: This restaurant audit report is generated by AI for educational and research purposes only. "
    "All scores, ratings, and recommendations are AI-generated approximations based on publicly available data. "
    "Always verify all information with the restaurant owner and conduct independent research before making "
    "operational or marketing decisions. The authors and creators of this tool accept no liability for any "
    "losses or damages incurred from reliance on this report."
)


# ---------------------------------------------------------------------------
# Main report generator
# ---------------------------------------------------------------------------
def generate_report(data, output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        rightMargin=50, leftMargin=50,
        topMargin=50, bottomMargin=50
    )

    S = get_styles()
    elements = []

    name = data.get("restaurant_name", "Bella Italia Trattoria")
    city = data.get("city", "Austin, TX")
    cuisine = data.get("cuisine", "Italian")
    rtype = data.get("restaurant_type", "Casual Dining")
    price_tier = data.get("price_tier", "$$")
    date_str = data.get("date", datetime.now().strftime("%B %d, %Y"))
    overall_score = data.get("overall_score", 64)
    grade = score_grade(overall_score)
    signal = score_signal(overall_score)
    sig_color = signal_color(overall_score)

    # =====================================================================
    # PAGE 1 — COVER
    # =====================================================================
    elements.append(Spacer(1, 0.4 * inch))
    elements.append(Paragraph("Restaurant Audit Report", S["title"]))
    elements.append(Spacer(1, 24))
    elements.append(Paragraph(name, S["name"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        f"{cuisine} &nbsp;&middot;&nbsp; {rtype} &nbsp;&middot;&nbsp; {price_tier} &nbsp;&middot;&nbsp; {city}",
        S["subtitle"]
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f"Generated: {date_str}", S["subtitle"]))
    elements.append(Spacer(1, 28))

    # Score gauge
    gauge = draw_score_gauge(overall_score, size=160)
    elements.append(gauge)
    elements.append(Spacer(1, 18))

    color = score_color(overall_score)
    elements.append(Paragraph(
        f'Restaurant Health Score: <font color="{color.hexval()}">{int(overall_score)}/100</font> '
        f'(Grade: <font color="{color.hexval()}">{grade}</font>)',
        S["grade_large"]
    ))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        f'Signal: <font color="{sig_color.hexval()}">{signal}</font>',
        ParagraphStyle("SigLine", parent=S["signal"], textColor=sig_color, fontSize=22)
    ))

    elements.append(Spacer(1, 26))

    # Mini profile table on cover
    prof = data.get("profile", {})
    rating_g = prof.get("google_rating", "4.2 (412)")
    rating_y = prof.get("yelp_rating", "3.9 (287)")
    years = prof.get("years_open", "10 years")
    seats = prof.get("seating", "85 seats")

    cover_tbl = [
        ["Google Rating", rating_g, "Yelp Rating", rating_y],
        ["Years in Business", years, "Seating", seats],
    ]
    cov_table = Table(cover_tbl, colWidths=[110, 130, 110, 130])
    cov_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), COLORS["light_bg"]),
        ("BACKGROUND", (2, 0), (2, -1), COLORS["light_bg"]),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
        ("TEXTCOLOR", (0, 0), (-1, -1), COLORS["text"]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(cov_table)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(DISCLAIMER_TEXT, S["disclaimer"]))
    elements.append(PageBreak())

    # =====================================================================
    # PAGE 2 — SCORE DASHBOARD
    # =====================================================================
    elements.append(Paragraph("Restaurant Health Score Dashboard", S["heading"]))
    elements.append(Spacer(1, 6))

    cats = data.get("categories", {
        "Reviews & Reputation": {"score": 68, "weight": "25%"},
        "Menu & Pricing": {"score": 72, "weight": "20%"},
        "Online Presence": {"score": 55, "weight": "20%"},
        "Marketing & Engagement": {"score": 48, "weight": "15%"},
        "Local Competition": {"score": 70, "weight": "20%"},
    })

    cat_names = list(cats.keys())
    cat_scores = [cats[c].get("score", 50) if isinstance(cats[c], dict) else cats[c]
                  for c in cat_names]

    chart = create_bar_chart(cat_names, cat_scores)
    elements.append(chart)
    elements.append(Spacer(1, 14))

    # Signal badge
    elements.append(Paragraph(
        f'Health Score: <font color="{color.hexval()}">{int(overall_score)}/100</font> &nbsp;|&nbsp; '
        f'Grade: <font color="{color.hexval()}">{grade}</font> &nbsp;|&nbsp; '
        f'Signal: <font color="{sig_color.hexval()}">{signal}</font>',
        ParagraphStyle("SigBadge", parent=S["body"], fontSize=12,
                       fontName="Helvetica-Bold", alignment=1, spaceAfter=14)
    ))

    # Score breakdown table
    sd = [["Category", "Score", "Weight", "Status"]]
    for n, sc in zip(cat_names, cat_scores):
        weight = cats[n].get("weight", "--") if isinstance(cats[n], dict) else "--"
        status = "Strong" if sc >= 70 else ("Mixed" if sc >= 40 else "Weak")
        sd.append([n, f"{int(sc)}/100", weight, status])

    sd_tbl = Table(sd, colWidths=[170, 80, 60, 100])
    sd_extra = [("ALIGN", (1, 0), (-1, -1), "CENTER")]
    for i, sc in enumerate(cat_scores, 1):
        c = score_color(sc)
        sd_extra.append(("TEXTCOLOR", (3, i), (3, i), c))
        sd_extra.append(("FONTNAME", (3, i), (3, i), "Helvetica-Bold"))
    sd_tbl.setStyle(standard_table_style(sd_extra))
    elements.append(sd_tbl)

    elements.append(Spacer(1, 18))
    elements.append(Paragraph("Executive Summary", S["subheading"]))
    exec_summary = data.get("executive_summary",
        f"{name} is a {price_tier} {cuisine.lower()} {rtype.lower()} in {city} with strong fundamentals "
        f"but significant gaps in online presence and marketing engagement. The restaurant's review reputation "
        f"is solid (4.2 Google) but suffers from a low owner response rate (12% on negative reviews). "
        f"Menu pricing is competitive but the photography and social media presence trail local competitors. "
        f"Closing the top 5 quick wins could lift monthly revenue by an estimated $4,800-$9,800."
    )
    elements.append(Paragraph(exec_summary, S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 3 — REVIEWS & REPUTATION
    # =====================================================================
    elements.append(Paragraph("Reviews & Reputation", S["heading"]))
    elements.append(Spacer(1, 6))

    reviews = data.get("reviews", {})
    review_score = reviews.get("score", 68)

    rv_tbl = [["Platform", "Rating", "Reviews", "Response Rate"]]
    for plat in reviews.get("platforms", [
        {"name": "Google", "rating": "4.2", "count": "412", "response_rate": "12%"},
        {"name": "Yelp", "rating": "3.9", "count": "287", "response_rate": "20%"},
        {"name": "TripAdvisor", "rating": "4.0", "count": "98", "response_rate": "0%"},
        {"name": "DoorDash", "rating": "4.4", "count": "187", "response_rate": "n/a"},
    ]):
        rv_tbl.append([plat.get("name", ""), str(plat.get("rating", "")),
                       str(plat.get("count", "")), str(plat.get("response_rate", ""))])

    rv_t = Table(rv_tbl, colWidths=[110, 80, 90, 130])
    rv_t.setStyle(standard_table_style([("ALIGN", (1, 0), (-1, -1), "CENTER")]))
    elements.append(rv_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Top Recurring Complaints", S["subheading"]))
    complaints = reviews.get("complaints", [
        {"theme": "Slow service", "freq": "~28%", "example": "Waited 45 minutes on a Tuesday."},
        {"theme": "Cold food on delivery", "freq": "~22%", "example": "Pasta arrived lukewarm."},
        {"theme": "Noise level", "freq": "~18%", "example": "Couldn't hear my date."},
        {"theme": "Parking", "freq": "~14%", "example": "Circled the block 4 times."},
        {"theme": "Portion size vs price", "freq": "~10%", "example": "Expected more for $24."},
    ])

    ct = [["Theme", "Freq", "Example Quote"]]
    for c in complaints:
        ct.append([c.get("theme", ""), c.get("freq", ""),
                   Paragraph(c.get("example", ""), S["body_small"])])
    ct_t = Table(ct, colWidths=[140, 60, 260])
    ct_t.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(ct_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Top Recurring Praises", S["subheading"]))
    praises = reviews.get("praises", [
        {"theme": "Carbonara dish", "freq": "~35%", "example": "Best carbonara in Austin."},
        {"theme": "Server Maria", "freq": "~20%", "example": "Maria remembered my favorite wine."},
        {"theme": "Atmosphere", "freq": "~18%", "example": "Felt like Italy."},
        {"theme": "Wine list", "freq": "~15%", "example": "Great Barolo selection."},
        {"theme": "Owner Marco", "freq": "~12%", "example": "Marco came by to say hi."},
    ])
    pt = [["Theme", "Freq", "Example Quote"]]
    for p in praises:
        pt.append([p.get("theme", ""), p.get("freq", ""),
                   Paragraph(p.get("example", ""), S["body_small"])])
    pt_t = Table(pt, colWidths=[140, 60, 260])
    pt_t.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(pt_t)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 4 — MENU ENGINEERING
    # =====================================================================
    elements.append(Paragraph("Menu Engineering", S["heading"]))
    elements.append(Spacer(1, 6))

    menu = data.get("menu", {})

    # Kasavana distribution
    elements.append(Paragraph("Kasavana Matrix Distribution", S["subheading"]))
    kasavana = menu.get("kasavana", {
        "Stars (high pop, high margin)": 4,
        "Plowhorses (high pop, low margin)": 8,
        "Puzzles (low pop, high margin)": 5,
        "Dogs (low pop, low margin)": 4,
    })

    kt = [["Quadrant", "Item Count", "% of Menu", "Strategy"]]
    total = sum(kasavana.values()) if kasavana else 1
    strategies = {
        "Stars (high pop, high margin)": "Protect and feature",
        "Plowhorses (high pop, low margin)": "Re-engineer cost or raise price",
        "Puzzles (low pop, high margin)": "Re-merchandise (photos, badges)",
        "Dogs (low pop, low margin)": "Remove or replace",
    }
    for q, count in kasavana.items():
        pct = f"{(count / total * 100):.0f}%" if total else "0%"
        kt.append([q, str(count), pct, strategies.get(q, "")])

    kt_t = Table(kt, colWidths=[180, 60, 65, 175])
    kt_t.setStyle(standard_table_style([("ALIGN", (1, 0), (2, -1), "CENTER")]))
    elements.append(kt_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Top Menu Quick Wins", S["subheading"]))
    quick_wins = menu.get("quick_wins", [
        {"action": "Move Carbonara to top-right of menu (golden triangle)", "effort": "Zero", "lift": "+5-8% category sales"},
        {"action": "Rewrite Lasagna description with sensory language", "effort": "30 min", "lift": "Supports $1.50 price increase"},
        {"action": "Add 'Make it Bolognese' (+$4) modifier to all pastas", "effort": "POS update", "lift": "+$1.50/cover avg ticket"},
        {"action": "Photograph Branzino + add 'Chef's Pick' badge", "effort": "Photo session", "lift": "+30-50% on low-pop high-margin item"},
        {"action": "Remove Three Cheese Ravioli (Dog)", "effort": "Inventory drawdown", "lift": "Less waste + cleaner menu"},
    ])

    qw_tbl = [["#", "Action", "Effort", "Est. Lift"]]
    for i, qw in enumerate(quick_wins, 1):
        qw_tbl.append([str(i),
                       Paragraph(qw.get("action", ""), S["body_small"]),
                       qw.get("effort", ""), qw.get("lift", "")])
    qw_t = Table(qw_tbl, colWidths=[25, 235, 90, 130])
    qw_t.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(qw_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Pricing Position vs Local Market", S["subheading"]))
    pricing = menu.get("pricing", [
        {"item": "Margherita Pizza", "subject": "$16", "market_avg": "$18.50", "position": "Underpriced"},
        {"item": "Carbonara", "subject": "$19", "market_avg": "$21.50", "position": "Underpriced"},
        {"item": "Ribeye", "subject": "$42", "market_avg": "$48", "position": "Underpriced"},
        {"item": "Tiramisu", "subject": "$11", "market_avg": "$9.50", "position": "Overpriced"},
        {"item": "House Wine (glass)", "subject": "$9", "market_avg": "$11.50", "position": "Underpriced"},
    ])

    pr_tbl = [["Item", "Your Price", "Market Avg", "Position"]]
    for p in pricing:
        pr_tbl.append([p.get("item", ""), p.get("subject", ""),
                       p.get("market_avg", ""), p.get("position", "")])
    pr_t = Table(pr_tbl, colWidths=[180, 90, 90, 120])
    pr_extra = [("ALIGN", (1, 0), (2, -1), "CENTER")]
    for i, p in enumerate(pricing, 1):
        pos = p.get("position", "")
        if "Under" in pos:
            pr_extra.append(("TEXTCOLOR", (3, i), (3, i), COLORS["red"]))
            pr_extra.append(("FONTNAME", (3, i), (3, i), "Helvetica-Bold"))
        elif "Over" in pos:
            pr_extra.append(("TEXTCOLOR", (3, i), (3, i), COLORS["orange"]))
            pr_extra.append(("FONTNAME", (3, i), (3, i), "Helvetica-Bold"))
    pr_t.setStyle(standard_table_style(pr_extra))
    elements.append(pr_t)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 5 — ONLINE PRESENCE
    # =====================================================================
    elements.append(Paragraph("Online Presence Audit", S["heading"]))
    elements.append(Spacer(1, 6))

    online = data.get("online", {})

    elements.append(Paragraph("Channel Health Snapshot", S["subheading"]))
    channels = online.get("channels", [
        {"channel": "Google Business Profile", "score": "60/100", "status": "Mixed", "key_gap": "Missing online order link, 0 posts in 30 days"},
        {"channel": "Yelp", "score": "70/100", "status": "OK", "key_gap": "Reservations not enabled"},
        {"channel": "Website", "score": "45/100", "status": "Weak", "key_gap": "No online ordering, no schema markup"},
        {"channel": "DoorDash / Uber Eats", "score": "55/100", "status": "Mixed", "key_gap": "Photo coverage 60% / 40%"},
        {"channel": "NAP Consistency", "score": "50/100", "status": "Weak", "key_gap": "3 directory mismatches"},
    ])

    ch_tbl = [["Channel", "Score", "Status", "Key Gap"]]
    for c in channels:
        ch_tbl.append([c.get("channel", ""), c.get("score", ""),
                       c.get("status", ""),
                       Paragraph(c.get("key_gap", ""), S["body_small"])])
    ch_t = Table(ch_tbl, colWidths=[150, 70, 70, 190])
    ch_extra = [("VALIGN", (0, 0), (-1, -1), "TOP")]
    for i, c in enumerate(channels, 1):
        status = c.get("status", "").lower()
        if "strong" in status or "ok" in status:
            ch_extra.append(("TEXTCOLOR", (2, i), (2, i), COLORS["green"]))
        elif "weak" in status:
            ch_extra.append(("TEXTCOLOR", (2, i), (2, i), COLORS["red"]))
        else:
            ch_extra.append(("TEXTCOLOR", (2, i), (2, i), COLORS["orange"]))
        ch_extra.append(("FONTNAME", (2, i), (2, i), "Helvetica-Bold"))
    ch_t.setStyle(standard_table_style(ch_extra))
    elements.append(ch_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Critical Gaps to Close This Week", S["subheading"]))
    gaps = online.get("critical_gaps", [
        "Add online ordering link to Google Business Profile — losing direct-order revenue daily",
        "Upload 18 more photos to GBP (currently 12, target 30+) — listings with 30+ photos get 2x clicks",
        "Reply to 4 unanswered Q&A questions on GBP",
        "Standardize Name/Address/Phone across all platforms (currently 3 mismatches)",
        "Add Restaurant schema markup to website for Google rich results",
        "Claim Apple Maps listing (currently unclaimed — invisible to iOS users)",
    ])
    for i, g in enumerate(gaps, 1):
        elements.append(Paragraph(f"{i}. {g}", S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 6 — MARKETING RECOMMENDATIONS
    # =====================================================================
    elements.append(Paragraph("Marketing Recommendations", S["heading"]))
    elements.append(Spacer(1, 6))

    marketing = data.get("marketing", {})

    elements.append(Paragraph("Current Marketing Audit", S["subheading"]))
    audit_items = marketing.get("audit", [
        {"area": "Instagram posting", "current": "3 posts/30d", "benchmark": "12-20 posts/30d", "gap": "Major"},
        {"area": "Instagram Reels", "current": "0 in 30d", "benchmark": "8-12 in 30d", "gap": "Critical"},
        {"area": "TikTok", "current": "Dormant 5mo", "benchmark": "12+ posts/mo", "gap": "Critical"},
        {"area": "Email marketing", "current": "0 sends/mo", "benchmark": "4-8 sends/mo", "gap": "Major"},
        {"area": "Loyalty program", "current": "None", "benchmark": "Active program", "gap": "Major"},
        {"area": "Meta ads", "current": "$0/mo", "benchmark": "$500-$2,000/mo", "gap": "Major"},
    ])
    a_tbl = [["Area", "Current", "Benchmark", "Gap"]]
    for a in audit_items:
        a_tbl.append([a.get("area", ""), a.get("current", ""),
                      a.get("benchmark", ""), a.get("gap", "")])
    a_t = Table(a_tbl, colWidths=[140, 110, 130, 80])
    a_extra = [("ALIGN", (1, 0), (-1, -1), "CENTER")]
    for i, a in enumerate(audit_items, 1):
        gap = a.get("gap", "").lower()
        if "critical" in gap:
            a_extra.append(("TEXTCOLOR", (3, i), (3, i), COLORS["red"]))
        elif "major" in gap:
            a_extra.append(("TEXTCOLOR", (3, i), (3, i), COLORS["orange"]))
        else:
            a_extra.append(("TEXTCOLOR", (3, i), (3, i), COLORS["green"]))
        a_extra.append(("FONTNAME", (3, i), (3, i), "Helvetica-Bold"))
    a_t.setStyle(standard_table_style(a_extra))
    elements.append(a_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Recommended 30-Day Marketing Push", S["subheading"]))
    push_items = marketing.get("recommendations", [
        "Set up weekly Instagram Reels production cadence (2-3 per week)",
        "Launch monthly email newsletter to existing email signup list",
        "Set up Meta ads with $25/day budget on happy hour and lunch angles",
        "Implement simple punch-card loyalty program via Toast or Square POS",
        "Reach out to 5 local food bloggers for restaurant features",
        "Reactivate TikTok with 'POV: You ordered the carbonara' Reel-format content",
    ])
    for i, p in enumerate(push_items, 1):
        elements.append(Paragraph(f"{i}. {p}", S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 7 — COMPETITOR COMPARISON
    # =====================================================================
    elements.append(Paragraph("Local Competitor Comparison", S["heading"]))
    elements.append(Spacer(1, 6))

    comp = data.get("competition", {})

    elements.append(Paragraph("Head-to-Head Scorecard", S["subheading"]))
    competitors = comp.get("competitors", [
        {"name": name, "rating": "4.2", "reviews": "412", "social_followers": "1,247", "score": 28},
        {"name": "Competitor A", "rating": "4.5", "reviews": "1,247", "social_followers": "12,400", "score": 43},
        {"name": "Competitor B", "rating": "4.4", "reviews": "892", "social_followers": "4,800", "score": 38},
        {"name": "Competitor C", "rating": "4.3", "reviews": "612", "social_followers": "2,100", "score": 33},
        {"name": "Competitor D", "rating": "4.6", "reviews": "310", "social_followers": "8,700", "score": 38},
        {"name": "Competitor E", "rating": "4.0", "reviews": "1,420", "social_followers": "800", "score": 31},
    ])

    cp_tbl = [["Restaurant", "Rating", "Reviews", "IG Followers", "Total Score /50"]]
    for c in competitors:
        cp_tbl.append([c.get("name", "")[:24], c.get("rating", ""),
                       c.get("reviews", ""), c.get("social_followers", ""),
                       str(c.get("score", ""))])
    cp_t = Table(cp_tbl, colWidths=[150, 60, 70, 95, 105])
    cp_extra = [("ALIGN", (1, 0), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, 1), (-1, 1), COLORS["orange_light"]),
                ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold")]
    cp_t.setStyle(standard_table_style(cp_extra))
    elements.append(cp_t)
    elements.append(Spacer(1, 14))

    # Competitor chart
    comp_names = [c.get("name", "") for c in competitors]
    comp_scores = [c.get("score", 0) for c in competitors]
    elements.append(Paragraph("Total Score Comparison", S["subheading"]))
    cc = create_competitor_chart(comp_names, comp_scores)
    elements.append(cc)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Positioning Gaps to Own", S["subheading"]))
    gaps_to_own = comp.get("positioning_gaps", [
        "Family-style 'Sunday Sauce' Italian — no local competitor offers",
        "Cooking classes — revenue diversification + UGC opportunity",
        "Late-night dining (10pm-12am Fri/Sat) — uncontested daypart",
        "Wine club program — only one competitor has a basic version",
        "Sub-$15/head catering — competitors at $18+ — value entry point",
    ])
    for g in gaps_to_own:
        elements.append(Paragraph(f"• {g}", S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 8 — 90-DAY ACTION PLAN
    # =====================================================================
    elements.append(Paragraph("90-Day Action Plan", S["heading"]))
    elements.append(Spacer(1, 6))

    plan = data.get("action_plan", {})

    elements.append(Paragraph("Week 1 — Quick Wins (Today)", S["subheading"]))
    week1 = plan.get("week_1", [
        "Add online order link to Google Business Profile (5 min)",
        "Upload 18 photos to GBP (30 min)",
        "Reply to 10 unanswered negative Google reviews (60 min)",
        "Standardize NAP across 6 directories (60 min)",
        "Launch first weekly Instagram Reel",
    ])
    for i, w in enumerate(week1, 1):
        elements.append(Paragraph(f"{i}. {w}", S["body"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Days 8-30 — Foundations", S["subheading"]))
    days_8_30 = plan.get("days_8_30", [
        "Set up review response system (15 min/day weekly slot)",
        "Reprice 5 underpriced items (carbonara, ribeye, wine glass)",
        "Add 3 strategic menu add-ons (Bolognese upgrade, truffle, dessert duo)",
        "Schedule and complete food photography shoot (top 12 missing items)",
        "Launch monthly email newsletter to existing list",
        "Set up simple punch-card loyalty program (Toast/Square)",
    ])
    for i, d in enumerate(days_8_30, 1):
        elements.append(Paragraph(f"{i}. {d}", S["body"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Days 31-90 — Compounding Plays", S["subheading"]))
    days_31_90 = plan.get("days_31_90", [
        "Launch 'Sunday Sauce' family-style service (own a unique angle)",
        "Begin Meta ad spend at $25/day on best-performing angle",
        "Reach out to 5 local food bloggers and 3 press outlets",
        "Add Restaurant schema markup and 4 dedicated dish landing pages",
        "Start consistent TikTok cadence (3-5 posts/week)",
        "Set up birthday automation and win-back email flows",
    ])
    for i, d in enumerate(days_31_90, 1):
        elements.append(Paragraph(f"{i}. {d}", S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 9 — REVENUE OPPORTUNITY + DISCLAIMER
    # =====================================================================
    elements.append(Paragraph("Revenue Opportunity Summary", S["heading"]))
    elements.append(Spacer(1, 8))

    rev = data.get("revenue_opportunity", {})
    rev_items = rev.get("items", [
        {"source": "Owner response rate → 100% on negatives", "monthly_lift": "+$2,500-$4,500"},
        {"source": "Menu engineering (golden triangle + add-ons)", "monthly_lift": "+$3,000-$5,500"},
        {"source": "Online ordering on GBP", "monthly_lift": "+$2,000-$4,000"},
        {"source": "GBP photo expansion + posts", "monthly_lift": "+$800-$1,500"},
        {"source": "Loyalty program", "monthly_lift": "+$1,200-$2,500"},
        {"source": "Email marketing", "monthly_lift": "+$500-$2,000"},
        {"source": "Meta ads ($25/day)", "monthly_lift": "+$3,000-$8,000"},
        {"source": "Pricing optimization (underpriced items)", "monthly_lift": "+$2,000-$3,500"},
    ])

    rv_tbl = [["Source", "Estimated Monthly Lift"]]
    for r in rev_items:
        rv_tbl.append([r.get("source", ""), r.get("monthly_lift", "")])

    # Total row
    rv_tbl.append(["TOTAL ESTIMATED MONTHLY LIFT", rev.get("total", "+$15,000-$31,500/month")])

    rv_t = Table(rv_tbl, colWidths=[330, 130])
    rv_extra = [
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), COLORS["orange_light"]),
        ("TEXTCOLOR", (0, -1), (-1, -1), COLORS["red_dark"]),
    ]
    rv_t.setStyle(standard_table_style(rv_extra))
    elements.append(rv_t)
    elements.append(Spacer(1, 18))

    annual = rev.get("annual_estimate", "+$180,000 to $378,000/year")
    elements.append(Paragraph(
        f'<b>Annualized opportunity:</b> <font color="{COLORS["red"].hexval()}">{annual}</font>',
        ParagraphStyle("AnnRev", parent=S["body"], fontSize=14,
                       fontName="Helvetica-Bold", alignment=1, spaceAfter=14)
    ))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Notes", S["subheading"]))
    notes = data.get("notes",
        "These estimates assume current cover counts hold and recommendations are implemented in priority order. "
        "Revenue ranges reflect conservative (low) to optimistic (high) scenarios. The largest lever is usually "
        "the combination of menu engineering + online presence optimization, which compound together. "
        "Marketing channels (ads, email, loyalty) need 30-60 days to mature before delivering full ROI."
    )
    elements.append(Paragraph(notes, S["body"]))

    elements.append(Spacer(1, 22))
    elements.append(Paragraph(
        "Generated by AI Restaurant Team for Claude Code", S["footer"]
    ))
    elements.append(Paragraph(DISCLAIMER_TEXT, S["disclaimer"]))

    # Build
    doc.build(elements)
    return output_path


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------
def get_demo_data():
    return {
        "restaurant_name": "Bella Italia Trattoria",
        "city": "Austin, TX",
        "cuisine": "Italian",
        "restaurant_type": "Casual Dining",
        "price_tier": "$$",
        "date": datetime.now().strftime("%B %d, %Y"),
        "overall_score": 64,
        "profile": {
            "google_rating": "4.2 (412 reviews)",
            "yelp_rating": "3.9 (287 reviews)",
            "years_open": "Since 2014",
            "seating": "85 seats",
        },
        "categories": {
            "Reviews & Reputation": {"score": 68, "weight": "25%"},
            "Menu & Pricing": {"score": 72, "weight": "20%"},
            "Online Presence": {"score": 55, "weight": "20%"},
            "Marketing & Engagement": {"score": 48, "weight": "15%"},
            "Local Competition": {"score": 70, "weight": "20%"},
        },
        "executive_summary": (
            "Bella Italia Trattoria is a 10-year-old family-owned Italian casual dining restaurant in Austin "
            "with strong food fundamentals (4.2 Google stars, 412 reviews) but significant gaps in online "
            "presence and marketing engagement. The restaurant's pricing is competitive — actually 12-25% "
            "below local Italian leaders on signature dishes — but the photography quality and social media "
            "cadence trail competitors. Owner response rate on negative reviews is only 12% (industry top "
            "decile: 100%). Closing the top 5 quick wins should lift monthly revenue by an estimated "
            "$4,800-$9,800, with the 90-day plan unlocking a $15,000-$31,500/month opportunity at "
            "annualized $180K-$378K."
        ),
        "reviews": {
            "score": 68,
            "platforms": [
                {"name": "Google", "rating": "4.2", "count": "412", "response_rate": "12%"},
                {"name": "Yelp", "rating": "3.9", "count": "287", "response_rate": "20%"},
                {"name": "TripAdvisor", "rating": "4.0", "count": "98", "response_rate": "0%"},
                {"name": "DoorDash", "rating": "4.4", "count": "187", "response_rate": "n/a"},
            ],
            "complaints": [
                {"theme": "Slow service", "freq": "~28%", "example": "Waited 45 minutes on a Tuesday."},
                {"theme": "Cold food on delivery", "freq": "~22%", "example": "Pasta arrived lukewarm."},
                {"theme": "Noise level", "freq": "~18%", "example": "Couldn't hear my date."},
                {"theme": "Parking", "freq": "~14%", "example": "Circled the block 4 times."},
                {"theme": "Portion vs price", "freq": "~10%", "example": "Expected more for $24."},
            ],
            "praises": [
                {"theme": "Carbonara dish", "freq": "~35%", "example": "Best carbonara in Austin."},
                {"theme": "Server Maria", "freq": "~20%", "example": "Maria remembered my favorite wine."},
                {"theme": "Atmosphere", "freq": "~18%", "example": "Felt like Italy."},
                {"theme": "Wine list", "freq": "~15%", "example": "Great Barolo selection."},
                {"theme": "Owner Marco", "freq": "~12%", "example": "Marco came by to say hi."},
            ],
        },
        "menu": {
            "score": 72,
            "kasavana": {
                "Stars (high pop, high margin)": 4,
                "Plowhorses (high pop, low margin)": 8,
                "Puzzles (low pop, high margin)": 5,
                "Dogs (low pop, low margin)": 4,
            },
            "quick_wins": [
                {"action": "Move Carbonara to top-right of menu (golden triangle)", "effort": "Zero", "lift": "+5-8% category"},
                {"action": "Rewrite Lasagna description with sensory language", "effort": "30 min", "lift": "+$1.50/plate"},
                {"action": "Add 'Make it Bolognese' (+$4) modifier to all pastas", "effort": "POS update", "lift": "+$1.50/cover"},
                {"action": "Photograph Branzino + add 'Chef's Pick' badge", "effort": "Photo session", "lift": "+30-50%"},
                {"action": "Remove Three Cheese Ravioli (Dog)", "effort": "Drawdown", "lift": "Less waste"},
            ],
            "pricing": [
                {"item": "Margherita Pizza", "subject": "$16", "market_avg": "$18.50", "position": "Underpriced"},
                {"item": "Carbonara", "subject": "$19", "market_avg": "$21.50", "position": "Underpriced"},
                {"item": "Ribeye", "subject": "$42", "market_avg": "$48", "position": "Underpriced"},
                {"item": "Tiramisu", "subject": "$11", "market_avg": "$9.50", "position": "Overpriced"},
                {"item": "House Wine (glass)", "subject": "$9", "market_avg": "$11.50", "position": "Underpriced"},
            ],
        },
        "online": {
            "channels": [
                {"channel": "Google Business Profile", "score": "60/100", "status": "Mixed", "key_gap": "Missing online order link, 0 posts in 30 days"},
                {"channel": "Yelp", "score": "70/100", "status": "OK", "key_gap": "Reservations not enabled"},
                {"channel": "Website", "score": "45/100", "status": "Weak", "key_gap": "No online ordering, no schema"},
                {"channel": "Delivery Platforms", "score": "55/100", "status": "Mixed", "key_gap": "Photo coverage 60% / 40%"},
                {"channel": "NAP Consistency", "score": "50/100", "status": "Weak", "key_gap": "3 directory mismatches"},
            ],
            "critical_gaps": [
                "Add online ordering link to Google Business Profile — losing direct-order revenue daily",
                "Upload 18 more photos to GBP (currently 12, target 30+) — 2x click lift potential",
                "Reply to 4 unanswered Q&A questions on GBP",
                "Standardize NAP across 6 platforms (currently 3 mismatches)",
                "Add Restaurant schema markup to website for Google rich results",
                "Claim Apple Maps listing (currently invisible to iOS users)",
            ],
        },
        "marketing": {
            "audit": [
                {"area": "Instagram posting", "current": "3 / 30d", "benchmark": "12-20 / 30d", "gap": "Major"},
                {"area": "Instagram Reels", "current": "0 / 30d", "benchmark": "8-12 / 30d", "gap": "Critical"},
                {"area": "TikTok", "current": "Dormant 5mo", "benchmark": "12+ / mo", "gap": "Critical"},
                {"area": "Email marketing", "current": "0 sends/mo", "benchmark": "4-8 sends/mo", "gap": "Major"},
                {"area": "Loyalty program", "current": "None", "benchmark": "Active", "gap": "Major"},
                {"area": "Meta ads", "current": "$0/mo", "benchmark": "$500-2k/mo", "gap": "Major"},
            ],
            "recommendations": [
                "Set up weekly Instagram Reels production (2-3 per week)",
                "Launch monthly email newsletter to existing signup list",
                "Set up Meta ads at $25/day on happy hour and lunch angles",
                "Implement punch-card loyalty via Toast or Square POS",
                "Reach out to 5 local food bloggers for features",
                "Reactivate TikTok with POV-style content",
            ],
        },
        "competition": {
            "competitors": [
                {"name": "Bella Italia Trattoria", "rating": "4.2", "reviews": "412", "social_followers": "1,247", "score": 28},
                {"name": "Tony's Pizzeria", "rating": "4.5", "reviews": "1,247", "social_followers": "12,400", "score": 43},
                {"name": "Sapore Italiano", "rating": "4.4", "reviews": "892", "social_followers": "4,800", "score": 38},
                {"name": "Casa Romana", "rating": "4.3", "reviews": "612", "social_followers": "2,100", "score": 33},
                {"name": "Nonna's Kitchen", "rating": "4.6", "reviews": "310", "social_followers": "8,700", "score": 38},
                {"name": "Italia Classica", "rating": "4.0", "reviews": "1,420", "social_followers": "800", "score": 31},
            ],
            "positioning_gaps": [
                "Family-style 'Sunday Sauce' Italian — no local competitor offers",
                "Cooking classes — revenue diversification + UGC opportunity",
                "Late-night dining (10pm-12am Fri/Sat) — uncontested daypart",
                "Wine club program — only one competitor has a basic version",
                "Sub-$15/head catering — competitors at $18+",
            ],
        },
        "action_plan": {
            "week_1": [
                "Add online order link to Google Business Profile (5 min)",
                "Upload 18 photos to GBP (30 min)",
                "Reply to 10 unanswered negative Google reviews (60 min)",
                "Standardize NAP across 6 directories (60 min)",
                "Launch first weekly Instagram Reel",
            ],
            "days_8_30": [
                "Set up review response system (15 min/day weekly slot)",
                "Reprice 5 underpriced items (carbonara, ribeye, wine glass, pizza, pasta)",
                "Add 3 strategic menu add-ons (Bolognese, truffle, dessert duo)",
                "Schedule food photography shoot (top 12 missing items)",
                "Launch monthly email newsletter to existing list",
                "Set up punch-card loyalty (Toast/Square)",
            ],
            "days_31_90": [
                "Launch 'Sunday Sauce' family-style service",
                "Begin Meta ad spend at $25/day on best-performing angle",
                "Reach out to 5 local food bloggers and 3 press outlets",
                "Add Restaurant schema markup + 4 dish landing pages",
                "Start consistent TikTok cadence (3-5 posts/week)",
                "Set up birthday and win-back email automations",
            ],
        },
        "revenue_opportunity": {
            "items": [
                {"source": "Owner response rate to 100% on negatives", "monthly_lift": "+$2,500-$4,500"},
                {"source": "Menu engineering (golden triangle + add-ons)", "monthly_lift": "+$3,000-$5,500"},
                {"source": "Online ordering on GBP", "monthly_lift": "+$2,000-$4,000"},
                {"source": "GBP photo expansion + posts", "monthly_lift": "+$800-$1,500"},
                {"source": "Loyalty program launch", "monthly_lift": "+$1,200-$2,500"},
                {"source": "Email marketing reactivation", "monthly_lift": "+$500-$2,000"},
                {"source": "Meta ads ($25/day starter)", "monthly_lift": "+$3,000-$8,000"},
                {"source": "Pricing optimization (underpriced items)", "monthly_lift": "+$2,000-$3,500"},
            ],
            "total": "+$15,000-$31,500/month",
            "annual_estimate": "+$180,000 to $378,000/year",
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--demo":
        data = get_demo_data()
        output = "RESTAURANT-REPORT-sample.pdf"
        generate_report(data, output)
        print(f"Sample report generated: {output}")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "RESTAURANT-REPORT.pdf"

    with open(input_file, "r") as f:
        data = json.load(f)

    generate_report(data, output_file)
    print(f"Report generated: {output_file}")


if __name__ == "__main__":
    main()
