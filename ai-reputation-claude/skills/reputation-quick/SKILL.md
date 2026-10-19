# 60-Second Reputation Scorecard

## Skill Purpose
Generate a fast, high-level reputation scorecard for a business in under 60 seconds. This is the quick triage version of the full audit -- designed for rapid evaluation, comparing multiple businesses, or getting a snapshot before deciding whether a deep dive is warranted. Returns an overall score, star rating averages, review volume, sentiment ratio, top complaint and praise themes, and a one-line recommendation.

## When to Use
- User wants a quick reputation check without a full audit
- User is evaluating multiple businesses and needs fast comparisons
- User wants to triage which businesses need deeper analysis
- User asks for a "quick look" or "snapshot" of reputation
- User is vetting a potential partner, vendor, or acquisition target
- Triggered by `/reputation quick <business name>`

## How to Execute

### Step 1: Rapid Data Collection

Speed is the priority. Run the minimum searches needed for a meaningful scorecard.

**Core searches (execute all in parallel via WebSearch):**

```
Search 1: "[Business Name]" reviews
Search 2: "[Business Name]" site:google.com/maps (Google reviews)
Search 3: "[Business Name]" site:yelp.com
Search 4: "[Business Name]" (complaint OR terrible OR scam OR avoid)
Search 5: "[Business Name]" (amazing OR love OR recommend OR best)
```

**Data points to extract rapidly:**

| Data Point | Source | How to Find |
|---|---|---|
| Google star rating | Google Maps / Knowledge Panel | Search result 1 or 2 |
| Google review count | Google Maps / Knowledge Panel | Same as above |
| Yelp star rating | Yelp listing | Search result 3 |
| Yelp review count | Yelp listing | Same as above |
| Other platform ratings | Search results | Search result 1 |
| Negative signal volume | Search result 4 | Count and scan negative results |
| Positive signal volume | Search result 5 | Count and scan positive results |
| Overall search sentiment | All results | Quick scan of page 1 titles and snippets |

### Step 2: Score Calculation

Calculate the Overall Reputation Score (0-100) using this weighted formula:

**Component Scores:**

| Component | Weight | How to Score | Scoring Guide |
|---|---|---|---|
| Star Rating Average | 30% | Average star rating across found platforms, normalized to 0-100 | 5.0 stars = 100, 4.5 = 90, 4.0 = 80, 3.5 = 65, 3.0 = 50, 2.5 = 35, 2.0 = 20, 1.5 = 10, 1.0 = 0 |
| Review Volume | 15% | Total reviews across all platforms | 500+ = 100, 200-499 = 85, 100-199 = 70, 50-99 = 55, 20-49 = 40, 10-19 = 25, 1-9 = 15, 0 = 0 |
| Sentiment Ratio | 25% | Ratio of positive to negative search results on page 1 | All positive = 100, 90%+ positive = 85, 70-89% = 70, 50-69% = 50, 30-49% = 30, <30% = 10 |
| Search Result Health | 15% | Quality and sentiment of top 10 branded search results | 9-10 positive/neutral = 100, 7-8 = 80, 5-6 = 60, 3-4 = 40, 1-2 = 20, 0 = 0 |
| Recency and Velocity | 15% | How recent are reviews, and are they coming in regularly | Active within last month with steady flow = 100, Last 3 months = 75, Last 6 months = 50, Last year = 30, Older = 10 |

**Overall Score = (Star Rating * 0.30) + (Review Volume * 0.15) + (Sentiment * 0.25) + (Search Health * 0.15) + (Recency * 0.15)**

**Score Interpretation:**

