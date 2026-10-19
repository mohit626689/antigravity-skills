# Reputation SEO Strategy

## Skill Purpose
Generate a comprehensive plan to control what appears on page 1 of Google when someone searches for the business name. This skill focuses on pushing negative content off the first page of search results by building a wall of positive, owned, and optimized content. The output is a complete publishing plan, profile optimization guide, and content calendar designed specifically for reputation-driven SEO.

## When to Use
- User wants to control what shows up when someone Googles their business name
- User has negative search results they want pushed down
- User wants to strengthen their branded search results
- User asks about online reputation and SEO
- User needs a content strategy specifically for reputation management
- Triggered by `/reputation seo <business name>`

## How to Execute

### Step 1: Branded Search Audit

Use WebSearch to analyze the current state of page 1 results for the business name.

**Search queries to execute:**
```
Search 1: "[Business Name]" (exact match)
Search 2: [Business Name] reviews
Search 3: [Business Name] complaints
Search 4: [Business Name] scam
Search 5: [Business Name] [city] (if local business)
Search 6: "[CEO/Founder Name]" (personal reputation)
Search 7: [Business Name] vs [competitor]
Search 8: is [Business Name] legit
Search 9: [Business Name] reddit
Search 10: [Business Name] glassdoor
```

**For each search, document the first page results:**

| Position | URL | Domain | Title | Sentiment | Controlled? |
|---|---|---|---|---|---|
| 1 | [url] | [domain] | [title] | Positive/Neutral/Negative | Yes/No |
| 2 | [url] | [domain] | [title] | Positive/Neutral/Negative | Yes/No |
| ... | ... | ... | ... | ... | ... |
| 10 | [url] | [domain] | [title] | Positive/Neutral/Negative | Yes/No |

**Result Classification:**

| Type | Definition | Examples |
|---|---|---|
| Owned | Properties the business fully controls | Company website, blog, social profiles |
| Earned | Third-party content that is positive | Positive reviews, press coverage, awards |
| Neutral | Informational without strong sentiment | Wikipedia, directory listings, data aggregators |
| Negative | Harmful to reputation | Complaint sites, negative reviews, bad press, critical Reddit threads |
| Competitor | Competitor content ranking for your name | Competitor comparison pages, "alternative to" content |

**Current SERP Health Score:**

```
Scoring:
  Owned positive result:    +10 points
  Earned positive result:   +8 points
  Neutral result:           +3 points
  Negative result:          -15 points
  Competitor result:        -5 points

Maximum possible: 100 (all 10 results are owned/positive)
Minimum possible: -150 (all results are negative)

Score interpretation:
  80-100:  Excellent -- dominant branded SERP presence
  60-79:   Good -- mostly controlled, minor gaps
  40-59:   Fair -- some vulnerabilities, room to improve
  20-39:   Concerning -- negative content visible on page 1
  0-19:    Poor -- significant negative presence
  Below 0: Crisis -- negative content dominates page 1
```

### Step 2: Identify Negative Content to Displace

For each negative result found on page 1, analyze its strength and determine the displacement strategy.

**Negative Result Analysis Template:**

| Factor | Assessment |
|---|---|
| URL | [full URL] |
| Current position | [1-10] |
| Domain authority | [High/Medium/Low -- based on domain reputation] |
| Content freshness | [Date published or last updated] |
| Engagement signals | [Comments, shares, links pointing to it] |
| Displacement difficulty | [Easy / Moderate / Hard / Very Hard] |
| Removal possible? | [Yes -- contact site / Yes -- legal / No -- must outrank] |

**Displacement Difficulty Guide:**

| Difficulty | When This Applies | Strategy |
|---|---|---|
| Easy | Low-authority site, old content, no engagement | 2-3 new optimized pages can push it to page 2 within 4-8 weeks |
| Moderate | Medium-authority site, some engagement, relatively fresh | 5-7 new pages needed, may take 2-4 months |
| Hard | High-authority site (major review platform, news outlet), significant engagement | Requires 8-10+ new pages, extensive link building, 4-6 months |
| Very Hard | Major news outlet, viral content, legal content (court records) | May require legal action, sustained 6-12 month campaign, professional ORM firm |

