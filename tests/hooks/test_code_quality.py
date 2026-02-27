"""
Tests for code quality PostToolUse hooks.

Each hook is tested with:
  - should-fire: content that triggers the warning (stderr contains expected keyword, exit 0)
  - should-not-fire: clean content, no issues (stderr empty or no keyword, exit 0)
  - wrong file extension: non-target extension is silently ignored
  - wrong tool_name: Read tool is silently ignored
"""
import json
import subprocess
import textwrap
import pytest
from pathlib import Path

HOOKS_DIR = Path(__file__).parent.parent.parent / "plugins" / "ima-claude" / "hooks"


# ---------------------------------------------------------------------------
# wp_security_check.py
#
# Write mode: reads tool_input["content"]
# Edit mode:  reads the file at tool_input["file_path"] from disk
#             (new_string is NOT used — the hook opens the file directly)
# ---------------------------------------------------------------------------


class TestWpSecurityCheck:
    HOOK = "wp_security_check.py"

    def _write_input(self, file_path: str, content: str) -> dict:
        return {
            "tool_name": "Write",
            "tool_input": {"file_path": file_path, "content": content},
        }

    def _edit_input(self, file_path: str) -> dict:
        """Edit mode reads the file from disk; new_string is not used."""
        return {
            "tool_name": "Edit",
            "tool_input": {"file_path": file_path, "new_string": ""},
        }

    # --- ajax nonce check ---

    def test_ajax_missing_nonce_fires(self, run_hook, tmp_path):
        php = tmp_path / "handler.php"
        php.write_text("<?php\nadd_action('wp_ajax_my_action', 'my_handler');\nfunction my_handler() {}\n")
        result = run_hook(self.HOOK, self._edit_input(str(php)))
        assert result.returncode == 0
        assert "nonce" in result.stderr

    def test_ajax_with_nonce_no_nonce_warning(self, run_hook, tmp_path):
        php = tmp_path / "handler.php"
        php.write_text(textwrap.dedent("""\
            <?php
            declare(strict_types=1);
            add_action('wp_ajax_my_action', 'my_handler');
            function my_handler() {
                check_ajax_referer('my-nonce', 'nonce');
                current_user_can('manage_options');
            }
        """))
        result = run_hook(self.HOOK, self._edit_input(str(php)))
        assert result.returncode == 0
        assert "nonce" not in result.stderr

    # --- wpdb prepare check ---

    def test_wpdb_without_prepare_fires(self, run_hook):
        content = "<?php\ndeclare(strict_types=1);\n$wpdb->query(\"SELECT * FROM {$wpdb->posts}\");\n"
        result = run_hook(self.HOOK, self._write_input("/var/www/plugin.php", content))
        assert result.returncode == 0
        assert "prepare" in result.stderr

    def test_wpdb_with_prepare_no_warning(self, run_hook):
        content = "<?php\ndeclare(strict_types=1);\n$wpdb->query($wpdb->prepare('SELECT * FROM %s', $table));\n"
        result = run_hook(self.HOOK, self._write_input("/var/www/plugin.php", content))
        assert result.returncode == 0
        assert "prepare" not in result.stderr

    # --- sanitization check ---

    def test_raw_post_without_sanitize_fires(self, run_hook):
        content = "<?php\ndeclare(strict_types=1);\n$name = $_POST['name'];\n"
        result = run_hook(self.HOOK, self._write_input("/var/www/plugin.php", content))
        assert result.returncode == 0
        assert "sanitiz" in result.stderr

    def test_post_with_sanitize_no_warning(self, run_hook):
        content = "<?php\ndeclare(strict_types=1);\n$name = sanitize_text_field($_POST['name']);\n"
        result = run_hook(self.HOOK, self._write_input("/var/www/plugin.php", content))
        assert result.returncode == 0
        assert "sanitiz" not in result.stderr

    # --- strict_types check ---

    def test_missing_strict_types_fires(self, run_hook):
        content = "<?php\necho 'hello';\n"
        result = run_hook(self.HOOK, self._write_input("/var/www/plugin.php", content))
        assert result.returncode == 0
        assert "strict_types" in result.stderr

    def test_has_strict_types_no_warning(self, run_hook):
        content = "<?php\ndeclare(strict_types=1);\necho 'hello';\n"
        result = run_hook(self.HOOK, self._write_input("/var/www/plugin.php", content))
        assert result.returncode == 0
        assert "strict_types" not in result.stderr

    def test_blade_php_skips_strict_types(self, run_hook):
        content = "{{ $name }}"
        result = run_hook(self.HOOK, self._write_input("/var/www/views/page.blade.php", content))
        assert result.returncode == 0
        assert "strict_types" not in result.stderr

    # --- function_exists cross-plugin check ---

    def test_function_exists_cross_plugin_fires(self, run_hook):
        content = "<?php\ndeclare(strict_types=1);\nif (function_exists('acf_add_local_field_group')) {}\n"
        result = run_hook(self.HOOK, self._write_input("/var/www/plugin.php", content))
        assert result.returncode == 0
        assert "function_exists" in result.stderr

    def test_function_exists_wp_core_no_warning(self, run_hook):
        content = "<?php\ndeclare(strict_types=1);\nif (function_exists('wp_enqueue_scripts')) {}\n"
        result = run_hook(self.HOOK, self._write_input("/var/www/plugin.php", content))
        assert result.returncode == 0
        assert "function_exists" not in result.stderr

    # --- extension / tool gating ---

    def test_wrong_extension_ignored(self, run_hook):
        content = "SELECT * FROM users;"
        result = run_hook(self.HOOK, self._write_input("/var/www/query.js", content))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_read_tool_ignored(self, run_hook):
        result = run_hook(self.HOOK, {
            "tool_name": "Read",
            "tool_input": {"file_path": "/var/www/plugin.php", "content": "<?php echo 1;"},
        })
        assert result.returncode == 0
        assert result.stderr == ""


