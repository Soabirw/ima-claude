"""
Integration hook tests for:
  - atlassian_prereqs.py
  - jira_issue_fetch.py
  - serena_project_check.py
  - docs_organization.py

Each hook is exercised as a subprocess (matching real Claude Code behaviour)
so that module-level code, sys.exit(), and stderr output are all captured.

The conftest `run_hook` fixture handles the subprocess plumbing.
State files written by hooks default to ~/.claude/; tests that need to avoid
polluting that directory redirect HOME via a tmp_path + env override.
"""

import json
import os
import subprocess
import time
from pathlib import Path

import pytest

HOOKS_DIR = (
    Path(__file__).parent.parent.parent / "plugins" / "ima-claude" / "hooks"
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def run_hook_with_home(hook_filename: str, input_data: dict, home: Path, **kwargs):
    """Run a hook with HOME redirected to `home` so state files stay isolated."""
    env = {**os.environ, "HOME": str(home)}
    env.update(kwargs.pop("extra_env", {}))
    return subprocess.run(
        ["python3", str(HOOKS_DIR / hook_filename)],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        env=env,
        **kwargs,
    )


# ===========================================================================
# atlassian_prereqs.py
# ===========================================================================

class TestAtlassianPrereqs:
    HOOK = "atlassian_prereqs.py"

    # -------------------------------------------------------------------
    # Non-Atlassian tool: hook is a no-op
    # -------------------------------------------------------------------
    def test_non_atlassian_tool_exits_silently(self, run_hook):
        """Hook must exit 0 with no output for tools it doesn't own."""
        result = run_hook(self.HOOK, {"tool_name": "Bash", "tool_input": {}})
        assert result.returncode == 0
        assert result.stderr == ""

    def test_wrong_tool_prefix_exits_silently(self, run_hook):
        """Any tool name that doesn't start with mcp__claude_ai_Atlassian__ is ignored."""
        result = run_hook(
            self.HOOK,
            {"tool_name": "mcp__serena__find_symbol", "tool_input": {}},
        )
        assert result.returncode == 0
        assert result.stderr == ""

    # -------------------------------------------------------------------
    # Invalid JSON: hook must not crash
    # -------------------------------------------------------------------
    def test_invalid_json_exits_cleanly(self, tmp_path):
        """Malformed JSON on stdin must exit 0 without a Python traceback."""
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / self.HOOK)],
            input="this is not json",
            capture_output=True,
            text=True,
            env={**os.environ, "HOME": str(tmp_path)},
        )
        assert result.returncode == 0
        assert "Traceback" not in result.stderr

    # -------------------------------------------------------------------
    # Bootstrap tool: marks state and exits silently
    # -------------------------------------------------------------------
    def test_bootstrap_tool_marks_state_and_exits(self, tmp_path):
        """getAccessibleAtlassianResources should set bootstrapped=True and produce no output."""
        result = run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__claude_ai_Atlassian__getAccessibleAtlassianResources", "tool_input": {}},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert result.stderr == ""
        # State file should now exist
        state_file = tmp_path / ".claude" / ".atlassian_session_state"
        assert state_file.exists()
        state = json.loads(state_file.read_text())
        assert state["bootstrapped"] is True

    # -------------------------------------------------------------------
    # H3 warning: un-bootstrapped session triggers cloudId reminder
    # -------------------------------------------------------------------
    def test_unbootstrapped_session_warns(self, tmp_path):
        """Any Atlassian tool called before bootstrap should print the cloudId warning."""
        result = run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__claude_ai_Atlassian__getJiraIssue", "tool_input": {}},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert "getAccessibleAtlassianResources" in result.stderr

    # -------------------------------------------------------------------
    # H3: bootstrapped session suppresses the cloudId warning
    # -------------------------------------------------------------------
    def test_bootstrapped_session_no_warning(self, tmp_path):
        """After bootstrap, subsequent Atlassian tool calls must not repeat the cloudId warning."""
        # First call: bootstrap
        run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__claude_ai_Atlassian__getAccessibleAtlassianResources", "tool_input": {}},
            home=tmp_path,
        )
        # Second call: any other Atlassian tool
        result = run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__claude_ai_Atlassian__getJiraIssue", "tool_input": {"cloudId": "x"}},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert "getAccessibleAtlassianResources" not in result.stderr

    # -------------------------------------------------------------------
    # H4 warning: transitionJiraIssue without prior transitions fetch
    # -------------------------------------------------------------------
    def test_transition_without_fetch_warns(self, tmp_path):
        """transitionJiraIssue before getTransitionsForJiraIssue should warn with the issue key."""
        # Bootstrap first so H3 doesn't also fire
        run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__claude_ai_Atlassian__getAccessibleAtlassianResources", "tool_input": {}},
            home=tmp_path,
        )
        result = run_hook_with_home(
            self.HOOK,
            {
                "tool_name": "mcp__claude_ai_Atlassian__transitionJiraIssue",
                "tool_input": {"issueIdOrKey": "IMA-99"},
            },
            home=tmp_path,
        )
        assert result.returncode == 0
        assert "getTransitionsForJiraIssue" in result.stderr
        assert "IMA-99" in result.stderr

    # -------------------------------------------------------------------
    # H4: transitions fetched first suppresses H4 warning
    # -------------------------------------------------------------------
    def test_transition_after_fetch_no_warning(self, tmp_path):
        """No H4 warning after getTransitionsForJiraIssue has been called."""
        # Bootstrap
        run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__claude_ai_Atlassian__getAccessibleAtlassianResources", "tool_input": {}},
            home=tmp_path,
        )
        # Fetch transitions
        run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__claude_ai_Atlassian__getTransitionsForJiraIssue", "tool_input": {}},
            home=tmp_path,
        )
        # Now transition
        result = run_hook_with_home(
            self.HOOK,
            {
                "tool_name": "mcp__claude_ai_Atlassian__transitionJiraIssue",
                "tool_input": {"issueIdOrKey": "IMA-99"},
            },
            home=tmp_path,
        )
        assert result.returncode == 0
        assert "getTransitionsForJiraIssue" not in result.stderr

    # -------------------------------------------------------------------
    # M5: ADF body as raw dict triggers warning
    # -------------------------------------------------------------------
    def test_adf_body_as_dict_warns(self, tmp_path):
        """createConfluencePage with contentFormat=adf and body as a raw dict must warn."""
        # Bootstrap first
        run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__claude_ai_Atlassian__getAccessibleAtlassianResources", "tool_input": {}},
            home=tmp_path,
        )
        result = run_hook_with_home(
            self.HOOK,
            {
                "tool_name": "mcp__claude_ai_Atlassian__createConfluencePage",
                "tool_input": {
                    "cloudId": "x",
                    "spaceId": "s",
                    "contentFormat": "adf",
                    "body": {"type": "doc", "content": []},
                },
            },
            home=tmp_path,
        )
        assert result.returncode == 0
        assert "ADF" in result.stderr or "JSON string" in result.stderr

    # -------------------------------------------------------------------
    # M5: ADF body as string (correct) produces no warning
    # -------------------------------------------------------------------
    def test_adf_body_as_string_no_warning(self, tmp_path):
        """ADF body provided as a JSON string must not trigger the M5 warning."""
        run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__claude_ai_Atlassian__getAccessibleAtlassianResources", "tool_input": {}},
            home=tmp_path,
        )
        result = run_hook_with_home(
            self.HOOK,
            {
                "tool_name": "mcp__claude_ai_Atlassian__createConfluencePage",
                "tool_input": {
                    "cloudId": "x",
                    "spaceId": "s",
                    "contentFormat": "adf",
                    "body": '{"type":"doc","content":[]}',
                },
            },
            home=tmp_path,
        )
        assert result.returncode == 0
        assert "ADF" not in result.stderr

    # -------------------------------------------------------------------
    # M5: markdown format body as dict is fine (only ADF is restricted)
    # -------------------------------------------------------------------
    def test_markdown_body_as_dict_no_warning(self, tmp_path):
        """Markdown-format body as a dict must not trigger the ADF warning."""
        run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__claude_ai_Atlassian__getAccessibleAtlassianResources", "tool_input": {}},
            home=tmp_path,
        )
        result = run_hook_with_home(
            self.HOOK,
            {
                "tool_name": "mcp__claude_ai_Atlassian__createConfluencePage",
                "tool_input": {
                    "cloudId": "x",
                    "spaceId": "s",
                    "contentFormat": "markdown",
                    "body": {"some": "dict"},
                },
            },
            home=tmp_path,
        )
        assert result.returncode == 0
        assert "ADF" not in result.stderr

    # -------------------------------------------------------------------
    # Stale state file resets to defaults (bootstrapped=False)
    # -------------------------------------------------------------------
    def test_stale_state_treated_as_fresh_session(self, tmp_path):
        """A state file older than 1 hour is ignored; unbootstrapped warning re-fires."""
        state_file = tmp_path / ".claude" / ".atlassian_session_state"
        state_file.parent.mkdir(parents=True)
        old_ts = time.time() - 3601  # just over the 1-hour threshold
        state_file.write_text(json.dumps({
            "bootstrapped": True,
            "transitions_fetched": True,
            "timestamp": old_ts,
        }))
        result = run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__claude_ai_Atlassian__getJiraIssue", "tool_input": {}},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert "getAccessibleAtlassianResources" in result.stderr


