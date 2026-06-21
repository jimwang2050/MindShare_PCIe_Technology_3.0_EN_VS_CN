#!/usr/bin/env python3
"""Scan each chapter MD for ## N.X headings and rebuild the per-chapter TOC."""

import re, sys
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')

def rebuild_chapter_toc(ch_file):
    text = ch_file.read_text(encoding='utf-8')

    # Find all sections with their content
    section_pattern = re.compile(
        r'<a id="(sec-\d+-\d+)"></a>\n## (\d+\.\d+) (.+?)(?: \| (.+?))?\n'
        r'(.*?)'
        r'(?=\n<a id="sec-|$)',
        re.DOTALL
    )

    sections = []
    for m in section_pattern.finditer(text):
        anchor = m.group(1)
        sec_num = m.group(2)
        en_title = m.group(3).strip()
        zh_title = (m.group(4) or '').strip()
        body = m.group(5)

        # Try to find a descriptive heading from the English <td> content
        # Extract first meaningful ## heading, or first line of actual text
        desc = None
        td_match = re.search(r'<td>\s*\n(.*?)</td>', body, re.DOTALL)
        if td_match:
            td_content = td_match.group(1)
            # Look for any ## heading within td
            h_match = re.search(r'## \*?\*?(.+?)\*?\*?\s*\n', td_content)
            if h_match:
                desc = h_match.group(1).strip()
            else:
                # Fallback: first non-empty, non-tag line
                for line in td_content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('<') and len(line) > 5:
                        # Take first sentence or first ~50 chars
                        desc = re.sub(r'[#*_]+', '', line).strip()
                        break
        if desc:
            desc = re.sub(r'\*+', '', desc).strip()
            if len(desc) > 60:
                desc = desc[:57] + '...'
            en_title = desc

        sections.append((anchor, sec_num, en_title, zh_title))

    if not sections:
        return False

    # Build TOC
    toc_lines = ['## 📑 本章目录 (Table of Contents)\n']
    for anchor, sec_num, en_title, zh_title in sections:
        en_clean = en_title.replace('**', '').strip()
        zh_clean = zh_title.replace('**', '').strip() if zh_title else ''
        display = f'{sec_num} {en_clean}'
        if zh_clean and zh_clean != en_clean and zh_clean not in en_clean:
            display += f' — {zh_clean}'
        toc_lines.append(f'- [{display}](#{anchor})')

    new_toc = '\n'.join(toc_lines) + '\n'

    # Replace old TOC section
    old_toc_pattern = re.compile(
        r'## 📑 本章目录 \(Table of Contents\)\n.*?(?=\n<a id="sec-)',
        re.DOTALL
    )
    text = old_toc_pattern.sub(new_toc, text)

    ch_file.write_text(text, encoding='utf-8')
    return len(sections)

# Process all chapters except Ch0 (already has proper TOC)
for ch_file in sorted(ROOT.glob('MindShare_PCIe_ch[0-9]*.md')):
    if 'ch00_' in ch_file.name:
        continue  # Ch0 already has hand-crafted TOC
    count = rebuild_chapter_toc(ch_file)
    if count:
        print(f'  ✅ {ch_file.name}: {count} sections')
    else:
        print(f'  ⚠️  {ch_file.name}: no sections found')
