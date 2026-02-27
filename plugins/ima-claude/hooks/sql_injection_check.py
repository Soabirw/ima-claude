#!/usr/bin/env python3
"""
PostToolUse hook: Warn about SQL string interpolation in JS/TS files.

Checks (soft warning only, exit 0):
  H2 — Template literals or string concatenation building SQL queries with dynamic values.

Applies to: Edit, Write on .js, .ts, .mjs, .mts files.
"""
import json
import re
import sys

JS_EXTENSIONS = (".js", ".ts", ".mjs", ".mts")

SQL_KEYWORDS = r"(?:SELECT|INSERT|UPDATE|DELETE|WHERE)"

# Template literal: `SELECT ... ${`
TEMPLATE_LITERAL_PATTERN = re.compile(
    rf"`[^`]*\b{SQL_KEYWORDS}\b[^`]*\${{",
    re.IGNORECASE | re.DOTALL,
)

# String concatenation: "SELECT..." + or 'SELECT...' +
STRING_CONCAT_PATTERN = re.compile(
    rf"""(?:"|')[^"']*\b{SQL_KEYWORDS}\b[^"']*(?:"|')\s*\+""",
    re.IGNORECASE,
)

WARNING = (
    "⚠️  H2: SQL string interpolation detected — use parameterized queries instead.\n"
    "  WRONG: `SELECT * FROM users WHERE id = ${userId}`\n"
    "  RIGHT: { sql: 'SELECT * FROM users WHERE id = ?', params: [userId] }"
)


def has_sql_interpolation(content: str) -> bool:
    return bool(
        TEMPLATE_LITERAL_PATTERN.search(content)
        or STRING_CONCAT_PATTERN.search(content)
    )


def get_content(tool_name: str, tool_input: dict) -> str:
    if tool_name == "Write":
        return tool_input.get("content", "")
    # Edit: scan only the new_string — no need to read the full file for SQL injection
    return tool_input.get("new_string", "")


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
file_path = tool_input.get("file_path", "")

if tool_name not in ("Edit", "Write"):
    sys.exit(0)

if not file_path.endswith(JS_EXTENSIONS):
    sys.exit(0)

content = get_content(tool_name, tool_input)
if not content:
    sys.exit(0)

if has_sql_interpolation(content):
    print(WARNING, file=sys.stderr)

sys.exit(0)
