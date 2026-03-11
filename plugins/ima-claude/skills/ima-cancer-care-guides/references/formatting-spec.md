# Cancer Care Guide — Normalized Formatting Spec

## Purpose

Maps Word doc paragraph types → HTML/PDF styling. Values confirmed by extracting
Canva design data from the Cancer Drug Resistance Guide (March 2026).

**Pipeline:** Word (.docx) → `extract_docx.py` → `generate_html.py` → branded HTML

---

## Page Setup

| Property          | Value               | Notes |
|-------------------|----------------------|-------|
| Page size         | US Letter (8.5 × 11 in) | 612 × 792 pt / 816 × 1056 Canva px |
| Margins (L/R/T/B) | 0.5 in (36 pt)      | Confirmed from Canva element positions |
| Body text width   | 7.5 in (540 pt)     | = page width − 2 × margin |
| Footer position   | 0.4 in from bottom   | Centered, thin rule above |

---

## Cover Page

Gradient background: `linear-gradient(150deg, #00066F → #00B8B8)` (Trustworthy Indigo → Bright Teal).
All text centered. Canva uses IMA gradient teal/indigo logo at top.

| Element          | Font          | Size     | Weight  | Color    | Align  | Tracking | Notes |
|------------------|---------------|----------|---------|----------|--------|----------|-------|
| Title line 1     | Lato          | 90.5 pt  | Bold    | #FFFFFF  | Center | 0        | ALL CAPS, e.g. "CANCER" (Canva: 120.722 × 0.75) |
| Title line 2     | Lato          | 67 pt    | Bold    | #FFFFFF  | Center | 0        | ALL CAPS, e.g. "RESISTANCE" (Canva: 89.293 × 0.75) |
| Subtitle         | Lato          | 25 pt    | Regular | #FFFFFF  | Center | wide     | e.g. "And Interventions to Mitigate Resistance" (Canva: 33.33 × 0.75) |
| Authors          | Lato          | 19 pt    | Regular | #FFFFFF  | Center | wide     | e.g. "Paul E. Marik, MD / Justus R. Hope, MD" (Canva: 25.33 × 0.75) |
| Disclaimer       | Lato          | 12 pt    | Bold    | #FFFFFF  | Center | 0        | Guide description, Canva uses bold for this text |
| Date             | Lato          | 12 pt    | Bold    | #000000  | Center | 0        | e.g. "Updated March 2026" — Canva shows this as bold black |

### Cover confirmed from Canva design data:
- [x] Title line 1: 90.5pt (Canva 120.722 × 0.75)
- [x] Title line 2: 67pt (Canva 89.293 × 0.75) — second line is SMALLER than first
- [x] Subtitle: 25pt (Canva 33.33 × 0.75)
- [x] Authors: 19pt (Canva 25.33 × 0.75)
- [x] Background: gradient #00066F → #00B8B8
- [ ] Logo placement: IMA gradient logo at top, exact position TBD

---

## Content Pages — Headings

| Element          | Font   | Size   | Weight | Color    | Align   | Tracking | Notes |
|------------------|--------|--------|--------|----------|---------|----------|-------|
| Section heading  | Lato   | 15 pt  | Bold   | #00066F  | Center  | tight    | Canva: 20.05 × 0.75 = 15pt, tracking=-16 (x10 occurrences) |
| Sub heading      | Lato   | 13 pt  | Bold   | #00066F  | Justify | tight    | Canva: 17.33 × 0.75 = 13pt, tracking=-16 (x29 occurrences) |
| Intro heading    | Lato   | 15 pt  | Bold   | #00066F  | Center  | tight    | "Introduction" — same as section heading |

### Heading confirmed from Canva:
- [x] Section headings: 15pt bold navy, **centered**, tight tracking
- [x] Sub-headings: 13pt bold navy, **justified** (not left-aligned), tight tracking

---

## Content Pages — Body Text

| Element          | Font   | Size   | Weight  | Color    | Align   | Tracking | Notes |
|------------------|--------|--------|---------|----------|---------|----------|-------|
| Body paragraph   | Lato   | 12 pt  | Regular | #000000  | Justify | tight    | Canva: 16.0 × 0.75 = 12pt, tracking=-16 (x31 occurrences) |
| Body bold inline | Lato   | 12 pt  | Bold    | #000000  | Justify | tight    | Canva: 16.0 × 0.75, bold + black (x26 occurrences) |
| Body bold navy   | Lato   | 12 pt  | Bold    | #00066F  | Justify | tight    | Canva: 16.0 × 0.75, bold + navy (x16 occurrences) — inline bold headings |
| Bullet item (L1) | Lato   | 12 pt  | Regular | #000000  | Left    | —        | Bullet char: • (solid dot), ~18pt indent, navy marker |
| Bullet item (L2) | Lato   | 12 pt  | Regular | #000000  | Left    | —        | Nested sub-bullet, ~36pt indent |

