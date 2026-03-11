"""
Shared utilities for Word document processing across ima-cancer-care-guides scripts.
"""

from docx.oxml.ns import qn


def has_page_break(para):
    """Detect a hard page break in a Word paragraph.

    Checks both explicit w:br type=page runs and section-level page breaks
    (w:pPr/w:sectPr), which appear on the last paragraph of a section.
    """
    for run in para.runs:
        for br in run._element.findall(qn('w:br')):
            if br.get(qn('w:type')) == 'page':
                return True
    pPr = para._element.find(qn('w:pPr'))
    if pPr is not None and pPr.find(qn('w:sectPr')) is not None:
        return True
    return False
