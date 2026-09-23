# Portfolio Management & Swing Holding Protocols

This guide outlines how to share your portfolio, how long to hold each position, and the strict rules governing averaging down vs. averaging up (pyramiding).

---

## 📸 1. How to Share Your Portfolio

You can share your portfolio with the agent in any of the following three ways:

### Option A: Upload a Screenshot (Easiest)
- Take a screenshot of your broker holding screen (Zerodha Kite, Groww, Angel One, Upstox, Robinhood, Schwab, etc.).
- Drop the image directly into the chat or workspace.
- The vision model automatically extracts:
  - **Stock Symbol / Ticker**
  - **Quantity Held**
  - **Average Buy Price**
  - **Current Market Price (CMP)**
  - **Unrealized P&L (%)**

### Option B: Quick Text Format
Paste a quick comma-separated list directly in the chat:
```text
RELIANCE 25 shares @ 2420 (CMP 2510)
TATASTEEL 200 shares @ 160 (CMP 149)
INFY 40 shares @ 1820 (CMP 1835)
ZOMATO 150 shares @ 280 (CMP 272)
```

### Option C: Markdown Table or CSV
Provide structured tabular data:
```markdown
| Symbol | Qty | Buy Price | Current Price | Target Stop Loss |
| :--- | :--- | :--- | :--- | :--- |
| RELIANCE | 25 | 2420.00 | 2510.00 | 2360.00 |
| TATASTEEL | 200 | 160.00 | 149.00 | 150.00 |
```

---

## ⏱️ 2. Holding Period Rules: How Many Days to Hold?

Swing trading is based on **time-horizon discipline**. Holding too long turns a swing into a stagnant investment; cutting too early kills your Risk-to-Reward ratio.

| Setup Type | Target Impulse | Typical Holding Window | Exit Trigger |
| :--- | :--- | :--- | :--- |
| **Momentum Breakout** *(Bull Flag, 20-Day High)* | Fast expansion (+6% to +12%) | **3 to 7 trading days** | Take 50% at Target 1; trail remainder on 1-hour/daily high-low. |
| **Trend Pullback** *(20 EMA / 50 SMA Bounce)* | Retest of swing high (+8% to +15%) | **1 to 2 weeks (5–12 days)** | Close 50% at prior pivot high; trail runner behind rising 20 EMA. |
| **Base Reversal** *(Cup & Handle / Double Bottom)* | New trend cycle (+15% to +25%) | **2 to 4 weeks (10–20 days)** | Exit if weekly candle breaks moving average support. |

### The "Time-Stop" Rule:
If a stock consolidates sideways without any directional movement for **more than 10 trading days**, close the position at breakeven/minor P&L to free up locked capital for faster-moving opportunities.

---

## ⚖️ 3. The Strict Truth About "Averaging Down"

### ❌ The Deadly Mistake: Averaging Down on Losers
> [!CAUTION]
> **NEVER average down on a short-term swing trade whose Stop Loss was hit.**  
> Averaging down on a failing trade is the #1 reason retail traders blow up accounts. A stock that falls from ₹100 to ₹50 needs a +100% gain just to break even. Respect your stop loss—take the small 1% loss and move on.

---

### 🟢 When Averaging Down is Allowed (Strategic Accumulation)
Averaging down is **only** permitted if ALL four criteria are satisfied:
1. **Bluechip / Large-Cap Quality**: The company is an index constituent or market leader with strong balance sheet and earnings growth (never on mid/small-caps or penny stocks).
2. **Major Technical Floor**: Price is testing multi-month horizontal support or the **200-day SMA**.
3. **Pre-Planned Tranches**: The trade was designed as a multi-stage buy (e.g., Tranche 1: 40% initial, Tranche 2: 30% at support, Tranche 3: 30% on reversal candle).
4. **Strict Portfolio Cap**: The total accumulated position does not exceed **10% to 15%** of your total portfolio capital.

---

### 🚀 The Professional Secret: Averaging UP ("Pyramiding")
Top swing traders do not average down on losers—they **average UP on winners**:
1. Enter with initial position size (Tranche 1).
2. When the stock moves in your favor (+3% to +5%) and breaks out of a secondary consolidation, add Tranche 2 (50% of initial size).
3. Immediately trail the Stop Loss on the **entire position** to above your first entry price.
4. Result: Higher profit potential with zero net risk to initial capital.
