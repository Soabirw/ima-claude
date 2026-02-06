---
name: "ima-bootstrap"
description: "Bootstrap 5.3 with IMA brand integration for WordPress/Picostrap5 sites. Utility-first CSS, component patterns, SCSS customization, and IMA brand system (colors, typography, mixins). Use when: writing HTML with Bootstrap classes, creating Bootstrap components, styling WordPress templates, customizing Bootstrap Sass variables, working with IMA brand colors/typography/components, building responsive layouts, or when user mentions Bootstrap, btn-, card, modal, accordion, grid, container, row, col, d-flex, text-center, bg-primary, or IMA brand colors."
---

# IMA Bootstrap

Bootstrap 5.3 with IMA brand integration for WordPress/Picostrap5 child theme sites.

## Core Principle

**Utility-first: prefer Bootstrap utility classes over custom CSS.**

```
Need spacing/display/flex/text? → Bootstrap utility class
Need IMA brand color/typography? → IMA SCSS variable or mixin
Need component? → Bootstrap component + IMA brand overrides
Need deep Bootstrap API details? → Context7: /websites/getbootstrap
```

## Decision Tree

```
Writing HTML/template markup?
├── Layout → .container, .row, .col-{bp}-{n} (12-column grid)
├── Spacing → .m{side}-{size}, .p{side}-{size} (0-5 scale)
├── Display → .d-{value}, .d-{bp}-{value}
├── Flex → .d-flex, .justify-content-{v}, .align-items-{v}
├── Text → .text-{align}, .fw-{weight}, .fs-{size}
├── Colors → .text-{color}, .bg-{color} (primary = IMA indigo)
├── Component → card, modal, accordion, btn, badge, alert, navbar
└── Custom need? → Check IMA brand mixins first, then write SCSS

Writing SCSS?
├── Use IMA variable → $ima-brand-{color}, $ima-font-{prop}
├── Use IMA mixin → @include ima-{component}
├── Override Bootstrap → Set $variable BEFORE @import "bootstrap5/variables"
└── Custom utility? → Probably Bootstrap already has it
```

## Anti-Patterns

| BAD | GOOD | Why |
|-----|------|-----|
| `margin-top: 16px` | `class="mt-3"` | Bootstrap spacing scale |
| `display: flex` | `class="d-flex"` | Bootstrap utility |
| `color: #040C53` | `$ima-brand-primary` or `.text-primary` | Theme-mapped |
| `font-family: Lato` | `$ima-font-family-primary` | Centralized |
| `border-radius: 10px` on every element | Already set via `$border-radius` | Global override |
| Custom `.my-card { padding: 24px; ... }` | `class="card"` | Cards already IMA-branded |
| `@media (min-width: 768px)` for layout | `class="col-md-6"` | Grid handles it |

## Bootstrap Utility Quick Reference

### Spacing (rem-based, 0-5 scale)
- **Pattern**: `{property}{side}-{size}` → `mt-3`, `px-4`, `mb-0`
- **Properties**: `m` (margin), `p` (padding)
- **Sides**: `t` top, `b` bottom, `s` start, `e` end, `x` horizontal, `y` vertical, blank = all
- **Sizes**: `0`=0, `1`=0.25rem, `2`=0.5rem, `3`=1rem, `4`=1.5rem, `5`=3rem, `auto` (margin only)

### Display & Flex
- `d-none`, `d-block`, `d-flex`, `d-grid`, `d-inline-block`
- Responsive: `d-{bp}-{value}` → `d-none d-md-block` (hidden below md)
- `flex-row`, `flex-column`, `flex-wrap`, `flex-nowrap`
- `justify-content-{start|center|end|between|around|evenly}`
- `align-items-{start|center|end|stretch|baseline}`
- `gap-{0-5}`, `row-gap-{n}`, `column-gap-{n}`

### Grid (12-column)
- `.container` (responsive), `.container-fluid` (full-width)
- `.col`, `.col-{1-12}`, `.col-{bp}-{1-12}`
- Breakpoints: `sm`≥576, `md`≥768, `lg`≥992, `xl`≥1200, `xxl`≥1400
- `.offset-{bp}-{n}`, `.order-{bp}-{n}`

### Text & Typography
- `text-start`, `text-center`, `text-end`
- `fw-bold`, `fw-semibold`, `fw-normal`, `fw-light`
- `fs-1` (largest) through `fs-6` (smallest)
- `text-uppercase`, `text-lowercase`, `text-capitalize`
- `text-nowrap`, `text-break`, `text-truncate`

### Colors (IMA-mapped via theme)
- Text: `text-primary` (indigo), `text-secondary` (teal), `text-danger`, `text-warning`, `text-success`, `text-info`, `text-muted`, `text-white`
- Background: `bg-primary`, `bg-secondary`, `bg-light`, `bg-dark`, `bg-white`, `bg-body-tertiary`
- Subtle: `text-{color}-emphasis`, `bg-{color}-subtle`

### Sizing & Position
- `w-25`, `w-50`, `w-75`, `w-100`, `w-auto`, `mw-100`
- `h-25`, `h-50`, `h-75`, `h-100`, `h-auto`
- `position-relative`, `position-absolute`, `position-fixed`, `position-sticky`
- `top-0`, `start-0`, `end-0`, `bottom-0`, `translate-middle`

### Borders & Shadows
- `border`, `border-top`, `border-0`, `border-top-0`
- `rounded`, `rounded-{0-5}`, `rounded-circle`, `rounded-pill`
- `shadow-none`, `shadow-sm`, `shadow`, `shadow-lg`

