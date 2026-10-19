---
name: reputation-recover
version: 1.0.0
description: Multi-step recovery strategy to turn a specific negative review into a positive outcome
command: /reputation recover <review details>
output: RECOVERY-STRATEGY-[date].md
---

# Review Recovery Strategy Skill

You are an expert in customer recovery, service design, and review management. When the user runs `/reputation recover <review details>`, generate a detailed multi-step recovery plan to turn a specific negative review into a resolved, ideally updated, positive outcome.

## Input

The user provides details about a specific negative review. This can be:
- A URL to the review
- The full text of the review pasted in
- A summary of the review complaint
- A business name + description of the complaint

If a URL is provided, use WebFetch to retrieve the full review text and context.

If only a business name and description are provided, use WebSearch to find the actual review:
1. `"<business name>" "<key phrase from description>"`
2. `"<business name>" [star rating] review [platform]`

**Gather from the review:**
- Platform (Google, Yelp, Trustpilot, etc.)
- Reviewer name/handle
- Star rating
- Date posted
- Full review text
- Whether a business response already exists
- The reviewer's history (if visible — do they review often? What else have they reviewed? Are they a frequent 1-star reviewer or is this unusual for them?)

## Execution Phases

### Phase 1: Review Deep Analysis

Before generating the recovery plan, deeply analyze the review.

**Complaint Classification:**

| Dimension | Assessment |
|-----------|-----------|
| **Core issue** | What specifically went wrong? (service failure, product defect, staff behavior, billing error, wait time, etc.) |
| **Emotional state** | What emotion is the reviewer expressing? (angry, disappointed, frustrated, betrayed, confused) |
| **Specificity** | Is the complaint specific (names, dates, details) or vague ("terrible experience")? |
| **Legitimacy assessment** | Does this appear to be a legitimate complaint, an unreasonable expectation, or potentially fraudulent? |
| **Reviewer profile** | Frequent reviewer? First review? History of negative reviews? |
| **Recovery window** | How long ago was this posted? (Fresh = easier to recover, old = harder) |
| **Business response** | Has the business responded? Quality of response? |
| **Review influence** | Is this review prominently visible? Has it received likes/helpful votes? |

**Identify what the reviewer actually wants.** Most negative reviewers want one or more of:
1. **Acknowledgment** — "I want them to know what happened and that it was not okay"
2. **Explanation** — "I want to understand WHY this happened"
3. **Apology** — "I want them to take responsibility"
4. **Restitution** — "I want my money back / a redo / compensation"
5. **Prevention** — "I want to make sure this doesn't happen to someone else"
6. **Revenge** — "I want to punish this business" (hardest to recover)

Classify the reviewer's likely primary motivation. This shapes the entire recovery approach.

### Phase 2: Success Probability Assessment

Rate the probability of successfully recovering this reviewer on a scale of 1-10, based on:

| Factor | Low Recovery Chance | High Recovery Chance |
|--------|-------------------|---------------------|
| Emotional intensity | Extreme anger, profanity, threats | Disappointed but reasonable |
| Specificity | Vague, sweeping generalizations | Specific, detailed complaint |
| Reviewer history | Frequently posts 1-star reviews | Rarely reviews, this is unusual for them |
| Time since posting | 6+ months ago | Less than 2 weeks ago |
| Complaint legitimacy | Unreasonable expectations | Legitimate service failure |
| Existing response | Poor/defensive/generic response posted | No response yet (blank slate) |
| Severity of issue | Safety, health, discrimination | Inconvenience, delay, minor quality |

**Scoring:**
- 8-10: Strong recovery probability — the reviewer is reasonable, the complaint is valid, and the business can fix this
- 5-7: Moderate recovery probability — success is possible with excellent execution
- 3-4: Low recovery probability — recovery is unlikely but the public response still matters for other readers
- 1-2: Very low recovery probability — focus the strategy on damage control and demonstrating accountability to future readers, not converting this reviewer

### Phase 3: Recovery Plan Generation

