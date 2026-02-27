#!/usr/bin/env python3
"""
PreToolUse hook: Enforce Atlassian MCP prerequisites before tool calls.

Three checks combined:
  H3 — cloudId bootstrap: getAccessibleAtlassianResources must be called first
  H4 — transitions: getTransitionsForJiraIssue must precede transitionJiraIssue
  M5 — ADF body: Confluence page body must be a JSON string, not a raw object

State is tracked in a JSON file that expires after 1 hour (new session boundary).
Exit code 0 = allow tool to proceed (soft warnings only).
"""
import json
import os
import sys
import time

STATE_FILE = os.path.expanduser("~/.claude/.atlassian_session_state")
STALENESS_SECONDS = 3600  # 1 hour — new session after this gap

BOOTSTRAP_TOOL = "mcp__claude_ai_Atlassian__getAccessibleAtlassianResources"
TRANSITIONS_TOOL = "mcp__claude_ai_Atlassian__getTransitionsForJiraIssue"
TRANSITION_ISSUE_TOOL = "mcp__claude_ai_Atlassian__transitionJiraIssue"
CONFLUENCE_WRITE_TOOLS = {
    "mcp__claude_ai_Atlassian__createConfluencePage",
    "mcp__claude_ai_Atlassian__updateConfluencePage",
}

BOOTSTRAP_WARNING = """Atlassian bootstrap: Call getAccessibleAtlassianResources first to obtain cloudId.
  mcp__claude_ai_Atlassian__getAccessibleAtlassianResources
"""

TRANSITIONS_WARNING = """Transition IDs are issue-specific — call getTransitionsForJiraIssue first.
  mcp__claude_ai_Atlassian__getTransitionsForJiraIssue issueIdOrKey: "{key}"
"""

ADF_WARNING = """ADF body must be a JSON string (JSON.stringify'd), not a raw object — #1 cause of Confluence failures.
"""


def load_state():
    """Load session state, returning defaults if missing or stale."""
    default = {"bootstrapped": False, "transitions_fetched": False, "timestamp": 0.0}
    if not os.path.exists(STATE_FILE):
        return default
    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
        if (time.time() - state.get("timestamp", 0)) > STALENESS_SECONDS:
            return default
        return state
    except (json.JSONDecodeError, OSError):
        return default


def save_state(state):
    """Write session state to disk."""
    state_dir = os.path.dirname(STATE_FILE)
    os.makedirs(state_dir, exist_ok=True)
    state["timestamp"] = time.time()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

# Only act on Atlassian MCP tools
if not tool_name.startswith("mcp__claude_ai_Atlassian__"):
    sys.exit(0)

state = load_state()

# H3: If this IS the bootstrap tool, mark and exit silently
if tool_name == BOOTSTRAP_TOOL:
    state["bootstrapped"] = True
    save_state(state)
    sys.exit(0)

# H4: If this IS the transitions fetch tool, mark and exit silently
if tool_name == TRANSITIONS_TOOL:
    state["transitions_fetched"] = True
    save_state(state)
    sys.exit(0)

warnings = []

# H3: Any other Atlassian tool requires bootstrap first
if not state["bootstrapped"]:
    warnings.append(BOOTSTRAP_WARNING)

# H4: transitionJiraIssue requires getTransitionsForJiraIssue first
if tool_name == TRANSITION_ISSUE_TOOL and not state["transitions_fetched"]:
    issue_key = tool_input.get("issueIdOrKey", "<issueIdOrKey>")
    warnings.append(TRANSITIONS_WARNING.format(key=issue_key))

# M5: ADF body must be a JSON string, not a raw Python dict
if tool_name in CONFLUENCE_WRITE_TOOLS:
    content_format = tool_input.get("contentFormat", "")
    body = tool_input.get("body")
    if content_format == "adf" and isinstance(body, dict):
        warnings.append(ADF_WARNING)

for warning in warnings:
    print(warning, file=sys.stderr)

sys.exit(0)
