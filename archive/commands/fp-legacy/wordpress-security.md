---
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, Grep, TodoWrite, Task]
description: "Security-first WordPress development with pragmatic functional programming"
---

# /wp:security-first - WordPress Security-First Development

## Core Philosophy
**Security practices prevent vulnerabilities, not architectural patterns.** WordPress plugins suffer from missing capability checks (53% XSS vulnerabilities), absent nonce validation (15-17% CSRF), and inadequate sanitization—not from using functions vs classes. This persona applies functional programming principles pragmatically while prioritizing WordPress security practices that actually prevent the 22 daily vulnerabilities discovered in WordPress plugins.

## Usage
```bash
/wp:security-first [component-name] [--type plugin|theme] [--complexity simple|medium|complex]
```

## The Evidence-Based Approach

**WordPress Official Position**: Explicitly supports procedural, OOP, and hybrid architectures equally. No mandate for classes.

**Security Research**: Analysis of 7,966 vulnerabilities (2024) shows ZERO correlation between OOP vs functional patterns and vulnerability rates. All vulnerabilities stem from specific coding mistakes.

**What Actually Causes Vulnerabilities**:
1. Missing capability checks - #1 cause
2. Missing nonce verification - CSRF
3. Inadequate input sanitization - XSS
4. Improper output escaping - XSS
5. Unsanitized SQL queries - SQL injection

## Mandatory Security Practices (Every Plugin)

These practices work identically in functional and OOP code:

```php
<?php
/**
 * CRITICAL: The 5 Non-Negotiable Security Practices
 * Implement these regardless of architectural pattern
 */

// 1. CAPABILITY CHECKS - Always verify permissions
add_action('wp_ajax_delete_user_data', 'handle_delete_user_data');
function handle_delete_user_data() {
    // ✅ Check capability FIRST
    if (!current_user_can('delete_users')) {
        wp_send_json_error('Insufficient permissions', 403);
        return;
    }
    
    // Then proceed with operation
    delete_user_data($_POST['user_id']);
}

// 2. NONCE VERIFICATION - Prevent CSRF
add_action('admin_post_save_settings', 'save_plugin_settings');
function save_plugin_settings() {
    // ✅ Verify nonce
    if (!isset($_POST['settings_nonce']) || 
        !wp_verify_nonce($_POST['settings_nonce'], 'save_settings_action')) {
        wp_die('Security check failed');
    }
    
    // Then save settings
}

// 3. INPUT SANITIZATION - Clean all user input
function process_form_submission() {
    // ✅ Sanitize based on data type
    $name = sanitize_text_field($_POST['name']);
    $email = sanitize_email($_POST['email']);
    $content = wp_kses_post($_POST['content']); // Allow safe HTML
    $url = esc_url_raw($_POST['website']);
    
    save_to_database($name, $email, $content, $url);
}

// 4. OUTPUT ESCAPING - Escape based on context
function render_user_profile($user) {
    // ✅ Escape for HTML context
    echo '<h2>' . esc_html($user->name) . '</h2>';
    
    // ✅ Escape for attribute context
    echo '<img src="' . esc_url($user->avatar) . '" alt="' . esc_attr($user->name) . '">';
    
    // ✅ Escape for JavaScript context
    echo '<script>var userName = ' . wp_json_encode($user->name) . ';</script>';
}

// 5. PREPARED SQL STATEMENTS - Prevent SQL injection
function get_user_posts($user_id) {
    global $wpdb;
    
    // ✅ Use prepared statements - ALWAYS
    $posts = $wpdb->get_results($wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_author = %d AND post_status = %s",
        $user_id,
        'publish'
    ));
    
    return $posts;
}

// ❌ NEVER DO THIS - SQL injection vulnerability
function get_user_posts_UNSAFE($user_id) {
    global $wpdb;
    // This is how 2-5% of WordPress vulnerabilities happen
    return $wpdb->get_results("SELECT * FROM {$wpdb->posts} WHERE post_author = $user_id");
}
```

## Pragmatic Functional Programming Pattern

**The Hybrid Approach That Works**: Pure functions for business logic, WordPress integration where needed.

```php
<?php
/**
 * Pattern: Pure Business Logic + WordPress Wrapper
 * 
 * Pure functions = Testable, predictable, no side effects
 * WordPress wrapper = Hooks, database, UI integration
 */

namespace MyPlugin\BusinessLogic;

//──────────────────────────────────────────────────────
// PURE BUSINESS LOGIC (Zero WordPress Dependencies)
//──────────────────────────────────────────────────────

/**
 * Calculate membership discount
 * 
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
 * 
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
 * 
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
 * WordPress action hook - handles side effects
 */
add_action('wp_ajax_upgrade_membership', function() {
    // 1. Security first
    if (!current_user_can('edit_user')) {
        wp_send_json_error('Insufficient permissions', 403);
    }
    
    check_ajax_referer('upgrade_membership', 'nonce');
    
    // 2. Sanitize inputs
    $user_id = absint($_POST['user_id']);
    $new_tier = sanitize_text_field($_POST['new_tier']);
    
    // 3. Get current data (side effect)
    $current_tier = get_user_meta($user_id, 'membership_tier', true);
    
    // 4. Use pure function for validation
    $validation = BusinessLogic\validate_tier_upgrade($current_tier, $new_tier);
    
    if (!$validation['valid']) {
        wp_send_json_error($validation['error']);
    }
    
    // 5. Update database (side effect)
    update_user_meta($user_id, 'membership_tier', $new_tier);
    update_user_meta($user_id, 'tier_upgraded_at', current_time('mysql'));
    
    // 6. Send response
    wp_send_json_success([
        'message' => 'Membership upgraded successfully',
        'new_tier' => $new_tier
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

## Plugin Complexity Guidelines

### Simple Plugin (< 500 lines)
**Use**: Namespaced functions with direct hook usage

```php
<?php
/**
 * Plugin Name: Simple Analytics Tracker
 */

