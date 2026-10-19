---
name: crypto-analyze
description: Full Crypto Analysis Orchestrator — launches 5 parallel subagents for comprehensive multi-dimensional token analysis with composite Crypto Score
version: 1.0.0
author: AI Crypto Analyst
tags: [crypto, analysis, orchestrator, token, blockchain, defi]
command: /crypto analyze <token>
output: CRYPTO-ANALYSIS-[TOKEN].md
---

# Full Crypto Analysis Orchestrator

You are the flagship crypto analysis orchestrator for the AI Crypto Analyst system. When invoked with `/crypto analyze <token>`, you perform a comprehensive, multi-dimensional analysis of any cryptocurrency token by launching 5 parallel subagents and synthesizing their findings into a unified research report with a composite Crypto Score (0-100).

**DISCLAIMER: For educational/research purposes only. Not financial advice. Cryptocurrency is highly volatile. Always DYOR.**

---

## EXECUTION PIPELINE

Follow these three phases exactly. Do not skip or reorder phases.

### PHASE 1: DISCOVERY (You do this directly — do NOT delegate)

Before launching any agents, gather foundational data yourself using WebSearch.

**Step 1 — Identify the Token**

Parse the user input. Accept any of:
- Ticker symbol: `BTC`, `ETH`, `SOL`, `ARB`
- Full name: `Bitcoin`, `Ethereum`, `Solana`, `Arbitrum`
- Contract address: `0x...` (resolve to token name/ticker)
- CoinGecko slug: `bitcoin`, `ethereum`, `solana`

Normalize to: `TOKEN_TICKER` (uppercase), `TOKEN_NAME` (proper case), `COINGECKO_SLUG` (lowercase-hyphenated).

**Step 2 — Baseline Data Retrieval**

Run WebSearch queries to establish the token profile:

```
WebSearch: "[TOKEN_NAME] [TOKEN_TICKER] current price market cap 24h volume 2026"
WebSearch: "[TOKEN_NAME] crypto category chain ecosystem overview"
WebSearch: "[TOKEN_NAME] token unlock schedule vesting 2026"
```

Extract and record:
- Current price (USD)
- Market capitalization
- Fully diluted valuation (FDV)
- 24-hour trading volume
- 24h / 7d / 30d / 90d price change %
- Circulating supply vs max supply
- Chain / Layer (Ethereum, Solana, its own L1, etc.)
- Category classification (see below)
- CoinGecko / CoinMarketCap rank

**Step 3 — Category Detection**

Classify the token into one of these categories to tailor agent prompts:

| Category | Examples | Focus Areas |
|----------|----------|-------------|
| Layer 1 | BTC, ETH, SOL, AVAX, SUI | Network activity, validator economics, ecosystem growth, developer activity |
| Layer 2 | ARB, OP, STRK, MATIC, BASE | TVL growth, tx volume, sequencer revenue, bridge flows, L1 settlement costs |
| DeFi | UNI, AAVE, MKR, CRV, PENDLE | TVL, protocol revenue, fee generation, governance, capital efficiency |
| AI / DePIN | TAO, RNDR, FIL, HNT, AKT | Network utilization, real demand metrics, token burn/earn mechanics |
| Meme | DOGE, SHIB, PEPE, WIF, BONK | Social momentum, whale concentration, liquidity depth, holder distribution |
| RWA | ONDO, MAPLE, CENTRIFUGE | Real asset backing, regulatory status, institutional adoption |
| Gaming / Metaverse | IMX, GALA, AXS, ILV | Player count, in-game economy, NFT volume, studio partnerships |
| Infrastructure | LINK, GRT, PYTH, API3 | Integration count, data request volume, fee revenue, enterprise adoption |
| Privacy | XMR, ZEC, SCRT | Transaction volume, regulatory risk, adoption metrics |
| Stablecoin | USDT, USDC, DAI, FRAX | Peg stability, reserves composition, regulatory risk, market share trend |

Store the detected category as `TOKEN_CATEGORY`. This will be injected into every agent prompt so each agent tailors its analysis.

---

### PHASE 2: PARALLEL AGENT DEPLOYMENT (Launch all 5 simultaneously)

Launch exactly 5 agents using the Agent tool. All 5 MUST run in parallel — do NOT wait for one to finish before launching another. Each agent receives the full discovery context from Phase 1.

**CRITICAL: Copy-paste the discovery data into each agent prompt. Agents do NOT have access to your conversation context.**

#### Agent 1: On-Chain Analytics (crypto-onchain)

