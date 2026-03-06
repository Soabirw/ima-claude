---
name: "task-runner"
description: "Agent delegation and execution sub-skill. Selects models (opus/sonnet/haiku), assigns skills, and delegates tasks to subagents via the Task tool. Use after work has been decomposed by task-planner."
---

# Task Runner - Agent Delegation & Execution

**You are the Orchestrator. You coordinate. Agents implement.**

This skill handles the execution phase: delegating decomposed tasks to subagents with the right model, minimal context, and relevant skills.

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

### Named Agents (Preferred)

**Delegate to named agents when one fits. Fall back to generic agents for edge cases.**

The plugin provides purpose-built agents with enforced constraints (model, tools, permissions, skills). Use them instead of manually configuring generic agents.

```
Agent(agent_type="ima-claude:explorer", ...)       # Read-only codebase exploration (haiku)
Agent(agent_type="ima-claude:implementer", ...)     # Standard implementation (sonnet + FP skills)
Agent(agent_type="ima-claude:reviewer", ...)        # Code quality review (sonnet, read-only)
Agent(agent_type="ima-claude:wp-developer", ...)    # WordPress specialist (sonnet + WP skills)
```

**Agent selection tree:**

```
What does the subtask need?
├── Find files, understand structure, explore code?
│   → ima-claude:explorer (haiku, read-only, cheap/fast)
├── Implement a feature, fix a bug, write code?
│   → ima-claude:implementer (sonnet, FP-aware)
├── WordPress-specific work (plugin, theme, WP-CLI, forms)?
│   → ima-claude:wp-developer (sonnet, full WP skill bundle)
├── Review code quality, check for bugs/security?
│   → ima-claude:reviewer (sonnet, read-only)
├── Write tests, run test suites, TDD, debug test failures?
│   → ima-claude:tester (sonnet, test orchestration + FP)
├── Memory operations (search, store, consolidate)?
│   → ima-claude:memory (sonnet, Vestige/Qdrant/Serena)
├── Needs a custom tool/skill combination?
│   → general-purpose with explicit model parameter
└── Uncertain?
    → ima-claude:implementer (safe default)
```

| Agent | Model | Mode | Use For |
|-------|-------|------|---------|
| **explorer** | haiku | read-only | File discovery, architecture understanding, code search |
| **implementer** | sonnet | full access | Feature dev, bug fixes, refactoring, tests |
| **reviewer** | sonnet | read-only | Code review, security audit, FP compliance |
| **tester** | sonnet | full access | Test creation, test running, TDD, debugging failures |
| **wp-developer** | sonnet | full access | WordPress plugins, themes, WP-CLI, forms, Bootstrap |
| **memory** | sonnet | full access | Memory search, storage, consolidation (Vestige/Qdrant/Serena) |

### Model Selection (Generic Agents)

For tasks that don't fit a named agent, fall back to generic agents with explicit model selection.

**Opus orchestrates. Sonnet executes. Haiku handles the trivial.**

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

### Anti-Patterns (Delegation)

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| "The agent needs everything" | Context overload, errors | Minimal context principle |
| "Just one more level of agents" | Debugging nightmare | Max 2 levels, restructure |
| "Every agent needs Opus" | Wastes expensive tokens | Sonnet for most tasks, Opus for orchestration |

## Integration Points

This skill works with:
- **Named agents** - `ima-claude:explorer`, `ima-claude:implementer`, `ima-claude:reviewer`, `ima-claude:tester`, `ima-claude:wp-developer` — preferred delegation targets
- **task-planner** - For decomposition before delegation
- **mcp-serena** - For persistent memory across sessions
- **mcp-vestige** - For cross-project decisions, patterns, and intentions
- **architect** - For evaluating architectural choices during planning
- **save-session / resume-session** - For session state management

**REQUIRED SUB-SKILL:** If work hasn't been decomposed yet, use `task-planner` first.

## The Final Word

*"The goal isn't to create perfect plans. It's to think through the work before doing it. A 10-minute planning session that gets revised three times is infinitely better than diving in blind. Master small chunks, then combine. The whole becomes greater than the sum of its parts."*
