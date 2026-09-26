#!/usr/bin/env python3
"""
Portfolio Health & Swing Action Analyzer (agentskills.io standard)
Audits an active swing trading portfolio, evaluates risk/reward for current holdings,
flags danger zones, estimates holding periods, and provides clear action recommendations:
HOLD, BOOK 50% & TRAIL, CUT LOSS, or ACCUMULATE/AVERAGE.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any


def analyze_holding(
    symbol: str,
    qty: int,
    buy_price: float,
    current_price: float,
    stop_loss: float = None,
    target_1: float = None,
    setup_type: str = "swing_pullback",
    category: str = "large_cap",
) -> Dict[str, Any]:
    """
    Evaluates an individual stock holding in a swing trading portfolio.
    """
    invested_val = qty * buy_price
    current_val = qty * current_price
    pnl = current_val - invested_val
    pnl_pct = ((current_price - buy_price) / buy_price) * 100.0

    # Default stop loss if not explicitly tracked (default -5% to -7% from entry)
    if stop_loss is None or stop_loss <= 0:
        stop_loss = buy_price * 0.94

    # Default target if not specified (default 1:2 R:R based on stop)
    risk_per_share = buy_price - stop_loss
    if target_1 is None or target_1 <= 0:
        target_1 = buy_price + (risk_per_share * 2.0)

    # Holding period projection based on setup type
    holding_projections = {
        "breakout": "3 to 7 trading days",
        "swing_pullback": "1 to 2 weeks (5 to 12 trading days)",
        "base_reversal": "2 to 4 weeks (10 to 20 trading days)",
        "long_term_core": "4 to 8 weeks",
    }
    est_holding = holding_projections.get(setup_type.lower(), "5 to 10 trading days")

    # Action Logic & Averaging Down Assessment
    action = "HOLD"
    urgency = "LOW"
    action_reason = ""
    can_average_down = False
    average_down_guidance = ""

    if current_price <= stop_loss:
        action = "🚨 EXIT / CUT LOSS"
        urgency = "HIGH"
        action_reason = f"Price breached invalidation Stop Loss (₹/{current_price:.2f} <= ₹/{stop_loss:.2f}). Swing trade thesis has failed."
        can_average_down = False
        average_down_guidance = "DO NOT AVERAGE DOWN! Averaging down on a broken swing setup causes catastrophic account drawdown."
    elif current_price >= target_1:
        action = "💰 BOOK 50% & TRAIL"
        urgency = "MEDIUM"
        action_reason = f"Target 1 reached (₹/{current_price:.2f} >= ₹/{target_1:.2f}). Lock in half profit and move Stop Loss to Breakeven (₹/{buy_price:.2f})."
        can_average_down = False
        average_down_guidance = "Stock is winning. Do not average down; consider adding on next consolidation breakout (Averaging UP / Pyramiding)."
    elif pnl_pct < -3.0 and current_price > stop_loss:
        # Stock is pulling back but still above stop loss
        if category in ("large_cap", "bluechip", "index"):
            action = "👀 HOLD / MONITOR"
            action_reason = "Pullback is within acceptable stop buffer. Holding structure is intact."
            can_average_down = True
            average_down_guidance = f"Conditional Average Down permitted ONLY if price prints a reversal candle near support (₹/{stop_loss * 1.01:.2f}) and total position size stays under 10% of portfolio."
        else:
            action = "⚠️ HOLD (TIGHTEN STOP)"
            action_reason = "Mid/small-cap in drawdown. Do not add risk until recovery is confirmed."
            can_average_down = False
            average_down_guidance = "DO NOT AVERAGE DOWN on high-beta / mid-cap stocks without a confirmed trend reversal."
    elif pnl_pct >= 2.0:
        action = "🚀 HOLD (RUNNER)"
        action_reason = f"In profit (+{pnl_pct:.1f}%). Riding momentum toward Target 1 (₹/{target_1:.2f})."
        can_average_down = False
        average_down_guidance = "Winning trade. Add shares only on breakout continuation (Pyramiding), not on dips."
    else:
        action = "⏳ HOLD (CONSOLIDATION)"
        action_reason = "Price hovering near cost basis. Allow trade room to develop."
        can_average_down = False
        average_down_guidance = "Position size is adequate; let the setup play out."

    return {
        "symbol": symbol.upper(),
        "qty": qty,
        "buy_price": round(buy_price, 2),
        "current_price": round(current_price, 2),
        "invested_val": round(invested_val, 2),
        "current_val": round(current_val, 2),
        "pnl": round(pnl, 2),
        "pnl_pct": round(pnl_pct, 2),
        "stop_loss": round(stop_loss, 2),
        "target_1": round(target_1, 2),
        "action": action,
        "urgency": urgency,
        "action_reason": action_reason,
        "estimated_holding_days": est_holding,
        "can_average_down": can_average_down,
        "average_down_guidance": average_down_guidance,
    }


def analyze_portfolio(holdings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Evaluates the complete portfolio and checks risk allocation."""
    analyzed_holdings = []
    total_invested = 0.0
    total_current = 0.0

    for h in holdings:
        res = analyze_holding(
            symbol=h.get("symbol", "UNKNOWN"),
            qty=int(h.get("qty", 1)),
            buy_price=float(h.get("buy_price", 0.0)),
            current_price=float(h.get("current_price", 0.0)),
            stop_loss=h.get("stop_loss"),
            target_1=h.get("target_1"),
            setup_type=h.get("setup_type", "swing_pullback"),
            category=h.get("category", "large_cap"),
        )
        total_invested += res["invested_val"]
        total_current += res["current_val"]
        analyzed_holdings.append(res)

    total_pnl = total_current - total_invested
    total_pnl_pct = (total_pnl / total_invested * 100.0) if total_invested > 0 else 0.0

    # Calculate concentration %
    warnings = []
    for h in analyzed_holdings:
        conc_pct = (h["invested_val"] / total_invested * 100.0) if total_invested > 0 else 0.0
        h["portfolio_concentration_pct"] = round(conc_pct, 1)
        if conc_pct > 25.0:
            warnings.append(f"⚠️ {h['symbol']} makes up {conc_pct:.1f}% of your portfolio. Over-concentrated for swing trading (keep under 15-20% per position).")

    return {
        "total_invested": round(total_invested, 2),
        "total_current": round(total_current, 2),
        "total_pnl": round(total_pnl, 2),
        "total_pnl_pct": round(total_pnl_pct, 2),
        "holdings": analyzed_holdings,
        "concentration_warnings": warnings,
    }


