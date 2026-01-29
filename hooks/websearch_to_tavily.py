#!/usr/bin/env python3
"""
PreToolUse hook: Suggest Tavily search over WebSearch.

Warns (allows command to proceed):
- WebSearch → suggests Tavily via Airis gateway for better results

Tavily provides more comprehensive search results and is preferred for
research tasks requiring current information.
"""
import json
import sys

try:
    data = json.load(sys.stdin)
    tool_input = data.get("tool_input", {})
    query = tool_input.get("query", "")
except json.JSONDecodeError as err:
    print(f"hook-error: {err}", file=sys.stderr)
    sys.exit(1)

# Print warning to stderr (shown to Claude)
warning = f"""⚠️  PREFER Tavily: For web research, use Tavily via Airis gateway instead of WebSearch.

Tavily provides better results for current information, research questions, and comparisons.

To use Tavily search:
  mcp__airis-mcp-gateway__airis-exec
    tool: "tavily:tavily_search"
    arguments: {{"query": "{query}", "search_depth": "basic", "max_results": 10}}

See /mcp-tavily skill for full usage patterns and search_depth options.
"""

print(warning, file=sys.stderr)

# Exit 0 allows the command to proceed (soft warning)
sys.exit(0)
