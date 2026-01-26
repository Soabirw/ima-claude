# Quasar Utility Classes - Complete Reference

**Purpose**: Comprehensive reference for all Quasar utility classes (Bootstrap-style)

---

## Spacing System (8px Grid)

### Size Scale
- `xs` = 4px (0.25rem)
- `sm` = 8px (0.5rem)
- `md` = 16px (1rem)
- `lg` = 24px (1.5rem)
- `xl` = 48px (3rem)

### Padding Classes

**All Sides:**
- `q-pa-none` - 0
- `q-pa-xs` - 4px
- `q-pa-sm` - 8px
- `q-pa-md` - 16px
- `q-pa-lg` - 24px
- `q-pa-xl` - 48px

**Top:** `q-pt-{size}`
**Right:** `q-pr-{size}`
**Bottom:** `q-pb-{size}`
**Left:** `q-pl-{size}`
**Horizontal (L+R):** `q-px-{size}`
**Vertical (T+B):** `q-py-{size}`

### Margin Classes

Same pattern as padding, but with `m` instead of `p`:
- `q-ma-{size}` - All sides
- `q-mt-{size}` - Top
- `q-mr-{size}` - Right
- `q-mb-{size}` - Bottom
- `q-ml-{size}` - Left
- `q-mx-{size}` - Horizontal
- `q-my-{size}` - Vertical

### Margin Auto
- `q-mx-auto` - Center horizontally
- `q-ml-auto` - Push to right
- `q-mr-auto` - Push to left

---

## Typography Classes

### Headings
- `text-h1` - 6rem (96px), weight 300
- `text-h2` - 3.75rem (60px), weight 300
- `text-h3` - 3rem (48px), weight 400
- `text-h4` - 2.125rem (34px), weight 400
- `text-h5` - 1.5rem (24px), weight 400
- `text-h6` - 1.25rem (20px), weight 500

### Body Text
- `text-body1` - 1rem (16px), weight 400
- `text-body2` - 0.875rem (14px), weight 400
- `text-subtitle1` - 1rem (16px), weight 500
- `text-subtitle2` - 0.875rem (14px), weight 500
- `text-caption` - 0.75rem (12px), weight 400
- `text-overline` - 0.75rem (12px), weight 400, uppercase

### Font Weight
- `text-weight-thin` - 100
- `text-weight-light` - 300
- `text-weight-regular` - 400
- `text-weight-medium` - 500
- `text-weight-bold` - 700
- `text-weight-bolder` - 900

### Text Style
- `text-italic`
- `text-no-wrap`
- `text-strike`
- `text-uppercase`
- `text-lowercase`
- `text-capitalize`

### Text Alignment
- `text-left`
- `text-center`
- `text-right`
- `text-justify`

---

## Color Classes

### Brand Colors (Theme-Aware)
- `text-primary` / `bg-primary`
- `text-secondary` / `bg-secondary`
- `text-accent` / `bg-accent`

### Semantic Colors
- `text-positive` / `bg-positive` - Success (green)
- `text-negative` / `bg-negative` - Error (red)
- `text-warning` / `bg-warning` - Warning (yellow/orange)
- `text-info` / `bg-info` - Info (blue)

### Grayscale
- `text-grey-1` / `bg-grey-1` - Lightest
- `text-grey-2` / `bg-grey-2`
- `text-grey-3` / `bg-grey-3`
- `text-grey-4` / `bg-grey-4`
- `text-grey-5` / `bg-grey-5` - Medium
- `text-grey-6` / `bg-grey-6`
- `text-grey-7` / `bg-grey-7`
- `text-grey-8` / `bg-grey-8`
- `text-grey-9` / `bg-grey-9` - Darkest

### Special Colors
- `text-white` / `bg-white`
- `text-black` / `bg-black`
- `text-transparent` / `bg-transparent`

---

## Flexbox Classes

### Containers
- `row` - flex row (display: flex)
- `column` - flex column (display: flex; flex-direction: column)
- `row inline` - inline flex row
- `column inline` - inline flex column
- `reverse` - reverse order (combine with row/column)

### Alignment (align-items)
- `items-start` - flex-start
- `items-center` - center
- `items-end` - flex-end
- `items-stretch` - stretch
- `items-baseline` - baseline

