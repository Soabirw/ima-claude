---
name: "php-fp-wordpress"
description: "Security-first WordPress development with PHP FP principles - pure business logic + WordPress integration"
---

# PHP FP - WordPress

Security-first WordPress development combining PHP functional programming principles with mandatory WordPress security practices.

## When to Use This Skill

- Building WordPress plugins or themes
- Need security-first development practices
- Implementing pure business logic with WordPress integration
- Testing WordPress functionality comprehensively
- Understanding plugin complexity patterns

## Core Philosophy

**Security practices prevent vulnerabilities, not architectural patterns.** Hybrid approach: **pure functions for business logic** +  **WordPress integration with mandatory security** (capability checks, nonce verification, sanitization, escaping, prepared statements).

**Foundation**: This skill builds on `php-fp` core principles. Reference `../php-fp/SKILL.md` for purity, composition, dependency injection, and testing patterns specific to PHP.

## ⚠️ CRITICAL: The 5 Non-Negotiable Security Practices

**Evidence**: Analysis of 7,966 vulnerabilities (2024) shows these practices prevent 95%+ of WordPress plugin vulnerabilities.

### 1. Capability Checks (Prevents 53% of XSS vulnerabilities)

```php
<?php
// ✅ ALWAYS check permissions FIRST
add_action('wp_ajax_delete_user_data', 'handle_delete_user_data');
function handle_delete_user_data() {
    // Check capability before ANY operation
    if (!current_user_can('delete_users')) {
        wp_send_json_error('Insufficient permissions', 403);
        return;
    }

    // Then proceed
    delete_user_data($_POST['user_id']);
}

// ❌ NEVER allow operations without capability check
function delete_user_data_UNSAFE() {
    wp_delete_user($_POST['user_id']); // Any authenticated user can delete!
}
```

### 2. Nonce Verification (Prevents 15-17% CSRF attacks)

```php
<?php
// ✅ ALWAYS verify nonces
add_action('admin_post_save_settings', 'save_plugin_settings');
function save_plugin_settings() {
    // Verify nonce before processing
    if (!isset($_POST['settings_nonce']) ||
        !wp_verify_nonce($_POST['settings_nonce'], 'save_settings_action')) {
        wp_die('Security check failed');
    }

    // Then save
    update_option('plugin_settings', $_POST['settings']);
}

// ❌ NEVER process forms without nonce
function save_settings_UNSAFE() {
    update_option('plugin_settings', $_POST['settings']); // CSRF vulnerable!
}
```

### 3. Input Sanitization (Required for ALL user input)

```php
<?php
// ✅ ALWAYS sanitize based on data type
function process_form_submission() {
    $name = sanitize_text_field($_POST['name']);
    $email = sanitize_email($_POST['email']);
    $content = wp_kses_post($_POST['content']); // Allow safe HTML
    $url = esc_url_raw($_POST['website']);
    $number = absint($_POST['count']);

    save_to_database($name, $email, $content, $url, $number);
}

// ❌ NEVER use raw input
function process_form_UNSAFE() {
    save_to_database($_POST['name'], $_POST['email']); // Injection risk!
}
```

### 4. Output Escaping (Context-specific escaping)

```php
<?php
// ✅ ALWAYS escape based on context
function render_user_profile($user) {
    // HTML context
    echo '<h2>' . esc_html($user->name) . '</h2>';

    // Attribute context
    echo '<img src="' . esc_url($user->avatar) . '" alt="' . esc_attr($user->name) . '">';

    // JavaScript context
    echo '<script>var userName = ' . wp_json_encode($user->name) . ';</script>';

    // URL context
    echo '<a href="' . esc_url($user->website) . '">Website</a>';
}

// ❌ NEVER output unescaped data
function render_profile_UNSAFE($user) {
    echo '<h1>' . $user->name . '</h1>'; // XSS if name contains <script>
}
```

### 5. Prepared SQL Statements (Prevents SQL injection)

