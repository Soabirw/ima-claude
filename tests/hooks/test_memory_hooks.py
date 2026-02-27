"""
Tests for memory-related hooks:
  - memory_bootstrap.py
  - vestige_before_external.py
  - memory_store_reminder.py
"""
import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).parent.parent.parent / "plugins" / "ima-claude" / "hooks"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_memory_bootstrap(input_data: dict, fake_home: Path) -> subprocess.CompletedProcess:
    """Run memory_bootstrap.py with HOME redirected so state files go to a temp dir."""
    (fake_home / ".claude").mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "HOME": str(fake_home)}
    return subprocess.run(
        ["python3", str(HOOKS_DIR / "memory_bootstrap.py")],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        env=env,
    )


def run_vestige_external(input_data: dict, fake_home: Path) -> subprocess.CompletedProcess:
    """Run vestige_before_external.py with HOME redirected."""
    (fake_home / ".claude").mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "HOME": str(fake_home)}
    return subprocess.run(
        ["python3", str(HOOKS_DIR / "vestige_before_external.py")],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        env=env,
    )


def run_store_reminder(input_data: dict, fake_home: Path) -> subprocess.CompletedProcess:
    """Run memory_store_reminder.py with HOME redirected."""
    (fake_home / ".claude").mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "HOME": str(fake_home)}
    return subprocess.run(
        ["python3", str(HOOKS_DIR / "memory_store_reminder.py")],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        env=env,
    )


# ---------------------------------------------------------------------------
# memory_bootstrap.py
# ---------------------------------------------------------------------------

class TestMemoryBootstrap:

    def test_fires_on_first_non_memory_tool(self, tmp_path):
        """First non-memory tool use should print the reminder to stderr."""
        result = run_memory_bootstrap({"tool_name": "Bash"}, tmp_path)
        assert result.returncode == 0
        assert "Memory bootstrap" in result.stderr
        assert "mcp__vestige__search" in result.stderr

    def test_silent_for_memory_tool(self, tmp_path):
        """Vestige search tool should mark bootstrapped without printing anything."""
        result = run_memory_bootstrap({"tool_name": "mcp__vestige__search"}, tmp_path)
        assert result.returncode == 0
        assert result.stderr == ""

    def test_silent_after_memory_tool_marks_bootstrapped(self, tmp_path):
        """After a memory tool marks state, the next non-memory tool is silent."""
        # First: memory tool marks bootstrapped
        run_memory_bootstrap({"tool_name": "mcp__vestige__search"}, tmp_path)
        # Second: non-memory tool should be silent because state file is fresh
        result = run_memory_bootstrap({"tool_name": "Bash"}, tmp_path)
        assert result.returncode == 0
        assert result.stderr == ""

    def test_idempotent_after_first_fire(self, tmp_path):
        """After the reminder fires once, subsequent non-memory tools are silent."""
        # First call: fires reminder
        first = run_memory_bootstrap({"tool_name": "Edit"}, tmp_path)
        assert "Memory bootstrap" in first.stderr
        # Second call: should be silent
        second = run_memory_bootstrap({"tool_name": "Read"}, tmp_path)
        assert second.returncode == 0
        assert second.stderr == ""

    def test_all_memory_tools_are_silent(self, tmp_path):
        """Every tool in MEMORY_TOOLS should be silent (they mark bootstrapped)."""
        memory_tools = [
            "mcp__vestige__search",
            "mcp__vestige__smart_ingest",
            "mcp__vestige__ingest",
            "mcp__vestige__memory",
            "mcp__vestige__intention",
            "mcp__vestige__codebase",
            "mcp__qdrant-memory__qdrant-find",
            "mcp__qdrant-memory__qdrant-store",
            "mcp__serena__read_memory",
            "mcp__serena__list_memories",
            "mcp__serena__write_memory",
        ]
        for tool in memory_tools:
            local_tmp = tmp_path / tool.replace(":", "_").replace("_", "-")
            local_tmp.mkdir(parents=True, exist_ok=True)
            result = run_memory_bootstrap({"tool_name": tool}, local_tmp)
            assert result.returncode == 0, f"Non-zero exit for {tool}"
            assert result.stderr == "", f"Unexpected stderr for {tool}: {result.stderr!r}"

    def test_invalid_json_exits_silently(self, tmp_path):
        """Malformed JSON input should cause silent exit."""
        (tmp_path / ".claude").mkdir(parents=True, exist_ok=True)
        env = {**os.environ, "HOME": str(tmp_path)}
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "memory_bootstrap.py")],
            input="not json",
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_missing_tool_name_fires_reminder(self, tmp_path):
        """Input with no tool_name defaults to empty string (non-memory) — reminder fires."""
        result = run_memory_bootstrap({}, tmp_path)
        assert result.returncode == 0
        assert "Memory bootstrap" in result.stderr


