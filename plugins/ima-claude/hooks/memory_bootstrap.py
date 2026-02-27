#!/usr/bin/env python3
"""
PreToolUse hook: Remind Claude to search Vestige + Qdrant before starting work.

On the first non-memory tool use per session, prints a reminder to stderr.
Uses a timestamp-based state file to avoid repeating within the same session.
Exit code 0 = allow tool to proceed (soft warning only).
"""
import json
import os
import sys
import time

STATE_FILE = os.path.expanduser("~/.claude/.memory_bootstrapped")
STALENESS_SECONDS = 3600  # 1 hour — new session after this gap

MEMORY_TOOLS = {
    "mcp__vestige__search",
    "mcp__vestige__smart_ingest",
    "mcp__vestige__ingest",
    "mcp__vestige__memory",
    "mcp__vestige__intention",
    "mcp__vestige__codebase",
    "mcp__vestige__promote_memory",
    "mcp__vestige__demote_memory",
    "mcp__vestige__session_checkpoint",
    "mcp__qdrant-memory__qdrant-find",
    "mcp__qdrant-memory__qdrant-store",
    "mcp__serena__read_memory",
    "mcp__serena__list_memories",
    "mcp__serena__write_memory",
}

REMINDER = """Memory bootstrap: Search Vestige and Qdrant before starting work.
  mcp__vestige__search query: "{project}" limit: 5
  mcp__qdrant-memory__qdrant-find query: "{project}"
  mcp__vestige__intention action: "check"
"""


def is_bootstrapped():
    """Check if memory bootstrap already happened this session."""
    if not os.path.exists(STATE_FILE):
        return False
    try:
        mtime = os.path.getmtime(STATE_FILE)
        return (time.time() - mtime) < STALENESS_SECONDS
    except OSError:
        return False


def mark_bootstrapped():
    """Mark that bootstrap reminder has fired."""
    state_dir = os.path.dirname(STATE_FILE)
    os.makedirs(state_dir, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(str(time.time()))


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")

# If this IS a memory tool, mark as bootstrapped and exit silently
if tool_name in MEMORY_TOOLS:
    mark_bootstrapped()
    sys.exit(0)

# If already bootstrapped this session, exit silently
if is_bootstrapped():
    sys.exit(0)

# First non-memory tool use — print reminder and mark bootstrapped
print(REMINDER, file=sys.stderr)
mark_bootstrapped()
sys.exit(0)
