# 🔍 自检计划 (Self-Inspection Plan)

> **目标**: 在交付前,自动检测 4 类常见问题 — 主段/翻译缺失、figure 未单独成段、figure 剪裁失真、结构与引用错误。
> **参考**: PCIe 6.2 Spec 翻译 (`PCIe6.2_zh/`) Round 1-3 经验 + CXL 3.2 Spec 翻译 (`CXL_zh/`) `extract_ch08_figs.py` 等 figure 工具。

---

## 📋 4 大类检查

| 类别 | 关注问题 | 严重度 |
|------|----------|:------:|
| **A. 主段/翻译缺失** | 内容空洞、段落跳译、TODO 占位、英文未翻译 | 🔴 |
| **B. Figure 完整性** | Figure 未独立成段、`<img>` 引用断裂、跨列重复 | 🟡 |
| **C. Figure 剪裁质量** | 紧裁剪失真、bbox 越界、空文件、宽高比异常 | 🟡 |
| **D. 结构与引用** | `<table>` 不平衡、重复锚点、`<img src=>` 不存在 | 🟠 |

---

## 🔴 A. 主段/翻译缺失 (Content Loss / Translation Gaps)

### A1. 空/占位翻译
**检测**: `output_chunk*.md` 大小 < 50 bytes
**已知**: 当前 **21 个** chunk 是空/占位 (主要在 Ch 0 前言)
**工具**: `tools/qa_chunk_coverage.py` 已覆盖
**修复**: 重新调用 LLM 翻译这些 chunk

### A2. 短翻译 (< 200 bytes 但 > 50 bytes)
**检测**: 输出文件 50-200 bytes (可能是图注、表格单元格)
**已知**: 当前 **16 个** chunk 是小尺寸
**判断**: 对照源 `chunks/chunkNNNN.md` 大小
- 源 < 200 bytes → 可能是封面/版权,空翻译可接受
- 源 ≥ 1000 bytes → 翻译**未完成**,需补译
**工具**: 新增 `tools/qa_short_translations.py` (按源/译比例判定)
**修复**: 源大译小的 chunk → 重跑翻译

### A3. TODO 占位 marker
**检测**: `re.search(r'⚠️\s*TODO', text)` 或 `(TODO|占位|未完成)`
**已知**: 当前 **9 个** (ch2 × 3 / ch3 × 1 / ch4 × 5)
**工具**: `tools/qa_audit.py` 已统计,需要按 chapter 列清单
**修复**: 找到 TODO 上下文 → 重译 → 替换

### A4. 英文未翻译行 (EN-only row)
**检测**: HTML 行 `<td>` 中只有英文,无中文 (`background-color:#e8e8e8` 缺失)
**工具**: 扩展 `tools/qa_audit.py`,扫描每行 EN|ZH 双列表
**修复**: 用 zh 内容替换

### A5. 主段跳译 / 段落丢失
**检测** (最难):
1. 提取源 chunk 中所有 H2/H3 标题 (`## **Title**`)
2. 检查翻译 chunk 中是否每个源标题都有对应中文标题 (`## **中文**`)
3. 缺失标题 → 该节被跳过翻译
**工具**: 新增 `tools/qa_section_coverage.py`
   ```python
   src_titles = set(re.findall(r"^##\s*\*\*([^*]+)\*\*", source))
   zh_titles  = set(re.findall(r"^##\s*\*\*([^*]+)\*\*", translation))
   missing = src_titles - zh_titles
   ```
**修复**: 把缺失的小节单独提交给 LLM 翻译,合并回 chunk

### A6. 页码锚点保留
**检测**: 源中 `**NNN**` 形页码在翻译中仍在
**意义**: PDF 章节引用 (如 "见第 287 页") 失效 = 翻译质量下降
**工具**: 简单 grep 比对
**修复**: 提示词里强调 "保留所有 `**NNN**` 页码"

---

## 🟡 B. Figure 完整性 (Figure Standalone Placement)

