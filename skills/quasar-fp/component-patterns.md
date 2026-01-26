# Quasar Component Patterns - Best Practices

**Purpose**: Guide for using Quasar components effectively with Vue 3 Composition API

---

## Component Philosophy

**Use Quasar components instead of HTML** for:
- ✅ Better accessibility (built-in ARIA)
- ✅ Consistent UX (Material Design)
- ✅ Theme integration (auto-respects brand colors)
- ✅ Mobile optimization (touch-friendly, responsive)
- ✅ Less code (handles edge cases automatically)

---

## Essential Components

### Buttons (QBtn)

**Replace HTML buttons with QBtn:**

❌ **Bad:**
```vue
<button @click="handleClick" class="my-button">
  <i class="icon">✓</i>
  Click Me
</button>
```

✅ **Good:**
```vue
<q-btn
  @click="handleClick"
  label="Click Me"
  icon="check"
  color="primary"
/>
```

**Common Props:**
- `label` - Button text
- `icon` - Left icon
- `icon-right` - Right icon
- `color` - primary|secondary|accent|positive|negative
- `flat` - No background
- `outline` - Outlined style
- `rounded` - Rounded corners
- `fab` - Floating action button
- `loading` - Show loading spinner
- `disable` - Disable button

**Typical Patterns:**
```vue
<!-- Primary action button -->
<q-btn label="Save" color="primary" icon="save" />

<!-- Secondary action -->
<q-btn label="Cancel" flat />

<!-- Icon-only button -->
<q-btn icon="settings" flat round dense />

<!-- Loading state -->
<q-btn label="Submit" color="primary" :loading="isSubmitting" />
```

---

### Forms (QInput, QSelect, QToggle)

**QInput - Text Input:**

❌ **Bad:**
```vue
<input v-model="name" placeholder="Enter name" type="text" />
```

✅ **Good:**
```vue
<q-input
  v-model="name"
  label="Enter name"
  outlined
/>
```

**Common Props:**
- `outlined` - Outlined style (recommended)
- `filled` - Filled background style
- `standout` - Standout style
- `label` - Floating label
- `hint` - Helper text below
- `error` - Show error state
- `error-message` - Error text
- `rules` - Validation rules array

**Typical Patterns:**
```vue
<!-- Basic text input -->
<q-input
  v-model="text"
  label="Name"
  outlined
  class="q-mb-md"
/>

<!-- With validation -->
<q-input
  v-model="email"
  label="Email"
  type="email"
  outlined
  :rules="[val => !!val || 'Required', val => /@/.test(val) || 'Invalid email']"
  class="q-mb-md"
/>

<!-- With hint -->
<q-input
  v-model="password"
  label="Password"
  type="password"
  outlined
  hint="At least 8 characters"
  class="q-mb-md"
/>
```

**QSelect - Dropdown:**

```vue
<q-select
  v-model="selected"
  :options="options"
  label="Choose option"
  outlined
  class="q-mb-md"
/>
```

**QToggle - Toggle Switch:**

```vue
<q-toggle
  v-model="enabled"
  label="Enable Feature"
  color="primary"
  class="text-weight-medium"
/>
```

---

### Cards (QCard)

❌ **Bad:**
```vue
<div class="card">
  <div class="card-header">Title</div>
  <div class="card-body">Content</div>
  <div class="card-footer">
    <button>Action</button>
  </div>
</div>
```

✅ **Good:**
```vue
<q-card flat bordered class="q-mb-md">
  <q-card-section class="text-h6">
    Title
  </q-card-section>
  <q-card-section>
    Content
  </q-card-section>
  <q-card-actions align="right">
    <q-btn label="Action" color="primary" />
  </q-card-actions>
</q-card>
```

**Common Props:**
- `flat` - No shadow
- `bordered` - Add border
- `square` - No border radius

