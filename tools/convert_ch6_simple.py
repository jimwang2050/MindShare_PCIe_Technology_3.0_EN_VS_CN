#!/usr/bin/env python3
"""Simple string-level transform: HTML tables → blockquote markdown. Image-safe."""
import re
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')
f = ROOT / 'MindShare_PCIe_ch06_Flow_Control_流控.md'
text = f.read_text(encoding='utf-8')

# ── Header ──
first_table = text.find('<table>')
header = text[:first_table]
body = text[first_table:]
header = re.sub(r'> 🎨 \*\*Format\*\*: .+', '> 🎨 **Format**: 中英上下对照 · 标准 Markdown 表格', header)

# ── Strip HTML wrappers ──
body = re.sub(r'</?(?:table|thead|tbody|colgroup|th)[^>]*>\s*', '', body)

# ── Strip HTML wrappers but keep content between them ──
# Remove table/thead/tbody/colgroup/th tags, replace with newlines
body = re.sub(r'</?(?:table|thead|tbody|colgroup|th)[^>]*>\s*', '\n', body)

# Split into segments: rows and between-table content
segments = re.split(r'(<tr>.*?</tr>)', body, flags=re.DOTALL)
output = []
img_count = 0
en_lines = zh_lines = 0

for seg in segments:
    if seg.startswith('<tr>'):
        # It's a row
        tds = re.findall(r'<td[^>]*>(.*?)</td>', seg, re.DOTALL)
        en = re.sub(r'^\n+|\n+$', '', tds[0]) if tds else ''
        zh = re.sub(r'^\n+|\n+$', '', tds[1]) if len(tds) > 1 else ''

        # Detect images
        en_imgs = re.findall(r'<img[^>]+>', en)
        zh_imgs = re.findall(r'<img[^>]+>', zh)
        all_imgs = en_imgs + zh_imgs

        if all_imgs:
            fig_column = en if en_imgs else zh
            other_column = zh if en_imgs else en

            for img_tag in all_imgs:
                src_m = re.search(r'src="([^"]+)"', img_tag)
                if not src_m: continue
                src = src_m.group(1)
                pn_m = re.search(r'page(\d+)', src)
                pn = pn_m.group(1) if pn_m else None

                cap = 'Figure'
                cap_m = re.search(
                    r'(?:^|\n)\s*([_*]?(?:Figure|Table)\s+\d+[‐\-]\d+[^_*\n]{3,80}[_*]?)\s*(?:\n|$)',
                    fig_column
                )
                if cap_m:
                    cap = cap_m.group(1).strip('_* ').strip()

                output.append(f'\n<p align="center"><b>{cap}</b></p>')
                output.append(f'<p align="center"><img src="{src}" width="700"></p>')
                if pn:
                    output.append(f'<p align="center"><sub>📄 <a href="{src}">Page {pn}</a></sub></p>')
                output.append('')
                img_count += 1

            other = re.sub(r'<img[^>]+>\s*(?:<br>)?\s*', '', other_column)
            other = re.sub(r'[_*]?(?:Figure|Table)\s+\d+[‐\-]\d+[^_*\n]+[_*]?\s*\n?', '', other)
            other = other.strip()
            if other:
                output.append(other + '\n')
            continue

        # Text row → blockquote
        en, zh = en.strip(), zh.strip()
        if en:
            for line in en.split('\n'):
                ls = line.strip()
                output.append(f'> 🇬🇧 {ls}' if ls else '>')
                en_lines += 1
            output.append('')
        if zh:
            for line in zh.split('\n'):
                ls = line.strip()
                output.append(f'> 🇨🇳 {ls}' if ls else '>')
                zh_lines += 1
            output.append('')
    else:
        # Between-row content: keep as-is (contains extracted figures, headings, anchors)
        seg = seg.strip()
        if seg:
            # Don't add empty segments
            seg = re.sub(r'\n{3,}', '\n\n', seg)
            if seg:
                output.append(seg)

# ── Assemble ──
result = header.rstrip() + '\n\n---\n\n' + '\n'.join(output)

# ── Tech value highlighting ──
for pat, rep in [
    (r'(?<![`\w])([0-9A-Fa-f]{2,6}h)(?![`\w])', r'`\1`'),
    (r'(?<![`\w])(\d+DW)(?![`\w])', r'`\1`'),
    (r'(?<![`])(\[\d+(?::\d+)?\])(?![`\w(])', r'`\1`'),
    (r'(?<![`\w])(\d+\.?\d*\s*GT/s)(?![`\w])', r'`\1`'),
    (r'(?<![`\w])(\d+\s*KB)(?![`\w])', r'`\1`'),
    (r'(?<![`\w])(VC[0-7])(?![`\w])', r'`\1`'),
]:
    result = re.sub(pat, rep, result)

# ── Clean artifacts ──
result = re.sub(r'\n> [🇬🇧🇨🇳] \*\*(?:PCI Express(?: 3\.0)? Technology|Chapter \d+:.+)\*\*\s*\n', '\n', result)
result = re.sub(r'\n{4,}', '\n\n\n', result)
result = result.strip() + '\n'

f.write_text(result, encoding='utf-8')

# ── Stats ──
imgs_out = len(re.findall(r'<img src=', result))
print(f'  Segments → Lines: {len(result.splitlines())}')
print(f'  Images: {img_count} centered, {imgs_out} total')
print(f'  EN blocks: {en_lines}, ZH blocks: {zh_lines}')
