#!/usr/bin/env python3
"""
UserPromptSubmit hook: Remind Claude to invoke task-master before non-trivial implementation.

M7 — Remind about task-master for non-trivial implementation requests.

Fires when the prompt contains both an action verb and a scope noun, is longer than
30 words, and does not contain trivial-signal words or a skill invocation prefix.
Fires once per session using a timestamp-based state file.
Exit code 0 = soft warning via stderr.
"""
import json
import os
import re
import sys
import time

STATE_FILE = os.path.expanduser("~/.claude/.task_master_reminded")
STALENESS_SECONDS = 3600  # 1 hour — new session after this gap

ACTION_VERBS = re.compile(
    r"\b(implement|build|create|write|add|develop|make|set\s+up|refactor|migrate|convert)\b",
    re.IGNORECASE,
)

SCOPE_NOUNS = re.compile(
    r"\b(feature|component|system|module|plugin|endpoint|service|page|form|api|hook"
    r"|integration|workflow|authentication|dashboard)\b",
    re.IGNORECASE,
)

TRIVIAL_SIGNALS = re.compile(
    r"\b(trivial|quick|simple|just|only)\b",
    re.IGNORECASE,
)

REMINDER = """Non-trivial implementation request detected — consider task-planner first:
  /task-planner to decompose into Epic > Story > Task hierarchy and select storage.
  Then /task-runner to delegate to agents. Opus orchestrates. Sonnet implements."""


def is_reminded() -> bool:
    """Check if the task-master reminder already fired this session."""
    if not os.path.exists(STATE_FILE):
        return False
    try:
        mtime = os.path.getmtime(STATE_FILE)
        return (time.time() - mtime) < STALENESS_SECONDS
    except OSError:
        return False


def mark_reminded() -> None:
    """Record that the reminder has fired."""
    state_dir = os.path.dirname(STATE_FILE)
    os.makedirs(state_dir, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(str(time.time()))


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

prompt = input_data.get("user_prompt", "").strip()

if not prompt:
    sys.exit(0)

# Skip skill invocations
if prompt.startswith("/"):
    sys.exit(0)

# Skip if trivial signals present
if TRIVIAL_SIGNALS.search(prompt):
    sys.exit(0)

# Must be longer than 30 words
if len(prompt.split()) <= 30:
    sys.exit(0)

# Must have both an action verb and a scope noun
if not ACTION_VERBS.search(prompt) or not SCOPE_NOUNS.search(prompt):
    sys.exit(0)

# Only remind once per session
if is_reminded():
    sys.exit(0)

mark_reminded()
print(REMINDER, file=sys.stderr)
sys.exit(0)