namespace SimpleAnalytics;

// Pure function
function calculate_page_views(array $logs): int {
    return count(array_filter($logs, fn($log) => $log['type'] === 'page_view'));
}

// WordPress integration
add_action('wp_footer', function() {
    if (!current_user_can('edit_posts')) return; // Security
    
    $logs = get_option('analytics_logs', []);
    $views = calculate_page_views($logs);
    
    echo '<div id="analytics">' . esc_html($views) . ' page views</div>';
});
```

### Medium Plugin (500-2000 lines)
**Use**: Classes for features + functional transformations

```php
<?php
namespace MediumPlugin;

// Pure functions in separate file (includes/functions.php)
function calculate_shipping_cost(float $weight, string $zone): float {
    // Pure calculation
}

// Class for WordPress integration
class ShippingCalculator {
    public function __construct() {
        add_filter('woocommerce_shipping_cost', [$this, 'apply_calculation'], 10, 2);
    }
    
    public function apply_calculation($cost, $package) {
        if (!current_user_can('view_shop')) return $cost; // Security
        
        $weight = $package['contents_weight'];
        $zone = $package['destination']['country'];
        
        return calculate_shipping_cost($weight, $zone); // Use pure function
    }
}
```

### Complex Plugin (2000+ lines)
**Use**: Dependency Injection + Service Architecture

```php
<?php
namespace ComplexPlugin;

use ComplexPlugin\Services\{OrderService, PaymentService};
use ComplexPlugin\BusinessLogic;

// Pure business logic (separate namespace)
namespace ComplexPlugin\BusinessLogic;

function calculate_order_total(array $items, array $discounts): float {
    // Pure calculation
}

// DI Container setup
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

// Main plugin class with DI
class Plugin {
    private Container $container;
    
    public function __construct() {
        $this->container = new Container();
        $this->setup_services();
        $this->init_hooks();
    }
    
    private function setup_services(): void {
        $this->container->register('order', fn($c) => new OrderService($c->get('payment')));
        $this->container->register('payment', fn($c) => new PaymentService());
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
        
        // Use injected services
        $order_service = $this->container->get('order');
        $result = $order_service->process($_POST);
        
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

## Security Checklist (Every Feature)

Before deploying ANY feature:

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

## Common Vulnerability Patterns to Avoid

```php
<?php
// ❌ Missing capability check
add_action('wp_ajax_delete_user', 'delete_user');
function delete_user() {
    wp_delete_user($_POST['user_id']); // Any authenticated user can delete users!
}

// ✅ With capability check
function delete_user() {
    if (!current_user_can('delete_users')) {
        wp_die('Unauthorized');
    }
    wp_delete_user(absint($_POST['user_id']));
}

// ❌ Missing nonce verification
add_action('admin_post_save', 'save_data');
function save_data() {
    update_option('data', $_POST['data']); // CSRF vulnerable!
}

// ✅ With nonce
function save_data() {
    check_admin_referer('save_data_action');
    update_option('data', sanitize_text_field($_POST['data']));
}

// ❌ Unsanitized SQL
function get_posts_by_category($cat_id) {
    global $wpdb;
    return $wpdb->get_results("SELECT * FROM {$wpdb->posts} WHERE category = $cat_id");
}

// ✅ Prepared statement
function get_posts_by_category($cat_id) {
    global $wpdb;
    return $wpdb->get_results($wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE category = %d",
        $cat_id
    ));
}

// ❌ Unescaped output
function show_user_name($user) {
    echo '<h1>' . $user->name . '</h1>'; // XSS if name contains <script>
}

// ✅ Escaped output
function show_user_name($user) {
    echo '<h1>' . esc_html($user->name) . '</h1>';
}
```

## Philosophy

*"Security practices prevent vulnerabilities, not architectural patterns. Write pure functions for business logic, wrap them in WordPress integration with mandatory security checks, and test both layers appropriately. Choose architecture based on plugin complexity, not dogma."*

## Key Takeaways

1. **Security is practice, not pattern** - Missing capability checks cause 53% of vulnerabilities, not architectural choices
2. **WordPress supports both** - Official standards explicitly allow procedural, OOP, and hybrid approaches
3. **Hybrid works best** - Pure functions for logic, WordPress integration for hooks/database/UI
4. **Test appropriately** - Unit test pure functions (fast), integration test WordPress interactions
5. **Complexity determines structure** - Simple = functions, Medium = classes, Complex = DI containers
6. **Never skip security** - Capability checks, nonces, sanitization, escaping, prepared statements - ALWAYS

---

**Evidence Base**: Analysis of 7,966 WordPress plugin vulnerabilities (2024), WordPress Core Team official standards, Wordfence/Patchstack security research, and production plugin architecture review.
