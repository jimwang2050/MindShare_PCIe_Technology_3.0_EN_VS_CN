#!/usr/bin/env python3
"""
Convert Ch6 (and other chapters) from HTML table EN/ZH columns
to markdown blockquote top-bottom bilingual format.

New format:
- EN text → > 🇬🇧 blockquote
- ZH text → > 🇨🇳 blockquote
- Figures → centered markdown
- Tables → standard markdown with backtick-wrapped values
"""

import re
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')


def wrap_en_block(text):
    """Wrap English text in blockquote."""
    if not text.strip():
        return text
    lines = text.strip().split('\n')
    result = []
    for line in lines:
        if line.strip():
            result.append(f'> 🇬🇧 {line}')
        else:
            result.append('>')
    return '\n'.join(result) + '\n'


def wrap_zh_block(text):
    """Wrap Chinese text in blockquote."""
    if not text.strip():
        return text
    lines = text.strip().split('\n')
    result = []
    for line in lines:
        if line.strip():
            result.append(f'> 🇨🇳 {line}')
        else:
            result.append('>')
    return '\n'.join(result) + '\n'


def wrap_value_backticks(text):
    """Wrap key values, codes, and register fields in backticks."""
    # Only modify text NOT inside existing backticks or code blocks
    # Target specific technical patterns
    patterns = [
        # Hex values: 00h, FFh, 040h (2-6 hex digits + h suffix)
        (r'(?<![`\w])([0-9A-Fa-f]{2,6}h)(?![`\w])', r'`\1`'),
        # Register sizes: 4DW, 5DW, 3DW, 1DW
        (r'(?<![`\w])(\d+DW)(?![`\w])', r'`\1`'),
        # Field widths in square brackets: [2:0], [31:12], [7]
        (r'(?<![`])(\[\d+(?::\d+)?\])(?![`\w])', r'`\1`'),
        # Multi-bit values: 000b, 001b, 010b
        (r'(?<![`\w])([01]{3,4}b)(?![`\w])', r'`\1`'),
        # GT/s speeds: 2.5 GT/s, 5.0 GT/s, 8.0 GT/s
        (r'(?<![`\w])(\d+\.?\d*\s*GT/s)(?![`\w])', r'`\1`'),
        # GB/s bandwidth
        (r'(?<![`\w])(\d+\.?\d*\s*GB/s)(?![`\w])', r'`\1`'),
        # KB/MB/GB sizes with numbers
        (r'(?<![`\w])(\d+\s*(?:KB|MB|GB))(?![`\w])', r'`\1`'),
        # VC0-VC7
        (r'(?<![`\w])(VC[0-7])(?![`\w])', r'`\1`'),
        # BAR0-BAR5
        (r'(?<![`\w])(BAR[0-5])(?![`\w])', r'`\1`'),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    return text


def clean_artifacts(text):
    """Remove OCR and PDF artifacts."""
    # Remove orphaned page headers
    text = re.sub(r'\n> 🇬🇧 \*\*PCI Express(?: 3\.0)? Technology\*\*', '', text)
    text = re.sub(r'\n> 🇨🇳 \*\*PCI Express(?: 3\.0)? Technology\*\*', '', text)
    text = re.sub(r'\n> 🇬🇧 \*\*Chapter \d+:.+\*\*', '', text)
    text = re.sub(r'\n> 🇨🇳 \*\*Chapter \d+:.+\*\*', '', text)
    # Remove empty blockquote lines
    text = re.sub(r'\n> \n', '\n\n', text)
    # Clean excessive blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text


def extract_row_content(row_html):
    """Extract EN and ZH content from a <tr>...</tr> block."""
    tds = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
    en = tds[0].strip() if len(tds) > 0 else ''
    zh = tds[1].strip() if len(tds) > 1 else ''

    # Remove leading/trailing blank lines inside td
    en = re.sub(r'^\n+|\n+$', '', en)
    zh = re.sub(r'^\n+|\n+$', '', zh)

    return en, zh


def convert_chapter(ch_file):
    text = ch_file.read_text(encoding='utf-8')
    original = text

    # ── Step 1: Extract chapter header (before first <table>) ──
    first_table = text.find('<table>')
    if first_table < 0:
        # Ch0 has no tables
        return

    header = text[:first_table]
    body = text[first_table:]

    # Clean up the header: remove old format lines
    header = re.sub(r'> 🎨 \*\*Format\*\*: .+', '> 🎨 **Format**: 中英上下对照 · 标准 Markdown 表格', header)

    # ── Step 2: Process body - remove all HTML table wrappers ──
    # Remove table open/close tags
    body = re.sub(r'</?table[^>]*>\s*', '', body)
    body = re.sub(r'</?thead[^>]*>\s*', '', body)
    body = re.sub(r'</?tbody[^>]*>\s*', '', body)

    # Process each row
    rows = re.findall(r'<tr>(.*?)</tr>', body, re.DOTALL)
    print(f'  Found {len(rows)} rows')

    output_sections = []

    for row_html in rows:
        en, zh = extract_row_content(row_html)

        # Handle rows with figures (img tags)
        has_figure = '<img src=' in en or '<img src=' in zh

        if has_figure:
            # Extract figure and caption from whichever column has it
            fig_content = en if '<img src=' in en else zh

            # Extract caption
            caption_match = re.search(r'[_*]?(Figure|Table)\s+[^_*\n]+[_*]?', fig_content)
            caption = caption_match.group(0).strip('_* ') if caption_match else ''

            # Extract img src and page number
            img_match = re.search(r'<img src="([^"]+)"[^>]*>', fig_content)
            if img_match:
                img_path = img_match.group(1)
                page_num = None
                pm = re.search(r'page(\d+)', img_path)
                if pm:
                    page_num = int(pm.group(1))

                # Build centered figure block
                fig_parts = []
                if caption:
                    fig_parts.append(f'\n<p align="center"><b>{caption}</b></p>')
                fig_parts.append(f'<p align="center"><img src="{img_path}" width="700"></p>')
                if page_num:
                    fig_parts.append(f'<p align="center"><sub>📄 <a href="{img_path}">Page {page_num}</a></sub></p>')
                output_sections.append('\n'.join(fig_parts) + '\n')

            # If there's non-figure content in the other column, keep it
            other = zh if '<img src=' in en else en
            other_clean = re.sub(r'[_*]?(?:Figure|Table)\s+[^_*\n]+[_*]?\s*\n?', '', other)
            other_clean = re.sub(r'<img src="[^"]+"[^>]*>\s*(?:<br>)?\s*', '', other_clean)
            if other_clean.strip():
                output_sections.append(other_clean.strip() + '\n')

        elif en.strip() and zh.strip():
            # Both columns have content - top-bottom format
            section_text = ''
            section_text += wrap_en_block(en)
            section_text += '\n'
            section_text += wrap_zh_block(zh)
            output_sections.append(section_text)

        elif en.strip():
            output_sections.append(en.strip() + '\n')
        elif zh.strip():
            output_sections.append(zh.strip() + '\n')

    # ── Step 3: Assemble ──
    result = header.rstrip() + '\n\n---\n\n'
    result += '\n\n'.join(output_sections)

    # ── Step 4: Apply markdown improvements ──
    result = wrap_value_backticks(result)
    result = clean_artifacts(result)

    # Clean up: remove residual HTML
    result = re.sub(r'</?th[^>]*>\s*', '', result)
    result = re.sub(r'<br>\s*\n', '\n', result)
    result = re.sub(r'\n{4,}', '\n\n\n', result)

    # ── Step 5: Rebuild TOC ──
    # Find all ## headings and build TOC
    headings = re.findall(r'^## (.+?)$', result, re.MULTILINE)
    if headings:
        toc_lines = ['## 📑 本章目录 (Table of Contents)\n']
        for h in headings:
            anchor = re.sub(r'[^a-z0-9一-鿿-]', '', h.lower().replace(' ', '-')[:50])
            toc_lines.append(f'- [{h.strip()}](#{anchor})')
        new_toc = '\n'.join(toc_lines) + '\n'

        # Replace old TOC
        old_toc = re.search(
            r'## 📑 本章目录 \(Table of Contents\).*?(?=\n---\n)',
            result, re.DOTALL
        )
        if old_toc:
            result = result[:old_toc.start()] + new_toc + result[old_toc.end():]

    # Clean up leading/trailing whitespace
    result = result.strip() + '\n'

    if result != original:
        ch_file.write_text(result, encoding='utf-8')
        return len(rows)

    return 0


# Process Ch6 only for now
ch6 = ROOT / 'MindShare_PCIe_ch06_Flow_Control_流控.md'
rows = convert_chapter(ch6)
if rows:
    lines = len(ch6.read_text().splitlines())
    print(f'  Converted: {rows} rows → {lines} lines')
