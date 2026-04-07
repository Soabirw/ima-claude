# Phase B: Prompt → Code — Detailed Procedure

Execute a structured implementation prompt to produce working WordPress code. This phase delegates to `ima-claude:wp-developer` agents and reviews their output.

**Steps**: [1. RESEARCH](#step-1-research-parallel-explorers) → [2. ARCHITECTURE](#step-2-architecture-decisions-before-code) → [3. DECOMPOSE](#step-3-decompose-stories-by-section) → [4. IMPLEMENT](#step-4-implement-agent-delegation) → [5. REVIEW](#step-5-review-before-visual-test) → [6. VISUAL-QA](#step-6-visual-qa)

---

## Step 1: RESEARCH (Parallel Explorers)

Dispatch `ima-claude:explorer` agents in parallel to gather:

### Explorer 1: Brand System
- Read `_variables.scss` — complete color palette, font stack, spacing scale
- Read `_mixins.scss` — available brand mixins and their parameters
- Read `_theme_variables.scss` — Bootstrap variable overrides
- Summarize: what Bootstrap utilities map to brand colors

### Explorer 2: Current Implementation
- Read the template file being modified (or closest existing template)
- Inventory existing shortcodes: names, parameters, what they return
- Read existing helper/render functions — signatures, return types, reuse candidates
- Check page template chain: what does `get_header()` provide? What does `get_footer()` provide?

### Explorer 3: Component Libraries (if applicable)
- Check ima-forms: does it support the form patterns needed? (icons in inputs, custom dropdowns)
- Check ima-ui-components: any reusable components?
- Evaluate migration: use existing library or raw HTML + Bootstrap?

---

## Step 2: ARCHITECTURE (Decisions Before Code)

Document these decisions before proceeding:

1. **New file vs modify existing?** — New shortcode file for redesigns avoids merge conflicts during development
2. **Function reuse** — List exact functions to call (not duplicate). Include signatures:
   ```
   ima_directory_get_filter_options() → ['specialties' => [...], 'states' => [...]]
   ima_directory_search($params) → WP_Query results
   ```
3. **Component migration** — Use existing library or raw HTML? Decide based on feature support, not preference
4. **Page template changes** — Does the page template need modification, or just the shortcode?
5. **State management** — What's shared between page states vs state-specific?

---

## Step 3: DECOMPOSE (Stories by Section)

Break the prompt into implementation stories. Follow the foundation-first pattern:

### Story 1: Foundation (no dependencies)
- Create the file (PHP shortcode + SCSS partial)
- Main orchestrator function with state detection
- Placeholder calls for each section
- SCSS import in `_custom.scss`
- `require_once` in `functions.php`

### Stories 2-N: Section Fills (parallelizable)
- Group by page state when applicable:
  - Landing state sections (one story)
  - Results state sections (one story)
  - Shared sections (one story)
- Each story fills placeholder slots from Story 1
- Stories touching independent insertion points run in parallel

### Final Story: Polish
- Animation and transitions (progressive enhancement — static first)
- Responsive refinements
- Accessibility review
- Visual QA

### Parallelization Rules
- Stories with independent insertion points → run in parallel
- Stories sharing the same function/placeholder → run sequentially
- Story 1 must complete before all others (creates the file structure)
- Polish story runs last (needs all sections in place)

---

## Step 4: IMPLEMENT (Agent Delegation)

Delegate each story to `ima-claude:wp-developer`. Each agent prompt MUST include:

### Required Prompt Elements
1. **Task identity** — Story number, section name, where it fits in the page
2. **File context** — Exact file paths, line numbers to modify, current state of the code
3. **HTML structure** — Specific elements with Bootstrap classes, not "create a search form" but:
   ```
   Row 1: Full-width input with fa-magnifying-glass icon
     - Placeholder: "Keyword search (e.g. name, specialty, or city...)"
   Row 2: 3 equal-width dropdowns (col-12 col-md-4)
   ```
4. **Brand color mapping** — Exact variable names for every color used in this section
5. **Existing functions to reuse** — Function names, signatures, return values
6. **What NOT to do** — Guardrails specific to this story
7. **Verification step** — `php -l` on the PHP file after changes

### Anti-patterns
- "Implement the discover section" → too vague, inconsistent results
- "Make it look like the screenshot" → agent can't see screenshots
- "Use appropriate colors" → must specify exact variable names
- Omitting existing function signatures → agent will reinvent them

---

## Step 5: REVIEW (Before Visual Test)

The orchestrator reviews each agent's output BEFORE visual testing. This catches most issues faster than visual → fix → retest cycles.

### Review Checklist
1. **Exact copy** — Diff generated text against prompt's quoted text. Agents paraphrase.
2. **Element order** — Compare DOM order to prompt's section order. Spatial relationships get reversed.
3. **URL paths** — Verify every href matches the prompt spec. Agents default to common paths (`/join/` instead of `/register/`)
4. **Asset paths** — Glob to verify every referenced image/icon path exists. Grep for existing usage patterns.
5. **Color compliance** — Grep for hardcoded hex values (should be zero — all brand variables)
6. **Function reuse** — Verify agents called existing functions instead of reimplementing

### Fixing Issues
- <5 lines: Orchestrator fixes directly via Edit tool (faster than re-delegating)
- Larger issues: Re-delegate to wp-developer with specific correction instructions

---

## Step 6: VISUAL-QA

### Step 0: Compile SASS (before anything else)
New SCSS won't appear until compiled. Verify new classes exist in `bundle.css` before testing.
```
ddev wp ima-scss compile
```

### Desktop Testing
1. Navigate to page in chrome-devtools
2. Full-page screenshot at 1920px width (landing state)
3. Full-page screenshot (results state with search params)
4. Viewport screenshots of specific sections as needed

### Mobile Testing
1. Emulate mobile device (390x844, 2x DPR, touch)
2. Screenshot both page states
3. Verify responsive stacking (single-column layout)

### What to Check
- Gradient rendering
- Card floating/overlap effects
- Color matches (brand colors, not approximations)
- Text content matches design exactly
- Icons correct (FA vs BI, regular vs solid weight)
- Responsive stacking on mobile
- Interactive elements visible and clickable
- Sticky/fixed elements behave correctly

### Iteration
Compare screenshots against original design. Note discrepancies, fix via Edit or re-delegate, re-screenshot until acceptable. Usually 1-2 iteration rounds.
