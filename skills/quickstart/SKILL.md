---
name: "quickstart"
description: "Team cheat sheet — scannable reference of the most common ima-claude workflows, commands, and MCP tools. What to type, not why."
version: "1.14.1"
triggers:
  - "quickstart"
  - "cheat sheet"
  - "what can I do"
  - "getting started"
  - "how do I use"
  - "help me get started"
---

# ima-claude Quickstart

## Instructions

**Display the entire cheat sheet below directly to the user.** Output it as-is in your response. Do not summarize, do not run any tools, do not perform memory bootstrap. Just print the cheat sheet.

---

## Starting a Session

| What | Command |
|------|---------|
| Resume previous work | `/resume-session` |
| Save before ending | `/save-session` |

Memory bootstrap runs automatically at session start (Vestige search + intention check).

---

## Planning Work

| What | Command |
|------|---------|
| Brainstorm requirements | `/workflows:brainstorm` |
| Create implementation plan | `/workflows:plan` |
| Execute a plan | `/workflows:work` |
| Ad-hoc task breakdown | "Break this into tasks" (triggers `task-master`) |

Pipeline: **brainstorm → plan → work → review → compound**

---

## Writing Code

FP skills auto-activate by file type — just start coding.

| Context | Skill |
|---------|-------|
| JavaScript/TypeScript | `js-fp` |
| React | `js-fp-react` |
| Vue/Quasar | `js-fp-vue`, `quasar-fp` |
| WordPress JS | `js-fp-wordpress`, `jquery` |
| PHP | `php-fp` |
| WordPress PHP | `php-fp-wordpress` |
| Bootstrap/CSS | `ima-bootstrap` |
| E2E tests | `playwright` |

Core rule: **Simple > Complex. No custom FP utilities. Native patterns.**

---

## Reviewing Code

| What | Command |
|------|---------|
| Full multi-agent review | `/workflows:review` |
| New project setup | Create `compound-engineering.local.md` (see `compound-bridge` skill) |

---

## Documenting Solutions

| What | Command |
|------|---------|
| Document a solved problem | `/workflows:compound` |
| Organize docs | `docs-organize` skill (Active/Archive/Transient tiers) |

---

## Searching & Research

| Need | Tool |
|------|------|
| Current info (2025/2026, "latest") | Tavily (`mcp-tavily`) |
| Library/framework API docs | Context7 (`mcp-context7`) |
| Code symbols, references, rename | Serena (`mcp-serena`) |
| Past solutions, large docs | Qdrant (`mcp-qdrant`) |
| Cross-session knowledge | Vestige (`mcp-vestige`) |
| Complex reasoning, debugging | Sequential Thinking (`mcp-sequential`) |

---

## Memory — Where to Store What

| What | Where |
|------|-------|
| Preferences, decisions, patterns | **Vestige** (auto-stored, spaced repetition) |
| PRDs, plans, large docs | **Qdrant** (semantic search, local RAG) |
| Session state (current task, WIP) | **Serena** (`/save-session`) |

Vestige stores automatically when you say "I prefer...", "Let's go with...", "From now on..."

---

## Project Setup

| What | Where |
|------|-------|
| Project skills & philosophy | `CLAUDE.md` in project root |
| Review agent config | `compound-engineering.local.md` in project root |
| Team Jira sync | `jira-checkpoint` skill (before/during/after work) |

---

## Fun Stuff

| What | Command |
|------|---------|
| Warhammer 40K themed responses | "Enable 40k mode" |
| Medieval crusader themed | "Enable templars" |
| Back to normal | "Disable personality" |

Personalities are tone overlays — expertise stays the same.
