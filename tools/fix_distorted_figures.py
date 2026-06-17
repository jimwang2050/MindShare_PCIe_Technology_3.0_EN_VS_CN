#!/usr/bin/env python3
"""Fix distorted figure PNGs in figures/.

Strategies:
1. **Empty (0 bytes)** — try to re-extract from PDF with proper CMYK→RGB.
2. **Tiny strips < 5KB AND aspect > 3** — likely marketing/course-listing/
   watermark content, NOT figures. Delete them from embedded/ + chapter
   copies.
3. **Page1054 marketing bloat** — page 1054 is the last page (MindShare
   contact info), all images on it are not figures. Delete.

After fix, re-render figures/page/ for pages that lost embedded figures
but still might have figure content (skip pure-marketing pages).

Also re-syncs chapter_NN/ copies.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
EMB = ROOT / "figures" / "embedded"
PG = ROOT / "figures" / "page"
REPORT = ROOT / "qa_distortion_report.json"
PDF = "/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCI Express Technology 3.0.pdf"

# Pages with no real figure content — skip entirely
NON_FIGURE_PAGES = {
    77,    # MindShare training course catalog
    982, 984,  # Arbor tool marketing
    1054, # Last page - MindShare contact info
    217, 220, 221,  # Watermark/logo strips
}

# MindShare training/marketing pages (full-page render not useful)
NON_FIGURE_PAGES.update(range(954, 985))  # 954-984 = appendix + marketing
NON_FIGURE_PAGES.update(range(1047, 1058))  # last 10 pages


def re_extract_empty(doc: fitz.Document, path: Path) -> bool:
    """Try to re-extract an empty image from PDF using CMYK conversion."""
    name = path.name  # e.g. page0001_img3.png
    page_no = int(name[4:8])
    img_idx = int(name.split("_img")[1].split(".")[0])
    try:
        page = doc[page_no - 1]
        imgs = page.get_images(full=True)
        if img_idx > len(imgs):
            return False
        xref = imgs[img_idx - 1][0]
        pix = fitz.Pixmap(doc, xref)
        if pix.colorspace and pix.colorspace.n >= 4:  # CMYK
            pix = fitz.Pixmap(fitz.csRGB, pix)
        pix.save(str(path))
        return True
    except Exception as e:
        print(f"  ! re-extract {path.name}: {e}")
        return False


def main() -> int:
    doc = fitz.open(PDF)
    if not REPORT.exists():
        print(f"Run tools/qa_crop_distortion.py first")
        return 1
    findings = json.loads(REPORT.read_text())

    # Group by action
    re_extract = []  # (path, page, img_idx)
    delete = []
    for f in findings:
        path = ROOT / f["path"]
        if not path.exists():
            continue
        reason = f["reason"]
        page = int(path.stem[4:8])
        if "empty file" in reason:
            re_extract.append(path)
        else:
            # All other distortions = delete (tiny strips are not figures)
            delete.append(path)

    print(f"Found {len(re_extract)} empty files (re-extract)")
    print(f"Found {len(delete)} distorted files (delete)")
    print()

    # Re-extract empty ones
    re_extracted = 0
    for path in re_extract:
        if re_extract_empty(doc, path):
            re_extracted += 1
            print(f"  ✓ re-extracted: {path.name}")
    print(f"\nRe-extracted: {re_extracted}/{len(re_extract)}")

    # Delete distorted ones
    deleted = 0
    for path in delete:
        # Delete from embedded/
        path.unlink(missing_ok=True)
        # Also delete from chapter_NN/embedded/ copies
        for ch_dir in (ROOT / "figures").glob("chapter_*"):
            cand = ch_dir / "embedded" / path.name
            if cand.exists():
                cand.unlink()
        # Also delete from chapter_NN/page/ if it's there
        for ch_dir in (ROOT / "figures").glob("chapter_*"):
            cand = ch_dir / "page" / path.name
            if cand.exists():
                cand.unlink()
        deleted += 1
    print(f"Deleted: {deleted}/{len(delete)}")

    # Delete non-figure pages from figures/page/ + chapter copies
    removed_pages = 0
    for png in sorted(PG.glob("*.png")):
        page_no = int(png.stem[4:8])
        if page_no in NON_FIGURE_PAGES:
            png.unlink()
            for ch_dir in (ROOT / "figures").glob("chapter_*"):
                cand = ch_dir / "page" / png.name
                if cand.exists():
                    cand.unlink()
            removed_pages += 1
    print(f"\nRemoved {removed_pages} non-figure page renders")

    # Final stats
    print()
    print("=" * 70)
    print("After fix:")
    print(f"  figures/embedded/: {len(list(EMB.glob('*.png')))} files")
    print(f"  figures/page/:     {len(list(PG.glob('*.png')))} files")
    chapter_total = 0
    for ch_dir in (ROOT / "figures").glob("chapter_*"):
        if ch_dir.is_dir():
            emb_n = len(list((ch_dir / 'embedded').glob('*.png'))) if (ch_dir / 'embedded').exists() else 0
            pg_n = len(list((ch_dir / 'page').glob('*.png'))) if (ch_dir / 'page').exists() else 0
            chapter_total += emb_n + pg_n
            if emb_n + pg_n > 0:
                print(f"  {ch_dir.name}/: {emb_n} emb + {pg_n} pg")
    print(f"\n  TOTAL embedded: {len(list(EMB.glob('*.png')))}")
    print(f"  TOTAL pages:    {len(list(PG.glob('*.png')))}")
    print(f"  TOTAL chapter copies: {chapter_total}")

    doc.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
