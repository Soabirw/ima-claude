---
name: skill-analyzer
description: Analyzes Skills against best practices and provides actionable improvement recommendations. Use when reviewing, auditing, or improving existing Skills (.skill files or skill directories), when validating Skills before distribution, or when the user asks for feedback on a skill they're developing.
---

# Skill Analyzer

Evaluate Skills against best practices and provide actionable feedback.

## Quick Start

```bash
python scripts/analyze_skill.py /path/to/skill-directory
```

Review report → apply fixes → verify with checklists below.

## Analysis Phases

### Phase 1: Structural Validation

Frontmatter:
- `name`: present, ≤64 chars, lowercase letters/numbers/hyphens, no reserved words (anthropic, claude)
- `description`: present, non-empty, ≤1024 chars, no XML tags

File organization:
- `SKILL.md` exists at root
- Body ≤500 lines
- References one level deep from SKILL.md (no nested chains)

### Phase 2: Description Quality

Good descriptions: what the skill does + trigger contexts + key terms.

| Bad | Good |
|-----|------|
| "Helps with PDFs" | "Extracts text and tables from PDF files, fills forms, merges documents. Use when working with PDFs, forms, or document extraction." |
| "I can help you..." | Third-person, action-oriented |
| Missing trigger contexts | Explicit trigger phrases |

### Phase 3: Content Efficiency

For each section ask: Does Claude need this? Can Claude already know this? Does it justify token cost?

Compress verbose paragraphs to code examples. Drop explanations of concepts Claude already knows.

### Phase 4: Progressive Disclosure

Verify layering:
1. Frontmatter → triggers skill selection
2. SKILL.md body → core instructions on trigger
3. Reference files → loaded only when needed

Reference files: split content >100 lines, include ToC if >100 lines, clear pointers in SKILL.md for when to load each.

### Phase 5: Workflow Quality

For multi-step skills:
- Steps are sequential and unambiguous
- Decision points have branching criteria
- Validation steps precede irreversible actions

### Phase 6: Anti-Pattern Detection

| Anti-Pattern | Fix |
|--------------|-----|
| Multiple equivalent approaches offered | One default + escape hatch |
| Windows backslash paths | Use forward slashes |
| Dates or "before/after X" conditionals | Use "old patterns" section or remove |
| Same concept, multiple terms | Choose one term throughout |
| File A → B → C reference chains | Flatten to one level from SKILL.md |
| Unexplained magic numbers | Document why each value was chosen |
| README, CHANGELOG, QUICK_REFERENCE files | Only SKILL.md + essential resources |

## Output Report Format

```markdown
# Skill Analysis: [skill-name]

## Summary
- Overall assessment: [Pass/Needs Work/Major Issues]
- Lines: X (target: <500)
- Description quality: [Good/Needs Work]

## Critical Issues
[Must fix]

## Recommendations
[Helpful but not blocking]

## Strengths
[What the skill does well]
```

## Detailed Checklists

- [references/core-checklist.md](references/core-checklist.md) — Essential quality checks
- [references/advanced-checklist.md](references/advanced-checklist.md) — For skills with scripts/code
