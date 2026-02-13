---
name: "task-master"
description: "Effective task breakdown and delegation for Claude Code workflows. Hierarchical decomposition (Epic > Story > Task), optimal storage strategy (Serena/TaskList/Markdown), and agent delegation patterns. Trigger when: planning work, breaking down tasks, organizing projects, delegating to subagents, managing epics/stories, or when complexity requires structured approach. Keywords: decompose, task list, project planning, phases, milestones, step by step."
---

# Task Master - Structured Work Breakdown

**"Slow is smooth, smooth is fast."**

Complex work fails when we dive in without structure. This skill provides a systematic approach to breaking down work, choosing the right storage, and delegating effectively.

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

## Agent Delegation Patterns

### The Two-Level Rule

**Maximum nesting: 2 levels deep.**

```
Main Claude
├── Subagent A (specific task)
└── Subagent B (specific task)
```

Deeper hierarchies create:
- Debugging nightmares
- Context loss
- Coordination overhead
- Exponential complexity

**If you think you need 3+ levels, restructure the work instead.**

### Model Selection for Subagents

**Opus orchestrates. Sonnet executes. Haiku handles the trivial.**

When the orchestrator is running on Opus, most delegated tasks should use Sonnet via the
`model` parameter on the Task tool. Opus tokens are expensive - reserve them for the
orchestration layer and genuinely complex subtasks.

```
Task(subagent_type="general-purpose", model="sonnet", ...)  # Default for delegation
Task(subagent_type="general-purpose", model="opus", ...)    # Only when justified
Task(subagent_type="Explore", model="haiku", ...)           # Quick file lookups
```

**Model decision tree:**

```
Is the subtask...
├── Simple/mechanical (search, read, write, format, list)?
│   → sonnet (or haiku for pure exploration)
├── Requires judgment but well-scoped (implement feature, write tests, refactor)?
│   → sonnet
├── Requires architectural reasoning, complex trade-offs, or multi-step analysis?
│   → opus
└── Uncertain?
    → Start with sonnet. Escalate to opus only if quality is insufficient.
```

| Model | Cost | Use For |
|-------|------|---------|
| **haiku** | Lowest | File searches, quick lookups, simple reads |
| **sonnet** | Medium | Most delegated work: implementation, research, testing, formatting |
| **opus** | Highest | Orchestration (main agent), complex reasoning, architecture decisions |

**Rule of thumb:** If you can describe the task in 2-3 sentences with clear success criteria,
Sonnet can handle it. If the agent needs to make judgment calls about ambiguous trade-offs,
consider Opus.

### Minimal Context Principle

**Give subagents only what they need: task in, result out.**

```
Bad:  "Here's the full project context, all decisions we've made,
       the entire codebase history, and now please also add a button."

Good: "Add a submit button to /src/components/LoginForm.vue that
       calls the onSubmit prop. Return the updated file."
```

**The 80% Rule:** 80% of subagent tasks should be completely isolated. They get:
- The specific task
- The specific file(s) to modify
- The expected output format

They don't get:
- Project history
- Architectural decisions
- Other tasks
- Your reasoning process

### Vertical vs Horizontal Decomposition

**Vertical (Sequential):** When steps depend on each other.
```
Step 1: Create database schema
    ↓
Step 2: Implement data access layer
    ↓
Step 3: Build API endpoints
    ↓
Step 4: Create UI components
```
*Execute in order. Each step needs the previous step's output.*

**Horizontal (Parallel):** When steps are independent.
```
┌─────────────────────────────────────────┐
│ Main Claude (coordinator)                │
├──────────┬──────────┬──────────┬────────┤
│ Agent A  │ Agent B  │ Agent C  │ Agent D│
│ Login UI │ Auth API │ DB Setup │ Tests  │
└──────────┴──────────┴──────────┴────────┘
```
*Execute in parallel when tasks don't share state or dependencies.*

### Delegation Decision Framework

Before delegating to a subagent, ask:

**1. Is the task clearly bounded?**
- Can you describe the input and expected output in 2-3 sentences?
- Are the success criteria unambiguous?
- No? → Break it down further before delegating.

**2. Does it require shared state?**
- Does the agent need to modify files another agent is touching?
- Does it need context from other ongoing work?
- Yes? → Don't parallelize. Do sequentially or yourself.

**3. Is the context minimal?**
- Can the agent succeed with just the task description?
- Do they need more than 1-2 files for context?
- No? → Simplify the task or provide only essential context.

**4. What's the failure mode?**
- If the subagent fails, can you retry or fix easily?
- Does failure cascade to other work?
- High risk? → Do it yourself or add verification.

**5. What model does this need?**
- Is the task well-scoped with clear criteria? → `model: "sonnet"`
- Is it a quick file search or lookup? → `model: "haiku"`
- Does it require complex reasoning or ambiguous trade-offs? → `model: "opus"`
- Default to Sonnet. Opus orchestrates, Sonnet executes.

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

### Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| "I'll figure it out as I go" | Rework, tangents, debt | Plan first, even 5 minutes |
| "The agent needs everything" | Context overload, errors | Minimal context principle |
| "Just one more level of agents" | Debugging nightmare | Max 2 levels, restructure |
| "This task is simple enough" | Scope creep | Still write it down |
| "I'll remember the plan" | Context loss after compact | Use TaskList or Serena |
| "Every agent needs Opus" | Wastes expensive tokens | Sonnet for most tasks, Opus for orchestration |

## Integration Points

This skill works with:
- **mcp-serena** - For persistent memory across sessions
- **mcp-vestige** - For cross-project decisions, patterns, and intentions
- **architect** - For evaluating architectural choices during planning
- **save-session / resume-session** - For session state management

## The Final Word

*"The goal isn't to create perfect plans. It's to think through the work before doing it. A 10-minute planning session that gets revised three times is infinitely better than diving in blind. Master small chunks, then combine. The whole becomes greater than the sum of its parts."*
