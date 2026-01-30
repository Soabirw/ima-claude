---
name: "phpunit-wp"
description: "PHPUnit testing for WordPress plugins with FP principles - fast unit tests, minimal mocks, environment-aware setup"
triggers:
  - "phpunit"
  - "unit test"
  - "test wordpress"
  - "composer test"
  - "test bootstrap"
  - "mock wordpress"
---

# PHPUnit for WordPress Plugins

Expert guidance for PHPUnit testing in WordPress plugins, emphasizing pure function testing, minimal mocking, and FP principles.

## When to Use This Skill

- Setting up PHPUnit for new WordPress plugins
- Debugging silent/hanging test runs
- Writing testable pure functions
- Mocking WordPress functions correctly
- Testing with FP principles

## Core Philosophy

**Test pure functions, not WordPress integration.**

1. **Pure business logic** = Fast unit tests (<100ms, no WordPress)
2. **WordPress wrappers** = Integration tests (slower, full WP environment)
3. **Mock minimally** = Only mock what's needed for pure function context

**Foundation**: Reference `../php-fp/SKILL.md` and `../php-fp-wordpress/SKILL.md` for FP patterns.

---

## THE TWO CRITICAL SETUP BUGS (We Keep Forgetting!)

### 🐛 Bug #1: Silent PHPUnit Execution

**Symptom**: `composer test` produces ZERO output, not even "no tests found"

**Root Cause**: PHPUnit 9.x doesn't output anything without `--testdox` flag

**❌ BROKEN** (silent execution):
```json
{
    "scripts": {
        "test": "phpunit"
    }
}
```

**✅ FIXED** (visible output):
```json
{
    "scripts": {
        "test": "phpunit --colors=always --testdox",
        "test:coverage": "phpunit --coverage-html coverage"
    }
}
```

---

### 🐛 Bug #2: Autoload Files Kill Tests

**Symptom**: Tests hang or exit silently with no error message

**Root Cause**: Composer autoload runs BEFORE test bootstrap defines `ABSPATH`

**The Fatal Flow**:
```
1. bootstrap.php line 17: require vendor/autoload.php
2. Composer sees: "autoload": { "files": ["includes/helpers.php"] }
3. Composer loads helpers.php IMMEDIATELY
4. helpers.php line 14: if (!defined('ABSPATH')) { exit; }
5. ABSPATH not defined yet (happens bootstrap.php line 22)
6. Script exits silently
7. PHPUnit never starts
```

**❌ BROKEN** (causes silent exit):
```json
{
    "autoload": {
        "files": [
            "includes/helpers/url-validation.php",
            "includes/helpers/share-urls.php"
        ]
    }
}
```

**✅ FIXED** (no autoload files):
```json
{
    // NO autoload section with files array!
    // Bootstrap loads helpers manually AFTER defining ABSPATH
    "autoload-dev": {
        "psr-4": {
            "MyPlugin\\Tests\\": "tests/"
        }
    }
}
```

---

## Environment Setup

### Running Tests in Local WP Environment

**Important**: Composer and PHPUnit need Local WP's PHP environment. Git commands work in normal terminal.

**Use the project's configured Local WP environment**:

The `wp-local` skill provides the environment loader pattern. For composer/phpunit commands, create a similar wrapper or use the pattern directly:

```bash
# Pattern from wp-local skill:
# 1. Sources ~/kitty/load-localwp-env.sh with site name from $WP_LOCAL_SITE or .wp-local
# 2. Runs command in that environment

# Example - Run tests:
bash -c "source ~/kitty/load-localwp-env.sh \$(cat .wp-local || echo \$WP_LOCAL_SITE) && composer test"

# Or install dependencies:
bash -c "source ~/kitty/load-localwp-env.sh \$(cat .wp-local || echo \$WP_LOCAL_SITE) && composer install"
```

**Pro Tip**: Create a shell alias in your `~/.bashrc` or `~/.zshrc`:
```bash
alias wptest='bash -c "source ~/kitty/load-localwp-env.sh \$(cat .wp-local || echo \$WP_LOCAL_SITE) && composer test"'
alias wpcomposer='bash -c "source ~/kitty/load-localwp-env.sh \$(cat .wp-local || echo \$WP_LOCAL_SITE) && composer $@"'
```

Then simply:
```bash
wptest                    # Run tests
wpcomposer install       # Install dependencies
```

### Environment Configuration

**Priority order** (same as wp-local):
1. `$WP_LOCAL_SITE` environment variable (set by Kitty terminal)
2. `.wp-local` file in project root (site UUID like `19efkkzWB`)
3. Error if neither configured

**For git operations** (no environment needed):
```bash
# Regular terminal works fine - git doesn't need PHP environment
git status
git commit -m "fix: phpunit setup"
git push
```

### Quick Test Diagnosis