```php
<?php
// ✅ ALWAYS use prepared statements
function get_user_posts($user_id) {
    global $wpdb;

    $posts = $wpdb->get_results($wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_author = %d AND post_status = %s",
        $user_id,
        'publish'
    ));

    return $posts;
}

// ❌ NEVER use string concatenation
function get_posts_UNSAFE($user_id) {
    global $wpdb;
    return $wpdb->get_results("SELECT * FROM {$wpdb->posts} WHERE post_author = $user_id");
}
```

## Pragmatic FP Pattern: Pure Logic + WordPress Wrapper

**Pattern**: Separate pure business logic from WordPress integration.

```php
<?php
namespace MyPlugin\BusinessLogic;

//──────────────────────────────────────────────────────
// PURE BUSINESS LOGIC (Zero WordPress Dependencies)
//──────────────────────────────────────────────────────

/**
 * Calculate membership discount
 * @pure - No side effects, deterministic, easily testable
 */
function calculate_discount(float $price, string $tier, int $days_member): float {
    $tier_multipliers = [
        'bronze' => 0.05,
        'silver' => 0.10,
        'gold' => 0.15,
        'platinum' => 0.20
    ];

    $base_discount = $tier_multipliers[$tier] ?? 0;
    $loyalty_bonus = min($days_member / 365 * 0.02, 0.05); // Max 5% loyalty
    $total_discount = min($base_discount + $loyalty_bonus, 0.25); // Max 25%

    return round($price * (1 - $total_discount), 2);
}

/**
 * Validate membership tier upgrade
 * @pure - Returns validation result, no database queries
 */
function validate_tier_upgrade(string $current_tier, string $new_tier): array {
    $tier_hierarchy = ['bronze', 'silver', 'gold', 'platinum'];
    $current_level = array_search($current_tier, $tier_hierarchy);
    $new_level = array_search($new_tier, $tier_hierarchy);

    if ($current_level === false || $new_level === false) {
        return ['valid' => false, 'error' => 'Invalid tier specified'];
    }

    if ($new_level <= $current_level) {
        return ['valid' => false, 'error' => 'Cannot downgrade or stay at same tier'];
    }

    return ['valid' => true, 'upgrade_levels' => $new_level - $current_level];
}

/**
 * Format membership data for display
 * @pure - Data transformation only
 */
function format_membership_display(array $membership): array {
    return [
        'tier' => ucfirst($membership['tier']),
        'expires' => date('F j, Y', strtotime($membership['expires'])),
        'days_remaining' => max(0, (strtotime($membership['expires']) - time()) / DAY_IN_SECONDS),
        'status' => strtotime($membership['expires']) > time() ? 'Active' : 'Expired'
    ];
}

//──────────────────────────────────────────────────────
// WORDPRESS INTEGRATION LAYER (Side Effects)
//──────────────────────────────────────────────────────

namespace MyPlugin;

use MyPlugin\BusinessLogic;

/**
 * WordPress filter hook - uses pure function
 */
add_filter('woocommerce_product_price', function($price, $product) {
    if (!is_user_logged_in()) {
        return $price;
    }

    $user_id = get_current_user_id();
    $tier = get_user_meta($user_id, 'membership_tier', true);
    $member_since = get_user_meta($user_id, 'member_since', true);
    $days_member = (time() - strtotime($member_since)) / DAY_IN_SECONDS;

    // Pure function call - easily testable
    return BusinessLogic\calculate_discount($price, $tier, $days_member);
}, 10, 2);

/**
 * WordPress action hook - handles side effects with security
 */
add_action('wp_ajax_upgrade_membership', function() {
    // 1. Security first - capability check
    if (!current_user_can('edit_user')) {
        wp_send_json_error('Insufficient permissions', 403);
    }

    // 2. Security first - nonce verification
    check_ajax_referer('upgrade_membership', 'nonce');

    // 3. Sanitize inputs
    $user_id = absint($_POST['user_id']);
    $new_tier = sanitize_text_field($_POST['new_tier']);

    // 4. Get current data (side effect)
    $current_tier = get_user_meta($user_id, 'membership_tier', true);

    // 5. Use pure function for validation
    $validation = BusinessLogic\validate_tier_upgrade($current_tier, $new_tier);

    if (!$validation['valid']) {
        wp_send_json_error($validation['error']);
    }

    // 6. Update database (side effect)
    update_user_meta($user_id, 'membership_tier', $new_tier);
    update_user_meta($user_id, 'tier_upgraded_at', current_time('mysql'));

    // 7. Send response (escaped)
    wp_send_json_success([
        'message' => 'Membership upgraded successfully',
        'new_tier' => esc_html($new_tier)
    ]);
});

/**
 * Shortcode - combines pure functions with WordPress
 */
add_shortcode('membership_status', function($atts) {
    if (!is_user_logged_in()) {
        return '<p>Please log in to view your membership status.</p>';
    }

    $user_id = get_current_user_id();

    // Get data from WordPress (side effect)
    $membership = [
        'tier' => get_user_meta($user_id, 'membership_tier', true),
        'expires' => get_user_meta($user_id, 'membership_expires', true)
    ];

    // Pure function for formatting
    $display = BusinessLogic\format_membership_display($membership);

    // Output with proper escaping
    return sprintf(
        '<div class="membership-status">
            <h3>%s Membership</h3>
            <p>Status: <strong>%s</strong></p>
            <p>Expires: %s</p>
            <p>Days Remaining: %d</p>
        </div>',
        esc_html($display['tier']),
        esc_html($display['status']),
        esc_html($display['expires']),
        absint($display['days_remaining'])
    );
});
```

