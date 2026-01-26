---
name: "js-fp-wordpress"
description: "FP patterns for JavaScript in WordPress/Bootstrap context - ecosystem-native patterns, jQuery guidance, pure business logic"
---

# JavaScript FP - WordPress/Bootstrap

Functional programming patterns for JavaScript in WordPress environments where jQuery is already loaded and Bootstrap is the UI framework.

## When to Use This Skill

- Building WordPress plugin/theme JavaScript
- Need guidance on jQuery vs Vanilla JS decisions
- Implementing pure business logic in browser JavaScript
- Working with Gravity Forms, ACF, or other jQuery-dependent plugins
- Creating form handlers, AJAX operations, or DOM interactions

## Core Philosophy

**"Use what's simple and native to the ecosystem. In WordPress, jQuery IS native."**

**Key Insight**: The js-fp principle "Native patterns > FP utilities" targets AI-generated abstractions like custom `pipe()` and `curry()` functions - it does NOT mean "avoid established ecosystem libraries like jQuery."

**Foundation**: This skill builds on `js-fp` core principles. Reference `../js-fp/SKILL.md` for purity, composition, dependency injection, and testing patterns.

## TL;DR Decision Matrix

| Context | Recommendation | Rationale |
|---------|---------------|-----------|
| **New isolated component** | Vanilla JS | No jQuery event coupling needed |
| **AJAX operations** | jQuery `$.ajax` | Cleaner than `fetch` + error handling |
| **DOM event delegation** | Either | Both work well |
| **Integrating with WP plugins** | jQuery | Match ecosystem patterns |
| **Animation** | CSS transitions | Neither jQuery nor vanilla JS |
| **Pure business logic** | Vanilla JS | No DOM, fully testable |

## Critical Context: WordPress Reality Check

**jQuery IS guaranteed available** in WordPress because:
1. WordPress core depends on jQuery
2. Bootstrap 5 JavaScript works with or without jQuery
3. Gravity Forms, ACF, and most plugins use jQuery
4. The overhead argument is **irrelevant** - it's already loaded (0 additional bytes)

### Arguments That DON'T Apply Here

| Common Argument | Why It Doesn't Apply |
|-----------------|---------------------|
| "jQuery adds bundle size" | Already loaded - 0 additional bytes |
| "jQuery is a dependency" | Already a core WordPress dependency |
| "Modern browsers don't need jQuery" | True, but jQuery is still there |
| "jQuery is slower" | Negligible for DOM operations |

## Practical Guidelines

### 1. Don't Rewrite Working jQuery Code

**YAGNI applies**. If existing code works, leave it:

```javascript
// KEEP: Working jQuery AJAX handler
(function($) {
    'use strict';

    $('.ima-form').on('submit', function(e) {
        e.preventDefault();
        var $form = $(this);

        $.ajax({
            url: imaAjax.url,
            type: 'POST',
            data: $form.serialize(),
            success: function(response) {
                $form.find('.ima-response').html(response.message);
            }
        });
    });

})(jQuery);

// DON'T: Rewrite to vanilla "just because" - No benefit, adds risk
```

### 2. New Code: Choose Based on Context

```javascript
// jQuery: When integrating with WordPress plugins
(function($) {
    'use strict';

    // Gravity Forms event - MUST use jQuery
    $(document).on('gform_post_render', function(event, formId) {
        initImaFields($('#gform_' + formId));
    });

})(jQuery);

// Vanilla JS: Isolated component with no WP plugin interaction
(function() {
    'use strict';

    class RepeaterController {
        constructor(element) {
            this.container = element;
            this.template = element.querySelector('[data-repeater-template]');
            this.init();
        }

        init() {
            this.container.addEventListener('click', this.handleClick.bind(this));
        }

        // Pure method - no DOM side effects
        generateRowId() {
            return 'row_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        }
    }

    document.querySelectorAll('[data-repeater-container]').forEach(function(el) {
        new RepeaterController(el);
    });

})();
```

### 3. Prefer Consistency Within Files

```javascript
// AVOID: Mixing jQuery and vanilla in same file
(function($) {
    document.querySelectorAll('.foo').forEach(function(el) {  // Vanilla
        $(el).on('click', handler);  // jQuery - inconsistent!
    });
})(jQuery);

// GOOD: Consistent jQuery throughout
(function($) {
    'use strict';
    $('.foo').each(function() {
        $(this).on('click', handler);
    });
})(jQuery);

// GOOD: Consistent vanilla throughout
(function() {
    'use strict';
    document.querySelectorAll('.foo').forEach(function(el) {
        el.addEventListener('click', handler);
    });
})();
```

## Pure Business Logic Pattern

**Rule**: Extract pure JavaScript functions from DOM-dependent code.

