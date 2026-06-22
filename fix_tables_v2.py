#!/usr/bin/env python3
"""Fix the broken dual-column table structure in MindShare PCIe chapter files.

Per section, the original broken structure is:
    <table>
    <thead><table>                            ← BOGUS: <table> inside <thead>
    <thead>                                   ← inner thead of bogus table
    <tr><th>English</th><th>中文</th></tr>
    </thead>
    <tbody>                                   ← inner tbody of bogus table
    <tr><th>English</th><th>中文</th></tr>     ← duplicate header row
    </tbody>
    </table></thead>                          ← BOGUS: closes bogus table + outer thead
    <tbody><table>                            ← BOGUS: <table> inside <tbody>
    <thead>                                   ← inner thead
    <tr><th>English</th><th>中文</th></tr>
    </thead>
    <tbody>                                   ← inner tbody
    <tr>                                      ← may have a duplicate <tr> after this
    <tr>                                      ← double <tr> (ch12 only)
    <td width="50%">EN content</td>
    <td width="50%">CN content</td>
    </tr>
    </tbody>
    </table>                                  ← BOGUS: closes bogus table
    </tbody>                                  ← close outer tbody
    </table>                                  ← close outer table

Target valid GFM structure:
    <table>
    <thead>
    <tr><th width="50%">English</th><th width="50%">中文</th></tr>
    </thead>
    <tbody>
    <tr>
    <td width="50%">EN content</td>
    <td width="50%">CN content</td>
    </tr>
    </tbody>
    </table>
"""

import re
import sys
from pathlib import Path

ROOT = Path('/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_EN_VS_CN')


