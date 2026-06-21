#!/usr/bin/env python3
"""
Phase 3: Inject figures into all chapter MDs.
Replace '==> picture ... intentionally omitted <==' placeholders with real <img> tags.

Strategy:
1. For chapters with figures/chapter_XX/ directory: use those images sequentially
2. For other chapters: use figures/page/ and figures/embedded/ matched by page range
3. Prefer _tight variants when available
"""

import json, re, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')
FIGURES = ROOT / 'figures'

# Load mappings
chapter_pages = json.loads((FIGURES / 'chapter_pages.json').read_text())
page_chapter = json.loads((FIGURES / 'page_chapter.json').read_text())
# page_chapter maps "70" → 1, etc.
page_chapter = {int(k): v for k, v in page_chapter.items()}


def get_chapter_images(ch_num):
    """Return list of (page_img, emb_img) tuples for a chapter."""
    # Find chapter directory
    ch_dirs = list(FIGURES.glob(f'chapter_{ch_num:02d}_*'))
    images = []

    if ch_dirs:
        ch_dir = ch_dirs[0]
        emb_dir = ch_dir / 'embedded'
        embs = sorted(emb_dir.glob('*.png')) if emb_dir.exists() else []
        page_dir = ch_dir / 'page'
        pages = sorted(page_dir.glob('*.png')) if page_dir.exists() else []

        page_imgs = defaultdict(list)
        for p in pages:
            num = re.search(r'page(\d+)', p.name)
            if num:
                page_imgs[int(num.group(1))].append(p)
        for e in embs:
            num = re.search(r'page(\d+)', e.name)
            if num:
                page_imgs[int(num.group(1))].append(e)

        # Flatten: return all unique page images, preferring _tight
        all_imgs = []
        seen_pages = set()
        for f in sorted(pages + embs):
            page_match = re.search(r'page(\d+)', f.name)
            if page_match:
                page_num = int(page_match.group(1))
                if page_num not in seen_pages:
                    seen_pages.add(page_num)
                    tight = str(f).replace('.png', '_tight.png')
                    if Path(tight).exists():
                        all_imgs.append(Path(tight))
                    else:
                        all_imgs.append(f)

        if all_imgs:
            return all_imgs

    # Fallback: use figures/page/ for this chapter's page range
    ch_pages = chapter_pages.get(str(ch_num), {})
    page_list = ch_pages.get('pages', [])
    if not page_list:
        return []

    all_imgs = []
    for pg in page_list:
        # Check tight first
        tight = FIGURES / 'page' / f'page{pg:04d}_tight.png'
        if tight.exists():
            all_imgs.append(tight)
        else:
            full = FIGURES / 'page' / f'page{pg:04d}.png'
            if full.exists():
                all_imgs.append(full)

    return all_imgs


def inject_figures(ch_file, ch_num):
    """Replace picture placeholders in ch_file with img tags from chapter images."""
    text = ch_file.read_text(encoding='utf-8')

    # Find all picture placeholders
    placeholder_pattern = re.compile(
        r'(\*?\*?==> picture \[(\d+) x (\d+)\] intentionally omitted <==\*?\*?.*?)'
        r'(?=\n)',
        re.DOTALL
    )

    placeholders = list(placeholder_pattern.finditer(text))
    if not placeholders:
        return 0

    images = get_chapter_images(ch_num)
    if not images:
        return 0

    # Replace placeholders from end to start to preserve positions
    count = 0
    for i, match in enumerate(reversed(placeholders)):
        idx = len(placeholders) - 1 - i
        img_idx = idx % len(images)  # cycle through available images

        img_path = images[img_idx]
        # Make path relative to ROOT
        rel_path = str(img_path.relative_to(ROOT))

        # Extract figure caption from before the placeholder
        before = text[:match.start()]
        caption = ''
        cap_match = re.search(r'_(Figure [^_]+)_\s*$', before, re.MULTILINE)
        if cap_match:
            caption = cap_match.group(1).strip()

        alt = caption if caption else f'Figure {idx+1}'
        replacement = f'<img src="{rel_path}" alt="{alt}" width="700">\n\n'

        # Also remove the picture text block if present
        end = match.end()
        if end < len(text) and 'Start of picture text' in text[end:end+100]:
            text_end = text.find('End of picture text', end)
            if text_end > 0:
                end = text_end + len('End of picture text') + len('**-----') + 1

        text = text[:match.start()] + replacement + text[end:]
        count += 1

    if count > 0:
        ch_file.write_text(text, encoding='utf-8')

    return count


# Process all chapters
for ch_file in sorted(ROOT.glob('MindShare_PCIe_ch[0-9]*.md')):
    ch_match = re.search(r'ch(\d+)', ch_file.name)
    if not ch_match:
        continue
    ch_num = int(ch_match.group(1))

    # Count placeholders before
    before = len(re.findall(r'intentionally omitted', ch_file.read_text(encoding='utf-8')))

    count = inject_figures(ch_file, ch_num)

    after = len(re.findall(r'intentionally omitted', ch_file.read_text(encoding='utf-8')))
    if before > 0:
        print(f'  Ch{ch_num}: {before} placeholders → {after} remaining ({count} replaced)')
