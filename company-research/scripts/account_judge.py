#!/usr/bin/env python3
"""
Jev-Style Objective Account Decision Judge Gate — Company Research
Inspired by the TypeSafe Jev System-1 Decision Architecture.
100% Free, Deterministic, and Repeatable.
"""

import sys
import os
import re
import json
import argparse


def judge_company_account(content: str = "", company_name: str = "TARGET") -> dict:
    """
    Evaluates a company research brief or parameters against strict institutional due-diligence rubrics.
    Returns composite score, category breakdown, account verdict, and strategic call openers.
    """
    # 1. Financial Health & Budget Viability (0–25)
    financial_score = 14
    if re.search(r'series [c-z]|profitable|profitable growth|ipo|public|10-k|arr\s*>\s*\$?10m', content, re.I):
        financial_score = 24
    elif re.search(r'series [a-b]|venture-backed|growth round|arr\s*>\s*\$?2m', content, re.I):
        financial_score = 21
    elif re.search(r'seed|pre-seed|bootstrapped|micro', content, re.I):
        financial_score = 16

    # 2. Product & Tech Stack Moat (0–25)
    tech_score = 15
    tech_signals = ['aws', 'gcp', 'azure', 'kubernetes', 'cloud', 'api', 'proprietary', 'patents', 'ai', 'microservices']
    detected_tech = sum(1 for t in tech_signals if re.search(r'\b' + t + r'\b', content, re.I))
    tech_score = min(25, 12 + (detected_tech * 2))

    # 3. Buying Committee Accessibility (0–25)
    buying_score = 14
    committee_roles = ['economic buyer', 'champion', 'technical evaluator', 'cfo', 'cto', 'vp', 'head of']
    detected_roles = sum(1 for r in committee_roles if re.search(r'\b' + r + r'\b', content, re.I))
    if detected_roles >= 4:
        buying_score = 25
    elif detected_roles >= 2:
        buying_score = 21
    else:
        buying_score = 17

    # 4. Landmine & Risk Radar (0–25)
    risk_score = 22  # Start high, penalize on red flags
    red_flags = ['layoffs', 'churn', 'lawsuit', 'controversy', 'turnover', 'restructuring', 'burn rate']
    flag_count = sum(1 for f in red_flags if re.search(r'\b' + f + r'\b', content, re.I))
    risk_score = max(5, 25 - (flag_count * 5))

    composite_score = financial_score + tech_score + buying_score + risk_score

    # Deterministic Verdict Gate
    if risk_score <= 10 or (flag_count >= 3 and financial_score < 18):
        verdict = "DISQUALIFY / RED FLAG"
        badge = "[DISQUALIFY / RED FLAG 🔴]"
        strategy = "Severe organizational instability, high executive churn, or distress signals detected. Not recommended for high-touch sales outreach."
    elif composite_score >= 84 and risk_score >= 18:
        verdict = "PRIME TARGET"
        badge = "[PRIME TARGET 🟢]"
        strategy = "High willingness-to-pay, modern infrastructure, clearly identified decision makers, and healthy balance sheet. Prioritize for executive meeting."
    else:
        verdict = "QUALIFY CAREFULLY"
        badge = "[QUALIFY CAREFULLY 🟡]"
        strategy = "Viable opportunity with budget potential, but requires validating specific decision-making authority and timeline blockers during discovery."

    return {
        "engine": "Jev-Style Account Decision Judge Gate v1.2",
        "company": company_name,
        "composite_score": composite_score,
        "account_tier": "Tier-1 Enterprise / Strategic Account" if composite_score >= 85 else ("Tier-2 Qualified Account" if composite_score >= 70 else "High Friction / Unqualified"),
        "scores": {
            "financial_budget_viability": financial_score,
            "tech_stack_moat": tech_score,
            "buying_committee_accessibility": buying_score,
            "landmine_safety": risk_score
        },
        "verdict": verdict,
        "verdict_badge": badge,
        "recommended_strategy": strategy,
        "pre_meeting_actions": [
            "Validate whether the economic buyer has direct budget sign-off vs. committee consensus.",
            "Reference their recent infrastructure / growth milestone as the conversational anchor.",
            "Probe on the single highest operational friction point without triggering defensiveness."
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="Jev-Style Account Decision Judge Gate")
    parser.add_argument("--file", "-f", help="Path to company markdown brief or dossier")
    parser.add_argument("--company", "-c", default="Target Account", help="Company Name")
    parser.add_argument("--json", action="store_true", help="Output in raw JSON format")
    args = parser.parse_args()

    content = ""
    if args.file and os.path.exists(args.file):
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    result = judge_company_account(content=content, company_name=args.company)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "=" * 65)
        print(f"⚖️  JEV-STYLE OBJECTIVE ACCOUNT DECISION JUDGE: {result['company']}")
        print("=" * 65)
        print(f"📊 Account Quality Score:   {result['composite_score']} / 100 ({result['account_tier']})")
        print(f"• Financial & Budget:      {result['scores']['financial_budget_viability']} / 25")
        print(f"• Tech Stack & Moats:      {result['scores']['tech_stack_moat']} / 25")
        print(f"• Buying Committee Access: {result['scores']['buying_committee_accessibility']} / 25")
        print(f"• Landmine & Risk Safety:  {result['scores']['landmine_safety']} / 25")
        print("-" * 65)
        print(f"🎯 Account Verdict:        {result['verdict_badge']}")
        print(f"💡 Recommended Strategy:   {result['recommended_strategy']}")
        print("-" * 65)
        print("📋 Pre-Meeting Tactical Actions:")
        for idx, act in enumerate(result['pre_meeting_actions'], 1):
            print(f"   {idx}. {act}")
        print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
