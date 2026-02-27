"""
Tests for tool-redirect PreToolUse hooks.

Each hook class covers:
  - should_fire: input that triggers a warning (stderr non-empty, exit 0)
  - should_not_fire: clean input, no warning (stderr empty, exit 0)
  - wrong_tool_name: hook silently exits 0 with no output
  - invalid_json: hook exits without crashing (exit 0 or 1, no raw traceback)

Notes on hook-specific quirks:
  - webfetch_to_tavily and websearch_to_tavily have no tool_name guard, so they
    always emit a warning regardless of tool_name. The wrong_tool_name cases for
    those hooks verify that the warning still contains the expected keyword.
  - serena_over_grep uses a file-backed counter and only fires on every 2nd
    symbol-like grep. Tests reset by deleting the state file between runs so the
    counter is always at 0 (fires on the even-indexed call).
  - serena_over_read stat()s the actual file to check size (>= 5 KB fires). Tests
    use a real temporary file large enough to trigger, and a small real file to
    suppress.
"""
import os
import subprocess
import tempfile

import pytest


# ---------------------------------------------------------------------------
# enforce_rg_over_grep
# ---------------------------------------------------------------------------

HOOK_RG = "enforce_rg_over_grep.py"


class TestEnforceRgOverGrep:
    def test_should_fire_grep(self, run_hook):
        result = run_hook(HOOK_RG, {
            "tool_name": "Bash",
            "tool_input": {"command": "grep -r 'foo' src/"},
        })
        assert result.returncode == 0
        assert "ripgrep" in result.stderr

    def test_should_fire_find_name(self, run_hook):
        result = run_hook(HOOK_RG, {
            "tool_name": "Bash",
            "tool_input": {"command": "find . -name '*.php'"},
        })
        assert result.returncode == 0
        assert "ripgrep" in result.stderr

    def test_should_not_fire_rg_command(self, run_hook):
        result = run_hook(HOOK_RG, {
            "tool_name": "Bash",
            "tool_input": {"command": "rg 'foo' src/"},
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_should_not_fire_no_command(self, run_hook):
        result = run_hook(HOOK_RG, {
            "tool_name": "Bash",
            "tool_input": {},
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_wrong_tool_name(self, run_hook):
        result = run_hook(HOOK_RG, {
            "tool_name": "Read",
            "tool_input": {"command": "grep -r 'foo' src/"},
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_invalid_json(self, run_hook):
        proc = subprocess.run(
            ["python3", str(
                __import__("pathlib").Path(__file__).parent.parent.parent
                / "plugins" / "ima-claude" / "hooks" / HOOK_RG
            )],
            input="not valid json {{{",
            capture_output=True,
            text=True,
        )
        # Must not crash with an unhandled Python traceback
        assert proc.returncode in (0, 1)
        assert "Traceback" not in proc.stderr


# ---------------------------------------------------------------------------
# serena_over_read
# ---------------------------------------------------------------------------

HOOK_SERENA_READ = "serena_over_read.py"


class TestSerenaOverRead:
    def test_should_fire_large_code_file(self, run_hook, tmp_path):
        # Create a real .py file >= 5 KB
        large_file = tmp_path / "big_module.py"
        large_file.write_text("x = 1\n" * 1000)  # ~7 KB
        assert large_file.stat().st_size >= 5000

        result = run_hook(HOOK_SERENA_READ, {
            "tool_name": "Read",
            "tool_input": {"file_path": str(large_file)},
        })
        assert result.returncode == 0
        assert "Serena" in result.stderr

    def test_should_not_fire_small_code_file(self, run_hook, tmp_path):
        # Create a real .py file < 5 KB
        small_file = tmp_path / "tiny.py"
        small_file.write_text("x = 1\n")
        assert small_file.stat().st_size < 5000

        result = run_hook(HOOK_SERENA_READ, {
            "tool_name": "Read",
            "tool_input": {"file_path": str(small_file)},
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_should_not_fire_markdown_file(self, run_hook, tmp_path):
        # Markdown is in SKIP_EXTENSIONS regardless of size
        md_file = tmp_path / "README.md"
        md_file.write_text("# Title\n" * 1000)

        result = run_hook(HOOK_SERENA_READ, {
            "tool_name": "Read",
            "tool_input": {"file_path": str(md_file)},
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_should_not_fire_json_file(self, run_hook, tmp_path):
        json_file = tmp_path / "config.json"
        json_file.write_text('{"key": "value"}\n' * 500)

        result = run_hook(HOOK_SERENA_READ, {
            "tool_name": "Read",
            "tool_input": {"file_path": str(json_file)},
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_wrong_tool_name(self, run_hook, tmp_path):
        large_file = tmp_path / "big.py"
        large_file.write_text("x = 1\n" * 1000)

        result = run_hook(HOOK_SERENA_READ, {
            "tool_name": "Bash",
            "tool_input": {"file_path": str(large_file)},
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_invalid_json(self):
        hook_path = (
            __import__("pathlib").Path(__file__).parent.parent.parent
            / "plugins" / "ima-claude" / "hooks" / HOOK_SERENA_READ
        )
        proc = subprocess.run(
            ["python3", str(hook_path)],
            input="{ bad json",
            capture_output=True,
            text=True,
        )
        # serena_over_read exits 0 on JSONDecodeError
        assert proc.returncode == 0
        assert "Traceback" not in proc.stderr


# ---------------------------------------------------------------------------
# serena_over_grep
# ---------------------------------------------------------------------------

HOOK_SERENA_GREP = "serena_over_grep.py"
STATE_FILE = os.path.expanduser("~/.claude/.serena_grep_count")


def _delete_serena_state():
    """Remove the counter file so the next call is index 0 (fires)."""
    try:
        os.remove(STATE_FILE)
    except FileNotFoundError:
        pass


class TestSerenaOverGrep:
    def test_should_fire_class_definition_pattern(self, run_hook):
        _delete_serena_state()
        result = run_hook(HOOK_SERENA_GREP, {
            "tool_name": "Grep",
            "tool_input": {
                "pattern": "class MyService",
                "path": "src/",
            },
        })
        assert result.returncode == 0
        assert "Serena" in result.stderr

    def test_should_fire_function_pattern(self, run_hook):
        _delete_serena_state()
        result = run_hook(HOOK_SERENA_GREP, {
            "tool_name": "Grep",
            "tool_input": {
                "pattern": "function doSomething",
                "path": "src/",
            },
        })
        assert result.returncode == 0
        assert "Serena" in result.stderr

    def test_should_not_fire_plain_text_pattern(self, run_hook):
        _delete_serena_state()
        result = run_hook(HOOK_SERENA_GREP, {
            "tool_name": "Grep",
            "tool_input": {
                "pattern": "TODO fixme",
                "path": "src/",
            },
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_should_not_fire_every_other_call(self, run_hook):
        # After one firing call (count=0 -> increments to 1), count%2 != 0, so no fire
        _delete_serena_state()
        # First call fires (count=0)
        run_hook(HOOK_SERENA_GREP, {
            "tool_name": "Grep",
            "tool_input": {"pattern": "class MyService"},
        })
        # Second call should not fire (count=1, 1%2 != 0)
        result = run_hook(HOOK_SERENA_GREP, {
            "tool_name": "Grep",
            "tool_input": {"pattern": "class MyService"},
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_wrong_tool_name(self, run_hook):
        _delete_serena_state()
        result = run_hook(HOOK_SERENA_GREP, {
            "tool_name": "Bash",
            "tool_input": {"pattern": "class MyService"},
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_invalid_json(self):
        hook_path = (
            __import__("pathlib").Path(__file__).parent.parent.parent
            / "plugins" / "ima-claude" / "hooks" / HOOK_SERENA_GREP
        )
        proc = subprocess.run(
            ["python3", str(hook_path)],
            input="not json at all",
            capture_output=True,
            text=True,
        )
        # serena_over_grep exits 0 on JSONDecodeError
        assert proc.returncode == 0
        assert "Traceback" not in proc.stderr


# ---------------------------------------------------------------------------
# webfetch_to_tavily
# ---------------------------------------------------------------------------

HOOK_WEBFETCH = "webfetch_to_tavily.py"


class TestWebfetchToTavily:
    def test_should_fire_with_url(self, run_hook):
        result = run_hook(HOOK_WEBFETCH, {
            "tool_name": "WebFetch",
            "tool_input": {"url": "https://example.com/docs"},
        })
        assert result.returncode == 0
        assert "Tavily" in result.stderr

    def test_should_fire_embeds_url_in_warning(self, run_hook):
        url = "https://docs.python.org/3/library/json.html"
        result = run_hook(HOOK_WEBFETCH, {
            "tool_name": "WebFetch",
            "tool_input": {"url": url},
        })
        assert result.returncode == 0
        assert url in result.stderr

    def test_should_fire_no_url_field(self, run_hook):
        # No url key — hook still warns (fires unconditionally on any valid JSON)
        result = run_hook(HOOK_WEBFETCH, {
            "tool_name": "WebFetch",
            "tool_input": {},
        })
        assert result.returncode == 0
        assert "Tavily" in result.stderr

    def test_wrong_tool_name_still_fires(self, run_hook):
        # webfetch_to_tavily has no tool_name guard — fires for any tool
        result = run_hook(HOOK_WEBFETCH, {
            "tool_name": "Bash",
            "tool_input": {"url": "https://example.com"},
        })
        assert result.returncode == 0
        assert "Tavily" in result.stderr

    def test_invalid_json(self):
        hook_path = (
            __import__("pathlib").Path(__file__).parent.parent.parent
            / "plugins" / "ima-claude" / "hooks" / HOOK_WEBFETCH
        )
        proc = subprocess.run(
            ["python3", str(hook_path)],
            input="{bad",
            capture_output=True,
            text=True,
        )
        assert proc.returncode in (0, 1)
        assert "Traceback" not in proc.stderr
        # The hook prints its own error on JSONDecodeError
        assert "hook-error" in proc.stderr


# ---------------------------------------------------------------------------
# websearch_to_tavily
# ---------------------------------------------------------------------------

HOOK_WEBSEARCH = "websearch_to_tavily.py"


class TestWebsearchToTavily:
    def test_should_fire_with_query(self, run_hook):
        result = run_hook(HOOK_WEBSEARCH, {
            "tool_name": "WebSearch",
            "tool_input": {"query": "python async patterns"},
        })
        assert result.returncode == 0
        assert "Tavily" in result.stderr

    def test_should_fire_embeds_query_in_warning(self, run_hook):
        query = "pytest fixtures best practices"
        result = run_hook(HOOK_WEBSEARCH, {
            "tool_name": "WebSearch",
            "tool_input": {"query": query},
        })
        assert result.returncode == 0
        assert query in result.stderr

    def test_should_fire_no_query_field(self, run_hook):
        # No query key — hook still warns unconditionally on valid JSON
        result = run_hook(HOOK_WEBSEARCH, {
            "tool_name": "WebSearch",
            "tool_input": {},
        })
        assert result.returncode == 0
        assert "Tavily" in result.stderr

    def test_wrong_tool_name_still_fires(self, run_hook):
        # websearch_to_tavily has no tool_name guard — fires for any tool
        result = run_hook(HOOK_WEBSEARCH, {
            "tool_name": "Bash",
            "tool_input": {"query": "some search"},
        })
        assert result.returncode == 0
        assert "Tavily" in result.stderr

    def test_invalid_json(self):
        hook_path = (
            __import__("pathlib").Path(__file__).parent.parent.parent
            / "plugins" / "ima-claude" / "hooks" / HOOK_WEBSEARCH
        )
        proc = subprocess.run(
            ["python3", str(hook_path)],
            input="{bad",
            capture_output=True,
            text=True,
        )
        assert proc.returncode in (0, 1)
        assert "Traceback" not in proc.stderr
        assert "hook-error" in proc.stderr