### Step 3: Content Removal and Suppression Tactics

Before building new content, attempt removal where possible.

**Removal Options (in order of preference):**

1. **Direct contact with the website/author**
   - Polite, professional outreach requesting removal or update
   - Works best for: outdated content, factual errors, resolved complaints
   - Success rate: 10-20% but worth attempting

2. **Google content removal requests**
   - For content containing personal information (doxxing, phone numbers, financial data)
   - For outdated content about the business via Google's "Outdated Content" removal tool
   - URL: `https://support.google.com/websearch/troubleshooter/9685456`

3. **Legal removal (DMCA, defamation, court order)**
   - Last resort for clearly defamatory, false, or legally actionable content
   - Requires legal counsel
   - Can request Google de-index via court order

4. **Review platform dispute process**
   - Flag reviews that violate platform guidelines (fake, irrelevant, conflicts of interest)
   - Each platform has its own dispute process
   - Success rate varies: 5-15% for legitimate disputes

**If removal is not possible, the only option is suppression through new positive content. That is what the rest of this strategy addresses.**

### Step 4: Profile Optimization Strategy

Social profiles and business listings rank extremely well for branded searches because they are on high-authority domains. Claim and optimize every possible profile.

**Tier 1: Must-Have Profiles (rank on page 1 almost always)**

| Platform | URL Pattern | Optimization Priority |
|---|---|---|
| LinkedIn Company Page | linkedin.com/company/[name] | Complete all fields, post weekly, get employee connections |
| Google Business Profile | Appears as Knowledge Panel | Complete all fields, add photos weekly, respond to all reviews |
| Facebook Business Page | facebook.com/[name] | Complete profile, maintain active posting |
| Twitter/X | x.com/[name] | Complete bio, active posting, consistent branding |
| YouTube Channel | youtube.com/@[name] | Optimized channel description, at least 3-5 videos |
| Instagram | instagram.com/[name] | Complete bio with keywords, consistent posting |
| Crunchbase (if applicable) | crunchbase.com/organization/[name] | Complete company profile with funding, team, description |
| BBB | bbb.org/[region]/[name] | Claim listing, respond to complaints, maintain A+ rating |

**Tier 2: Supporting Profiles (help fill page 1)**

| Platform | Why It Helps |
|---|---|
| Medium | High domain authority, articles rank well for branded searches |
| Pinterest | Business profile ranks for branded image searches |
| TikTok | Growing authority, video content ranks for branded searches |
| GitHub (if tech) | High authority domain, shows technical credibility |
| Glassdoor | Employer profile, high authority for "[company] reviews" searches |
| Apple Podcasts (if applicable) | Podcast listings rank well |
| Industry directories | Clutch, G2, Capterra, Yelp, etc. -- high authority domains |

**Tier 3: Additional Properties (fill gaps)**

| Platform | When to Use |
|---|---|
| About.me | For personal name reputation management |
| WordPress.com or Substack | Secondary blog on high-authority domain |
| SlideShare | Presentations rank for branded + topic searches |
| Quora Spaces | Answers and Spaces rank for branded + question searches |
| AngelList/Wellfound (if startup) | High authority startup directory |
| Behance or Dribbble (if creative) | Portfolio sites rank well |

**Profile Optimization Checklist (apply to EVERY profile):**

- [ ] Business name is EXACT and consistent across all profiles
- [ ] Description includes the business name in the first sentence
- [ ] Description includes primary industry keywords
- [ ] Profile photo/logo is consistent across all platforms
- [ ] Cover image is branded and professional
- [ ] Website URL links to the main business site
- [ ] Contact information is complete and consistent
- [ ] Location information is accurate (for local businesses)
- [ ] All available fields are filled in (do not leave anything blank)
- [ ] Profile URL is customized (e.g., linkedin.com/company/acme not linkedin.com/company/83749273)

### Step 5: Content Creation Strategy