```bash
# 1. Check if bootstrap prints (should see "Bootstrap Loaded")
php tests/bootstrap.php

# 2. Check if PHPUnit is installed
ls -la vendor/bin/phpunit

# 3. Check composer.json scripts
cat composer.json | grep -A 3 scripts

# 4. Check for autoload files bug
cat composer.json | grep -A 5 autoload
```

---

## Copy-Paste Working Template

### composer.json
```json
{
    "name": "ima-network/my-plugin",
    "description": "Plugin description",
    "type": "wordpress-plugin",
    "license": "GPL-2.0-or-later",
    "require": {
        "php": ">=7.4"
    },
    "require-dev": {
        "phpunit/phpunit": "^9.5"
    },
    "autoload-dev": {
        "psr-4": {
            "MyPlugin\\Tests\\": "tests/"
        }
    },
    "scripts": {
        "test": "phpunit --colors=always --testdox",
        "test:coverage": "phpunit --coverage-html coverage"
    }
}
```

### phpunit.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/9.5/phpunit.xsd"
         bootstrap="tests/bootstrap.php"
         colors="true"
         verbose="true"
         stopOnFailure="false">
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
    </testsuites>
    <coverage>
        <include>
            <directory suffix=".php">includes</directory>
        </include>
        <exclude>
            <directory>tests</directory>
            <directory>templates</directory>
        </exclude>
    </coverage>
    <php>
        <ini name="error_reporting" value="E_ALL"/>
        <ini name="display_errors" value="true"/>
    </php>
</phpunit>
```

### tests/bootstrap.php
```php
<?php
/**
 * PHPUnit Bootstrap for My Plugin
 *
 * Loads pure functions for unit testing without WordPress dependencies.
 */
declare(strict_types=1);

// 1. Load Composer autoloader FIRST (but it won't autoload files - we removed that!)
require_once dirname(__DIR__) . '/vendor/autoload.php';

// 2. Define ABSPATH to prevent plugin file exits
if (!defined('ABSPATH')) {
    define('ABSPATH', '/tmp/wordpress/');
}

// 3. Define plugin constants
if (!defined('MY_PLUGIN_PATH')) {
    define('MY_PLUGIN_PATH', dirname(__DIR__) . '/');
}

// 4. NOW manually load helper files (AFTER ABSPATH defined!)
require_once MY_PLUGIN_PATH . 'includes/helpers/url-validation.php';
require_once MY_PLUGIN_PATH . 'includes/helpers/share-urls.php';

// 5. Mock WordPress functions minimally
if (!function_exists('home_url')) {
    function home_url(string $path = ''): string {
        return 'https://example.com' . $path;
    }
}

if (!function_exists('sanitize_text_field')) {
    function sanitize_text_field(string $str): string {
        $filtered = strip_tags($str);
        $filtered = str_replace(["\r", "\n"], '', $filtered);
        return trim($filtered);
    }
}

if (!function_exists('esc_html')) {
    function esc_html(string $text): string {
        return htmlspecialchars($text, ENT_QUOTES, 'UTF-8');
    }
}

// 6. Confirmation message (proves bootstrap loaded)
echo "✅ My Plugin Test Bootstrap Loaded\n";
```

---

## What to Test (FP Principles)

### ✅ DO TEST: Pure Business Logic

```php
<?php
// includes/helpers/validation.php
declare(strict_types=1);

/**
 * PURE function - Zero WordPress dependencies
 * Perfect for unit testing
 */
function my_plugin_validate_email_pure(string $email): array {
    if (empty($email)) {
        return ['valid' => false, 'error' => 'Email required'];
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        return ['valid' => false, 'error' => 'Invalid email format'];
    }

    // Check for disposable domains
    $disposable = ['tempmail.com', 'throwaway.email'];
    $domain = substr(strrchr($email, '@'), 1);
    if (in_array($domain, $disposable)) {
        return ['valid' => false, 'error' => 'Disposable email not allowed'];
    }

    return ['valid' => true];
}
```

**Test**:
```php
<?php
// tests/Unit/ValidationTest.php
use PHPUnit\Framework\TestCase;

class ValidationTest extends TestCase {
    public function test_empty_email_returns_error() {
        $result = my_plugin_validate_email_pure('');

        $this->assertFalse($result['valid']);
        $this->assertEquals('Email required', $result['error']);
    }

    public function test_invalid_format_returns_error() {
        $result = my_plugin_validate_email_pure('not-an-email');

        $this->assertFalse($result['valid']);
        $this->assertEquals('Invalid email format', $result['error']);
    }

    public function test_disposable_email_rejected() {
        $result = my_plugin_validate_email_pure('user@tempmail.com');

        $this->assertFalse($result['valid']);
        $this->assertEquals('Disposable email not allowed', $result['error']);
    }

