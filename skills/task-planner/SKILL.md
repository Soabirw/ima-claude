---
name: "task-planner"
description: "Decomposition and planning sub-skill. Breaks work into Epic > Story > Task hierarchy, selects storage strategy (Serena/TaskList/Markdown), and creates structured task lists. Use when work needs to be planned and broken down before execution."
---

# Task Planner - Structured Work Breakdown

**"Slow is smooth, smooth is fast."**

Complex work fails when we dive in without structure. This skill provides a systematic approach to breaking down work and choosing the right storage.

## Core Philosophy

### The Planning Imperative

**Think before acting. Plan before implementing.**

Every hour of planning saves 10 hours of rework. The urge to "just start coding" is the enemy of clean architecture and maintainable systems.

```
Unplanned work → Rework → Technical debt → More rework
Planned work   → Clean implementation → Iteration → Progress
```

### The Hierarchy of Work

```
Epic (Big Goal)
├── Story (Deliverable Outcome)
│   ├── Task (Actionable Step)
│   ├── Task
│   └── Task
├── Story
│   ├── Task
│   └── Task
└── Story
    └── Task
```

**Definitions:**
- **Epic**: A large goal spanning multiple sessions (e.g., "Implement user authentication system")
- **Story**: A coherent deliverable that provides value (e.g., "Users can log in with email/password")
- **Task**: A single actionable step, completable in one session (e.g., "Create login form component")

**Rule:** If a task takes more than 2 hours or requires context switches, break it down further.

## Storage Strategy Decision Tree

```
Is Serena MCP available?
├── Yes → Does this need to persist across sessions?
│         ├── Yes → Serena Memory (write_memory/read_memory)
│         └── No  → Claude Task List (TaskCreate/TaskUpdate)
│
└── No  → Does this need to persist across sessions?
          ├── Yes → Markdown file (docs/PLANNING.md or similar)
          └── No  → Claude Task List (survives compacts)
```

### When to Use Each

| Storage | Use Case | Survives | Example |
|---------|----------|----------|---------|
| **Serena Memory** | Big-picture milestones, decisions, project state | Sessions | "Phase 1 complete, moving to Phase 2" |
| **Claude Task List** | In-session tracking, current work items | Compacts | "[ ] Implement validation [ ] Add tests" |
| **Markdown File** | No Serena, need persistence, team visibility | Forever | `docs/PLANNING.md` with full breakdown |

### Serena Memory Pattern

For cross-session persistence of project state:

```
# Save project state
mcp__serena__write_memory
  memory_file_name: "planning-{project-name}"
  content: |
    # Project: {name}
    ## Current Phase: 2 - Core Implementation

    ## Completed
    - [x] Phase 1: Project setup and architecture

    ## In Progress
    - [ ] Story: User authentication
      - [x] Task: Database schema
      - [ ] Task: Login endpoint
      - [ ] Task: Session management

    ## Upcoming
    - Phase 3: Testing and polish

# Resume later
mcp__serena__read_memory
  memory_file_name: "planning-{project-name}"
```

### Claude Task List Pattern

For in-session work tracking (survives context compaction):

```
# Create tasks for current work
TaskCreate
  description: "Implement login form validation"
  status: "in_progress"
  priority: "high"

TaskCreate
  description: "Add unit tests for auth service"
  status: "pending"
  priority: "medium"

# Update as you work
TaskUpdate
  id: {task-id}
  status: "completed"

# Check status
TaskList
```

### Markdown Fallback Pattern

**Note:** When using Markdown, use the `docs-organize` Skill for proper file/folder structure

When Serena isn't available but you need persistence:

```markdown
<!-- docs/PLANNING.md -->
# Project Planning

## Epic: User Authentication System

### Story: Email/Password Login
**Status:** In Progress

- [x] Task: Create users table migration
- [x] Task: Implement password hashing utility
- [ ] Task: Create login endpoint
- [ ] Task: Add session management
- [ ] Task: Write integration tests

### Story: Password Reset Flow
**Status:** Not Started

- [ ] Task: Create password reset tokens table
- [ ] Task: Implement reset email sender
- [ ] Task: Create reset confirmation endpoint
```

## The Breakdown Process

### Step 1: Define the Epic

Start with the end state:
```
"Users can authenticate via email/password, reset forgotten passwords,
and stay logged in across browser sessions."
```

### Step 2: Identify Stories

What deliverable outcomes compose the epic?
```
1. Users can log in with email/password
2. Users can register new accounts
3. Users can reset forgotten passwords
4. Sessions persist across browser restarts
```

### Step 3: Decompose into Tasks

For each story, what specific steps are needed?
```
Story: Users can log in with email/password
├── Create users table with email, password_hash columns
├── Implement password hashing utility (use bcrypt)
├── Create POST /api/auth/login endpoint
├── Add login form component
├── Connect form to API
└── Add error handling for invalid credentials
```

### Step 4: Estimate and Sequence

Mark dependencies and rough effort:
```
1. [15m] Create users table ─┐
2. [30m] Password hashing   ─┼─→ 3. [45m] Login endpoint ─→ 5. [30m] Connect form
4. [30m] Login form component ─────────────────────────────┘
6. [30m] Error handling (after 5)
```

### Step 5: Choose Storage and Execute

Based on the decision tree above, store appropriately and begin work.

## Quick Reference

### Breakdown Checklist

Before starting any significant work:

- [ ] Can I describe the goal in one sentence?
- [ ] Have I identified all major deliverables (stories)?
- [ ] Is each task completable in under 2 hours?
- [ ] Do I know the dependencies between tasks?
- [ ] Have I chosen appropriate storage (Serena/TaskList/Markdown)?
- [ ] If delegating, does each subagent have minimal, clear context?

### Red Flags

**Stop and restructure if:**
- A "task" has more than 3 subtasks → It's actually a story
- You're nesting agents 3+ levels deep → Flatten the structure
- Subagent needs "full context" → Task is too broad
- Task estimate exceeds 2 hours → Break down further
- Dependencies form cycles → Rethink the approach

### Anti-Patterns (Planning)

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| "I'll figure it out as I go" | Rework, tangents, debt | Plan first, even 5 minutes |
| "This task is simple enough" | Scope creep | Still write it down |
| "I'll remember the plan" | Context loss after compact | Use TaskList or Serena |

**REQUIRED SUB-SKILL:** After decomposition is complete, use `task-runner` to delegate tasks to agents.
