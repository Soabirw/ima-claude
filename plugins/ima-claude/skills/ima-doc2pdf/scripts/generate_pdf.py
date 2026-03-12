"""
Generate a styled IMA branded document PDF directly from a Word doc.

Usage:
    python3 generate_pdf.py <path_to_docx> [--out <output.pdf>]

Required: pip install reportlab python-docx
"""

import sys
import io
import re
import base64
import tempfile
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from extract_docx import extract_document

try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.platypus import (
        BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
        ListFlowable, ListItem, HRFlowable, PageBreak, NextPageTemplate,
        KeepTogether, Image
    )
    from reportlab.platypus.flowables import Flowable
    from reportlab.pdfgen import canvas as pdfcanvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("ERROR: reportlab not installed. Run:")
    print("  pip install reportlab")
    sys.exit(1)


# ── Register Lato fonts ──────────────────────────────────────────────────────
FONT_DIR = Path(__file__).parent.parent / "fonts"
LATO_FONTS = ("Lato-Regular.ttf", "Lato-Bold.ttf", "Lato-Italic.ttf", "Lato-BoldItalic.ttf")
LATO_BASE_URL = "https://github.com/google/fonts/raw/main/ofl/lato/"


def ensure_fonts():
    """Download Lato fonts from Google Fonts GitHub repo if any are missing."""
    if FONT_DIR.exists() and all((FONT_DIR / f).exists() for f in LATO_FONTS):
        return

    print("Downloading Lato fonts...")
    FONT_DIR.mkdir(parents=True, exist_ok=True)

    for font_file in LATO_FONTS:
        dest = FONT_DIR / font_file
        if dest.exists():
            continue
        url = LATO_BASE_URL + font_file
        urllib.request.urlretrieve(url, dest)
        print(f"  {font_file}")


def register_fonts():
    """Register Lato TTF fonts with reportlab."""
    ensure_fonts()
    fonts = {
        "Lato":            "Lato-Regular.ttf",
        "Lato-Bold":       "Lato-Bold.ttf",
        "Lato-Italic":     "Lato-Italic.ttf",
        "Lato-BoldItalic": "Lato-BoldItalic.ttf",
    }
    for name, filename in fonts.items():
        path = FONT_DIR / filename
        if path.exists():
            pdfmetrics.registerFont(TTFont(name, str(path)))
        else:
            print(f"WARNING: Font not found: {path}")

    # Register font family so <b> and <i> markup works in Paragraphs
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    registerFontFamily(
        "Lato",
        normal="Lato",
        bold="Lato-Bold",
        italic="Lato-Italic",
        boldItalic="Lato-BoldItalic",
    )


# ── Brand colours (IMA Brand Book v4.0) ──────────────────────────────────────
NAVY        = HexColor("#00066F")   # Trustworthy Indigo
GOLD        = HexColor("#FFCC00")   # Vital Gold
BODY_TEXT   = HexColor("#000000")
GREY_LIGHT  = HexColor("#CCCCCC")
GREY_TEXT   = HexColor("#666666")

PAGE_W, PAGE_H = LETTER   # 612 × 792 pt
MARGIN = 0.5 * inch