def fix(text: str) -> tuple[str, dict]:
    """Apply table fix. Returns (new_text, stats)."""
    original = text
    stats = {
        'thead_table_removed': 0,
        'tbody_table_removed': 0,
        'tr_tr_collapsed': 0,
        'tr_th_collapsed': 0,
        'closing_collapsed': 0,
    }

    # ─────────────────────────────────────────────────────────────
    # Fix 1: Remove the bogus <thead><table>...</table></thead> block.
    # The block contains:
    #   <thead><table>\n
    #   <thead><tr><th>English</th><th>中文</th></tr></thead>\n
    #   <tbody>\n<tr><th>English</th><th>中文</th></tr>\n</tbody>\n
    #   </table></thead>
    # We keep ONLY the first <tr> (the proper header) wrapped in <thead>.
    # ─────────────────────────────────────────────────────────────
    pattern_thead = re.compile(
        r'<thead><table>\s*\n\s*'
        r'<thead>(<tr>.*?</tr>)</thead>\s*\n\s*'
        r'<tbody>\s*\n\s*<tr>.*?</tr>\s*\n\s*</tbody>\s*\n\s*'
        r'</table>\s*</thead>',
        re.DOTALL
    )
    text, n = pattern_thead.subn(r'<thead>\1</thead>', text)
    stats['thead_table_removed'] = n

    # ─────────────────────────────────────────────────────────────
    # Fix 2: Remove the bogus <tbody><table>...</table></tbody></table> tail.
    # The pattern after Fix 1 looks like:
    #   <tbody><table>\n
    #   <thead><tr><th>English</th><th>中文</th></tr></thead>\n
    #   <tbody>\n
    #   <tr>(<tr>)?     ← optional double <tr>
    #   <td>EN</td>
    #   <td>CN</td>
    #   </tr>
    #   </tbody>\n
    #   </table>\n
    #   </tbody>\n
    #   </table>
    # We want to keep the <tr>...<td>EN</td><td>CN</td>...</tr> content
    # inside the outer <tbody>, dropping all the inner <table> wrappers.
    # ─────────────────────────────────────────────────────────────
    # Step 2a: drop the leading <tbody><table>...\n<thead>...</thead>\n<tbody>
    pattern_body_open = re.compile(
        r'<tbody><table>\s*\n\s*'
        r'<thead>.*?</thead>\s*\n\s*'
        r'<tbody>\s*\n\s*',
        re.DOTALL
    )
    text, n = pattern_body_open.subn('<tbody>\n', text)
    stats['tbody_table_removed'] = n

    # Step 2b: drop the trailing </tbody>\n</table></tbody></table> tail
    pattern_body_close = re.compile(
        r'</tr>\s*\n\s*</tbody>\s*\n\s*</table>\s*</tbody>\s*</table>',
        re.DOTALL
    )
    text, n = pattern_body_close.subn('</tr>\n</tbody>\n</table>', text)
    stats['closing_collapsed'] += n

    # Inline variant: </tr></tbody></table></tbody></table>
    pattern_body_close_inline = re.compile(
        r'</tr></tbody></table></tbody></table>',
        re.DOTALL
    )
    text, n = pattern_body_close_inline.subn('</tr></tbody></table>', text)
    stats['closing_collapsed'] += n

    # Multi-line variant 2: </tbody>\n</table>\n</tbody>\n</table>
    pattern_body_close2 = re.compile(
        r'</tbody>\s*\n\s*</table>\s*\n\s*</tbody>\s*\n\s*</table>',
        re.DOTALL
    )
    text, n = pattern_body_close2.subn('</tbody>\n</table>', text)
    stats['closing_collapsed'] += n

    # Variant: </table></tr></tbody></table>  (extra </tr>)
    pattern_extra_tr = re.compile(
        r'</table></tr></tbody></table>',
        re.DOTALL
    )
    text, n = pattern_extra_tr.subn('</table>', text)
    stats['closing_collapsed'] += n

    # Variant: </table>\n</tr>\n</tbody>\n</table>  (extra </tr> on own line)
    pattern_extra_tr2 = re.compile(
        r'</table>\s*\n\s*</tr>\s*\n\s*</tbody>\s*\n\s*</table>',
        re.DOTALL
    )
    text, n = pattern_extra_tr2.subn('</table>', text)
    stats['closing_collapsed'] += n

    # Step 2c: collapse any <tr>\s*\n\s*<tr> double-tr to single
    pattern_double_tr = re.compile(r'<tr>\s*\n\s*<tr>')
    text, n = pattern_double_tr.subn('<tr>', text)
    stats['tr_tr_collapsed'] = n

    stats['changed'] = text != original
    return text, stats


def main():
    chapters = sorted(ROOT.glob('MindShare_PCIe_ch[0-9]*.md'))
    print(f"Found {len(chapters)} chapters\n")
    print(f"{'Chapter':70s} {'open/close':12s}  {'fixes':40s}  status")
    print("-" * 130)

    total_changed = 0
    issues = []
    for f in chapters:
        text = f.read_text(encoding='utf-8')
        orig_open = text.count('<table>')
        orig_close = text.count('</table>')

        new_text, stats = fix(text)
        new_open = new_text.count('<table>')
        new_close = new_text.count('</table>')

        if new_open != new_close:
            issues.append((f.name, new_open, new_close))

        if stats['changed']:
            f.write_text(new_text, encoding='utf-8')
            total_changed += 1
            fix_summary = f"th={stats['thead_table_removed']} tb={stats['tbody_table_removed']} tr={stats['tr_tr_collapsed']} cl={stats['closing_collapsed']}"
            status = f"✓ ({orig_open}/{orig_close}→{new_open}/{new_close})"
        else:
            fix_summary = "—"
            status = "(no changes)"

        print(f"{f.name[:70]:70s} {new_open:3d}/{new_close:3d}      {fix_summary:40s}  {status}")

    print()
    if issues:
        print(f"⚠️  {len(issues)} files still have unbalanced tables:")
        for name, o, c in issues:
            print(f"   {name}: {o} open / {c} close (diff {o - c})")
    else:
        print("✅ All files balanced.")
    print(f"\nTotal fixed: {total_changed}/{len(chapters)}")


if __name__ == '__main__':
    main()
