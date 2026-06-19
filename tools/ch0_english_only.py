#!/usr/bin/env python3
"""Convert Ch0 from bilingual table format to English-only plain format."""

import re
import sys

def convert_ch0_to_english_only(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # --- 1. Update header ---
    # Remove "中英对照双语 · 中文灰底" from the format line
    text = text.replace(
        '> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)',
        '> 🎨 **Format**: 英文原文 · 保留原始排版与插图'
    )

    # --- 2. Process each bilingual table ---
    # Pattern: <table> ... <tbody><tr> <td> ENG </td> <td ...> ZH </td> </tr></tbody></table>
    table_pattern = re.compile(
        r'<table>\s*'
        r'<thead>.*?</thead>\s*'
        r'<tbody><tr>\s*'
        r'(<td>.*?</td>)\s*'
        r'<td[^>]*>.*?</td>\s*'
        r'</tr></tbody></table>',
        re.DOTALL
    )

    def replace_table(match):
        td_content = match.group(1)  # <td> ... English ... </td>
        # Extract inner content (remove the <td> and </td> wrappers)
        inner = td_content[4:-5]  # strip <td> and </td>
        return inner

    text = table_pattern.sub(replace_table, text)

    # --- 3. Update section headings: remove Chinese part after | ---
    # "## 0.N Front Matter (...) | 前言（...）" → "## 0.N Front Matter (...)"
    text = re.sub(
        r'^(## \d+\.\d+ .+?) \| .+$',
        r'\1',
        text,
        flags=re.MULTILINE
    )

    # --- 4. Remove [⬆️ 返回目录] links (no longer in bilingual table context) ---
    # Actually keep them - they're still useful navigation

    # --- 5. Clean up extra blank lines (max 2 consecutive) ---
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    # Stats
    print(f"Converted: {input_path}")
    print(f"Output:    {output_path}")
    print(f"Lines:     {len(text.splitlines())}")

if __name__ == '__main__':
    input_path = sys.argv[1] if len(sys.argv) > 1 else (
        '/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/'
        'MindShare_PCIe_Technology_3.0_EN_VS_CN/'
        'MindShare_PCIe_ch00_Front_Matter_Cover_Copyright_TOC_'
        '前言_封面_版权_目录.md'
    )
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path
    convert_ch0_to_english_only(input_path, output_path)
