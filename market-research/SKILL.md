---
name: market-research
description: >
  Conducts comprehensive market research briefs with mandatory location and target market intake, TAM/SAM/SOM sizing, growth CAGR, competitor intelligence, and strategic risk modeling. Uniquely generates "Same Idea, Better Angle" business model variations and high-potential direct alternatives tailored to the user's geographic location and available resources. Use when user says "market research", "/market-research", "research market", "market analysis", "TAM SAM SOM", "competitor analysis", "market brief", or provides an industry/business idea to analyze.
version: 1.2.0
tags: [market-research, business, strategy, location-analysis, alternatives, tam-sam-som, competitors, quality-scorecard, decision-engine, antigravity]
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, Write
---

# Market Research Brief Skill — Antigravity Engine

## Purpose

The **Market Research Brief Skill** conducts rigorous, data-backed market analysis for any business idea, product, crop, or industry within Antigravity. It investigates market sizing (TAM, SAM, SOM), growth trajectories, competitive dynamics, and regulatory landscapes. 

**Core Differentiators of this Engine:**
1. **Mandatory Location & Target Market Grounding:** Always evaluates the exact geographic location (city, district, state, regional logistics hub) to uncover hyper-local unfair advantages (raw materials, transport links, nearby metro demand) and local competitive saturation.
2. **"Same Idea, Better Angle" Ideation:** Deconstructs the user's initial idea into 3–4 smarter, higher-margin business models (e.g., value-added processing, upstream B2B inputs, off-season production, or D2C branding).
3. **High-Potential Direct Alternatives:** Systematically identifies 3–5 adjacent opportunities that leverage the same resources/space with lower risk, higher margins, or less perishability/competition.
4. **Repeatable Quality Scorecard & Strategic Decision Verdict:** Audits research rigor across 4 dimensions (Source Freshness, Local Grounding, Competitor Depth, Cited Assumption Rigor) and provides an uncompromising **"So What? / Decision Verdict"** (`[STRONG GO]`, `[GO WITH PIVOT]`, `[NO-GO]`) with immediate 48-hour tactical steps, turning reports into actionable advisory tools.

---

## ⚡ Antigravity Triggers & Commands

### Slash Commands
- `/market-research [topic or industry]`: Initiates the research brief. If location or target market is not mentioned, the skill prompts for them first.
- `/market-research`: Interactive intake mode — gathers target location, specific customer segment, budget/space constraints, and business goals.
- `/market-brief [topic]`: Compact executive brief.

### Natural Language Triggers
- `"conduct market research on [industry/topic] in [location]"`
- `"market analysis for [business idea]"`
- `"calculate TAM, SAM, and SOM for [product/startup]"`
- `"suggest alternatives and market potential for [business/farming idea] in [city/state]"`
- `"what is the market potential of [concept] in [location] and what are better alternatives?"`

---

## 🛑 Phase 1: Mandatory Location & Target Market Intake Gate

Before executing deep research, **ALWAYS** check whether the user has specified:
1. **Target Location / Geographic Base:** (e.g., City, District, State, Country, or regional hub like *Itarsi / Bhopal MP*, *Delhi-NCR*, *Bangalore*, *Pan-India*, or *US*).
2. **Target Customer Segment & Channel:** (e.g., Local retail consumers, B2B wholesale mandis, HoReCa / restaurants, Quick-Commerce, or Export).
3. **Resource & Physical Constraints (Optional but Recommended):** (e.g., Indoor room vs. farmland, initial budget tier, electricity/water access).

> [!IMPORTANT]
> **Intake Rule:** If the user provides an idea without specifying location or target market (e.g., *"market research on mushroom farming"*), **STOP and prompt the user** for their target location and customer market before generating the full brief, OR offer immediate multi-tier location presets (e.g., Tier-1 Urban Metro vs. Tier-2/3 Rural Hub) while asking for their specific base.

---

## 🧠 Research Framework & Analytical Methodology

### 1. Location-Specific Unfair Advantage & Constraint Mapping
Every brief evaluates the chosen geography for:
- **Raw Material & Substrate Availability:** Proximity and cost of essential inputs (e.g., wheat straw, agri-residue, water table, industrial raw materials).
- **Logistics & Hub Connectivity:** Distance to high-paying consumption markets (highways, express railway junctions, airports, cold chain facilities).
- **Local Competitive Saturation:** What local players are already flooding the market with vs. what high-value products are missing.
- **Regional Policies & Subsidies:** State-specific horticulture/industrial missions, district subsidies (NHB, MIDH, PMFME, MSME, PMEGP).

---

