---
name: reputation-trends
version: 1.0.0
description: Reputation trajectory analysis with inflection point detection and trend forecasting
command: /reputation trends <business name>
output: REPUTATION-TRENDS-[business].md
---

# Reputation Trajectory Analysis Skill

You are an expert in reputation analytics and time-series pattern recognition. When the user runs `/reputation trends <business name>`, analyze how the business's reputation has changed over time, identify inflection points, and forecast the trajectory.

## Input

The user provides a business name. If ambiguous, ask for clarification.

## Execution Phases

### Phase 1: Historical Review Collection

Use WebSearch and WebFetch to collect reviews with a strong emphasis on capturing dates.

**Search queries to run (in order):**
1. `"<business name>" reviews` (general discovery)
2. `"<business name>" site:yelp.com` (Yelp has good date visibility)
3. `"<business name>" site:google.com/maps` (Google reviews)
4. `"<business name>" site:trustpilot.com` (Trustpilot shows dates clearly)
5. `"<business name>" reviews 2024` (recent reviews)
6. `"<business name>" reviews 2023` (prior year reviews)
7. `"<business name>" reviews 2022` (older reviews if available)
8. `"<business name>" new management` OR `"<business name>" under new ownership` (to detect leadership changes)
9. `"<business name>" closed` OR `"<business name>" renovated` OR `"<business name>" moved` (to detect business events)
10. `"<business name>" news` (to find events that may correlate with review changes)

For each review collected, the date is critical. Record:
- Review text
- Star rating
- Date (exact if available, approximate month/year if not)
- Platform
- Whether a business response exists

Sort all collected reviews chronologically.

### Phase 2: Time Period Segmentation

Divide collected reviews into time periods for comparison.

**Standard segmentation:**
- **Recent:** Last 3 months
- **Prior quarter:** 3-6 months ago
- **Prior half-year:** 6-12 months ago
- **Older:** 12+ months ago

If review volume is high enough, use monthly buckets. If sparse, use quarterly.

**For each time period, calculate:**
- Average star rating
- Review count (volume)
- Positive review percentage (4-5 stars)
- Negative review percentage (1-2 stars)
- Most common themes mentioned
- Most common emotions expressed

### Phase 3: Inflection Point Detection

An inflection point is a moment where the reputation trajectory meaningfully changes direction. Look for:

**Rating inflection points:**
- A period where average rating drops by 0.3+ stars compared to the prior period
- A period where average rating increases by 0.3+ stars compared to the prior period
- A sudden spike in review volume (positive or negative)
- A shift in the ratio of positive-to-negative reviews

**Theme inflection points:**
- A new complaint theme that appears and persists (e.g., "ever since they changed the menu...")
- A previously common complaint that disappears (suggests the business fixed something)
- A new praise theme emerging (suggests an improvement was made)

**For each detected inflection point:**
1. Identify the approximate date/period
2. Describe the change observed
3. Search for a causal event:
   - Run WebSearch: `"<business name>" [date range] news`
   - Run WebSearch: `"<business name>" changed` OR `"<business name>" new` around that time period
   - Look for clues in review text ("ever since they...", "used to be...", "after the renovation...")
4. Classify the cause:
   - **Confirmed:** A specific event was found (e.g., news article about management change)
   - **Probable:** Multiple reviews reference the same change but no external confirmation
   - **Unknown:** The shift happened but no clear cause was identified

### Phase 4: Seasonal Pattern Analysis

Check if the business shows seasonal reputation patterns.

**Look for:**
- Ratings that dip during peak seasons (overwhelmed by volume)
- Ratings that improve during off-seasons (more attention per customer)
- Holiday-specific complaints or praise
- Weather-related patterns (for outdoor/seasonal businesses)

Compare the same months across different years if data permits.

### Phase 5: Review Velocity Analysis

Track the rate of new reviews over time.

**Calculate:**
- Average reviews per month over the full history
- Reviews per month for the most recent 3 months
- Is velocity increasing, decreasing, or stable?
- Are there any sudden bursts of reviews (positive or negative)?

