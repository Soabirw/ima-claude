"""
Extract embedded images from a Word document in document order.
Optionally uploads to file.io for temporary public access.

Usage:
    /c/Python313/python.exe extract_figures.py <path_to_docx> [--upload] [--output-dir DIR]

Output JSON:
    [
      {
        "figure_num": 1,
        "path": "/abs/path/figure_01.png",
        "url": "https://file.io/xxxx",  (null if not uploaded)
        "page_num": 15,
        "size_bytes": 107122,
        "content_type": "image/png",
        "para_index": 140
      },
      ...
    ]

Notes:
  - Images are extracted in document paragraph order.
  - file.io links expire after 14 days and delete on first download.
  - Requires: pip install python-docx requests
  - Python path: /c/Python313/python.exe
"""

import sys
import io
import json
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn


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


def extract_figures(docx_path, output_dir=None, upload=False):
    """
    Extract all inline images from a Word doc in paragraph order.

    Returns list of dicts with figure metadata.
    Each image is saved to output_dir as figure_NN.ext.
    If upload=True, attempts to upload to file.io and records the URL.
    """
    doc = Document(docx_path)

    if output_dir is None:
        output_dir = Path(docx_path).parent / 'figures'
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    figures = []
    page_num = 1
    fig_num = 0

    # Build relationship map once
    rels = doc.part.rels

    for i, para in enumerate(doc.paragraphs):
        if has_page_break(para):
            page_num += 1

        # Find all blip references (inline images) in this paragraph
        blips = para._element.findall('.//' + qn('a:blip'))
        for blip in blips:
            rid = blip.get(qn('r:embed'))
            if not rid or rid not in rels:
                continue

            rel = rels[rid]
            if 'image' not in rel.reltype.lower():
                continue

            img_part = rel.target_part
            ct = img_part.content_type
            ext = ct.split('/')[-1]
            if ext == 'jpeg':
                ext = 'jpg'

            fig_num += 1
            filename = output_dir / f'figure_{fig_num:02d}.{ext}'
            with open(filename, 'wb') as f:
                f.write(img_part.blob)

            entry = {
                'figure_num': fig_num,
                'path': str(filename),
                'url': None,
                'page_num': page_num,
                'size_bytes': len(img_part.blob),
                'content_type': ct,
                'para_index': i,
            }

            if upload:
                try:
                    import requests
                    with open(filename, 'rb') as f:
                        resp = requests.post(
                            'https://file.io',
                            files={'file': f},
                            timeout=30,
                        )
                    data = resp.json()
                    if data.get('success'):
                        entry['url'] = data['link']
                    else:
                        entry['upload_error'] = data.get('message', 'upload failed')
                except Exception as exc:
                    entry['upload_error'] = str(exc)

            figures.append(entry)

    return figures


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    if len(sys.argv) < 2:
        print('Usage: python extract_figures.py <path_to_docx> [--upload] [--output-dir DIR]')
        sys.exit(1)

    docx_path = Path(sys.argv[1])
    if not docx_path.exists():
        print(f'Error: File not found: {docx_path}')
        sys.exit(1)

    do_upload = '--upload' in sys.argv

    out_dir = None
    for j, arg in enumerate(sys.argv):
        if arg == '--output-dir' and j + 1 < len(sys.argv):
            out_dir = sys.argv[j + 1]

    result = extract_figures(docx_path, output_dir=out_dir, upload=do_upload)

    print(json.dumps(result, indent=2, ensure_ascii=False))
