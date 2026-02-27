#!/usr/bin/env python3
"""
PostToolUse hook: Warn when a Markdown file is written to the project root.

M10 — Markdown files scattered in project root.

After a Write to a .md file, checks whether the file lands at the root level of the
project rather than in a designated docs subdirectory. Exempt files (README.md, etc.)
and files in docs/, .claude/, skills/, or hooks/ subdirectories are silently allowed.
Exit code 0 = soft warning via stderr.
"""
import json
import os
import subprocess
import sys

EXEMPT_FILENAMES = {
    "README.md",
    "CLAUDE.md",
    "CHANGELOG.md",
    "LICENSE.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
}

EXEMPT_DIRS = {"docs", ".claude", "skills", "hooks"}

WARNING = (
    "⚠️  Markdown file written to project root — consider docs-organize structure:\n"
    "  docs/active/    — permanent documentation\n"
    "  docs/archive/   — historical records\n"
    "  docs/transient/ — ephemeral notes (git-ignored)"
)


def get_git_root(path: str) -> str:
    """Return the git repository root, or the file's directory as fallback.

    Walks up from the file's directory to find the first existing ancestor,
    so this works even when Claude is writing a file into a not-yet-created dir.
    """
    search_dir = os.path.dirname(os.path.abspath(path))
    while search_dir and not os.path.isdir(search_dir):
        parent = os.path.dirname(search_dir)
        if parent == search_dir:
            break
        search_dir = parent

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            cwd=search_dir,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except OSError:
        pass
    return search_dir


def is_exempt(file_path: str, git_root: str) -> bool:
    filename = os.path.basename(file_path)
    if filename in EXEMPT_FILENAMES:
        return True

    rel = os.path.relpath(file_path, git_root)
    parts = rel.split(os.sep)

    # File is inside an exempt subdirectory
    if len(parts) > 1 and parts[0] in EXEMPT_DIRS:
        return True

    return False


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
file_path = tool_input.get("file_path", "")

if tool_name != "Write":
    sys.exit(0)

if not file_path.endswith(".md"):
    sys.exit(0)

git_root = get_git_root(file_path)
rel = os.path.relpath(file_path, git_root)

# Only warn when the file is at the root level (no subdirectory component)
if os.path.dirname(rel) != "":
    sys.exit(0)

if is_exempt(file_path, git_root):
    sys.exit(0)

print(WARNING, file=sys.stderr)
sys.exit(0)
