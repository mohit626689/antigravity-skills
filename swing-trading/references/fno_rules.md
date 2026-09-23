# ⚡ Low-Cost & Low-Risk F&O Trading Engine (Retail Capital Framework)

> **Core Objective**: Enable sustainable, risk-protected Futures & Options participation for retail accounts with capital between ₹15,000 and ₹50,000, eliminating the fatal traps that cause 93% of retail option buyers to lose capital.

---

## 🛑 The Brutal Reality of Indian Retail F&O (SEBI Facts)
- **93% of retail F&O traders incur net losses**, averaging ₹2,00,000 in losses per trader.
- **The #1 Culprit**: Buying out-of-the-money (OTM) "Hero-Zero" lottery tickets (₹10–₹30 options) on expiry days. Theta (time) decay burns 100% of the invested premium by 3:30 PM.
- **The #2 Culprit**: Trading without a mechanical Stop-Loss (averaging down on losing option positions).
- **The Margin Barrier**: Naked Futures and Naked Option Selling require ₹1,20,000 to ₹1,80,000+ margin per lot on NSE, rendering them inaccessible for smaller cash accounts.

---

## 🛡️ The Only 2 Mathematically Sound Methods for Low-Cost F&O

### Method 1: Disciplined Intraday Momentum ATM Option Buying (Risk Capped at ₹500–₹800)
- **Strike Selection**: **At-the-Money (ATM)** or 1 strike **In-the-Money (ITM)** ONLY (Delta $\approx 0.50$ to $0.60$).
- **Never Trade OTM**: OTM options have low Delta and high Theta decay.
- **Capital Deployed**: Only ₹3,000 to ₹6,000 per lot.
- **Strict Stop-Loss**: 10 to 12 points on Option Premium (Risk $\approx$ ₹300 to ₹800 depending on lot size). If breached, **exit immediately**.
- **Target 1**: 20 to 25 points gain on Option Premium (Risk-Reward 1:1.8). Book 50% lot or lock gains.
- **Target 2**: 35+ points gain on Option Premium (Risk-Reward 1:2.8). Trail behind rising 5-min 20 EMA.
- **Execution Windows**:
  - Morning Momentum: **09:30 AM to 11:00 AM IST**
  - Afternoon Expiry / Trend Move: **01:30 PM to 03:00 PM IST**
  - **Dead Zone**: Avoid 11:30 AM to 01:15 PM (chop & theta bleed).
- **Golden Rule**: **100% Intraday**. Zero overnight holding of long naked options.

### Method 2: Defined-Risk Hedged Spreads (Bull Call / Bear Put Spread)
- **Concept**: Buy an ATM Strike + simultaneously Sell an OTM Strike.
- **Why It's Low Risk**:
  - Max Loss is strictly capped at the net debit paid.
  - Selling the OTM leg pays you premium and acts as a shield against Theta decay.
  - Flash crashes or overnight gap-downs cannot cause catastrophic drawdown.
- **Groww Margin Benefit**:
  - Under SEBI margin framework, brokers offer **margin benefit on hedged option pairs**.
  - Capital required: Only ~₹18,000 to ₹22,000 in your Groww cash balance!

---

## 📈 Candlestick & Indicator Confirmation Rules

Before entering any F&O trade on live market, **3 out of 3 gates must be GREEN**:

1. **15-Minute Candlestick Close**:
   - **For Call (CE)**: A 15-minute candle must close with a decisive green body ABOVE the R1 Resistance or Central Pivot.
   - **For Put (PE)**: A 15-minute candle must close with a decisive red body BELOW the S1 Support or Central Pivot.
2. **VWAP (Volume-Weighted Average Price)**:
   - Price must be **trading firmly above VWAP** for Call buys.
   - Price must be **trading firmly below VWAP** for Put buys.
3. **20 EMA Momentum Gate**:
   - Spot price must hold above the 5-min and 15-min 20 EMA for Call trades.
   - If price re-crosses below 20 EMA, exit immediately.

---

## ⚡ Execution Command

Run the F&O setup engine anytime:
```bash
python3 scripts/fno_analyzer.py --index NIFTY --spot <CMP> --high <HIGH> --low <LOW> --close <CLOSE> --capital 20487
```
