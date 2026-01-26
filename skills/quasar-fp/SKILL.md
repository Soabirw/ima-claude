---
name: "quasar-fp"
description: "Quasar Framework best practices with utility-first CSS and FP patterns - references js-fp-vue core"
---

# Quasar Framework - Functional Patterns & Utility-First Approach

## Core Principles

**Primary Directive**: "Utilities > custom CSS | Components > HTML | Theme system > inline styles"

### Anti-Over-Engineering for Quasar
- **DON'T write custom CSS** for spacing, typography, colors, layout (use utilities)
- **DON'T reinvent components** that Quasar provides (QBtn, QCard, QDialog, etc.)
- **DON'T bypass theme system** with hardcoded colors or magic numbers
- **DO use utilities first**, custom CSS only for theme-specific brand elements
- **DO leverage Quasar components** for consistent UX and accessibility
- **DO integrate with theme system** via CSS custom properties and SCSS variables

---

## Detection Algorithm

### Auto-Activation Triggers

**File-Based Detection** (Confidence: 95%):
```javascript
// Trigger on .vue files
file.endsWith('.vue')

// Trigger on quasar.config.js presence
fs.existsSync('quasar.config.js')

// Trigger on Quasar imports
/import\s+{[^}]*}\s+from\s+['"]quasar['"]/
```

**Content-Based Detection** (Confidence: 90%):
```javascript
// Quasar components in template
/<q-[a-z-]+/gi

// Quasar utility classes
/class="[^"]*q-(pa|ma|pt|mt|mb|ml|mr|mx|my|px|py)-[a-z]{2,}/

// Quasar specific patterns
/useQuasar|QBtn|QCard|QDialog|QExpansionItem/
```

**Context-Based Detection** (Confidence: 85%):
```javascript
// Vue 3 + component creation keywords
keywords: ['create component', 'build UI', 'add form', 'settings panel']
&& framework: 'vue'
&& quasar_detected: true
```

### Context7 Integration Triggers

**Load Quasar docs when:**
- User asks about Quasar-specific features
- Creating new Quasar component types (QTable, QUploader, etc.)
- Configuration questions (quasar.config.js, plugins, boot files)
- Theme or styling questions specific to Quasar

**Example Context7 Query:**
```javascript
// When user asks: "How do I use QTable with server-side pagination?"
resolveLibraryId({ libraryName: 'quasar', query: 'QTable server-side pagination' })
→ getLibraryDocs({ libraryId: '/quasarframework/quasar', query: 'QTable pagination' })
```

---

## Utility-First Patterns

### ✅ GOOD: Utility-First Approach

```vue
<template>
  <!-- Spacing, layout, typography via utilities -->
  <div class="q-pa-md q-mb-lg rounded-borders">
    <h2 class="text-h5 text-weight-bold text-primary q-mb-sm q-mt-none">
      Title
    </h2>
    <p class="text-caption text-grey-7 q-mb-none">
      Description text
    </p>

    <!-- Quasar components for interactive elements -->
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

### ❌ BAD: Hand-Written CSS for Standard Properties

```vue
<template>
  <div class="my-container">
    <h2 class="my-title">Title</h2>
    <p class="my-text">Description</p>
  </div>
</template>

<style scoped>
/* DON'T DO THIS - utilities exist for all of these! */
.my-container {
  padding: 16px;              /* Use q-pa-md */
  margin-bottom: 24px;        /* Use q-mb-lg */
  border-radius: 8px;         /* Use rounded-borders */
}

.my-title {
  font-size: 1.5rem;          /* Use text-h5 */
  font-weight: 700;           /* Use text-weight-bold */
  color: #1976D2;             /* Use text-primary */
  margin-bottom: 8px;         /* Use q-mb-sm */
}

