#!/usr/bin/env python3
"""
V2: Global figure restructuring. Find ALL <img> tags, extract with captions,
place as standalone centered blocks outside bilingual tables.
Fix column widths and blank areas.
"""

import re
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')

NEW_TABLE_HEAD = ('<table style="width:100%; table-layout:fixed">\n'
                  '<colgroup><col style="width:50%"><col style="width:50%"></colgroup>\n'
                  '<thead><tr><th>🇬🇧 English</th>'
                  '<th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>\n'
                  '<tbody><tr>')
TABLE_FOOT = '</tr></tbody></table>'


def build_figure_block(img_path, caption, page_num):
    """Build standalone centered figure block."""
    parts = []
    if caption:
        parts.append(f'\n<p align="center"><b>{caption}</b></p>')
    img_to_use = img_path
    tight = img_path.replace('.png', '_tight.png')
    if (ROOT / tight).exists():
        img_to_use = tight
    parts.append(f'\n<p align="center"><img src="{img_to_use}" width="700"></p>')
    if page_num:
        parts.append(f'\n<p align="center"><sub>📄 <a href="{img_path}">Page {page_num}</a></sub></p>')
    return ''.join(parts) + '\n'


def restructure_file(filepath):
    text = filepath.read_text(encoding='utf-8')
    original = text

    # ── Step 1: Replace old table headers ──
    text = re.sub(
        r'<table>\s*<thead><tr><th width="50%">🇬🇧 English</th>'
        r'<th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>\s*<tbody><tr>',
        NEW_TABLE_HEAD,
        text
    )

    # ── Step 2: Find ALL <img> tags globally ──
    img_pattern = re.compile(r'<img src="([^"]+)"[^>]*>')

    # Process imgs from end to start (to preserve positions)
    img_positions = list(img_pattern.finditer(text))

    for m in reversed(img_positions):
        img_path = m.group(1)
        page_num = None
        pm = re.search(r'page(\d+)', img_path)
        if pm:
            page_num = int(pm.group(1))

        # Find caption in the 400 chars before this image
        before = text[max(0, m.start()-400):m.start()]
        caption = None
        cap_match = re.search(
            r'(?:_?(Figure|Table)\s+[^\n]+?_?)\s*$',
            before,
            re.MULTILINE
        )
        if cap_match:
            caption = cap_match.group(1).strip().strip('_').strip()

        # Build figure block
        fig_block = build_figure_block(img_path, caption, page_num)

        # Determine where to place the figure block:
        # 1. Find the nearest table boundary before this img
        # 2. Place figure block right BEFORE the closing </tr></tbody></table> or at current position
        after = text[m.end():m.end()+200]

        # If image is inside a table, close table, insert figure, reopen
        # Find preceding <td> and following </td>
        prev_td_close = text.rfind('</td>', 0, m.start())
        next_td_open = text.find('<td', m.end())
        in_table = (prev_td_close > 0 and
                    text.rfind('<td', 0, prev_td_close) > 0 and
                    text.find('</tr></tbody></table>', prev_td_close) > m.end())

        # Find a good insertion point: before next ## heading or section break
        next_section = text.find('\n<a id="sec-', m.end())
        next_heading = text.find('\n## ', m.end())

        # Remove the img tag and its surrounding whitespace/newlines
        # Also remove the caption line if we captured it
        start_remove = m.start()
        end_remove = m.end()

        # Extend back to include caption line
        if caption and cap_match:
            cap_start = text.rfind(cap_match.group(1), 0, m.start())
            if cap_start >= 0 and (m.start() - cap_start) < 500:
                start_remove = cap_start

        # Extend forward to include trailing <br> and whitespace
        while end_remove < len(text) and text[end_remove] in ' \n':
            end_remove += 1
        if text[end_remove:end_remove+4] == '<br>':
            end_remove += 4
        while end_remove < len(text) and text[end_remove] in ' \n':
            end_remove += 1

        # Build replacement
        replacement = fig_block

        # If we're inside a table, wrap with table close/open
        if in_table:
            replacement = f'{TABLE_FOOT}\n{replacement}\n{NEW_TABLE_HEAD}\n'

        text = text[:start_remove] + replacement + text[end_remove:]

    # ── Step 3: Clean up ──
    # Remove empty table segments created by extraction
    text = re.sub(
        r'</tr></tbody></table>\s*\n\s*' +
        re.escape(NEW_TABLE_HEAD.strip()) +
        r'\s*\n\s*<td>\n\n\s*\n\n</td>\n<td[^>]*>\n\n\s*\n\n</td>\s*\n\s*</tr></tbody></table>',
        '',
        text,
        flags=re.DOTALL
    )

    # Remove orphaned table open/close with empty content
    text = re.sub(
        r'<table[^>]*>\s*\n\s*<colgroup>[^<]*</colgroup>\s*\n\s*<thead>.*?</thead>\s*\n\s*<tbody><tr>\s*\n\s*<td>\n\n\s*\n\n</td>\n<td[^>]*>\n\n\s*\n\n</td>\s*\n\s*</tr></tbody></table>',
        '',
        text,
        flags=re.DOTALL
    )

    # Clean excessive blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # Remove PDF page headers
    text = re.sub(r'\n\n\*\*(?:PCI Express(?: 3\.0)? Technology|Chapter \d+: [^*]+)\*\*\s*\n\n', '\n\n', text)

    if text != original:
        filepath.write_text(text, encoding='utf-8')
        imgs = len(re.findall(r'<img src=', text))
        centered = len(re.findall(r'<p align="center">', text))
        return imgs, centered
    return None, None


# Process all chapters
for ch_file in sorted(ROOT.glob('MindShare_PCIe_ch[0-9]*.md')):
    imgs, centered = restructure_file(ch_file)
    if imgs is not None:
        print(f'  {ch_file.name}: {imgs} imgs, {centered} centered blocks')
    else:
        print(f'  {ch_file.name}: (no changes)')
