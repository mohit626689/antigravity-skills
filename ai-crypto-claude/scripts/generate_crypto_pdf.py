#!/usr/bin/env python3
"""
AI Crypto Research Report PDF Generator — AI Crypto Claude Code Skills
Generates professional 6-page PDF crypto research reports with score gauges,
bar charts, on-chain/tokenomics tables, sentiment, technical levels,
investment thesis, and risk matrix.

Requires: reportlab (pip install reportlab)

Usage:
  python3 generate_crypto_pdf.py                        # Demo mode
  python3 generate_crypto_pdf.py --demo                 # Demo mode (explicit)
  python3 generate_crypto_pdf.py data.json              # From JSON
  python3 generate_crypto_pdf.py data.json output.pdf   # From JSON with custom output
"""

import sys
import json
import os
import math
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, PageBreak)
    from reportlab.graphics.shapes import Drawing, Rect, Circle, String, Line, Wedge
except ImportError:
    print("Error: reportlab is required. Install with: pip install reportlab")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Color palette — Crypto / Dark theme
# ---------------------------------------------------------------------------
COLORS = {
    "deep_dark": HexColor("#0a0a1a"),        # Deep dark background
    "purple": HexColor("#7c3aed"),           # Crypto purple (primary)
    "bitcoin": HexColor("#f7931a"),          # Bitcoin orange
    "neon_green": HexColor("#00ff88"),       # Neon green (buy/bull)
    "neon_blue": HexColor("#00d4ff"),        # Neon blue (info)
    "danger": HexColor("#ef4444"),           # Danger red (sell/bear)
    "gold": HexColor("#fbbf24"),             # Gold accent
    "gray": HexColor("#78909c"),             # Muted gray
    "light_bg": HexColor("#f0f4f8"),         # Light background
    "dark_card": HexColor("#12122a"),        # Dark card bg
    "text": HexColor("#1e293b"),             # Dark text
    "text_light": HexColor("#64748b"),       # Light text
    "border": HexColor("#cbd5e1"),           # Border
    "header_bg": HexColor("#1e1045"),        # Table header (dark purple)
    "white": white,
    "black": black,
}


def score_color(score):
    """Return color based on crypto score value."""
    if score >= 70:
        return COLORS["neon_green"]
    elif score >= 40:
        return COLORS["gold"]
    else:
        return COLORS["danger"]


def score_grade(score):
    """Return crypto grade from score."""
    if score >= 85:
        return "A+"
    elif score >= 70:
        return "A"
    elif score >= 55:
        return "B"
    elif score >= 40:
        return "C"
    elif score >= 25:
        return "D"
    else:
        return "F"


def crypto_signal(score):
    """Return crypto signal from score."""
    if score >= 85:
        return "STRONG BUY"
    elif score >= 70:
        return "BUY"
    elif score >= 55:
        return "HOLD / ACCUMULATE"
    elif score >= 40:
        return "NEUTRAL"
    elif score >= 25:
        return "CAUTION"
    else:
        return "AVOID"


def signal_color(score):
    """Return color for the crypto signal."""
    if score >= 70:
        return COLORS["neon_green"]
    elif score >= 55:
        return COLORS["neon_blue"]
    elif score >= 40:
        return COLORS["gold"]
    else:
        return COLORS["danger"]


def draw_score_gauge(score, size=140):
    """Create a circular score gauge with crypto-themed styling."""
    d = Drawing(size + 20, size + 20)

    cx = size / 2 + 10
    cy = size / 2 + 10

    # Outer ring background
    d.add(Circle(cx, cy, size / 2,
                 fillColor=COLORS["light_bg"], strokeColor=COLORS["purple"], strokeWidth=2))

    # Score arc (colored ring)
    color = score_color(score)
    inner_r = size / 2 - 8
    d.add(Circle(cx, cy, inner_r,
                 fillColor=color, strokeColor=None))

    # White center
    d.add(Circle(cx, cy, inner_r - 14,
                 fillColor=COLORS["white"], strokeColor=None))

    # Score text
    d.add(String(cx, cy + 2, str(int(score)),
                 fontSize=36, fillColor=COLORS["deep_dark"],
                 textAnchor="middle", fontName="Helvetica-Bold"))

    # "/ 100" label
    d.add(String(cx, cy - 18, "/ 100",
                 fontSize=10, fillColor=COLORS["gray"],
                 textAnchor="middle", fontName="Helvetica"))

    return d


