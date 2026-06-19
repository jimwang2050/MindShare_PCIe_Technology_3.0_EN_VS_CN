#!/usr/bin/env python3
"""
Rebuild Ch0 with:
1. Proper hierarchical TOC at the top
2. Descriptive section headings (instead of all "Front Matter")
3. Aligned page numbers — merge standalone roman numerals into TOC lines
4. Clean up scattered "Contents" headers
"""

import re, sys, os

PROJECT = '/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN'
CH0_FILE = os.path.join(PROJECT, 'MindShare_PCIe_ch00_Front_Matter_Cover_Copyright_TOC_前言_封面_版权_目录.md')

# ── Section heading mapping ──────────────────────────────────────────────
# Derived from first content line of each section
SECTION_TITLES = {
    1:  'Praise for MindShare Books',
    2:  'MindShare Technology Series',
    3:  'PCI Express Technology — Title Page',
    4:  'MINDSHARE, INC.',
    5:  'Authors — Mike Jackson, Ravi Budruk',
    6:  'MindShare Live Training and Self-Paced Training',
    7:  'ARBOR — Debug / Validation / Analysis Tool',
    8:  'The Ultimate Tool to View, Edit and Verify Configuration Settings',
    9:  'Arbor — Feature List',
    10: 'Arbor — COMING SOON: Decoded x86 Structures',
    11: 'Arbor — Introduction',
    12: 'Arbor — View Reference Info',
    13: 'Arbor — Decoding Standard and Custom Structures from a Live System',
    14: 'Arbor — Run Rule Checks',
    15: 'Arbor — Write Capability',
    16: 'Arbor — Saving System Scans (XML)',
    17: 'Title Page — PCI Express Technology',
    18: 'MINDSHARE, INC. — Title Page',
    19: 'Authors & Copyright Notice',
    20: 'Library of Congress Cataloging-in-Publication Data',
    21: 'Acknowledgments',
    22: 'Revision Updates',
    23: 'About This Book',
    24: 'Part One: The Big Picture (TOC)',
    25: 'Chapter 1: Background (TOC)',
    26: 'Chapter 1: Background — Contents continued (TOC)',
    27: 'Chapter 2: PCIe Architecture Overview (TOC)',
    28: 'Chapter 3: Configuration Overview (TOC)',
    29: 'Chapter 3: Configuration Overview — Contents continued (TOC)',
    30: 'Chapter 4: Address Space & Transaction Routing (TOC)',
    31: 'Part Two: Transaction Layer (TOC)',
    32: 'Chapter 5: TLP Elements (TOC)',
    33: 'Chapter 6: Flow Control (TOC)',
    34: 'Chapter 6: Flow Control — Contents continued (TOC)',
    35: 'Chapter 7: Quality of Service (TOC)',
    36: 'Chapter 8: Transaction Ordering (TOC)',
    37: 'Part Three: Data Link Layer (TOC)',
    38: 'Chapter 9: DLLP Elements / Chapter 10: Ack/Nak Protocol (TOC)',
    39: 'Chapter 10: Ack/Nak Protocol — Contents continued (TOC)',
    40: 'Part Four: Physical Layer (TOC)',
    41: 'Chapter 11: Physical Layer — Logical (Gen1 and Gen2) (TOC)',
    42: 'Chapter 11 — Contents continued / Chapter 12 intro (TOC)',
    43: 'Chapter 12: Physical Layer — Logical (Gen3) (TOC)',
    44: 'Chapter 13: Physical Layer — Electrical (TOC)',
    45: 'Chapter 13 — Contents continued (TOC)',
    46: 'Chapter 14: Link Initialization & Training (TOC)',
    47: 'Chapter 14 — Contents continued (TOC)',
    48: 'Chapter 14 — Contents continued / Chapter 15 intro (TOC)',
    49: 'Part Five: Additional System Topics (TOC)',
    50: 'Chapter 15: Error Detection and Handling (TOC)',
    51: 'Chapter 16: Power Management (TOC)',
    52: 'Chapter 16 — Contents continued (TOC)',
    53: 'Chapter 16 — Contents continued / Chapter 17 intro (TOC)',
    54: 'Chapter 17: Interrupt Support (TOC)',
    55: 'Chapter 17 — Contents continued (TOC)',
    56: 'Chapter 19: Hot Plug and Power Budgeting (TOC)',
    57: 'Chapter 20: Updates for Spec Revision 2.1 (TOC)',
    58: 'Chapter 20 — Contents / Appendix intro (TOC)',
    59: 'Appendices (TOC)',
    60: 'Appendix A: Debugging PCIe Traffic with LeCroy Tools (TOC)',
    61: 'Appendix B: Markets & Applications for PCI Express (TOC)',
    62: 'Appendix C: Implementing Intelligent Adapters and Multi-Host Systems (TOC)',
    63: 'Appendix D: Locked Transactions (TOC)',
    64: 'Appendices — Contents continued / Glossary intro (TOC)',
    65: 'Glossary (TOC)',
    66: 'Figures — List of Figures 0–32 (TOC)',
    67: 'Figures — List of Figures 33–77 (TOC)',
    68: 'Figures — List of Figures 78–119 (TOC)',
    69: 'Figures — List of Figures 120–149 (TOC)',
    70: 'Figures — List of Figures 150–189 (TOC)',
    71: 'Figures — List of Figures 190–204 (TOC)',
    72: 'Tables — List of Tables (TOC)',
    73: 'The MindShare Technology Series',
    74: 'Cautionary Note',
    75: 'Intended Audience',
    76: 'Prerequisite Knowledge',
    77: 'Book Topics and Organization',
    78: 'Part 6: Appendices',
    79: 'Documentation Conventions',
    80: 'PCI Express™',
    81: 'Hexadecimal Notation',
    82: 'Binary Notation',
    83: 'Decimal Notation',
    84: 'Bits, Bytes and Transfers Notation',
    85: 'Bit Fields',
    86: 'Active Signal States',
    87: 'Visit Our Web Site',
    88: 'We Want Your Feedback',
    89: 'www.mindshare.com',
    90: 'Corporate Mailing Address',
}

