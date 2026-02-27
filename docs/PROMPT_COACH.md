# Prompt Coach

A Haiku-powered prompt evaluation system that provides inline feedback when your prompts could be improved against team standards.

## Overview

Prompt Coach uses Claude Haiku to analyze your prompts before they reach the main Claude session. It suggests relevant skills, flags anti-patterns, and catches potential issues — but stays silent when you're on the right track.

## Requirements

- `ANTHROPIC_API_KEY` environment variable (same key used for Claude Code — no separate setup)
- `anthropic` Python package: `pip install anthropic`

## Setup

Prompt Coach ships with ima-claude and activates via environment variable. It is **disabled by default**.

### Quick Setup with Aliases (Recommended)

Add these to your `~/.bash_aliases` or shell profile:

```bash
alias coach-on='export PROMPT_COACH_ENABLED=true && echo "Prompt Coach enabled"'
alias coach-off='export PROMPT_COACH_ENABLED=false && echo "Prompt Coach disabled"'
alias coach-log-on='export PROMPT_COACH_LOG=true && echo "Prompt Coach logging enabled"'
alias coach-log-off='export PROMPT_COACH_LOG=false && echo "Prompt Coach logging disabled"'
alias coach-status='echo "Coach: ${PROMPT_COACH_ENABLED:-false} | Logging: ${PROMPT_COACH_LOG:-false}"'
alias coach-view='less ~/.claude/prompt_coach.log'
alias coach-tail='tail -f ~/.claude/prompt_coach.log'
alias coach-clear='> ~/.claude/prompt_coach.log && echo "Log cleared"'
```

Reload your shell (`source ~/.bash_aliases`) and use:

```bash
coach-on        # Enable coaching
coach-log-on    # Enable logging
coach-status    # Check status
coach-view      # Review logged feedback
coach-tail      # Watch feedback in real-time
coach-off       # Disable when not needed
```

### Manual

```bash
# Enable (add to shell profile for persistence)
export PROMPT_COACH_ENABLED=true

# Enable logging
export PROMPT_COACH_LOG=true   # logs to ~/.claude/prompt_coach.log

# Disable
unset PROMPT_COACH_ENABLED
```

## How It Works

1. **Pre-filtering**: Short prompts (<20 chars) and common follow-ups ("yes", "continue", "ok") are skipped — no API call made
2. **Haiku evaluation**: Prompt is analyzed against team standards using the skills digest
3. **Inline feedback**: If issues are found, feedback appears before Claude's response
4. **Silent by default**: Good prompts produce no output

## What It Checks

### Skill Suggestions
- WordPress PHP → suggests `php-fp-wordpress`
- Node.js APIs → suggests `js-fp-api`
- React components → suggests `js-fp-react`
- Web research → suggests `mcp-tavily`
- Code refactoring → suggests `mcp-serena`

### Anti-Patterns
- "Create helper/utility function" → native patterns preferred
- "Make it more generic" → start specific, generalize with evidence
- "Add wrapper for X" → often over-engineering

### Security Concerns
- Raw SQL without prepared statements
- User input without validation
- Missing WordPress nonce verification

### FP Violations
- Mutable state without clear need
- Side effects mixed with business logic
- Class-heavy design where functions suffice

## Example Output

When feedback is provided:

```
📋 Prompt Coach:
• Consider: mcp-serena for finding symbol references
• Specify which validation rules you need
---
```

When no issues are found: *silence*

## Cost

~$0.0002 per evaluated prompt (~$0.20 per 1,000 prompts). Pre-filtering skips most short follow-ups, keeping actual API usage low.

## Troubleshooting

**Feedback not appearing**
1. Confirm `PROMPT_COACH_ENABLED=true` is set in the current shell
2. Confirm `ANTHROPIC_API_KEY` is set: `echo $ANTHROPIC_API_KEY`
3. Enable logging and check the log: `export PROMPT_COACH_LOG=true`, then `tail ~/.claude/prompt_coach.log`

**Too much feedback / wrong suggestions**

The system prompt and skills digest live inside the plugin at `plugins/ima-claude/hooks/prompt_coach_system.md` and `prompt_coach_digest.md`. These ship with each release. If you want to tune behavior locally, copy `prompt_coach_system.md` to `~/.claude/ima-claude/prompt_coach_system.md` — (future: local override support planned).

**API errors**

Check `~/.claude/prompt_coach.log` for error messages. Common issues:
- `ANTHROPIC_API_KEY` not set or invalid
- `anthropic` package not installed (`pip install anthropic`)
- Rate limiting (unlikely with Haiku)

## Files

| File | Location | Purpose |
|------|----------|---------|
| `prompt_coach.py` | plugin hooks dir | Main hook script |
| `prompt_coach_system.md` | plugin hooks dir | Haiku system prompt (ships with plugin) |
| `prompt_coach_digest.md` | plugin hooks dir | Skills summary for Haiku (updated with releases) |
| `prompt_coach.log` | `~/.claude/` | Log file (when `PROMPT_COACH_LOG=true`) |

## How Skills Are Known

Haiku doesn't have direct access to Claude Code's skill system. A **skills digest** (`prompt_coach_digest.md`) provides:
- Skill trigger patterns (when to suggest each skill)
- Core anti-patterns to flag
- Team philosophy summary

This digest ships with ima-claude and is updated with each release. The combined context (~80 lines) keeps Haiku fast and cheap while giving it enough knowledge to make useful suggestions.
