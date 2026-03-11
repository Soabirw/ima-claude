"""
Map Word doc pages to Canva template slots via page-break-based mapping.

Architecture: The Word doc uses explicit page breaks to define Canva page boundaries.
Each page in the Word doc maps 1:1 to a page in the Canva design.

Usage:
    /c/Python313/python.exe map_to_canva.py <path_to_docx> [--dry-run] [--json]

Pipeline:
  1. Split Word doc by explicit page breaks → list of pages
  2. Page 1 → cover slots (p1): title_1, title_2, subtitle, authors, disclaimer, date
  3. Page 2 → intro slots (p2): heading, body, warning, running_header
  4. Pages 3..N-1 → [CONTENT] + [RUNNING_HEADER] on p3..pN-1
       - Bold formatting applied to heading paragraphs via format_text
       - List level applied to bullet paragraphs via format_text
  5. Last page (if References) → next content slot as references page
  6. Remaining unused content pages → cleared to empty string

Design: DAHDZNUAgxE (64 pages: p1 cover, p2 intro, p3–p62 content, p63 references, p64 donation)

Python path: /c/Python313/python.exe
Required: pip install python-docx
"""

import sys
import io
import json
import re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn

sys.path.insert(0, str(Path(__file__).parent))
from extract_docx import classify_paragraph, extract_runs_with_formatting


# ---------------------------------------------------------------------------
# Design constants — DAHDZNUAgxE
# ---------------------------------------------------------------------------

DESIGN_ID = "DAHDZNUAgxE"

# Cover (p1)
COVER_IDS = {
    "title_1":    "PBhMCnWGZWhcwN0p-LB5Dfy4LKBHLbvZ2",
    "title_2":    "PBhMCnWGZWhcwN0p-LBBB35r43HBY5VV8",
    "subtitle":   "PBhMCnWGZWhcwN0p-LBTJXp22Y0Hg7CWx",
    "authors":    "PBhMCnWGZWhcwN0p-LBLDVg5Z9qfRZsLS",
    "disclaimer": "PBhMCnWGZWhcwN0p-LB5BKJbRpVCbpX5N",
    "date":       "PBhMCnWGZWhcwN0p-LBWkKcxh68wh1BzW",
}

# Intro (p2)
INTRO_IDS = {
    "heading": "PBhzHx5FDf3N5L3x-LBrQmFjfT0B2CHtH",
    "body":    "PBhzHx5FDf3N5L3x-LBWrc7qLRWTCtN7w",
    "warning": "PBhzHx5FDf3N5L3x-LBT9zKDJCwdNzVD6-LB6VrTxBz5YNrXW8",
    "header":  "PBhzHx5FDf3N5L3x-LBXT1qDqQCt6Zr62",
}

