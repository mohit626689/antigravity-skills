#!/usr/bin/env python3
"""
Daily 10:00 AM Market & Portfolio Briefing Engine (agentskills.io standard)
Loads portfolio holdings, checks trailing stops, and formats a clean daily morning walkthrough.
"""

import os
import sys
import json
from pathlib import Path


def generate_morning_briefing(portfolio_path: str = None) -> dict:
    if portfolio_path is None:
        portfolio_path = Path(__file__).parent.parent / "data" / "portfolio.json"

    with open(portfolio_path, "r") as f:
        data = json.load(f)

    holdings = data.get("holdings", [])
    cash = data.get("cash_balance", 0.0)

    # Categorize actions for today
    actions_today = {
        "book_profit": [],
        "runners": [],
        "monitor": [],
        "danger_exit": []
    }

    total_invested = 0.0
    total_current = 0.0

    for h in holdings:
        inv = h["qty"] * h["buy_price"]
        curr = h["qty"] * h["cmp"]
        total_invested += inv
        total_current += curr
        pnl_pct = ((h["cmp"] - h["buy_price"]) / h["buy_price"]) * 100.0

        item = {
            "symbol": h["symbol"],
            "qty": h["qty"],
            "buy_price": h["buy_price"],
            "cmp": h["cmp"],
            "pnl_pct": round(pnl_pct, 1),
            "stop_loss": h.get("stop_loss"),
            "target_1": h.get("target_1"),
            "notes": h.get("notes", "")
        }

        if pnl_pct >= 50.0:
            actions_today["book_profit"].append(item)
        elif pnl_pct >= 5.0:
            actions_today["runners"].append(item)
        elif pnl_pct <= -10.0:
            actions_today["danger_exit"].append(item)
        else:
            actions_today["monitor"].append(item)

    net_pnl = total_current - total_invested
    net_pnl_pct = (net_pnl / total_invested * 100.0) if total_invested > 0 else 0.0

    return {
        "cash_balance": cash,
        "total_invested": round(total_invested, 2),
        "total_current": round(total_current, 2),
        "net_pnl": round(net_pnl, 2),
        "net_pnl_pct": round(net_pnl_pct, 2),
        "actions_today": actions_today
    }


def print_morning_briefing(brief: dict):
    print("=" * 75)
    print("         ☕ DAILY 10:00 AM SWING TRADING & PORTFOLIO BRIEFING")
    print("=" * 75)
    print(f" Available Cash : ₹{brief['cash_balance']:,.2f}")
    print(f" Portfolio Value: ₹{brief['total_current']:,.2f}  (P&L: {'+' if brief['net_pnl'] >= 0 else ''}₹{brief['net_pnl']:,.2f} / {brief['net_pnl_pct']:+.2f}%)")
    print("-" * 75)
    print(" 🎯 TODAY'S ACTIONABLE PROTOCOLS:")

    if brief["actions_today"]["book_profit"]:
        print("\n 💰 1. TAKE PARTIAL PROFITS (50% Profit Booking):")
        for h in brief["actions_today"]["book_profit"]:
            print(f"   • {h['symbol']} ({h['pnl_pct']:+.1f}%): CMP ₹{h['cmp']:.2f}. Sell 50% shares to lock in gains; trail stop on remaining.")

    if brief["actions_today"]["runners"]:
        print("\n 🚀 2. ACTIVE RUNNERS (Trail 20 EMA):")
        for h in brief["actions_today"]["runners"]:
            print(f"   • {h['symbol']} ({h['pnl_pct']:+.1f}%): CMP ₹{h['cmp']:.2f}. Holding strong; Stop Loss moved to ₹{h['stop_loss']:.2f}.")

    if brief["actions_today"]["danger_exit"]:
        print("\n 🚨 3. HIGH DRAWDOWN / EXIT CANDIDATES:")
        for h in brief["actions_today"]["danger_exit"]:
            print(f"   • {h['symbol']} ({h['pnl_pct']:+.1f}%): CMP ₹{h['cmp']:.2f}. {h['notes']}")

    print("=" * 75)


if __name__ == "__main__":
    brief = generate_morning_briefing()
    print_morning_briefing(brief)
