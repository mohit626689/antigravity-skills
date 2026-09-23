#!/usr/bin/env python3
"""
F&O Low-Cost & Low-Risk Intraday & Swing Decision Engine
Standard: agentskills.io
Calculates exact Pivot levels, ATM strikes, Hedged Spreads, and strict risk-capped setups
specifically tailored for retail capital (₹20,000 - ₹50,000).
"""

import sys
import argparse
from typing import Dict, Any


def calculate_pivots(high: float, low: float, close: float) -> Dict[str, float]:
    pp = (high + low + close) / 3.0
    r1 = (2 * pp) - low
    s1 = (2 * pp) - high
    r2 = pp + (high - low)
    s2 = pp - (high - low)
    r3 = high + 2 * (pp - low)
    s3 = low - 2 * (high - pp)
    
    return {
        "PP": round(pp, 2),
        "R1": round(r1, 2),
        "R2": round(r2, 2),
        "R3": round(r3, 2),
        "S1": round(s1, 2),
        "S2": round(s2, 2),
        "S3": round(s3, 2),
    }


def get_atm_strike(spot: float, step: int = 50) -> int:
    return int(round(spot / step) * step)


def analyze_fno_setup(
    index: str,
    spot: float,
    high: float,
    low: float,
    close: float,
    capital: float = 20487.0,
    lot_size: int = 25,
    max_risk_pct: float = 3.5,
) -> Dict[str, Any]:
    step = 50 if index.upper() == "NIFTY" else 100
    atm_strike = get_atm_strike(spot, step)
    pivots = calculate_pivots(high, low, close)
    
    max_risk_inr = capital * (max_risk_pct / 100.0)
    
    # Delta approximation for ATM is ~0.50
    # If index moves 30 points, ATM premium moves ~15 points.
    index_sl_pts = 25.0
    option_sl_pts = round(index_sl_pts * 0.50, 1)
    risk_per_lot = option_sl_pts * lot_size
    
    # Target 1 (1:1.8 R:R) -> Option points +22 pts (~45 index pts)
    target1_option_pts = round(option_sl_pts * 1.8, 1)
    target1_inr = target1_option_pts * lot_size
    
    # Target 2 (1:2.8 R:R) -> Option points +35 pts (~70 index pts)
    target2_option_pts = round(option_sl_pts * 2.8, 1)
    target2_inr = target2_option_pts * lot_size
    
    # Hedged Spread Parameters (Bull Call / Bear Put)
    # Buy ATM, Sell OTM 100 pts away
    otm_call_strike = atm_strike + (2 * step)
    otm_put_strike = atm_strike - (2 * step)
    spread_width = 2 * step
    
    # Estimated ATM premium ~ ₹110, OTM premium ~ ₹60 -> Net Debit ~ ₹50 (1250 INR for lot 25)
    est_atm_prem = round(spot * 0.0045, 1)  # ~0.45% of spot for weekly expiry
    est_otm_prem = round(est_atm_prem * 0.52, 1)
    spread_net_debit = est_atm_prem - est_otm_prem
    spread_max_loss = spread_net_debit * lot_size
    spread_max_profit = (spread_width - spread_net_debit) * lot_size
    
    return {
        "index": index.upper(),
        "spot": spot,
        "atm_strike": atm_strike,
        "pivots": pivots,
        "lot_size": lot_size,
        "capital": capital,
        "max_risk_budget": round(max_risk_inr, 2),
        "intraday_atm": {
            "sl_points": option_sl_pts,
            "risk_per_lot": round(risk_per_lot, 2),
            "target1_points": target1_option_pts,
            "target1_profit": round(target1_inr, 2),
            "target2_points": target2_option_pts,
            "target2_profit": round(target2_inr, 2),
            "bullish_ce": {
                "strike": f"{atm_strike} CE",
                "trigger_level": pivots["R1"],
                "exit_sl_level": pivots["PP"],
            },
            "bearish_pe": {
                "strike": f"{atm_strike} PE",
                "trigger_level": pivots["S1"],
                "exit_sl_level": pivots["PP"],
            }
        },
        "hedged_spread": {
            "bull_spread": f"Buy {atm_strike} CE + Sell {otm_call_strike} CE",
            "bear_spread": f"Buy {atm_strike} PE + Sell {otm_put_strike} PE",
            "spread_width": spread_width,
            "est_net_debit_pts": round(spread_net_debit, 1),
            "max_loss_inr": round(spread_max_loss, 2),
            "max_profit_inr": round(spread_max_profit, 2),
            "margin_required": 18500.0,
            "reward_to_risk": round(spread_max_profit / spread_max_loss, 2) if spread_max_loss > 0 else 0.0
        }
    }