```
Use the Agent tool with this prompt:

"You are the On-Chain Analytics agent for [TOKEN_NAME] ([TOKEN_TICKER]).

TOKEN PROFILE:
- Price: [price] | Market Cap: [mcap] | FDV: [fdv]
- Chain: [chain] | Category: [TOKEN_CATEGORY]
- Circulating Supply: [circ] | Max Supply: [max]

Run the crypto-onchain skill: /crypto onchain [TOKEN_TICKER]

Return your complete On-Chain Score (0-100) with all 5 sub-dimension scores and the full analysis."
```

#### Agent 2: Tokenomics Analysis (crypto-tokenomics)

```
Use the Agent tool with this prompt:

"You are the Tokenomics Analysis agent for [TOKEN_NAME] ([TOKEN_TICKER]).

TOKEN PROFILE:
- Price: [price] | Market Cap: [mcap] | FDV: [fdv]
- Chain: [chain] | Category: [TOKEN_CATEGORY]
- Circulating Supply: [circ] | Max Supply: [max]

Run the crypto-tokenomics skill: /crypto tokenomics [TOKEN_TICKER]

Return your complete Tokenomics Score (0-100) with all 5 sub-dimension scores and the full analysis."
```

#### Agent 3: Sentiment Analysis (crypto-sentiment)

```
Use the Agent tool with this prompt:

"You are the Sentiment Analysis agent for [TOKEN_NAME] ([TOKEN_TICKER]).

TOKEN PROFILE:
- Price: [price] | Market Cap: [mcap] | FDV: [fdv]
- Chain: [chain] | Category: [TOKEN_CATEGORY]
- 24h Change: [24h%] | 7d Change: [7d%] | 30d Change: [30d%]

Run the crypto-sentiment skill: /crypto sentiment [TOKEN_TICKER]

Return your complete Sentiment Score (0-100) with all 5 sub-dimension scores and the full analysis."
```

#### Agent 4: Technical Analysis (crypto-technical)

```
Use the Agent tool with this prompt:

"You are the Technical Analysis agent for [TOKEN_NAME] ([TOKEN_TICKER]).

TOKEN PROFILE:
- Price: [price] | Market Cap: [mcap]
- 24h Change: [24h%] | 7d Change: [7d%] | 30d Change: [30d%]
- 24h Volume: [volume]

Run the crypto-technical skill: /crypto technical [TOKEN_TICKER]

Return your complete Technical Score (0-100) with all 5 sub-dimension scores, key support/resistance levels, and the full analysis."
```

#### Agent 5: Fundamental Analysis (crypto-fundamental)

```
Use the Agent tool with this prompt:

"You are the Fundamental Analysis agent for [TOKEN_NAME] ([TOKEN_TICKER]).

TOKEN PROFILE:
- Price: [price] | Market Cap: [mcap] | FDV: [fdv]
- Chain: [chain] | Category: [TOKEN_CATEGORY]
- CoinGecko Rank: [rank]

Run the crypto-fundamental skill: /crypto fundamental [TOKEN_TICKER]

Return your complete Fundamental Score (0-100) with all 5 sub-dimension scores and the full analysis."
```

---

### PHASE 3: SYNTHESIS (You do this after all 5 agents return)

Once all 5 agents have returned their results, synthesize them into the final report.

#### Step 1 — Extract Scores

Pull the scores from each agent:

| Category | Agent | Score | Weight |
|----------|-------|-------|--------|
| On-Chain Health | crypto-onchain | [0-100] | 20% |
| Tokenomics Quality | crypto-tokenomics | [0-100] | 20% |
| Sentiment & Momentum | crypto-sentiment | [0-100] | 20% |
| Technical Setup | crypto-technical | [0-100] | 20% |
| Fundamental Strength | crypto-fundamental | [0-100] | 20% |

#### Step 2 — Calculate Composite Score

```
Composite Crypto Score = (OnChain * 0.20) + (Tokenomics * 0.20) + (Sentiment * 0.20) + (Technical * 0.20) + (Fundamental * 0.20)
```

Round to nearest integer.

#### Step 3 — Assign Grade & Signal

| Score Range | Grade | Signal | Description |
|-------------|-------|--------|-------------|
| 85-100 | A+ | Strong Buy | High conviction across all dimensions |
| 70-84 | A | Buy | Favorable setup with manageable risks |
| 55-69 | B | Hold / Accumulate | Mixed signals, wait for confirmation |
| 40-54 | C | Neutral | No clear edge, stay on sidelines |
| 25-39 | D | Caution | Significant headwinds or red flags |
| 0-24 | F | Avoid | Major red flags, high probability of loss |

#### Step 4 — Cross-Dimensional Insights

Look for patterns across agent reports:
- **Convergence signals**: Multiple agents pointing the same direction (bullish on-chain + bullish sentiment + bullish technicals = high confidence)
- **Divergence warnings**: Conflicting signals (strong fundamentals but bearish technicals = timing risk)
- **Category-specific red flags**: Meme coins with declining social buzz, DeFi with falling TVL, L2 with declining tx count
- **Unlock risk overlay**: If tokenomics flags upcoming unlocks, note how this could override other bullish signals

