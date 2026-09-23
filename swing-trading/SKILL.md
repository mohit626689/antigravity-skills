---
name: swing-trading
description: Share market research, swing trading, portfolio optimizer, and low-risk F&O engine. Provides 7 core commands (/swing, /swing-scan, /swing-size, /swing-check, /swing-manage, /swing-portfolio, /fno), multi-timeframe moving averages (20/50/200), RSI pullbacks, volume breakouts, strict 1% risk sizing, portfolio screenshot intake, holding duration guidance, and low-cost hedged F&O setups.
compatibility: Requires Python 3.8+ for bundled calculation scripts
metadata:
  standard: "agentskills.io"
  version: "1.3.0"
  category: "finance"
  tags: ["swing-trading", "portfolio-management", "risk-control", "technical-analysis", "fno-options"]
---

# Swing Trading & Share Market Research Engine

This skill guides the agent through systematic technical analysis, pattern recognition, position sizing, and portfolio management to capture short-term moves in equities (holding period: **3 to 15 trading days**).

---

## ⚡ The 6 Core Commands

| Command | Syntax | Purpose |
| :--- | :--- | :--- |
| **`/swing`** | `/swing <stock>` | Deep-dive technical dossier, setup score (0–100), entry trigger, stop loss, and Target 1 & 2. |
| **`/swing-scan`** | `/swing-scan <setup_type>` | Screen candidates for `breakout` (20-day high with volume) or `pullback` (dip to 20 EMA / 50 SMA). |
| **`/swing-size`** | `/swing-size <entry> <stop>` | Exact share count using the 1% risk rule, capital allocated, and Target 1/2 prices. |
| **`/swing-check`** | `/swing-check <stock>` | 10-point pre-trade sanity gatekeeper audit before placing orders. |
| **`/swing-manage`** | `/swing-manage <stock>` | Active trade tracker: locks 50% at Target 1, moves stop to Breakeven, and trails 20 EMA. |
| **`/swing-portfolio`** | `/swing-portfolio` | Multi-stock audit: holding period days, exit/trim/pyramid advice, and averaging down guidance. |
| **`/fno`** | `/fno <index/stock>` | Low-cost, low-risk F&O setup: ATM strike, Pivot triggers, SL in points, and hedged spreads. |

---

## 📸 Portfolio Intake (3 Ways to Share)

Users can share their active holdings using any of these methods:
1. **Screenshot Upload (Easiest)**: Drag-and-drop a screenshot from Zerodha Kite, Groww, Angel One, Upstox, Robinhood, or any broker. The vision model extracts Symbol, Quantity, Buy Price, CMP, and P&L.
2. **Quick Text**: `RELIANCE 25 shares @ 2420, TATASTEEL 200 @ 160, INFY 40 @ 1820`
3. **Markdown / CSV Table**: Structured table with Symbol, Qty, Buy Price, Current Price.

Detailed portfolio intake rules and parsing tips are in [Portfolio Protocols](references/portfolio_rules.md).

---

## ⏱️ How Long to Hold Each Stock?

Swing trading requires time-horizon discipline:
- **Momentum Breakouts (Bull Flags, 20-Day Highs)**: **3 to 7 trading days** (fast impulse to Target 1).
- **Trend Pullbacks (20 EMA / 50 SMA Bounces)**: **1 to 2 weeks (5 to 12 trading days)**.
- **Base Reversals (Cup & Handle, Double Bottom)**: **2 to 4 weeks (10 to 20 trading days)**.
- **Time-Stop Rule**: If a stock trades flat/choppy for **$>10$ trading days** without progress, exit at breakeven to redeploy capital.

---

## ⚖️ The Strict Truth About "Averaging Down"

1. **NEVER Average Down on Speculative Swing Trades**:
   If price hits your Stop Loss, **exit immediately**. Averaging down on a failing swing setup turns a 1% loss into a portfolio-crippling baghold.
2. **When Averaging Down is Allowed (Strategic Bluechip Accumulation)**:
   - Stock is an established, profitable Large-Cap / Index leader (never mid/small-caps).
   - Price is testing major historical support or the 200-day SMA.
   - Part of a planned tranche entry, capping total position at **10%–15%** of portfolio capital.
3. **The Pro Technique — Averaging UP (Pyramiding)**:
   Add shares to **winning positions** as they break out into new highs, trailing the stop loss to protect total gains.

See full framework in [Averaging Down & Pyramiding Guide](references/portfolio_rules.md).

---

## 🛠️ Command Execution Workflows

### 1. `/swing <stock>`
Runs full multi-timeframe analysis (200 SMA trend, 20 EMA momentum, RSI 14, MACD, Volume surge):
```bash
python3 scripts/swing_analyzer.py --symbol <TICKER> --demo
```
Audits the setup with the quantitative judge:
```bash
python3 scripts/trade_judge.py --ticker <TICKER> --price <ENTRY> --stop <STOP> --target <T1>
```

### 2. `/swing-size <entry> <stop>`
Calculates exact position sizing based on portfolio capital and the 1% risk rule:
```bash
python3 scripts/position_sizer.py --capital 200000 --risk 1.0 --entry <ENTRY> --stop <STOP>
```

### 3. `/swing-check <stock>`
Audits the stock against the [10-Point Pre-Trade Checklist](references/trade_checklist.md):
- Market Tide ($>50$ SMA)
- Sector Leadership
- Moving Average Alignment ($>200$ SMA, $>20$ EMA)
- Volume Expansion ($>1.2\times$)
- Minimum 1:2 R:R
- Earnings Clearance (no report in 72 hours)

### 4. `/swing-manage <stock>`
Evaluates active trade status:
- If Target 1 hit: Book 50% profit, move Stop Loss to Breakeven.
- If trending: Trail remaining 50% behind rising 20 EMA on daily chart.
- If Stop Loss hit: Cut loss with zero hesitation.

### 5. `/swing-portfolio`
Audits user holdings and prints actionable suggestions:
```bash
python3 scripts/portfolio_analyzer.py --demo
```
Outputs:
- Total Invested, Current Value, and Unrealized P&L.
- Individual stock action: `HOLD`, `BOOK 50% & TRAIL`, `CUT LOSS`, or `ACCUMULATE`.
- Expected holding period in days for each stock.
- Averaging down vs. pyramiding advice.
- Portfolio concentration alerts (flags positions $>20\%$).

### 6. `/fno <index>`
Generates exact intraday Pivot triggers, ATM strikes, capped ₹ risk, and hedged spreads:
```bash
python3 scripts/fno_analyzer.py --index NIFTY --spot 23446.80 --high 23466.90 --low 23349.55 --close 23446.80 --capital 20487
```

---

## 📁 Reference Architecture

- **Patterns Reference**: [Swing Chart Patterns](references/swing_patterns.md) (Bull Flag, 20 EMA Pullback, Cup & Handle, Ascending Triangle).
- **Checklist & Journal**: [Pre-Trade Checklist & Trade Journal](references/trade_checklist.md).
- **Portfolio Rules**: [Holding Duration & Averaging Protocols](references/portfolio_rules.md).
- **F&O Protocols**: [Low-Risk F&O Framework & Spread Rules](references/fno_rules.md).