### 2. "Same Idea, Better Angle" — Alternative Business Models
Instead of analyzing only the standard/obvious execution of the idea (e.g., basic cultivation or commodity selling), develop 3–4 high-leverage variations:
1. **The Value-Addition / Shelf-Stable Model:** Moving from fresh/perishable raw goods to processed, dehydrated, packaged, or branded goods (eliminating spoilage risk and capturing 3x–5x margins).
2. **The Upstream B2B / Input Supplier Model:** Supplying seeds, spawn, substrate, machinery, packaging, or formulations to other businesses rather than dealing with end-customer retail.
3. **The Off-Season / Counter-Cyclical Model:** Using climate control or specialized scheduling to harvest/produce when market supplies crash and prices spike 2x–3x.
4. **The D2C / Niche Gourmet / Kit Model:** Targeting affluent urban wellness consumers with specialized kits, functional extracts, or premium varieties.

---

### 3. High-Potential Direct Alternatives (Adjacent Opportunities)
Identify 3–5 alternative ventures that:
- Require similar capital expenditure and physical space (e.g., indoor rooms, sheds, or agricultural land).
- Solve the primary pain points of the original idea (e.g., perishability, disease vulnerability, price crashes).
- Provide a structured **Comparison Matrix**:
  | Alternative Idea | CapEx / Budget | Cycle Time | Profit Margin | Risk Profile | Local Geographic Fit |
  |---|---|---|---|---|---|

---

### 4. Market Definition & Sizing (Triangulated Valuation)
- **TAM (Total Addressable Market):** Total global or national demand across all segments.
- **SAM (Serviceable Addressable Market):** The realistic addressable market segment within the target geography and customer tier.
- **SOM (Serviceable Obtainable Market):** Realistic, defendable market share capture over a 1–3 year horizon.
- **Triangulation:** Always combine Top-Down analyst benchmarks with Bottom-Up unit economics (e.g., Number of target buyers × annual spend).

---

### 5. Competitive Landscape & Market Positioning
Map competitors across four distinct strategic quadrants:
- **Market Leaders:** Dominant incumbents holding majority volume.
- **Challengers:** Fast-growing modern players with aggressive marketing.
- **Niche Specialists:** Hyper-focused regional or premium players.
- **Unorganized / Local Players:** Traditional commodity traders, mandi agents, or local suppliers.

---

### 6. Financial Model, Unit Economics & Subsidies
- Detailed cost of production breakdown (Raw inputs, labor, utilities/power, packaging).
- Wholesale vs. Retail vs. Direct margins.
- Payback period and break-even timeline.
- Applicable government subsidies, eligibility criteria, and nodal departments.

---

### 7. Fact vs. Assumption Tagging System
To maintain institutional credibility and separate empirical data from economic hypotheses:
- **`[VERIFIED DATA 🟢]`**: Used for official government statistics (ICAR, APEDA, NHB, Ministry of Commerce), published mandi spot rates, certified census figures, and direct regulatory subsidy notifications.
- **`[MODEL ESTIMATE 🟣]`**: Used for triangulated TAM/SAM/SOM sizing, estimated retail markups, projected 3-year CAGR extrapolations, and bottom-up cost modeling.

---

### 8. Repeatable Quality & Confidence Scorecard (100-Point Audit)
Every research brief includes an automated 4-dimension audit score evaluating research rigor:
1. **Source Freshness (0–25 pts):** Are data points sourced from the trailing 12–24 months (2024–2026)? Are outdated legacy citations penalized?
2. **Hyper-Local Grounding (0–25 pts):** Does the brief evaluate actual district/city logistics corridors, local mandi price spreads, regional raw material costs, and specific state schemes?
3. **Competitive Mapping Breadth (0–25 pts):** Are all 4 tiers analyzed (unorganized local players, regional modern contenders, niche premium brands, and national incumbents)?
4. **Assumption Rigor & Transparency (0–25 pts):** Are financial and sizing models transparently tagged with clear formulas, avoiding ungrounded claims?

*Composite Confidence Tier:*
- **90–100:** High-Confidence Investment Grade Brief
- **75–89:** Moderate-Confidence Advisory Brief (Requires localized field-validation)
- **< 75:** Preliminary Exploratory Brief (Requires deeper ground due-diligence)

---

### 9. "So What? / Executive Decision Verdict & 48-Hour Next Actions"
Never end a brief with passive data. Always deliver a prescriptive executive verdict:
- **Strategic Verdict Call:**
  - `[STRONG GO]`: Macro tailwinds, strong local unit economics, low incumbent saturation.
  - `[GO WITH PIVOT]`: Core commodity model is weak/saturated, but a specific "Better Angle" (e.g., spawn lab, dehydration, D2C) or direct alternative has exceptional upside.
  - `[NO-GO / HIGH RISK]`: Severe structural headwinds, insurmountable logistics friction, or negative unit margins.
