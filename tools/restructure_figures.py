#!/usr/bin/env python3
"""
Restructure chapter MDs:
1. Extract figures from inside <td> to standalone centered blocks between tables
2. Use tight-crop variants where available
3. Add page index links
4. Fix column widths and blank areas
"""

import re
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')

# New table header with better column sizing
NEW_TABLE_HEAD = ('<table style="width:100%; table-layout:fixed">\n'
                  '<colgroup><col style="width:50%"><col style="width:50%"></colgroup>\n'
                  '<thead><tr><th>🇬🇧 English</th>'
                  '<th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>\n'
                  '<tbody><tr>')

TABLE_FOOT = '</tr></tbody></table>'


def build_figure_block(img_path, caption, page_num=None):
    """Build a standalone centered figure block."""
    parts = []

    # Caption centered
    if caption:
        cap_clean = caption.strip().strip('_').strip()
        parts.append(f'\n<p align="center"><b>{cap_clean}</b></p>')

    # Image - prefer tight variant
    img_to_use = img_path
    tight = img_path.replace('.png', '_tight.png')
    if Path(ROOT / tight).exists():
        img_to_use = tight

    parts.append(f'\n<p align="center"><img src="{img_to_use}" width="700"></p>')

    # Page index link
    if page_num:
        orig_page = re.sub(r'_tight\.png$', '.png', img_to_use)
        parts.append(f'\n<p align="center"><sub>📄 <a href="{orig_page}">Page {page_num}</a></sub></p>')

    return ''.join(parts) + '\n'


def extract_page_num(img_path):
    """Extract page number from image path like 'figures/.../page0276.png'."""
    m = re.search(r'page(\d+)', img_path)
    return int(m.group(1)) if m else None


def process_section_body(en_text, zh_text):
    """
    Process a section's English and Chinese text.
    Extract figures from English text, split at figure boundaries.
    Returns list of (en_part, zh_part, figure_block) tuples.
    The last tuple has figure_block=None.
    """
    # Find all img tags in English text
    img_tag_pattern = re.compile(r'<img src="([^"]+)"[^>]*>')
    img_matches = list(img_tag_pattern.finditer(en_text))
    if not img_matches:
        return [(en_text.strip(), zh_text.strip(), None)]

    blocks = []
    last_end = 0

    for i, m in enumerate(img_matches):
        img_path = m.group(1)
        page_num = extract_page_num(img_path)

        # Text before this image
        before_en = en_text[last_end:m.start()]

        # Try to find a caption in the 300 chars before the img tag
        caption = None
        pre_text = before_en[-300:] if len(before_en) > 300 else before_en
        cap_match = re.search(
            r'(_?(?:Figure|Table)\s+[^\n]+?_?)\s*$',
            pre_text,
            re.MULTILINE
        )
        if cap_match:
            caption = cap_match.group(1).strip().strip('_').strip()
            # Remove the caption from before_en
            cap_start_in_before = before_en.rfind(cap_match.group(1))
            if cap_start_in_before >= 0:
                before_en = before_en[:cap_start_in_before]

        before_en = before_en.strip()
        if before_en:
            blocks.append((before_en, '', None))

        # Figure block
        fig_block = build_figure_block(img_path, caption or 'Figure', page_num)
        blocks.append((None, None, fig_block))

        last_end = m.end()

    # Remaining text after last figure
    after_en = en_text[last_end:].strip()
    if after_en:
        blocks.append((after_en, '', None))

    # Distribute Chinese text proportionally
    if zh_text.strip():
        # Simple approach: put all Chinese text in the first text block
        # and empty in subsequent text blocks
        zh_parts = zh_text.strip()
        text_blocks = [b for b in blocks if b[2] is None]
        if text_blocks:
            # Put all Chinese in first text block
            blocks_list = list(blocks)
            for i, b in enumerate(blocks_list):
                if b[2] is None:
                    if i == 0:
                        blocks_list[i] = (b[0], zh_parts, None)
                    else:
                        blocks_list[i] = (b[0], '', None)
                    break
            blocks = blocks_list

    return blocks


def restructure_chapter(ch_file):
    text = ch_file.read_text(encoding='utf-8')
    original = text

    # Step 1: Replace old table headers with new fixed-width headers
    text = re.sub(
        r'<table>\s*<thead><tr><th width="50%">',
        NEW_TABLE_HEAD,
        text
    )
    # Also fix old-style headers
    text = re.sub(
        r'<table>\s*<thead><tr><th width="50%">🇬🇧 English</th>'
        r'<th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>\s*<tbody><tr>',
        NEW_TABLE_HEAD,
        text
    )

    # Step 2: Process each section to extract figures from inside <td>
    # Match: <td>\n\n...content...\n\n</td>\n<td style="...">\n\n...content...\n\n</td>
    section_pattern = re.compile(
        r'<td>\n\n(.*?)\n\n</td>\n'
        r'<td style="background-color:#e8e8e8">\n\n(.*?)\n\n</td>',
        re.DOTALL
    )

    def restructure_section(match):
        en_text = match.group(1)
        zh_text = match.group(2)

        blocks = process_section_body(en_text, zh_text)

        result_parts = []
        for en_part, zh_part, fig_block in blocks:
            if fig_block:
                # Close current table, insert figure, open new table
                result_parts.append(f'{TABLE_FOOT}\n')
                result_parts.append(fig_block)
                result_parts.append(f'\n{NEW_TABLE_HEAD}\n')
            else:
                result_parts.append(f'<td>\n\n{en_part}\n\n</td>\n')
                result_parts.append(f'<td style="background-color:#e8e8e8">\n\n{zh_part}\n\n</td>\n')

        return ''.join(result_parts)

    text = section_pattern.sub(restructure_section, text)

    # Step 3: Fix empty table sections (remove orphaned <table> open/close pairs)
    # Collapse: </tr></tbody></table>\n\n<table...><tbody><tr> → nothing
    text = re.sub(
        r'</tr></tbody></table>\s*\n\s*' + re.escape(NEW_TABLE_HEAD.strip()) + r'\s*\n\s*<td>\n\n\s*\n\n</td>',
        '',
        text,
        flags=re.DOTALL
    )

    # Step 4: Clean up excessive blank lines (>2 consecutive)
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # Step 5: Remove orphaned PDF page headers that remain
    text = re.sub(r'\n\n\*\*PCI Express Technology\*\*\s*\n\n', '\n\n', text)
    text = re.sub(r'\n\n\*\*Chapter \d+:[^*]+\*\*\s*\n\n', '\n\n', text)

    if text != original:
        ch_file.write_text(text, encoding='utf-8')
        return True
    return False


# Process all chapters
for ch_file in sorted(ROOT.glob('MindShare_PCIe_ch[0-9]*.md')):
    if restructure_chapter(ch_file):
        # Count figures extracted
        text = ch_file.read_text(encoding='utf-8')
        imgs = len(re.findall(r'<img src=', text))
        figs_outside = len(re.findall(r'<p align="center">', text))
        print(f'  {ch_file.name}: {imgs} imgs, {figs_outside} centered blocks')
    else:
        print(f'  {ch_file.name}: (no changes)')
