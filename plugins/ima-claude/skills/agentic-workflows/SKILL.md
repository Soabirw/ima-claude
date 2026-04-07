---
name: agentic-workflows
description: "Headless phase files and standards for Jira-triggered agentic content pipelines. Not for interactive use."
---

# Agentic Workflows

Headless workflow system for Jira-triggered content creation. Not an interactive skill. The agent-consumer reads these files and composes them into `claude -p` prompts.

---

## What This Is

A skill family of system prompts and standards files consumed by an external Node.js agent-consumer. When a Jira ticket is filed, the consumer:

1. Reads the Jira issue to identify content type and source material
2. Selects the matching recipe (e.g., `webinar-summary`)
3. Composes a prompt from: phase file + recipe overrides + standards + previous phase output + source material
4. Runs `claude -p` with that prompt
5. Parses the YAML frontmatter from the output to advance to the next phase

No human is in the loop between phases. Each phase is a single, self-contained `claude -p` call.

---

## Directory Layout

```
references/
  phases/
    gather.md       # Phase 1: Intake — read source material, surface gaps
    outline.md      # Phase 2: Structure — propose content architecture
    draft.md        # Phase 3: Write — turn outline into complete blueprint
    review.md       # Phase 4: Quality gate — score, fix, re-score
    deliver.md      # Phase 5: Production — blog post + Avada markup + email HTML
  standards/
    editorial-standards.md   # Voice, writing principles, formatting rules, AI tells
    outline-format.md        # Structural rules for outlines
    draft-format.md          # Structural rules for drafts
  templates/                 # Production templates (local-only, not committed)
    avada-construction-guide.md    # Fusion Builder syntax and patterns
    avada-webinar-example.txt      # Complete worked example of webinar post
    cta-block-catalog.md           # All CTA global IDs with full markup
    espo-email-preparation.md      # EspoCRM HTML requirements
    webinar-recap-email-espo.html  # Recap email template
    webinar-reminder-email-espo.html  # Reminder email template
```

Recipes live in `references/workflows/` organized by content family:

```
  workflows/
    editorial/
      webinar-summary.md    # Webinar → blog post recipe
```

Each recipe declares which standards files to inject and provides content-type-specific overrides for each phase. The consumer reads these files and composes them into prompts.

---

## Phase Sequence

```
gather → outline → draft → review → deliver
```

Each phase reads the previous phase's output (provided by the consumer in the prompt) and produces its own output. Phases do not share session state — they are stateless.

---

## How the Consumer Composes Prompts

For each phase, the consumer builds a prompt like:

```
[phase file contents]          ← system prompt for this phase
[recipe overrides for phase]   ← content-type-specific rules (optional)
[standards files declared by recipe] ← injected quality criteria
[template files declared by recipe]  ← production templates (deliver phase)
---
Previous phase output:
[YAML + markdown from previous phase]
---
Source material:
[transcript / PDF / press release / etc.]
```

The phase file tells Claude what to do. The recipe overrides customize behavior for the content type. The standards files give Claude the quality bar. The templates provide production markup patterns (Avada, email HTML). The previous output and source material are the data.

---

## Output Format (All Phases)

Every phase must produce output in this exact format:

```
---
phase: gather|outline|draft|review|deliver
status: complete|needs_input|error
issue_key: {{from input}}
content_type: {{from recipe}}
word_count: {{actual word count of body below}}
next_phase: outline|draft|review|deliver|none
needs_input_reason: {{only if status is needs_input}}
---

[markdown body — structured output for this phase]
```

The consumer parses the YAML frontmatter to determine whether to advance, pause for human input, or surface an error. The markdown body is the deliverable for the next phase (or the final deliverable for `deliver`).

---

## Status Rules

- `complete` — phase ran successfully, output is ready, advance to `next_phase`
- `needs_input` — phase cannot proceed without information it cannot infer; set `needs_input_reason`, set `next_phase` to the current phase (retry after human provides input)
- `error` — unrecoverable failure; describe in body

Phases must not use `needs_input` for generic gaps or best-practice questions. Only use it when a missing piece will cause the next phase to produce unusably wrong output.

---

## Recipe Files

Recipes live in `references/workflows/` organized by content family (e.g., `editorial/`). A recipe declares:

- `content_type` — the content format (e.g., `webinar-summary`, `blog-post`)
- `standards` — which files from `references/standards/` to inject per phase
- `templates` — which files from `references/templates/` to inject per phase (production templates for markup/email generation)
- Per-phase overrides — additional instructions appended to the phase prompt

The consumer reads these files and injects the relevant sections into the prompt for each phase.