# ── Styles (confirmed from Canva) ────────────────────────────────────────────
def build_styles():
    S = {}

    def s(name, **kw):
        S[name] = ParagraphStyle(name=name, **kw)

    # ── Cover ────────────────────────────────────────────────────────────
    s("cover_title_1",
      fontName="Lato-Bold", fontSize=90.5, leading=95,
      textColor=white, alignment=TA_CENTER, spaceAfter=8)

    s("cover_title_2",
      fontName="Lato-Bold", fontSize=67, leading=72,
      textColor=white, alignment=TA_CENTER, spaceAfter=8)

    s("cover_subtitle",
      fontName="Lato-Bold", fontSize=24, leading=30,
      textColor=white, alignment=TA_CENTER, spaceAfter=6)

    s("cover_authors",
      fontName="Lato", fontSize=20, leading=26,
      textColor=white, alignment=TA_CENTER, spaceAfter=4)

    s("cover_disclaimer",
      fontName="Lato", fontSize=12, leading=16,
      textColor=white, alignment=TA_CENTER, spaceAfter=3)

    s("cover_date",
      fontName="Lato-Italic", fontSize=12, leading=16,
      textColor=white, alignment=TA_CENTER)

    # ── Content headings ─────────────────────────────────────────────────
    s("intro_heading",
      fontName="Lato-Bold", fontSize=15, leading=20,
      textColor=NAVY, alignment=TA_CENTER,
      spaceBefore=6, spaceAfter=10)

    s("section_heading",
      fontName="Lato-Bold", fontSize=15, leading=20,
      textColor=NAVY, spaceBefore=16, spaceAfter=5)

    s("sub_heading",
      fontName="Lato-Bold", fontSize=13, leading=17,
      textColor=NAVY, spaceBefore=10, spaceAfter=3)

    # ── Body text ────────────────────────────────────────────────────────
    s("body",
      fontName="Lato", fontSize=12, leading=14.5,
      textColor=BODY_TEXT, spaceBefore=0, spaceAfter=6,
      alignment=TA_JUSTIFY)

    s("bullet",
      fontName="Lato", fontSize=12, leading=14.5,
      textColor=BODY_TEXT, spaceBefore=1, spaceAfter=1)

    # ── Warning box — navy bg, white + Vital Gold text ───────────────────
    s("warning",
      fontName="Lato-Bold", fontSize=12, leading=16,
      textColor=white, alignment=TA_CENTER,
      backColor=NAVY, borderColor=NAVY,
      borderWidth=0, borderPad=10,
      spaceBefore=10, spaceAfter=10)

    # ── Q&A ──────────────────────────────────────────────────────────────
    s("qa_question",
      fontName="Lato-Bold", fontSize=12, leading=16,
      textColor=NAVY, spaceBefore=10, spaceAfter=2)

    s("qa_answer",
      fontName="Lato", fontSize=12, leading=14.5,
      textColor=BODY_TEXT, spaceBefore=2, spaceAfter=4,
      alignment=TA_JUSTIFY)

    # ── References ───────────────────────────────────────────────────────
    s("ref_heading",
      fontName="Lato-Bold", fontSize=13, leading=17,
      textColor=NAVY, spaceBefore=10, spaceAfter=8)

    s("reference",
      fontName="Lato", fontSize=8, leading=11,
      textColor=HexColor("#333333"), spaceBefore=1, spaceAfter=1,
      leftIndent=14, firstLineIndent=-14)

    # ── Captions ─────────────────────────────────────────────────────────
    s("caption",
      fontName="Lato", fontSize=12, leading=14.5,
      textColor=BODY_TEXT, spaceBefore=4, spaceAfter=4)

    s("disclaimer",
      fontName="Lato", fontSize=12, leading=16,
      textColor=white, alignment=TA_CENTER,
      spaceBefore=4, spaceAfter=4)

    s("content_disclaimer",
      fontName="Lato", fontSize=12, leading=16,
      textColor=BODY_TEXT, alignment=TA_JUSTIFY,
      spaceBefore=4, spaceAfter=6)

    # ── Footer ───────────────────────────────────────────────────────────
    s("footer",
      fontName="Lato", fontSize=10, leading=12,
      textColor=GREY_TEXT, alignment=TA_CENTER)

    return S


# ── Page canvas callbacks ─────────────────────────────────────────────────────
def make_cover_canvas(footer_h):
    def on_cover(canv, doc):
        canv.saveState()
        # Full navy background
        canv.setFillColor(NAVY)
        canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        canv.restoreState()
    return on_cover


def make_content_canvas(title_short, date_str, footer_h):
    if date_str:
        clean_date = date_str.replace("Updated ", "").strip()
        footer_text = f"{title_short} ({clean_date})"
    else:
        footer_text = title_short

    def on_content(canv, doc):
        canv.saveState()
        # Bottom footer rule
        canv.setStrokeColor(GREY_LIGHT)
        canv.setLineWidth(0.5)
        canv.line(MARGIN, footer_h + 8, PAGE_W - MARGIN, footer_h + 8)
        # Single centered footer line — Lato 10pt
        canv.setFont("Lato", 10)
        canv.setFillColor(GREY_TEXT)
        canv.drawCentredString(PAGE_W / 2, footer_h - 2, footer_text)
        canv.restoreState()
    return on_content


# ── Markup helpers ────────────────────────────────────────────────────────────
def safe(text):
    return (text.replace("&", "&amp;")
               .replace("<", "&lt;")
               .replace(">", "&gt;"))


