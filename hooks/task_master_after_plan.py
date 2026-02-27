#!/usr/bin/env python3
"""
PostToolUse hook: After exiting plan mode, remind Claude to delegate via task-master.

Matcher: ExitPlanMode
Fires once per plan exit. Reminds the orchestrator (Opus) to decompose work
and delegate to agents (sonnet) via the Task tool instead of implementing directly.
Exit code 0 = soft warning via stderr.
"""
import json
import sys

REMINDER = """STOP. You are the Orchestrator. You plan and delegate. You do NOT implement directly.

Before writing any code, invoke /task-master to decompose this plan into tasks:
  1. Break the plan into tasks (Epic > Story > Task)
  2. For each task: select model (default: sonnet), assign skills, delegate via Task tool
  3. Review agent output → integrate → report to user

Task tool delegation pattern:
  Task(subagent_type="general-purpose", model="sonnet", prompt="[task + skills + context]")

Do NOT skip delegation. The plan is ready — now delegate the work to agents.
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
