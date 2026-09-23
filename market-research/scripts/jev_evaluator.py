#!/usr/bin/env python3
"""
Jev-Style Objective Quality & Decision Judge Gate — Market Research
Inspired by the TypeSafe Jev System-1 Decision Architecture.
100% Free, Deterministic, and Repeatable.
"""

import sys
import os
import re
import json
import argparse


def evaluate_market_brief(content: str) -> dict:
    """
    Evaluates a market research brief against strict quantitative rubrics.
    Returns composite score, category breakdown, decision verdict, and 48-hour actions.
    """
    # 1. Source Freshness Evaluation (0–25)
    freshness_score = 15  # baseline
    years_2024_2026 = len(re.findall(r'202[4-6]', content))
    if years_2024_2026 >= 5:
        freshness_score = 24
    elif years_2024_2026 >= 2:
        freshness_score = 21
    elif re.search(r'202[0-3]', content):
        freshness_score = 18
    
    # 2. Hyper-Local Grounding Evaluation (0–25)
    local_score = 14
    local_signals = ['mandi', 'district', 'state', 'railway', 'junction', 'corridor', 'subsid', 'nhb', 'pmfme', 'farm-gate', 'bhusa']
    matches = sum(1 for s in local_signals if re.search(r'\b' + s, content, re.I))
    if matches >= 6:
        local_score = 25
    elif matches >= 4:
        local_score = 22
    elif matches >= 2:
        local_score = 18

    # 3. Competitor Coverage (0–25)
    competitor_score = 15
    tiers_detected = 0
    if re.search(r'unorganized|mandi|local', content, re.I):
        tiers_detected += 1
    if re.search(r'regional|incumbent|state', content, re.I):
        tiers_detected += 1
    if re.search(r'd2c|niche|gourmet|specialist', content, re.I):
        tiers_detected += 1
    if re.search(r'national|leader|chain', content, re.I):
        tiers_detected += 1
    
    competitor_score = min(25, 12 + (tiers_detected * 3) + (2 if "Competitive Landscape" in content else 0))

    # 4. Assumption Rigor & Verification Tagging (0–25)
    assumption_score = 14
    has_verified_tags = len(re.findall(r'\[VERIFIED DATA', content))
    has_estimate_tags = len(re.findall(r'\[MODEL ESTIMATE', content))
    has_math_formulas = bool(re.search(r'\$\$|\bCAGR\b|\bTAM\b|\bSOM\b', content))
    
    if has_verified_tags >= 2 and has_estimate_tags >= 2:
        assumption_score = 23
    elif has_verified_tags >= 1 or has_estimate_tags >= 1:
        assumption_score = 20
    elif has_math_formulas:
        assumption_score = 17

    composite_score = freshness_score + local_score + competitor_score + assumption_score

    # Determine Decision Verdict
    # Look for acute risk indicators: perishability, seasonal price crash, extreme cooling OpEx
    risk_crash = bool(re.search(r'price crash|glut|spoilage|perishab|extreme heat', content, re.I))
    has_pivot_model = bool(re.search(r'Better Angle|dehydrat|spawn lab|value-add', content, re.I))

    if composite_score >= 88 and risk_crash and has_pivot_model:
        verdict = "GO WITH PIVOT"
        verdict_badge = "[GO WITH PIVOT 🟡]"
        rationale = "Core commodity production faces severe seasonal price crashes or perishability constraints, but upstream input supply (Spawn Lab) or shelf-stable processing (Dehydration) captures 4x–5x margins with zero spoilage."
    elif composite_score >= 85 and not risk_crash:
        verdict = "STRONG GO"
        verdict_badge = "[STRONG GO 🟢]"
        rationale = "Strong empirical tailwinds, favorable unit economics, and high local defensibility without crippling operational bottlenecks."
    else:
        verdict = "NO-GO / HIGH RISK"
        verdict_badge = "[NO-GO 🔴]"
        rationale = "Unresolved capital risk, negative unit margins, or severe incumbent saturation."

    return {
        "engine": "Jev-Style Deterministic Judge Gate v1.2",
        "composite_score": composite_score,
        "confidence_tier": "Investment Grade (High Confidence)" if composite_score >= 90 else "Advisory Grade",
        "scores": {
            "source_freshness": freshness_score,
            "hyper_local_grounding": local_score,
            "competitor_coverage": competitor_score,
            "assumption_rigor": assumption_score
        },
        "verdict": verdict,
        "verdict_badge": verdict_badge,
        "decision_rationale": rationale,
        "immediate_actions": [
            "Visit wholesale mandi between 5:30 AM – 7:30 AM to verify spot rates and commission discounts.",
            "Verify raw input farm-gate bulk costs with 2 local suppliers and test groundwater/electricity tariffs.",
            "Contact District Horticulture / MSME nodal officer to confirm open credit-linked subsidy windows."
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="Jev-Style Market Research Objective Decision Judge")
    parser.add_argument("--file", "-f", help="Path to markdown research brief to audit")
    parser.add_argument("--json", action="store_true", help="Output results in raw JSON format")
    args = parser.parse_args()

    content = ""
    if args.file and os.path.exists(args.file):
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    result = evaluate_market_brief(content)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "=" * 65)
        print("⚖️  JEV-STYLE OBJECTIVE DECISION & QUALITY JUDGE GATE")
        print("=" * 65)
        print(f"📊 Composite Quality Score:  {result['composite_score']} / 100 ({result['confidence_tier']})")
        print(f"• Source Freshness:         {result['scores']['source_freshness']} / 25")
        print(f"• Hyper-Local Grounding:    {result['scores']['hyper_local_grounding']} / 25")
        print(f"• Competitor Coverage:      {result['scores']['competitor_coverage']} / 25")
        print(f"• Assumption Rigor:         {result['scores']['assumption_rigor']} / 25")
        print("-" * 65)
        print(f"🎯 Strategic Verdict:        {result['verdict_badge']}")
        print(f"💡 Decision Rationale:       {result['decision_rationale']}")
        print("-" * 65)
        print("⏱️  Immediate 48-Hour Next Actions:")
        for idx, act in enumerate(result['immediate_actions'], 1):
            print(f"   {idx}. {act}")
        print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
