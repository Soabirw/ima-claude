#!/usr/bin/env python3
"""
Standalone debug logger for ima-claude hooks.

Only active when the environment variable CLAUDE_HOOK_DEBUG=1 is set.
When the variable is absent or set to anything else, log_hook() is a no-op —
zero overhead in normal operation.

Usage
-----
Add to any hook script to gain a persistent audit trail:

    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from hook_logger import log_hook

    # When the hook fires:
    log_hook("my_hook_name", triggered=True, reason="why it fired")

    # On skip paths:
    log_hook("my_hook_name", triggered=False, reason="why it was skipped")

Enable logging before launching Claude Code:

    export CLAUDE_HOOK_DEBUG=1
    claude

Watch the log in real time:

    tail -f ~/.claude/hook-activity.log

Log format:

    2026-02-27 14:23:01 | enforce_rg_over_grep | TRIGGERED | grep found in command
    2026-02-27 14:23:05 | serena_over_read     | SKIPPED   | non-code file extension

This file does NOT modify any existing hook scripts. It is imported on demand only.
"""
import datetime
import os


LOG_FILE = os.path.expanduser("~/.claude/hook-activity.log")
_DEBUG_ENABLED = os.environ.get("CLAUDE_HOOK_DEBUG", "").strip() == "1"


def log_hook(hook_name: str, triggered: bool, reason: str = "") -> None:
    """Write a timestamped entry to the hook activity log.

    Args:
        hook_name: Short name identifying the hook (e.g. "enforce_rg_over_grep").
        triggered: True if the hook emitted a warning/action; False if it skipped.
        reason:    Human-readable explanation for the outcome.
    """
    if not _DEBUG_ENABLED:
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "TRIGGERED" if triggered else "SKIPPED"
    entry = f"{timestamp} | {hook_name:<24} | {status:<9} | {reason}\n"

    try:
        log_dir = os.path.dirname(LOG_FILE)
        os.makedirs(log_dir, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
    except OSError:
        # Never let logging errors propagate into a hook and alter its exit code.
        pass
