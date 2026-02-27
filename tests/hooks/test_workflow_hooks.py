"""
Tests for workflow-related hooks:
  - task_master_before_impl.py
  - task_master_after_plan.py
  - sequential_thinking_check.py
  - prompt_coach.py
"""
import json
import os
import subprocess
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).parent.parent.parent / "plugins" / "ima-claude" / "hooks"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_hook_with_home(hook_filename: str, input_data: dict, fake_home: Path) -> subprocess.CompletedProcess:
    """Run a hook with HOME redirected so state files land in a temp directory."""
    (fake_home / ".claude").mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "HOME": str(fake_home)}
    return subprocess.run(
        ["python3", str(HOOKS_DIR / hook_filename)],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        env=env,
    )


def run_hook_plain(hook_filename: str, input_data: dict) -> subprocess.CompletedProcess:
    """Run a hook without HOME override (for stateless hooks)."""
    return subprocess.run(
        ["python3", str(HOOKS_DIR / hook_filename)],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
    )


# A long prompt (>30 words) with both an action verb and a scope noun.
TRIGGERING_IMPL_PROMPT = (
    "Please implement a new authentication feature for the user dashboard. "
    "This should include OAuth2 integration, session management, and role-based access control. "
    "The feature needs to work across both the web and mobile interfaces."
)

# A long prompt (>10 words) with investigation/analysis language.
TRIGGERING_SEQ_PROMPT = (
    "Can you help me debug why the authentication middleware is not working correctly? "
    "I need to figure out the root cause of the issue before we proceed."
)


# ---------------------------------------------------------------------------
# task_master_before_impl.py
# ---------------------------------------------------------------------------

class TestTaskMasterBeforeImpl:

    def test_fires_on_non_trivial_implementation_prompt(self, tmp_path):
        """A long prompt with action verb + scope noun should trigger the reminder."""
        result = run_hook_with_home("task_master_before_impl.py", {"user_prompt": TRIGGERING_IMPL_PROMPT}, tmp_path)
        assert result.returncode == 0
        assert "task-planner" in result.stderr

    def test_silent_for_short_prompt(self, tmp_path):
        """Prompts with 30 words or fewer should not fire."""
        short = "Implement a small feature for the system module."
        result = run_hook_with_home("task_master_before_impl.py", {"user_prompt": short}, tmp_path)
        assert result.returncode == 0
        assert result.stderr == ""

    def test_silent_when_trivial_signal_present(self, tmp_path):
        """Prompts containing trivial-signal words (simple, quick, just) should not fire."""
        trivial = (
            "Just implement a simple endpoint for the API service. "
            "This is a quick change and should not take long to build out "
            "since we already have most of the component infrastructure ready to go."
        )
        result = run_hook_with_home("task_master_before_impl.py", {"user_prompt": trivial}, tmp_path)
        assert result.returncode == 0
        assert result.stderr == ""

    def test_silent_for_skill_invocation(self, tmp_path):
        """Prompts starting with '/' are skill invocations and should be skipped."""
        result = run_hook_with_home(
            "task_master_before_impl.py",
            {"user_prompt": "/ima-claude:task-planner implement the authentication feature system module integration"},
            tmp_path,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_silent_when_no_action_verb(self, tmp_path):
        """Prompt with scope noun but no action verb should not fire."""
        no_verb = (
            "The authentication system component is causing problems in the endpoint "
            "integration workflow dashboard. We need to understand what the service "
            "does and how the module interacts with the existing codebase and plugin."
        )
        result = run_hook_with_home("task_master_before_impl.py", {"user_prompt": no_verb}, tmp_path)
        assert result.returncode == 0
        assert result.stderr == ""

    def test_silent_when_no_scope_noun(self, tmp_path):
        """Prompt with action verb but no scope noun should not fire."""
        no_noun = (
            "Please implement the changes we discussed earlier and make sure everything "
            "is working correctly. Build it the same way we did last time and add the "
            "necessary tests to verify the behavior works as expected in all cases."
        )
        result = run_hook_with_home("task_master_before_impl.py", {"user_prompt": no_noun}, tmp_path)
        assert result.returncode == 0
        assert result.stderr == ""

    def test_fires_only_once_per_session(self, tmp_path):
        """After the reminder fires, subsequent matching prompts should be silent."""
        first = run_hook_with_home("task_master_before_impl.py", {"user_prompt": TRIGGERING_IMPL_PROMPT}, tmp_path)
        assert "task-planner" in first.stderr
        second = run_hook_with_home("task_master_before_impl.py", {"user_prompt": TRIGGERING_IMPL_PROMPT}, tmp_path)
        assert second.returncode == 0
        assert second.stderr == ""

    def test_empty_prompt_is_silent(self, tmp_path):
        """Empty user_prompt should exit silently."""
        result = run_hook_with_home("task_master_before_impl.py", {"user_prompt": ""}, tmp_path)
        assert result.returncode == 0
        assert result.stderr == ""

    def test_invalid_json_exits_silently(self, tmp_path):
        """Malformed JSON input should cause silent exit."""
        (tmp_path / ".claude").mkdir(parents=True, exist_ok=True)
        env = {**os.environ, "HOME": str(tmp_path)}
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "task_master_before_impl.py")],
            input="not json",
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_reminder_text_mentions_task_runner(self, tmp_path):
        """The reminder should reference task-runner and Orchestrator/agents."""
        result = run_hook_with_home("task_master_before_impl.py", {"user_prompt": TRIGGERING_IMPL_PROMPT}, tmp_path)
        assert "task-runner" in result.stderr
        assert "Orchestrator" in result.stderr or "agents" in result.stderr


