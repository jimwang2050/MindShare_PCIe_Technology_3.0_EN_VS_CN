#!/usr/bin/env python3
"""Renumber non-sequential section IDs in chapter MD files."""

import re
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')

for f in sorted(ROOT.glob('MindShare_PCIe_ch*.md')):
    ch_match = re.search(r'ch(\d+)', f.name)
    if not ch_match:
        continue
    ch_num = int(ch_match.group(1))

    text = f.read_text(encoding='utf-8')
    anchors = re.findall(rf'<a id="sec-{ch_num}-(\d+)"></a>', text)
    if not anchors:
        continue

    unique_nums = sorted(set(int(x) for x in anchors))
    expected = list(range(1, len(unique_nums) + 1))
    if unique_nums == expected:
        continue

    # Build old→new mapping
    mapping = {old: new for old, new in zip(unique_nums, expected)}
    print(f'  Ch{ch_num}: renumbering {len(mapping)} sections ({unique_nums} → {expected})')

    # Replace sec-N-X in all contexts (anchors, hrefs)
    text = re.sub(
        rf'(sec-{ch_num}-)(\d+)',
        lambda m: m.group(1) + str(mapping.get(int(m.group(2)), int(m.group(2)))),
        text
    )
    # Replace ## N.X headings
    text = re.sub(
        rf'(## {ch_num}\.)(\d+)( )',
        lambda m: m.group(1) + str(mapping.get(int(m.group(2)), int(m.group(2)))) + m.group(3),
        text
    )

    f.write_text(text, encoding='utf-8')

print('\nDone!')
