---
name: ima-doc2pdf
description: >-
  Convert DOCX content into branded IMA PDF documents using ReportLab with Lato
  typography, navy headings, justified body text, running footers, and embedded
  images. Produces branded PDF documents with content pages. Generates a placeholder
  cover that can be replaced by ima-cover-creator for production output. Use when: converting a Word doc to branded PDF,
  creating PDF content pages for Canva import, generating an IMA branded document PDF,
  or when the user says "convert this docx to PDF," "branded PDF," "content pages,"
  "PDF for Canva," or "doc to PDF." Also triggers on: "make a PDF from this Word
  file," "export to PDF," "generate branded PDF," "IMA branded document PDF."
  Always load ima-brand alongside for color/typography authority.
---

# IMA DOCX → Branded PDF

Extracts content from any Word document and generates a branded IMA PDF with
Lato typography, navy/gold colors, and IMA layout standards. Works with guides,
reports, white papers, and other IMA documents. Outputs content pages only
(no cover page) — the cover is handled by `ima-cover-creator` and merged via pypdf.

---

## Why ReportLab for Content

Content pages are pure document flow: headings, body paragraphs, bullet lists,
inline bold/italic, embedded images, and running footers. ReportLab handles all of
this with proper Lato font registration, automatic page breaks, and precise
typographic control. No coordinate math needed — the flow engine does the work.

---

## Quick Start

### 1. Install dependencies (once)

```bash
pip install python-docx reportlab Pillow pypdf --break-system-packages
```

### 2. Generate content PDF

```bash
python3 scripts/generate_pdf.py path/to/document.docx --out content.pdf
```

### 3. Merge with cover (from ima-cover-creator)

```python
from pypdf import PdfReader, PdfWriter

cover = PdfReader("cover.pdf")
content = PdfReader("content.pdf")

writer = PdfWriter()
writer.add_page(cover.pages[0])

# Skip the first 2 pages (ReportLab's placeholder cover + overflow)
for page in content.pages[2:]:
    writer.add_page(page)

with open("final.pdf", "wb") as f:
    writer.write(f)
```

---

## Pipeline

```
DOCX
  ↓  extract_docx.py (text, structure, metadata)
  ↓  generate_pdf.py (ReportLab → branded PDF)
  ↓
content.pdf (N pages, no cover)
  +
cover.pdf (from ima-cover-creator)
  ↓  pypdf merge
  ↓
final.pdf → Canva import
```

---

## Typography Spec (Canva-confirmed)

All values confirmed from Canva design data. Font: Lato (Google Fonts).

### Headings

| Element | Size | Weight | Color | Align |
|---------|------|--------|-------|-------|
| Section heading (h2) | 15pt | Bold | #00066F | Center |
| Sub-heading (h3) | 13pt | Bold | #00066F | Left |
| Intro heading | 15pt | Bold | #00066F | Center |

### Body Text

| Element | Size | Weight | Color | Align |
|---------|------|--------|-------|-------|
| Body paragraph | 12pt | Regular | #000000 | Justify |
| Body bold inline | 12pt | Bold | #000000 | Justify |
| Body bold navy | 12pt | Bold | #00066F | Justify |
| Bullet item | 12pt | Regular | #000000 | Left |
| Bullet marker | — | — | #00066F | — |

### Other Elements

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Footer | 10pt | Regular | #666666 |
| Reference entry | 8pt | Regular | #333333 |
| Reference heading | 13pt | Bold | #00066F |
| Q&A question | 12pt | Bold | #00066F |
| Q&A answer | 12pt | Regular | #000000 |
| Warning box | 12pt | Bold | #FFFFFF on #00066F bg |

### Page Setup

| Property | Value |
|----------|-------|
| Page size | US Letter (8.5 × 11 in) |
| Margins | 0.5 in all sides |
| Body width | 7.5 in |
| Footer height | 0.4 in from bottom |

---

## Content Extraction

The `extract_docx.py` script classifies each Word paragraph into typed blocks:

| Type | Description |
|------|-------------|
| `h1` | Top-level heading (title) |
| `h2` | Section heading |
| `h3` | Sub-heading |
| `heading_bold` | All-bold paragraph (inline heading) |
| `body` | Regular paragraph |
| `bullet` | List item |
| `author` | Author name |
| `date` | Date string |
| `disclaimer` | Disclaimer text |
| `warning` | Warning box content |
| `question` | Q&A question |
| `answer_start` | Q&A answer (YES/NO prefix) |
| `reference` | Numbered citation |
| `ref_heading` | "References" heading |
| `figure_caption` | Figure/table caption |
| `page_break` | Hard page break |

Each block includes `runs` with per-run bold/italic flags for inline formatting.

---

## Image Handling

The script extracts embedded DOCX images via `python-docx`:

1. Reads all image relationships from the DOCX package
2. Maps paragraph indices to embedded image positions
3. Writes images to temp files
4. Inserts ReportLab `Image` flowables at the correct positions
5. Scales to fit within `page_width - 2 × margin`

Images that appear between text paragraphs (image-only paragraphs) are also caught
and appended after all text content.

---

## Cover Page Behavior

The ReportLab script generates a **placeholder cover** (navy background with title
text) as pages 1-2 of its output. This exists so the script works standalone, but
when pairing with `ima-cover-creator`, **skip the first 2 pages** during merge.

To check which pages to skip:
```python
from pypdf import PdfReader
r = PdfReader("content.pdf")
for i in range(min(3, len(r.pages))):
    text = r.pages[i].extract_text()[:100]
    print(f"Page {i}: {text}")
```

The first content page typically starts with "Introduction" or a section heading.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `generate_pdf.py` | Main: DOCX → branded PDF via ReportLab |
| `extract_docx.py` | Extracts structured content from Word documents |
| `docx_utils.py` | Shared utilities for DOCX parsing |

---

## Fonts

Lato TTF files are auto-downloaded from Google Fonts on first run into the `fonts/`
directory (which is git-ignored). The font family (Regular, Bold, Italic, BoldItalic)
is registered with ReportLab so that `<b>` and `<i>` markup works in Paragraph objects.

If the fonts are already present, the download is skipped.

---

## Customization

### Adjusting the footer

The footer shows the document title and date. To customize:
```python
# In generate_pdf.py, the footer text is built from:
title_short = (title[:60] + "...") if len(title) > 60 else title
footer_text = f"{title_short} ({clean_date})"
```

### Adding new paragraph types

1. Add a classifier rule in `extract_docx.py`
2. Add a handler in `block_to_flowables()` in `generate_pdf.py`
3. Create a ReportLab `ParagraphStyle` in `build_styles()`

---

## Relationship to Other Skills

| Skill | Role |
|-------|------|
| **ima-cover-creator** | Generates branded cover page (PPTX → PDF) |
| **ima-cancer-care-guides** | Full pipeline including Markdown source and Canva API mapping |
| **ima-brand** | Source of truth for colors, typography, voice |

**Typical workflow:**
```
ima-cover-creator  →  cover.pdf (1 page)
ima-doc2pdf        →  content.pdf (skip first 2 pages)
pypdf merge        →  final.pdf → Canva import
```
