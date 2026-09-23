# Swing Trade Gatekeeper Checklist & Journal

Every trade must satisfy the **10-Point Pre-Trade Checklist** before capital is committed. Discipline and risk control are the only guarantees of long-term trading longevity.

---

## 🛡️ 10-Point Pre-Trade Gatekeeper

Do **NOT** take the trade unless you can check at least **8 of the 10** criteria:

### Market & Sector Context
- [ ] **1. Market Tide Alignment**: Is the broader index (Nifty 50 / S&P 500) trading above its 50-day moving average or showing bullish breadth? *(Never fight a macro market correction).*
- [ ] **2. Sector Leadership**: Is the stock's sector in the top 3 performing sectors over the past 1 to 4 weeks?

### Technical Confluence
- [ ] **3. Structural Trend**: Is the stock trading above its 200 SMA and 50 SMA?
- [ ] **4. Clear Pattern**: Can you identify one of the 5 canonical swing patterns (Bull Flag, 20 EMA Pullback, Cup & Handle, Ascending Triangle, Double Bottom)?
- [ ] **5. Moving Average Support**: Is the entry anchored near dynamic support (20 EMA or 50 SMA)?
- [ ] **6. Volume Confirmation**: Did volume dry up during the pullback, and is it expanding on the entry trigger ($>1.2\times$ 20-day average)?
- [ ] **7. Momentum Health**: Is RSI(14) between 45 and 68? *(Avoid buying stocks with RSI $>75$ without waiting for a retest).*

### Risk & Execution
- [ ] **8. Risk-to-Reward Ratio**: Is the calculated R:R at least **1 : 2.0** to Target 1?
- [ ] **9. Position Size & Capital Risk**: Have you calculated exact shares using `scripts/position_sizer.py` so total account risk is strictly $\le 1.0\% - 1.5\%$?
- [ ] **10. Catalyst Clearance**: Are there **NO** binary hazard events (Earnings release, FDA decision, budget announcement) scheduled within the planned holding window?

---

## 📈 Trade Management Rules (Scaling & Trailing)

1. **At Target 1 (1:2 Risk-to-Reward)**:
   - Sell **50% of the position** to lock in guaranteed profit.
   - Immediately move the Stop Loss on the remaining 50% to **Breakeven (Entry Price)**. The trade is now mathematically risk-free.
2. **At Target 2 (Runner)**:
   - Trail the remaining shares behind the **rising 20 EMA** on the daily chart.
   - Close the remainder only when a daily candle closes below the 20 EMA.
3. **If Stop Loss is Hit**:
   - Exit with zero hesitation. Never average down on a losing swing trade. Never turn a short-term swing into a "long-term investment" because it went against you.

---

## 📓 Standard Swing Trade Journal Template

Copy and paste this template for every swing trade logged:

```markdown
### Trade Log: [SYMBOL] — [Date]
- **Market Regime**: Bullish / Neutral / Choppy
- **Sector**: [Sector Name] (Relative Strength: High / Medium / Low)
- **Setup Type**: [Bull Flag / 20 EMA Dip / Breakout / Reversal]
- **Entry Trigger Price**: ₹ / $ [Price]
- **Stop Loss Price**: ₹ / $ [Price] (Risk per Share: [Risk])
- **Target 1 Price**: ₹ / $ [Price] (1:2 R:R)
- **Target 2 Price**: ₹ / $ [Price] (1:3+ R:R)
- **Shares Purchased**: [Qty]
- **Total Investment**: ₹ / $ [Total] ([% of Account])
- **Maximum Account Risk**: ₹ / $ [Risk] ([1.0%] of Portfolio)

#### Execution Notes:
- Why did you enter? [Technical reasons & volume signature]
- What went well?
- What could be improved?
- Final Result: [R-multiple achieved: +2.0R / -1.0R / BE]
```
