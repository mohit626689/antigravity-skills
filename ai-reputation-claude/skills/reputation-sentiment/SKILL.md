---
name: reputation-sentiment
version: 1.0.0
description: Deep emotional sentiment analysis beyond positive/negative classification
command: /reputation sentiment <business name>
output: SENTIMENT-ANALYSIS-[business].md
---

# Deep Sentiment Analysis Skill

You are an expert sentiment analyst specializing in emotional intelligence and customer psychology. When the user runs `/reputation sentiment <business name>`, perform a granular emotional analysis of the business's online reviews.

## Input

The user provides a business name. If ambiguous, ask for clarification (city/state, URL, or additional identifying details).

## Execution Phases

### Phase 1: Review Collection

Use WebSearch to gather reviews from all available platforms.

**Search queries to run:**
1. `"<business name>" reviews`
2. `"<business name>" customer experience`
3. `"<business name>" complaints`
4. `"<business name>" testimonials`
5. `"<business name>" "worst experience"` (to find strongly negative reviews)
6. `"<business name>" "best experience"` OR `"<business name>" "highly recommend"` (to find strongly positive reviews)
7. `"<business name>" reddit` (for unfiltered opinions)
8. `"<business name>" review site:yelp.com OR site:google.com OR site:trustpilot.com`

Use WebFetch on discovered review URLs to extract full review text. Collect a minimum of 30 reviews if available, prioritizing diversity across star ratings and platforms.

### Phase 2: Emotion Classification

Classify each review into one or more of the following emotional categories. A single review may express multiple emotions (e.g., a reviewer can be both frustrated AND disappointed).

**Primary Emotion Categories:**

| Emotion | Intensity Range | Typical Indicators |
|---------|----------------|-------------------|
| **Delighted** | High positive | "amazing", "exceeded expectations", "blown away", "love", "absolutely wonderful", exclamation marks, superlatives |
| **Grateful** | Medium-high positive | "thank you", "appreciate", "thankful", "grateful", "saved us", "went out of their way" |
| **Impressed** | Medium positive | "professional", "knowledgeable", "efficient", "well done", "pleasantly surprised", "exceeded" |
| **Satisfied** | Low positive | "good", "fine", "as expected", "no complaints", "decent", "solid", "would return" |
| **Neutral** | Baseline | Factual statements without emotional language, balanced pros/cons, "it was okay", "nothing special" |
| **Confused** | Low negative | "unclear", "didn't understand", "confusing", "mixed signals", "contradictory", "wasn't sure", questions in review |
| **Disappointed** | Medium negative | "expected more", "let down", "unfortunately", "used to be better", "mediocre", "underwhelming" |
| **Frustrated** | Medium-high negative | "multiple attempts", "kept trying", "no one helped", "impossible to reach", "wasted my time", "run-around" |
| **Angry** | High negative | "never again", "unacceptable", "outraged", "disgusted", "scam", "worst", "furious", ALL CAPS, profanity |

**For each review, record:**
- Primary emotion (the dominant emotion)
- Secondary emotion(s) (if present)
- Emotional intensity (1-10 scale)
- Key phrases that signal the emotion
- The specific trigger that caused the emotion

### Phase 3: Emotional Journey Mapping

Many reviews describe an emotional arc — the customer's feelings changed during their experience. Map these journeys.

**Common emotional journey patterns to identify:**

| Pattern Name | Arc | Example |
|-------------|-----|---------|
| **The Letdown** | Positive start, negative end | "I was so excited to try this place but..." |
| **The Recovery** | Negative start, positive end | "Had a problem with my order but the manager made it right..." |
| **The Spiral** | Bad to worse | "First the wait was long, then the food was cold, then..." |
| **The Delight** | Positive throughout, escalating | "Good from the start and then they surprised us with..." |
| **The Shrug** | Neutral throughout | "It was fine. Nothing special. Nothing terrible." |
| **The Betrayal** | Long-time positive, sudden negative | "Been a customer for 5 years but this last visit..." |
| **The Conversion** | Skeptic to believer | "I was hesitant based on other reviews but was pleasantly..." |

**For each pattern found, record:**
- Pattern name
- How many reviews follow this pattern
- The typical trigger point where emotion shifts
- A representative example review

### Phase 4: Sentiment Trigger Analysis

Identify the specific triggers that cause each emotional response.

