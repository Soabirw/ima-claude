---
name: ima-cancer-care-guides
description: >
  Create IMA Health Cancer Care companion guides from Markdown source files.
  Outputs branded HTML (primary), PowerPoint, or PDF for Canva import.
  Use when: user asks to create a cancer care guide, resistance guide,
  repurposed drugs guide, or any standalone IMA cancer topic document.
  Triggers on: "cancer care guide", "cancer companion guide", "resistance guide",
  "repurposed drugs guide", "IMA cancer guide", "create cancer guide", "new cancer guide".
---

# IMA Cancer Care Guide Generator

One Markdown file → HTML, PDF, or PowerPoint — all consistently styled.

## Outputs

| Output | How | Use for |
|--------|-----|---------|
| **HTML** | `generate_html_md.py` | Browser preview, print to PDF |
| **PDF** | Chrome print → Save as PDF | Canva import, distribution |
| **PPTX** | `generate_pptx.py` | Presentations |

Canva tip: Import PDF (not PPTX) — renders more faithfully.

## Quick Start

Install once: `pip install -r scripts/requirements.txt`

```bash
# HTML
python3 scripts/generate_html_md.py "path/to/guide.md" --out "output.html"

# PowerPoint
python3 scripts/generate_pptx.py "path/to/guide.md" --out "output.pptx"

# PDF: Open HTML in Chrome → Ctrl+P → Save as PDF → Margins: None, enable Background graphics
```

## Markdown Format

### Cover (YAML front matter)
```yaml
---
title1: Cancer
title2: Resistance
subtitle: and Interventions to Mitigate Resistance
authors: Paul E. Marik, MD, FCCM, FCCP | Justus R. Hope, MD
date: Updated March 2026
---
```

### Page Control
```markdown
<!-- pagebreak -->          ← new page/slide
<!-- spacer -->             ← vertical space (default 65pt)
<!-- spacer 30pt -->        ← specific vertical space
```

### Content Markup
```markdown
## Section Heading         ← major section (navy, large)
### Sub-heading            ← sub-section (navy, medium)

- Bullet point

**Bold text** and *italic text* inline.

:::warning
Warning box text — rendered with gold highlight.
:::

> Disclaimer text — rendered italic navy, appears on cover.

![Figure 1](C:\path\to\figure.png)
```

- Numbered sub-headings: use `### 1. Title` format
- Roman numeral labels: use bold text `**I. Different cellular targets**` (not headings)

## Document Structure

1. **Cover** — YAML front matter (title, authors, date, disclaimer snippet)
2. **Introduction** — context, scope, clinician supervision warning
3. **Core content sections** — scientific/medical detail with sub-headings
4. **Figures** — treatment protocol diagrams (embed as images)
5. **Explanatory Notes / Q&A** — numbered clinical questions
6. **Safety considerations** — interactions, warnings, contraindications
7. **References** — numbered citation list
8. **Donation CTA** — "Help make resources like this possible." + donate link

## Style Guidelines

- Tone: medical/scientific, accessible but accurate
- Drug dosages inline (e.g., "0.2–0.4 mg/kg/day")
- **Bold** key terms, drug names, critical warnings
- Running footer: document title + date — auto-generated
- Preserve Greek (κ, β), em dashes (–), arrows (↔)
- Brand: navy `#1F3864`, gold `#C9A84C`, Lato typeface (IMA Brand Book v4.0)

## Pipelines

### Pipeline A — Markdown → HTML/PDF (primary)

| Step | Tool |
|------|------|
| Author content | `.md` source file (`input-template.md` as starter) |
| Generate HTML | `generate_html_md.py` |
| Generate PPTX | `generate_pptx.py` |
| Print to PDF | Chrome → Ctrl+P → Save as PDF |

Reference docs: `formatting-spec.md`, `markup-spec.md`, `input-template.md`, `test-input-cancer-resistance.md`

### Pipeline B — DOCX → Canva API (advanced)

For existing Word files needing import into Canva template via API.

| Step | Tool |
|------|------|
| Extract content | `extract_docx.py`, `extract_figures.py` |
| Map to Canva slots | `map_to_canva.py` |
| Push via API | Canva editing API |

Reference docs: `slot-map.md`, `template-slot-map.md`, `slot-types.md`, `docx-to-pdf-mapping.md`

## Scripts Reference

| Script | Pipeline | Purpose |
|--------|----------|---------|
| `generate_html_md.py` | A | Markdown → branded HTML (primary) |
| `generate_pptx.py` | A | Markdown → PowerPoint (16:9, IMA branded) |
| `generate_html.py` | B | Word docx → HTML (legacy, CSS source of truth) |
| `extract_docx.py` | B | Extract text/images from Word doc |
| `generate_pdf.py` | A | Direct PDF via reportlab (experimental) |
| `extract_figures.py` | B | Pull embedded images from Word doc in order |
| `render_table.py` | A/B | Render JSON table spec as styled PNG |
| `map_to_canva.py` | B | Map Word doc pages to Canva template slots |

## Reference Docs

| File | Pipeline | Covers | Read when |
|------|----------|--------|-----------|
| `formatting-spec.md` | A | CSS values, font sizes, colors, spacing for HTML | Debugging visual output or updating styles |
| `markup-spec.md` | A | Markdown conventions: front matter, `:::warning`, spacers, pagebreaks | Writing or troubleshooting a `.md` source file |
| `input-template.md` | A | Starter template for new guide `.md` file | Creating a new cancer care guide from scratch |
| `test-input-cancer-resistance.md` | A | Complete test input (cancer resistance topic) | Running end-to-end tests or verifying script output |
| `slot-map.md` / `template-slot-map.md` | B | Canva page slot names (p1–p64) and content types | Using `map_to_canva.py` or placing content in Canva |
| `slot-types.md` | B | Data types for each slot (text, image, list) | Validating slot payloads before Canva import |
| `docx-to-pdf-mapping.md` | B | How Word styles map to PDF/HTML equivalents | Working with legacy Word source files |

## Examples

- [Cancer Drug Resistance Guide](examples/cancer-drug-resistance-guide.md)
- [Repurposed Drugs Guide](examples/repurposed-drugs-cancer-guide.md)
