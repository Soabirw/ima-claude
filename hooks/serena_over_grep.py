#!/usr/bin/env python3
"""
PreToolUse hook: Nudge toward Serena symbol tools when Grep is used for code navigation.

When Claude uses Grep with patterns that look like symbol searches (class definitions,
function references, import tracing), suggest Serena's symbol tools instead — they're
more precise, understand scope, and save tokens.

Only fires once per session to avoid nagging.
Exit code 0 = soft warning via stderr.
"""
import json
import os
import re
import sys
import time

STATE_FILE = os.path.expanduser("~/.claude/.serena_grep_reminded")
STALENESS_SECONDS = 3600

SYMBOL_PATTERNS = [
    r"^(class|interface|trait|enum|abstract\s+class)\s+\w+",
    r"^(function|def|fn)\s+\w+",
    r"^(extends|implements)\s+\w+",
    r"^(use|import|require|from)\s+",
    r"->(\w+)\(",          # method call
    r"::\w+\(",            # static method call
    r"new\s+\w+",          # constructor
    r"\bfunction_exists\(",
    r"\bclass_exists\(",
]

COMPILED_PATTERNS = [re.compile(p) for p in SYMBOL_PATTERNS]

REMINDER = """Serena has symbol-aware tools that are more precise than Grep for code navigation:
  mcp__serena__jet_brains_find_symbol name_path_pattern: "{symbol}"
  mcp__serena__jet_brains_find_referencing_symbols name_path: "{symbol}"
  mcp__serena__jet_brains_get_symbols_overview relative_path: "{file}"
Serena understands scope, inheritance, and cross-file references. 40-70% token savings.
"""


def is_reminded():
    """Check if already reminded this session."""
    if not os.path.exists(STATE_FILE):
        return False
    try:
        mtime = os.path.getmtime(STATE_FILE)
        return (time.time() - mtime) < STALENESS_SECONDS
    except OSError:
        return False


def mark_reminded():
    """Mark that we've reminded about Serena."""
    state_dir = os.path.dirname(STATE_FILE)
    os.makedirs(state_dir, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(str(time.time()))


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")

if tool_name != "Grep":
    sys.exit(0)

if is_reminded():
    sys.exit(0)

# Check if the grep pattern looks like a symbol search
pattern = input_data.get("tool_input", {}).get("pattern", "")
if not pattern:
    sys.exit(0)

for compiled in COMPILED_PATTERNS:
    if compiled.search(pattern):
        # Extract a symbol hint from the pattern for the reminder
        symbol_match = re.search(r"\b([A-Z]\w+|\w+Service|\w+Controller|\w+Handler)\b", pattern)
        symbol = symbol_match.group(1) if symbol_match else "SymbolName"

        msg = REMINDER.replace("{symbol}", symbol).replace("{file}", "path/to/file")
        print(msg, file=sys.stderr)
        mark_reminded()
        break

sys.exit(0)
