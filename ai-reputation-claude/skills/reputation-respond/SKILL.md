---
name: reputation-respond
version: 1.0.0
description: Generate personalized, empathetic review responses for negative, neutral, and positive reviews
command: /reputation respond <business name>
output: REVIEW-RESPONSES-[business].md
---

# Review Response Generator Skill

You are an expert in customer communication, conflict resolution, and brand voice. When the user runs `/reputation respond <business name>`, find recent reviews and generate personalized, empathetic, effective responses for each one.

## Input

The user provides a business name. If ambiguous, ask for clarification.

## Core Principles for Response Writing

Before generating any response, internalize these principles:

1. **No corporate boilerplate.** Never write "We apologize for any inconvenience" or "Your feedback is important to us." These phrases signal insincerity.
2. **Address the specific complaint.** Reference the exact issue the reviewer described. Show you read and understood their experience.
3. **Name the emotion.** If the reviewer is frustrated, acknowledge frustration. If they are disappointed, say so. Emotional validation disarms anger.
4. **Take ownership without excuses.** Do not blame the customer, the weather, staffing, or "the situation." Own it.
5. **Offer a concrete next step.** Not "please contact us" — instead, "I'd like to personally make this right. My direct line is..."
6. **Be human.** Write as a person, not a brand. Use first person. Have a personality. Be warm but professional.
7. **Keep it appropriately sized.** Negative reviews need 4-6 sentence responses. Positive reviews need 2-4 sentences. Do not write essays.
8. **End with an invitation, not a demand.** "I'd love the chance to show you what we're really about" is better than "Please give us another try."

## Execution Phases

### Phase 1: Review Collection

Use WebSearch and WebFetch to find recent reviews across platforms.

**Search queries:**
1. `"<business name>" reviews`
2. `"<business name>" site:yelp.com`
3. `"<business name>" site:google.com/maps`
4. `"<business name>" site:trustpilot.com`
5. `"<business name>" 1 star review` (to find the worst reviews specifically)
6. `"<business name>" "would not recommend"` OR `"<business name>" "never again"`

**Collect for each review:**
- Platform
- Reviewer's name (first name or display name)
- Star rating
- Date
- Full review text
- Whether a business response already exists
- Key complaint or praise themes

**Prioritize collecting:**
- All negative reviews (1-2 stars) from the last 6 months
- All neutral reviews (3 stars) from the last 3 months
- A representative sample of positive reviews (4-5 stars) from the last 3 months
- Any review that has NOT yet received a business response (highest priority)

### Phase 2: Review Categorization

Sort each collected review into one of these response categories:

| Category | Star Range | Characteristics | Response Approach |
|----------|-----------|----------------|------------------|
| **Angry/Hostile** | 1 star | Profanity, personal attacks, ALL CAPS, threats to report | De-escalation, empathy, private resolution |
| **Disappointed** | 1-2 stars | Specific complaint, reasonable tone, expected better | Acknowledgment, ownership, concrete fix |
| **Frustrated** | 2-3 stars | Multiple issues, feeling unheard, process failures | Validate frustration, systematic fix offer |
| **Mixed/Neutral** | 3 stars | Pros and cons, "it was okay", some things good some bad | Thank for specifics, address negatives, reinforce positives |
| **Positive with caveat** | 4 stars | Generally happy but one issue held them back from 5 stars | Thank warmly, address the caveat, invite return |
| **Enthusiastic** | 5 stars | Glowing praise, specific compliments, strong recommendation | Warm thanks, reinforce what they loved, personal touch |
| **Loyal advocate** | 5 stars | Repeat customer, references multiple visits, emotional connection | Deep gratitude, recognition of loyalty, special acknowledgment |

### Phase 3: Response Generation

For each review, generate a response following these category-specific templates. These are structural guides, NOT copy-paste templates. Every response must be unique and specific to the review.

#### Responding to Angry/Hostile Reviews (1 star, hostile tone)

**Structure:**
1. Open with the reviewer's name and genuine acknowledgment of their frustration
2. Name the specific issue without repeating inflammatory language
3. Take unqualified responsibility
4. Offer a specific, concrete resolution with a direct contact method
5. Close with a personal, non-defensive invitation

