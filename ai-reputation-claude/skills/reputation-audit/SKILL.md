# Full Reputation Audit

## Skill Purpose
Perform a comprehensive, end-to-end reputation audit for a business in a single command. This is the all-in-one version that runs every analysis sequentially: review collection and analysis, sentiment scoring, competitor benchmarking, response generation, social media scan, search presence analysis, and a complete audit report. For users who want everything in one command without needing to orchestrate multiple skills.

## When to Use
- User wants a complete reputation audit without running individual skills separately
- User asks for a "full audit", "complete analysis", or "everything" about a business's reputation
- User is new to the tool and wants the comprehensive experience
- User needs a single deliverable that covers all reputation angles
- Triggered by `/reputation audit <business name>`

## How to Execute

This skill runs 7 phases sequentially. Each phase builds on the data from previous phases. Display progress to the user after each phase completes.

```
=== REPUTATION AUDIT: [Business Name] ===
Phase 1 of 7: Review Collection and Analysis ........... [running]
Phase 2 of 7: Sentiment Deep Dive ...................... [pending]
Phase 3 of 7: Competitor Benchmarking .................. [pending]
Phase 4 of 7: Social Media Reputation Scan ............. [pending]
Phase 5 of 7: Search Presence Analysis ................. [pending]
Phase 6 of 7: Response Strategy Generation ............. [pending]
Phase 7 of 7: Final Report Compilation ................. [pending]
```

Update the status as each phase completes:
- `[running]` -- Currently executing
- `[complete]` -- Finished successfully
- `[skipped]` -- Skipped due to insufficient data
- `[pending]` -- Not yet started

---

### Phase 1: Review Collection and Analysis

**Objective:** Find and analyze reviews across all major platforms.

**WebSearch queries to execute:**
```
"[Business Name]" reviews
"[Business Name]" site:google.com/maps
"[Business Name]" site:yelp.com
"[Business Name]" site:trustpilot.com
"[Business Name]" site:bbb.org
"[Business Name]" site:facebook.com reviews
"[Business Name]" reviews [industry-specific platform]
```

**Data to collect per platform:**

| Data Point | How to Find |
|---|---|
| Platform name | Which review platform |
| Star rating | Current average rating |
| Total review count | Number of reviews |
| Recent review count | Reviews in last 90 days (estimate from search results) |
| Rating trend | Improving, stable, or declining (based on recent vs overall) |
| Response rate (estimated) | Does the business respond to reviews? What percentage? |
| Top positive themes | Most frequently praised aspects |
| Top negative themes | Most frequently complained about aspects |
| Notable reviews | Any reviews that are unusually detailed, viral, or significant |

**Platform-specific search targets by industry:**

| Industry | Primary Platforms | Secondary Platforms |
|---|---|---|
| Restaurant / Food | Google, Yelp, TripAdvisor | DoorDash, UberEats, OpenTable |
| Healthcare | Google, Healthgrades, Zocdoc | Vitals, RateMDs, WebMD |
| SaaS / Software | G2, Capterra, Google | TrustRadius, Product Hunt, Trustpilot |
| Agency / Services | Google, Clutch, Yelp | UpCity, Agency Spotter |
| Retail | Google, Yelp, Trustpilot | Facebook, Amazon (if applicable) |
| Home Services | Google, Yelp, Angi | HomeAdvisor, Thumbtack |
| Hospitality | Google, TripAdvisor, Booking.com | Expedia, Hotels.com |
| Auto | Google, DealerRater, Yelp | Cars.com, CarGurus |
| Real Estate | Google, Zillow, Realtor.com | Homes.com, Yelp |
| Legal | Google, Avvo, Martindale | FindLaw, Lawyers.com |
| Education | Google, Niche, GreatSchools | RateMyProfessors (if higher ed) |
| Fitness | Google, Yelp, ClassPass | Mindbody |

**Phase 1 Output:**
- Platform ratings summary table
- Total review count across all platforms
- Weighted average star rating
- Review velocity (estimated reviews per month)
- Top 3 positive themes with evidence
- Top 3 negative themes with evidence
- Unanswered negative review count (estimated)

---

### Phase 2: Sentiment Deep Dive

**Objective:** Analyze the sentiment distribution across all found reviews and mentions.

