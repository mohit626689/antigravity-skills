#!/usr/bin/env python3
"""
Jev-Style Objective Proposal Decision Judge Gate — Client Proposal
Inspired by the TypeSafe Jev System-1 Decision Architecture.
100% Free, Deterministic, and Conversion-Optimized.
"""

import sys
import os
import re
import json
import argparse


def judge_proposal(content: str = "", client_name: str = "Client") -> dict:
    """
    Evaluates a client proposal against strict conversion, trust, and margin defensibility rubrics.
    Returns composite score, category breakdown, deal verdict, and pre-send action items.
    """
    # 1. Pain & Cost-of-Inaction Clarity (0–25)
    pain_score = 14
    pain_signals = ['cost of inaction', 'bottleneck', 'hours lost', 'wasted', 'friction', 'manual delay', 'delay', 'dropped']
    detected_pain = sum(1 for p in pain_signals if re.search(r'\b' + p + r'\b', content, re.I))
    if detected_pain >= 4 or re.search(r'\$\d+[\d,]*\s*/\s*(?:mo|month|yr|year)', content):
        pain_score = 24
    elif detected_pain >= 2:
        pain_score = 20
    else:
        pain_score = 16

    # 2. Measurable Before vs. After Contrast (0–25)
    transform_score = 12
    has_table = bool(re.search(r'\|\s*Operational Dimension|\|\s*Before\s*\|', content, re.I))
    has_metrics = bool(re.search(r'\d+%\s*(?:reduction|increase|faster)|under \d+ seconds|zero hours', content, re.I))
    if has_table and has_metrics:
        transform_score = 25
    elif has_table or has_metrics:
        transform_score = 20
    else:
        transform_score = 14

    # 3. Scope & Deliverable Boundary Protection (0–25)
    scope_score = 14
    has_deliverables = len(re.findall(r'###\s*Deliverable\s*\d+', content, re.I))
    has_plain_english = bool(re.search(r'What You Get|Why It Matters', content, re.I))
    if has_deliverables >= 3 and has_plain_english:
        scope_score = 24
    elif has_deliverables >= 2:
        scope_score = 20
    else:
        scope_score = 15

    # 4. Pricing Defensibility & ROI Ratio (0–25)
    pricing_score = 14
    has_3_tiers = bool(re.search(r'Tier 1|Tier 2|Tier 3|Basic|Growth|Enterprise', content, re.I))
    has_recommended = bool(re.search(r'Recommended|Anchor|Most Popular', content, re.I))
    has_roi = bool(re.search(r'ROI|payback|value generated|annual return', content, re.I))
    
    if has_3_tiers and has_recommended and has_roi:
        pricing_score = 25
    elif has_3_tiers:
        pricing_score = 21
    else:
        pricing_score = 16

    composite_score = pain_score + transform_score + scope_score + pricing_score

    # Deterministic Deal Verdict
    if composite_score >= 85 and transform_score >= 20 and pricing_score >= 20:
        verdict = "READY TO PITCH"
        badge = "[READY TO PITCH 🟢]"
        advice = "High win-probability proposal. Clear cost of inaction, strong before/after contrast, and defended pricing tiers. Send with confidence."
    elif composite_score >= 70:
        verdict = "SCOPE REVISION NEEDED"
        badge = "[SCOPE REVISION NEEDED 🟡]"
        advice = "Solid foundation, but tighten the deliverable boundaries or strengthen the before/after contrast table before sending to executive buyers."
    else:
        verdict = "MARGIN RISK / PASS"
        badge = "[MARGIN RISK / DO NOT PURSUE 🔴]"
        advice = "Unclear scope boundaries, missing ROI justification, or high vulnerability to client scope creep. Refactor offer before pitching."

    return {
        "engine": "Jev-Style Proposal Decision Judge Gate v1.2",
        "client": client_name,
        "composite_score": composite_score,
        "deal_confidence_tier": "High Conversion Probability (Investment-Grade Offer)" if composite_score >= 85 else ("Moderate Probability" if composite_score >= 70 else "High Friction"),
        "scores": {
            "pain_cost_of_inaction": pain_score,
            "transformation_contrast": transform_score,
            "scope_boundary_protection": scope_score,
            "pricing_roi_defensibility": pricing_score
        },
        "verdict": verdict,
        "verdict_badge": badge,
        "pitch_advice": advice,
        "pre_send_checklist": [
            "Verify that Tier 2 (Recommended) is visually anchored as the highest-value option.",
            "Confirm that technical AI jargon is translated into business capabilities (e.g. speed, hours saved).",
            "Include an interactive demo or Loom video link to eliminate client trust hesitation."
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="Jev-Style Proposal Decision Judge Gate")
    parser.add_argument("--file", "-f", help="Path to proposal markdown file")
    parser.add_argument("--client", "-c", default="Prospective Client", help="Client Name")
    parser.add_argument("--json", action="store_true", help="Output in raw JSON format")
    args = parser.parse_args()

    content = ""
    if args.file and os.path.exists(args.file):
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    result = judge_proposal(content=content, client_name=args.client)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "=" * 65)
        print(f"⚖️  JEV-STYLE OBJECTIVE PROPOSAL DECISION JUDGE: {result['client']}")
        print("=" * 65)
        print(f"📊 Proposal Quality Score: {result['composite_score']} / 100 ({result['deal_confidence_tier']})")
        print(f"• Pain & Inaction Clarity: {result['scores']['pain_cost_of_inaction']} / 25")
        print(f"• Before / After Contrast: {result['scores']['transformation_contrast']} / 25")
        print(f"• Scope Boundary Safety:   {result['scores']['scope_boundary_protection']} / 25")
        print(f"• Pricing & ROI Defense:   {result['scores']['pricing_roi_defensibility']} / 25")
        print("-" * 65)
        print(f"🎯 Deal Verdict:           {result['verdict_badge']}")
        print(f"💡 Pitch Strategy:         {result['pitch_advice']}")
        print("-" * 65)
        print("📋 Pre-Send Quality Checklist:")
        for idx, act in enumerate(result['pre_send_checklist'], 1):
            print(f"   {idx}. {act}")
        print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
