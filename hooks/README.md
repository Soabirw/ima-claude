# Claude Code Hooks

Pre-tool-use hooks that enhance Claude Code's behavior with soft warnings and suggestions.

## Installation

Copy hooks to your Claude Code hooks directory:

```bash
cp hooks/*.py ~/.claude/hooks/
cp hooks/*.md ~/.claude/hooks/
```

For the Prompt Coach hook, also copy and configure the API key:

```bash
cp hooks/prompt_coach_config.json.template ~/.claude/hooks/prompt_coach_config.json
# Edit ~/.claude/hooks/prompt_coach_config.json with your API key
```

Or the installer will do this automatically when you run `bun run scripts/install.ts`.

## Available Hooks

### `enforce_rg_over_grep.py`

**Type**: PreToolUse (Bash)

Warns about suboptimal search tools (allows command to proceed):
- Warns on `grep` → suggests `rg` (ripgrep) for better performance
- Warns on `find -name` → suggests `rg --files -g pattern`

The warning is shown to Claude, encouraging use of `rg` for the rest of the session. See the `/rg` skill for usage patterns.

### `websearch_to_tavily.py`

**Type**: PreToolUse (WebSearch)

Suggests using Tavily search instead of WebSearch (allows command to proceed):
- Provides correct Airis gateway syntax for Tavily search
- Includes query from original request in the suggestion
- References `/mcp-tavily` skill for full documentation

Best for: Research tasks, current information, comparisons.

### `webfetch_to_tavily.py`

**Type**: PreToolUse (WebFetch)

Suggests considering Tavily extract for complex pages (allows command to proceed):
- Notes that Tavily often extracts cleaner content
- Provides correct Airis gateway syntax
- References `/mcp-tavily` skill for full documentation

Note: WebFetch is fine for simple pages; Tavily shines on complex/dynamic content.

### `tavily_extract_advanced.py`

**Type**: PreToolUse (mcp__tavily__*)

Informational hook for direct Tavily tool usage:
- Reminds about the correct Airis gateway pattern if using old `mcp__tavily__*` tool names
- References `/mcp-tavily` skill

### `prompt_coach.py`

**Type**: UserPromptSubmit

Evaluates user prompts against team standards using Haiku:
- Provides inline feedback when prompts could be improved
- Stays silent when prompts are well-formed
- Skips short prompts and common follow-ups (yes/no/ok)
- Uses skills digest for context-aware evaluation

**Configuration:**
1. Copy config template: `cp hooks/prompt_coach_config.json.template ~/.claude/hooks/prompt_coach_config.json`
2. Add your Anthropic API key to the config file
3. Set environment variables:
   - `PROMPT_COACH_ENABLED=true` - Enable evaluation
   - `PROMPT_COACH_LOG=true` - Optional: Log to `~/.claude/prompt_coach.log`

**Note:** The API key is isolated in the hook's config file and does not affect Claude Code's OAuth authentication.

## Hook Behavior

All hooks use **soft warnings** (exit code 0) that:
1. Print helpful suggestions to stderr (shown to Claude)
2. Allow the original command to proceed
3. Reference relevant skills for detailed usage patterns

This approach teaches the LLM better patterns without breaking workflows.

## Hook Configuration

Hooks are configured in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python3 ~/.claude/hooks/enforce_rg_over_grep.py" }
        ]
      },
      {
        "matcher": "mcp__tavily__tavily-extract",
        "hooks": [
          { "type": "command", "command": "python3 ~/.claude/hooks/tavily_extract_advanced.py" }
        ]
      },
      {
        "matcher": "WebFetch",
        "hooks": [
          { "type": "command", "command": "python3 ~/.claude/hooks/webfetch_to_tavily.py" }
        ]
      },
      {
        "matcher": "WebSearch",
        "hooks": [
          { "type": "command", "command": "python3 ~/.claude/hooks/websearch_to_tavily.py" }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "python3 ~/.claude/hooks/prompt_coach.py"
      }
    ]
  }
}
```

## Requirements

- Python 3.8+
- Tavily MCP server via Airis gateway (for Tavily-related suggestions)
- ripgrep (`rg`) installed (for rg enforcement hook)

## Related Skills

- `/rg` - Ripgrep usage patterns and examples
- `/mcp-tavily` - Tavily search and extract via Airis gateway
