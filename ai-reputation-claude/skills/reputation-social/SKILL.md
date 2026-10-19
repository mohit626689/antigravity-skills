# Social Media Reputation Scan

## Skill Purpose
Perform a comprehensive scan of a business's social media reputation by searching across Twitter/X, LinkedIn, Facebook, Reddit, Instagram, TikTok, and industry forums. This skill uses WebSearch to find mentions, analyze sentiment, identify brand advocates and detractors, and surface trending conversations about the brand. The output is a complete social reputation snapshot.

## When to Use
- User wants to understand how their brand is perceived on social media
- User asks about social media mentions, brand sentiment, or online discussions
- User wants to find brand advocates, detractors, or influencers talking about them
- User needs to assess social reputation before a campaign, launch, or crisis response
- Triggered by `/reputation social <business name or url>`

## How to Execute

### Step 1: Identify the Business and Search Parameters

If a URL is provided, use WebSearch to determine the business name, industry, and key details from the website. If a business name is provided directly, proceed with that.

**Establish search identity:**

| Parameter | How to Determine | Example |
|---|---|---|
| Business name (exact) | User input or website title | "Acme Solutions" |
| Business name (variations) | Abbreviations, nicknames, common references | "Acme", "AcmeSolutions", "@acmesolutions" |
| Social handles | Search for official accounts | @acme on Twitter, /acmesolutions on LinkedIn |
| Branded hashtags | Search for #BusinessName variations | #AcmeSolutions, #AcmeLife |
| Products/services | Key offerings that people discuss | "Acme CRM", "Acme Pro Plan" |
| Key personnel | CEO, founders, public figures | "Jane Smith CEO Acme" |
| Industry context | What category discussions happen in | SaaS, marketing tools, CRM |

### Step 2: Platform-by-Platform Search

Execute WebSearch queries for each platform. Run searches in parallel where possible.

**Twitter/X Searches:**

```
Search 1: "[Business Name]" site:twitter.com OR site:x.com
Search 2: "[Business Name]" (complaint OR terrible OR love OR amazing) site:twitter.com
Search 3: "@[handle]" (review OR recommend OR avoid OR issue)
Search 4: "[Business Name]" -from:[official_handle] site:twitter.com (exclude own posts)
Search 5: "[Product Name]" site:twitter.com
```

**Analysis points for Twitter/X:**
- Volume of mentions (high/medium/low activity)
- Sentiment ratio of recent mentions
- Retweet/engagement levels on brand-related tweets
- Common complaints and common praise
- Influencer mentions (accounts with 10K+ followers)
- Customer service interactions (response presence, tone, speed)
- Trending topics or viral moments involving the brand

**LinkedIn Searches:**

```
Search 1: "[Business Name]" site:linkedin.com
Search 2: "[Business Name]" review OR experience site:linkedin.com
Search 3: "[CEO/Founder Name]" "[Business Name]" site:linkedin.com
Search 4: "[Business Name]" company culture OR working at site:linkedin.com
Search 5: "[Business Name]" partnership OR collaboration site:linkedin.com
```

**Analysis points for LinkedIn:**
- Company page engagement (comments, shares on posts)
- Employee advocacy (do employees share/promote the brand?)
- Thought leadership presence (articles, posts by leadership)
- Client testimonials and recommendations
- Job posting sentiment and employer brand signals
- Industry recognition and award mentions

**Facebook Searches:**

```
Search 1: "[Business Name]" site:facebook.com
Search 2: "[Business Name]" review OR complaint OR recommend site:facebook.com
Search 3: "[Business Name]" group discussion (for Facebook group mentions)
```

**Analysis points for Facebook:**
- Page rating and review count
- Community engagement (comments, reactions on posts)
- Customer complaints in comments
- Facebook Group discussions about the brand
- User-generated content and photo tags
- Recommendation posts

**Reddit Searches:**

```
Search 1: "[Business Name]" site:reddit.com
Search 2: "[Business Name]" review OR worth it OR avoid OR scam site:reddit.com
Search 3: "[Business Name]" vs OR alternative OR competitor site:reddit.com
Search 4: "[Product Name]" site:reddit.com
Search 5: "[Business Name]" experience OR honest review site:reddit.com
```

