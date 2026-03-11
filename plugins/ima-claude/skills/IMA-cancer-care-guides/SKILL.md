---
name: IMA-cancer-care-guides
description: >
  Create IMA Health Cancer Care companion guides from Word docs (.docx).
  Outputs: branded HTML (primary), Canva design, or PDF.
  These are standalone topic-specific guides (e.g., drug resistance, repurposed drugs)
  that complement the main Cancer Care monograph. NOT for updating the monograph itself.
  Use when: user asks to create a new cancer care companion guide, resistance guide,
  repurposed drugs guide, or any standalone IMA cancer topic document.
  Triggers on: "cancer care guide", "cancer companion guide", "resistance guide",
  "repurposed drugs guide", "IMA cancer guide", "create cancer guide", "new cancer guide".
  Do NOT use for: updating the Cancer Care monograph itself (that will be a separate skill).
---

# Cancer Care Guides — IMA Brand Document Generator

Create IMA Health cancer care companion guides from Word docs. Primary output is branded HTML
that matches the Canva design template. Can also output via Canva API or PDF.

## Quick Start — HTML from Word Doc

```bash
/c/Python313/python.exe scripts/generate_html.py "<path_to.docx>" --out "<output.html>"
```

This runs the full pipeline: Word → extract_docx → generate_html → branded HTML with:
- IMA brand colors (gradient cover, navy headings, gold accents)
- Lato font throughout (Google Fonts CDN)
- Embedded images from the Word doc (base64)
- Print-ready CSS with `@page` rules

## Workflows

### Workflow A: Word → HTML (Primary)
1. User provides Word doc (.docx)
2. Run `generate_html.py` — extracts content + images, applies IMA brand CSS
3. Output: standalone HTML file, viewable in browser, print to PDF

### Workflow B: Word → Canva (Alternative)
1. User duplicates template design in Canva (File → Make a copy)
   - Template: Cancer Drug Resistance Guide (`DAHC5t-HGsk` / `DAHDZdIiuHk`)
   - Alternative: Repurposed Drugs Guide (`DAG1qttimy0`)
2. Update content via Canva editing API
3. Export as PDF, validate against Word doc using pdfplumber

### Workflow C: Word → PDF (Direct)
1. Run `generate_pdf.py` — uses reportlab with registered Lato TTF fonts
2. Requires Lato fonts in `fonts/` directory

## Important Limitations

### Do NOT use `generate-design` for layout-matching
The `generate-design` tool creates its own layouts and cannot replicate a specific design's
cover page or visual structure. Always use the template-copy approach instead.

### Do NOT trust `get-design-content` for text comparison
The Canva `get-design-content` API strips special characters during extraction:
- **Em dashes (–)** are removed, merging adjacent words
- **Greek letters (κ, β)** may be dropped
- **Symbols (↔, ™)** may be stripped
- **Numbers in ranges** may be truncated

Always use **PDF export + pdfplumber** for accurate text comparison.

### Font limitations
The `format_text` editing operation does NOT support changing font family — only size, weight,
color, alignment, and decoration. Font changes must be done manually in Canva.

## Input Template

See [input-template.md](references/input-template.md) for the blank template users fill in.
Users can also provide a Word doc — extract and map it to the template structure automatically.

## Required Inputs

Collect these before creating. Ask for any missing:

- **Title** and **subtitle**
- **Authors** with credentials (default: "Paul E. Marik, MD, FCCM, FCCP" and "Justus R. Hope, MD")
- **Date** (default: current date)
- **Topic content** — sections with headings and body text
- **Safety considerations** (if applicable)
- **References** (numbered academic citations)
- **Golden source Word doc** (.docx) for validation

## Document Structure Template

Follow this structure for all guides. Adapt sections to fit the content:

1. **Cover page**: Title, subtitle, author names/credentials, IMA branding, disclaimer snippet, "Updated [Month Year]"
2. **Disclaimer**: "This guide outlines our complementary approach... not intended as a comprehensive reference." Link to full guide at imahealth.org/research/cancer-care/
3. **Introduction**: Context, scope, clinician supervision warning: "Cancer is a complicated disease, and patient care should be supervised by an integrative clinician; patients should not treat themselves."
4. **Core content sections**: Scientific/medical detail with clear subheadings. Use running header on each page: "[Title] (MM/DD/YYYY)"
5. **Treatment protocols** (if applicable): Bulleted drug/supplement lists with dosages, prioritized by evidence strength
6. **Figures**: Treatment protocol diagrams, flowcharts — sourced from template design or uploaded
7. **Explanatory Notes / Q&A**: Numbered clinical questions with detailed answers
8. **Safety considerations**: Drug interactions, dosing guidance, contraindications, warnings
9. **References**: Numbered academic citation list (preserve exact formatting from Word doc)
10. **Donation CTA** (final page):
    - "Help make resources like this possible."
    - "Donate Today!" linking to https://geni.us/ima-donate
    - "We're 100% donor-supported. Your gift enables us to do this critical research and create these life-saving, FREE resources."
    - "IMA is a 501(c)(3) organization. Your gift is tax-deductible."

## Canva MCP Tool Usage

### Template designs (for duplication)
- Cancer Drug Resistance Guide: `DAHC5t-HGsk`
- Repurposed Drugs Guide: `DAG1qttimy0`
- IMA Brand Kit ID: `kAGcxiSCBf0`

### Editing the document
1. `start-editing-transaction` with the design ID
2. `perform-editing-operations` — use `find_and_replace_text` for content updates
3. Show preview thumbnails to user
4. `commit-editing-transaction` after user approval

### Exporting as PDF
```
export-design:
  design_id: [design ID]
  format:
    type: "pdf"
```

### Validating against Word doc
```python
# Extract PDF text (preserves special characters)
import pdfplumber
pdf = pdfplumber.open('exported.pdf')
pdf_text = '\n'.join([p.extract_text() for p in pdf.pages if p.extract_text()])

# Extract Word doc text
from docx import Document
doc = Document('golden_source.docx')
docx_text = '\n'.join([p.text.strip() for p in doc.paragraphs if p.text.strip()])

# Compare — check special chars, references, page ranges
```
Python path: `/c/Python313/python.exe` with `PYTHONIOENCODING=utf-8`

## Style Guidelines

- **Tone**: Medical/scientific, accessible but mechanistically accurate
- **Formatting**: Bold key terms and drug names. Use bulleted/numbered lists for protocols.
- **References**: Numbered inline citations (1-N) with full reference list at end
- **Drug dosages**: Include inline (e.g., "0.2-0.4 mg/kg/day")
- **Running header**: Document title with date on each page
- **Special characters**: Preserve Greek letters (κ, β), em dashes (–), arrows (↔), trademark (™)

## Example Documents

For structural reference, see:
- [Cancer Drug Resistance Guide](examples/cancer-drug-resistance-guide.md) — 23-page guide with scientific sections, Q&A format, figures
- [Repurposed Drugs Guide](examples/repurposed-drugs-cancer-guide.md) — 24-page guide with cancer-specific protocols, safety section, ranked tables
