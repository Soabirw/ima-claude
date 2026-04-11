---
name: scorecard
description: "Generate a quick visual scorecard for any project's README. Scores codebase on Code Standards, Security, Test Coverage, Documentation, and Maintainability using a Markdown table with letter grades and color indicators. Use when: user wants a project review with scores, project quality assessment, README badge/scorecard generation, or code health check. Usage: /scorecard [skill1] [skill2] ... where skills are the domain-relevant FP/framework skills to evaluate against (e.g., js-fp js-fp-api, or php-fp php-fp-wordpress)."
---

# Scorecard — Project Quality Assessment

Generate compact visual scorecard and insert into project README.

## Invocation

```
/scorecard js-fp js-fp-api
/scorecard php-fp php-fp-wordpress
/scorecard js-fp js-fp-vue quasar-fp
```

Arguments are domain skills to evaluate against. If none provided, auto-detect from project files.

## Process

### Step 1: Setup

1. Invoke `task-master` for orchestration
2. Load each domain skill passed as argument (defines code standards to score against)
3. Identify project's primary language(s) and framework(s)
4. Locate README (or note its absence)

### Step 2: Parallel Review

Spawn parallel agents per category (`model: "sonnet"`). Each returns letter grade (A-F) + 2-3 justifying bullets. Be honest — inflated scores help nobody.

| Category | What to Evaluate | Key Signals |
|----------|-----------------|-------------|
| **Code Standards** | FP adherence, naming, patterns | Pure functions, immutability, composition, no anti-patterns |
| **Security** | Input validation, injection, auth, secrets | OWASP top 10, hardcoded credentials, SQL/XSS/command injection |
| **Test Coverage** | Test existence, quality, edge cases | Test files present, meaningful assertions, critical paths covered |
| **Documentation** | README quality, inline docs, API docs | Setup instructions, usage examples, architecture notes |
| **Maintainability** | Complexity, coupling, file organization | Small functions, clear boundaries, no circular deps |

### Step 3: Compile Scores

```markdown
## Scorecard

| Category | Grade | Notes |
|----------|-------|-------|
| Code Standards | 🟢 A | Brief justification |
| Security | 🟡 B | Brief justification |
| Test Coverage | 🔴 D | Brief justification |
| Documentation | 🟡 C | Brief justification |
| Maintainability | 🟢 A | Brief justification |

> Last reviewed: YYYY-MM-DD · Skills: js-fp, js-fp-api
```

### Grading Scale

**Formatting rules (non-negotiable):**
- Use **exact emoji characters**: `🟢` `🟡` `🔴` — never GitHub shortcodes (`:green_circle:`), never Unicode geometric shapes
- **Whole letter grades only**: A, B, C, D, F — no `+` or `-`. Nuance goes in Notes column
- Format as `🟢 A` (emoji + space + letter) — no backticks in README output

| Grade | Indicator | Meaning |
|-------|-----------|---------|
| A | 🟢 A | Excellent |
| B | 🟢 B | Good — minor improvements possible |
| C | 🟡 C | Adequate — notable gaps |
| D | 🔴 D | Poor — significant issues |
| F | 🔴 F | Failing — critical problems |

### Step 4: Insert into README

- Replace existing `## Scorecard` section, or insert after first heading if absent
- Present full scorecard to user before writing
- Notes: 5-10 words max each

## Rules

- Security always evaluated regardless of domain skills passed
- Auto-detect skills when none given (scan package.json, composer.json, etc.)
- Date-stamp every scorecard