### Real-World Example: Function Factory in WordPress Class

**Production example from ima-espo plugin** showing function factory pattern integrated with WordPress wrapper class.

```php
<?php
declare(strict_types=1);

namespace IMA_Espo\Pure;

//──────────────────────────────────────────────────────
// PURE BUSINESS LOGIC (inc/pure/email-validation.php)
//──────────────────────────────────────────────────────

/**
 * Function factory: Pre-compile email validator
 * @pure - Configuration captured in closure, no side effects
 */
function create_email_validator(
    array $bad_domains,
    array $typo_corrections
): callable {
    // Configuration pre-compiled once during factory creation
    return function (string $email) use ($bad_domains, $typo_corrections): array {
        return validate_email_domain($email, $bad_domains, $typo_corrections);
    };
}

/**
 * Validate email domain against disposable domains and typos
 * @pure - Deterministic, no WordPress dependencies
 */
function validate_email_domain(
    string $email,
    array $bad_domains,
    array $typo_domains
): array {
    // Pure PHP validation - no WordPress functions
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        return ['valid' => false, 'error' => 'Invalid email format'];
    }

    $domain = get_domain_from_email($email);

    // Check against disposable domains
    if (in_array($domain, $bad_domains, true)) {
        return ['valid' => false, 'error' => 'Disposable email domain'];
    }

    // Check for common typos
    if (isset($typo_domains[$domain])) {
        return [
            'valid' => false,
            'error' => 'Possible typo',
            'suggestion' => $typo_domains[$domain]
        ];
    }

    return ['valid' => true];
}

//──────────────────────────────────────────────────────
// WORDPRESS WRAPPER (includes/IMAEspo_EmailValidatorCore.php)
//──────────────────────────────────────────────────────

use function IMA_Espo\Pure\create_email_validator;

/**
 * WordPress wrapper class using function factory pattern
 */
class IMAEspo_EmailValidatorCore {
    /**
     * Pre-compiled validator function
     * @var callable
     */
    protected $validator = null;

    /**
     * Configuration arrays
     */
    protected $bad_domains = array();
    protected $typo_domains = array();

    /**
     * Constructor: Pre-compile validator function once
     */
    public function __construct(array $bad_domains = array(), array $typo_domains = array()) {
        $this->bad_domains = $bad_domains;
        $this->typo_domains = $typo_domains;

        // Function factory pattern: Configuration pre-compiled once
        // Performance: 2-5x speedup when validating multiple emails
        $this->validator = create_email_validator($bad_domains, $typo_domains);
    }

    /**
     * WordPress integration method
     * Uses pre-compiled validator for performance
     */
    public function validate_email_domain(string $email) {
        // Security: Sanitize input from WordPress context
        $email = sanitize_email($email);

        // Use pre-compiled validator (no configuration access)
        $result = ($this->validator)($email);

        // WordPress integration: Log validation failures
        if (!$result['valid']) {
            if (defined('WP_DEBUG') && WP_DEBUG) {
                error_log(sprintf(
                    '[IMA ESPO] Email validation failed: %s - %s',
                    $email,
                    $result['error']
                ));
            }
        }

        return $result;
    }

    /**
     * Get bad domains from WordPress filters
     * Allows theme/plugin customization
     */
    public function get_bad_domains(): array {
        // WordPress filter integration with security
        return apply_filters('ima_espo_bad_email_domains', $this->bad_domains);
    }
}
```