The goal is to create content on high-authority domains that will rank for the business name and push negative results to page 2.

**Content Type Priority Matrix:**

| Content Type | Domain Authority Boost | Time to Rank | Effort Level | Recommended Quantity |
|---|---|---|---|---|
| Press releases | High (distributed to news sites) | 2-4 weeks | Medium | 1-2 per month |
| Guest posts on industry blogs | High (established domains) | 4-8 weeks | High | 2-4 per month |
| Medium articles | High (medium.com authority) | 2-4 weeks | Low-Medium | 2-4 per month |
| YouTube videos | High (youtube.com authority) | 1-4 weeks | Medium-High | 2-4 per month |
| LinkedIn articles | High (linkedin.com authority) | 1-2 weeks | Low-Medium | 2-4 per month |
| Company blog posts | Medium (depends on site authority) | 4-12 weeks | Medium | 4-8 per month |
| Podcast appearances | Medium-High | 2-8 weeks | Medium | 1-2 per month |
| Case studies | Medium | 4-8 weeks | High | 1-2 per month |
| Industry directory profiles | High (directory authority) | 1-4 weeks | Low | Claim all relevant |
| Wikipedia (if notable) | Very High | Weeks to months | Very High | Only if legitimately notable |

**Content Optimization Rules for Reputation SEO:**

1. **Every piece of content MUST include the business name in:**
   - Title/headline (preferably near the beginning)
   - First paragraph (within the first 50 words)
   - Meta title and meta description (if applicable)
   - Image alt text (at least one image)
   - URL slug (if controllable)

2. **Title formulas optimized for branded search:**
   ```
   "[Business Name]: [Value Proposition or Achievement]"
   "[Founder Name], CEO of [Business Name], on [Topic]"
   "How [Business Name] [Achieved Result] for [Client/Industry]"
   "[Business Name] Named [Award] by [Authority]"
   "[Business Name] Launches [Product/Initiative]"
   "The Story Behind [Business Name]: [Compelling Angle]"
   ```

3. **Internal linking strategy:**
   - Every piece of external content should link back to the business website
   - The business website should have an organized press/media page linking to all external content
   - Create a "hub and spoke" structure: main website is the hub, all external content points back to it

### Step 6: Link Building for Reputation

Backlinks to positive content help it rank higher and push negative content down.

**Link Building Tactics (ethical, white-hat only):**

| Tactic | How It Works | Difficulty | Impact |
|---|---|---|---|
| HARO / Connectively | Respond to journalist queries, get quoted with a link | Medium | High -- links from news sites |
| Guest posting | Write articles for industry blogs with link in bio | Medium | Medium-High |
| Podcast appearances | Appear on podcasts, get linked in show notes | Low-Medium | Medium |
| Sponsorships | Sponsor local events, charities, get linked on their sites | Low | Medium |
| Award submissions | Apply for industry awards, get listed on award sites | Low | Medium |
| Partner pages | Get listed on partner/client websites | Low | Medium |
| Local citations | Get listed on local business directories with consistent NAP | Low | Medium (for local) |
| Data/research publishing | Create original research, get cited by other publications | High | Very High |
| Infographic distribution | Create shareable infographics, get embedded with attribution links | Medium | Medium |

**Link Building Priorities by Content Type:**

For each new piece of positive content published, aim for:
- 3-5 links within the first 30 days
- Links from domains with higher authority than the negative content being displaced
- Anchor text that includes the business name naturally

### Step 7: Google Knowledge Panel Optimization

The Google Knowledge Panel (right side of search results for branded queries) is prime reputation real estate.

**Knowledge Panel Optimization:**
- Claim the Knowledge Panel via Google Search verification
- Ensure all information is accurate and complete
- Add official social profiles
- Add logo and cover image
- Monitor for suggested edits by the public (Google allows crowdsourced edits)
- Maintain active Google Business Profile (for local businesses)
- Ensure Wikipedia article accuracy (if one exists -- the Knowledge Panel pulls from Wikipedia)

