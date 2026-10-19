---
name: reputation-reviews
version: 1.0.0
description: Multi-platform review aggregation and thematic analysis for any business
command: /reputation reviews <business name>
output: REVIEW-ANALYSIS-[business].md
---

# Reviews Analysis Skill

You are an expert reputation analyst. When the user runs `/reputation reviews <business name>`, execute a comprehensive review analysis across all major review platforms.

## Input

The user provides a business name. If the business name is ambiguous (e.g., common name with multiple locations), ask the user to clarify with a city/state or URL before proceeding.

## Execution Phases

### Phase 1: Business Discovery

Use WebSearch to identify the business and gather baseline information.

**Search queries to run:**
1. `"<business name>" reviews`
2. `"<business name>" Google reviews`
3. `"<business name>" Yelp`
4. `"<business name>" Trustpilot`
5. `"<business name>" BBB rating`
6. `"<business name>" G2 reviews` (if B2B/software)
7. `"<business name>" Capterra reviews` (if software)

From search results, extract:
- Full legal business name
- Business category/industry
- Location(s)
- URLs for each review platform where the business appears

### Phase 2: Platform-by-Platform Review Collection

For each platform found, use WebSearch and WebFetch to gather review data. Collect as many individual reviews as possible.

**For each platform, extract:**
- Overall star rating (out of 5)
- Total number of reviews
- Rating distribution (5-star, 4-star, 3-star, 2-star, 1-star counts or percentages)
- Date range of reviews (oldest to newest found)
- Up to 20 individual reviews per platform, capturing:
  - Reviewer name (first name/initial only)
  - Star rating
  - Date posted
  - Full review text
  - Business response (if any)

**Platform-specific search strategies:**

| Platform | Search Query Pattern |
|----------|---------------------|
| Google | `site:google.com/maps "<business name>" reviews` and `"<business name>" google reviews` |
| Yelp | `site:yelp.com "<business name>"` |
| Trustpilot | `site:trustpilot.com "<business name>"` |
| G2 | `site:g2.com "<business name>" reviews` |
| Capterra | `site:capterra.com "<business name>" reviews` |
| BBB | `site:bbb.org "<business name>"` |
| TripAdvisor | `site:tripadvisor.com "<business name>"` (hospitality/food) |
| Glassdoor | `site:glassdoor.com "<business name>" reviews` (employer reputation) |
| Facebook | `"<business name>" facebook reviews recommendations` |

Use WebFetch on each discovered URL to pull actual review content. If a page blocks scraping, fall back to search snippet extraction.

### Phase 3: Thematic Analysis

Categorize every collected review into one or more themes. A single review can map to multiple themes.

**Standard theme categories:**

| Theme | Trigger Keywords/Phrases |
|-------|-------------------------|
| Service Quality | service, helpful, attentive, rude, slow service, great service, above and beyond |
| Pricing/Value | expensive, overpriced, worth it, good value, cheap, affordable, rip-off, fair price |
| Wait Times | wait, waited, slow, quick, fast, took forever, prompt, on time, delayed |
| Staff/Personnel | staff, employee, team, friendly, knowledgeable, unprofessional, rude, courteous |
| Product Quality | quality, broken, defective, well-made, durable, flimsy, excellent product |
| Communication | communication, responded, ghosted, follow-up, kept informed, no response, transparent |
| Cleanliness/Atmosphere | clean, dirty, atmosphere, ambiance, filthy, spotless, comfortable, cramped |
| Location/Accessibility | location, parking, easy to find, convenient, hard to get to, accessible |
| Food/Menu | food, taste, menu, portions, fresh, stale, delicious, bland (restaurants only) |
| Technical Support | support, help desk, ticket, resolved, unresolved, bug, downtime (tech/SaaS) |
| Onboarding/Setup | setup, onboarding, getting started, learning curve, easy to use, confusing |
| Reliability | reliable, consistent, inconsistent, hit or miss, always, never |
| Management Response | owner responded, management, addressed, ignored, apologized |

**For each theme, calculate:**
- Frequency: how many reviews mention this theme
- Frequency percentage: out of total reviews collected
- Average sentiment: positive, mixed, or negative (with a numeric score from -1.0 to +1.0)
- Representative quotes: 2-3 direct quotes that exemplify the theme (one positive, one negative if both exist)

### Phase 4: Complaint and Praise Identification

**Top 3 Complaints (most frequently mentioned negative themes):**
For each complaint, provide:
- The specific issue
- How many reviews mention it
- Severity rating (Minor / Moderate / Severe / Critical)
- A direct quote exemplifying the complaint
- Whether the business has responded to reviews about this issue

**Top 3 Praise Points (most frequently mentioned positive themes):**
For each praise point, provide:
- The specific strength
- How many reviews mention it
- A direct quote exemplifying the praise
- Whether this strength appears consistent across time

### Phase 5: Platform Health Assessment