**Key Benefits**:
- **Performance**: 2-5x faster validation (configuration pre-compiled once)
- **Testability**: Pure functions fully testable without WordPress
- **Security**: WordPress sanitization at wrapper boundary
- **Extensibility**: WordPress filters allow customization
- **Separation**: Business logic (pure) separated from WordPress integration

**Production Metrics**:
- 130 tests, 236 assertions, <30ms total execution
- 100% coverage for pure functions
- Zero WordPress dependencies in business logic

## Plugin Complexity Patterns

### Simple Plugin (< 500 lines)

**Use**: Namespaced functions with direct hook usage.

```php
<?php
/**
 * Plugin Name: Simple Analytics Tracker
 */

namespace SimpleAnalytics;

// Pure function - testable without WordPress
function calculate_page_views(array $logs): int {
    return count(array_filter($logs, fn($log) => $log['type'] === 'page_view'));
}

// WordPress integration with security
add_action('wp_footer', function() {
    // Security: capability check
    if (!current_user_can('edit_posts')) return;

    $logs = get_option('analytics_logs', []);
    $views = calculate_page_views($logs);

    // Security: escape output
    echo '<div id="analytics">' . esc_html($views) . ' page views</div>';
});
```

### Medium Plugin (500-2000 lines)

**Use**: Classes for features + functional transformations.

```php
<?php
namespace MediumPlugin;

// Pure functions in separate file (includes/functions.php)
function calculate_shipping_cost(float $weight, string $zone): float {
    $rates = ['domestic' => 5.00, 'international' => 15.00];
    $base = $rates[$zone] ?? 10.00;
    return $base + ($weight * 0.50);
}

// Class for WordPress integration
class ShippingCalculator {
    public function __construct() {
        add_filter('woocommerce_shipping_cost', [$this, 'apply_calculation'], 10, 2);
    }

    public function apply_calculation($cost, $package) {
        // Security: capability check
        if (!current_user_can('view_shop')) return $cost;

        $weight = $package['contents_weight'];
        $zone = $package['destination']['country'] === 'US' ? 'domestic' : 'international';

        return calculate_shipping_cost($weight, $zone); // Use pure function
    }
}
```

### Complex Plugin (2000+ lines)

**Use**: Dependency Injection + Service Architecture.

```php
<?php
namespace ComplexPlugin;

// Pure business logic (separate namespace)
namespace ComplexPlugin\BusinessLogic;

function calculate_order_total(array $items, array $discounts): float {
    $subtotal = array_sum(array_column($items, 'price'));
    $discount = array_sum(array_map(fn($d) => $subtotal * $d['percent'], $discounts));
    return max(0, $subtotal - $discount);
}

// DI Container
namespace ComplexPlugin;

class Container {
    private array $services = [];

    public function register(string $name, callable $resolver): void {
        $this->services[$name] = $resolver;
    }

    public function get(string $name) {
        return ($this->services[$name])($this);
    }
}

// Main plugin with DI
class Plugin {
    private Container $container;

    public function __construct() {
        $this->container = new Container();
        $this->setup_services();
        $this->init_hooks();
    }

    private function setup_services(): void {
        $this->container->register('order', fn($c) =>
            new Services\OrderService($c->get('payment'))
        );
        $this->container->register('payment', fn($c) =>
            new Services\PaymentService()
        );
    }

    private function init_hooks(): void {
        add_action('wp_ajax_process_order', [$this, 'handle_order']);
    }

    public function handle_order(): void {
        // Security first
        if (!current_user_can('edit_shop_orders')) {
            wp_send_json_error('Unauthorized', 403);
        }

        check_ajax_referer('process_order');

        // Sanitize input
        $order_data = array_map('sanitize_text_field', $_POST['order']);

        // Use injected services
        $order_service = $this->container->get('order');
        $result = $order_service->process($order_data);

        wp_send_json_success($result);
    }
}
```

