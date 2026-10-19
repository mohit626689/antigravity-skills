# Reputation Monitoring Setup Guide

## Skill Purpose
Generate a comprehensive reputation monitoring strategy for a business, covering what platforms to track, what tools to use (free and paid), keyword monitoring setup, alert triggers, escalation procedures, team responsibilities, and daily/weekly/monthly checklists. The output is a complete operational playbook that a team can follow immediately.

## When to Use
- User wants to set up ongoing reputation monitoring
- User asks how to track reviews, mentions, or brand sentiment over time
- User needs an alert system for negative reviews or social mentions
- User wants to know what tools and processes to use for reputation monitoring
- Triggered by `/reputation alerts <business name>`

## How to Execute

### Step 1: Business Profile Discovery

Use WebSearch to understand the business and its digital footprint.

**Search queries to run:**
```
"[business name]" reviews
"[business name]" site:google.com/maps
"[business name]" site:yelp.com
"[business name]" site:bbb.org
"[business name]" site:trustpilot.com
"[business name]" site:glassdoor.com
"[business name]" site:reddit.com
"[business name]" complaints OR scam OR terrible OR worst
```

**Establish the monitoring baseline:**

| Element | What to Capture |
|---|---|
| Business name | Legal name and all variations (abbreviations, common misspellings) |
| Business type | Industry category and subcategory |
| Locations | All physical locations, service areas |
| Key personnel | CEO, founders, public-facing executives |
| Products/services | Major product names, service offerings |
| Existing review presence | Which platforms already have reviews, current counts and ratings |
| Competitors | Top 3-5 competitors to benchmark against |
| Known issues | Any existing reputation problems, past crises |

### Step 2: Platform Monitoring Matrix

Identify every platform where the business has or should have a presence, and assign monitoring priority.

**Tier 1: Monitor Daily (High Impact, High Volume)**

| Platform | Why It Matters | What to Monitor | Alert Speed |
|---|---|---|---|
| Google Business Profile | #1 review source, affects local SEO, appears in search results | New reviews, Q&A, photo uploads, suggested edits, Google Posts engagement | Immediate |
| Yelp | Major consumer trust platform, high search visibility | New reviews, check-ins, messages, business page edits | Immediate |
| Industry-specific platform | Depends on business type (see table below) | New reviews, ratings changes, profile completeness | Immediate |
| Social media (primary) | Brand mentions, customer complaints, DMs | Mentions, tags, DMs, comments, hashtag usage | Within 1 hour |

**Tier 2: Monitor Weekly (Moderate Impact)**

| Platform | Why It Matters | What to Monitor |
|---|---|---|
| Facebook | Business reviews, community mentions, group discussions | Page reviews, mentions, comments on posts |
| LinkedIn | Professional reputation, employer brand, B2B perception | Company page comments, employee mentions, industry discussions |
| BBB (Better Business Bureau) | Trust indicator, complaint resolution tracking | New complaints, rating changes |
| Glassdoor / Indeed | Employer reputation affects customer perception | New employee reviews, rating trends, CEO approval |
| Reddit | Unfiltered customer opinions, viral complaint risk | Subreddit mentions, brand discussions, complaint threads |

**Tier 3: Monitor Monthly (Lower Volume, Still Important)**

| Platform | Why It Matters | What to Monitor |
|---|---|---|
| Trustpilot | Growing consumer review platform, SEO impact | Review volume, star trend, response rate |
| Consumer complaint sites | Early warning for systemic issues | Complaints.com, PissedConsumer, Ripoff Report |
| News and media | PR issues, media coverage | Mentions in news articles, blog posts |
| Forum and community sites | Industry-specific conversations | Niche forums, Quora, Stack Exchange |
| App stores (if applicable) | Product reputation for software/apps | App Store and Play Store review trends |

**Industry-Specific Platform Priorities:**

| Business Type | Must-Monitor Platform | Why |
|---|---|---|
| Restaurant / Cafe | Google, Yelp, TripAdvisor, DoorDash/UberEats | Food service reviews heavily influence foot traffic |
| Dentist / Doctor | Healthgrades, Zocdoc, Vitals, RateMDs | Healthcare decisions driven by trust signals |
| SaaS / Software | G2, Capterra, TrustRadius, Product Hunt | B2B buying committees check these before purchasing |
| Marketing Agency | Clutch, UpCity, Google, LinkedIn | Agency selection relies on verified client reviews |
| Hotel / Hospitality | TripAdvisor, Booking.com, Expedia, Google | Travel planning revolves around review platforms |
| Auto Dealer | DealerRater, Cars.com, Google, CarGurus | Vehicle purchases are high-consideration, research-heavy |
| Real Estate | Zillow, Realtor.com, Google, Homes.com | Agent reputation directly impacts client acquisition |
| E-commerce | Trustpilot, Amazon, Google Shopping | Purchase decisions driven by product and seller reviews |
| Legal | Avvo, Martindale, Google, FindLaw | Legal clients research attorney reputation extensively |
| Home Services | Angi, HomeAdvisor, Thumbtack, Google | Local service selection depends on verified reviews |

