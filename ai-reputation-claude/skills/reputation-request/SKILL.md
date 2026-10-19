# Review Request Campaign Generator

## Skill Purpose
Generate complete, ready-to-deploy campaigns for soliciting positive reviews from customers. This skill produces email sequences, SMS templates, in-store QR code strategies, social media ask templates, and timing recommendations tailored to the specific business type. Every template is ready to copy-paste into an email tool, CRM, or messaging platform.

## When to Use
- User wants to increase their review volume on Google, Yelp, or industry platforms
- User asks how to get more positive reviews
- User needs review request email templates or SMS scripts
- User wants a systematic review generation campaign
- Triggered by `/reputation request <business type>`

## How to Execute

### Step 1: Identify Business Type and Context

Determine the business category from the user input. If not explicitly provided, ask. The business type dictates every aspect of the campaign: timing, channel, tone, and platform priority.

**Supported Business Types and Their Review Ecosystems:**

| Business Type | Primary Review Platform | Secondary Platforms | Best Ask Channel | Optimal Ask Window |
|---|---|---|---|---|
| Restaurant / Cafe | Google Business, Yelp | TripAdvisor, OpenTable, DoorDash | In-store QR, SMS | 1-2 hours after dining |
| Dentist / Doctor | Google Business, Healthgrades | Zocdoc, Vitals, RateMDs | Email, SMS | 2-4 hours after appointment |
| SaaS / Software | G2, Capterra | TrustRadius, Product Hunt, Trustpilot | In-app prompt, Email | After milestone achievement |
| Marketing Agency | Google Business, Clutch | UpCity, Agency Spotter, LinkedIn | Email | After deliverable or win |
| Retail Store | Google Business, Yelp | Facebook, Trustpilot | Receipt QR, SMS | Same day as purchase |
| Home Services | Google Business, Yelp | Angi, HomeAdvisor, Thumbtack, BBB | SMS, Email | Within 1 hour of job completion |
| E-commerce | Trustpilot, Amazon | Google Shopping, Product reviews | Post-delivery email | 3-5 days after delivery |
| Hotel / Hospitality | TripAdvisor, Google | Booking.com, Expedia | Checkout email, QR in room | Day of checkout or next day |
| Auto Dealer / Mechanic | Google Business, Yelp | DealerRater, Cars.com, CarGurus | SMS | 2-4 hours after pickup |
| Real Estate Agent | Google Business, Zillow | Realtor.com, Homes.com, Yelp | Email | After closing, 1-3 days |
| Fitness / Gym | Google Business, Yelp | ClassPass, Mindbody | App notification, Email | After 30-day milestone |
| Legal / Attorney | Google Business, Avvo | Martindale, Lawyers.com, FindLaw | Email | After case resolution |

### Step 2: The Psychology of the Ask

Before generating templates, apply these psychological principles to every ask:

**Principle 1: Reciprocity Trigger**
Ask after you have delivered clear value. The customer should feel they received something worth talking about. Never ask before the service is complete.

**Principle 2: Specific Gratitude**
Reference something specific about their experience. "Thank you for trusting us with your kitchen remodel" beats "Thank you for your business."

**Principle 3: Ease of Action**
Every ask must include a direct link. No "go to Google and search for us." One tap to the review form. Reduce friction to near zero.

**Principle 4: Social Identity**
Frame the review as something people like them do. "Join 200+ homeowners who have shared their experience" leverages social proof to generate more social proof.

**Principle 5: Impact Framing**
Tell them WHY their review matters. "Your review helps other families find a dentist they can trust" gives the act meaning beyond the business.

**Principle 6: Timing is Everything**
The emotional peak of the experience is the ask window. For restaurants, it is right after the meal. For SaaS, it is right after a success moment. For home services, it is standing in a clean house.

**Ask Timing Matrix:**

| Emotional State | When It Happens | Ask Effectiveness |
|---|---|---|
| Peak satisfaction | Just completed service, seeing result | Highest -- ask NOW |
| Gratitude window | 1-4 hours post-service | High -- still feeling it |
| Reflection phase | 1-2 days later | Moderate -- needs reminder |
| Memory fade | 3-7 days later | Low -- requires re-engagement |
| Forgotten | 7+ days | Very low -- feels random |

### Step 3: Email Sequence Templates

Generate a 3-email sequence for the business type. Each email should be short (under 150 words), mobile-friendly, and include a direct review link placeholder.

**Email 1: The Initial Ask (Sent at optimal timing window)**

