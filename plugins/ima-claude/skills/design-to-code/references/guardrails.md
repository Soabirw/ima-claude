# Guardrails — Lessons from Real Failures

Every rule here was learned from a specific failure during the FNR-2785 implementation. Prevention strategies are included so the same mistakes don't recur.

---

## Color

- **Never hardcode hex values** in SCSS or inline styles. Every color must come from `$ima-brand-*` SCSS variables or Bootstrap `.text-*` / `.bg-*` utility classes.
- **Load the brand palette BEFORE composing the prompt or writing code.** Doing this after means an expensive editing pass to replace color descriptions with variable names.
- **Decorative category colors are the exception** — colors that serve UI categorization (not brand identity) can use explicit hex values. Example: pink for "Family Medicine" chip icons.
- **Final check**: `rg '#[0-9a-fA-F]{3,6}' --type php --type scss` should return zero matches in new code.

## Copy

- **Always provide exact text in quotes.** "Search our directory of ethics-committed physicians dedicated to honest, patient-first care." — not a paraphrase like "Search our curated network of independent practitioners."
- **Agents WILL paraphrase** descriptive text unless given the exact copy. This is the most common failure mode.
- **If text is unclear in the screenshot**, flag it with `[VERIFY: exact text unclear from screenshot]` rather than guessing.
- **Include ALL text** — headings, subheadings, body copy, button labels, placeholder text, tooltip text. If it's visible in the design, it goes in the prompt.

## Assets

- **Verify every asset path exists** before referencing it in code. Use `Glob` or `rg` to find existing usage.
- **Never assume local file paths.** Logos may be served from CDN, uploads directory, or rendered via a filter. Grep for existing usage patterns (e.g., `ima_ui_footer_logo_url`).
- **Check the existing icon system** before introducing new icon dependencies. If the site uses Font Awesome, use Font Awesome — don't mix Bootstrap Icons into FA sites.

## Architecture

- **Check if site header/footer already provides the element.** Design screenshots show the final composite — the nav bar in the design may BE the standard site header via `get_header()`, not a custom inline nav. Building a custom one creates a duplicate.
- **Preserve existing backend logic.** Design changes are presentation-layer only. Search logic, API endpoints, pure functions, sorting, pagination — these do NOT change unless explicitly stated.
- **Bootstrap utility first, custom SCSS only when Bootstrap cannot express the style.** Check the hierarchy: Bootstrap utility → IMA brand mixin → Bootstrap variable override → then custom CSS.
- **Evaluate component libraries before implementing.** Check ima-forms, ima-ui-components for existing patterns. Decide based on feature support, not preference. Document the decision.

## Spatial Relationships

- **Be explicit about element order** in prompts. "Left to right: social icons → logo" — agents don't reliably interpret spatial relationships from screenshots.
- **Specify flex direction and alignment** when order matters: `d-flex flex-row` vs `flex-row-reverse`.
- **For stacked layouts**, specify top-to-bottom order explicitly.

## Verification

- **Run `php -l` after every PHP change.** Syntax errors caught early prevent cascading debugging.
- **Recompile SASS before ANY visual testing.** New SCSS imports don't auto-apply. Run `ddev wp ima-scss compile` and verify new classes appear in `bundle.css`.
- **Screenshot at both desktop and mobile widths.** Desktop (1920px) and mobile (375px) catch different categories of issues.
- **Grep for hardcoded hex values** as a final check. New code should reference only brand variables.
- **Verify existing functionality** still works after changes — search, filters, pagination, form submissions.
