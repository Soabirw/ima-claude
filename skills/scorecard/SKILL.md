---
name: scorecard
description: "Generate a quick visual scorecard for any project's README. Scores codebase on Code Standards, Security, Test Coverage, Documentation, and Maintainability using a Markdown table with letter grades and color indicators. Use when: user wants a project review with scores, project quality assessment, README badge/scorecard generation, or code health check. Usage: /scorecard [skill1] [skill2] ... where skills are the domain-relevant FP/framework skills to evaluate against (e.g., js-fp js-fp-api, or php-fp php-fp-wordpress)."
---

# Scorecard — Project Quality Assessment

Generate a compact visual scorecard and insert it into the project README.

## Invocation

```
/scorecard js-fp js-fp-api
/scorecard php-fp php-fp-wordpress
/scorecard js-fp js-fp-vue quasar-fp
```

Arguments are domain skills to evaluate against. If none provided, auto-detect from project files.

## Process

Use `task-master` to organize all work. Delegate review categories to parallel agents.

### Step 1: Setup

1. Invoke `task-master` skill for orchestration
2. Invoke each domain skill passed as arguments (these define the code standards to score against)
3. Identify the project's primary language(s) and framework(s)
4. Locate the README (or note its absence)

### Step 2: Parallel Review (delegate via task-master)

Spawn parallel agents for each scoring category:

| Category | What to Evaluate | Key Signals |
|----------|-----------------|-------------|
| **Code Standards** | FP adherence, naming, patterns, consistency | Pure functions, immutability, composition, no anti-patterns from loaded skills |
| **Security** | Input validation, injection risks, auth patterns, secrets | OWASP top 10, hardcoded credentials, SQL/XSS/command injection, dependency vulnerabilities |
| **Test Coverage** | Test existence, quality, edge cases | Test files present, assertions meaningful, critical paths covered |
| **Documentation** | README quality, inline docs where needed, API docs | Setup instructions, usage examples, architecture notes |
| **Maintainability** | Complexity, coupling, file organization, dead code | Small functions, clear boundaries, no circular deps, sensible structure |

Each agent should:
- Use `model: "sonnet"` (Opus orchestrates, Sonnet evaluates)
- Scan relevant files for its category
- Return a letter grade (A-F) with 2-3 bullet points justifying the score
- Be honest — inflated scores help nobody

### Step 3: Compile Scores

Collect agent results into the scorecard table format:

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

| Grade | Color | Meaning |
|-------|-------|---------|
| A | 🟢 | Excellent — meets or exceeds standards |
| B | 🟢 | Good — minor improvements possible |
| C | 🟡 | Adequate — notable gaps to address |
| D | 🔴 | Poor — significant issues |
| F | 🔴 | Failing — critical problems |

### Step 4: Insert into README

- Find the existing `## Scorecard` section and replace it, OR
- Insert after the first heading (title) if no scorecard section exists
- Keep the table compact — no lengthy explanations in the README
- Present the full scorecard to the user before writing, in case they want adjustments

## Guidelines

- **Honest scores only.** A scorecard that says everything is an A is useless.
- **Notes are terse.** Each note is 5-10 words max. The scorecard is a glance, not a report.
- **Domain skills define "Code Standards."** The loaded FP/framework skills set the bar for what good looks like.
- **Security is always evaluated** regardless of which domain skills are passed.
- **Auto-detect when no skills given.** Scan for package.json (JS), composer.json (PHP), etc. and suggest appropriate skills.
- **Date stamp every scorecard** so readers know how fresh it is.