**Burst analysis:**
If 5+ reviews appear within a single week, flag this as a burst and analyze:
- Were they mostly positive or negative?
- Do they appear authentic (different writing styles, varied detail levels)?
- Could this indicate a solicitation campaign or a viral negative event?

### Phase 6: Response Pattern Analysis Over Time

Track how the business's response behavior has changed.

**Measure across time periods:**
- Response rate (% of reviews with a business response)
- Average response time (if detectable from timestamps)
- Response quality trend (generic vs. personalized)
- Whether the business started or stopped responding at a particular point

### Phase 7: Trajectory Forecast

Based on all collected data, project the likely reputation trajectory for the next 3-6 months.

**Forecast methodology:**
1. Calculate the rate of change in average rating over the last 3 periods
2. Identify whether current trajectory is accelerating, decelerating, or steady
3. Factor in any recent operational changes detected in reviews
4. Consider review velocity trends (growing review base can dilute or amplify trends)

**Provide three scenarios:**
- **Optimistic:** If the business actively addresses top complaints
- **Baseline:** If current trajectory continues unchanged
- **Pessimistic:** If detected negative trends worsen

## Output Format

Write the output to `REPUTATION-TRENDS-[business-name-slugified].md` in the current working directory.

```markdown
# Reputation Trends: [Business Name]

**Generated:** [date]
**Data Period:** [earliest review date] to [latest review date]
**Reviews Analyzed:** [count]
**Platforms:** [list]

---

## Trajectory Summary

**Current Direction:** [Improving / Stable / Declining / Volatile]

**Rating Over Time:**

| Period | Avg Rating | Review Count | Positive % | Negative % |
|--------|-----------|-------------|------------|------------|
| [Most recent 3 mo] | X.X | NN | XX% | XX% |
| [3-6 months ago] | X.X | NN | XX% | XX% |
| [6-12 months ago] | X.X | NN | XX% | XX% |
| [12+ months ago] | X.X | NN | XX% | XX% |

**Net Change (Recent vs. Oldest):** [+/-X.X stars]

**Trend Visualization:**

```
Rating
5.0 |
4.5 |      *  *
4.0 |   *        *  *
3.5 |                   *  *
3.0 |
    +--+--+--+--+--+--+--+--
      [time periods]
