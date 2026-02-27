#!/usr/bin/env python3
"""
PreToolUse hook: Auto-upgrade Tavily extract to advanced mode for better results.

This hook intercepts tavily_extract calls and suggests using extract_depth: "advanced"
for LinkedIn, protected sites, or when tables/embedded content are needed.
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

# Check if using Tavily extract
if tool_name == "mcp__tavily__tavily_extract":
    extract_depth = tool_input.get("extract_depth", "basic")
    urls = tool_input.get("urls", [])

    # Check if any URLs need advanced extraction
    needs_advanced = any(
        "linkedin.com" in url or
        "protected" in url.lower() or
        "login" in url.lower()
        for url in urls
    )

    if extract_depth == "basic" and needs_advanced:
        warning = """💡 SUGGESTION: Consider extract_depth: "advanced" for:
  - LinkedIn profiles or protected sites
  - Pages with tables or embedded content
  - Sites requiring more thorough extraction

To use advanced extraction:
  mcp__tavily__tavily_extract
    urls: [...]
    extract_depth: "advanced"

Proceeding with basic extraction...
"""
        print(warning, file=sys.stderr)

# Always allow - this is just informational
sys.exit(0)