def runs_to_markup(runs):
    if not runs:
        return ""
    out = []
    for r in runs:
        t = safe(r.get("text", ""))
        if r.get("bold") and r.get("italic"):
            out.append(f"<b><i>{t}</i></b>")
        elif r.get("bold"):
            out.append(f"<b>{t}</b>")
        elif r.get("italic"):
            out.append(f"<i>{t}</i>")
        else:
            out.append(t)
    return "".join(out)


def para_markup(entry):
    markup = runs_to_markup(entry.get("runs", []))
    return markup if markup else safe(entry["text"])


def warning_markup(text):
    """Format warning text with Vital Gold for emphasis portions."""
    # The warning box has white text with gold emphasis
    # For now, render all as white; gold portions need manual Word markup
    return safe(text)


# ── Extract cover metadata ────────────────────────────────────────────────────
def extract_cover_meta(sections):
    """
    Pull title, authors, disclaimer, date from the document preamble.
    Only the FIRST heading is the guide title — stop taking headings after that
    so section headings like 'Introduction' don't bleed onto the cover.
    """
    title = disclaimer = date_str = ""
    author_list = []
    got_title = False

    for entry in sections[:30]:
        t = entry["type"]
        text = entry["text"].strip()

        if t in ("h1", "heading_bold"):
            if not got_title:
                title = text
                got_title = True
            else:
                break

        elif t == "author":
            author_list.append(text)

        elif t == "disclaimer":
            disclaimer = text

        elif t == "date":
            date_str = text

        elif t == "body" and got_title:
            break

    authors = "<br/>".join(safe(a) for a in author_list) if author_list else ""

    return title, authors, disclaimer, date_str


# ── Image extraction ─────────────────────────────────────────────────────────
def extract_images_from_docx(docx_path):
    """Extract embedded images from DOCX, return dict of paragraph_index -> temp file path."""
    from docx import Document
    from docx.oxml.ns import qn
    
    doc = Document(docx_path)
    images = {}  # rId -> (blob, content_type)
    for rel in doc.part.rels.values():
        if 'image' in rel.reltype:
            images[rel.rId] = (rel.target_part.blob, rel.target_part.content_type)
    
    # Find which paragraphs have images
    positions = {}  # para_index -> [(rId, blob, content_type)]
    for i, para in enumerate(doc.paragraphs):
        for run in para.runs:
            drawings = run._element.findall(qn('w:drawing'))
            for d in drawings:
                blips = d.findall('.//' + qn('a:blip'))
                for blip in blips:
                    embed = blip.get(qn('r:embed'))
                    if embed and embed in images:
                        blob, ct = images[embed]
                        positions.setdefault(i, []).append((embed, blob, ct))
    
    # Write to temp files and return para_index -> [filepath]
    result = {}
    for para_idx, items in positions.items():
        paths = []
        for rId, blob, ct in items:
            ext = '.png' if 'png' in ct else '.jpg'
            tf = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
            tf.write(blob)
            tf.close()
            paths.append(tf.name)
        result[para_idx] = paths
    
    return result


# ── Build story helpers ───────────────────────────────────────────────────────
def group_consecutive_bullets(sections):
    """Merge consecutive bullet entries into grouped blocks.

    Returns a new list where runs of {'type': 'bullet'} entries are replaced
    by a single {'type': 'bullet_group', 'items': [...]} dict.
    """
    result = []
    i = 0
    while i < len(sections):
        if sections[i]["type"] == "bullet":
            group = []
            while i < len(sections) and sections[i]["type"] == "bullet":
                group.append(sections[i])
                i += 1
            result.append({"type": "bullet_group", "items": group})
        else:
            result.append(sections[i])
            i += 1
    return result


