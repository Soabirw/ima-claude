#!/usr/bin/env python3
"""
PostToolUse hook: Warn about WordPress PHP security issues.

Checks (soft warnings only, exit 0):
  H1 — AJAX handlers missing nonce verification or capability checks
  H1 — $wpdb queries missing ->prepare()
  H1 — Raw $_POST/$_GET/$_REQUEST without sanitization
  M4 — Missing declare(strict_types=1)
  M8 — function_exists() used instead of action/filter hooks for cross-plugin calls

Applies to: Edit, Write on .php files.
"""
import json
import re
import sys

# WordPress core function prefixes — function_exists() on these is fine
WP_CORE_PREFIXES = (
    "wp_", "is_", "get_", "the_", "add_", "remove_", "do_", "apply_", "has_", "did_",
)

SANITIZE_FUNCTIONS = (
    "sanitize_text_field", "absint", "sanitize_email", "wp_kses",
    "esc_html", "esc_attr", "intval",
)


def check_ajax_security(content: str) -> list[str]:
    warnings = []

    if not re.search(r"wp_ajax_", content):
        return warnings

    has_nonce = re.search(r"wp_verify_nonce|check_ajax_referer", content)
    if not has_nonce:
        warnings.append(
            "⚠️  H1: AJAX handler missing nonce verification.\n"
            "  Add wp_verify_nonce() or check_ajax_referer() before processing."
        )

    has_capability = re.search(r"current_user_can\s*\(", content)
    if not has_capability:
        warnings.append(
            "⚠️  H1: AJAX handler missing capability check.\n"
            "  Add current_user_can() to restrict access."
        )

    return warnings


def check_wpdb_prepare(content: str) -> list[str]:
    if re.search(r"\$wpdb->", content) and not re.search(r"->prepare\s*\(", content):
        return [
            "⚠️  H1: $wpdb query detected without ->prepare().\n"
            "  Use $wpdb->prepare() for all queries with dynamic values."
        ]
    return []


def check_sanitization(content: str) -> list[str]:
    has_raw_input = re.search(r"\$_(POST|GET|REQUEST)\s*\[", content)
    if not has_raw_input:
        return []

    sanitize_pattern = "|".join(re.escape(fn) for fn in SANITIZE_FUNCTIONS)
    has_sanitize = re.search(sanitize_pattern, content)
    if not has_sanitize:
        return [
            "⚠️  H1: Raw $_POST/$_GET/$_REQUEST access without sanitization.\n"
            "  Wrap user input with sanitize_text_field(), absint(), wp_kses(), etc."
        ]
    return []


def check_strict_types(content: str, file_path: str) -> list[str]:
    if file_path.endswith(".blade.php"):
        return []

    first_lines = content[:200]
    if re.search(r"<\?php\s+//\s*legacy", first_lines, re.IGNORECASE):
        return []

    if not re.search(r"declare\s*\(\s*strict_types\s*=\s*1\s*\)", content):
        return [
            "⚠️  M4: Missing declare(strict_types=1).\n"
            "  Add after opening <?php tag for type safety."
        ]
    return []


def check_function_exists(content: str) -> list[str]:
    matches = re.findall(r"function_exists\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", content)
    cross_plugin = [
        fn for fn in matches
        if not fn.startswith(WP_CORE_PREFIXES)
    ]
    if cross_plugin:
        fns = ", ".join(cross_plugin)
        return [
            f"⚠️  M8: function_exists() used for cross-plugin calls: {fns}\n"
            "  Prefer do_action()/apply_filters() hooks for cross-plugin integration."
        ]
    return []


def get_content(tool_name: str, tool_input: dict) -> str:
    if tool_name == "Write":
        return tool_input.get("content", "")

    # Edit: file already written to disk — read it for full context
    file_path = tool_input.get("file_path", "")
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

if not file_path.endswith(".php"):
    sys.exit(0)

content = get_content(tool_name, tool_input)
if not content:
    sys.exit(0)

warnings = [
    *check_ajax_security(content),
    *check_wpdb_prepare(content),
    *check_sanitization(content),
    *check_strict_types(content, file_path),
    *check_function_exists(content),
]

for warning in warnings:
    print(warning, file=sys.stderr)

sys.exit(0)
