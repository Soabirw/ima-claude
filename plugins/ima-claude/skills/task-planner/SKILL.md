---
name: "task-planner"
description: "Decomposition and planning sub-skill. Breaks work into Epic > Story > Task hierarchy, selects storage strategy (Serena/TaskList/Markdown), and creates structured task lists. Use when work needs to be planned and broken down before execution."
---

# Task Planner - Structured Work Breakdown

Plan before implementing. Every hour of planning prevents rework.

## Work Hierarchy

```
Epic (large goal, multi-session)
├── Story (deliverable outcome with value)
│   ├── Task (single actionable step, <2 hours)
│   └── Task
└── Story
    └── Task
```

If a task exceeds 2 hours or requires context switches, break it down further.

## Storage Decision Tree

```
Serena MCP available?
├── Yes → Needs cross-session persistence?
│         ├── Yes → Serena Memory (write_memory/read_memory)
│         └── No  → Claude Task List (TaskCreate/TaskUpdate)
└── No  → Needs cross-session persistence?
          ├── Yes → Markdown file (docs/PLANNING.md)
          └── No  → Claude Task List (survives compacts)
```

| Storage | Survives | Use Case |
|---------|----------|----------|
| **Serena Memory** | Sessions | Milestones, decisions, project state |
| **Claude Task List** | Compacts | In-session tracking, current work items |
| **Markdown File** | Forever | No Serena, need persistence or team visibility |

## Storage Patterns

**Serena Memory:**
```
mcp__serena__write_memory
  memory_file_name: "planning-{project-name}"
  content: |
    # Project: {name}
    ## Current Phase: 2 - Core Implementation
    ## Completed
    - [x] Phase 1: Setup and architecture
    ## In Progress
    - [ ] Story: User authentication
      - [x] Task: Database schema
      - [ ] Task: Login endpoint
    ## Upcoming
    - Phase 3: Testing and polish

mcp__serena__read_memory
  memory_file_name: "planning-{project-name}"
```

**Claude Task List:**
```
TaskCreate
  description: "Implement login form validation"
  status: "in_progress"
  priority: "high"

TaskUpdate
  id: {task-id}
  status: "completed"

TaskList
```

**Markdown fallback** (use `docs-organize` skill for file placement):
```markdown
## Epic: User Authentication System

### Story: Email/Password Login — In Progress
- [x] Task: Create users table migration
- [ ] Task: Create login endpoint
- [ ] Task: Write integration tests
```

## Breakdown Process

1. **Define Epic** — one sentence end state
2. **Identify Stories** — deliverable outcomes composing the epic
3. **Decompose Tasks** — specific steps per story, each <2 hours
4. **Sequence** — mark dependencies, estimate effort
5. **Store** — use decision tree above, then execute

**Example sequencing:**
```
1. [15m] Create users table ─┐
2. [30m] Password hashing   ─┼─→ 3. [45m] Login endpoint → 5. [30m] Connect form
4. [30m] Login form ─────────┘
6. [30m] Error handling (after 5)
```

## Red Flags — Stop and Restructure

- "Task" has 3+ subtasks → it's a Story
- Agents nesting 3+ levels → flatten
- Subagent needs "full context" → task too broad
- Task estimate >2 hours → break down further
- Dependencies form cycles → rethink approach

## Anti-Patterns

| Anti-Pattern | Solution |
|--------------|----------|
| "I'll figure it out as I go" | Plan first, even 5 minutes |
| "This task is simple enough" | Still write it down |
| "I'll remember the plan" | Use TaskList or Serena |

**REQUIRED:** After decomposition, use `task-runner` to delegate to agents.
