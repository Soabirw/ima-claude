# Cancer Care Guide — Document Markup Specification

## Purpose

This spec defines how to annotate a source Word document so Claude can automatically
map its content into the Canva template's slots. The markup bridges the gap between
how authors write (flowing Word doc) and how Canva stores content (discrete text elements).

**End-to-end flow:**
```
Source Word doc (.docx)
    → Claude extracts text via python-docx
    → Claude matches content to slots using markup rules
    → Claude generates Canva editing API calls (replace_text / find_and_replace_text)
    → Canva template copy receives all content
    → Export as PDF, validate against Word doc
```

---

## Markup Format

### Approach: Inline Comment Markers in Word

Authors add **Word comments** (Review → New Comment) to mark slot boundaries.
Each comment contains a slot directive in this format:

```
@SLOT: slot_name
```

The comment is attached to the **first word or paragraph** of the content that belongs
to that slot. Everything from that marker until the next `@SLOT` marker (or end of
section) belongs to that slot.

### Why Word Comments?

- Non-destructive: doesn't change the visible document text
- Authors already know how to add comments in Word
- python-docx can read comments and their anchored positions
- The golden source remains clean for PDF comparison

---

## Alternative: Heading-Based Auto-Mapping (No Manual Markup)

For guides that follow the template structure closely, Claude can auto-map content
based on document structure without any manual markup:

### Auto-mapping Rules

| Document Feature | Maps To | Detection |
|-----------------|---------|-----------|
| First H1 or title | `cover_title_1` + `cover_title_2` | Split on line break or first major word |
| Subtitle line | `cover_subtitle` | Text immediately after title |
| Author block | `cover_authors` | Lines with "MD" or credential patterns |
| "Updated [Month Year]" | `cover_date` | Regex: `Updated\s+\w+\s+\d{4}` |
| Disclaimer paragraph | `cover_disclaimer` | Contains "complementary approach" or "not intended as a comprehensive" |
| "Introduction" heading | `intro_heading` | Exact or fuzzy match |
| Text under Introduction | `intro_body` | All paragraphs until next H2 |
| Warning box text | `intro_warning_text` | Contains "patients should not treat themselves" |
| H2 section headings | `pN_section_heading` | Match against slot map heading text |
| H3 subheadings | `pN_subN_heading` | Match against slot map subheading text |
| Body paragraphs | `pN_subN_body` or `pN_body` | Content between subheadings |
| "Q:" prefixed lines | `pN_qN_heading` | Regex: `^Q[:.]?\s` or bold question text |
| "A:" prefixed lines | `pN_qN_body` | Content following a Q heading |
| "YES." or "NO." starts | Part of Q&A body | First word of answer |
| "References" heading | `p22_ref_heading` | Exact match |
| Numbered reference list | `p22_ref_list` | Lines starting with `\d+\.` after References |
| "Figure N." captions | `pN_figN_caption` | Regex: `^Figure\s+\d+` |
| Footer pattern | All `pN_footer` slots | Bulk update via find_and_replace_text |

### Auto-mapping Algorithm

```
1. Extract all paragraphs from Word doc with style info (heading level, bold runs)
2. Build a "section tree" from heading hierarchy:
   - H1 → top-level sections
   - H2 → major sections (map to section_heading slots)
   - H3 → subsections (map to sub_heading slots)
   - Body → content between headings (map to body slots)
3. Match each section against the slot map using:
   a. Exact heading text match (primary)
   b. Fuzzy match with >80% similarity (fallback)
   c. Sequential position matching (last resort)
4. For Q&A sections, detect question/answer pairs by:
   - Bold text ending in "?" → question heading
   - Following paragraphs until next question → answer body
5. Concatenate multi-paragraph body content with \n\n separators
6. Generate slot assignments: { slot_name: content_text }
```

---

## Hybrid Approach (Recommended)

Use **auto-mapping as the default**, with **@SLOT comments for overrides** when:
- The guide structure differs from the template
- A slot boundary falls mid-paragraph
- Content needs to be split across slots differently than headings suggest
- New sections don't match any existing slot name

### Override Priority

1. Explicit `@SLOT` comment → always wins
2. Auto-mapped heading match → used when no comment exists
3. Positional fallback → last resort, flags for human review

---

## Slot Assignment Output Format

The mapping engine produces a JSON structure:

```json
{
  "metadata": {
    "source_file": "Cancer-Resistance-Guide-v3.docx",
    "template_id": "DAHC5t-HGsk",
    "mapped_at": "2026-03-08T12:00:00Z",
    "unmapped_slots": ["p15_fig1_image", "p23_background_image"],
    "unmapped_content": []
  },
  "slots": {
    "cover_title_1": {
      "element_id": "PBhMCnWGZWhcwN0p-LB5Dfy4LKBHLbvZ2",
      "content": "cancer",
      "method": "replace_text"
    },
    "cover_title_2": {
      "element_id": "PBhMCnWGZWhcwN0p-LBBB35r43HBY5VV8",
      "content": "Resistance",
      "method": "replace_text"
    },
    "intro_body": {
      "element_id": "PBhzHx5FDf3N5L3x-LBWrc7qLRWTCtN7w",
      "content": "\nCaution to the reader: This is a complex...",
      "method": "replace_text"
    }
  },
  "footer": {
    "old_text": "Cancer-Resistance and Interventions to Mitigate Resistance  (03/04/2026)",
    "new_text": "New Guide Title  (MM/DD/YYYY)",
    "method": "find_and_replace_text",
    "note": "Applied to all footer slots at once"
  },
  "images": {
    "p15_fig1_image": {
      "element_id": "PBG1T8SmdnbBZfly-LB6gbPcZLWhr6QWH",
      "action": "update_fill",
      "asset_id": null,
      "note": "Requires manual upload or asset URL"
    }
  }
}
```

---

## Content Transformation Rules

When mapping Word doc content to Canva slots, apply these transformations:

### Text Handling
1. **Preserve line breaks**: `\n` within a slot = line break in Canva element
2. **Paragraph breaks**: `\n\n` = paragraph separation within a single text element
3. **Bold text**: Canva preserves formatting structure when using `replace_text` —
   the template's existing bold/regular pattern is maintained. For new bold spans,
   use `format_text` after `replace_text`.
4. **Reference citations**: Keep inline as `(1-3)` or `(24)` — these are plain text

### Special Characters (preserve exactly)
- Em dashes: `–` (not `--`)
- Greek letters: `κ`, `β`
- Arrows: `↔`
- Trademark: `™`
- Smart quotes: `"..."` and `'...'`

### Slot-Specific Rules
- **Footer slots**: All 21 footers (pages 2-22) share identical text. Use one
  `find_and_replace_text` call to update all at once.
- **Cover title split**: The cover has separate elements for line 1 (`cover_title_1`)
  and line 2 (`cover_title_2`). Split the main title at the natural break.
- **Q&A format**: Question goes in heading slot, "YES./NO." + explanation goes in body slot.
- **Multi-page content**: Some answers span multiple pages (e.g., Q5 spans pages 19-20).
  Each page's portion goes in its own slot (`p19_q5_body`, `p20_q5_cont`).

---

## Canva API Call Generation

The mapping engine converts the slot assignments into Canva MCP tool calls:

### Step 1: Start Transaction
```
start-editing-transaction(design_id=<copy_id>)
```

### Step 2: Perform Operations

For each text slot, generate a `replace_text` operation:
```json
{
  "type": "replace_text",
  "element_id": "<from slot map>",
  "text": "<mapped content>"
}
```

For footer bulk update:
```json
{
  "type": "find_and_replace_text",
  "find": "<old footer text>",
  "replace": "<new footer text>"
}
```

For images:
```json
{
  "type": "update_fill",
  "element_id": "<from slot map>",
  "asset_id": "<uploaded asset ID>"
}
```

### Step 3: Batch Operations
Group operations into batches (Canva may have limits per call).
Process text replacements first, then images.

### Step 4: Preview & Commit
Show page thumbnails to user for approval, then commit.

---

## Validation Checklist

After generating the Canva guide, validate:

- [ ] All text slots populated (no template placeholder text remaining)
- [ ] Footer text updated on all pages
- [ ] Cover page: title, subtitle, authors, date all correct
- [ ] Special characters preserved (export PDF, check with pdfplumber)
- [ ] Reference numbers sequential and complete
- [ ] Figure captions match figure content
- [ ] Q&A answers start with YES/NO as appropriate
- [ ] Disclaimer text present and links to imahealth.org/research/cancer-care/
- [ ] Donation CTA on final page with correct URL

---

## Usage Examples

### Example 1: Same-structure guide (resistance guide → new resistance guide update)
```
User: "Here's the updated Cancer Resistance guide Word doc. Create the Canva version."
Claude:
1. Extract text from .docx via python-docx
2. Auto-map using heading matching (same structure)
3. Generate slot assignments
4. User duplicates template in Canva
5. Claude runs editing API calls
6. Export PDF, validate against Word doc
7. Fix any differences
```

### Example 2: New-topic guide (different structure)
```
User: "Create a new Cancer Immunotherapy guide from this Word doc."
Claude:
1. Extract text from .docx
2. Auto-map what matches (cover, intro, disclaimer, references, donation CTA)
3. Flag unmatched sections — ask user to add @SLOT comments or assign manually
4. May need to add/remove pages via merge-designs
5. Generate slot assignments for matched content
6. Run editing API calls
7. Validate
```
