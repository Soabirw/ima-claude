"""
Generate a styled IMA Cancer Care companion guide PDF directly from a Word doc.

Usage:
    /c/Python313/python.exe generate_pdf.py <path_to_docx> [--out <output.pdf>]

Python path: /c/Python313/python.exe
Required: pip install reportlab python-docx
"""

import sys
import io
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
        KeepTogether
    )
    from reportlab.platypus.flowables import Flowable
    from reportlab.pdfgen import canvas as pdfcanvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("ERROR: reportlab not installed. Run:")
    print("  /c/Python313/python.exe -m pip install reportlab")
    sys.exit(1)


# ── Register Lato fonts ──────────────────────────────────────────────────────
FONT_DIR = Path(__file__).parent.parent / "fonts"

def register_fonts():
    """Register Lato TTF fonts with reportlab."""
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
BODY_TEXT   = HexColor("#1A1A1A")
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
      fontName="Lato-Bold", fontSize=138, leading=145,
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
      fontName="Lato-Bold", fontSize=14, leading=18,
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
    title = authors = disclaimer = date_str = ""
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
            authors = text

        elif t == "disclaimer":
            disclaimer = text

        elif t == "date":
            date_str = text

        elif t == "body" and got_title:
            break

    if not authors:
        authors = "Paul E. Marik, MD, FCCM, FCCP  |  Justus R. Hope, MD"

    return title, authors, disclaimer, date_str


# ── Build story ───────────────────────────────────────────────────────────────
def build_story(data, styles, title_short, date_str):
    story = []
    footer_h = 0.4 * inch

    # ── Cover page (all on navy background) ──────────────────────────────
    title, authors, disclaimer, cover_date = extract_cover_meta(
        data["sections"]
    )

    # Split title into two lines for large cover text
    # e.g. "Cancer Resistance..." → line 1 "CANCER", line 2 "RESISTANCE"
    story.append(Spacer(1, 1.8 * inch))
    if title:
        words = title.upper().split()
        if len(words) >= 2:
            # First word large, rest as subtitle
            story.append(Paragraph(safe(words[0]), styles["cover_title_1"]))
            # Second line — could be one or two words
            line2 = " ".join(words[1:3]) if len(words) > 2 else words[1]
            story.append(Paragraph(safe(line2), styles["cover_title_2"]))
            # Remaining as subtitle if any
            if len(words) > 3:
                subtitle_text = " ".join(title.split()[3:])
                story.append(Spacer(1, 0.2 * inch))
                story.append(Paragraph(safe(subtitle_text), styles["cover_subtitle"]))
        else:
            story.append(Paragraph(safe(title.upper()), styles["cover_title_1"]))

    story.append(Spacer(1, 0.5 * inch))
    if authors:
        story.append(Paragraph(safe(authors), styles["cover_authors"]))
    if disclaimer:
        story.append(Spacer(1, 0.4 * inch))
        story.append(Paragraph(safe(disclaimer), styles["cover_disclaimer"]))
    if cover_date:
        story.append(Spacer(1, 0.15 * inch))
        story.append(Paragraph(safe(cover_date), styles["cover_date"]))

    # Switch to content template for all following pages
    story.append(NextPageTemplate("content"))
    story.append(PageBreak())

    # ── Content ──────────────────────────────────────────────────────────
    sections = data["sections"]
    heading_count = 0
    intro_added = False
    i = 0

    while i < len(sections):
        entry = sections[i]
        t = entry["type"]

        # Skip cover metadata we already used
        if t in ("h1", "date"):
            i += 1
            continue
        if t == "author":
            i += 1
            continue
        if t == "heading_bold":
            heading_count += 1
            if heading_count == 1:
                i += 1
                continue
            # Check if this is "Introduction"
            if not intro_added and entry["text"].strip().lower() == "introduction":
                story.append(Spacer(1, 0.15 * inch))
                story.append(Paragraph("Introduction", styles["intro_heading"]))
                story.append(Spacer(1, 0.05 * inch))
                intro_added = True
                i += 1
                continue
            story.append(Paragraph(para_markup(entry), styles["section_heading"]))
            i += 1
            continue

        if t in ("h2",):
            if not intro_added and entry["text"].strip().lower() == "introduction":
                story.append(Spacer(1, 0.15 * inch))
                story.append(Paragraph("Introduction", styles["intro_heading"]))
                story.append(Spacer(1, 0.05 * inch))
                intro_added = True
                i += 1
                continue
            story.append(Paragraph(para_markup(entry), styles["section_heading"]))
            i += 1
            continue

        if t in ("h3",):
            story.append(Paragraph(para_markup(entry), styles["sub_heading"]))
            i += 1
            continue

        if t == "ref_heading":
            story.append(PageBreak())
            story.append(Paragraph("References", styles["ref_heading"]))
            story.append(HRFlowable(width="100%", color=NAVY, thickness=1.5,
                                     spaceAfter=8))
            i += 1
            continue

        if t == "warning":
            story.append(Paragraph(warning_markup(entry["text"]), styles["warning"]))
            i += 1
            continue

        if t == "disclaimer":
            story.append(Paragraph(safe(entry["text"]), styles["cover_disclaimer"]))
            i += 1
            continue

        if t == "body":
            story.append(Paragraph(para_markup(entry), styles["body"]))
            i += 1
            continue

        if t == "bullet":
            items = []
            while i < len(sections) and sections[i]["type"] == "bullet":
                items.append(ListItem(
                    Paragraph(para_markup(sections[i]), styles["bullet"]),
                    bulletColor=NAVY, bulletFontSize=10, leftIndent=18
                ))
                i += 1
            story.append(ListFlowable(
                items, bulletType="bullet",
                bulletFontName="Lato", bulletFontSize=10,
                leftIndent=18, bulletOffsetY=-1,
                spaceBefore=4, spaceAfter=6,
            ))
            continue

        if t in ("figure_caption", "table_caption"):
            story.append(Paragraph(safe(entry["text"]), styles["caption"]))
            i += 1
            continue

        # Default
        story.append(Paragraph(para_markup(entry), styles["body"]))
        i += 1

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

    story = build_story(data, styles, title_short, date_str)

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