# ---------------------------------------------------------------------------
# sql_injection_check.py
#
# Edit mode: reads tool_input["new_string"]
# Write mode: reads tool_input["content"]
# ---------------------------------------------------------------------------


class TestSqlInjectionCheck:
    HOOK = "sql_injection_check.py"

    def _write_input(self, file_path: str, content: str) -> dict:
        return {
            "tool_name": "Write",
            "tool_input": {"file_path": file_path, "content": content},
        }

    def _edit_input(self, file_path: str, new_string: str) -> dict:
        return {
            "tool_name": "Edit",
            "tool_input": {"file_path": file_path, "new_string": new_string},
        }

    def test_template_literal_sql_fires(self, run_hook):
        code = "const q = `SELECT * FROM users WHERE id = ${userId}`;"
        result = run_hook(self.HOOK, self._write_input("/app/db.js", code))
        assert result.returncode == 0
        assert "SQL" in result.stderr

    def test_string_concat_sql_fires(self, run_hook):
        code = "const q = 'SELECT * FROM users WHERE name = ' + name;"
        result = run_hook(self.HOOK, self._edit_input("/app/db.ts", code))
        assert result.returncode == 0
        assert "SQL" in result.stderr

    def test_parameterized_query_no_warning(self, run_hook):
        code = "const result = await db.query('SELECT * FROM users WHERE id = ?', [userId]);"
        result = run_hook(self.HOOK, self._write_input("/app/db.ts", code))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_non_sql_template_literal_no_warning(self, run_hook):
        code = "const msg = `Hello, ${name}! Welcome to the site.`;"
        result = run_hook(self.HOOK, self._write_input("/app/utils.js", code))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_wrong_extension_ignored(self, run_hook):
        code = "const q = `SELECT * FROM users WHERE id = ${userId}`;"
        result = run_hook(self.HOOK, self._write_input("/app/db.php", code))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_read_tool_ignored(self, run_hook):
        result = run_hook(self.HOOK, {
            "tool_name": "Read",
            "tool_input": {
                "file_path": "/app/db.js",
                "content": "const q = `SELECT * FROM users WHERE id = ${userId}`;",
            },
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_mjs_extension_fires(self, run_hook):
        code = "const q = `DELETE FROM sessions WHERE token = ${token}`;"
        result = run_hook(self.HOOK, self._write_input("/app/auth.mjs", code))
        assert result.returncode == 0
        assert "SQL" in result.stderr

    def test_edit_new_string_used(self, run_hook):
        """Edit mode should scan new_string, not content (content key doesn't exist)."""
        result = run_hook(self.HOOK, {
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "/app/db.js",
                "new_string": "const q = `INSERT INTO logs WHERE session = ${s}`;",
            },
        })
        assert result.returncode == 0
        assert "SQL" in result.stderr


# ---------------------------------------------------------------------------
# fp_utility_check.py
#
# Edit mode: reads tool_input["new_string"]
# Write mode: reads tool_input["content"]
# ---------------------------------------------------------------------------


class TestFpUtilityCheck:
    HOOK = "fp_utility_check.py"

    def _write_input(self, file_path: str, content: str) -> dict:
        return {
            "tool_name": "Write",
            "tool_input": {"file_path": file_path, "content": content},
        }

    def _edit_input(self, file_path: str, new_string: str) -> dict:
        return {
            "tool_name": "Edit",
            "tool_input": {"file_path": file_path, "new_string": new_string},
        }

    def test_pipe_with_reduce_fires(self, run_hook):
        code = "const pipe = (...fns) => fns.reduce((f, g) => (...args) => g(f(...args)));"
        result = run_hook(self.HOOK, self._write_input("/app/utils.js", code))
        assert result.returncode == 0
        assert "FP utility" in result.stderr

    def test_curry_definition_fires(self, run_hook):
        code = "const curry = fn => (...args) => args.length >= fn.length ? fn(...args) : curry(fn.bind(null, ...args));"
        result = run_hook(self.HOOK, self._write_input("/app/utils.ts", code))
        assert result.returncode == 0
        assert "FP utility" in result.stderr

    def test_maybe_monad_fires(self, run_hook):
        code = "class Maybe {\n  constructor(val) { this.val = val; }\n  map(fn) { return this.val ? Maybe.of(fn(this.val)) : this; }\n}"
        result = run_hook(self.HOOK, self._write_input("/app/fp.js", code))
        assert result.returncode == 0
        assert "FP utility" in result.stderr

    def test_either_monad_fires(self, run_hook):
        code = "class Either { static left(val) { return new Left(val); } }"
        result = run_hook(self.HOOK, self._write_input("/app/fp.ts", code))
        assert result.returncode == 0
        assert "FP utility" in result.stderr

    def test_php_pipe_fires(self, run_hook):
        code = "<?php\nfunction pipe($value, ...$fns) { return array_reduce($fns, fn($v, $f) => $f($v), $value); }"
        result = run_hook(self.HOOK, self._write_input("/app/helpers.php", code))
        assert result.returncode == 0
        assert "FP utility" in result.stderr

    def test_clean_code_no_warning(self, run_hook):
        code = textwrap.dedent("""\
            const double = x => x * 2;
            const addOne = x => x + 1;
            const result = [1, 2, 3].map(double).map(addOne);
        """)
        result = run_hook(self.HOOK, self._write_input("/app/utils.js", code))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_import_of_pipe_no_warning(self, run_hook):
        """Importing pipe from a library is fine; only defining it triggers the hook."""
        code = "import { pipe } from 'ramda';\nconst process = pipe(trim, toLower);"
        result = run_hook(self.HOOK, self._write_input("/app/utils.js", code))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_wrong_extension_ignored(self, run_hook):
        code = "const pipe = (...fns) => fns.reduce((f, g) => x => g(f(x)));"
        result = run_hook(self.HOOK, self._write_input("/app/utils.txt", code))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_read_tool_ignored(self, run_hook):
        result = run_hook(self.HOOK, {
            "tool_name": "Read",
            "tool_input": {
                "file_path": "/app/utils.js",
                "content": "const pipe = (...fns) => fns.reduce((f, g) => x => g(f(x)));",
            },
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_edit_new_string_used(self, run_hook):
        result = run_hook(self.HOOK, {
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "/app/utils.js",
                "new_string": "const compose = (...fns) => fns.reduceRight((f, g) => x => g(f(x)));",
            },
        })
        assert result.returncode == 0
        assert "FP utility" in result.stderr


# ---------------------------------------------------------------------------
# jquery_in_wordpress.py
#
# Write mode: uses tool_input["content"] for both WP context signals and vanilla DOM
# Edit mode:  reads disk file for WP context; uses tool_input["new_string"] for vanilla DOM
# ---------------------------------------------------------------------------


class TestJqueryInWordpress:
    HOOK = "jquery_in_wordpress.py"

    def _write_input(self, file_path: str, content: str) -> dict:
        return {
            "tool_name": "Write",
            "tool_input": {"file_path": file_path, "content": content},
        }

    def test_vanilla_dom_in_wp_path_fires(self, run_hook):
        content = "document.querySelector('.btn').addEventListener('click', handler);"
        result = run_hook(self.HOOK, self._write_input(
            "/var/www/wp-content/plugins/my-plugin/assets/app.js", content
        ))
        assert result.returncode == 0
        assert "jQuery" in result.stderr

    def test_vanilla_dom_with_jquery_content_signal_fires(self, run_hook):
        content = textwrap.dedent("""\
            jQuery(document).ready(function($) {
                document.querySelector('#app').addEventListener('click', handler);
            });
        """)
        result = run_hook(self.HOOK, self._write_input("/var/www/assets/app.js", content))
        assert result.returncode == 0
        assert "jQuery" in result.stderr

    def test_jquery_usage_no_vanilla_dom_no_warning(self, run_hook):
        content = textwrap.dedent("""\
            (function($) {
                $('#btn').on('click', function() { $(this).toggleClass('active'); });
            })(jQuery);
        """)
        result = run_hook(self.HOOK, self._write_input(
            "/var/www/wp-content/plugins/my-plugin/app.js", content
        ))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_vanilla_dom_outside_wp_context_no_warning(self, run_hook):
        content = "document.querySelector('#app').addEventListener('click', handler);"
        result = run_hook(self.HOOK, self._write_input("/var/www/react-app/src/main.js", content))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_wrong_extension_ignored(self, run_hook):
        content = "document.querySelector('.btn').addEventListener('click', handler);"
        result = run_hook(self.HOOK, self._write_input(
            "/var/www/wp-content/plugins/my-plugin/app.ts", content
        ))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_read_tool_ignored(self, run_hook):
        result = run_hook(self.HOOK, {
            "tool_name": "Read",
            "tool_input": {
                "file_path": "/var/www/wp-content/plugins/my-plugin/app.js",
                "content": "document.querySelector('.btn').addEventListener('click', handler);",
            },
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_edit_mode_wp_path_with_vanilla_dom_fires(self, run_hook, tmp_path):
        """Edit mode: WP context comes from the path; vanilla DOM from new_string."""
        js_file = tmp_path / "app.js"
        js_file.write_text("// existing file\n")
        # The path must contain wp-content/plugins for detection by path
        wp_path = "/var/www/wp-content/plugins/my-plugin/app.js"
        result = run_hook(self.HOOK, {
            "tool_name": "Edit",
            "tool_input": {
                "file_path": wp_path,
                "new_string": "document.getElementById('modal').addEventListener('click', open);",
            },
        })
        assert result.returncode == 0
        assert "jQuery" in result.stderr

    def test_getelementbyid_fires(self, run_hook):
        content = "document.getElementById('nav').addEventListener('click', toggle);"
        result = run_hook(self.HOOK, self._write_input(
            "/var/www/wp-content/themes/my-theme/js/main.js", content
        ))
        assert result.returncode == 0
        assert "jQuery" in result.stderr


# ---------------------------------------------------------------------------
# bootstrap_utility_check.py
#
# Edit mode: reads tool_input["new_string"]
# Write mode: reads tool_input["content"]
# CSS/SCSS files only fire when Bootstrap context signals are present in the content.
# HTML/PHP files always fire when inline styles are detected.
# ---------------------------------------------------------------------------


class TestBootstrapUtilityCheck:
    HOOK = "bootstrap_utility_check.py"

    def _write_input(self, file_path: str, content: str) -> dict:
        return {
            "tool_name": "Write",
            "tool_input": {"file_path": file_path, "content": content},
        }

    def _edit_input(self, file_path: str, new_string: str) -> dict:
        return {
            "tool_name": "Edit",
            "tool_input": {"file_path": file_path, "new_string": new_string},
        }

    def test_inline_margin_in_php_fires(self, run_hook):
        content = '<div style="margin-top: 16px">Hello</div>'
        result = run_hook(self.HOOK, self._write_input("/var/www/template.php", content))
        assert result.returncode == 0
        assert "Bootstrap" in result.stderr

    def test_inline_padding_in_html_fires(self, run_hook):
        content = '<section style="padding: 24px">Content</section>'
        result = run_hook(self.HOOK, self._write_input("/var/www/page.html", content))
        assert result.returncode == 0
        assert "Bootstrap" in result.stderr

    def test_inline_display_flex_fires(self, run_hook):
        content = '<div style="display: flex; gap: 8px">Items</div>'
        result = run_hook(self.HOOK, self._write_input("/var/www/layout.html", content))
        assert result.returncode == 0
        assert "Bootstrap" in result.stderr

    def test_inline_text_center_fires(self, run_hook):
        content = '<h1 style="text-align: center">Title</h1>'
        result = run_hook(self.HOOK, self._write_input("/var/www/page.php", content))
        assert result.returncode == 0
        assert "Bootstrap" in result.stderr

    def test_clean_html_no_warning(self, run_hook):
        content = '<div class="mt-3 d-flex text-center">Clean markup</div>'
        result = run_hook(self.HOOK, self._write_input("/var/www/page.html", content))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_scss_with_bootstrap_import_fires(self, run_hook):
        # The hook's INLINE_STYLE_PATTERNS match style="..." HTML attribute syntax.
        # CSS/SCSS files must contain both a Bootstrap context signal AND an inline
        # style attribute (e.g. inside a Twig/Blade partial mixed into a .scss file,
        # or more realistically an HTML snippet) to trigger.
        content = textwrap.dedent("""\
            @import 'bootstrap/scss/bootstrap';
            /* component override */
            <div style="margin-top: 16px">Use mt-3 instead</div>
        """)
        result = run_hook(self.HOOK, self._write_input("/var/www/styles.scss", content))
        assert result.returncode == 0
        assert "Bootstrap" in result.stderr

    def test_css_without_bootstrap_context_no_warning(self, run_hook):
        """CSS files without Bootstrap context signal should be silently skipped."""
        content = ".card { margin-top: 16px; padding: 8px; }"
        result = run_hook(self.HOOK, self._write_input("/var/www/styles.css", content))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_css_with_bootstrap_context_fires(self, run_hook):
        # Bootstrap context is detected; inline style attribute triggers the warning.
        content = "@import 'bootstrap';\n<div style=\"padding: 8px\">Use p-2 instead</div>"
        result = run_hook(self.HOOK, self._write_input("/var/www/styles.css", content))
        assert result.returncode == 0
        assert "Bootstrap" in result.stderr

    def test_wrong_extension_ignored(self, run_hook):
        content = '<div style="margin: 20px">Hello</div>'
        result = run_hook(self.HOOK, self._write_input("/var/www/template.js", content))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_read_tool_ignored(self, run_hook):
        result = run_hook(self.HOOK, {
            "tool_name": "Read",
            "tool_input": {
                "file_path": "/var/www/page.html",
                "content": '<div style="margin: 20px">Hello</div>',
            },
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_edit_new_string_used(self, run_hook):
        result = run_hook(self.HOOK, self._edit_input(
            "/var/www/template.php",
            '<p style="font-weight: bold">Important</p>',
        ))
        assert result.returncode == 0
        assert "Bootstrap" in result.stderr


# ---------------------------------------------------------------------------
# composer_autoload_check.py
#
# Write mode: reads tool_input["content"] directly (JSON string)
# Edit mode:  reads the file at tool_input["file_path"] from disk
# Only fires on files named composer.json
# ---------------------------------------------------------------------------


class TestComposerAutoloadCheck:
    HOOK = "composer_autoload_check.py"

    def _write_input(self, file_path: str, content: str) -> dict:
        return {
            "tool_name": "Write",
            "tool_input": {"file_path": file_path, "content": content},
        }

    def _composer_json_with_files(self) -> str:
        return json.dumps({
            "name": "my/plugin",
            "autoload": {
                "files": ["src/helpers.php"],
                "classmap": ["src/"],
            },
        })

    def _composer_json_clean(self) -> str:
        return json.dumps({
            "name": "my/plugin",
            "autoload": {
                "classmap": ["src/"],
                "psr-4": {"MyPlugin\\": "src/"},
            },
        })

    def test_autoload_files_fires(self, run_hook):
        result = run_hook(self.HOOK, self._write_input(
            "/var/www/composer.json", self._composer_json_with_files()
        ))
        assert result.returncode == 0
        assert "autoload" in result.stderr.lower()

    def test_clean_composer_no_warning(self, run_hook):
        result = run_hook(self.HOOK, self._write_input(
            "/var/www/composer.json", self._composer_json_clean()
        ))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_empty_files_array_no_warning(self, run_hook):
        content = json.dumps({
            "name": "my/plugin",
            "autoload": {"files": [], "classmap": ["src/"]},
        })
        result = run_hook(self.HOOK, self._write_input("/var/www/composer.json", content))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_wrong_filename_ignored(self, run_hook):
        """Non-composer.json files are ignored even with matching content."""
        result = run_hook(self.HOOK, self._write_input(
            "/var/www/package.json", self._composer_json_with_files()
        ))
        assert result.returncode == 0
        assert result.stderr == ""

    def test_read_tool_ignored(self, run_hook):
        result = run_hook(self.HOOK, {
            "tool_name": "Read",
            "tool_input": {
                "file_path": "/var/www/composer.json",
                "content": self._composer_json_with_files(),
            },
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_edit_mode_reads_disk(self, run_hook, tmp_path):
        """Edit mode reads the file from disk, not from new_string."""
        composer = tmp_path / "composer.json"
        composer.write_text(self._composer_json_with_files())
        result = run_hook(self.HOOK, {
            "tool_name": "Edit",
            "tool_input": {
                "file_path": str(composer),
                "new_string": "{}",  # new_string is irrelevant for Edit mode
            },
        })
        assert result.returncode == 0
        assert "autoload" in result.stderr.lower()

    def test_edit_mode_clean_file_no_warning(self, run_hook, tmp_path):
        composer = tmp_path / "composer.json"
        composer.write_text(self._composer_json_clean())
        result = run_hook(self.HOOK, {
            "tool_name": "Edit",
            "tool_input": {
                "file_path": str(composer),
                "new_string": "{}",
            },
        })
        assert result.returncode == 0
        assert result.stderr == ""

    def test_invalid_json_no_crash(self, run_hook):
        result = run_hook(self.HOOK, self._write_input(
            "/var/www/composer.json", "not valid json {"
        ))
        assert result.returncode == 0
        assert result.stderr == ""
