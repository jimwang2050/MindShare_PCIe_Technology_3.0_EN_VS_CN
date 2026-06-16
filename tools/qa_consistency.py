#!/usr/bin/env python3
"""QA check for chapter MD vs chapter_index.json consistency.

Verifies:
  - Every chapter in chapter_index.json has a MindShare_PCIe_ch*.md file
  - The chapter MD covers the expected chunk range (start/end)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    idx = json.loads((ROOT / "chapter_index.json").read_text(encoding='utf-8'))
    chapters = idx["chapters"]
    print("=" * 70)
    print("MindShare PCIe 3.0 — Chapter Consistency Audit")
    print("=" * 70)

    missing_files = []
    empty_files = []
    chunks = ROOT / "chunks"
    ch_trans = ROOT / "chunks_translated"

    print(f"\n{'Ch':>4s} {'Range':>14s} {'Exist':>6s} {'Trans':>7s} {'File'}")
    for c in chapters:
        # Find MD by partial match
        ch_num = c["ch"]
        candidates = sorted(ROOT.glob(f"MindShare_PCIe_ch{ch_num:02d}_*.md"))
        # Fallback: any MD starting with MindShare_PCIe_ch{ch_num:02d}
        if not candidates:
            # try without zero pad
            candidates = sorted(ROOT.glob(f"MindShare_PCIe_ch{ch_num}_*.md"))
        if not candidates:
            missing_files.append((ch_num, c["en"]))
            print(f"  {ch_num:>3d} chunks {c['start']:>4d}-{c['end']:<4d} {'MISS':>6s}")
            continue
        md_path = candidates[0]
        size = md_path.stat().st_size
        # Count chunks with real translations
        real = 0
        for n in range(c["start"], c["end"] + 1):
            of = ch_trans / f"output_chunk{n:04d}.md"
            if of.exists() and of.stat().st_size > 200:
                real += 1
        total_chunks = c["end"] - c["start"] + 1
        marker = "OK" if size > 100 else "EMPTY"
        if size < 100:
            empty_files.append((ch_num, md_path.name))
        print(f"  {ch_num:>3d} chunks {c['start']:>4d}-{c['end']:<4d} {marker:>6s} {real:>3d}/{total_chunks:<3d} {md_path.name}")

    print(f"\nMissing MDs: {len(missing_files)}")
    print(f"Empty MDs:   {len(empty_files)}")

    out = ROOT / "qa_consistency_report.json"
    out.write_text(json.dumps({
        "missing": missing_files,
        "empty": empty_files,
    }, ensure_ascii=False, indent=2))
    print(f"Saved: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
