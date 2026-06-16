#!/usr/bin/env python3
"""QA check for short translations.

A translation is "short" if output_chunk size is small relative to source_chunk.
We distinguish:
  - Empty/placeholder:  < 50 bytes
  - Suspicious small:   50-200 bytes
  - Likely short:       > 200 bytes but ratio < 30% of source size

Skip chunks whose source is itself < 200 bytes (covers, headers) — those
empty translations are acceptable.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "chunks"
TR = ROOT / "chunks_translated"


def main() -> int:
    findings = {"empty": [], "suspicious_small": [], "likely_short": []}
    src_files = sorted(SRC.glob("chunk*.md"))
    for src_path in src_files:
        out_path = TR / f"output_{src_path.name}"
        if not out_path.exists():
            continue
        src_size = src_path.stat().st_size
        out_size = out_path.stat().st_size
        chunk_n = src_path.stem[5:]
        if src_size < 200:  # source is itself tiny — skip
            continue
        if out_size < 50:
            findings["empty"].append((chunk_n, src_size, out_size))
        elif out_size < 200:
            findings["suspicious_small"].append((chunk_n, src_size, out_size))
        elif out_size < src_size * 0.30:
            findings["likely_short"].append((chunk_n, src_size, out_size))

    print("=" * 70)
    print("MindShare PCIe 3.0 — Short Translation Audit")
    print("=" * 70)
    print(f"\n[Empty / placeholder]  output < 50 bytes (source ≥ 200 bytes)")
    if findings["empty"]:
        for n, s, o in findings["empty"]:
            print(f"  chunk{n}: src={s}B, out={o}B")
    else:
        print("  (none)")
    print(f"\n[Suspicious small]     50-200 bytes")
    if findings["suspicious_small"]:
        for n, s, o in findings["suspicious_small"]:
            print(f"  chunk{n}: src={s}B, out={o}B")
    else:
        print("  (none)")
    print(f"\n[Likely short]         > 200B but ratio < 30% of source")
    if findings["likely_short"]:
        for n, s, o in findings["likely_short"]:
            print(f"  chunk{n}: src={s}B, out={o}B ({o/s*100:.1f}%)")
    else:
        print("  (none)")
    total = sum(len(v) for v in findings.values())
    print(f"\nTotal suspicious: {total}")
    out = ROOT / "qa_short_report.json"
    out.write_text(json.dumps({
        "empty": findings["empty"],
        "suspicious_small": findings["suspicious_small"],
        "likely_short": findings["likely_short"],
        "total_suspicious": total,
    }, ensure_ascii=False, indent=2))
    print(f"Saved: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
