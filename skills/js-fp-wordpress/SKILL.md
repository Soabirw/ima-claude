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
// ✅ KEEP: Working jQuery AJAX handler
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
            },
            error: function() {
                $form.find('.ima-response').html('Error occurred');
            }
        });
    });

})(jQuery);

// ❌ DON'T: Rewrite to vanilla "just because"
// No benefit, adds risk, wastes time
```

### 2. New Code: Choose Based on Context

```javascript
// ✅ jQuery: When integrating with WordPress plugins
(function($) {
    'use strict';

    // Gravity Forms event - MUST use jQuery
    $(document).on('gform_post_render', function(event, formId) {
        initImaFields($('#gform_' + formId));
    });

    // ACF field interaction - matches ecosystem
    acf.addAction('ready', function() {
        $('.acf-field-type-repeater').each(function() {
            setupRepeaterEnhancements($(this));
        });
    });

})(jQuery);

// ✅ Vanilla JS: Isolated component with no WP plugin interaction
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

        handleClick(e) {
            if (e.target.matches('[data-add-row]')) {
                this.addRow();
            } else if (e.target.matches('[data-remove-row]')) {
                this.removeRow(e.target.closest('[data-repeater-row]'));
            }
        }

        // Pure method - no DOM side effects
        generateRowId() {
            return 'row_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        }

        addRow() {
            var clone = this.template.cloneNode(true);
            clone.removeAttribute('data-repeater-template');
            clone.setAttribute('data-repeater-row', this.generateRowId());
            this.container.appendChild(clone);
        }

        removeRow(row) {
            if (row && this.container.contains(row)) {
                row.remove();
            }
        }
    }

    // Self-contained initialization
    document.querySelectorAll('[data-repeater-container]').forEach(function(el) {
        new RepeaterController(el);
    });

})();
```

### 3. Prefer Consistency Within Files

```javascript
// ❌ AVOID: Mixing jQuery and vanilla in same file
(function($) {
    document.querySelectorAll('.foo').forEach(function(el) {  // Vanilla
        $(el).on('click', handler);  // jQuery - inconsistent!
    });
})(jQuery);

// ✅ GOOD: Consistent jQuery throughout
(function($) {
    'use strict';

    $('.foo').each(function() {
        $(this).on('click', handler);
    });

})(jQuery);

// ✅ GOOD: Consistent vanilla throughout
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
// ❌ Mixed: Business logic entangled with DOM
(function($) {
    $('.price-calculator').on('change', 'input', function() {
        var quantity = parseInt($('#quantity').val()) || 0;
        var price = parseFloat($('#unit-price').val()) || 0;
        var discount = parseFloat($('#discount').val()) || 0;

        // Business logic mixed with DOM operations
        var subtotal = quantity * price;
        var discountAmount = subtotal * (discount / 100);
        var total = subtotal - discountAmount;

        $('#subtotal').text('$' + subtotal.toFixed(2));
        $('#discount-amount').text('-$' + discountAmount.toFixed(2));
        $('#total').text('$' + total.toFixed(2));
    });
})(jQuery);

