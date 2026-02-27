---
name: "mcp-vestige"
description: "Cognitive memory engine with semantic search, spaced repetition, and codebase awareness. Replaces Memory MCP for all persistent knowledge: preferences, decisions, patterns, bugs, intentions. You MUST use this proactively - search at session start, store decisions as they happen, set intentions for future work."
triggers:
  # Reactive (user asks)
  - "remember this"
  - "what did we decide"
  - "previously"
  - "last time"
  - "remind me"
  - "set intention"
  # Proactive (Claude recognizes)
  - always  # See Proactive Behavior Rules below
---

# Vestige MCP - Cognitive Memory Engine

**Replaces Memory MCP.** Vestige is a Rust-based cognitive memory system with FSRS-6 spaced repetition, semantic search, prediction error gating, and codebase awareness.

## Architecture (3-Tier Memory)

| System | Role | Lifecycle | Example |
|--------|------|-----------|---------|
| **Vestige** | Neural memory — decisions, preferences, patterns, bugs, learnings | Fades if unused (FSRS-6 decay) | "We chose JWT over sessions because..." |
| **Qdrant** | Permanent library — reference material, standards, PRDs, architecture docs | Persistent forever | "Our payment system uses Accept.js with ARB" |
| **Serena Memory** | Project workbench — session state, task progress | Project-scoped, survives git ops | "Currently on task 3/5, next: write tests" |

## Session Start Protocol (REQUIRED)

At session start, BEFORE asking questions:

```
mcp__vestige__search query: "{project-name}" limit: 5
mcp__vestige__search query: "user-eric preferences" limit: 5
mcp__vestige__intention action: "check"
```

If working in a Serena-activated project, also check:
```
mcp__serena__list_memories
```

## Core Tools

### Search (Your Most-Used Tool)

```
mcp__vestige__search
  query: "authentication decision"
  limit: 5
```

Hybrid search — keyword + semantic + RRF fusion. Returns ranked results with similarity scores.

### Smart Ingest (Intelligent Storage)

```
mcp__vestige__smart_ingest
  content: "We chose Zod over Yup for validation because..."
  node_type: "decision"
```

Automatically handles CREATE/UPDATE/SUPERSEDE based on similarity thresholds:

| Similarity | Action | Meaning |
|------------|--------|---------|
| >92% | REINFORCE | Near-duplicate — strengthen existing memory |
| 75-92% | UPDATE | Related — merge new info into existing |
| <75% | CREATE | Novel — store as new memory |

**Always prefer `smart_ingest` over `ingest`** — it prevents duplicates and maintains coherence.

### Direct Ingest (When You Need Control)

```
mcp__vestige__ingest
  content: "User prefers early returns over nested conditionals"
  node_type: "preference"
```

Bypasses dedup logic. Use only when you specifically want to force a new entry.

### Memory (Retrieve/Remove/Check)

```
mcp__vestige__memory
  action: "get"
  id: "{memory-id}"
```

Actions: `get`, `remove`, `check_state`

## Codebase Tools

```
mcp__vestige__codebase
  content: "LoginForm uses composition API with Zod validation"
  pattern_type: "architecture"
```

Store codebase patterns and architectural decisions. Pattern types: `architecture`, `pattern`, `convention`, `dependency`.

## Feedback Tools

```
mcp__vestige__promote_memory id: "{memory-id}"
mcp__vestige__demote_memory id: "{memory-id}"
```

Strengthen or weaken memories based on relevance. Use when:
- **Promote**: Memory proved useful, user referenced it, decision confirmed
- **Demote**: Memory outdated, user contradicted it, no longer relevant

## Intention Tools

```
mcp__vestige__intention
  action: "set"
  content: "Review test coverage after auth refactor"
  trigger: "next session"
```

Actions: `set`, `check`, `complete`, `cancel`

Set reminders and future triggers that surface automatically at session start.

## Session & Maintenance Tools

| Tool | Purpose |
|------|---------|
| `session_checkpoint` | Batch-save an entire session's work |
| `find_duplicates` | Detect and merge redundant memories |
| `consolidate` | Run FSRS-6 decay and maintenance |
| `importance_score` | 4-channel scoring (novelty, arousal, reward, attention) |
| `memory_timeline` | Browse memories chronologically |
| `health_check` | System health with warnings |