### Step 3: Keyword Monitoring Setup

**Brand Keywords (Always Monitor):**
- Exact business name: `"[Business Name]"`
- Common misspellings: `"[Busness Name]"`, `"[Bussiness Name]"`
- Abbreviations: `"[BN]"`, `"[B.N.]"`
- Product/service names: `"[Product Name]"`
- CEO/founder name: `"[Person Name]" + "[Business Name]"`
- Domain name: `"[domain.com]"`
- Phone number: `"[phone number]"`

**Sentiment Keywords (Pair with Brand Name):**

| Category | Keywords to Monitor |
|---|---|
| Negative alerts | scam, fraud, terrible, worst, horrible, rip off, ripoff, lawsuit, complaint, avoid, warning, do not use, never again, disappointed, disgusting |
| Positive signals | love, amazing, best, recommend, fantastic, excellent, outstanding, life-changing, saved, grateful, thank you |
| Competitor mentions | "[Business Name]" vs "[Competitor]", "[Business Name]" alternative, better than "[Business Name]" |
| Crisis indicators | fired, lawsuit, investigation, health department, recall, data breach, hack, violation, shutdown, arrest |
| Employee reputation | working at "[Business Name]", "[Business Name]" culture, "[Business Name]" management, "[Business Name]" salary |

**Contextual Keywords (Industry-Specific):**
Generate 10-15 industry-specific keywords that would indicate someone is discussing the business or its category. Examples:
- Restaurant: food poisoning, health code, wait time, cold food, reservation
- Dentist: overbilling, pain, insurance, wait time, billing dispute
- SaaS: downtime, outage, bug, data loss, pricing increase, cancellation

### Step 4: Google Alerts Setup Instructions

**Step-by-step setup for each alert:**

1. Go to `https://www.google.com/alerts`
2. Create the following alerts:

**Alert 1: Brand Name (Exact Match)**
```
Query: "[Business Name]"
How often: As-it-happens
Sources: Automatic
Language: English
Region: [Business region or Any Region]
How many: All results
Deliver to: [monitoring email address]
```

**Alert 2: Brand + Negative Keywords**
```
Query: "[Business Name]" AND (scam OR fraud OR complaint OR terrible OR lawsuit OR avoid)
How often: As-it-happens
Sources: Automatic
Language: English
Region: Any Region
How many: All results
Deliver to: [monitoring email address]
```

**Alert 3: Brand + Review Keywords**
```
Query: "[Business Name]" AND (review OR reviews OR rating OR rated OR stars)
How often: As-it-happens
Sources: Automatic
Language: English
Region: Any Region
How many: All results
Deliver to: [monitoring email address]
```

**Alert 4: CEO/Founder Name**
```
Query: "[CEO Name]" AND "[Business Name]"
How often: Once a day
Sources: News
Language: English
Region: Any Region
How many: Only the best results
Deliver to: [monitoring email address]
```

**Alert 5: Competitor Monitoring (create one per competitor)**
```
Query: "[Competitor Name]" AND (review OR complaint OR news)
How often: Once a week
Sources: Automatic
Language: English
Region: [Business region]
How many: Only the best results
Deliver to: [monitoring email address]
```

**Pro tip:** Create a dedicated email address for alerts (e.g., `alerts@businessname.com` or a Gmail address like `businessname.alerts@gmail.com`) and set up filters/labels to organize incoming alerts by type.

### Step 5: Monitoring Tools Recommendations

**Free Tools:**

| Tool | What It Does | Setup Time | Limitations |
|---|---|---|---|
| Google Alerts | Monitors web mentions, news, blog posts | 10 minutes | Misses social media, forums, review platforms. Delayed results. |
| Google Business Profile notifications | Alerts for new reviews, Q&A, messages | 5 minutes | Only covers Google reviews |
| Yelp for Business app | Push notifications for new Yelp reviews | 5 minutes | Only covers Yelp |
| Facebook Page notifications | Alerts for reviews, mentions, comments | 5 minutes | Only covers Facebook ecosystem |
| Twitter/X search bookmarks | Save searches for brand mentions | 10 minutes | Manual checking required, no push alerts |
| Reddit keyword search | Search brand mentions on Reddit | 5 minutes | Manual, no real-time alerts. Use `site:reddit.com "[brand]"` in Google Alerts as workaround. |
| Social Searcher (free tier) | Basic social media monitoring | 10 minutes | Limited searches per day, delayed results |

