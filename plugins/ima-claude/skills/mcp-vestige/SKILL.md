---
name: "mcp-vestige"
description: "Cognitive memory engine with semantic search, spaced repetition, and codebase awareness. Replaces Memory MCP for all persistent knowledge: preferences, decisions, patterns, bugs, intentions. You MUST use this proactively - search at session start, store decisions as they happen, set intentions for future work. Triggers on: remember this, what did we decide, previously, last time, remind me, set intention, and always proactively."
---

# Vestige MCP - Cognitive Memory Engine

Rust-based cognitive memory system with FSRS-6 spaced repetition, semantic search, prediction error gating, and codebase awareness. Replaces Memory MCP.

## 3-Tier Memory Architecture

| System | Role | Lifecycle |
|--------|------|-----------|
| **Vestige** | Neural memory — decisions, preferences, patterns, bugs | Fades if unused (FSRS-6 decay) |
| **Qdrant** | Permanent library — standards, PRDs, architecture docs | Persistent forever |
| **Serena Memory** | Project workbench — session state, task progress | Project-scoped |

## Session Start Protocol (REQUIRED)

Run BEFORE asking questions:

```
mcp__vestige__search query: "{project-name}" limit: 5
mcp__vestige__search query: "user-eric preferences" limit: 5
mcp__vestige__intention action: "check"
```

If Serena-activated project, also run `mcp__serena__list_memories`.

## Core Tools

### search

```
mcp__vestige__search
  query: "authentication decision"
  limit: 5
```

Hybrid keyword + semantic + RRF fusion. Your most-used tool.

### smart_ingest

```
mcp__vestige__smart_ingest
  content: "We chose Zod over Yup for validation because..."
  node_type: "decision"
```

Auto-handles CREATE/UPDATE/SUPERSEDE:

| Similarity | Action |
|------------|--------|
| >92% | REINFORCE — strengthen existing |
| 75-92% | UPDATE — merge into existing |
| <75% | CREATE — new memory |

Prefer `smart_ingest` over `ingest` — prevents duplicates.

### ingest

```
mcp__vestige__ingest
  content: "User prefers early returns over nested conditionals"
  node_type: "preference"
```

Bypasses dedup. Use only when forcing a new entry.

### memory

```
mcp__vestige__memory
  action: "get"
  id: "{memory-id}"
```

Actions: `get`, `remove`, `check_state`

### codebase

```
mcp__vestige__codebase
  content: "LoginForm uses composition API with Zod validation"
  pattern_type: "architecture"
```

Pattern types: `architecture`, `pattern`, `convention`, `dependency`

### Feedback

```
mcp__vestige__promote_memory id: "{memory-id}"
mcp__vestige__demote_memory id: "{memory-id}"
```

Promote when memory proved useful. Demote when outdated or contradicted.

### intention

```
mcp__vestige__intention
  action: "set"
  content: "Review test coverage after auth refactor"
  trigger: "next session"
```

Actions: `set`, `check`, `complete`, `cancel`

## Maintenance Tools

| Tool | Purpose |
|------|---------|
| `session_checkpoint` | Batch-save entire session |
| `find_duplicates` | Detect and merge redundant memories |
| `consolidate` | Run FSRS-6 decay and maintenance |
| `memory_timeline` | Browse chronologically |
| `health_check` | System health warnings |

## Proactive Behavior (MUST, not suggestions)

### Store immediately — no prompting needed

| Event | Action |
|-------|--------|
| User states preference | `smart_ingest` node_type: "preference" |
| Architectural decision | `smart_ingest` node_type: "decision" |
| Bug root cause identified | `smart_ingest` node_type: "bug" |
| Pattern chosen over alternatives | `smart_ingest` node_type: "pattern" |
| User corrects your approach | `smart_ingest` node_type: "preference" |
| Codebase pattern discovered | `codebase` with appropriate pattern_type |

Recognition phrases — store when you hear:
- "I prefer..." / "I always..." / "I never..."
- "Let's go with X because..." / "We chose X over Y"
- "Root cause:" / "The reason this failed was..."
- "From now on..." / "That's not how we do it"

### Before asking questions, search first

```
mcp__vestige__search query: "preference {topic}"
```

### Session end — capture before closing

- What decisions persist?
- What preferences were revealed?
- Set intentions for next session?

## Node Types

| Type | Use For |
|------|---------|
| `preference` | User preferences, corrections, working style |
| `decision` | Architectural choices with rationale |
| `pattern` | Reusable code patterns, conventions |
| `bug` | Root causes worth remembering |
| `codebase` | Code architecture, file structure, dependencies |
| `intention` | Future reminders and triggers |
| `note` | General knowledge, learnings |

## Memory States

| State | Meaning |
|-------|---------|
| Active | Readily accessible |
| Dormant | Weakly retrievable — promote if still relevant |
| Silent | Deeply encoded, temporarily inaccessible |
| Unavailable | Decayed or removed |

## Decision Logic

```
IF knowledge that strengthens with use, fades if unused
   (preferences, decisions, patterns, bugs):
    → Vestige smart_ingest
ELSE IF reference material that must never be forgotten
   (standards, PRDs, architecture docs):
    → Qdrant qdrant-store
ELSE IF session state or project progress:
    → Serena write_memory
ELSE IF future reminder:
    → Vestige intention
ELSE IF codebase architecture pattern:
    → Vestige codebase
ELSE IF searching for prior context:
    → Vestige search
```

## What NOT to Store

- Temporary debugging steps (use Serena session state)
- One-off fixes unlikely to recur
- Info already in CLAUDE.md or README
- Credentials, API keys
- Session progress (use Serena)

## Migration from Memory MCP

| Memory MCP | Vestige Equivalent |
|------------|-------------------|
| `search_nodes` | `search` |
| `open_nodes` | `search` with specific name |
| `create_entities` | `smart_ingest` |
| `add_observations` | `smart_ingest` |
| `create_relations` | Not needed (spreading activation via semantic similarity) |
| `read_graph` | `memory_timeline` or `search` |
| `delete_*` | `memory` action: "remove" or `demote_memory` |

## Setup

```bash
cargo install vestige-mcp
claude mcp add --scope user vestige -- vestige-mcp
```

Config: `~/.config/vestige/` (global) or `.vestige/` (per-project).