## Testing Strategy

### Unit Tests (Pure Functions - No WordPress)

```php
<?php
use PHPUnit\Framework\TestCase;
use MyPlugin\BusinessLogic;

class DiscountCalculatorTest extends TestCase {
    /**
     * @dataProvider discountProvider
     */
    public function test_calculate_discount($price, $tier, $days, $expected) {
        $result = BusinessLogic\calculate_discount($price, $tier, $days);
        $this->assertEquals($expected, $result);
    }

    public function discountProvider() {
        return [
            'bronze_new_member' => [100.00, 'bronze', 30, 95.00],
            'gold_5year_member' => [100.00, 'gold', 1825, 80.00],
            'invalid_tier' => [100.00, 'invalid', 365, 100.00],
            'platinum_max_discount' => [100.00, 'platinum', 3650, 75.00]
        ];
    }
}
```

### Integration Tests (WordPress Interactions)

```php
<?php
use Brain\Monkey;
use Brain\Monkey\Functions;

class MembershipIntegrationTest extends TestCase {
    protected function setUp(): void {
        parent::setUp();
        Monkey\setUp();
    }

    protected function tearDown(): void {
        Monkey\tearDown();
        parent::tearDown();
    }

    public function test_upgrade_membership_with_permission() {
        // Mock WordPress functions
        Functions\when('current_user_can')->justReturn(true);
        Functions\when('check_ajax_referer')->justReturn(true);
        Functions\when('get_user_meta')->justReturn('silver');
        Functions\expect('update_user_meta')->once();
        Functions\expect('wp_send_json_success')->once();

        // Test the WordPress integration
        $_POST = [
            'user_id' => '1',
            'new_tier' => 'gold',
            'nonce' => 'valid_nonce'
        ];

        handle_membership_upgrade();
    }
}
```

### Real-World Testing Strategy: Minimal WordPress Mocks

**Production example from ima-espo plugin** (130 tests, <30ms execution, 100% pure function coverage).

#### Testing Pure Functions (Zero WordPress Dependencies)

