#!/usr/bin/env python3
"""Fill missing figures/chapter_XX/ directories from figures/page/ and figures/embedded/."""

import json, re, shutil
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')
FIGURES = ROOT / 'figures'

chapter_pages = json.loads((FIGURES / 'chapter_pages.json').read_text())

def safe_name(s):
    return re.sub(r'[^\w\-]+', '_', s)[:50]

# Find which chapters need figure dirs
existing = set()
for d in FIGURES.glob('chapter_*'):
    m = re.match(r'chapter_(\d+)_', d.name)
    if m:
        existing.add(int(m.group(1)))

for ch_str, ch_data in sorted(chapter_pages.items(), key=lambda x: int(x[0])):
    ch_num = int(ch_str)
    if ch_num in existing:
        continue  # already has directory

    pages = ch_data.get('pages', [])
    if not pages:
        continue

    en = ch_data.get('en', f'Chapter_{ch_num}')
    zh = ch_data.get('zh', '')
    dir_name = f'chapter_{ch_num:02d}_{safe_name(en)}'
    ch_dir = FIGURES / dir_name
    ch_dir.mkdir(parents=True, exist_ok=True)

    page_dir = ch_dir / 'page'
    emb_dir = ch_dir / 'embedded'
    page_dir.mkdir(exist_ok=True)
    emb_dir.mkdir(exist_ok=True)

    page_count = 0
    emb_count = 0

    for pg in pages:
        # Copy page image
        for variant in [f'page{pg:04d}_tight.png', f'page{pg:04d}.png']:
            src = FIGURES / 'page' / variant
            if src.exists():
                shutil.copy2(src, page_dir / variant)
                page_count += 1
                break

    # Copy embedded images for these pages
    for emb_src in sorted((FIGURES / 'embedded').glob(f'page{pg:04d}_img*.png')):
        if emb_src.exists():
            shutil.copy2(emb_src, emb_dir / emb_src.name)
            emb_count += 1

    if page_count > 0 or emb_count > 0:
        print(f'  Ch{ch_num} ({en[:25]}): {page_count} page + {emb_count} embedded images')
    else:
        # Remove empty directory
        shutil.rmtree(ch_dir)
        print(f'  Ch{ch_num} ({en[:25]}): no images available from pool')

print('\nDone!')
