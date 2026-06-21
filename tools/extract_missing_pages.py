#!/usr/bin/env python3
"""Extract page images for chapters missing figure coverage from source PDF."""

import json, re, sys
from pathlib import Path
import fitz  # PyMuPDF

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')
PDF_PATH = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCI Express Technology 3.0.pdf')
FIGURES = ROOT / 'figures'

# Chapters needing extraction and their page ranges
# (page numbers are 0-based in PyMuPDF, but chapter_pages.json uses PDF page numbers)
MISSING_CHAPTERS = {
    2: 'PCIe_Architecture_Overview',
    6: 'Flow_Control',
    7: 'Quality_of_Service',
    9: 'DLLP_Elements',
    11: 'Physical_Layer_Logical_Gen1_Gen2',
    12: 'Physical_Layer_Logical_Gen3',
    100: 'Index',
}

chapter_pages = json.loads((FIGURES / 'chapter_pages.json').read_text())
pdf = fitz.open(str(PDF_PATH))
total_pdf_pages = pdf.page_count

print(f'Source PDF: {PDF_PATH.name} ({total_pdf_pages} pages)')

for ch_num, ch_name in sorted(MISSING_CHAPTERS.items()):
    ch_data = chapter_pages.get(str(ch_num), {})
    pages = ch_data.get('pages', [])
    if not pages:
        print(f'  Ch{ch_num}: no page data, skipping')
        continue

    # Create chapter directory
    dir_name = f'chapter_{ch_num:02d}_{ch_name}'
    ch_dir = FIGURES / dir_name
    page_dir = ch_dir / 'page'
    page_dir.mkdir(parents=True, exist_ok=True)

    extracted = 0
    for pg_num in pages:
        # PDF pages are 1-based in our metadata, 0-based in PyMuPDF
        pdf_idx = pg_num - 1
        if pdf_idx < 0 or pdf_idx >= total_pdf_pages:
            continue

        out_path = page_dir / f'page{pg_num:04d}.png'
        if out_path.exists():
            extracted += 1
            continue

        try:
            page = pdf[pdf_idx]
            # Render at 150 DPI (~1280px wide for letter size)
            pix = page.get_pixmap(dpi=150)
            pix.save(str(out_path))
            extracted += 1
        except Exception as e:
            print(f'    page {pg_num}: ERROR {e}')

    print(f'  Ch{ch_num} ({ch_name}): {extracted}/{len(pages)} pages extracted')

pdf.close()
print('\nDone!')
