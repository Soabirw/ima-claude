#!/usr/bin/env python3
"""
PreToolUse hook: Ensure Serena is using the right project, especially in WP plugin subdirs.

Problem: Serena uses --project-from-cwd, so when Claude Code runs from a plugin
subdirectory (wp-content/plugins/my-plugin/), Serena can't find the .serena/ config
at the WordPress root. PHPStorm has the parent WP project open, not the plugin.

Fix: When any mcp__serena__jet_brains_* tool is called, check if we're inside a
wp-content/plugins/ or wp-content/themes/ path. If so, remind Claude that the
Serena project is the parent WordPress root and may need explicit activation.

Also tracks whether Serena has been used this session. If not, and Claude is doing
code navigation via Grep with symbol-like patterns, nudges toward Serena.

Exit code 0 = soft warning via stderr.
"""
import json
import os
import sys
import time

STATE_FILE = os.path.expanduser("~/.claude/.serena_session_state")
STALENESS_SECONDS = 3600


def get_state():
    """Read session state."""
    if not os.path.exists(STATE_FILE):
        return {"activated": False, "warned_wp": False, "timestamp": 0}
    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
        if time.time() - state.get("timestamp", 0) > STALENESS_SECONDS:
            return {"activated": False, "warned_wp": False, "timestamp": 0}
        return state
    except (json.JSONDecodeError, OSError):
        return {"activated": False, "warned_wp": False, "timestamp": 0}


def save_state(state):
    """Write session state."""
    state["timestamp"] = time.time()
    state_dir = os.path.dirname(STATE_FILE)
    os.makedirs(state_dir, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def find_wp_root(cwd):
    """Walk up from cwd to find a WordPress root (contains wp-content/)."""
    path = cwd
    for _ in range(10):  # max 10 levels up
        if os.path.isdir(os.path.join(path, "wp-content")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    return None


def find_serena_project(cwd):
    """Walk up from cwd to find nearest .serena/project.yml."""
    path = cwd
    for _ in range(10):
        project_yml = os.path.join(path, ".serena", "project.yml")
        if os.path.exists(project_yml):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    return None


def get_project_name(serena_root):
    """Extract project_name from .serena/project.yml."""
    try:
        project_yml = os.path.join(serena_root, ".serena", "project.yml")
        with open(project_yml, "r") as f:
            for line in f:
                if line.strip().startswith("project_name:"):
                    name = line.split(":", 1)[1].strip().strip('"').strip("'")
                    if name:
                        return name
    except OSError:
        pass
    return None


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
state = get_state()
cwd = os.getcwd()

# Track Serena usage
if tool_name.startswith("mcp__serena__"):
    state["activated"] = True
    save_state(state)

# Check 1: WP plugin subdirectory detection for Serena JetBrains tools
if tool_name.startswith("mcp__serena__jet_brains_") and not state.get("warned_wp"):
    # Are we in a wp-content subdirectory?
    in_wp_subdir = "wp-content/plugins/" in cwd or "wp-content/themes/" in cwd

    if in_wp_subdir:
        wp_root = find_wp_root(cwd)
        serena_root = find_serena_project(cwd)

        if serena_root and serena_root != cwd:
            project_name = get_project_name(serena_root)
            msg = (
                f"Serena project is at the WordPress root, not this plugin directory.\n"
                f"  Project root: {serena_root}\n"
            )
            if project_name:
                msg += f"  Project name: {project_name}\n"
            msg += (
                f"  Current dir:  {cwd}\n"
                f"  If Serena tools fail, activate the project explicitly:\n"
                f"    mcp__serena__check_onboarding_performed\n"
                f"  Use relative_path from the WP root, not the plugin directory."
            )
            print(msg, file=sys.stderr)
            state["warned_wp"] = True
            save_state(state)

sys.exit(0)