def block_to_flowables(block, styles, intro_added, heading_count):
    """Map a single block dict to a list of ReportLab flowables.

    Returns (flowables, intro_added, heading_count) — the bool state is
    threaded through so this stays a pure transformation.
    """
    t = block["type"]

    if t in ("h1", "date", "author"):
        return [], intro_added, heading_count

    if t == "heading_bold":
        heading_count += 1
        if heading_count == 1:
            return [], intro_added, heading_count
        if not intro_added and block["text"].strip().lower() == "introduction":
            return (
                [Spacer(1, 0.15 * inch),
                 Paragraph("Introduction", styles["intro_heading"]),
                 Spacer(1, 0.05 * inch)],
                True,
                heading_count,
            )
        return [Paragraph(para_markup(block), styles["section_heading"])], intro_added, heading_count

    if t == "h2":
        if not intro_added and block["text"].strip().lower() == "introduction":
            return (
                [Spacer(1, 0.15 * inch),
                 Paragraph("Introduction", styles["intro_heading"]),
                 Spacer(1, 0.05 * inch)],
                True,
                heading_count,
            )
        return [Paragraph(para_markup(block), styles["section_heading"])], intro_added, heading_count

    if t == "h3":
        return [Paragraph(para_markup(block), styles["sub_heading"])], intro_added, heading_count

    if t == "ref_heading":
        return (
            [PageBreak(),
             Paragraph("References", styles["ref_heading"]),
             HRFlowable(width="100%", color=NAVY, thickness=1.5, spaceAfter=8)],
            intro_added,
            heading_count,
        )

    if t == "warning":
        return [Paragraph(warning_markup(block["text"]), styles["warning"])], intro_added, heading_count

    if t == "disclaimer":
        return [Paragraph(safe(block["text"]), styles["content_disclaimer"])], intro_added, heading_count

    if t == "body":
        return [Paragraph(para_markup(block), styles["body"])], intro_added, heading_count

    if t == "bullet_group":
        items = [
            ListItem(
                Paragraph(para_markup(entry), styles["bullet"]),
                bulletColor=NAVY, bulletFontSize=10, leftIndent=18,
            )
            for entry in block["items"]
        ]
        return (
            [ListFlowable(
                items, bulletType="bullet",
                bulletFontName="Lato", bulletFontSize=10,
                leftIndent=18, bulletOffsetY=-1,
                spaceBefore=4, spaceAfter=6,
            )],
            intro_added,
            heading_count,
        )

    if t in ("figure_caption", "table_caption"):
        return [Paragraph(safe(block["text"]), styles["caption"])], intro_added, heading_count

    # Default
    return [Paragraph(para_markup(block), styles["body"])], intro_added, heading_count