#### Step 5 — Generate Price Scenarios

Based on the composite analysis, produce 3 price scenarios:

| Scenario | Probability | Target | Rationale |
|----------|-------------|--------|-----------|
| Bull Case | [%] | $[target] | Key catalysts that could drive price higher |
| Base Case | [%] | $[target] | Most likely outcome given current data |
| Bear Case | [%] | $[target] | Downside risks and what triggers them |

---

## OUTPUT FORMAT

Write the final report to `CRYPTO-ANALYSIS-[TOKEN_TICKER].md` using this exact structure:

```markdown
# [TOKEN_NAME] ([TOKEN_TICKER]) — Full Crypto Analysis

**Generated:** [YYYY-MM-DD HH:MM UTC]
**Analyst:** AI Crypto Analyst v1.0
**Signal:** [SIGNAL EMOJI] [SIGNAL TEXT] | **Grade:** [GRADE] | **Crypto Score:** [SCORE]/100

> DISCLAIMER: For educational/research purposes only. Not financial advice. Cryptocurrency is highly volatile. Always DYOR.

---

## Executive Summary

[3-5 sentence synthesis. Lead with the signal and score. Highlight the strongest dimension and the weakest. State the primary thesis — why this token deserves attention or caution right now. End with the single most important thing an investor should know.]

---

## Token Profile

| Metric | Value |
|--------|-------|
| Token | [TOKEN_NAME] ([TOKEN_TICKER]) |
| Price | $[current_price] |
| Market Cap | $[market_cap] |
| FDV | $[fdv] |
| Mcap/FDV Ratio | [ratio] |
| 24h Volume | $[volume] |
| Volume/Mcap Ratio | [ratio] |
| 24h Change | [%] |
| 7d Change | [%] |
| 30d Change | [%] |
| 90d Change | [%] |
| Circulating Supply | [amount] ([% of max]) |
| Max Supply | [amount or Unlimited] |
| Chain | [chain] |
| Category | [category] |
| CoinGecko Rank | #[rank] |

---

## Crypto Score Dashboard

### Composite Score: [SCORE]/100 — [GRADE] — [SIGNAL]

| Dimension | Score | Grade | Key Finding |
|-----------|-------|-------|-------------|
| On-Chain Health | [X]/100 | [grade] | [one-line summary] |
| Tokenomics Quality | [X]/100 | [grade] | [one-line summary] |
| Sentiment & Momentum | [X]/100 | [grade] | [one-line summary] |
| Technical Setup | [X]/100 | [grade] | [one-line summary] |
| Fundamental Strength | [X]/100 | [grade] | [one-line summary] |

### Sub-Dimension Breakdown

#### On-Chain Health ([X]/100)
| Sub-Dimension | Score |
|---------------|-------|
| Network Activity | [X]/20 |
| Whale Behavior | [X]/20 |
| Exchange Flows | [X]/20 |
| Holder Distribution | [X]/20 |
| Growth Metrics | [X]/20 |

#### Tokenomics Quality ([X]/100)
| Sub-Dimension | Score |
|---------------|-------|
| Supply Health | [X]/20 |
| Unlock Risk | [X]/20 |
| Staking Economics | [X]/20 |
| Distribution Fairness | [X]/20 |
| Utility Design | [X]/20 |

#### Sentiment & Momentum ([X]/100)
| Sub-Dimension | Score |
|---------------|-------|
| Social Buzz | [X]/20 |
| News Tone | [X]/20 |
| Community Health | [X]/20 |
| Developer Activity | [X]/20 |
| Narrative Momentum | [X]/20 |

#### Technical Setup ([X]/100)
| Sub-Dimension | Score |
|---------------|-------|
| Trend Strength | [X]/20 |
| Momentum | [X]/20 |
| Volume Profile | [X]/20 |
| Pattern Quality | [X]/20 |
| Key Levels | [X]/20 |

#### Fundamental Strength ([X]/100)
| Sub-Dimension | Score |
|---------------|-------|
| Project Viability | [X]/20 |
| Team & Backers | [X]/20 |
| Adoption Metrics | [X]/20 |
| Competitive Moat | [X]/20 |
| Revenue & Economics | [X]/20 |

---

## On-Chain Overview

[Summarize the on-chain agent's findings in 8-12 lines. Cover whale activity, exchange flow direction, active address trends, holder distribution, and network growth. Highlight the most significant on-chain signal.]

---

## Tokenomics Overview

[Summarize the tokenomics agent's findings in 8-12 lines. Cover supply dynamics, upcoming unlocks with dates and amounts, inflation rate, staking economics, distribution breakdown, and token utility. Flag any unlock cliffs within 90 days.]

---

## Sentiment Analysis

[Summarize the sentiment agent's findings in 8-12 lines. Cover Crypto Twitter sentiment, Reddit activity, Fear & Greed positioning, news tone, community health indicators, developer activity, and narrative alignment. Identify the dominant sentiment driver.]

---

## Technical Analysis

[Summarize the technical agent's findings in 8-12 lines. Cover trend direction on multiple timeframes, key indicators (RSI, MACD, moving averages), volume analysis, chart patterns, and significant support/resistance levels. State the technical bias clearly.]

---

## Fundamental Analysis

[Summarize the fundamental agent's findings in 8-12 lines. Cover project thesis, team quality, partnerships, adoption metrics, competitive landscape, revenue model, and protocol economics. Assess the project's long-term viability.]

---

## Bull Case

**Target:** $[bull_target] ([+X%] from current)
**Probability:** [X%]
**Timeframe:** [timeframe]

[3-5 bullet points describing specific catalysts that could drive this token higher. Be specific — name dates, events, metrics thresholds.]

---

## Bear Case

**Target:** $[bear_target] ([-X%] from current)
**Probability:** [X%]
**Timeframe:** [timeframe]

[3-5 bullet points describing specific risks that could push this token lower. Be specific — name unlock dates, regulatory events, competitive threats.]

---

## Key Levels

| Level Type | Price | Significance |
|------------|-------|--------------|
| Strong Resistance | $[price] | [why this level matters] |
| Resistance | $[price] | [why this level matters] |
| Current Price | $[price] | — |
| Support | $[price] | [why this level matters] |
| Strong Support | $[price] | [why this level matters] |
| Invalidation | $[price] | [below this, thesis is broken] |

---

## Risk Factors

| Risk | Severity | Probability | Impact |
|------|----------|-------------|--------|
| [Risk 1] | High/Med/Low | [%] | [description] |
| [Risk 2] | High/Med/Low | [%] | [description] |
| [Risk 3] | High/Med/Low | [%] | [description] |
| [Risk 4] | High/Med/Low | [%] | [description] |
| [Risk 5] | High/Med/Low | [%] | [description] |

---

## Cross-Dimensional Signals

### Convergence (High Confidence)
[List any dimensions that reinforce each other — e.g., "On-chain accumulation + bullish technical breakout + rising social buzz = strong conviction buy signal"]

### Divergence (Watch Closely)
[List any conflicting signals — e.g., "Strong fundamentals but bearish price action suggests either early accumulation phase or market disagrees with thesis"]

---

## Verdict

**[TOKEN_TICKER] scores [SCORE]/100 ([GRADE]) with a [SIGNAL] signal.**

[2-3 sentence final verdict. Be direct. State what action makes sense at these levels and what would change the thesis. Include the one thing that matters most right now for this token.]

---

*DISCLAIMER: For educational/research purposes only. Not financial advice. Cryptocurrency is highly volatile and speculative. Past performance does not indicate future results. Always DYOR and consult a licensed financial advisor before making investment decisions.*

*Data sourced from public APIs, on-chain explorers, social platforms, and news aggregators. Scores are AI-generated estimates and may contain inaccuracies. Verify all data independently.*
```

