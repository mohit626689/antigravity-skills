#!/usr/bin/env python3
"""
AI Personal Finance Advisor — PDF Report Generator
==================================================

Generates a polished, multi-page Financial Plan PDF using ReportLab.

Inputs:
  --data PATH       Path to a JSON file containing the financial plan data.
                    See `_demo_data()` for the schema.
  --output PATH     Output PDF path. Defaults to FINANCE-PLAN.pdf.
  --demo            Generate a sample report with built-in demo data.

Layout (page-by-page):
  1. Cover page      — Financial Health Score gauge + grade + signal
  2. Score dashboard — 5 category bars (Cash Flow, Debt, Investments,
                       Retirement, Protection)
  3. Cash flow       — Income vs expense breakdown table
  4. Debt summary    — Payoff timeline and total interest cost
  5. Investments     — Allocation pie chart and commentary
  6. Retirement      — Current vs needed projection gap
  7. Protection      — Insurance / estate scorecard
  8. Action items    — Top 10 prioritized actions
  9. 90-day plan     — Month 1 / 2 / 3 focus areas

Disclaimer footer appears on every page.

This is NOT financial advice.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

try:
    from reportlab.lib import colors
    from reportlab.lib.colors import HexColor, Color
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import (
        BaseDocTemplate,
        Frame,
        KeepTogether,
        PageBreak,
        PageTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
    )
    from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String, Wedge, Polygon
    from reportlab.graphics.charts.barcharts import HorizontalBarChart
    from reportlab.graphics.charts.piecharts import Pie
except ImportError as exc:  # pragma: no cover
    sys.stderr.write(
        "ERROR: ReportLab is required.\n"
        "Install with:  pip3 install 'reportlab>=4.0.0'\n"
        f"Underlying error: {exc}\n"
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
GREEN = HexColor("#2d8a4e")
GREEN_LIGHT = HexColor("#e8f5ed")
BLUE = HexColor("#4a9eff")
BLUE_LIGHT = HexColor("#eaf3ff")
GOLD = HexColor("#e8a838")
GOLD_LIGHT = HexColor("#fcf2dc")
RED = HexColor("#e74c3c")
RED_LIGHT = HexColor("#fde8e6")
NAVY = HexColor("#0c1220")
SLATE = HexColor("#1a2840")
INK = HexColor("#1f2937")
MUTED = HexColor("#6b7280")
RULE = HexColor("#e5e7eb")
PAGE_BG = HexColor("#ffffff")
SOFT = HexColor("#f7f9fc")


def score_color(score: float) -> Color:
    """Green (>=70), amber (40-69), red (<40)."""
    if score >= 70:
        return GREEN
    if score >= 40:
        return GOLD
    return RED


def score_color_light(score: float) -> Color:
    if score >= 70:
        return GREEN_LIGHT
    if score >= 40:
        return GOLD_LIGHT
    return RED_LIGHT


def hexstr(c: Color) -> str:
    """Return a #RRGGBB string for a reportlab Color."""
    r = int(round(c.red * 255))
    g = int(round(c.green * 255))
    b = int(round(c.blue * 255))
    return f"#{r:02x}{g:02x}{b:02x}"


def score_grade(score: float) -> str:
    if score >= 90:
        return "A+"
    if score >= 85:
        return "A"
    if score >= 80:
        return "A-"
    if score >= 75:
        return "B+"
    if score >= 70:
        return "B"
    if score >= 65:
        return "B-"
    if score >= 60:
        return "C+"
    if score >= 55:
        return "C"
    if score >= 50:
        return "C-"
    if score >= 45:
        return "D+"
    if score >= 40:
        return "D"
    return "F"


def score_signal(score: float) -> str:
    if score >= 80:
        return "Excellent — On Track"
    if score >= 65:
        return "Healthy — Minor Tune-Up"
    if score >= 50:
        return "Fair — Action Needed"
    if score >= 35:
        return "Weak — Plan Required"
    return "Critical — Immediate Action"


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def build_styles() -> Dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "title", parent=base["Title"],
            fontName="Helvetica-Bold", fontSize=30, leading=34,
            textColor=NAVY, alignment=TA_CENTER, spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", parent=base["Normal"],
            fontName="Helvetica", fontSize=13, leading=16,
            textColor=MUTED, alignment=TA_CENTER, spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"],
            fontName="Helvetica-Bold", fontSize=22, leading=26,
            textColor=NAVY, spaceBefore=6, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"],
            fontName="Helvetica-Bold", fontSize=15, leading=18,
            textColor=NAVY, spaceBefore=10, spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "h3", parent=base["Heading3"],
            fontName="Helvetica-Bold", fontSize=12, leading=15,
            textColor=GREEN, spaceBefore=6, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body", parent=base["BodyText"],
            fontName="Helvetica", fontSize=10.5, leading=14.5,
            textColor=INK, alignment=TA_LEFT, spaceAfter=6,
        ),
        "body_just": ParagraphStyle(
            "body_just", parent=base["BodyText"],
            fontName="Helvetica", fontSize=10.5, leading=14.5,
            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "small", parent=base["Normal"],
            fontName="Helvetica", fontSize=8.5, leading=11,
            textColor=MUTED, alignment=TA_LEFT,
        ),
        "kicker": ParagraphStyle(
            "kicker", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=9.5, leading=12,
            textColor=GOLD, alignment=TA_LEFT, spaceAfter=2,
        ),
        "callout": ParagraphStyle(
            "callout", parent=base["Normal"],
            fontName="Helvetica", fontSize=10, leading=14,
            textColor=INK, alignment=TA_LEFT,
        ),
        "footer": ParagraphStyle(
            "footer", parent=base["Normal"],
            fontName="Helvetica-Oblique", fontSize=7.5, leading=10,
            textColor=MUTED, alignment=TA_CENTER,
        ),
    }
    return styles