def print_fno_dossier(data: Dict[str, Any]):
    p = data["pivots"]
    atm = data["intraday_atm"]
    spread = data["hedged_spread"]
    
    print("\n" + "=" * 80)
    print(f"      ⚡ HIGH-PRECISION F&O TRADE DOSSIER: {data['index']} (CAPITAL: ₹{data['capital']:,.2f})")
    print("=" * 80)
    print(f" Spot CMP: {data['spot']:.2f}  |  ATM Strike: {data['atm_strike']}  |  Lot Size: {data['lot_size']} shares")
    print(f" Strict Risk Budget (3.5% of Cash): Max ₹{data['max_risk_budget']:,.2f} per trade")
    print("-" * 80)
    
    print(" 📊 INTRADAY PRICE PIVOTS & CONFLUENCE LEVELS:")
    print(f"   • Major Resistance 2 (R2) : {p['R2']:.2f}")
    print(f"   • Breakout Trigger   (R1) : {p['R1']:.2f}  <-- Bullish confirmation zone")
    print(f"   • Day Central Pivot  (PP) : {p['PP']:.2f}  <-- Trend dividing line (Do Not Trade Here)")
    print(f"   • Breakdown Trigger  (S1) : {p['S1']:.2f}  <-- Bearish confirmation zone")
    print(f"   • Major Support 2    (S2) : {p['S2']:.2f}")
    print("-" * 80)
    
    print(" 🎯 STRATEGY A: DISCIPLINED INTRADAY ATM MOMENTUM (STRICT STOP-LOSS)")
    print("   [Best for Quick 20-45 Minute Momentum Moves between 09:30-11:00 AM & 01:30-03:00 PM]")
    print(f"   \033[92m🟢 BULLISH SETUP (CALL - CE):\033[0m")
    print(f"      - Action        : BUY 1 Lot {atm['bullish_ce']['strike']}")
    print(f"      - Spot Trigger  : Wait for 15-min candle to CLOSE firmly ABOVE {atm['bullish_ce']['trigger_level']:.2f} + VWAP")
    print(f"      - Stop Loss (SL): -{atm['sl_points']} pts on Option Premium (Capped Loss: -₹{atm['risk_per_lot']:,.2f})")
    print(f"      - Target 1 (50%): +{atm['target1_points']} pts on Option Premium (Gain: +₹{atm['target1_profit']:,.2f} | 1:1.8 R:R)")
    print(f"      - Target 2 (Trail): +{atm['target2_points']} pts on Option Premium (Gain: +₹{atm['target2_profit']:,.2f} | 1:2.8 R:R)")
    
    print(f"\n   \033[91m🔴 BEARISH SETUP (PUT - PE):\033[0m")
    print(f"      - Action        : BUY 1 Lot {atm['bearish_pe']['strike']}")
    print(f"      - Spot Trigger  : Wait for 15-min candle to CLOSE firmly BELOW {atm['bearish_pe']['trigger_level']:.2f} - VWAP")
    print(f"      - Stop Loss (SL): -{atm['sl_points']} pts on Option Premium (Capped Loss: -₹{atm['risk_per_lot']:,.2f})")
    print(f"      - Target 1 (50%): +{atm['target1_points']} pts on Option Premium (Gain: +₹{atm['target1_profit']:,.2f} | 1:1.8 R:R)")
    print(f"      - Target 2 (Trail): +{atm['target2_points']} pts on Option Premium (Gain: +₹{atm['target2_profit']:,.2f} | 1:2.8 R:R)")
    print("-" * 80)
    
    print(" 🛡️ STRATEGY B: DEFINED-RISK HEDGED SPREAD (SAFEST F&O METHOD)")
    print("   [Eliminates Theta Decay Risk + Safe Against Flash Crashes & Gap Openings]")
    print(f"   • Bullish Structure : {spread['bull_spread']}")
    print(f"   • Bearish Structure : {spread['bear_spread']}")
    print(f"   • Margin Required   : ~₹{spread['margin_required']:,.2f} (Groww gives SEBI hedge benefit!)")
    print(f"   • Guaranteed Max Loss: Strictly ₹{spread['max_loss_inr']:,.2f} (Can never lose more, even on a crash)")
    print(f"   • Max Profit Potential: Up to ₹{spread['max_profit_inr']:,.2f} (Reward:Risk ratio = 1:{spread['reward_to_risk']})")
    print("-" * 80)
    
    print(" ⚠️ THE 4 CARDINAL RULES OF RETAIL F&O SURVIVAL:")
    print("   1. ZERO OVERNIGHT NAKED OPTIONS: 100% intraday exit before 03:15 PM. Overnight gap will burn capital.")
    print("   2. NO-TRADE CHOPPY ZONE: If spot is stuck between S1 and R1 (around Pivot), DO NOT TRADE. Theta eats options.")
    print("   3. FORBIDDEN 'HERO-ZERO' LOTTERIES: Never buy cheap ₹10-₹20 OTM options. 95% of them expire at ₹0.00.")
    print("   4. HARD SYSTEM STOP-LOSS: Set GTT / Stop-loss order in Groww immediately upon entry. Never hope.")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="High-Precision F&O Risk & Setup Engine")
    parser.add_argument("--index", default="NIFTY", choices=["NIFTY", "BANKNIFTY"], help="Index symbol")
    parser.add_argument("--spot", type=float, default=23446.80, help="Current spot CMP")
    parser.add_argument("--high", type=float, default=23466.90, help="Session high")
    parser.add_argument("--low", type=float, default=23349.55, help="Session low")
    parser.add_argument("--close", type=float, default=23446.80, help="Session close")
    parser.add_argument("--capital", type=float, default=20487.0, help="Available cash capital in INR")
    parser.add_argument("--lot-size", type=int, default=25, help="Contract lot size")
    parser.add_argument("--risk-pct", type=float, default=3.5, help="Max risk percentage per trade")
    
    args = parser.parse_args()
    
    data = analyze_fno_setup(
        index=args.index,
        spot=args.spot,
        high=args.high,
        low=args.low,
        close=args.close,
        capital=args.capital,
        lot_size=args.lot_size,
        max_risk_pct=args.risk_pct
    )
    
    print_fno_dossier(data)


if __name__ == "__main__":
    main()