def create_bar_chart(categories, scores, width=470, height=200):
    """Create horizontal bar charts for category scores."""
    d = Drawing(width, height)

    bar_height = 20
    gap = 14
    max_bar_width = width - 200
    start_y = height - 25
    label_x = 5
    bar_x = 170

    for i, (cat, score) in enumerate(zip(categories, scores)):
        y = start_y - i * (bar_height + gap)

        # Category label
        d.add(String(label_x, y + 5, cat[:25],
                     fontSize=9, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica"))

        # Background bar
        d.add(Rect(bar_x, y, max_bar_width, bar_height,
                   fillColor=COLORS["light_bg"], strokeColor=None, rx=3))

        # Score bar — color coded by range
        bar_width = max((score / 100) * max_bar_width, 2)
        color = score_color(score)
        d.add(Rect(bar_x, y, bar_width, bar_height,
                   fillColor=color, strokeColor=None, rx=3))

        # Score label
        d.add(String(bar_x + max_bar_width + 10, y + 5, f"{int(score)}/100",
                     fontSize=10, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica-Bold"))

    return d


# ---------------------------------------------------------------------------
# Custom styles
# ---------------------------------------------------------------------------
def get_styles():
    """Create custom paragraph styles for crypto reports."""
    styles = getSampleStyleSheet()

    custom = {
        "title": ParagraphStyle(
            "CryptoTitle", parent=styles["Title"],
            fontSize=30, textColor=COLORS["purple"],
            spaceAfter=4, fontName="Helvetica-Bold",
            leading=36
        ),
        "token": ParagraphStyle(
            "CryptoToken", parent=styles["Title"],
            fontSize=48, textColor=COLORS["bitcoin"],
            spaceAfter=4, fontName="Helvetica-Bold",
            leading=56
        ),
        "subtitle": ParagraphStyle(
            "CryptoSubtitle", parent=styles["Normal"],
            fontSize=14, textColor=COLORS["gray"],
            spaceAfter=6, fontName="Helvetica"
        ),
        "heading": ParagraphStyle(
            "CryptoHeading", parent=styles["Heading1"],
            fontSize=20, textColor=COLORS["purple"],
            spaceBefore=16, spaceAfter=10,
            fontName="Helvetica-Bold"
        ),
        "subheading": ParagraphStyle(
            "CryptoSubheading", parent=styles["Heading2"],
            fontSize=14, textColor=COLORS["neon_blue"],
            spaceBefore=12, spaceAfter=6,
            fontName="Helvetica-Bold"
        ),
        "body": ParagraphStyle(
            "CryptoBody", parent=styles["Normal"],
            fontSize=10, textColor=COLORS["text"],
            spaceAfter=6, fontName="Helvetica", leading=14
        ),
        "body_small": ParagraphStyle(
            "CryptoBodySmall", parent=styles["Normal"],
            fontSize=8, textColor=COLORS["text"],
            spaceAfter=4, fontName="Helvetica", leading=11
        ),
        "signal": ParagraphStyle(
            "CryptoSignal", parent=styles["Title"],
            fontSize=22, textColor=COLORS["neon_green"],
            spaceAfter=4, fontName="Helvetica-Bold",
            alignment=1
        ),
        "footer": ParagraphStyle(
            "CryptoFooter", parent=styles["Normal"],
            fontSize=7, textColor=COLORS["gray"],
            fontName="Helvetica", leading=10
        ),
        "disclaimer": ParagraphStyle(
            "CryptoDisclaimer", parent=styles["Normal"],
            fontSize=6.5, textColor=COLORS["gray"],
            fontName="Helvetica", leading=9,
            spaceBefore=8
        ),
        "grade_large": ParagraphStyle(
            "CryptoGrade", parent=styles["Title"],
            fontSize=18, textColor=COLORS["deep_dark"],
            spaceAfter=6, fontName="Helvetica-Bold",
            alignment=1
        ),
        "bullet": ParagraphStyle(
            "CryptoBullet", parent=styles["Normal"],
            fontSize=10, textColor=COLORS["text"],
            spaceAfter=4, fontName="Helvetica", leading=14,
            leftIndent=16, bulletIndent=4
        ),
    }
    return custom


# ---------------------------------------------------------------------------
# Table style helpers
# ---------------------------------------------------------------------------
def standard_table_style(extra=None):
    """Return a standard table style with crypto-themed header."""
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), COLORS["header_bg"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["white"]),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLORS["white"], COLORS["light_bg"]]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if extra:
        cmds.extend(extra)
    return TableStyle(cmds)


DISCLAIMER_TEXT = (
    "DISCLAIMER: This report is generated by AI for educational and research purposes only. "
    "It is NOT financial advice. Cryptocurrency investments are highly volatile and speculative. "
    "It does NOT constitute a recommendation to buy, sell, or hold any token or digital asset. "
    "Past performance does not guarantee future results. You could lose your entire investment. "
    "Always DYOR (Do Your Own Research) and consult a licensed financial advisor. "
    "The authors and creators of this tool accept no liability for any losses incurred."
)


# ---------------------------------------------------------------------------
# Report generator
# ---------------------------------------------------------------------------
def generate_report(data, output_path):
    """Generate a professional 6-page crypto research PDF report."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    S = get_styles()
    elements = []

    token_symbol = data.get("token_symbol", "BTC")
    token_name = data.get("token_name", "Bitcoin")
    date_str = data.get("date", datetime.now().strftime("%B %d, %Y"))
    overall_score = data.get("overall_score", 0)
    grade = score_grade(overall_score)
    signal = crypto_signal(overall_score)
    sig_color = signal_color(overall_score)

    # =====================================================================
    # PAGE 1 — COVER
    # =====================================================================
    elements.append(Spacer(1, 0.6 * inch))
    elements.append(Paragraph("AI Crypto Research Report", S["title"]))
    elements.append(Spacer(1, 40))
    elements.append(Paragraph(token_symbol.upper(), S["token"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(token_name, ParagraphStyle(
        "TokenName", parent=S["subtitle"], fontSize=18,
        textColor=COLORS["neon_blue"], spaceAfter=4
    )))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"Generated: {date_str}", S["subtitle"]))
    elements.append(Spacer(1, 35))

    # Score gauge
    gauge = draw_score_gauge(overall_score, size=140)
    elements.append(gauge)
    elements.append(Spacer(1, 30))

    # Grade + signal
    color = score_color(overall_score)
    elements.append(Paragraph(
        f'Crypto Score: <font color="{color.hexval()}">{int(overall_score)}/100</font> '
        f'(Grade: <font color="{color.hexval()}">{grade}</font>)',
        S["grade_large"]
    ))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        f'Signal: <font color="{sig_color.hexval()}">{signal}</font>',
        ParagraphStyle("SignalLine", parent=S["signal"],
                       textColor=sig_color, fontSize=24)
    ))

    elements.append(Spacer(1, 50))

    # Disclaimer at bottom of cover
    elements.append(Paragraph(DISCLAIMER_TEXT, S["disclaimer"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 2 — SCORE DASHBOARD
    # =====================================================================
    elements.append(Paragraph("Score Dashboard", S["heading"]))
    elements.append(Spacer(1, 6))

    categories = data.get("categories", {})
    default_cats = {
        "On-Chain Health": {"score": 68, "weight": "20%"},
        "Tokenomics Quality": {"score": 72, "weight": "20%"},
        "Sentiment & Momentum": {"score": 65, "weight": "20%"},
        "Technical Setup": {"score": 70, "weight": "20%"},
        "Fundamental Strength": {"score": 60, "weight": "20%"},
    }
    if not categories:
        categories = default_cats

    cat_names = list(categories.keys())
    cat_scores = [categories[c].get("score", 50) if isinstance(categories[c], dict)
                  else categories[c] for c in cat_names]

    # Bar chart
    chart = create_bar_chart(cat_names, cat_scores)
    elements.append(chart)
    elements.append(Spacer(1, 16))

    # Signal badge line
    elements.append(Paragraph(
        f'Composite Crypto Score: <font color="{color.hexval()}">'
        f'{int(overall_score)}/100</font> &nbsp; | &nbsp; '
        f'Grade: <font color="{color.hexval()}">{grade}</font> &nbsp; | &nbsp; '
        f'Signal: <font color="{sig_color.hexval()}">{signal}</font>',
        ParagraphStyle("SignalBadge", parent=S["body"], fontSize=12,
                       fontName="Helvetica-Bold", alignment=1, spaceAfter=12)
    ))

    # Score breakdown table
    score_data = [["Category", "Score", "Weight", "Status"]]
    for name, score in zip(cat_names, cat_scores):
        weight = categories[name].get("weight", "--") if isinstance(categories[name], dict) else "--"
        if score >= 70:
            status = "Strong"
        elif score >= 40:
            status = "Mixed"
        else:
            status = "Weak"
        score_data.append([name, f"{int(score)}/100", weight, status])

    score_table = Table(score_data, colWidths=[160, 80, 60, 100])
    score_style_extra = [("ALIGN", (1, 0), (-1, -1), "CENTER")]
    for i, sc in enumerate(cat_scores, 1):
        c = score_color(sc)
        score_style_extra.append(("TEXTCOLOR", (3, i), (3, i), c))
        score_style_extra.append(("FONTNAME", (3, i), (3, i), "Helvetica-Bold"))
    score_table.setStyle(standard_table_style(score_style_extra))
    elements.append(score_table)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 3 — ON-CHAIN & TOKENOMICS
    # =====================================================================
    elements.append(Paragraph("On-Chain Analytics &amp; Tokenomics", S["heading"]))
    elements.append(Spacer(1, 6))

    # On-chain metrics table
    elements.append(Paragraph("Key On-Chain Metrics", S["subheading"]))
    onchain = data.get("onchain", {})

    onchain_metrics = onchain.get("metrics", [
        {"metric": "Active Addresses (24h)", "value": "1.02M", "trend": "Up 8% (7d)", "assessment": "Growing network usage"},
        {"metric": "Whale Transactions (>$100K)", "value": "4,218", "trend": "Up 15% (7d)", "assessment": "Accumulation signal"},
        {"metric": "Exchange Net Flow", "value": "-12,450 BTC", "trend": "Outflows 5 days", "assessment": "Supply leaving exchanges"},
        {"metric": "NVT Ratio", "value": "42.3", "trend": "Below 90d avg", "assessment": "Not overvalued by activity"},
        {"metric": "Hash Rate / Validators", "value": "612 EH/s", "trend": "All-time high", "assessment": "Strong network security"},
    ])

    oc_data = [["Metric", "Value", "Trend", "Assessment"]]
    for m in onchain_metrics:
        oc_data.append([m.get("metric", ""), m.get("value", ""),
                        m.get("trend", ""), Paragraph(m.get("assessment", ""), S["body_small"])])

    oc_table = Table(oc_data, colWidths=[130, 85, 100, 155])
    oc_table.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(oc_table)
    elements.append(Spacer(1, 16))

    # Tokenomics summary
    elements.append(Paragraph("Tokenomics Summary", S["subheading"]))
    tokenomics = data.get("tokenomics", {})

    token_metrics = tokenomics.get("metrics", [
        {"metric": "Circulating Supply", "value": "19.6M BTC", "notes": "93.3% of max supply"},
        {"metric": "Max Supply", "value": "21M BTC", "notes": "Hard-capped, deflationary"},
        {"metric": "Fully Diluted Valuation", "value": "$1.42T", "notes": "FDV / Market Cap = 1.07x"},
        {"metric": "Inflation Rate", "value": "1.7% annual", "notes": "Post-halving (Apr 2024)"},
        {"metric": "Staking / Yield", "value": "N/A (PoW)", "notes": "No native staking for BTC"},
        {"metric": "Next Unlock / Event", "value": "Halving 2028", "notes": "Block reward to 1.5625 BTC"},
    ])

    tk_data = [["Metric", "Value", "Notes"]]
    for m in token_metrics:
        tk_data.append([m.get("metric", ""), m.get("value", ""),
                        Paragraph(m.get("notes", ""), S["body_small"])])

    tk_table = Table(tk_data, colWidths=[130, 120, 220])
    tk_table.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(tk_table)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 4 — SENTIMENT & TECHNICAL
    # =====================================================================
    elements.append(Paragraph("Sentiment &amp; Technical Analysis", S["heading"]))
    elements.append(Spacer(1, 6))

    # Sentiment section
    elements.append(Paragraph("Market Sentiment", S["subheading"]))
    sentiment = data.get("sentiment", {})

    fear_greed = sentiment.get("fear_greed", "72 — Greed")
    social_buzz = sentiment.get("social_buzz", "High — trending on CT, Reddit, mainstream media")
    news_tone = sentiment.get("news_tone", "Bullish — ETF inflows, institutional adoption narratives")
    community_health = sentiment.get("community_health", "Strong — active development, engaged governance")

    sent_data = [
        ["Sentiment Metric", "Reading"],
        ["Fear & Greed Index", fear_greed],
        ["Social Buzz Level", social_buzz],
        ["News Tone", news_tone],
        ["Community Health", community_health],
    ]
    sent_table = Table(sent_data, colWidths=[160, 310])
    sent_style = [
        ("ALIGN", (1, 0), (1, -1), "LEFT"),
    ]
    sent_table.setStyle(standard_table_style(sent_style))
    elements.append(sent_table)
    elements.append(Spacer(1, 18))

    # Technical section
    elements.append(Paragraph("Technical Levels &amp; Indicators", S["subheading"]))
    technical = data.get("technical", {})

    key_levels = technical.get("key_levels", [
        {"level": "Resistance 2", "price": "$72,500", "notes": "All-time high zone"},
        {"level": "Resistance 1", "price": "$69,800", "notes": "Recent local high"},
        {"level": "Current Price", "price": "$67,240", "notes": "As of report date"},
        {"level": "Support 1", "price": "$63,500", "notes": "50-day MA convergence"},
        {"level": "Support 2", "price": "$58,200", "notes": "200-day MA / major support"},
    ])

    levels_data = [["Level", "Price", "Notes"]]
    for kl in key_levels:
        levels_data.append([kl.get("level", ""), kl.get("price", ""), kl.get("notes", "")])

    levels_table = Table(levels_data, colWidths=[120, 100, 250])
    levels_table.setStyle(standard_table_style([("ALIGN", (1, 0), (1, -1), "CENTER")]))
    elements.append(levels_table)
    elements.append(Spacer(1, 12))

    # Trend / pattern summary
    trend = technical.get("trend", "Uptrend — higher highs and higher lows on daily timeframe")
    pattern = technical.get("pattern", "Bull flag consolidation above breakout level")
    elements.append(Paragraph(f"<b>Trend Direction:</b> {trend}", S["body"]))
    elements.append(Paragraph(f"<b>Chart Pattern:</b> {pattern}", S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 5 — INVESTMENT THESIS
    # =====================================================================
    elements.append(Paragraph("Investment Thesis", S["heading"]))
    elements.append(Spacer(1, 6))

    thesis = data.get("thesis", {})

    # Bull case
    elements.append(Paragraph("Bull Case", ParagraphStyle(
        "BullCase", parent=S["subheading"], textColor=COLORS["neon_green"])))
    bull_points = thesis.get("bull_case", [
        "Spot ETF inflows accelerating — institutional demand creating sustained buying pressure",
        "Halving supply shock reduces new issuance by 50%, historically precedes major rallies",
        "Macro tailwinds: rate cuts expected H2, weakening DXY, inflation hedge narrative strengthening"
    ])
    for i, pt in enumerate(bull_points, 1):
        elements.append(Paragraph(f"{i}. {pt}", S["body"]))
    elements.append(Spacer(1, 10))

    # Bear case
    elements.append(Paragraph("Bear Case", ParagraphStyle(
        "BearCase", parent=S["subheading"], textColor=COLORS["danger"])))
    bear_points = thesis.get("bear_case", [
        "Regulatory crackdowns could restrict access (SEC enforcement, exchange delistings)",
        "Mt. Gox and government BTC distributions add sell-side pressure (~140K BTC overhang)",
        "Macro risk: persistent inflation could delay rate cuts, strengthening USD hurts risk assets"
    ])
    for i, pt in enumerate(bear_points, 1):
        elements.append(Paragraph(f"{i}. {pt}", S["body"]))
    elements.append(Spacer(1, 10))

    # Catalyst timeline
    elements.append(Paragraph("Catalyst Timeline", S["subheading"]))
    catalysts = thesis.get("catalysts", [
        {"event": "Halving Impact Window", "date": "Q3-Q4 2025", "impact": "High — historical supply shock effect peaks 6-12 months post-halving"},
        {"event": "Fed Rate Decision", "date": "Next FOMC", "impact": "High — rate cuts bullish for risk assets and BTC"},
        {"event": "ETF Quarterly Reports", "date": "Quarterly", "impact": "Medium — reveals institutional adoption pace"},
    ])
    cat_data = [["Event", "Expected Date", "Potential Impact"]]
    for cat in catalysts:
        cat_data.append([cat.get("event", ""), cat.get("date", ""),
                         Paragraph(cat.get("impact", ""), S["body_small"])])
    cat_table = Table(cat_data, colWidths=[140, 90, 240])
    cat_table.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(cat_table)
    elements.append(Spacer(1, 14))

    # Entry/exit strategy
    elements.append(Paragraph("Entry / Exit Strategy", S["subheading"]))
    entry_exit = thesis.get("entry_exit", {})
    entry = entry_exit.get("entry_price", "$62,000 - $65,000")
    target = entry_exit.get("target_price", "$85,000 - $100,000")
    stop = entry_exit.get("stop_loss", "$55,000")
    timeframe = entry_exit.get("timeframe", "6-12 months")

    ee_data = [
        ["Parameter", "Level"],
        ["Entry Zone", entry],
        ["Price Target", target],
        ["Stop Loss", stop],
        ["Timeframe", timeframe],
    ]
    ee_table = Table(ee_data, colWidths=[160, 200])
    ee_style = [
        ("TEXTCOLOR", (1, 1), (1, 1), COLORS["neon_blue"]),
        ("TEXTCOLOR", (1, 2), (1, 2), COLORS["neon_green"]),
        ("TEXTCOLOR", (1, 3), (1, 3), COLORS["danger"]),
        ("FONTNAME", (1, 1), (1, 4), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
    ]
    ee_table.setStyle(standard_table_style(ee_style))
    elements.append(ee_table)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 6 — RISK MATRIX & POSITION SIZING
    # =====================================================================
    elements.append(Paragraph("Risk Matrix &amp; Position Sizing", S["heading"]))
    elements.append(Spacer(1, 6))

    risk = data.get("risk", {})

    # Risk factors table
    elements.append(Paragraph("Risk Factors", S["subheading"]))
    risk_factors = risk.get("risk_factors", [
        {"factor": "Regulatory / Legal", "probability": "Medium", "impact": "High", "notes": "SEC actions, global crypto regulation"},
        {"factor": "Smart Contract / Protocol", "probability": "Low", "impact": "Critical", "notes": "Exploit risk (for DeFi/L1 tokens)"},
        {"factor": "Market / Volatility", "probability": "High", "impact": "High", "notes": "30-50% drawdowns are normal in crypto"},
        {"factor": "Liquidity Risk", "probability": "Low", "impact": "Medium", "notes": "BTC has deep liquidity; altcoins vary"},
        {"factor": "Macro / Correlation", "probability": "Medium", "impact": "Medium", "notes": "Crypto increasingly correlated to NASDAQ"},
    ])

    rf_data = [["Risk Factor", "Probability", "Impact", "Notes"]]
    for rf in risk_factors:
        rf_data.append([rf.get("factor", ""), rf.get("probability", ""),
                        rf.get("impact", ""),
                        Paragraph(rf.get("notes", ""), S["body_small"])])
    rf_table = Table(rf_data, colWidths=[120, 75, 70, 205])
    rf_style = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (1, 0), (2, -1), "CENTER")]
    rf_table.setStyle(standard_table_style(rf_style))
    elements.append(rf_table)
    elements.append(Spacer(1, 16))

    # Position sizing recommendation
    elements.append(Paragraph("Position Sizing Recommendation", S["subheading"]))
    position_rec = risk.get("position_recommendation",
        "Crypto is high-volatility. Never allocate more than 5-10% of total portfolio to crypto. "
        "For a single token position, limit to 1-3% of total portfolio. Use dollar-cost averaging (DCA) "
        "for entries rather than lump-sum. Set hard stop-losses. Keep stablecoins for rebalancing. "
        "Consider cold storage for long-term holdings."
    )
    elements.append(Paragraph(position_rec, S["body"]))
    elements.append(Spacer(1, 14))

    # Scenario analysis
    elements.append(Paragraph("Scenario Analysis", S["subheading"]))
    scenarios = risk.get("scenarios", [
        {"scenario": "Bull Case", "probability": "30%", "return": "+50% to +100%",
         "trigger": "ETF inflows + halving supply shock + rate cuts"},
        {"scenario": "Base Case", "probability": "40%", "return": "+10% to +40%",
         "trigger": "Steady adoption, range-bound with upward bias"},
        {"scenario": "Bear Case", "probability": "30%", "return": "-20% to -50%",
         "trigger": "Regulatory crackdown + macro recession + black swan event"},
    ])
    sc_data = [["Scenario", "Probability", "Expected Return", "Trigger"]]
    for sc in scenarios:
        sc_data.append([sc.get("scenario", ""), sc.get("probability", ""),
                        sc.get("return", ""),
                        Paragraph(sc.get("trigger", ""), S["body_small"])])
    sc_table = Table(sc_data, colWidths=[85, 80, 110, 195])
    sc_style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
    ]
    if len(scenarios) >= 3:
        sc_style.append(("TEXTCOLOR", (2, 1), (2, 1), COLORS["neon_green"]))
        sc_style.append(("TEXTCOLOR", (2, 2), (2, 2), COLORS["neon_blue"]))
        sc_style.append(("TEXTCOLOR", (2, 3), (2, 3), COLORS["danger"]))
        sc_style.append(("FONTNAME", (2, 1), (2, 3), "Helvetica-Bold"))
    sc_table.setStyle(standard_table_style(sc_style))
    elements.append(sc_table)

    elements.append(Spacer(1, 24))

    # Footer + disclaimer
    elements.append(Paragraph(
        "Generated by AI Crypto Analyst for Claude Code", S["footer"]
    ))
    elements.append(Paragraph(DISCLAIMER_TEXT, S["disclaimer"]))

    # Build PDF
    doc.build(elements)
    return output_path


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------
def get_demo_data():
    """Return sample data for demo mode."""
    return {
        "token_symbol": "BTC",
        "token_name": "Bitcoin",
        "date": datetime.now().strftime("%B %d, %Y"),
        "overall_score": 72,
        "categories": {
            "On-Chain Health": {"score": 75, "weight": "20%"},
            "Tokenomics Quality": {"score": 82, "weight": "20%"},
            "Sentiment & Momentum": {"score": 68, "weight": "20%"},
            "Technical Setup": {"score": 70, "weight": "20%"},
            "Fundamental Strength": {"score": 65, "weight": "20%"},
        },
        "onchain": {
            "metrics": [
                {"metric": "Active Addresses (24h)", "value": "1.02M", "trend": "Up 8% (7d)", "assessment": "Growing network usage"},
                {"metric": "Whale Txns (>$100K)", "value": "4,218", "trend": "Up 15% (7d)", "assessment": "Accumulation signal"},
                {"metric": "Exchange Net Flow", "value": "-12,450 BTC", "trend": "Outflows 5 days", "assessment": "Supply leaving exchanges"},
                {"metric": "NVT Ratio", "value": "42.3", "trend": "Below 90d avg", "assessment": "Not overvalued by activity"},
                {"metric": "Hash Rate", "value": "612 EH/s", "trend": "All-time high", "assessment": "Strong network security"},
            ],
        },
        "tokenomics": {
            "metrics": [
                {"metric": "Circulating Supply", "value": "19.6M BTC", "notes": "93.3% of max supply mined"},
                {"metric": "Max Supply", "value": "21M BTC", "notes": "Hard-capped, deflationary by design"},
                {"metric": "Fully Diluted Valuation", "value": "$1.42T", "notes": "FDV / Market Cap ratio = 1.07x"},
                {"metric": "Inflation Rate", "value": "1.7% annual", "notes": "Post-halving (April 2024)"},
                {"metric": "Staking / Yield", "value": "N/A (PoW)", "notes": "No native staking for BTC"},
                {"metric": "Next Major Event", "value": "Halving 2028", "notes": "Block reward drops to 1.5625 BTC"},
            ],
        },
        "sentiment": {
            "fear_greed": "72 — Greed",
            "social_buzz": "High — trending on Crypto Twitter, Reddit, mainstream media",
            "news_tone": "Bullish — ETF inflows narrative, institutional adoption stories",
            "community_health": "Strong — active development, growing Lightning Network adoption",
        },
        "technical": {
            "key_levels": [
                {"level": "Resistance 2", "price": "$72,500", "notes": "All-time high zone"},
                {"level": "Resistance 1", "price": "$69,800", "notes": "Recent local high / rejection"},
                {"level": "Current Price", "price": "$67,240", "notes": "As of report generation date"},
                {"level": "Support 1", "price": "$63,500", "notes": "50-day MA convergence zone"},
                {"level": "Support 2", "price": "$58,200", "notes": "200-day MA / major support level"},
            ],
            "trend": "Uptrend — higher highs and higher lows on the daily timeframe",
            "pattern": "Bull flag consolidation above prior breakout level, targeting $72K+",
        },
        "thesis": {
            "bull_case": [
                "Spot ETF inflows accelerating — institutional demand creating sustained buying pressure",
                "Halving supply shock reduces new issuance by 50%, historically precedes 300%+ rallies",
                "Macro tailwinds: expected rate cuts in H2, weakening DXY, inflation hedge narrative"
            ],
            "bear_case": [
                "Regulatory crackdowns could restrict access (SEC enforcement, exchange delistings)",
                "Mt. Gox and government BTC distributions add ~140K BTC sell-side overhang",
                "Macro risk: persistent inflation delays rate cuts, strengthening USD hurts risk assets"
            ],
            "catalysts": [
                {"event": "Halving Impact Window", "date": "Q3-Q4 2025", "impact": "High — supply shock peaks 6-12 months post-halving"},
                {"event": "Fed Rate Decision", "date": "Next FOMC", "impact": "High — rate cuts are bullish for BTC and risk assets"},
                {"event": "ETF Quarterly Reports", "date": "Quarterly", "impact": "Medium — reveals pace of institutional adoption"},
            ],
            "entry_exit": {
                "entry_price": "$62,000 - $65,000",
                "target_price": "$85,000 - $100,000",
                "stop_loss": "$55,000",
                "timeframe": "6-12 months"
            },
        },
        "risk": {
            "risk_factors": [
                {"factor": "Regulatory / Legal", "probability": "Medium", "impact": "High", "notes": "SEC, global crypto regulation uncertainty"},
                {"factor": "Smart Contract Risk", "probability": "Very Low", "impact": "Critical", "notes": "BTC is PoW, minimal smart contract exposure"},
                {"factor": "Market / Volatility", "probability": "High", "impact": "High", "notes": "30-50% drawdowns are historically normal"},
                {"factor": "Liquidity Risk", "probability": "Low", "impact": "Low", "notes": "BTC has deepest crypto liquidity"},
                {"factor": "Macro / Correlation", "probability": "Medium", "impact": "Medium", "notes": "Increasingly correlated with NASDAQ/risk-on assets"},
            ],
            "position_recommendation": (
                "Bitcoin is the highest-conviction crypto asset but still highly volatile. "
                "Allocate no more than 5-10% of total portfolio to crypto, with BTC as the core position. "
                "Use dollar-cost averaging (DCA) over 4-8 weeks rather than lump-sum entry. "
                "Set a hard stop-loss at -15% to -20% from entry. Keep 20% of crypto allocation in stablecoins "
                "for rebalancing on dips. Use cold storage (hardware wallet) for long-term holdings."
            ),
            "scenarios": [
                {"scenario": "Bull Case", "probability": "30%", "return": "+50% to +100%",
                 "trigger": "ETF super-cycle + halving supply shock + global rate cuts"},
                {"scenario": "Base Case", "probability": "45%", "return": "+15% to +40%",
                 "trigger": "Steady institutional adoption, gradual appreciation"},
                {"scenario": "Bear Case", "probability": "25%", "return": "-25% to -45%",
                 "trigger": "Regulatory crackdown + macro recession + exchange failure"},
            ],
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--demo":
        # Demo mode
        data = get_demo_data()
        output = "CRYPTO-REPORT-sample.pdf"
        generate_report(data, output)
        print(f"Sample report generated: {output}")
        return

    # JSON input mode
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "CRYPTO-REPORT.pdf"

    with open(input_file, "r") as f:
        data = json.load(f)

    generate_report(data, output_file)
    print(f"Report generated: {output_file}")


if __name__ == "__main__":
    main()