# Content pages p3–p62: [BODY] element IDs (index 0 = p3, index 59 = p62)
CONTENT_IDS = [
    "PB3RQkYcYx9M2Mgl-LBVN9MmcWw7b1Y6G",   # p3
    "PBRwLfwyTmds9QlW-LByM1vt3fqp6zFWq",   # p4
    "PBCJJsjv8Y9P8RMT-LB21H1hrGpk5kyCC",   # p5
    "PB0gPB20JdPQmXk8-LBvW1vVMHPq2z6Wz",   # p6
    "PBGsgVh30wxFn9b2-LB48d2ZX6HJRZhqX",   # p7
    "PBcc0M50F2slFzsx-LBPXhDJXZZMz7W51",   # p8
    "PB2fd6CqG2C0Sh7c-LBdSN0lvZT1zt5rG",   # p9
    "PBSK4s6cbZThgtbf-LBysFGJxNxrLB1pH",   # p10
    "PBgNNmlqdX2KrHzn-LBWQ4zYH5DkwJ5Cb",   # p11
    "PBWP43B3sPvdNmM2-LBByV8JXDd5SxTCC",   # p12
    "PB0zLyn7nCrXfX66-LByy1vlvr6x0Fr6G",   # p13
    "PB3sRgS7NQXVJrwJ-LBXM0fTzCv6QLZg2",   # p14
    "PBK4W6sz2NXT6c0n-LBLwRJ9C08vrv26z",   # p15
    "PBpzxMZDKhTL7hn1-LBKm6VjZHDzr43DG",   # p16
    "PBM6Xx4WKzX1cb5h-LBD46JnJ48jvd75w",   # p17
    "PBS72ZwWWnhqkB3w-LBrnTCpSN6pZkdGt",   # p18
    "PBXck2sWLymX8BZk-LB0yGvhGYpcntQ9G",   # p19
    "PBTB67Y7w2dbsTxj-LBJts9Kn443ZGH55",   # p20
    "PBpjQf2tjNrGR1xH-LB6Hr85sYvZ4Bp5v",   # p21
    "PBsVWfvS4kyTMGkV-LBqV4nSxzWT70Rqv",   # p22
    "PB09gk3Y0bvb0PFS-LBH0VPP1zLr65rSY",   # p23
    "PB58t9JXHDh857mw-LBrmjtWG1XKYq5kp",   # p24
    "PBgKX24J4w57B15v-LBH8Fh880xPsMwgq",   # p25
    "PBPkl1rNcpk9jgGb-LB3XFxVCCzlPNP5v",   # p26
    "PBZsFWypHTq4vDyC-LB5b82MdBc5wPQ6x",   # p27
    "PB63KQN4jh2TJJR3-LBHMG9WYJ36WLyhd",   # p28
    "PBGdr2c1nfP5RfNV-LB1cFdJsKpZYgHqp",   # p29
    "PBn3T0DFMCZMlDD2-LBH7M5Q3mqZ8F5bY",   # p30
    "PBhmxLpX18ttCMTg-LBBlwPyZrshLgscw",   # p31
    "PB9px7qLw9JLr023-LB4xM9ZsB6w3xLfh",   # p32
    "PB5JnYb6Qmw9gmb6-LByxdVjLdRX5XMFz",   # p33
    "PB24lx3fqWpGz0Rg-LBz7VMwNvz15NpRl",   # p34
    "PBmwrBJqF7pyhLmw-LBd3YsNWmdL97mFT",   # p35
    "PBDsxvgmDgSGsBfF-LBQQBWQVZp1mFM3S",   # p36
    "PBV13ZqjXqsVzrk6-LB1TbnKY6sYZbwhh",   # p37
    "PBhDhPRpTSx9h6Kw-LBHXVyfsMSGH1cVr",   # p38
    "PB1gtC6hvWL42jcX-LBFZgVwFvW87f9xD",   # p39
    "PBhz0fRGtpPCFdF8-LByHmpGpggjF7ZlJ",   # p40
    "PBsCzsTdYHkxnry6-LBd36XssDjlVhkD0",   # p41
    "PByxv80QpsJBhjtT-LB1jZ9KJ0dG5HRC3",   # p42
    "PBCy0gQ3Qsv7g7wt-LB7kMtsHrqpLwPcC",   # p43
    "PBbV2FqsVL1PBvbN-LB7jkPrcFv39LRf1",   # p44
    "PB1Ly6dPjl4kkrtd-LBGQnJHtB8sSTW3h",   # p45
    "PBwHlKRK45TrSz37-LB9M6bSsbGDPTmrZ",   # p46
    "PBcKn43b37fnJW7x-LB2Ht5pYqbXqknXh",   # p47
    "PB84DfJb7RjhBB5R-LBY2Tt5MB7q9CLNY",   # p48
    "PB85d9q1M2hb3Fp0-LBCfXfCM8hy2sx1C",   # p49
    "PB48QKPjtktds7kl-LBvj1Sd17Sc0Vpt3",   # p50
    "PBDSrchfXxcrgR7n-LBYt7058k1qbwVCd",   # p51
    "PBTKkPmgsBxF5D92-LBVjGS2yMyg4PtN0",   # p52
    "PBDTCt5hN6qxKNWX-LBmCmzCPWncJHxtG",   # p53
    "PBsRgH6yYJtYl0Tk-LBrr1byD2LZpx4WD",   # p54
    "PBQSJBL158blxhg4-LBvrQ0BycctVT3pK",   # p55
    "PBJSDLVdvyk0rzpF-LBxvdryzQqTfwCTl",   # p56
    "PB80MMWLVQ0J1jsp-LBdb2fBKN5x7DbQV",   # p57
    "PB4hYrS6hRnWPr2g-LBgysTqLcMvhmxgV",   # p58
    "PBLsFy0qTQtMZgJ2-LBJZLFtFy6G7G05l",   # p59
    "PBnSzHWGft73LCjP-LB7GM3V4Y3TsLLpM",   # p60
    "PB1cP1fqCZND8fGQ-LB4FRLZqb8fJ6YF8",   # p61
    "PBYBqJPmkFLhtnX5-LBNXqBP08FWSJC3z",   # p62
]

