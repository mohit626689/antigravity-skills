---
name: company-research
description: >-
  Performs deep-dive research on any company using public information with parallel multi-agent synthesis, strict fact-vs-assumption verification tagging, and living account delta tracking. Produces a 5-minute pre-meeting battlecard with verification badges, a living account brief (/company-research), or an illustrated executive storybook (/company-book). Separates verified facts (🟢) from AI hypotheses (🟣), cites sources with timestamps, and tracks changes over time across repeat client meetings. Use when user says "company research", "/company-research", "/company-battlecard", "/company-book", "company book", "research company", "company profile", "diligence on [company]", "pre-meeting battlecard", or asks to create a storybook biography for a company.
version: 1.4.0
tags: [company-research, sales-prep, battlecard, company-book, storybook, visual-biography, multi-agent, investment, due-diligence, competitive-intelligence, antigravity, verification-rigor, living-account, jev-decision, account-judge]
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, Write
---

# Company Research & Pre-Meeting Battlecard Skill — Antigravity Engine

## Purpose

The **Company Research Skill** performs intelligence-grade research on any company using verified public data, parallel subagent synthesis, and executive battlecard structuring.

It incorporates three foundational enterprise intelligence protocols:
1. **The Rakhim Ford Verification Protocol (Truth vs. Prediction Rigor):** Strictly separates verified public facts from AI-generated assumptions. Every data point, buying committee persona, and landmine is tagged with explicit confidence indicators (`🟢 [VERIFIED FACT]`, `🟡 [HIGH CONFIDENCE PATTERN]`, or `🟣 [AI HYPOTHESIS / TO VALIDATE]`) accompanied by primary citations and research timestamps.
2. **The Joan Marquez Living Account Protocol (Continuous Account Memory):** Converts static one-off reports into living account briefs. Automatically detects previous research in `~/Desktop/Company Research/<CompanyName>/`, archives historical dossiers to `history/`, and generates a dedicated **Section 0: Living Account Delta** detailing what shifted, which assumptions were confirmed or debunked, and open questions to validate on the upcoming call.
3. **The Jev-Style Objective Account Judge Gate (Quantitative Due-Diligence):** Employs an automated, objective decision gate (`scripts/account_judge.py`) that audits financial viability, tech stack maturity, buying committee access, and churn/layoff landmines to compute a **100-Point Account Quality Scorecard** and enforce an unambiguous **Account Engagement Verdict** (`[PRIME TARGET 🟢]`, `[QUALIFY CAREFULLY 🟡]`, or `[DISQUALIFY / RED FLAG 🔴]`).