### B1. Figure 未单独成段 (核心问题)
**问题**: 当前 MindShare_PCIe_ch*.md **没有**自动嵌入 figure,翻译段落也没预留 figure 位置
**PCIe6.2 模板要求**:
```markdown
## 2.5.1 Section Title | 小节标题

<table>
<tr><td>EN text...</td><td>ZH text...</td></tr>
</table>

![Figure 2-5: PCIe packet format](figures/chapter_02/fig_0141_5_tight.png)

[⬆️ 返回目录]
```
**检测**: 在 chapter MD 中,figure 应独占一行 (前后空行)
**修复方案** (按优先级):
1. **扫描 `chunks/chunk*.md`** 找 `==> picture [...] intentionally omitted <==` → 已知图片位置
2. **扫描 page render** 找 `Figure X-Y` caption text → 定位页内位置
3. 在 chapter MD 的双语表**之后**插入 `<img>` 标签
**工具**: 新增 `tools/inject_figures.py`

### B2. `<img>` 引用断裂
**检测**: `<img src="figures/chapter_NN/fig_PPPP_N.png">` 但文件不存在
**工具**: 新增 `tools/qa_broken_img_refs.py`
**修复**: 找不到 → 改用 `figures/page/fig_PPPP.png` 全页兜底,或标记 `⚠️ 待补图`

### B3. 跨列/跨页重复 figure
**问题**: PCIe6.2_zh 修复过 85 对重复 (ch2/5/6/7/8/11)
**检测**: 按 file hash 去重 (相同 image hash = 同一张图)
**工具**: `tools/dedup_figures.py` (copy from PCIe6.2_zh/tools/dedup_figures.py)
**修复**: 移除重复文件,更新引用

### B4. Figure 命名混乱
**当前**: 章节目录下混用 `embedded/` 和 `page/` 命名 (如 `page0001_img1.png`)
**目标**: 统一为 `fig_PPPP_NN.png` (page-prefixed,NN = 同页多图序号)
**工具**: `tools/rename_figures.py`

---

## 🟡 C. Figure 剪裁质量 (Crop Distortion)

### C1. 失真检测
**问题**: 紧裁剪 bbox 越界 / 缩放比例异常 / 空白页
**PCIe6.2_zh 的失真判定** (`fix_broken_crops.py`):
```python
def is_broken(f):
    size = os.path.getsize(f)
    if size == 0: return True              # 空
    im = Image.open(f)
    w, h = im.size
    if size < 5KB: return True              # 极小
    if w / h > 6 or w / h < 0.17: return True  # 异常宽高比
    if w < 200 or h < 100: return True      # 极窄条
```
**检测工具**: `tools/qa_crop_distortion.py` (复用 PCIe6.2_zh 逻辑)
**修复**: 失真文件 → 重新渲染为全页 fallback

### C2. 紧裁剪 vs 全页覆盖率
**PCIe6.2_zh 经验**: 12 章共 611 `<img>` 标签,**80% (491)** 升级到 `*_tight.png`,120 个保留全页
**MindShare 现状**: 100% 走全页 `figures/page/`,**0 个紧裁剪**
**下一步**: 实现 `tools/tight_crop_figures.py`
1. 从 PDF 解析每页 layout (用 `page.get_text("blocks")`)
2. 找 "Figure X-Y" caption 块的 bbox
3. caption 上方/下方 1.5x 行距 = figure bbox
4. 渲染 150 DPI 紧裁剪,加 4% padding (PCIe6.2_zh 经验值)

### C3. 矢量图 vs 位图
**问题**: MindShare PDF 中很多 figure 是矢量 (线 + 文字) 不是嵌入位图,只截 PDF 区域会带页眉/页脚/页码
**解决**:
- 紧裁剪时**剔除页眉/页脚** (PCIe6.2_zh `CLIP = fitz.Rect(0, 110, 1275, 1530)`)
- 验证裁剪结果与 figure 实际边界吻合

### C4. 多图页面拆分
**问题**: 一页可能含 2-3 张 figure (如 Figure 4-40 / 4-41 在 page 449)
**PCIe6.2_zh 方案**: 按 caption y 坐标排序,生成 `_1/_2/_3` 后缀
**MindShare**: 当前 `embedded/` 已用 `_img1/_img2` 后缀,但 page render 是整页

