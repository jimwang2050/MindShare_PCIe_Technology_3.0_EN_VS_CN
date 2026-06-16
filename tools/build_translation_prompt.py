#!/usr/bin/env python3
"""Build per-chapter translation prompts from chunks/ + glossary.

Generates prompts/prompt_chapter_NN.md for each chapter defined in
chapter_index.json. Mirrors PCIe6.2_zh/tools/build_translation_prompt.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHUNKS = ROOT / "chunks"
INDEX = ROOT / "chapter_index.json"
GLOSSARY = ROOT / "glossary.json"
PROMPTS = ROOT / "prompts"


def main() -> int:
    idx = json.loads(INDEX.read_text(encoding='utf-8'))
    glossary = json.loads(GLOSSARY.read_text(encoding='utf-8'))
    terms_block = "\n".join(f"- `{t['source']}` → {t['target']}" for t in glossary.get("terms", [])[:80])

    template = """# 📝 翻译任务: {en} ({zh})

You are translating Chapter {ch} of "MindShare PCI Express Technology 3.0".

## Source
The English source is split across these chunks (already extracted):
{src_list}

Please:
1. Read each source chunk
2. Produce a Chinese translation following the glossary below
3. Preserve technical terms, register names, and signal names verbatim
4. Use the format:
   - Section headers: `## N.M Section Title | 小节标题`
   - Body paragraphs: free-form Markdown
5. Save translation to `chunks_translated/output_chunkXXXX.md` matching each source chunk number

## Glossary (sample — full list in glossary.json)
{terms}

## Output format per chunk
```
{{translated_markdown_with_bilingual_table_if_appropriate}}
```

Begin.
"""

    for c in idx["chapters"]:
        ch_num = c["ch"]
        src_files = [f"chunks/chunk{n:04d}.md" for n in range(c["start"], c["end"]+1)
                     if (CHUNKS / f"chunk{n:04d}.md").exists()]
        prompt_text = template.format(
            ch=ch_num, en=c["en"], zh=c.get("zh", c["en"]),
            src_list="\n".join(f"- `{f}`" for f in src_files[:50]),
            terms=terms_block,
        )
        out = PROMPTS / f"prompt_chapter_{ch_num:02d}.md"
        out.write_text(prompt_text, encoding='utf-8')
        print(f"  → {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
