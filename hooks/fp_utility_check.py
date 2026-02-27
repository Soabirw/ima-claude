#!/usr/bin/env python3
"""
PostToolUse hook: Warn about custom FP utility definitions.

Checks (soft warning only, exit 0):
  M1 — Custom pipe/compose using reduce/reduceRight
  M1 — Custom curry with rest/spread params
  M1 — Custom monads (Maybe, Either, Result, Option classes)
  M1 — Custom pattern matching function named 'match'

Applies to: Edit, Write on .js, .ts, .mjs, .mts, .php files.
"""
import json
import re
import sys

JS_PHP_EXTENSIONS = (".js", ".ts", ".mjs", ".mts", ".php")

# Import lines — these are safe, skip them
IMPORT_LINE = re.compile(r"^\s*(import|require|use)\b", re.MULTILINE)

FP_UTILITY_PATTERNS = [
    # pipe/compose backed by reduce
    re.compile(r"(function|const|let|var)\s+pipe\s*[=(].*reduce", re.DOTALL),
    re.compile(r"(function|const|let|var)\s+compose\s*[=(].*reduce", re.DOTALL),
    # PHP pipe/compose
    re.compile(r"function\s+pipe\s*\("),
    re.compile(r"function\s+compose\s*\("),
    # curry definitions
    re.compile(r"(function|const|let|var)\s+curry\s*[=(]"),
    # monad classes
    re.compile(r"class\s+(Maybe|Either|Result|Option)\b"),
    # custom match pattern matching
    re.compile(r"(function|const|let|var)\s+match\s*[=(][^;]*patterns", re.DOTALL),
]

WARNING = (
    "⚠️  Custom FP utility detected — js-fp/php-fp skills say: use native patterns instead.\n"
    "  No pipe/compose — use chained methods or intermediate variables\n"
    "  No curry — use closures and partial application naturally\n"
    "  No custom monads — use early returns, null coalescing, optional chaining"
)


def is_import_line(line: str) -> bool:
    return bool(IMPORT_LINE.match(line))


def strip_import_lines(content: str) -> str:
    return "\n".join(
        line for line in content.splitlines()
        if not is_import_line(line)
    )


def has_fp_utility(content: str) -> bool:
    cleaned = strip_import_lines(content)
    return any(pattern.search(cleaned) for pattern in FP_UTILITY_PATTERNS)


def get_content(tool_name: str, tool_input: dict) -> str:
    if tool_name == "Write":
        return tool_input.get("content", "")
    # Edit: scan only new_string — we care about what's being added
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

if not file_path.endswith(JS_PHP_EXTENSIONS):
    sys.exit(0)

content = get_content(tool_name, tool_input)
if not content:
    sys.exit(0)

if has_fp_utility(content):
    print(WARNING, file=sys.stderr)

sys.exit(0)
