# Market Research Brief Skill — Antigravity Engine

The **Market Research Brief Skill** equips Antigravity to conduct comprehensive, location-grounded market intelligence briefs with TAM/SAM/SOM sizing, competitive intelligence, alternative business models, and high-potential adjacent opportunities.

---

## What Makes This Skill Unique

1. **Mandatory Location & Target Market Intake:** Always establishes your target location (city, district, state, regional hub) and customer segment first to identify hyper-local unfair advantages (cheap raw materials, transit links, regional subsidies) and local market saturation.
2. **"Same Idea, Better Angle" Ideation:** Deconstructs your primary concept into 3–4 smarter, higher-margin business variations (e.g., value-added processing, upstream B2B inputs, off-season climate control, or D2C branding).
3. **High-Potential Direct Alternatives:** Systematically surfaces 3–5 alternative business ventures that leverage the same physical assets, budget, and local geographic strengths with lower risk or higher return, complete with a structured comparison matrix.
4. **Triangulated Sizing:** Top-down macro benchmarks combined with bottom-up unit economics.
5. **Publication-Grade Delivery:** Generates clean Markdown reports, executive artifacts, and ready-to-compile ReportLab PDFs.

---

## Directory Structure

```text
market-research/
├── SKILL.md            # Antigravity skill definition, mandatory intake gates & workflows
├── README.md           # Documentation & trigger reference
├── templates/
│   └── market_research_template.md   # Markdown deliverable template with alternatives matrix
└── scripts/
    └── generate_market_research_pdf.py # Executive ReportLab PDF compiler
```

---

## Antigravity Triggers & Usage

### 1. Slash Commands
- `/market-research [topic]` — Initiates a research brief. If location is missing, prompts for it first.
- `/market-research` — Interactive intake mode (asks for location, customer tier, and resource footprint).
- `/market-brief [topic]` — Compact executive brief.

### 2. Natural Language
- *"Conduct market research on organic dairy processing in Bhopal MP"*
- *"Market analysis for mushroom farming in Itarsi and suggest better alternatives"*
- *"What is the market potential of hydroponics in Delhi-NCR and what are same-idea better angles?"*

---

## Compiling Publication-Grade PDFs

```bash
python scripts/generate_market_research_pdf.py \
  --input MARKET-RESEARCH-Topic.md \
  --output MARKET-RESEARCH-Topic.pdf
```
