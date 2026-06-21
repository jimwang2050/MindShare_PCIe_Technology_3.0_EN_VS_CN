#!/usr/bin/env python3
"""
V2: Convert Ch6 from HTML table EN/ZH columns to clean markdown blockquote format.
- Headings extracted from blockquotes as standalone ## headings
- EN → > 🇬🇧 blockquote, ZH → > 🇨🇳 blockquote
- Figures → centered <p> blocks
- Tables → standard markdown with backtick values
"""

import re
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')


def process_row(en_text, zh_text):
    """Convert one row's EN and ZH content to markdown blocks."""
    blocks = []

    # Check for figures in either column
    en_has_img = '<img src=' in en_text
    zh_has_img = '<img src=' in zh_text

    if en_has_img or zh_has_img:
        fig_source = en_text if en_has_img else zh_text
        other_source = zh_text if en_has_img else en_text

        # Extract figure caption properly
        cap_match = re.search(
            r'(?:^|\n)([_*]?(?:Figure|Table)\s+\d+[‐\-]\d+[^_*\n]+[_*]?)',
            fig_source
        )
        caption = ''
        if cap_match:
            caption = cap_match.group(1).strip('_* ').strip()
            # Remove caption from source text
            fig_source = fig_source.replace(cap_match.group(1), '', 1)

        # Extract img src
        img_match = re.search(r'<img src="([^"]+)"[^>]*>', fig_source)
        if img_match:
            img_path = img_match.group(1)
            page_num = None
            pm = re.search(r'page(\d+)', img_path)
            if pm:
                page_num = int(pm.group(1))

            if caption:
                blocks.append(f'<p align="center"><b>{caption}</b></p>')
            blocks.append(f'<p align="center"><img src="{img_path}" width="700"></p>')
            if page_num:
                blocks.append(f'<p align="center"><sub>📄 <a href="{img_path}">Page {page_num}</a></sub></p>')
            blocks.append('')

        # Check for non-figure text in the other column
        other_clean = re.sub(r'<img[^>]*>\s*(?:<br>)?\s*', '', other_source)
        other_clean = re.sub(r'[_*]?(?:Figure|Table)\s+[^_*\n]+[_*]?\s*\n?', '', other_clean)
        other_clean = other_clean.strip()
        if other_clean:
            blocks.append(other_clean + '\n')

        return '\n'.join(blocks) if blocks else ''

    # No figures - handle text content
    en_clean = en_text.strip()
    zh_clean = zh_text.strip()

    # Extract ## headings from content
    def extract_headings(text):
        headings = []
        clean = text
        for m in re.finditer(r'(?:^|\n)(## \*?\*?.+?\*?\*?\s*(?:\n|$))', text):
            h_text = m.group(1).strip()
            headings.append(h_text)
            clean = clean.replace(m.group(1), '\n', 1)
        return clean, headings

    en_body, en_headings = extract_headings(en_clean)
    zh_body, zh_headings = extract_headings(zh_clean)

    # Use the first heading as section header (prefer EN heading, fallback to ZH)
    all_headings = []
    if en_headings:
        all_headings = en_headings
    elif zh_headings:
        all_headings = zh_headings

    # Render
    en_body = en_body.strip()
    zh_body = zh_body.strip()

    if not en_body and not zh_body and not all_headings:
        return ''

    if all_headings:
        for h in all_headings:
            blocks.append(h + '\n')

    if en_body:
        lines = en_body.split('\n')
        wrapped = []
        for line in lines:
            if line.strip():
                wrapped.append(f'> 🇬🇧 {line}')
            else:
                wrapped.append('>')
        blocks.append('\n'.join(wrapped) + '\n')

    if zh_body:
        lines = zh_body.split('\n')
        wrapped = []
        for line in lines:
            if line.strip():
                wrapped.append(f'> 🇨🇳 {line}')
            else:
                wrapped.append('>')
        blocks.append('\n'.join(wrapped) + '\n')

    return '\n'.join(blocks) if blocks else ''


def wrap_tech_values(text):
    """Wrap technical values in backticks (conservative - only clear tech patterns)."""
    patterns = [
        (r'(?<![`\w])([0-9A-Fa-f]{2,6}h)(?![`\w])', r'`\1`'),       # 00h, FFFFh
        (r'(?<![`\w])(\d+DW)(?![`\w])', r'`\1`'),                    # 4DW
        (r'(?<![`])(\[\d+(?::\d+)?\])(?![`\w(])', r'`\1`'),          # [2:0], [31:12]
        (r'(?<![`\w])([01]{3,4}b)(?![`\w])', r'`\1`'),               # 000b
        (r'(?<![`\w])(\d+\.?\d*\s*GT/s)(?![`\w])', r'`\1`'),         # 2.5 GT/s
        (r'(?<![`\w])(\d+\.?\d*\s*G[BT]/s)(?![`\w])', r'`\1`'),      # GB/s, GT/s
        (r'(?<![`\w])(\d+\s*KB)(?![`\w])', r'`\1`'),                 # 2KB
        (r'(?<![`\w])(\d+\s*bytes)(?![`\w])', r'`\1`'),              # 4096 bytes
        (r'(?<![`\w])(VC[0-7])(?![`\w])', r'`\1`'),                  # VC0
        (r'(?<![`\w])(BAR[0-5])(?![`\w])', r'`\1`'),                 # BAR0
        (r'(?<![`\w])(Max_Payload_Size)(?![`\w])', r'`\1`'),         # Max_Payload_Size
    ]
    for p, r in patterns:
        text = re.sub(p, r, text)
    return text