Structure:
```
Subject Line: [Personalized, specific to experience]
Preview Text: [Compelling reason to open]

Hi [First Name],

[1 sentence acknowledging their specific experience/purchase]

[1 sentence about why their feedback matters]

[Direct CTA button: "Share Your Experience" -> review link]

[1 sentence about how quick it is -- "Takes less than 60 seconds"]

[Sign-off with real person's name, not company name]
```

**Email 2: The Gentle Reminder (Sent 3-5 days after Email 1, only if no review submitted)**

Structure:
```
Subject Line: [Different angle -- focus on helping others]
Preview Text: [New reason to engage]

Hi [First Name],

[1 sentence -- "We noticed you haven't had a chance to share your experience yet"]

[1 sentence -- social proof: "Over X customers have shared their stories this month"]

[Direct CTA button: "Leave a Quick Review" -> review link]

[1 sentence -- time framing: "Most people finish in under 30 seconds"]

[Sign-off]
```

**Email 3: The Final Follow-Up (Sent 7-10 days after Email 2, only if no review submitted)**

Structure:
```
Subject Line: [Last chance framing without pressure]
Preview Text: [Impact-focused]

Hi [First Name],

[1 sentence -- "Your experience matters to us and to future customers"]

[1 sentence -- impact: what their review helps with specifically]

[Direct CTA button -> review link]

[1 sentence -- "No worries if now isn't the right time. We just wanted to make sure you had the chance."]

[Sign-off]
```

**Generate 3 complete subject line options per email:**
- Option A: Question-based ("How was your [specific service]?")
- Option B: Gratitude-based ("Thank you for choosing [business]")
- Option C: Impact-based ("Help other [audience] find [what you offer]")

### Step 4: SMS Templates

SMS must be under 160 characters where possible. Include a shortened review link placeholder.

**SMS Template 1: Immediate Post-Service**
```
Hi [Name]! Thanks for visiting [Business]. We'd love your feedback -- it takes 30 seconds: [LINK]
```

**SMS Template 2: Delayed Follow-Up (if no response)**
```
[Name], your review helps others find great [service type]. Would you mind sharing? [LINK] Thanks! - [Person Name] at [Business]
```

**SMS Template 3: After Positive Interaction**
```
So glad we could help with [specific thing], [Name]! If you have a moment, a quick review means a lot: [LINK]
```

**SMS Rules:**
- Always identify the business by name
- Always include a real person's name when possible
- Never send more than 2 SMS review requests per customer
- Respect opt-out preferences immediately
- Include opt-out language where legally required: "Reply STOP to opt out"
- Best send times: 10am-12pm or 5pm-7pm local time
- Never send on Sundays before noon

### Step 5: In-Store / On-Site QR Code Strategy

**QR Code Placement Recommendations by Business Type:**

| Business Type | Best QR Locations | Trigger Moment |
|---|---|---|
| Restaurant | On table tent, on receipt, at exit door, on check presenter | After paying, feeling satisfied |
| Dentist / Doctor | At checkout desk, in waiting room (for return visits), on appointment card | After treatment is done |
| Retail | On receipt, at register display, on shopping bag, on product tag | After purchase completion |
| Home Services | Leave-behind card, on invoice, on fridge magnet | Standing in completed space |
| Hotel | On nightstand card, at checkout desk, in departure email | During stay or at checkout |
| Auto | On invoice, on dashboard card, on key tag | Picking up their vehicle |

**QR Code Card Template:**
```
[Front of card]
-----------------------------------------
|                                       |
|   Loved your experience?              |
|                                       |
|   [QR CODE]                           |
|                                       |
|   Scan to leave a quick review        |
|   It takes less than 60 seconds       |
|                                       |
-----------------------------------------

[Back of card]
-----------------------------------------
|                                       |
|   Your review helps us serve          |
|   our community better.               |
|                                       |
|   Thank you, [Business Name]          |
|                                       |
|   Or visit: [shortened URL]           |
|                                       |
-----------------------------------------
```

**QR Code Best Practices:**
- Link directly to the review form, not the business profile page
- Use a URL shortener that allows tracking (Bitly, Rebrandly)
- Test the QR code on 3 different phones before printing
- Minimum print size: 1 inch x 1 inch
- Include a plain-text URL as backup for QR scanner issues
- Track QR scan rates by location to optimize placement

### Step 6: Social Media Ask Templates

