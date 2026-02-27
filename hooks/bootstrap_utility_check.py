#!/usr/bin/env python3
"""
PostToolUse hook: Warn about hardcoded CSS when Bootstrap utilities are available.

Checks (soft warning only, exit 0):
  M3 — Inline styles in HTML/PHP that have Bootstrap 5 utility equivalents
  M3 — CSS properties in .scss/.css only when Bootstrap context is detected

Applies to: Edit, Write on .html, .php, .scss, .css files.
"""
import json
import re
import sys

HTML_PHP_EXTENSIONS = (".html", ".php")
CSS_EXTENSIONS = (".scss", ".css")
ALL_EXTENSIONS = HTML_PHP_EXTENSIONS + CSS_EXTENSIONS

# Bootstrap context signals in CSS/SCSS files
BOOTSTRAP_CONTEXT = re.compile(
    r"@import\s+['\"].*bootstrap|"
    r"\$spacer\b|"
    r"\bbs-"
)

# Inline style patterns with their Bootstrap equivalents
INLINE_STYLE_PATTERNS = [
    (re.compile(r'style=["\'][^"\']*margin', re.IGNORECASE), "margin-*", "m-* / mt-* / mb-* / ms-* / me-*"),
    (re.compile(r'style=["\'][^"\']*padding', re.IGNORECASE), "padding-*", "p-* / pt-* / pb-* / ps-* / pe-*"),
    (re.compile(r'style=["\'][^"\']*display\s*:\s*flex', re.IGNORECASE), "display: flex", "d-flex"),
    (re.compile(r'style=["\'][^"\']*display\s*:\s*none', re.IGNORECASE), "display: none", "d-none"),
    (re.compile(r'style=["\'][^"\']*text-align\s*:\s*center', re.IGNORECASE), "text-align: center", "text-center"),
    (re.compile(r'style=["\'][^"\']*font-weight\s*:\s*bold', re.IGNORECASE), "font-weight: bold", "fw-bold"),
]

WARNING_HEADER = "⚠️  Hardcoded CSS detected — Bootstrap 5 utilities available:"
WARNING_EXAMPLES = (
    '  style="margin-top: 16px"   →  class="mt-3"\n'
    '  style="display: flex"      →  class="d-flex"\n'
    '  style="text-align: center" →  class="text-center"\n'
    "  See /ima-bootstrap skill for utility-first patterns."
)


def is_bootstrap_context(content: str) -> bool:
    return bool(BOOTSTRAP_CONTEXT.search(content))


def find_inline_style_issues(content: str) -> list[str]:
    return [
        f"  {css_prop}  →  {utility}"
        for pattern, css_prop, utility in INLINE_STYLE_PATTERNS
        if pattern.search(content)
    ]


def get_content(tool_name: str, tool_input: dict) -> str:
    if tool_name == "Write":
        return tool_input.get("content", "")
    # Edit: scan only new_string — what's being written now
    return tool_input.get("new_string", "")


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
file_path = tool_input.get("file_path", "")

if tool_name not in ("Edit", "Write"):
    sys.exit(0)

if not file_path.endswith(ALL_EXTENSIONS):
    sys.exit(0)

content = get_content(tool_name, tool_input)
if not content:
    sys.exit(0)

is_css_file = file_path.endswith(CSS_EXTENSIONS)

# CSS/SCSS files only warn when Bootstrap is confirmed in context
if is_css_file and not is_bootstrap_context(content):
    sys.exit(0)

issues = find_inline_style_issues(content)
if issues:
    print(WARNING_HEADER, file=sys.stderr)
    print(WARNING_EXAMPLES, file=sys.stderr)

sys.exit(0)
