---
name: "task-master"
description: "Default orchestration skill for ALL non-trivial tasks. Umbrella that dispatches to task-planner (decomposition) and task-runner (delegation). Invoke FIRST before implementing. Trivial = single file, < 5 lines, no judgment. Everything else gets task-master."
---

# Task Master - Orchestration Umbrella

Think before acting. Plan before implementing. Delegate before coding.

## Phase Dispatch

```
Do you have an approved plan with decomposed tasks?
├── No  → task-planner (Epic > Story > Task hierarchy, storage strategy)
└── Yes → task-runner (model selection, skill assignment, parallel execution)
```

## Decision Tree

| Situation | Action |
|-----------|--------|
| New request, no plan yet | `/ima-claude:task-planner` |
| Plan approved, tasks ready | `/ima-claude:task-runner` |
| Mid-session, need to re-plan | `/ima-claude:task-planner` |
| Subagent failed, need to retry | `/ima-claude:task-runner` |
| Subagent returned `ESCALATION: <trigger>` | Opus arbitrates, then `/ima-claude:task-runner` with resolution added to task |
| Not sure if trivial | If >1 file or >5 lines or judgment needed → task-master |

## Advisor Pattern

Executor agents (sonnet/haiku) escalate out-of-scope forks to the parent session (opus) via structured `ESCALATION:` return — see `task-runner` for handling. This keeps work on cheap models while reserving opus for the decisions it's actually good at. Don't rewrite the escalation as a normal retry; handle it as arbitration.
