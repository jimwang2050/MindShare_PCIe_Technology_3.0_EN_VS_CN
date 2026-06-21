#!/usr/bin/env python3
"""Clean PDF artifacts and OCR errors from chapter MD files."""

import re
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')

# --- OCR error fixes ---
OCR_FIXES = [
    (r'\bEx ress\b', 'Express'),
    (r'\bTechnolo gy\b', 'Technology'),
    (r'\bTechnolo p gy\b', 'Technology'),  # 3-segment: Technolo p gy
    (r'\bprod‐\s*ucts\b', 'products'),
    (r'\bconnec‐\s*tion\b', 'connection'),
    (r'\btrans‐\s*mission\b', 'transmission'),
    (r'\bsynchro‐\s*nized\b', 'synchronized'),
    (r'\bunder‐\s*stand\b', 'understand'),
    (r'\backnowl‐\s*edged\b', 'acknowledged'),
    (r'\bconfig‐\s*uration\b', 'configuration'),
    (r'\binforma‐\s*tion\b', 'information'),
    (r'\bpack‐\s*ets\b', 'packets'),
]

def clean_chapter(ch_file, ch_num):
    text = ch_file.read_text(encoding='utf-8')
    original = text
    chapter_name = ''
    ch_name_match = re.search(r'Chapter (\d+)\. (.+)', text)
    if ch_name_match:
        chapter_name = ch_name_match.group(2).strip()

    # --- 1. Apply OCR fixes ---
    for pattern, replacement in OCR_FIXES:
        text = re.sub(pattern, replacement, text)

    # --- 2. Remove orphaned PDF page numbers ---
    # Lines that are just a bold page number: **123** (on its own line, not in TOC)
    # These appear as \n\n**123**\n\n in the text
    # Only target 2-4 digit page numbers that appear between text sections
    text = re.sub(
        r'\n\n\*\*(\d{2,4})\*\*\s*\n\n(?!\w)',
        r'\n\n',
        text
    )

    # --- 3. Remove orphaned chapter title headers from PDF ---
    # Patterns like: **Chapter X: Some Title** that are page headers
    # Only remove if they don't match the current chapter
    other_chapter_pattern = re.compile(
        r'\n\n\*\*Chapter (\d+): (.+?)\*\*\s*\n',
        re.IGNORECASE
    )
    def remove_other_chapters(m):
        ref_ch = int(m.group(1))
        ref_title = m.group(2)
        if ref_ch != ch_num:
            return '\n'
        # Keep it if it's our chapter
        return m.group(0)
    text = other_chapter_pattern.sub(remove_other_chapters, text)

    # --- 4. Remove orphaned "PCI Express Technology" headers ---
    # These are PDF page headers appearing as \n\n**PCI Express Technology**\n\n
    text = re.sub(
        r'\n\n\*{0,2}PCI Ex(p?)ress Technolo(p?)( gy|gy)?\*{0,2}\s*\n\n',
        r'\n\n',
        text
    )

    # Also clean the ocr'd version
    text = re.sub(
        r'\n\n\*{0,2}PCI Ex ress Technolo gy\*{0,2}\s*\n\n',
        r'\n\n',
        text
    )

    # --- 5. Clean up excessive whitespace ---
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    text = re.sub(r'  +', ' ', text)

    if text != original:
        ch_file.write_text(text, encoding='utf-8')
        return True
    return False

# Process all chapters
total_fixes = 0
for ch_file in sorted(ROOT.glob('MindShare_PCIe_ch[0-9]*.md')):
    ch_match = re.search(r'ch(\d+)', ch_file.name)
    if not ch_match:
        continue
    ch_num = int(ch_match.group(1))

    # Count artifacts before
    before_ocr = len(re.findall(r'Ex ress|Technolo gy|Technolo p gy', ch_file.read_text(encoding='utf-8')))
    before_page = len(re.findall(r'\n\n\*\*\d{2,4}\*\*\s*\n\n(?!\w)', ch_file.read_text(encoding='utf-8')))

    if clean_chapter(ch_file, ch_num):
        after_ocr = len(re.findall(r'Ex ress|Technolo gy|Technolo p gy', ch_file.read_text(encoding='utf-8')))
        after_page = len(re.findall(r'\n\n\*\*\d{2,4}\*\*\s*\n\n(?!\w)', ch_file.read_text(encoding='utf-8')))
        fixes_ocr = before_ocr - after_ocr
        fixes_page = before_page - after_page
        if fixes_ocr > 0 or fixes_page > 0:
            print(f'  Ch{ch_num}: {fixes_ocr} OCR fixes, {fixes_page} page num cleanups')
            total_fixes += fixes_ocr + fixes_page

print(f'\nTotal fixes: {total_fixes}')