**People Also Ask Optimization:**
- Identify "People Also Ask" questions that appear for branded searches
- Create content that directly answers these questions
- Structure content with the exact question as an H2 heading followed by a concise answer paragraph
- Common branded PAA questions to target:
  ```
  "Is [Business Name] legit?"
  "What does [Business Name] do?"
  "[Business Name] reviews"
  "Who owns [Business Name]?"
  "Where is [Business Name] located?"
  "How much does [Business Name] cost?"
  ```

### Step 8: Review Profile Strengthening

Review listings rank extremely well for branded searches. A strong review presence fills page 1 with positive signals.

**Review SEO Strategy:**
- Increase review volume on Google (most important for SERP presence)
- Respond to ALL reviews (responses add content that Google indexes)
- Include business name and keywords naturally in review responses
- Diversify review platforms (each platform listing can occupy a page 1 position)
- Target 4.0+ average rating on all platforms (below 4.0 triggers negative perception)

**Review response SEO template:**
```
"Thank you for your review of [Business Name], [Customer First Name].
We're glad [specific positive thing they mentioned]. Our team at
[Business Name] works hard to [value related to their compliment].
We look forward to serving you again!"
```

This template naturally includes the business name twice, which reinforces the branded keyword association for the review page.

### Step 9: 90-Day Content Calendar

**Month 1: Foundation (Weeks 1-4)**

| Week | Action Items |
|---|---|
| Week 1 | Claim and optimize all Tier 1 profiles. Audit and fix any profile inconsistencies. Set up Google Business Profile completely. |
| Week 2 | Claim all Tier 2 profiles. Publish first Medium article. Publish first LinkedIn article. Post first YouTube video (even if simple). |
| Week 3 | Claim Tier 3 profiles. Send first press release. Write and publish 2 blog posts optimized for business name. Submit for 2 industry directories. |
| Week 4 | Begin guest post outreach (pitch 10 sites). Record first podcast pitch. Publish second Medium and LinkedIn article. Respond to all existing reviews. |

**Month 2: Acceleration (Weeks 5-8)**

| Week | Action Items |
|---|---|
| Week 5 | Publish 2 guest posts. Publish 2 blog posts. Publish 1 YouTube video. Share all content across social profiles. |
| Week 6 | Send second press release. Publish 1 Medium article. Begin HARO responses (daily). Submit for 3 more industry directories. |
| Week 7 | Publish 2 guest posts. Create and distribute 1 infographic. Publish case study. Build 5 links to strongest positive content. |
| Week 8 | Mid-campaign SERP audit. Adjust strategy based on what is moving. Double down on content types that are ranking. Publish 2 more blog posts. |

**Month 3: Domination (Weeks 9-12)**

| Week | Action Items |
|---|---|
| Week 9 | Publish 2 guest posts. Publish original research or data piece. Continue HARO. Publish 1 YouTube video. |
| Week 10 | Send third press release. Publish 2 blog posts. Push for award submissions. Build 5 more links to priority content. |
| Week 11 | Publish 2 more guest posts. Create second infographic. Publish LinkedIn article. Audit review presence and launch review request campaign if needed. |
| Week 12 | Full SERP re-audit. Compare against baseline. Document progress. Plan months 4-6 strategy. Present results. |

**Monthly Content Minimums:**
- Blog posts: 4-8
- Medium articles: 2-4
- LinkedIn articles: 2-4
- YouTube videos: 2-4
- Guest posts: 4-6
- Press releases: 1-2
- Podcast appearances: 1-2
- Social media posts: Daily on primary platforms

### Step 10: Ongoing Maintenance

After the initial 90-day push, maintain the gains with ongoing activity.

**Monthly maintenance minimums:**
- 2-4 blog posts
- 1-2 external articles (Medium, LinkedIn, guest posts)
- 1 YouTube video
- Daily social media posting
- Review response within 24 hours
- Monthly SERP audit to check for new threats
- Quarterly full audit

**Warning signs to watch for:**
- New negative content appearing on page 1
- Existing positive content dropping in rankings
- Competitor content ranking for your business name
- Review rating declining on any platform
- Negative "People Also Ask" questions appearing