---

## 🟠 D. 结构与引用 (Structure & Reference)

### D1. `<table>` 平衡 (open = close)
**工具**: `tools/qa_audit.py` 已覆盖
**当前**: ✅ 358/358 表格平衡

### D2. 灰底 ZH cell 缺失
**检测**: ZH `<td>` 必须带 `style="background-color:#e8e8e8"`
**工具**: 扩展 `qa_audit.py`,扫描每个 `<td>` 的 sibling td

### D3. 锚点重复
**检测**: `<a id="sec-N-X">` 重复
**工具**: 扩展 `qa_audit.py`

### D4. 章节 MD 与 chapter_index.json 一致性
**检测**: 23 个 `MindShare_PCIe_ch*.md` 文件名应匹配 chapter_index.json
**工具**: `tools/qa_consistency.py`

---

## 🛠 待新增的工具脚本

| 脚本名 | 类别 | 来源/参考 |
|--------|------|----------|
| `tools/qa_short_translations.py` | A2 | 全新 (源/译比例判定) |
| `tools/qa_section_coverage.py` | A5 | 全新 (标题完整性) |
| `tools/inject_figures.py` | B1 | 全新 (figure 注入 MD) |
| `tools/qa_broken_img_refs.py` | B2 | 全新 (引用完整性) |
| `tools/dedup_figures.py` | B3 | 复用 `PCIe6.2_zh/tools/ch4_dedup_imgs.py` |
| `tools/rename_figures.py` | B4 | 全新 |
| `tools/qa_crop_distortion.py` | C1 | 复用 `PCIe6.2_zh/tools/fix_broken_crops.py` |
| `tools/tight_crop_figures.py` | C2 | 复用 `PCIe6.2_zh/tools/chx_tight_crops.py` (改为基于 caption y 坐标) |
| `tools/qa_consistency.py` | D4 | 全新 |

---

## 📅 执行节奏

### 第 1 阶段: 立即可做 (基础检查)
```bash
python3 tools/qa_chunk_coverage.py    # A1
python3 tools/qa_audit.py             # D1/D2/D3
python3 tools/qa_short_translations.py # A2 (新建后)
```

### 第 2 阶段: 章节深度检查
```bash
python3 tools/qa_section_coverage.py  # A5 — 标题级翻译完整性
python3 tools/qa_broken_img_refs.py   # B2
python3 tools/qa_consistency.py       # D4
```

### 第 3 阶段: Figure 精修
```bash
python3 tools/inject_figures.py          # B1 — 自动注入
python3 tools/tight_crop_figures.py      # C2 — 紧裁剪
python3 tools/qa_crop_distortion.py      # C1 — 失真检测
python3 tools/dedup_figures.py           # B3 — 去重
```

### 第 4 阶段: 综合验收
```bash
python3 tools/qa_audit.py             # 最终统计
python3 tools/build_html_preview.sh   # HTML 渲染 (如装 pandoc)
```

---

## 📊 当前已知问题 (基于 Round 2 自检实测)

| 类别 | 数量 | 章节分布 | 修复优先级 |
|------|----:|----------|:----------:|
| A1 空翻译 | 21 | Ch 0 (前言) | 🟢 (源文也极短,可接受) |
| A2 小翻译 (源/译比例异常) | 1 | chunk0309 (6%) | 🟡 需补译 |
| A3 TODO marker | 9 | Ch 2/3/4 | 🟡 (源完整,需重译) |
| **A5 小节标题缺失** | **19** | **多个 chunk 0-58% 覆盖率** | 🔴 |
|   └ 严重 0% | 7 | chunk0352-0358 (附录/索引) | 🔴 |
|   └ 部分 23-58% | 12 | 散布在多章 | 🟡 |
| B1 figure 未注入 | 全部 23 章 | 🔴 (核心) |
| B2 img 引用断裂 | 0 | ✅ (尚无 `<img>` 引用) |
| C1 紧裁剪失真 | 35 (10K page1054+ 异常 + 空文件) | 🟡 过滤 |
| C1 空文件 | 2 | page0001_img3, _img4 | 🟡 (CMYK 转换失败) |
| D1 table 平衡 | 0 失衡 | ✅ | 🟢 |
| D3 锚点重复 | 0 | ✅ | 🟢 |
| D4 章节 MD 一致性 | 0 缺失 | ✅ | 🟢 |

