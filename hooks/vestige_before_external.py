#!/usr/bin/env python3
"""
PreToolUse hook: Remind Claude to check Vestige before external lookups.

H5 — If Context7 or Tavily is called before any Vestige search this session,
warn once that memory may already contain the needed context.

State is tracked via a timestamp file that expires after 1 hour (new session boundary).
Exit code 0 = allow tool to proceed (soft warning only).
"""
import json
import os
import sys
import time

STATE_FILE = os.path.expanduser("~/.claude/.vestige_searched")
STALENESS_SECONDS = 3600  # 1 hour — new session after this gap

REMINDER = """No Vestige search detected yet — check memory before external lookups.
  mcp__vestige__search query: "{topic}" limit: 5
Vestige may already have what you need (decisions, patterns, prior context).
"""


def is_fresh():
    """Return True if state file exists and was written within this session."""
    if not os.path.exists(STATE_FILE):
        return False
    try:
        mtime = os.path.getmtime(STATE_FILE)
        return (time.time() - mtime) < STALENESS_SECONDS
    except OSError:
        return False


def mark_state(tag):
    """Write a tag to the state file and refresh its mtime."""
    state_dir = os.path.dirname(STATE_FILE)
    os.makedirs(state_dir, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(tag)


def read_state():
    """Read the current tag from the state file."""
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    except OSError:
        return ""


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

# If this IS a Vestige search, mark session as searched and exit silently
if tool_name.startswith("mcp__vestige__search"):
    mark_state("searched")
    sys.exit(0)

# Only act on Context7 or Tavily calls
if not (tool_name.startswith("mcp__context7__") or tool_name.startswith("mcp__tavily__")):
    sys.exit(0)

# If state file is fresh (searched or warned), exit silently — don't nag
if is_fresh():
    sys.exit(0)

# Derive a topic hint from the tool input for the suggestion
topic = (
    tool_input.get("query")
    or tool_input.get("libraryName")
    or tool_input.get("url")
    or "<topic>"
)

print(REMINDER.format(topic=topic), file=sys.stderr)

# Mark as warned so this fires only once per session
mark_state("warned")
sys.exit(0)
