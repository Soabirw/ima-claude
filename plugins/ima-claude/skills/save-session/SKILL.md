---
name: "save-session"
description: "Save session state to Serena MCP memory (no file path confusion)"
---

# save-session

Save current session state to Serena MCP memory for cross-session persistence.

## Trigger Phrases

- "save session"
- "save the session"
- "save current session"
- "create session save"
- "checkpoint session"

## Instructions

Use `mcp__serena__write_memory` to save session state.

**Memory name**: `session-state`

**Content format**:

```markdown
# Session State
Saved: {current_date_time}

## Current Task
{1-2 sentences describing the active task or goal}

## Modified Files
- {path/to/file1}
- {path/to/file2}

## Decisions Made
- {Key decision 1}
- {Key decision 2}

## Technical Context
- **Relevant code**: {endpoints, functions, components involved}
- **Patterns**: {FP patterns, type constraints, architectural decisions}
- **Dependencies**: {external libraries, services, APIs}

## Outstanding Items
- [ ] {Incomplete item or next step}
- [ ] {Blocker or open question}

## Resume Hint
{One sentence: what to do first when resuming}
```

## Rules

**Include:**
- Active task state (what's in progress)
- Files touched this session
- Decisions that affect future work
- Blockers or open questions
- Enough context to resume without re-reading entire codebase

**Exclude:**
- Conversation history or dialogue
- Code snippets (the actual files have the code)
- Completed work that doesn't affect next steps
- Research paths that led nowhere
- Obvious context (project name, basic structure)

## After Writing

Confirm with: "Session saved to Serena memory 'session-state'"

**Note:** For persistent knowledge (decisions, patterns, preferences) that should survive beyond this session, use Vestige via `smart_ingest` — not Serena memory. Serena is for ephemeral session state only.

## Technical Notes

- Uses Serena MCP `write_memory` tool (no file path confusion)
- Memory persists across Claude sessions in project context
- Overwrites previous session-state (single checkpoint model)
- Project-specific storage (appropriate for session state)