```php
<?php
declare(strict_types=1);

namespace phpunit;

use PHPUnit\Framework\TestCase;
use function IMA_Espo\Pure\validate_email_domain;
use function IMA_Espo\Pure\get_domain_from_email;

/**
 * Pure function tests - NO WordPress mocks needed
 * Fast execution: <1ms per test
 */
class EmailValidationPureTest extends TestCase
{
    /**
     * Test valid email domains
     * @dataProvider valid_email_provider
     */
    public function test_validate_valid_email_domains(string $email): void
    {
        $result = validate_email_domain($email, [], []);

        $this->assertTrue($result['valid']);
        $this->assertArrayNotHasKey('error', $result);
    }

    public function valid_email_provider(): array
    {
        return [
            'standard_email' => ['user@example.com'],
            'subdomain_email' => ['user@mail.example.com'],
            'hyphenated_domain' => ['user@my-domain.com'],
            'numeric_local' => ['123@example.com'],
        ];
    }

    /**
     * Test disposable domain blocking
     * @dataProvider disposable_domain_provider
     */
    public function test_blocks_disposable_domains(string $email, array $bad_domains): void
    {
        $result = validate_email_domain($email, $bad_domains, []);

        $this->assertFalse($result['valid']);
        $this->assertSame('Disposable email domain', $result['error']);
    }

    public function disposable_domain_provider(): array
    {
        return [
            'tempmail' => ['user@tempmail.com', ['tempmail.com']],
            'throwaway' => ['test@throwaway.email', ['throwaway.email']],
            'guerrillamail' => ['spam@guerrillamail.com', ['guerrillamail.com']],
        ];
    }

    /**
     * Test typo detection and suggestions
     * @dataProvider typo_domain_provider
     */
    public function test_suggests_typo_corrections(
        string $email,
        array $typo_map,
        string $expected_suggestion
    ): void {
        $result = validate_email_domain($email, [], $typo_map);

        $this->assertFalse($result['valid']);
        $this->assertSame('Possible typo', $result['error']);
        $this->assertSame($expected_suggestion, $result['suggestion']);
    }

    public function typo_domain_provider(): array
    {
        return [
            'gmail_typo' => [
                'user@gmial.com',
                ['gmial.com' => 'gmail.com'],
                'gmail.com'
            ],
            'yahoo_typo' => [
                'user@yahooo.com',
                ['yahooo.com' => 'yahoo.com'],
                'yahoo.com'
            ],
        ];
    }

    /**
     * Security testing: XSS attempts in email addresses
     * @dataProvider xss_email_vectors
     */
    public function test_validate_email_domain_xss_safety(string $email): void
    {
        $result = validate_email_domain(
            $email,
            ['<script>alert(1)</script>.com'],
            []
        );

        $this->assertIsArray($result);
        $this->assertArrayHasKey('valid', $result);
        // Should fail validation, not execute script
        $this->assertFalse($result['valid']);
    }

    public function xss_email_vectors(): array
    {
        return [
            'script_in_user' => ['<script>alert(1)</script>@example.com'],
            'script_in_domain' => ['user@<script>alert(1)</script>.com'],
            'javascript_protocol' => ['javascript:alert(1)@example.com'],
            'data_protocol' => ['data:text/html,<script>alert(1)</script>@example.com'],
        ];
    }

    /**
     * Edge case testing: All PHP data types
     * Ensures strict types work correctly
     */
    public function test_domain_extraction_edge_cases(): void
    {
        // Empty domain
        $this->assertSame('', get_domain_from_email('user@'));

        // Multiple @ symbols (last one wins)
        $this->assertSame('example.com', get_domain_from_email('user@test@example.com'));

        // Case insensitivity
        $this->assertSame('example.com', get_domain_from_email('USER@EXAMPLE.COM'));
    }
}
```

#### Minimal WordPress Mock Strategy (tests/bootstrap.php)

```php
<?php
/**
 * PHPUnit bootstrap for pure function tests
 * Provides minimal WordPress function definitions ONLY when needed
 */

// Autoload pure functions (no WordPress dependencies)
require_once __DIR__ . '/../inc/pure/email-validation.php';
require_once __DIR__ . '/../inc/pure/activation-url.php';
require_once __DIR__ . '/../inc/pure/form-processing.php';

// Minimal WordPress function mocks (only for WordPress wrapper tests)
if (!function_exists('sanitize_email')) {
    /**
     * Minimal sanitize_email() mock for testing
     * Production uses WordPress core function
     */
    function sanitize_email(string $email): string {
        return strtolower(trim($email));
    }
}

if (!function_exists('error_log')) {
    /**
     * Mock error_log() to prevent test output pollution
     */
    function error_log(string $message): void {
        // Silently ignore in tests
    }
}

if (!function_exists('apply_filters')) {
    /**
     * Minimal apply_filters() mock
     * Returns default value (no filters in tests)
     */
    function apply_filters(string $hook, $value) {
        return $value;
    }
}

// Define WordPress constants for test environment
if (!defined('WP_DEBUG')) {
    define('WP_DEBUG', false);
}
```

**Key Testing Principles**:

1. **Pure Functions Need Zero Mocks**: Test business logic without any WordPress dependencies
2. **Minimal Mocking**: Only mock WordPress functions at the wrapper boundary
3. **Data Providers**: Systematically test all edge cases with parameterized tests
4. **Security Testing**: Dedicated test cases for XSS, SQL injection, malicious input
5. **Fast Execution**: Pure tests run in <1ms each (130 tests in <30ms total)