| Score | Grade | Label | Meaning |
|---|---|---|---|
| 90-100 | A+ | Exceptional | Dominant positive reputation. Minimal risk. |
| 80-89 | A | Excellent | Strong reputation with minor room for improvement. |
| 70-79 | B | Good | Solid reputation. Some areas to strengthen. |
| 60-69 | C+ | Fair | Acceptable but notable gaps or concerns. |
| 50-59 | C | Mediocre | Mixed reputation. Needs active management. |
| 40-49 | D | Poor | Significant reputation problems. Intervention needed. |
| 30-39 | D- | Very Poor | Major reputation damage. Urgent action required. |
| 0-29 | F | Critical | Reputation crisis. Immediate professional intervention recommended. |

### Step 3: Theme Identification

Quickly scan the search results to identify the single most prominent positive and negative themes.

**Common Positive Themes:**
- Great customer service / friendly staff
- High quality product or service
- Good value for money / fair pricing
- Professional and reliable
- Fast response time / quick delivery
- Clean facility / great atmosphere
- Knowledgeable and helpful team
- Easy to work with / seamless experience

**Common Negative Themes:**
- Poor customer service / rude staff
- Long wait times / slow response
- Overpriced / hidden fees / billing issues
- Quality issues / product defects
- Broken promises / misleading marketing
- Difficulty getting refunds or cancellations
- Dirty facility / poor maintenance
- Management issues / unresponsive to complaints

Select the ONE top theme for each (positive and negative) based on frequency in the search results scanned.

### Step 4: One-Line Recommendation

Based on the overall score and findings, generate a single actionable recommendation.

**Recommendation Templates by Score Range:**

| Score Range | Recommendation Focus |
|---|---|
| 90-100 | Maintain momentum: "Continue current review generation strategy and consider leveraging your strong reputation in marketing materials." |
| 80-89 | Optimize gaps: "Address [specific gap] to move from good to exceptional -- focus on [specific platform or theme]." |
| 70-79 | Strengthen weaknesses: "Increase review volume on [platform] and proactively address [complaint theme] to strengthen overall perception." |
| 60-69 | Active intervention: "Prioritize responding to negative reviews on [platform] and launch a systematic review request campaign to improve your [X]-star average." |
| 50-59 | Significant work needed: "Implement a review response strategy immediately and address the recurring [complaint theme] at the operational level before soliciting new reviews." |
| 40-49 | Urgent action: "Stop the bleeding -- respond to all unanswered negative reviews within 48 hours and fix the underlying [issue] causing complaints." |
| 30-39 | Crisis management: "Consider running `/reputation crisis` -- your reputation needs immediate professional attention focused on [primary issue]." |
| 0-29 | Full intervention: "Reputation crisis detected. Run `/reputation audit` for a complete analysis and action plan. Prioritize legal review if defamatory content is present." |

### Step 5: Comparison Mode (Optional)

If the user provides multiple business names, generate a comparison table.

**Comparison Scorecard:**

| Metric | Business A | Business B | Business C |
|---|---|---|---|
| Overall Score | [X]/100 | [X]/100 | [X]/100 |
| Grade | [A-F] | [A-F] | [A-F] |
| Google Rating | [X] stars ([N]) | [X] stars ([N]) | [X] stars ([N]) |
| Yelp Rating | [X] stars ([N]) | [X] stars ([N]) | [X] stars ([N]) |
| Sentiment Ratio | [+/N/-] | [+/N/-] | [+/N/-] |
| Top Praise | [theme] | [theme] | [theme] |
| Top Complaint | [theme] | [theme] | [theme] |
| Recommendation | [one-line] | [one-line] | [one-line] |

---

## Output Format

Generate a file called `REPUTATION-SCORECARD-[business-name].md`:

```markdown
# Reputation Scorecard
## [Business Name]
### Quick Scan: [Date]

---

## Overall Reputation Score: [X]/100 ([Grade])

---

## Star Ratings

| Platform | Rating | Reviews | Status |
|---|---|---|---|
| Google | [X.X] stars | [N] reviews | [Emoji-free status: Strong / Adequate / Weak / Critical / Not Found] |
| Yelp | [X.X] stars | [N] reviews | [status] |
| [Other] | [X.X] stars | [N] reviews | [status] |
| **Average** | **[X.X] stars** | **[N] total** | |

---

## Sentiment Snapshot

| Sentiment | Percentage |
|---|---|
| Positive | [X]% |
| Neutral | [X]% |
| Negative | [X]% |

**Sentiment Ratio: [X] positive for every 1 negative**

---

## Score Breakdown

| Component | Score | Weight | Weighted |
|---|---|---|---|
| Star Rating Average | [X]/100 | 30% | [X] |
| Review Volume | [X]/100 | 15% | [X] |
| Sentiment Ratio | [X]/100 | 25% | [X] |
| Search Result Health | [X]/100 | 15% | [X] |
| Recency and Velocity | [X]/100 | 15% | [X] |
| **Overall** | | | **[X]/100** |

---

## Top Themes

**What customers love most:** [Theme with brief evidence]

**What customers complain about most:** [Theme with brief evidence]

---

## One-Line Recommendation

> [Single actionable recommendation]

---

## Need More Detail?

- Run `/reputation audit [business name]` for a comprehensive analysis
- Run `/reputation respond [business name]` for review response templates
- Run `/reputation social [business name]` for social media reputation scan
- Run `/reputation seo [business name]` for search result optimization
```

---

## Terminal Output

The terminal output IS the scorecard for quick scanning. This is the primary output -- the file is secondary.

```
================================================
  REPUTATION SCORECARD: [Business Name]
================================================

  Overall Score:  [XX]/100  ([Grade])

  Star Ratings:
    Google:     [X.X] stars  ([N] reviews)
    Yelp:       [X.X] stars  ([N] reviews)
    [Other]:    [X.X] stars  ([N] reviews)
    Average:    [X.X] stars  ([N] total reviews)

  Sentiment:
    Positive:   [XX]%
    Neutral:    [XX]%
    Negative:   [XX]%

  Top Praise:    [Theme]
  Top Complaint: [Theme]

  Recommendation:
    [One-line recommendation]

================================================
  Saved to: REPUTATION-SCORECARD-[business].md
  For full audit: /reputation audit [business]
================================================
```

**For comparison mode (multiple businesses):**

```
=================================================================
  REPUTATION SCORECARD COMPARISON
=================================================================

  Business          Score   Grade   Stars   Reviews   Sentiment
  ----------------------------------------------------------------
  [Business A]      [XX]    [A]     [X.X]   [NNN]     [XX]% pos
  [Business B]      [XX]    [B]     [X.X]   [NNN]     [XX]% pos
  [Business C]      [XX]    [C]     [X.X]   [NNN]     [XX]% pos

  Best Overall:  [Business A]
  Most Reviews:  [Business B]
  Best Rated:    [Business A]

=================================================================
  Saved to: REPUTATION-SCORECARD-comparison.md
=================================================================
```

## Key Principles
- Speed over depth. This skill should feel almost instant. If it is taking more than 60-90 seconds of search time, you are doing too much. Save the deep analysis for `/reputation audit`.
- The score must be defensible. Every number should map to observable data from the search results. Do not inflate scores to make the user feel good. Honesty builds trust.
- The one-line recommendation is the most important output. It should be specific enough to act on immediately. "Improve your reputation" is useless. "Respond to the 12 unanswered 1-star Google reviews from the last 3 months" is actionable.
- When data is missing, say so. If a platform has no reviews or the business is not listed, report "Not Found" rather than guessing. Missing data is itself a finding -- low review presence is a reputation gap.
- The terminal output is the primary deliverable. Many users will not open the file. Make the terminal summary complete enough to be useful on its own.
- The comparison mode is extremely valuable for agencies evaluating clients, investors evaluating targets, or businesses benchmarking against competitors. Make the comparison table scannable at a glance.
- This skill is the gateway to deeper analysis. Always include pointers to `/reputation audit` and other skills at the bottom.
