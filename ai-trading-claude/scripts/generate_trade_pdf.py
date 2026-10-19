#!/usr/bin/env python3
"""
AI Trading Analysis PDF Report Generator — AI Trading Claude Code Skills
Generates professional 6-page PDF investment reports with score gauges,
bar charts, technical/fundamental tables, investment thesis, and risk analysis.

Requires: reportlab (pip install reportlab)

Usage:
  python3 generate_trade_pdf.py                        # Demo mode
  python3 generate_trade_pdf.py --demo                 # Demo mode (explicit)
  python3 generate_trade_pdf.py data.json               # From JSON
  python3 generate_trade_pdf.py data.json output.pdf    # From JSON with custom output
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
# Color palette — Financial / Trading theme
# ---------------------------------------------------------------------------
COLORS = {
    "navy": HexColor("#0a0e27"),           # Deep navy background
    "green": HexColor("#00c853"),          # Trading green (buy)
    "red": HexColor("#ff1744"),            # Trading red (sell)
    "gold": HexColor("#ffd700"),           # Gold accent
    "blue": HexColor("#2196f3"),           # Neutral blue
    "gray": HexColor("#78909c"),           # Muted gray
    "light_bg": HexColor("#f0f4f8"),       # Light background
    "dark_bg": HexColor("#0d1117"),        # Dark card bg
    "text": HexColor("#1e293b"),           # Dark text
    "text_light": HexColor("#64748b"),     # Light text
    "border": HexColor("#cbd5e1"),         # Border
    "amber": HexColor("#ff9800"),          # Amber/warning
    "white": white,
    "black": black,
}


def score_color(score):
    """Return color based on score value (trading context)."""
    if score >= 70:
        return COLORS["green"]
    elif score >= 40:
        return COLORS["amber"]
    else:
        return COLORS["red"]


def score_grade(score):
    """Return trade grade from score."""
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


def trade_signal(score):
    """Return trade signal from score."""
    if score >= 85:
        return "STRONG BUY"
    elif score >= 70:
        return "BUY"
    elif score >= 55:
        return "HOLD"
    elif score >= 40:
        return "CAUTION"
    else:
        return "AVOID"


def signal_color(score):
    """Return color for the trade signal."""
    if score >= 70:
        return COLORS["green"]
    elif score >= 55:
        return COLORS["blue"]
    elif score >= 40:
        return COLORS["amber"]
    else:
        return COLORS["red"]


def draw_score_gauge(score, size=140):
    """Create a circular score gauge with trade-themed styling."""
    d = Drawing(size + 20, size + 20)

    cx = size / 2 + 10
    cy = size / 2 + 10

    # Outer ring background
    d.add(Circle(cx, cy, size / 2,
                 fillColor=COLORS["light_bg"], strokeColor=COLORS["border"], strokeWidth=2))

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
                 fontSize=36, fillColor=COLORS["navy"],
                 textAnchor="middle", fontName="Helvetica-Bold"))

    # "/ 100" label
    d.add(String(cx, cy - 18, "/ 100",
                 fontSize=10, fillColor=COLORS["gray"],
                 textAnchor="middle", fontName="Helvetica"))

    return d


def create_bar_chart(categories, scores, width=470, height=180):
    """Create horizontal bar charts for category scores."""
    d = Drawing(width, height)

    bar_height = 20
    gap = 12
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
    """Create custom paragraph styles for trading reports."""
    styles = getSampleStyleSheet()

    custom = {
        "title": ParagraphStyle(
            "TradeTitle", parent=styles["Title"],
            fontSize=30, textColor=COLORS["navy"],
            spaceAfter=4, fontName="Helvetica-Bold",
            leading=36
        ),
        "ticker": ParagraphStyle(
            "TradeTicker", parent=styles["Title"],
            fontSize=48, textColor=COLORS["blue"],
            spaceAfter=4, fontName="Helvetica-Bold",
            leading=56
        ),
        "subtitle": ParagraphStyle(
            "TradeSubtitle", parent=styles["Normal"],
            fontSize=14, textColor=COLORS["gray"],
            spaceAfter=6, fontName="Helvetica"
        ),
        "heading": ParagraphStyle(
            "TradeHeading", parent=styles["Heading1"],
            fontSize=20, textColor=COLORS["navy"],
            spaceBefore=16, spaceAfter=10,
            fontName="Helvetica-Bold"
        ),
        "subheading": ParagraphStyle(
            "TradeSubheading", parent=styles["Heading2"],
            fontSize=14, textColor=COLORS["blue"],
            spaceBefore=12, spaceAfter=6,
            fontName="Helvetica-Bold"
        ),
        "body": ParagraphStyle(
            "TradeBody", parent=styles["Normal"],
            fontSize=10, textColor=COLORS["text"],
            spaceAfter=6, fontName="Helvetica", leading=14
        ),
        "body_small": ParagraphStyle(
            "TradeBodySmall", parent=styles["Normal"],
            fontSize=8, textColor=COLORS["text"],
            spaceAfter=4, fontName="Helvetica", leading=11
        ),
        "signal": ParagraphStyle(
            "TradeSignal", parent=styles["Title"],
            fontSize=22, textColor=COLORS["green"],
            spaceAfter=4, fontName="Helvetica-Bold",
            alignment=1
        ),
        "footer": ParagraphStyle(
            "TradeFooter", parent=styles["Normal"],
            fontSize=7, textColor=COLORS["gray"],
            fontName="Helvetica", leading=10
        ),
        "disclaimer": ParagraphStyle(
            "TradeDisclaimer", parent=styles["Normal"],
            fontSize=6.5, textColor=COLORS["gray"],
            fontName="Helvetica", leading=9,
            spaceBefore=8
        ),
        "grade_large": ParagraphStyle(
            "TradeGrade", parent=styles["Title"],
            fontSize=18, textColor=COLORS["navy"],
            spaceAfter=6, fontName="Helvetica-Bold",
            alignment=1
        ),
        "bullet": ParagraphStyle(
            "TradeBullet", parent=styles["Normal"],
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
    """Return a standard table style with optional extras."""
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), COLORS["navy"]),
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
    "It is NOT financial advice. It does NOT constitute a recommendation to buy, sell, or hold "
    "any security. Past performance does not guarantee future results. Always do your own due "
    "diligence and consult a licensed financial advisor before making investment decisions. "
    "The authors and creators of this tool accept no liability for any losses incurred."
)


# ---------------------------------------------------------------------------
# Report generator
# ---------------------------------------------------------------------------
def generate_report(data, output_path):
    """Generate a professional 6-page trading analysis PDF report."""
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

    ticker = data.get("ticker", "AAPL")
    company_name = data.get("company_name", ticker)
    date_str = data.get("date", datetime.now().strftime("%B %d, %Y"))
    overall_score = data.get("overall_score", 0)
    grade = score_grade(overall_score)
    signal = trade_signal(overall_score)
    sig_color = signal_color(overall_score)

    # =====================================================================
    # PAGE 1 — COVER
    # =====================================================================
    elements.append(Spacer(1, 0.8 * inch))
    elements.append(Paragraph("AI Trading Analysis Report", S["title"]))
    elements.append(Spacer(1, 35))
    elements.append(Paragraph(ticker.upper(), S["ticker"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(company_name, ParagraphStyle(
        "CompanyName", parent=S["subtitle"], fontSize=16,
        textColor=COLORS["blue"], spaceAfter=4
    )))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"Generated: {date_str}", S["subtitle"]))
    elements.append(Spacer(1, 40))

    # Score gauge
    gauge = draw_score_gauge(overall_score, size=140)
    elements.append(gauge)
    elements.append(Spacer(1, 35))

    # Grade + signal
    color = score_color(overall_score)
    elements.append(Paragraph(
        f'Trade Score: <font color="{color.hexval()}">{int(overall_score)}/100</font> '
        f'(Grade: <font color="{color.hexval()}">{grade}</font>)',
        S["grade_large"]
    ))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        f'Signal: <font color="{sig_color.hexval()}">{signal}</font>',
        ParagraphStyle("SignalLine", parent=S["signal"],
                       textColor=sig_color, fontSize=24)
    ))

    elements.append(Spacer(1, 40))

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
        "Technical Strength": {"score": 72, "weight": "25%"},
        "Fundamental Quality": {"score": 68, "weight": "25%"},
        "Sentiment & Momentum": {"score": 61, "weight": "20%"},
        "Risk Profile": {"score": 55, "weight": "15%"},
        "Thesis Conviction": {"score": 65, "weight": "15%"},
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
        f'Composite Trade Score: <font color="{color.hexval()}">'
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
    # PAGE 3 — TECHNICAL OVERVIEW
    # =====================================================================
    elements.append(Paragraph("Technical Overview", S["heading"]))
    elements.append(Spacer(1, 6))

    # Key levels table
    elements.append(Paragraph("Key Levels", S["subheading"]))
    technical = data.get("technical", {})

    levels_data = [["Level", "Price", "Notes"]]
    key_levels = technical.get("key_levels", [
        {"level": "Resistance 2", "price": "$198.50", "notes": "52-week high zone"},
        {"level": "Resistance 1", "price": "$192.30", "notes": "Recent rejection point"},
        {"level": "Current Price", "price": "$185.40", "notes": "As of report date"},
        {"level": "Support 1", "price": "$178.60", "notes": "50-day MA convergence"},
        {"level": "Support 2", "price": "$171.20", "notes": "200-day MA / major support"},
    ])
    for kl in key_levels:
        levels_data.append([kl.get("level", ""), kl.get("price", ""), kl.get("notes", "")])

    levels_table = Table(levels_data, colWidths=[120, 100, 250])
    levels_table.setStyle(standard_table_style([
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
    ]))
    elements.append(levels_table)
    elements.append(Spacer(1, 14))

    # Indicator readings
    elements.append(Paragraph("Indicator Readings", S["subheading"]))

    indicators = technical.get("indicators", [
        {"indicator": "Trend Direction", "value": "Uptrend", "interpretation": "Higher highs, higher lows on daily"},
        {"indicator": "RSI (14)", "value": "62.3", "interpretation": "Bullish, approaching overbought"},
        {"indicator": "MACD", "value": "Bullish crossover", "interpretation": "Signal line cross 3 days ago"},
        {"indicator": "Volume", "value": "Above average", "interpretation": "1.3x 20-day avg volume"},
        {"indicator": "Pattern", "value": "Bull flag", "interpretation": "Consolidation after breakout"},
        {"indicator": "50/200 MA", "value": "Golden cross", "interpretation": "50 MA above 200 MA"},
    ])

    ind_data = [["Indicator", "Value", "Interpretation"]]
    for ind in indicators:
        ind_data.append([ind.get("indicator", ""), ind.get("value", ""),
                         Paragraph(ind.get("interpretation", ""), S["body_small"])])

    ind_table = Table(ind_data, colWidths=[120, 120, 230])
    ind_table.setStyle(standard_table_style([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(ind_table)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 4 — FUNDAMENTAL OVERVIEW
    # =====================================================================
    elements.append(Paragraph("Fundamental Overview", S["heading"]))
    elements.append(Spacer(1, 6))

    fundamental = data.get("fundamental", {})

    # Key metrics table
    elements.append(Paragraph("Key Metrics", S["subheading"]))

    metrics = fundamental.get("metrics", [
        {"metric": "P/E Ratio", "value": "28.5x", "sector_avg": "25.2x", "assessment": "Slightly elevated"},
        {"metric": "P/S Ratio", "value": "7.2x", "sector_avg": "5.8x", "assessment": "Premium valuation"},
        {"metric": "Revenue Growth (YoY)", "value": "+12.4%", "sector_avg": "+8.1%", "assessment": "Above sector"},
        {"metric": "EPS Growth (YoY)", "value": "+18.7%", "sector_avg": "+11.3%", "assessment": "Strong"},
        {"metric": "Gross Margin", "value": "45.2%", "sector_avg": "38.6%", "assessment": "Competitive advantage"},
        {"metric": "Debt/Equity", "value": "0.42", "sector_avg": "0.68", "assessment": "Conservative"},
    ])

    met_data = [["Metric", "Value", "Sector Avg", "Assessment"]]
    for m in metrics:
        met_data.append([m.get("metric", ""), m.get("value", ""),
                         m.get("sector_avg", ""), m.get("assessment", "")])

    met_table = Table(met_data, colWidths=[130, 90, 90, 160])
    met_table.setStyle(standard_table_style([
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
    ]))
    elements.append(met_table)
    elements.append(Spacer(1, 14))

    # Valuation assessment
    elements.append(Paragraph("Valuation Assessment", S["subheading"]))
    val_text = fundamental.get("valuation_assessment",
        "The stock trades at a moderate premium to sector averages across most metrics. "
        "The elevated P/E and P/S ratios are partially justified by above-average revenue and "
        "EPS growth. Gross margins suggest a durable competitive advantage. The conservative "
        "balance sheet with low debt/equity provides downside cushion and financial flexibility."
    )
    elements.append(Paragraph(val_text, S["body"]))
    elements.append(Spacer(1, 10))

    # Moat rating
    elements.append(Paragraph("Competitive Moat", S["subheading"]))
    moat = fundamental.get("moat", {})
    moat_rating = moat.get("rating", "Moderate")
    moat_sources = moat.get("sources", [
        "Brand recognition and customer loyalty",
        "Switching costs in enterprise segment",
        "Network effects in platform ecosystem"
    ])
    elements.append(Paragraph(f"<b>Moat Rating:</b> {moat_rating}", S["body"]))
    for src in moat_sources:
        elements.append(Paragraph(f"&bull; {src}", S["bullet"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 5 — INVESTMENT THESIS
    # =====================================================================
    elements.append(Paragraph("Investment Thesis", S["heading"]))
    elements.append(Spacer(1, 6))

    thesis = data.get("thesis", {})

    # Bull case
    elements.append(Paragraph("Bull Case", ParagraphStyle(
        "BullCase", parent=S["subheading"], textColor=COLORS["green"])))
    bull_points = thesis.get("bull_case", [
        "Revenue acceleration from new product launches expected in Q3/Q4",
        "Market share gains in enterprise segment with 15% YoY growth",
        "Margin expansion from operational efficiencies and scale benefits"
    ])
    for i, pt in enumerate(bull_points, 1):
        elements.append(Paragraph(f"{i}. {pt}", S["body"]))
    elements.append(Spacer(1, 10))

    # Bear case
    elements.append(Paragraph("Bear Case", ParagraphStyle(
        "BearCase", parent=S["subheading"], textColor=COLORS["red"])))
    bear_points = thesis.get("bear_case", [
        "Valuation premium leaves little room for execution missteps",
        "Competitive pressure from well-funded new entrants in core market",
        "Macro headwinds could slow enterprise IT spending in H2"
    ])
    for i, pt in enumerate(bear_points, 1):
        elements.append(Paragraph(f"{i}. {pt}", S["body"]))
    elements.append(Spacer(1, 10))

    # Catalyst timeline
    elements.append(Paragraph("Catalyst Timeline", S["subheading"]))
    catalysts = thesis.get("catalysts", [
        {"event": "Q2 Earnings Report", "date": "Jul 25", "impact": "High — revenue guidance update"},
        {"event": "Product Launch Event", "date": "Sep 10", "impact": "Medium — new revenue stream"},
        {"event": "Analyst Day", "date": "Nov 15", "impact": "Medium — long-term guidance"},
    ])
    cat_data = [["Event", "Expected Date", "Potential Impact"]]
    for cat in catalysts:
        cat_data.append([cat.get("event", ""), cat.get("date", ""),
                         Paragraph(cat.get("impact", ""), S["body_small"])])
    cat_table = Table(cat_data, colWidths=[160, 100, 210])
    cat_table.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(cat_table)
    elements.append(Spacer(1, 14))

    # Entry/exit strategy
    elements.append(Paragraph("Entry / Exit Strategy", S["subheading"]))
    entry_exit = thesis.get("entry_exit", {})
    entry = entry_exit.get("entry_price", "$178 - $182")
    target = entry_exit.get("target_price", "$198 - $205")
    stop = entry_exit.get("stop_loss", "$168")
    timeframe = entry_exit.get("timeframe", "3-6 months")

    ee_data = [
        ["Parameter", "Level"],
        ["Entry Zone", entry],
        ["Price Target", target],
        ["Stop Loss", stop],
        ["Timeframe", timeframe],
    ]
    ee_table = Table(ee_data, colWidths=[160, 200])
    ee_style = [
        ("TEXTCOLOR", (1, 1), (1, 1), COLORS["blue"]),
        ("TEXTCOLOR", (1, 2), (1, 2), COLORS["green"]),
        ("TEXTCOLOR", (1, 3), (1, 3), COLORS["red"]),
        ("FONTNAME", (1, 1), (1, 4), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
    ]
    ee_table.setStyle(standard_table_style(ee_style))
    elements.append(ee_table)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 6 — RISK & POSITION SIZING
    # =====================================================================
    elements.append(Paragraph("Risk & Position Sizing", S["heading"]))
    elements.append(Spacer(1, 6))

    risk = data.get("risk", {})

    # Risk/reward table
    elements.append(Paragraph("Risk / Reward Analysis", S["subheading"]))

    rr_ratio = risk.get("risk_reward_ratio", "2.8:1")
    position_size = risk.get("recommended_position_size", "3-5% of portfolio")
    max_drawdown = risk.get("max_drawdown_scenario", "-18% in severe market selloff")
    volatility = risk.get("volatility", "Medium (Beta 1.12)")
    correlation = risk.get("correlation", "0.78 to S&P 500, 0.85 to sector ETF")

    risk_data = [
        ["Risk Metric", "Value"],
        ["Risk/Reward Ratio", rr_ratio],
        ["Recommended Position Size", position_size],
        ["Max Drawdown Scenario", max_drawdown],
        ["Volatility Profile", volatility],
        ["Market Correlation", correlation],
    ]
    risk_table = Table(risk_data, colWidths=[200, 270])
    risk_style = [
        ("ALIGN", (1, 0), (1, -1), "LEFT"),
        ("TEXTCOLOR", (1, 1), (1, 1), COLORS["green"]),
        ("FONTNAME", (1, 1), (1, 1), "Helvetica-Bold"),
        ("TEXTCOLOR", (1, 3), (1, 3), COLORS["red"]),
    ]
    risk_table.setStyle(standard_table_style(risk_style))
    elements.append(risk_table)
    elements.append(Spacer(1, 16))

    # Position sizing methodology
    elements.append(Paragraph("Position Sizing Methodology", S["subheading"]))
    sizing_text = risk.get("sizing_methodology",
        "Position size is calculated using the fixed-percentage risk model. Risk per trade is "
        "limited to 1-2% of total portfolio value. The entry-to-stop distance determines the "
        "number of shares. For a $100,000 portfolio with 1.5% risk ($1,500) and a $14 stop distance, "
        "the recommended position is approximately 107 shares ($19,800 or ~20% of portfolio). "
        "Scale in with 50% at entry, 25% on first pullback, 25% on confirmation."
    )
    elements.append(Paragraph(sizing_text, S["body"]))
    elements.append(Spacer(1, 14))

    # Scenario analysis
    elements.append(Paragraph("Scenario Analysis", S["subheading"]))
    scenarios = risk.get("scenarios", [
        {"scenario": "Bull Case", "probability": "35%", "return": "+15% to +22%",
         "trigger": "Earnings beat + raised guidance"},
        {"scenario": "Base Case", "probability": "40%", "return": "+5% to +12%",
         "trigger": "In-line results, gradual appreciation"},
        {"scenario": "Bear Case", "probability": "25%", "return": "-8% to -18%",
         "trigger": "Miss on revenue + macro deterioration"},
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
    # Color code scenario returns
    if len(scenarios) >= 3:
        sc_style.append(("TEXTCOLOR", (2, 1), (2, 1), COLORS["green"]))
        sc_style.append(("TEXTCOLOR", (2, 2), (2, 2), COLORS["blue"]))
        sc_style.append(("TEXTCOLOR", (2, 3), (2, 3), COLORS["red"]))
        sc_style.append(("FONTNAME", (2, 1), (2, 3), "Helvetica-Bold"))
    sc_table.setStyle(standard_table_style(sc_style))
    elements.append(sc_table)

    elements.append(Spacer(1, 24))

    # Footer + disclaimer
    elements.append(Paragraph(
        "Generated by AI Trading Analyst for Claude Code", S["footer"]
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
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "date": datetime.now().strftime("%B %d, %Y"),
        "overall_score": 74,
        "categories": {
            "Technical Strength": {"score": 78, "weight": "25%"},
            "Fundamental Quality": {"score": 82, "weight": "25%"},
            "Sentiment & Momentum": {"score": 68, "weight": "20%"},
            "Risk Profile": {"score": 62, "weight": "15%"},
            "Thesis Conviction": {"score": 71, "weight": "15%"},
        },
        "technical": {
            "key_levels": [
                {"level": "Resistance 2", "price": "$198.50", "notes": "52-week high zone"},
                {"level": "Resistance 1", "price": "$192.30", "notes": "Recent rejection point"},
                {"level": "Current Price", "price": "$185.40", "notes": "As of report date"},
                {"level": "Support 1", "price": "$178.60", "notes": "50-day MA convergence"},
                {"level": "Support 2", "price": "$171.20", "notes": "200-day MA / major support"},
            ],
            "indicators": [
                {"indicator": "Trend Direction", "value": "Uptrend", "interpretation": "Higher highs and higher lows on the daily chart"},
                {"indicator": "RSI (14)", "value": "62.3", "interpretation": "Bullish momentum, room before overbought (70)"},
                {"indicator": "MACD", "value": "Bullish crossover", "interpretation": "Signal line cross confirmed 3 sessions ago"},
                {"indicator": "Volume", "value": "Above average", "interpretation": "1.3x the 20-day average volume on recent up days"},
                {"indicator": "Pattern", "value": "Bull flag", "interpretation": "Tight consolidation after +8% breakout move"},
                {"indicator": "50/200 MA", "value": "Golden cross", "interpretation": "50 MA crossed above 200 MA two weeks ago"},
            ],
        },
        "fundamental": {
            "metrics": [
                {"metric": "P/E Ratio", "value": "28.5x", "sector_avg": "25.2x", "assessment": "Slightly elevated"},
                {"metric": "P/S Ratio", "value": "7.2x", "sector_avg": "5.8x", "assessment": "Premium valuation"},
                {"metric": "Revenue Growth (YoY)", "value": "+12.4%", "sector_avg": "+8.1%", "assessment": "Above sector average"},
                {"metric": "EPS Growth (YoY)", "value": "+18.7%", "sector_avg": "+11.3%", "assessment": "Strong earnings momentum"},
                {"metric": "Gross Margin", "value": "45.2%", "sector_avg": "38.6%", "assessment": "Competitive advantage"},
                {"metric": "Debt/Equity", "value": "0.42", "sector_avg": "0.68", "assessment": "Conservative leverage"},
            ],
            "valuation_assessment": (
                "Apple trades at a moderate premium to sector averages. The elevated P/E and P/S "
                "ratios are justified by superior revenue growth, expanding margins, and a robust "
                "services segment. The conservative balance sheet with low debt/equity provides "
                "downside protection and flexibility for capital returns."
            ),
            "moat": {
                "rating": "Wide",
                "sources": [
                    "Ecosystem lock-in with 2B+ active devices worldwide",
                    "Brand loyalty and pricing power across hardware and services",
                    "Services revenue (App Store, iCloud, Apple Music) provides recurring income",
                    "Vertical integration in silicon design (M-series chips)"
                ]
            },
        },
        "thesis": {
            "bull_case": [
                "AI integration across product lineup drives hardware upgrade supercycle",
                "Services revenue growing at 15%+ with expanding margins (70%+)",
                "India and emerging markets provide next leg of hardware growth"
            ],
            "bear_case": [
                "Premium valuation leaves limited margin of safety on execution misses",
                "Regulatory risk: App Store antitrust actions in EU and US",
                "China revenue exposure (~18%) amid geopolitical tensions"
            ],
            "catalysts": [
                {"event": "Q3 Earnings Report", "date": "Jul 31", "impact": "High — services growth and AI roadmap update"},
                {"event": "iPhone 17 Launch", "date": "Sep 15", "impact": "High — AI features as upgrade driver"},
                {"event": "Developer Conference", "date": "Jun 10", "impact": "Medium — AI SDK announcements"},
            ],
            "entry_exit": {
                "entry_price": "$178 - $182",
                "target_price": "$198 - $205",
                "stop_loss": "$168",
                "timeframe": "3-6 months"
            },
        },
        "risk": {
            "risk_reward_ratio": "2.8:1",
            "recommended_position_size": "3-5% of portfolio",
            "max_drawdown_scenario": "-18% in severe market selloff (based on historical beta)",
            "volatility": "Medium (Beta 1.12, 30-day IV 24%)",
            "correlation": "0.78 to S&P 500, 0.85 to QQQ",
            "sizing_methodology": (
                "Position size is calculated using the fixed-percentage risk model. Risk per trade is "
                "limited to 1-2% of total portfolio value. With entry at $180 and stop at $168 "
                "($12 risk per share), a $100K portfolio risking 1.5% ($1,500) should buy ~125 shares "
                "($22,500 or 22.5% of portfolio). Scale in: 50% at entry, 25% on pullback to $178, "
                "25% on confirmed breakout above $192."
            ),
            "scenarios": [
                {"scenario": "Bull Case", "probability": "35%", "return": "+15% to +22%",
                 "trigger": "Earnings beat + AI product launch success + services acceleration"},
                {"scenario": "Base Case", "probability": "40%", "return": "+5% to +12%",
                 "trigger": "In-line results, steady buybacks, gradual appreciation"},
                {"scenario": "Bear Case", "probability": "25%", "return": "-8% to -18%",
                 "trigger": "Revenue miss + regulatory headwinds + China slowdown"},
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
        output = "TRADE-REPORT-sample.pdf"
        generate_report(data, output)
        print(f"Sample report generated: {output}")
        return

    # JSON input mode
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "TRADE-REPORT.pdf"

    with open(input_file, "r") as f:
        data = json.load(f)

    generate_report(data, output_file)
    print(f"Report generated: {output_file}")


if __name__ == "__main__":
    main()
