#!/usr/bin/env python3
"""
PostToolUse hook: Nudge Claude to store decisions/patterns after several edits.

After every 5th Edit/Write without a Vestige or Qdrant store, prints a gentle reminder.
Counter resets when a memory store is detected or after the reminder fires.
Exit code 0 = allow tool to proceed (soft warning only).
"""
import json
import os
import sys

STATE_FILE = os.path.expanduser("~/.claude/.memory_edit_count")
EDIT_THRESHOLD = 5

MEMORY_STORE_TOOLS = {
    "mcp__vestige__smart_ingest",
    "mcp__vestige__ingest",
    "mcp__vestige__codebase",
    "mcp__vestige__session_checkpoint",
    "mcp__qdrant-memory__qdrant-store",
    "mcp__serena__write_memory",
}

REMINDER = """You've made several changes this session. Any decisions or patterns worth storing?
  → Vestige smart_ingest for decisions/patterns (neural, fades if unused)
  → Qdrant qdrant-store for reference material (permanent library)
"""


def get_edit_count():
    """Read current edit count from state file."""
    if not os.path.exists(STATE_FILE):
        return 0
    try:
        with open(STATE_FILE, "r") as f:
            return int(f.read().strip())
    except (ValueError, OSError):
        return 0


def set_edit_count(count):
    """Write edit count to state file."""
    state_dir = os.path.dirname(STATE_FILE)
    os.makedirs(state_dir, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(str(count))


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")

# If a memory store just happened, reset counter
if tool_name in MEMORY_STORE_TOOLS:
    set_edit_count(0)
    sys.exit(0)

# Only count Edit and Write tools
if tool_name not in ("Edit", "Write"):
    sys.exit(0)

# Increment edit count
count = get_edit_count() + 1

if count >= EDIT_THRESHOLD:
    print(REMINDER, file=sys.stderr)
    set_edit_count(0)  # Reset after reminding
else:
    set_edit_count(count)

sys.exit(0)