### Visibility
- `visible`, `invisible` (layout preserved)
- `visually-hidden` (screen reader only)

## Key Components

### Cards (IMA: no shadow, 10px radius, 24px padding)
```html
<div class="card">
  <div class="card-header">Title</div>
  <div class="card-body">
    <h5 class="card-title">Heading</h5>
    <p class="card-text">Content</p>
    <a href="#" class="btn btn-primary">Action</a>
  </div>
</div>
```

### Modals
```html
<button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal">Open</button>
<div class="modal fade" id="myModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Title</h5>
        <button class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">Content</div>
      <div class="modal-footer">
        <button class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button class="btn btn-primary">Save</button>
      </div>
    </div>
  </div>
</div>
```

### Accordion
```html
<div class="accordion" id="acc1">
  <div class="accordion-item">
    <h2 class="accordion-header">
      <button class="accordion-button" data-bs-toggle="collapse" data-bs-target="#c1">Item 1</button>
    </h2>
    <div id="c1" class="accordion-collapse collapse show" data-bs-parent="#acc1">
      <div class="accordion-body">Content</div>
    </div>
  </div>
</div>
```

### Buttons (IMA: Lato Bold 18px, 20px/40px padding, 10px radius)
```html
<button class="btn btn-primary">Primary (teal)</button>
<button class="btn btn-outline-primary">Outline</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-lg btn-primary">Large (20px radius)</button>
```

### Tables
```html
<div class="table-responsive">
  <table class="table table-striped table-hover">
    <thead><tr><th>Column</th></tr></thead>
    <tbody><tr><td>Data</td></tr></tbody>
  </table>
</div>
```

## IMA Brand Integration

For detailed IMA brand variables, colors, mixins, and component patterns:
- See [references/ima-brand.md](references/ima-brand.md)

For theme SCSS architecture and Bootstrap variable override chain:
- See [references/theme-integration.md](references/theme-integration.md)

For extended Bootstrap utility patterns and Sass customization:
- See [references/bootstrap-patterns.md](references/bootstrap-patterns.md)

### Quick IMA Color Reference

| Name | Hex | SCSS Variable | Bootstrap Class |
|------|-----|---------------|-----------------|
| Trustworthy Indigo | `#040C53` | `$ima-brand-primary` | `.text-primary`, `.bg-primary` |
| Aquatic Pulse | `#0296A1` | `$ima-brand-secondary` | `.text-secondary`, `.bg-secondary` |
| Bright Teal | `#00B8B8` | `$ima-brand-accent-teal` | (hover states) |
| Guidance Sky | `#A2CFF0` | `$ima-brand-sky` | — |
| Vital Gold | `#FFCC00` | `$ima-brand-gold` | `.text-warning`, `.bg-warning` |
| Red Ribbon | `#DD153B` | `$ima-brand-red` | `.text-danger`, `.bg-danger` |
| Clarity Wash | `#F2F3F5` | `$ima-brand-gray-light` | `.bg-light` |

### IMA Typography Mixins
```scss
@include ima-page-header;        // Lato Bold 40px, uppercase, primary
@include ima-section-header;     // Lato Bold 20px, primary
@include ima-provider-title;     // Lato Semi Bold 32px, primary
@include ima-button-text;        // Lato Bold 18px, uppercase
@include ima-body-text;          // Proxima Nova Regular 16px
@include ima-form-label;         // Open Sans 14px, gray
```

### IMA Component Mixins
```scss
@include ima-button-primary;      // Teal bg, white text, 20px/40px padding
@include ima-button-primary-wide; // Same, 80px horizontal padding
@include ima-button-outline;      // Transparent bg, primary border
@include ima-form-field;          // 15px radius, gray border, teal focus
@include ima-card;                // Light gray bg, no shadow, 10px radius
@include ima-card-white;          // White bg, 1px gray border
@include ima-gradient-bg;         // 150deg gradient, #00066F → #00B8B8
```

## SCSS File Locations

```
picostrap5-child-base/sass/
├── main.scss                    ← Entry point
├── _bootstrap-loader.scss       ← Bootstrap import chain
├── _theme_variables.scss        ← Variable overrides (loads IMA brand)
├── _custom.scss                 ← Modular custom styles
├── base/                        ← Global base styles
├── components/                  ← Reusable components
├── pages/                       ← Page-specific styles
└── bootstrap5/                  ← Bootstrap 5.3 source (DO NOT EDIT)

plugins/ima-brand/sass/
├── brand.scss                   ← Main import
├── _variables.scss              ← Colors, typography, spacing
├── _typography.scss             ← Font mixins
└── _spacing.scss                ← Component mixins, layout
```

**Import order**: Bootstrap functions → IMA brand → theme variables → Bootstrap variables → Bootstrap components → custom styles

## Context7 Integration

For deep Bootstrap docs (specific component APIs, all Sass variables):
```
mcp__context7__query-docs({ libraryId: "/websites/getbootstrap", query: "..." })
```

Example queries: `"navbar responsive collapse"`, `"form validation custom styles"`, `"utility API extend"`, `"offcanvas placement responsive"`

## Success Metrics

- Bootstrap utility usage: ≥80% (vs custom CSS for standard properties)
- IMA brand variables: 100% (no hardcoded brand colors)
- Custom CSS only for: truly custom patterns with no Bootstrap equivalent
- Bootstrap components: used for all standard UI patterns
