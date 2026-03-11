"""
Generate a styled IMA Cancer Care companion guide as HTML from a Markdown file.

Styling matches the Canva "Cancer Drug Resistance Guide March 2026" design.
Reuses the same CSS and cover layout as the docx-based generator.

Usage:
    /c/Python313/python.exe generate_html_md.py <path_to_md> [--out <output.html>]

Python path: /c/Python313/python.exe

Markdown conventions:
    ---                          YAML front matter (title1, title2, subtitle, authors, date)
    > blockquote                 Disclaimer text
    :::warning ... :::           Warning box
    <!-- pagebreak -->           Page break
    ## Heading                   Section heading (h2)
    ### Heading                  Sub-heading (h3)
    - bullet                    Bullet list item
    **bold line**               Bold body text (all-bold paragraph)
    *italic caption*            Figure caption (when followed by ![...])
    ![alt](path)                Figure image (local files are base64-embedded)
    1. text / N.<tab>text       Numbered reference (in References section)
"""

import sys
import io
import re
import base64
from pathlib import Path


# ── Reuse CSS from the docx generator ─────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
from generate_html import CSS, load_cover_asset, safe


def parse_front_matter(lines):
    """Extract YAML front matter from --- delimited block."""
    meta = {}
    if not lines or lines[0].strip() != '---':
        return meta, lines

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end = i
            break
    if end is None:
        return meta, lines

    for line in lines[1:end]:
        if ':' in line:
            key, _, val = line.partition(':')
            meta[key.strip()] = val.strip()

    return meta, lines[end + 1:]


def inline_format(text):
    """Apply inline Markdown formatting (bold, italic) to text."""
    t = safe(text)
    # Bold+italic: ***text*** or ___text___
    t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', t)
    # Bold: **text**
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    # Italic: *text*  (but not inside words like OXPHOS-*)
    t = re.sub(r'(?<!\w)\*([^*]+?)\*(?!\w)', r'<em>\1</em>', t)
    return t


def encode_image(path_str):
    """Read a local image file and return a base64 data URI."""
    p = Path(path_str)
    if not p.exists():
        return path_str  # Return original path if file not found
    suffix = p.suffix.lower()
    mime_map = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.webp': 'image/webp',
    }
    mime = mime_map.get(suffix, 'image/png')
    b64 = base64.b64encode(p.read_bytes()).decode('ascii')
    return f"data:{mime};base64,{b64}"


def parse_markdown(lines):
    """Parse Markdown lines into structured blocks."""
    blocks = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Empty line
        if not stripped:
            i += 1
            continue

        # Page break
        if stripped == '<!-- pagebreak -->':
            blocks.append({'type': 'pagebreak'})
            i += 1
            continue

        # Spacer: <!-- spacer --> or <!-- spacer 120pt -->
        spacer_match = re.match(r'^<!-- spacer(?:\s+(\d+)pt)? -->', stripped)
        if spacer_match:
            amount = spacer_match.group(1)
            blocks.append({'type': 'spacer', 'amount': f"{amount}pt" if amount else "65pt"})
            i += 1
            continue

        # Warning box
        if stripped == ':::warning':
            warning_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() != ':::':
                warning_lines.append(lines[i].strip())
                i += 1
            if i < len(lines):
                i += 1  # skip closing :::
            blocks.append({'type': 'warning', 'text': ' '.join(warning_lines)})
            continue

        # Blockquote (disclaimer)
        if stripped.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            blocks.append({'type': 'disclaimer', 'text': ' '.join(quote_lines)})
            continue

        # H2
        if stripped.startswith('## ') and not stripped.startswith('### '):
            blocks.append({'type': 'h2', 'text': stripped[3:]})
            i += 1
            continue

        # H3
        if stripped.startswith('### '):
            blocks.append({'type': 'h3', 'text': stripped[4:]})
            i += 1
            continue

        # Image: ![alt](path)
        img_match = re.match(r'^!\[([^\]]*)\]\((.+?)\)\s*$', stripped)
        if img_match:
            blocks.append({
                'type': 'image',
                'alt': img_match.group(1),
                'path': img_match.group(2),
            })
            i += 1
            continue

        # Bullet list item
        if stripped.startswith('- '):
            blocks.append({'type': 'bullet', 'text': stripped[2:]})
            i += 1
            continue

        # Figure caption: *italic text* as standalone line (before an image)
        if (re.match(r'^\*[^*]+\*$', stripped) and
                i + 1 < len(lines) and re.match(r'^!\[', lines[i + 1].strip())):
            blocks.append({'type': 'figure_caption', 'text': stripped[1:-1]})
            i += 1
            continue

        # All-bold standalone paragraph: **text**
        if stripped.startswith('**') and stripped.endswith('**') and stripped.count('**') == 2:
            inner = stripped[2:-2]
            blocks.append({'type': 'bold_para', 'text': inner})
            i += 1
            continue

        # Numbered reference (in references section): starts with N. or N.<tab>
        # We'll detect these contextually later

        # Regular paragraph (may span multiple lines until blank line)
        para_lines = [stripped]
        i += 1
        while i < len(lines):
            next_stripped = lines[i].strip()
            # Stop at blank line, heading, list item, pagebreak, image, warning, blockquote
            if (not next_stripped or
                    next_stripped.startswith('#') or
                    next_stripped.startswith('- ') or
                    next_stripped.startswith('> ') or
                    next_stripped == '<!-- pagebreak -->' or
                    next_stripped.startswith(':::') or
                    re.match(r'^!\[', next_stripped) or
                    (re.match(r'^\*[^*]+\*$', next_stripped) and
                     i + 1 < len(lines) and re.match(r'^!\[', lines[i + 1].strip()))):
                break
            para_lines.append(next_stripped)
            i += 1
        blocks.append({'type': 'body', 'text': ' '.join(para_lines)})
        continue

    return blocks