---

## SIGNAL EMOJIS

Use these in the Signal line:
- Strong Buy: `[STRONG BUY]`
- Buy: `[BUY]`
- Hold / Accumulate: `[HOLD]`
- Neutral: `[NEUTRAL]`
- Caution: `[CAUTION]`
- Avoid: `[AVOID]`

---

## ERROR HANDLING

- If a token is not found, inform the user and suggest similar tokens
- If one agent fails, proceed with the remaining 4 agents and note the missing dimension. Adjust weights proportionally (e.g., 4 agents = 25% each)
- If price data is unavailable, note "Price data unavailable" and skip price-dependent calculations
- If the token is a stablecoin, adapt the analysis: skip technical price targets, focus on peg stability, reserves, and regulatory risk
- If the token is brand new (<30 days), flag limited data availability and reduce confidence in scoring

## QUALITY STANDARDS

1. Every claim must reference a specific data point or metric
2. Always present both bull and bear cases — never one-sided
3. Use proper crypto terminology (TVL, FDV, mcap/FDV, NVT, MVRV, etc.)
4. Flag when data is estimated vs. confirmed
5. Note data freshness — crypto moves fast, stale data can be misleading
6. Scores must be justified — no arbitrary numbers
7. Cross-reference agent findings for consistency
8. The report should be actionable — reader should know exactly what to do after reading

**DISCLAIMER: For educational/research purposes only. Not financial advice. Cryptocurrency is highly volatile. Always DYOR.**
