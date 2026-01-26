# Quasar Theme Integration - CSS Variables & SCSS Patterns

**Purpose**: Guide for integrating custom themes with Quasar's utility system

---

## Theme System Architecture

### Three-Layer System

**Layer 1: Theme Definition** (`src/styles/theme.scss`)
- Central source of truth for colors, typography, spacing
- SCSS variables for build-time values
- CSS custom properties for runtime theming (dark mode)

**Layer 2: Quasar Integration** (`src/css/quasar.variables.scss`)
- Maps theme to Quasar's color system
- Overrides Quasar defaults with brand colors

**Layer 3: Component Usage**
- Quasar utilities use theme automatically (`text-primary`, `bg-secondary`)
- Custom CSS uses theme variables for brand-specific styling

---

## CSS Custom Properties vs SCSS Variables

### CSS Custom Properties (Runtime)

**Use for:** Values that change at runtime (dark mode, user preferences)

```scss
:root {
  --color-text-primary: #391c11;
  --color-prayer-text: #f0dab8;
}

body.body--dark {
  --color-text-primary: #f0dab8;
}
```

```vue
<style scoped>
.prayer-text {
  color: var(--color-prayer-text);  /* Auto-switches in dark mode */
}
</style>
```

### SCSS Variables (Build-Time)

**Use for:** Static values that don't change at runtime

```scss
$color-brand-primary: #844628;
$font-family-prayer: 'Crimson Text', serif;
```

```vue
<style scoped lang="scss">
@import '@/styles/theme.scss';

.custom-element {
  background-color: rgba($color-brand-primary, 0.05);
  font-family: $font-family-prayer;
}
</style>
```

---

## Quasar Color Integration

### Mapping Custom Colors

**In `quasar.variables.scss`:**
```scss
@import '@/styles/theme.scss';

$primary: $color-brand-primary;
$secondary: $color-brand-secondary;
$accent: $color-brand-accent;

// Now Quasar utilities use your brand colors!
// class="text-primary" uses your custom color
```

---

## Decision Tree

```
Need to style something?
|-- Is it spacing, typography, or layout?
|   --> Use Quasar utilities (q-pa-md, text-h5, row)
|
|-- Is it a color in Quasar's palette?
|   --> Use Quasar color utilities (text-primary, bg-grey-1)
|
|-- Is it a custom brand color?
|   --> Use SCSS variable: rgba($color-brand-primary, 0.05)
|
|-- Does it need to change in dark mode?
|   --> Use CSS custom property: var(--color-prayer-text)
|
|-- Is it a unique design element?
    --> Write minimal custom CSS with theme variables
```

---

## Theme Mixin Patterns

**Define in `theme.scss`:**
```scss
@mixin prayer-text-base {
  font-family: $font-family-prayer;
  color: var(--color-prayer-text);
  line-height: $line-height-relaxed;
}

@mixin bg-elevated {
  background-color: var(--color-surface-elevated);
  border-radius: $radius-md;
  box-shadow: $shadow-sm;
}
```

**Use in components:**
```vue
<style scoped lang="scss">
@import '@/styles/theme.scss';

.prayer-content {
  @include prayer-text-base;
}
</style>
```

---

## Complete Example: Hybrid Approach

```vue
<template>
  <q-card flat bordered class="prayer-card rounded-borders q-mb-lg">
    <q-card-section>
      <!-- Header: 100% utilities -->
      <div class="row items-start q-mb-md">
        <div class="prayer-number row items-center justify-center">1</div>
        <div class="col">
          <h2 class="text-h5 text-weight-bold text-primary q-mb-sm q-mt-none">
            Prayer Title
          </h2>
        </div>
      </div>

      <!-- Content: utilities + custom mixin -->
      <div class="prayer-content q-pa-md q-my-md rounded-borders">
        <pre class="prayer-text">Prayer text</pre>
      </div>
    </q-card-section>
  </q-card>
</template>

<style scoped lang="scss">
@import '@/styles/theme.scss';

/* Custom CSS ONLY for theme-specific brand elements */

.prayer-card {
  background-color: rgba($color-brand-primary, 0.05);
  border-color: rgba($color-brand-primary, 0.2);
}

.prayer-number {
  width: 48px;
  height: 48px;
  background-color: $color-brand-primary;
  color: white;
  border-radius: 50%;
}

.prayer-text {
  @include prayer-text-base;
}

/* Dark mode */
body.body--dark {
  .prayer-card {
    background-color: rgba($color-brand-primary, 0.15);
  }
}
</style>
```

---

## Common Mistakes & Solutions

### Mistake 1: Hardcoded Colors

Bad: `color: #844628;`
Good: `class="text-primary"` or `color: $color-brand-primary;`

### Mistake 2: Magic Number Spacing

Bad: `padding: 17px;`
Good: `class="q-pa-md"` (16px from 8px grid)

### Mistake 3: Bypassing Dark Mode

Bad: `background: #ffffff;`
Good: `class="bg-grey-1"` or `background-color: var(--color-surface-bg);`

---

## CSS Architecture Summary

**Ideal Component Structure:**
- 80% utilities in template
- 20% custom CSS in style block

**What Goes Where:**
- **Utilities**: spacing, typography, layout, standard colors
- **SCSS Variables**: brand colors, custom fonts
- **CSS Properties**: runtime theme values (dark mode)
- **Mixins**: reusable patterns

---

**Reference**: https://quasar.dev/style/theme-builder