// ✅ Separated: Pure business logic + DOM wrapper
(function($) {
    'use strict';

    // ───── Pure business logic (testable without DOM) ─────
    function calculatePricing(quantity, unitPrice, discountPercent) {
        var subtotal = Math.max(0, quantity) * Math.max(0, unitPrice);
        var discountAmount = subtotal * (Math.min(100, Math.max(0, discountPercent)) / 100);
        var total = subtotal - discountAmount;

        return {
            subtotal: subtotal,
            discountAmount: discountAmount,
            total: total
        };
    }

    function formatCurrency(amount) {
        return '$' + amount.toFixed(2);
    }

    // ───── DOM wrapper (side effects isolated here) ─────
    function PriceCalculator($container) {
        this.$container = $container;
        this.$quantity = $container.find('#quantity');
        this.$unitPrice = $container.find('#unit-price');
        this.$discount = $container.find('#discount');
        this.$subtotal = $container.find('#subtotal');
        this.$discountAmount = $container.find('#discount-amount');
        this.$total = $container.find('#total');

        this.init();
    }

    PriceCalculator.prototype.init = function() {
        this.$container.on('change', 'input', this.update.bind(this));
    };

    PriceCalculator.prototype.getInputValues = function() {
        return {
            quantity: parseInt(this.$quantity.val()) || 0,
            unitPrice: parseFloat(this.$unitPrice.val()) || 0,
            discount: parseFloat(this.$discount.val()) || 0
        };
    };

    PriceCalculator.prototype.update = function() {
        var values = this.getInputValues();
        var pricing = calculatePricing(values.quantity, values.unitPrice, values.discount);

        this.$subtotal.text(formatCurrency(pricing.subtotal));
        this.$discountAmount.text('-' + formatCurrency(pricing.discountAmount));
        this.$total.text(formatCurrency(pricing.total));
    };

    // ───── Initialization ─────
    $('.price-calculator').each(function() {
        new PriceCalculator($(this));
    });

    // ───── Export for testing (optional) ─────
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = { calculatePricing: calculatePricing, formatCurrency: formatCurrency };
    }

})(jQuery);
```

## AJAX Patterns

### jQuery AJAX (Recommended for WordPress)

```javascript
(function($) {
    'use strict';

    function submitForm($form, successCallback, errorCallback) {
        $.ajax({
            url: imaAjax.url,
            type: 'POST',
            data: {
                action: 'ima_process_form',
                nonce: imaAjax.nonce,
                form_data: $form.serialize()
            },
            beforeSend: function() {
                $form.find('button[type="submit"]').prop('disabled', true);
                $form.find('.ima-loading').show();
            },
            success: function(response) {
                if (response.success) {
                    successCallback(response.data);
                } else {
                    errorCallback(response.data || 'Unknown error');
                }
            },
            error: function(xhr, status, error) {
                errorCallback('Network error: ' + error);
            },
            complete: function() {
                $form.find('button[type="submit"]').prop('disabled', false);
                $form.find('.ima-loading').hide();
            }
        });
    }

    // Usage
    $('.ima-ajax-form').on('submit', function(e) {
        e.preventDefault();
        var $form = $(this);

        submitForm(
            $form,
            function(data) {
                $form.find('.ima-response').html(data.message).removeClass('error').addClass('success');
            },
            function(error) {
                $form.find('.ima-response').html(error).removeClass('success').addClass('error');
            }
        );
    });

})(jQuery);
```

### Vanilla fetch (When Appropriate)

```javascript
(function() {
    'use strict';

    // Pure function - formats data for WordPress AJAX
    function buildFormData(action, nonce, data) {
        var formData = new FormData();
        formData.append('action', action);
        formData.append('nonce', nonce);

        Object.keys(data).forEach(function(key) {
            formData.append(key, data[key]);
        });

        return formData;
    }

    // Wrapper with side effects
    function submitToWordPress(action, data) {
        return fetch(imaAjax.url, {
            method: 'POST',
            credentials: 'same-origin',
            body: buildFormData(action, imaAjax.nonce, data)
        })
        .then(function(response) {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(function(data) {
            if (!data.success) {
                throw new Error(data.data || 'Unknown error');
            }
            return data.data;
        });
    }

    // Usage
    document.querySelectorAll('.ima-fetch-form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            var formData = new FormData(form);
            var data = {};
            formData.forEach(function(value, key) {
                data[key] = value;
            });

            submitToWordPress('ima_process_form', data)
                .then(function(result) {
                    form.querySelector('.ima-response').textContent = result.message;
                })
                .catch(function(error) {
                    form.querySelector('.ima-response').textContent = error.message;
                });
        });
    });

})();
```

## Event Delegation Patterns

### jQuery Event Delegation

```javascript
(function($) {
    'use strict';

    // Delegated events - works with dynamically added elements
    $(document).on('click', '.ima-toggle-btn', function(e) {
        e.preventDefault();
        var $target = $($(this).data('target'));
        $target.toggleClass('is-visible');
    });

    // Scoped delegation (more efficient)
    $('.ima-component').on('click', '.ima-action-btn', function(e) {
        e.preventDefault();
        handleAction($(this).data('action'), $(this).closest('.ima-item'));
    });

})(jQuery);
```

### Vanilla Event Delegation

```javascript
(function() {
    'use strict';

    // Delegated events using event bubbling
    document.addEventListener('click', function(e) {
        // Toggle button delegation
        if (e.target.matches('.ima-toggle-btn') || e.target.closest('.ima-toggle-btn')) {
            e.preventDefault();
            var btn = e.target.closest('.ima-toggle-btn');
            var target = document.querySelector(btn.dataset.target);
            if (target) {
                target.classList.toggle('is-visible');
            }
        }
    });

    // Scoped delegation
    document.querySelectorAll('.ima-component').forEach(function(component) {
        component.addEventListener('click', function(e) {
            var actionBtn = e.target.closest('.ima-action-btn');
            if (actionBtn) {
                e.preventDefault();
                var action = actionBtn.dataset.action;
                var item = actionBtn.closest('.ima-item');
                handleAction(action, item);
            }
        });
    });

})();
```

## WordPress Hooks Integration

```javascript
(function($) {
    'use strict';

    // ───── Gravity Forms Integration ─────
    // MUST use jQuery - GF events are jQuery-based
    $(document).on('gform_post_render', function(event, formId) {
        var $form = $('#gform_' + formId);

        // Initialize custom fields
        initConsentFields($form);
        initRepeaterFields($form);
    });

    $(document).on('gform_confirmation_loaded', function(event, formId) {
        // Track form completion
        if (typeof gtag === 'function') {
            gtag('event', 'form_submit', {
                'form_id': formId
            });
        }
    });

    // ───── ACF Integration ─────
    // ACF uses jQuery events
    if (typeof acf !== 'undefined') {
        acf.addAction('ready', function($el) {
            // ACF fields are ready
            initAcfEnhancements($el);
        });

        acf.addAction('append', function($el) {
            // New ACF repeater row added
            initAcfEnhancements($el);
        });
    }

    // ───── WordPress Admin Integration ─────
    $(document).ready(function() {
        // Admin-specific enhancements
        if (typeof pagenow !== 'undefined' && pagenow === 'edit-listing') {
            initListingAdminEnhancements();
        }
    });

})(jQuery);
```

## DOMContentLoaded Patterns

### jQuery Document Ready

```javascript
// Standard WordPress pattern
(function($) {
    $(document).ready(function() {
        // DOM is ready
        initComponents();
    });
})(jQuery);

