---
name: design-to-code
description: "Convert design screenshots into working WordPress code through a two-phase workflow. Phase A: analyze screenshots + Jira context → detailed implementation prompt. Phase B: execute prompt → PHP/SCSS code via agent delegation. Use when: user provides design screenshots, says 'implement this design,' 'design to code,' 'convert this mockup,' or has screenshots to turn into WordPress code. Also use when user has an existing implementation prompt to execute. Requires opus for orchestration. Delegates to wp-developer for code generation. Always load ima-brand alongside."
---

# Design to Code

Two-phase workflow: screenshots → implementation prompt (Phase A) → working WordPress code (Phase B). You orchestrate; delegate implementation to `ima-claude:wp-developer`.

## Mode Selection

```
What did the user provide?
├── Screenshots/mockups (no existing prompt)
│   → Phase A → references/phase-a-design-to-prompt.md
├── Existing implementation prompt
│   → Phase B → references/phase-b-prompt-to-code.md
└── Screenshots + "implement this" / "full pipeline"
    → Phase A then Phase B in sequence
```

## Required Skills

- **`ima-brand`** — color palette, typography, mixins (both phases)
- **`ima-bootstrap`** — utility classes, grid, components
- **`php-fp-wordpress`** — WordPress patterns (Phase B only)

## Phase A: Design → Prompt

Output: ~200-300 line prompt file matching team template. Search Qdrant for `design-to-prompt` before starting.

| Step | Action |
|------|--------|
| GATHER | Fetch Jira context + receive screenshots + explore codebase (parallel) |
| ANALYZE | Load brand palette from `ima-brand` — must complete before COMPOSE |
| CROP | Full view → section detection → detail crops (iterative PIL cropping) |
| EXTRACT | Per crop: exact text, icons, colors, layout, spacing |
| MAP | Visual elements → brand variables, components → existing shortcodes |
| COMPOSE | Write prompt using `references/prompt-template.md` structure |
| VALIDATE | Re-check each section against its crop for accuracy |

Save prompt to `docs/designs/{ticket}/PROMPT.md` and Serena memory as `{feature-name}-plan`. Present to user; stop here unless running full pipeline.

## Phase B: Prompt → Code

Search Qdrant for `design-to-code` before starting.

| Step | Action |
|------|--------|
| RESEARCH | Brand SCSS files + current code + component libraries (parallel explorers) |
| ARCHITECTURE | New file vs modify, function reuse, component migration decision |
| DECOMPOSE | Stories by page section; Story 1 = foundation, Stories 2-N = parallel fills, final = polish |
| IMPLEMENT | Delegate to `ima-claude:wp-developer` per story with precise prompts |
| REVIEW | Verify copy, colors, element order, asset paths before visual test |
| VISUAL-QA | Compile SASS → screenshot desktop + mobile → compare to design → iterate |

## Critical Guardrails

Full set in `references/guardrails.md`. Top 5:

1. Never hardcode colors — use brand SCSS variables or Bootstrap utilities
2. Always verify asset paths exist — Glob/grep before referencing
3. Always provide exact copy text — include verbatim text in quotes, never let agents paraphrase
4. Load brand palette BEFORE composition — informs every color reference on first pass
5. Check site header/footer first — don't build components that duplicate existing site elements

## Agent Delegation

| Role | Agent | When |
|------|-------|------|
| Orchestrator | opus (you) | All phases — research, planning, decomposition, delegation, review, surgical fixes |
| Codebase explorer | `ima-claude:explorer` (haiku) | GATHER/RESEARCH: find existing shortcodes, templates, SCSS files |
| Implementer | `ima-claude:wp-developer` (sonnet) | IMPLEMENT: write PHP/SCSS with skills: ima-brand, ima-bootstrap, php-fp-wordpress |
| Reviewer | `ima-claude:reviewer` (sonnet, read-only) | REVIEW: brand compliance + accessibility audit (larger implementations) |

Orchestrator does surgical fixes (<5 lines) directly via Edit. Anything larger → delegate to wp-developer.

## Qdrant Integration

- Phase A: `qdrant_find("design-to-prompt workflow")`
- Phase B: `qdrant_find("design-to-code implementation")`

## Related Skills

| Skill | Relationship |
|-------|------|
| `ima-brand` | Required — color palette, typography, mixins |
| `ima-bootstrap` | Required — utility classes, grid, components |
| `php-fp-wordpress` | Required for Phase B |
| `task-master` | Optional — complex multi-page designs needing Epic > Story > Task |
| `prompt-starter` | Phase A follows its "builder not executor" philosophy |