.my-text {
  font-size: 0.875rem;        /* Use text-caption */
  color: #6b7280;             /* Use text-grey-7 */
}
</style>
```

---

## Utility Class Reference

### Spacing (Bootstrap-style)

**Pattern**: `q-{property}{side}-{size}`

**Properties:**
- `p` = padding
- `m` = margin

**Sides:**
- `a` = all
- `t` = top
- `r` = right
- `b` = bottom
- `l` = left
- `x` = left + right
- `y` = top + bottom

**Sizes:**
- `xs` = 4px
- `sm` = 8px
- `md` = 16px
- `lg` = 24px
- `xl` = 48px

**Examples:**
```vue
<div class="q-pa-md">      <!-- padding: 16px all sides -->
<div class="q-mb-lg">      <!-- margin-bottom: 24px -->
<div class="q-px-sm">      <!-- padding-left/right: 8px -->
<div class="q-my-xl">      <!-- margin-top/bottom: 48px -->
```

### Typography

**Headings:**
```vue
<h1 class="text-h1">  <!-- 6rem, 300 weight -->
<h2 class="text-h2">  <!-- 3.75rem, 300 weight -->
<h3 class="text-h3">  <!-- 3rem, 400 weight -->
<h4 class="text-h4">  <!-- 2.125rem, 400 weight -->
<h5 class="text-h5">  <!-- 1.5rem, 400 weight -->
<h6 class="text-h6">  <!-- 1.25rem, 500 weight -->
```

**Body Text:**
```vue
<p class="text-body1">     <!-- 1rem, 400 weight -->
<p class="text-body2">     <!-- 0.875rem, 400 weight -->
<p class="text-caption">   <!-- 0.75rem, 400 weight -->
<p class="text-overline">  <!-- 0.75rem, uppercase -->
```

**Text Weight:**
```vue
<span class="text-weight-thin">      <!-- 100 -->
<span class="text-weight-light">     <!-- 300 -->
<span class="text-weight-regular">   <!-- 400 -->
<span class="text-weight-medium">    <!-- 500 -->
<span class="text-weight-bold">      <!-- 700 -->
<span class="text-weight-bolder">    <!-- 900 -->
```

**Text Style:**
```vue
<span class="text-italic">
<span class="text-uppercase">
<span class="text-lowercase">
<span class="text-capitalize">
```

### Colors

**Brand Colors** (from theme integration):
```vue
<div class="text-primary">    <!-- #844628 - rich wood -->
<div class="text-secondary">  <!-- #e7c18a - light wood -->
<div class="text-accent">     <!-- #d5863a - warm amber -->

<div class="bg-primary">
<div class="bg-secondary">
<div class="bg-accent">
```

**Semantic Colors:**
```vue
<div class="text-positive">   <!-- Success/green -->
<div class="text-negative">   <!-- Error/red -->
<div class="text-warning">    <!-- Warning/yellow -->
<div class="text-info">       <!-- Info/blue -->
```

**Greyscale:**
```vue
<div class="text-grey-1">     <!-- Lightest -->
<div class="text-grey-5">     <!-- Medium -->
<div class="text-grey-9">     <!-- Darkest -->
```

### Layout (Flexbox)

**Flex Containers:**
```vue
<div class="row">              <!-- display: flex -->
<div class="column">           <!-- display: flex; flex-direction: column -->
<div class="row inline">       <!-- display: inline-flex -->
```

**Alignment:**
```vue
<div class="row items-start">        <!-- align-items: flex-start -->
<div class="row items-center">       <!-- align-items: center -->
<div class="row items-end">          <!-- align-items: flex-end -->
<div class="row items-stretch">      <!-- align-items: stretch -->

