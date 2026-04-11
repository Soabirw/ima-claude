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
| Not sure if trivial | If >1 file or >5 lines or judgment needed → task-master |
