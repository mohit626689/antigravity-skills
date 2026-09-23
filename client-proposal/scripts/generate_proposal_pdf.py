#!/usr/bin/env python3
"""
Client Proposal Generator — Executive PDF Builder
Compiles markdown or JSON proposals into high-converting, professional PDF deliverables.

Usage:
  python generate_proposal_pdf.py --input PROPOSAL-Client.md --output PROPOSAL-Client.pdf
"""

import os
import sys
import re
import argparse

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
    )
    from reportlab.pdfgen import canvas
except ImportError:
    venv_site = "/Users/shivpratap/.gemini/config/skills/reputation/.venv/lib/python3.11/site-packages"
    if os.path.exists(venv_site):
        sys.path.insert(0, venv_site)
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
        )
        from reportlab.pdfgen import canvas
    else:
        print("Error: ReportLab is required. Run with the reputation venv or run 'pip install reportlab'.")
        sys.exit(1)

try:
    import pymupdf
except ImportError:
    venv_site = "/Users/shivpratap/.gemini/config/skills/reputation/.venv/lib/python3.11/site-packages"
    if os.path.exists(venv_site):
        sys.path.insert(0, venv_site)
        try:
            import pymupdf
        except ImportError:
            pymupdf = None
    else:
        pymupdf = None

# Brand Color Palette (ShivWork / Modern Executive)
PRIMARY = colors.HexColor("#0F172A")       # Slate 900
PRIMARY_MUTED = colors.HexColor("#334155") # Slate 700
ACCENT = colors.HexColor("#0284C7")        # Sky 600
ACCENT_BG = colors.HexColor("#F0F9FF")     # Sky 50
EMERALD = colors.HexColor("#059669")       # Emerald 600
EMERALD_BG = colors.HexColor("#ECFDF5")    # Emerald 50
BORDER_COLOR = colors.HexColor("#CBD5E1")  # Slate 300
LIGHT_BG = colors.HexColor("#F8FAFC")      # Slate 50
TEXT_MAIN = colors.HexColor("#1E293B")     # Slate 800
TEXT_MUTED = colors.HexColor("#64748B")    # Slate 500
WHITE = colors.white

class NumberedCanvas(canvas.Canvas):
    """Canvas that adds page numbers and running footer during multi-pass rendering."""
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
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "Client Proposal — Confidential")
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
            
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, footer_text)
        self.drawString(54, 36, "Prepared with ShivWork Client Proposal Engine")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * inch - 54, 46)
        self.restoreState()


def clean_inline_markdown(text):
    """Convert common markdown bold/italic/links to reportlab HTML tags."""
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__([^_]+)__', r'<b>\1</b>', text)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    text = re.sub(r'_([^_]+)_', r'<i>\1</i>', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<font face="Courier">\1</font>', text)
    return text