### 🔴 重点关注: 小节标题缺失 (A5)

`tools/qa_section_coverage.py` 实测发现 **19 个 chunk** 翻译后小节标题数显著低于源:

```
chunk0227: 28.6% (7 src / 2 out)  - Ch 5 TLP Elements
chunk0266: 28.6% (14 src / 4 out) - Ch 11 PHY Gen1/2
chunk0271: 57.1% (14 src / 8 out) - Ch 12 PHY Gen3
chunk0273: 57.1% (7 src / 4 out)  - Ch 12
chunk0280: 41.7% (12 src / 5 out) - Ch 13 PHY Electrical
chunk0289: 27.8% (18 src / 5 out) - Ch 14 Link Init
chunk0294: 46.4% (28 src / 13 out) - Ch 14
chunk0303: 58.8% (17 src / 10 out) - Ch 14
chunk0309: 33.3% (6 src / 2 out)  - Ch 15 Error Detection
chunk0346: 52.9% (17 src / 9 out) - Ch 99 Appendix
chunk0348: 23.1% (13 src / 3 out) - Ch 99
chunk0351: 50.0% (6 src / 3 out)  - Ch 99
chunk0352:  0.0% (14 src / 0 out) - Ch 99 Appendix C   🔴
chunk0353:  0.0% (10 src / 0 out) - Ch 99             🔴
chunk0354:  0.0% (5 src / 0 out)  - Ch 99 Glossary    🔴
chunk0355:  0.0% (6 src / 0 out)  - Ch 99 Glossary    🔴
chunk0356:  0.0% (11 src / 0 out) - Ch 99 Index B-P   🔴
chunk0357:  0.0% (12 src / 0 out) - Ch 99 Index P-W   🔴
chunk0358:  0.0% (6 src / 0 out)  - Ch 100 Index      🔴
```

**根因**: 翻译 agent 在处理 appendix/index 类型内容时,直接翻译了正文而**漏掉了源中的 `## **章节标题**` 行**。可能是 prompt 里没有强调保留 markdown 结构。

**修复**: 重新翻译这 19 个 chunk,prompt 显式要求:
> "保留所有源中的 markdown 标题 (`## **...**`),翻译为中文 (例如 `## **PCIe 总线**`) 但不删除。"

---

## ✅ 验收标准 (Acceptance Criteria)

MindShare 翻译达到"可发布"状态需要满足:

- [ ] A 类: 0 个 TODO marker,0 个 > 200B 源但 < 200B 译的 chunk
- [ ] B 类: 每个 `##` 小节标题后 5 行内有 figure 引用 (如适用),0 个 `<img>` 失效
- [ ] C 类: 紧裁剪 PNG 全部通过 distortion check (size ≥ 5KB,aspect 0.17-6)
- [ ] D 类: 表格平衡 = 1.0,锚点唯一,zh_gray = 2× open_table

---

## 📚 参考

- `../PCIe6.2_zh/qa_report.json` — 已知问题样本
- `../PCIe6.2_zh/qa_deep_report.json` — 章节级统计
- `../PCIe6.2_zh/CH4_FIGURE_STRATEGY.md` — 双轨制紧裁剪
- `../PCIe6.2_zh/tools/fix_broken_crops.py` — 失真检测
- `../PCIe6.2_zh/tools/chx_tight_crops.py` — 通用紧裁剪
- `../PCIe6.2_zh/tools/dedup_figures.py` — 跨列去重
- `../CXL_zh/tools/extract_ch08_figs.py` — ch8 figure 抽取
- `../CXL_zh/tools/insert_orphan_figures.py` — 孤儿 figure 插入

---

> 🤖 Generated 2026-06-17 · Self-Inspection Plan for MindShare PCIe 3.0 EN_VS_CN repo