**Methodology:**
Using the review data collected in Phase 1 and additional search results, classify sentiment across all mentions found.

**Additional WebSearch queries:**
```
"[Business Name]" (love OR amazing OR best OR excellent OR outstanding)
"[Business Name]" (terrible OR worst OR horrible OR scam OR avoid OR never)
"[Business Name]" (okay OR decent OR fine OR average OR not bad)
```

**Sentiment Classification:**

| Sentiment | Keywords/Indicators | Score Weight |
|---|---|---|
| Strongly Positive | "love", "amazing", "best ever", "life-changing", "highly recommend", 5-star with detail | +2 |
| Positive | "good", "nice", "solid", "recommend", "happy", 4-star | +1 |
| Neutral | Factual mention, 3-star, mixed feelings, "it was okay" | 0 |
| Negative | "disappointed", "frustrated", "issues", "problems", 2-star | -1 |
| Strongly Negative | "terrible", "worst", "scam", "avoid", "never again", 1-star with detail | -2 |

**Sentiment Analysis Outputs:**
- Sentiment distribution (percentage breakdown)
- Sentiment score (-2.0 to +2.0)
- Sentiment trend over time (if discernible from search results)
- Platform-by-platform sentiment comparison
- Theme-by-theme sentiment (e.g., "service" sentiment vs "pricing" sentiment)

**Sentiment Scoring Interpretation:**

| Score | Interpretation |
|---|---|
| +1.5 to +2.0 | Exceptional -- customers are enthusiastic advocates |
| +1.0 to +1.4 | Strong -- consistently positive with minor complaints |
| +0.5 to +0.9 | Good -- generally positive but notable concerns exist |
| 0.0 to +0.4 | Mixed -- equal positive and negative signals |
| -0.5 to -0.1 | Concerning -- more negative than positive |
| -1.0 to -0.6 | Poor -- significant negative sentiment dominates |
| -2.0 to -1.1 | Crisis -- overwhelming negative sentiment |

---

### Phase 3: Competitor Benchmarking

**Objective:** Compare the business's reputation against 3-5 direct competitors.

**Finding competitors:**
```
"[Business Name]" vs
"[Business Name]" alternative
"[Business Name]" competitor
[industry] [location] (to find similar businesses)
best [industry] [location]
```

**For each competitor (top 3-5), collect:**

| Data Point | How to Find |
|---|---|
| Business name | Search results |
| Google rating + review count | Google Maps search |
| Yelp rating + review count | Yelp search |
| Other platform rating | Industry platform search |
| Estimated sentiment | Quick scan of review snippets |
| Key strength | Most praised aspect |
| Key weakness | Most complained about aspect |
| Response behavior | Do they respond to reviews? |

**Benchmarking Analysis:**

| Metric | [Business] | Comp A | Comp B | Comp C | Industry Avg |
|---|---|---|---|---|---|
| Google Rating | [X.X] | [X.X] | [X.X] | [X.X] | [X.X] |
| Google Reviews | [N] | [N] | [N] | [N] | [N] |
| Yelp Rating | [X.X] | [X.X] | [X.X] | [X.X] | [X.X] |
| Yelp Reviews | [N] | [N] | [N] | [N] | [N] |
| Response Rate | [%] | [%] | [%] | [%] | [%] |
| Sentiment Score | [X] | [X] | [X] | [X] | [X] |

**Competitive Position Assessment:**
- Where does the business rank among its competitors?
- What do competitors do better (that the business should emulate)?
- What does the business do better (that it should emphasize)?
- Are there reputation gaps that competitors exploit?

---

### Phase 4: Social Media Reputation Scan

**Objective:** Assess social media sentiment and presence.

**WebSearch queries:**
```
"[Business Name]" site:twitter.com OR site:x.com
"[Business Name]" site:reddit.com
"[Business Name]" site:linkedin.com
"[Business Name]" site:facebook.com
"[Business Name]" site:instagram.com
"[Business Name]" site:tiktok.com
"[Business Name]" (complaint OR issue OR problem) social media
"[Business Name]" (love OR recommend) social media
```

**For each platform, assess:**
- Presence: Does the business have an active profile?
- Mention volume: How often is the business discussed?
- Sentiment: What is the tone of mentions?
- Engagement: Do they respond to mentions and messages?
- Advocates: Are there vocal supporters?
- Detractors: Are there vocal critics?