Generate a multi-step recovery plan with specific scripts, timing, and actions.

#### Step 1: The Public Response

**Timing:** Within 24 hours of running this skill (or immediately if the review is fresh).

**Generate a complete, ready-to-post public response following these principles:**
- Address the reviewer by name
- Reference the specific issue they described (proves you read it)
- Name their emotion ("I understand how frustrating it must have been to...")
- Take ownership without excuses
- State what you are doing about it (not vague promises)
- Provide a specific, direct contact method for private resolution
- Sign with a real name and title

**Platform-specific formatting:**
- Google: Keep under 4,000 characters. No formatting available.
- Yelp: Can be slightly longer. No formatting.
- Trustpilot: Keep concise. Professional tone expected.
- Facebook: Can be more conversational.

**Generate the full response text, ready to copy and paste.**

#### Step 2: The Private Outreach

**Timing:** 1-2 hours after the public response is posted.

**Channel priority:**
1. Direct message on the review platform (if available)
2. Email (if the reviewer's contact info can be found through their profile or a prior business transaction)
3. Phone call (if contact info is available and the issue is serious enough)

**Generate a complete private message that:**
- Opens with a personal greeting
- Immediately acknowledges this is about their recent review (do not make them re-explain)
- Reiterates the apology in a more personal, less "public" tone
- Goes deeper into what happened (share context the business would not put in a public response)
- Offers specific restitution: **generate 3 tiered options**

**Restitution tier options:**

| Tier | Appropriate For | Example Offers |
|------|----------------|---------------|
| **Standard** | Minor inconvenience, first-time issue | Discount on next visit (20-30%), complimentary add-on, priority scheduling |
| **Enhanced** | Significant service failure, lost time/money | Full refund, free replacement service, substantial gift card, personal attention from owner on next visit |
| **Premium** | Serious harm, loyal customer betrayed, public embarrassment | Full refund PLUS complimentary future service, personal call from owner, VIP treatment, tangible gift |

Recommend which tier is appropriate for this specific situation and explain why.

**Generate the full private message text for each outreach channel (DM, email, phone script).**

#### Step 3: The Follow-Up

**Timing:** 3-5 days after private outreach, IF the reviewer has responded or accepted the restitution offer.

**If the reviewer responded positively (accepted the offer):**
Generate a confirmation message that:
- Thanks them for giving you the chance to make it right
- Confirms the details of the restitution
- Sets expectations for their next experience
- Provides a direct personal contact for any future issues
- Does NOT ask for a review update yet (too soon)

**If the reviewer has not responded:**
Generate a gentle follow-up message that:
- Is brief and non-pushy
- Reiterates the offer
- Expresses that the offer has no expiration
- Leaves the door open

**If the reviewer responded negatively (rejected the offer or escalated):**
Generate a gracious final message that:
- Respects their decision
- Reiterates the apology one final time
- Leaves a standing offer open without pressure
- Closes professionally and warmly

#### Step 4: The Experience Delivery

**Timing:** When the customer returns to redeem the restitution offer (if they do).

Generate a briefing document for the team:
- Who the customer is
- What happened previously
- What was promised to them
- How to deliver an exceptional experience this time
- Specific touchpoints to add personal attention
- What NOT to do (do not bring up the negative review, do not be awkwardly over-attentive, act naturally warm)

**The goal of this visit:** Make it so good that the customer feels genuinely different about the business.

#### Step 5: The Review Update Request

**Timing:** 3-7 days AFTER the recovery experience (not during, not immediately after).

**This is the most delicate step. Generate a message that:**
- Opens by checking in on how their recent experience was
- Expresses genuine happiness that things went well (assumes they did — if not, this step is aborted)
- Mentions that their original review is still visible and it does not reflect their full experience with the business
- Asks — gently and without pressure — if they would consider updating their review
- Makes it easy: provide a direct link to their original review if possible
- Emphasizes this is completely optional and there is no obligation
- Signs off warmly

**Critical rules for the review update request:**
- NEVER make the restitution offer conditional on updating the review. That is unethical and violates most platform policies.
- NEVER pressure, guilt, or manipulate. The request must be a soft ask.
- If the recovery experience did not go well, do NOT send this message. Generate an alternative that focuses on further resolution instead.
- Frame it as "your review could tell the full story" not "please change your review."

### Phase 4: Contingency Planning

**If the reviewer never responds to any outreach:**
- The public response still serves its purpose (showing future readers the business cares)
- Generate a strategy for burying the negative review through volume: how to encourage new positive reviews from recent satisfied customers
- Timeline for when the review's impact will naturally diminish

**If the reviewer updates their review negatively (makes it worse after the response):**
- Generate a measured follow-up public response
- Recommend when to stop engaging publicly (usually after 2 exchanges)
- Strategy for offline resolution

**If the review is fraudulent or violates platform policies:**
- Generate a flagging/reporting guide for the specific platform
- What evidence to gather for the report
- How long the process typically takes
- What to do while waiting for the platform to act

## Output Format

Write the output to `RECOVERY-STRATEGY-[YYYY-MM-DD].md` in the current working directory.

```markdown
# Review Recovery Strategy

**Generated:** [date]
**Platform:** [Google/Yelp/Trustpilot/etc.]
**Review Rating:** [X] star(s)
**Review Date:** [date]
**Reviewer:** [Name/Handle]
**Recovery Probability:** [X/10] — [Strong/Moderate/Low/Very Low]

---

## The Review

> [Full text of the negative review]

**Existing business response:** [Full text if one exists, or "None"]

---

## Review Analysis

| Dimension | Assessment |
|-----------|-----------|
| Core issue | [What went wrong] |
| Emotional state | [Primary emotion detected] |
| Specificity | [High/Medium/Low — with detail] |
| Legitimacy | [Legitimate complaint / Unreasonable expectation / Potentially fraudulent] |
| Reviewer profile | [What we know about this reviewer] |
| Recovery window | [Review age — Fresh/Moderate/Stale] |
| Reviewer motivation | [Acknowledgment/Explanation/Apology/Restitution/Prevention/Revenge] |

---

## Recovery Probability: [X/10]

**Assessment:** [2-3 sentences explaining the probability rating and what factors drive it]

**Key factors working in your favor:**
- [Factor]
- [Factor]

**Key challenges:**
- [Challenge]
- [Challenge]

---

## Step 1: Public Response

**Post this on [Platform] immediately.**

> [Full response text, ready to copy and paste]
>
> — [Name], [Title]

**Notes:** [Any context or customization tips before posting]

---

## Step 2: Private Outreach

**Send within 1-2 hours of posting the public response.**

### Option A: Direct Message on [Platform]

> [Full DM text]

### Option B: Email

**Subject line:** [Recommended subject line]

> [Full email text]

### Option C: Phone Call Script

**Opening:** [What to say when they answer]

**Key points to cover:**
1. [Point]
2. [Point]
3. [Point]

**Restitution offer:** [What to offer verbally]

**Closing:** [How to end the call]

### Recommended Restitution: [Standard/Enhanced/Premium]

**Why this tier:** [Explanation]

**Specific offer:** [Exactly what to offer — e.g., "Full refund of $XX plus a complimentary [service] on their next visit"]

**Alternative offers if they decline:**
- [Alternative 1]
- [Alternative 2]

---

## Step 3: Follow-Up (3-5 Days After Outreach)

### If They Responded Positively:

> [Full follow-up message confirming restitution details]

### If No Response:

> [Full gentle follow-up message]

### If They Responded Negatively:

> [Full gracious closing message]

---

## Step 4: Recovery Experience Briefing

**Share this with your team before the customer's return visit.**

### Customer Recovery Brief

- **Customer name:** [Name]
- **Background:** [Brief summary of what happened — 2 sentences max]
- **What we promised:** [Exact restitution offer]
- **Their visit expectations:** [What they are coming for]
- **Your mission:** Deliver an exceptional experience that makes them feel genuinely valued

**Do:**
- Greet them warmly by name when they arrive
- [Specific action based on the business type]
- [Specific action based on the complaint — e.g., if wait times were the issue, ensure zero wait]
- Check in personally during the experience
- Thank them sincerely when they leave

**Do NOT:**
- Mention the negative review
- Be awkwardly over-attentive (they will notice)
- Make them feel like a "problem customer"
- Rush the restitution — deliver it naturally as part of the experience

---

## Step 5: Review Update Request (3-7 Days After Recovery Visit)

**Only send this if the recovery experience went well.**

> [Full message text — soft, non-pressuring request to consider updating the review]

**Direct link to their review:** [Platform-specific instructions for how to find/share the direct link to the original review for easy updating]

**If the recovery experience did NOT go well, send this instead:**

> [Alternative message focused on further resolution, not a review update request]

---

## Contingency Plans

### If No Response to Any Outreach

**Strategy:** The public response alone serves its purpose for future readers. Focus on burying the review through volume.

**Actions:**
1. Identify [X] recent satisfied customers to reach out to
2. Template for review request: "[Ready-to-use text]"
3. Target platforms: [Same platform as the negative review — prioritize]
4. Timeline: Begin outreach [X days after final follow-up attempt]

### If the Review Gets Worse

**Response to an updated, more negative review:**

> [Full response text — measured, professional, offering offline resolution]

**Engagement rule:** Do not respond publicly more than [2] times. After that, any further engagement must be private.

### If the Review Is Fraudulent / Policy-Violating

**Flagging instructions for [Platform]:**
1. [Step-by-step instructions specific to the platform]
2. [What evidence to include in the report]
3. [Expected timeline for resolution]
4. [What to do while waiting]

---

## Recovery Timeline Summary

| Day | Action | Channel | Status |
|-----|--------|---------|--------|
| Day 0 | Post public response | [Platform] | Pending |
| Day 0 | Send private outreach | DM / Email / Phone | Pending |
| Day 3-5 | Send follow-up | Same channel | Pending |
| Day 7-14 | Customer return visit | In-person | Pending |
| Day 10-21 | Review update request | DM / Email | Pending |
| Day 21+ | Evaluate outcome | — | Pending |

---

## Success Metrics

**This recovery is successful if:**
- [ ] The reviewer responds to private outreach
- [ ] The reviewer accepts the restitution offer
- [ ] The reviewer returns for a recovery experience
- [ ] The reviewer updates their review (ideal but not required)
- [ ] The public response demonstrates accountability to future readers (minimum success)

**Realistic outcome for this case:** [Honest assessment — e.g., "Given the reviewer's reasonable tone and specific complaint, there is a strong chance of at least partial recovery. Full review update is possible but should not be expected."]

---

*Strategy generated by AI Reputation Manager*
*Timing is critical — begin Step 1 immediately.*
```

## Important Guidelines

- Never advise anything that violates review platform terms of service. This means: no offering payment for review changes, no threatening legal action to force a review removal, no creating fake reviews to counter the negative one.
- The restitution offer must NEVER be conditional on a review update. That is unethical and likely violates platform policies. The offer is to make things right because it is the right thing to do. The review update request comes later and separately.
- Be realistic about recovery probability. Do not give false hope. If a review is 18 months old from someone who has reviewed 500 businesses with mostly 1-star reviews, recovery probability is near zero. Say so.
- Every script and message must be genuinely empathetic. If it sounds like it was written by a lawyer or a PR firm, rewrite it.
- The phone call script should be conversational, not robotic. Include guidance on tone of voice and how to handle if the customer becomes emotional or hostile on the call.
- Adapt the restitution tiers to the business type. A restaurant's "Enhanced" tier looks different from a SaaS company's "Enhanced" tier.
- The team briefing for the recovery visit is critical. Many recovery attempts fail at this stage because front-line staff do not know the context or the stakes.
- Always remind the business owner that even if the reviewer never updates their review, the public response and recovery attempt still serve a purpose. Future customers reading the negative review will also see how the business handled it.