**Facebook Post Template:**
```
We love hearing from our customers!

If we've helped you [specific benefit], we'd be grateful if you shared your experience.

Your reviews help other [audience] find [what you offer], and they mean the world to our team.

[Direct review link]

Thank you for being part of our community!
```

**Instagram Story Template:**
```
Slide 1: "You made our day!"
Slide 2: "[Customer quote or star screenshot]"
Slide 3: "Want to share your experience too?"
Slide 4: "Tap the link in our bio to leave a review"
[Link sticker directly to review page]
```

**LinkedIn Ask (for B2B/SaaS/Agency):**
```
To our clients and partners --

If we've helped you [achieve result], we'd be honored by a review on [Platform].

Your insights help other [audience] make informed decisions, and they help our team know what's working.

[Direct review link]

Thank you for your trust and partnership.
```

**Post-Positive-Interaction Reply Template (any platform):**
```
When a customer posts something positive publicly:

"Thank you so much for this, [Name]! Comments like yours make our day. If you ever have a moment, we'd love if you shared this on [Platform] too -- it really helps other [audience type] find us. [review link] Either way, thank you for being an amazing customer!"
```

### Step 7: Review Funnel Strategy

**The Review Gate (Ethical Version):**
Instead of hiding negative feedback, use a satisfaction check to route customers appropriately:

```
Step 1: Send satisfaction survey (1 question: "How was your experience? Great / OK / Not Great")

If "Great" -> Direct to public review platform with message:
  "Wonderful! We'd love for you to share that on [Platform]. [Link]"

If "OK" -> Direct to feedback form with message:
  "Thanks for letting us know. What could we have done better? [Internal feedback form]"

If "Not Great" -> Direct to manager/support with message:
  "We're sorry to hear that. [Manager Name] would like to make this right. [Contact info/form]"
```

This is NOT review gating (which violates most platform policies). This is satisfaction routing -- everyone CAN still leave a public review. You are simply making the path easier for satisfied customers while giving dissatisfied customers a faster resolution path.

### Step 8: Response Rate Optimization

**Benchmarks by Channel:**

| Channel | Average Response Rate | Good Rate | Excellent Rate |
|---|---|---|---|
| Post-service SMS | 8-12% | 15-20% | 25%+ |
| Email sequence (3 emails) | 5-8% | 10-15% | 20%+ |
| In-store QR code | 2-5% | 5-8% | 10%+ |
| In-app prompt | 10-15% | 15-25% | 30%+ |
| Social media ask | 1-3% | 3-5% | 8%+ |
| Staff verbal ask + card | 15-25% | 25-35% | 40%+ |

**Optimization Tactics:**

1. **Personalize everything** -- Use first name, reference specific service, mention the staff member who helped them
2. **A/B test subject lines** -- Test 2-3 subject lines per email, track open rates
3. **Shorten the path** -- Every extra click loses 50% of potential reviewers
4. **Staff training** -- The verbal ask from a real person converts 3-5x higher than any digital channel
5. **Incentive-free** -- Do NOT offer incentives for reviews (violates Google, Yelp, and FTC guidelines)
6. **Volume over perfection** -- Send more asks. A 10% response rate on 1000 asks beats 20% on 100
7. **Segment by satisfaction** -- Only send review requests to customers who had positive interactions or gave positive NPS scores
8. **Mobile-first** -- 70%+ of reviews are written on mobile. Every link and form must be mobile-optimized

### Step 9: Staff Training Script

**For front-line employees to use in person:**

```
The Setup (while completing the service):
"[Name], I'm really glad we could help with [specific thing]."

The Bridge:
"We actually rely a lot on reviews from customers like you --
it helps other people in [area] find us."

The Ask:
"Would you mind leaving us a quick Google review?
I can text you the link right now so it's easy."

The Close:
"Thank you so much. It really means a lot to our team."
```

**Key training points:**
- Ask while the positive emotion is still fresh
- Make eye contact and be genuine
- Never pressure -- if they hesitate, say "No worries at all"
- Offer to send the link via text so they do not have to remember
- Train ALL customer-facing staff, not just managers

### Step 10: Platform-Specific Review Link Setup

**How to get direct review links for each platform:**

