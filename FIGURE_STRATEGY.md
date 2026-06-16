# 📐 Figure Extraction Strategy

## Source PDF

- **File**: `/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCI Express Technology 3.0.pdf`
- **Pages**: 1057
- **Format**: PDF 1.6 (Acrobat Distiller output)

## Extraction Approach

Two complementary outputs:

### 1. Embedded raster images → `figures/embedded/`

`PyMuPDF.page.get_images(full=True)` — extracts all embedded raster bitmaps (logos, photos, diagrams saved as bitmaps). Saves to `figures/embedded/pageNNNN_imgM.png`.

**Stats**: 109 images across 68 pages.

### 2. Page renders at 150 DPI → `figures/page/`

Full page rendered to PNG. Only rendered for pages with embedded images OR pages containing "Figure X-Y" caption text — to keep repo size manageable.

**Stats**: 68 page PNGs.

### 3. Chapter-organized copies → `figures/chapter_NN_<Title>/`

Same files copied into per-chapter subdirs using `page_chapter.json` mapping (derived from `**NNN**` page markers in chunks).

```
figures/
├── embedded/                        # 109 files — all embedded images
├── page/                            # 68 files — page renders
├── page_chapter.json                # page → chapter mapping
├── chapter_pages.json               # chapter → pages list
├── chapter_00_Front_Matter_Cover_Copyright/   # 63 embedded + 33 page
├── chapter_04_Address_Space_Transaction_Ro/   # 4 + 1
├── chapter_10_Ack_Nak_Protocol/                # 12 + 10
├── chapter_13_Physical_Layer_-_Electrical/     # 1 + 1
├── chapter_14_Link_Initialization_Training/    # 5 + 4
├── chapter_15_Error_Detection_and_Handling/    # 1 + 1
├── chapter_16_Power_Management/                # 1 + 1
├── chapter_17_Interrupt_Support/               # 12 + 10
├── chapter_19_Hot_Plug_and_Power_Budgeting/    # 4 + 1
└── chapter_99_Appendices/                      # 6 + 6
```

## Re-running extraction

```bash
python3 tools/extract_figures.py             # extract + chapter-organize
python3 tools/extract_figures.py --full      # also render every page (large!)
python3 tools/extract_figures.py --dpi 300   # higher resolution
```

## Limitations & Future Work

- **Vector diagrams not extracted**: Many PCIe diagrams are vector drawings (lines + text). Currently only rendered as part of full-page PNGs. To extract tight bounds, would need `MinerU bbox + cropping` approach (as used in PCIe6.2_zh Round 2).
- **Chapter mapping imperfect**: Some pages map to ch0 (front matter) due to chunks 91-229 mixing TOC + body content. The `**NNN**` page-marker heuristic picks up TOC entries too. `page_chapter.json` is best-effort.
- **No figure captions in MDs**: Chapter MDs currently don't embed `<img>` tags pointing to figures. Next pass: scan chunks for "Figure X-Y" caption text + scan page renders for caption position, then inject `<img>` references into chapter MDs.

## Disk usage

| | Files | Size |
|---|---:|---:|
| `figures/embedded/` | 109 | ~10 MB |
| `figures/page/` | 68 | ~20 MB |
| `figures/chapter_*/` (copies) | 177 | ~30 MB |
| **Total** | **354** | **~60 MB** |
