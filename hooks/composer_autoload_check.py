#!/usr/bin/env python3
"""
PostToolUse hook: Warn about Composer autoload "files" entries that break PHPUnit.

M9 — Composer autoload files bug detection (from phpunit-wp skill).

After writing or editing a composer.json, checks whether autoload.files is populated.
Autoload files run BEFORE the test bootstrap defines ABSPATH/WPINC, causing WordPress
plugin files to fatal error during `composer install` in test environments.
Exit code 0 = soft warning via stderr.
"""
import json
import sys

WARNING = (
    '⚠️  Composer autoload "files" detected — this can break PHPUnit tests.\n'
    "  Autoload files run BEFORE test bootstrap defines ABSPATH/WPINC.\n"
    "  WordPress plugin files will fatal error during `composer install`.\n"
    "  Fix: Move plugin files to autoload.classmap or load via bootstrap.\n"
    "  See /phpunit-wp skill for the full fix pattern."
)


def get_content(tool_name: str, tool_input: dict) -> str:
    if tool_name == "Write":
        return tool_input.get("content", "")

    # Edit: file already written to disk — read it for the current state
    file_path = tool_input.get("file_path", "")
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def has_autoload_files(content: str) -> bool:
    try:
        data = json.loads(content)
    except (json.JSONDecodeError, ValueError):
        return False

    files = data.get("autoload", {}).get("files", [])
    return isinstance(files, list) and len(files) > 0


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
file_path = tool_input.get("file_path", "")

if tool_name not in ("Edit", "Write"):
    sys.exit(0)

if not file_path.endswith("composer.json"):
    sys.exit(0)

content = get_content(tool_name, tool_input)

if not content:
    sys.exit(0)

if has_autoload_files(content):
    print(WARNING, file=sys.stderr)

sys.exit(0)
