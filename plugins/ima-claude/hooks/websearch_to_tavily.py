#!/usr/bin/env python3
"""
PreToolUse hook: Suggest Tavily search over WebSearch.

Warns (allows command to proceed):
- WebSearch → suggests Tavily for better results

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
warning = f"""⚠️  PREFER Tavily: For web research, use Tavily instead of WebSearch.

Tavily provides better results for current information, research questions, and comparisons.

To use Tavily search:
  mcp__tavily__tavily_search
    query: "{query}"
    search_depth: "basic"
    max_results: 10

For comprehensive research, use search_depth: "advanced"

See mcp-tavily skill for full usage patterns and options.
"""

print(warning, file=sys.stderr)

# Exit 0 allows the command to proceed (soft warning)
sys.exit(0)
