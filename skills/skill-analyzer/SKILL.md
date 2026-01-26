---
name: skill-analyzer
description: Analyzes Skills against best practices and provides actionable improvement recommendations. Use when reviewing, auditing, or improving existing Skills (.skill files or skill directories), when validating Skills before distribution, or when the user asks for feedback on a skill they're developing.
---

# Skill Analyzer

Evaluate Skills against documented best practices and provide actionable feedback.

## Quick Start

1. Run automated validation:
   ```bash
   python scripts/analyze_skill.py /path/to/skill-directory
   ```

2. Review the analysis report for issues and recommendations

3. For manual deep-dive, follow the Analysis Workflow below

## Analysis Workflow

### Phase 1: Structural Validation

Check YAML frontmatter requirements:
- `name`: Present, ≤64 chars, lowercase letters/numbers/hyphens only, no reserved words (anthropic, claude)
- `description`: Present, non-empty, ≤1024 chars, no XML tags

Check file organization:
- SKILL.md exists at root
- Body ≤500 lines (optimal context efficiency)
- References are one level deep from SKILL.md (no nested chains)

### Phase 2: Description Quality

**Good descriptions include:**
- What the skill does
- When/triggers for using it
- Key terms users might mention

**Red flags:**
- Vague: "helps with documents", "processes data"
- First/second person: "I can help you...", "You can use this to..."
- Missing trigger contexts

**Example transformation:**
```
Bad:  "Helps with PDFs"
Good: "Extracts text and tables from PDF files, fills forms, merges documents. 
       Use when working with PDF files or when the user mentions PDFs, forms, 
       or document extraction."
```

### Phase 3: Content Efficiency

**Check for over-explanation:**
- Does the skill explain concepts Claude already knows?
- Are there verbose paragraphs that could be concise code examples?
- Token cost vs. value delivered?

**Conciseness test:** For each section ask:
1. "Does Claude really need this?"
2. "Can I assume Claude knows this?"
3. "Does this justify its token cost?"

### Phase 4: Progressive Disclosure

**Verify proper layering:**
1. Metadata (name + description) - triggers skill selection
2. SKILL.md body - core instructions loaded on trigger
3. Reference files - loaded only when needed

**Check reference patterns:**
- Large content (>100 lines) split into separate files
- Reference files have table of contents if >100 lines
- Domain-specific content organized by domain
- Clear pointers in SKILL.md to when each reference should be read

### Phase 5: Workflow Quality

For skills with multi-step processes:
- Steps are clear and sequential
- Decision points have conditional guidance
- Feedback loops exist for quality-critical operations
- Validation steps precede irreversible actions

### Phase 6: Anti-Pattern Detection

Check for these common issues:

| Anti-Pattern | Detection | Fix |
|--------------|-----------|-----|
| Too many options | Multiple equivalent approaches offered | Provide one default + escape hatch |
| Windows paths | Backslashes in file paths | Use forward slashes everywhere |
| Time-sensitive info | Dates, "before/after X" conditionals | Use "old patterns" section or remove |
| Inconsistent terminology | Same concept, multiple terms | Choose one term throughout |
| Deeply nested refs | File A → File B → File C | Flatten to one level from SKILL.md |
| Voodoo constants | Unexplained magic numbers in scripts | Document why each value was chosen |
| Excessive files | README, CHANGELOG, QUICK_REFERENCE | Only SKILL.md + essential resources |

## Output Report Format

After analysis, produce a structured report:

```markdown
# Skill Analysis: [skill-name]

## Summary
- Overall assessment: [Pass/Needs Work/Major Issues]
- Lines: X (target: <500)
- Description quality: [Good/Needs Work]

## Critical Issues
[Issues that must be fixed]

## Recommendations
[Improvements that would help but aren't blocking]

## Strengths
[What the skill does well]
```

## Detailed Checklists

For comprehensive evaluation criteria, see:
- [references/core-checklist.md](references/core-checklist.md) - Essential quality checks
- [references/advanced-checklist.md](references/advanced-checklist.md) - For skills with scripts/code
