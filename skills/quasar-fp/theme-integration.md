# Quasar Theme Integration - CSS Variables & SCSS Patterns

**Purpose**: Guide for integrating custom themes with Quasar's utility system

---

## Theme System Architecture

### The Three-Layer Theme System

**Layer 1: Theme Definition** (`src/styles/theme.scss`)
- Central source of truth for all colors, typography, spacing
- SCSS variables for build-time values
- CSS custom properties for runtime theming (dark mode)

**Layer 2: Quasar Integration** (`src/css/quasar.variables.scss`)
- Maps theme to Quasar's color system
- Overrides Quasar defaults with brand colors
- Enables utility classes to use custom colors

**Layer 3: Component Usage**
- Quasar utilities use theme automatically (`text-primary`, `bg-secondary`)
- Custom CSS uses theme variables/mixins for brand-specific styling
- JavaScript access via composables (`useTheme()`)

---

## CSS Custom Properties vs SCSS Variables

### CSS Custom Properties (Runtime)

**Use for:** Values that change at runtime (dark mode, user preferences)

```scss
/* In theme.scss - define custom properties */
:root {
  --color-text-primary: #391c11;
  --color-text-secondary: #6b4423;
  --color-prayer-text: #f0dab8;
}

body.body--dark {
  --color-text-primary: #f0dab8;
  --color-text-secondary: #d4c4b0;
  --color-prayer-text: #f0dab8;
}
```

```vue
<style scoped>
/* In components - use custom properties */
.prayer-text {
  color: var(--color-prayer-text);  /* Auto-switches in dark mode */
}
</style>
```

### SCSS Variables (Build-Time)

**Use for:** Static values that don't change at runtime

```scss
/* In theme.scss - define SCSS variables */
$color-brand-primary: #844628;
$color-brand-secondary: #e7c18a;
$color-brand-accent: #d5863a;

$spacing-4: 1rem;
$font-family-prayer: 'Crimson Text', serif;
```

```vue
<style scoped lang="scss">
@import '@/styles/theme.scss';

/* In components - use SCSS variables */
.custom-element {
  background-color: rgba($color-brand-primary, 0.05);
  padding: $spacing-4;
  font-family: $font-family-prayer;
}
</style>
```

---

## Quasar Color Integration

### Mapping Custom Colors to Quasar

**In `quasar.variables.scss`:**
```scss
@import '@/styles/theme.scss';

// Override Quasar's brand colors with your theme
$primary: $color-brand-primary;    // #844628
$secondary: $color-brand-secondary; // #e7c18a
$accent: $color-brand-accent;      // #d5863a

// Now Quasar utilities use your brand colors!
// class="text-primary" → #844628
// class="bg-secondary" → #e7c18a
```

### Using Theme Colors in Templates

**Via Quasar Utilities** (automatic):
```vue
<div class="text-primary bg-secondary">
  <!-- Uses #844628 text on #e7c18a background -->
</div>
```

**Via Custom CSS Properties** (manual):
```vue
<template>
  <div class="custom-prayer-text q-pa-md">Prayer</div>
</template>

<style scoped>
.custom-prayer-text {
  color: var(--color-prayer-text);  /* Custom color not in Quasar palette */
}
</style>
```

---

## When to Use Each Approach

### Decision Tree

```
Need to style something?
├─ Is it spacing, typography, or layout?
│  └─ YES → Use Quasar utilities (q-pa-md, text-h5, row)
│
├─ Is it a color in Quasar's palette (primary, secondary, grey-7)?
│  └─ YES → Use Quasar color utilities (text-primary, bg-grey-1)
│
├─ Is it a custom brand color from theme?
│  └─ YES → Use SCSS variable: rgba($color-brand-primary, 0.05)
│
├─ Does it need to change in dark mode?
│  └─ YES → Use CSS custom property: var(--color-prayer-text)
│
└─ Is it a unique design element (circular badge, special border)?
   └─ YES → Write minimal custom CSS with theme variables
```