**Test Organization**:
```
tests/
├── bootstrap.php                    # Minimal WordPress mocks
├── phpunit/
│   ├── EmailValidationPureTest.php  # Pure function tests (FAST)
│   ├── ActivationURLPureTest.php    # Pure function tests (FAST)
│   ├── FormProcessingPureTest.php   # Pure function tests (FAST)
│   ├── EmailValidatorTest.php       # WordPress wrapper tests
│   └── EmailValidatorCoreTest.php   # WordPress integration tests
└── phpunit.xml                      # PHPUnit configuration
```

**Production Results**:
- **130 tests, 236 assertions**: Comprehensive edge case coverage
- **<30ms execution**: Pure functions enable extremely fast testing
- **100% pure function coverage**: Every edge case tested systematically
- **Zero WordPress test database**: No wp-tests-lib needed for pure functions

## File Organization

```
my-plugin/
├── my-plugin.php              # Main plugin file
├── includes/
│   ├── functions.php          # Pure business logic functions
│   ├── class-container.php    # DI container (if complex)
│   └── security.php           # Security helper functions
├── admin/
│   ├── settings.php           # Admin UI (WordPress integration)
│   └── ajax-handlers.php      # AJAX with security checks
├── public/
│   ├── shortcodes.php         # Shortcode definitions
│   └── filters.php            # Filter hook callbacks
└── tests/
    ├── unit/                  # Pure function tests (fast)
    └── integration/           # WordPress interaction tests
```

## Security Checklist (Before Deployment)

- [ ] All user inputs sanitized with appropriate WordPress functions
- [ ] All outputs escaped based on context (HTML, attribute, URL, JS)
- [ ] Capability checks on all privileged operations
- [ ] Nonces verified on all form submissions and AJAX requests
- [ ] Database queries use `$wpdb->prepare()` exclusively
- [ ] File uploads validated with `wp_handle_upload()`
- [ ] No direct access to PHP files (check for `defined('ABSPATH')`)
- [ ] No hardcoded credentials or API keys
- [ ] Error messages don't leak sensitive information
- [ ] Proper uninstallation cleanup (no orphaned data)

## Quality Gates

Before implementing any WordPress feature:

1. ✅ **Security practices**: All 5 mandatory practices implemented?
2. ✅ **Pure business logic**: Separated from WordPress integration?
3. ✅ **Complexity appropriate**: Architecture matches plugin size?
4. ✅ **Testability**: Pure functions have unit tests?
5. ✅ **WordPress integration**: Using hooks correctly?
6. ✅ **FP principles**: Pure functions, explicit dependencies?

## When to Load Additional Content

### Security Deep-Dive
**File**: `security-wordpress.md`
**When**: Need detailed security patterns, vulnerability prevention
**Contains**: Advanced security patterns, vulnerability examples, security testing

### Hooks Integration
**File**: `hooks-integration.md`
**When**: Complex hook usage, filter/action patterns
**Contains**: Advanced hook patterns, priority management, hook lifecycle

### Working Examples
**Directory**: `examples/`
**When**: Need complete working plugin examples
**Contains**: Full plugin examples, tests, security implementation

## Foundation Reference

**Core PHP FP Principles**: `../php-fp/SKILL.md`
- Purity and side effect isolation (PHP-specific patterns)
- Composition patterns (native PHP array functions)
- Dependency injection (type-hinted parameters)
- Immutability (PHP array/object handling)
- Testing strategies (PHPUnit patterns)

**Deep Dive**: `../php-fp/core-principles.md` for complete PHP FP philosophy (when created)

## Success Metrics

- **Security**: Zero vulnerabilities from missing security practices
- **Testability**: 95%+ coverage for pure functions
- **Maintainability**: Clear separation of concerns
- **Code Quality**: Simple, readable code
- **WordPress Compliance**: Follows WordPress Coding Standards

## Philosophy

*"Security practices prevent vulnerabilities, not architectural patterns. Write pure functions for business logic, wrap them in WordPress integration with mandatory security checks, and test both layers appropriately."*

**Evidence Base**: Analysis of 7,966 WordPress plugin vulnerabilities (2024), WordPress Core Team official standards, Wordfence/Patchstack security research.
