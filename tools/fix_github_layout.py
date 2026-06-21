#!/usr/bin/env python3
"""
Fix GitHub rendering: table width, blank areas, td width attributes.
1. Remove table-layout:fixed → GitHub doesn't support it well
2. Add width="50%" to <td> cells → GitHub respects this
3. Remove colgroup → GitHub strips it
4. Clean blank areas from figure extraction
"""

import re
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')


def fix_chapter(filepath):
    text = filepath.read_text(encoding='utf-8')
    original = text

    # ── 1. Replace complex table headers ──
    # Pattern A: with colgroup
    text = re.sub(
        r'<table style="width:100%;table-layout:fixed">\s*\n'
        r'<colgroup><col style="width:50%"><col style="width:50%"></colgroup>\s*\n',
        '<table>\n',
        text
    )
    # Pattern B: plain table-layout:fixed
    text = re.sub(
        r'<table style="width:100%;table-layout:fixed">\s*\n?',
        '<table>\n',
        text
    )

    # ── 2. Ensure <td> cells have width="50%" ──
    text = re.sub(
        r'<td>\n\n',
        '<td width="50%">\n\n',
        text
    )
    text = re.sub(
        r'<td style="background-color:#e8e8e8">\n\n',
        '<td width="50%">\n\n',
        text
    )

    # ── 3. Clean excessive blank lines inside <td> ──
    # Remove 3+ blank lines inside cells
    text = re.sub(r'(<td[^>]*>)\n{3,}', r'\1\n\n', text)
    text = re.sub(r'\n{3,}(</td>)', r'\n\n\1', text)
    # Overall cleanup
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # ── 4. Remove orphaned empty table segments ──
    text = re.sub(
        r'<table>\s*\n\s*<thead>.*?</thead>\s*\n\s*<tbody><tr>\s*\n'
        r'\s*<td width="50%">\s*\n\s*\n\s*\n\s*</td>\s*\n'
        r'\s*<td width="50%">\s*\n\s*\n\s*\n\s*</td>\s*\n'
        r'\s*</tr>\s*\n\s*</tbody>\s*\n\s*</table>',
        '',
        text,
        flags=re.DOTALL
    )

    if text != original:
        filepath.write_text(text, encoding='utf-8')
        tables = len(re.findall(r'<table>', text))
        td50 = len(re.findall(r'<td width="50%">', text))
        return tables, td50
    return None, None


# Process all chapters
for ch_file in sorted(ROOT.glob('MindShare_PCIe_ch[0-9]*.md')):
    result = fix_chapter(ch_file)
    if result[0] is not None:
        t, td = result
        print(f'  {ch_file.name}: {t} tables, {td} td[width=50%]')
    else:
        print(f'  {ch_file.name}: (no changes)')
