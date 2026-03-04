#!/usr/bin/env python3
"""
PreToolUse hook: BLOCK sed file editing via Bash.

Hard guard (exit 1 = block execution). sed edits are a symptom of a broken
workflow — Claude either didn't read the file first, didn't use Serena's
symbolic editing, or is working with a file that's too large.

Allowed through:
- Piped sed transforms (no -i, no file redirect)
- Data pipelines (echo ... | sed ...)
"""
import json
import re
import sys

BLOCK_MESSAGE = """🚫 BLOCKED: sed file editing is never the right approach.

You're using sed because something went wrong. Stop and fix the root cause:

1. READ the file first — Edit/Write require a prior Read (did you skip this?)
2. Use Serena symbolic editing — replace_symbol_body, insert_after_symbol, insert_before_symbol
3. Use Edit tool for targeted string replacements
4. If the file is too large to read (>500 lines), that's a separate problem — the file needs refactoring

DO NOT retry with sed. Go back to step 1."""


def is_sed_file_edit(command: str) -> bool:
    """Detect sed commands that mutate files (not piped transforms)."""
    # sed -i (in-place edit) in any flag position
    if re.search(r"\bsed\b.*\s-[^\s]*i", command):
        return True

    # sed ... > file or sed ... >> file (redirect output to file)
    if re.search(r"\bsed\b.+>{1,2}\s*\S+", command):
        # But not if sed input is piped (e.g., echo x | sed ... > file is borderline,
        # but still a file mutation via sed — block it)
        return True

    return False


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

if is_sed_file_edit(command):
    print(BLOCK_MESSAGE, file=sys.stderr)
    sys.exit(1)