**Typical Patterns:**
```vue
<!-- Simple card -->
<q-card class="q-pa-md q-mb-md">
  <div class="text-h6 q-mb-sm">Card Title</div>
  <p class="text-body2 q-mb-none">Card content</p>
</q-card>

<!-- Interactive card with actions -->
<q-card flat bordered>
  <q-card-section>
    <div class="text-h6">Title</div>
    <div class="text-caption text-grey-7">Subtitle</div>
  </q-card-section>
  <q-separator />
  <q-card-actions align="right">
    <q-btn flat label="Cancel" />
    <q-btn label="Save" color="primary" />
  </q-card-actions>
</q-card>
```

---

### Expansion Items (QExpansionItem)

**Collapsible sections:**

```vue
<q-expansion-item
  default-opened
  icon="settings"
  label="Settings Section"
  header-class="text-weight-bold"
>
  <q-card flat class="q-pa-md">
    <!-- Content inside expansion -->
  </q-card>
</q-expansion-item>
```

**Common Props:**
- `default-opened` - Start expanded
- `icon` - Left icon
- `expand-icon` - Custom expand icon
- `header-class` - CSS class for header
- `v-model` - Control expanded state

---

### Lists (QList, QItem)

```vue
<q-list bordered class="rounded-borders">
  <q-item clickable @click="handleClick">
    <q-item-section avatar>
      <q-icon name="settings" />
    </q-item-section>
    <q-item-section>
      <q-item-label>Setting Name</q-item-label>
      <q-item-label caption>Setting description</q-item-label>
    </q-item-section>
    <q-item-section side>
      <q-toggle v-model="value" />
    </q-item-section>
  </q-item>
</q-list>
```

---

### Dialogs (QDialog)

```vue
<q-dialog v-model="dialogOpen">
  <q-card style="min-width: 350px">
    <q-card-section>
      <div class="text-h6">Dialog Title</div>
    </q-card-section>

    <q-card-section class="q-pt-none">
      Dialog content goes here
    </q-card-section>

    <q-card-actions align="right">
      <q-btn flat label="Cancel" v-close-popup />
      <q-btn label="OK" color="primary" v-close-popup />
    </q-card-actions>
  </q-card>
</q-dialog>
```

---

### Separators (QSeparator)

```vue
<q-separator class="q-my-md" />
<q-separator spaced />  <!-- Adds margin automatically -->
<q-separator inset />   <!-- Inset separator -->
```

---

### Icons (QIcon)

```vue
<q-icon name="settings" size="24px" />
<q-icon name="mdi-home" color="primary" />

<!-- Material Icons -->
<q-icon name="check" />

<!-- Material Design Icons (mdi-*) -->
<q-icon name="mdi-account" />

<!-- Custom SVG -->
<q-icon name="img:/path/to/icon.svg" />
```

---

## Complex Patterns

### Settings Panel with Expansion Items

```vue
<template>
  <div>
    <q-expansion-item
      default-opened
      icon="settings"
      label="Display Settings"
      header-class="text-weight-bold"
    >
      <div class="q-pa-md">
        <!-- Individual setting -->
        <div class="q-pa-md q-mb-md rounded-borders bg-grey-1">
          <q-toggle
            v-model="setting1"
            label="Show Feature"
            class="text-weight-medium q-mb-sm"
          />
          <p class="text-caption text-grey-7 q-pl-sm q-mb-none">
            Feature description
          </p>
        </div>

        <!-- Another setting -->
        <div class="q-pa-md rounded-borders bg-grey-1">
          <q-select
            v-model="style"
            :options="styleOptions"
            label="Style"
            outlined
          />
        </div>
      </div>
    </q-expansion-item>
  </div>
</template>
```

### Responsive Header

```vue
<div class="text-center q-py-lg q-mb-lg">
  <h1 class="text-h3 text-weight-bold text-primary q-mb-sm q-mt-none">
    Page Title
  </h1>
  <p class="text-h6 text-italic text-accent q-mb-sm q-mt-none">
    Subtitle
  </p>
  <p class="text-caption text-grey-7 q-mx-auto q-mb-none" style="max-width: 600px">
    Description text that wraps nicely
  </p>
</div>
```

