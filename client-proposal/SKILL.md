---
name: client-proposal
description: >
  Creates high-converting, professional client proposals focused on the client's problem, expected business outcomes, clear deliverables, and simple pricing. Translates complex AI capabilities into plain-English business value, keeping technical details light while anchoring on trust-building case studies, interactive demos, and measurable before/after transformations. Use when user says "create a proposal", "client proposal", "/proposal", "/client-proposal", "proposal for [client]", "pitch proposal", "draft proposal", or provides project details for a client quote.
version: 1.2.0
tags: [proposal, sales, client, business, pricing, contract, trust, case-study, jev-decision, proposal-judge, antigravity]
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write

---

# Client Proposal Generator — Antigravity Engine

## Purpose

The **Client Proposal Generator** creates professional, conversion-optimized client proposals from minimal project inputs. It produces an end-to-end proposal laser-focused on **the client's problem, expected business outcomes, clear deliverables, and simple pricing**.

Instead of confusing non-technical clients with heavy AI jargon, this skill translates technical workflows into tangible business value and builds unshakeable trust through **measurable before/after results, relatable case studies, and interactive demo proof**.

---

## ⚡ Antigravity Triggers & Commands

### Slash Commands
- `/proposal [client-name]`: Creates a tailored proposal for the specified client.
- `/proposal`: Interactive mode — gathers client name, problem, deliverables, and target investment.
- `/client-proposal`: Alias for `/proposal`.

### Natural Language Triggers
- `"create a proposal for [client]"`
- `"generate a proposal for [client] based on [details]"`
- `"draft a proposal for [client] with 3 pricing tiers and a case study"`
- `"turn this client brief into a proposal"`
- `"proposal for [client]"`

---

## 🧠 Core Strategy & Proposal Psychology

### 1. The 4 Non-Negotiable Pillars
Every proposal must stay anchored on four fundamentals:
1. **The Client's Problem & Cost of Inaction**: Start with their pain, bottleneck, and lost money/time.
2. **Expected Business Outcomes**: Frame everything around revenue uplift, hours saved, speed, and peace of mind.
3. **Clear Deliverables in Plain English**: Explicit, boundary-protected deliverables described by what the client gets, not internal tasks.
4. **Simple, Transparent Pricing**: 3 clear tiers with a "⭐ Recommended" middle anchor, explicit payment terms, and zero hidden gotchas.

### 2. The "Light on AI Jargon" Rule
> [!IMPORTANT]
> **Keep technical AI details fairly light unless the client explicitly asks for them.**
> Non-technical clients often do not understand LLMs, RAG embeddings, vector databases, multi-agent orchestrations, or token budgets. Heavy technical jargon triggers skepticism, confusion, and fear of complexity.
>
> **Always translate AI mechanics into business capabilities:**
> - ❌ *"Deploying a RAG vector database with Gemini 1.5 Pro to index your customer knowledge base"*  
>   ➔ 🟢 *"A 24/7 instant answers assistant that responds to customer questions in under 10 seconds using your verified business guidelines."*
> - ❌ *"Autonomous multi-agent system executing web scraping, entity extraction, and JSON normalization"*  
>   ➔ 🟢 *"An automated market monitor that scours the web and delivers a weekly 1-page competitor intelligence brief to your inbox."*
> - ❌ *"Prompt engineering and LLM temperature calibration for marketing pipelines"*  
>   ➔ 🟢 *"A repeatable content engine that cuts your team's weekly production time from 15 hours to 45 minutes."*

### 3. The "Trust Bridge" (Overcoming Client Skepticism)
The hardest hurdle when selling high-ticket solutions (especially AI and automations) is **proving value and building trust**, particularly with prospects who don't fully grasp how AI works or fear it's just hype.