| Platform | How to Get Direct Link |
|---|---|
| Google Business | Search your business on Google Maps > Click "Write a review" > Copy that URL. Or use the Place ID URL format: `https://search.google.com/local/writereview?placeid=[YOUR_PLACE_ID]` |
| Yelp | Go to your Yelp business page > Copy URL and append `/review` |
| Facebook | `https://facebook.com/[your-page]/reviews` |
| TripAdvisor | Go to your listing > Click "Write a Review" > Copy URL |
| G2 | `https://g2.com/products/[your-product]/reviews#reviews` |
| Capterra | Log into vendor portal > Get your unique review collection link |
| Healthgrades | Search your profile > Click "Leave a Review" > Copy URL |
| Trustpilot | Log into business portal > Get your unique review invitation link |

---

## Output Format

Generate a file called `REVIEW-REQUEST-CAMPAIGN-[business-type].md`:

```markdown
# Review Request Campaign
## Business Type: [Type]
### Generated: [Date]

---

## Campaign Overview
- **Target Platform(s):** [Primary and secondary platforms]
- **Campaign Duration:** 90 days (ongoing after setup)
- **Expected Review Increase:** [X-Y]% based on industry benchmarks
- **Channels:** Email, SMS, In-Store QR, Social Media, Staff Training

---

## Review Request Email Sequence

### Email 1: Initial Ask
**Send Timing:** [Specific timing for this business type]
**Subject Line Options:**
1. [Option A]
2. [Option B]
3. [Option C]

**Email Body:**
[Complete email ready to copy into email tool]

### Email 2: Gentle Reminder
**Send Timing:** [X] days after Email 1
[Complete email]

### Email 3: Final Follow-Up
**Send Timing:** [X] days after Email 2
[Complete email]

---

## SMS Templates
[All SMS templates with character counts]

---

## In-Store / On-Site Strategy
[QR code placement guide, card template, tracking setup]

---

## Social Media Ask Templates
[Platform-specific templates]

---

## Review Funnel Setup
[Satisfaction routing flowchart]

---

## Staff Training Guide
[Verbal ask script, training points, do's and don'ts]

---

## Review Link Setup Checklist
[Step-by-step for getting direct review links on target platforms]

---

## Response Rate Optimization Plan
[A/B testing plan, timing optimization, segmentation strategy]

---

## 90-Day Campaign Calendar
### Month 1: Foundation
- Week 1-2: [Setup tasks]
- Week 3-4: [Launch tasks]

### Month 2: Optimization
- Week 5-6: [Optimization tasks]
- Week 7-8: [Scaling tasks]

### Month 3: Scale
- Week 9-10: [Expansion tasks]
- Week 11-12: [Refinement tasks]

---

## Metrics to Track
| Metric | Target | How to Measure |
|---|---|---|
| Review request send rate | [X]/month | CRM or email tool |
| Review conversion rate | [X]% | Reviews received / requests sent |
| Average star rating | [X]+ stars | Platform dashboards |
| Review velocity | [X] reviews/month | Monthly count |
| Platform distribution | [breakdown] | Manual tracking |

---

## Legal and Compliance Notes
- [Platform-specific policy reminders]
- [FTC guidelines summary]
- [Incentive prohibition details]
```

---

## Terminal Output

Display a condensed summary:

```
=== REVIEW REQUEST CAMPAIGN GENERATED ===

Business Type: [type]
Target Platforms: [list]
Campaign Channels: Email (3-part sequence), SMS (3 templates),
                   QR Code, Social Media, Staff Training

Templates Generated:
  Email templates:     3 (with 9 subject line variants)
  SMS templates:       3
  Social templates:    4 (Facebook, Instagram, LinkedIn, Reply)
  QR card template:    1
  Staff script:        1

Expected Impact:
  Current review velocity:  ~[X] reviews/month (estimated)
  Target review velocity:   ~[X] reviews/month
  Timeline to see results:  30-60 days

Full campaign saved to: REVIEW-REQUEST-CAMPAIGN-[business-type].md
```

## Key Principles
- Every template must be ready to use immediately. No placeholders like "[insert benefit here]" -- use specific, realistic examples for the business type that the user can customize.
- Never suggest incentivizing reviews. This violates Google, Yelp, Trustpilot, and FTC guidelines. The consequences include review removal, account penalties, and legal liability.
- The verbal ask is the highest-converting channel. Always include staff training regardless of business type.
- Timing beats copy. A mediocre ask at the right moment outperforms a perfect ask sent a week late.
- Respect the customer. One sequence per transaction. No harassment. Easy opt-out. If they do not want to leave a review, accept it gracefully.
- Different industries have radically different review ecosystems. A dentist campaign looks nothing like a SaaS campaign. Tailor everything.
