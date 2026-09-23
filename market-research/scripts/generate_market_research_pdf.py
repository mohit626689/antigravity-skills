#!/usr/bin/env python3
"""
Market Research Brief — Highly Engaging Executive PDF Builder
Features:
- Smart conditional page breaks (CondPageBreak): Never starts at bottom of page, fills blank space naturally.
- Visual Charts: Native ReportLab Pie Chart (Variety share) & Bar Chart (Top producing states).
- Visual KPI cards & highlighted key words/metrics.
- Styled badges & callout containers.
- Zero broken glyphs or black blocks.
- No preview folder generated.

Usage:
  python generate_market_research_pdf.py --input MARKET-RESEARCH-Topic.md --output MARKET-RESEARCH-Topic.pdf
"""

import os
import sys
import re
import argparse

# Try ReportLab imports, with fallback to local skill venv
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, CondPageBreak, KeepTogether, HRFlowable
    )
    from reportlab.pdfgen import canvas
    from reportlab.graphics.shapes import Drawing, String, Rect, Line, Group
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart
    from reportlab.graphics.charts.legends import Legend
except ImportError:
    venv_site = "/Users/shivpratap/.gemini/config/skills/reputation/.venv/lib/python3.11/site-packages"
    if os.path.exists(venv_site):
        sys.path.insert(0, venv_site)
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, CondPageBreak, KeepTogether, HRFlowable
        )
        from reportlab.pdfgen import canvas
        from reportlab.graphics.shapes import Drawing, String, Rect, Line, Group
        from reportlab.graphics.charts.piecharts import Pie
        from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart
        from reportlab.graphics.charts.legends import Legend
    else:
        print("Error: ReportLab is required. Run with python environment containing reportlab.")
        sys.exit(1)

# Executive Brand Color Palette
PRIMARY = colors.HexColor("#0F172A")        # Deep Slate 900
PRIMARY_MUTED = colors.HexColor("#334155")  # Slate 700
ACCENT = colors.HexColor("#2563EB")         # Royal Blue 600
ACCENT_LIGHT = colors.HexColor("#3B82F6")   # Blue 500
ACCENT_BG = colors.HexColor("#EFF6FF")      # Blue 50
EMERALD = colors.HexColor("#059669")        # Emerald 600
EMERALD_BG = colors.HexColor("#ECFDF5")     # Emerald 50
AMBER = colors.HexColor("#D97706")          # Amber 600
AMBER_BG = colors.HexColor("#FFFBEB")       # Amber 50
CRIMSON = colors.HexColor("#DC2626")        # Crimson 600
CRIMSON_BG = colors.HexColor("#FEF2F2")     # Red 50
PURPLE = colors.HexColor("#8B5CF6")         # Purple 500
BORDER_COLOR = colors.HexColor("#CBD5E1")   # Slate 300
LIGHT_BG = colors.HexColor("#F8FAFC")       # Slate 50
TEXT_MAIN = colors.HexColor("#1E293B")      # Slate 800
TEXT_MUTED = colors.HexColor("#64748B")     # Slate 500
WHITE = colors.white


