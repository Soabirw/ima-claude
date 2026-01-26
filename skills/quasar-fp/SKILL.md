---
name: "quasar-fp"
description: "Quasar Framework best practices with utility-first CSS and FP patterns. Use when working with .vue files in Quasar projects, when creating Vue/Quasar components, or when user mentions Quasar, QBtn, QCard, or utility classes like q-pa-md. Enforces utility-first approach to prevent hand-written CSS for standard properties."
---

# Quasar Framework - Functional Patterns & Utility-First Approach

## Core Principles

**Primary Directive**: "Utilities > custom CSS | Components > HTML | Theme system > inline styles"

### Anti-Over-Engineering for Quasar
- **DO NOT** write custom CSS for spacing, typography, colors, layout (use utilities)
- **DO NOT** reinvent components that Quasar provides (QBtn, QCard, QDialog, etc.)
- **DO NOT** bypass theme system with hardcoded colors or magic numbers
- **DO** use utilities first, custom CSS only for theme-specific brand elements
- **DO** leverage Quasar components for consistent UX and accessibility
- **DO** integrate with theme system via CSS custom properties and SCSS variables

---

## Quick Decision Tree

```
Creating new component?
|-- Can Quasar utility classes handle spacing/layout/text?
|   |-- YES --> Use utilities (q-pa-*, text-*, row/column)
|   |-- NO --> Is this a standard UI pattern?
|       |-- YES --> Use Quasar component (QBtn, QCard, QDialog)
|       |-- NO --> Custom CSS, but use theme variables
|
|-- Final check: Does custom CSS exceed 20% of total styling?
    |-- YES --> Refactor to use more utilities
```

---

## Utility-First Pattern

### GOOD: Utility-First Approach

```vue
<template>
  <div class="q-pa-md q-mb-lg rounded-borders">
    <h2 class="text-h5 text-weight-bold text-primary q-mb-sm q-mt-none">
      Title
    </h2>
    <p class="text-caption text-grey-7 q-mb-none">
      Description text
    </p>
    <q-toggle
      v-model="enabled"
      label="Enable Feature"
      class="text-weight-medium q-mb-sm"
    />
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

### BAD: Hand-Written CSS for Standard Properties

```vue
<!-- DO NOT DO THIS - utilities exist for all of these! -->
<style scoped>
.my-container {
  padding: 16px;              /* Use q-pa-md */
  margin-bottom: 24px;        /* Use q-mb-lg */
}
.my-title {
  font-size: 1.5rem;          /* Use text-h5 */
  font-weight: 700;           /* Use text-weight-bold */
  color: #1976D2;             /* Use text-primary */
}
</style>
```

---

## Common Anti-Patterns & Fixes

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

---

## When to Use Custom CSS

Custom CSS is appropriate ONLY for:

1. **Theme-Specific Brand Colors:**
   ```scss
   .prayer-card {
     background-color: rgba($color-brand-primary, 0.05);
     border-left: $border-width-thick solid $color-brand-accent;
   }
   ```

2. **Unique Design Elements:**
   ```scss
   .circular-badge {
     width: 48px;
     height: 48px;
     border-radius: 50%;
     background-color: $color-brand-primary;
   }
   ```

3. **Custom Font Families:**
   ```scss
   .prayer-title {
     font-family: $font-family-prayer;
   }
   ```

4. **Dark Mode Theme Overrides:**
   ```scss
   body.body--dark {
     .prayer-card {
       background-color: rgba($color-brand-primary, 0.15);
     }
   }
   ```

---

## Settings Panel Pattern

```vue
<script setup>
import { useUserPreferences } from '@/composables/useUserPreferences.js';
const userPrefs = useUserPreferences();
</script>

<template>
  <q-expansion-item
    default-opened
    icon="settings"
    label="Settings Section"
    header-class="text-weight-bold"
  >
    <div class="q-pa-md">
      <div class="q-pa-md q-mb-md rounded-borders bg-grey-1">
        <q-toggle
          v-model="userPrefs.someOption"
          label="Enable Feature"
          class="text-weight-medium q-mb-sm"
        />
        <p class="text-caption text-grey-7 q-pl-sm q-mb-none">
          Feature description using Quasar utilities
        </p>
      </div>
    </div>
  </q-expansion-item>
