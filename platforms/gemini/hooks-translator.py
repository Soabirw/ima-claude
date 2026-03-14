#!/usr/bin/env python3
"""Gemini CLI → Claude Code tool name translator shim.

Sits between Gemini CLI and ima-claude hook scripts, translating
Gemini tool names to their Claude Code equivalents so existing hooks
work unmodified.

Usage (in hooks.json):
  python3 ~/.gemini/hooks/hooks-translator.py ~/.gemini/hooks/some_hook.py
"""

import json
import subprocess
import sys

# Gemini CLI → Claude Code tool name mapping (reverse of adapter TOOL_MAP)
GEMINI_TO_CLAUDE = {
    "run_shell_command": "Bash",
    "read_file": "Read",
    "replace": "Edit",
    "write_file": "Write",
    "glob": "Glob",
    "grep_search": "Grep",
    "list_directory": "LS",
    "google_web_search": "WebSearch",
    "web_fetch": "WebFetch",
    "exit_plan_mode": "ExitPlanMode",
}


def main():
    if len(sys.argv) < 2:
        print("Usage: hooks-translator.py <hook-script> [args...]", file=sys.stderr)
        sys.exit(1)

    target_script = sys.argv[1]
    extra_args = sys.argv[2:]

    # Read JSON from stdin
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as e:
        print(f"hooks-translator: invalid JSON from stdin: {e}", file=sys.stderr)
        sys.exit(1)

    # Translate tool_name if present
    tool_name = data.get("tool_name", "")
    if tool_name in GEMINI_TO_CLAUDE:
        data["tool_name"] = GEMINI_TO_CLAUDE[tool_name]

    # Pipe translated JSON to the actual hook script
    translated = json.dumps(data)
    result = subprocess.run(
        ["python3", target_script] + extra_args,
        input=translated,
        stdout=None,
        stderr=None,
        text=True,
    )

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
