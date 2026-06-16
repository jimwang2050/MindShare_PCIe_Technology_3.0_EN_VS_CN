#!/usr/bin/env python3
"""QA check for figure cropping distortion.

Mirrors PCIe6.2_zh/tools/fix_broken_crops.py logic:
  - Empty file (size 0)
  - Very small (< 5KB) — likely blank
  - Extreme aspect ratio (> 6 or < 0.17) — likely strip
  - Very narrow strip (width < 200 or height < 100)

Scans figures/embedded/, figures/page/, and figures/chapter_NN/.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install pillow")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent


def is_distorted(path: Path) -> tuple[bool, str]:
    sz = path.stat().st_size
    if sz == 0:
        return True, "empty file"
    if sz < 5000:
        return True, f"very small ({sz}B)"
    try:
        im = Image.open(path)
        w, h = im.size
    except Exception as e:
        return True, f"PIL error: {e}"
    ratio = w / h if h else 0
    if ratio > 6 or ratio < 0.17:
        return True, f"extreme aspect {w}x{h} (ratio={ratio:.2f})"
    if w < 200 or h < 100:
        return True, f"narrow strip {w}x{h}"
    return False, ""


def scan_dir(d: Path) -> list[dict]:
    if not d.exists():
        return []
    out = []
    for png in sorted(d.rglob("*.png")):
        bad, reason = is_distorted(png)
        if bad:
            out.append({"path": str(png.relative_to(ROOT)), "reason": reason,
                        "size": png.stat().st_size})
    return out


def main() -> int:
    print("=" * 70)
    print("MindShare PCIe 3.0 — Figure Crop Distortion Audit")
    print("=" * 70)
    findings = []
    for sub in ["embedded", "page"]:
        d = ROOT / "figures" / sub
        findings.extend(scan_dir(d))
    for d in (ROOT / "figures").glob("chapter_*"):
        if d.is_dir():
            findings.extend(scan_dir(d))

    print(f"\nTotal distorted figures: {len(findings)}")
    if findings:
        for f in findings[:30]:
            print(f"  {f['path']}: {f['reason']} ({f['size']}B)")
        if len(findings) > 30:
            print(f"  ... and {len(findings) - 30} more")
    out = ROOT / "qa_distortion_report.json"
    out.write_text(json.dumps(findings, ensure_ascii=False, indent=2))
    print(f"\nSaved: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
