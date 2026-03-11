#!/usr/bin/env python3
"""
annotate_docx.py — IMA Cancer Care Guide slot annotator

Reads a Word doc and inserts {{SLOT_TYPE}} marker paragraphs before each
content block. The markers tell map_to_canva.py how to format content and
how to distribute it across Canva template pages.

Usage:
    python annotate_docx.py input.docx [output.docx]

Output:
    input-annotated.docx (or specified path)

Slot types produced:
    Cover:   COVER_TITLE_1, COVER_TITLE_2, COVER_SUBTITLE,
             COVER_AUTHORS, COVER_DATE, COVER_DISCLAIMER
    Intro:   INTRO_BODY, INTRO_WARNING
    Content: SECTION_HEADING, SUB_HEADING, BODY, BULLET
    Q&A:     QA_HEADING, QA_BODY
    Other:   FIGURE_CAPTION, REFERENCES, PAGE_BREAK
"""

import sys
import re
from pathlib import Path
from collections import Counter
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# ---------------------------------------------------------------------------
# Marker paragraph builder
# ---------------------------------------------------------------------------

def make_marker(slot_type):
    """Return an XML paragraph element styled as a grey monospace marker."""
    p = OxmlElement('w:p')
    r = OxmlElement('w:r')

    rPr = OxmlElement('w:rPr')
    for tag, attrs in [
        ('w:rFonts', {qn('w:ascii'): 'Courier New', qn('w:hAnsi'): 'Courier New'}),
        ('w:sz',     {qn('w:val'): '14'}),       # 7pt — small but readable
        ('w:color',  {qn('w:val'): '888888'}),   # mid-grey
        ('w:i',      {}),                          # italic
    ]:
        el = OxmlElement(tag)
        for k, v in attrs.items():
            el.set(k, v)
        rPr.append(el)

    # Zero-space paragraph margins
    pPr = OxmlElement('w:pPr')
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), '0')
    spacing.set(qn('w:after'),  '0')
    pPr.append(spacing)

    t = OxmlElement('w:t')
    t.text = f'{{{{{slot_type}}}}}'
    r.append(rPr)
    r.append(t)
    p.append(pPr)
    p.append(r)
    return p


# ---------------------------------------------------------------------------
# Paragraph analysis helpers
# ---------------------------------------------------------------------------

def text_of(para):
    return para.text.strip()


def is_bold(para):
    runs = [r for r in para.runs if r.text.strip()]
    return bool(runs) and all(r.bold for r in runs)


def style_name(para):
    return para.style.name if para.style else ''


def has_word_page_break(para):
    """True if paragraph contains an explicit (hard) page break only.
    Ignores w:lastRenderedPageBreak which is just Word's soft rendering hint."""
    xml = para._element.xml
    # Hard break: <w:br w:type="page"/> inside a run
    if 'w:type="page"' in xml:
        return True
    # Page break before style: <w:pageBreakBefore/> in paragraph properties
    if 'w:pageBreakBefore' in xml:
        return True
    return False


# ---------------------------------------------------------------------------
# State machine annotator
# ---------------------------------------------------------------------------