It provides three distinct deliverable modes:
1. **The 5-Minute Pre-Meeting Battlecard (`/company-battlecard`):** An executive cheat sheet designed to be digested in under 3 minutes before a high-stakes call (Golden Openers, Landmines to Avoid, Buying Committee Map, Catalysts vs. Stall Friction, Discovery Questions)—all color-coded with verification badges.
2. **The Comprehensive Living Dossier (`/company-research`):** An in-depth investigation covering Section 0 (Living Delta) + 8 dimensions of company DNA, financials, tech stack, leadership, moats, workplace culture, and recent developments.
3. **The Illustrated Company Storybook (`/company-book`):** An immersive, 8×10 illustrated visual biography and narrative reader with AI-generated artwork, founder lessons, and team reflection questions (adopting the architecture of the Children's Book Studio for executive & member reading).

---

## ⚡ Antigravity Triggers & Slash Commands

### Slash Commands
- `/company-research [Company Name]`: Executes full parallel multi-agent deep dive, producing both the 5-Minute Battlecard and the full Dossier.
- `/company-battlecard [Company Name]`: Generates a standalone, hyper-focused 1-Page Pre-Meeting Battlecard for rapid briefing.
- `/company-book [Company Name]`: Creates a complete, illustrated executive storybook with narrative chapters, AI-generated chapter artwork, founder principles, interactive HTML reader, and print-ready PDF.
- `/company-research [Company Name] for sales`: Emphasizes pain points, buying committee roles, trigger events, and discovery hooks.
- `/company-research [Company Name] for investment`: Highlights unit economics, valuation history, cap table signals, and risk factors.
- `/company-research [Company Name] for interview`: Focuses on executive reputations, team culture dynamics, and reverse-interview questions.
- `/company-profile [Company Name]`: Compact executive profile.

### Natural Language Triggers
- `"create a company book for [company name]"`
- `"make an illustrated storybook biography about [company name] for our members"`
- `"generate a pre-meeting battlecard for [company name]"`
- `"research [company name] for an upcoming sales call"`
- `"run parallel company research on [company name]"`
- `"prepare a company dossier on [company name] with talking points"`
- `"conduct investment due diligence on [company name] from public sources"`

---

## 🚀 Multi-Subagent Parallel Architecture

To maximize research depth while keeping turnaround time under 60 seconds, Antigravity orchestrates **three specialized subagents** in parallel before synthesizing the final dossier:

```
                               ┌──────────────────────────────────────────────┐
                               │       Antigravity Lead Orchestrator          │
                               │ Workspace Context & Research Objective Intake│
                               └──────────────────────┬───────────────────────┘
                                                      │
                       ┌──────────────────────────────┼──────────────────────────────┐
                       │ (Parallel Dispatch)          │ (Parallel Dispatch)          │ (Parallel Dispatch)
                       ▼                              ▼                              ▼
        ┌─────────────────────────────┐┌─────────────────────────────┐┌─────────────────────────────┐
        │  Subagent 1: Financials &   ││  Subagent 2: Tech Stack &   ││  Subagent 3: Sentiment &    │
        │      Capital Diligence      ││      Product Moats          ││     Culture Intelligence    │
        ├─────────────────────────────┤├─────────────────────────────┤├─────────────────────────────┤
        │ • SEC Filings (10-K, 10-Q)  ││ • Cloud & CDN Footprint     ││ • Customer Reviews (G2)     │
        │ • Crunchbase / PitchBook    ││ • Languages, Frameworks, AI ││ • Reddit & Forum Sentiment  │
        │ • Round History & Backers   ││ • GitHub & Engineering Blog ││ • Glassdoor & Blind Ratings  │
        │ • Valuation & ARR Estimates ││ • Open Tech Job Specs       ││ • Executive Churn Velocity  │
        │ • Burn Rate & Efficiency    ││ • Proprietary Moats / IP    ││ • Layoffs & Morale Signals  │
        └──────────────┬──────────────┘└──────────────┬──────────────┘└──────────────┬──────────────┘
                       │                              │                              │
                       └──────────────────────────────┼──────────────────────────────┘
                                                      │ (Aggregate Streams)
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │           Antigravity Synthesis              │
                               │  Cross-Triangulation & Strategic Modeling    │
                               ├──────────────────────────────────────────────┤
                               │ 1. 5-Minute Pre-Meeting Battlecard           │
                               │ 2. Master Markdown Dossier                   │
                               │ 3. Inline Interactive Chat Artifact          │
                               │ 4. Executive PDF / HTML Compilation          │
                               └──────────────────────────────────────────────┘
```

### Subagent 1: Financials & Capital Diligence
- **Focus:** Capitalization, funding rounds, lead institutional investors, valuation trajectory, estimated ARR/burn, and path to profitability.
- **Sources:** SEC Edgar (if public), Crunchbase, PitchBook, press releases, venture debt announcements.

### Subagent 2: Tech Stack & Product Defensibility
- **Focus:** Infrastructure (AWS/GCP/Azure/Cloudflare), frontend/backend frameworks, database/AI layer, proprietary IP/patents, and hiring signals from job specs.
- **Sources:** Engineering blogs, developer documentation, GitHub organizations, job descriptions, HTTP header fingerprinting.

### Subagent 3: Customer Sentiment & Culture Radar
- **Focus:** Authentic user friction, common complaints about competitors, churn triggers, Glassdoor/Blind workplace sentiment, recent executive turnover, and PR controversies.
- **Sources:** G2, Capterra, Trustpilot, Reddit, Twitter/X, Glassdoor.

---

## ⚖️ The Jev-Style Objective Account Judge Gate (scripts/account_judge.py)

Before generating the battlecard or sending the brief to executive stakeholders, Antigravity executes the **Jev-Style Account Decision Judge** to evaluate the compiled findings against strict commercial and risk criteria:

```bash
python3 scripts/account_judge.py \
  --file "~/Desktop/Company Research/<CompanyName>/COMPANY-RESEARCH-<CompanyName>.md" \
  --company "<CompanyName>"
```

### Deterministic Account Verdict Rubric:
- **`[PRIME TARGET 🟢]` (Score $\ge 85$, Landmine Score $\ge 18$):** High willingness to pay, healthy capitalization, clear decision-makers, and modern tech stack. Prioritize for executive outreach.
- **`[QUALIFY CAREFULLY 🟡]` (Score 70–84):** Viable prospect with budget, but requires validating specific decision-making blockers or navigating slower procurement cycles.
- **`[DISQUALIFY / RED FLAG 🔴]` (Score $< 70$ or $\ge 3$ critical red flags):** High churn velocity, layoffs, or distressed balance sheet. Not recommended for high-touch enterprise sales.

---

## 🎯 The 5-Minute Pre-Meeting Battlecard Framework


Every dossier features a prominent **5-Minute Pre-Meeting Battlecard** at the very top, organized into five mission-critical quadrants:

### 1. 🎯 3 Golden Conversation Openers
Hyper-personalized, high-signal conversation starters that immediately prove you've done homework:
- *Example:* "I noticed on your engineering blog last month that you migrated your ingestion layer to ClickHouse—how has that impacted your real-time processing latency?"

### 2. ⚠️ 3 Landmines to Avoid
Critical topics, recent controversies, failed initiatives, or competitor sensitivities to dodge:
- *Example:* "Avoid praising Competitor X; they recently lost a 7-figure account to them and filed a trade secret complaint."
- *Example:* "Do not assume their European expansion is live; German office launch was delayed by 6 months."

### 3. 👥 Buying Committee / Stakeholder Map
- **Economic Buyer:** VP/C-level with budget authority and P&L responsibility.
- **Internal Champion:** The operational manager whose daily pain your solution eliminates.
- **Technical Gatekeeper:** Security, compliance, or infrastructure lead checking risk and integration.
- **Potential Blocker:** Department head whose budget or team influence might be challenged.

### 4. ⚖️ Catalysts vs. Stall Friction
- **Why They Buy (The Burning Urgency):** The quantifiable ROI, revenue upside, or compliance mandate driving action now.
- **Why They Stall (The Hesitation):** The top internal objection (e.g. migration friction, procurement security reviews, incumbent inertia).

### 5. 🔍 3 High-Impact Discovery Questions
Questions that go beyond generic pitches to uncover unstated budget, timeline, and workflow requirements.

---

## 🧠 The 8 Research Dimensions

In addition to the battlecard, the full dossier covers:

1. **Company Overview & Core DNA:** Identity, founding, HQ, global footprint, stage, and verified headcount growth.
2. **Business Model & Monetization Architecture:** How they make money, pricing tiers, feature gating, unit economics signals.
3. **Product Offerings & Technology Stack:** Core products, architecture, AI capabilities, and defensibility moats.
4. **Leadership & Executive Team:** CEO, CTO, CRO backgrounds, prior exits, and recent C-suite turnover.
5. **Funding, Valuation & Financial Health:** Capital raised, valuation trajectory, burn signals, and revenue estimates.
6. **Market Position, Moats & Competition:** Leader/Challenger/Niche quadrant, comparative advantage matrix, vulnerabilities.
7. **Workplace Culture & Employer Brand:** Stated values vs. Glassdoor sentiment, remote/hybrid policy, hiring priorities.
8. **Recent Developments (Last 6 Months):** Product launches, M&A, partnerships, enterprise customer wins.

---

## 🔄 Antigravity Execution Workflow

### Phase 1: Living Account Delta Check & Archive (The Joan Marquez Protocol)
1. **Desktop & Vault Memory Scan:** Check `~/Desktop/Company Research/<CompanyName>/` and Second Brain folders (`20_Clients/`, `10_Projects/`) for an existing `COMPANY-RESEARCH-[CompanyName].md`.
2. **Delta Detection & Historical Archiving:**
   - If prior research exists:
     - Read the previous `research_date` and key findings (revenue, tech stack, buying committee, open hypotheses).
     - Archive the older dossier to `~/Desktop/Company Research/<CompanyName>/history/COMPANY-RESEARCH-[CompanyName]-[PriorDate].md`.
     - Activate **Living Account Delta Mode** to construct **Section 0: Living Account Delta**:
       1. 🆕 *New Signals & Strategic Shifts Since [PriorDate]* (Funding, new products, leadership hires, job spec surges).
       2. ✅ *Assumptions Confirmed or Debunked* (Which previous AI hypotheses proved accurate vs. invalidated).
       3. ❓ *Open Questions to Validate on Your Next Call* (Unresolved inquiries carrying over).
   - If no prior research exists, initialize as **Baseline Dossier**.
3. Confirm research objective (Sales Call, Investment Due Diligence, Interview Prep, or Partnership).

### Phase 2: Parallel Multi-Agent Live Research (Cross-Tier Diligence)
1. **Handling Diverse Company Tiers (The Rakhim Ford Requirement):**
   - **For Public Mega-Caps (e.g. Tesla, Apple):** Extract audited 10-K/10-Q filings, institutional transcripts, and regulatory submissions.
   - **For Private Startups & Mid-Market B2B (e.g. Supabase, Linear, PostHog):** In the absence of SEC filings, triangulate verified facts from:
     - PitchBook / Crunchbase funding disclosures and founder interviews.
     - Official changelogs, GitHub releases, and documentation architecture.
     - Live job board postings (revealing actual tech stack requirements and expansion priorities).
     - G2, Capterra, Reddit, and Hacker News user sentiment.
2. **Automated Infrastructure Fingerprinting:** Run the domain inspector:
   ```bash
   python .agents/skills/company-research/scripts/inspect_company_tech.py [company-domain.com]
   ```

### Phase 3: Triangulation & 3-Tier Verification Tagging (The Rakhim Ford Protocol)
Every finding, metric, opener, landmine, and stakeholder entry must be labeled with an explicit verification badge:
1. 🟢 `[VERIFIED FACT]`: Grounded in primary public documentation (audited SEC filings, official press releases, verified executive profiles, official documentation). Must include inline citation links and research timestamp.
2. 🟡 `[HIGH CONFIDENCE PATTERN]`: Triangulated from multiple secondary signals (cluster of open job requisitions, HTTP response headers, recurring review themes on G2/Glassdoor).
3. 🟣 `[AI HYPOTHESIS / TO VALIDATE]`: Educated predictive inferences (e.g. likely internal blocker, unstated architecture bottlenecks, inferred budget constraints). **Explicitly flags that the sales rep or researcher must validate this hypothesis during the live call.**

### Phase 4: Systematic Desktop Directory Architecture & Second Brain Memory
1. **Dedicated Desktop Directory Architecture:**
   - Always maintain one unified master directory on the Desktop:
     `~/Desktop/Company Research/`
   - Inside the master directory, create a company-specific folder named after the company or domain:
     `~/Desktop/Company Research/<CompanyName>/`
   - **All assets and deliverables for that company must be stored inside this folder** to keep Desktop memory systematic and prevent any loose files on Desktop root:
     - `[CompanyName]-Company-Research-Report.pdf` (Executive research report PDF)
     - `[CompanyName]-Illustrated-Storybook.pdf` (Illustrated narrative storybook PDF)
     - `COMPANY-RESEARCH-[CompanyName]-Report.html` (Interactive HTML report)
     - `COMPANY-RESEARCH-[CompanyName].md` (Full intelligence markdown dossier)
     - `Storybook/` (Folder containing `book.html`, `manuscript.md`, and high-res chapter `images/`)
2. Render an executive preview artifact in the Antigravity session featuring the complete Battlecard and Snapshot table.

### Phase 5: Publication-Grade HTML & Compact PDF Compilation
1. **Interactive HTML Dashboard:**
   Save into `~/Desktop/Company Research/<CompanyName>/COMPANY-RESEARCH-[CompanyName]-Report.html`.
2. **Compact Executive PDF Compilation (Zero Unnecessary Whitespace):**
   Render via headless Chrome without forced page breaks to eliminate awkward blank spaces and maintain compact density:
   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --no-pdf-header-footer \
     --print-to-pdf="/Users/shivpratap/Desktop/Company Research/<CompanyName>/<CompanyName>-Company-Research-Report.pdf" \
     "file:///Users/shivpratap/Desktop/Company Research/<CompanyName>/COMPANY-RESEARCH-<CompanyName>-Report.html"
   ```
3. **Internal Skill Archive Copy (Optional):**
   Copy generated PDFs to `.agents/skills/company-research/reports/` for central version tracking.

---

## 📚 The `/company-book` Command: Executive Storybook Studio

When the user triggers `/company-book [Company Name]`, Antigravity adapts the architecture of the **Children's Book Studio** to produce an illustrated, narrative-driven **Executive Storybook & Visual Biography** for members, founders, and team onboarding.

Instead of reading dry financial spreadsheets, members experience the company's story through an immersive 8×10 illustrated reader with chapter art, founder turning points, and strategic reflection questions.

### The 5-Step Storybook Pipeline

```
┌────────────────────────────────────────────────────────────┐
│ Step 0: Intake & Thematic Framing                          │
│ Company, founders, core theme, reader tone, book slug      │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Step 1: Write Narrative Manuscript (manuscript.md)         │
│ 5 illustrated chapters + Executive Principles + Questions │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Step 2: Cohesive Image Generation (generate_image)         │
│ Native Antigravity 3:4 portrait art with style anchors     │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Step 2.5: Mandatory User Approval Checkpoint               │
│ User reviews and confirms illustrations before layout      │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Step 3: Lay Out the 8×10 Interactive Book (book.html)      │
│ Assembled using company_book.css & page patterns           │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Step 4: Headless Chrome Print-Ready PDF Rendering          │
│ Run render_book_pdf.sh to compile publication PDF          │
└────────────────────────────────────────────────────────────┘
```

#### Step 0 — Intake & Framing
1. Define company parameters:
   - **Company & Founders:** (e.g. Stripe / Patrick & John Collison)
   - **Book Title & Subtitle:** (e.g. *The Architecture of Ambition: The Story of Stripe and How Two Brothers Rewired the Internet's Economy*)
   - **Core Theme:** (e.g. Developer Empathy, Relentless Velocity, Simplicity)
   - **Art Style Anchor:** Pick one from `templates/company_book_style_anchors.md` (Default: *Editorial Graphic Novel & Silicon Valley Noir*).
2. Create workspace output folder: `./COMPANY-BOOK-[CompanySlug]/` with an `images/` subfolder.

#### Step 1 — Write the Narrative Manuscript (`manuscript.md`)
Write a 5-chapter biographical narrative (~2,500–3,500 words total):
- **Front Matter:** Book Title, Subtitle, Preface note (*"Why This Story Matters"*), Memorable Founder Quote.
- **Chapter 1: The Spark & The Genesis** (The founder origin, the initial frustration, the blank canvas)
- **Chapter 2: The Crucible of Scale** (Early rejections, technical near-death moments, the first big customer)
- **Chapter 3: The Secret Architecture** (The product moat, culture, how the engine works)
- **Chapter 4: The Modern Empire** (The global footprint, market dominance, customer triumphs)
- **Chapter 5: The Unwritten Horizon** (The future vision, AI frontier, challenges ahead)
- **Chapter Apparatus (Repeating at the end of each chapter):**
  - **✦ Executive Principle:** One memorable, actionable mental model.
  - **✦ Question for Your Team:** A deep reflective inquiry for leadership discussions.

#### Step 2 — Generate Visual Illustrations (Native `generate_image`)
Use Antigravity's native `generate_image` tool:
- **Aspect Ratio:** `'3:4'` (Portrait 8×10 book format).
- **Art Style Anchor:** Append the selected anchor string to every prompt to maintain visual harmony.
- **Negative Constraints:** Always append `"no text, no words, no lettering, no borders"`.
- **Cover Requirement:** Specify `"leave open, uncluttered negative space at the TOP third for title overlay"`.
- **Planned Assets:**
  - `images/cover.png` (Front cover hero image)
  - `images/chapter1.png` through `images/chapter5.png` (One full-bleed illustration per chapter)

#### Step 2.5 — Mandatory Image Verification & Confirmation Checkpoint
> [!IMPORTANT]
> **DO NOT proceed to Step 3 (Layout) or Step 4 (PDF Rendering) without explicit confirmation from the user.**
1. Present the generated illustrations to the user in chat.
2. Ask: *"Here are the generated illustrations for [Company Book]. Please review them. Do they meet your expectations, or would you like adjustments to character likeness, setting, or lighting?"*
3. If the user requests tweaks, refine the prompt and re-run `generate_image`. Proceed only once approved.

#### Step 3 — Lay Out the Interactive Book (`book.html`)
Build `./COMPANY-BOOK-[CompanySlug]/book.html` by combining:
- `templates/company_book.css`
- `templates/company_book_patterns.html`
- Include the browser reader toolbar with sticky **"Export / Print PDF (Cmd+P)"** button.

#### Step 4 — Render Print-Ready PDF & Consolidate Deliverables
1. Execute headless Chrome to compile the publication-grade 8×10 storybook PDF directly into the company's Desktop folder:
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="/Users/shivpratap/Desktop/Company Research/<CompanyName>/<CompanyName>-The-Master-Plan-Illustrated-Storybook.pdf" \
  "file:///Users/shivpratap/Desktop/Company Research/<CompanyName>/Storybook/book.html"
```
2. Move the storybook project files (`book.html`, `manuscript.md`, `images/`) into `/Users/shivpratap/Desktop/Company Research/<CompanyName>/Storybook/` so all information regarding that company is systematically organized in one place.

---

## 📄 Standard Markdown Output Template

Output must be saved as `COMPANY-RESEARCH-[CompanyName].md`:

```markdown
# Company Research Dossier: [Company Name]

**Research Date:** [YYYY-MM-DD]  
**Company Domain:** [https://example.com]  
**Research Objective:** [Sales Call Prep / Investment Due Diligence / Interview Prep / Partnership]  
**Research Engine:** Antigravity Multi-Agent Intelligence System  

---

## ⚡ Section 1: The 5-Minute Pre-Meeting Battlecard

> [!IMPORTANT]
> **Executive Briefing**: Review this section 5 minutes before your conversation. It contains high-signal openers, critical landmines, and your stakeholder map.

### 🎯 3 Golden Conversation Openers
1. **[Opener 1 - Recent Milestone / News]:** "[Specific conversational opener citing recent product drop, partnership, or interview]"
2. **[Opener 2 - Technical / Workflow Shift]:** "[Opener referencing recent engineering blog post, architecture change, or hiring focus]"
3. **[Opener 3 - Industry / Market Positioning]:** "[Opener acknowledging their recent positioning move against competitors]"

### ⚠️ 3 Landmines to Avoid
1. **[Landmine 1 - Sensitive Event]:** Avoid bringing up [recent layoff, executive exit, or missed deadline] unless they raise it.
2. **[Landmine 2 - Competitor Bias]:** Do not praise [Competitor Name]; [explain specific friction or lost deal history].
3. **[Landmine 3 - Product Assumption]:** Do not assume [Feature/Tier] is mature; [explain current limitation or beta status].

### 👥 Buying Committee & Stakeholder Map
| Role in Decision | Likely Title / Persona | Primary Agenda / Priority | Key Concern / Objection |
|---|---|---|---|
| **Economic Buyer** | [e.g. VP of Sales / CFO] | [ROI, Revenue acceleration, Cost control] | [Budget payback period] |
| **Internal Champion** | [e.g. Head of Ops / Lead Eng] | [Removing daily workflow friction] | [Implementation effort] |
| **Technical Gatekeeper** | [e.g. CISO / VP Architecture] | [Security, SOC2, API reliability] | [Data privacy, vendor lock-in] |
| **Potential Blocker** | [e.g. Legacy Systems Manager] | [Defending existing internal tooling] | [Disruption to current team] |

### ⚖️ Catalysts vs. Stall Friction
- **Why They Buy (The Urgency Catalyst):** [The acute pain point, executive mandate, or growth target forcing them to solve this now.]
- **Why They Stall (The Hesitation Friction):** [The primary reason deals or partnerships stall with this company (e.g. long security reviews, competing internal projects).]

### 🔍 3 High-Impact Discovery Questions
1. *Context:* [Why you're asking]  
   👉 **Question:** "[Question formulated to uncover unstated workflow pain]"
2. *Context:* [Why you're asking]  
   👉 **Question:** "[Question probing their current tool integration and bottleneck]"
3. *Context:* [Why you're asking]  
   👉 **Question:** "[Question clarifying timeline, budget authority, and decision criteria]"

---

## 2. Executive Summary

[4–6 sentences providing a high-signal overview: core business, market standing, scale, and primary strategic development. Written so someone with zero context can quickly understand the company.]

---

## 3. Company Snapshot

| Metric | Detail | Source / Status |
|---|---|---|
| **Founded** | [Year] | [Confirmed / Web] |
| **Founders** | [Founder Names] | [LinkedIn / Corporate] |
| **Global HQ** | [City, State, Country] | [Corporate Site] |
| **Headcount** | [Estimated count] ([Growth % over 1 yr]) | [LinkedIn / Press] |
| **Growth Stage** | [Seed / Early / Growth / Mature / Public] | [Analysis] |
| **Total Capital Raised** | $[X]M ([Round details, Date]) | [Crunchbase / Press] |
| **Estimated Revenue / ARR** | $[X]M ARR (or Public Market Cap: $[X]B) | [Estimate / SEC] |
| **Key Backers / Investors** | [Investor 1, Investor 2, Investor 3] | [Crunchbase / PitchBook] |

---

## 4. Business Model & Monetization Architecture

### How They Make Money
[Detailed breakdown of monetization engines: subscriptions, usage, services, transactions]

### Pricing Architecture
| Plan / Tier | Price Point | Target Customer | Key Feature Gating |
|---|---|---|---|
| **[Starter]** | $[X]/mo | [SMB / Individual] | [Core features] |
| **[Pro]** | $[X]/mo | [Growing Teams] | [Advanced features] |
| **[Enterprise]** | Custom / Contact | [Global Enterprise] | [SSO, SLA, Custom integrations] |

---

## 5. Products, Services & Technology Stack

### Core Offerings
- **[Product A]:** [Functionality, value proposition, and key use cases]
- **[Product B]:** [Functionality, value proposition, and key use cases]

### Technology Stack & Architecture
- **Infrastructure & Cloud:** [AWS, GCP, Azure, Cloudflare]
- **Languages & Frameworks:** [Python, React, Go, etc.]
- **AI / Data Stack:** [LLM integrations, vector databases, ML pipelines]

### Defensibility & Moats
- **[Moat 1]:** [e.g. Proprietary dataset, high switching costs, developer lock-in]
- **[Moat 2]:** [e.g. Strong brand community, regulatory moat]

---

## 6. Leadership & Governance

| Name | Role | Background & Prior Companies | Strategic Focus |
|---|---|---|---|
| **[Name]** | Chief Executive Officer | [Ex-Company, Notable achievements] | [Company vision] |
| **[Name]** | Chief Technology Officer | [Engineering leadership background] | [Product architecture] |
| **[Name]** | Chief Revenue Officer | [Commercial track record] | [Enterprise sales] |

---

## 7. Market Positioning & Competitive Landscape

**Market Category:** [Primary industry segment]  
**Positioning Tier:** [Market Leader / Disruptive Challenger / Niche Specialist / Fast Follower]  

### Direct Competitors
1. **[Competitor 1]:** [Key overlap, differentiation, pricing angle]
2. **[Competitor 2]:** [Key overlap, differentiation, pricing angle]
3. **[Competitor 3]:** [Key overlap, differentiation, pricing angle]

---

## 8. Culture, Talent & Workplace Signals

- **Core Stated Values:** [Values cited on career pages]
- **Work Model:** [Remote / Hybrid / In-Office policy]
- **Hiring Priorities:** [Departments with most active job postings — indicates growth areas]
- **Employee Sentiment (Glassdoor / Blind):** [Average rating: X/5.0; key themes of satisfaction vs. critique]

---

## 9. Recent Developments (Past 6 Months)

| Date | Milestone / Event | Strategic Significance |
|---|---|---|
| [MM/YYYY] | [Product Launch / Feature Release] | [Impact on market competitiveness] |
| [MM/YYYY] | [Funding Round / Acquisition] | [Impact on capital runway & expansion] |
| [MM/YYYY] | [Partnership / Customer Win] | [Impact on enterprise validation] |

---

## 10. Verified Sources & Citations

1. [Primary Corporate Domain - URL]
2. [SEC Filings / Crunchbase Profile - URL]
3. [Industry Press / Newsroom Announcements - URL]
4. [Customer Review Aggregators - URL]
```

---

## 📋 Quality Verification Checklist Before Delivery

- [ ] **Battlecard Completeness:** Section 1 includes 3 Golden Openers, 3 Landmines, Stakeholder Map, Catalysts vs. Stall reasons, and 3 Discovery Questions.
- [ ] **Public Sourcing:** All data points are extracted from verifiable public sources.
- [ ] **Status Labeling:** Figures are clearly tagged as `[Confirmed]`, `[Estimated]`, or `[Inferred]`.
- [ ] **Financial Rigor:** Capital raised, valuation, and revenue metrics cite dates and sources.
- [ ] **Competitive Depth:** Identifies at least 3–5 direct competitors with specific differentiation.
- [ ] **Recency:** Recent developments cover the trailing 6-month window.
- [ ] **Second Brain Storage:** Deliverable saved cleanly into workspace with artifact preview rendered.
