#!/usr/bin/env python3
"""
PostToolUse hook: Warn about vanilla DOM JS in WordPress context.

Checks (soft warning only, exit 0):
  M2 — querySelector/addEventListener/etc. when jQuery is already loaded

WordPress context is detected via file path (wp-content/plugins, wp-content/themes)
or file content (jQuery signals).

Applies to: Edit, Write on .js files only.
"""
import json
import re
import sys

WP_PATH_SIGNALS = ("wp-content/plugins/", "wp-content/themes/")

WP_CONTENT_SIGNALS = re.compile(
    r"jQuery\s*[\(\.]|"
    r"\(function\s*\(\$\)|"
    r"\$\s*\(document\)|"
    r"\bwp\."
)

VANILLA_DOM_PATTERNS = re.compile(
    r"document\.querySelectorAll\s*\(|"
    r"document\.querySelector\s*\(|"
    r"document\.getElementById\s*\(|"
    r"document\.getElementsByClassName\s*\(|"
    r"\.addEventListener\s*\(|"
    r"document\.createElement\s*\("
)

WARNING = (
    "⚠️  Vanilla DOM JS in WordPress context — jQuery is already loaded (0 extra bytes).\n"
    "  document.querySelector('.x')  →  $('.x')\n"
    "  el.addEventListener('click')  →  $(el).on('click')\n"
    "  See /jquery skill for FP-aligned patterns."
)


def is_wordpress_path(file_path: str) -> bool:
    return any(signal in file_path for signal in WP_PATH_SIGNALS)


def is_wordpress_content(content: str) -> bool:
    return bool(WP_CONTENT_SIGNALS.search(content))


def has_vanilla_dom(content: str) -> bool:
    return bool(VANILLA_DOM_PATTERNS.search(content))


def read_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
file_path = tool_input.get("file_path", "")

if tool_name not in ("Edit", "Write"):
    sys.exit(0)

if not file_path.endswith(".js"):
    sys.exit(0)

if tool_name == "Write":
    written_content = tool_input.get("content", "")
    wp_context = is_wordpress_path(file_path) or is_wordpress_content(written_content)
    vanilla_found = has_vanilla_dom(written_content)
else:
    # Edit: check path for WP context; read disk file for content signals
    new_string = tool_input.get("new_string", "")
    disk_content = read_file(file_path)
    wp_context = is_wordpress_path(file_path) or is_wordpress_content(disk_content)
    vanilla_found = has_vanilla_dom(new_string)

if wp_context and vanilla_found:
    print(WARNING, file=sys.stderr)

sys.exit(0)
