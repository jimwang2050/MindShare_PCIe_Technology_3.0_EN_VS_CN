#!/usr/bin/env python3
"""
Split each section's EN/ZH text at ## heading boundaries into separate aligned table rows.
This fixes paragraph alignment and reduces blank spaces.
"""

import re
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')

ROW_HEADER = ('<table>\n<thead><tr><th width="50%">🇬🇧 English</th>'
              '<th width="50%">🇨🇳 中文</th></tr></thead>\n<tbody>')


def split_at_headings(text):
    """Split text at ## heading boundaries. Returns list of text blocks."""
    # Split on ## headings, keeping the heading with its following content
    # Pattern: split before each ## (except at start)
    parts = re.split(r'(\n## .+?\n)', text)
    blocks = []
    current = parts[0] if parts else ''

    for i in range(1, len(parts), 2):
        heading = parts[i] if i < len(parts) else ''
        body = parts[i+1] if i+1 < len(parts) else ''

        if current.strip():
            blocks.append(current)
        current = heading + body

    if current.strip():
        blocks.append(current)

    return blocks if blocks else [text]


def align_and_build_rows(en_text, zh_text):
    """Split EN and ZH at headings, build aligned table rows."""
    en_blocks = split_at_headings(en_text)
    zh_blocks = split_at_headings(zh_text)

    # If both are single blocks, return as-is
    if len(en_blocks) == 1 and len(zh_blocks) == 1:
        return (f'<td width="50%">\n\n{en_text.strip()}\n\n</td>\n'
                f'<td width="50%">\n\n{zh_text.strip()}\n\n</td>')

    # Pad shorter list with empty strings
    max_len = max(len(en_blocks), len(zh_blocks))
    while len(en_blocks) < max_len:
        en_blocks.append('')
    while len(zh_blocks) < max_len:
        zh_blocks.append('')

    rows = []
    for i in range(max_len):
        en_block = en_blocks[i].strip()
        zh_block = zh_blocks[i].strip()

        # Skip completely empty rows
        if not en_block and not zh_block:
            continue

        rows.append(
            f'<tr>\n'
            f'<td width="50%">\n\n{en_block}\n\n</td>\n'
            f'<td width="50%">\n\n{zh_block}\n\n</td>\n'
            f'</tr>'
        )

    return '\n'.join(rows)


def restructure_chapter(filepath):
    text = filepath.read_text(encoding='utf-8')
    original = text

    # Find table sections: <td>EN</td><td>ZH</td> pairs
    # These are inside <table>...</table> blocks
    section_pattern = re.compile(
        r'<td width="50%">\n\n(.*?)\n\n</td>\n'
        r'<td width="50%">\n\n(.*?)\n\n</td>',
        re.DOTALL
    )

    split_count = 0

    def process_section(m):
        nonlocal split_count
        en_text = m.group(1)
        zh_text = m.group(2)

        result = align_and_build_rows(en_text, zh_text)

        # Count if we actually split
        rows = result.count('<tr>')
        if rows > 1:
            split_count += 1

        return result

    text = section_pattern.sub(process_section, text)

    # Now wrap split rows in proper table blocks
    # Replace consecutive <tr>...</tr> groups with <table>...</table> wrappers
    # Pattern: find groups of <tr> lines and wrap them
    text = re.sub(
        r'(?<!</tr>\n)((?:\s*<tr>.*?</tr>\s*)+)',
        lambda m: f'{ROW_HEADER}\n{m.group(1)}\n</tbody>\n</table>',
        text,
        flags=re.DOTALL
    )

    # Clean up: remove duplicate table wrappers
    text = re.sub(r'</tbody>\n</table>\s*\n\s*<table>[^<]*<tbody>', '', text, flags=re.DOTALL)

    # Clean excessive blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # Fix: ensure table headers are proper
    # Replace bare <tr> groups with proper table wrapper
    # Pattern: consecutive <tr> not inside <table>
    def wrap_bare_rows(m):
        rows_content = m.group(0)
        return f'{ROW_HEADER}\n{rows_content}\n</tbody>\n</table>'

    text = re.sub(
        r'(?:^|\n\n)(<tr>.*?</tr>(?:\s*<tr>.*?</tr>)*)',
        wrap_bare_rows,
        text,
        flags=re.DOTALL
    )

    # Remove orphaned empty table wrappers
    text = re.sub(
        r'<table>\s*<thead>.*?</thead>\s*<tbody>\s*</tbody>\s*</table>',
        '',
        text,
        flags=re.DOTALL
    )

    # Final blank line cleanup
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    if text != original:
        filepath.write_text(text, encoding='utf-8')

    return split_count


# Process all chapters
total_split = 0
for ch_file in sorted(ROOT.glob('MindShare_PCIe_ch[0-9]*.md')):
    if 'ch00_' in ch_file.name:
        continue  # Skip Ch0 (English-only)
    n = restructure_chapter(ch_file)
    if n > 0:
        # Count total rows
        rows = len(re.findall(r'<tr>', ch_file.read_text(encoding='utf-8')))
        print(f'  {ch_file.name}: {n} sections split, {rows} total rows')
        total_split += n
    else:
        print(f'  {ch_file.name}: (no splits needed)')

print(f'\nTotal sections split: {total_split}')