def extract_sections(text):
    """Extract all sections as (sec_num, old_heading, body, start, end)."""
    pattern = re.compile(
        r'<a id="sec-0-(\d+)"></a>\n'
        r'## (0\.\d+ .+?)\n'
        r'(.*?)'
        r'(?=\n<a id="sec-0-|$)',
        re.DOTALL
    )
    sections = []
    for m in pattern.finditer(text):
        sec_num = int(m.group(1))
        old_heading = m.group(2)
        body = m.group(3)
        sections.append((sec_num, old_heading, body, m.start(), m.end()))
    return sections

def clean_page_numbers(body):
    """Merge standalone roman-numeral page numbers into preceding TOC text."""
    # Remove standalone page number lines like: \n\n**vii**\n\n or \n\n**xii**\n\n
    # These are page numbers from the printed TOC — keep them as trailing markers

    # Pattern: bold roman numeral on its own line, often between TOC content
    # We'll convert: \n\n**vii**\n\n → <small>p. vii</small>\n\n
    roman_pattern = re.compile(
        r'\n\n(\*{0,2})([ivxlcdm]+)(\*{0,2})\s*\n\n',
        re.IGNORECASE
    )

    def replace_page(match):
        stars_before = match.group(1)
        numeral = match.group(2).strip()
        stars_after = match.group(3)
        # Only treat as page number if it looks like a roman numeral page number
        # (short, valid roman chars only)
        if len(numeral) <= 5 and all(c in 'ivxlcdmIVXLCDM' for c in numeral):
            return f'  \n'
        return match.group(0)

    # Don't do this — better approach: keep page numbers but style them
    # as right-aligned or small text
    return body

def clean_contents_headers(body):
    """Merge scattered '**Contents**' headers into the TOC flow."""
    # Convert standalone "**Contents**" to a subtle divider
    body = re.sub(
        r'\n\n\*\*Contents\*\*\s*\n',
        r'\n\n---\n',
        body
    )
    return body

def build_toc(sections_data):
    """Build hierarchical top-level TOC from section data."""
    lines = []
    lines.append('## 📑 目录 (Table of Contents)\n')

    groups = [
        ('Cover & Promo', range(1, 10)),
        ('Arbor Tool', range(10, 18)),
        ('Copyright & Credits', range(18, 23)),
        ('Detailed TOC — Main', range(23, 73)),
        ('About This Book — Subsections', range(73, 89)),
        ('Publisher Info', range(89, 91)),
    ]

    for group_name, r in groups:
        lines.append(f'### {group_name}')
        for sec_num, _, _, _, _ in sections_data:
            if sec_num in r:
                title = SECTION_TITLES.get(sec_num, f'Front Matter')
                lines.append(f'- [0.{sec_num} {title}](#sec-0-{sec_num})')
        lines.append('')

    return '\n'.join(lines)

def rebuild_ch0(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split at first <a id="sec-0-1"> (boundary between header and sections)
    split_marker = '\n<a id="sec-0-1">'
    idx = text.find(split_marker)
    if idx == -1:
        print('ERROR: could not find section boundary')
        return
    header = text[:idx]
    rest = text[idx:]  # starts with \n<a id="sec-0-1">...

    # Remove old TOC from header (from "## 📑 本章目录" to end of header)
    toc_start = header.find('## 📑 本章目录')
    if toc_start != -1:
        # Find the end of the old TOC (next blank line before end of header)
        # Keep everything before the old TOC
        header_before = header[:toc_start].rstrip()
    else:
        header_before = header.rstrip()

    # Extract all sections
    sections_data = extract_sections(rest)

    # Build new TOC
    new_toc = build_toc(sections_data)

    # Reassemble header: header_before + new_toc
    new_header = header_before + '\n\n' + new_toc

    # Rebuild each section with descriptive heading
    rebuilt_sections = []
    for sec_num, old_heading, body, start, end in sections_data:
        title = SECTION_TITLES.get(sec_num, f'Front Matter')
        new_heading = f'## 0.{sec_num} {title}'

        body = body.strip()

        # Clean up page numbers: standalone bold roman numerals → inline
        body = re.sub(
            r'\n\n\*\*([ivxlcdm]+)\*\*\n\n',
            r'<br><small>p. \1</small>\n\n',
            body,
            flags=re.IGNORECASE
        )

        # Non-bold roman numeral page markers
        body = re.sub(
            r'\n\n([ivxlcdm]+)\n\n',
            r'<br><small>p. \1</small>\n\n',
            body,
            flags=re.IGNORECASE
        )

        # Clean up scattered "Contents" headers — remove standalone ones
        body = re.sub(
            r'\n\n\*\*Contents\*\*\s*\n',
            r'\n',
            body
        )

        rebuilt = f'<a id="sec-0-{sec_num}"></a>\n{new_heading}\n\n{body}'
        rebuilt_sections.append(rebuilt)

    # Assemble
    result = new_header + '\n\n' + '\n\n'.join(rebuilt_sections)

    # Collapse excessive blank lines
    result = re.sub(r'\n{4,}', '\n\n\n', result)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f'Input:  {input_path}')
    print(f'Output: {output_path}')
    print(f'Sections rebuilt: {len(sections_data)}')
    print(f'Lines: {len(result.splitlines())}')

if __name__ == '__main__':
    rebuild_ch0(CH0_FILE, sys.argv[1] if len(sys.argv) > 1 else CH0_FILE)
