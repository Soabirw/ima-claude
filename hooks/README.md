# Claude Code Hooks

Pre-tool-use hooks that enhance Claude Code's behavior.

## Installation

Copy hooks to your Claude Code hooks directory:

```bash
cp hooks/*.py ~/.claude/hooks/
```

Or the installer will do this automatically when you run `bun run scripts/install.ts`.

## Available Hooks

### `enforce_rg_over_grep.py`

**Type**: PreToolUse (Bash)

Enforces best practices for file searching:
- Blocks `grep` → suggests `rg` (ripgrep) for better performance
- Blocks `find -name` → suggests `rg --files -g pattern`

### `tavily_extract_advanced.py`

**Type**: PreToolUse (mcp__tavily__tavily-extract)

Automatically upgrades Tavily extract calls to use `extract_depth: "advanced"` for better content extraction.

### `webfetch_to_tavily.py`

**Type**: PreToolUse (WebFetch)

Redirects WebFetch calls to use Tavily extract instead, which provides better content extraction and respects rate limits.

### `websearch_to_tavily.py`

**Type**: PreToolUse (WebSearch)

Redirects WebSearch calls to use Tavily search instead for more comprehensive results.

## Hook Configuration

Hooks are configured in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "preToolUse": [
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
    ]
  }
}
```

## Requirements

- Python 3.8+
- Tavily MCP server (for Tavily-related hooks)
- ripgrep (`rg`) installed (for enforcement hook)
