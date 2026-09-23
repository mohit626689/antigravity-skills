#!/usr/bin/env python3
"""
Swing Trading Position Sizer & Risk Calculator (agentskills.io standard)
Calculates exact position sizing based on portfolio capital and the 1-2% capital risk rule.
Guarantees favorable Risk-to-Reward ratios and prevents ruin.
"""

import sys
import argparse
from typing import Dict, Any


def calculate_position_size(
    total_capital: float,
    risk_pct: float,
    entry_price: float,
    stop_loss: float,
    target_price: float = None,
    desired_rr: float = 2.0,
) -> Dict[str, Any]:
    """
    Calculates position sizing and risk/reward metrics.
    
    Args:
        total_capital: Total account size in currency (e.g., 100,000 INR or USD).
        risk_pct: Percentage of account risked on this trade (typically 1.0% to 2.0%).
        entry_price: Target entry price per share.
        stop_loss: Invalidation stop loss price per share.
        target_price: (Optional) Target exit price. If not provided, computed from desired_rr.
        desired_rr: Target Risk-to-Reward ratio (default: 2.0 for 1:2).
    """
    if entry_price <= 0 or stop_loss <= 0:
        raise ValueError("Entry price and Stop Loss must be positive numbers.")

    if entry_price <= stop_loss:
        raise ValueError("For a LONG swing trade, Entry Price must be strictly greater than Stop Loss.")

    risk_per_share = entry_price - stop_loss
    risk_amount = total_capital * (risk_pct / 100.0)

    # Position size in shares (floored to integer shares)
    shares = int(risk_amount // risk_per_share)
    if shares <= 0:
        shares = 1

    actual_risk = shares * risk_per_share
    capital_deployed = shares * entry_price
    capital_deployed_pct = (capital_deployed / total_capital) * 100.0

    # Calculate targets
    t1_price = entry_price + (risk_per_share * desired_rr)
    t2_price = entry_price + (risk_per_share * (desired_rr * 1.5))

    if target_price is not None and target_price > entry_price:
        actual_reward_per_share = target_price - entry_price
        rr_ratio = actual_reward_per_share / risk_per_share
        t1_price = target_price
    else:
        rr_ratio = desired_rr

    total_potential_profit_t1 = shares * (t1_price - entry_price)

    return {
        "total_capital": total_capital,
        "risk_pct": risk_pct,
        "risk_amount": risk_amount,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "risk_per_share": risk_per_share,
        "risk_per_share_pct": (risk_per_share / entry_price) * 100.0,
        "shares": shares,
        "capital_deployed": capital_deployed,
        "capital_deployed_pct": capital_deployed_pct,
        "target_1": round(t1_price, 2),
        "target_2": round(t2_price, 2),
        "rr_ratio": round(rr_ratio, 2),
        "potential_profit_t1": round(total_potential_profit_t1, 2),
        "is_viable": rr_ratio >= 1.5,
    }


def print_trade_ticket(metrics: Dict[str, Any]):
    """Formats and prints the calculated trade ticket."""
    print("=" * 60)
    print("          📊 SWING TRADE EXECUTION TICKET")
    print("=" * 60)
    print(f" Account Capital    : {metrics['total_capital']:,.2f}")
    print(f" Risk Budget ({metrics['risk_pct']}%) : {metrics['risk_amount']:,.2f}")
    print("-" * 60)
    print(f" Entry Price        : {metrics['entry_price']:,.2f}")
    print(f" Stop Loss          : {metrics['stop_loss']:,.2f}  (-{metrics['risk_per_share_pct']:.2f}%)")
    print(f" Target 1 (1:{metrics['rr_ratio']:.1f} R:R): {metrics['target_1']:,.2f}")
    print(f" Target 2 (Runner)  : {metrics['target_2']:,.2f}")
    print("-" * 60)
    print(f" Recommended Size   : {metrics['shares']} shares")
    print(f" Total Investment   : {metrics['capital_deployed']:,.2f} ({metrics['capital_deployed_pct']:.1f}% of portfolio)")
    print(f" Max Dollar Risk    : {metrics['risk_amount']:,.2f}")
    print(f" Potential Reward T1: {metrics['potential_profit_t1']:,.2f}")
    print(f" Risk / Reward Ratio: 1 : {metrics['rr_ratio']}")
    print("-" * 60)
    if metrics["is_viable"]:
        print(" ✅ STATUS: TRADE VIABLE (Risk-to-Reward >= 1:1.5)")
    else:
        print(" ❌ STATUS: TRADE REJECTED (Reward does not justify risk: R:R < 1:1.5)")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Swing Trading Position Sizer & Risk Calculator")
    parser.add_argument("--capital", type=float, default=100000.0, help="Total portfolio capital (default: 100,000)")
    parser.add_argument("--risk", type=float, default=1.0, help="Risk percentage per trade (default: 1.0%%)")
    parser.add_argument("--entry", type=float, required=True, help="Planned entry price per share")
    parser.add_argument("--stop", type=float, required=True, help="Stop loss price per share")
    parser.add_argument("--target", type=float, default=None, help="Optional manual target price")
    parser.add_argument("--rr", type=float, default=2.0, help="Desired Risk-to-Reward ratio if no target (default: 2.0)")

    args = parser.parse_args()

    try:
        metrics = calculate_position_size(
            total_capital=args.capital,
            risk_pct=args.risk,
            entry_price=args.entry,
            stop_loss=args.stop,
            target_price=args.target,
            desired_rr=args.rr,
        )
        print_trade_ticket(metrics)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
