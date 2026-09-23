# Company Research & Pre-Meeting Battlecard — Antigravity Engine

The **Company Research Skill** performs deep-dive, multi-source research on any company using verified public information and **parallel multi-agent intelligence** within Google Antigravity.

It delivers a dual-level strategic briefing:
1. **The 5-Minute Pre-Meeting Battlecard:** An executive cheat sheet designed to be digested in under 3 minutes before a call (Golden Openers, Critical Landmines, Buying Committee Map, Catalysts vs. Stall Friction, Discovery Questions).
2. **The Comprehensive Intelligence Dossier:** A deep 8-dimension investigation into business model, pricing, tech stack, leadership, moats, workplace culture, and trailing 6-month developments.

> **"Walk into any meeting knowing more about the company than the person across the table."**

---

## ⚡ What's New in v1.1.0

### 1. 🎯 The 5-Minute Pre-Meeting Battlecard
Never scramble before a client pitch, diligence review, or interview again. Section 1 of every dossier now includes:
- **3 Golden Conversation Openers:** Hyper-personalized conversation hooks from recent podcasts, engineering blogs, or product launches.
- **3 Landmines to Avoid:** Sensitive topics, recent quiet layoffs, discontinued features, or competitor trade secrets to dodge.
- **Buying Committee / Stakeholder Map:** Who holds the budget (Economic Buyer), who feels the pain (Champion), who reviews compliance (Gatekeeper), and who might resist (Blocker).
- **Catalysts vs. Stall Friction:** "Why they buy now" vs. "Why deals stall".
- **3 High-Impact Discovery Questions:** Context-backed questions that uncover unstated needs.

### 2. 🚀 Parallel Multi-Subagent Execution
Instead of running a slow, sequential web search, Antigravity dispatches **three specialized subagents in parallel**:
- **Subagent 1 (Financials & Cap Table):** SEC filings (10-K, 10-Q), Crunchbase, round history, valuation, and burn signals.
- **Subagent 2 (Tech Stack & Moats):** Public headers, DNS records, engineering blogs, GitHub, and hiring specs for tech requirements.
- **Subagent 3 (Customer & Culture Sentiment):** G2, Capterra, Reddit, Glassdoor, Blind, and X/Twitter for authentic friction and morale alerts.
- **Lead Orchestrator:** Synthesizes all streams into the master dossier in under 60 seconds.

---

## 📋 What This Skill Researches

| Dimension | What Antigravity Analyzes |
|---|---|
| **⚡ Pre-Meeting Battlecard** | 3 Golden Openers, 3 Landmines, Buying Committee, Catalysts vs. Stall reasons, Discovery Questions. |
| **Company Snapshot** | Founded year, global HQ, employee count & 1-year growth rate, funding stage, lead backers. |
| **Business Model & Pricing** | Monetization mechanics (SaaS, usage, marketplace), pricing tiers, feature gating, unit economics signals. |
| **Products & Technology** | Core offerings, technology stack, AI integration, technological defensibility/moats, product roadmap signals. |
| **Leadership & Governance** | CEO and executive team backgrounds, previous exits, recent C-suite turnover, board members, public commentary. |
| **Financials & Capital** | Funding round breakdown, valuation trajectory, burn rate indicators, estimated ARR, path to profitability. |
| **Market Position & Moats** | Competitor matrix (leaders, challengers, niche), market share signals, key differentiators, vulnerabilities. |
| **Culture & Talent Signals** | Stated values vs. Glassdoor/Blind sentiment, remote/in-office work model, open roles revealing growth areas. |
| **Recent Developments** | Last 6 months of news, product launches, partnerships, enterprise customer wins, executive changes. |

---

## ⚡ How to Use It in Antigravity

### 1. Slash Commands & Triggers

- `/company-research [Company Name]` — Full multi-agent deep dive with Battlecard + Dossier.
- `/company-battlecard [Company Name]` — Standalone 1-Page Pre-Meeting Battlecard for rapid call prep.
- `/company-book [Company Name]` — Generates an illustrated 8×10 Executive Storybook with AI chapter artwork, narrative chapters, founder lessons, and print-ready PDF.
- `/company-research [Company Name] for sales` — Focused on pain points, buying committee, trigger events, and discovery hooks.
- `/company-research [Company Name] for investment` — Focused on unit economics, valuation history, cap table signals, and due diligence checks.
- `/company-research [Company Name] for interview` — Focused on leadership backgrounds, team culture, and reverse-interview questions.
- `/company-profile [Company Name]` — Compact executive snapshot.

### 2. Natural Language
- *"Create a company book for Stripe."*
- *"Generate an illustrated storybook biography about Figma for our members."*
- *"Generate a pre-meeting battlecard for Stripe."*
- *"Research Figma for an upcoming enterprise sales call."*
- *"Run a parallel multi-agent company research on Datadog."*
- *"Conduct investment due diligence on Notion from public sources."*

---

## 📁 Directory Structure

```text
.agents/skills/company-research/
├── SKILL.md                          # Antigravity skill definition & triggers
├── README.md                         # Quickstart and overview guide
├── templates/
│   ├── company_research_template.md  # Standardized Battlecard + Dossier markdown template
│   ├── company_book.css              # 8×10 Executive Storybook stylesheet
│   ├── company_book_patterns.html    # Storybook HTML layout patterns
│   └── company_book_style_anchors.md # Cohesive visual style prompts for generate_image
├── examples/
│   ├── SAMPLE-COMPANY-RESEARCH-Stripe.md   # Reference benchmark dossier
│   └── SAMPLE-COMPANY-RESEARCH-Stripe.html # Reference interactive HTML dashboard
└── scripts/
    ├── inspect_company_tech.py          # Domain infrastructure & tech stack inspector
    ├── generate_company_research_html.py # Zero-dependency interactive HTML dashboard compiler
    ├── generate_company_research_pdf.py  # Executive ReportLab PDF compiler
    └── render_book_pdf.sh               # Headless Chrome 8×10 Book PDF renderer
```

---

## 📄 Output Deliverables

1. **Workspace Markdown Dossier:** Saved directly to `COMPANY-RESEARCH-[CompanyName].md` or `20_Clients/<ClientName>/`.
2. **Interactive Antigravity Artifact:** Delivered inline in your chat window for immediate review.
3. **Interactive HTML Dashboard (Recommended):**
   ```bash
   python .agents/skills/company-research/scripts/generate_company_research_html.py \
     --input "COMPANY-RESEARCH-[CompanyName].md" \
     --output "COMPANY-RESEARCH-[CompanyName].html"
   ```
   *Features: Plus Jakarta Sans typography, priority battlecard layout, copyable prompts, and one-click print to PDF (`Cmd+P`). Requires zero external pip packages.*

4. **Publication-Grade PDF (Optional via ReportLab):**
   ```bash
   python .agents/skills/company-research/scripts/generate_company_research_pdf.py \
     --input "COMPANY-RESEARCH-[CompanyName].md" \
     --output "COMPANY-RESEARCH-[CompanyName].pdf"
   ```