# ---------------------------------------------------------------------------
# Page frame + footer
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = LETTER
MARGIN_L = MARGIN_R = 0.7 * inch
MARGIN_T = 0.7 * inch
MARGIN_B = 0.85 * inch
DISCLAIMER_TEXT = (
    "This report is for informational purposes only and is NOT financial, "
    "investment, tax, or legal advice. Consult a licensed financial advisor "
    "before making decisions. Projections are estimates and not guarantees."
)


def _draw_footer(canvas: Canvas, doc: BaseDocTemplate) -> None:
    canvas.saveState()
    # Top rule on first page header is handled per-page; footer is universal.
    # Footer bar
    canvas.setFillColor(SOFT)
    canvas.rect(0, 0, PAGE_W, 0.55 * inch, stroke=0, fill=1)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, 0.55 * inch, PAGE_W - MARGIN_R, 0.55 * inch)

    # Disclaimer (left two-thirds)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica-Oblique", 7.5)
    # Wrap manually — text is short
    canvas.drawString(MARGIN_L, 0.36 * inch, DISCLAIMER_TEXT[:115])
    canvas.drawString(MARGIN_L, 0.24 * inch, DISCLAIMER_TEXT[115:])

    # Page number (right)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(NAVY)
    canvas.drawRightString(PAGE_W - MARGIN_R, 0.30 * inch, f"Page {doc.page}")

    # Brand strip top-right
    canvas.setFillColor(GOLD)
    canvas.rect(PAGE_W - MARGIN_R - 1.2 * inch, PAGE_H - 0.35 * inch, 1.2 * inch, 0.06 * inch, stroke=0, fill=1)
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica-Bold", 7)
    canvas.drawRightString(
        PAGE_W - MARGIN_R, PAGE_H - 0.20 * inch, "AI PERSONAL FINANCE ADVISOR"
    )

    canvas.restoreState()


# ---------------------------------------------------------------------------
# Reusable drawings
# ---------------------------------------------------------------------------
def gauge_drawing(score: float, width: float = 4.2 * inch, height: float = 2.3 * inch) -> Drawing:
    """Half-circle gauge for the Financial Health Score."""
    d = Drawing(width, height)
    cx = width / 2
    cy = 0.35 * inch
    radius = min(width / 2.4, height - 0.1 * inch)

    # Background arc (gray track)
    d.add(Wedge(cx, cy, radius, 180, 0, fillColor=HexColor("#eef1f6"), strokeColor=None))
    inner = radius * 0.62
    d.add(Wedge(cx, cy, inner, 180, 0, fillColor=PAGE_BG, strokeColor=None))

    # Colored arc proportional to score
    score = max(0.0, min(100.0, float(score)))
    end_angle = 180 - (score / 100.0) * 180  # sweep from 180 -> 0
    fill = score_color(score)
    if score > 0:
        d.add(Wedge(cx, cy, radius, 180, end_angle, fillColor=fill, strokeColor=None))
        d.add(Wedge(cx, cy, inner, 180, end_angle, fillColor=PAGE_BG, strokeColor=None))

    # Tick labels
    for i, label in enumerate(["0", "25", "50", "75", "100"]):
        ang_deg = 180 - i * 45
        ang = math.radians(ang_deg)
        tx = cx + (radius + 0.12 * inch) * math.cos(ang)
        ty = cy + (radius + 0.12 * inch) * math.sin(ang)
        s = String(tx, ty, label, fontName="Helvetica", fontSize=7, fillColor=MUTED, textAnchor="middle")
        d.add(s)

    # Score number
    num = String(cx, cy + 0.18 * inch, f"{int(round(score))}", fontName="Helvetica-Bold", fontSize=36, fillColor=NAVY, textAnchor="middle")
    d.add(num)
    sub = String(cx, cy - 0.02 * inch, "out of 100", fontName="Helvetica", fontSize=8.5, fillColor=MUTED, textAnchor="middle")
    d.add(sub)
    return d


def category_bar(label: str, score: float, width: float = 6.5 * inch) -> Table:
    """A single horizontal bar row used on the score dashboard."""
    score = max(0.0, min(100.0, float(score)))
    fill = score_color(score)
    track_w = width - 2.3 * inch
    bar_w = max(0.05 * inch, track_w * (score / 100.0))

    d = Drawing(track_w, 0.28 * inch)
    d.add(Rect(0, 0.06 * inch, track_w, 0.16 * inch, fillColor=HexColor("#eef1f6"), strokeColor=None))
    d.add(Rect(0, 0.06 * inch, bar_w, 0.16 * inch, fillColor=fill, strokeColor=None))

    label_para = Paragraph(f"<b>{label}</b>", ParagraphStyle("lbl", fontName="Helvetica-Bold", fontSize=10, textColor=INK, leading=12))
    score_para = Paragraph(
        f"<font color='#1f2937'><b>{int(round(score))}</b></font> "
        f"<font color='#6b7280' size=8>/ 100</font>",
        ParagraphStyle("sc", fontName="Helvetica", fontSize=10, alignment=TA_RIGHT, leading=12),
    )

    tbl = Table([[label_para, d, score_para]],
                colWidths=[1.6 * inch, track_w, 0.7 * inch], rowHeights=[0.32 * inch])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return tbl


