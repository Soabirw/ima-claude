#!/usr/bin/env python3
"""
PreToolUse hook: Redirect WebFetch to Tavily extract.

Tavily provides better content extraction and respects rate limits.
"""
import json
import sys

try:
    data = json.load(sys.stdin)
    url = data["tool_input"]["url"]
except (KeyError, json.JSONDecodeError) as err:
    print(f"hook-error: {err}", file=sys.stderr)
    sys.exit(1)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"Please use mcp__tavily__tavily-extract with urls: ['{url}'] and extract_depth: 'advanced'"
    }
}, separators=(',', ':')))
sys.exit(0)
