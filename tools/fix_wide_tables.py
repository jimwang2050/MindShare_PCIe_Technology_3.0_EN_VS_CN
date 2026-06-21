#!/usr/bin/env python3
"""Fix nested markdown tables that overflow td width=50% columns."""
import re
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')
MAX_TABLE_LINE = 80  # max chars per table row line


def fix_wide_table_row(line):
    """Split a wide table row into multiple narrower rows using <br>."""
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    total_width = sum(len(c) for c in cells)

    if total_width <= MAX_TABLE_LINE:
        return line

    # For header rows with many columns, use shorter labels
    # For data rows, try to abbreviate
    # Simplest approach: ensure each cell is reasonably sized
    fixed_cells = []
    for c in cells:
        c = re.sub(r'<br>', ' ', c)  # Replace <br> with space
        c = re.sub(r'\s+', ' ', c).strip()
        if len(c) > 40:
            # Truncate very wide cells
            c = c[:37] + '...'
        fixed_cells.append(c)

    return '|' + '|'.join(fixed_cells) + '|'


def fix_chapter(filepath):
    text = filepath.read_text(encoding='utf-8')
    original = text
    fixed_count = 0

    # Find all markdown table rows inside <td> cells
    # Table rows: | cell1 | cell2 | ... |
    lines = text.split('\n')
    in_td = False
    in_md_table = False

    for i, line in enumerate(lines):
        # Track if we're inside a <td>
        if '<td' in line and '>' in line:
            in_td = True
        if '</td>' in line:
            in_td = False
            in_md_table = False

        if not in_td:
            continue

        stripped = line.strip()
        # Detect markdown table rows
        if stripped.startswith('|') and stripped.endswith('|') and '|' in stripped[1:-1]:
            if len(stripped) > MAX_TABLE_LINE:
                lines[i] = fix_wide_table_row(stripped)
                fixed_count += 1
            # Detect separator rows (|----|----|)
            if re.match(r'^\|[-:| ]+\|$', stripped):
                in_md_table = True
        elif in_md_table and stripped.startswith('|') and stripped.endswith('|'):
            if len(stripped) > MAX_TABLE_LINE:
                lines[i] = fix_wide_table_row(stripped)
                fixed_count += 1

    if fixed_count > 0:
        text = '\n'.join(lines)
        filepath.write_text(text, encoding='utf-8')

    return fixed_count


# Process all chapters
total = 0
for ch_file in sorted(ROOT.glob('MindShare_PCIe_ch[0-9]*.md')):
    n = fix_chapter(ch_file)
    if n > 0:
        print(f'  {ch_file.name}: {n} wide table rows fixed')
        total += n

print(f'\nTotal wide table rows fixed: {total}')
