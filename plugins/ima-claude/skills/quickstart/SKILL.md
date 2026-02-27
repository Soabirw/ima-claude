---
name: "quickstart"
description: "Team cheat sheet — scannable reference of the most common ima-claude workflows, commands, and MCP tools. What to type, not why. Use when: quickstart, cheat sheet, what can I do, getting started, how do I use, help me get started."
---

# ima-claude Quickstart

## Instructions

**Display the entire cheat sheet below directly to the user.** Output it as-is in your response. Do not summarize, do not run any tools, do not perform memory bootstrap. Just print the cheat sheet.

---

## Starting a Session

| What | Command |
|------|---------|
| Resume previous work | `/ima-claude:resume-session` |
| Save before ending | `/ima-claude:save-session` |

Memory bootstrap runs automatically at session start (Vestige search + intention check).

---

## IMA Workflow

Habit-driven, not tool-enforced. Six steps:

| Step | Where | Command / Action |
|------|-------|-----------------|
| **1. Brainstorm** | Claude Web Project | Ideate, flush out concept into a plan |
| **2. Plan** | Claude Code — Plan Mode | `/plan` or ask Claude to enter Plan Mode |
| **3. Implement** | Claude Code | "Break this into tasks" (triggers `task-master`) |
| **4. Test** | Claude Code + manual | Unit tests + human testing |
| **5. Review** | Fresh Claude Code terminal | `/ima-claude:scorecard` + targeted reviews |
| **6. Document** | Confluence / Jira / MCP memory | Update Qdrant, Serena, Vestige, Markdowns |

Review findings may cycle back to any earlier step.

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
| Project quality scorecard | `/ima-claude:scorecard` |
| Full multi-agent review (Compound Engineering) | `/workflows:review` |
| Organize docs | `docs-organize` skill (Active/Archive/Transient tiers) |

---

## Documenting Solutions

| What | Command |
|------|---------|
| Update cross-session knowledge | Vestige (`smart_ingest`) |
| Store large docs / plans | Qdrant (`mcp-qdrant`) |
| Document a solved problem (Compound Engineering) | `/workflows:compound` |
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
| Session state (current task, WIP) | **Serena** (`/ima-claude:save-session`) |

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