# Running headers p3–p62 (index 0 = p3, index 59 = p62)
HEADER_IDS = [
    "PB3RQkYcYx9M2Mgl-LByR2K5QLHvcFwvS",   # p3
    "PBRwLfwyTmds9QlW-LByZjcH8Kbh4MRG4",   # p4
    "PBCJJsjv8Y9P8RMT-LBTvShs5Ct0bhCM5",   # p5
    "PB0gPB20JdPQmXk8-LBbd2xc1pRD7Gs51",   # p6
    "PBGsgVh30wxFn9b2-LBzFHNgyV6vzv0SB",   # p7
    "PBcc0M50F2slFzsx-LBZs6Rvq4jLvc413",   # p8
    "PB2fd6CqG2C0Sh7c-LBSDr7TZZYn3VHJb",   # p9
    "PBSK4s6cbZThgtbf-LBG0nTYW4sNMLMZG",   # p10
    "PBgNNmlqdX2KrHzn-LB0btqqgRYxpvJHQ",   # p11
    "PBWP43B3sPvdNmM2-LBRJqcwH2c6BXwgL",   # p12
    "PB0zLyn7nCrXfX66-LBtlbbP7jL7L4DTm",   # p13
    "PB3sRgS7NQXVJrwJ-LB3d6y4NFBzgzrXL",   # p14
    "PBK4W6sz2NXT6c0n-LByqzYsbTrn3hhgn",   # p15
    "PBpzxMZDKhTL7hn1-LBp3Vn57T3Rm5l7V",   # p16
    "PBM6Xx4WKzX1cb5h-LBgK9Jn56v2F9n9f",   # p17
    "PBS72ZwWWnhqkB3w-LBql5Hs8zdVRb9s3",   # p18
    "PBXck2sWLymX8BZk-LBYqNTYcgsDty4Gh",   # p19
    "PBTB67Y7w2dbsTxj-LBqM7N52Wck4nflw",   # p20
    "PBpjQf2tjNrGR1xH-LBrh3M8CmcQWmFdF",   # p21
    "PBsVWfvS4kyTMGkV-LBh1PgrlXW8dvPPq",   # p22
    "PB09gk3Y0bvb0PFS-LBSw2JnndTc64Fg5",   # p23
    "PB58t9JXHDh857mw-LBH8zvB6p3Crwfw2",   # p24
    "PBgKX24J4w57B15v-LBMHS6hzrZGVxMdb",   # p25
    "PBPkl1rNcpk9jgGb-LBLqMcdNwjrCjGd0",   # p26
    "PBZsFWypHTq4vDyC-LBqwQzq0HKknd2PT",   # p27
    "PB63KQN4jh2TJJR3-LBPW6Zrp9tmPHQd8",   # p28
    "PBGdr2c1nfP5RfNV-LByjFvHP9979gFBB",   # p29
    "PBn3T0DFMCZMlDD2-LBWLSvr1BHF5vvMw",   # p30
    "PBhmxLpX18ttCMTg-LBsXMywXvk3FswR3",   # p31
    "PB9px7qLw9JLr023-LB8pn82497WRQvmM",   # p32
    "PB5JnYb6Qmw9gmb6-LBbQMX0b53zlbTPR",   # p33
    "PB24lx3fqWpGz0Rg-LBqwzQJn8DqqZ3XW",   # p34
    "PBmwrBJqF7pyhLmw-LBnjgHSdDmv1fLpq",   # p35
    "PBDsxvgmDgSGsBfF-LBydWlVq9x2ccxMJ",   # p36
    "PBV13ZqjXqsVzrk6-LBkJW0rSjpHkbr2Q",   # p37
    "PBhDhPRpTSx9h6Kw-LBQlJg282VnnsNYn",   # p38
    "PB1gtC6hvWL42jcX-LB4s3J7tsqTVxrhy",   # p39
    "PBhz0fRGtpPCFdF8-LBprb55ncRbhGnFJ",   # p40
    "PBsCzsTdYHkxnry6-LBWDDYXCVkmRgRsy",   # p41
    "PByxv80QpsJBhjtT-LBXf5TXf2dYLnpPN",   # p42
    "PBCy0gQ3Qsv7g7wt-LBfb1N2lyMrlY4mQ",   # p43
    "PBbV2FqsVL1PBvbN-LB9zVjCbql1HbSNB",   # p44
    "PB1Ly6dPjl4kkrtd-LBsBZHvmrbw1KGDR",   # p45
    "PBwHlKRK45TrSz37-LBQt41fWC95XHFSd",   # p46
    "PBcKn43b37fnJW7x-LBvvnkWS8LL0VZsM",   # p47
    "PB84DfJb7RjhBB5R-LBKsBxPJ7mNKMcbR",   # p48
    "PB85d9q1M2hb3Fp0-LBh2YCfZXSLLxmyg",   # p49
    "PB48QKPjtktds7kl-LBj3NqHTbKXhSgRQ",   # p50
    "PBDSrchfXxcrgR7n-LB1d7D09Z1RJpPvR",   # p51
    "PBTKkPmgsBxF5D92-LBvhmyFHzNPj95dW",   # p52
    "PBDTCt5hN6qxKNWX-LBpfFBHmD4syWltm",   # p53
    "PBsRgH6yYJtYl0Tk-LBG51Z3F3DbldZPf",   # p54
    "PBQSJBL158blxhg4-LBbL2LXnvBFcbZlG",   # p55
    "PBJSDLVdvyk0rzpF-LBJDfBqSNPw5LQRG",   # p56
    "PB80MMWLVQ0J1jsp-LB6J4myc3syz3JlP",   # p57
    "PB4hYrS6hRnWPr2g-LBtZrh09q4M51m5P",   # p58
    "PBLsFy0qTQtMZgJ2-LBtwCksGVjtFffc9",   # p59
    "PBnSzHWGft73LCjP-LBrFtLX4wxnDrmgr",   # p60
    "PB1cP1fqCZND8fGQ-LBxKDtqtTwwcN9Jl",   # p61
    "PBYBqJPmkFLhtnX5-LB70dJBfJzhhJLR1",   # p62
]

