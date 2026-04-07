---
name: design-to-code
description: "Convert design screenshots into working WordPress code through a two-phase workflow. Phase A: analyze screenshots + Jira context → detailed implementation prompt. Phase B: execute prompt → PHP/SCSS code via agent delegation. Use when: user provides design screenshots, says 'implement this design,' 'design to code,' 'convert this mockup,' or has screenshots to turn into WordPress code. Also use when user has an existing implementation prompt to execute. Requires opus for orchestration. Delegates to wp-developer for code generation. Always load ima-brand alongside."
---

# Design to Code

Orchestrate the transformation of design screenshots into working WordPress code. Two phases, one skill — produce the implementation prompt (Phase A), then execute it (Phase B).

You are the orchestrator. You analyze designs, compose prompts, delegate implementation, and verify results. You do NOT implement directly — you delegate to `ima-claude:wp-developer` agents.

---

## Mode Selection

Determine the mode from the user's input:

```
What did the user provide?
├── Screenshots/mockups (no existing prompt)
│   → Phase A: Design → Prompt
│   → Read references/phase-a-design-to-prompt.md
│
├── An existing implementation prompt
│   → Phase B: Prompt → Code
│   → Read references/phase-b-prompt-to-code.md
│
└── Screenshots + "implement this" / "full pipeline"
    → Phase A then Phase B in sequence
    → Phase A produces prompt → user reviews → Phase B executes
```

---

## Required Skills

Always load alongside this skill:
- **`ima-brand`** — color palette, typography, mixins (needed for both phases)
- **`ima-bootstrap`** — utility classes, grid system, components

Phase B additionally needs:
- **`php-fp-wordpress`** — WordPress development patterns, security, shortcodes

---

## Phase A: Design → Prompt

Transform design screenshots into a detailed, section-by-section implementation prompt. Output: a ~200-300 line prompt file matching the team's established template structure.

Before starting, search Qdrant for `design-to-prompt` to recall prior lessons.

### Steps (read `references/phase-a-design-to-prompt.md` for detailed procedures)

1. **GATHER** — Fetch Jira context + receive screenshots + explore codebase (parallel)
2. **ANALYZE** — Load brand palette from `ima-brand` (**must complete before COMPOSE**)
3. **CROP** — Full view → section detection → detail crops (iterative PIL cropping)
4. **EXTRACT** — Per crop: exact text, icons, colors, layout, spacing
5. **MAP** — Visual elements → brand variables, components → existing shortcodes
6. **COMPOSE** — Write prompt using `references/prompt-template.md` structure
7. **VALIDATE** — Re-check each section against its crop for accuracy

**Output**: Save prompt to `docs/designs/{ticket}/PROMPT.md` and Serena memory as `{feature-name}-plan`.

After Phase A, present the prompt to the user. Stop here unless running full pipeline.

---

## Phase B: Prompt → Code

Execute an implementation prompt to produce working WordPress code. Input: a structured prompt (from Phase A or user-provided).

Before starting, search Qdrant for `design-to-code` to recall prior lessons.

### Steps (read `references/phase-b-prompt-to-code.md` for detailed procedures)

1. **RESEARCH** — Brand SCSS files + current code + component libraries (parallel explorers)
2. **ARCHITECTURE** — New file vs modify, function reuse, component migration decision
3. **DECOMPOSE** — Stories by page section; Story 1 = foundation, Stories 2-N = parallel fills, final = polish
4. **IMPLEMENT** — Delegate to `ima-claude:wp-developer` per story with precise prompts
5. **REVIEW** — Verify copy, colors, element order, asset paths (orchestrator review before visual test)
6. **VISUAL-QA** — Compile SASS → screenshot desktop + mobile → compare to design → iterate

---

## Critical Guardrails

Read `references/guardrails.md` for the complete set. The top 5 (each learned from a real failure):

1. **Never hardcode colors** — always brand SCSS variables or Bootstrap utilities
2. **Always verify asset paths exist** — Glob/grep before referencing; check existing usage patterns
3. **Always provide exact copy text** — never let agents paraphrase; include verbatim text in quotes
4. **Load brand palette BEFORE composition** — informs every color reference on first pass
5. **Check site header/footer first** — don't build custom components that duplicate existing site elements

---

## Agent Delegation Model

| Role | Agent | When |
|---|---|---|
| Orchestrator | opus (you) | All phases — research, planning, decomposition, delegation, review, surgical fixes |
| Codebase explorer | `ima-claude:explorer` (haiku) | GATHER/RESEARCH: find existing shortcodes, templates, SCSS files |
| Implementer | `ima-claude:wp-developer` (sonnet) | IMPLEMENT: write PHP/SCSS with skills: ima-brand, ima-bootstrap, php-fp-wordpress |
| Reviewer | `ima-claude:reviewer` (sonnet, read-only) | REVIEW: brand compliance + accessibility audit (for larger implementations) |

Orchestrator does surgical fixes (<5 lines) directly via Edit tool. Anything larger → delegate to wp-developer.

---

## Qdrant Integration

Before each phase, search Qdrant for prior lessons:
- Phase A: `qdrant_find("design-to-prompt workflow")` — retrieves methodology, cropping techniques, composition decisions
- Phase B: `qdrant_find("design-to-code implementation")` — retrieves decomposition patterns, delegation templates, QA patterns

---

## Related Skills

| Skill | Relationship |
|---|---|
| `ima-brand` | Required — color palette, typography, mixins |
| `ima-bootstrap` | Required — utility classes, grid, components |
| `php-fp-wordpress` | Required for Phase B — WordPress dev patterns |
| `task-master` | Optional — for complex multi-page designs needing Epic > Story > Task decomposition |
| `prompt-starter` | Pattern borrowed — Phase A follows its "builder not executor" philosophy |
