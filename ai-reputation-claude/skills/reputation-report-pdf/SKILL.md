# Professional PDF Reputation Report Generator

## Skill Purpose
Generate a polished, client-ready PDF reputation report using the ReportLab Python library. This skill searches for the most recent reputation analysis files in the project directory, compiles them into a structured JSON format, and produces a professional PDF with a cover page featuring a reputation score gauge, sentiment breakdown charts, review theme analysis, competitor benchmarking table, response templates section, and a prioritized 90-day action plan.

## When to Use
- User wants a PDF version of the reputation report (not just Markdown)
- User is preparing a deliverable for a client or executive presentation
- User asks for a "polished report", "client-ready report", or "PDF report"
- User wants a visual report with charts, scores, and professional formatting
- Triggered by `/reputation report-pdf` or `/reputation report-pdf <business name>`

## When to Use PDF vs Markdown

| Format | Best For | Pros | Cons |
|---|---|---|---|
| **PDF** | Client presentations, email attachments, board reports, sales collateral | Professional appearance, consistent formatting, visual charts, printable, portable | Harder to edit, requires Python script |
| **Markdown** | Internal use, quick reference, iterative editing, version control | Easy to edit, readable in any editor, git-friendly, fast to generate | Less visually polished, no charts |

**Rule of thumb:** If the report is going to a client, prospect, or executive, use PDF. If it is for internal use or further editing, use Markdown.

## How to Execute

### Step 1: Check for PDF Generation Script

First, check if the dedicated PDF generation script exists:

```bash
ls scripts/generate_reputation_pdf.py 2>/dev/null
```

**If the script exists:** Use it directly (skip to Step 4).
**If the script does not exist:** Generate the PDF inline using ReportLab (follow all steps).

### Step 2: Collect All Available Data

Gather data from all previous reputation skill runs. Check for these files in the project directory:

**Primary data sources (search for all of these):**
- `REPUTATION-AUDIT-*.md` -- Full reputation audit results
- `REPUTATION-SCORECARD-*.md` -- Quick scorecard data
- `SOCIAL-REPUTATION-*.md` -- Social media reputation scan
- `REPUTATION-SEO-*.md` -- SEO reputation strategy
- `REVIEW-RESPONSES-*.md` -- Generated review responses
- `REVIEW-REQUEST-CAMPAIGN-*.md` -- Review request campaign
- `MONITORING-GUIDE-*.md` -- Monitoring setup guide
- `COMPETITOR-REPUTATION-*.md` -- Competitor reputation analysis
- `CRISIS-RESPONSE-*.md` -- Crisis response plan
- `REPUTATION-RECOVERY-*.md` -- Recovery strategy
- `REPUTATION-TRENDS-*.md` -- Trend analysis

**Use glob patterns to find the most recent version of each:**
```bash
ls -t REPUTATION-AUDIT-*.md 2>/dev/null | head -1
ls -t REPUTATION-SCORECARD-*.md 2>/dev/null | head -1
ls -t SOCIAL-REPUTATION-*.md 2>/dev/null | head -1
# ... and so on for each file type
```

**If no previous data exists:**
1. Recommend the user run `/reputation audit <business name>` first for the best results
2. If the user insists on generating a report without prior audits, ask for the business name and run a quick data collection using WebSearch to build the data structure from scratch
3. At minimum, run the equivalent of `/reputation quick <business name>` to populate basic scores

### Step 3: Build the JSON Data Structure

Assemble the collected data into a structured JSON format for the PDF generator.