### Justification (justify-content)
- `justify-start` - flex-start
- `justify-center` - center
- `justify-end` - flex-end
- `justify-between` - space-between
- `justify-around` - space-around
- `justify-evenly` - space-evenly

### Self Alignment
- `self-start`
- `self-center`
- `self-end`
- `self-stretch`
- `self-baseline`

### Flex Items
- `col` - flex: 1 (equal width)
- `col-auto` - flex: 0 0 auto (content width)
- `col-grow` - flex-grow: 1
- `col-shrink` - flex-shrink: 1

### Flex Wrap
- `wrap` - flex-wrap: wrap
- `no-wrap` - flex-wrap: nowrap
- `reverse-wrap` - flex-wrap: wrap-reverse

---

## Display Classes

- `block` - display: block
- `inline` - display: inline
- `inline-block` - display: inline-block
- `hidden` - display: none (use v-if/v-show instead when possible)

---

## Border & Radius Classes

- `rounded-borders` - border-radius: 4px
- `no-border` - border: 0
- `no-border-radius` - border-radius: 0

---

## Shadow Classes

- `shadow-1` - Subtle elevation
- `shadow-2` - Low elevation
- `shadow-3` - Medium elevation (default)
- `shadow-4` - High elevation
- `shadow-5` - Very high elevation
- `no-shadow` - box-shadow: none

---

## Position Classes

- `relative-position` - position: relative
- `absolute` - position: absolute
- `fixed` - position: fixed
- `absolute-top` - top: 0
- `absolute-right` - right: 0
- `absolute-bottom` - bottom: 0
- `absolute-left` - left: 0
- `absolute-center` - Center absolutely
- `absolute-full` - Fill parent (top/right/bottom/left: 0)

---

## Cursor Classes

- `cursor-pointer` - pointer
- `cursor-not-allowed` - not-allowed
- `cursor-inherit` - inherit
- `cursor-none` - none

---

## Overflow Classes

- `overflow-auto` - auto
- `overflow-hidden` - hidden
- `overflow-visible` - visible
- `scroll` - overflow: auto

---

## Width/Height Classes

### Width
- `fit` - width: 100%
- `full-width` - width: 100%
- `full-height` - height: 100%

### Max/Min
- Can use inline styles: `style="max-width: 600px"`
- Or custom classes in scoped styles

---

## Responsive Classes

### Breakpoint Visibility

Hide on specific breakpoints:
- `lt-sm` - Hide when < 600px
- `lt-md` - Hide when < 1024px
- `lt-lg` - Hide when < 1440px
- `gt-xs` - Hide when > 599px
- `gt-sm` - Hide when > 1023px
- `gt-md` - Hide when > 1439px

**Example:**
```vue
<div class="lt-md">Hidden on mobile/tablet</div>
<div class="gt-sm">Hidden on mobile, shown on desktop</div>
```

---

## Common Utility Combinations

### Centered Header
```vue
<div class="text-center q-py-lg q-mb-lg">
  <h1 class="text-h3 text-weight-bold text-primary q-mb-sm q-mt-none">
    Title
  </h1>
  <p class="text-h6 text-italic text-accent q-mb-none">
    Subtitle
  </p>
</div>
```

### Flex Container with Gap
```vue
<div class="row items-center justify-between q-mb-md">
  <div class="col-auto">Left content</div>
  <div class="col-auto">Right content</div>
</div>
```

### Card with Padding
```vue
<q-card class="q-pa-md q-mb-lg rounded-borders">
  <div class="text-h6 text-weight-bold q-mb-sm">Card Title</div>
  <p class="text-body2 text-grey-7 q-mb-none">Card content</p>
</q-card>
```

### Toggle with Description
```vue
<div class="q-pa-md q-mb-md rounded-borders">
  <q-toggle
    v-model="value"
    label="Option Label"
    class="text-weight-medium q-mb-sm"
  />
  <p class="text-caption text-grey-7 q-pl-sm q-mb-none">
    Description of what this toggle does
  </p>
</div>
```

---

**Reference**: Official Quasar docs at https://quasar.dev/style/spacing
