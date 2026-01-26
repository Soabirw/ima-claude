Resume a previously saved session from `.claude/session.md`.

## Instructions

1. Construct the absolute path: `{working_directory}/.claude/session.md`
2. Use the **Read** tool to read the file
3. Provide a brief status summary (see format below)
4. Wait for user direction before taking action

## Output Format

```
## Session Resumed

**Task**: {current task from file}
**Last saved**: {date from file}

### Status
- {bullet 1: what was in progress}
- {bullet 2: key decision or context}
- {bullet 3: main outstanding item}

### Suggested Next Step
{The "Resume Hint" from the file, or first outstanding item}

Ready to continue. What would you like to focus on?
```

## Rules

- **Do not** take any actions beyond reading and summarizing
- **Do not** start working on outstanding items automatically
- **Do not** re-read files mentioned unless user asks
- **Do** present the state clearly and wait for direction

## If File Not Found

Respond with:
```
No session file found at `.claude/session.md`.

To save a session, use: /save-session
```
