#!/usr/bin/env python3
"""Fix wide table layout in chapter MDs by wrapping long <td> content lines."""

import re, textwrap
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')
MAX_WIDTH = 140

for f in sorted(ROOT.glob('MindShare_PCIe_ch*.md')):
    text = f.read_text(encoding='utf-8')
    old_lines = len(text.splitlines())
    old_long = sum(1 for l in text.splitlines() if len(l) > 200)

    if old_long == 0:
        continue

    # Re-wrap long lines inside <td>...</td>
    def wrap_td(match):
        td_open = match.group(1)
        content = match.group(2)
        td_close = match.group(3)
        paras = content.split('\n\n')
        wrapped = []
        for p in paras:
            lines = p.split('\n')
            new_lines = []
            for line in lines:
                if len(line) > MAX_WIDTH:
                    new_lines.append(textwrap.fill(line, width=MAX_WIDTH,
                                                   break_long_words=False,
                                                   break_on_hyphens=False))
                else:
                    new_lines.append(line)
            wrapped.append('\n'.join(new_lines))
        return td_open + '\n\n'.join(wrapped) + td_close

    text = re.sub(r'(<td(?:\s[^>]*)?>)(.*?)(</td>)', wrap_td, text, flags=re.DOTALL)

    new_lines = len(text.splitlines())
    new_long = sum(1 for l in text.splitlines() if len(l) > 200)

    f.write_text(text, encoding='utf-8')
    print(f'  {f.name}: {old_lines}→{new_lines} lines, {old_long}→{new_long} long lines')
