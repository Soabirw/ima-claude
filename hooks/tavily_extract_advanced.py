#!/usr/bin/env python3
"""
PreToolUse hook: Auto-upgrade Tavily extract to advanced mode.

Automatically sets extract_depth="advanced" for better content extraction.
"""
import json
import sys

try:
    data = json.load(sys.stdin)
    tool_input = data["tool_input"]

    # Always ensure extract_depth="advanced"
    tool_input["extract_depth"] = "advanced"

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Auto-upgraded Tavily extract to advanced mode"
        }
    }, separators=(',', ':')))
    sys.exit(0)

except (KeyError, json.JSONDecodeError) as err:
    print(f"hook-error: {err}", file=sys.stderr)
    sys.exit(1)
