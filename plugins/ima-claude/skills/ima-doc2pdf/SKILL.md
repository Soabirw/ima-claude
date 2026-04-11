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

Extracts content from Word documents, generates branded IMA PDF (Lato, navy/gold, IMA layout). Outputs content pages only — cover handled by `ima-cover-creator` and merged via pypdf.

## Quick Start

```bash
# Install (once)
pip install python-docx reportlab Pillow pypdf --break-system-packages

# Generate content PDF
python3 scripts/generate_pdf.py path/to/document.docx --out content.pdf
```

## Merge with Cover

```python
from pypdf import PdfReader, PdfWriter

cover = PdfReader("cover.pdf")
content = PdfReader("content.pdf")

writer = PdfWriter()
writer.add_page(cover.pages[0])

# Skip first 2 pages (ReportLab placeholder cover + overflow)
for page in content.pages[2:]:
    writer.add_page(page)

with open("final.pdf", "wb") as f:
    writer.write(f)
```

## Pipeline

```
DOCX → extract_docx.py → generate_pdf.py → content.pdf
                                                +
                                           cover.pdf (ima-cover-creator)
                                                ↓ pypdf merge
                                           final.pdf → Canva import
```

## Typography Spec

Font: Lato (Google Fonts). Values confirmed from Canva design data.

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

## Content Extraction

`extract_docx.py` classifies each paragraph into typed blocks. Each block includes `runs` with per-run bold/italic flags.

| Type | Description |
|------|-------------|
| `h1` | Top-level heading |
| `h2` | Section heading |
| `h3` | Sub-heading |
| `heading_bold` | All-bold paragraph |
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
| `figure_caption` | Caption |
| `page_break` | Hard page break |

## Image Handling

1. Read all image relationships from DOCX package
2. Map paragraph indices to embedded image positions
3. Write images to temp files
4. Insert ReportLab `Image` flowables at correct positions
5. Scale to fit `page_width - 2 × margin`

## Cover Page Behavior

ReportLab generates placeholder cover as pages 1-2. Skip them during merge. To verify:

```python
from pypdf import PdfReader
r = PdfReader("content.pdf")
for i in range(min(3, len(r.pages))):
    print(f"Page {i}: {r.pages[i].extract_text()[:100]}")
```

First content page typically starts with "Introduction" or section heading.

## Scripts

| Script | Purpose |
|--------|---------|
| `generate_pdf.py` | DOCX → branded PDF via ReportLab |
| `extract_docx.py` | Extracts structured content from Word documents |
| `docx_utils.py` | Shared DOCX parsing utilities |

## Fonts

Lato TTF auto-downloaded from Google Fonts on first run into `fonts/` (git-ignored). Family (Regular, Bold, Italic, BoldItalic) registered with ReportLab. Download skipped if fonts present.

## Customization

```python
# Footer text (in generate_pdf.py)
title_short = (title[:60] + "...") if len(title) > 60 else title
footer_text = f"{title_short} ({clean_date})"
```

To add paragraph types: add classifier rule in `extract_docx.py`, handler in `block_to_flowables()`, and `ParagraphStyle` in `build_styles()`.

## Related Skills

| Skill | Role |
|-------|------|
| **ima-cover-creator** | Branded cover page (PPTX → PDF) |
| **ima-cancer-care-guides** | Full pipeline with Markdown source and Canva API |
| **ima-brand** | Source of truth for colors, typography, voice |
