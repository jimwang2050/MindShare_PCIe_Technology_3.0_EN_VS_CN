#!/usr/bin/env bash
# Re-rasterize figures from source PDF if needed.
# Placeholder; in PCIe6.2_zh this is PyMuPDF-based extraction.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
PDF="$(grep '^input_file=' "$ROOT/config.txt" | cut -d= -f2-)"
echo "PDF: $PDF"
echo "(figures/ directory is reserved for PNG extraction outputs)"
echo "Run after mineru_local conversion populates figures/chapter_NN/*.png"
