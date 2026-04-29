#!/usr/bin/env python3
"""OpenAI Codex CLI → Claude Code tool name translator shim.

Sits between Codex CLI and ima-claude hook scripts, translating Codex
tool names to their Claude Code equivalents so existing hooks (which
read `tool_name="Bash"`, etc.) work unmodified.

Codex hook events (PreToolUse, PostToolUse, UserPromptSubmit, SessionStart)
already match Claude Code's names, so only the `tool_name` field inside
the JSON payload needs rewriting.

Usage (in hooks.json):
  python3 ~/.codex/hooks/hooks-translator.py ~/.codex/hooks/some_hook.py
"""

import json
import subprocess
import sys

# Codex CLI → Claude Code tool name mapping (reverse of adapter TOOL_MAP)
CODEX_TO_CLAUDE = {
    "shell": "Bash",
    "read": "Read",
    "edit": "Edit",
    "write": "Write",
    "glob": "Glob",
    "grep": "Grep",
    "list": "LS",
    "web_search": "WebSearch",
    "fetch": "WebFetch",
    "ExitPlanMode": "ExitPlanMode",
}


def main():
    if len(sys.argv) < 2:
        print("Usage: hooks-translator.py <hook-script> [args...]", file=sys.stderr)
        sys.exit(1)

    target_script = sys.argv[1]
    extra_args = sys.argv[2:]

    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as e:
        print(f"hooks-translator: invalid JSON from stdin: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = data.get("tool_name", "")
    if tool_name in CODEX_TO_CLAUDE:
        data["tool_name"] = CODEX_TO_CLAUDE[tool_name]

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
