"""
Render a structured table as a PNG image in IMA Cancer Care style.

Style: navy header (#1F3864) with white bold text, white data rows with dark text,
thin navy cell borders, navy footer bar. Matches the DAGvyVwZJls table template.

Usage:
    python3 render_table.py <json_file> <output.png>

Or import and call render_table() directly:
    from render_table import render_table
    render_table(table_data, "output.png")

Table data format:
    {
        "title": "Glycolysis Suppression by EGCG",
        "headers": ["Pathway/Component", "Mechanism of Suppression by EGCG", "Degree of Suppression"],
        "rows": [
            ["Hexokinase 2 (HK2)", "Direct inhibition of HK2 enzyme activity...", "High"],
            ...
        ]
    }

Required: pip install Pillow
"""

import sys
import json
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# IMA Brand Colours
# ---------------------------------------------------------------------------
NAVY        = (31, 56, 100)       # #1F3864  — header bg + border + footer bar
WHITE       = (255, 255, 255)     # row backgrounds
ROW_ALT     = (248, 248, 252)     # very light blue-grey for alternating rows (optional)
TEXT_DARK   = (30, 30, 30)        # body text
TEXT_WHITE  = (255, 255, 255)     # header text
BORDER      = (31, 56, 100)       # cell borders (same as navy)

# ---------------------------------------------------------------------------
# Layout constants (pixels at 150 dpi → good for Canva)
# ---------------------------------------------------------------------------
PAGE_W      = 1400    # canvas width
MARGIN      = 40      # left/right page margin
TITLE_H     = 70      # height of the title area above the table
HEADER_H    = 64      # height of the header row
ROW_H_MIN   = 52      # minimum height per data row (grows with content)
FOOTER_H    = 24      # navy footer bar height
PAD_X       = 14      # horizontal cell padding
PAD_Y       = 10      # vertical cell padding
BORDER_W    = 1       # cell border width

# Font sizes
TITLE_SIZE  = 28
HEADER_SIZE = 18
BODY_SIZE   = 16

# ---------------------------------------------------------------------------
# Font loading — falls back gracefully
# ---------------------------------------------------------------------------

def _load_font(size, bold=False):
    """Load a system font, falling back to PIL default."""
    candidates_bold = [
        "C:/Windows/Fonts/calibrib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/verdanab.ttf",
    ]
    candidates_regular = [
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/verdana.ttf",
    ]
    candidates = candidates_bold if bold else candidates_regular
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    # PIL built-in default (no size control)
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Text wrapping
# ---------------------------------------------------------------------------

def _wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width pixels. Returns list of lines."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines if lines else [""]


def _text_block_height(lines, font, draw, line_spacing=4):
    """Calculate total height of a block of lines."""
    if not lines:
        return 0
    sample_bbox = draw.textbbox((0, 0), "Ag", font=font)
    line_h = sample_bbox[3] - sample_bbox[1]
    return len(lines) * (line_h + line_spacing)


# ---------------------------------------------------------------------------
# Column width calculation
# ---------------------------------------------------------------------------

def _calc_col_widths(headers, rows, body_font, header_font, draw, table_w):
    """
    Calculate column widths proportionally based on content.
    Minimum 80px per column. Total = table_w.
    """
    n = len(headers)
    # Score each column by max content length
    scores = []
    for i, h in enumerate(headers):
        max_len = len(h)
        for row in rows:
            if i < len(row):
                max_len = max(max_len, len(row[i]))
        scores.append(max(max_len, 8))

    total_score = sum(scores)
    min_w = 80
    available = table_w - n * min_w

    widths = []
    for s in scores:
        extra = int(available * s / total_score)
        widths.append(min_w + extra)

    # Adjust last column to fill exactly
    widths[-1] = table_w - sum(widths[:-1])
    return widths


# ---------------------------------------------------------------------------
# Core render function
# ---------------------------------------------------------------------------