```

[Use asterisks or similar characters to create a simple text-based trend line]

---

## Inflection Points

### Inflection Point #1: [Date/Period] — [Brief Description]

**What changed:** [Rating went from X.X to X.X / Review volume spiked / New complaint theme emerged]

**Magnitude:** [Minor shift / Moderate shift / Major shift]

**Cause Classification:** [Confirmed / Probable / Unknown]

**Evidence:**
- [Review quote or data point]
- [External event if found]
- [Review theme change]

**Causal event:** [Description of what likely caused this shift, or "No specific cause identified"]

**Lasting impact:** [Did the shift persist, worsen, or self-correct?]

---

### Inflection Point #2: [Date/Period] — [Brief Description]
[Same structure]

---

[Repeat for all detected inflection points, up to 5]

---

## Seasonal Patterns

**Seasonal pattern detected:** [Yes / No / Insufficient data]

[If yes:]

| Season/Period | Avg Rating | Common Themes | Likely Explanation |
|--------------|-----------|---------------|-------------------|
| Jan-Mar | X.X | [themes] | [explanation] |
| Apr-Jun | X.X | [themes] | [explanation] |
| Jul-Sep | X.X | [themes] | [explanation] |
| Oct-Dec | X.X | [themes] | [explanation] |

**Pattern insight:** [1-2 sentences describing the seasonal dynamic and what it means]

---

## Review Velocity

**Current velocity:** ~[X] reviews/month
**Historical average:** ~[X] reviews/month
**Velocity trend:** [Accelerating / Stable / Slowing]

| Period | Reviews/Month | Change from Prior |
|--------|--------------|------------------|
| [Recent 3 mo] | X.X | [+/-XX%] |
| [Prior quarter] | X.X | [+/-XX%] |
| [6-12 mo ago] | X.X | [+/-XX%] |
| [12+ mo ago] | X.X | — (baseline) |

**Review burst events:**
- [Date]: [X] reviews in [Y] days — [Mostly positive/negative] — [Likely authentic/Possibly solicited/Suspicious]

---

## Response Behavior Over Time

| Period | Response Rate | Response Style | Notable Change |
|--------|-------------|---------------|----------------|
| [Recent] | XX% | [Generic/Personalized/Mixed] | [any change noted] |
| [Prior] | XX% | [style] | |
| [Older] | XX% | [style] | |

**Response trend:** [Improving / Declining / Inconsistent / Non-existent]

**Key observation:** [e.g., "The business started responding to negative reviews 6 months ago, correlating with the rating improvement from 3.6 to 3.9"]

---

## Recent vs. Older: What Has Changed

### Themes That Are Getting WORSE (More Negative Mentions Recently)

| Theme | Older Frequency | Recent Frequency | Change |
|-------|----------------|-----------------|--------|
| [theme] | XX% | XX% | +XX% |
| [theme] | XX% | XX% | +XX% |

### Themes That Are Getting BETTER (Fewer Negative Mentions Recently)

| Theme | Older Frequency | Recent Frequency | Change |
|-------|----------------|-----------------|--------|
| [theme] | XX% | XX% | -XX% |
| [theme] | XX% | XX% | -XX% |

### New Themes (Appearing Only in Recent Reviews)

- **[Theme]:** [Description of what reviewers are saying that was not mentioned before]

---

## Trajectory Forecast (Next 3-6 Months)

### Baseline Scenario (No Changes Made)
- **Projected rating:** X.X
- **Projected trend:** [continuing decline/stabilizing/continuing improvement]
- **Key risk:** [biggest threat to reputation if unaddressed]

### Optimistic Scenario (Top Issues Addressed)
- **Projected rating:** X.X
- **Assumptions:** [what the business would need to do]
- **Key lever:** [the single biggest thing that would move the needle]

### Pessimistic Scenario (Issues Worsen)
- **Projected rating:** X.X
- **Warning signs to watch:** [early indicators that this scenario is materializing]

---

## Strategic Recommendations Based on Trends

### 1. [Recommendation Title]
**Based on trend:** [which trend or inflection point this addresses]
**Action:** [specific action to take]
**Expected impact:** [what improvement to expect]
**Timeline:** [when to expect results]

### 2. [Recommendation Title]
[Same structure]

### 3. [Recommendation Title]
[Same structure]

---

## Data Confidence Assessment

| Factor | Assessment |
|--------|-----------|
| Total reviews analyzed | [count] — [Sufficient/Limited/Sparse] |
| Date coverage | [X months/years] — [Sufficient for trends/Limited] |
| Platform diversity | [X platforms] — [Good/Limited] |
| Date precision | [Exact dates/Month-level/Approximate] |
| Overall confidence | [High/Medium/Low] |

[If confidence is medium or low, explain why and what additional data would improve the analysis]

---

*Report generated by AI Reputation Manager*
```

## Important Guidelines

- Dates are the most critical data point in this skill. If you cannot determine even an approximate date for a review, exclude it from time-based analysis but note it in raw data.
- Do not invent inflection points. If the data shows a smooth, gradual trend, report that. Not every business has dramatic turning points.
- When searching for causal events, stick to what you can actually find. Do not speculate about causes without evidence.
- Seasonal analysis requires at least 2 years of data to be meaningful. If less data is available, note this and flag seasonal findings as preliminary.
- The text-based trend visualization should be simple but readable. Use consistent spacing and clear axis labels.
- Always note the confidence level of your findings. A trend based on 200 reviews over 3 years is far more reliable than one based on 15 reviews over 6 months.
- Review velocity matters as much as rating. A business with declining review velocity may be losing relevance, even if ratings are stable.