<div class="row justify-start">      <!-- justify-content: flex-start -->
<div class="row justify-center">     <!-- justify-content: center -->
<div class="row justify-end">        <!-- justify-content: flex-end -->
<div class="row justify-between">    <!-- justify-content: space-between -->
<div class="row justify-around">     <!-- justify-content: space-around -->
```

**Flex Items:**
```vue
<div class="col">              <!-- flex: 1 -->
<div class="col-auto">         <!-- flex: 0 0 auto -->
<div class="col-grow">         <!-- flex-grow: 1 -->
<div class="col-shrink">       <!-- flex-shrink: 1 -->
```

### Borders & Rounding

```vue
<div class="rounded-borders">  <!-- border-radius: 4px -->
<div class="no-border">
<div class="no-border-radius">
```

### Display

```vue
<div class="block">
<div class="inline">
<div class="inline-block">
<div class="hidden">           <!-- display: none -->
```

---

## Component Best Practices

### Use Quasar Components, Not HTML

❌ **Bad:**
```vue
<button @click="doSomething">Click Me</button>
<input v-model="text" placeholder="Enter text">
<div class="card">...</div>
```

✅ **Good:**
```vue
<q-btn @click="doSomething" label="Click Me" color="primary" />
<q-input v-model="text" label="Enter text" />
<q-card>...</q-card>
```

### Quasar Component Advantages
- **Accessibility**: Built-in ARIA labels, keyboard navigation
- **Theming**: Automatic theme color integration
- **Responsive**: Mobile-optimized out of the box
- **Consistency**: Material Design principles enforced

---

## Theme Integration Patterns

### Using Theme Colors in Templates

**Via Quasar Utilities:**
```vue
<div class="text-primary bg-secondary">
  <!-- Automatically uses theme colors from quasar.variables.scss -->
</div>
```

**Via CSS Custom Properties:**
```vue
<template>
  <div class="custom-element q-pa-md">Prayer text</div>
</template>

<style scoped>
.custom-element {
  /* Use CSS custom properties for theme-specific colors */
  color: var(--color-prayer-text);
  background-color: var(--color-page-bg);
}
</style>
```

**Via SCSS Variables:**
```vue
<style scoped lang="scss">
@import '@/styles/theme.scss';