# ── Build story ───────────────────────────────────────────────────────────────
def build_story(data, styles, title_short, date_str, image_positions=None):
    story = []
    footer_h = 0.4 * inch
    if image_positions is None:
        image_positions = {}

    # ── Cover page (all on navy background) ──────────────────────────────
    title, authors, disclaimer, cover_date = extract_cover_meta(
        data["sections"]
    )

    story.append(Spacer(1, 1.2 * inch))
    if title:
        # Split title visually: first half as hero text, second half as subtitle.
        # This is a placeholder cover — ima-cover-creator replaces it for final output.
        words = title.split()
        mid = max(1, len(words) // 2)
        line1 = " ".join(words[:mid]).upper()
        line2 = " ".join(words[mid:]).upper() if len(words) > mid else ""

        story.append(Paragraph(safe(line1), styles["cover_title_1"]))
        if line2:
            story.append(Spacer(1, 0.2 * inch))
            story.append(Paragraph(safe(line2), styles["cover_title_2"]))

    story.append(Spacer(1, 0.5 * inch))
    if authors:
        story.append(Paragraph(authors, styles["cover_authors"]))
    if disclaimer:
        story.append(Spacer(1, 0.4 * inch))
        story.append(Paragraph(safe(disclaimer), styles["cover_disclaimer"]))
    if cover_date:
        story.append(Spacer(1, 0.15 * inch))
        story.append(Paragraph(safe(cover_date), styles["cover_date"]))

    story.append(NextPageTemplate("content"))
    story.append(PageBreak())

    # ── Content — pipeline: group bullets → map blocks → flatten ─────────
    grouped = group_consecutive_bullets(data["sections"])
    intro_added = False
    heading_count = 0
    rendered_images = set()
    
    # Build a lookup of section index -> paragraph index for image placement
    for block in grouped:
        flowables, intro_added, heading_count = block_to_flowables(
            block, styles, intro_added, heading_count
        )
        story.extend(flowables)
        
        # Insert images at this paragraph position
        para_idx = block.get("index", -1)
        if para_idx in image_positions and para_idx not in rendered_images:
            max_w = PAGE_W - 2 * MARGIN - 0.5 * inch
            for img_path in image_positions[para_idx]:
                try:
                    img = Image(img_path, width=max_w, height=None)
                    # Let reportlab scale proportionally
                    img._restrictSize(max_w, PAGE_H - 3 * inch)
                    story.append(Spacer(1, 6))
                    story.append(img)
                    story.append(Spacer(1, 6))
                except Exception as e:
                    print(f"  Warning: Could not embed image at para {para_idx}: {e}")
            rendered_images.add(para_idx)
        
        # Also check for images between consecutive section indices
        if block.get("type") == "bullet_group":
            for item in block.get("items", []):
                item_idx = item.get("index", -1)
                if item_idx in image_positions and item_idx not in rendered_images:
                    max_w = PAGE_W - 2 * MARGIN - 0.5 * inch
                    for img_path in image_positions[item_idx]:
                        try:
                            img = Image(img_path, width=max_w, height=None)
                            img._restrictSize(max_w, PAGE_H - 3 * inch)
                            story.append(Spacer(1, 6))
                            story.append(img)
                            story.append(Spacer(1, 6))
                        except Exception as e:
                            print(f"  Warning: Could not embed image: {e}")
                    rendered_images.add(item_idx)
    
    # Insert any remaining images not yet rendered (e.g. image-only paragraphs)
    for para_idx, paths in image_positions.items():
        if para_idx not in rendered_images:
            max_w = PAGE_W - 2 * MARGIN - 0.5 * inch
            for img_path in paths:
                try:
                    img = Image(img_path, width=max_w, height=None)
                    img._restrictSize(max_w, PAGE_H - 3 * inch)
                    story.append(Spacer(1, 6))
                    story.append(img)
                    story.append(Spacer(1, 6))
                except Exception as e:
                    print(f"  Warning: Could not embed orphan image: {e}")
            rendered_images.add(para_idx)

    # ── Q&A ───────────────────────────────────────────────────────────────
    if data.get("qa_pairs"):
        story.append(Spacer(1, 0.1 * inch))
        story.append(HRFlowable(width="100%", color=GREY_LIGHT,
                                 thickness=0.5, spaceAfter=8))
        for qa in data["qa_pairs"]:
            block = [Paragraph(para_markup(qa["question"]), styles["qa_question"])]
            for ans in qa["answer_parts"]:
                block.append(Paragraph(para_markup(ans), styles["qa_answer"]))
            story.append(KeepTogether(block))

    # ── References ────────────────────────────────────────────────────────
    if data.get("references"):
        story.append(PageBreak())
        story.append(Paragraph("References", styles["ref_heading"]))
        story.append(HRFlowable(width="100%", color=NAVY, thickness=1.5,
                                 spaceAfter=8))
        for ref in data["references"]:
            story.append(Paragraph(safe(ref["text"]), styles["reference"]))

    return story


# ── Main ──────────────────────────────────────────────────────────────────────
def generate_pdf(docx_path, out_path):
    print(f"Extracting: {docx_path}")
    data = extract_document(docx_path)
    
    # Extract images from DOCX
    print("Extracting images...")
    image_positions = extract_images_from_docx(docx_path)
    print(f"  Found images at {len(image_positions)} paragraph positions")

    register_fonts()
    styles = build_styles()

    title, authors, disclaimer, date_str = extract_cover_meta(
        data["sections"]
    )
    title_short = (title[:60] + "...") if len(title) > 60 else title

    footer_h = 0.4 * inch

    doc = BaseDocTemplate(
        str(out_path),
        pagesize=LETTER,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )

    cover_frame = Frame(
        MARGIN, footer_h + 0.3 * inch,
        PAGE_W - 2 * MARGIN,
        PAGE_H - 2 * MARGIN - footer_h,
        id="cover_frame"
    )
    content_frame = Frame(
        MARGIN, footer_h + 0.4 * inch,
        PAGE_W - 2 * MARGIN,
        PAGE_H - 2 * MARGIN - footer_h,
        id="content_frame"
    )

    doc.addPageTemplates([
        PageTemplate(
            id="cover",
            frames=[cover_frame],
            onPage=make_cover_canvas(footer_h)
        ),
        PageTemplate(
            id="content",
            frames=[content_frame],
            onPage=make_content_canvas(title_short, date_str, footer_h)
        ),
    ])

    story = build_story(data, styles, title_short, date_str, image_positions)

    print(f"Building PDF...")
    doc.build(story)
    print(f"Done → {out_path}")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    if len(sys.argv) < 2:
        print("Usage: python generate_pdf.py <path_to_docx> [--out output.pdf]")
        sys.exit(1)

    docx_path = Path(sys.argv[1])
    if not docx_path.exists():
        print(f"Error: File not found: {docx_path}")
        sys.exit(1)

    if "--out" in sys.argv:
        out_path = Path(sys.argv[sys.argv.index("--out") + 1])
    else:
        out_path = docx_path.with_suffix(".pdf")

    generate_pdf(docx_path, out_path)