### Conditional Rendering with Utilities

```vue
<template>
  <!-- Show different content based on state -->
  <div v-if="loading" class="text-center q-pa-xl">
    <q-spinner size="50px" color="primary" />
    <p class="text-body2 text-grey-7 q-mt-md">Loading...</p>
  </div>

  <div v-else-if="error" class="text-center q-pa-xl">
    <q-icon name="error" size="50px" color="negative" />
    <p class="text-body2 text-negative q-mt-md">{{ error }}</p>
  </div>

  <div v-else>
    <!-- Actual content -->
  </div>
</template>
```

---

## Component + Utility Combinations

### Sectioned Content

```vue
<div class="q-mb-xl">
  <h2 class="text-h5 text-weight-bold text-primary q-mb-md q-pb-sm section-border">
    Section Title
  </h2>

  <div class="row q-col-gutter-md">
    <div class="col-12 col-md-6">
      <q-card flat bordered class="q-pa-md">
        Left content
      </q-card>
    </div>
    <div class="col-12 col-md-6">
      <q-card flat bordered class="q-pa-md">
        Right content
      </q-card>
    </div>
  </div>
</div>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.section-border {
  border-bottom: 1px solid rgba($color-brand-primary, 0.2);
}
</style>
```

### Form with Validation

```vue
<q-form @submit="onSubmit" class="q-gutter-md">
  <q-input
    v-model="name"
    label="Name *"
    outlined
    :rules="[val => !!val || 'Required']"
  />

  <q-input
    v-model="email"
    label="Email *"
    type="email"
    outlined
    :rules="[
      val => !!val || 'Required',
      val => /@/.test(val) || 'Invalid email'
    ]"
  />

  <div class="row justify-end q-gutter-sm">
    <q-btn label="Cancel" flat />
    <q-btn label="Submit" type="submit" color="primary" />
  </div>
</q-form>
```

---

## Performance Patterns

### Lazy Loading Components

```javascript
// Pattern from: quasar-fp (code splitting)
const MyHeavyComponent = defineAsyncComponent(() =>
  import('@/components/MyHeavyComponent.vue')
);
```

### V-Show vs V-If

```vue
<!-- Use v-show for frequently toggled content -->
<div v-show="isVisible" class="q-pa-md">
  Frequently toggled content
</div>

<!-- Use v-if for conditionally loaded content -->
<div v-if="condition" class="q-pa-md">
  Rarely shown content
</div>
```

---

## Accessibility Patterns

### Semantic Structure

```vue
<!-- Use semantic HTML with Quasar components -->
<header>
  <q-toolbar>
    <q-btn icon="menu" flat round aria-label="Menu" />
    <q-toolbar-title>Site Title</q-toolbar-title>
  </q-toolbar>
</header>

<main>
  <q-page class="q-pa-md">
    <h1 class="text-h3">Page Title</h1>
    <!-- Content -->
  </q-page>
</main>

<footer class="text-center q-pa-md">
  <p class="text-caption">© 2024</p>
</footer>
```

### ARIA Labels

```vue
<q-btn
  icon="settings"
  flat
  round
  aria-label="Open settings"
  @click="openSettings"
/>

<q-input
  v-model="search"
  label="Search"
  aria-label="Search input"
/>
```

---

## Dark Mode Patterns

### Auto-Detect Dark Mode

```vue
<script setup>
import { useQuasar } from 'quasar';

const $q = useQuasar();

// Access dark mode state
const isDark = computed(() => $q.dark.isActive);

// Toggle dark mode
const toggleDark = () => $q.dark.toggle();
</script>

<template>
  <!-- Quasar utilities auto-handle dark mode -->
  <div class="text-primary bg-secondary q-pa-md">
    Automatically switches colors in dark mode
  </div>

  <!-- Manual dark mode handling if needed -->
  <div :class="isDark ? 'bg-grey-9' : 'bg-grey-1'" class="q-pa-md">
    Custom dark mode handling
  </div>
</template>
```