.custom-element {
  /* Use SCSS variables for brand colors */
  background-color: rgba($color-brand-primary, 0.05);
  border-left: $border-width-thick solid $color-brand-accent;
}
</style>
```

---

## Common Anti-Patterns & Fixes

### Anti-Pattern 1: Hand-Written Spacing

❌ **Bad:**
```vue
<style>
.container { padding: 16px; margin-bottom: 24px; }
</style>
```

✅ **Good:**
```vue
<div class="q-pa-md q-mb-lg">
```

### Anti-Pattern 2: Custom Typography CSS

❌ **Bad:**
```vue
<style>
.title { font-size: 1.5rem; font-weight: 700; color: #1976D2; }
</style>
```

✅ **Good:**
```vue
<h2 class="text-h5 text-weight-bold text-primary">
```

### Anti-Pattern 3: Manual Flexbox

❌ **Bad:**
```vue
<style>
.header { display: flex; align-items: center; justify-content: space-between; }
</style>
```

✅ **Good:**
```vue
<div class="row items-center justify-between">
```

### Anti-Pattern 4: Reinventing Quasar Components

❌ **Bad:**
```vue
<div class="custom-card">
  <div class="card-header">Title</div>
  <div class="card-body">Content</div>
</div>
```

✅ **Good:**
```vue
<q-card>
  <q-card-section class="text-h6">Title</q-card-section>
  <q-card-section>Content</q-card-section>
</q-card>
```

---

## When to Use Custom CSS

### ✅ Appropriate Custom CSS Use Cases

**1. Theme-Specific Brand Colors:**
```scss
.prayer-card {
  background-color: rgba($color-brand-primary, 0.05);
  border-left: $border-width-thick solid $color-brand-accent;
}
```

**2. Unique Design Elements:**
```scss
.circular-badge {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: $color-brand-primary;
}
```

**3. Custom Font Families:**
```scss
.prayer-title {
  font-family: $font-family-prayer;  // Custom spiritual font
}
```

**4. Complex Hover/Transition Effects:**
```scss
.prayer-card {
  transition: $transition-base;

  &:hover {
    border-color: rgba($color-brand-primary, 0.4);
    box-shadow: $shadow-md;
  }
}
```

**5. Dark Mode Theme Overrides:**
```scss
body.body--dark {
  .prayer-card {
    background-color: rgba($color-brand-primary, 0.15);
  }
}
```

---

## Quasar + Vue 3 FP Patterns

### Composable Integration

```javascript
// Pattern from: quasar-fp (utility-first with composables)
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

### Settings Panel Pattern

```vue
<script setup>
// Pattern from: quasar-fp (utility-first settings)
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
      <!-- Individual option -->
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

### Page Layout Pattern

```vue
<template>
  <!-- Pattern from: quasar-fp (utility-first page layout) -->
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

/* Custom CSS only for theme-specific borders/colors */
.page-header {
  border-bottom: 2px solid rgba($color-brand-primary, 0.3);
}

.custom-title {
  font-family: $font-family-prayer;  // Custom font
}
</style>
```

---

## Component Library Quick Reference

### Layout Components
- `<q-page>` - Page container
- `<q-card>` - Card container
- `<q-list>` - List container
- `<q-item>` - List item
- `<q-separator>` - Divider line

### Form Components
- `<q-btn>` - Button
- `<q-input>` - Text input
- `<q-select>` - Dropdown select
- `<q-toggle>` - Toggle switch
- `<q-checkbox>` - Checkbox
- `<q-radio>` - Radio button

### Interactive Components
- `<q-dialog>` - Modal dialog
- `<q-expansion-item>` - Collapsible section
- `<q-tab>` / `<q-tabs>` - Tabs
- `<q-drawer>` - Side drawer
- `<q-menu>` - Dropdown menu

### Display Components
- `<q-icon>` - Icon
- `<q-avatar>` - Avatar/circular image
- `<q-badge>` - Badge/label
- `<q-chip>` - Chip/tag
- `<q-banner>` - Banner message

---

## Context7 Integration Examples

### Example 1: Component Usage Question

**User asks:** "How do I use QTable with sorting?"

**AI Response:**
```javascript
// 1. Detect Quasar context → Load quasar-fp skill
// 2. Detect specific component question → Query Context7

resolveLibraryId({
  libraryName: 'quasar',
  query: 'QTable sorting functionality'
});

getLibraryDocs({
  libraryId: '/quasarframework/quasar/v2',
  query: 'QTable sorting columns props'
});

// 3. Provide official documentation + utility-first example
```

### Example 2: Styling Question

**User asks:** "How do I style this Quasar component?"

**AI Response:**
```javascript
// 1. Load quasar-fp skill
// 2. Check if utilities can solve it
// 3. If custom styling needed, query Context7 for best practices

getLibraryDocs({
  libraryId: '/quasarframework/quasar/v2',
  query: 'component styling customization CSS'
});

// 4. Suggest utility-first approach with minimal custom CSS
```

---

## Detection Implementation

### Auto-Load Logic

```javascript
/**
 * Quasar skill auto-detection algorithm
 * Pattern from: ORCHESTRATOR.md (intelligent routing)
 */
function shouldLoadQuasarSkill(context) {
  const { files, imports, keywords, route } = context;

  // High confidence triggers (95%+)
  if (files.some(f => f.endsWith('.vue')) &&
      fs.existsSync('quasar.config.js')) {
    return { load: true, confidence: 0.95 };
  }

  // Medium confidence triggers (80%+)
  if (imports.some(i => i.includes('quasar')) ||
      content.match(/<q-[a-z-]+/gi)) {
    return { load: true, confidence: 0.85 };
  }

  // Low confidence triggers (70%+)
  if (keywords.some(k => ['component', 'UI', 'form'].includes(k)) &&
      framework === 'vue') {
    return { load: true, confidence: 0.70 };
  }

  return { load: false, confidence: 0 };
}
```

### Context7 Query Builder

```javascript
/**
 * Build Context7 query for Quasar documentation
 * Pattern from: MCP_Context7.md (documentation lookup)
 */
function buildQuasarContext7Query(userQuery) {
  // Extract component name
  const componentMatch = userQuery.match(/Q[A-Z][a-zA-Z]+/);
  const component = componentMatch ? componentMatch[0] : null;

  // Extract feature/topic
  const topics = ['styling', 'props', 'events', 'slots', 'configuration'];
  const topic = topics.find(t => userQuery.toLowerCase().includes(t));

  // Build focused query
  return {
    libraryId: '/quasarframework/quasar/v2',
    query: component
      ? `${component} ${topic || 'usage examples'}`
      : `Quasar ${userQuery}`
  };
}
```

---

## Progressive Skill Loading

### Level 1: Metadata Scan (Always)
- Skill name, version, purpose
- Auto-detection triggers
- Quick reference patterns

### Level 2: Core Patterns (On Detection)
- Utility class reference
- Common anti-patterns
- Component guidelines

### Level 3: Deep Dive (On Demand)
- Load `utility-classes.md` - Complete utility reference
- Load `component-patterns.md` - All Quasar components
- Load `theme-integration.md` - Advanced theming
- Query Context7 - Official docs for specific questions

---

## Success Metrics

**Skill effectiveness measured by:**
- ✅ % of new components using utilities vs custom CSS (target: 80%+)
- ✅ CSS line count reduction (target: 30-50%)
- ✅ Quasar component usage vs HTML reimplementation (target: 90%+)
- ✅ Theme system integration (CSS vars vs hardcoded values) (target: 100%)
- ✅ Accessibility compliance (Quasar components have built-in a11y)

---

## Reference Examples

**Exemplary Components** (from Seven Sorrows Chaplet):
- `src/components/chaplet/SevenSorrowsChapletOptions.vue` - Settings panel pattern
- `src/components/chaplet/SorrowSection.vue` - Complex component with conditionals
- `src/pages/chaplets/SevenSorrowsChaplet.vue` - Page layout pattern

**Study these for:**
- Utility-first approach (80% utilities, 20% custom CSS)
- Theme integration (CSS vars, SCSS variables, mixins)
- Quasar component usage (QCard, QExpansionItem, QToggle)
- Responsive design (utilities + minimal media queries)
- Dark mode support (theme system handles automatically)

---

## Quick Decision Tree

```
Creating new component?
├─ Can Quasar utility classes handle spacing/layout/text?
│  ├─ YES → Use utilities (q-pa-*, text-*, row/column)
│  └─ NO → Is this standard UI pattern?
│     ├─ YES → Use Quasar component (QBtn, QCard, QDialog)
│     └─ NO → Custom CSS, but...
│        └─ Use theme variables ($color-brand-*, var(--color-*))
│
└─ Final check: Does custom CSS exceed 20% of total styling?
   └─ YES → Refactor to use more utilities
```

---

## Integration with SuperClaude Framework

### Persona Coordination
- **Primary**: Frontend persona (UI/UX specialist)
- **Supports**: Refactorer (code quality), Performance (optimization)
- **Auto-activates with**: Vue 3 + Quasar component creation

### MCP Server Integration
- **Context7**: Quasar official documentation lookup
- **Sequential**: Complex Quasar configuration analysis
- **Magic**: Can work alongside for UI generation (Magic generates, Quasar styles)

### Flag Compatibility
- Works with `--uc` (utility-first naturally token-efficient)
- Compatible with `--think` (analyze component architecture)
- Enhances `--improve --quality` (refactor to utilities)

---

**Version**: 1.0.0
**Last Updated**: 2026-01-12
**Framework Version**: Quasar v2 + Vue 3
**Status**: Production-ready, battle-tested
