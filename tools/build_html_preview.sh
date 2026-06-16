#!/usr/bin/env bash
# Build HTML preview from bilingual chapter MDs.
# Mirrors PCIe6.2_zh/tools/build_html_preview.sh.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
cd "$ROOT"

OUT="$ROOT/preview"
mkdir -p "$OUT"

CSS='body{font-family:-apple-system,Helvetica,Arial,sans-serif;max-width:1100px;margin:2em auto;padding:0 1em;line-height:1.55}
table{border-collapse:collapse;width:100%;margin:1em 0}
th,td{border:1px solid #ddd;padding:0.6em;vertical-align:top}
th{background:#f5f5f5;text-align:left}
img{max-width:100%;height:auto}
pre,code{font-family:"SFMono-Regular",Consolas,monospace;font-size:0.92em}
h1,h2,h3{line-height:1.25}
a{color:#0a66c2;text-decoration:none}
a:hover{text-decoration:underline}
hr{border:none;border-top:1px solid #ddd;margin:2em 0}
'

echo "$CSS" > "$OUT/pcie3_style.css"

# Build chapter HTML files (uses pandoc if available)
if command -v pandoc >/dev/null 2>&1; then
  for md in MindShare_PCIe_ch*.md; do
    [ -f "$md" ] || continue
    name="${md%.md}.html"
    pandoc --standalone --self-contained --css=pcie3_style.css \
      --metadata title="${md%.md}" "$md" -o "$OUT/$name"
    echo "  → preview/$name"
  done
  pandoc --standalone --self-contained --css=pcie3_style.css \
    --metadata title="MindShare PCIe 3.0 中英对照翻译" \
    MindShare_PCIe_ch*.md -o "$OUT/book.html"
  echo "  → preview/book.html"
else
  echo "(pandoc not installed — skipping HTML render)"
fi

# Build index.html
{
  echo '<!doctype html><html><meta charset="utf-8">'
  echo '<title>MindShare PCIe 3.0 中英对照翻译</title>'
  echo '<link rel="stylesheet" href="pcie3_style.css">'
  echo '<body><h1>📚 MindShare PCI Express Technology 3.0 — 中英对照</h1>'
  echo '<ul>'
  for md in MindShare_PCIe_ch*.md; do
    [ -f "$md" ] || continue
    echo "  <li><a href=\"${md%.md}.html\">$md</a></li>"
  done
  echo '</ul>'
  if [ -f "$OUT/book.html" ]; then
    echo '<p><a href="book.html">📖 完整版 (book.html)</a></p>'
  fi
  echo '</body></html>'
} > "$OUT/index.html"
echo "  → preview/index.html"