```json
{
  "business_name": "Example Business",
  "date": "March 26, 2026",
  "overall_score": 72,
  "grade": "B",
  "executive_summary": "A 2-4 sentence summary of the overall reputation health, key strengths, primary vulnerabilities, and recommended first action.",
  "categories": {
    "Review Ratings": {
      "score": 78,
      "weight": "25%"
    },
    "Review Volume": {
      "score": 62,
      "weight": "15%"
    },
    "Sentiment Analysis": {
      "score": 70,
      "weight": "20%"
    },
    "Response Management": {
      "score": 45,
      "weight": "15%"
    },
    "Social Reputation": {
      "score": 68,
      "weight": "15%"
    },
    "Search Presence": {
      "score": 82,
      "weight": "10%"
    }
  },
  "platform_ratings": [
    {
      "platform": "Google",
      "rating": 4.3,
      "review_count": 187,
      "trend": "stable"
    },
    {
      "platform": "Yelp",
      "rating": 3.8,
      "review_count": 52,
      "trend": "declining"
    }
  ],
  "sentiment_breakdown": {
    "positive": 65,
    "neutral": 20,
    "negative": 15
  },
  "review_themes": {
    "positive": [
      {
        "theme": "Customer Service",
        "frequency": 45,
        "example": "Brief example quote or paraphrase"
      },
      {
        "theme": "Product Quality",
        "frequency": 32,
        "example": "Brief example"
      }
    ],
    "negative": [
      {
        "theme": "Wait Times",
        "frequency": 28,
        "example": "Brief example"
      },
      {
        "theme": "Pricing Concerns",
        "frequency": 15,
        "example": "Brief example"
      }
    ]
  },
  "findings": [
    {
      "severity": "Critical",
      "finding": "Description of the most important finding"
    },
    {
      "severity": "High",
      "finding": "Description of a high-priority finding"
    },
    {
      "severity": "Medium",
      "finding": "Description of a medium-priority finding"
    },
    {
      "severity": "Low",
      "finding": "Description of a lower-priority finding"
    }
  ],
  "competitors": [
    {
      "name": "Competitor A",
      "overall_score": 68,
      "google_rating": 4.1,
      "google_reviews": 143,
      "yelp_rating": 3.5,
      "yelp_reviews": 38,
      "sentiment": "Mixed",
      "strength": "High review volume",
      "weakness": "Inconsistent service complaints"
    }
  ],
  "response_templates": [
    {
      "type": "Positive Review Response",
      "template": "Complete template text ready to use"
    },
    {
      "type": "Negative Review Response (Service)",
      "template": "Complete template text ready to use"
    },
    {
      "type": "Negative Review Response (Product)",
      "template": "Complete template text ready to use"
    }
  ],
  "quick_wins": [
    "First quick win action item -- specific and actionable",
    "Second quick win action item",
    "Third quick win action item"
  ],
  "medium_term": [
    "First medium-term action item (1-3 months)",
    "Second medium-term action item",
    "Third medium-term action item"
  ],
  "strategic": [
    "First strategic action item (3-6 months)",
    "Second strategic action item",
    "Third strategic action item"
  ]
}
```

### Step 3b: Field-by-Field Data Assembly Guide

#### `business_name` (string, required)
The business name exactly as it appears on review platforms.

#### `date` (string, required)
Report generation date. Format: "Month DD, YYYY".

#### `overall_score` (integer, 0-100, required)
Weighted average of all category scores:
```
overall_score = (review_ratings * 0.25) + (review_volume * 0.15) + (sentiment * 0.20) + (response_mgmt * 0.15) + (social * 0.15) + (search * 0.10)
```

#### `grade` (string, required)
Letter grade corresponding to the overall score:
- 90-100: A+
- 80-89: A
- 70-79: B
- 60-69: C+
- 50-59: C
- 40-49: D
- 30-39: D-
- 0-29: F

#### `executive_summary` (string, required)
2-4 sentences covering: current reputation health, top strength, biggest vulnerability, and the single most impactful recommended action. This appears on the cover page below the score gauge.

#### `categories` (object, required)
Exactly 6 categories with scores and weights:

