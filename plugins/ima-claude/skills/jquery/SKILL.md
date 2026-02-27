---
name: jquery
description: >-
  jQuery patterns and API reference for WordPress/Bootstrap environments where jQuery
  is already loaded. FP-aligned: chaining as composition, $.map/$.grep as declarative
  transforms, pure logic extraction. Use when: writing DOM manipulation in WordPress
  themes/plugins, working with Bootstrap JS components, handling events on dynamic
  content, AJAX in WordPress, any browser JS where jQuery is available. Triggers on:
  jQuery, $(), .on(), .find(), .ajax(), $.each, DOM manipulation in WordPress context,
  Bootstrap JS, "how do I select", "how do I toggle", event delegation, IIFE wrapper.
  IMPORTANT: In WordPress, jQuery IS native (0 additional bytes). Default to jQuery
  for DOM work unless building an isolated module with no WP plugin interaction.
---

# jQuery - FP-Aligned Patterns

**"jQuery IS native in WordPress. Reach for it first."**

## Why This Skill Exists

Agents default to verbose vanilla JS even when jQuery is loaded and simpler. In WordPress, jQuery is **always available** (core dependency, 0 additional bytes). Writing `document.querySelectorAll('.foo').forEach(el => el.addEventListener('click', ...))` when `$('.foo').on('click', ...)` exists is unnecessary complexity.

**This skill ensures jQuery is the default for DOM work in WordPress/Bootstrap environments.**

## When to Use jQuery (Decision Tree)

```
Writing browser JS in a WordPress environment?
├── YES: Does it touch the DOM (select, manipulate, events, AJAX)?
│   ├── YES → Use jQuery (default choice)
│   │   Exception: Pure business logic (calculations, validation, formatting)
│   │   → Keep as vanilla JS in pure/ directory (testable without DOM)
│   └── NO (pure data transforms, utilities) → Vanilla JS
├── Is jQuery already loaded on the page?
│   ├── YES → Use jQuery for DOM work
│   └── NO → Vanilla JS (don't add jQuery just for convenience)
└── NO WordPress context?
    └── See js-fp for vanilla patterns
```

**Strong signals to use jQuery:**
- WordPress theme or plugin JavaScript
- Bootstrap component initialization or interaction
- Gravity Forms, ACF, or any jQuery-based plugin integration
- AJAX calls to `admin-ajax.php` or WP REST API
- Event delegation on dynamic content
- DOM traversal and manipulation

**Signals to use vanilla JS instead:**
- Pure business logic (no DOM)
- Isolated ES module with no WP plugin interaction
- Node.js / server-side code
- React/Vue component internals

## jQuery + FP: They're Compatible

jQuery's API is inherently functional in several ways:

### Chaining IS Composition

```javascript
// jQuery chaining = function composition without pipe()
$('.user-card')
    .filter('.active')
    .find('.username')
    .addClass('highlighted')
    .text(function(i, text) { return text.toUpperCase(); });

// Each method takes input, returns output (the jQuery object)
// This IS composition — no custom pipe() needed
```

### $.map and $.grep ARE Declarative

```javascript
// jQuery's functional utilities
var activeNames = $.map($('.user'), function(el) {
    return $(el).data('active') ? $(el).text() : null;
});

// $.grep = filter
var admins = $.grep(users, function(user) {
    return user.role === 'admin';
});

// Prefer native Array methods for plain data:
var activeNames = users.filter(u => u.active).map(u => u.name);
// Use $.map/$.grep when working with jQuery collections
```

### Pure Logic Extraction (The FP Core)

```javascript
(function($) {
    'use strict';

    // PURE: Business logic — testable, no DOM
    function calculateShipping(weight, zone) {
        var rates = { domestic: 0.5, international: 1.2 };
        return Math.max(0, weight) * (rates[zone] || rates.domestic);
    }

    function formatPrice(amount) {
        return '$' + Math.max(0, amount).toFixed(2);
    }

    // IMPURE: DOM wrapper — uses jQuery, calls pure functions
    function ShippingCalculator($container) {
        this.$container = $container;
        this.$container.on('change', 'select, input', this.update.bind(this));
    }

    ShippingCalculator.prototype.update = function() {
        var weight = parseFloat(this.$container.find('[name="weight"]').val()) || 0;
        var zone = this.$container.find('[name="zone"]').val();
        var cost = calculateShipping(weight, zone);
        this.$container.find('.shipping-cost').text(formatPrice(cost));
    };

    // Init
    $('.shipping-calculator').each(function() {
        new ShippingCalculator($(this));
    });

    // Export pure functions for testing
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = { calculateShipping: calculateShipping, formatPrice: formatPrice };
    }
})(jQuery);
```

