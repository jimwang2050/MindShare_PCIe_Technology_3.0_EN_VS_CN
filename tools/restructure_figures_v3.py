#!/usr/bin/env python3
"""
V3: Extract figures from inside <td> cells to standalone centered blocks.
Simple, targeted approach: process each <td>...</td> block independently.
"""

import re
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')

NEW_TH = ('<table style="width:100%;table-layout:fixed">\n'
          '<colgroup><col style="width:50%"><col style="width:50%"></colgroup>\n'
          '<thead><tr><th>🇬🇧 English</th>'
          '<th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>\n'
          '<tbody><tr>')
OLD_TH_PAT = (
    r'<table>\s*<thead><tr><th width="50%">🇬🇧 English</th>'
    r'<th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>\s*<tbody><tr>'
)


def extract_figures_from_cell(cell_text):
    """Find (caption, img_path) pairs in cell text and return cleaned text + figure blocks."""
    # Pattern: italic or underscore caption followed by <img> tag
    fig_pattern = re.compile(
        r'([*_]?(?:Figure|Table)\s+[^*_\n]+?[*_]?)\s*\n'
        r'<img src="([^"]+)"[^>]*>\s*(?:<br>)?\s*\n?',
        re.DOTALL
    )

    figures = []
    clean_text = cell_text

    for m in fig_pattern.finditer(cell_text):
        caption = m.group(1).strip().strip('*_').strip()
        img_path = m.group(2)

        page_num = None
        pm = re.search(r'page(\d+)', img_path)
        if pm:
            page_num = int(pm.group(1))

        img_to_use = img_path
        tight = img_path.replace('.png', '_tight.png')
        if (ROOT / tight).exists():
            img_to_use = tight

        figures.append((caption, img_to_use, img_path, page_num))

    # Remove all figure blocks from text
    clean_text = fig_pattern.sub('', cell_text)

    # Clean up residual blank lines
    clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)

    return clean_text.strip(), figures


def build_figure_html(caption, img_src, orig_path, page_num):
    """Build standalone centered figure HTML block."""
    parts = []
    parts.append(f'\n<p align="center"><b>{caption}</b></p>')
    parts.append(f'<p align="center"><img src="{img_src}" width="700"></p>')
    if page_num:
        parts.append(f'<p align="center"><sub>📄 <a href="{orig_path}">Page {page_num}</a></sub></p>')
    return '\n'.join(parts) + '\n'


def restructure_chapter(filepath):
    text = filepath.read_text(encoding='utf-8')
    original = text

    # Step 1: Replace old table header with fixed-width
    text = re.sub(OLD_TH_PAT, NEW_TH, text)

    # Step 2: Find all <td>...</td> blocks and extract figures
    td_pattern = re.compile(
        r'<td(?:\s[^>]*)?>\n\n(.*?)\n\n</td>',
        re.DOTALL
    )

    def process_td(match):
        attrs = match.group(0)[:match.group(0).find('>')+1]
        cell_text = match.group(1)
        clean, figures = extract_figures_from_cell(cell_text)

        if not figures:
            # No figures - return original
            return match.group(0)

        # Has figures - rebuild
        result = f'<td>\n\n{clean}\n\n</td>'
        return result

    # Process ZHS cells
    zh_td_pattern = re.compile(
        r'<td style="background-color:#e8e8e8">\n\n(.*?)\n\n</td>',
        re.DOTALL
    )

    # Find all paired (EN td, ZH td) blocks
    section_pattern = re.compile(
        r'(<td>\n\n.*?\n\n</td>)\n'
        r'(<td style="background-color:#e8e8e8">\n\n.*?\n\n</td>)',
        re.DOTALL
    )

    def process_section(m):
        en_td = m.group(1)
        zh_td_full = m.group(2)

        # Extract ZH cell content
        zh_inner = re.search(r'<td style="background-color:#e8e8e8">\n\n(.*?)\n\n</td>',
                             zh_td_full, re.DOTALL)
        if not zh_inner:
            return m.group(0)

        zh_text = zh_inner.group(1)
        clean_zh, figures = extract_figures_from_cell(zh_text)

        if not figures:
            return m.group(0)

        # Build figure blocks
        fig_blocks = []
        for caption, img_src, orig_path, page_num in figures:
            fig_blocks.append(build_figure_html(caption, img_src, orig_path, page_num))

        # Rebuild: EN td + ZH td (cleaned) + figures outside
        result = f'{en_td}\n<td style="background-color:#e8e8e8">\n\n{clean_zh}\n\n</td>'
        result += f'\n</tr></tbody></table>\n'
        result += '\n'.join(fig_blocks)
        result += f'\n{NEW_TH}\n'

        return result

    text = section_pattern.sub(process_section, text)

    # Step 3: Clean up
    # Remove empty table segments
    text = re.sub(
        r'</tr></tbody></table>\s*\n\s*' +
        re.escape(NEW_TH.strip()) +
        r'\s*\n\s*<td>\n\n\s*\n\n</td>\n<td[^>]*>\n\n\s*\n\n</td>',
        '',
        text,
        flags=re.DOTALL
    )
    # Clean excessive blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    # Remove orphaned page headers
    text = re.sub(
        r'\n\n\*\*(?:PCI Express(?: 3\.0)? Technology|Chapter \d+: [^*]+)\*\*\s*\n\n',
        '\n\n', text
    )

    if text != original:
        filepath.write_text(text, encoding='utf-8')
        imgs = len(re.findall(r'<img src=', text))
        figs = len(re.findall(r'<p align="center"><b>', text))
        return imgs, figs
    return None, None


# Process all chapters
for ch_file in sorted(ROOT.glob('MindShare_PCIe_ch[0-9]*.md')):
    result = restructure_chapter(ch_file)
    if result[0] is not None:
        imgs, figs = result
        print(f'  {ch_file.name}: {imgs} imgs, {figs} figures extracted')
    else:
        print(f'  {ch_file.name}: (no changes)')
