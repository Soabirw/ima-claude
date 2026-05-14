#!/usr/bin/env python3
"""
UserPromptSubmit hook: Remind Claude to fetch Jira issue context when a key is detected.

M6 — Auto-fetch Jira issue when key detected in prompt.

Scans the user prompt for Jira issue key patterns (e.g., FNR-123, IMA-456).
Prints a reminder to fetch the issue via Atlassian MCP for the first new key seen.
Tracks seen keys in ~/.claude/.jira_keys_fetched to avoid repeat reminders.
Exit code 0 = soft warning via stderr.
"""
import json
import os
import re
import sys
import time

# Only run if Jira/Atlassian integration is enabled
if os.environ.get("JIRA_ENABLED", "").lower() != "true":
    sys.exit(0)

STATE_FILE = os.path.expanduser("~/.claude/.jira_keys_fetched")
STALENESS_SECONDS = 3600  # 1 hour — reset seen keys after this gap

JIRA_KEY_PATTERN = re.compile(r"\b[A-Z]{2,10}-\d+\b")

CLOUD_ID = "<cloudId>"


def load_seen_keys() -> set[str]:
    """Load previously seen Jira keys from state file, if still fresh."""
    if not os.path.exists(STATE_FILE):
        return set()
    try:
        mtime = os.path.getmtime(STATE_FILE)
        if (time.time() - mtime) >= STALENESS_SECONDS:
            return set()
        with open(STATE_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    except OSError:
        return set()


def save_seen_keys(keys: set[str]) -> None:
    """Persist the set of seen Jira keys to the state file."""
    state_dir = os.path.dirname(STATE_FILE)
    os.makedirs(state_dir, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write("\n".join(sorted(keys)))


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

prompt = input_data.get("user_prompt", "")

if not prompt:
    sys.exit(0)

matches = JIRA_KEY_PATTERN.findall(prompt)

if not matches:
    sys.exit(0)

first_key = matches[0]

seen_keys = load_seen_keys()

if first_key in seen_keys:
    sys.exit(0)

seen_keys.add(first_key)
save_seen_keys(seen_keys)

print(
    f'Jira issue key {first_key} detected — consider fetching context:\n'
    f'  mcp__claude_ai_Atlassian__getJiraIssue issueIdOrKey: "{first_key}" cloudId: "{CLOUD_ID}"',
    file=sys.stderr,
)

sys.exit(0)
