---
name: ima-editorial-scorecard
description: "Score and assess any piece of IMA content against editorial standards and brand guidelines. Generates a visual scorecard with letter grades across Brand Voice, Evidence Quality, Audience Clarity, Structural Craft, and CTA Effectiveness. Use when: user wants an editorial review, content quality check, draft assessment, brand compliance review, or asks to 'score this,' 'review this draft,' 'how does this stack up,' or 'editorial feedback.' Works on newsletters, webinar emails, blog posts, press releases, fundraising emails, op-eds, and social posts."
metadata:
  version: 2.0.0
---

# IMA Editorial Scorecard

Score any piece of IMA content against editorial best practices and brand standards. Honest grades that help writers improve.

## Invocation

```
/scorecard [paste or attach content]
/scorecard [content type: newsletter | webinar | blog | press-release | fundraising | op-ed | social]
```

If content type isn't specified, auto-detect from structure and formatting cues.

---

## Process

### Step 1: Identify Content Type

Detect or confirm the format:

| Content Type | Key Signals |
|-------------|-------------|
| Newsletter | "Dear {Person.firstName}", Quick Links block, multiple sections |
| Webinar Email | "Watch Now!", "In this episode, you'll learn", short format |
| Blog Post | H2 headers, long-form prose, embedded media references |
| Press Release | "FOR IMMEDIATE RELEASE", dateline, "###" |
| Fundraising | "Donate Now", match language, P.S. block, gift impact |
| Op-Ed | Named author byline, argumentative structure, word count |
| Social Post | Short format, @ mentions, platform-native CTAs, hashtags |

### Step 2: Load Scoring References

Read the appropriate reference files:
- **[references/scoring-rubrics.md](references/scoring-rubrics.md)** — Grade-level criteria for all 5 categories
- **[references/format-expectations.md](references/format-expectations.md)** — Voice check and structural expectations by content type

### Step 3: Score Across Five Categories

Evaluate the content against each category. Be honest — inflated scores help nobody.

| Category | What to Evaluate |
|----------|-----------------|
| **Brand Voice** | Does this sound like IMA? Tone match for channel? Terminology compliance? |
| **Evidence Quality** | Are claims supported? Sources cited? Precision of language? |
| **Audience Clarity** | Will the target reader understand AND respect this? Plain language with precision? |
| **Structural Craft** | Does the format follow IMA patterns? Logical flow? Scannable? |
| **CTA Effectiveness** | Does the reader know what to do? Are CTAs specific and well-placed? |

### Step 4: Assign Grades

**Formatting rules (non-negotiable):**
- Use **exact emoji characters**: `🟢` `🟡` `🔴` — never text substitutes
- Use **whole letter grades only**: A, B, C, D, F — no `+` or `-` modifiers
- Format as `🟢 A` (emoji + space + letter)
- Notes column: 5-15 words max. The scorecard is a glance, not a report.

| Grade | Indicator | Meaning |
|-------|-----------|---------|
| A | 🟢 A | Excellent — meets or exceeds IMA standards |
| B | 🟢 B | Good — minor improvements possible |
| C | 🟡 C | Adequate — notable gaps to address |
| D | 🔴 D | Poor — significant issues |
| F | 🔴 F | Failing — does not meet IMA standards |

### Step 5: Compile & Present

Present the scorecard in this exact format:

```markdown
## Editorial Scorecard

**Content Type:** [Newsletter / Webinar Email / Blog Post / Press Release / Fundraising / Op-Ed / Social Post]

| Category | Grade | Notes |
|----------|-------|-------|
| Brand Voice | 🟢 A | Brief justification |
| Evidence Quality | 🟡 C | Brief justification |
| Audience Clarity | 🟢 B | Brief justification |
| Structural Craft | 🟢 A | Brief justification |
| CTA Effectiveness | 🟡 C | Brief justification |

> Reviewed: YYYY-MM-DD · Content Type: [type]
```

Then provide the editorial memo:

**What's Working** (2-3 bullets)
- Specific things the content does well
- Quote or reference the actual text

**Priority Fixes** (2-3 bullets, ordered by impact)
- Most impactful improvements first
- Be specific: "Change X to Y" not "Improve the tone"

**Line-Level Notes** (if applicable)
- Flag specific sentences, phrases, or sections
- Suggest rewrites for the most critical issues
- Call out AI tells, terminology violations, or unsupported claims

---

## Special Checks

### AI Detection Flags

Scan for these patterns and flag them in notes:

- **AI openers**: "In today's rapidly evolving...", "In the realm of..."
- **AI transitions**: Repeated "Moreover," "Furthermore," "It's worth noting"
- **AI hedges**: "That being said," "It is important to note that"
- **AI closers**: "In conclusion," at paragraph start
- **Generic filler**: "Navigate the complexities," "At its core," "Delve into"
- **Unnatural formality**: Passive constructions where active voice is standard for IMA

If 3+ AI tells are detected, automatically deduct one letter grade from Brand Voice and note it explicitly.

### Disclaimer Check

For any content containing health information, verify:
- Medical disclaimer present (or appropriate for format)
- "Not medical advice" language where needed
- "Consult your physician" or equivalent for patient-facing content

### Independence Signal

Verify that at least one of these independence markers appears:
- "Independent" in organizational description
- "No pharma funding" or equivalent
- "501(c)(3) nonprofit" identification
- "funded by people/donors" language

**Note:** Social posts are exempt from the independence signal check on individual posts — the profile bio and linked website carry this. Flag only if a statement or long-form social post lacks it.

---

## Guidelines

- **Honest scores only.** A scorecard that says everything is an A is useless.
- **Notes are terse.** 5-15 words per note. The scorecard is a glance.
- **Format-aware grading.** A newsletter shouldn't be scored like a press release. A social post shouldn't be scored like a blog.
- **Prioritize fixes by impact.** What single change would improve this most?
- **Show, don't just tell.** When suggesting a rewrite, write the actual improved version.
- **Date stamp every scorecard** so teams know how fresh the review is.
- **Non-editorial team members** should be able to read and act on this feedback.

---

## Related Skills

- **ima-copywriting**: Write new content or rewrite existing drafts
- **ima-brand**: Source of truth for voice, tone, terminology
