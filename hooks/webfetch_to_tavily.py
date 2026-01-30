#!/usr/bin/env python3
"""
PreToolUse hook: Suggest Tavily extract over WebFetch for certain URLs.

Warns (allows command to proceed):
- WebFetch → suggests Tavily extract for better content extraction

Tavily provides better content extraction for articles, documentation,
and complex web pages.
"""
import json
import sys

try:
    data = json.load(sys.stdin)
    tool_input = data.get("tool_input", {})
    url = tool_input.get("url", "")
except json.JSONDecodeError as err:
    print(f"hook-error: {err}", file=sys.stderr)
    sys.exit(1)

# Print warning to stderr (shown to Claude)
warning = f"""⚠️  CONSIDER Tavily: For web content extraction, Tavily often provides cleaner results.

WebFetch is fine for simple pages, but Tavily extract handles complex pages better.

To use Tavily extract:
  mcp__tavily__tavily_extract
    urls: ["{url}"]
    extract_depth: "basic"

For LinkedIn or protected sites, use extract_depth: "advanced"

See mcp-tavily skill for full usage patterns.

Proceeding with WebFetch...
"""

print(warning, file=sys.stderr)

# Exit 0 allows the command to proceed (soft warning)
sys.exit(0)
