---
name: "resume-session"
description: "Resume previous session from Serena MCP memory. Use when: resume session, restore session, load session, continue session, resume from save."
---

# resume-session

## Steps

1. `mcp__serena__read_memory` with name `session-state`
2. `mcp__vestige__search query: "{project-name}" limit: 5`
3. `mcp__vestige__intention action: "check"`
4. Summarize state, wait for user direction

## Output Format

```
## Session Resumed

**Task**: {current task}
**Last saved**: {date}

### Status
- {what was in progress}
- {key decision or context}
- {main outstanding item}

### Suggested Next Step
{Resume Hint from memory, or first outstanding item}

Ready to continue. What would you like to focus on?
```

## Rules

- Read and summarize only — no automatic action on outstanding items
- Do not re-read files unless asked

## If Memory Not Found

```
No session memory found.

To save a session, use: /ima-claude:save-session
```

Check available memories with `mcp__serena__list_memories` if helpful.