**Social Reputation Summary:**

| Platform | Presence | Mention Volume | Sentiment | Engagement |
|---|---|---|---|---|
| Twitter/X | [Active/Inactive/None] | [High/Med/Low] | [Pos/Mixed/Neg] | [Good/Fair/Poor] |
| LinkedIn | [Active/Inactive/None] | [High/Med/Low] | [Pos/Mixed/Neg] | [Good/Fair/Poor] |
| Facebook | [Active/Inactive/None] | [High/Med/Low] | [Pos/Mixed/Neg] | [Good/Fair/Poor] |
| Reddit | [Discussed/Rare/None] | [High/Med/Low] | [Pos/Mixed/Neg] | [N/A] |
| Instagram | [Active/Inactive/None] | [High/Med/Low] | [Pos/Mixed/Neg] | [Good/Fair/Poor] |
| TikTok | [Active/Inactive/None] | [High/Med/Low] | [Pos/Mixed/Neg] | [Good/Fair/Poor] |

---

### Phase 5: Search Presence Analysis

**Objective:** Audit what appears on page 1 of Google when someone searches the business name.

**WebSearch queries:**
```
"[Business Name]"
[Business Name] reviews
[Business Name] complaints
[Business Name] scam
is [Business Name] legit
```

**For each search, document the top 10 results:**

| Position | URL | Domain | Sentiment | Controlled by Business? |
|---|---|---|---|---|
| 1 | [url] | [domain] | [Pos/Neu/Neg] | [Yes/No] |
| ... | ... | ... | ... | ... |

**SERP Health Score Calculation:**
- Owned positive result: +10 points
- Earned positive result: +8 points
- Neutral result: +3 points
- Negative result: -15 points
- Competitor result: -5 points
- Maximum: 100, Minimum: -150

**Search Presence Assessment:**
- How many of the top 10 results are positive/neutral?
- Are there any negative results on page 1?
- Is the Knowledge Panel present and accurate?
- What "People Also Ask" questions appear for the brand name?
- Are there any autocomplete suggestions that are negative?

---

### Phase 6: Response Strategy Generation

**Objective:** Generate ready-to-use response templates based on the actual review themes found in Phase 1.

**For each negative theme identified, generate:**

1. **Empathetic acknowledgment** of the specific complaint
2. **Explanation or context** (without being defensive)
3. **Resolution offer** (specific to the complaint type)
4. **Offline redirect** (take the conversation private)
5. **Professional sign-off** with a real name

**Template structure:**

```
"Thank you for sharing your experience, [Name]. We're sorry to hear about
[specific issue from their review]. [Brief context or acknowledgment].
We'd like to make this right -- please reach out to [contact method]
so we can [specific resolution action]. Your feedback helps us improve,
and we appreciate you bringing this to our attention.

- [Name], [Title] at [Business]"
```

**Generate templates for:**
- Top 3 negative themes (customized to each theme)
- Generic positive review response (with personalization guidance)
- Generic neutral review response
- Review that mentions a specific employee (positive)
- Review that mentions a specific employee (negative)
- Fake/suspicious review response
- Review with factual inaccuracies

**For each positive theme identified, generate:**
A thank-you response that reinforces the positive aspect and encourages return/referral.

---

### Phase 7: Final Report Compilation

**Objective:** Compile all findings into a comprehensive audit report.

**Overall Reputation Score Calculation:**

| Category | Weight | Score |
|---|---|---|
| Review Ratings (avg star rating) | 25% | [X]/100 |
| Review Volume (count and velocity) | 15% | [X]/100 |
| Sentiment Analysis (pos/neg ratio) | 20% | [X]/100 |
| Response Management (rate and quality) | 15% | [X]/100 |
| Social Reputation (mentions and sentiment) | 15% | [X]/100 |
| Search Presence (SERP health) | 10% | [X]/100 |
| **Overall Score** | **100%** | **[X]/100** |

**Grade Assignment:**

| Score | Grade |
|---|---|
| 90-100 | A+ |
| 80-89 | A |
| 70-79 | B |
| 60-69 | C+ |
| 50-59 | C |
| 40-49 | D |
| 30-39 | D- |
| 0-29 | F |

---

## Output Format

Generate a file called `REPUTATION-AUDIT-[business-name].md`:

```markdown
# Reputation Audit Report
## [Business Name]
### Audit Date: [Date]

---

## Executive Summary

**Overall Reputation Score: [X]/100 ([Grade])**

[3-5 sentence executive summary covering: current reputation state, biggest strength, biggest vulnerability, competitive position, and the single most important action to take]

---

## Score Breakdown

| Category | Score | Weight | Status |
|---|---|---|---|
| Review Ratings | [X]/100 | 25% | [Strong/Adequate/Weak/Critical] |
| Review Volume | [X]/100 | 15% | [Strong/Adequate/Weak/Critical] |
| Sentiment Analysis | [X]/100 | 20% | [Strong/Adequate/Weak/Critical] |
| Response Management | [X]/100 | 15% | [Strong/Adequate/Weak/Critical] |
| Social Reputation | [X]/100 | 15% | [Strong/Adequate/Weak/Critical] |
| Search Presence | [X]/100 | 10% | [Strong/Adequate/Weak/Critical] |

---

## Phase 1: Review Analysis

### Platform Ratings Summary
| Platform | Rating | Reviews | Trend | Response Rate |
|---|---|---|---|---|
| [Platform] | [X.X] stars | [N] | [trend] | [%] |
| ... | ... | ... | ... | ... |
| **Weighted Average** | **[X.X] stars** | **[N] total** | | |

### Review Velocity
- Current rate: ~[X] reviews per month
- Industry benchmark: ~[X] reviews per month
- Assessment: [Above/At/Below] expected velocity

### Top Positive Themes
1. **[Theme]** -- [Evidence and frequency]
2. **[Theme]** -- [Evidence and frequency]
3. **[Theme]** -- [Evidence and frequency]

### Top Negative Themes
1. **[Theme]** -- [Evidence and frequency]
2. **[Theme]** -- [Evidence and frequency]
3. **[Theme]** -- [Evidence and frequency]

---

## Phase 2: Sentiment Analysis

### Sentiment Distribution
| Sentiment | Percentage | Count |
|---|---|---|
| Strongly Positive | [X]% | [N] |
| Positive | [X]% | [N] |
| Neutral | [X]% | [N] |
| Negative | [X]% | [N] |
| Strongly Negative | [X]% | [N] |

**Sentiment Score: [X] / 2.0** ([Interpretation])
**Positive-to-Negative Ratio: [X]:1**

### Sentiment by Theme
| Theme | Sentiment | Notes |
|---|---|---|
| [Theme] | [Pos/Mixed/Neg] | [detail] |
| ... | ... | ... |

---

## Phase 3: Competitor Benchmarking

### Competitive Comparison
| Metric | [Business] | [Comp A] | [Comp B] | [Comp C] |
|---|---|---|---|---|
| Overall Score | [X] | [X] | [X] | [X] |
| Google Rating | [X.X] ([N]) | [X.X] ([N]) | [X.X] ([N]) | [X.X] ([N]) |
| Yelp Rating | [X.X] ([N]) | [X.X] ([N]) | [X.X] ([N]) | [X.X] ([N]) |
| Sentiment | [+/-] | [+/-] | [+/-] | [+/-] |
| Response Rate | [%] | [%] | [%] | [%] |
| Key Strength | [X] | [X] | [X] | [X] |
| Key Weakness | [X] | [X] | [X] | [X] |

### Competitive Position: [Rank] of [N]
[1-2 sentences on where the business stands relative to competitors]

### Competitive Advantages
[What the business does better than competitors]

### Competitive Gaps
[What competitors do better]

---

## Phase 4: Social Media Reputation

### Social Presence Summary
| Platform | Presence | Mentions | Sentiment | Engagement |
|---|---|---|---|---|
| [Platform] | [status] | [volume] | [sentiment] | [quality] |
| ... | ... | ... | ... | ... |

### Key Social Findings
[Bullet points of notable social mentions, advocates, detractors, trending conversations]

---

## Phase 5: Search Presence

### SERP Health Score: [X]/100

### Branded Search Results: "[Business Name]"
| Position | Domain | Sentiment | Controlled? |
|---|---|---|---|
| 1 | [domain] | [sentiment] | [yes/no] |
| ... | ... | ... | ... |

### Negative Content on Page 1
[List any negative results with URLs and assessment]

### Knowledge Panel Status
[Present/Missing, accuracy assessment]

---

## Phase 6: Response Templates

### Negative Review Responses

#### Template 1: [Theme] Complaint
```
[Ready-to-use response template]
```

#### Template 2: [Theme] Complaint
```
[Ready-to-use response template]
```

#### Template 3: [Theme] Complaint
```
[Ready-to-use response template]
```

### Positive Review Response
```
[Ready-to-use response template]
```

### Neutral Review Response
```
[Ready-to-use response template]
```

---

## Key Findings

| # | Severity | Finding |
|---|---|---|
| 1 | Critical | [finding] |
| 2 | High | [finding] |
| 3 | High | [finding] |
| 4 | Medium | [finding] |
| 5 | Medium | [finding] |
| 6 | Low | [finding] |

---

## 90-Day Action Plan

### Quick Wins (This Week)
1. [Specific, immediately actionable item]
2. [Specific item]
3. [Specific item]
4. [Specific item]
5. [Specific item]

### Medium-Term (1-3 Months)
1. [Specific item with expected impact]
2. [Specific item]
3. [Specific item]

### Strategic (3-6 Months)
1. [Specific item with expected impact]
2. [Specific item]
3. [Specific item]

---

## Next Steps

| Skill | When to Use | Command |
|---|---|---|
| Review Request Campaign | To increase positive review volume | `/reputation request [industry]` |
| Monitoring Setup | To set up ongoing monitoring | `/reputation alerts [business]` |
| Reputation SEO | To control search results | `/reputation seo [business]` |
| Crisis Response | If a reputation crisis occurs | `/reputation crisis [business]` |
| PDF Report | To generate a client-ready PDF | `/reputation report-pdf` |
```