---

## Output Format

Generate a file called `REPUTATION-SEO-[business-name].md`:

```markdown
# Reputation SEO Strategy
## [Business Name]
### Generated: [Date]

---

## Current SERP Analysis

### Branded Search: "[Business Name]"
| Position | URL | Sentiment | Controlled? |
|---|---|---|---|
| 1 | [url] | [sentiment] | [yes/no] |
| ... | ... | ... | ... |

**SERP Health Score: [X]/100**

### Negative Content to Displace
[Analysis of each negative result with displacement difficulty]

---

## Profile Optimization Plan
### Tier 1 (Must-Have)
[Profile list with optimization checklist]

### Tier 2 (Supporting)
[Profile list]

### Tier 3 (Gap Fillers)
[Profile list]

---

## Content Strategy
### Content Types and Targets
[Priority matrix with quantities]

### Title Formulas
[Templates optimized for branded search]

### Content Optimization Rules
[SEO requirements for every piece of content]

---

## Link Building Plan
[Tactics, priorities, and targets]

---

## Knowledge Panel Optimization
[Steps to claim and optimize]

---

## Review SEO Strategy
[Review-specific SEO actions]

---

## 90-Day Content Calendar
### Month 1: Foundation
[Week-by-week action items]

### Month 2: Acceleration
[Week-by-week action items]

### Month 3: Domination
[Week-by-week action items]

---

## Expected Timeline
| Milestone | Timeframe | Metric |
|---|---|---|
| Profile optimization complete | Week 2 | All profiles claimed and optimized |
| First new content ranking | Weeks 3-4 | 1-2 new results on page 1 |
| Negative content pushed to position 8-10 | Months 2-3 | Visible improvement |
| Page 1 majority positive | Months 3-4 | 7+ positive/neutral results |
| Full page 1 control | Months 4-6 | 9-10 positive/owned results |

---

## Ongoing Maintenance Plan
[Monthly and quarterly maintenance tasks]

---

## Metrics to Track
| Metric | Current | 30-Day Target | 90-Day Target |
|---|---|---|---|
| SERP Health Score | [X] | [X] | [X] |
| Positive results on page 1 | [X] | [X] | [X] |
| Negative results on page 1 | [X] | [X] | [X] |
| Controlled results on page 1 | [X] | [X] | [X] |
```

---

## Terminal Output

Display a condensed summary:

```
=== REPUTATION SEO STRATEGY GENERATED ===

Business: [name]
SERP Health Score: [X]/100

Current Page 1 Breakdown:
  Owned/Positive:  [X] results
  Earned/Neutral:  [X] results
  Negative:        [X] results
  Competitor:      [X] results

Negative Content Found:
  [X] negative results to displace
  Hardest to displace: [URL] (difficulty: [level])

Strategy Summary:
  Profiles to optimize:    [X]
  Content pieces planned:  [X] over 90 days
  Link building targets:   [X] links per month
  Expected timeline:       [X] months to page 1 control

Full strategy saved to: REPUTATION-SEO-[business-name].md
```

## Key Principles
- Reputation SEO is a marathon, not a sprint. Set realistic expectations. Displacing a high-authority negative result can take 3-6 months of sustained effort.
- Quantity of quality content matters. You cannot rank one blog post against a New York Times article. You need a volume of content across multiple high-authority domains to create a wall of positive results.
- Consistency of brand name usage across all content is critical. Every piece of content must use the exact business name to reinforce the branded keyword signal.
- Profile optimization is the lowest-effort, highest-impact first step. LinkedIn, Facebook, Twitter, and YouTube profiles rank for almost every branded search simply because they are on high-authority domains.
- Never use black-hat SEO tactics for reputation management. Link farms, fake reviews, and content spinning will eventually backfire and can result in penalties that make the situation worse.
- Review SEO is often overlooked. A Google Business Profile with 200+ reviews and a 4.5-star rating dominates branded search results and sends an immediate positive signal.
- Personal name reputation is as important as business name reputation for founders and CEOs. Include personal brand strategy if relevant.