# ---------------------------------------------------------------------------
# vestige_before_external.py
# ---------------------------------------------------------------------------

class TestVestigeBeforeExternal:

    def test_fires_on_context7_without_prior_vestige_search(self, tmp_path):
        """Context7 call without prior Vestige search should trigger the reminder."""
        result = run_vestige_external(
            {"tool_name": "mcp__context7__query-docs", "tool_input": {"query": "React hooks"}},
            tmp_path,
        )
        assert result.returncode == 0
        assert "No Vestige search detected" in result.stderr
        assert "mcp__vestige__search" in result.stderr

    def test_fires_on_tavily_without_prior_vestige_search(self, tmp_path):
        """Tavily call without prior Vestige search should trigger the reminder."""
        result = run_vestige_external(
            {"tool_name": "mcp__tavily__tavily_search", "tool_input": {"query": "pytest fixtures"}},
            tmp_path,
        )
        assert result.returncode == 0
        assert "No Vestige search detected" in result.stderr

    def test_silent_after_vestige_search_marks_state(self, tmp_path):
        """After a Vestige search marks state, Context7 calls should be silent."""
        # Mark as searched
        run_vestige_external({"tool_name": "mcp__vestige__search", "tool_input": {}}, tmp_path)
        # Now Context7 should be silent
        result = run_vestige_external(
            {"tool_name": "mcp__context7__query-docs", "tool_input": {"query": "something"}},
            tmp_path,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_silent_on_irrelevant_tool(self, tmp_path):
        """Tools that are neither Vestige nor Context7/Tavily should be ignored."""
        result = run_vestige_external({"tool_name": "Bash", "tool_input": {}}, tmp_path)
        assert result.returncode == 0
        assert result.stderr == ""

    def test_vestige_search_itself_is_silent(self, tmp_path):
        """mcp__vestige__search should mark state and produce no output."""
        result = run_vestige_external(
            {"tool_name": "mcp__vestige__search", "tool_input": {"query": "test"}},
            tmp_path,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_fires_only_once_per_session(self, tmp_path):
        """After the reminder fires once, subsequent Context7 calls are silent."""
        # First Tavily call — fires
        first = run_vestige_external(
            {"tool_name": "mcp__tavily__tavily_search", "tool_input": {"query": "something"}},
            tmp_path,
        )
        assert "No Vestige search detected" in first.stderr
        # Second call — should be silent (state is now "warned")
        second = run_vestige_external(
            {"tool_name": "mcp__context7__query-docs", "tool_input": {"query": "other"}},
            tmp_path,
        )
        assert second.returncode == 0
        assert second.stderr == ""

    def test_topic_hint_from_query(self, tmp_path):
        """The reminder should include the query string as a topic hint."""
        result = run_vestige_external(
            {"tool_name": "mcp__tavily__tavily_search", "tool_input": {"query": "pytest best practices"}},
            tmp_path,
        )
        assert "pytest best practices" in result.stderr

    def test_topic_hint_from_library_name(self, tmp_path):
        """The reminder should use libraryName when query is absent."""
        result = run_vestige_external(
            {"tool_name": "mcp__context7__resolve-library-id", "tool_input": {"libraryName": "React"}},
            tmp_path,
        )
        assert "React" in result.stderr

    def test_topic_hint_fallback(self, tmp_path):
        """With no query/libraryName/url in tool_input, the hint defaults to <topic>."""
        result = run_vestige_external(
            {"tool_name": "mcp__tavily__tavily_search", "tool_input": {}},
            tmp_path,
        )
        assert "<topic>" in result.stderr

    def test_invalid_json_exits_silently(self, tmp_path):
        """Malformed JSON input should cause silent exit."""
        (tmp_path / ".claude").mkdir(parents=True, exist_ok=True)
        env = {**os.environ, "HOME": str(tmp_path)}
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "vestige_before_external.py")],
            input="not json",
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0
        assert result.stderr == ""


