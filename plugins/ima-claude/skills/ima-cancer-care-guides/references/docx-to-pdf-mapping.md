# Word → PDF Style Mapping

How to format the Word doc so `extract_docx.py` reliably classifies each paragraph for PDF generation.

## Recommended Word Styles

| What you want in the PDF | How to format in Word | Detection method | PDF style |
|---|---|---|---|
| **Cover title** | `Heading 1` or `Title` style | Word style name | Lato 90.5/138pt Bold white, ALL CAPS |
| **Section heading** | `Heading 2` style | Word `Heading 2` | Lato 15pt Bold #00066F |
| **Sub heading** | `Heading 3` style | Word `Heading 3` | Lato 14pt Bold #00066F |
| **Body text** | `Normal` / `Body` style | Default fallback | Lato 12pt Regular #1A1A1A, justified |
| **Bullet list** | `List Bullet` style or Word bullet/number list | Word list style or numPr XML | Lato 12pt, solid dot (•), 18pt indent |
| **Warning box** | Paragraph containing "patients should not treat themselves" | Keyword match | Lato 12pt Bold, white on #00066F bg |
| **Disclaimer** | Paragraph containing "complementary approach" or "not intended as a comprehensive" | Keyword match | Lato 12pt white, centered |
| **Authors** | Paragraph containing "M.D." + "Marik" or "Hope" (under 100 chars) | Keyword match | Lato 20pt Regular white |
| **Date** | Text starting with "Updated Month DD, YYYY" | Regex match | Lato 12pt Italic white |
| **Q&A question** | Starts with "Q:" or "Q." or first run bold + contains "?" | Regex/bold check | Lato 12pt Bold #00066F |
| **Q&A answer** | Starts with "YES" or "NO" | Regex match | Lato 12pt Regular, justified |
| **Table caption** | Starts with "Table N" | Regex match | Lato 12pt Regular |
| **Figure caption** | Starts with "Figure N" | Regex match | Lato 12pt Regular |
| **References heading** | Paragraph text is exactly "References" | Exact match | Lato 13pt Bold #00066F + navy rule |
| **Reference entry** | Starts with "N. " (number-dot-space) after "References" heading | Regex, only in refs section | Lato 8pt Regular #333333, hanging indent |

## Best Practices for Word Doc Authors

1. **Use `Heading 1`** for the guide title only (one per document)
2. **Use `Heading 2`** for all section headings — this is the most reliable detection
3. **Use `Heading 3`** for sub-headings under sections
4. **Use `Normal`** for body text — bold/italic runs within Normal are preserved
5. **Use `List Bullet`** for bullet points — or use Word's built-in bullet formatting
6. **Don't bold entire Normal paragraphs** — short all-bold Normal text gets misclassified as a heading

## Fallback Detection (Less Reliable)

These work but are fragile — prefer Word heading styles instead:

| Pattern | Detected as | Risk |
|---|---|---|
| Short all-bold `Normal` paragraph (< 120 chars) | `heading_bold` → section heading | Any short bold paragraph triggers this |
| First all-bold paragraph in document | Cover title | Only works if it's truly first |
| Numbered paragraph after "References" | Reference entry | Numbered lists before References section also match |

## Inline Formatting (Always Preserved)

Within any paragraph, these run-level formats carry through to PDF:

- **Bold runs** → `<b>` markup in PDF
- **Italic runs** → `<i>` markup in PDF
- **Bold+Italic runs** → `<b><i>` markup in PDF
