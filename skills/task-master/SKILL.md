---
name: "task-master"
description: "Default orchestration skill for ALL non-trivial tasks. Umbrella that dispatches to task-planner (decomposition) and task-runner (delegation). Invoke FIRST before implementing. Trivial = single file, < 5 lines, no judgment. Everything else gets task-master."
---

# Task Master - Orchestration Umbrella

**"Slow is smooth, smooth is fast."**

Complex work fails when we dive in without structure. Task Master coordinates two phases: planning the work and executing through delegation.

## Core Philosophy

**Think before acting. Plan before implementing. Delegate before coding.**

Every hour of planning saves 10 hours of rework. The urge to "just start coding" is the enemy of clean architecture and maintainable systems.

## Phase Dispatch

```
Do you have an approved plan with decomposed tasks?
├── No  → Use task-planner to decompose the work
│         (Epic > Story > Task hierarchy, storage strategy)
│
└── Yes → Use task-runner to delegate to agents
          (Model selection, skill assignment, parallel execution)
```

**REQUIRED SUB-SKILL:** Use `task-planner` for decomposition (Epic > Story > Task hierarchy, storage strategy selection).

**REQUIRED SUB-SKILL:** Use `task-runner` for delegation (model selection, skill assignment, agent execution).

## Quick Decision Tree

| Situation | Action |
|-----------|--------|
| New request, no plan yet | → `/task-planner` |
| Plan approved, tasks ready | → `/task-runner` |
| Mid-session, need to re-plan | → `/task-planner` |
| Subagent failed, need to retry | → `/task-runner` |
| Not sure if trivial | If >1 file or >5 lines or judgment needed → task-master |

## Integration Points

This skill works with:
- **task-planner** - Decomposition, hierarchy, storage strategy
- **task-runner** - Delegation, model selection, execution
- **mcp-serena** - For persistent memory across sessions
- **mcp-vestige** - For cross-project decisions, patterns, and intentions
- **architect** - For evaluating architectural choices during planning
- **save-session / resume-session** - For session state management
