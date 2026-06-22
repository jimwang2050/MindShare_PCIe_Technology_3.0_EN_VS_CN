#!/usr/bin/env python3
"""Fix duplicate image alts in MindShare PCIe chapter files.

Problem: every <img> in a chapter has the same alt text (the alt from the
first figure was propagated to all subsequent images). This breaks GitHub
rendering and hurts accessibility.

Fix: derive a unique alt per image from its `src` path. The src encodes the
page number (e.g. `figures/chapter_X/page/page0468.png` or `figures/page/page0080.png`).
We use `Figure from page N` as the alt, which is unique and informative.
"""

import re
from pathlib import Path
from collections import Counter

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')


def derive_alt(src: str) -> str:
    """Extract page and image index from src and return a unique alt.

    Handles two src formats:
      - figures/embedded/page0004_img1_tight.png → "Figure from page 4 (img 1)"
      - figures/page/page0080.png                → "Figure from page 80"
    """
    m = re.search(r'page(\d+)_img(\d+)', src)
    if m:
        page = int(m.group(1))
        idx = m.group(2)
        return f"Figure from page {page} (img {idx})"
    m = re.search(r'page(\d+)\.png', src)
    if m:
        page = int(m.group(1))
        return f"Figure from page {page}"
    return "Figure"


def fix_chapter(text: str) -> tuple[str, dict]:
    """Replace duplicate alts with unique page-based alts."""
    # Find all <img> tags and their srcs
    pattern = re.compile(r'<img\s+([^>]*?)alt="([^"]*)"([^>]*?)>', re.DOTALL)

    # First pass: collect (full_match, src, old_alt) for each img
    matches = []
    for m in pattern.finditer(text):
        before, old_alt, after = m.group(1), m.group(2), m.group(3)
        full_attrs = before + after
        src_match = re.search(r'src="([^"]*)"', full_attrs)
        if not src_match:
            continue
        src = src_match.group(1)
        new_alt = derive_alt(src)
        matches.append((m.start(), m.end(), old_alt, new_alt, before, after))

    # Skip if all alts are already unique
    old_alts = [m[2] for m in matches]
    if len(set(old_alts)) == len(old_alts):
        return text, {'changed': False, 'count': 0}

    # Second pass: build new text with corrected alts
    # We do this by replacing from the end backwards to preserve indices
    new_text = text
    for start, end, old_alt, new_alt, before, after in reversed(matches):
        if new_alt != old_alt:
            new_tag = f'<img {before}alt="{new_alt}"{after}>'
            new_text = new_text[:start] + new_tag + new_text[end:]

    return new_text, {'changed': new_text != text, 'count': sum(1 for m in matches if m[3] != m[2])}


def main():
    chapters = sorted(ROOT.glob('MindShare_PCIe_ch[0-9]*.md'))
    print(f"Processing {len(chapters)} chapters\n")
    print(f"{'Chapter':70s} {'imgs':5s}  {'uniq-alts':10s}  status")
    print("-" * 110)

    total_fixed = 0
    total_alts_fixed = 0
    for f in chapters:
        text = f.read_text(encoding='utf-8')
        imgs = re.findall(r'<img\s+[^>]*alt="([^"]*)"[^>]*>', text)
        uniq_before = len(set(imgs))

        new_text, stats = fix_chapter(text)
        new_imgs = re.findall(r'<img\s+[^>]*alt="([^"]*)"[^>]*>', new_text)
        uniq_after = len(set(new_imgs))

        if stats['changed']:
            f.write_text(new_text, encoding='utf-8')
            total_fixed += 1
            total_alts_fixed += stats['count']
            status = f"✓ fixed {stats['count']} alts ({uniq_before}→{uniq_after})"
        else:
            status = "—"

        print(f"{f.name[:70]:70s} {len(imgs):5d}  {uniq_after:10d}  {status}")

    print()
    print(f"Total: {total_fixed} files updated, {total_alts_fixed} alt texts fixed")


if __name__ == '__main__':
    main()