def pie_drawing(slices: List[Tuple[str, float]], width: float = 3.4 * inch, height: float = 3.0 * inch) -> Drawing:
    """Allocation pie chart."""
    d = Drawing(width, height)
    p = Pie()
    p.x = 0.4 * inch
    p.y = 0.2 * inch
    p.width = 2.4 * inch
    p.height = 2.4 * inch
    p.data = [max(0.001, float(v)) for _, v in slices]
    p.labels = [f"{n} ({v:.0f}%)" for n, v in slices]
    p.simpleLabels = 1
    p.slices.strokeColor = colors.white
    p.slices.strokeWidth = 1.2
    palette = [GREEN, BLUE, GOLD, RED, HexColor("#7c5cff"), HexColor("#16b6c9"), MUTED]
    for i in range(len(slices)):
        p.slices[i].fillColor = palette[i % len(palette)]
    p.sideLabels = 1
    p.sideLabelsOffset = 0.06 * inch
    d.add(p)
    return d


def kv_table(rows: List[Tuple[str, str]], col_widths: Optional[List[float]] = None,
             header: Optional[Tuple[str, str]] = None) -> Table:
    """Simple two-column key/value table."""
    data: List[List[Any]] = []
    if header:
        data.append([header[0], header[1]])
    data.extend(rows)
    cw = col_widths or [2.6 * inch, 4.0 * inch]
    tbl = Table(data, colWidths=cw)
    style = [
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [PAGE_BG, SOFT]),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica"),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10.5),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
        ]
    tbl.setStyle(TableStyle(style))
    return tbl


def money(n: float) -> str:
    sign = "-" if n < 0 else ""
    return f"{sign}${abs(n):,.0f}"


def pct(n: float, decimals: int = 1) -> str:
    return f"{n:.{decimals}f}%"


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------
def build_cover(story: List[Any], styles: Dict[str, ParagraphStyle], data: Dict[str, Any]) -> None:
    client = data.get("client_name") or "Personal Financial Plan"
    as_of = data.get("as_of") or datetime.now().strftime("%B %d, %Y")
    score = float(data.get("health_score", 0))
    grade = data.get("grade") or score_grade(score)
    signal = data.get("signal") or score_signal(score)

    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph("FINANCIAL HEALTH REPORT", styles["kicker"]))
    story.append(Paragraph(client, styles["title"]))
    story.append(Paragraph(f"Prepared {as_of}", styles["subtitle"]))

    story.append(Spacer(1, 0.15 * inch))
    story.append(gauge_drawing(score, width=4.6 * inch, height=2.4 * inch))
    story.append(Spacer(1, 0.05 * inch))

    grade_box = Table(
        [[Paragraph(f"<font size=22 color='#0c1220'><b>{grade}</b></font>", styles["body"]),
          Paragraph(f"<font size=11 color='#6b7280'>OVERALL GRADE</font>", styles["body"])],
         [Paragraph(f"<font size=13 color='{hexstr(score_color(score))}'><b>{signal}</b></font>", styles["body"]),
          Paragraph(f"<font size=11 color='#6b7280'>SIGNAL</font>", styles["body"])]],
        colWidths=[2.6 * inch, 2.6 * inch],
        rowHeights=[0.45 * inch, 0.45 * inch],
    )
    grade_box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, RULE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.4, RULE),
        ("LINEAFTER", (0, 0), (0, -1), 0.4, RULE),
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(grade_box)

    story.append(Spacer(1, 0.35 * inch))
    summary = data.get("executive_summary") or (
        "This report summarizes your overall financial health across five dimensions: "
        "cash flow, debt, investments, retirement readiness, and protection. "
        "Each section includes a score, key findings, and prioritized actions."
    )
    story.append(Paragraph("Executive Summary", styles["h2"]))
    story.append(Paragraph(summary, styles["body_just"]))

    story.append(PageBreak())


def build_score_dashboard(story: List[Any], styles: Dict[str, ParagraphStyle], data: Dict[str, Any]) -> None:
    story.append(Paragraph("Score Dashboard", styles["h1"]))
    story.append(Paragraph(
        "Your Financial Health Score is a weighted composite of five categories. "
        "Each is scored 0–100. Green = strong, amber = needs attention, red = critical.",
        styles["body"]))
    story.append(Spacer(1, 0.15 * inch))

    cats = data.get("categories", {})
    rows = [
        ("Cash Flow", float(cats.get("cash_flow", 0))),
        ("Debt", float(cats.get("debt", 0))),
        ("Investments", float(cats.get("investments", 0))),
        ("Retirement", float(cats.get("retirement", 0))),
        ("Protection", float(cats.get("protection", 0))),
    ]
    for label, sc in rows:
        story.append(category_bar(label, sc))
        story.append(Spacer(1, 0.04 * inch))

    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("Category Notes", styles["h2"]))
    notes = data.get("category_notes", {})
    note_rows = [
        ("Cash Flow", notes.get("cash_flow", "—")),
        ("Debt", notes.get("debt", "—")),
        ("Investments", notes.get("investments", "—")),
        ("Retirement", notes.get("retirement", "—")),
        ("Protection", notes.get("protection", "—")),
    ]
    for label, note in note_rows:
        story.append(Paragraph(f"<b>{label}.</b> {note}", styles["body"]))

    story.append(PageBreak())


