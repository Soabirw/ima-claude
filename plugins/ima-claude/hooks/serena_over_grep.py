#!/usr/bin/env python3
"""
PreToolUse hook: Nudge toward Serena symbol tools when Grep is used for code navigation.

When Claude uses Grep with patterns that look like symbol searches (class definitions,
function references, import tracing), suggest Serena's symbol tools instead — they're
more precise, understand scope, and save tokens.

Fires on every other symbol-like Grep (counter-based) to stay persistent without
being noise on every single search.
Exit code 0 = soft warning via stderr.
"""
import json
import os
import re
import sys
import time

STATE_FILE = os.path.expanduser("~/.claude/.serena_grep_count")
STALENESS_SECONDS = 3600
FIRE_EVERY_N = 2  # Remind on every Nth symbol-like grep

SYMBOL_PATTERNS = [
    r"^(class|interface|trait|enum|abstract\s+class)\s+\w+",
    r"^(function|def|fn)\s+\w+",
    r"^(extends|implements)\s+\w+",
    r"^(use|import|require|from)\s+",
    r"->(\w+)\(",            # method call
    r"::\w+\(",              # static method call
    r"new\s+\w+",            # constructor
    r"\bfunction_exists\(",
    r"\bclass_exists\(",
]

COMPILED_PATTERNS = [re.compile(p) for p in SYMBOL_PATTERNS]

REMINDER = """Serena finds symbols without scanning file contents — much cheaper than Grep:
  mcp__serena__jet_brains_find_symbol name_path_pattern: "{symbol}"
      → exact match, understands scope and inheritance
  mcp__serena__jet_brains_find_referencing_symbols name_path: "{symbol}"  relative_path: "{file}"
      → every caller across the codebase
  mcp__serena__jet_brains_get_symbols_overview relative_path: "{file}"
      → all symbols in a file without reading it
Grep for text search. Serena for symbol search. 40-70% token savings."""


def get_count() -> int:
    if not os.path.exists(STATE_FILE):
        return 0
    try:
        with open(STATE_FILE) as f:
            data = json.load(f)
        if time.time() - data.get("ts", 0) > STALENESS_SECONDS:
            return 0
        return data.get("count", 0)
    except (json.JSONDecodeError, OSError):
        return 0


def increment_count(current: int) -> None:
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"count": current + 1, "ts": time.time()}, f)


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
if tool_name != "Grep":
    sys.exit(0)

pattern = input_data.get("tool_input", {}).get("pattern", "")
if not pattern:
    sys.exit(0)

is_symbol_search = any(cp.search(pattern) for cp in COMPILED_PATTERNS)
if not is_symbol_search:
    sys.exit(0)

count = get_count()
increment_count(count)

# Fire on every Nth symbol grep (0-indexed: fire when count % N == 0)
if count % FIRE_EVERY_N != 0:
    sys.exit(0)

symbol_match = re.search(r"\b([A-Z]\w+|\w+Service|\w+Controller|\w+Handler|\w+Repository)\b", pattern)
symbol = symbol_match.group(1) if symbol_match else "SymbolName"

file_hint = input_data.get("tool_input", {}).get("path", "path/to/file")

print(REMINDER.replace("{symbol}", symbol).replace("{file}", str(file_hint)), file=sys.stderr)
sys.exit(0)