### Body confirmed from Canva:
- [x] Body text color: **#000000** (pure black, not #1A1A1A)
- [x] Body size: 12pt
- [x] Bullet markers: navy colored (::marker { color: #00066F })
- [x] Three body text roles: regular (#000000), bold (#000000), bold navy (#00066F)

---

## Warning Box

| Property    | Value              | Notes |
|-------------|---------------------|-------|
| Background  | #00066F (navy)      | Full-width box |
| Text color  | #FFFFFF + #FFCC00   | White body text, Vital Gold for emphasis |
| Font        | Lato 12pt Bold      | Canva: 16.0 × 0.75, bold, white |
| Alignment   | Center              | |
| Padding     | 10pt all sides      | |

---

## Q&A Section

| Element     | Font  | Size   | Weight | Color   | Align   | Notes |
|-------------|-------|--------|--------|---------|---------|-------|
| Question    | Lato  | 12 pt  | Bold   | #00066F | Left    | Ends with "?" |
| Answer      | Lato  | 12 pt  | Regular| #000000 | Justify | Starts with YES/NO |

---

## References

| Element      | Font  | Size    | Weight  | Color    | Align | Notes |
|--------------|-------|---------|---------|----------|-------|-------|
| Ref heading  | Lato  | 13 pt   | Bold    | #00066F  | Left  | "References" + navy rule below |
| Ref entry    | Lato  | 8 pt    | Regular | #333333  | Left  | Hanging 14pt indent |

---

## Footer (all content pages)

| Property    | Value                    | Notes |
|-------------|---------------------------|-------|
| Font        | Lato 10pt                 | Canva: 13.33 × 0.75 = 10pt |
| Color       | #000000 (title) + #FFCC00 (date) | Footer has gold date element |
| Alignment   | Center                    | Wide tracking |
| Content     | "Guide Title (Date)"      | Single line |
| Rule above  | 0.5pt, #D9D9D9            | Canva uses #D9D9D9 for lines |

---

## Figure / Table Captions

| Property    | Value       | Notes |
|-------------|-------------|-------|
| Font        | Lato 12pt   | |
| Color       | #000000     | |
| Alignment   | Left        | |
| Format      | "Table N. Description" / "Figure N. Description" | |

---

## Color Palette (Canva-confirmed)

| Name               | Hex       | Usage |
|--------------------|-----------|-------|
| Trustworthy Indigo | #00066F   | Cover gradient start, headings, bullets, warning bg |
| Bright Teal        | #00B8B8   | Cover gradient end |
| Vital Gold         | #FFCC00   | Warning emphasis, footer date |
| Light Gray         | #D9D9D9   | Rules, dividers |
| Body Black         | #000000   | Body text (Canva uses pure black) |
| Dark Gray          | #333333   | Reference entries |
| White              | #FFFFFF   | Cover text, warning text |

### Color notes:
- IMA Brand Book is source of truth — all colors map to brand palette
- Canva design body text is #000000 (not #1A1A1A from earlier estimates)
- Cover uses gradient background, not flat navy

---

## Font Families (Canva IDs)

| Canva ID      | Actual Font | Usage |
|---------------|-------------|-------|
| YAFdJuFCnaw   | Lato        | 95% of all text — body, headings, cover |
| YAFcfoaHu-s   | (secondary) | Cover subtitle line — may be Open Sans |
| YACgEcnJpjs   | (accent)    | Small uppercase decorative elements |

For HTML output: use Lato from Google Fonts for everything (matches 95% of Canva usage).

---

## Word → HTML/PDF Paragraph Type Mapping

| extract_docx type    | HTML element / class    | Canva size (× 0.75 = pt) |
|----------------------|------------------------|--------------------------|
| `h1`                 | `.cover-title-1`       | 120.7 → 90.5pt          |
| `heading_bold` (1st) | `.cover-title-1`       | 120.7 → 90.5pt          |
| `heading_bold` (2nd) | `.cover-title-2`       | 89.3 → 67pt             |
| `heading_bold` (3rd+)| `h2.section-heading`   | 20.1 → 15pt             |
| `h2`                 | `h2.section-heading`   | 20.1 → 15pt             |
| `h3`                 | `h3.sub-heading`       | 17.3 → 13pt             |
| `body`               | `p`                    | 16.0 → 12pt             |
| `bullet`             | `li`                   | 16.0 → 12pt             |
| `author`             | `.cover-authors`       | 25.3 → 19pt             |
| `date`               | `.cover-date`          | 16.0 → 12pt             |
| `disclaimer`         | `.cover-disclaimer`    | 16.0 → 12pt             |
| `warning`            | `.warning-box`         | 16.0 → 12pt             |
| `question`           | `.qa-question`         | 16.0 → 12pt             |
| `answer_start`       | `.qa-answer`           | 16.0 → 12pt             |
| `figure_caption`     | `.caption`             | 16.0 → 12pt             |
| `table_caption`      | `.caption`             | 16.0 → 12pt             |
| `ref_heading`        | `.ref-heading`         | 13.3 → 10pt             |
| `reference`          | `.reference`           | ~10.7 → 8pt             |

---

## Canva Design Data Source

Values extracted from `Copy of Cancer Drug Resistance Guide March 2026.html`
(Canva design viewer export, March 2026). 176 font-size declarations analyzed,
94 positioned elements mapped. Canva internal units convert to points at × 0.75.
