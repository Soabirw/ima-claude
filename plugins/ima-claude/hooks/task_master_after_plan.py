#!/usr/bin/env python3
"""
PostToolUse hook: After exiting plan mode, direct Claude to delegate tasks to agents.

Matcher: ExitPlanMode
Fires once per plan exit. The plan is already done — this hook pushes Claude
to delegate each task to subagents via the Task tool instead of implementing directly.
Does NOT re-invoke task-master (that would restart planning).
Exit code 0 = soft warning via stderr.
"""
import json
import sys

REMINDER = """STOP. The plan is approved. Do NOT implement directly — DELEGATE.

Invoke /ima-claude:task-runner now to delegate each task to subagents.
You are the Orchestrator. You coordinate. Agents implement. Do NOT write code yourself.
"""

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")

if tool_name != "ExitPlanMode":
    sys.exit(0)

print(REMINDER, file=sys.stderr)
sys.exit(0)