```javascript
(function($) {
    'use strict';

    // Pure business logic (testable without DOM)
    function calculatePricing(quantity, unitPrice, discountPercent) {
        var subtotal = Math.max(0, quantity) * Math.max(0, unitPrice);
        var discountAmount = subtotal * (Math.min(100, Math.max(0, discountPercent)) / 100);
        return {
            subtotal: subtotal,
            discountAmount: discountAmount,
            total: subtotal - discountAmount
        };
    }

    function formatCurrency(amount) {
        return '$' + amount.toFixed(2);
    }

    // DOM wrapper (side effects isolated here)
    function PriceCalculator($container) {
        this.$container = $container;
        this.$container.on('change', 'input', this.update.bind(this));
    }

    PriceCalculator.prototype.update = function() {
        var values = {
            quantity: parseInt(this.$container.find('#quantity').val()) || 0,
            unitPrice: parseFloat(this.$container.find('#unit-price').val()) || 0,
            discount: parseFloat(this.$container.find('#discount').val()) || 0
        };
        var pricing = calculatePricing(values.quantity, values.unitPrice, values.discount);
        this.$container.find('#total').text(formatCurrency(pricing.total));
    };

    // Export for testing
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = { calculatePricing: calculatePricing, formatCurrency: formatCurrency };
    }

})(jQuery);
```

## Anti-Patterns (AVOID)

### Rewriting Working jQuery for No Benefit

```javascript
// DON'T: Same functionality, more code, no benefit
// Before (working): $('.btn').on('click', handler);
// After (unnecessary):
document.querySelectorAll('.btn').forEach(function(btn) {
    btn.addEventListener('click', handler);
});
```

### Fighting the WordPress Ecosystem

```javascript
// DON'T: Ignore GF jQuery events (this won't work!)
document.addEventListener('gform_post_render', function() {});

// DO: Use jQuery for GF integration
$(document).on('gform_post_render', function(event, formId) {});
```

### Custom FP Utilities

```javascript
// NEVER: Create custom FP utilities
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x)

// INSTEAD: Direct function calls
function processFormData(data) {
    var sanitized = sanitizeData(data);
    var validated = validateData(sanitized);
    return formatData(validated);
}
```

## Quality Gates

Before implementing JavaScript in WordPress:

1. **Ecosystem check**: Does this need to interact with jQuery-based plugins (GF, ACF)?
2. **Existing code**: Is there working code that just needs enhancement?
3. **Pure logic**: Is business logic separated from DOM operations?
4. **Consistency**: Is the file using one approach consistently?
5. **Testability**: Can pure functions be tested without DOM?
6. **YAGNI**: Are we adding complexity without clear benefit?

## Reference Files

Load these as needed for detailed patterns:

### AJAX Patterns
**File**: [references/ajax-patterns.md](references/ajax-patterns.md)
**When**: Need AJAX implementation patterns
**Contains**: jQuery $.ajax, vanilla fetch, error handling, retry patterns

### Event Patterns
**File**: [references/event-patterns.md](references/event-patterns.md)
**When**: Need event delegation or DOMContentLoaded patterns
**Contains**: jQuery delegation, vanilla delegation, document ready patterns

### WordPress Integration
**File**: [references/wp-integration.md](references/wp-integration.md)
**When**: Integrating with Gravity Forms, ACF, or WordPress admin
**Contains**: GF hooks, ACF hooks, admin JS, pure logic extraction, testing

### PHP Integration
**File**: `../php-fp-wordpress/SKILL.md`
**When**: Need server-side integration patterns
**Contains**: WordPress AJAX handlers, security practices, PHP/JS coordination

### Core FP Principles
**File**: `../js-fp/SKILL.md`
**When**: Need foundational FP patterns
**Contains**: Purity, composition, dependency injection, immutability, testing

## File Organization

```
plugin-name/
└── assets/
    └── js/
        ├── plugin-base.js         # jQuery - AJAX, GF integration
        ├── plugin-admin.js        # jQuery - Admin UI interactions
        ├── plugin-repeater.js     # Vanilla - Isolated component
        └── pure/
            ├── formatting.js      # Pure functions (testable)
            └── calculations.js    # Pure functions (testable)
```

## Success Metrics

- **Ecosystem Fit**: JavaScript integrates smoothly with WordPress/plugins
- **Consistency**: Files use one approach throughout
- **Testability**: Pure business logic has unit tests
- **Maintainability**: Clear separation of concerns
- **Pragmatism**: Working code not rewritten without benefit

## Philosophy

*"In WordPress, jQuery IS native. Use what's simple and matches the ecosystem. Separate pure business logic for testability, but don't fight the platform. Working code > ideological purity."*
