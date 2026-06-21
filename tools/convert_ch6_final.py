#!/usr/bin/env python3
"""Convert Ch6 to professional markdown blockquote format. Image-safe."""
import re
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')
f = ROOT / 'MindShare_PCIe_ch06_Flow_Control_流控.md'
text = f.read_text(encoding='utf-8')

# ── 1. Extract chapter header ──
first_table = text.find('<table>')
header = text[:first_table]
header = re.sub(r'> 🎨 \*\*Format\*\*: .+',
                '> 🎨 **Format**: 中英上下对照 · 标准 Markdown 表格', header)
body = text[first_table:]

# ── 2. Save ALL images and captions ──
imgs = []  # (src, full_tag, page_num)
captions_map = {}  # img_index → caption_text

def save_img(m):
    src = m.group(1)
    page_num = None
    pm = re.search(r'page(\d+)', src)
    if pm: page_num = pm.group(1)
    imgs.append((src, page_num))
    return f'<<IMG{len(imgs)-1}>>'

body = re.sub(r'<img src="([^"]+)"[^>]*>\s*(?:<br>)?', save_img, body)

# Find captions near each IMG marker
for i in range(len(imgs)):
    pos = body.find(f'<<IMG{i}>>')
    if pos < 0: continue
    before = body[max(0,pos-500):pos]
    cap_match = re.search(
        r'([_*]?(?:Figure|Table)\s+\d+[‐\-]\d+[^_*\n]{5,80}[_*]?)\s*$',
        before
    )
    if cap_match:
        captions_map[i] = cap_match.group(1).strip('_* ').strip()
        # Remove caption from body
        body = body.replace(cap_match.group(1), '', 1)

# ── 3. Strip HTML wrappers ──
body = re.sub(r'</?(?:table|thead|tbody|th|colgroup)[^>]*>\s*', '', body)

# ── 4. Process rows ──
rows = re.findall(r'<tr>(.*?)</tr>', body, re.DOTALL)
output = []
row_count = len(rows)

for ri, row_html in enumerate(rows):
    tds = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
    en = re.sub(r'^\n+|\n+$', '', tds[0]) if tds else ''
    zh = re.sub(r'^\n+|\n+$', '', tds[1]) if len(tds) > 1 else ''

    # Check for image markers
    en_imgs = [i for i in range(len(imgs)) if f'<<IMG{i}>>' in en]
    zh_imgs = [i for i in range(len(imgs)) if f'<<IMG{i}>>' in zh]

    # Handle rows with images
    all_imgs_here = en_imgs + zh_imgs
    if all_imgs_here:
        for idx in all_imgs_here:
            src, page_num = imgs[idx]
            caption = captions_map.get(idx, 'Figure')

            output.append(f'\n<p align="center"><b>{caption}</b></p>')
            output.append(f'<p align="center"><img src="{src}" width="700"></p>')
            if page_num:
                output.append(f'<p align="center"><sub>📄 <a href="{src}">Page {page_num}</a></sub></p>')
            output.append('')

            # Remove marker from text
            en = en.replace(f'<<IMG{idx}>>', '')
            zh = zh.replace(f'<<IMG{idx}>>', '')

    # Process remaining text content
    en = en.strip()
    zh = zh.strip()

    # Extract ## headings to standalone
    def extract_h(text):
        hs = re.findall(r'## \*?\*?.+?\*?\*?\s*', text)
        for h in hs:
            text = text.replace(h, '', 1)
        return text.strip(), [h.strip() for h in hs]

    en_text, en_hs = extract_h(en)
    zh_text, zh_hs = extract_h(zh)

    # Use headings (prefer EN)
    headings = en_hs or zh_hs
    for h in headings:
        output.append(h + '\n')

    # EN blockquote
    if en_text.strip():
        lines = []
        for line in en_text.split('\n'):
            if line.strip():
                lines.append(f'> 🇬🇧 {line}')
            else:
                lines.append('>')
        output.append('\n'.join(lines) + '\n')

    # ZH blockquote
    if zh_text.strip():
        lines = []
        for line in zh_text.split('\n'):
            if line.strip():
                lines.append(f'> 🇨🇳 {line}')
            else:
                lines.append('>')
        output.append('\n'.join(lines) + '\n')

# ── 5. Clean remaining IMG markers (shouldn't be any left) ──
result = '\n\n'.join(output)
remaining = re.findall(r'<<IMG\d+>>', result)
if remaining:
    print(f'WARNING: {len(remaining)} orphan image markers')
    for m in remaining:
        idx = int(re.search(r'\d+', m).group())
        src, page_num = imgs[idx]
        result = result.replace(m, f'<img src="{src}" width="700">')

# ── 6. Post-processing ──
# Tech value highlighting
for p, r in [
    (r'(?<![`\w])([0-9A-Fa-f]{2,6}h)(?![`\w])', r'`\1`'),
    (r'(?<![`\w])(\d+DW)(?![`\w])', r'`\1`'),
    (r'(?<![`])(\[\d+(?::\d+)?\])(?![`\w(])', r'`\1`'),
    (r'(?<![`\w])(\d+\.?\d*\s*GT/s)(?![`\w])', r'`\1`'),
    (r'(?<![`\w])(\d+\s*KB)(?![`\w])', r'`\1`'),
    (r'(?<![`\w])(VC[0-7])(?![`\w])', r'`\1`'),
]:
    result = re.sub(p, r, result)

# Clean artifacts
result = re.sub(r'\n> 🇬🇧 \*\*(?:PCI Express(?: 3\.0)? Technology|Chapter \d+:.+)\*\*\s*\n', '\n', result)
result = re.sub(r'\n> 🇨🇳 \*\*(?:PCI Express(?: 3\.0)? Technology|Chapter \d+:.+)\*\*\s*\n', '\n', result)
result = re.sub(r'\n{4,}', '\n\n\n', result)
result = re.sub(r'\n> \n', '\n', result)

# ── 7. Build TOC ──
seen = set()
toc = ['## 📑 本章目录 (Table of Contents)\n']
for h in re.findall(r'^## (.+?)$', result, re.MULTILINE):
    hc = h.strip()
    if '本章目录' in hc or 'Table of Contents' in hc: continue
    if len(hc) < 6: continue
    if hc in seen: continue
    seen.add(hc)
    anchor = re.sub(r'[^\w一-鿿\s-]', '', hc).strip()
    anchor = re.sub(r'\s+', '-', anchor).lower()[:60]
    toc.append(f'- [{hc}](#{anchor})')

# ── 8. Assemble ──
final = header.rstrip() + '\n\n---\n\n'
final += '\n'.join(toc) + '\n\n---\n\n'
final += result
final = re.sub(r'\n{4,}', '\n\n\n', final)
final = final.strip() + '\n'

f.write_text(final, encoding='utf-8')

# Stats
imgs_out = len(re.findall(r'<img src=', final))
en_blocks = len(re.findall(r'> 🇬🇧', final))
zh_blocks = len(re.findall(r'> 🇨🇳', final))
print(f'{f.name}: {row_count} rows → {len(final.splitlines())} lines')
print(f'  Images: {len(imgs)} in → {imgs_out} out')
print(f'  EN blocks: {en_blocks}, ZH blocks: {zh_blocks}')
print(f'  TOC entries: {len(toc)-1}')
