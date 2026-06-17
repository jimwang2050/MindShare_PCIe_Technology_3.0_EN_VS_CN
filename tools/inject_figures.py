#!/usr/bin/env python3
"""Inject <img> figure references into chapter MDs.

Algorithm:
1. Load `figures/page_chapter.json` to get page → chapter mapping.
2. For each chapter MD, parse sections (`<a id="sec-N-M">` → `## N.M ...`).
3. For each section N.M:
   - Find the chunk number (from section sequence in chapter)
   - Look up the chunk's first page anchor (`**NNN**`)
   - Find embedded images on that page in `figures/embedded/`
   - Insert `<img src="figures/embedded/pageNNNN_imgM.png">` after the
     section's bilingual table, on its own line with blank lines around.
4. Re-merge book.md at the end.

Figure filenames are matched against `figures/embedded/page{page:04d}_img{N}.png`.
Figures not found on the section's page fall back to neighboring pages
in the same chapter (±5 pages).

Usage:
    python3 tools/inject_figures.py
    python3 tools/inject_figures.py --ch 5    # only chapter 5
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EMB = ROOT / "figures" / "embedded"
CHAPTERS_DIR = ROOT


def find_chunk_for_section(ch_num: int, section_idx: int, ch_start: int) -> int:
    """Map section index (1-based within chapter) → chunk number."""
    return ch_start + section_idx - 1


def chunk_first_page(chunk_n: int) -> int | None:
    """Find first '**NNN**' page anchor in a chunk."""
    p = ROOT / "chunks" / f"chunk{chunk_n:04d}.md"
    if not p.exists():
        return None
    text = p.read_text(encoding='utf-8', errors='ignore')
    for m in re.finditer(r"\*\*\s*(\d{1,4})\s*\*\*", text):
        page = int(m.group(1))
        if 1 <= page <= 1057:
            return page
    return None


def figures_on_page(page: int) -> list[str]:
    """Return figure filenames for a page, preferring tight crops.

    For each image on the page, prefer `pageNNNN_imgM_tight.png` if it
    exists; otherwise fall back to the original embedded bitmap
    `pageNNNN_imgM.png`. If no embedded images, fall back to the
    full-page render `figures/page/pageNNNN.png`.
    """
    if not EMB.exists():
        return []
    tight = set(p.name for p in EMB.glob(f"page{page:04d}_img*_tight.png"))
    out = []
    # First add all tight crops
    for t in sorted(tight):
        out.append(t)
    # Then add originals only if no tight version exists
    for orig in sorted(p.name for p in EMB.glob(f"page{page:04d}_img*.png")):
        if orig.endswith("_tight.png"):
            continue
        tight_name = orig.replace(".png", "_tight.png")
        if tight_name not in tight:
            out.append(orig)
    # If no embedded images found, fall back to full-page render
    if not out:
        page_render = ROOT / "figures" / "page" / f"page{page:04d}.png"
        if page_render.exists():
            out.append(f"../page/page{page:04d}.png")  # relative path
    return out


def figures_in_range(start_page: int, end_page: int) -> dict[int, list[str]]:
    """Return all embedded images for pages in [start_page, end_page]."""
    result = {}
    for p in range(start_page, end_page + 1):
        figs = figures_on_page(p)
        if figs:
            result[p] = figs
    return result


def all_figures_in_chapter(ch_min: int, ch_max: int) -> list[tuple[int, str]]:
    """Return all figures for a chapter's page range, sorted by page.

    Each entry is (page_number, figure_filename). Searches both
    embedded/ (tight + original) and page/ (full-page render) dirs.
    """
    out = []
    for p in range(ch_min, ch_max + 1):
        # Tight crops first (preferred)
        for tight in sorted((EMB).glob(f"page{p:04d}_img*_tight.png")):
            out.append((p, tight.name))
        # Originals (only if no tight)
        tight_names = {t.name for t in (EMB).glob(f"page{p:04d}_img*_tight.png")}
        for orig in sorted((EMB).glob(f"page{p:04d}_img*.png")):
            if orig.name.endswith("_tight.png"):
                continue
            tight_name = orig.name.replace(".png", "_tight.png")
            if tight_name not in tight_names:
                out.append((p, orig.name))
        # Full-page render fallback
        page_render = ROOT / "figures" / "page" / f"page{p:04d}.png"
        if page_render.exists():
            # Only add if no embedded images on this page
            has_embedded = any(1 for _ in (EMB).glob(f"page{p:04d}_img*.png"))
            if not has_embedded:
                out.append((p, f"page/page{p:04d}.png"))  # page/ subpath with pageNNNN.png name
    return out


def inject_into_chapter(md_path: Path, ch_num: int, ch_start: int,
                        ch_end: int, ch_pages: tuple[int, int]) -> int:
    """Inject figure references into a chapter MD. Returns number injected.

    Strategy: collect ALL figures for the chapter's page range, then
    distribute them evenly across sections (one figure per section, in
    order). This handles the case where chunk→page mapping via the
    **NNN** marker is unreliable.
    """
    text = md_path.read_text(encoding='utf-8')
    used: set[str] = set()

    section_pat = re.compile(r'(<a id="sec-(\d+)-(\d+)"></a>\s*\n##\s+[^\n]+)', re.MULTILINE)
    matches = list(section_pat.finditer(text))
    if not matches:
        return 0

    # Collect all figures for the chapter, dedup by filename
    seen_figs: set[str] = set()
    figures: list[tuple[int, str]] = []
    for page, fname in all_figures_in_chapter(*ch_pages):
        if fname in seen_figs:
            continue
        seen_figs.add(fname)
        figures.append((page, fname))

    if not figures:
        return 0

    injected = 0
    new_parts = []
    last_end = 0

    # Distribute figures: assign one figure per section (round-robin
    # over the section list, in figure order)
    fig_iter = iter(figures)
    fig_pool = list(figures)

    for i, m in enumerate(matches):
        new_parts.append(text[last_end:m.start()])
        sec_start = m.start()
        if i + 1 < len(matches):
            this_section_end = matches[i + 1].start()
        else:
            this_section_end = len(text)
        section_text = text[sec_start:this_section_end]

        # Pick the next figure for this section
        img_lines = []
        if i < len(fig_pool):
            page, fname = fig_pool[i]
            # If it's a page render, prefix with figures/
            if fname.startswith("page/"):
                img_path = f"figures/{fname}"
            else:
                img_path = f"figures/embedded/{fname}"
            img_lines.append("")
            img_lines.append(f'<img src="{img_path}" alt="Figure from page {page}" width="700">')
            img_lines.append("")
            injected += 1

        insertion = ""
        if img_lines:
            insertion = "\n" + "\n".join(img_lines) + "\n"

        new_section = section_text + insertion
        new_parts.append(new_section)
        last_end = this_section_end

    new_parts.append(text[last_end:])
    md_path.write_text("".join(new_parts), encoding='utf-8')
    return injected


def chapter_page_ranges() -> dict[int, tuple[int, int]]:
    """For each chapter, compute its [min_page, max_page] range."""
    with open(ROOT / "figures" / "chapter_pages.json", encoding='utf-8') as f:
        cp = json.load(f)
    result = {}
    for ch_str, info in cp.items():
        ch = int(ch_str)
        if "min" in info and "max" in info:
            result[ch] = (info["min"], info["max"])
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ch", type=int, default=None)
    args = parser.parse_args()

    idx = json.loads((ROOT / "chapter_index.json").read_text(encoding='utf-8'))
    ch_ranges = chapter_page_ranges()

    print("=" * 70)
    print("MindShare PCIe 3.0 — Figure Auto-Injection")
    print("=" * 70)

    total_injected = 0
    for c in idx["chapters"]:
        if args.ch is not None and c["ch"] != args.ch:
            continue
        ch_num = c["ch"]
        ch_start, ch_end = c["start"], c["end"]
        # Find MD
        candidates = sorted(CHAPTERS_DIR.glob(f"MindShare_PCIe_ch{ch_num:02d}_*.md"))
        if not candidates:
            continue
        md = candidates[0]
        # Chapter page range from figures/chapter_pages.json
        ch_pages = ch_ranges.get(ch_num, (0, 0))
        if ch_pages == (0, 0):
            # Fallback: use a wide range so pages 0-end includes everything
            ch_pages = (1, 1057)
        n = inject_into_chapter(md, ch_num, ch_start, ch_end, ch_pages)
        total_injected += n
        print(f"  Ch {ch_num:>3d} ({c['en'][:35]:<35s}): injected {n} figure(s)")

    print(f"\nTotal figures injected: {total_injected}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