**Paid Tools (by budget tier):**

| Budget Tier | Tool | Monthly Cost | Best For | Key Features |
|---|---|---|---|---|
| Budget ($0-50/mo) | Mention (starter) | ~$29/mo | Small businesses, solo operators | Basic web and social monitoring, email alerts |
| Mid-range ($50-200/mo) | Brand24 | ~$79/mo | Growing businesses, agencies | Sentiment analysis, influencer tracking, Slack integration |
| Mid-range ($50-200/mo) | ReviewTrackers | ~$99/mo | Multi-location businesses | Review aggregation, response management, analytics |
| Professional ($200-500/mo) | Birdeye | ~$299/mo | Multi-location, high volume | Review management, surveys, listings, social |
| Professional ($200-500/mo) | Reputation.com | ~$300/mo | Enterprise, franchise | Full reputation platform, competitive benchmarking |
| Enterprise ($500+/mo) | Sprinklr | Custom | Large enterprises | Unified CXM, AI-powered insights, omni-channel |
| Enterprise ($500+/mo) | Brandwatch | Custom | Agencies, large brands | Deep social listening, trend analysis, image recognition |

**Recommended Stack by Business Size:**

| Business Size | Recommended Stack | Monthly Cost |
|---|---|---|
| Solo / Small (1 location) | Google Alerts + Platform notifications + Social Searcher | Free |
| Growing (2-5 locations) | Google Alerts + Brand24 + Platform notifications | ~$79/mo |
| Established (5-20 locations) | ReviewTrackers + Brand24 + Google Alerts | ~$178/mo |
| Large (20+ locations) | Birdeye or Reputation.com + Brandwatch | $300-800/mo |

### Step 6: Alert Triggers and Thresholds

Define what triggers an alert and what priority level it receives.

**Alert Priority Levels:**

| Priority | Trigger | Response Time | Who Gets Notified |
|---|---|---|---|
| P0: Crisis | 1-star review mentioning legal action, health/safety issue, viral social post (50+ shares), media inquiry, data breach mention | Within 15 minutes | Owner/CEO, PR lead, legal (if applicable) |
| P1: Urgent | 1-star review on any platform, negative social post gaining traction (10+ engagements), BBB complaint filed, competitor attack | Within 1 hour | Reputation manager, department manager |
| P2: Important | 2-star review, neutral-negative social mention, employee review below 3 stars, declining rating trend | Within 4 hours | Reputation manager |
| P3: Standard | 3-star review, general brand mention, positive review (for thank-you response), competitor review | Within 24 hours | Reputation manager or assigned responder |
| P4: Informational | 4-5 star review, positive social mention, industry mention, competitor update | Within 48 hours | Logged for reporting, optional thank-you |

**Automatic Escalation Rules:**
- Any review mentioning legal/lawsuit/attorney -> Escalate to owner + legal immediately
- Any review mentioning health/safety/injury -> Escalate to owner + operations immediately
- 3 or more negative reviews within 7 days -> Escalate to owner (pattern alert)
- Rating drops below [threshold] on any platform -> Escalate to owner
- Any mention in news/media outlet -> Escalate to owner + PR
- Employee review mentioning harassment/discrimination -> Escalate to HR + legal

### Step 7: Escalation Procedures

**Escalation Flowchart:**

```
New alert received
       |
       v
Is it a crisis (P0)?
  YES -> Immediately notify Owner/CEO + PR + Legal
         -> Draft holding response within 15 min
         -> Activate crisis protocol (see /reputation crisis)
  NO  -> Continue
       |
       v
Is it negative (P1-P2)?
  YES -> Route to appropriate responder
         -> Draft response using templates (see /reputation respond)
         -> Log in tracking system
         -> Monitor for escalation (replies, shares)
  NO  -> Continue
       |
       v
Is it a review requiring response (P3-P4)?
  YES -> Queue for response within SLA
         -> Use appropriate template
         -> Log in tracking system
  NO  -> Log for monthly report
```

**Response SLA by Platform:**

| Platform | Target Response Time | Maximum Response Time |
|---|---|---|
| Google Business | 4 hours | 24 hours |
| Yelp | 4 hours | 24 hours |
| Facebook | 1 hour (comments/DMs) | 4 hours |
| Twitter/X | 30 minutes (public mentions) | 2 hours |
| TripAdvisor | 24 hours | 48 hours |
| BBB | 24 hours | 48 hours (BBB mandates within 14 days) |
| Glassdoor | 48 hours | 1 week |
| Reddit | Assess before responding (see note) | N/A |
| Industry platforms | 24 hours | 48 hours |