def build_pdf_from_markdown(md_content, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=14
    )
    
    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=TEXT_MAIN,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=16,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    callout_style = ParagraphStyle(
        'Callout',
        parent=body_style,
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=PRIMARY_MUTED
    )
    
    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=body_style,
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=PRIMARY_MUTED
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=body_style,
        fontSize=8.5,
        leading=11,
        spaceAfter=0
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=body_style,
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=PRIMARY,
        spaceAfter=0
    )

    story = []
    lines = md_content.split('\n')
    i = 0
    in_meta_header = True
    meta_rows = []
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
            
        # Top Title
        if line.startswith('# '):
            title_text = clean_inline_markdown(line[2:].strip())
            story.append(Paragraph(title_text, title_style))
            i += 1
            continue
            
        # Metadata block: **Key:** Value
        if in_meta_header and line.startswith('**') and ':' in line:
            m = re.match(r'\*\*([^*]+):\*\*\s*(.*)', line)
            if m:
                k, v = m.group(1).strip(), clean_inline_markdown(m.group(2).strip())
                meta_rows.append([Paragraph(f"<b>{k}:</b>", meta_label), Paragraph(v, body_style)])
                i += 1
                continue
        else:
            if meta_rows and in_meta_header:
                # Flush meta table
                meta_table = Table(meta_rows, colWidths=[110, 394])
                meta_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
                    ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('LEFTPADDING', (0,0), (-1,-1), 10),
                    ('RIGHTPADDING', (0,0), (-1,-1), 10),
                ]))
                story.append(meta_table)
                story.append(Spacer(1, 14))
                meta_rows = []
                in_meta_header = False

        if line.startswith('---'):
            if meta_rows:
                meta_table = Table(meta_rows, colWidths=[110, 394])
                meta_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
                    ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('LEFTPADDING', (0,0), (-1,-1), 10),
                    ('RIGHTPADDING', (0,0), (-1,-1), 10),
                ]))
                story.append(meta_table)
                story.append(Spacer(1, 14))
                meta_rows = []
                in_meta_header = False
            story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceBefore=10, spaceAfter=12))
            i += 1
            continue

        # Headings
        if line.startswith('## '):
            heading_text = clean_inline_markdown(line[3:].strip())
            story.append(Paragraph(heading_text, h1_style))
            i += 1
            continue
            
        if line.startswith('### '):
            heading_text = clean_inline_markdown(line[4:].strip())
            story.append(Paragraph(heading_text, h2_style))
            i += 1
            continue

        if line.startswith('#### '):
            heading_text = clean_inline_markdown(line[5:].strip())
            story.append(Paragraph(heading_text, h2_style))
            i += 1
            continue

        # Markdown Table Detection
        if line.startswith('|') and '|' in line[1:]:
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
                
            if len(table_lines) >= 2:
                headers = [c.strip() for c in table_lines[0].split('|')[1:-1]]
                data_rows = []
                for row_line in table_lines[2:]: # skip separator
                    cols = [c.strip() for c in row_line.split('|')[1:-1]]
                    if len(cols) == len(headers):
                        data_rows.append(cols)
                    elif len(cols) < len(headers):
                        cols += [''] * (len(headers) - len(cols))
                        data_rows.append(cols)
                    else:
                        data_rows.append(cols[:len(headers)])
                
                num_cols = len(headers)
                avail_width = 504
                col_width = avail_width / num_cols
                
                table_data = []
                table_data.append([Paragraph(clean_inline_markdown(h), table_cell_bold) for h in headers])
                for r in data_rows:
                    table_data.append([Paragraph(clean_inline_markdown(cell), table_cell) for cell in r])
                    
                t = Table(table_data, colWidths=[col_width]*num_cols)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
                    ('TEXTCOLOR', (0,0), (-1,0), PRIMARY),
                    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('TOPPADDING', (0,0), (-1,-1), 5),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                    ('LEFTPADDING', (0,0), (-1,-1), 6),
                    ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ]))
                story.append(Spacer(1, 4))
                story.append(t)
                story.append(Spacer(1, 8))
                continue
            else:
                i += 1
                continue

        # Blockquotes / Callout boxes
        if line.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            quote_text = clean_inline_markdown(" ".join(quote_lines))
            callout_p = Paragraph(quote_text, callout_style)
            callout_t = Table([[callout_p]], colWidths=[504])
            callout_t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), ACCENT_BG),
                ('LEFTPADDING', (0,0), (-1,-1), 14),
                ('RIGHTPADDING', (0,0), (-1,-1), 12),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('BOX', (0,0), (-1,-1), 1, ACCENT),
            ]))
            story.append(Spacer(1, 4))
            story.append(callout_t)
            story.append(Spacer(1, 8))
            continue

        # Bullet lists
        if line.startswith('- ') or line.startswith('* '):
            bullet_text = clean_inline_markdown(line[2:].strip())
            story.append(Paragraph(f"• {bullet_text}", bullet_style))
            i += 1
            continue
            
        # Numbered lists
        m_num = re.match(r'^(\d+)\.\s+(.*)', line)
        if m_num:
            num_idx = m_num.group(1)
            num_text = clean_inline_markdown(m_num.group(2).strip())
            story.append(Paragraph(f"<b>{num_idx}.</b> {num_text}", bullet_style))
            i += 1
            continue

        # Standard Paragraph
        para_text = clean_inline_markdown(line)
        story.append(Paragraph(para_text, body_style))
        i += 1

    # Add Sign-off / Acceptance Box if not explicitly added
    sign_block = Table([
        [
            Paragraph("<b>Client Acceptance & Authorization:</b>", table_cell_bold),
            Paragraph("<b>Service Provider Authorization:</b>", table_cell_bold)
        ],
        [
            Paragraph("Signature: ___________________________<br/><br/>Printed Name: _______________________<br/><br/>Title: _______________________________<br/><br/>Date: _______________________________", table_cell),
            Paragraph("Signature: ___________________________<br/><br/>Printed Name: _______________________<br/><br/>Title: _______________________________<br/><br/>Date: _______________________________", table_cell)
        ]
    ], colWidths=[246, 246])
    sign_block.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    
    story.append(Spacer(1, 14))
    story.append(KeepTogether([
        Paragraph("Agreement & Sign-Off", h1_style),
        sign_block
    ]))

    doc.build(story, canvasmaker=NumberedCanvas)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Compile Proposal Markdown into PDF")
    parser.add_argument("--input", "-i", required=True, help="Input proposal Markdown file path")
    parser.add_argument("--output", "-o", help="Output PDF file path (optional)")
    args = parser.parse_args()

    input_file = os.path.abspath(args.input)
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    if args.output:
        output_file = os.path.abspath(args.output)
    else:
        output_file = os.path.splitext(input_file)[0] + ".pdf"

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"Compiling proposal PDF: {output_file} ...")
    build_pdf_from_markdown(content, output_file)
    print(f"✓ Proposal PDF generated successfully: {output_file}")


if __name__ == "__main__":
    main()
