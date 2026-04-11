---
name: "task-runner"
description: "Agent delegation and execution sub-skill. Selects models (opus/sonnet/haiku), assigns skills, and delegates tasks to subagents via the Task tool. Use after work has been decomposed by task-planner."
---

# Task Runner - Agent Delegation & Execution

You are the Orchestrator. Agents implement. Max nesting: 2 levels deep.

## Named Agents (Prefer over generic)

```
Agent(agent_type="ima-claude:explorer", ...)       # Read-only codebase exploration (haiku)
Agent(agent_type="ima-claude:implementer", ...)     # Standard implementation (sonnet + FP skills)
Agent(agent_type="ima-claude:reviewer", ...)        # Code quality review (sonnet, read-only)
Agent(agent_type="ima-claude:tester", ...)          # Test writing/running (sonnet + test skills)
Agent(agent_type="ima-claude:wp-developer", ...)    # WordPress specialist (sonnet + WP skills)
Agent(agent_type="ima-claude:memory", ...)          # Memory ops (Vestige/Qdrant/Serena)
```

**Selection tree:**
```
What does the subtask need?
├── Find files, explore code?            → ima-claude:explorer (haiku, read-only, cheap)
├── Implement, fix, refactor?            → ima-claude:implementer (sonnet, FP-aware)
├── WordPress (plugin/theme/WP-CLI)?     → ima-claude:wp-developer (sonnet, full WP bundle)
├── Review code quality/security?        → ima-claude:reviewer (sonnet, read-only)
├── Write/run tests, TDD?               → ima-claude:tester (sonnet)
├── Memory search/store/consolidate?     → ima-claude:memory (sonnet)
├── Custom tool/skill combo?             → generic agent with explicit model
└── Uncertain?                           → ima-claude:implementer (safe default)
```

| Agent | Model | Mode | Use For |
|-------|-------|------|---------|
| **explorer** | haiku | read-only | File discovery, architecture, code search |
| **implementer** | sonnet | full | Feature dev, bug fixes, refactoring |
| **reviewer** | sonnet | read-only | Code review, security, FP compliance |
| **tester** | sonnet | full | Test creation, TDD, debugging failures |
| **wp-developer** | sonnet | full | WordPress plugins, themes, WP-CLI |
| **memory** | sonnet | full | Vestige/Qdrant/Serena memory ops |

## Model Selection (Generic Agents)

Opus orchestrates. Sonnet executes. Haiku handles trivial.

| Model | Use For |
|-------|---------|
| **haiku** | File searches, quick lookups, simple reads |
| **sonnet** | Most delegated work: implementation, research, testing |
| **opus** | Orchestration, complex reasoning, ambiguous trade-offs |

## Minimal Context Principle

Give subagents only what they need.

```
Bad:  Full project history + all decisions + "also add a button"
Good: "Add submit button to /src/components/LoginForm.vue calling onSubmit prop. Return updated file."
```

80% of subagent tasks are fully isolated: specific task + specific file(s) + expected output. No project history, no architectural decisions, no other tasks.

## Decomposition Patterns

**Vertical (sequential):** Steps depend on each other → execute in order.
```
Schema → Data layer → API endpoints → UI components
```

**Horizontal (parallel):** Independent steps → execute concurrently.
```
Main Claude → [Login UI | Auth API | DB Setup | Tests]
```

## Delegation Checklist

Before delegating, verify:
1. **Bounded?** Task describable in 2-3 sentences with clear success criteria
2. **No shared state?** Agent won't conflict with other agents' files
3. **Minimal context?** Agent succeeds with task + 1-2 files max
4. **Failure safe?** Can retry or fix without cascading

## Anti-Patterns

| Anti-Pattern | Solution |
|--------------|----------|
| "Agent needs everything" | Minimal context — task + files only |
| "3+ levels of agents" | Max 2 levels — restructure the work |
| "Every agent needs Opus" | Sonnet for most; Opus orchestrates only |

**REQUIRED:** If work isn't decomposed yet, use `task-planner` first.