**Reddit Note:** Reddit requires a careful approach. Do NOT use a branded account to respond defensively. If the business already has a genuine Reddit presence, respond transparently. If not, monitor only and address systemic issues internally. Responding on Reddit when the community perceives it as damage control often backfires.

### Step 8: Team Responsibilities

**RACI Matrix for Reputation Monitoring:**

| Activity | Owner/CEO | Reputation Manager | Front-line Staff | Marketing | Legal |
|---|---|---|---|---|---|
| Daily monitoring dashboard check | I | R/A | - | I | - |
| Respond to positive reviews | I | R/A | C | - | - |
| Respond to negative reviews | C | R/A | C | I | C (if needed) |
| Crisis response | A | R | I | R | C |
| Monthly reputation report | A | R | - | C | - |
| Review request campaigns | A | R | R | C | - |
| Competitor monitoring | I | R | - | C | - |
| Employee review monitoring | A | R | - | - | C |
| Google Alerts management | I | R/A | - | - | - |
| Tool subscription management | A | R | - | - | - |

R = Responsible, A = Accountable, C = Consulted, I = Informed

**Role Definitions:**

**Reputation Manager (primary):**
- Checks all monitoring dashboards daily
- Responds to all reviews within SLA
- Escalates P0 and P1 alerts immediately
- Produces weekly and monthly reports
- Manages monitoring tools and alert configuration
- Trains staff on review request procedures

**Owner/CEO:**
- Reviews weekly reputation summary
- Approves crisis response strategy
- Makes final decisions on difficult responses
- Reviews monthly reputation trends

**Front-line Staff:**
- Executes review request campaigns (verbal asks, QR distribution)
- Flags customer complaints or issues to Reputation Manager
- Does NOT respond to online reviews or social mentions directly

### Step 9: Monitoring Checklists

**Daily Checklist (5-10 minutes):**
- [ ] Check Google Business Profile for new reviews and Q&A
- [ ] Check Yelp for new reviews and messages
- [ ] Check industry-specific platform for new reviews
- [ ] Check social media mentions and DMs (primary platforms)
- [ ] Review Google Alerts email digest
- [ ] Respond to any reviews within SLA
- [ ] Log new reviews in tracking spreadsheet
- [ ] Escalate any P0 or P1 alerts

**Weekly Checklist (30-45 minutes):**
- [ ] Calculate weekly review count by platform
- [ ] Calculate weekly average rating by platform
- [ ] Review sentiment trends (positive/negative/neutral ratio)
- [ ] Check Facebook, LinkedIn, BBB for new reviews
- [ ] Check Glassdoor/Indeed for new employee reviews
- [ ] Search Reddit for brand mentions
- [ ] Review competitor ratings and recent reviews (top 3)
- [ ] Identify and document top complaint themes
- [ ] Identify and document top praise themes
- [ ] Update response templates if new patterns emerge
- [ ] Brief owner/CEO on any notable developments

**Monthly Checklist (2-3 hours):**
- [ ] Produce monthly reputation report (see output format below)
- [ ] Calculate month-over-month rating trends across all platforms
- [ ] Calculate review velocity (reviews per month) by platform
- [ ] Analyze sentiment breakdown with percentages
- [ ] Review response rate and average response time
- [ ] Compare ratings against competitors
- [ ] Audit Google Alerts -- add/remove keywords as needed
- [ ] Audit monitoring tools -- check all integrations are working
- [ ] Review and update escalation procedures if needed
- [ ] Identify systemic issues from recurring complaint themes
- [ ] Present findings and recommendations to leadership
- [ ] Plan next month's review request campaign adjustments

**Quarterly Checklist (half day):**
- [ ] Full platform audit -- ensure profiles are claimed, complete, and accurate on all platforms
- [ ] Review and update monitoring tool stack
- [ ] Competitive reputation benchmark (full comparison)
- [ ] Review and update response templates
- [ ] Staff training refresher on review request procedures
- [ ] Evaluate ROI of paid monitoring tools
- [ ] Set goals for next quarter (review volume, rating targets, response time)

### Step 10: Tracking and Reporting Template

**Weekly Tracking Spreadsheet Structure:**