# ---------------------------------------------------------------------------
# memory_store_reminder.py
# ---------------------------------------------------------------------------

class TestMemoryStoreReminder:

    def _simulate_n_edits(self, n: int, fake_home: Path) -> list[subprocess.CompletedProcess]:
        """Run n Edit tool events and return all results."""
        return [
            run_store_reminder({"tool_name": "Edit"}, fake_home)
            for _ in range(n)
        ]

    def test_fires_on_fifth_edit(self, tmp_path):
        """After 5 consecutive edits without memory store, reminder should fire."""
        results = self._simulate_n_edits(5, tmp_path)
        assert results[4].returncode == 0
        assert "several changes" in results[4].stderr

    def test_silent_before_threshold(self, tmp_path):
        """Fewer than 5 edits should not trigger the reminder."""
        results = self._simulate_n_edits(4, tmp_path)
        for r in results:
            assert r.stderr == "", f"Unexpected output at count <5: {r.stderr!r}"

    def test_counter_resets_after_reminder(self, tmp_path):
        """After the reminder fires, next 4 edits should be silent again."""
        self._simulate_n_edits(5, tmp_path)  # fires and resets
        results = self._simulate_n_edits(4, tmp_path)
        for r in results:
            assert r.stderr == "", f"Counter should have reset: {r.stderr!r}"

    def test_counter_resets_on_memory_store(self, tmp_path):
        """A memory store tool should reset the counter; next 4 edits stay silent."""
        self._simulate_n_edits(4, tmp_path)  # count = 4
        run_store_reminder({"tool_name": "mcp__vestige__smart_ingest"}, tmp_path)  # resets
        results = self._simulate_n_edits(4, tmp_path)
        for r in results:
            assert r.stderr == "", f"Expected silence after reset: {r.stderr!r}"

    def test_memory_store_tool_is_silent(self, tmp_path):
        """Memory store tools should always be silent."""
        store_tools = [
            "mcp__vestige__smart_ingest",
            "mcp__vestige__ingest",
            "mcp__vestige__codebase",
            "mcp__vestige__session_checkpoint",
            "mcp__qdrant-memory__qdrant-store",
            "mcp__serena__write_memory",
        ]
        for tool in store_tools:
            result = run_store_reminder({"tool_name": tool}, tmp_path)
            assert result.returncode == 0
            assert result.stderr == "", f"Unexpected stderr for {tool}: {result.stderr!r}"

    def test_write_tool_counts_like_edit(self, tmp_path):
        """Write tool should also count toward the edit threshold."""
        # 4 Edits then 1 Write = 5 total — should fire
        for _ in range(4):
            run_store_reminder({"tool_name": "Edit"}, tmp_path)
        result = run_store_reminder({"tool_name": "Write"}, tmp_path)
        assert result.returncode == 0
        assert "several changes" in result.stderr

    def test_irrelevant_tool_is_silent(self, tmp_path):
        """Tools that are not Edit/Write/memory-store should be ignored silently."""
        result = run_store_reminder({"tool_name": "Bash"}, tmp_path)
        assert result.returncode == 0
        assert result.stderr == ""

    def test_irrelevant_tool_does_not_increment_counter(self, tmp_path):
        """Irrelevant tools should not affect the edit counter."""
        for _ in range(4):
            run_store_reminder({"tool_name": "Edit"}, tmp_path)
        # A Bash call sandwiched in — should not push to threshold
        run_store_reminder({"tool_name": "Bash"}, tmp_path)
        # Still at 4 — next Edit brings to 5 and fires
        result = run_store_reminder({"tool_name": "Edit"}, tmp_path)
        assert "several changes" in result.stderr

    def test_reminder_contains_vestige_and_qdrant(self, tmp_path):
        """The reminder text should mention both Vestige and Qdrant."""
        self._simulate_n_edits(5, tmp_path)
        # Re-run after reset to get a fresh reminder on next cycle
        results = self._simulate_n_edits(5, tmp_path)
        assert "Vestige" in results[4].stderr
        assert "Qdrant" in results[4].stderr

    def test_invalid_json_exits_silently(self, tmp_path):
        """Malformed JSON input should cause silent exit."""
        (tmp_path / ".claude").mkdir(parents=True, exist_ok=True)
        env = {**os.environ, "HOME": str(tmp_path)}
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / "memory_store_reminder.py")],
            input="not json",
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 0
        assert result.stderr == ""