def build_cash_flow(story: List[Any], styles: Dict[str, ParagraphStyle], data: Dict[str, Any]) -> None:
    cf = data.get("cash_flow", {})
    income = float(cf.get("monthly_income", 0))
    expenses_list: List[Tuple[str, float]] = cf.get("expenses", []) or []
    total_exp = sum(v for _, v in expenses_list)
    surplus = income - total_exp
    savings_rate = (surplus / income * 100.0) if income else 0.0

    story.append(Paragraph("Cash Flow Analysis", styles["h1"]))
    story.append(Paragraph(
        "Monthly inflows and outflows. A healthy savings rate is typically 15–25% of "
        "gross income; aggressive savers target 30%+.", styles["body"]))

    # Summary cards
    cards = Table([[
        Paragraph(f"<font color='#6b7280' size=9>MONTHLY INCOME</font><br/><font color='#0c1220' size=18><b>{money(income)}</b></font>", styles["body"]),
        Paragraph(f"<font color='#6b7280' size=9>MONTHLY EXPENSES</font><br/><font color='#0c1220' size=18><b>{money(total_exp)}</b></font>", styles["body"]),
        Paragraph(f"<font color='#6b7280' size=9>NET SURPLUS</font><br/><font color='{hexstr(GREEN if surplus>=0 else RED)}' size=18><b>{money(surplus)}</b></font>", styles["body"]),
        Paragraph(f"<font color='#6b7280' size=9>SAVINGS RATE</font><br/><font color='#0c1220' size=18><b>{pct(savings_rate)}</b></font>", styles["body"]),
    ]], colWidths=[1.6 * inch] * 4, rowHeights=[0.7 * inch])
    cards.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, RULE),
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(cards)
    story.append(Spacer(1, 0.25 * inch))

    # Expense breakdown table
    story.append(Paragraph("Expense Breakdown", styles["h2"]))
    rows: List[List[Any]] = [["Category", "Monthly Amount", "% of Income"]]
    for name, amount in expenses_list:
        share = (amount / income * 100.0) if income else 0.0
        rows.append([name, money(amount), pct(share)])
    rows.append(["TOTAL", money(total_exp), pct((total_exp / income * 100.0) if income else 0.0)])
    tbl = Table(rows, colWidths=[3.0 * inch, 1.8 * inch, 1.8 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [PAGE_BG, SOFT]),
        ("BACKGROUND", (0, -1), (-1, -1), GREEN_LIGHT),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, RULE),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(tbl)

    story.append(Spacer(1, 0.2 * inch))
    commentary = cf.get("commentary") or (
        "Your largest expense categories drive the most leverage. "
        "A 5% reduction in housing and food typically yields the highest savings rate gains."
    )
    story.append(Paragraph(f"<b>Insight.</b> {commentary}", styles["body_just"]))

    story.append(PageBreak())


def build_debt_summary(story: List[Any], styles: Dict[str, ParagraphStyle], data: Dict[str, Any]) -> None:
    debt = data.get("debt", {})
    debts: List[Dict[str, Any]] = debt.get("accounts", []) or []
    total_balance = sum(float(d.get("balance", 0)) for d in debts)
    total_min = sum(float(d.get("min_payment", 0)) for d in debts)
    method = debt.get("strategy", "Avalanche (highest APR first)")
    payoff_months = int(debt.get("payoff_months", 0))
    total_interest = float(debt.get("total_interest", 0))

    story.append(Paragraph("Debt Summary & Payoff Plan", styles["h1"]))
    story.append(Paragraph(
        f"Strategy: <b>{method}</b>. The avalanche method minimizes total interest by attacking the highest-APR balance first. "
        "The snowball method builds momentum by attacking the smallest balance first.",
        styles["body_just"]))
    story.append(Spacer(1, 0.1 * inch))

    cards = Table([[
        Paragraph(f"<font color='#6b7280' size=9>TOTAL DEBT</font><br/><font color='#0c1220' size=16><b>{money(total_balance)}</b></font>", styles["body"]),
        Paragraph(f"<font color='#6b7280' size=9>MIN. PAYMENTS</font><br/><font color='#0c1220' size=16><b>{money(total_min)}/mo</b></font>", styles["body"]),
        Paragraph(f"<font color='#6b7280' size=9>PAYOFF TIMELINE</font><br/><font color='#0c1220' size=16><b>{payoff_months} months</b></font>", styles["body"]),
        Paragraph(f"<font color='#6b7280' size=9>TOTAL INTEREST</font><br/><font color='#e74c3c' size=16><b>{money(total_interest)}</b></font>", styles["body"]),
    ]], colWidths=[1.6 * inch] * 4, rowHeights=[0.7 * inch])
    cards.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, RULE),
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(cards)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Account Detail", styles["h2"]))
    rows: List[List[Any]] = [["Account", "Balance", "APR", "Min Pmt", "Payoff Order"]]
    for i, d in enumerate(debts, start=1):
        rows.append([
            d.get("name", "—"),
            money(float(d.get("balance", 0))),
            pct(float(d.get("apr", 0))),
            money(float(d.get("min_payment", 0))),
            f"#{d.get('order', i)}",
        ])
    tbl = Table(rows, colWidths=[2.2 * inch, 1.2 * inch, 0.9 * inch, 1.1 * inch, 1.2 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAGE_BG, SOFT]),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, RULE),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(tbl)

    # Payoff timeline visual (simple bar)
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("Payoff Timeline", styles["h2"]))
    months = max(payoff_months, 1)
    timeline_w = 6.5 * inch
    d = Drawing(timeline_w, 0.4 * inch)
    d.add(Rect(0, 0.18 * inch, timeline_w, 0.16 * inch, fillColor=HexColor("#eef1f6"), strokeColor=None))
    d.add(Rect(0, 0.18 * inch, timeline_w, 0.16 * inch, fillColor=GREEN, strokeColor=None))
    # Year markers
    years = max(1, math.ceil(months / 12))
    for y in range(years + 1):
        x = (y * 12 / months) * timeline_w
        x = min(x, timeline_w)
        d.add(Line(x, 0.12 * inch, x, 0.38 * inch, strokeColor=MUTED, strokeWidth=0.4))
        d.add(String(x, 0.02 * inch, f"Yr {y}", fontName="Helvetica", fontSize=7.5, fillColor=MUTED, textAnchor="middle"))
    story.append(d)
    story.append(Paragraph(
        f"<font color='#6b7280' size=9>At your current strategy you become debt-free in approximately <b>{payoff_months} months</b> "
        f"({months/12:.1f} years), paying <b>{money(total_interest)}</b> in interest.</font>",
        styles["body"]))

    story.append(PageBreak())