---

## Terminal Output

Display a comprehensive summary:

```
=========================================================
  REPUTATION AUDIT COMPLETE: [Business Name]
=========================================================

  Overall Score:  [XX]/100  ([Grade])

  Phase Results:
    1. Review Analysis ....... COMPLETE
    2. Sentiment Deep Dive ... COMPLETE
    3. Competitor Benchmark .. COMPLETE
    4. Social Media Scan ..... COMPLETE
    5. Search Presence ....... COMPLETE
    6. Response Strategy ..... COMPLETE
    7. Report Compilation .... COMPLETE

  Score Breakdown:
    Review Ratings:        [XX]/100
    Review Volume:         [XX]/100
    Sentiment Analysis:    [XX]/100
    Response Management:   [XX]/100
    Social Reputation:     [XX]/100
    Search Presence:       [XX]/100

  Key Metrics:
    Average Star Rating:   [X.X] stars across [N] platforms
    Total Reviews:         [N] across all platforms
    Sentiment Ratio:       [X]% positive / [X]% negative
    Review Velocity:       ~[X] reviews/month
    Competitors Analyzed:  [N]
    Competitive Rank:      [X] of [N]

  Top Finding:   [Most critical finding]
  Top Action:    [Most important recommended action]

  Response Templates:  [N] generated (see report)

  Full report saved to: REPUTATION-AUDIT-[business-name].md

  Next steps:
    /reputation request [industry]  -- Get more reviews
    /reputation alerts [business]   -- Set up monitoring
    /reputation report-pdf          -- Generate PDF report
=========================================================
```

## Key Principles
- This is the flagship skill. It should be thorough enough to justify a consulting engagement if presented as a deliverable.
- Sequential execution matters. Each phase builds on previous phase data. Do not skip phases or run them out of order.
- WebSearch results are the data source. Be transparent about what was found and what could not be verified. Never fabricate data.
- The response templates should use actual themes found in Phase 1, not generic templates. If the top complaint is "long wait times," the response template should specifically address wait times.
- The competitive benchmarking should provide genuine insight, not just a data table. What can the business LEARN from its competitors' reputation?
- The action plan must be specific and prioritized. "Improve your reviews" is not an action item. "Respond to the 15 unanswered 1-star Google reviews within the next 48 hours, starting with the 3 most recent" is an action item.
- Show progress to the user. The phase-by-phase status updates keep the user informed during what can be a lengthy process.
- Always end with next steps. Guide the user to the specific skills that will help them act on the findings.
- If any phase cannot be completed due to data limitations, mark it as `[limited data]` and explain what is missing rather than guessing.
