Save current session state to `.claude/session.md` in the working directory.

## Instructions

1. Determine the absolute path: `{working_directory}/.claude/session.md`
2. Create the `.claude` directory if it doesn't exist
3. Use the **Write** tool to create/overwrite the file with the format below

## File Format

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

Confirm with: "Session saved to `.claude/session.md`"