    public function test_valid_email_passes() {
        $result = my_plugin_validate_email_pure('user@example.com');

        $this->assertTrue($result['valid']);
        $this->assertArrayNotHasKey('error', $result);
    }

    // FP Principle: Test determinism
    public function test_function_is_deterministic() {
        $email = 'test@example.com';
        $result1 = my_plugin_validate_email_pure($email);
        $result2 = my_plugin_validate_email_pure($email);

        $this->assertEquals($result1, $result2);
    }
}
```

---

### ❌ DON'T TEST: WordPress Integration Wrappers

```php
<?php
// includes/ajax-handlers.php - WordPress wrapper
function my_plugin_ajax_validate_email() {
    // DON'T unit test this - it's all WordPress integration!
    check_ajax_referer('validate_email_nonce', 'nonce');

    if (!current_user_can('read')) {
        wp_send_json_error('Unauthorized', 403);
    }

    $email = sanitize_email($_POST['email']);

    // Call pure function (which IS tested)
    $result = my_plugin_validate_email_pure($email);

    wp_send_json_success($result);
}
add_action('wp_ajax_my_plugin_validate_email', 'my_plugin_ajax_validate_email');
```

**Why not test**: This is 100% WordPress integration. Testing it requires:
- Full WordPress environment
- Mocking `$_POST`, nonces, capabilities, AJAX functions
- Complex setup that's brittle and slow

**Better approach**:
- Unit test the pure function (`my_plugin_validate_email_pure`) ✅
- Integration test the AJAX handler with real WordPress (separate test suite)

---

## Mocking Rules (Minimal Philosophy)

### Mock Only What's Needed for Pure Context

**❌ DON'T over-mock**:
```php
<?php
// Excessive mocking for a pure function test
if (!function_exists('wp_remote_post')) { /* ... */ }
if (!function_exists('wp_remote_get')) { /* ... */ }
if (!function_exists('get_option')) { /* ... */ }
if (!function_exists('update_option')) { /* ... */ }
if (!function_exists('delete_option')) { /* ... */ }
// ... 50 more mocks you don't need
```

**✅ DO mock minimally**:
```php
<?php
// Only mock what pure functions actually use
if (!function_exists('sanitize_text_field')) {
    function sanitize_text_field(string $str): string {
        return trim(strip_tags($str));
    }
}

if (!function_exists('home_url')) {
    function home_url(string $path = ''): string {
        return 'https://example.com' . $path;
    }
}
```

### Common WordPress Mocks for Pure Functions

```php
<?php
// WordPress utility functions (pure-ish)
if (!function_exists('wp_parse_args')) {
    function wp_parse_args($args, $defaults = []): array {
        if (is_string($args)) {
            parse_str($args, $parsed_args);
            $args = $parsed_args;
        }
        return array_merge($defaults, (array) $args);
    }
}

// Sanitization functions
if (!function_exists('sanitize_email')) {
    function sanitize_email(string $email): string {
        return strtolower(trim($email));
    }
}

if (!function_exists('esc_url_raw')) {
    function esc_url_raw(string $url): string {
        return filter_var($url, FILTER_SANITIZE_URL) ?: '';
    }
}

// URL parsing (WordPress wrapper for parse_url)
if (!function_exists('wp_parse_url')) {
    function wp_parse_url(string $url, int $component = -1) {
        return $component === -1 ? parse_url($url) : parse_url($url, $component);
    }
}
```

---

## Test Organization Patterns

### Pattern 1: Pure Function Testing (Fastest)

```
tests/
└── Unit/
    ├── ValidationTest.php      # Pure validation functions
    ├── CalculationTest.php     # Pure calculation logic
    └── FormatterTest.php       # Pure formatting functions
```

**Characteristics**:
- No WordPress dependencies
- Fast (<100ms total)
- No database, no HTTP, no filesystem
- Run on every commit

### Pattern 2: Integration Testing (Slower)

```
tests/
└── Integration/
    ├── AjaxHandlerTest.php     # Full WordPress + AJAX
    ├── ShortcodeTest.php       # Full WordPress + rendering
    └── DatabaseTest.php        # Full WordPress + DB
```

**Characteristics**:
- Requires full WordPress installation
- Uses WP_UnitTestCase from wordpress-develop
- Slower (seconds to minutes)
- Run before releases

---

## Testing Patterns by Function Type

### Pure Calculations
```php
<?php
function calculate_discount_pure(float $price, float $rate): float {
    return round($price * (1 - $rate), 2);
}

// Test: Assert exact values
$this->assertEquals(90.0, calculate_discount_pure(100.0, 0.10));
$this->assertEquals(95.0, calculate_discount_pure(100.0, 0.05));
```

### Pure Validation
```php
<?php
function validate_age_pure(int $age): array {
    if ($age < 0) return ['valid' => false, 'error' => 'Negative age'];
    if ($age < 18) return ['valid' => false, 'error' => 'Must be 18+'];
    return ['valid' => true];
}