def clean_artifacts(text):
    """Remove OCR/PDF artifacts."""
    text = re.sub(r'\n> 🇬🇧 \*\*PCI Express(?: 3\.0)? Technology\*\*\s*\n', '\n', text)
    text = re.sub(r'\n> 🇨🇳 \*\*PCI Express(?: 3\.0)? Technology\*\*\s*\n', '\n', text)
    text = re.sub(r'\n> 🇬🇧 \*\*Chapter \d+:.+\*\*\s*\n', '\n', text)
    text = re.sub(r'\n> 🇨🇳 \*\*Chapter \d+:.+\*\*\s*\n', '\n', text)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    text = re.sub(r'\n> \n', '\n', text)  # empty blockquote lines
    return text


def build_toc(text):
    """Build proper TOC from ## headings (filter out noise)."""
    headings = re.findall(r'^## (.+?)$', text, re.MULTILINE)
    # Filter: only include headings that look like real section titles
    good = []
    for h in headings:
        h_clean = h.strip()
        # Skip TOC itself
        if '本章目录' in h_clean or 'Table of Contents' in h_clean:
            continue
        # Skip headings that are just values or short noise
        if len(h_clean) < 8:
            continue
        if re.match(r'^[`\d\s]+$', h_clean):
            continue
        # Skip duplicate entries
        if h_clean not in [g[0] for g in good]:
            good.append((h_clean, h_clean))

    if not good:
        return ''

    toc_lines = ['## 📑 本章目录 (Table of Contents)\n']
    for display, _ in good:
        # Build anchor from heading text (simplified)
        anchor = re.sub(r'[^\w一-鿿\s-]', '', display)
        anchor = re.sub(r'\s+', '-', anchor.strip()).lower()[:60]
        toc_lines.append(f'- [{display.strip()}](#{anchor})')

    return '\n'.join(toc_lines) + '\n\n'


def convert_chapter(ch_file):
    text = ch_file.read_text(encoding='utf-8')

    # ── Extract chapter header (before first <table>) ──
    first_table = text.find('<table>')
    if first_table < 0:
        return None
    header = text[:first_table]
    body = text[first_table:]

    # Update format line
    header = re.sub(
        r'> 🎨 \*\*Format\*\*: .+',
        '> 🎨 **Format**: 中英上下对照 · 标准 Markdown 表格',
        header
    )

    # ── Strip HTML table wrappers ──
    body = re.sub(r'</?(?:table|thead|tbody|th)[^>]*>\s*', '', body)

    # ── Process rows ──
    rows = re.findall(r'<tr>(.*?)</tr>', body, re.DOTALL)
    output_blocks = []

    for row_html in rows:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
        en = tds[0].strip() if len(tds) > 0 else ''
        zh = tds[1].strip() if len(tds) > 1 else ''

        # Clean td padding
        en = re.sub(r'^\n+|\n+$', '', en)
        zh = re.sub(r'^\n+|\n+$', '', zh)

        block = process_row(en, zh)
        if block.strip():
            output_blocks.append(block)

    # ── Assemble ──
    result = header.rstrip() + '\n\n---\n\n'
    result += '\n\n'.join(output_blocks)

    # ── Post-process ──
    result = wrap_tech_values(result)
    result = clean_artifacts(result)
    result = re.sub(r'\n{4,}', '\n\n\n', result)

    # Build TOC
    toc = build_toc(result)
    if toc:
        # Find old TOC area and replace
        old_toc_start = result.find('## 📑 本章目录')
        if old_toc_start >= 0:
            old_toc_end = result.find('\n---\n', old_toc_start)
            if old_toc_end < 0:
                old_toc_end = result.find('\n## ', old_toc_start + 1)
            if old_toc_end > old_toc_start:
                result = result[:old_toc_start] + toc + result[old_toc_end:]

    result = result.strip() + '\n'
    ch_file.write_text(result, encoding='utf-8')
    return len(rows)


# Convert Ch6
ch6 = ROOT / 'MindShare_PCIe_ch06_Flow_Control_流控.md'
rows = convert_chapter(ch6)
if rows:
    lines = len(ch6.read_text().splitlines())
    blocks_en = len(re.findall(r'> 🇬🇧', ch6.read_text()))
    blocks_zh = len(re.findall(r'> 🇨🇳', ch6.read_text()))
    figs = len(re.findall(r'<img src=', ch6.read_text()))
    print(f'Converted: {rows} rows → {lines} lines')
    print(f'  EN blocks: {blocks_en}, ZH blocks: {blocks_zh}, Figures: {figs}')
