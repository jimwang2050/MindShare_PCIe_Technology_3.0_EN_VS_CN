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
    """Return embedded image filenames for a page (sorted)."""
    if not EMB.exists():
        return []
    prefix = f"page{page:04d}_img"
    return sorted(p.name for p in EMB.glob(f"{prefix}*.png"))


def figures_in_range(start_page: int, end_page: int) -> dict[int, list[str]]:
    """Return all embedded images for pages in [start_page, end_page]."""
    result = {}
    for p in range(start_page, end_page + 1):
        figs = figures_on_page(p)
        if figs:
            result[p] = figs
    return result


def inject_into_chapter(md_path: Path, ch_num: int, ch_start: int,
                        ch_end: int, chapter_pages: dict[int, list[int]]) -> int:
    """Inject figure references into a chapter MD. Returns number injected."""
    text = md_path.read_text(encoding='utf-8')
    # Track which embedded images we've already inserted (avoid duplicates)
    used: set[str] = set()

    # Split into sections by <a id="sec-N-M">
    # Each section ends at next <a id="..."> or end-of-file
    section_pat = re.compile(r'(<a id="sec-(\d+)-(\d+)"></a>\s*\n##\s+[^\n]+)', re.MULTILINE)
    matches = list(section_pat.finditer(text))
    if not matches:
        return 0

    injected = 0
    new_parts = []
    last_end = 0

    for i, m in enumerate(matches):
        new_parts.append(text[last_end:m.start()])
        sec_start, sec_end = m.span()
        # Find this section's end (next section start or EOF)
        if i + 1 < len(matches):
            this_section_end = matches[i + 1].start()
        else:
            this_section_end = len(text)
        section_text = text[sec_start:this_section_end]
        # Find chunk number for this section
        section_n = i + 1
        chunk_n = find_chunk_for_section(ch_num, section_n, ch_start)
        # Find page
        page = chunk_first_page(chunk_n)
        figs_for_section = []
        if page:
            # Try exact page first
            figs_for_section = figures_on_page(page)
            # Fallback: search ±5 pages
            if not figs_for_section and chapter_pages:
                for delta in range(1, 6):
                    for offset in (page - delta, page + delta):
                        if offset in chapter_pages:
                            figs_for_section = figures_on_page(offset)
                            if figs_for_section:
                                page = offset
                                break
                    if figs_for_section:
                        break

        # Build <img> block
        img_lines = []
        for fname in figs_for_section:
            if fname in used:
                continue
            used.add(fname)
            img_lines.append("")
            img_lines.append(f'<img src="figures/embedded/{fname}" alt="Figure from page {page}" width="700">')
            img_lines.append("")

        # Insert after the bilingual table — find the next </table> and insert after
        insertion = ""
        if img_lines:
            insertion = "\n" + "\n".join(img_lines) + "\n"

        new_section = section_text + insertion
        new_parts.append(new_section)
        last_end = this_section_end
        injected += len(img_lines) // 3  # 3 lines per figure (blank + img + blank)

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
        # Compute chapter pages
        if ch_num in ch_ranges:
            p_min, p_max = ch_ranges[ch_num]
        else:
            p_min, p_max = 0, 0
        chapter_pages = {}
        for p in range(p_min, p_max + 1):
            figs = figures_on_page(p)
            if figs:
                chapter_pages[p] = figs
        n = inject_into_chapter(md, ch_num, ch_start, ch_end, chapter_pages)
        total_injected += n
        print(f"  Ch {ch_num:>3d} ({c['en'][:35]:<35s}): injected {n} figure(s)")

    print(f"\nTotal figures injected: {total_injected}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
