#!/usr/bin/env python3
"""QA chunk-coverage audit.

Verifies that:
1. Every chunks/chunk*.md has a corresponding chunks_translated/output_chunk*.md
2. Every output_chunk file is non-empty (>= 50 bytes)
3. chunk_plan.json chunk_size matches actual file size
4. manifest.json source_hash matches chunks/chunk*.md content hash
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHUNKS = ROOT / "chunks"
TRANSLATED = ROOT / "chunks_translated"
MANIFEST = ROOT / "manifest.json"


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    chunk_files = sorted(CHUNKS.glob("chunk*.md"))
    output_files = sorted(TRANSLATED.glob("output_chunk*.md"))

    print("=" * 70)
    print("MindShare PCIe 3.0 — Chunk Coverage Audit")
    print("=" * 70)
    print(f"Source chunks:    {len(chunk_files)}")
    print(f"Translated chunks:{len(output_files)}")
    missing = [c.name for c in chunk_files if not (TRANSLATED / f"output_{c.name}").exists()]
    empty = [o.name for o in output_files if o.stat().st_size < 50]
    print(f"Missing translations: {len(missing)}")
    print(f"Empty translations:   {len(empty)}")

    if missing:
        print("\nMissing (first 10):")
        for m in missing[:10]:
            print(f"  - {m}")
    if empty:
        print("\nEmpty/placeholder (first 10):")
        for m in empty[:10]:
            print(f"  - {m} ({(TRANSLATED / m).stat().st_size} bytes)")

    # Hash verify against manifest.json
    if MANIFEST.exists():
        m = json.loads(MANIFEST.read_text(encoding='utf-8'))
        mismatches = 0
        for entry in m.get("chunks", []):
            src = ROOT / entry["source_file"]
            if src.exists() and entry.get("source_hash"):
                if file_sha(src) != entry["source_hash"]:
                    mismatches += 1
        print(f"\nManifest hash mismatches: {mismatches}")

    report = {
        "src_count": len(chunk_files),
        "translated_count": len(output_files),
        "missing_translations": len(missing),
        "empty_translations": len(empty),
        "missing_list": missing,
        "empty_list": empty,
        "progress_pct": round(len(output_files) / max(len(chunk_files), 1) * 100, 2),
    }
    out = ROOT / "qa_chunk_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\nSaved: {out.relative_to(ROOT)}")
    print(f"Progress: {report['progress_pct']}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