class NumberedCanvas(canvas.Canvas):
    """Multi-pass canvas that calculates total page count and adds running headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        
        # Running Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "Market Research Brief — Strategic Business Intelligence")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "CONFIDENTIAL")
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
            
        # Running Footer (all pages)
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 34, footer_text)
        self.drawString(54, 34, "Antigravity Market Intelligence Engine — Strategic Business Planning")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(54, 44, 8.5 * inch - 54, 44)
        
        self.restoreState()


def clean_inline_markdown(text):
    """Sanitizes text, converts symbols into clean text badges, and highlights key terms."""
    if not text:
        return ""
        
    # Replace Rupee symbol
    text = text.replace('₹', 'Rs. ')
    
    # Replace box drawing characters
    text = text.replace('├─', '• ')
    text = text.replace('└─', '• ')
    text = text.replace('│', ' ')
    text = text.replace('─', '-')
    text = text.replace('┌', '+')
    text = text.replace('┐', '+')
    text = text.replace('┘', '+')
    text = text.replace('└', '+')
    text = text.replace('┬', '+')
    text = text.replace('┴', '+')
    text = text.replace('▼', 'v ')
    text = text.replace('▲', '^ ')
    text = text.replace('►', '> ')
    text = text.replace('◄', '< ')
    text = text.replace('■', '')
    
    # High-impact decision badges & verification tags
    text = text.replace('[VERIFIED DATA 🟢]', '<font color="#059669"><b>[VERIFIED DATA]</b></font>')
    text = text.replace('[MODEL ESTIMATE 🟣]', '<font color="#7C3AED"><b>[MODEL ESTIMATE]</b></font>')
    text = text.replace('[STRONG GO 🟢]', '<font color="#059669"><b>[STRONG GO]</b></font>')
    text = text.replace('[GO WITH PIVOT 🟡]', '<font color="#D97706"><b>[GO WITH PIVOT]</b></font>')
    text = text.replace('[NO-GO 🔴]', '<font color="#DC2626"><b>[NO-GO / HIGH RISK]</b></font>')
    text = text.replace('🟣', '<font color="#7C3AED"><b>[ESTIMATE]</b></font> ')
    text = text.replace('🎯', '<font color="#2563EB"><b>[TARGET]</b></font> ')

    # Convert emojis to professional styled badges
    text = text.replace('🔴', '<font color="#DC2626"><b>[CRITICAL]</b></font> ')
    text = text.replace('🟡', '<font color="#D97706"><b>[HIGH]</b></font> ')
    text = text.replace('🟢', '<font color="#059669"><b>[MODERATE]</b></font> ')
    text = text.replace('⭐', '<font color="#2563EB"><b>[RECOMMENDED]</b></font> ')
    text = text.replace('💡', '<font color="#D97706"><b>[OPPORTUNITY]</b></font> ')
    text = text.replace('🔷', '<font color="#2563EB"><b>[FOCUS]</b></font> ')
    text = text.replace('✅', '<font color="#059669"><b>[VERIFIED]</b></font> ')
    text = text.replace('⚠️', '<font color="#DC2626"><b>[ALERT]</b></font> ')
    text = text.replace('📍', '<font color="#2563EB"><b>[LOCATION]</b></font> ')
    text = text.replace('📊', '<font color="#2563EB"><b>[DATA]</b></font> ')
    text = text.replace('💰', '<font color="#059669"><b>[ECONOMICS]</b></font> ')
    text = text.replace('🍄', '')
    
    # XML entity escaping
    text = text.replace('&', '&amp;')
    text = text.replace('&amp;amp;', '&amp;')
    text = text.replace('<br/>', '###BR###').replace('<br>', '###BR###')
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    text = text.replace('###BR###', '<br/>')
    
    # Re-enable allowed HTML tags for font/bold
    text = re.sub(r'&lt;font(.*?)&gt;', r'<font\1>', text)
    text = text.replace('&lt;/font&gt;', '</font>')
    text = re.sub(r'&lt;b&gt;(.*?)&lt;/b&gt;', r'<b>\1</b>', text)
    text = re.sub(r'&lt;i&gt;(.*?)&lt;/i&gt;', r'<i>\1</i>', text)
    
    # Markdown bold, italic, code, links
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.*?)`', r'<font face="Courier" color="#0F172A"><b>\1</b></font>', text)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<font color="#2563EB"><u>\1</u></font>', text)
    
    return text


def create_kpi_card_table():
    """Builds a top-level 4-card KPI highlight banner."""
    card_data = [
        [
            Paragraph("<b>TOTAL MARKET (TAM)</b><br/><font size=12 color='#2563EB'><b>$1.61 Billion</b></font><br/><font size=7 color='#64748B'>Rs. 13,400 Crore Pan-India</font>", ParagraphStyle('KPI1', fontName='Helvetica', fontSize=8, leading=11, alignment=1)),
            Paragraph("<b>ANNUAL PRODUCTION</b><br/><font size=12 color='#059669'><b>400,000 MT</b></font><br/><font size=7 color='#64748B'>7x Expansion since 2015</font>", ParagraphStyle('KPI2', fontName='Helvetica', fontSize=8, leading=11, alignment=1)),
            Paragraph("<b>PROJECTED CAGR</b><br/><font size=12 color='#D97706'><b>11.4% CAGR</b></font><br/><font size=7 color='#64748B'>Forecast through 2033</font>", ParagraphStyle('KPI3', fontName='Helvetica', fontSize=8, leading=11, alignment=1)),
            Paragraph("<b>GOVT CAPITAL SUBSIDY</b><br/><font size=12 color='#8B5CF6'><b>35% – 50%</b></font><br/><font size=7 color='#64748B'>NHB / MIDH / PMFME</font>", ParagraphStyle('KPI4', fontName='Helvetica', fontSize=8, leading=11, alignment=1)),
        ]
    ]
    t = Table(card_data, colWidths=[126, 126, 126, 126])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), ACCENT_BG),
        ('BACKGROUND', (1, 0), (1, 0), EMERALD_BG),
        ('BACKGROUND', (2, 0), (2, 0), AMBER_BG),
        ('BACKGROUND', (3, 0), (3, 0), colors.HexColor("#F5F3FF")),
        ('BOX', (0, 0), (0, 0), 1, ACCENT),
        ('BOX', (1, 0), (1, 0), 1, EMERALD),
        ('BOX', (2, 0), (2, 0), 1, AMBER),
        ('BOX', (3, 0), (3, 0), 1, PURPLE),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t


def create_state_volume_bar_chart():
    """Generates native ReportLab bar chart of top producing states in India."""
    d = Drawing(504, 135)
    # Container box
    d.add(Rect(0, 0, 504, 135, fillColor=LIGHT_BG, strokeColor=BORDER_COLOR, strokeWidth=0.5, rx=5, ry=5))
    d.add(String(16, 118, "TOP PRODUCING STATES IN INDIA (ANNUAL YIELD IN 000s METRIC TONNES)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=PRIMARY))
    
    bc = VerticalBarChart()
    bc.x = 35
    bc.y = 22
    bc.height = 80
    bc.width = 440
    bc.data = [[42.2, 34.6, 28.0, 24.5, 21.0, 18.5]]
    bc.categoryAxis.categoryNames = ["Bihar (#1)", "Odisha (#2)", "Maharashtra", "Haryana", "Punjab", "MP (Emerging)"]
    bc.categoryAxis.labels.fontName = "Helvetica-Bold"
    bc.categoryAxis.labels.fontSize = 7.5
    bc.categoryAxis.labels.fillColor = PRIMARY_MUTED
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 50
    bc.valueAxis.valueStep = 10
    bc.valueAxis.labels.fontName = "Helvetica"
    bc.valueAxis.labels.fontSize = 7
    bc.valueAxis.labels.fillColor = TEXT_MUTED
    bc.bars[0].fillColor = ACCENT
    d.add(bc)
    return d


def create_variety_pie_chart():
    """Generates native ReportLab pie chart of mushroom variety market share."""
    d = Drawing(504, 135)
    d.add(Rect(0, 0, 504, 135, fillColor=LIGHT_BG, strokeColor=BORDER_COLOR, strokeWidth=0.5, rx=5, ry=5))
    d.add(String(16, 118, "COMMERCIAL VARIETY PRODUCTION SHARE IN INDIA (% VOLUME)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=PRIMARY))
    
    pc = Pie()
    pc.x = 35
    pc.y = 10
    pc.width = 100
    pc.height = 100
    pc.data = [72, 18, 5, 3, 2]
    pc.labels = ["72%", "18%", "5%", "3%", "2%"]
    pc.slices.strokeWidth = 0.5
    pc.slices[0].fillColor = ACCENT
    pc.slices[1].fillColor = EMERALD
    pc.slices[2].fillColor = AMBER
    pc.slices[3].fillColor = PURPLE
    pc.slices[4].fillColor = colors.HexColor("#EC4899")
    d.add(pc)
    
    leg = Legend()
    leg.x = 185
    leg.y = 102
    leg.dx = 8
    leg.dy = 8
    leg.fontName = "Helvetica"
    leg.fontSize = 8
    leg.boxAnchor = "nw"
    leg.columnMaximum = 5
    leg.colorNamePairs = [
        (ACCENT, "White Button Mushroom (72%) — Primary commercial volume"),
        (EMERALD, "Oyster / Dhingri (18%) — Low cost, easiest for beginners"),
        (AMBER, "Paddy Straw (5%) — Humid monsoon coastal crop (Odisha/WB)"),
        (PURPLE, "Milky Mushroom (3%) — Summer heat tolerant, 5-day shelf life"),
        (colors.HexColor("#EC4899"), "Exotic & Cordyceps (2%) — Ultra high-margin medicinal niche"),
    ]
    d.add(leg)
    return d


def create_price_comparison_chart():
    """Generates native ReportLab horizontal bar chart comparing channel realizations."""
    d = Drawing(504, 130)
    d.add(Rect(0, 0, 504, 130, fillColor=LIGHT_BG, strokeColor=BORDER_COLOR, strokeWidth=0.5, rx=5, ry=5))
    d.add(String(16, 114, "VALUE REALIZATION PER KG ACROSS DISTRIBUTION CHANNELS (IN RS.)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=PRIMARY))
    
    hc = HorizontalBarChart()
    hc.x = 135
    hc.y = 16
    hc.height = 82
    hc.width = 345
    # Values: Wholesale Mandi, HoReCa, Packaged Retail, Dehydrated Powder
    hc.data = [[110, 145, 250, 1100]]
    hc.categoryAxis.categoryNames = ["Mandi Bulk", "HoReCa B2B", "Retail 200g", "Dry Powder"]
    hc.categoryAxis.labels.fontName = "Helvetica-Bold"
    hc.categoryAxis.labels.fontSize = 7.5
    hc.categoryAxis.labels.fillColor = PRIMARY_MUTED
    hc.valueAxis.valueMin = 0
    hc.valueAxis.valueMax = 1200
    hc.valueAxis.valueStep = 300
    hc.valueAxis.labels.fontName = "Helvetica"
    hc.valueAxis.labels.fontSize = 7
    hc.valueAxis.labels.fillColor = TEXT_MUTED
    hc.bars[0].fillColor = EMERALD
    d.add(hc)
    return d


def build_market_research_pdf(markdown_content, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Hierarchy
    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=8
    )

    style_h2 = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=0,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h3 = ParagraphStyle(
        'SectionH3',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=PRIMARY_MUTED,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    style_h4 = ParagraphStyle(
        'SectionH4',
        parent=styles['Heading4'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=ACCENT,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'MainBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=TEXT_MAIN,
        spaceAfter=5
    )

    style_bullet = ParagraphStyle(
        'ListBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_MAIN,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5
    )

    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=PRIMARY
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=WHITE
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.5,
        textColor=TEXT_MAIN
    )

    style_meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=PRIMARY_MUTED
    )

    style_meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT_MAIN
    )

    story = []
    lines = markdown_content.split('\n')
    i = 0
    num_lines = len(lines)

    table_buffer = []

    def flush_table():
        nonlocal table_buffer, story
        if not table_buffer:
            return
        
        raw_rows = []
        for r in table_buffer:
            cells = [c.strip() for c in r.strip('|').split('|')]
            if all(re.match(r'^:?-+:?$', c) for c in cells if c):
                continue
            if any(cells):
                raw_rows.append(cells)
        
        table_buffer = []
        if not raw_rows:
            return
        
        num_cols = max(len(row) for row in raw_rows)
        normalized_rows = []
        for row in raw_rows:
            if len(row) < num_cols:
                row.extend([''] * (num_cols - len(row)))
            normalized_rows.append(row[:num_cols])
            
        total_width = 504
        is_scorecard = any("Audit Dimension" in c or "Audit Criteria" in c for c in raw_rows[0])
        if is_scorecard and num_cols == 4:
            col_widths = [135, 75, 215, 79]
        elif num_cols == 3:
            col_widths = [130, 160, 214]
        elif num_cols == 4:
            col_widths = [130, 115, 159, 100]
        elif num_cols == 5:
            col_widths = [100, 75, 95, 114, 120]
        elif num_cols == 6:
            col_widths = [85, 75, 75, 75, 74, 120]
        else:
            col_widths = [total_width / num_cols] * num_cols
        
        table_data = []
        for row_idx, row in enumerate(normalized_rows):
            row_data = []
            is_header = (row_idx == 0)
            for cell in row:
                formatted = clean_inline_markdown(cell)
                if is_header:
                    p = Paragraph(f"<b>{formatted}</b>", style_table_header)
                else:
                    p = Paragraph(formatted, style_table_cell)
                row_data.append(p)
            table_data.append(row_data)

        t_style = [
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ]
        
        for r_i in range(1, len(table_data)):
            is_composite = any("Composite" in str(c) for c in normalized_rows[r_i])
            if is_composite:
                t_style.append(('BACKGROUND', (0, r_i), (-1, r_i), ACCENT_BG))
                t_style.append(('BOX', (0, r_i), (-1, r_i), 1.5, ACCENT))
            else:
                bg = LIGHT_BG if r_i % 2 == 1 else WHITE
                t_style.append(('BACKGROUND', (0, r_i), (-1, r_i), bg))

        t = Table(table_data, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle(t_style))
        story.append(Spacer(1, 2))
        story.append(t)
        story.append(Spacer(1, 5))

    added_kpi = False
    added_state_chart = False
    added_variety_chart = False
    added_price_chart = False

    while i < num_lines:
        line = lines[i].rstrip()
        clean = line.strip()

        # Check for table rows
        if clean.startswith('|') and clean.endswith('|'):
            table_buffer.append(clean)
            i += 1
            continue
        elif table_buffer:
            flush_table()

        # Skip empty lines
        if not clean:
            i += 1
            continue

        # Skip code blocks
        if clean.startswith('```'):
            i += 1
            while i < num_lines and not lines[i].strip().startswith('```'):
                i += 1
            if i < num_lines and lines[i].strip().startswith('```'):
                i += 1
            continue

        # Document Title (# Title)
        if clean.startswith('# '):
            title_text = clean[2:].strip()
            story.append(Spacer(1, 4))
            story.append(Paragraph(clean_inline_markdown(title_text), style_title))
            story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceBefore=2, spaceAfter=8))
            i += 1
            continue

        # Metadata block parsing (**Prepared For:**, **Date:**, etc.)
        if clean.startswith('**Prepared For:**') or clean.startswith('**Prepared By:**') or clean.startswith('**Date:**') or clean.startswith('**Target Location'):
            meta_rows = []
            while i < num_lines and ('**' in lines[i] and ':' in lines[i]):
                m_line = lines[i].strip()
                if not m_line:
                    i += 1
                    continue
                match = re.match(r'\*\*(.*?):\*\*\s*(.*)', m_line)
                if match:
                    label = match.group(1).strip()
                    val = clean_inline_markdown(match.group(2).strip())
                    meta_rows.append([
                        Paragraph(f"{label}:", style_meta_label),
                        Paragraph(val, style_meta_val)
                    ])
                else:
                    break
                i += 1
            
            if meta_rows:
                meta_table = Table(meta_rows, colWidths=[130, 374])
                meta_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
                    ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ]))
                story.append(meta_table)
                story.append(Spacer(1, 6))

                # Inject visual KPI cards right below metadata
                if not added_kpi:
                    story.append(create_kpi_card_table())
                    story.append(Spacer(1, 8))
                    added_kpi = True
            continue

        # Major Headings (## 1. Executive Summary, ## 2. Location Analysis, etc.)
        if clean.startswith('## '):
            h2_text = clean[3:].strip()
            
            # Smart Conditional Page Break:
            # If less than 165 points (~2.3 inches) left on the page, break to top of next page!
            # Otherwise continue on same page, filling blank space naturally.
            story.append(CondPageBreak(165))
            story.append(Spacer(1, 6))

            # Styled Banner Heading
            header_table = Table([[
                Paragraph(f"<b>{clean_inline_markdown(h2_text).upper()}</b>", ParagraphStyle(
                    'BannerH2', fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=WHITE
                ))
            ]], colWidths=[504])
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(header_table)
            story.append(Spacer(1, 6))
            i += 1

            # Contextual Chart Injection:
            # Inject State Volume Bar Chart under Section 2
            if "Location-Specific Advantage" in h2_text and not added_state_chart:
                story.append(Spacer(1, 2))
                story.append(create_state_volume_bar_chart())
                story.append(Spacer(1, 6))
                added_state_chart = True

            # Inject Variety Pie Chart under Section 4
            if "Product Varietal Breakdown" in h2_text and not added_variety_chart:
                story.append(Spacer(1, 2))
                story.append(create_variety_pie_chart())
                story.append(Spacer(1, 6))
                added_variety_chart = True

            # Inject Price Comparison Chart under Section 8
            if "Financial Model" in h2_text and not added_price_chart:
                story.append(Spacer(1, 2))
                story.append(create_price_comparison_chart())
                story.append(Spacer(1, 6))
                added_price_chart = True

            continue

        # Executive Decision Verdict Callout Box
        if clean.startswith('### Executive Decision Verdict'):
            h3_text = clean[4:].strip()
            story.append(CondPageBreak(120))
            story.append(Spacer(1, 4))
            story.append(Paragraph(clean_inline_markdown(h3_text), style_h3))
            i += 1
            verdict_items = []
            while i < num_lines:
                v_line = lines[i].strip()
                if not v_line:
                    i += 1
                    continue
                if v_line.startswith('#') or v_line in ['---', '***', '___'] or v_line.startswith('|'):
                    break
                v_clean = re.sub(r'^[-*]\s+', '', v_line)
                verdict_items.append(clean_inline_markdown(v_clean))
                i += 1
            
            if verdict_items:
                full_v = " ".join(verdict_items)
                if "STRONG GO" in full_v:
                    box_bg = colors.HexColor("#ECFDF5")
                    box_border = EMERALD
                    tag_title = "EXECUTIVE STRATEGIC VERDICT: STRONG GO"
                elif "NO-GO" in full_v:
                    box_bg = colors.HexColor("#FEF2F2")
                    box_border = colors.HexColor("#DC2626")
                    tag_title = "EXECUTIVE STRATEGIC VERDICT: NO-GO / HIGH RISK"
                else:
                    box_bg = colors.HexColor("#FFFBEB")
                    box_border = AMBER
                    tag_title = "EXECUTIVE STRATEGIC VERDICT: RECOMMENDED PIVOT"

                v_flowables = [
                    Paragraph(f"<b><font color='{box_border.hexval()}'>{tag_title}</font></b>", ParagraphStyle('VTitle', fontName='Helvetica-Bold', fontSize=10, leading=13)),
                    Spacer(1, 4)
                ]
                for item in verdict_items:
                    v_flowables.append(Paragraph(f"• &nbsp; {item}", style_body))
                    v_flowables.append(Spacer(1, 2))
                
                v_table = Table([[v_flowables]], colWidths=[504])
                v_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), box_bg),
                    ('BOX', (0, 0), (-1, -1), 1.5, box_border),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                story.append(v_table)
                story.append(Spacer(1, 6))
            continue

        # Sub-Headings (### Title)
        if clean.startswith('### '):
            h3_text = clean[4:].strip()
            story.append(CondPageBreak(90))
            story.append(Spacer(1, 3))
            story.append(Paragraph(clean_inline_markdown(h3_text), style_h3))
            i += 1
            continue


        # Sub-sub-headings (#### Title)
        if clean.startswith('#### '):
            h4_text = clean[5:].strip()
            story.append(Spacer(1, 2))
            story.append(Paragraph(clean_inline_markdown(h4_text), style_h4))
            i += 1
            continue

        # Horizontal Rule
        if clean in ['---', '***', '___']:
            story.append(Spacer(1, 2))
            story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=2, spaceAfter=4))
            i += 1
            continue

        # Executive Callout / Blockquote
        if clean.startswith('> ') or clean.startswith('>'):
            quote_lines = []
            while i < num_lines and (lines[i].strip().startswith('> ') or lines[i].strip().startswith('>')):
                q_line = re.sub(r'^>\s?', '', lines[i].strip())
                if q_line:
                    quote_lines.append(clean_inline_markdown(q_line))
                i += 1
            quote_text = "<br/>".join(quote_lines)
            callout_cell = [
                Paragraph(f"<b>STRATEGIC EXECUTIVE SUMMARY:</b><br/>{quote_text}", style_callout)
            ]
            callout_table = Table([[callout_cell]], colWidths=[504])
            callout_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), ACCENT_BG),
                ('BOX', (0, 0), (-1, -1), 1, ACCENT),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            story.append(Spacer(1, 3))
            story.append(callout_table)
            story.append(Spacer(1, 5))
            continue

        # Bullet List Items (- or *)
        if clean.startswith('- ') or clean.startswith('* '):
            item_text = clean[2:].strip()
            formatted = clean_inline_markdown(item_text)
            p = Paragraph(f"• &nbsp; {formatted}", style_bullet)
            story.append(p)
            i += 1
            continue

        # Numbered List Items
        num_match = re.match(r'^(\d+)\.\s+(.*)', clean)
        if num_match:
            num = num_match.group(1)
            item_text = clean_inline_markdown(num_match.group(2).strip())
            p = Paragraph(f"<b>{num}.</b> &nbsp; {item_text}", style_bullet)
            story.append(p)
            i += 1
            continue

        # Standard Paragraph
        formatted = clean_inline_markdown(clean)
        story.append(Paragraph(formatted, style_body))
        i += 1

    if table_buffer:
        flush_table()

    # Build PDF using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ Market Research PDF successfully compiled: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Compile Market Research Brief Markdown into Executive PDF")
    parser.add_argument("--input", "-i", required=True, help="Path to input Markdown file")
    parser.add_argument("--output", "-o", required=True, help="Path to output PDF file")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()

    build_market_research_pdf(content, args.output)


if __name__ == "__main__":
    main()