**Analysis points for Reddit:**
- Subreddits where the brand is discussed
- Thread sentiment (upvote/downvote patterns on brand-related comments)
- Common questions people ask about the brand
- Comparison threads (brand vs competitors)
- Employee or insider perspectives
- Unfiltered customer experiences
- Whether the brand has an official Reddit presence

**Instagram Searches:**

```
Search 1: "[Business Name]" site:instagram.com
Search 2: #[BusinessName] site:instagram.com
Search 3: #[BrandedHashtag] site:instagram.com
Search 4: "[Business Name]" tagged OR mention site:instagram.com
```

**Analysis points for Instagram:**
- Branded hashtag usage volume
- User-generated content quality and quantity
- Influencer partnerships and mentions
- Story mentions and tags
- Comment sentiment on official posts
- Competitor visual positioning comparison

**TikTok Searches:**

```
Search 1: "[Business Name]" site:tiktok.com
Search 2: "[Business Name]" review OR honest OR worth it site:tiktok.com
Search 3: #[BusinessName] site:tiktok.com
```

**Analysis points for TikTok:**
- Video content about the brand (reviews, unboxings, complaints)
- Viral moments (any videos with significant views)
- Trend participation (is the brand part of any TikTok trends)
- Comment section sentiment on brand-related videos
- Creator/influencer content about the brand

**Industry Forums and Communities:**

```
Search 1: "[Business Name]" forum OR community OR discussion
Search 2: "[Business Name]" review (site:quora.com OR site:producthunt.com OR site:trustpilot.com)
Search 3: "[Business Name]" [industry-specific forum domain]
```

**Industry-specific forum targets:**
- SaaS: Product Hunt, Hacker News, IndieHackers, SaaStr community
- Restaurant: Chowhound, local food blogs, OpenTable community
- Healthcare: patient forums, WebMD community, health subreddits
- Real estate: BiggerPockets, local real estate forums
- E-commerce: seller forums, product review communities

### Step 3: Sentiment Analysis

For each mention found, categorize the sentiment.

**Sentiment Classification Framework:**

| Sentiment | Indicators | Weight |
|---|---|---|
| Strongly Positive | "love", "amazing", "best", "life-changing", "highly recommend", enthusiastic language, multiple exclamation points, personal endorsement | +2 |
| Positive | "good", "nice", "solid", "recommend", "happy", satisfied tone, practical endorsement | +1 |
| Neutral | Factual mention without opinion, informational reference, news coverage without angle | 0 |
| Negative | "disappointed", "frustrated", "issues", "problems", "not great", "could be better", complaint without hostility | -1 |
| Strongly Negative | "terrible", "worst", "scam", "avoid", "never again", "rip off", hostile language, public complaint with evidence, legal threats | -2 |

**Sentiment Summary Calculation:**

```
Total Mentions Found: [N]
Strongly Positive: [n] ([%])
Positive:          [n] ([%])
Neutral:           [n] ([%])
Negative:          [n] ([%])
Strongly Negative: [n] ([%])

Sentiment Score: (sum of weighted mentions) / total mentions
Range: -2.0 (catastrophic) to +2.0 (exceptional)

Interpretation:
  +1.5 to +2.0: Exceptional social reputation
  +1.0 to +1.4: Strong positive reputation
  +0.5 to +0.9: Generally positive, some concerns
   0.0 to +0.4: Mixed reputation, needs attention
  -0.5 to -0.1: Leaning negative, action required
  -1.0 to -0.6: Significant reputation problems
  -2.0 to -1.1: Reputation crisis
```

### Step 4: Brand Advocates and Detractors

**Identifying Brand Advocates:**

Look for individuals who:
- Repeatedly mention the brand positively (3+ positive mentions)
- Recommend the brand unprompted to others
- Create user-generated content featuring the brand
- Defend the brand in negative threads
- Have significant audience reach (follower count)

**Advocate Profile Template:**

```
Handle/Name: [@username or Name]
Platform: [where they're most active]
Reach: [follower count / influence level]
Advocacy Type: [Organic fan / Power user / Industry influencer / Employee advocate]
Notable Mention: [Quote or summary of their strongest endorsement]
Engagement Opportunity: [How the brand could engage or thank them]
```