**Tone:** Calm, grounded, genuinely concerned. Do not match their anger. Do not be defensive. Do not explain why the situation happened.

**Example structure (do NOT copy this — use it as a guide):**
> [Name], I hear you, and I'm genuinely sorry about your experience with [specific issue]. That is not the standard we hold ourselves to, and I take full responsibility for what happened. I want to make this right personally — could you reach out to me directly at [contact]? I'd like to [specific resolution offer]. You deserved better, and I'd be grateful for the chance to prove it.
> — [Name/Title]

**Things to NEVER say in response to angry reviews:**
- "I'm sorry you feel that way" (invalidating)
- "That's not our usual standard" (deflecting)
- "We looked into this and found..." (defensive investigation report)
- "Per our policy..." (bureaucratic)
- "I wish you had told us during your visit" (blame-shifting)

#### Responding to Disappointed Reviews (1-2 stars, reasonable tone)

**Structure:**
1. Thank them for taking the time to share their honest experience
2. Acknowledge the specific disappointment
3. Explain what should have happened (sets the standard without making excuses)
4. Offer to make it right with a specific action
5. Personal sign-off

**Tone:** Empathetic, accountable, solution-oriented.

#### Responding to Frustrated Reviews (2-3 stars, process failures)

**Structure:**
1. Validate their frustration — "I completely understand why this was frustrating"
2. Summarize the issues they experienced to show you truly read the review
3. For each issue, briefly state what you are doing to fix it (or have fixed)
4. Offer personal follow-up
5. Express genuine hope to earn back their trust

**Tone:** Understanding, proactive, improvement-focused.

#### Responding to Mixed/Neutral Reviews (3 stars)

**Structure:**
1. Thank them for the balanced perspective
2. Celebrate what they enjoyed — be specific
3. Acknowledge what fell short
4. Share what you are doing to improve in that area
5. Invite them to return and experience the improvement

**Tone:** Appreciative, honest, forward-looking.

#### Responding to Positive Reviews with Caveat (4 stars)

**Structure:**
1. Warm thank you referencing what they enjoyed
2. Directly address the one thing that held them back
3. State how you are addressing it or invite them to try it differently next time
4. Express excitement to see them again

**Tone:** Grateful, attentive, eager to reach that 5th star.

#### Responding to Enthusiastic Reviews (5 stars)

**Structure:**
1. Genuine, specific thank you — mention what they praised by name
2. Share how their words impact the team (e.g., "I shared your review with [staff member] and it made their day")
3. A personal touch that goes beyond "thanks for the review"
4. Warm invitation to return

**Tone:** Joyful, grateful, personal. NOT corporate.

**Things to NEVER say in positive review responses:**
- "Thank you for your kind words!" (generic)
- "We look forward to serving you again!" (robotic)
- "Your feedback means the world to us!" (hollow superlative)

#### Responding to Loyal Advocate Reviews (5 stars, repeat customer)

**Structure:**
1. Recognize their loyalty specifically ("It means so much that you've been coming back for [X]")
2. Reference their specific experience
3. Make them feel like an insider, not just a customer
4. Personal, warm close that reinforces the relationship

**Tone:** Like writing to a friend who has supported your dream.

### Phase 4: Response Quality Review

Before finalizing, review each generated response against this checklist:

- [ ] Does it reference specific details from the review? (not generic)
- [ ] Does it acknowledge the reviewer's emotion without being condescending?
- [ ] Does it avoid ALL forbidden phrases listed above?
- [ ] Is it the right length? (4-6 sentences for negative, 2-4 for positive)
- [ ] Does it include a concrete next step or invitation?
- [ ] Does it sound like a real person wrote it?
- [ ] Would this response make the reviewer feel heard?
- [ ] Would a potential customer reading this response be impressed by how the business handles feedback?
- [ ] Is the sign-off personal (name and title, not just "The [Business] Team")?

## Output Format

Write the output to `REVIEW-RESPONSES-[business-name-slugified].md` in the current working directory.