# ---------------------------------------------------------------------------
# task_master_after_plan.py  (stateless — fires on ExitPlanMode)
# ---------------------------------------------------------------------------

class TestTaskMasterAfterPlan:

    def test_fires_on_exit_plan_mode(self):
        """ExitPlanMode tool_name should always trigger the delegate reminder."""
        result = run_hook_plain("task_master_after_plan.py", {"tool_name": "ExitPlanMode"})
        assert result.returncode == 0
        assert "STOP" in result.stderr
        assert "task-runner" in result.stderr

    def test_fires_repeatedly(self):
        """Unlike session-based hooks this one fires every time ExitPlanMode is seen."""
        for _ in range(3):
            result = run_hook_plain("task_master_after_plan.py", {"tool_name": "ExitPlanMode"})
            assert "STOP" in result.stderr

    def test_silent_for_non_exit_plan_mode_tool(self):
        """Any tool other than ExitPlanMode should produce no output."""
        for tool in ("Bash", "Edit", "Write", "Read", "mcp__vestige__search"):
            result = run_hook_plain("task_master_after_plan.py", {"tool_name": tool})
            assert result.returncode == 0, f"Non-zero exit for {tool}"
            assert result.stderr == "", f"Unexpected stderr for {tool}: {result.stderr!r}"

    def test_silent_for_empty_tool_name(self):
        """Missing tool_name defaults to empty string — should be silent."""
        result = run_hook_plain("task_master_after_plan.py", {})
        assert result.returncode == 0
        assert result.stderr == ""

    def test_invalid_json_exits_silently(self):
        """Malformed JSON input should cause silent exit."""
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "task_master_after_plan.py")],
            input="not json",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_reminder_mentions_delegate_and_agents(self):
        """The reminder should emphasize delegation over direct implementation."""
        result = run_hook_plain("task_master_after_plan.py", {"tool_name": "ExitPlanMode"})
        assert "DELEGATE" in result.stderr
        assert "Orchestrator" in result.stderr


# ---------------------------------------------------------------------------
# sequential_thinking_check.py
# ---------------------------------------------------------------------------

class TestSequentialThinkingCheck:

    def test_fires_on_investigation_prompt(self, tmp_path):
        """A prompt containing debugging language should trigger the reminder."""
        result = run_hook_with_home(
            "sequential_thinking_check.py",
            {"user_prompt": TRIGGERING_SEQ_PROMPT},
            tmp_path,
        )
        assert result.returncode == 0
        assert "Sequential Thinking" in result.stderr

    def test_fires_on_analysis_prompt(self, tmp_path):
        """A prompt with trade-off / architecture language should trigger the reminder."""
        analysis_prompt = (
            "Can you help me analyze the trade-offs between using Redux and Zustand "
            "for our state management architecture? I want to evaluate the best approach "
            "for our use case and understand the pros and cons of each option."
        )
        result = run_hook_with_home(
            "sequential_thinking_check.py",
            {"user_prompt": analysis_prompt},
            tmp_path,
        )
        assert result.returncode == 0
        assert "Sequential Thinking" in result.stderr

    def test_fires_on_root_cause_language(self, tmp_path):
        """Prompts mentioning 'root cause' should fire."""
        prompt = (
            "I need you to find the root cause of this unexpected exception that keeps "
            "appearing in production. The error trace shows something weird happening in "
            "the middleware layer that doesn't make sense to me."
        )
        result = run_hook_with_home("sequential_thinking_check.py", {"user_prompt": prompt}, tmp_path)
        assert "Sequential Thinking" in result.stderr

    def test_silent_for_short_prompt(self, tmp_path):
        """Prompts with fewer than 10 words should not fire."""
        result = run_hook_with_home(
            "sequential_thinking_check.py",
            {"user_prompt": "debug this error"},
            tmp_path,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_silent_for_skill_invocation(self, tmp_path):
        """Prompts starting with '/' should be skipped."""
        result = run_hook_with_home(
            "sequential_thinking_check.py",
            {"user_prompt": "/ima-claude:architect analyze the trade-offs and debug the system architecture"},
            tmp_path,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_silent_for_plain_implementation_prompt(self, tmp_path):
        """A prompt with no investigation or analysis signals should not fire."""
        plain = (
            "Please update the button color on the homepage from blue to green and "
            "make sure the hover state also changes to match the new color scheme."
        )
        result = run_hook_with_home("sequential_thinking_check.py", {"user_prompt": plain}, tmp_path)
        assert result.returncode == 0
        assert result.stderr == ""

    def test_fires_only_once_per_session(self, tmp_path):
        """After the reminder fires, subsequent matching prompts should be silent."""
        first = run_hook_with_home(
            "sequential_thinking_check.py", {"user_prompt": TRIGGERING_SEQ_PROMPT}, tmp_path
        )
        assert "Sequential Thinking" in first.stderr
        second = run_hook_with_home(
            "sequential_thinking_check.py", {"user_prompt": TRIGGERING_SEQ_PROMPT}, tmp_path
        )
        assert second.returncode == 0
        assert second.stderr == ""

    def test_reminder_contains_tool_name(self, tmp_path):
        """The reminder should mention the sequentialthinking tool."""
        result = run_hook_with_home(
            "sequential_thinking_check.py", {"user_prompt": TRIGGERING_SEQ_PROMPT}, tmp_path
        )
        assert "sequentialthinking" in result.stderr

    def test_invalid_json_exits_silently(self, tmp_path):
        """Malformed JSON input should cause silent exit."""
        (tmp_path / ".claude").mkdir(parents=True, exist_ok=True)
        env = {**os.environ, "HOME": str(tmp_path)}
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "sequential_thinking_check.py")],
            input="not json",
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0
        assert result.stderr == ""