# Paragraph types treated as bold section headings
HEADING_TYPES = frozenset({'heading_bold', 'h1', 'h2', 'h3'})
# Paragraph types treated as bullet list items
BULLET_TYPES = frozenset({'bullet'})

# Figure page layout (Canva page = 816 × 1056 pts)
# Caption goes in [CONTENT] at top; image is inserted below it.
FIGURE_IMAGE_POSITION  = {"top": 190, "left": 40}
FIGURE_IMAGE_DIMENSION = {"width": 736, "height": 790}

# Maximum figure pages supported per document
MAX_FIGURE_PAGES = 8


# ---------------------------------------------------------------------------
# Page break detection
# ---------------------------------------------------------------------------

def has_page_break(para):
    """Detect a hard page break in a Word paragraph."""
    for run in para.runs:
        for br in run._element.findall(qn('w:br')):
            if br.get(qn('w:type')) == 'page':
                return True
    pPr = para._element.find(qn('w:pPr'))
    if pPr is not None and pPr.find(qn('w:sectPr')) is not None:
        return True
    return False


# ---------------------------------------------------------------------------
# Step 1: Split Word doc into pages by explicit page breaks
# ---------------------------------------------------------------------------

def _count_drawings(para):
    """Count inline image drawings in a paragraph."""
    return len(para._element.findall('.//' + qn('w:drawing')))


