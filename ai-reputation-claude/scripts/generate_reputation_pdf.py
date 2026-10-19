#!/usr/bin/env python3
"""
AI Reputation Manager — PDF Report Generator

Generates a professional reputation analysis report PDF using ReportLab.
Reads structured data from a JSON file and produces a polished multi-page report.

Usage:
    python generate_reputation_pdf.py --input report_data.json --output report.pdf
    python generate_reputation_pdf.py --input report_data.json  # outputs to ./reputation_report_<business>.pdf
"""

import argparse
import json
import math
import os
import sys
from datetime import datetime

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch, mm
    from reportlab.pdfgen import canvas
    from reportlab.platypus import (
        BaseDocTemplate,
        Frame,
        Image,
        NextPageTemplate,
        PageBreak,
        PageTemplate,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
except ImportError:
    print("ERROR: ReportLab is required. Install it with:")
    print("  pip install reportlab")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Color Palette
# ---------------------------------------------------------------------------
NAVY = colors.HexColor("#1a1a2e")
DARK_NAVY = colors.HexColor("#0f0f1a")
ACCENT_BLUE = colors.HexColor("#4361ee")
ACCENT_LIGHT = colors.HexColor("#7b8cde")
LIGHT_BG = colors.HexColor("#f0f2f8")
WHITE = colors.white
BLACK = colors.black
GRAY = colors.HexColor("#6c757d")
LIGHT_GRAY = colors.HexColor("#e9ecef")
MEDIUM_GRAY = colors.HexColor("#adb5bd")

# Score colors
SCORE_RED = colors.HexColor("#dc3545")
SCORE_ORANGE = colors.HexColor("#fd7e14")
SCORE_YELLOW = colors.HexColor("#ffc107")
SCORE_GREEN = colors.HexColor("#28a745")
SCORE_DARK_GREEN = colors.HexColor("#1a7431")

# Priority colors
PRIORITY_HIGH = colors.HexColor("#dc3545")
PRIORITY_MEDIUM = colors.HexColor("#fd7e14")
PRIORITY_LOW = colors.HexColor("#28a745")

# Sentiment colors
SENTIMENT_POSITIVE = colors.HexColor("#28a745")
SENTIMENT_NEUTRAL = colors.HexColor("#ffc107")
SENTIMENT_NEGATIVE = colors.HexColor("#dc3545")

DISCLAIMER_TEXT = (
    "DISCLAIMER: This report is generated using AI-powered analysis of publicly available "
    "online reviews and information. Scores and recommendations are estimates based on "
    "available data and should not be considered definitive assessments. Review data may be "
    "incomplete. This report does not constitute legal, financial, or professional advice. "
    "The business should verify all findings independently before taking action."
)


# ---------------------------------------------------------------------------
# Helper: Score -> Color
# ---------------------------------------------------------------------------
def score_color(score):
    """Return color based on reputation score (0-100)."""
    if score >= 80:
        return SCORE_GREEN
    elif score >= 60:
        return SCORE_YELLOW
    elif score >= 40:
        return SCORE_ORANGE
    else:
        return SCORE_RED


def score_label(score):
    """Return label based on reputation score."""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Needs Improvement"
    else:
        return "Critical"


def priority_color(priority):
    """Return color for priority level."""
    p = str(priority).upper()
    if "1" in p or "HIGH" in p or "CRITICAL" in p:
        return PRIORITY_HIGH
    elif "2" in p or "MED" in p:
        return PRIORITY_MEDIUM
    else:
        return PRIORITY_LOW


# ---------------------------------------------------------------------------
# Default / Fallback Data
# ---------------------------------------------------------------------------
def get_default_data():
    """Return default structure when fields are missing from input."""
    return {
        "business_name": "Business Name",
        "report_date": datetime.now().strftime("%B %d, %Y"),
        "reputation_score": 0,
        "executive_summary": "No executive summary available.",
        "pillar_scores": {
            "reviews": 0,
            "sentiment": 0,
            "competitive": 0,
            "response": 0,
            "action_plan": 0,
        },
        "platform_ratings": {},
        "total_review_count": 0,
        "sentiment": {
            "positive_pct": 0,
            "neutral_pct": 0,
            "negative_pct": 0,
            "overall_polarity": 0,
            "emotional_arc": "Unknown",
            "dominant_positive_emotion": "N/A",
            "dominant_negative_emotion": "N/A",
        },
        "emotion_distribution": [],
        "theme_analysis": [],
        "competitors": [],
        "competitor_comparison": [],
        "competitive_gaps": [],
        "competitive_opportunities": [],
        "negative_reviews_with_responses": [],
        "response_templates": [],
        "immediate_actions": [],
        "short_term_improvements": [],
        "medium_term_strategies": [],
        "long_term_initiatives": [],
        "review_generation_plan": [],
        "projected_scores": {},
    }


def safe_get(data, key, default=None):
    """Safely get nested key with fallback."""
    if default is None:
        default = get_default_data().get(key, "")
    return data.get(key, default)


# ---------------------------------------------------------------------------
# Page Footer / Header Callbacks
# ---------------------------------------------------------------------------
def add_page_footer(canvas_obj, doc):
    """Draw footer on every page with disclaimer and page number."""
    canvas_obj.saveState()

    # Divider line
    canvas_obj.setStrokeColor(LIGHT_GRAY)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(50, 58, letter[0] - 50, 58)

    # Disclaimer
    canvas_obj.setFont("Helvetica", 5.5)
    canvas_obj.setFillColor(GRAY)

    # Word-wrap disclaimer to fit
    max_width = letter[0] - 100
    words = DISCLAIMER_TEXT.split()
    lines = []
    current_line = ""
    for word in words:
        test = current_line + " " + word if current_line else word
        if canvas_obj.stringWidth(test, "Helvetica", 5.5) < max_width:
            current_line = test
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    y = 52
    for line in lines:
        canvas_obj.drawString(50, y, line)
        y -= 8

    # Page number
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(MEDIUM_GRAY)
    canvas_obj.drawRightString(
        letter[0] - 50, 30, f"Page {doc.page}"
    )

    # Left footer branding
    canvas_obj.setFont("Helvetica-Bold", 7)
    canvas_obj.setFillColor(ACCENT_BLUE)
    canvas_obj.drawString(50, 30, "AI Reputation Manager Report")

    canvas_obj.restoreState()


def add_cover_footer(canvas_obj, doc):
    """Minimal footer for cover page."""
    canvas_obj.saveState()
    canvas_obj.setFont("Helvetica", 6)
    canvas_obj.setFillColor(MEDIUM_GRAY)
    canvas_obj.drawCentredString(
        letter[0] / 2, 30,
        "Generated by AI Reputation Manager | Confidential"
    )
    canvas_obj.restoreState()


# ---------------------------------------------------------------------------
# Gauge Drawing
# ---------------------------------------------------------------------------
def draw_score_gauge(canvas_obj, x, y, score, size=120):
    """Draw a semicircular gauge for the reputation score."""
    canvas_obj.saveState()

    center_x = x
    center_y = y
    radius = size / 2

    # Draw background arc segments
    segments = [
        (0, 39, SCORE_RED),
        (39, 59, SCORE_ORANGE),
        (59, 79, SCORE_YELLOW),
        (79, 100, SCORE_GREEN),
    ]

    for seg_start, seg_end, seg_color in segments:
        angle_start = 180 - (seg_start / 100 * 180)
        angle_end = 180 - (seg_end / 100 * 180)

        canvas_obj.setStrokeColor(seg_color)
        canvas_obj.setLineWidth(12)
        # Draw arc manually with line segments
        steps = max(int(abs(angle_start - angle_end)), 2)
        for i in range(steps):
            frac = i / steps
            angle = math.radians(angle_start + frac * (angle_end - angle_start))
            ax = center_x + radius * math.cos(angle)
            ay = center_y + radius * math.sin(angle)
            angle2 = math.radians(angle_start + (frac + 1 / steps) * (angle_end - angle_start))
            bx = center_x + radius * math.cos(angle2)
            by = center_y + radius * math.sin(angle2)
            canvas_obj.line(ax, ay, bx, by)

    # Draw needle
    score_clamped = max(0, min(100, score))
    needle_angle = math.radians(180 - (score_clamped / 100 * 180))
    needle_length = radius * 0.75
    nx = center_x + needle_length * math.cos(needle_angle)
    ny = center_y + needle_length * math.sin(needle_angle)

    canvas_obj.setStrokeColor(DARK_NAVY)
    canvas_obj.setLineWidth(2.5)
    canvas_obj.line(center_x, center_y, nx, ny)

    # Center dot
    canvas_obj.setFillColor(DARK_NAVY)
    canvas_obj.circle(center_x, center_y, 5, fill=1, stroke=0)

    # Score text
    canvas_obj.setFont("Helvetica-Bold", 28)
    canvas_obj.setFillColor(score_color(score))
    canvas_obj.drawCentredString(center_x, center_y - 30, str(int(score)))

    # Label
    canvas_obj.setFont("Helvetica", 10)
    canvas_obj.setFillColor(GRAY)
    canvas_obj.drawCentredString(center_x, center_y - 44, score_label(score))

    # Min/Max labels
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.setFillColor(MEDIUM_GRAY)
    canvas_obj.drawString(center_x - radius - 5, center_y - 8, "0")
    canvas_obj.drawRightString(center_x + radius + 5, center_y - 8, "100")

    canvas_obj.restoreState()


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def get_styles():
    """Build and return all paragraph styles used in the report."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=32,
        leading=38,
        textColor=WHITE,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        name="CoverSubtitle",
        fontName="Helvetica",
        fontSize=14,
        leading=20,
        textColor=ACCENT_LIGHT,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=24,
        textColor=NAVY,
        spaceBefore=20,
        spaceAfter=10,
        borderPadding=(0, 0, 4, 0),
    ))

    styles.add(ParagraphStyle(
        name="SubHeader",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=18,
        textColor=ACCENT_BLUE,
        spaceBefore=14,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="BodyText2",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=BLACK,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="SmallText",
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=GRAY,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="QuoteText",
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=13,
        textColor=GRAY,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=8,
        borderPadding=(4, 8, 4, 8),
    ))

    styles.add(ParagraphStyle(
        name="ScoreLabel",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=NAVY,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        name="TableHeader",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=WHITE,
        alignment=TA_CENTER,
    ))

    styles.add(ParagraphStyle(
        name="TableCell",
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=BLACK,
    ))

    styles.add(ParagraphStyle(
        name="TableCellCenter",
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=BLACK,
        alignment=TA_CENTER,
    ))

    return styles


# ---------------------------------------------------------------------------
# Table Helpers
# ---------------------------------------------------------------------------
def styled_table(data, col_widths=None, header_color=NAVY):
    """Create a consistently styled table."""
    if not data:
        return Spacer(1, 0)

    style_commands = [
        # Header row
        ("BACKGROUND", (0, 0), (-1, 0), header_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        # Body rows
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
        ("TOPPADDING", (0, 1), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        # Grid
        ("GRID", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, header_color),
    ]

    # Alternating row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_commands.append(("BACKGROUND", (0, i), (-1, i), LIGHT_BG))

    kwargs = {}
    if col_widths:
        kwargs["colWidths"] = col_widths

    table = Table(data, repeatRows=1, **kwargs)
    table.setStyle(TableStyle(style_commands))
    return table


def draw_horizontal_bar(canvas_obj, x, y, width, height, value, max_value=100, bar_color=ACCENT_BLUE):
    """Draw a horizontal progress bar."""
    canvas_obj.saveState()

    # Background
    canvas_obj.setFillColor(LIGHT_GRAY)
    canvas_obj.roundRect(x, y, width, height, 3, fill=1, stroke=0)

    # Fill
    fill_width = max(0, min(width, (value / max_value) * width))
    if fill_width > 0:
        canvas_obj.setFillColor(bar_color)
        canvas_obj.roundRect(x, y, fill_width, height, 3, fill=1, stroke=0)

    canvas_obj.restoreState()


# ---------------------------------------------------------------------------
# Section Builders
# ---------------------------------------------------------------------------
def build_cover_page(data, styles):
    """Build the cover page elements. Returns list of flowables."""
    elements = []

    # We'll use a custom canvas drawing for the cover, but add spacers
    # to position content since we can't draw directly from flowables.
    # The actual cover drawing is done in the page template callback.
    elements.append(Spacer(1, 1.8 * inch))

    elements.append(Paragraph("REPUTATION ANALYSIS REPORT", styles["CoverTitle"]))
    elements.append(Spacer(1, 40))

    business = safe_get(data, "business_name", "Business")
    elements.append(Paragraph(business, styles["CoverSubtitle"]))
    elements.append(Spacer(1, 30))

    report_date = safe_get(data, "report_date", datetime.now().strftime("%B %d, %Y"))
    elements.append(Paragraph(report_date, styles["CoverSubtitle"]))
    elements.append(Spacer(1, 80))

    # Score display placeholder text — the gauge is drawn via canvas
    score = safe_get(data, "reputation_score", 0)
    elements.append(Paragraph("OVERALL REPUTATION SCORE", ParagraphStyle(
        name="CoverScoreLabel",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=ACCENT_LIGHT,
        alignment=TA_CENTER,
    )))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        f'<font size="48" color="{score_color(score).hexval()}">{int(score)}</font>'
        f'<font size="18" color="#7b8cde"> / 100</font>',
        ParagraphStyle(name="CoverScoreNum", alignment=TA_CENTER, fontSize=48),
    ))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        score_label(score),
        ParagraphStyle(
            name="CoverScoreGrade",
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=score_color(score),
            alignment=TA_CENTER,
        ),
    ))

    elements.append(PageBreak())
    return elements


def build_executive_summary(data, styles):
    """Build the executive summary section."""
    elements = []

    elements.append(Paragraph("1. Executive Summary", styles["SectionHeader"]))

    # Divider line via a small table
    elements.append(Table(
        [[""]], colWidths=[5 * inch],
        style=TableStyle([("LINEBELOW", (0, 0), (-1, 0), 2, ACCENT_BLUE)])
    ))
    elements.append(Spacer(1, 10))

    summary = safe_get(data, "executive_summary", "No executive summary available.")
    elements.append(Paragraph(summary, styles["BodyText2"]))
    elements.append(Spacer(1, 16))

    # Pillar scores summary table
    pillars = safe_get(data, "pillar_scores", {})
    pillar_data = [
        ["Pillar", "Score", "Weight", "Weighted"],
        ["Review Collection & Analysis", str(pillars.get("reviews", 0)), "20%",
         f"{pillars.get('reviews', 0) * 0.2:.1f}"],
        ["Sentiment & Emotion", str(pillars.get("sentiment", 0)), "20%",
         f"{pillars.get('sentiment', 0) * 0.2:.1f}"],
        ["Competitive Reputation", str(pillars.get("competitive", 0)), "20%",
         f"{pillars.get('competitive', 0) * 0.2:.1f}"],
        ["Response Strategy", str(pillars.get("response", 0)), "20%",
         f"{pillars.get('response', 0) * 0.2:.1f}"],
        ["Action Plan Readiness", str(pillars.get("action_plan", 0)), "20%",
         f"{pillars.get('action_plan', 0) * 0.2:.1f}"],
    ]

    # Totals row
    total = sum(pillars.get(k, 0) * 0.2 for k in
                ["reviews", "sentiment", "competitive", "response", "action_plan"])
    pillar_data.append(["OVERALL REPUTATION SCORE", "", "100%", f"{total:.1f}"])

    table = styled_table(pillar_data, col_widths=[2.6 * inch, 0.8 * inch, 0.8 * inch, 1.0 * inch])

    # Bold the last row
    table_style = table.style
    table.setStyle(TableStyle([
        *table_style.getCommands(),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), NAVY),
        ("TEXTCOLOR", (0, -1), (-1, -1), WHITE),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 10))

    return elements


def build_sentiment_section(data, styles):
    """Build the sentiment breakdown section."""
    elements = []

    elements.append(Paragraph("2. Sentiment Analysis", styles["SectionHeader"]))
    elements.append(Table(
        [[""]], colWidths=[5 * inch],
        style=TableStyle([("LINEBELOW", (0, 0), (-1, 0), 2, ACCENT_BLUE)])
    ))
    elements.append(Spacer(1, 10))

    sentiment = safe_get(data, "sentiment", {})

    # Summary metrics
    summary_data = [
        ["Metric", "Value"],
        ["Overall Polarity", str(sentiment.get("overall_polarity", "N/A"))],
        ["Positive Reviews", f"{sentiment.get('positive_pct', 0)}%"],
        ["Neutral Reviews", f"{sentiment.get('neutral_pct', 0)}%"],
        ["Negative Reviews", f"{sentiment.get('negative_pct', 0)}%"],
        ["Emotional Arc", str(sentiment.get("emotional_arc", "Unknown"))],
        ["Dominant Positive Emotion", str(sentiment.get("dominant_positive_emotion", "N/A"))],
        ["Dominant Negative Emotion", str(sentiment.get("dominant_negative_emotion", "N/A"))],
    ]
    elements.append(styled_table(summary_data, col_widths=[2.5 * inch, 2.5 * inch]))
    elements.append(Spacer(1, 16))

    # Emotion distribution
    emotion_data = safe_get(data, "emotion_distribution", [])
    if emotion_data:
        elements.append(Paragraph("Emotion Distribution", styles["SubHeader"]))
        table_data = [["Emotion", "Count", "% of Reviews", "Avg Intensity"]]
        for e in emotion_data:
            table_data.append([
                str(e.get("emotion", "")),
                str(e.get("count", 0)),
                f"{e.get('pct', 0)}%",
                f"{e.get('intensity', 0):.1f}/5",
            ])
        elements.append(styled_table(table_data, col_widths=[1.6 * inch, 0.9 * inch, 1.2 * inch, 1.2 * inch]))
        elements.append(Spacer(1, 10))

    return elements


def build_theme_section(data, styles):
    """Build the review theme analysis section."""
    elements = []

    elements.append(Paragraph("3. Review Theme Analysis", styles["SectionHeader"]))
    elements.append(Table(
        [[""]], colWidths=[5 * inch],
        style=TableStyle([("LINEBELOW", (0, 0), (-1, 0), 2, ACCENT_BLUE)])
    ))
    elements.append(Spacer(1, 10))

    themes = safe_get(data, "theme_analysis", [])
    if themes:
        table_data = [["Theme", "Frequency", "Avg Sentiment", "Top Positive", "Top Negative"]]
        for t in themes:
            table_data.append([
                str(t.get("theme", "")),
                f"{t.get('frequency', 0)}%",
                f"{t.get('sentiment', 0)}/100",
                str(t.get("top_positive", "")),
                str(t.get("top_negative", "")),
            ])
        elements.append(styled_table(
            table_data,
            col_widths=[1.2 * inch, 0.8 * inch, 0.9 * inch, 1.2 * inch, 1.2 * inch]
        ))
    else:
        elements.append(Paragraph(
            "Theme analysis data not available. Run the full analysis to populate this section.",
            styles["BodyText2"]
        ))

    elements.append(Spacer(1, 10))

    # Platform ratings if available
    platform_data = safe_get(data, "platform_ratings", {})
    if platform_data:
        elements.append(Paragraph("Platform Ratings Summary", styles["SubHeader"]))
        table_data = [["Platform", "Rating", "Review Count"]]
        for platform, info in platform_data.items():
            if isinstance(info, dict):
                table_data.append([
                    platform.capitalize(),
                    f"{info.get('rating', 'N/A')}/5",
                    str(info.get("count", "N/A")),
                ])
            else:
                table_data.append([platform.capitalize(), str(info), "N/A"])
        elements.append(styled_table(table_data, col_widths=[2.0 * inch, 1.5 * inch, 1.5 * inch]))
        elements.append(Spacer(1, 10))

    return elements


def build_competitor_section(data, styles):
    """Build the competitor benchmarking section."""
    elements = []

    elements.append(Paragraph("4. Competitor Benchmarking", styles["SectionHeader"]))
    elements.append(Table(
        [[""]], colWidths=[5 * inch],
        style=TableStyle([("LINEBELOW", (0, 0), (-1, 0), 2, ACCENT_BLUE)])
    ))
    elements.append(Spacer(1, 10))

    comparison = safe_get(data, "competitor_comparison", [])
    if comparison:
        table_data = [["Business", "Avg Rating", "Total Reviews", "Response Rate", "Sentiment %"]]
        for comp in comparison:
            is_target = comp.get("is_target", False)
            name = str(comp.get("name", ""))
            if is_target:
                name = f"** {name} (Target) **"
            table_data.append([
                name,
                f"{comp.get('avg_rating', 'N/A')}",
                str(comp.get("total_reviews", "N/A")),
                f"{comp.get('response_rate', 'N/A')}%",
                f"{comp.get('positive_pct', 'N/A')}%",
            ])
        t = styled_table(table_data, col_widths=[1.6 * inch, 0.9 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch])

        # Highlight target row
        for i, comp in enumerate(comparison):
            if comp.get("is_target", False):
                row_idx = i + 1  # +1 for header
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, row_idx), (-1, row_idx), colors.HexColor("#e8edff")),
                    ("FONTNAME", (0, row_idx), (-1, row_idx), "Helvetica-Bold"),
                ]))
        elements.append(t)
        elements.append(Spacer(1, 12))

    # Gaps
    gaps = safe_get(data, "competitive_gaps", [])
    if gaps:
        elements.append(Paragraph("Competitive Gaps", styles["SubHeader"]))
        gap_data = [["Gap", "Target Value", "Competitor Avg", "Severity"]]
        for g in gaps:
            gap_data.append([
                str(g.get("gap", "")),
                str(g.get("target_value", "")),
                str(g.get("competitor_avg", "")),
                str(g.get("severity", "")),
            ])
        elements.append(styled_table(gap_data, col_widths=[2.0 * inch, 1.0 * inch, 1.2 * inch, 1.0 * inch]))
        elements.append(Spacer(1, 10))

    # Opportunities
    opps = safe_get(data, "competitive_opportunities", [])
    if opps:
        elements.append(Paragraph("Competitive Opportunities", styles["SubHeader"]))
        opp_data = [["Opportunity", "Current State", "Potential Impact"]]
        for o in opps:
            opp_data.append([
                str(o.get("opportunity", "")),
                str(o.get("current_state", "")),
                str(o.get("impact", "")),
            ])
        elements.append(styled_table(opp_data, col_widths=[2.0 * inch, 1.5 * inch, 1.5 * inch]))
        elements.append(Spacer(1, 10))

    return elements


def build_response_section(data, styles):
    """Build the negative reviews with recommended responses section."""
    elements = []

    elements.append(Paragraph("5. Review Responses", styles["SectionHeader"]))
    elements.append(Table(
        [[""]], colWidths=[5 * inch],
        style=TableStyle([("LINEBELOW", (0, 0), (-1, 0), 2, ACCENT_BLUE)])
    ))
    elements.append(Spacer(1, 10))

    reviews = safe_get(data, "negative_reviews_with_responses", [])
    if reviews:
        elements.append(Paragraph(
            "The following are the most critical negative reviews found, along with "
            "recommended responses crafted to address each specific concern.",
            styles["BodyText2"]
        ))
        elements.append(Spacer(1, 8))

        for i, review in enumerate(reviews[:10]):  # Limit to 10
            # Review header
            platform = review.get("platform", "Unknown")
            rating = review.get("rating", "N/A")
            date = review.get("date", "N/A")

            elements.append(Paragraph(
                f'<b>Review #{i + 1}</b> | {platform} | {rating} stars | {date}',
                ParagraphStyle(
                    name=f"ReviewHeader{i}",
                    fontName="Helvetica-Bold",
                    fontSize=9,
                    textColor=NAVY,
                    spaceBefore=10,
                    spaceAfter=4,
                )
            ))

            # Review text
            review_text = review.get("review_text", "No text available.")
            elements.append(Paragraph(
                f'"{review_text}"',
                styles["QuoteText"]
            ))

            # Recommended response
            elements.append(Paragraph(
                '<font color="#28a745"><b>Recommended Response:</b></font>',
                ParagraphStyle(name=f"ResponseLabel{i}", fontSize=9, spaceBefore=2)
            ))
            response_text = review.get("recommended_response", "No response generated.")
            elements.append(Paragraph(
                response_text,
                ParagraphStyle(
                    name=f"ResponseText{i}",
                    fontName="Helvetica",
                    fontSize=9,
                    leading=12,
                    textColor=colors.HexColor("#333333"),
                    leftIndent=10,
                    spaceAfter=8,
                    borderPadding=(4, 4, 4, 4),
                )
            ))

            # Thin separator
            elements.append(Table(
                [[""]], colWidths=[4.5 * inch],
                style=TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.5, LIGHT_GRAY)])
            ))
    else:
        elements.append(Paragraph(
            "No negative reviews with responses available. Run the full analysis to populate.",
            styles["BodyText2"]
        ))

    elements.append(Spacer(1, 10))
    return elements


def build_action_plan_section(data, styles):
    """Build the 90-day action plan section."""
    elements = []

    elements.append(Paragraph("6. 90-Day Action Plan", styles["SectionHeader"]))
    elements.append(Table(
        [[""]], colWidths=[5 * inch],
        style=TableStyle([("LINEBELOW", (0, 0), (-1, 0), 2, ACCENT_BLUE)])
    ))
    elements.append(Spacer(1, 10))

    # Immediate actions
    immediate = safe_get(data, "immediate_actions", [])
    if immediate:
        elements.append(Paragraph("Immediate Actions (This Week)", styles["SubHeader"]))
        table_data = [["#", "Action", "Priority", "Effort", "Expected Impact"]]
        for i, action in enumerate(immediate):
            table_data.append([
                str(i + 1),
                str(action.get("title", "")),
                str(action.get("priority", "")),
                str(action.get("effort", "")),
                str(action.get("impact", "")),
            ])
        t = styled_table(table_data, col_widths=[0.3 * inch, 2.2 * inch, 0.7 * inch, 0.7 * inch, 1.3 * inch])

        # Color-code priority column
        for i, action in enumerate(immediate):
            row_idx = i + 1
            p = str(action.get("priority", ""))
            color = priority_color(p)
            t.setStyle(TableStyle([
                ("TEXTCOLOR", (2, row_idx), (2, row_idx), color),
                ("FONTNAME", (2, row_idx), (2, row_idx), "Helvetica-Bold"),
            ]))
        elements.append(t)
        elements.append(Spacer(1, 12))

    # Short-term improvements
    short_term = safe_get(data, "short_term_improvements", [])
    if short_term:
        elements.append(Paragraph("Short-Term Improvements (30 Days)", styles["SubHeader"]))
        table_data = [["#", "Improvement", "Priority", "Expected Outcome"]]
        for i, item in enumerate(short_term):
            table_data.append([
                str(i + 1),
                str(item.get("title", "")),
                str(item.get("priority", "")),
                str(item.get("expected_outcome", "")),
            ])
        elements.append(styled_table(
            table_data, col_widths=[0.3 * inch, 2.0 * inch, 0.7 * inch, 2.2 * inch]
        ))
        elements.append(Spacer(1, 12))

    # Medium-term
    medium_term = safe_get(data, "medium_term_strategies", [])
    if medium_term:
        elements.append(Paragraph("Medium-Term Strategy (90 Days)", styles["SubHeader"]))
        table_data = [["#", "Strategy", "Priority", "KPIs", "Target"]]
        for i, item in enumerate(medium_term):
            table_data.append([
                str(i + 1),
                str(item.get("title", "")),
                str(item.get("priority", "")),
                str(item.get("kpis", "")),
                str(item.get("target", "")),
            ])
        elements.append(styled_table(
            table_data, col_widths=[0.3 * inch, 1.8 * inch, 0.7 * inch, 1.2 * inch, 1.2 * inch]
        ))
        elements.append(Spacer(1, 12))

    # Long-term
    long_term = safe_get(data, "long_term_initiatives", [])
    if long_term:
        elements.append(Paragraph("Long-Term Initiatives (6-12 Months)", styles["SubHeader"]))
        table_data = [["#", "Initiative", "Vision", "Investment"]]
        for i, item in enumerate(long_term):
            table_data.append([
                str(i + 1),
                str(item.get("title", "")),
                str(item.get("vision", "")),
                str(item.get("investment", "")),
            ])
        elements.append(styled_table(
            table_data, col_widths=[0.3 * inch, 1.8 * inch, 2.0 * inch, 1.1 * inch]
        ))
        elements.append(Spacer(1, 12))

    # Projected scores
    projected = safe_get(data, "projected_scores", {})
    if projected:
        elements.append(Paragraph("Projected Reputation Score Improvement", styles["SubHeader"]))
        table_data = [["Timeframe", "Projected Score", "Key Drivers"]]
        for timeframe, info in projected.items():
            if isinstance(info, dict):
                table_data.append([
                    timeframe,
                    f"{info.get('score', 'N/A')}/100",
                    str(info.get("drivers", "")),
                ])
            else:
                table_data.append([timeframe, str(info), ""])
        elements.append(styled_table(
            table_data, col_widths=[1.5 * inch, 1.2 * inch, 2.5 * inch]
        ))

    elements.append(Spacer(1, 10))
    return elements


# ---------------------------------------------------------------------------
# Cover Page Canvas Drawing
# ---------------------------------------------------------------------------
def draw_cover_bg(canvas_obj, doc):
    """Draw the navy background for the cover page."""
    canvas_obj.saveState()

    # Full-page navy background
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)

    # Decorative accent bar at top
    canvas_obj.setFillColor(ACCENT_BLUE)
    canvas_obj.rect(0, letter[1] - 6, letter[0], 6, fill=1, stroke=0)

    # Decorative bottom strip
    canvas_obj.setFillColor(DARK_NAVY)
    canvas_obj.rect(0, 0, letter[0], 60, fill=1, stroke=0)

    # Side accent line
    canvas_obj.setStrokeColor(ACCENT_BLUE)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(50, letter[1] - 80, 50, 80)

    add_cover_footer(canvas_obj, doc)
    canvas_obj.restoreState()


# ---------------------------------------------------------------------------
# Main PDF Builder
# ---------------------------------------------------------------------------
def generate_pdf(data, output_path):
    """Generate the full reputation report PDF."""

    styles = get_styles()

    doc = BaseDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=70,
    )

    # Two page templates: one for cover, one for content
    cover_frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        id="cover_frame",
    )
    content_frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        id="content_frame",
    )

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover_bg),
        PageTemplate(id="content", frames=[content_frame], onPage=add_page_footer),
    ])

    # Build all elements
    elements = []

    # Cover page
    elements.extend(build_cover_page(data, styles))

    # Switch to content template after cover
    elements.append(NextPageTemplate("content"))

    # Executive Summary
    elements.extend(build_executive_summary(data, styles))
    elements.append(PageBreak())

    # Sentiment Analysis
    elements.extend(build_sentiment_section(data, styles))
    elements.append(PageBreak())

    # Theme Analysis
    elements.extend(build_theme_section(data, styles))
    elements.append(PageBreak())

    # Competitor Benchmarking
    elements.extend(build_competitor_section(data, styles))
    elements.append(PageBreak())

    # Review Responses
    elements.extend(build_response_section(data, styles))
    elements.append(PageBreak())

    # Action Plan
    elements.extend(build_action_plan_section(data, styles))

    # Build PDF
    try:
        doc.build(elements)
        print(f"PDF generated successfully: {output_path}")
        return True
    except Exception as e:
        print(f"ERROR generating PDF: {e}")
        return False


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate AI Reputation Manager PDF Report"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input JSON file with report data",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output PDF path (default: reputation_report_<business>.pdf)",
    )

    args = parser.parse_args()

    # Load input data
    input_path = args.input
    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in input file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Could not read input file: {e}")
        sys.exit(1)

    # Merge with defaults for missing keys
    defaults = get_default_data()
    for key, value in defaults.items():
        if key not in data:
            data[key] = value

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        biz = data.get("business_name", "business").replace(" ", "_").lower()
        output_path = f"reputation_report_{biz}.pdf"

    # Generate
    success = generate_pdf(data, output_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