**Negative sentiment triggers to look for:**
- Broken promises (advertised one thing, delivered another)
- Unresponsive communication (calls/emails not returned)
- Unexpected charges or pricing surprises
- Long wait times without acknowledgment
- Staff attitude problems (rudeness, condescension, indifference)
- Quality inconsistency (great one visit, terrible the next)
- Policy rigidity ("they refused to..." "their policy wouldn't allow...")
- Feeling unvalued as a customer ("treated like a number")

**Positive sentiment triggers to look for:**
- Personal recognition (remembered name, preferences)
- Going above and beyond (unexpected extras, special accommodations)
- Problem resolution speed and empathy
- Staff expertise and genuine helpfulness
- Consistent quality delivery
- Transparent communication (proactive updates, honest assessments)
- Value perception (felt they got more than they paid for)
- Follow-up and aftercare

**For each trigger, calculate:**
- Frequency (how many reviews reference this trigger)
- Average emotional intensity when this trigger is present
- Which platforms this trigger appears on most
- Whether the trigger has been increasing or decreasing in recent reviews

### Phase 5: Sentiment Score Calculation

Calculate the overall Sentiment Score (0-100) using the following weighted formula:

```
Sentiment Score = (
  (Delighted_count x 10) +
  (Grateful_count x 8) +
  (Impressed_count x 7) +
  (Satisfied_count x 5) +
  (Neutral_count x 3) +
  (Confused_count x 2) +
  (Disappointed_count x 1) +
  (Frustrated_count x 0.5) +
  (Angry_count x 0)
) / (Total_reviews x 10) x 100
```

Round to the nearest whole number. Provide context for the score:
- 80-100: Exceptional — customers are emotionally invested advocates
- 65-79: Strong — more positive emotions than negative, with room to improve
- 50-64: Mixed — significant emotional friction alongside genuine appreciation
- 35-49: Concerning — negative emotions dominate, urgent attention needed
- 0-34: Crisis — overwhelming negative sentiment, fundamental issues

### Phase 6: Competitive Emotion Benchmarking (Brief)

Run 1-2 quick searches for the top competitor to provide a rough emotional comparison point. This is not a full competitive analysis (that is the `/reputation competitors` skill) but provides context for the sentiment score.

## Output Format

Write the output to `SENTIMENT-ANALYSIS-[business-name-slugified].md` in the current working directory.

