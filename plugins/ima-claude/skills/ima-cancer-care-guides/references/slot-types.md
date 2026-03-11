# Cancer Care Guide — Slot Types

The 87 text slots in the template collapse into **10 reusable types**.
Each type has consistent typography. When mapping a Word doc to the template,
match Word paragraph structures to these types — not to individual slots.

---

## Slot Type Taxonomy

| Type | Count | Word Doc Source | Example Slots |
|------|-------|-----------------|---------------|
| `section_heading` | 9 | All-bold short paragraph (< 80 chars) at section level | `p3_section_heading`, `p5_section_heading`, `p8_section_heading` |
| `sub_heading` | 24 | All-bold short paragraph nested under a section heading | `p3_sub1_heading`, `p5_sub1_heading`, `p11_sub1_heading` |
| `body` | 28 | Regular (non-bold) paragraphs — main content. Multiple Word paragraphs concatenated with `\n\n` | `intro_body`, `p3_sub1_body`, `p7_section1_body` |
| `footer` | 21 | Auto-generated. Title + date, same on every page. One `find_and_replace_text` updates all. | `intro_footer`, `p3_footer` ... `p22_footer` |
| `cover` | 6 | Title, subtitle, authors, disclaimer, date — each a distinct cover element | `cover_title_1`, `cover_subtitle`, `cover_authors` |
| `qa_heading` | 6 | Bold question text ending in `?` | `p17_q1_heading`, `p18_q3_heading`, `p20_q6_heading` |
| `qa_body` | 8 | Answer text starting with YES/NO, may span multiple pages | `p17_q1_body`, `p18_q3_body`, `p19_q5_body` |
| `fig_caption` | 4 | Lines starting with "Figure N." | `p15_fig1_caption`, `p16_fig3_caption` |
| `ref_list` | 1 | Numbered academic citations, single dense block | `p22_ref_list` |
| `warning` | 1 | Special callout box text | `intro_warning_text` |

**Not mapped from Word** (static/shared):
- `donation` (3 slots on page 23) — reused as-is from template
- `ref_heading` (1 slot) — just the word "References"
- Images and shapes — separate asset management

---

## Word Doc → Slot Type Mapping Rules

```
Word Paragraph                          →  Slot Type
─────────────────────────────────────────────────────────
First all-bold paragraph                →  cover.title
Author lines (with "MD" credentials)    →  cover.authors
"Updated [Month Year]"                  →  cover.date
Contains "complementary approach"       →  cover.disclaimer
"patients should not treat themselves"  →  warning

All-bold < 80 chars (top-level)         →  section_heading
All-bold < 80 chars (nested)            →  sub_heading
Regular body paragraphs                 →  body
"List Paragraph" style items            →  body (concatenated)

Bold text ending in "?"                 →  qa_heading
"YES./NO." + following paragraphs       →  qa_body

"Figure N." lines                       →  fig_caption
Numbered references after "References"  →  ref_list

Page footers                            →  footer (bulk update)
```

---

## How Content Flows Into Slots

A single Canva text slot often holds **multiple Word paragraphs**. The grouping rule:

> **Everything between two headings of the same or higher level becomes one body slot.**

Example from the Word doc:
```
** Biological Basis of Metabolic Resistance    ← section_heading
** Evolutionary dynamics under chronic pressure ← sub_heading
This scenario reflects acquired...              ← ┐
Under chronic low-to-moderate...                ←  ├─ body (one slot)
Under chronic exposure...                       ← ┘
** Metabolic plasticity as a central driver     ← sub_heading
This adaptive flexibility...                    ← body (one slot)
```

Each group is joined with `\n\n` and sent as a single `replace_text` call.

---

## Page Layout Patterns

The template reuses these page layouts:

### Pattern A: Section + Subsections (pages 3, 5, 8, 11, 12)
```
┌─────────────────────────────┐
│ section_heading              │
│                              │
│ sub_heading_1                │
│ body_1                       │
│                              │
│ sub_heading_2                │
│ body_2                       │
│                              │
│ footer                       │
└─────────────────────────────┘
```

### Pattern B: Subsection Continuation (pages 4, 6, 10, 14)
```
┌─────────────────────────────┐
│ sub_heading (continues from  │
│   previous page)             │
│ body                         │
│                              │
│ [optional: new section]      │
│                              │
│ footer                       │
└─────────────────────────────┘
```

### Pattern C: Q&A (pages 17-21)
```
┌─────────────────────────────┐
│ section_heading              │
│                              │
│ qa_heading_1                 │
│ qa_body_1                    │
│                              │
│ qa_heading_2                 │
│ qa_body_2                    │
│                              │
│ footer                       │
└─────────────────────────────┘
```

### Pattern D: Figures (pages 15-16)
```
┌─────────────────────────────┐
│ fig_caption_1                │
│ [IMAGE]                      │
│                              │
│ fig_caption_2                │
│ [IMAGE]                      │
│                              │
│ footer                       │
└─────────────────────────────┘
```

---

## Mapping Process

1. **Extract** Word doc → list of typed paragraphs (extract_docx.py)
2. **Group** consecutive body/list paragraphs under their nearest heading
3. **Match** each heading to a slot type based on the rules above
4. **Assign** each group to a specific slot by:
   - Same-structure guide: match heading text to slot map
   - New-topic guide: match by page position and slot type
5. **Generate** `replace_text` calls for each slot assignment
6. **Bulk update** footers with one `find_and_replace_text` call
