#!/usr/bin/env python3
"""QA check for section-level translation completeness.

For each source chunk, count H2/H3 headings (`## ...`) — translations
should have a similar count. If significantly fewer headings appear in
the translation, sections were likely skipped.

Note: We compare heading **counts** (not exact titles), because legitimate
translations render English titles as Chinese equivalents — comparing text
would flag valid translations as missing.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "chunks"
TR = ROOT / "chunks_translated"

# Count H2 (`## ...`) and H3 (`### ...`) headings only
HEADING_RE = re.compile(r"^#{2,3}\s+\S", re.MULTILINE)


def main() -> int:
    findings = []
    src_files = sorted(SRC.glob("chunk*.md"))
    for src_path in src_files:
        out_path = TR / f"output_{src_path.name}"
        if not out_path.exists() or out_path.stat().st_size < 50:
            continue
        src_count = len(HEADING_RE.findall(src_path.read_text(encoding='utf-8')))
        out_count = len(HEADING_RE.findall(out_path.read_text(encoding='utf-8')))
        # Flag if translation has fewer than 60% of source headings
        if src_count >= 2 and out_count < src_count * 0.6:
            findings.append({
                "chunk": src_path.stem.replace("chunk", ""),
                "src_headings": src_count,
                "out_headings": out_count,
                "ratio": round(out_count / src_count, 3),
            })

    print("=" * 70)
    print("MindShare PCIe 3.0 — Section Coverage Audit")
    print("=" * 70)
    print(f"\nThreshold: translation must have ≥60% of source H2/H3 headings")
    print(f"Chunks with section-level coverage gap: {len(findings)}")
    if findings:
        for f in findings[:30]:
            print(f"  chunk{f['chunk']}: src={f['src_headings']}, "
                  f"out={f['out_headings']} ({f['ratio']*100:.1f}%)")
        if len(findings) > 30:
            print(f"  ... and {len(findings) - 30} more")
    out = ROOT / "qa_section_report.json"
    out.write_text(json.dumps(findings, ensure_ascii=False, indent=2))
    print(f"\nSaved: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