---

## Theme Mixin Patterns

### Define Reusable Mixins

**In `theme.scss`:**
```scss
@mixin prayer-text-base {
  font-family: $font-family-prayer;
  color: var(--color-prayer-text);
  line-height: $line-height-relaxed;
  white-space: pre-wrap;
  word-wrap: break-word;
}

@mixin text-muted {
  color: var(--color-text-secondary);
  font-size: $font-size-sm;
}

@mixin bg-elevated {
  background-color: var(--color-surface-elevated);
  border-radius: $radius-md;
  box-shadow: $shadow-sm;
}
```

### Use Mixins in Components

```vue
<style scoped lang="scss">
@import '@/styles/theme.scss';

.prayer-content {
  @include prayer-text-base;  /* Applies all prayer text styles */
}

.description {
  @include text-muted;  /* Applies muted text pattern */
}

.card-surface {
  @include bg-elevated;  /* Applies elevated surface pattern */
}
</style>
```

---

## Complete Example: Hybrid Approach

```vue
<script setup>
/**
 * Exemplary component showing ideal utility + custom CSS balance
 * Pattern from: quasar-fp (80% utilities, 20% theme CSS)
 */
import { useUserPreferences } from '@/composables/useUserPreferences.js';

const userPrefs = useUserPreferences();
</script>

<template>
  <q-card flat bordered class="prayer-card rounded-borders q-mb-lg">
    <q-card-section>
      <!-- Header: 100% utilities -->
      <div class="row items-start q-mb-md">
        <div class="prayer-number row items-center justify-center">
          1
        </div>
        <div class="col">
          <h2 class="prayer-title text-h5 text-weight-bold text-primary q-mb-sm q-mt-none">
            Prayer Title
          </h2>
          <p class="text-caption text-italic text-accent q-mb-none">
            Scripture Reference
          </p>
        </div>
      </div>

      <!-- Content: utilities + custom prayer-text mixin -->
      <div class="prayer-content q-pa-md q-my-md rounded-borders">
        <pre class="prayer-text">Prayer text content</pre>
      </div>

      <!-- Toggle: 100% utilities -->
      <div class="q-pa-md rounded-borders">
        <q-toggle
          v-model="userPrefs.someOption"
          label="Enable Option"
          class="text-weight-medium q-mb-sm"
        />
        <p class="text-caption text-grey-7 q-pl-sm q-mb-none">
          Description of option
        </p>
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

  &:hover {
    border-color: rgba($color-brand-primary, 0.4);
    box-shadow: $shadow-md;
  }
}

.prayer-number {
  width: 48px;
  height: 48px;
  background-color: $color-brand-primary;
  color: white;
  border-radius: 50%;
  flex-shrink: 0;
}

.prayer-title {
  font-family: $font-family-prayer;  /* Custom font */
}

.prayer-content {
  background-color: rgba($color-brand-secondary, 0.1);
  border-left: 4px solid $color-brand-accent;
}

.prayer-text {
  @include prayer-text-base;  /* Reusable mixin */
}

/* Dark mode - theme colors only */
body.body--dark {
  .prayer-card {
    background-color: rgba($color-brand-primary, 0.15);
    border-color: rgba($color-brand-primary, 0.3);
  }

  .prayer-content {
    background-color: rgba($color-brand-secondary, 0.2);
  }
}
</style>
```

---

## JavaScript Theme Access

### Using useTheme Composable

```javascript
// Pattern from: quasar-fp (JavaScript theme access)
import { useTheme } from '@/composables/useTheme.js';

const { colors, getColor, getSpacing } = useTheme();

// Access theme values
const primaryColor = getColor('brand.primary');  // #844628
const spacing = getSpacing(4);  // 1rem

// Use in computed styles
const dynamicStyles = computed(() => ({
  color: getColor('prayer.text'),
  padding: getSpacing(4),
  backgroundColor: colors.brand.primary
}));
```