def split_into_pages(docx_path):
    """
    Split the document into a list of pages.
    Each page is a list of typed paragraph dicts {type, text, runs, style}.
    Empty paragraphs are dropped UNLESS they contain drawings.
    Each page dict also has a top-level 'image_count' tracking embedded images.

    Returns: list of page dicts:
      {
        'paragraphs': [...],
        'image_count': int,   # total inline drawings on this page
      }
    """
    doc = Document(docx_path)
    pages = []
    current_paras = []
    current_images = 0

    for para in doc.paragraphs:
        text = para.text.strip()
        runs = extract_runs_with_formatting(para)
        para_type, meta = classify_paragraph(para, runs)
        drawing_count = _count_drawings(para)

        if has_page_break(para):
            if para_type != 'empty' and text:
                entry = {'type': para_type, 'text': text, 'runs': runs,
                         'style': para.style.name if para.style else ''}
                if meta:
                    entry['meta'] = meta
                current_paras.append(entry)
            current_images += drawing_count
            pages.append({'paragraphs': current_paras, 'image_count': current_images})
            current_paras = []
            current_images = 0
        else:
            current_images += drawing_count
            if para_type != 'empty' and text:
                entry = {'type': para_type, 'text': text, 'runs': runs,
                         'style': para.style.name if para.style else ''}
                if meta:
                    entry['meta'] = meta
                current_paras.append(entry)

    if current_paras or current_images:
        pages.append({'paragraphs': current_paras, 'image_count': current_images})

    return pages


# ---------------------------------------------------------------------------
# Step 2: Extract cover fields from page 1
# ---------------------------------------------------------------------------

_AUTHOR_PATTERN = re.compile(
    r'\bM\.?D\.?\b|\bD\.?O\.?\b|\bPhD\b|\bFCCP\b|\bFCCM\b|\bFACCM\b|\bMD\b', re.I
)

def _is_author_heading(text):
    """True if a heading_bold paragraph looks like an author byline."""
    return bool(_AUTHOR_PATTERN.search(text))


def extract_cover(page):
    """
    Parse cover page paragraphs into slot values.

    Expected structure:
      heading_bold × 1–3  → title_1, title_2, subtitle (author-like headings excluded)
      author or author-like heading_bold → joined as AUTHORS
      disclaimer × 1      → COVER_DISCLAIMER
      date × 0–1          → COVER_DATE
    """
    title_headings = []
    author_texts = []
    paras = page['paragraphs']

    for p in paras:
        if p['type'] in ('heading_bold', 'h1'):
            if _is_author_heading(p['text']):
                author_texts.append(p['text'])
            else:
                title_headings.append(p['text'])
        elif p['type'] == 'author':
            author_texts.append(p['text'])
    disclaimers = [p for p in paras if p['type'] == 'disclaimer']
    dates = [p for p in paras if p['type'] == 'date']

    headings = title_headings
    title_1 = headings[0] if len(headings) > 0 else ''
    title_2 = headings[1] if len(headings) > 1 else ''
    subtitle = headings[2] if len(headings) > 2 else ''
    full_title = ' '.join(headings)

    date_text = ''
    if dates:
        date_text = re.sub(r'^Updated\s+', '', dates[0]['text']).strip()

    return {
        'title_1':    title_1,
        'title_2':    title_2,
        'subtitle':   subtitle,
        'full_title': full_title,
        'authors':    '\n'.join(author_texts),
        'disclaimer': disclaimers[0]['text'] if disclaimers else '',
        'date':       date_text,
    }


# ---------------------------------------------------------------------------
# Step 3: Extract intro fields from page 2
# ---------------------------------------------------------------------------

