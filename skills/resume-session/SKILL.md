---
name: "resume-session"
description: "Resume previous session from Serena MCP memory"
---

# resume-session

Resume a previously saved session from Serena MCP memory.

## Trigger Phrases

- "resume session"
- "restore session"
- "load session"
- "continue session"
- "resume from save"

## Instructions

1. Use `mcp__serena__read_memory` with memory name `session-state`
2. Parse the content and provide a brief status summary
3. Wait for user direction before taking action

## Output Format

```
## Session Resumed

**Task**: {current task from memory}
**Last saved**: {date from memory}

### Status
- {bullet 1: what was in progress}
- {bullet 2: key decision or context}
- {bullet 3: main outstanding item}

### Suggested Next Step
{The "Resume Hint" from memory, or first outstanding item}

Ready to continue. What would you like to focus on?
```

## Rules

- **Do not** take any actions beyond reading and summarizing
- **Do not** start working on outstanding items automatically
- **Do not** re-read files mentioned unless user asks
- **Do** present the state clearly and wait for direction

## If Memory Not Found

Respond with:
```
No session memory found.

To save a session, use: /save-session
```

You can also check available memories with `mcp__serena__list_memories` if helpful.

## Technical Notes

- Uses Serena MCP `read_memory` tool (no file path confusion)
- Memory persists across Claude sessions in project context
- Project-specific storage (sessions are project-bound)
- Single checkpoint model (latest session-state only)