class Annotator:
    """
    Walks paragraphs in order, tracking document zones (cover / intro /
    content / qa / refs) and emitting slot type labels.
    """

    # Known section-level headings for Cancer Care guides.
    # These are top-level topics; everything else bold+short is a sub-heading.
    SECTION_HEADINGS = {
        'introduction',
        'biological basis of metabolic resistance',
        'key drivers of resistance under metabolic pressure',
        'why multi-agent metabolic regimens are double-edged',
        'why chronic, flat multi-agent regimens are risky',
        'role of press–pulse and adaptive therapy',
        'practical design strategies',
        'multi-agent protocol: adaptive resistance considerations',
        'practical modifications to reduce adaptive resistance',
        'example adaptive schedules',
        'explanatory notes',
        'references',
    }

    def __init__(self):
        self.zone = 'cover'       # cover | intro | content | qa | refs
        self.cover_titles = 0
        self.prev_slot = None

    def classify(self, para):
        """
        Return (slot_type, emit, new_zone) where:
          slot_type  — string label, or None to skip
          emit       — True  = insert marker before this paragraph
                       False = continuation (no new marker needed)
          new_zone   — zone to transition to, or None to keep current zone
        """
        text = text_of(para)
        if not text:
            return None, False, None

        bold  = is_bold(para)
        style = style_name(para)

        # ── Explicit page break ──────────────────────────────────────────
        if has_word_page_break(para):
            return 'PAGE_BREAK', True, None

        # ── COVER ZONE ───────────────────────────────────────────────────
        if self.zone == 'cover':
            # "Introduction" heading ends cover zone
            if re.match(r'^introduction$', text, re.I) and bold:
                return 'INTRO_BODY', True, 'intro'   # The Introduction heading itself

            # Disclaimer
            if re.search(r'complementary approach|not intended as a comprehensive', text, re.I):
                return 'COVER_DISCLAIMER', True, None

            # Authors (any line with medical credentials)
            if re.search(r'\b(MD|PhD|FCCP|FCCM|FACP|DO)\b', text):
                return 'COVER_AUTHORS', True, None

            # Date
            if re.match(r'Updated\s+\w+\s+\d{4}', text):
                return 'COVER_DATE', True, None

            # Bold short lines = title parts (first = COVER_TITLE_1, etc.)
            if bold and len(text) < 80:
                self.cover_titles += 1
                key = 'COVER_TITLE_1' if self.cover_titles == 1 else 'COVER_TITLE_2'
                return key, True, None

            # Everything else on cover = subtitle
            return 'COVER_SUBTITLE', True, None

        # ── INTRO ZONE ───────────────────────────────────────────────────
        if self.zone == 'intro':
            # Warning box sentinel
            if 'should not treat themselves' in text:
                return 'INTRO_WARNING', True, None

            # Any bold heading after intro/warning content exits to content zone
            if bold and len(text) < 100 and not text.endswith('?'):
                if self.prev_slot not in ('COVER_TITLE_1', 'COVER_TITLE_2',
                                          'COVER_SUBTITLE'):
                    return self._content_heading(text, bold, style), True, 'content'

            # Continuation of intro body — no new marker if previous was INTRO_BODY
            if self.prev_slot == 'INTRO_BODY':
                return None, False, None
            return 'INTRO_BODY', True, None

        # ── Q&A BODY continuation ─────────────────────────────────────────
        if self.zone == 'qa':
            if bold and text.endswith('?'):
                return 'QA_HEADING', True, None
            if self.prev_slot in ('QA_HEADING',):
                return 'QA_BODY', True, None
            if self.prev_slot == 'QA_BODY' and not (bold and len(text) < 100):
                return None, False, None   # continuation
            # Fall through to content classification below

        # ── REFERENCES ZONE ──────────────────────────────────────────────
        if self.zone == 'refs':
            # Continuation — all refs go into one block
            if self.prev_slot == 'REFERENCES':
                return None, False, None
            return 'REFERENCES', True, None

        # ── CONTENT ZONE ─────────────────────────────────────────────────

        # References heading transitions to refs zone
        if re.match(r'^references$', text, re.I) and bold:
            return 'REFERENCES', True, 'refs'   # heading + body share the slot

        # Figure captions
        if re.match(r'^Figure\s+\d+[\.\:]', text, re.I):
            return 'FIGURE_CAPTION', True, None

        # Q&A heading — bold question
        if bold and text.endswith('?'):
            return 'QA_HEADING', True, 'qa'

        # Q&A answer start
        if self.zone == 'qa' and re.match(r'^(YES|NO)[\.\,\:]?\s', text):
            return 'QA_BODY', True, None

        # Bullet / list paragraph
        if 'List' in style or re.match(r'^[•\-\*]\s', text):
            if self.prev_slot == 'BULLET':
                return None, False, None   # consecutive bullets share no new marker
            return 'BULLET', True, None

        return self._content_heading(text, bold, style), True, None

    def _content_heading(self, text, bold, style):
        """Distinguish SECTION_HEADING vs SUB_HEADING vs BODY."""
        if bold and len(text) < 120:
            # Check against known section headings (case-insensitive)
            if text.lower().rstrip('.') in self.SECTION_HEADINGS:
                return 'SECTION_HEADING'
            # Heading 1 style also = section
            if 'Heading 1' in style:
                return 'SECTION_HEADING'
            return 'SUB_HEADING'
        # Consecutive BODY paragraphs don't need repeated markers
        if self.prev_slot == 'BODY':
            return None   # caller checks for None
        return 'BODY'


# ---------------------------------------------------------------------------
# Main annotate function
# ---------------------------------------------------------------------------

def annotate(input_path: str, output_path: str):
    doc = Document(input_path)
    ann = Annotator()

    body = doc.element.body

    # First pass: collect (para_element, slot_type) for every paragraph
    # that needs a marker inserted before it.
    insertions = []   # list of (para._element, slot_type)

    for para in doc.paragraphs:
        slot_type, emit, new_zone = ann.classify(para)
        if new_zone is not None:
            ann.zone = new_zone
        if slot_type is not None:
            ann.prev_slot = slot_type
        if slot_type and emit:
            insertions.append((para._element, slot_type))

    # Second pass: insert markers in reverse order so earlier indices stay valid
    for para_elem, slot_type in reversed(insertions):
        children = list(body)
        idx = children.index(para_elem)
        body.insert(idx, make_marker(slot_type))

    doc.save(output_path)

    # Summary
    counts = Counter(s for _, s in insertions)
    total = len(insertions)
    print(f'Annotated: {total} markers inserted')
    print(f'Saved to:  {output_path}')
    print()
    print('Slot type counts:')
    for slot, n in sorted(counts.items()):
        print(f'  {slot:<20} {n}')


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    inp = Path(sys.argv[1])
    if not inp.exists():
        print(f'Error: file not found: {inp}')
        sys.exit(1)

    out = (
        Path(sys.argv[2])
        if len(sys.argv) >= 3
        else inp.with_stem(inp.stem + '-annotated')
    )

    annotate(str(inp), str(out))
