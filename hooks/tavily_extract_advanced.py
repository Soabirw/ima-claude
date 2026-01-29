#!/usr/bin/env python3
"""
PreToolUse hook: Note about Tavily extract usage.

This hook is informational - Tavily extract calls proceed normally.
It reminds about the Airis gateway pattern if using direct tool names.
"""
import json
import sys

try:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
except json.JSONDecodeError as err:
    print(f"hook-error: {err}", file=sys.stderr)
    sys.exit(1)

# Check if using old direct tool name pattern
if tool_name.startswith("mcp__tavily__"):
    warning = """⚠️  Tavily via Airis: Use the Airis gateway pattern for Tavily tools:

  mcp__airis-mcp-gateway__airis-exec
    tool: "tavily:tavily_search"    (for search)
    tool: "tavily:tavily_extract"   (for URL extraction)

See /mcp-tavily skill for full usage patterns.
"""
    print(warning, file=sys.stderr)

# Always allow - this is just informational
sys.exit(0)