## Quick Reference

### IIFE Wrapper (WordPress Standard)

```javascript
// Always use this pattern in WordPress — avoids $ conflicts
(function($) {
    'use strict';

    // All jQuery code here, $ is safe

})(jQuery);

// Shorthand document ready
jQuery(function($) {
    // DOM ready, $ is safe
});
```

### Selectors and Traversal

```javascript
// Selecting
$('.class')                    // By class
$('#id')                       // By ID
$('[data-action="delete"]')    // By attribute
$('.parent .child')            // Descendant
$('.item:first')               // Pseudo-selector
$('input[type="text"]')        // Attribute selector

// Traversal (chained)
$('.item')
    .closest('.container')     // Up: nearest ancestor matching selector
    .find('.target')           // Down: descendants matching selector
    .siblings('.active')       // Sideways: siblings matching selector
    .parent()                  // Up: direct parent
    .children('.row')          // Down: direct children only
    .first()                   // Filter: first in set
    .filter('.visible')        // Filter: matching selector
    .not('.disabled')          // Filter: exclude matching
    .eq(2)                     // Filter: by index

// Context-scoped selection (efficient)
var $form = $('#my-form');
$form.find('.field')           // Only searches within $form
$form.find('input').val()      // Get value within scope
```

### DOM Manipulation

```javascript
// Classes
$el.addClass('active')
$el.removeClass('loading')
$el.toggleClass('visible')
$el.hasClass('hidden')          // Returns boolean

// Content
$el.text('Plain text')          // Set text (escapes HTML)
$el.html('<strong>HTML</strong>') // Set HTML
$el.val()                       // Get form value
$el.val('new value')            // Set form value

// Attributes and Data
$el.attr('href')                // Get attribute
$el.attr('href', '/new-url')    // Set attribute
$el.prop('checked', true)       // Set property (for checkboxes, disabled, etc.)
$el.data('user-id')             // Get data-* attribute (cached, parsed)
$el.removeAttr('disabled')

// DOM insertion
$container.append($newElement)   // Add inside, at end
$container.prepend($newElement)  // Add inside, at start
$el.after($sibling)             // Add outside, after
$el.before($sibling)            // Add outside, before
$el.wrap('<div class="wrapper"></div>')
$el.remove()                    // Remove from DOM
$el.empty()                     // Remove children
$el.clone()                     // Deep clone

// CSS and Display
$el.css('color', 'red')         // Set single property
$el.css({ color: 'red', fontSize: '14px' }) // Set multiple
$el.show()                      // display: previous value
$el.hide()                      // display: none
$el.toggle()                    // Toggle visibility
```

### Events

```javascript
// Binding
$el.on('click', handler)                        // Direct bind
$container.on('click', '.child', handler)        // Delegated (dynamic content!)
$el.off('click', handler)                        // Unbind specific
$el.off('click')                                 // Unbind all click

// Common events
$el.on('click', fn)
$el.on('change', fn)           // Form elements
$el.on('submit', fn)           // Forms
$el.on('keyup', fn)
$el.on('input', fn)            // Real-time input tracking
$el.on('focus blur', fn)       // Multiple events

// Event object
$el.on('click', function(e) {
    e.preventDefault();         // Stop default behavior
    e.stopPropagation();        // Stop bubbling
    var $this = $(this);        // Cache $(this)
    var data = $this.data('id');
});

// Namespaced events (clean removal)
$el.on('click.myPlugin', handler);
$el.off('.myPlugin');           // Remove all myPlugin events

// One-time events
$el.one('click', handler);     // Fires once, then auto-unbinds
```

### AJAX

```javascript
// Standard WordPress AJAX
$.ajax({
    url: myVars.ajaxUrl,        // wp_localize_script value
    type: 'POST',
    data: {
        action: 'my_action',    // WordPress action hook
        nonce: myVars.nonce,    // Security token
        id: itemId
    },
    success: function(response) {
        if (response.success) {
            // response.data contains the payload
        }
    },
    error: function(xhr, status, error) {
        console.error('AJAX failed:', error);
    }
});

// Shorthand GET
$.get(myVars.restUrl + '/items', function(data) {
    renderItems(data);
});

// Shorthand POST
$.post(myVars.ajaxUrl, { action: 'save_item', data: formData }, function(response) {
    handleResponse(response);
});

// Promise-style (chainable)
$.ajax({ url: '/api/data', dataType: 'json' })
    .done(function(data) { /* success */ })
    .fail(function(xhr) { /* error */ })
    .always(function() { /* cleanup */ });
```