def build_investments(story: List[Any], styles: Dict[str, ParagraphStyle], data: Dict[str, Any]) -> None:
    inv = data.get("investments", {})
    total = float(inv.get("total_value", 0))
    allocation: List[Tuple[str, float]] = [(a["name"], float(a["pct"])) for a in inv.get("allocation", [])]

    story.append(Paragraph("Investment Allocation", styles["h1"]))
    story.append(Paragraph(
        f"Total invested assets: <b>{money(total)}</b>. The pie below shows your current allocation. "
        "A well-diversified portfolio typically holds a mix appropriate for your age and risk tolerance.",
        styles["body_just"]))
    story.append(Spacer(1, 0.1 * inch))

    # Pie + commentary table side-by-side
    pie = pie_drawing(allocation, width=3.4 * inch, height=2.8 * inch)
    commentary = inv.get("commentary") or (
        "Your equity exposure looks appropriate for your age band. "
        "Consider rebalancing if any asset class has drifted more than 5 percentage points from target."
    )
    target_rows = [["Asset Class", "Current", "Target", "Variance"]]
    for a in inv.get("allocation", []):
        cur = float(a.get("pct", 0))
        tgt = float(a.get("target_pct", cur))
        var = cur - tgt
        target_rows.append([a.get("name", "—"), pct(cur), pct(tgt), f"{'+' if var>=0 else ''}{var:.1f}%"])
    tbl = Table(target_rows, colWidths=[1.5 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAGE_BG, SOFT]),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    layout = Table([[pie, tbl]], colWidths=[3.6 * inch, 3.6 * inch])
    layout.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(layout)

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"<b>Allocation insight.</b> {commentary}", styles["body_just"]))

    story.append(PageBreak())


def build_retirement(story: List[Any], styles: Dict[str, ParagraphStyle], data: Dict[str, Any]) -> None:
    r = data.get("retirement", {})
    current = float(r.get("current_balance", 0))
    needed = float(r.get("target_balance", 0))
    gap = needed - current
    age = int(r.get("current_age", 0))
    retire_age = int(r.get("retirement_age", 65))
    years_left = max(0, retire_age - age)
    monthly_save = float(r.get("monthly_contribution", 0))

    story.append(Paragraph("Retirement Projection", styles["h1"]))
    story.append(Paragraph(
        f"At age <b>{age}</b>, targeting retirement at age <b>{retire_age}</b> "
        f"({years_left} years away). Projections assume a 6–7% real return.",
        styles["body_just"]))
    story.append(Spacer(1, 0.1 * inch))

    cards = Table([[
        Paragraph(f"<font color='#6b7280' size=9>CURRENT BALANCE</font><br/><font color='#0c1220' size=16><b>{money(current)}</b></font>", styles["body"]),
        Paragraph(f"<font color='#6b7280' size=9>TARGET AT RETIREMENT</font><br/><font color='#0c1220' size=16><b>{money(needed)}</b></font>", styles["body"]),
        Paragraph(f"<font color='#6b7280' size=9>GAP</font><br/><font color='{hexstr(GREEN if gap<=0 else RED)}' size=16><b>{money(gap)}</b></font>", styles["body"]),
        Paragraph(f"<font color='#6b7280' size=9>MONTHLY CONTRIBUTION</font><br/><font color='#0c1220' size=16><b>{money(monthly_save)}</b></font>", styles["body"]),
    ]], colWidths=[1.6 * inch] * 4, rowHeights=[0.7 * inch])
    cards.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, RULE),
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(cards)

    # Progress bar to target
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("Progress to Target", styles["h2"]))
    track_w = 6.5 * inch
    pctp = 0 if needed <= 0 else min(1.0, current / needed)
    d = Drawing(track_w, 0.45 * inch)
    d.add(Rect(0, 0.18 * inch, track_w, 0.18 * inch, fillColor=HexColor("#eef1f6"), strokeColor=None))
    d.add(Rect(0, 0.18 * inch, track_w * pctp, 0.18 * inch, fillColor=GREEN, strokeColor=None))
    d.add(String(track_w / 2, 0.22 * inch, f"{pctp*100:.0f}% of target", fontName="Helvetica-Bold", fontSize=10, fillColor=NAVY, textAnchor="middle"))
    story.append(d)

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Scenario Comparison", styles["h2"]))
    scenarios = r.get("scenarios", []) or []
    if scenarios:
        rows = [["Scenario", "Monthly Save", "Projected Balance @ Retirement", "Result"]]
        for s in scenarios:
            rows.append([
                s.get("name", "—"),
                money(float(s.get("monthly", 0))),
                money(float(s.get("projected", 0))),
                s.get("verdict", "—"),
            ])
        tbl = Table(rows, colWidths=[1.6 * inch, 1.4 * inch, 2.3 * inch, 1.2 * inch])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAGE_BG, SOFT]),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(tbl)

    story.append(Spacer(1, 0.2 * inch))
    insight = r.get("commentary") or (
        f"To close the gap, increasing contributions by ~10–15% or adding $300–$500/mo can "
        f"materially shift your projected balance by {years_left} years from now."
    )
    story.append(Paragraph(f"<b>Retirement insight.</b> {insight}", styles["body_just"]))

    story.append(PageBreak())


