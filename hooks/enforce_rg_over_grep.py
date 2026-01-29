#!/usr/bin/env python3
"""
PreToolUse hook: Warn about using grep/find instead of ripgrep.

Warns (allows command to proceed):
- grep → suggests rg
- find -name → suggests rg --files -g pattern

The warning is shown to Claude, encouraging it to use rg for subsequent operations.
"""
import json
import re
import sys

VALIDATION_RULES = [
    (
        r"\bgrep\b(?!.*\|)",
        "⚠️  PREFER ripgrep: Use 'rg' instead of 'grep' - faster, better defaults, respects .gitignore. "
        "Please use 'rg' for the rest of this session. See /rg skill for usage.",
    ),
    (
        r"\bfind\s+\S+\s+-name\b",
        "⚠️  PREFER ripgrep: Use 'rg --files -g \"pattern\"' instead of 'find -name' - faster, respects .gitignore. "
        "Please use 'rg' for the rest of this session. See /rg skill for usage.",
    ),
]


def validate_command(command: str) -> list[str]:
    issues = []
    for pattern, message in VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)
    return issues


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

if tool_name != "Bash" or not command:
    sys.exit(0)

issues = validate_command(command)

if issues:
    for message in issues:
        print(f"{message}", file=sys.stderr)
    # Exit code 0 allows command to proceed but stderr is shown to Claude as a warning
    sys.exit(0)
