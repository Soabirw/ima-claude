---
name: "quasar-fp"
description: "Quasar Framework best practices with utility-first CSS and FP patterns. Use when working with .vue files in Quasar projects, when creating Vue/Quasar components, or when user mentions Quasar, QBtn, QCard, or utility classes like q-pa-md. Enforces utility-first approach to prevent hand-written CSS for standard properties."
---

# Quasar Framework - Utility-First + FP

**Directive**: Utilities > custom CSS | Components > HTML | Theme system > inline styles

## Rules

- Use utility classes for spacing, typography, colors, layout — no custom CSS for these
- Use Quasar components (QBtn, QCard, QDialog, etc.) — don't reinvent them
- Integrate with theme system via CSS custom properties and SCSS variables
- Custom CSS only for theme-specific brand elements

## Decision Tree

```
Creating new component?
├── Can Quasar utilities handle spacing/layout/text?
│   ├── YES → Use utilities (q-pa-*, text-*, row/column)
│   └── NO → Standard UI pattern?
│       ├── YES → Use Quasar component (QBtn, QCard, QDialog)
│       └── NO → Custom CSS with theme variables
└── Does custom CSS exceed 20% of total styling? → Refactor to more utilities
```

## Anti-Patterns & Fixes

| Anti-Pattern | Fix |
|--------------|-----|
| `padding: 16px;` | `class="q-pa-md"` |
| `margin-bottom: 24px;` | `class="q-mb-lg"` |
| `font-size: 1.5rem; font-weight: 700;` | `class="text-h5 text-weight-bold"` |
| `color: #1976D2;` | `class="text-primary"` |
| `display: flex; align-items: center;` | `class="row items-center"` |
| `<button>` | `<q-btn>` |
| `<input>` | `<q-input>` |
| Custom card div | `<q-card>` |

## Utility-First Example

```vue
<template>
  <div class="q-pa-md q-mb-lg rounded-borders">
    <h2 class="text-h5 text-weight-bold text-primary q-mb-sm q-mt-none">Title</h2>
    <p class="text-caption text-grey-7 q-mb-none">Description</p>
    <q-toggle v-model="enabled" label="Enable Feature" class="text-weight-medium q-mb-sm" />
  </div>
</template>

<style scoped lang="scss">
@import '@/styles/theme.scss';
/* ONLY theme-specific custom styling */
.custom-theme-box {
  background-color: rgba($color-brand-primary, 0.05);
  border-left: $border-width-thick solid $color-brand-accent;
}
</style>
```

## When Custom CSS Is Appropriate

1. Theme-specific brand colors: `rgba($color-brand-primary, 0.05)`
2. Unique design elements: circular badges, custom shapes
3. Custom font families: `font-family: $font-family-prayer`
4. Dark mode theme overrides: `body.body--dark { ... }`

## Composable Integration

```javascript
import { useQuasar } from 'quasar';
import { computed } from 'vue';

export function useThemeAwareStyles() {
  const $q = useQuasar();
  const containerClasses = computed(() => ({
    'q-pa-md': true,
    'q-mb-lg': true,
    'rounded-borders': true,
    'bg-grey-1': !$q.dark.isActive,
    'bg-grey-9': $q.dark.isActive
  }));
  return { containerClasses };
}
```

## Component Quick Reference

| Need | Component |
|------|-----------|
| Button | `<q-btn>` |
| Text input | `<q-input>` |
| Dropdown | `<q-select>` |
| Toggle | `<q-toggle>` |
| Card | `<q-card>` |
| Modal | `<q-dialog>` |
| Tabs | `<q-tabs>` |
| List | `<q-list>` + `<q-item>` |

## Essential Utility Classes

**Spacing (8px grid):** `q-pa-{xs|sm|md|lg|xl}` (4/8/16/24/48px), `q-mb-{size}`, `q-mt-none`

**Typography:** `text-h1`–`text-h6`, `text-body1`, `text-body2`, `text-caption`, `text-weight-bold`, `text-weight-medium`, `text-italic`, `text-uppercase`

**Colors:** `text-primary`, `text-secondary`, `text-accent`, `text-grey-7`, `bg-grey-1`

**Layout:** `row`, `column`, `items-center`, `justify-between`, `col`, `col-auto`

## Targets

- Utility usage: 80%+ vs custom CSS
- Quasar component usage: 90%+ vs raw HTML
- Theme integration: 100% (no hardcoded colors)
- Dark mode: automatic via theme system

## References

- **[references/utility-classes.md](references/utility-classes.md)** — Complete utility class reference
- **[references/component-patterns.md](references/component-patterns.md)** — Component usage patterns
- **[references/theme-integration.md](references/theme-integration.md)** — SCSS variables, dark mode

Requires: `js-fp-vue` | Framework: Quasar v2 + Vue 3
Docs: https://quasar.dev | https://quasar.dev/style/spacing | https://quasar.dev/vue-components
