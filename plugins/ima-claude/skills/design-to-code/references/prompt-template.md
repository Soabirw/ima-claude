# Implementation Prompt Template

This is the template structure for Phase A output. Fill in the bracketed placeholders with extracted design data. Delete sections that don't apply.

---

```markdown
/task-master [One-line goal as a user story]
Save this prompt and plan to Serena memory as `{feature-name}-plan`.

## Context

- **Page URL**: [current URL of the page being built/redesigned]
- **Design files**: [paths to screenshots in docs/designs/{ticket}/]
- **Related pages**: [URLs of pages with shared components or navigation]
- **Branding reference**: Load `ima-brand` skill for color palette and typography
- **Bootstrap reference**: Load `ima-bootstrap` skill for utility classes and grid
- **Existing code**: [paths to current shortcode files, SCSS partials, page templates]

## What Changes vs What Stays

> Include this section for redesigns. Omit for greenfield pages.

**Changes** (presentation layer only):
- [List specific files/functions that will be modified]

**Stays unchanged** (do not modify):
- [List backend logic, APIs, pure functions, search/filter logic]
- [List existing shortcodes that continue to work as-is]

## Plan

### [Section Name] ([State Annotation])

> State annotations: (Both States), (Landing State Only), (Results State Only)
> Repeat this block for each visual section of the page.

**Layout**: [grid description — e.g., "full-width container, 3-column card grid on lg, stacked on mobile"]
**Background**: [brand variable — e.g., "$ima-brand-primary" or "@include ima-gradient-bg"]

**Text**:
- Heading: "[exact heading text]" — `h2`, `.text-primary`, `fw-bold`
- Subheading: "[exact subheading text]" — `p`, `.text-white`, `mx-auto`
- Body: "[exact body copy]" — `p`, `.text-muted`

**Elements** (left to right, top to bottom):
- [element description] — [Bootstrap classes] — [icon: `fa-regular fa-icon-name`]
- [element description] — [href: /path/to/page]
- [element description] — [existing function: `ima_function_name()`]

**SCSS needed**:
- [Custom SCSS rules — only what Bootstrap utilities can't express]
- [Reference brand mixins: `@include ima-card-white`]

**Notes**: [animation as progressive enhancement, conditional display logic, accessibility considerations]

## Implement

1. Create/modify [file path] — [what to add: main shortcode, orchestrator function, state detection]
2. Create/modify [SCSS file path] — [what to add: page-specific styles, import in _custom.scss]
3. [Additional file changes in priority order]

**Branch strategy**: `feature/{ticket}-{short-description}`
**Approach**: Mobile-first, progressive enhancement. Static layout first, animation as enhancement.

## Test

- [ ] `php -l` on all modified PHP files
- [ ] SCSS compiles without errors (`ddev wp ima-scss compile`)
- [ ] Desktop screenshot matches design at 1920px (landing state)
- [ ] Desktop screenshot matches design at 1920px (results state)
- [ ] Mobile screenshot matches design at 375px (both states)
- [ ] All links resolve to valid paths
- [ ] No hardcoded color values (`rg '#[0-9a-fA-F]{3,6}' --type php --type scss`)
- [ ] Existing functionality preserved (search, filters, pagination)

## Review

- `ima-claude:reviewer` for brand compliance + accessibility audit
- Verify exact copy matches design screenshots
- Verify element order matches design
- Check responsive behavior at all breakpoints

## Document

- [ ] Update Jira ticket with implementation notes
- [ ] Save session to Serena memory as `{feature-name}-implementation`
- [ ] Update component inventory if new shortcodes were created

## Agents

- `ima-claude:explorer` (haiku) — parallel codebase research
- `ima-claude:wp-developer` (sonnet) — PHP/SCSS implementation with skills: `ima-brand`, `ima-bootstrap`, `php-fp-wordpress`
- `ima-claude:reviewer` (sonnet, read-only) — brand compliance after implementation
```
