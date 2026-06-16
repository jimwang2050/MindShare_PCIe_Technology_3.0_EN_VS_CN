#!/usr/bin/env python3
"""Extract figures from MindShare PCI Express Technology 3.0 PDF.

Strategy (lightweight, suited for a GitHub repo):
1. Extract embedded raster images → `figures/embedded/page_NNNN_img_M.png`
2. Render full pages at 150 DPI for pages with embedded images or
   page-number anchors found in chunks → `figures/page_NNNN.png`
3. Skip pure-text pages to keep repo size manageable.

Usage:
    python3 tools/extract_figures.py             # default
    python3 tools/extract_figures.py --full      # also render every page
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
PDF = "/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCI Express Technology 3.0.pdf"
OUT = ROOT / "figures"
EMBED_DIR = OUT / "embedded"
PAGE_DIR = OUT / "page"
CHUNKS_DIR = ROOT / "chunks"


def find_pages_with_diagrams(doc: fitz.Document) -> set[int]:
    """Heuristic: pages with embedded images OR contain 'Figure X-Y' caption text."""
    pages = set()
    for i, page in enumerate(doc):
        if page.get_images(full=True):
            pages.add(i + 1)
        text = page.get_text() or ""
        if re.search(r"\bFigure\s+\d+-\d+\b", text):
            pages.add(i + 1)
    return pages


def extract_embedded_images(doc: fitz.Document, pages: set[int]) -> int:
    """Extract embedded raster images."""
    EMBED_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    for page_no in sorted(pages):
        page = doc[page_no - 1]
        for img_idx, img in enumerate(page.get_images(full=True), 1):
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.colorspace and pix.colorspace.n >= 4:  # CMYK
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                out_path = EMBED_DIR / f"page{page_no:04d}_img{img_idx}.png"
                pix.save(str(out_path))
                n += 1
            except Exception as e:
                print(f"  ! page {page_no} img {img_idx}: {e}")
    return n


def render_pages(doc: fitz.Document, pages: set[int], dpi: int = 150) -> int:
    """Render selected pages as PNGs at given DPI."""
    PAGE_DIR.mkdir(parents=True, exist_ok=True)
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    n = 0
    for page_no in sorted(pages):
        out_path = PAGE_DIR / f"page{page_no:04d}.png"
        if out_path.exists():
            continue
        page = doc[page_no - 1]
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        pix.save(str(out_path))
        n += 1
    return n


def page_to_chapter_map() -> dict[int, int]:
    """Build page→chapter map by parsing first page-number anchors in chunks.

    For each chunk, find the first page-number-like token ("**NNN**") and
    pair it with the chapter that contains the chunk.
    """
    import json
    idx = json.loads((ROOT / "chapter_index.json").read_text(encoding='utf-8'))
    chunk_pages: dict[int, int] = {}  # chunk_num → page
    for fn in sorted(CHUNKS_DIR.glob("chunk*.md")):
        n = int(fn.stem[5:])
        text = fn.read_text(encoding='utf-8', errors='ignore')
        # Find first "**NNN**" page marker (3 digits, surrounded by **)
        m = re.search(r"\*\*\s*(\d{1,4})\s*\*\*", text)
        if m:
            chunk_pages[n] = int(m.group(1))

    # For each chapter, assign chunks to pages
    page_chapter: dict[int, int] = {}
    for c in idx["chapters"]:
        chunk_nums = list(range(c["start"], c["end"] + 1))
        ch_pages = [chunk_pages.get(n) for n in chunk_nums if chunk_pages.get(n)]
        if not ch_pages:
            continue
        for p in range(min(ch_pages), max(ch_pages) + 1):
            page_chapter[p] = c["ch"]
    return page_chapter


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true",
                        help="render every page (large output)")
    parser.add_argument("--dpi", type=int, default=150)
    args = parser.parse_args()

    print(f"PDF: {PDF}")
    doc = fitz.open(PDF)
    print(f"Pages: {doc.page_count}")

    diagram_pages = find_pages_with_diagrams(doc)
    print(f"Pages with diagrams/images: {len(diagram_pages)}")

    # 1. Embedded images
    print("\n[1/2] Extracting embedded raster images...")
    n_embedded = extract_embedded_images(doc, diagram_pages)
    print(f"  → {n_embedded} embedded images extracted to {EMBED_DIR.relative_to(ROOT)}")

    # 2. Page renders
    pages_to_render = set(range(1, doc.page_count + 1)) if args.full else diagram_pages
    print(f"\n[2/2] Rendering {len(pages_to_render)} pages at {args.dpi} DPI...")
    n_pages = render_pages(doc, pages_to_render, args.dpi)
    print(f"  → {n_pages} page PNGs rendered to {PAGE_DIR.relative_to(ROOT)}")

    # 3. Chapter map
    print("\n[3/3] Building page→chapter map...")
    page_chapter = page_to_chapter_map()
    if page_chapter:
        import json
        map_path = OUT / "page_chapter.json"
        map_path.write_text(json.dumps(page_chapter, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"  → {len(page_chapter)} pages mapped → {map_path.relative_to(ROOT)}")

    doc.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