def build_protection(story: List[Any], styles: Dict[str, ParagraphStyle], data: Dict[str, Any]) -> None:
    p = data.get("protection", {})
    items: List[Dict[str, Any]] = p.get("items", []) or []

    story.append(Paragraph("Protection Scorecard", styles["h1"]))
    story.append(Paragraph(
        "Protection covers insurance and estate planning — the foundation that prevents "
        "a single event from undoing years of saving and investing.",
        styles["body_just"]))
    story.append(Spacer(1, 0.1 * inch))

    rows: List[List[Any]] = [["Coverage Area", "Status", "Recommendation"]]
    for it in items:
        status = it.get("status", "—")
        rows.append([it.get("name", "—"), status, it.get("recommendation", "—")])

    tbl = Table(rows, colWidths=[2.0 * inch, 1.4 * inch, 3.2 * inch])
    style_rows = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAGE_BG, SOFT]),
        ("ALIGN", (1, 1), (1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    # Color the status cells
    for i, it in enumerate(items, start=1):
        st = (it.get("status") or "").lower()
        if "good" in st or "ok" in st or "yes" in st or "covered" in st:
            style_rows.append(("BACKGROUND", (1, i), (1, i), GREEN_LIGHT))
            style_rows.append(("TEXTCOLOR", (1, i), (1, i), GREEN))
        elif "partial" in st or "review" in st or "gap" in st:
            style_rows.append(("BACKGROUND", (1, i), (1, i), GOLD_LIGHT))
            style_rows.append(("TEXTCOLOR", (1, i), (1, i), GOLD))
        elif "miss" in st or "none" in st or "no" == st or "critical" in st:
            style_rows.append(("BACKGROUND", (1, i), (1, i), RED_LIGHT))
            style_rows.append(("TEXTCOLOR", (1, i), (1, i), RED))
    tbl.setStyle(TableStyle(style_rows))
    story.append(tbl)

    story.append(Spacer(1, 0.2 * inch))
    note = p.get("commentary") or (
        "Term life insurance is cheap when you're young and healthy — lock in coverage early. "
        "Disability insurance is often the most overlooked policy and protects your largest asset: your future income."
    )
    story.append(Paragraph(f"<b>Protection insight.</b> {note}", styles["body_just"]))

    story.append(PageBreak())


def build_action_items(story: List[Any], styles: Dict[str, ParagraphStyle], data: Dict[str, Any]) -> None:
    actions: List[Dict[str, Any]] = data.get("action_items", []) or []
    actions = actions[:10]

    story.append(Paragraph("Top 10 Action Items", styles["h1"]))
    story.append(Paragraph(
        "Prioritized by impact and ease of execution. Work through these in order for the "
        "fastest improvement to your Financial Health Score.",
        styles["body_just"]))
    story.append(Spacer(1, 0.1 * inch))

    rows: List[List[Any]] = [["#", "Action", "Category", "Priority", "Impact"]]
    for i, a in enumerate(actions, start=1):
        rows.append([
            str(i),
            Paragraph(a.get("action", "—"), ParagraphStyle("ai", fontName="Helvetica", fontSize=9.5, leading=12)),
            a.get("category", "—"),
            a.get("priority", "—"),
            a.get("impact", "—"),
        ])
    tbl = Table(rows, colWidths=[0.35 * inch, 3.4 * inch, 1.1 * inch, 0.9 * inch, 0.85 * inch])
    style_rows = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAGE_BG, SOFT]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for i, a in enumerate(actions, start=1):
        prio = (a.get("priority") or "").lower()
        if "high" in prio or "critical" in prio:
            style_rows.append(("TEXTCOLOR", (3, i), (3, i), RED))
            style_rows.append(("FONTNAME", (3, i), (3, i), "Helvetica-Bold"))
        elif "med" in prio:
            style_rows.append(("TEXTCOLOR", (3, i), (3, i), GOLD))
        elif "low" in prio:
            style_rows.append(("TEXTCOLOR", (3, i), (3, i), GREEN))
    tbl.setStyle(TableStyle(style_rows))
    story.append(tbl)

    story.append(PageBreak())


def build_90_day_plan(story: List[Any], styles: Dict[str, ParagraphStyle], data: Dict[str, Any]) -> None:
    plan = data.get("ninety_day_plan", {}) or {}
    m1 = plan.get("month_1", []) or []
    m2 = plan.get("month_2", []) or []
    m3 = plan.get("month_3", []) or []

    story.append(Paragraph("Your 90-Day Plan", styles["h1"]))
    story.append(Paragraph(
        "Three focused months. Each month has 3–5 concrete tasks. Completing all three "
        "months typically moves your Financial Health Score by 10–20 points.",
        styles["body_just"]))
    story.append(Spacer(1, 0.15 * inch))

    def month_block(title: str, color: Color, items: List[str]) -> Table:
        header = Paragraph(
            f"<font color='#ffffff'><b>{title}</b></font>",
            ParagraphStyle("mh", fontName="Helvetica-Bold", fontSize=12, alignment=TA_CENTER, leading=14),
        )
        body_lines = []
        for it in items or ["—"]:
            body_lines.append(f"• {it}")
        body_para = Paragraph("<br/>".join(body_lines),
                              ParagraphStyle("mb", fontName="Helvetica", fontSize=9.5, leading=13, textColor=INK))
        t = Table([[header], [body_para]], colWidths=[2.15 * inch], rowHeights=[0.38 * inch, 2.4 * inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), color),
            ("BACKGROUND", (0, 1), (-1, 1), SOFT),
            ("BOX", (0, 0), (-1, -1), 0.5, color),
            ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
            ("VALIGN", (0, 1), (-1, 1), "TOP"),
            ("LEFTPADDING", (0, 1), (-1, 1), 10),
            ("RIGHTPADDING", (0, 1), (-1, 1), 10),
            ("TOPPADDING", (0, 1), (-1, 1), 10),
            ("BOTTOMPADDING", (0, 1), (-1, 1), 10),
        ]))
        return t

    cols = Table(
        [[month_block("MONTH 1 — Foundation", GREEN, m1),
          month_block("MONTH 2 — Acceleration", BLUE, m2),
          month_block("MONTH 3 — Optimization", GOLD, m3)]],
        colWidths=[2.25 * inch, 2.25 * inch, 2.25 * inch],
    )
    cols.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(cols)

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("After 90 Days", styles["h2"]))
    after = plan.get("after_90_days") or (
        "Re-run /finance to recalculate your Financial Health Score. Most users see "
        "10–20 point gains in the first 90 days of focused execution."
    )
    story.append(Paragraph(after, styles["body_just"]))

    story.append(Spacer(1, 0.3 * inch))
    # Final disclaimer block
    final = Paragraph(
        "<b>Important disclaimer.</b> This Financial Plan is generated by an AI tool using the inputs you provided. "
        "It is for educational and informational purposes only and does not constitute financial, investment, tax, or "
        "legal advice. Consult a licensed financial advisor, CPA, or attorney before making any financial decisions. "
        "All projections are estimates based on assumptions that may not match real-world outcomes.",
        ParagraphStyle("final", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=MUTED, alignment=TA_JUSTIFY),
    )
    fbox = Table([[final]], colWidths=[7.1 * inch])
    fbox.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GOLD_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.6, GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(fbox)


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------
def _demo_data() -> Dict[str, Any]:
    return {
        "client_name": "Sample Client — Jordan Rivera",
        "as_of": datetime.now().strftime("%B %d, %Y"),
        "health_score": 68,
        "grade": "B-",
        "signal": "Healthy — Minor Tune-Up",
        "executive_summary": (
            "Jordan, age 38, has a solid foundation: positive cash flow, retirement contributions in place, "
            "and term life insurance. The biggest leverage points are accelerating credit card payoff "
            "(saving ~$4,800 in interest) and raising the 401(k) deferral from 8% to 12% to close the "
            "retirement gap by age 65. Estate documents are missing — a critical fix."
        ),
        "categories": {
            "cash_flow": 78,
            "debt": 52,
            "investments": 71,
            "retirement": 64,
            "protection": 58,
        },
        "category_notes": {
            "cash_flow": "21% savings rate is above average. Housing at 28% of income is healthy.",
            "debt": "Credit card balance at 22% APR is dragging the score. Avalanche payoff in 14 months.",
            "investments": "Equity-heavy allocation suits age 38. Slight overweight in US large-cap.",
            "retirement": "On track for ~85% of target at age 65. Boosting contributions closes the gap.",
            "protection": "Term life is good. Disability coverage is partial. No will or POA on file.",
        },
        "cash_flow": {
            "monthly_income": 9200,
            "expenses": [
                ("Housing (mortgage, tax, ins.)", 2580),
                ("Utilities & internet", 290),
                ("Groceries", 720),
                ("Dining & entertainment", 420),
                ("Transportation", 540),
                ("Insurance (health, auto)", 480),
                ("Subscriptions", 95),
                ("Personal / shopping", 380),
                ("Childcare / education", 620),
                ("Debt payments (min)", 360),
                ("Misc / buffer", 200),
            ],
            "commentary": (
                "Dining + subscriptions ($515/mo) is the easiest place to recapture $150–$200/month "
                "and redirect it to debt payoff or retirement contributions."
            ),
        },
        "debt": {
            "strategy": "Avalanche (highest APR first)",
            "payoff_months": 38,
            "total_interest": 7420,
            "accounts": [
                {"name": "Credit Card — Chase Sapphire", "balance": 8400, "apr": 22.0, "min_payment": 220, "order": 1},
                {"name": "Auto Loan — Toyota", "balance": 14200, "apr": 5.9, "min_payment": 380, "order": 3},
                {"name": "Student Loan — Federal", "balance": 18600, "apr": 6.2, "min_payment": 210, "order": 2},
            ],
        },
        "investments": {
            "total_value": 184000,
            "allocation": [
                {"name": "US Stocks", "pct": 58, "target_pct": 50},
                {"name": "Intl Stocks", "pct": 14, "target_pct": 20},
                {"name": "Bonds", "pct": 18, "target_pct": 20},
                {"name": "Real Estate (REIT)", "pct": 6, "target_pct": 7},
                {"name": "Cash / MM", "pct": 4, "target_pct": 3},
            ],
            "commentary": (
                "US large-cap is overweight by 8 percentage points. Rebalance toward international and bonds "
                "to reduce single-country concentration risk."
            ),
        },
        "retirement": {
            "current_age": 38,
            "retirement_age": 65,
            "current_balance": 184000,
            "target_balance": 1450000,
            "monthly_contribution": 920,
            "scenarios": [
                {"name": "Current path", "monthly": 920, "projected": 1230000, "verdict": "Short ~$220k"},
                {"name": "+ $200/mo", "monthly": 1120, "projected": 1402000, "verdict": "On track"},
                {"name": "+ $400/mo", "monthly": 1320, "projected": 1574000, "verdict": "Ahead"},
                {"name": "Max 401(k)", "monthly": 1958, "projected": 1948000, "verdict": "Exceeds target"},
            ],
            "commentary": (
                "Bumping the 401(k) deferral from 8% to 12% closes the gap and captures additional employer match "
                "if the plan allows. Run /finance-retirement to model spousal contributions."
            ),
        },
        "protection": {
            "items": [
                {"name": "Term Life Insurance", "status": "Good", "recommendation": "$1M policy in place — review every 3 years."},
                {"name": "Disability Insurance", "status": "Partial", "recommendation": "Employer LTD covers 60%. Consider supplemental own-occupation policy."},
                {"name": "Health Insurance", "status": "Good", "recommendation": "HDHP + HSA — max HSA contributions for triple tax benefit."},
                {"name": "Auto / Home", "status": "Good", "recommendation": "Umbrella liability of $1M is recommended given net worth."},
                {"name": "Will / Estate Plan", "status": "Missing", "recommendation": "CRITICAL — draft will, POA, and healthcare directive this quarter."},
                {"name": "Emergency Fund", "status": "Partial", "recommendation": "$11k of $24k target (4 months expenses). Build to 6 months."},
            ],
            "commentary": (
                "Missing estate documents are the single highest-impact protection gap. "
                "An online platform (e.g., trust & will services) can deliver a basic will + POA in under 60 minutes."
            ),
        },
        "action_items": [
            {"action": "Draft will, POA, and healthcare directive", "category": "Protection", "priority": "High", "impact": "Critical"},
            {"action": "Increase 401(k) deferral from 8% to 12%", "category": "Retirement", "priority": "High", "impact": "High"},
            {"action": "Throw $400/mo extra at Chase credit card (22% APR)", "category": "Debt", "priority": "High", "impact": "High"},
            {"action": "Build emergency fund from $11k to $24k", "category": "Cash Flow", "priority": "High", "impact": "High"},
            {"action": "Rebalance portfolio: trim US large-cap, add international", "category": "Investments", "priority": "Med", "impact": "Med"},
            {"action": "Max HSA contributions ($4,150 individual / $8,300 family)", "category": "Tax", "priority": "Med", "impact": "Med"},
            {"action": "Add $1M umbrella liability policy", "category": "Protection", "priority": "Med", "impact": "Med"},
            {"action": "Cancel 3 unused subscriptions (save ~$45/mo)", "category": "Cash Flow", "priority": "Low", "impact": "Low"},
            {"action": "Open Roth IRA for spouse (backdoor if needed)", "category": "Retirement", "priority": "Med", "impact": "Med"},
            {"action": "Set up automated 529 plan contributions ($200/mo)", "category": "Goals", "priority": "Low", "impact": "Med"},
        ],
        "ninety_day_plan": {
            "month_1": [
                "Open online will service account and complete will + POA",
                "Set up auto-transfer of $400/mo to credit card payoff",
                "Cancel 3 unused subscriptions",
                "Open HSA if not already open",
            ],
            "month_2": [
                "Increase 401(k) deferral to 12% via HR portal",
                "Rebalance brokerage to target allocation",
                "Apply for $1M umbrella liability policy",
                "Open spousal Roth IRA",
            ],
            "month_3": [
                "Auto-set $500/mo to emergency fund until $24k",
                "Set up 529 plan with $200/mo auto-contribution",
                "Apply for supplemental disability insurance",
                "Schedule annual review reminder",
            ],
            "after_90_days": (
                "Re-run /finance to see updated Financial Health Score. Most clients executing this plan "
                "move from B- to B+ or A- in 90 days."
            ),
        },
    }