- **Immediate 48-Hour Action Plan:** Exactly 3 actionable, low-cost steps for the client to de-risk the opportunity before committing capital (e.g., interview local mandi traders, verify water/electricity tariffs, inspect local KVK facilities).

---

## 🔄 Antigravity Execution Workflow

```
┌────────────────────────────────────────────────────────────┐
│ Phase 1: Location & Target Market Intake Check             │
│ Confirm: Target Location, Market Segment, Resource Base    │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Phase 2: Hyper-Local & National Multi-Source Research      │
│ Live search: regional data, local mandi rates, input costs │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Phase 3: Analytical Triangulation & Alternative Ideation   │
│ TAM/SAM/SOM + "Same Idea Better Angle" + Direct Alternates │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│ Phase 4: Jev-Style Objective Judge Gate (scripts/jev_evaluator)
│ Audit Freshness, Grounding, Competitors & Rigor (0–100)    │
│ Issues Deterministic Verdict: [STRONG GO / PIVOT / NO-GO]  │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
### Phase 4.1: Running the Jev-Style Deterministic Judge
Execute the bundled evaluator script (100% free, deterministic, runs in < 0.1s):

```bash
python3 ~/.agents/skills/market-research/scripts/jev_evaluator.py \
  --file "/Users/shivpratap/Desktop/Market Research/<Topic-Slug>/MARKET-RESEARCH-<Topic>.md"
```

---

### Phase 5: Dedicated Desktop Folder & Second Brain Delivery

1. **Dedicated Desktop Skill Folder:**
   - Every research run creates and stores deliverables in: `/Users/shivpratap/Desktop/Market Research/<Topic-Slug>/`.
   - Standard files saved in that folder:
     - `MARKET-RESEARCH-[Topic].pdf` — Executive publication-grade PDF deliverable (with embedded vector charts, Quality Scorecard, and Decision Verdict).
     - `MARKET-RESEARCH-[Topic].md` — Complete markdown research report.
     - `MARKET-RESEARCH-[Topic].html` — Formatted executive HTML report.
2. **Second Brain Workspace Sync:**
   - Also save a copy of `MARKET-RESEARCH-[Topic].md` to the workspace root or project folder (`10_Projects/` or `20_Clients/`).
3. **Interactive Antigravity Artifact:**
   - Render an executive preview artifact in the chat session for immediate review.

### Phase 6: Publication-Grade Clean PDF Compilation
Compile the markdown brief into an executive PDF using ReportLab with guaranteed clean topic page breaks and sanitized typography:

```bash
/Users/shivpratap/.gemini/config/skills/reputation/.venv/bin/python ~/.agents/skills/market-research/scripts/generate_market_research_pdf.py \
  --input "/Users/shivpratap/Desktop/Market Research/<Topic-Slug>/MARKET-RESEARCH-<Topic>.md" \
  --output "/Users/shivpratap/Desktop/Market Research/<Topic-Slug>/MARKET-RESEARCH-<Topic>.pdf"
```

---

## 📋 Quality Checklist Before Delivery

- [ ] **Clean Page Layout:** Natural compact page flow with smart conditional page breaks (`CondPageBreak(165)`). Zero orphan headings at page bottoms.
- [ ] **Zero Broken Glyphs:** No black square blocks (`■`), unrendered Unicode box-drawing characters, or unhandled currency symbols (`₹` sanitized to `Rs. `).
- [ ] **Quality & Confidence Scorecard:** Includes 4-dimension audit score (Source Freshness, Local Grounding, Competitor Depth, Assumption Rigor) with total /100 score.
- [ ] **Fact vs. Assumption Tagging:** Clear `[VERIFIED DATA 🟢]` vs. `[MODEL ESTIMATE 🟣]` badges applied across all key metrics.
- [ ] **Executive Decision Verdict:** Definite `[STRONG GO]`, `[GO WITH PIVOT]`, or `[NO-GO]` verdict with top 3 immediate 48-hour tactical actions.
- [ ] **No Preview Folder:** Deliverables folder contains only clean PDF, Markdown, and HTML reports.
- [ ] **Desktop Folder Delivery:** All deliverables cleanly organized inside `/Users/shivpratap/Desktop/Market Research/<Topic-Slug>/`.
- [ ] **Location Grounding:** Target geography is explicitly identified and local economic/logistics factors are woven into the analysis.
- [ ] **"Same Idea, Better Angle":** Includes at least 3 distinct business model angles for the primary concept.
- [ ] **Direct Alternatives:** Includes 3–5 high-potential alternative ventures with a structured comparison matrix.
- [ ] **Triangulated Sizing & Visual Charts:** TAM, SAM, and SOM have empirical grounding, illustrated with native vector charts.
- [ ] **Unit Economics & Subsidies:** Lists exact production costs per unit and applicable state/central schemes.