## Proactive Behavior Rules

**These are MUST behaviors, not suggestions:**

### 1. Session Start: Search for Context
When beginning work on any project, **automatically search** for relevant context:
```
mcp__vestige__search query: "{project-name}"
mcp__vestige__search query: "user-eric"
mcp__vestige__intention action: "check"
```

### 2. During Work: Store Decisions As They Happen
When ANY of these occur, **immediately store without being asked**:

| Event | Action |
|-------|--------|
| User states a preference | `smart_ingest` with node_type: "preference" |
| Architectural decision made | `smart_ingest` with node_type: "decision" |
| Bug root cause identified | `smart_ingest` with node_type: "bug" |
| Pattern chosen over alternatives | `smart_ingest` with node_type: "pattern" |
| User corrects your approach | `smart_ingest` with node_type: "preference" |
| Codebase pattern discovered | `codebase` with appropriate pattern_type |
| `/workflows:compound` creates solution | `smart_ingest` with node_type: "pattern" (root cause + insight) |
| `/workflows:plan` research completes | `smart_ingest` with node_type: "decision" (approach chosen) |
| `/workflows:review` finds P1/P2 | `smart_ingest` with node_type: "pattern" (finding summary) |

**Recognition patterns** — store when you hear:
- "I prefer..." / "I like..." / "I always..." / "I never..."
- "Let's go with X because..." / "We chose X over Y"
- "The reason this failed was..." / "Root cause:"
- "From now on..." / "Going forward..."
- "That's not how we do it" / "Actually, we..."

### 3. Session End: Capture Learnings
Before ending significant sessions:
- What decisions were made that should persist?
- What did you learn about the user's preferences?
- Set any intentions for future work?

### 4. Before Asking Questions You Might Already Know
Before asking "What framework do you use?" or "How do you prefer X?", **search first**:
```
mcp__vestige__search query: "preference {topic}"
```

## Node Types Reference

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

Vestige manages memory lifecycle automatically via FSRS-6:

| State | Meaning |
|-------|---------|
| **Active** | Readily accessible, frequently retrieved |
| **Dormant** | Stored but weakly retrievable — promote if still relevant |
| **Silent** | Deeply encoded, temporarily inaccessible |
| **Unavailable** | Naturally decayed or removed |

Memories that are searched for get reinforced. Unused memories naturally decay. This prevents knowledge bloat without manual cleanup.

## Decision Logic

**Will it fade if we stop referencing it? That determines where it goes.**

```
IF knowledge that should strengthen with use, fade if unused
   (preferences, decisions, patterns, bugs, learnings):
    → Vestige smart_ingest (neural memory — decays naturally)
ELSE IF reference material that should never be forgotten
   (wiki, standards, PRDs, architecture docs, code samples):
    → Qdrant qdrant-store (permanent library)
ELSE IF session state or project progress:
    → Serena write_memory (project workbench)
ELSE IF future reminder or intention:
    → Vestige intention
ELSE IF codebase architecture pattern:
    → Vestige codebase
ELSE IF searching for prior context:
    → Vestige search (semantic + keyword)
```

## What NOT to Store

- Temporary debugging steps (use Serena session state instead)
- One-off fixes unlikely to recur
- Information already in project docs (CLAUDE.md, README)
- Sensitive data (credentials, API keys)
- Session progress (use Serena for that)

## Migration from Memory MCP

Vestige replaces Memory MCP. The mapping:

| Memory MCP | Vestige Equivalent |
|------------|-------------------|
| `search_nodes` | `search` (semantic + keyword hybrid) |
| `open_nodes` | `search` with specific name |
| `create_entities` | `smart_ingest` (auto-dedup) |
| `add_observations` | `smart_ingest` (auto-UPDATE on similarity) |
| `create_relations` | Not needed — spreading activation via semantic similarity |
| `read_graph` | `memory_timeline` or `search` |
| `delete_*` | `memory` with action: "remove" or `demote_memory` |

## Setup

Install Vestige MCP:

```bash
# Via cargo (Rust required)
cargo install vestige-mcp

# Or download binary from releases
# https://github.com/samvallad33/vestige/releases
```

Configure in Claude Code:
```bash
claude mcp add --scope user vestige -- vestige-mcp
```

Configuration is stored in `~/.config/vestige/` (global) or `.vestige/` (per-project).