| Category | What It Measures | Scoring Guidance |
|---|---|---|
| Review Ratings | Average star rating across platforms | 4.5+ = 90+, 4.0-4.4 = 70-89, 3.5-3.9 = 50-69, 3.0-3.4 = 30-49, <3.0 = below 30 |
| Review Volume | Total number of reviews, velocity, recency | 200+ active reviews with steady flow = 90+, 100-199 = 70-89, 50-99 = 50-69, <50 = below 50 |
| Sentiment Analysis | Ratio of positive to negative sentiment across reviews and social | 85%+ positive = 90+, 70-84% = 70-89, 55-69% = 50-69, <55% = below 50 |
| Response Management | Review response rate, response quality, response time | 90%+ response rate within 24h = 90+, 70-89% = 70-89, 50-69% = 50-69, <50% = below 50 |
| Social Reputation | Social media sentiment, mention volume, advocate presence | Strong positive social presence = 90+, mostly positive = 70-89, mixed = 50-69, negative = below 50 |
| Search Presence | Branded SERP health, Knowledge Panel, positive results on page 1 | 9-10 positive results on page 1 = 90+, 7-8 = 70-89, 5-6 = 50-69, <5 = below 50 |

#### `platform_ratings` (array, required)
Array of objects with platform name, star rating, review count, and trend (improving/stable/declining).

#### `sentiment_breakdown` (object, required)
Percentages for positive, neutral, and negative sentiment. Must sum to 100.

#### `review_themes` (object, required)
Top 3-5 positive themes and top 3-5 negative themes, each with frequency count and a brief example.

#### `findings` (array, required)
5-10 findings ordered by severity (Critical, High, Medium, Low). Each finding should be specific and evidence-based.

#### `competitors` (array, optional)
1-3 competitor objects. Omit if no competitor data is available.

#### `response_templates` (array, optional)
3-5 ready-to-use review response templates. Omit if not generated.

#### `quick_wins`, `medium_term`, `strategic` (arrays, required)
3-5 items each. Specific, actionable recommendations at each time horizon.

### Step 4: Write the JSON File

```bash
cat > /tmp/reputation_report_data.json << 'JSONEOF'
{
  ... assembled JSON data ...
}
JSONEOF
```

### Step 5: Generate the PDF

**Prerequisites check:**
```bash
python3 -c "import reportlab" 2>/dev/null || pip3 install reportlab
```

**Option A: If `scripts/generate_reputation_pdf.py` exists:**
```bash
python3 scripts/generate_reputation_pdf.py /tmp/reputation_report_data.json "REPUTATION-REPORT-[business-name].pdf"
```

**Option B: If the script does not exist, generate the PDF inline:**

Write a Python script to `/tmp/generate_reputation_report.py` that uses ReportLab to create the PDF. The script must produce the following pages:

**Page 1: Cover Page**
- Report title: "Reputation Audit Report"
- Business name
- Generation date
- Overall score gauge (circular visualization with color coding)
- Grade letter (A+ through F)
- Executive summary paragraph

**Page 2: Score Breakdown**
- Horizontal bar chart showing all 6 category scores with color coding
- Score table with category names, scores, weights, and status labels
- Color coding: Green (80+), Blue (60-79), Amber (40-59), Red (<40)

**Page 3: Platform Ratings and Sentiment**
- Platform ratings table (platform, stars, review count, trend)
- Sentiment breakdown pie chart or bar (positive/neutral/negative percentages)
- Review velocity indicator

**Page 4: Review Theme Analysis**
- Top positive themes with frequency bars
- Top negative themes with frequency bars
- Theme examples for each

**Page 5: Key Findings**
- Findings table with severity labels and descriptions
- Color-coded severity indicators (Critical = red, High = orange, Medium = amber, Low = blue)

**Page 6: Competitor Benchmarking (if data exists)**
- Comparison table: business vs competitors
- Rows: Overall Score, Google Rating, Yelp Rating, Review Volume, Sentiment, Key Strength, Key Weakness

**Page 7: Response Templates (if data exists)**
- 3-5 ready-to-use review response templates
- Organized by response type (positive, negative-service, negative-product, neutral)