# ===========================================================================
# jira_issue_fetch.py
# ===========================================================================

class TestJiraIssueFetch:
    HOOK = "jira_issue_fetch.py"

    # -------------------------------------------------------------------
    # Invalid JSON: no crash
    # -------------------------------------------------------------------
    def test_invalid_json_exits_cleanly(self, tmp_path):
        """Malformed JSON on stdin must exit 0 without a traceback."""
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / self.HOOK)],
            input="{bad json",
            capture_output=True,
            text=True,
            env={**os.environ, "HOME": str(tmp_path)},
        )
        assert result.returncode == 0
        assert "Traceback" not in result.stderr

    # -------------------------------------------------------------------
    # Empty prompt: exit silently
    # -------------------------------------------------------------------
    def test_empty_prompt_exits_silently(self, tmp_path):
        """A prompt with no Jira key must produce no stderr output."""
        result = run_hook_with_home(
            self.HOOK,
            {"user_prompt": "Please help me with this task"},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    # -------------------------------------------------------------------
    # Absent user_prompt key: graceful exit
    # -------------------------------------------------------------------
    def test_missing_prompt_key_exits_silently(self, tmp_path):
        """Input with no user_prompt field must exit 0 without output."""
        result = run_hook_with_home(
            self.HOOK,
            {"some_other_field": "value"},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    # -------------------------------------------------------------------
    # Normal path: Jira key detected, reminder printed
    # -------------------------------------------------------------------
    def test_jira_key_detected_prints_reminder(self, tmp_path):
        """A prompt containing a Jira key should print a fetch reminder to stderr."""
        result = run_hook_with_home(
            self.HOOK,
            {"user_prompt": "Looking at IMA-123 today"},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert "IMA-123" in result.stderr
        assert "getJiraIssue" in result.stderr

    # -------------------------------------------------------------------
    # Key pattern matching: various valid formats
    # -------------------------------------------------------------------
    def test_jira_key_various_formats(self, tmp_path):
        """Keys like FNR-1, ABCDE-999 must all be detected."""
        for key in ["FNR-1", "AB-42", "ABCDE-999"]:
            result = run_hook_with_home(
                self.HOOK,
                {"user_prompt": f"Work on {key} please"},
                home=tmp_path,
            )
            assert result.returncode == 0
            assert key in result.stderr, f"Expected {key} in stderr"
            # Wipe state so the next key is fresh
            state = tmp_path / ".claude" / ".jira_keys_fetched"
            if state.exists():
                state.unlink()

    # -------------------------------------------------------------------
    # Same key seen twice: reminder only fires once per session
    # -------------------------------------------------------------------
    def test_repeat_key_suppressed(self, tmp_path):
        """The second call with the same key in the same session must produce no output."""
        payload = {"user_prompt": "Fix IMA-200 please"}
        # First call – should warn
        first = run_hook_with_home(self.HOOK, payload, home=tmp_path)
        assert "IMA-200" in first.stderr
        # Second call – should be silent
        second = run_hook_with_home(self.HOOK, payload, home=tmp_path)
        assert second.returncode == 0
        assert second.stderr == ""

    # -------------------------------------------------------------------
    # Only the first key in a multi-key prompt triggers the reminder
    # -------------------------------------------------------------------
    def test_first_key_only_triggered(self, tmp_path):
        """When multiple keys appear, only the first triggers a reminder."""
        result = run_hook_with_home(
            self.HOOK,
            {"user_prompt": "IMA-10 and IMA-20 are related"},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert "IMA-10" in result.stderr
        assert "IMA-20" not in result.stderr

    # -------------------------------------------------------------------
    # Stale state file: key is treated as new again
    # -------------------------------------------------------------------
    def test_stale_state_file_resets_seen_keys(self, tmp_path):
        """Keys seen in a stale (>1h) state file are treated as unseen."""
        state_file = tmp_path / ".claude" / ".jira_keys_fetched"
        state_file.parent.mkdir(parents=True)
        state_file.write_text("IMA-300\n")
        # Make the file appear old by changing its mtime
        old_mtime = time.time() - 3700
        os.utime(state_file, (old_mtime, old_mtime))

        result = run_hook_with_home(
            self.HOOK,
            {"user_prompt": "Re-visiting IMA-300 again"},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert "IMA-300" in result.stderr

    # -------------------------------------------------------------------
    # Pattern does not match lowercase or partial patterns
    # -------------------------------------------------------------------
    def test_lowercase_key_not_matched(self, tmp_path):
        """Lowercase 'ima-123' must not trigger the hook (pattern requires uppercase)."""
        result = run_hook_with_home(
            self.HOOK,
            {"user_prompt": "ima-123 is not a jira key"},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    # -------------------------------------------------------------------
    # Single-letter project prefix does not match (pattern requires 2+ letters)
    # -------------------------------------------------------------------
    def test_single_letter_prefix_not_matched(self, tmp_path):
        """A single-letter prefix like A-1 must not match the Jira key pattern."""
        result = run_hook_with_home(
            self.HOOK,
            {"user_prompt": "See A-1 for details"},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert result.stderr == ""


# ===========================================================================
# serena_project_check.py
# ===========================================================================

class TestSerenaProjectCheck:
    HOOK = "serena_project_check.py"

    # -------------------------------------------------------------------
    # Non-Serena tool: silent pass-through
    # -------------------------------------------------------------------
    def test_non_serena_tool_exits_silently(self, tmp_path):
        """Hook must exit 0 with no output for non-Serena tools."""
        result = run_hook_with_home(
            self.HOOK,
            {"tool_name": "Bash", "tool_input": {}},
            home=tmp_path,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    # -------------------------------------------------------------------
    # Invalid JSON: no crash
    # -------------------------------------------------------------------
    def test_invalid_json_exits_cleanly(self, tmp_path):
        """Malformed JSON must exit 0 without a traceback."""
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / self.HOOK)],
            input="]bad[",
            capture_output=True,
            text=True,
            env={**os.environ, "HOME": str(tmp_path)},
        )
        assert result.returncode == 0
        assert "Traceback" not in result.stderr

    # -------------------------------------------------------------------
    # mcp__serena__ tool marks activated in state
    # -------------------------------------------------------------------
    def test_serena_tool_marks_activated(self, tmp_path):
        """Any mcp__serena__* call must set activated=True in the state file."""
        run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__serena__list_dir", "tool_input": {}},
            home=tmp_path,
        )
        state_file = tmp_path / ".claude" / ".serena_session_state"
        assert state_file.exists()
        state = json.loads(state_file.read_text())
        assert state["activated"] is True

    # -------------------------------------------------------------------
    # JetBrains tool outside WP subdir: no WP warning
    # -------------------------------------------------------------------
    def test_jet_brains_tool_outside_wp_no_warning(self, tmp_path):
        """A JetBrains tool called from a non-WP path must not emit the WP warning."""
        result = run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__serena__jet_brains_find_symbol", "tool_input": {}},
            home=tmp_path,
            # cwd is tmp_path itself — no wp-content anywhere in path
        )
        assert result.returncode == 0
        # The WP warning mentions "wp-content" or "WordPress root"
        assert "WordPress root" not in result.stderr
        assert "wp-content" not in result.stderr

    # -------------------------------------------------------------------
    # JetBrains tool inside WP plugins dir WITH .serena: warns
    # -------------------------------------------------------------------
    def test_jet_brains_tool_in_wp_plugins_warns(self, tmp_path):
        """JetBrains tool called from wp-content/plugins/<name>/ should warn about WP root."""
        # Build a minimal fake WP tree:
        #   tmp_path/
        #     wp-content/
        #       plugins/
        #         my-plugin/   <- cwd
        #     .serena/
        #       project.yml
        wp_root = tmp_path
        plugin_dir = wp_root / "wp-content" / "plugins" / "my-plugin"
        plugin_dir.mkdir(parents=True)
        serena_dir = wp_root / ".serena"
        serena_dir.mkdir()
        (serena_dir / "project.yml").write_text('project_name: "my-wp-site"\n')

        result = run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__serena__jet_brains_find_symbol", "tool_input": {}},
            home=tmp_path,
            cwd=str(plugin_dir),
        )
        assert result.returncode == 0
        assert "WordPress root" in result.stderr or "Serena project" in result.stderr

    # -------------------------------------------------------------------
    # WP warning fires only once per session (warned_wp flag)
    # -------------------------------------------------------------------
    def test_wp_warning_fires_only_once(self, tmp_path):
        """After the first WP warning, subsequent calls must not repeat it."""
        wp_root = tmp_path
        plugin_dir = wp_root / "wp-content" / "plugins" / "my-plugin"
        plugin_dir.mkdir(parents=True)
        serena_dir = wp_root / ".serena"
        serena_dir.mkdir()
        (serena_dir / "project.yml").write_text('project_name: "my-wp-site"\n')

        # First call: should warn
        run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__serena__jet_brains_find_symbol", "tool_input": {}},
            home=tmp_path,
            cwd=str(plugin_dir),
        )
        # Second call: must be silent
        second = run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__serena__jet_brains_find_symbol", "tool_input": {}},
            home=tmp_path,
            cwd=str(plugin_dir),
        )
        assert second.returncode == 0
        assert "WordPress root" not in second.stderr
        assert "Serena project" not in second.stderr

    # -------------------------------------------------------------------
    # Stale state file resets
    # -------------------------------------------------------------------
    def test_stale_state_file_resets_warned_wp(self, tmp_path):
        """A stale (>1h) state file must be treated as a fresh session."""
        state_file = tmp_path / ".claude" / ".serena_session_state"
        state_file.parent.mkdir(parents=True)
        old_ts = time.time() - 3700
        state_file.write_text(json.dumps({
            "activated": True,
            "warned_wp": True,
            "timestamp": old_ts,
        }))

        wp_root = tmp_path
        plugin_dir = wp_root / "wp-content" / "plugins" / "my-plugin"
        plugin_dir.mkdir(parents=True)
        serena_dir = wp_root / ".serena"
        serena_dir.mkdir()
        (serena_dir / "project.yml").write_text('project_name: "my-wp-site"\n')

        result = run_hook_with_home(
            self.HOOK,
            {"tool_name": "mcp__serena__jet_brains_find_symbol", "tool_input": {}},
            home=tmp_path,
            cwd=str(plugin_dir),
        )
        assert result.returncode == 0
        # warned_wp was True in stale file, but after reset it's False → warning fires
        assert "WordPress root" in result.stderr or "Serena project" in result.stderr