</template>

<style scoped lang="scss">
@import '@/styles/theme.scss';

/* Minimal custom CSS - ONLY for theme brand colors */
.option-box {
  background-color: rgba($color-brand-secondary, 0.08);
  border-left: $border-width-thick solid $color-brand-primary;
}
</style>
```

---

## Page Layout Pattern

```vue
<template>
  <q-page class="q-pa-md">
    <!-- Header with utilities -->
    <div class="text-center q-py-lg q-mb-lg page-header">
      <h1 class="text-h3 text-weight-bold text-primary q-mb-sm q-mt-none">
        Page Title
      </h1>
      <p class="text-h6 text-italic text-accent q-mb-none">
        Subtitle
      </p>
    </div>

    <!-- Content sections -->
    <div class="q-mb-xl">
      <h2 class="text-h5 text-weight-bold text-primary q-my-md">
        Section Title
      </h2>
      <!-- Content -->
    </div>
  </q-page>
</template>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.page-header {
  border-bottom: 2px solid rgba($color-brand-primary, 0.3);
}
</style>
```

---

## Composable Integration

```javascript
import { useQuasar } from 'quasar';
import { computed } from 'vue';

export function useThemeAwareStyles() {
  const $q = useQuasar();

  // Pure function: derive classes from state
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

---

## Reference Files

For detailed information, consult these reference files:

- **[references/utility-classes.md](references/utility-classes.md)** - Complete utility class reference (spacing, typography, colors, flexbox)
- **[references/component-patterns.md](references/component-patterns.md)** - Quasar component usage patterns (QBtn, QCard, QDialog, etc.)
- **[references/theme-integration.md](references/theme-integration.md)** - Theme system, SCSS variables, CSS custom properties, dark mode

---

## Component Quick Reference

| Need | Use Component | Not HTML |
|------|---------------|----------|
| Button | `<q-btn>` | `<button>` |
| Text input | `<q-input>` | `<input>` |
| Dropdown | `<q-select>` | `<select>` |
| Toggle | `<q-toggle>` | Custom toggle |
| Card | `<q-card>` | `<div class="card">` |
| Modal | `<q-dialog>` | Custom modal |
| Tabs | `<q-tabs>` | Custom tabs |
| List | `<q-list>` + `<q-item>` | `<ul>` + `<li>` |

---

## Essential Utility Classes

### Spacing (8px grid)
- `q-pa-{xs|sm|md|lg|xl}` - Padding all sides (4px, 8px, 16px, 24px, 48px)
- `q-mb-{size}` - Margin bottom
- `q-mt-none` - Remove margin top

### Typography
- `text-h1` through `text-h6` - Headings
- `text-body1`, `text-body2`, `text-caption` - Body text
- `text-weight-bold`, `text-weight-medium` - Font weight
- `text-italic`, `text-uppercase` - Text style

### Colors
- `text-primary`, `text-secondary`, `text-accent` - Brand colors
- `text-grey-7` - Muted text
- `bg-grey-1` - Light background

### Layout
- `row`, `column` - Flex containers
- `items-center`, `justify-between` - Alignment
- `col`, `col-auto` - Flex items

---

## Success Metrics

Target values for components using this skill:
- Utility usage: 80%+ (utilities vs custom CSS)
- CSS reduction: 30-50% compared to hand-written
- Quasar component usage: 90%+ (vs raw HTML)
- Theme integration: 100% (no hardcoded colors)
- Dark mode support: Automatic via theme system

---

## Integration

### Dependencies
- Requires: `js-fp-vue` (Vue 3 FP patterns)

### Context7 Integration
Query Quasar docs when user asks about specific components or configuration:
```javascript
resolveLibraryId({ libraryName: 'quasar', query: 'QTable pagination' })
```

### Official Documentation
- Main: https://quasar.dev
- Utilities: https://quasar.dev/style/spacing
- Components: https://quasar.dev/vue-components

---

**Framework Version**: Quasar v2 + Vue 3
**Status**: Production-ready