For each platform, assess:
- **Review velocity**: How many new reviews per month (estimate from dates)
- **Response rate**: What percentage of reviews (especially negative ones) received a business response
- **Response quality**: Are responses generic copy-paste or personalized and empathetic
- **Rating trend**: Is the rating trending up, down, or stable based on recent vs older reviews
- **Review authenticity signals**: Any signs of fake reviews (burst of 5-stars on same day, generic language, reviewer has no other reviews)

## Output Format

Write the output to `REVIEW-ANALYSIS-[business-name-slugified].md` in the current working directory.

```markdown
# Review Analysis: [Business Name]

**Generated:** [date]
**Platforms Analyzed:** [count]
**Total Reviews Collected:** [count]

---

## Executive Summary

[3-5 sentence summary of overall reputation health. Include the aggregate rating across platforms, the single biggest strength, and the single biggest vulnerability.]

---

## Platform Overview

| Platform | Rating | Reviews | Response Rate | Trend |
|----------|--------|---------|---------------|-------|
| Google | X.X/5 | NNN | XX% | [up/down/stable arrow] |
| Yelp | X.X/5 | NNN | XX% | [up/down/stable arrow] |
| [etc.] | | | | |

**Aggregate Rating:** X.X/5 (weighted by review volume)

---

## Rating Distribution

| Stars | Count | Percentage | Visual |
|-------|-------|------------|--------|
| 5 | NNN | XX% | [bar representation] |
| 4 | NNN | XX% | [bar representation] |
| 3 | NNN | XX% | [bar representation] |
| 2 | NNN | XX% | [bar representation] |
| 1 | NNN | XX% | [bar representation] |

---

## Thematic Analysis

### Theme Frequency Ranking

| Rank | Theme | Mentions | % of Reviews | Avg Sentiment | Sentiment Score |
|------|-------|----------|-------------|---------------|-----------------|
| 1 | [theme] | NN | XX% | [pos/mix/neg] | [+/-X.X] |
| 2 | [theme] | NN | XX% | [pos/mix/neg] | [+/-X.X] |
| [etc.] | | | | | |

### Detailed Theme Breakdown

#### [Theme Name] — [Mention Count] mentions ([Sentiment])

**What reviewers say:**
- Positive: "[direct quote]" — [Reviewer], [Platform], [Date]
- Negative: "[direct quote]" — [Reviewer], [Platform], [Date]

**Pattern:** [1-2 sentence description of the pattern within this theme]

[Repeat for each theme]

---

## Top 3 Complaints

### 1. [Complaint Title] — [Severity: Minor/Moderate/Severe/Critical]

- **Mentioned in:** NN reviews (XX%)
- **Platforms:** [which platforms this appears on]
- **Representative quote:** "[quote]"
- **Business responding:** [Yes/No/Partially — X of Y negative reviews received responses]
- **Impact assessment:** [How this likely affects new customer decisions]

### 2. [Complaint Title] — [Severity]
[same structure]

### 3. [Complaint Title] — [Severity]
[same structure]

---

## Top 3 Praise Points

### 1. [Praise Title]

- **Mentioned in:** NN reviews (XX%)
- **Platforms:** [which platforms]
- **Representative quote:** "[quote]"
- **Consistency:** [Is this consistent over time or only recent]
- **Leverage opportunity:** [How the business could amplify this strength]

### 2. [Praise Title]
[same structure]

### 3. [Praise Title]
[same structure]

---

## Platform Health Scorecard

| Metric | Google | Yelp | [Platform] | Overall |
|--------|--------|------|------------|---------|
| Review Volume | [low/med/high] | | | |
| Review Velocity (per month) | ~NN | | | |
| Response Rate | XX% | | | |
| Response Quality | [poor/fair/good/excellent] | | | |
| Rating Trend | [declining/stable/improving] | | | |
| Authenticity Confidence | [low/med/high] | | | |

---

## Recommendations

### Immediate Actions (This Week)
1. [Specific actionable recommendation]
2. [Specific actionable recommendation]

### Short-Term (This Month)
1. [Specific actionable recommendation]
2. [Specific actionable recommendation]

### Ongoing
1. [Specific actionable recommendation]
2. [Specific actionable recommendation]

---

## Raw Data: Recent Reviews

[Include the 10 most recent reviews across all platforms, formatted as:]

### [Platform] — [Star Rating] — [Date]
**Reviewer:** [Name]
> [Review text]

**Business Response:** [Response text or "No response"]

---

*Report generated by AI Reputation Manager*
```

## Important Guidelines

- Never fabricate reviews or ratings. Only report what you actually find through search and fetch.
- If a platform returns no results, note it as "No presence found on [platform]" rather than omitting it.
- If review data is limited (fewer than 10 total reviews found), flag this clearly in the executive summary and note that analysis confidence is low.
- Always attribute quotes to their source platform and approximate date.
- Weight Google and Yelp reviews more heavily in aggregate calculations as they have the highest consumer visibility.
- If the business is B2B or SaaS, prioritize G2 and Capterra over Yelp and TripAdvisor.
- If the business is a restaurant or hotel, include TripAdvisor and OpenTable in the platform search.
