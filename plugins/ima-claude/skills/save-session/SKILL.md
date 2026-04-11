---
name: "save-session"
description: "Save session state to Serena MCP memory (no file path confusion)"
---

# save-session

Use `mcp__serena__write_memory` with memory name `session-state`.

## Content Format

```markdown
# Session State
Saved: {current_date_time}

## Current Task
{1-2 sentences describing active task or goal}

## Modified Files
- {path/to/file1}

## Decisions Made
- {Key decision 1}

## Technical Context
- **Relevant code**: {endpoints, functions, components}
- **Patterns**: {FP patterns, type constraints, architectural decisions}
- **Dependencies**: {external libraries, services, APIs}

## Outstanding Items
- [ ] {Incomplete item or next step}

## Resume Hint
{One sentence: what to do first when resuming}
```

## Include / Exclude

**Include:** active task state, files touched, decisions affecting future work, blockers, enough context to resume without re-reading codebase.

**Exclude:** conversation history, code snippets (files have the code), completed work not affecting next steps, dead-end research paths, obvious context.

## After Writing

Confirm: "Session saved to Serena memory 'session-state'"

**Note:** For decisions/patterns/preferences surviving beyond this session, use Vestige `smart_ingest` — not Serena. Serena is ephemeral session state only.

## Technical Notes

- Overwrites previous session-state (single checkpoint model)
- Project-specific storage (project-bound)