---

## Performance Best Practices

### Minimize Custom CSS

**Benefits of utility-first:**
- ✅ Smaller CSS bundles (no duplicate styles)
- ✅ Better tree-shaking (utilities purged if unused)
- ✅ Faster development (no CSS file switching)
- ✅ Consistent spacing/sizing (design system enforced)

**Measurements from Seven Sorrows refactor:**
- Custom CSS: 535 lines → 335 lines (37% reduction)
- Bundle size: ~12KB → ~8KB gzipped (33% smaller)
- Development time: Faster (no custom CSS writing)

### Scoped Styles Pattern

```vue
<style scoped lang="scss">
@import '@/styles/theme.scss';

/* Scoped styles prevent CSS bleed */
/* Only define theme-specific custom elements */

.custom-brand-element {
  background-color: rgba($color-brand-primary, 0.05);
  border-left: $border-width-thick solid $color-brand-accent;
}

/* Dark mode in same scope */
body.body--dark {
  .custom-brand-element {
    background-color: rgba($color-brand-primary, 0.15);
  }
}
</style>
```

---

## Common Mistakes & Solutions

### Mistake 1: Hardcoded Colors

❌ **Bad:**
```vue
<style>
.element {
  color: #844628;  /* Breaks if theme changes! */
}
</style>
```

✅ **Good:**
```vue
<!-- Use utility if Quasar color -->
<div class="text-primary">

<!-- Or use theme variable -->
<style lang="scss">
@import '@/styles/theme.scss';
.element {
  color: $color-brand-primary;
}
</style>
```

### Mistake 2: Magic Number Spacing

❌ **Bad:**
```vue
<style>
.element {
  padding: 17px;  /* Random number! */
  margin-bottom: 23px;
}
</style>
```

✅ **Good:**
```vue
<div class="q-pa-md q-mb-lg">  <!-- 16px, 24px from 8px grid -->
```

### Mistake 3: Bypassing Dark Mode

❌ **Bad:**
```vue
<style>
.element {
  background: #ffffff;  /* Broken in dark mode! */
}
</style>
```

✅ **Good:**
```vue
<!-- Utility handles dark mode automatically -->
<div class="bg-grey-1">

<!-- Or use custom property -->
<style>
.element {
  background-color: var(--color-surface-bg);  /* Auto-switches */
}
</style>
```

---

## CSS Architecture Summary

**Ideal Component CSS Structure:**

```vue
<template>
  <!-- 80% utilities, 20% custom classes -->
  <div class="custom-brand-box q-pa-md q-mb-lg rounded-borders">
    <h2 class="text-h5 text-weight-bold text-primary q-mb-sm q-mt-none">
      Title
    </h2>
    <p class="text-caption text-grey-7 q-mb-none">
      Content
    </p>
  </div>
</template>

<style scoped lang="scss">
@import '@/styles/theme.scss';

/* Minimal custom CSS (~20% of total styling) */
/* ONLY for: brand colors, unique design elements, custom fonts */

.custom-brand-box {
  background-color: rgba($color-brand-secondary, 0.08);
  border-left: $border-width-thick solid $color-brand-primary;
}

body.body--dark {
  .custom-brand-box {
    background-color: rgba($color-brand-secondary, 0.15);
  }
}
</style>
```

**What Goes Where:**
- **Utilities**: spacing, typography, layout, standard colors → `class="..."`
- **SCSS Variables**: brand colors, custom fonts → `@import + $color-brand-*`
- **CSS Properties**: runtime theme values (dark mode) → `var(--color-*)`
- **Mixins**: reusable patterns → `@include prayer-text-base`

---

**Reference Examples:**
- SevenSorrowsChapletOptions.vue - Settings panel pattern
- SorrowSection.vue - Complex component pattern
- SevenSorrowsChaplet.vue - Page layout pattern
