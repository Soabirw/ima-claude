import json
import subprocess
from pathlib import Path
import pytest

HOOKS_DIR = Path(__file__).parent.parent.parent / "plugins" / "ima-claude" / "hooks"


@pytest.fixture
def run_hook():
    def _run(hook_filename: str, input_data: dict) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["python3", str(HOOKS_DIR / hook_filename)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
        )
    return _run


@pytest.fixture
def tmp_state_file(tmp_path, monkeypatch):
    """Redirect memory_bootstrap's state file to a temp path.

    Note: memory_bootstrap.py reads STATE_FILE as a module-level constant so
    this env var only takes effect if the hook is updated to read it. For tests
    that exercise memory_bootstrap, pass env={"CLAUDE_STATE_FILE": str(state_file)}
    directly to subprocess.run via a custom call rather than using run_hook.
    """
    state_file = tmp_path / ".memory_bootstrapped"
    monkeypatch.setenv("CLAUDE_STATE_FILE", str(state_file))
    return state_file
