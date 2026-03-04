---
name: livecanvas
description: >-
  LiveCanvas WordPress page builder with Bootstrap 5, Loops & Logic (Tangible) templating,
  and PicoStrap theme integration. Use when: building LiveCanvas pages, creating dynamic
  content with L&L/Tangible tags, designing Bootstrap layouts in LiveCanvas editor, working
  with LiveCanvas shortcodes, WooCommerce templates in LiveCanvas, ACF dynamic blocks,
  PicoStrap theme customization, or any visual page building that stores content in the
  WordPress database rather than PHP files. Triggers on: livecanvas, live canvas, tangible,
  loops and logic, L&L, picostrap, lc_get_posts, lc-block, tangible tag.
---

# LiveCanvas

Visual page builder for WordPress. Pure HTML/Bootstrap — no proprietary markup, no vendor lock-in.
Content lives in the WordPress database (`wp_posts`), not PHP template files.

**Cross-reference**: Use `ima-bootstrap` skill for Bootstrap 5.3 utilities, grid, components, and IMA brand integration. LiveCanvas uses your theme's Bootstrap — everything in `ima-bootstrap` applies directly.

## Mental Model

```
LiveCanvas Page = HTML + Bootstrap classes + <tangible> blocks for dynamic data
```

- **Static content**: Write Bootstrap HTML directly (cards, grids, heroes, etc.)
- **Dynamic content**: Wrap Loops & Logic tags in `<tangible>` blocks
- **Logic/conditions**: L&L replaces PHP — think Handlebars/Twig, not `<?php ?>`
- **No custom CSS framework**: LiveCanvas adds zero CSS. Your theme's Bootstrap is the only framework.

## Page Structure

Every LiveCanvas page follows this hierarchy:

```html
<main>
  <section>                          <!-- Full-width, not nestable -->
    <div class="container">          <!-- or container-fluid -->
      <div class="row">
        <div class="col-lg-6">
          <div class="lc-block">     <!-- Smallest editable unit -->
            <h2 editable="inline">Heading</h2>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="lc-block">
            <p editable="rich">Content here</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>
```

**Rules**:
- `<section>` elements are always direct children of `<main>`, edge-to-edge
- Standard Bootstrap grid inside: `.container` > `.row` > `.col-*`
- `lc-block` divs are the smallest building blocks
- `editable="inline"` for single-line text, `editable="rich"` for rich text

## Dynamic Content with Loops & Logic

Wrap L&L markup in `<tangible>` tags. Add `class="live-refresh"` for real-time preview in the editor.

```html
<tangible class="live-refresh">
  <Loop type="post" count="3" orderby="date" order="desc">
    <div class="card mb-3">
      <div class="card-body">
        <h5 class="card-title"><Field title /></h5>
        <p class="card-text"><Field excerpt /></p>
        <a href="{Field url}" class="btn btn-primary">Read More</a>
      </div>
    </div>
  </Loop>
</tangible>
```

### L&L Quick Reference

| Tag | Purpose | Example |
|-----|---------|---------|
| `<Loop>` | Query & iterate | `<Loop type="post" count="5">` |
| `<Field>` | Output a value | `<Field title />` |
| `<If>` / `<Else />` | Conditions | `<If field="image" exists>` |
| `<Set>` / `<Get>` | Variables | `<Set name="total">0</Set>` |
| `<Date>` | Date formatting | `<Date format="F j, Y" />` |
| `<Format>` | String ops | `<Format case="upper">text</Format>` |
| `<Math>` | Arithmetic | `<Math>price * 1.1</Math>` |
| `<Template>` | Reuse saved template | `<Template name="card" />` |

**Tags inside attributes** — use `{}` instead of `<>`:
```html
<a href="{Field url}"><Field title /></a>
<img src="{Field image_url}" alt="{Field title}" />
```

### Common Patterns

**Posts grid with fallback**:
```html
<tangible class="live-refresh">
  <If loop exists type="post" category="news">
    <div class="row g-4">
      <Loop type="post" category="news" count="6">
        <div class="col-md-4">
          <div class="card h-100">
            <If field="image">
              <img src="{Field image_url}" class="card-img-top" alt="{Field title}" />
            </If>
            <div class="card-body">
              <h5 class="card-title"><Field title /></h5>
              <p class="card-text"><Field excerpt /></p>
            </div>
            <div class="card-footer">
              <a href="{Field url}" class="btn btn-outline-primary btn-sm">Read More</a>
            </div>
          </div>
        </div>
      </Loop>
    </div>
  <Else />
    <p class="text-muted">No news posts found.</p>
  </If>
</tangible>
```

**ACF fields**:
```html
<tangible class="live-refresh">
  <Field acf_text="subtitle" />
  <img src="{Field acf_image=hero_image field=url}" alt="" />
  <If acf_true_false="show_cta">
    <a href="{Field acf_text=cta_url}" class="btn btn-primary">
      <Field acf_text="cta_label" />
    </a>
  </If>
</tangible>
```

**ACF Repeater**:
```html
<tangible class="live-refresh">
  <Loop acf_repeater="team_members">
    <div class="col-md-4 text-center">
      <img src="{Field acf_image=photo field=url}" class="rounded-circle mb-3" width="150" />
      <h5><Field name /></h5>
      <p class="text-muted"><Field role /></p>
    </div>
  </Loop>
</tangible>
```

**Custom post type with taxonomy filter**:
```html
<tangible class="live-refresh">
  <Loop type="post" post_type="portfolio" taxonomy="project_type" terms="web-design" count="9">
    <Field title />
  </Loop>
</tangible>
```

## Reusable Sections

Save any section to a library. Recall on other pages:
```
[lc_html_section id="123"]
```
Edits propagate everywhere the section is used.

## LiveCanvas Shortcodes (Legacy)

Still supported alongside L&L. Use for simple field output without `<tangible>` wrapper:

| Shortcode | Purpose |
|-----------|---------|
| `[lc_the_title]` | Post title |
| `[lc_the_content]` | Post content |
| `[lc_the_date]` | Post date |
| `[lc_the_thumbnail]` | Featured image |
| `[lc_the_excerpt]` | Excerpt |
| `[lc_the_permalink]` | URL |
| `[lc_the_cf]` | Custom field |
| `[lc_the_terms]` | Taxonomy terms |
| `[lc_if]` | Conditional |
| `[lc_get_posts]` | Post query loop |

**Prefer L&L for new work** — shortcodes are maintained for backward compatibility.

## When to Use What

| Need | Use |
|------|-----|
| Static layout, typography, spacing | Bootstrap classes directly (see `ima-bootstrap`) |
| Dynamic post loops, conditions | L&L `<tangible>` blocks |
| Simple single-field output | L&L `<Field>` or legacy shortcode |
| ACF field display | L&L ACF tags |
| WooCommerce templates | LiveCanvas WooCommerce shortcodes |
| SCSS/theme customization | PicoStrap child theme |
| Complex component patterns | Bootstrap components (see `ima-bootstrap`) |

## Reference Files

Load these as needed for deeper information:

- **[Loops & Logic Reference](references/loops-and-logic.md)** — Complete L&L syntax: all tags, Loop query parameters, Field types, If conditions, ACF integration, variables, Date/Format/Math, List/Map, WooCommerce
- **[LiveCanvas Features](references/livecanvas-features.md)** — Editor workflow, all shortcodes with parameters, WooCommerce shortcodes, Forms API, reusable sections, keyboard shortcuts, template assignment
- **[PicoStrap Integration](references/picostrap.md)** — Theme architecture, SCSS pipeline, NinjaBootstrap utilities, child theme setup, dark mode, customizer options
