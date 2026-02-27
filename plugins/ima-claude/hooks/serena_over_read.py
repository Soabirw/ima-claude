#!/usr/bin/env python3
"""
PreToolUse hook: Suggest Serena symbol tools before reading code files.

Reading an entire file to understand its structure costs 2-10x more tokens than
using Serena's symbol overview. This hook fires on every code file Read and
reminds Claude to try the cheaper path first.

Fires on every code file read — not rate-limited, because the savings compound.
Skip list: config files, markdown, json, yaml, lock files, env files.
Exit code 0 = soft warning via stderr.
"""
import json
import os
import sys

CODE_EXTENSIONS = {
    ".php", ".ts", ".tsx", ".js", ".jsx", ".py",
    ".rb", ".go", ".java", ".cs", ".vue", ".svelte",
    ".rs", ".cpp", ".c", ".h",
}

SKIP_EXTENSIONS = {
    ".md", ".json", ".yaml", ".yml", ".lock", ".env",
    ".txt", ".csv", ".xml", ".html", ".css", ".scss",
    ".toml", ".ini", ".cfg", ".conf", ".sh", ".bash",
}

REMINDER = """Serena symbol tools cost 40-70% fewer tokens than reading files:
  mcp__serena__jet_brains_get_symbols_overview relative_path: "{file}"
      → structure of the file (classes, methods, properties) without reading it
  mcp__serena__jet_brains_find_symbol name_path_pattern: "ClassName"
      → find any symbol across the codebase instantly
  mcp__serena__jet_brains_find_referencing_symbols name_path: "method"  relative_path: "{file}"
      → find every caller without grep
Use Read only when you need the full implementation body of a specific symbol."""


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
if tool_name != "Read":
    sys.exit(0)

file_path = input_data.get("tool_input", {}).get("file_path", "")
if not file_path:
    sys.exit(0)

_, ext = os.path.splitext(file_path.lower())

# Only fire for code files
if ext in SKIP_EXTENSIONS or ext not in CODE_EXTENSIONS:
    sys.exit(0)

# Skip very small files (probably configs or stubs) — threshold 5KB
try:
    if os.path.getsize(file_path) < 5000:
        sys.exit(0)
except OSError:
    pass  # File doesn't exist yet or can't stat — proceed

print(REMINDER.replace("{file}", file_path), file=sys.stderr)
sys.exit(0)