// Test: Assert result structure
$result = validate_age_pure(15);
$this->assertFalse($result['valid']);
$this->assertArrayHasKey('error', $result);
```

### Pure Transformations
```php
<?php
function format_phone_pure(string $phone): string {
    $digits = preg_replace('/\D/', '', $phone);
    if (strlen($digits) === 10) {
        return sprintf('(%s) %s-%s',
            substr($digits, 0, 3),
            substr($digits, 3, 3),
            substr($digits, 6, 4)
        );
    }
    return $phone;
}

// Test: Assert transformations
$this->assertEquals('(555) 123-4567', format_phone_pure('5551234567'));
$this->assertEquals('(555) 123-4567', format_phone_pure('555-123-4567'));
$this->assertEquals('invalid', format_phone_pure('invalid'));
```

---

## Performance Testing (FP Principle)

Pure functions enable easy performance testing:

```php
<?php
public function test_performance_fast_execution() {
    $iterations = 10000;
    $start = microtime(true);

    for ($i = 0; $i < $iterations; $i++) {
        my_plugin_validate_email_pure('user@example.com');
    }

    $elapsed = microtime(true) - $start;

    // Should complete 10k validations in < 100ms
    $this->assertLessThan(0.1, $elapsed);
}
```

---

## Common Anti-Patterns

### ❌ Testing Private Methods

```php
<?php
// DON'T use reflection to test private methods
class MyTest extends TestCase {
    public function test_private_method() {
        $reflection = new ReflectionClass(MyClass::class);
        $method = $reflection->getMethod('privateMethod');
        $method->setAccessible(true);
        // ...
    }
}

// DO extract pure function and test that
function my_plugin_process_data_pure(array $data): array {
    // Extracted logic, now testable
    return $data;
}
```

### ❌ Testing Implementation Details

```php
<?php
// DON'T test internal variable values
public function test_internal_state() {
    $obj = new MyClass();
    $this->assertEquals(5, $obj->internalCounter); // Brittle!
}

// DO test public behavior
public function test_public_behavior() {
    $result = my_plugin_process_items(['a', 'b', 'c']);
    $this->assertCount(3, $result);
}
```

### ❌ Over-Mocking

```php
<?php
// DON'T mock everything
$mock = $this->createMock(Database::class);
$mock->method('query')->willReturn([]);
$mock->method('insert')->willReturn(1);
$mock->method('update')->willReturn(true);
// ... 20 more mocks

// DO test pure functions that don't need mocks
function process_results_pure(array $results): array {
    return array_map('strtoupper', $results);
}
```

---

## Quality Gates

Before merging:
- [ ] `composer test` produces visible output (not silent)
- [ ] Bootstrap prints "Bootstrap Loaded" message
- [ ] Tests run in < 100ms for pure functions
- [ ] No autoload files section in composer.json
- [ ] Pure business logic separated from WordPress wrappers
- [ ] Mock count is minimal (< 10 functions)
- [ ] Test assertions are deterministic (no flaky tests)

---

## Working Examples

**Reference plugins with working tests**:
```bash
# ima-forms: Gold standard
cd wp-content/plugins/ima-forms
composer test

# ima-shortcodes: Recently fixed
cd wp-content/plugins/ima-shortcodes
composer test
```

---

## Troubleshooting

### Issue: Silent test execution

**Symptom**: `composer test` produces no output

**Fix**: Add `--testdox` flag to composer.json scripts

### Issue: Tests hang/exit silently

**Symptom**: Process hangs or exits without error

**Diagnosis**:
```bash
# Check if bootstrap runs
php tests/bootstrap.php

# Check for autoload files bug
cat composer.json | grep -A 5 autoload
```

**Fix**: Remove autoload files section, load manually in bootstrap

### Issue: "Class not found" errors

**Symptom**: PHPUnit can't find test classes

**Fix**: Check `autoload-dev` PSR-4 mapping in composer.json:
```json
"autoload-dev": {
    "psr-4": {
        "MyPlugin\\Tests\\": "tests/"
    }
}
```

Then run: `composer dump-autoload`

---

## References

- `../php-fp/SKILL.md` - Core FP principles
- `../php-fp-wordpress/SKILL.md` - WordPress security + FP
- `../wp-local/SKILL.md` - Local WP environment handling
- PHPUnit docs: https://phpunit.de/documentation.html
- WordPress test suite: https://make.wordpress.org/core/handbook/testing/automated-testing/phpunit/

---

**Last Updated**: 2026-01-29
**Discovery**: After debugging the same bugs across multiple plugins (ima-forms, ima-shortcodes, ima-access-control)
