# Quasar Component Patterns - Best Practices

**Purpose**: Guide for using Quasar components effectively with Vue 3 Composition API

---

## Component Philosophy

**Use Quasar components instead of HTML** for:
- Better accessibility (built-in ARIA)
- Consistent UX (Material Design)
- Theme integration (auto-respects brand colors)
- Mobile optimization (touch-friendly, responsive)
- Less code (handles edge cases automatically)

---

## Essential Components

### Buttons (QBtn)

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
- `icon` / `icon-right` - Icons
- `color` - primary|secondary|accent|positive|negative
- `flat` - No background
- `outline` - Outlined style
- `rounded` - Rounded corners
- `loading` / `disable` - States

---

### Forms (QInput, QSelect, QToggle)

**QInput:**
```vue
<q-input
  v-model="name"
  label="Enter name"
  outlined
  :rules="[val => !!val || 'Required']"
/>
```

**QSelect:**
```vue
<q-select
  v-model="selected"
  :options="options"
  label="Choose option"
  outlined
/>
```

**QToggle:**
```vue
<q-toggle
  v-model="enabled"
  label="Enable Feature"
  color="primary"
/>
```

---

### Cards (QCard)

```vue
<q-card flat bordered class="q-mb-md">
  <q-card-section class="text-h6">Title</q-card-section>
  <q-card-section>Content</q-card-section>
  <q-card-actions align="right">
    <q-btn label="Action" color="primary" />
  </q-card-actions>
</q-card>
```

---

### Expansion Items (QExpansionItem)

```vue
<q-expansion-item
  default-opened
  icon="settings"
  label="Settings Section"
  header-class="text-weight-bold"
>
  <q-card flat class="q-pa-md">
    <!-- Content -->
  </q-card>
</q-expansion-item>
```

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
      <q-item-label caption>Description</q-item-label>
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
      Dialog content
    </q-card-section>
    <q-card-actions align="right">
      <q-btn flat label="Cancel" v-close-popup />
      <q-btn label="OK" color="primary" v-close-popup />
    </q-card-actions>
  </q-card>
</q-dialog>
```

---

## Complex Patterns

### Settings Panel

```vue
<template>
  <q-expansion-item
    default-opened
    icon="settings"
    label="Display Settings"
    header-class="text-weight-bold"
  >
    <div class="q-pa-md">
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
    </div>
  </q-expansion-item>
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
    Description
  </p>
</div>
```

---

## Dark Mode Pattern

```vue
<script setup>
import { useQuasar } from 'quasar';
import { computed } from 'vue';

const $q = useQuasar();
const isDark = computed(() => $q.dark.isActive);
const toggleDark = () => $q.dark.toggle();
</script>

<template>
  <!-- Quasar utilities auto-handle dark mode -->
  <div class="text-primary bg-secondary q-pa-md">
    Automatically switches colors in dark mode
  </div>
</template>
```

---

## Responsive Grid

```vue
<div class="row q-col-gutter-md">
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
- `col-lg` - 1440px+ (large desktop)

---

## Quick Component Reference

| Need | Use Component | Not HTML |
|------|---------------|----------|
| Button | `<q-btn>` | `<button>` |
| Text input | `<q-input>` | `<input>` |
| Dropdown | `<q-select>` | `<select>` |
| Toggle | `<q-toggle>` | Custom toggle |
| Checkbox | `<q-checkbox>` | `<input type="checkbox">` |
| Card | `<q-card>` | `<div class="card">` |
| Modal | `<q-dialog>` | Custom modal |
| Tabs | `<q-tabs>` | Custom tabs |
| Table | `<q-table>` | `<table>` |
| Loading | `<q-spinner>` | Custom spinner |

---

**Reference**: https://quasar.dev/vue-components