def extract_intro(page):
    """
    Parse intro page paragraphs into slot values.

    Returns dict with: heading, body (joined text), warning.
    """
    heading = ''
    body_parts = []
    warning = ''

    for p in page['paragraphs']:
        if p['type'] in HEADING_TYPES and not heading:
            heading = p['text']
        elif p['type'] == 'warning':
            warning = p['text']
        elif p['type'] not in ('empty', 'date', 'author', 'disclaimer'):
            body_parts.append(p)

    body_text, _, _ = build_page_content(body_parts)
    return {'heading': heading, 'body': body_text, 'warning': warning}


# ---------------------------------------------------------------------------
# Step 4: Build content text + format operations for a page
# ---------------------------------------------------------------------------

def build_page_content(paragraphs):
    """
    Join page paragraphs into a single string and produce format_text ranges.

    Separator logic:
      - consecutive bullets   → single \n (tight list)
      - bullet → non-bullet   → \n\n
      - anything → heading    → \n\n
      - anything else         → \n\n

    Returns:
      text        : str — the full page text
      bold_ranges : list of (start, end) — character ranges for bold headings
      bullet_ranges: list of (start, end) — character ranges for bullet items
    """
    if not paragraphs:
        return '', [], []

    parts = []
    bold_ranges = []
    bullet_ranges = []
    pos = 0

    for i, para in enumerate(paragraphs):
        ptype = para['type']
        text = para['text']
        next_type = paragraphs[i + 1]['type'] if i + 1 < len(paragraphs) else None

        start = pos
        parts.append(text)
        pos += len(text)

        # Track formatting ranges
        if ptype in HEADING_TYPES:
            bold_ranges.append((start, pos))
        if ptype in BULLET_TYPES:
            bullet_ranges.append((start, pos))

        # Determine separator
        if next_type is None:
            sep = ''
        elif ptype in BULLET_TYPES and next_type in BULLET_TYPES:
            sep = '\n'
        else:
            sep = '\n\n'

        parts.append(sep)
        pos += len(sep)

    full_text = ''.join(parts).rstrip()
    return full_text, bold_ranges, bullet_ranges


# ---------------------------------------------------------------------------
# Step 5: Classify special page types
# ---------------------------------------------------------------------------

def is_references_page(page):
    """True if the page's first paragraph is a 'References' heading."""
    paras = page['paragraphs']
    if not paras:
        return False
    first = paras[0]
    return (first['type'] == 'ref_heading' or
            first['text'].strip().lower() == 'references')


def is_figure_page(page):
    """
    True if the page contains embedded images (inline drawings).
    A figure page has images + optional captions; no regular body text.
    """
    if page['image_count'] > 0:
        return True
    # Also treat as figure page if ALL text paragraphs are figure captions
    paras = page['paragraphs']
    if paras and all(p['type'] == 'figure_caption' for p in paras):
        return True
    return False


def get_page_id(content_element_id):
    """Extract the Canva page ID from a content element ID."""
    return content_element_id.split('-')[0]


# ---------------------------------------------------------------------------
# Step 6: Generate all Canva operations
# ---------------------------------------------------------------------------

def _emit_content_ops(ops, content_id, header_id, paras, running_header_text):
    """Emit replace_text + format_text ops for one content slot."""
    text, bold_ranges, bullet_ranges = build_page_content(paras)
    ops.append({"operation": "replace_text", "element_id": content_id, "text": text})
    for start, end in bold_ranges:
        ops.append({
            "operation": "format_text",
            "element_id": content_id,
            "text_range": {"start": start, "end": end},
            "formatting": {"bold": True},
        })
    for start, end in bullet_ranges:
        ops.append({
            "operation": "format_text",
            "element_id": content_id,
            "text_range": {"start": start, "end": end},
            "formatting": {"list_level": 1},
        })
    ops.append({"operation": "replace_text", "element_id": header_id, "text": running_header_text})