### Utilities

```javascript
// Iteration
$.each(array, function(index, value) { });
$.each(object, function(key, value) { });
$('.items').each(function(index) {
    var $this = $(this);        // Cache for performance
});

// Type checking — prefer native equivalents
Array.isArray(val)              // Not $.isArray (deprecated)
typeof val === 'string'         // Not $.type (deprecated)
val != null                     // Not $.isNullOrUndefined

// Object merge (deep copy)
var merged = $.extend(true, {}, defaults, options);

// Serialize form data
var data = $form.serialize();           // URL-encoded string
var dataArray = $form.serializeArray(); // Array of {name, value}
```

## Common Patterns

### Cache jQuery Selections

```javascript
// BAD: Re-querying DOM repeatedly
$('.my-element').addClass('active');
$('.my-element').find('.child').show();
$('.my-element').data('loaded', true);

// GOOD: Cache the selection
var $el = $('.my-element');
$el.addClass('active');
$el.find('.child').show();
$el.data('loaded', true);

// BEST: Chain when possible
$('.my-element')
    .addClass('active')
    .find('.child').show()
    .end()                      // Go back to .my-element
    .data('loaded', true);
```

### Delegated Events for Dynamic Content

```javascript
// BAD: Won't work for dynamically added elements
$('.delete-btn').on('click', handleDelete);

// GOOD: Delegated — works for current AND future elements
$('.item-list').on('click', '.delete-btn', handleDelete);

// Use delegation when:
// - Elements are added/removed dynamically (AJAX, repeaters)
// - Many identical handlers (performance — one handler vs hundreds)
```

### UI State Management

```javascript
(function($) {
    'use strict';

    // Pure: Compute next state
    function getToggleState($el) {
        return !$el.hasClass('is-open');
    }

    // Impure: Apply state to DOM
    function applyToggleState($trigger, $target, isOpen) {
        $trigger.attr('aria-expanded', isOpen);
        $target.toggleClass('is-open', isOpen);
        if (isOpen) {
            $target.slideDown(200);
        } else {
            $target.slideUp(200);
        }
    }

    // Wire up
    $('.accordion').on('click', '.accordion-trigger', function(e) {
        e.preventDefault();
        var $trigger = $(this);
        var $target = $($trigger.data('target'));
        applyToggleState($trigger, $target, getToggleState($target));
    });
})(jQuery);
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Vanilla JS when jQuery is loaded | Verbose, inconsistent | Use jQuery for DOM work |
| `document.querySelectorAll` + `forEach` in WP | Ignores available jQuery | `$('.selector').each()` |
| Mixing jQuery and vanilla in same file | Inconsistent, confusing | Pick one per file |
| Not caching `$(this)` in loops | Re-wraps DOM element each time | `var $this = $(this)` |
| `$('.selector')` inside loops | Re-queries DOM each iteration | Cache outside loop |
| Direct binding on dynamic elements | Handlers lost on DOM change | Use delegated `.on()` |
| Creating custom `pipe()` / `compose()` | Over-engineering | jQuery chaining IS composition |

## Integration

- **js-fp**: Core FP principles (purity, immutability, testing). jQuery DOM code follows these — pure logic extracted, side effects in DOM wrapper.
- **js-fp-wordpress**: WordPress-specific integration (GF hooks, ACF hooks, admin JS). References this skill for jQuery patterns.
- **ima-bootstrap**: Bootstrap 5 JS components. jQuery available but BS5 doesn't require it — use for custom enhancements.
- **Context7**: For deep jQuery API lookups use library ID `/jquery/jquery`.

## WordPress Coding Standards

Per WordPress JS coding standards:
- Use tabs for indentation
- IIFE wrapper with `jQuery` passed as `$`
- `'use strict'` inside the IIFE
- Spaces inside parentheses: `if ( condition )` not `if (condition)`
- `var` declarations at top of scope (unless using build tools with ES6+)

See [WordPress JavaScript Coding Standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/javascript/) for full reference.