// Shorthand (equivalent)
jQuery(function($) {
    initComponents();
});
```

### Vanilla DOMContentLoaded

```javascript
(function() {
    'use strict';

    function init() {
        initComponents();
    }

    // Handle both loading states
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOM already loaded (script loaded with defer or at bottom)
        init();
    }

})();
```

## Anti-Patterns (AVOID)

### ❌ Rewriting Working jQuery for No Benefit

```javascript
// ❌ DON'T: Rewrite working jQuery
// Before (working)
$('.btn').on('click', handler);

// After (same functionality, more code, no benefit)
document.querySelectorAll('.btn').forEach(function(btn) {
    btn.addEventListener('click', handler);
});
```

### ❌ Mixing jQuery and Vanilla Inconsistently

```javascript
// ❌ DON'T: Mix in same file/component
$('.container').each(function() {
    var element = document.createElement('div');  // Vanilla
    $(this).append(element);  // jQuery - inconsistent
});

// ✅ DO: Pick one and stay consistent
$('.container').each(function() {
    var $element = $('<div>');  // jQuery
    $(this).append($element);   // jQuery
});
```

### ❌ Fighting the WordPress Ecosystem

```javascript
// ❌ DON'T: Ignore GF jQuery events
document.addEventListener('gform_post_render', function() {
    // This won't work - GF uses jQuery events!
});