def generate_operations(pages, guide_title=None, guide_date=None):
    """
    Convert page list into Canva editing API operations.

    Figure pages produce caption text ops + a pending insert_fill entry
    (asset_id=null) that Claude fills after uploading the extracted image.

    Returns (ops, summary) where summary includes:
      - figure_pages: list of {slot_index, canva_page_index, canva_page_id,
                                content_element_id, image_count, caption,
                                insert_fill_op (asset_id=null)}
    """
    ops = []
    figure_pages = []

    if len(pages) < 1:
        return ops, {'error': 'No pages found in document'}

    # --- Cover (page 1) ---
    cover = extract_cover(pages[0])
    if not guide_title:
        guide_title = cover['full_title'] or 'Untitled Guide'
    if not guide_date:
        guide_date = cover['date'] or ''

    running_header_text = guide_title
    if guide_date:
        running_header_text = f"{guide_title} ({guide_date})"

    ops += [
        {"operation": "replace_text", "element_id": COVER_IDS["title_1"],    "text": cover['title_1']},
        {"operation": "replace_text", "element_id": COVER_IDS["title_2"],    "text": cover['title_2']},
        {"operation": "replace_text", "element_id": COVER_IDS["subtitle"],   "text": cover['subtitle']},
        {"operation": "replace_text", "element_id": COVER_IDS["authors"],    "text": cover['authors']},
        {"operation": "replace_text", "element_id": COVER_IDS["disclaimer"], "text": cover['disclaimer']},
        {"operation": "replace_text", "element_id": COVER_IDS["date"],       "text": cover['date']},
    ]

    # --- Intro (page 2) ---
    if len(pages) >= 2:
        intro = extract_intro(pages[1])
        ops += [
            {"operation": "replace_text", "element_id": INTRO_IDS["heading"], "text": intro['heading']},
            {"operation": "replace_text", "element_id": INTRO_IDS["body"],    "text": intro['body']},
            {"operation": "replace_text", "element_id": INTRO_IDS["warning"], "text": intro['warning']},
            {"operation": "replace_text", "element_id": INTRO_IDS["header"],  "text": running_header_text},
        ]

    # --- Content pages (pages 3 onwards) ---
    content_slot_idx = 0
    content_pages_used = 0
    content_pages_cleared = 0
    overflow_pages = 0

    # Separate references page (last page if it's a references page)
    body_pages = pages[2:]
    ref_page = None
    if body_pages and is_references_page(body_pages[-1]):
        ref_page = body_pages[-1]
        body_pages = body_pages[:-1]

    # Fill content pages from body pages
    for word_page in body_pages:
        if content_slot_idx >= len(CONTENT_IDS):
            overflow_pages += 1
            continue

        content_id = CONTENT_IDS[content_slot_idx]
        header_id  = HEADER_IDS[content_slot_idx]
        page_id    = get_page_id(content_id)
        canva_page = content_slot_idx + 3   # p3 = slot 0

        if is_figure_page(word_page):
            # Caption text → [CONTENT]; image will be inserted separately
            captions = [p['text'] for p in word_page['paragraphs']
                        if p['type'] == 'figure_caption']
            caption_text = '\n\n'.join(captions)

            ops.append({"operation": "replace_text", "element_id": content_id,
                        "text": caption_text})
            ops.append({"operation": "replace_text", "element_id": header_id,
                        "text": running_header_text})

            # One pending insert_fill per embedded image on this page
            for img_idx in range(word_page['image_count']):
                figure_pages.append({
                    "slot_index":        content_slot_idx,
                    "canva_page_index":  canva_page,
                    "canva_page_id":     page_id,
                    "content_element_id": content_id,
                    "image_count":       word_page['image_count'],
                    "image_index":       img_idx,   # 0-based within this page
                    "caption":           caption_text,
                    # Template for insert_fill — Claude fills asset_id after upload
                    "insert_fill_op": {
                        "operation":  "insert_fill",
                        "page_id":    page_id,
                        "asset_id":   None,          # → set by Claude after upload
                        "position":   FIGURE_IMAGE_POSITION,
                        "dimension":  FIGURE_IMAGE_DIMENSION,
                    },
                })
        else:
            _emit_content_ops(ops, content_id, header_id,
                              word_page['paragraphs'], running_header_text)

        content_slot_idx += 1
        content_pages_used += 1

    # References page — repurpose next content slot
    if ref_page is not None:
        if content_slot_idx < len(CONTENT_IDS):
            content_id = CONTENT_IDS[content_slot_idx]
            header_id  = HEADER_IDS[content_slot_idx]
            _emit_content_ops(ops, content_id, header_id,
                              ref_page['paragraphs'], running_header_text)
            content_slot_idx += 1
            content_pages_used += 1

    # Clear remaining unused content slots
    for i in range(content_slot_idx, len(CONTENT_IDS)):
        ops.append({"operation": "replace_text", "element_id": CONTENT_IDS[i], "text": ""})
        ops.append({"operation": "replace_text", "element_id": HEADER_IDS[i],  "text": ""})
        content_pages_cleared += 1

    summary = {
        'design_id':             DESIGN_ID,
        'guide_title':           guide_title,
        'guide_date':            guide_date,
        'running_header':        running_header_text,
        'word_pages_total':      len(pages),
        'content_pages_used':    content_pages_used,
        'content_pages_cleared': content_pages_cleared,
        'has_references':        ref_page is not None,
        'figure_page_count':     len(set(fp['slot_index'] for fp in figure_pages)),
        'total_images':          len(figure_pages),
        'total_operations':      len(ops),
    }
    if overflow_pages:
        summary['overflow_pages'] = overflow_pages

    return ops, summary, figure_pages


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def map_document(docx_path, guide_title=None, guide_date=None):
    """Full pipeline: split → extract → generate operations."""
    pages = split_into_pages(docx_path)
    ops, summary, figure_pages = generate_operations(
        pages, guide_title=guide_title, guide_date=guide_date
    )
    summary['source_file'] = str(docx_path)
    return {'summary': summary, 'operations': ops, 'figure_pages': figure_pages}