To bridge this trust gap, every proposal must incorporate **The Trust Bridge**:
1. **Measurable Before / After Transformation Table**: A high-impact, side-by-side contrast comparing their messy current state against their streamlined future state with quantified metrics (time saved, error reduction, revenue unlocked).
2. **Relatable, Concrete Case Study**: A brief, story-driven breakdown of a similar business: their starting pain, what was implemented, and the exact ROI achieved.
3. **Interactive Demo / Video Walkthrough (Show, Don't Tell)**: A direct invitation to experience a live proof asset (a 2-minute Loom walkthrough, clickable prototype, or test run). Seeing it work destroys deal hesitation instantly.

---

## 🏗️ The 8 High-Converting Proposal Sections

### Section 1: Executive Summary (30-Second Stand-Alone Read)
- Stand-alone brief that an executive can review and approve in 30 seconds.
- Mentions client name, their primary bottleneck, the high-level solution, projected measurable outcome, and price anchor.
- Maximum 4–5 sentences. Never use generic language.

### Section 2: Understanding Your Situation & Cost of Inaction
- **The Challenge:** Specific symptom, operational bottleneck, or market risk in the client's own words.
- **The Business Impact:** Quantified cost of inaction (e.g., ~$3,500/mo wasted on manual work, 20 lost hours/week, 40% lead drop-off).
- **The Opportunity:** What becomes possible when this bottleneck is eliminated (predictable scale, faster delivery, higher margins).

### Section 3: The Measurable Transformation (Before vs. After)
A stark, high-trust comparison matrix showing immediate business impact:

| Operational Dimension | Current Reality (Before) | With Our Solution (After) | Concrete Business Value |
|---|---|---|---|
| **Speed to Response** | 4–8 hours manual delay | Under 30 seconds automated | Eliminates lead decay; doubles booked calls |
| **Weekly Staff Drain** | 15–20 hours lost to manual tasks | Zero hours (100% background flow) | Saves ~$2,500/month in team overhead |
| **System Reliability** | Prone to human oversight & missed steps | 100% consistent execution 24/7 | Eliminates dropped balls and client friction |

### Section 4: Live Proof & Interactive Demo
A trust-building proof callout:
> **Experience It in Action:**  
> We have prepared a 2-minute interactive demo / video walkthrough showing this exact workflow operating in real time: **[Link to Demo / Loom / Prototype]**.

### Section 5: Proposed Solution & Deliverables
Limit to 3–6 clear deliverables. Describe each in plain English:
```markdown
### Deliverable [N]: [Outcome-Focused Title]
- **What You Get:** [1-2 sentences describing the finished asset/system in plain language]
- **Why It Matters:** [1 sentence connecting to client revenue, speed, or cost savings]
- **Includes:**
  - [Specific item A]
  - [Specific item B]
  - [Specific item C]
```

### Section 6: Timeline & Milestones
Clear phases with mutual commitments:
| Phase | Milestone / Deliverable | Timeline | Client Responsibilities |
|---|---|---|---|
| **Phase 1: Setup & Intake** | Kickoff diagnostic & asset intake | Week 1–2 | Provide logins, brand assets, & 45-min kickoff |
| **Phase 2: Build & Integration** | Core system build & automation flow | Week 3–4 | Review draft & provide unified feedback in 48h |
| **Phase 3: Testing & Handover** | End-to-end testing, SOPs & team training | Week 5 | Attend 30-min handover walk-through |

*Note: Timeline assumes a 2 business-day feedback turnaround on review milestones.*

### Section 7: Your Investment (Simple Tiered Pricing)
Always call it **"Investment"** (never "cost"). Use 3 straightforward tiers:
- **Tier 1: Foundation / Starter ($X,XXX)** — Essential core solution.
- **Tier 2: Growth / Comprehensive ($XX,XXX) ⭐ Recommended** — Complete, turn-key solution with highest ROI.
- **Tier 3: Scale / Accelerated ($XX,XXX)** — Expedited delivery, priority SLA, white-glove ongoing optimization.
- **Clear Terms:** Simple payment schedule (e.g. 50% upfront, 50% upon final sign-off). Scope protection against scope creep.

### Section 8: Proven Track Record & Frictionless Sign-Off
- **Case Study Spotlight:** 1 brief, highly relatable case study with verifiable numbers.
- **4-Step Frictionless Kickoff:**
  1. Select preferred tier.
  2. Sign acceptance block (or reply *"Approved"*).
  3. Receive invoice & onboarding intake link within 24 hours.
  4. Project kickoff within 3 business days.
- **Validity Window:** Valid for 14–30 days from proposal date.
- **Formal Sign-off Block:** Dual-column signature table.

---

## 🔄 Antigravity Execution Workflow

When invoked:

### Phase 1: Context Gathering & Second Brain Check
1. Scan the workspace (`20_Clients/<ClientName>/`) for existing client notes, discovery transcripts, or GEO/Reputation audit findings.
2. If context exists, automatically pull the client's actual pain points, metrics, and goals.
3. If minimal info is provided, prompt for 3 items:
   - Client name and what they need.
   - Core problem / friction.
   - Pricing target (or let Antigravity suggest the 3-tier structure).

### Phase 2: Proposal Generation
Draft the complete proposal following the 8 sections above, ensuring technical AI details remain light while the Trust Bridge (Before/After table, Case Study, Demo reference) is front and center.

### Phase 2.5: Jev-Style Objective Proposal Decision Judge Gate (scripts/proposal_judge.py)

Before generating the PDF or delivering to the client, execute the bundled **Jev-Style Proposal Decision Judge** to audit the proposal against strict conversion, ROI defensibility, and scope boundary rubrics:

```bash
python3 scripts/proposal_judge.py \
  --file "20_Clients/<ClientName>/PROPOSAL-<ClientName>.md" \
  --client "<ClientName>"
```

#### Deterministic Deal Verdict Rubric:
- **`[READY TO PITCH 🟢]` (Score $\ge 85$, Pricing $\ge 20$, Transformation $\ge 20$):** High conversion probability. Cost of inaction quantified, before/after contrast stark, and 3-tier pricing bulletproof. Send with complete confidence.
- **`[SCOPE REVISION NEEDED 🟡]` (Score 70–84):** Good core pitch, but deliverables are slightly ambiguous or the before/after metrics need sharpening before presenting to executive buyers.
- **`[MARGIN RISK / DO NOT PURSUE 🔴]` (Score $< 70$):** Weak pain definition, missing ROI justification, or high exposure to scope creep. Refactor the offer tiers before sending.

---

### Phase 3: File & Artifact Delivery
1. **Save Markdown File:**
   - Save to `20_Clients/<ClientName>/PROPOSAL-[ClientName].md` (or workspace `PROPOSAL-[ClientName].md`).
2. **Present in Antigravity:**
   - Display an interactive Markdown preview artifact with the Jev Proposal Quality Scorecard and Verdict.

### Phase 4: Executive PDF Generation
Compile into a publication-grade PDF using the built-in ReportLab engine:

```bash
/Users/shivpratap/.gemini/config/skills/reputation/.venv/bin/python ~/.gemini/config/skills/client-proposal/scripts/generate_proposal_pdf.py --input "20_Clients/<ClientName>/PROPOSAL-<ClientName>.md" --output "20_Clients/<ClientName>/PROPOSAL-<ClientName>.pdf"
```


### Phase 5: Pipeline & Dashboard Update
Update `20_Clients/Clients Dashboard.md` with:
- Client Name: `[[20_Clients/<ClientName>/<ClientName>|<ClientName>]]`
- Status: `🟡 Proposal Sent`
- Next Action: `Follow up on proposal (valid until [Date])`

---

## 📋 Quality Checklist Before Delivery

Verify before presenting to the user:
- [ ] **Focused on Core Value:** Explicitly targets client problem, business outcome, clear deliverables, and simple pricing.
- [ ] **Light on AI Jargon:** Technical AI mechanics are translated into plain-English capabilities (no confusing acronyms or buzzwords).
- [ ] **Trust Bridge Active:** Includes a **Measurable Before/After Transformation Table** with quantified metrics.
- [ ] **Proof Assets Included:** References a tangible case study with hard numbers and an interactive demo / video link.
- [ ] **Executive Summary Stand-Alone:** Conveys problem, solution, result, and ballpark in 30 seconds.
- [ ] **Client-Centric Language:** Uses "you / your" at least 2x more than "we / our".
- [ ] **Pricing Simplicity:** 3 tiers with an explicit "⭐ Recommended" anchor and straightforward payment terms.
- [ ] **Frictionless Next Steps:** Clear 4-step sign-off process with firm validity date.
- [ ] **Files Saved Cleanly:** Markdown file and publication-ready PDF saved in the client directory.
