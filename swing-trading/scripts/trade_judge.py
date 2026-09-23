#!/usr/bin/env python3
"""
Jev-Style Objective Trade Decision Judge Gate — Swing Trading
Inspired by the TypeSafe Jev System-1 Decision Architecture.
100% Free, Deterministic, and Quantitative.
"""

import sys
import json
import argparse


def judge_trade_setup(
    ticker: str,
    price: float,
    stop_loss: float,
    target: float,
    sma_200: float = None,
    sma_50: float = None,
    ema_20: float = None,
    rsi_14: float = None,
    volume_ratio: float = 1.0,
    days_to_earnings: int = 30
) -> dict:
    """
    Evaluates a swing trading setup against strict mathematical risk and technical rubrics.
    Returns composite score, category breakdown, deterministic verdict, and execution parameters.
    """
    # 1. Trend Confluence Score (0–25)
    trend_score = 12
    if sma_200 is not None and price > sma_200:
        trend_score += 7
    if sma_50 is not None and price > sma_50:
        trend_score += 4
    if ema_20 is not None and price > ema_20:
        trend_score += 2
    trend_score = min(25, trend_score)

    # 2. Momentum & Volume Signature (0–25)
    momentum_score = 10
    if volume_ratio >= 1.5:
        momentum_score += 8
    elif volume_ratio >= 1.2:
        momentum_score += 5
    elif volume_ratio >= 1.0:
        momentum_score += 2

    if rsi_14 is not None:
        if 48.0 <= rsi_14 <= 65.0:
            momentum_score += 7  # Sweet spot
        elif 40.0 <= rsi_14 < 48.0:
            momentum_score += 4  # Pullback zone
        elif 65.0 < rsi_14 <= 72.0:
            momentum_score += 2
        else:
            momentum_score -= 3  # Overbought >75 or oversold breakdown
    else:
        momentum_score += 4
    momentum_score = max(0, min(25, momentum_score))

    # 3. Mathematical Risk-to-Reward (0–25)
    risk = abs(price - stop_loss)
    reward = abs(target - price)
    rr_ratio = reward / risk if risk > 0 else 0.0

    if rr_ratio >= 3.0:
        rr_score = 25
    elif rr_ratio >= 2.5:
        rr_score = 22
    elif rr_ratio >= 2.0:
        rr_score = 18
    elif rr_ratio >= 1.5:
        rr_score = 10
    else:
        rr_score = 0  # Strict rejection if R:R < 1:1.5

    # 4. Binary Event & Extension Safety (0–25)
    safety_score = 15
    if days_to_earnings is not None:
        if days_to_earnings < 3:
            safety_score = 0  # Critical disqualifier
        elif days_to_earnings < 7:
            safety_score = 8
        else:
            safety_score = 15

    # Extension penalty if stock is too far from 20 EMA
    if ema_20 is not None and ema_20 > 0:
        extension_pct = ((price - ema_20) / ema_20) * 100.0
        if extension_pct <= 3.5:
            safety_score += 10
        elif extension_pct <= 5.5:
            safety_score += 6
        else:
            safety_score -= 5  # Chasing extended stock
    else:
        safety_score += 8

    safety_score = max(0, min(25, safety_score))
    composite_score = trend_score + momentum_score + rr_score + safety_score

    # Deterministic Verdict Gate
    if days_to_earnings < 3:
        verdict = "NO-TRADE / EARNINGS BLACKOUT"
        badge = "[NO-TRADE / AVOID 🔴]"
        action = "Binary earnings event within 72 hours. Flat risk rule: Do not take new positions into earnings."
    elif rr_ratio < 2.0:
        verdict = "REJECT / UNFAVORABLE RISK-REWARD"
        badge = "[NO-TRADE / AVOID 🔴]"
        action = f"Risk-to-reward ({rr_ratio:.1f}:1) fails the mandatory 1:2.0 threshold. Reject or find a tighter logical stop."
    elif composite_score >= 84 and rr_ratio >= 2.0:
        verdict = "STRONG BUY"
        badge = "[STRONG BUY 🟢]"
        action = "High-confluence A+ swing setup. Clear trend, volume confirmation, and asymmetric reward. Allocate full 1.0% risk."
    elif 70 <= composite_score < 84:
        if ema_20 and ((price - ema_20) / ema_20) * 100.0 > 4.5:
            verdict = "WAIT FOR PULLBACK"
            badge = "[WAIT FOR PULLBACK 🟡]"
            action = "Stock has momentum but is slightly extended (>4.5% above 20 EMA). Set alert near 20 EMA dip before triggering order."
        else:
            verdict = "TACTICAL BUY"
            badge = "[TACTICAL BUY 🟢]"
            action = "Solid B+ swing setup. Favorable trend and reward. Execute with standard risk."
    else:
        verdict = "AVOID"
        badge = "[NO-TRADE / AVOID 🔴]"
        action = "Insufficient technical confluence or sub-optimal momentum score. Pass and monitor watchlist."

    return {
        "engine": "Jev-Style Quantitative Trade Judge Gate v1.2",
        "ticker": ticker.upper(),
        "composite_score": composite_score,
        "quality_tier": "A+ Institutional Setup" if composite_score >= 85 else ("B+ Tactical Setup" if composite_score >= 70 else "Sub-Standard / Avoid"),
        "scores": {
            "trend_confluence": trend_score,
            "momentum_volume": momentum_score,
            "risk_reward": rr_score,
            "event_safety": safety_score
        },
        "metrics": {
            "entry_price": price,
            "stop_loss": stop_loss,
            "target": target,
            "risk_per_share": round(risk, 2),
            "reward_per_share": round(reward, 2),
            "risk_reward_ratio": round(rr_ratio, 2)
        },
        "verdict": verdict,
        "verdict_badge": badge,
        "actionable_guidance": action
    }


