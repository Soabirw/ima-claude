---
name: ima-editorial-workflow
description: "Orchestrates the IMA editorial process — Plan, Write, Review, Approve, Learn. Triggers on: /write, /rewrite, /social, /brainstorm, 'draft,' 'create,' 'improve,' 'fix,' 'edit,' 'make better,' 'new newsletter,' 'new press release,' or any editorial request that isn't a standalone /scorecard review. Routes to ima-copywriting for drafting and ima-editorial-scorecard for review. Always load ima-brand alongside."
metadata:
  version: 1.0.0
---

# IMA Editorial Workflow

Orchestrates every editorial request through a structured sequence. This skill is the traffic controller — it manages the process and delegates writing to `ima-copywriting` and scoring to `ima-editorial-scorecard`.

## Invocation

```
/write [type]          → Plan and draft new content
/rewrite               → Review existing content, then improve it
/social [category]     → Plan and draft a social media post
/brainstorm [topic]    → Explore ideas and angles before committing
```

Also triggers on natural language: "draft a newsletter," "improve this," "write a press release," "help me with this blog post," etc.

**Content types for `/write`:**
`newsletter` · `webinar` · `blog` · `press-release` · `fundraising` · `op-ed` · `social`

**Categories for `/social`:**
`video` · `statement` · `action` · `media-hit` · `announcement` · `journal` · `webinar-promo`

---

## The Workflow

Every editorial request follows this sequence. No diving straight into a draft. No three rounds of follow-up questions. Gather context once, execute cleanly, review honestly.

```
PLAN    → Identify intent, content type, gather missing context
WRITE   → Draft using ima-copywriting + format reference + ima-brand
REVIEW  → Score against standards using ima-editorial-scorecard
APPROVE → Present for human decision with clear next actions
LEARN   → Capture what worked for future drafts
```

---

## PLAN (Always Runs First)

Every editorial request starts with planning. Even quick ones. Especially quick ones.

### Step 1: Detect Intent

| Command or Signal | Intent | Workflow Path |
|-------------------|--------|---------------|
| `/write`, "draft," "create," "new" | **Create** new content | Plan → Write → Review → Approve |
| `/rewrite`, "improve," "fix," "edit," "make better" | **Rewrite** existing content | Plan → Review → Write → Review → Approve |
| `/social` | **Create** social post | Plan → Write → Review → Approve |
| `/brainstorm` | **Explore** before committing | Brainstorm → Plan (when ready) |
| Pastes content, no instructions | **Ambiguous** | Ask: "Score this or rewrite it?" |
| "Continue," "next version," "apply fixes" | **Iterate** | Skip Plan → Write |

**Note:** `/scorecard` is handled directly by the `ima-editorial-scorecard` skill, not this workflow.

### Step 2: Identify Content Type

From the command argument, or detect from context, or ask.

### Step 3: Gather Context (One Prompt, Not a Chain)

**Use the `ask_user_input` widget** to collect 2–3 answers in a single structured prompt. Do not ask questions one at a time across multiple messages.

**Rules:**
- If the user already provided enough context, skip answered questions. Don't ask "what's the content type?" when they said `/write press-release`.
- Default aggressively. If someone says `/write fundraising` about the year-end campaign, you already know the audience, tone, and CTA structure. Ask only for what's genuinely missing.
- For iteration ("apply the fixes," "next version"), skip Plan entirely.
- If the user says "just do it," respect that. Write with available context, note assumptions, flag gaps with `[brackets]`.

### Context Gathering by Command

**`/write [type]` — Creating new content:**
- Core message — what's the ONE takeaway? (open text)
- Reader action — what should they do? (widget: Read / Watch / Donate / Share / Sign / Attend / Download)
- Source material available? (widget multi-select: Study · Webinar · Quote from leader · Press release · External article · None yet)
- Subject matter expert? (open text)
- Responding to external events? (open text, optional)
- Audience segment? (widget: General supporters · Healthcare pros · Donors · Media · New subscribers)

**`/rewrite` — Improving content:**
- What's wrong with it? (open text)
- Keep structure or rebuild? (widget: Keep structure · Rebuild)
- Preserve specific elements? (open text, optional)

**`/social [category]` — Social media post:**
- Category, if not specified (widget: Video/Research · Statement · Action/Campaign · Media Hit · Announcement · Journal · Webinar Promo)
- What are you promoting/announcing? (open text)
- Link or media to attach? (open text)
- Quote to feature? (open text, optional)

**`/brainstorm [topic]` — Exploring angles:**
- What's the topic or event? (open text)
- Any format preference, or open to suggestions? (widget: Newsletter angle · Blog angle · Social angle · Op-ed angle · No preference)
- What's the goal? (widget: Drive awareness · Drive action · Respond to news · Celebrate a win · Educate)

---

## WRITE

After planning, load tools and draft:

1. Load `ima-brand` skill (always — voice/tone authority)
2. Load `ima-copywriting` skill (writing principles + format template for this content type)
3. Check project Files for published examples of this format as style benchmarks
4. Write the draft
5. Self-check against the Quality Checklist in ima-copywriting

**Deliver the draft with a brief note** on key editorial choices: why you opened this way, which template you followed, what still needs user input.

**Use placeholder brackets** for anything you don't have: `[study name]`, `[specific finding]`, `[dollar amount]`, `[date]`. Never invent evidence.

---

## REVIEW

Run the editorial scorecard — on your own draft (self-review) or user-submitted content.

1. Load `ima-editorial-scorecard` skill
2. Auto-detect content type or use what was specified
3. Score across five categories: Brand Voice · Evidence Quality · Audience Clarity · Structural Craft · CTA Effectiveness
4. Present scorecard table first, then What's Working, Priority Fixes, Line-Level Notes

**For self-review after writing:**
- Be honest. If the draft you wrote has a weak opening or missing independence signal, say so.
- Separate what *you* can fix on the next pass from what the *user* needs to provide (missing data, quotes, approvals).

**For user-submitted content:**
- Score first, then ask if they want a rewrite.

---

## APPROVE

Present the work for human decision. Use the `ask_user_input` widget to offer clear next actions:

| Option | What Happens Next |
|--------|-------------------|
| ✅ Approve | Content is ready. Move to Learn. |
| 🔄 Revise | Apply specific changes. Return to Write. |
| 🔁 Rebuild | Different approach. Return to Plan. |
| 💬 Discuss | Talk through a section before deciding. |

---

## LEARN

After approval, briefly capture what worked or what the user corrected:

> "Noted for future [content type] drafts:
> - [Pattern worth reusing or correction to remember]"

Examples:
- "Noted: Dr. Varon prefers 'the IMA' in formal quotes, not just 'IMA.'"
- "Noted: Year-end fundraising leads with match mechanic, not mission statement."
- "Noted: Thread format (1/4) works well for journal promotions on social."

If the learning should persist across sessions, ask: "Want me to remember this for future drafts?" and use memory.

---

## Related Skills

- **ima-brand**: Voice, tone, terminology, visual identity (ALWAYS load alongside)
- **ima-copywriting**: Format templates, writing principles, CTA patterns, quality checklist
- **ima-editorial-scorecard**: Scoring rubric for content review (handles `/scorecard` independently)