def print_summary(result):
    """Print human-readable mapping summary."""
    s = result['summary']
    print(f"Source:          {s['source_file']}")
    print(f"Design:          {s['design_id']}")
    print(f"Title:           {s['guide_title']}")
    print(f"Date:            {s['guide_date']}")
    print(f"Running header:  {s['running_header']}")
    print(f"Word pages:      {s['word_pages_total']}")
    print(f"Content used:    {s['content_pages_used']} pages")
    print(f"Content cleared: {s['content_pages_cleared']} pages")
    print(f"Has references:  {s['has_references']}")
    print(f"Figure pages:    {s['figure_page_count']} pages ({s['total_images']} images)")
    print(f"Total operations:{s['total_operations']}")

    if s.get('overflow_pages'):
        print(f"\nWARNING: {s['overflow_pages']} Word pages had no Canva slot (overflow)")

    fps = result.get('figure_pages', [])
    if fps:
        print(f"\n=== FIGURE PAGES (pending insert_fill — need asset_id after image upload) ===")
        for fp in fps:
            print(f"  Canva p{fp['canva_page_index']} (slot {fp['slot_index']}): "
                  f"{fp['image_count']} image(s) — {fp['caption'][:60]}")


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    if len(sys.argv) < 2:
        print("Usage: python map_to_canva.py <path_to_docx> [--json] [--dry-run] [--date 'March 2, 2026']")
        sys.exit(1)

    docx_path = Path(sys.argv[1])
    if not docx_path.exists():
        print(f"Error: File not found: {docx_path}")
        sys.exit(1)

    output_json = '--json' in sys.argv
    dry_run = '--dry-run' in sys.argv

    cli_date = None
    if '--date' in sys.argv:
        idx = sys.argv.index('--date')
        if idx + 1 < len(sys.argv):
            cli_date = sys.argv[idx + 1]

    result = map_document(docx_path, guide_date=cli_date)

    if dry_run:
        result.pop('operations', None)

    if output_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_summary(result)