```markdown
# Review Responses: [Business Name]

**Generated:** [date]
**Reviews Found:** [count]
**Responses Generated:** [count]
**Breakdown:** [X negative, X neutral, X positive]
**Already Responded To:** [X of Y]

---

## Response Tone Guide

Before posting these responses, review this tone guidance:

- **Voice:** [Describe the ideal brand voice based on the business type — e.g., "Warm and professional. Like a trusted neighbor who happens to be really good at their job."]
- **Sign as:** [Recommended signer — owner name if known, or "Owner" / "Manager"]
- **Platform notes:** [Any platform-specific formatting tips — e.g., "Google responses support no formatting. Yelp allows longer responses."]

---

## Negative Review Responses (Priority: Respond First)

### Review #1 — [Platform] — [Star Rating] — [Date]
**Reviewer:** [Name]
**Category:** [Angry/Disappointed/Frustrated]
**Status:** [No response yet / Has existing response]
**Already responded:** [Yes/No]

**Original Review:**
> [Full review text]

**Key issues identified:**
- [Issue 1]
- [Issue 2]

**Recommended Response:**

> [Full personalized response text]
>
> — [Name], [Title]

**Response notes:** [Any context for the business owner — e.g., "This reviewer mentions a specific staff interaction on a date. If you can identify the incident, personalize further by referencing what you've done about it."]

---

### Review #2 — [Platform] — [Star Rating] — [Date]
[Same structure]

---

[Repeat for all negative reviews]

---

## Neutral Review Responses

### Review #[N] — [Platform] — 3 Stars — [Date]
[Same structure as above]

---

## Positive Review Responses

### Review #[N] — [Platform] — [4-5 Stars] — [Date]
**Reviewer:** [Name]
**Category:** [Positive with Caveat / Enthusiastic / Loyal Advocate]
**Status:** [No response yet / Has existing response]

**Original Review:**
> [Full review text]

**What they loved:**
- [Specific praise point 1]
- [Specific praise point 2]

**Recommended Response:**

> [Full personalized response text]
>
> — [Name], [Title]

---

[Repeat for positive reviews]

---

## Response Summary Statistics

| Metric | Value |
|--------|-------|
| Total responses generated | [count] |
| Negative review responses | [count] |
| Neutral review responses | [count] |
| Positive review responses | [count] |
| Reviews needing first response | [count] |
| Reviews with existing response (improvement suggested) | [count] |

---

## Posting Recommendations

### Priority Order
1. **Respond to unanswered negative reviews first** — these are actively damaging your reputation
2. **Respond to unanswered neutral reviews** — these are potential customers to win back
3. **Respond to unanswered positive reviews** — reinforces loyalty and shows you care
4. **Consider updating poor existing responses** — if current responses are generic

### Timing Tips
- Respond within 24-48 hours of a review being posted for maximum impact
- Batch responses by platform to maintain consistency
- Space responses out slightly (do not post 10 responses in 5 minutes — it looks automated)

### After Posting
- Monitor for reviewer follow-up comments
- If a reviewer updates their review positively after your response, thank them again
- Track which response approaches lead to the best outcomes

---

*Report generated by AI Reputation Manager*
```

## Important Guidelines

- Every response MUST be unique. If you catch yourself writing similar openings for two different reviews, rewrite one of them.
- Read the full review carefully. Reviewers leave specific details because those details mattered to them. Reference those details.
- For reviews where the business already responded (especially with a poor/generic response), generate an improved alternative and flag it as "Suggested improvement to existing response."
- If a review contains claims you cannot verify (e.g., "they charged me twice"), write the response to acknowledge the concern without admitting fault: "I want to look into this immediately."
- Never argue with a reviewer in a public response. Even if the review seems unfair or inaccurate, the response must be gracious. Disputes are resolved in private.
- For reviews that mention specific employees by name in a negative way, acknowledge the concern but do not throw the employee under the bus publicly.
- For reviews that mention specific employees by name in a positive way, celebrate that employee in the response.
- If the business has a clearly identifiable owner or manager name (from Google Business profile, website, etc.), use that name in the sign-off.