def render_table(table_data: dict, output_path: str, alternate_rows: bool = False):
    """
    Render table_data as a PNG at output_path.

    Args:
        table_data: dict with keys "title", "headers", "rows"
        output_path: path to save the PNG
        alternate_rows: if True, alternate light-blue row backgrounds
    """
    title   = table_data.get("title", "")
    headers = table_data.get("headers", [])
    rows    = table_data.get("rows", [])

    if not headers:
        raise ValueError("Table data must have at least one header column.")

    # Fonts
    title_font   = _load_font(TITLE_SIZE, bold=True)
    header_font  = _load_font(HEADER_SIZE, bold=True)
    body_font    = _load_font(BODY_SIZE, bold=False)

    # Table dimensions
    table_w = PAGE_W - 2 * MARGIN

    # First pass: calculate layout on a dummy image to measure text
    dummy = Image.new("RGB", (PAGE_W, 100))
    dummy_draw = ImageDraw.Draw(dummy)

    col_widths = _calc_col_widths(headers, rows, body_font, header_font, dummy_draw, table_w)

    # Measure each row height based on wrapped content
    def row_height(row_texts, font):
        max_lines = 1
        for i, text in enumerate(row_texts):
            cw = col_widths[i] - 2 * PAD_X if i < len(col_widths) else 100
            lines = _wrap_text(str(text), font, cw, dummy_draw)
            max_lines = max(max_lines, len(lines))
        sample_bbox = dummy_draw.textbbox((0, 0), "Ag", font=font)
        line_h = sample_bbox[3] - sample_bbox[1]
        return max(ROW_H_MIN, max_lines * (line_h + 4) + 2 * PAD_Y)

    header_row_h = row_height(headers, header_font)
    header_row_h = max(header_row_h, HEADER_H)
    data_row_heights = [row_height(r, body_font) for r in rows]

    # Total canvas height
    total_h = (
        MARGIN
        + TITLE_H
        + header_row_h
        + sum(data_row_heights)
        + FOOTER_H
        + MARGIN
    )

    # Create final image
    img = Image.new("RGB", (PAGE_W, total_h), WHITE)
    draw = ImageDraw.Draw(img)

    # --- Title ---
    title_y = MARGIN + (TITLE_H - TITLE_SIZE) // 2
    # Centre the title
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_x = (PAGE_W - (title_bbox[2] - title_bbox[0])) // 2
    draw.text((title_x, title_y), title, fill=TEXT_DARK, font=title_font)

    # --- Table ---
    table_top = MARGIN + TITLE_H
    x0 = MARGIN

    # Draw header row
    y = table_top
    x = x0
    for i, header in enumerate(headers):
        cw = col_widths[i]
        # Navy background
        draw.rectangle([x, y, x + cw, y + header_row_h], fill=NAVY)
        # Cell border
        draw.rectangle([x, y, x + cw, y + header_row_h], outline=BORDER, width=BORDER_W)
        # Wrapped header text (white, bold, centred vertically)
        lines = _wrap_text(header, header_font, cw - 2 * PAD_X, draw)
        sample_bbox = draw.textbbox((0, 0), "Ag", font=header_font)
        line_h = sample_bbox[3] - sample_bbox[1]
        block_h = len(lines) * (line_h + 4)
        text_y = y + (header_row_h - block_h) // 2
        for line in lines:
            line_bbox = draw.textbbox((0, 0), line, font=header_font)
            line_w = line_bbox[2] - line_bbox[0]
            text_x = x + (cw - line_w) // 2
            draw.text((text_x, text_y), line, fill=TEXT_WHITE, font=header_font)
            text_y += line_h + 4
        x += cw

    y += header_row_h

    # Draw data rows
    for r_idx, row in enumerate(rows):
        rh = data_row_heights[r_idx]
        row_bg = ROW_ALT if (alternate_rows and r_idx % 2 == 1) else WHITE
        x = x0
        for i in range(len(col_widths)):
            cw = col_widths[i]
            cell_text = str(row[i]) if i < len(row) else ""
            # Background
            draw.rectangle([x, y, x + cw, y + rh], fill=row_bg)
            # Border
            draw.rectangle([x, y, x + cw, y + rh], outline=BORDER, width=BORDER_W)
            # Wrapped text (dark, centred vertically)
            lines = _wrap_text(cell_text, body_font, cw - 2 * PAD_X, draw)
            sample_bbox = draw.textbbox((0, 0), "Ag", font=body_font)
            line_h = sample_bbox[3] - sample_bbox[1]
            block_h = len(lines) * (line_h + 4)
            text_y = y + (rh - block_h) // 2
            for line in lines:
                # Centre text horizontally for narrow columns, left-align for wide
                line_bbox = draw.textbbox((0, 0), line, font=body_font)
                line_w = line_bbox[2] - line_bbox[0]
                if cw < 200:
                    text_x = x + (cw - line_w) // 2
                else:
                    text_x = x + PAD_X
                draw.text((text_x, text_y), line, fill=TEXT_DARK, font=body_font)
                text_y += line_h + 4
            x += cw
        y += rh

    # --- Navy footer bar ---
    draw.rectangle([x0, y, x0 + table_w, y + FOOTER_H], fill=NAVY)

    # Save
    img.save(output_path, "PNG", dpi=(150, 150))
    print(f"Saved: {output_path}  ({img.width}x{img.height}px)")
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    if len(sys.argv) < 3:
        print("Usage: python render_table.py <table_data.json> <output.png>")
        print()
        print("Or test with built-in sample:")
        print("  python render_table.py --test output.png")
        sys.exit(1)

    if sys.argv[1] == "--test":
        sample = {
            "title": "Glycolysis Suppression by EGCG",
            "headers": ["Pathway/\nComponent", "Mechanism of Suppression by EGCG", "Degree of Suppression"],
            "rows": [
                ["Hexokinase 2 (HK2)",
                 "Direct inhibition of HK2 enzyme activity and mRNA/protein expression; disrupts mitochondrial HK2 localization inducing apoptosis",
                 "High"],
                ["Lactate Production",
                 "Inhibits lactate dehydrogenase A (LDHA) activity and reduces extracellular accumulation",
                 "High"],
                ["Warburg Effect",
                 "Suppresses aerobic glycolysis in cancer cells and cancer-associated fibroblasts (CAFs) by targeting PFK, PK and LDHA",
                 "Moderate-High"],
                ["GLUT1 Transport",
                 "Competes with glucose for binding GLUT1, reducing cellular glucose uptake",
                 "Moderate"],
            ]
        }
        render_table(sample, sys.argv[2])
    else:
        with open(sys.argv[1], encoding="utf-8") as f:
            data = json.load(f)
        render_table(data, sys.argv[2])
