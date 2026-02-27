#!/usr/bin/env python3
"""
UserPromptSubmit hook: Remind Claude to use Sequential Thinking for complex reasoning tasks.

Sequential Thinking prevents costly back-and-forth by structuring reasoning upfront.
Fires when the prompt contains debugging, analysis, architecture, or trade-off language.

Fires once per session — it's a setup reminder, not a per-action nudge.
Exit code 0 = soft warning via stderr.
"""
import json
import os
import re
import sys
import time

STATE_FILE = os.path.expanduser("~/.claude/.sequential_reminded")
STALENESS_SECONDS = 3600

INVESTIGATION_SIGNALS = re.compile(
    r"\b(debug|diagnos|investigat|figure out|why (is|does|isn't|doesn't|won't)|"
    r"not working|broken|fail|error|exception|unexpected|strange|weird|"
    r"trace|root cause|hunt down|track down)\b",
    re.IGNORECASE,
)

ANALYSIS_SIGNALS = re.compile(
    r"\b(analyz|trade.?off|compare|evaluate|weigh|pros.?and.?cons|"
    r"best (way|approach|option|pattern)|should (we|I)|"
    r"architect|design|plan|how (should|would|do) (we|I))\b",
    re.IGNORECASE,
)

REMINDER = """Complex reasoning detected — Sequential Thinking structures the analysis before acting:
  mcp__sequential-thinking__sequentialthinking
      thought: "Step 1: ..."  thoughtNumber: 1  totalThoughts: 5  nextThoughtNeeded: true
Useful for: debugging root causes, evaluating trade-offs, architecture decisions,
multi-step investigations where the approach may need to change mid-stream.
Prevents expensive trial-and-error by thinking it through first."""


def is_reminded() -> bool:
    if not os.path.exists(STATE_FILE):
        return False
    try:
        mtime = os.path.getmtime(STATE_FILE)
        return (time.time() - mtime) < STALENESS_SECONDS
    except OSError:
        return False


def mark_reminded() -> None:
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(str(time.time()))


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

prompt = input_data.get("user_prompt", "").strip()
if not prompt or len(prompt.split()) < 10:
    sys.exit(0)

if prompt.startswith("/"):
    sys.exit(0)

if is_reminded():
    sys.exit(0)

has_investigation = INVESTIGATION_SIGNALS.search(prompt)
has_analysis = ANALYSIS_SIGNALS.search(prompt)

if not (has_investigation or has_analysis):
    sys.exit(0)

mark_reminded()
print(REMINDER, file=sys.stderr)
sys.exit(0)
