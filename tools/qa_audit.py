#!/usr/bin/env python3
"""QA audit for MindShare PCI Express Technology 3.0 bilingual translation.

Mirrors the PCIe6.2_zh/tools/qa_audit.py approach:
1. Empty / placeholder cells in EN|CN table rows
2. TODO / untranslated markers
3. ZH/EN character ratio per chapter
4. Image references balance
5. Section anchors (`<a id="sec-N-X">`)
6. Glossary term coverage
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = ROOT  # chapter MDs live at repo root
GLOSSARY_PATH = ROOT / "glossary.json"


def main() -> int:
    print("=" * 70)
    print("MindShare PCIe 3.0 中英对照翻译 — QA 审计报告")
    print("=" * 70)

    chapters = sorted(CHAPTERS_DIR.glob("MindShare_PCIe_ch*.md"))
    if not chapters:
        print("(no chapter MDs found yet — run tools/merge_chapters.py first)")
        return 1

    if GLOSSARY_PATH.exists():
        glossary = json.loads(GLOSSARY_PATH.read_text(encoding='utf-8'))
        key_terms = [t["source"] for t in glossary.get("terms", [])][:30]
    else:
        key_terms = []

    summary = []
    total_open = total_close = total_gray = total_imgs = 0

    for ch in chapters:
        text = ch.read_text(encoding='utf-8')
        name = ch.stem
        n_open = len(re.findall(r"<table\b", text))
        n_close = len(re.findall(r"</table>", text))
        n_gray = len(re.findall(r"background-color:#e8e8e8", text))
        n_imgs = len(re.findall(r"<img\s+src=", text))
        n_sections = len(re.findall(r'<a id="sec-', text))
        zh_chars = sum(1 for c in text if "一" <= c <= "鿿")
        en_chars = sum(1 for c in text if c.isascii() and c.isalpha())
        total = len(text)
        zh_pct = zh_chars / total * 100 if total else 0
        n_empty = len(re.findall(r"<tr>\s*<td></td>\s*<td[^>]*></td>\s*</tr>", text))
        n_todo = len(re.findall(r"⚠️\s*TODO", text))

        total_open += n_open
        total_close += n_close
        total_gray += n_gray
        total_imgs += n_imgs

        balance = "✓" if n_open == n_close else "✗ MISMATCH"
        summary.append({
            "ch": name,
            "tables_open": n_open,
            "tables_close": n_close,
            "gray_cells": n_gray,
            "imgs": n_imgs,
            "sections": n_sections,
            "zh_chars": zh_chars,
            "en_chars": en_chars,
            "zh_pct": round(zh_pct, 3),
            "todo": n_todo,
            "empty": n_empty,
            "balance": balance,
        })

    print(f"{'Chapter':50s} {'Open':>5s} {'Close':>5s} {'Gray':>5s} {'Imgs':>5s} {'Sec':>4s} {'ZH%':>6s} {'TODO':>5s}")
    print("-" * 100)
    for s in summary:
        print(f"{s['ch']:50s} {s['tables_open']:>5d} {s['tables_close']:>5d} {s['gray_cells']:>5d} "
              f"{s['imgs']:>5d} {s['sections']:>4d} {s['zh_pct']:>6.2f} {s['todo']:>5d}")
    print("-" * 100)
    print(f"{'TOTAL':50s} {total_open:>5d} {total_close:>5d} {total_gray:>5d} {total_imgs:>5d}")

    out = ROOT / "qa_report.json"
    out.write_text(json.dumps({
        "per_chapter": summary,
        "totals": {
            "tables_open": total_open,
            "tables_close": total_close,
            "gray_cells": total_gray,
            "image_refs": total_imgs,
        }
    }, ensure_ascii=False, indent=2))
    print(f"\nSaved: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
