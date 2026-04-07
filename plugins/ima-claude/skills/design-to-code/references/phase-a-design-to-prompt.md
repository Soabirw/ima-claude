# Phase A: Design → Prompt — Detailed Procedure

Transform design screenshots into a structured implementation prompt. This phase requires opus-level judgment for visual analysis, brand mapping, and prompt composition.

**Steps**: [1. GATHER](#step-1-gather-parallel) → [2. ANALYZE](#step-2-analyze-brand-palette-loading) → [3. CROP](#step-3-crop-iterative-image-analysis) → [4. EXTRACT](#step-4-extract-per-crop) → [5. MAP](#step-5-map-visual--technical) → [6. COMPOSE](#step-6-compose) → [7. VALIDATE](#step-7-validate)

---

## Step 1: GATHER (Parallel)

Run three parallel streams:

### Stream 1: Jira Context
- Fetch issue via mcp-atlassian (`getJiraIssue`)
- Extract: summary, description, acceptance criteria, linked issues
- Read ALL comments — stakeholder requirements often hide in comment threads, not the description
- Note attachment metadata (screenshot filenames, dimensions)

### Stream 2: Screenshots
- Receive screenshots from user or download from Jira attachments
- Save to `docs/designs/{ticket}/` directory
- Note image dimensions — tall images (>2000px) will need cropping

### Stream 3: Codebase Exploration
- Dispatch `ima-claude:explorer` agent to map:
  - Current template file and shortcodes
  - Existing helper/render functions (signatures and return types)
  - SCSS file structure (partials, variables, existing page styles)
  - Page template chain (`get_header()` → content → `get_footer()`)
- Key question: What exists today that the redesign must preserve?

---

## Step 2: ANALYZE (Brand Palette Loading)

**This step MUST complete before Step 6 (COMPOSE).** Loading the palette first means every section gets correct brand variable references on the first pass — avoiding an expensive editing pass afterward.

- Load `ima-brand` skill for the complete palette
- Create a working color mapping table:

```
| Visual Element | Brand Variable | Hex | Bootstrap Utility |
|---|---|---|---|
| Dark blue headers | $ima-brand-primary | #00066F | .text-primary |
| Teal buttons/CTAs | $ima-brand-secondary | #00B8B8 | .text-secondary, .bg-secondary |
| Gold accents | $ima-brand-gold | #FFCC00 | .text-ima-gold |
| Light backgrounds | $ima-brand-gray-light | #F2F3F5 | .bg-light |
```

- Inventory available brand mixins: `@include ima-gradient-bg`, `@include ima-card-white`, `@include ima-button-primary`, etc.

---

## Step 3: CROP (Iterative Image Analysis)

Full-image views lose critical detail — text becomes unreadable, subtle elements get missed. Use iterative cropping:

### Pass 1: Full-image overview
- View each screenshot at full size
- Identify section boundaries (background changes, whitespace gaps, visual groupings)
- Identify page states (e.g., landing vs results, empty vs populated)

### Pass 2: Section crops (6-8 per image)
- Use Python PIL to crop each section:
```python
from PIL import Image
img = Image.open('screenshot.png')
# Overlap sections by ~100px to avoid missing content at boundaries
section = img.crop((0, start_y, width, end_y))
section.save(f'section-{name}.png')
```
- Name crops descriptively: `hero-section.png`, `search-form.png`, `discover-cards.png`

### Pass 3: Detail crops (targeted)
- After viewing section crops, identify areas too small for text extraction
- Crop individual components: single cards (~450x360px), form fields, badge legends
- Crop text areas for exact copy extraction

---

## Step 4: EXTRACT (Per Crop)

For each section/detail crop, extract:

- **Text content** — exact wording in quotes. "Discover Providers Who Share Your Values" not "Find providers who share your values"
- **Icons** — identify by library and class name (e.g., `fa-regular fa-stethoscope`). If uncertain, use "fa-regular fa-stethoscope or similar" pattern
- **Colors** — note approximate hex values for mapping in Step 5
- **Layout** — describe grid structure (e.g., "3-column on desktop, stacked on mobile")
- **Interactive behavior** — specify URL params, form actions, click targets. Bridge design → engineering by documenting function, not just appearance

---

## Step 5: MAP (Visual → Technical)

Translate visual elements to technical references:

| Visual | Technical |
|---|---|
| Colors | Brand SCSS variables (`$ima-brand-primary`) |
| Components | Existing shortcode names (`[ima_directory_filters]`) |
| Icons | FontAwesome/Bootstrap Icons classes (`fa-regular fa-search`) |
| Layout | Bootstrap grid classes (`col-lg-4 col-md-6`) |
| Spacing | Bootstrap utilities (`py-5`, `mb-4`) or brand scale |

For redesigns: explicitly document which existing functions to reuse vs rebuild.

---

## Step 6: COMPOSE

Read `references/prompt-template.md` for the template structure. Write the prompt section-by-section:

### Structure conventions
- **Named sections** over numbered: "Header Section", "Search Form" not "Section 01"
- **State annotations** on every section: `(Both States)`, `(Landing Only)`, `(Results Only)`
- **Exact text in quotes** — never describe text, provide it verbatim
- **Brand variables inline** — `$ima-brand-secondary` not "teal"
- **Bootstrap classes inline** — `.text-primary`, `.bg-light`

### For redesigns
- Add a **"What Changes vs What Stays"** section at the top
- Explicitly list what NOT to modify (backend logic, API, pure functions)
- Frame component migration as a decision point with criteria, not a directive

### For multi-state pages
- Document each state separately with clear annotations
- Shared elements get `(Both States)` annotation

---

## Step 7: VALIDATE

Before presenting to the user:

1. Re-read each prompt section
2. Compare against the corresponding crop
3. Verify: exact text match, correct brand variables, correct element order, no missing elements
4. Check all referenced file paths exist in the codebase
5. Ensure the "What Changes vs What Stays" section is accurate

Save the completed prompt to `docs/designs/{ticket}/PROMPT.md` and Serena memory.