# ---------------------------------------------------------------------------
# prompt_coach.py
# ---------------------------------------------------------------------------

class TestPromptCoach:
    """
    prompt_coach.py gates entirely on PROMPT_COACH_ENABLED=true.
    Without that env var it exits silently, which is the safe default.
    These tests verify the disabled path and the skip-pattern logic
    without requiring a live Anthropic API key.
    """

    def _run_coach(self, input_data: dict, extra_env: dict | None = None) -> subprocess.CompletedProcess:
        env = {**os.environ, **(extra_env or {})}
        return subprocess.run(
            ["python3", str(HOOKS_DIR / "prompt_coach.py")],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            env=env,
        )

    def test_silent_when_disabled(self):
        """Without PROMPT_COACH_ENABLED the hook should exit silently."""
        env = {k: v for k, v in os.environ.items() if k != "PROMPT_COACH_ENABLED"}
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "prompt_coach.py")],
            input=json.dumps({"prompt": "How do I implement a caching layer for the API service?"}),
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_silent_when_explicitly_disabled(self):
        """PROMPT_COACH_ENABLED=false should also cause silent exit."""
        result = self._run_coach(
            {"prompt": "How do I implement a caching layer for the API service?"},
            {"PROMPT_COACH_ENABLED": "false"},
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_exits_silently_without_api_key_when_enabled(self, tmp_path):
        """When enabled but no config file exists, the hook should fail silently."""
        # Point HOME to a temp dir with no prompt_coach_config.json
        (tmp_path / ".claude" / "hooks").mkdir(parents=True, exist_ok=True)
        env = {
            **os.environ,
            "HOME": str(tmp_path),
            "PROMPT_COACH_ENABLED": "true",
        }
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "prompt_coach.py")],
            input=json.dumps({"prompt": "How do I implement a caching layer for the API service endpoint?"}),
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0
        # Should fail silently — no stderr output to user
        assert result.stderr == ""

    def test_invalid_json_exits_silently(self):
        """Malformed JSON should cause silent exit regardless of PROMPT_COACH_ENABLED."""
        result = self._run_coach({}, {"PROMPT_COACH_ENABLED": "true"})
        # Empty dict has no "prompt" key — treated as empty prompt, skipped
        assert result.returncode == 0

    def test_short_prompt_is_skipped_silently(self):
        """Prompts shorter than 20 chars should be skipped without output."""
        # Even with ENABLED=true, short prompts skip immediately
        result = self._run_coach(
            {"prompt": "ok"},
            {"PROMPT_COACH_ENABLED": "false"},
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_common_followup_words_are_skipped(self):
        """Common follow-up phrases in SKIP_PATTERNS should never invoke the API."""
        skip_prompts = ["yes", "no", "ok", "proceed", "continue", "go ahead", "looks good"]
        for phrase in skip_prompts:
            result = self._run_coach(
                {"prompt": phrase},
                {"PROMPT_COACH_ENABLED": "false"},
            )
            assert result.returncode == 0, f"Non-zero exit for '{phrase}'"
            assert result.stderr == "", f"Unexpected output for '{phrase}': {result.stderr!r}"

    def test_missing_prompt_key_is_silent(self):
        """Input with no 'prompt' key should exit silently."""
        result = self._run_coach({"user_prompt": "some text"}, {"PROMPT_COACH_ENABLED": "false"})
        assert result.returncode == 0
        assert result.stderr == ""
