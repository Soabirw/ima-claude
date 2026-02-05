---
name: "mcp-memory"
description: "Persistent knowledge graph for cross-session context. You MUST use this proactively - check at session start, store decisions as they happen, capture learnings at session end."
triggers:
  # Reactive (user asks)
  - "remember this"
  - "what did we decide"
  - "previously"
  - "last time"
  # Proactive (Claude recognizes)
  - always  # See Proactive Behavior Rules below
---

# Memory MCP - Proactive Knowledge Graph

**You have access to a persistent knowledge graph that you rely on across all sessions.**

Like Serena for code operations, Memory MCP is your system for preserving context. You use it **proactively** without being asked - checking for relevant context, storing decisions as they're made, and capturing learnings.

## Proactive Behavior Rules

**These are MUST behaviors, not suggestions:**

### 1. Session Start: Check for Context
When beginning work on any project, **automatically search memory** for relevant context:
```
mcp__memory__search_nodes query: "{project-name}"
mcp__memory__open_nodes names: ["user-eric"]
```
This takes 2 seconds and prevents re-learning what you already know.

### 2. During Work: Store Decisions As They Happen
When ANY of these occur, **immediately store without being asked**:

| Event | Action |
|-------|--------|
| User states a preference | Store to `user-eric` entity |
| Architectural decision made | Create `decision-{topic}` entity |
| Bug root cause identified | Create `bug-{description}` entity |
| Pattern chosen over alternatives | Create `pattern-{name}` with rationale |
| User corrects your approach | Update `user-eric` with the correction |
| Configuration choice with rationale | Create `decision-{topic}` entity |

**Recognition patterns** - store when you hear:
- "I prefer..." / "I like..." / "I always..." / "I never..."
- "Let's go with X because..." / "We chose X over Y"
- "The reason this failed was..." / "Root cause:"
- "From now on..." / "Going forward..."
- "That's not how we do it" / "Actually, we..."

### 3. Session End: Capture Learnings
Before ending significant sessions, consider:
- What decisions were made that should persist?
- What did you learn about the user's preferences?
- What patterns or approaches worked well?
- What should you remember for next time?

### 4. Before Asking Questions You Might Already Know
Before asking "What framework do you use?" or "How do you prefer X?", **check memory first**:
```
mcp__memory__search_nodes query: "preference"
mcp__memory__search_nodes query: "{topic}"
```

## Entity Structure

### Core Entities (create these)

**User Entity** (singleton - add observations, don't recreate):
```
name: "user-eric"
entityType: "user"
observations:
  - "Prefers FP patterns over OOP"
  - "Anti-over-engineering philosophy"
  - "Wants minimal code comments"
  - "Uses Quasar for Vue projects"
```

**Project Entities**:
```
name: "project-{name}"
entityType: "project"
observations:
  - "Tech stack: X, Y, Z"
  - "Key patterns: ..."
  - "Gotchas: ..."
```

**Decision Entities**:
```
name: "decision-{topic}"
entityType: "decision"
observations:
  - "Chose X over Y"
  - "Rationale: ..."
  - "Made: {date}"
  - "Applies to: {scope}"
```

### Relations (create these to build the graph)
```
user-eric → owns → project-imanetwork
project-imanetwork → follows → decision-fp-patterns
decision-fp-patterns → supersedes → decision-old-oop-approach
```

## Available Tools

| Tool | When to Use |
|------|-------------|
| `search_nodes` | **First** - before creating, before asking user |
| `open_nodes` | Load specific known entities |
| `create_entities` | New project, decision, pattern, bug |
| `add_observations` | New facts about existing entity |
| `create_relations` | Connect related entities |
| `read_graph` | Debug / audit (use sparingly) |
| `delete_*` | Cleanup outdated information |

## Quick Patterns

### Store a user preference (do this automatically)
```
mcp__memory__search_nodes query: "user-eric"
# If exists:
mcp__memory__add_observations
  observations: [{"entityName": "user-eric", "contents": ["Prefers early returns over nested conditionals"]}]
# If not exists:
mcp__memory__create_entities
  entities: [{"name": "user-eric", "entityType": "user", "observations": ["..."]}]
```

### Store a decision with rationale
```
mcp__memory__create_entities
  entities: [{
    "name": "decision-validators-at-registration",
    "entityType": "decision",
    "observations": [
      "IMA Forms: validators defined at field registration, not validation time",
      "Rationale: single source of truth, template IS the definition",
      "Made: 2026-01-15",
      "Supersedes: separate validation schema approach"
    ]
  }]
mcp__memory__create_relations
  relations: [{"from": "project-ima-forms", "to": "decision-validators-at-registration", "relationType": "follows"}]
```

### Check before asking
```
# Instead of asking "What's your code style preference?"
mcp__memory__search_nodes query: "code style"
mcp__memory__search_nodes query: "preference"
# Only ask if nothing found
```

## What NOT to Store

- Temporary debugging steps
- One-off fixes unlikely to recur
- Information already in project docs (CLAUDE.md, README)
- Sensitive data (credentials, API keys)

## Naming Conventions

| Prefix | Use |
|--------|-----|
| `user-{name}` | User preferences, corrections |
| `project-{name}` | Project context, tech stack |
| `decision-{topic}` | Architectural choices with rationale |
| `pattern-{name}` | Reusable code patterns |
| `bug-{description}` | Root causes worth remembering |
| `standard-{topic}` | Team/org standards |

## The Key Insight

**Serena works because it's wired into code operations automatically.**
**Memory works when it's wired into decision-making automatically.**

Don't wait to be asked. When context flows through the conversation that should persist:
1. Recognize it
2. Store it
3. Mention briefly: "I've noted your preference for X"

This builds a knowledge graph that makes every future session better.
