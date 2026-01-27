---
name: ima-forms-expert
description: |
  WordPress form component library with Bootstrap 5 integration, validators-at-registration
  architecture (v1.4.0+), and security-first patterns. Use when: building custom forms
  with IMA Forms components (ima_forms_* functions), implementing form validation,
  adding field types (text, email, phone, select, checkbox, repeater, consent agreement),
  creating dynamic repeater fields, handling AJAX form submissions, or integrating forms
  with ACF/custom post types. Key features: validators built as closures at field registration
  (single source of truth), enhanced email validation with disposable domain blocking,
  template-driven validation where "template IS the definition".
---

# IMA Forms Expert

WordPress form component library with Bootstrap 5 + functional programming patterns.

## When to Use This Skill

- Building custom forms using IMA Forms component library
- Implementing template-driven validation (v1.3.0+)
- Understanding validators-at-registration architecture (v1.4.0+)
- Adding field types or container components
- Creating repeater/dynamic field patterns
- Integrating forms with WordPress (ACF, custom post types, AJAX)
- Debugging form submission issues

## Core Principles

- **Template IS the definition**: Field rendering auto-registers validation specs + validators
- **Validators at registration**: Field functions build closures at registration time (v1.4.0)
- **Security by default**: Nonce verification, sanitization, escaping
- **Component-based**: Reusable field and container components
- **Bootstrap 5 native**: Uses Bootstrap utilities and components

## Architecture (v1.4.0 - Unified Validator Registry)

```
ima-forms/
├── ima-forms.php                      # Plugin initialization
├── includes/
│   ├── functions-core.php             # Security chokepoint, higher-order functions
│   ├── functions-registry.php         # Field spec registry (stores validators)
│   ├── functions-validation-engine.php # Runs validators, sanitizes data
│   ├── functions-fields.php           # Field rendering + validator building
│   ├── functions-containers.php       # Container/layout components
│   ├── functions-validators.php       # Pure validation functions
│   ├── functions-sanitizers.php       # Context-appropriate sanitization
│   ├── functions-form.php             # Form factory (v1.2.0)
│   └── forms/                         # Form implementations
├── templates/
│   ├── fields/                        # Field templates
│   ├── containers/                    # Container templates
│   └── forms/                         # Complete form templates
└── assets/js/                         # Vanilla JS (repeater, consent, AJAX)
```

### Validators-at-Registration Pattern (v1.4.0)

**Key change from v1.3.0**: Validators are now built as closures at field registration time, not rebuilt by the engine via type-switching.

```php
// Inside ima_forms_email_field_register():
$validators = [];

if ($required) {
    $validators[] = fn($v) => ima_forms_validate_required($v, $label);
}

$validators[] = function($v) use ($label, $enhanced) {
    if (empty($v)) return null;
    return ima_forms_validate_email_enhanced((string) $v, $label, $enhanced);
};

ima_forms_register_field_spec($name, [
    'type' => 'email',
    'label' => $label,
    'required' => $required,
    'validators' => $validators,  // Closures stored at registration!
]);
```

**Benefits**:
- Single source of truth: field function defines validation once
- No type switching: validators are closures, just iterate and run
- Testable: validators are pure functions captured at registration time

## Key Patterns

### Template-Driven Validation

Field functions auto-register specs + validators. Validate entire form in one call:

```php
$result = ima_forms_validate_form('templates/forms/my-form', $_POST, 'my-form');

if (!$result['valid']) {
    wp_send_json_error(['errors' => $result['errors']], 400);
}

$sanitized = $result['sanitized'];  // Ready to use
```

→ **Details**: See [references/validation-engine.md](references/validation-engine.md)

### Enhanced Email Validation

Blocks disposable domains, detects typos:

```php
ima_forms_email_field([
    'name' => 'email',
    'enhanced_validation' => true,  // gmial.com → suggests gmail.com
]);
```

## Quick Start Example

```php
// Template: templates/forms/contact.php
ima_forms_form(['id' => 'contact', 'action' => 'contact_submit'], function() use ($data, $errors) {
    ima_forms_text_field(['name' => 'name', 'label' => 'Name', 'required' => true, ...]);
    ima_forms_email_field(['name' => 'email', 'required' => true, 'enhanced_validation' => true, ...]);
    ima_forms_textarea_field(['name' => 'message', 'required' => true, ...]);
    ima_forms_submit_button(['text' => 'Send']);
});

// AJAX Handler
function contact_submit_handler() {
    if (!wp_verify_nonce($_POST['nonce'], 'ima_forms_ajax')) {
        wp_send_json_error(['message' => 'Security check failed.'], 403);
    }

    $result = ima_forms_validate_form('templates/forms/contact', $_POST, 'contact');

    if (!$result['valid']) {
        wp_send_json_error(['errors' => $result['errors']], 400);
    }

    // Process $result['sanitized']...
    wp_send_json_success(['message' => 'Sent!']);
}
add_action('wp_ajax_contact_submit', 'contact_submit_handler');
add_action('wp_ajax_nopriv_contact_submit', 'contact_submit_handler');
```

## Reference Files

| File | Read When |
|------|-----------|
| [validation-engine.md](references/validation-engine.md) | Using `ima_forms_validate_form()`, understanding validator registry, custom validators |
| [field-components.md](references/field-components.md) | Adding specific field types, customizing field behavior, repeaters |
| [container-components.md](references/container-components.md) | Using cards, sections, column layouts, fieldsets |
| [examples.md](references/examples.md) | Implementing complete new forms, testing patterns, anti-patterns |
| [quick-reference.md](references/quick-reference.md) | Function signatures, version features, filters |

## Common Tasks

| Task | Approach |
|------|----------|
| Add a simple form | Use `ima_forms_form()` + field components + `ima_forms_validate_form()` |
| Add custom validation | Filter: `add_filter('ima_forms_validate_{form-id}', ...)` |
| Block spam emails | Set `enhanced_validation => true` on email fields |
| Add repeater rows | Use `ima_forms_repeater()` with row callback |
| Create multi-column layout | Use `ima_forms_column_layout(['columns' => 3, ...])` |
| Debug validation | Use `ima_forms_debug_field_specs()` or `ima_forms_debug_validation_summary($specs)` |

## Success Indicators

- ✅ Template-driven validation (no manual field maps)
- ✅ Enhanced email validation on user-facing forms
- ✅ Standardized form wrappers (`ima_forms_form()`)
- ✅ Nonce verification in all AJAX handlers
- ✅ Sanitized data used for processing (never raw `$_POST`)
- ✅ Validators built at registration, not in engine