**Page 8: Prioritized 90-Day Action Plan**
- Quick Wins section (This Week)
- Medium-Term section (1-3 Months)
- Strategic section (3-6 Months)
- Numbered action items in each tier

**Final Page: Methodology**
- Scoring methodology explanation
- Category weights and measurement criteria
- Data sources and limitations
- Footer: "Generated by AI Reputation Manager for Claude Code"

**Run the inline script:**
```bash
python3 /tmp/generate_reputation_report.py /tmp/reputation_report_data.json "REPUTATION-REPORT-[business-name].pdf"
```

### Step 6: Verify the Output

```bash
ls -la "REPUTATION-REPORT-[business-name].pdf"
```

Report the file path and size to the user.

### Step 7: Clean Up

```bash
rm /tmp/reputation_report_data.json
rm /tmp/generate_reputation_report.py 2>/dev/null
```

## PDF Design Specifications

### Color Scheme

| Element | Color | Hex Code |
|---|---|---|
| Primary (headers, titles) | Dark Navy | #1B2A4A |
| Accent (highlights, links) | Blue | #2D5BFF |
| Attention (warnings) | Orange | #FF6B35 |
| Success (high scores) | Green | #00C853 |
| Caution (medium scores) | Amber | #FFB300 |
| Danger (low scores, critical) | Red | #FF1744 |
| Light background | Light Gray | #F5F7FA |
| Body text | Dark Gray | #2C3E50 |
| Secondary text | Medium Gray | #7F8C9B |
| Borders and dividers | Light Border | #E0E6ED |

