#!/usr/bin/env python3
"""
Company Research Dossier — Executive PDF Builder
Compiles markdown company research profiles into publication-grade, executive PDF deliverables.

Usage:
  python generate_company_research_pdf.py --input COMPANY-RESEARCH-Company.md --output COMPANY-RESEARCH-Company.pdf
"""

import os
import sys
import re
import argparse

# ReportLab imports with graceful error reporting
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
    )
    from reportlab.pdfgen import canvas
except Exception:
    venv_site = "/Users/shivpratap/.gemini/config/skills/reputation/.venv/lib/python3.11/site-packages"
    if os.path.exists(venv_site):
        sys.path.insert(0, venv_site)
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
        )
        from reportlab.pdfgen import canvas
    except Exception as e:
        print("Note: ReportLab is required to build executive PDF documents.")
        print("Install it with: pip install reportlab")
        print(f"Details: {e}")
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
            self.drawString(54, 11 * inch - 36, "Company Research Dossier — Executive Intelligence Brief")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "CONFIDENTIAL")
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
            
        # Running Footer (all pages)
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, footer_text)
        self.drawString(54, 36, "Antigravity Intelligence System — Due Diligence & Strategic Preparation")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * inch - 54, 46)
        
        self.restoreState()


def clean_inline_markdown(text):
    """Converts standard markdown bold, italic, and code formatting to ReportLab XML tags."""
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.*?)`', r'<font face="Courier" color="#0F172A"><b>\1</b></font>', text)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<font color="#2563EB"><u>\1</u></font>', text)

    # Verification Badges (Rakhim Ford Protocol)
    text = re.sub(r'🟢\s*(?:<font[^>]*><b>)?\[VERIFIED FACT\](?:</b></font>)?', r'<font color="#059669"><b>[VERIFIED FACT]</b></font>', text, flags=re.IGNORECASE)
    text = re.sub(r'🟢\s*(?:<font[^>]*><b>)?\[CONFIRMED\](?:</b></font>)?', r'<font color="#059669"><b>[CONFIRMED]</b></font>', text, flags=re.IGNORECASE)
    text = re.sub(r'🟡\s*(?:<font[^>]*><b>)?\[HIGH CONFIDENCE(?: PATTERN)?\](?:</b></font>)?', r'<font color="#D97706"><b>[HIGH CONFIDENCE]</b></font>', text, flags=re.IGNORECASE)
    text = re.sub(r'🟣\s*(?:<font[^>]*><b>)?\[AI HYPOTHESIS(?: / TO VALIDATE)?\](?:</b></font>)?', r'<font color="#7E22CE"><b>[AI HYPOTHESIS]</b></font>', text, flags=re.IGNORECASE)
    text = re.sub(r'🔴\s*(?:<font[^>]*><b>)?\[DEBUNKED(?: / REVISED)?\](?:</b></font>)?', r'<font color="#DC2626"><b>[REVISED]</b></font>', text, flags=re.IGNORECASE)

    return text


def build_company_research_pdf(markdown_content, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Hierarchy
    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=12
    )

    style_h2 = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    style_h3 = ParagraphStyle(
        'SectionH3',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=PRIMARY_MUTED,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'MainBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=TEXT_MAIN,
        spaceAfter=6
    )

    style_bullet = ParagraphStyle(
        'ListBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=TEXT_MAIN,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    style_meta = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY_MUTED
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=WHITE
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT_MAIN
    )

    story = []

    lines = markdown_content.split('\n')
    i = 0
    in_table = False
    table_lines = []

    def flush_table(tbl_lines):
        if not tbl_lines:
            return None
        rows_data = []
        is_header = True
        for line in tbl_lines:
            if re.match(r'^\s*\|?\s*[-:]+\s*\|', line):
                continue  # Divider row
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            formatted_row = []
            for cell in cells:
                cleaned = clean_inline_markdown(cell)
                if is_header:
                    formatted_row.append(Paragraph(cleaned, style_table_header))
                else:
                    formatted_row.append(Paragraph(cleaned, style_table_cell))
            if formatted_row:
                rows_data.append(formatted_row)
                is_header = False

        if not rows_data:
            return None

        # Build Table
        col_count = len(rows_data[0])
        col_width = (8.5 * 72 - 108) / col_count
        t = Table(rows_data, colWidths=[col_width] * col_count)
        t_style = [
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]
        for r in range(1, len(rows_data)):
            bg = LIGHT_BG if r % 2 == 1 else WHITE
            t_style.append(('BACKGROUND', (0, r), (-1, r), bg))

        t.setStyle(TableStyle(t_style))
        return t

    while i < len(lines):
        line = lines[i]

        # Table detection
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            in_table = True
            table_lines.append(line)
            i += 1
            continue
        elif in_table:
            t = flush_table(table_lines)
            if t:
                story.append(t)
                story.append(Spacer(1, 8))
            in_table = False
            table_lines = []

        stripped = line.strip()

        # Empty lines
        if not stripped:
            i += 1
            continue

        # Horizontal Rule
        if stripped in ('---', '***', '___'):
            story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceAfter=8, spaceBefore=8))
            i += 1
            continue

        # Document Title (# H1)
        if stripped.startswith('# '):
            title_text = clean_inline_markdown(stripped[2:])
            badge = Table(
                [[Paragraph(f'<font color="#2563EB"><b>ANTIGRAVITY INTELLIGENCE DOSSIER</b></font>', style_meta)]],
                colWidths=[8.5 * 72 - 108]
            )
            badge.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), ACCENT_BG),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#BFDBFE")),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(badge)
            story.append(Spacer(1, 10))
            story.append(Paragraph(title_text, style_title))
            i += 1
            continue

        # Section Header (## H2)
        if stripped.startswith('## '):
            h2_text = clean_inline_markdown(stripped[3:])
            story.append(Paragraph(h2_text, style_h2))
            i += 1
            continue

        # Subsection (### H3)
        if stripped.startswith('### '):
            h3_text = clean_inline_markdown(stripped[4:])
            story.append(Paragraph(h3_text, style_h3))
            i += 1
            continue

        # Metadata Lines (**Key:** Value)
        if stripped.startswith('**') and ':' in stripped and not stripped.startswith('**['):
            meta_clean = clean_inline_markdown(stripped)
            story.append(Paragraph(meta_clean, style_meta))
            i += 1
            continue

        # Blockquote / Alert Callout
        if stripped.startswith('>'):
            quote_text = re.sub(r'^>\s*(\[!.*?\])?\s*', '', stripped)
            if quote_text:
                q_clean = clean_inline_markdown(quote_text)
                callout_table = Table(
                    [[Paragraph(f'<b>EXECUTIVE NOTE:</b> {q_clean}', style_meta)]],
                    colWidths=[8.5 * 72 - 108]
                )
                callout_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), AMBER_BG),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#FCD34D")),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))
                story.append(callout_table)
                story.append(Spacer(1, 6))
            i += 1
            continue

        # Bullets / Lists
        if stripped.startswith(('- ', '* ')) or re.match(r'^\d+\.\s', stripped):
            bullet_body = re.sub(r'^(-|\*|\d+\.)\s+', '', stripped)
            bullet_clean = clean_inline_markdown(bullet_body)
            story.append(Paragraph(f"• {bullet_clean}", style_bullet))
            i += 1
            continue

        # Regular Paragraphs
        p_clean = clean_inline_markdown(stripped)
        story.append(Paragraph(p_clean, style_body))
        i += 1

    # Flush any remaining table
    if in_table and table_lines:
        t = flush_table(table_lines)
        if t:
            story.append(t)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ Successfully compiled Company Research PDF: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Compile Company Research markdown into Executive PDF.")
    parser.add_argument("--input", required=True, help="Path to input markdown file")
    parser.add_argument("--output", required=True, help="Path to output PDF file")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()

    build_company_research_pdf(content, args.output)


if __name__ == "__main__":
    main()
