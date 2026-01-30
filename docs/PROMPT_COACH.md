# Prompt Coach

A Haiku-powered prompt evaluation system that provides inline feedback when your prompts could be improved against team standards.

## Overview

Prompt Coach uses Claude 3.5 Haiku to analyze your prompts before they reach the main Claude session. It suggests relevant skills, flags anti-patterns, and catches potential issues—but stays silent when you're on the right track.

## Installation

Prompt Coach is installed automatically with ima-claude. The hook files are copied to `~/.claude/hooks/` and configured in `~/.claude/settings.json`.

## Configuration

### Quick Setup with Aliases (Recommended)

Add these aliases to your `~/.bash_aliases` or shell profile for easy control:

```bash
# ============================================================================
# Prompt Coach Aliases (Haiku-powered prompt feedback system)
# ============================================================================
alias coach-on='export PROMPT_COACH_ENABLED=true && echo "✅ Prompt Coach enabled"'
alias coach-off='export PROMPT_COACH_ENABLED=false && echo "❌ Prompt Coach disabled"'
alias coach-log-on='export PROMPT_COACH_LOG=true && echo "📝 Prompt Coach logging enabled"'
alias coach-log-off='export PROMPT_COACH_LOG=false && echo "🚫 Prompt Coach logging disabled"'
alias coach-status='echo "Coach: ${PROMPT_COACH_ENABLED:-false} | Logging: ${PROMPT_COACH_LOG:-false}"'
alias coach-view='less ~/.claude/prompt_coach.log'
alias coach-tail='tail -f ~/.claude/prompt_coach.log'
alias coach-clear='> ~/.claude/prompt_coach.log && echo "🗑️  Log cleared"'
```

Then reload your shell (`source ~/.bash_aliases`) and use:

```bash
coach-on              # Enable coaching
coach-log-on          # Enable logging
coach-status          # Check status
coach-view            # Review logged feedback
coach-tail            # Watch feedback in real-time
coach-off             # Disable when not needed
```

### Manual Configuration

#### Enable Prompt Coach

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export PROMPT_COACH_ENABLED=true
```

#### Enable Logging (Optional)

For tuning and review, you can log all prompt evaluations:

```bash
export PROMPT_COACH_LOG=true
# Logs to ~/.claude/prompt_coach.log
```

#### Disable Prompt Coach

```bash
unset PROMPT_COACH_ENABLED
# Or simply don't set it (disabled by default)
```

## How It Works

1. **Pre-filtering**: Short prompts (<20 chars) and common follow-ups ("yes", "continue", etc.) are skipped without calling Haiku
2. **Haiku Evaluation**: Prompts are analyzed against team standards
3. **Inline Feedback**: If issues are found, feedback appears before Claude's response
4. **Silent Mode**: Good prompts receive no feedback (no noise)

## What It Checks

### Skill Suggestions
- WordPress PHP → Suggests `php-fp-wordpress`
- Node.js APIs → Suggests `js-fp-api`
- React components → Suggests `js-fp-react`
- Web research → Suggests `mcp-tavily`
- Code refactoring → Suggests `mcp-serena`

### Anti-Patterns
- "Create helper/utility function" → Native patterns preferred
- "Make it more generic" → Start specific, generalize with evidence
- "Add wrapper for X" → Often over-engineering

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

When no issues are found: *silence* (no output)

## Cost

~$0.0002 per evaluated prompt (~$0.20 per 1,000 prompts)

Many prompts are skipped by pre-filtering, reducing actual API calls.

## Requirements

- `ANTHROPIC_API_KEY` environment variable (same key used for Claude Code)
- `anthropic` Python package (`pip install anthropic`)

## Troubleshooting

### Feedback not appearing

1. Check `PROMPT_COACH_ENABLED=true` is set
2. Verify `ANTHROPIC_API_KEY` is set
3. Enable logging: `export PROMPT_COACH_LOG=true`
4. Check log file: `tail ~/.claude/prompt_coach.log`

### Too much feedback

The system prompt in `~/.claude/hooks/prompt_coach_system.md` can be tuned. Add patterns to the "WHEN TO STAY SILENT" section.

### API errors

Check the log file for error messages. Common issues:
- Missing or invalid API key
- Network connectivity
- Rate limiting (unlikely with Haiku)

## Files

| File | Purpose |
|------|---------|
| `~/.claude/hooks/prompt_coach.py` | Main hook script |
| `~/.claude/hooks/prompt_coach_system.md` | Haiku instructions (editable) |
| `~/.claude/hooks/prompt_coach_digest.md` | Skills summary for Haiku (updated with releases) |
| `~/.claude/prompt_coach.log` | Log file (when enabled) |

## How Skills Are Known

Haiku doesn't have direct access to Claude Code's skill system. Instead, we maintain a **skills digest** (`prompt_coach_digest.md`) that contains:
- Skill trigger patterns (when to suggest each skill)
- Core anti-patterns to flag
- Team philosophy summary

This digest ships with ima-claude and is updated with each release. The combined context (~80 lines) keeps Haiku fast and cheap while giving it enough knowledge to make useful suggestions.