**Identifying Brand Detractors:**

Look for individuals who:
- Repeatedly post negative content about the brand
- Actively discourage others from using the brand
- Create negative review content or complaint threads
- Have significant reach that amplifies negative sentiment
- Respond to brand posts with criticism

**Detractor Profile Template:**

```
Handle/Name: [@username or Name]
Platform: [where they're most active]
Reach: [follower count / influence level]
Complaint Type: [Service issue / Product defect / Pricing / Support / Personal grudge]
Core Grievance: [Summary of their main complaint]
Frequency: [One-time vent / Recurring / Campaign against brand]
Resolution Potential: [High -- addressable issue / Medium -- complex / Low -- unreasonable]
Recommended Action: [Direct outreach / Public response / Monitor only / Ignore]
```

### Step 5: Trending Conversations

Identify any active or recent conversations trending about the brand.

**What qualifies as "trending":**
- Any single post/thread with 50+ engagements (likes, comments, shares)
- Multiple people discussing the same topic about the brand within 7 days
- A mention from a high-profile account (100K+ followers)
- A Reddit thread with 20+ upvotes about the brand
- Any news article that is generating social discussion
- A TikTok video about the brand with 10K+ views

**Trending Conversation Template:**

```
Topic: [What is being discussed]
Platform: [Where it started / where it's most active]
Started: [Date/timeframe]
Scale: [Engagement numbers]
Sentiment: [Positive / Negative / Mixed]
Key Participants: [Notable accounts involved]
Current Status: [Growing / Stable / Declining]
Brand Response: [Has responded / Has not responded / N/A]
Recommended Action: [What to do about it]
```

### Step 6: Competitive Social Comparison

If the business type is clear, briefly compare social reputation signals against 2-3 competitors.

**Comparison Points:**

| Metric | [Business] | Competitor A | Competitor B |
|---|---|---|---|
| Twitter followers | [N] | [N] | [N] |
| Twitter mention sentiment | [+/-] | [+/-] | [+/-] |
| LinkedIn followers | [N] | [N] | [N] |
| Instagram followers | [N] | [N] | [N] |
| Reddit mention volume | [High/Med/Low] | [High/Med/Low] | [High/Med/Low] |
| Reddit sentiment | [+/-] | [+/-] | [+/-] |
| TikTok presence | [Yes/No] | [Yes/No] | [Yes/No] |
| Overall social sentiment | [score] | [score] | [score] |

### Step 7: Risk Assessment

Identify potential reputation risks based on the social scan.

**Risk Categories:**

| Risk Level | Description | Criteria |
|---|---|---|
| Critical | Immediate threat to reputation | Viral negative content, active social media crisis, trending negative hashtag |
| High | Significant concern requiring action | Recurring complaint theme, growing detractor activity, negative Reddit threads with traction |
| Medium | Notable issues to monitor | Occasional negative mentions, competitors gaining social ground, declining engagement |
| Low | Minor concerns | Isolated complaints, low-reach negative mentions, minor social gaps |

### Step 8: Recommendations

Based on the scan findings, generate prioritized recommendations.

**Recommendation Categories:**

1. **Immediate Actions** (this week)
   - Respond to unanswered complaints or mentions
   - Address any active negative threads
   - Thank and engage with brand advocates

2. **Short-term Improvements** (this month)
   - Improve response time on social platforms
   - Develop response templates for common complaints
   - Engage with identified advocates

3. **Strategic Initiatives** (this quarter)
   - Build social listening infrastructure
   - Develop user-generated content program
   - Launch advocate recognition program
   - Create proactive positive content strategy

---

## Output Format

Generate a file called `SOCIAL-REPUTATION-[business-name].md`:

```markdown
# Social Media Reputation Scan
## [Business Name]
### Scan Date: [Date]

---

## Executive Summary
[3-5 sentence overview: overall social sentiment, key findings, biggest risk, biggest opportunity]

---

## Social Reputation Score: [X/100]

| Category | Score | Weight |
|---|---|---|
| Mention Volume | [X/100] | 15% |
| Sentiment Ratio | [X/100] | 30% |
| Advocate Strength | [X/100] | 15% |
| Response Presence | [X/100] | 15% |
| Competitive Position | [X/100] | 10% |
| Risk Level | [X/100] | 15% |

---

## Sentiment Analysis

**Overall Sentiment Score: [X] / 2.0**

| Sentiment | Count | Percentage |
|---|---|---|
| Strongly Positive | [n] | [%] |
| Positive | [n] | [%] |
| Neutral | [n] | [%] |
| Negative | [n] | [%] |
| Strongly Negative | [n] | [%] |

---

## Platform-by-Platform Analysis

### Twitter/X
- **Mention Volume:** [High/Medium/Low]
- **Sentiment:** [Summary]
- **Key Findings:** [Bullet points]
- **Notable Mentions:** [Specific examples]

### LinkedIn
[Same structure]

### Facebook
[Same structure]

### Reddit
[Same structure]

### Instagram
[Same structure]

### TikTok
[Same structure]

### Industry Forums
[Same structure]

---

## Brand Advocates
[Advocate profiles -- top 5-10]

## Brand Detractors
[Detractor profiles -- top 3-5, with recommended actions]

---

## Trending Conversations
[Active or recent trending discussions]

---

## Competitive Social Comparison
[Comparison table against 2-3 competitors]

---

## Risk Assessment
| Risk | Level | Platform | Details | Recommended Action |
|---|---|---|---|---|
| [risk] | [Critical/High/Medium/Low] | [platform] | [details] | [action] |

---

## Top Themes

### What People Love
1. [Theme with evidence]
2. [Theme with evidence]
3. [Theme with evidence]

### What People Complain About
1. [Theme with evidence]
2. [Theme with evidence]
3. [Theme with evidence]

---

## Recommendations

### Immediate (This Week)
1. [Action item]

### Short-Term (This Month)
1. [Action item]

### Strategic (This Quarter)
1. [Action item]

---

## Monitoring Recommendations
[Suggested ongoing monitoring approach based on findings]
```

---

## Terminal Output

Display a condensed summary:

```
=== SOCIAL MEDIA REPUTATION SCAN COMPLETE ===

Business: [name]
Scan Date: [date]

Social Reputation Score: [X]/100

Sentiment Breakdown:
  Positive:  [X]% ([n] mentions)
  Neutral:   [X]% ([n] mentions)
  Negative:  [X]% ([n] mentions)

Platform Activity:
  Twitter/X:     [High/Med/Low] activity, [sentiment]
  LinkedIn:      [High/Med/Low] activity, [sentiment]
  Facebook:      [High/Med/Low] activity, [sentiment]
  Reddit:        [High/Med/Low] activity, [sentiment]
  Instagram:     [High/Med/Low] activity, [sentiment]
  TikTok:        [High/Med/Low] activity, [sentiment]

Key Findings:
  Brand Advocates:   [N] identified
  Brand Detractors:  [N] identified
  Trending Topics:   [N] active conversations
  Risk Level:        [Critical/High/Medium/Low]

Top Praise Theme:    [theme]
Top Complaint Theme: [theme]

Full report saved to: SOCIAL-REPUTATION-[business-name].md
```

## Key Principles
- WebSearch results are a proxy for actual social media API data. Acknowledge this limitation in the report. Results represent what is publicly indexed, not the complete universe of mentions.
- Quality of analysis matters more than quantity of mentions found. Five deeply analyzed mentions are more valuable than fifty superficially listed ones.
- Always distinguish between organic mentions and paid/promotional content. Influencer sponsored posts are not the same as genuine customer sentiment.
- Reddit is the most unfiltered platform for honest opinions. Weight Reddit findings heavily in the overall assessment, but note that Reddit skews younger and more tech-savvy.
- Never fabricate mention counts or sentiment scores. If search results are limited, report what was found honestly and note the limitations.
- Competitor comparison provides critical context. A business with 80% positive sentiment sounds great until you learn competitors are at 95%.
- Detractor analysis should be empathetic, not adversarial. Most detractors have a legitimate grievance. The goal is resolution, not dismissal.
- The social scan is a point-in-time snapshot. Recommend ongoing monitoring (see `/reputation alerts`) for continuous tracking.
