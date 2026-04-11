---
name: agentic-workflows
description: "Headless phase files and standards for Jira-triggered agentic content pipelines. Not for interactive use."
---

# Agentic Workflows

Headless workflow system for Jira-triggered content creation. Not interactive. External Node.js agent-consumer reads these files and composes them into `claude -p` prompts.

## Consumer Flow

1. Read Jira issue → identify content type and source material
2. Select matching recipe (e.g., `webinar-summary`)
3. Compose prompt: phase file + recipe overrides + standards + previous phase output + source material
4. Run `claude -p` with that prompt
5. Parse YAML frontmatter from output → advance to next phase

No human in loop between phases. Each phase is a stateless, self-contained `claude -p` call.

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
    avada-construction-guide.md
    avada-webinar-example.txt
    cta-block-catalog.md
    espo-email-preparation.md
    webinar-recap-email-espo.html
    webinar-reminder-email-espo.html
  workflows/
    editorial/
      webinar-summary.md    # Webinar → blog post recipe
```

## Phase Sequence

```
gather → outline → draft → review → deliver
```

## Prompt Composition (per phase)

```
[phase file contents]                        ← system prompt
[recipe overrides for phase]                 ← content-type-specific rules (optional)
[standards files declared by recipe]         ← quality criteria
[template files declared by recipe]          ← production markup (deliver phase only)
---
Previous phase output: [YAML + markdown]
---
Source material: [transcript / PDF / etc.]
```

## Output Format (all phases)

```
---
phase: gather|outline|draft|review|deliver
status: complete|needs_input|error
issue_key: {{from input}}
content_type: {{from recipe}}
word_count: {{actual word count of body}}
next_phase: outline|draft|review|deliver|none
needs_input_reason: {{only if status is needs_input}}
---

[markdown body]
```

## Status Rules

| Status | Meaning |
|--------|---------|
| `complete` | Advance to `next_phase` |
| `needs_input` | Cannot proceed without missing info; set `needs_input_reason`, set `next_phase` to current phase |
| `error` | Unrecoverable failure; describe in body |

Use `needs_input` only when missing info will cause next phase to produce unusably wrong output — not for generic gaps.

## Recipe Files

Each recipe in `references/workflows/` declares:
- `content_type` — content format (e.g., `webinar-summary`)
- `standards` — which `references/standards/` files to inject per phase
- `templates` — which `references/templates/` files to inject per phase
- Per-phase overrides — additional instructions appended to phase prompt