```markdown
# Sentiment Analysis: [Business Name]

**Generated:** [date]
**Reviews Analyzed:** [count]
**Platforms:** [list]
**Sentiment Score:** [0-100] / 100 — [Exceptional/Strong/Mixed/Concerning/Crisis]

---

## Sentiment Score Breakdown

**Overall Score: [XX] / 100**

[Visual representation using filled/empty blocks]

**Score Context:** [1-2 sentences explaining what this score means for the business]

**Benchmark:** The average business in [industry] typically scores between [range]. [Business name] is [above/below/at] the typical range.

---

## Emotion Distribution

| Emotion | Count | % of Reviews | Avg Intensity (1-10) | Trend |
|---------|-------|-------------|---------------------|-------|
| Delighted | NN | XX% | X.X | [rising/stable/falling] |
| Grateful | NN | XX% | X.X | [rising/stable/falling] |
| Impressed | NN | XX% | X.X | [rising/stable/falling] |
| Satisfied | NN | XX% | X.X | [rising/stable/falling] |
| Neutral | NN | XX% | X.X | [rising/stable/falling] |
| Confused | NN | XX% | X.X | [rising/stable/falling] |
| Disappointed | NN | XX% | X.X | [rising/stable/falling] |
| Frustrated | NN | XX% | X.X | [rising/stable/falling] |
| Angry | NN | XX% | X.X | [rising/stable/falling] |

**Positive-to-Negative Ratio:** [X:1] — For every negative emotional review, there are X positive ones.

---

## Emotional Journey Patterns

### Most Common Patterns

#### 1. [Pattern Name] — [Count] reviews ([XX]%)

**The arc:** [Brief description of the emotional journey]

**Typical trigger point:** [What causes the emotional shift]

**Example:**
> "[Representative review excerpt]" — [Reviewer], [Platform]

**Business implication:** [What this pattern means for customer retention/acquisition]

#### 2. [Pattern Name] — [Count] reviews ([XX]%)
[Same structure]

#### 3. [Pattern Name] — [Count] reviews ([XX]%)
[Same structure]

---

## Sentiment Triggers

### Negative Triggers (What Causes Bad Feelings)

| Rank | Trigger | Frequency | Avg Intensity | Primary Emotion Caused |
|------|---------|-----------|---------------|----------------------|
| 1 | [trigger] | NN mentions | X.X/10 | [emotion] |
| 2 | [trigger] | NN mentions | X.X/10 | [emotion] |
| 3 | [trigger] | NN mentions | X.X/10 | [emotion] |
| [etc.] | | | | |

#### Deep Dive: #1 Negative Trigger — [Trigger Name]

**What happens:** [Detailed description of the scenario that triggers this emotion]

**Customer quotes:**
- "[quote]" — [emotion: intensity/10]
- "[quote]" — [emotion: intensity/10]

**Root cause hypothesis:** [What is likely causing this at the operational level]

**Fix priority:** [Critical/High/Medium/Low]

[Repeat deep dive for top 3 negative triggers]

### Positive Triggers (What Creates Good Feelings)

| Rank | Trigger | Frequency | Avg Intensity | Primary Emotion Caused |
|------|---------|-----------|---------------|----------------------|
| 1 | [trigger] | NN mentions | X.X/10 | [emotion] |
| 2 | [trigger] | NN mentions | X.X/10 | [emotion] |
| 3 | [trigger] | NN mentions | X.X/10 | [emotion] |

#### Deep Dive: #1 Positive Trigger — [Trigger Name]

**What happens:** [Detailed description]

**Customer quotes:**
- "[quote]" — [emotion: intensity/10]
- "[quote]" — [emotion: intensity/10]

**Amplification opportunity:** [How the business could do more of this]

[Repeat deep dive for top 3 positive triggers]

---

## Emotion-by-Platform Comparison

| Emotion | Google | Yelp | Trustpilot | [Others] |
|---------|--------|------|------------|----------|
| Delighted | XX% | XX% | XX% | XX% |
| Satisfied | XX% | XX% | XX% | XX% |
| Frustrated | XX% | XX% | XX% | XX% |
| Angry | XX% | XX% | XX% | XX% |

**Platform Insight:** [Which platform has the most negative sentiment and why — e.g., "Yelp skews more negative, which is typical of the platform, but the intensity of frustration on Yelp is notably higher than other platforms, suggesting Yelp users have more severe experiences or are more expressive."]

---

## Sentiment Improvement Roadmap

### Quick Wins (Impact within 30 days)
1. **[Action]** — Addresses [trigger], would reduce [emotion] by an estimated [X]%
   - Effort: [Low/Medium/High]
   - Expected sentiment score impact: +[X] points

2. **[Action]** — [same structure]

### Medium-Term (Impact within 90 days)
1. **[Action]** — [same structure]
2. **[Action]** — [same structure]

### Strategic (Impact within 6 months)
1. **[Action]** — [same structure]

### Target Sentiment Score: [XX] / 100
**Current gap:** [X] points
**Achievable timeline:** [estimate] if roadmap is executed

---

## Appendix: Review Emotion Classifications

[Table of all analyzed reviews with their emotion tags]

| # | Platform | Rating | Primary Emotion | Intensity | Secondary Emotion | Key Trigger |
|---|----------|--------|----------------|-----------|------------------|-------------|
| 1 | Google | 5 | Delighted | 9 | Grateful | Staff went above and beyond |
| 2 | Yelp | 2 | Frustrated | 7 | Disappointed | Long wait, no communication |
| [etc.] | | | | | | |

---

*Report generated by AI Reputation Manager*
```

## Important Guidelines

- Emotional classification requires nuance. A 3-star review is not automatically "neutral" — it could express strong disappointment (expected 5-star quality) or cautious satisfaction (expected worse).
- Read the full review text, not just the star rating. A 4-star review can contain frustrated language. A 2-star review can express gratitude for one aspect.
- Cultural context matters. Some reviewers are naturally more expressive than others. Focus on the language used, not assumptions.
- Never fabricate emotional data. If you cannot determine the emotion from the text, classify it as "Neutral" with a note.
- Intensity scores should be calibrated: 1-3 = mild, 4-6 = moderate, 7-8 = strong, 9-10 = extreme.
- When calculating the sentiment score, be transparent about the sample size. A score based on 10 reviews has much lower confidence than one based on 100.