def print_portfolio_report(report: Dict[str, Any]):
    """Prints a structured ASCII portfolio report."""
    print("=" * 80)
    print("               📊 SWING TRADING PORTFOLIO HEALTH & ACTION REPORT")
    print("=" * 80)
    print(f" Total Invested : {report['total_invested']:,.2f}")
    print(f" Current Value  : {report['total_current']:,.2f}")
    pnl_sign = "+" if report['total_pnl'] >= 0 else ""
    print(f" Overall P&L    : {pnl_sign}{report['total_pnl']:,.2f} ({pnl_sign}{report['total_pnl_pct']:.2f}%)")
    print("-" * 80)
    print(f" {'SYMBOL':<10} {'QTY':<5} {'AVG BUY':<9} {'CMP':<9} {'P&L %':<8} {'WEIGHT':<8} {'ACTION':<20}")
    print("-" * 80)
    for h in report["holdings"]:
        pnl_str = f"{'+' if h['pnl_pct'] >= 0 else ''}{h['pnl_pct']:.1f}%"
        print(f" {h['symbol']:<10} {h['qty']:<5} {h['buy_price']:<9.2f} {h['current_price']:<9.2f} {pnl_str:<8} {h['portfolio_concentration_pct']:<7.1f}% {h['action']:<20}")

    print("-" * 80)
    print(" 🎯 DETAILED ACTION & HOLDING RECOMMENDATIONS:")
    for h in report["holdings"]:
        print(f"\n • {h['symbol']} ({h['action']}):")
        print(f"   - Status/Reason    : {h['action_reason']}")
        print(f"   - Target Duration  : Hold for approx. {h['estimated_holding_days']}")
        print(f"   - Averaging Advice : {h['average_down_guidance']}")

    if report["concentration_warnings"]:
        print("\n ⚠️ RISK ALLOCATION ALERTS:")
        for w in report["concentration_warnings"]:
            print(f"   {w}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Swing Trading Portfolio Analyzer")
    parser.add_argument("--file", type=str, default=None, help="JSON file with portfolio holdings array")
    parser.add_argument("--demo", action="store_true", help="Run with demo sample portfolio")

    args = parser.parse_args()

    holdings = []
    target_file = args.file
    if not target_file and not args.demo:
        default_path = Path(__file__).parent.parent / "data" / "portfolio.json"
        if default_path.exists():
            target_file = str(default_path)

    if target_file:
        try:
            with open(target_file, "r") as f:
                raw_data = json.load(f)
                if isinstance(raw_data, dict) and "holdings" in raw_data:
                    raw_holdings = raw_data["holdings"]
                else:
                    raw_holdings = raw_data
                for item in raw_holdings:
                    if "current_price" not in item and "cmp" in item:
                        item["current_price"] = item["cmp"]
                    holdings.append(item)
        except Exception as e:
            print(f"Error loading {target_file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Default realistic demo portfolio
        holdings = [
            {"symbol": "RELIANCE", "qty": 25, "buy_price": 2420.0, "current_price": 2510.0, "stop_loss": 2360.0, "target_1": 2540.0, "setup_type": "breakout", "category": "large_cap"},
            {"symbol": "TATASTEEL", "qty": 200, "buy_price": 160.0, "current_price": 149.0, "stop_loss": 150.0, "target_1": 178.0, "setup_type": "swing_pullback", "category": "large_cap"},
            {"symbol": "INFY", "qty": 40, "buy_price": 1820.0, "current_price": 1835.0, "stop_loss": 1770.0, "target_1": 1920.0, "setup_type": "swing_pullback", "category": "large_cap"},
            {"symbol": "ZOMATO", "qty": 150, "buy_price": 280.0, "current_price": 272.0, "stop_loss": 262.0, "target_1": 315.0, "setup_type": "breakout", "category": "mid_cap"},
        ]

    report = analyze_portfolio(holdings)
    print_portfolio_report(report)


if __name__ == "__main__":
    main()