# ---------------------------------------------------------------------------
# Document
# ---------------------------------------------------------------------------
def build_pdf(data: Dict[str, Any], output_path: str) -> None:
    styles = build_styles()

    doc = BaseDocTemplate(
        output_path,
        pagesize=LETTER,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
        title=f"Financial Plan — {data.get('client_name','Personal')}",
        author="AI Personal Finance Advisor",
        subject="Personal Financial Plan",
        creator="ai-finance-claude",
    )
    frame = Frame(
        MARGIN_L, MARGIN_B,
        PAGE_W - MARGIN_L - MARGIN_R,
        PAGE_H - MARGIN_T - MARGIN_B,
        id="content", showBoundary=0,
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=_draw_footer)])

    story: List[Any] = []
    build_cover(story, styles, data)
    build_score_dashboard(story, styles, data)
    build_cash_flow(story, styles, data)
    build_debt_summary(story, styles, data)
    build_investments(story, styles, data)
    build_retirement(story, styles, data)
    build_protection(story, styles, data)
    build_action_items(story, styles, data)
    build_90_day_plan(story, styles, data)

    doc.build(story)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Personal Financial Plan PDF (AI Personal Finance Advisor)."
    )
    parser.add_argument("--data", help="Path to a JSON file containing plan data.")
    parser.add_argument("--output", default="FINANCE-PLAN.pdf",
                        help="Output PDF path (default: FINANCE-PLAN.pdf).")
    parser.add_argument("--demo", action="store_true",
                        help="Generate a sample report with built-in demo data.")
    args = parser.parse_args()

    if not args.demo and not args.data:
        parser.error("Provide --data <path-to-json> or use --demo for a sample report.")

    if args.demo:
        data = _demo_data()
        if args.output == "FINANCE-PLAN.pdf":
            args.output = "FINANCE-PLAN-sample.pdf"
    else:
        try:
            with open(args.data, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            sys.stderr.write(f"ERROR reading --data file: {exc}\n")
            return 1

    out_dir = os.path.dirname(os.path.abspath(args.output))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    try:
        build_pdf(data, args.output)
    except Exception as exc:  # pragma: no cover
        sys.stderr.write(f"ERROR generating PDF: {exc}\n")
        return 2

    print(f"✓ Generated: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
