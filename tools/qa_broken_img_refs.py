#!/usr/bin/env python3
"""QA check for broken <img src=> references in chapter MDs.

Scans every MindShare_PCIe_ch*.md, extracts <img src="..."> attributes,
verifies the referenced file exists.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = sorted(ROOT.glob("MindShare_PCIe_ch*.md"))

IMG_SRC_RE = re.compile(r'<img\s+[^>]*src="([^"]+)"', re.IGNORECASE)


def main() -> int:
    findings = []
    print("=" * 70)
    print("MindShare PCIe 3.0 — Broken Image Reference Audit")
    print("=" * 70)
    print(f"\nChapter MDs scanned: {len(CHAPTERS)}")
    total_refs = 0
    for ch in CHAPTERS:
        text = ch.read_text(encoding='utf-8')
        refs = IMG_SRC_RE.findall(text)
        if not refs:
            continue
        for ref in refs:
            total_refs += 1
            # Resolve path relative to repo root (where the chapter MD lives)
            target = ROOT / ref
            if not target.exists():
                findings.append({"chapter": ch.name, "ref": ref})
    print(f"Total <img src=> references: {total_refs}")
    print(f"Broken references: {len(findings)}")
    if findings:
        print("\nBroken refs:")
        for f in findings[:20]:
            print(f"  {f['chapter']}: {f['ref']}")
        if len(findings) > 20:
            print(f"  ... and {len(findings) - 20} more")
    out = ROOT / "qa_broken_img_report.json"
    out.write_text(json.dumps(findings, ensure_ascii=False, indent=2))
    print(f"\nSaved: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