def generate_html_from_md(md_path, out_path):
    print(f"Reading: {md_path}")
    text = Path(md_path).read_text(encoding='utf-8')
    all_lines = text.split('\n')

    # Parse front matter
    meta, content_lines = parse_front_matter(all_lines)
    title1 = meta.get('title1', 'Cancer')
    title2 = meta.get('title2', 'Resistance')
    subtitle = meta.get('subtitle', '')
    authors_str = meta.get('authors', 'Paul E. Marik, MD, FCCM, FCCP | Justus R. Hope, MD')
    date_str = meta.get('date', '')

    title_parts = [title1, title2]

    # Parse markdown content
    blocks = parse_markdown(content_lines)

    # ── Build HTML ─────────────────────────────────────────────────────────────
    html = []
    html.append("<!DOCTYPE html>")
    html.append('<html lang="en">')
    html.append("<head>")
    html.append('<meta charset="UTF-8">')
    html.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html.append(f"<title>{safe(' '.join(title_parts))}</title>")
    html.append(f"<style>{CSS}</style>")
    html.append("</head>")
    html.append("<body>")

    # ── Cover ──────────────────────────────────────────────────────────────────
    logo_b64 = load_cover_asset("logo_b64.txt")
    thumb_b64 = load_cover_asset("thumb_b64.txt")

    html.append('<div class="page cover-page"><div class="cover">')

    if logo_b64:
        html.append(f'<div class="cover-logo"><img src="{logo_b64}" alt="Independent Medical Alliance"></div>')

    html.append(f'<div class="cover-title-1-wrap"><div class="cover-title-1" data-text="{safe(title1)}">{safe(title1)}</div></div>')
    html.append('<div class="cover-hero"></div>')
    html.append(f'<div class="cover-title-2">{safe(title2)}</div>')

    if subtitle:
        html.append(f'<div class="cover-subtitle">{safe(subtitle)}</div>')

    author_list = [a.strip() for a in authors_str.split('|') if a.strip()]
    html.append('<div class="cover-authors">')
    html.append("<br>".join(safe(a) for a in author_list))
    html.append('</div>')

    if thumb_b64:
        html.append(f'<img class="cover-info" src="{thumb_b64}" alt="Cancer Care Guide">')

    # Disclaimer on cover — find it from blocks
    disclaimer_text = ""
    for b in blocks:
        if b['type'] == 'disclaimer':
            disclaimer_text = b['text']
            break

    if disclaimer_text:
        html.append(f'<div class="cover-info-text">{safe(disclaimer_text)}</div>')

    if date_str:
        html.append(f'<div class="cover-date">{safe(date_str)}</div>')

    html.append("</div></div>")  # close cover + cover-page

    # ── Content pages ──────────────────────────────────────────────────────────
    html.append('<div class="page">')

    in_list = False
    in_references = False
    skip_disclaimer = True  # skip first disclaimer (already on cover)
    skip_warning = True     # skip first warning (already on cover)
    page_has_content = False  # track whether current page has any content

    def close_list():
        nonlocal in_list
        if in_list:
            html.append("</ul>")
            in_list = False

    def next_block_is_bullet(idx):
        return idx + 1 < len(blocks) and blocks[idx + 1]['type'] == 'bullet'

    for bi, block in enumerate(blocks):
        btype = block['type']
        text = block.get('text', '')

        # Close list if not a bullet
        if btype != 'bullet' and in_list:
            close_list()

        # Disclaimer — first one goes on cover, skip it
        if btype == 'disclaimer':
            if skip_disclaimer:
                skip_disclaimer = False
                continue
            html.append(f'<div class="disclaimer">{inline_format(text)}</div>')
            page_has_content = True
            continue

        # Page break — skip if current page is empty (avoids blank pages)
        if btype == 'pagebreak':
            close_list()
            if page_has_content:
                html.append('</div><div class="page">')
            page_has_content = False
            continue

        # Spacer — vertical whitespace
        if btype == 'spacer':
            html.append(f'<div style="height:{block["amount"]}"></div>')
            continue

        # ── All remaining block types emit visible content ──────────────────────
        page_has_content = True

        # Warning box
        if btype == 'warning':
            if skip_warning:
                skip_warning = False
                continue
            warning_html = safe(text)
            warning_html = re.sub(
                r'(patients should not treat themselves)',
                r'<span class="gold">\1</span>',
                warning_html,
                flags=re.IGNORECASE
            )
            html.append(f'<div class="warning-box">{warning_html}</div>')
            continue

        # H2
        if btype == 'h2':
            close_list()
            in_references = (text.strip() == 'References')
            if in_references:
                html.append(f'<div class="ref-heading">{safe(text)}</div>')
            else:
                html.append(f"<h2>{inline_format(text)}</h2>")
            continue

        # H3
        if btype == 'h3':
            close_list()
            # Roman numeral sub-labels → bold body, not heading
            if re.match(r'^[IVX]+[\.\s]', text):
                classes = ["roman-label"]
                if next_block_is_bullet(bi):
                    classes.append("lead-in")
                html.append(f'<p class="{" ".join(classes)}"><strong>{safe(text)}</strong></p>')
            else:
                html.append(f"<h3>{inline_format(text)}</h3>")
            continue

        # Bold paragraph (all-bold line)
        if btype == 'bold_para':
            # Roman numeral sub-labels
            if re.match(r'^[IVX]+[\.\s]', text):
                classes = ["roman-label"]
                if next_block_is_bullet(bi):
                    classes.append("lead-in")
                html.append(f'<p class="{" ".join(classes)}"><strong>{safe(text)}</strong></p>')
            else:
                li = ' class="lead-in"' if next_block_is_bullet(bi) else ""
                html.append(f"<p{li}><strong>{inline_format(text)}</strong></p>")
            continue

        # Figure caption
        if btype == 'figure_caption':
            html.append(f'<div class="figure-caption"><em>{safe(text)}</em></div>')
            continue

        # Image
        if btype == 'image':
            src = encode_image(block['path'])
            html.append('<div class="figure">')
            html.append(f'<img src="{src}" alt="{safe(block["alt"])}">')
            html.append('</div>')
            continue

        # Bullet
        if btype == 'bullet':
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{inline_format(text)}</li>")
            continue

        # Body text
        if btype == 'body':
            if in_references:
                # Reference entries
                html.append(f'<div class="reference">{safe(text)}</div>')
            else:
                # Check for YES/NO answer starts
                m = re.match(r'^(YES|NO)\.?\s*', text)
                if m and m.group(1) in ('YES', 'NO'):
                    prefix = m.group(0).rstrip()
                    rest = text[m.end():]
                    html.append(f"<p><strong>{safe(prefix)}</strong> {inline_format(rest)}</p>")
                else:
                    li = ' class="lead-in"' if next_block_is_bullet(bi) else ""
                    html.append(f"<p{li}>{inline_format(text)}</p>")
            continue

    close_list()
    html.append("</div>")  # close last page
    html.append("</body>")
    html.append("</html>")

    # ── Inject footer ──────────────────────────────────────────────────────────
    footer_title = "-".join(title_parts)
    if subtitle:
        footer_title += " " + subtitle
    clean_date = date_str.strip()
    if not clean_date:
        clean_date = "03/04/2026"
    footer_html = (
        f'<div class="page-footer">'
        f'<span class="footer-title">{safe(footer_title)}</span>'
        f' <span class="footer-date">({safe(clean_date)})</span>'
        f'</div>'
    )

    output = "\n".join(html)
    output = output.replace(
        '</div><div class="page">',
        f'{footer_html}</div><div class="page">'
    )
    output = output.replace(
        '</div>\n</body>',
        f'{footer_html}</div>\n</body>'
    )

    with open(str(out_path), "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Done → {out_path}")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    if len(sys.argv) < 2:
        print("Usage: python generate_html_md.py <path_to_md> [--out output.html]")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"Error: File not found: {md_path}")
        sys.exit(1)

    if "--out" in sys.argv:
        out_path = Path(sys.argv[sys.argv.index("--out") + 1])
    else:
        out_path = md_path.with_suffix(".html")

    generate_html_from_md(md_path, out_path)