---

## Responsive Patterns

### Grid System

```vue
<div class="row q-col-gutter-md">
  <!-- Full width on mobile, half on tablet, third on desktop -->
  <div class="col-12 col-sm-6 col-md-4">
    <q-card>Content 1</q-card>
  </div>
  <div class="col-12 col-sm-6 col-md-4">
    <q-card>Content 2</q-card>
  </div>
  <div class="col-12 col-sm-6 col-md-4">
    <q-card>Content 3</q-card>
  </div>
</div>
```

**Breakpoints:**
- `col-xs` - < 600px (mobile)
- `col-sm` - 600px - 1023px (tablet)
- `col-md` - 1024px - 1439px (desktop)
- `col-lg` - 1440px - 1919px (large desktop)
- `col-xl` - ≥ 1920px (XL desktop)

### Responsive Utilities

```vue
<!-- Hide on mobile -->
<div class="gt-xs">Desktop only</div>

<!-- Hide on desktop -->
<div class="lt-md">Mobile/tablet only</div>

<!-- Responsive spacing -->
<div class="q-pa-sm q-pa-md-md q-pa-lg-lg">
  Responsive padding: small on mobile, medium on tablet, large on desktop
</div>
```

---

## Real-World Example: Settings Panel

```vue
<script setup>
import { useUserPreferences } from '@/composables/useUserPreferences.js';

const userPrefs = useUserPreferences();
</script>

<template>
  <div>
    <q-expansion-item
      default-opened
      icon="settings"
      label="Display Settings"
      header-class="text-weight-bold"
      class="rounded-borders"
    >
      <div class="q-pa-md">
        <!-- Toggle option with description -->
        <div class="q-pa-md q-mb-md rounded-borders bg-grey-1">
          <q-toggle
            v-model="userPrefs.showFeature"
            label="Show Feature"
            color="primary"
            class="text-weight-medium q-mb-sm"
          />
          <p class="text-caption text-grey-7 q-pl-sm q-mb-none">
            Enable this to show the feature throughout the app
          </p>
        </div>

        <!-- Select option -->
        <div class="q-pa-md rounded-borders bg-grey-1">
          <q-select
            v-model="userPrefs.style"
            :options="['Modern', 'Classic', 'Minimal']"
            label="Visual Style"
            outlined
            class="q-mb-sm"
          />
          <p class="text-caption text-grey-7 q-mb-none">
            Choose your preferred visual style
          </p>
        </div>
      </div>
    </q-expansion-item>
  </div>
</template>

<style scoped lang="scss">
@import '@/styles/theme.scss';

/* ONLY custom theme colors - everything else uses utilities */
.bg-grey-1 {
  border-left: $border-width-thick solid $color-brand-primary;
}

body.body--dark {
  .bg-grey-1 {
    background-color: rgba($color-brand-secondary, 0.15);
  }
}
</style>
```

---

## Quick Component Reference

| Need | Use Component | Not HTML |
|------|---------------|----------|
| Button | `<q-btn>` | `<button>` |
| Text input | `<q-input>` | `<input>` |
| Dropdown | `<q-select>` | `<select>` |
| Toggle | `<q-toggle>` | Custom toggle |
| Checkbox | `<q-checkbox>` | `<input type="checkbox">` |
| Radio | `<q-radio>` | `<input type="radio">` |
| Card | `<q-card>` | `<div class="card">` |
| Modal | `<q-dialog>` | Custom modal |
| Tabs | `<q-tabs>` | Custom tabs |
| Drawer | `<q-drawer>` | Custom sidebar |
| Toolbar | `<q-toolbar>` | `<header>` with custom CSS |
| Table | `<q-table>` | `<table>` |
| Pagination | `<q-pagination>` | Custom pagination |
| Loading | `<q-spinner>` | Custom spinner |

---

**Reference**: https://quasar.dev/vue-components