# ===========================================================================
# docs_organization.py
# ===========================================================================

class TestDocsOrganization:
    HOOK = "docs_organization.py"

    # -------------------------------------------------------------------
    # Non-Write tool: silent pass-through
    # -------------------------------------------------------------------
    def test_non_write_tool_exits_silently(self, run_hook):
        """Hook must exit 0 silently for any tool other than Write."""
        result = run_hook(
            self.HOOK,
            {"tool_name": "Read", "tool_input": {"file_path": "/tmp/foo.md"}},
        )
        assert result.returncode == 0
        assert result.stderr == ""

    # -------------------------------------------------------------------
    # Invalid JSON: no crash
    # -------------------------------------------------------------------
    def test_invalid_json_exits_cleanly(self):
        """Malformed JSON must exit 0 without a Python traceback."""
        result = subprocess.run(
            ["python3", str(HOOKS_DIR / self.HOOK)],
            input="not-json",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Traceback" not in result.stderr

    # -------------------------------------------------------------------
    # Non-.md file: silent
    # -------------------------------------------------------------------
    def test_non_md_file_exits_silently(self, run_hook, tmp_path):
        """A Write to a .txt file must not trigger the warning."""
        result = run_hook(
            self.HOOK,
            {
                "tool_name": "Write",
                "tool_input": {"file_path": str(tmp_path / "notes.txt")},
            },
        )
        assert result.returncode == 0
        assert result.stderr == ""

    # -------------------------------------------------------------------
    # Wrong tool_name: silent exit
    # -------------------------------------------------------------------
    def test_wrong_tool_name_exits_silently(self, run_hook, tmp_path):
        """Any tool name that isn't Write must be ignored."""
        result = run_hook(
            self.HOOK,
            {
                "tool_name": "Edit",
                "tool_input": {"file_path": str(tmp_path / "some.md")},
            },
        )
        assert result.returncode == 0
        assert result.stderr == ""

    # -------------------------------------------------------------------
    # Normal path: unexempt root-level .md triggers warning
    # -------------------------------------------------------------------
    def test_root_md_file_triggers_warning(self, tmp_path):
        """Writing a non-exempt .md at git root level must print the docs-organize warning."""
        # Create a minimal git repo so get_git_root() resolves correctly
        subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
        md_file = tmp_path / "NOTES.md"

        result = subprocess.run(
            ["python3", str(HOOKS_DIR / self.HOOK)],
            input=json.dumps({
                "tool_name": "Write",
                "tool_input": {"file_path": str(md_file)},
            }),
            capture_output=True,
            text=True,
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert "docs-organize" in result.stderr or "docs/active" in result.stderr

    # -------------------------------------------------------------------
    # Exempt filenames: README.md, CLAUDE.md, CHANGELOG.md, etc.
    # -------------------------------------------------------------------
    @pytest.mark.parametrize("filename", [
        "README.md",
        "CLAUDE.md",
        "CHANGELOG.md",
        "LICENSE.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
    ])
    def test_exempt_filename_no_warning(self, tmp_path, filename):
        """Exempt filenames at root must not trigger the warning."""
        subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
        md_file = tmp_path / filename

        result = subprocess.run(
            ["python3", str(HOOKS_DIR / self.HOOK)],
            input=json.dumps({
                "tool_name": "Write",
                "tool_input": {"file_path": str(md_file)},
            }),
            capture_output=True,
            text=True,
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert result.stderr == ""

    # -------------------------------------------------------------------
    # Files inside exempt directories: no warning
    # -------------------------------------------------------------------
    @pytest.mark.parametrize("subdir", ["docs", ".claude", "skills", "hooks"])
    def test_exempt_subdir_no_warning(self, tmp_path, subdir):
        """A .md file inside an exempt subdirectory must not trigger the warning."""
        subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
        target_dir = tmp_path / subdir
        target_dir.mkdir()
        md_file = target_dir / "any-file.md"

        result = subprocess.run(
            ["python3", str(HOOKS_DIR / self.HOOK)],
            input=json.dumps({
                "tool_name": "Write",
                "tool_input": {"file_path": str(md_file)},
            }),
            capture_output=True,
            text=True,
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert result.stderr == ""

    # -------------------------------------------------------------------
    # Nested (non-root) .md that isn't in an exempt dir: no warning
    # -------------------------------------------------------------------
    def test_nested_md_no_warning(self, tmp_path):
        """A .md file inside a non-exempt subdirectory is not at root, so no warning."""
        subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
        subdir = tmp_path / "some-other-dir"
        subdir.mkdir()
        md_file = subdir / "NOTES.md"

        result = subprocess.run(
            ["python3", str(HOOKS_DIR / self.HOOK)],
            input=json.dumps({
                "tool_name": "Write",
                "tool_input": {"file_path": str(md_file)},
            }),
            capture_output=True,
            text=True,
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert result.stderr == ""

    # -------------------------------------------------------------------
    # updateConfluencePage (wrong tool) is silently skipped
    # -------------------------------------------------------------------
    def test_update_confluence_tool_ignored(self, run_hook, tmp_path):
        """docs_organization only monitors 'Write' tool — Confluence tools are ignored."""
        result = run_hook(
            self.HOOK,
            {
                "tool_name": "mcp__claude_ai_Atlassian__updateConfluencePage",
                "tool_input": {"file_path": str(tmp_path / "NOTES.md")},
            },
        )
        assert result.returncode == 0
        assert result.stderr == ""