def main():
    parser = argparse.ArgumentParser(description="Jev-Style Quantitative Trade Decision Judge")
    parser.add_argument("--ticker", "-t", required=True, help="Stock ticker symbol (e.g. RELIANCE, NVDA)")
    parser.add_argument("--price", "-p", type=float, required=True, help="Current or planned entry price")
    parser.add_argument("--stop", "-s", type=float, required=True, help="Planned stop loss price")
    parser.add_argument("--target", "-g", type=float, required=True, help="Target price")
    parser.add_argument("--sma200", type=float, default=None, help="200-day Simple Moving Average")
    parser.add_argument("--sma50", type=float, default=None, help="50-day Simple Moving Average")
    parser.add_argument("--ema20", type=float, default=None, help="20-day Exponential Moving Average")
    parser.add_argument("--rsi", type=float, default=55.0, help="RSI(14) value")
    parser.add_argument("--volume-ratio", type=float, default=1.3, help="Volume vs 20-day average ratio (e.g. 1.5 = +50%%)")
    parser.add_argument("--earnings-days", type=int, default=20, help="Trading days until next earnings release")
    parser.add_argument("--json", action="store_true", help="Output in raw JSON format")
    args = parser.parse_args()

    result = judge_trade_setup(
        ticker=args.ticker,
        price=args.price,
        stop_loss=args.stop,
        target=args.target,
        sma_200=args.sma200,
        sma_50=args.sma50,
        ema_20=args.ema20,
        rsi_14=args.rsi,
        volume_ratio=args.volume_ratio,
        days_to_earnings=args.earnings_days
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "=" * 65)
        print(f"⚖️  JEV-STYLE OBJECTIVE TRADE DECISION JUDGE: {result['ticker']}")
        print("=" * 65)
        print(f"📊 Setup Quality Score:   {result['composite_score']} / 100 ({result['quality_tier']})")
        print(f"• Trend Confluence:       {result['scores']['trend_confluence']} / 25")
        print(f"• Momentum & Volume:      {result['scores']['momentum_volume']} / 25")
        print(f"• Risk-to-Reward (R:R):   {result['scores']['risk_reward']} / 25  (Ratio: {result['metrics']['risk_reward_ratio']}:1)")
        print(f"• Event & Safety:         {result['scores']['event_safety']} / 25")
        print("-" * 65)
        print(f"🎯 Execution Verdict:     {result['verdict_badge']}")
        print(f"💡 Tactical Action:       {result['actionable_guidance']}")
        print("-" * 65)
        print(f"💵 Parameters: Entry: {result['metrics']['entry_price']} | Stop: {result['metrics']['stop_loss']} | Target: {result['metrics']['target']}")
        print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
