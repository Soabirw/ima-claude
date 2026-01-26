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
- Testing WordPress functionality

## Core Philosophy

**Security practices prevent vulnerabilities, not architectural patterns.**

Hybrid approach:
1. **Pure functions** for business logic (testable, no WordPress deps)
2. **WordPress wrappers** with mandatory security (capability, nonce, sanitize, escape, prepare)

**Foundation**: Reference `../php-fp/SKILL.md` for PHP FP core principles.

## The 5 Non-Negotiable Security Practices

**Evidence**: Analysis of 7,966 vulnerabilities (2024) shows these prevent 95%+ of WordPress plugin vulnerabilities.

| Practice | Prevents | Rule |
|----------|----------|------|
| **Capability Checks** | 53% of XSS | `current_user_can()` before ANY privileged operation |
| **Nonce Verification** | 15-17% CSRF | `wp_verify_nonce()` on ALL form/AJAX submissions |
| **Input Sanitization** | Injection | Sanitize ALL user input by type |
| **Output Escaping** | XSS | Escape ALL output by context |
| **Prepared Statements** | SQL injection | `$wpdb->prepare()` for ALL queries |

### Quick Reference: Security Functions

**Sanitization (Input)**:
| Function | Use For |
|----------|---------|
| `sanitize_text_field()` | Plain text |
| `sanitize_email()` | Email addresses |
| `absint()` | Positive integers |
| `wp_kses_post()` | HTML content |
| `esc_url_raw()` | URLs (for storage) |

**Escaping (Output)**:
| Function | Context |
|----------|---------|
| `esc_html()` | HTML body |
| `esc_attr()` | HTML attributes |
| `esc_url()` | URLs in href/src |
| `wp_json_encode()` | JavaScript data |

### Minimal Security Pattern

```php
<?php
add_action('wp_ajax_my_action', function() {
    // 1. Capability check
    if (!current_user_can('edit_posts')) {
        wp_send_json_error('Unauthorized', 403);
    }

    // 2. Nonce verification
    check_ajax_referer('my_action_nonce', 'nonce');

    // 3. Sanitize input
    $id = absint($_POST['id']);
    $name = sanitize_text_field($_POST['name']);

    // 4. Use prepared statement
    global $wpdb;
    $result = $wpdb->get_row($wpdb->prepare(
        "SELECT * FROM {$wpdb->prefix}my_table WHERE id = %d",
        $id
    ));

    // 5. Escape output
    wp_send_json_success(['name' => esc_html($result->name)]);
});
```

## Pure Logic + WordPress Wrapper Pattern

**Separate testable business logic from WordPress integration.**

```php
<?php
// PURE: Zero WordPress dependencies, fully testable
namespace MyPlugin\Pure;

function calculate_discount(float $price, string $tier): float {
    $rates = ['bronze' => 0.05, 'silver' => 0.10, 'gold' => 0.15];
    return round($price * (1 - ($rates[$tier] ?? 0)), 2);
}

// WRAPPER: WordPress integration with security
namespace MyPlugin;

add_filter('product_price', function($price) {
    if (!is_user_logged_in()) return $price;

    $tier = get_user_meta(get_current_user_id(), 'tier', true);
    return Pure\calculate_discount($price, $tier);
});
```

## Plugin Complexity Guide

| Size | Lines | Pattern |
|------|-------|---------|
| Simple | <500 | Namespaced functions |
| Medium | 500-2000 | Classes + pure functions |
| Complex | 2000+ | DI Container + Services |

**Rule**: Start simple, add complexity only when needed.

## File Organization

```
my-plugin/
├── my-plugin.php              # Bootstrap
├── includes/
│   └── functions.php          # Pure business logic
├── admin/
│   └── ajax-handlers.php      # WordPress integration
└── tests/
    ├── unit/                  # Pure function tests (fast)
    └── integration/           # WordPress tests
```

## Security Checklist

- [ ] Capability checks on all privileged operations
- [ ] Nonces on all form/AJAX submissions
- [ ] Input sanitized by type
- [ ] Output escaped by context
- [ ] SQL uses `$wpdb->prepare()`
- [ ] File uploads use `wp_handle_upload()`
- [ ] No hardcoded credentials

## Quality Gates

1. **Security**: All 5 mandatory practices implemented?
2. **Pure logic**: Business logic separated from WordPress?
3. **Testability**: Pure functions have unit tests?
4. **Complexity**: Architecture matches plugin size?

## When to Load Reference Files

### Security Deep-Dive
**File**: [`references/security-examples.md`](references/security-examples.md)
**Load when**: Need detailed security patterns, vulnerable vs. safe comparisons
**Contains**: Full examples for all 5 practices, security function reference tables

### FP Patterns
**File**: [`references/fp-patterns.md`](references/fp-patterns.md)
**Load when**: Implementing pure logic + wrapper pattern, function factories
**Contains**: Complete membership system example, production email validator example

### Plugin Architecture
**File**: [`references/plugin-architecture.md`](references/plugin-architecture.md)
**Load when**: Deciding plugin structure, implementing DI container
**Contains**: Simple/medium/complex plugin patterns, file organization examples

### Testing Strategy
**File**: [`references/testing-strategy.md`](references/testing-strategy.md)
**Load when**: Setting up tests, writing security tests
**Contains**: Unit/integration test examples, minimal mock bootstrap, security test patterns

## Success Metrics

- **Security**: Zero vulnerabilities from missing practices
- **Testability**: 95%+ coverage for pure functions
- **Maintainability**: Clear separation of concerns

---

**Evidence Base**: Analysis of 7,966 WordPress vulnerabilities (2024), WordPress Core Team standards, Wordfence/Patchstack research.