// ✅ DO: Use jQuery for GF integration
$(document).on('gform_post_render', function(event, formId) {
    // This works correctly
});
```

### ❌ Custom FP Utilities

```javascript
// ❌ NEVER: Create custom FP utilities
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x)
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x)

// ✅ INSTEAD: Direct function calls
function processFormData(data) {
    var sanitized = sanitizeData(data);
    var validated = validateData(sanitized);
    return formatData(validated);
}
```

## Quality Gates

Before implementing JavaScript in WordPress:

1. ✅ **Ecosystem check**: Does this need to interact with jQuery-based plugins (GF, ACF)?
2. ✅ **Existing code**: Is there working code that just needs enhancement?
3. ✅ **Pure logic**: Is business logic separated from DOM operations?
4. ✅ **Consistency**: Is the file using one approach consistently?
5. ✅ **Testability**: Can pure functions be tested without DOM?
6. ✅ **YAGNI**: Are we adding complexity without clear benefit?

## File Organization

```
plugin-name/
└── assets/
    └── js/
        ├── plugin-base.js         # jQuery - AJAX, GF integration
        ├── plugin-admin.js        # jQuery - Admin UI interactions
        ├── plugin-repeater.js     # Vanilla - Isolated component
        ├── plugin-validation.js   # Vanilla - Pure validation logic
        └── pure/
            ├── formatting.js      # Pure functions (testable)
            └── calculations.js    # Pure functions (testable)
```

## Testing Strategy

### Pure Functions (Jest/Node)

```javascript
// pure/calculations.js
function calculatePricing(quantity, unitPrice, discountPercent) {
    var subtotal = Math.max(0, quantity) * Math.max(0, unitPrice);
    var discountAmount = subtotal * (Math.min(100, Math.max(0, discountPercent)) / 100);
    var total = subtotal - discountAmount;

    return { subtotal: subtotal, discountAmount: discountAmount, total: total };
}

module.exports = { calculatePricing: calculatePricing };

// pure/calculations.test.js
var calculatePricing = require('./calculations').calculatePricing;

describe('calculatePricing', function() {
    it('calculates correct pricing', function() {
        var result = calculatePricing(10, 25, 10);
        expect(result.subtotal).toBe(250);
        expect(result.discountAmount).toBe(25);
        expect(result.total).toBe(225);
    });

    it('handles zero quantity', function() {
        var result = calculatePricing(0, 25, 10);
        expect(result.total).toBe(0);
    });

    it('handles negative values gracefully', function() {
        var result = calculatePricing(-5, 25, 10);
        expect(result.total).toBe(0);
    });
});
```

## When to Load Additional Content

### Working Examples
**Directory**: `examples/`
**When**: Need complete working plugin JavaScript examples
**Contains**: Full examples with AJAX, GF integration, pure functions

### PHP Integration
**File**: `../php-fp-wordpress/SKILL.md`
**When**: Need server-side integration patterns
**Contains**: WordPress AJAX handlers, security practices, PHP/JS coordination

## Foundation Reference

**Core FP Principles**: `../js-fp/SKILL.md`
- Purity and side effect isolation
- Composition patterns
- Dependency injection
- Immutability
- Testing strategies

## Success Metrics

- **Ecosystem Fit**: JavaScript integrates smoothly with WordPress/plugins
- **Consistency**: Files use one approach throughout
- **Testability**: Pure business logic has unit tests
- **Maintainability**: Clear separation of concerns
- **Pragmatism**: Working code not rewritten without benefit

## Philosophy

*"In WordPress, jQuery IS native. Use what's simple and matches the ecosystem. Separate pure business logic for testability, but don't fight the platform. Working code > ideological purity."*