| Column | Description |
|---|---|
| Date | Date of review or mention |
| Platform | Where it appeared |
| Type | Review, mention, complaint, compliment |
| Rating | Star rating (if applicable) |
| Sentiment | Positive, Negative, Neutral |
| Summary | 1-line summary of content |
| Theme | Category (service, price, quality, staff, wait time, etc.) |
| Response Status | Responded / Pending / Not Required |
| Response Time | Hours between review and response |
| Escalated | Yes/No |
| Resolved | Yes/No/N/A |

---

## Output Format

Generate a file called `MONITORING-GUIDE-[business-name].md`:

```markdown
# Reputation Monitoring Guide
## [Business Name]
### Generated: [Date]

---

## Business Profile
- **Business Name:** [name]
- **Industry:** [type]
- **Locations:** [count and areas]
- **Current Rating Overview:**
  - Google: [X] stars ([N] reviews)
  - Yelp: [X] stars ([N] reviews)
  - [Platform]: [X] stars ([N] reviews)

---

## Platform Monitoring Matrix

### Tier 1: Daily Monitoring
[Platform list with what to monitor and how]

### Tier 2: Weekly Monitoring
[Platform list]

### Tier 3: Monthly Monitoring
[Platform list]

---

## Keyword Monitoring
### Brand Keywords
[Complete keyword list]

### Sentiment Keywords
[Negative and positive keyword pairs]

### Industry Keywords
[Contextual monitoring terms]

---

## Google Alerts Setup
[Step-by-step for each alert with exact queries]

---

## Recommended Tools
### Free Stack
[Tools with setup instructions]

### Recommended Paid Stack
[Tools with justification and cost]

---

## Alert Triggers and Priority Levels
[P0 through P4 definitions with response times]

---

## Escalation Procedures
[Flowchart and contact list template]

---

## Team Responsibilities
[RACI matrix and role definitions]

---

## Monitoring Checklists
### Daily (5-10 min)
[Checklist]

### Weekly (30-45 min)
[Checklist]

### Monthly (2-3 hours)
[Checklist]

### Quarterly (half day)
[Checklist]

---

## Tracking Template
[Spreadsheet structure and KPI definitions]

---

## Response SLAs
[Platform-by-platform response time targets]

---

## Competitor Monitoring
[What to track for each competitor]

---

## Setup Action Plan
### Week 1: Foundation
- [ ] Claim and verify all business listings
- [ ] Set up Google Alerts (all 5 queries)
- [ ] Enable notifications on all review platforms
- [ ] Create monitoring email address
- [ ] Set up free monitoring tools

### Week 2: Process
- [ ] Create tracking spreadsheet
- [ ] Define team roles and responsibilities
- [ ] Set up escalation contact list
- [ ] Train team on monitoring procedures

### Week 3: Optimization
- [ ] Evaluate and select paid tools (if budget allows)
- [ ] Set up integrations (Slack, email, etc.)
- [ ] Run first weekly report
- [ ] Adjust alert keywords based on initial results

### Week 4: Steady State
- [ ] Confirm all alerts are firing correctly
- [ ] Run first monthly report
- [ ] Document any gaps or adjustments needed
- [ ] Schedule recurring calendar reminders for all checklists
```

---

## Terminal Output

Display a condensed summary:

```
=== REPUTATION MONITORING GUIDE GENERATED ===

Business: [name]
Industry: [type]

Monitoring Coverage:
  Tier 1 (Daily):    [X] platforms
  Tier 2 (Weekly):   [X] platforms
  Tier 3 (Monthly):  [X] platforms
  Total platforms:    [X]

Alerts Configured:
  Google Alerts:      5 queries
  Keywords tracked:   [X] brand + [X] sentiment + [X] industry
  Alert priorities:   P0 (Crisis) through P4 (Informational)

Recommended Tools:
  Free:  [list]
  Paid:  [list] (~$[X]/month)

Setup timeline: 4 weeks to full operational monitoring

Full guide saved to: MONITORING-GUIDE-[business-name].md
```

## Key Principles
- Monitoring without action is pointless. Every alert must have a clear owner and response procedure.
- Start with free tools and upgrade only when volume or complexity demands it. Google Alerts + platform notifications cover 80% of what small businesses need.
- The daily checklist should take under 10 minutes. If it takes longer, the process is too complex and will be abandoned.
- False positives are better than missed negatives. Cast a wide net with keywords and filter manually rather than risk missing a crisis.
- Competitor monitoring is not optional. Reputation is relative. A 4.2-star rating is excellent if competitors average 3.8, but concerning if they average 4.7.
- Employee reputation (Glassdoor, Indeed) affects customer reputation. Candidates and customers both search the business name.
- Document everything in the tracking spreadsheet. Patterns only emerge with data over time.