### Score-to-Color Mapping
- 80-100: Green (#00C853) -- Strong performance
- 60-79: Blue (#2D5BFF) -- Solid with room to improve
- 40-59: Amber (#FFB300) -- Needs attention
- 0-39: Red (#FF1744) -- Critical issues

### Typography
- Headers: Helvetica-Bold, 18-24pt
- Subheaders: Helvetica-Bold, 14-16pt
- Body text: Helvetica, 10-11pt
- Table text: Helvetica, 9-10pt
- Footnotes: Helvetica, 8pt

### Score Gauge Design
The cover page score gauge should be a circular arc (like a speedometer):
- Full arc represents 0-100
- Filled portion represents the actual score
- Color transitions from red (0) through amber (40) to green (80+)
- Score number displayed large in the center
- Grade letter displayed below the number

## ReportLab Script Structure (for inline generation)

When generating the script inline, structure it as:

```python
#!/usr/bin/env python3
"""Reputation Report PDF Generator using ReportLab."""

import json
import sys
import math
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Wedge, Circle, String, Line, Rect
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics import renderPDF

# Color constants matching the design spec
NAVY = colors.HexColor('#1B2A4A')
BLUE = colors.HexColor('#2D5BFF')
ORANGE = colors.HexColor('#FF6B35')
GREEN = colors.HexColor('#00C853')
AMBER = colors.HexColor('#FFB300')
RED = colors.HexColor('#FF1744')
LIGHT_BG = colors.HexColor('#F5F7FA')
DARK_TEXT = colors.HexColor('#2C3E50')
GRAY_TEXT = colors.HexColor('#7F8C9B')
BORDER = colors.HexColor('#E0E6ED')

def score_color(score):
    """Return the appropriate color for a given score."""
    if score >= 80: return GREEN
    if score >= 60: return BLUE
    if score >= 40: return AMBER
    return RED

def draw_score_gauge(score, grade):
    """Create a circular score gauge drawing."""
    # Implementation: draw arc, fill based on score, center text
    ...

def build_cover_page(data):
    """Build cover page elements."""
    ...

def build_score_breakdown(data):
    """Build category score breakdown page."""
    ...

def build_sentiment_page(data):
    """Build platform ratings and sentiment page."""
    ...

def build_themes_page(data):
    """Build review theme analysis page."""
    ...

def build_findings_page(data):
    """Build key findings page."""
    ...

def build_competitors_page(data):
    """Build competitor benchmarking page."""
    ...

def build_templates_page(data):
    """Build response templates page."""
    ...

def build_action_plan_page(data):
    """Build 90-day action plan page."""
    ...

def build_methodology_page():
    """Build methodology page."""
    ...

def generate_report(json_path, output_path):
    """Main report generation function."""
    with open(json_path, 'r') as f:
        data = json.load(f)

    doc = SimpleDocTemplate(output_path, pagesize=letter, ...)
    elements = []

    elements.extend(build_cover_page(data))
    elements.append(PageBreak())
    elements.extend(build_score_breakdown(data))
    elements.append(PageBreak())
    elements.extend(build_sentiment_page(data))
    elements.append(PageBreak())
    elements.extend(build_themes_page(data))
    elements.append(PageBreak())
    elements.extend(build_findings_page(data))

    if data.get('competitors'):
        elements.append(PageBreak())
        elements.extend(build_competitors_page(data))

    if data.get('response_templates'):
        elements.append(PageBreak())
        elements.extend(build_templates_page(data))

    elements.append(PageBreak())
    elements.extend(build_action_plan_page(data))
    elements.append(PageBreak())
    elements.extend(build_methodology_page())

    doc.build(elements)
    print(f"Report generated: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        # Demo mode with sample data
        ...
    else:
        generate_report(sys.argv[1], sys.argv[2])
```

**Important:** The above is a structural guide. When generating the actual inline script, implement ALL functions completely with working ReportLab code. Do not leave stub functions with `...`. Every function must produce real PDF elements.

## Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'reportlab'` | Run `pip3 install reportlab` |
| Script produces empty PDF | Check that JSON data has all required fields |
| Score gauge not rendering | Ensure `overall_score` is a number 0-100 |
| Competitor table missing | Ensure `competitors` array has objects with all required fields |
| PDF is only 1 page | Check for JSON parsing errors: `python3 -c "import json; json.load(open('/tmp/reputation_report_data.json'))"` |
| Fonts look wrong | The script uses Helvetica (built into ReportLab). No custom fonts needed. |
| Charts not appearing | Ensure `reportlab` version is 3.5+ which includes graphics support |
| File size too large | Typical size is 200KB-600KB. If larger, check for uncompressed images. |

## Integration with Other Skills

This skill works best when other reputation skills have been run first. Recommended workflow:

1. Run `/reputation audit <business>` -- Generates comprehensive audit data
2. Run `/reputation social <business>` -- Adds social media analysis
3. Run `/reputation seo <business>` -- Adds search presence data
4. Run `/reputation quick <business>` -- Adds scorecard data
5. Run `/reputation report-pdf` -- Compiles everything into a polished PDF

The PDF skill will automatically search for output files from these skills and incorporate their data.

## Output
- **File:** `REPUTATION-REPORT-[business-name].pdf`
- **Location:** Project root directory
- **Size:** Typically 200KB-600KB depending on content volume
- **Pages:** 7-10 pages depending on whether competitor data, response templates, and additional sections are included

## Key Principles
- The PDF report is the most client-facing deliverable in the reputation toolkit. Quality and professionalism matter above all.
- Always verify the JSON data is complete before generating. Missing fields produce broken pages. Validate the JSON structure before passing it to the script.
- Every score must be justifiable. If a client asks "why did I get a 45 in Response Management?", the findings should provide clear evidence.
- Round scores to whole numbers. Decimals imply false precision for this type of assessment.
- Keep the executive summary to 2-4 sentences maximum. Executives and clients skim cover pages.
- The action plan should be the most actionable section. Specific steps, not vague advice.
- If generating for a prospect (pre-sale), the report is a sales tool. Make the opportunities compelling and the path to improvement clear.
- Color consistency matters. Use the exact hex codes from the design spec for professional appearance.
