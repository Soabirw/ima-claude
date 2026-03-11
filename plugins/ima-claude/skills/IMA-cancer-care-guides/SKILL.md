---
name: IMA-cancer-care-guides
description: >
  Create IMA Health Cancer Care companion guides from Markdown source files.
  Outputs branded HTML (primary), PowerPoint, or PDF for Canva import.
  Use when: user asks to create a cancer care guide, resistance guide,
  repurposed drugs guide, or any standalone IMA cancer topic document.
  Triggers on: "cancer care guide", "cancer companion guide", "resistance guide",
  "repurposed drugs guide", "IMA cancer guide", "create cancer guide", "new cancer guide".
---

# IMA Cancer Care Guide Generator

Creates branded IMA Health cancer care companion guides from a Markdown source file.
One Markdown file → HTML, PDF, or PowerPoint — all consistently styled.

---

## Outputs

| Output | How | Use for |
|--------|-----|---------|
| **HTML** | `generate_html_md.py` | Browser preview, print to PDF |
| **PDF** | Chrome print → Save as PDF | Canva import, distribution |
| **PPTX** | `generate_pptx.py` | Presentations |

> **Canva tip:** Import the PDF (not PPTX) — Canva renders PDFs more faithfully.

---

## Quick Start

### 1. HTML from Markdown
```bash
/c/Python313/python.exe scripts/generate_html_md.py "path/to/guide.md" --out "output.html"
```

### 2. PowerPoint from Markdown
```bash
/c/Python313/python.exe scripts/generate_pptx.py "path/to/guide.md" --out "output.pptx"
```

### 3. PDF
Open the HTML in Chrome → Ctrl+P → Save as PDF
- Margins: **None**
- Enable **Background graphics**

---

## Markdown Format

Every guide is a `.md` file with YAML front matter for the cover, then content sections.

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
<!-- pagebreak -->          ← start a new page/slide
<!-- spacer -->             ← add vertical space (default 65pt)
<!-- spacer 30pt -->        ← add specific vertical space
```

### Content Markup
```markdown
## Section Heading         ← major section (navy, large)
### Sub-heading            ← sub-section (navy, medium)

Normal paragraph text here.

- Bullet point
- Another bullet

**Bold text** and *italic text* inline.

:::warning
Warning box text here — rendered with gold highlight.
:::

> Disclaimer text — rendered italic navy, appears on cover.

![Figure 1](C:\path\to\figure.png)   ← embedded image
```

### Numbered sub-headings
Use `### 1. Title` format — numbers render automatically styled.

### Roman numeral labels (I. II. III.)
Write as bold text, not headings:
```markdown
**I. Different cellular targets**
```

---

## Document Structure

All guides follow this pattern:

1. **Cover** — from YAML front matter (title, authors, date, disclaimer snippet)
2. **Introduction** — context, scope, clinician supervision warning
3. **Core content sections** — scientific/medical detail with sub-headings
4. **Figures** — treatment protocol diagrams (embed as images)
5. **Explanatory Notes / Q&A** — numbered clinical questions
6. **Safety considerations** — interactions, warnings, contraindications
7. **References** — numbered citation list
8. **Donation CTA** — "Help make resources like this possible." + donate link

---

## Style Guidelines

- **Tone**: Medical/scientific, accessible but accurate
- **Drug dosages**: Inline (e.g., "0.2–0.4 mg/kg/day")
- **Bold** key terms, drug names, and critical warnings
- **Running footer**: Document title + date — auto-generated on every page
- **Special characters**: Preserve Greek (κ, β), em dashes (–), arrows (↔)

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `generate_html_md.py` | Markdown → branded HTML (primary) |
| `generate_pptx.py` | Markdown → PowerPoint (16:9, IMA branded) |
| `generate_html.py` | Word docx → HTML (legacy, CSS source of truth) |
| `extract_docx.py` | Extract text/images from Word doc |
| `generate_pdf.py` | Direct PDF via reportlab (experimental) |

Python path: `/c/Python313/python.exe`

---

## Examples

- [Cancer Drug Resistance Guide](examples/cancer-drug-resistance-guide.md)
- [Repurposed Drugs Guide](examples/repurposed-drugs-cancer-guide.md)
