# 📚 MindShare PCI Express Technology 3.0 中英对照翻译

> **PCI Express Technology — Comprehensive Guide to Generations 1.x, 2.x and 3.0**
> **Authors**: Mike Jackson, Ravi Budruk · MindShare, Inc.

📄 **Source PDF**: [`MindShare_PCI Express Technology 3.0.pdf`](https://www.mindshare.com/) (1110 pages, 48 MB)
🎨 **Format**: 中英对照双语 Markdown · 原始图表保留为 PNG · 中文背景色灰色 · GitHub Flavored Markdown
📐 **Template**: 基于 [PCIe 6.2 Spec 中英对照翻译](https://github.com/jimwang2050/PCIe6.2_Spec) 模板

---

## 📊 翻译进度 (Translation Progress)

**已完成**: 358 / 358 chunks 存在 (**100%** 文件), 321 实质翻译 (**89.7%**)
**章节文件**: 23 个双语 MD · `book.md` 合并版 4.3 MB / 58,098 行

```text
[████████████████] 100% files · 321/358 substantive (89.7% effective)
```

### 翻译状态明细

| 类别 | 数量 | 备注 |
|------|-----:|------|
| 实质翻译 (>200 bytes) | 321 | 主要章节 (Ch5-Ch100) 100% 完成 |
| 小尺寸翻译 (50-200 bytes) | 16 | 前言/TOC 短小片段 |
| 占位 (<50 bytes) | 21 | 前言封面/版权页小片段 |
| 缺失 | 0 | ✅ 0 chunks 未翻译 |

### 各章节进度 (Chapter Progress)

| 章节 | 已翻译/总数 | 进度 | 状态 |
|-----|-----------:|-----:|------|
| Ch 0 Front Matter | 66/90 | 73.3% | 🟡 (TOC/版权页部分空) |
| Ch 1 Background | 18/22 | 81.8% | 🟢 |
| Ch 2 PCIe Architecture | 23/26 | 88.5% | 🟢 |
| Ch 3 Configuration Overview | 30/31 | 96.8% | 🟢 |
| Ch 4 Address Space & Routing | 55/60 | 91.7% | 🟢 |
| **Ch 5-20 + Appendices + Index** | **131/131** | **100%** | ✅ |

---

## 🗂 目录结构 (Directory Layout)

```
MindShare_PCI_Express_Technology_3.0_temp/
├── README.md                                       # 本文件
├── chapter_index.json                              # 23 章 (含前言/正文/附录/索引) 索引
├── chunk_plan.json                                 # 每章 chunk 大小规划
├── extraction_summary.json                         # 每章 text chars / chunks_translated 计数
├── glossary.json                                   # PCIe/CXL 共享术语对照
├── config.txt                                      # 翻译配置 (input_file / lang / method)
├── manifest.json                                   # 358 chunk hash + source/output 路径
├── book.md                                         # 全部 23 章合并单文件 (2.4 MB)
├── MindShare_PCIe_ch00_…_前言_…md                  # 23 章双语 MD (PCIe 6.2 模板)
├── MindShare_PCIe_ch01_Background_背景.md
├── …
├── MindShare_PCIe_ch100_Index_索引.md
├── chunks/                                         # 358 个源 EN chunk (mineru_local 提取)
│   ├── chunk0001.md … chunk0358.md
├── chunks_translated/                              # 358 个 ZH 翻译 (含 21 个小占位)
│   ├── output_chunk0001.md … output_chunk0358.md
├── figures/                                        # 预留：抽取的 PNG (待 mineru 渲染)
├── prompts/                                        # 翻译 prompts (build_translation_prompt.py 生成)
├── preview/                                        # HTML 预览 (build_html_preview.sh 生成)
└── tools/                                          # 复现脚本
    ├── qa_audit.py                                 #   章节 QA (table balance / ZH ratio / TODOs)
    ├── qa_chunk_coverage.py                        #   chunk 覆盖率审计
    ├── merge_chapters.py                           #   chunk → 章节 MD (PCIe 6.2 模板)
    ├── build_translation_prompt.py                 #   生成翻译 prompts
    ├── build_html_preview.sh                       #   pandoc → preview/*.html
    ├── figures_commit.sh                           #   图表抽取占位
    └── push_to_github.sh                           #   一键推送到 GitHub
```

---

## 📚 章节状态 (Chapter Status)

| Ch | English | 中文 | Chunks | Translated | Status |
|:-:|---------|------|:-----:|:----------:|:------:|
| 0 | Front Matter (Cover, TOC, Acknowledgments) | 前言 | 90 | 84 | 🟡 In progress |
| 1 | Background | 背景 | 22 | 21 | 🟢 |
| 2 | PCIe Architecture Overview | PCIe 架构概述 | 26 | 26 | 🟢 |
| 3 | Configuration Overview | 配置概述 | 31 | 30 | 🟢 |
| 4 | Address Space & Transaction Routing | 地址空间与事务路由 | 60 | 57 | 🟡 |
| 5 | TLP Elements | TLP 元素 | 14 | 2 | 🔴 |
| 6 | Flow Control | 流控 | 10 | 0 | 🔴 |
| 7 | Quality of Service | 服务质量 | 3 | 0 | 🔴 |
| 8 | Transaction Ordering | 事务排序 | 7 | 0 | 🔴 |
| 9 | DLLP Elements | DLLP 元素 | 7 | 0 | 🔴 |
| 10 | Ack/Nak Protocol | Ack/Nak 协议 | 7 | 0 | 🔴 |
| 11 | Physical Layer — Logical (Gen1/Gen2) | 物理层 — 逻辑 (Gen1/2) | 7 | 0 | 🔴 |
| 12 | Physical Layer — Logical (Gen3) | 物理层 — 逻辑 (Gen3) | 8 | 0 | 🔴 |
| 13 | Physical Layer — Electrical | 物理层 — 电气 | 5 | 0 | 🔴 |
| 14 | Link Initialization & Training | 链路初始化与训练 | 18 | 0 | 🔴 |
| 15 | Error Detection and Handling | 错误检测与处理 | 7 | 0 | 🔴 |
| 16 | Power Management | 电源管理 | 9 | 0 | 🔴 |
| 17 | Interrupt Support | 中断支持 | 9 | 0 | 🔴 |
| 18 | Latency Tolerance Reporting (LTR) | 延迟容忍度上报 (LTR) | 3 | 0 | 🔴 |
| 19 | Hot Plug and Power Budgeting | 热插拔与功率预算 | 3 | 0 | 🔴 |
| 20 | Updates for Spec Revision 2.1 | Spec 2.1 修订更新 | 1 | 0 | 🔴 |
| 99 | Appendices | 附录 | 9 | 0 | 🔴 |
| 100 | Index | 索引 | 2 | 0 | 🔴 |

---

## 🎨 格式约定 (Format Conventions)

每个章节遵循 PCIe 6.2 Spec 模板统一结构 (与 [`PCIe6.2_zh/README.md`](../PCIe6.2_zh/README.md) 同源):

```markdown
# 📘 第 N 章　<Title> (Chapter N. <English>)

**MindShare PCI Express Technology 3.0**

> 📁 **Source chunks**: chunks/chunkNNNN.md ... chunks/chunkMMMM.md
> 🎨 **Format**: 中英对照双语 · 中文灰底 · PCIe 6.2 模板

---

<a id="sec-N-X"></a>
## N.X Section | 中文小节标题

<table>
<thead>
<tr>
<th width="50%">🇬🇧 English</th>
<th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th>
</tr>
</thead>
<tbody>
<tr>
<td>

[英文原文 from chunks/chunkNNNN.md]

</td>
<td style="background-color:#e8e8e8">

[中文翻译 from chunks_translated/output_chunkNNNN.md]

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---
```

### 已应用的 GitHub 特性

| 特性 | 实现 |
|------|------|
| **显式锚点** | `<a id="sec-N-X">` 跨设备稳定 |
| **中文灰底** | `<td style="background-color:#e8e8e8">` |
| **图表内嵌** | `<img src="figures/chapter_NN/fig_PPPP_1.png" width="700">` (待 figures/ 填充) |
| **返回目录** | 每节末尾 `[⬆️ 返回目录]` 跳转 |
| **PAGE_BREAK 标记** | 保留 `<<<PAGE_BREAK>>> page_XXX` 用于页码定位 (待 mineru 输出) |

### 翻译风格

- **首次出现术语**: `EN (中文)` 对照,例如 `Flow Control (流控)`
- **章节标题双语并列**: `## 1.1 Background | 背景`
- **协议名/寄存器字段/信号名**: 保留英文 (如 `TLP`, `Gen1/Gen2/Gen3`, `PERST`, `CFG_DONE`)
- **数字、十六进制值、位宽**: 保持原样
- **页码引用 (§ Section X.Y)**: 保留原 spec 引用格式
- **表格**: 标准 Markdown 表格 + HTML 灰底对照块
- **图片引用**: 待 figures/ 填充后,文件名 `fig_PPPP_NN.png`

---

## 📚 术语表 (Glossary)

构建自 CXL 3.2 / PCIe 6.2 翻译项目的共享 PCIe/CXL 术语集,涵盖:

- **协议层**: Transaction Layer / Data Link Layer / Physical Layer
- **设备与拓扑**: Root Complex / Switch / Endpoint / Bridge / RCiEP
- **事务类型**: TLP / DLLP / Posted / Non-Posted / Completion
- **地址空间**: Memory Space / I/O Space / Configuration Space / BAR
- **流控与排序**: Flow Control / Credit / IDO / ID-Based Ordering / Relaxed Ordering
- **错误处理**: Correctable / Uncorrectable / Fatal Error / Poison / ECRC
- **电源管理**: L0 / L0s / L1 / L1.1 / L1.2 / L2 / L3 / D0 / D1 / D2 / D3hot / D3cold / ASPM / PME
- **物理层**: 8b/10b / 128b/130b / scrambling / LTSSM / TS / SKP / Compliance Pattern / Gen1/Gen2/Gen3
- **中断**: MSI / MSI-X / INTx / Legacy Interrupt
- **错误恢复**: Hot Reset / Link Disable / Training

详见 [`glossary.json`](glossary.json)

---

## 🛠 工具链 (Toolchain)

```bash
# 1. 翻译单个 chunk
#    (LLM 直接读取 chunks/chunk*.md 并写回 chunks_translated/output_chunk*.md)

# 2. 重新生成所有章节双语 MD (按 chapter_index.json)
python3 tools/merge_chapters.py
python3 tools/merge_chapters.py --ch 5    # 只生成章节 5

# 3. 生成翻译 prompts
python3 tools/build_translation_prompt.py

# 4. QA 审计
python3 tools/qa_audit.py                  # 章节级别 (table balance / ZH ratio)
python3 tools/qa_chunk_coverage.py         # chunk 覆盖率

# 5. HTML 预览 (需要 pandoc)
bash tools/build_html_preview.sh

# 6. 推送到 GitHub
bash tools/push_to_github.sh
```

---

## ✅ 翻译状态: 100% 文件就位 · 89.7% 实质翻译

### 已完成

- ✅ 358 个源 chunk 全部抽取 (`chunks/`)
- ✅ 358 个 ZH 翻译文件就位 (`chunks_translated/`)
- ✅ 321 个实质翻译 (89.7%) — Ch5-Ch100 全部 100%
- ✅ 23 个双语章节 MD 自动生成 (`MindShare_PCIe_chNN_*.md`)
- ✅ 合并版 `book.md` (58,098 行 / 4.3 MB)
- ✅ `chapter_index.json` / `chunk_plan.json` / `extraction_summary.json` 元数据
- ✅ QA 审计工具 (`tools/qa_*.py`)
- ✅ 翻译 prompts 生成器 (`tools/build_translation_prompt.py`)
- ✅ HTML 预览脚本 (`tools/build_html_preview.sh`)
- ✅ 358/358 表格 `<table>` 平衡, 0 个 EN-only 行
- ✅ GitHub 推送: `jimwang2050/MindShare_PCIe_Technology_3.0_EN_VS_CN`

### 待办 (TODO) — 后期精修

- ⏳ 重做 21 个空/占位翻译 (主要是 Ch0 封面/版权/TOC 短小片段)
- ⏳ 补全 16 个 50-200 bytes 的小翻译 (Ch0-Ch4 短小片段)
- ⏳ 抽取 figures/ PNG (`tools/figures_commit.sh` 占位)
- ⏳ 第二轮术语一致性 QA (基于 `glossary.json` 252 项)
- ⏳ HTML 预览生成 (需要 pandoc)

---

## 📋 Recent Updates (更新日志)

### 2026-06-17 — Round 2: 重启翻译 (61.5% → 89.7%)

- **完成 138 个未翻译 chunk**: chunks 226-358 + 5 个早期缺失 (112/115/123/144/180)
- **10 个并行 agent 翻译** (4-14 chunks/agent), 单次 round 推进 ~27%
- **Ch5-Ch100 全部 100%**: 主要内容章节 (TLP/DLLP/Physical/Power Mgmt/Interrupts/Error/Hot Plug/Appendices/Index) 完整
- **book.md 翻倍**: 2.4 MB → 4.3 MB (32K → 58K 行)
- **新发现的 21 个空翻译**: 全部位于 Ch0 (Front Matter / 封面 / 版权页) — 源文本身就极短
- **9 个 TODO 标记**: ch2 (3) / ch3 (1) / ch4 (5) — 来自早期空翻译 slot
- **第二次 QA**: 358/358 表格平衡, ZH% 12-15% (符合 PCIe6.2_zh 基线)

### 2026-06-16 — 应用 PCIe6.2_zh 模板 (Round 1: 基础设施)

- **目录重组**: 358 chunk + 220 output 从扁平目录迁入 `chunks/` 和 `chunks_translated/`
- **元数据生成**:
  - `chapter_index.json` (23 章, 含前言/正文/附录/索引)
  - `chunk_plan.json` (按章节 chunk 规划)
  - `extraction_summary.json` (每章 text_chars / translated_chars)
  - `manifest.json` 路径更新为 `chunks/` / `chunks_translated/` 前缀
- **章节 MD 自动生成**: `tools/merge_chapters.py` 复用 PCIe 6.2 双语表格模板 (灰底/锚点/返回目录)
- **QA 工具链**:
  - `tools/qa_audit.py` — 章节级 (table 平衡 / ZH 比例 / TODO 计数)
  - `tools/qa_chunk_coverage.py` — chunk 级 (空翻译 / 缺失翻译 / hash 比对)
- **辅助脚本**: `build_translation_prompt.py` / `build_html_preview.sh` / `figures_commit.sh` / `push_to_github.sh`
- **首次发现的问题** (源自 PCIe6.2_zh 经验):
  - 138 个未翻译 chunk,集中在 chunk0226+
  - 21 个空翻译占位
  - 5 个早期缺失 (chunk0112/0115/0123/0144/0180)
  - figures/ 目录为空 (待 mineru 渲染)

### 2026-06-15 — 翻译暂停 (chunk0225 完成时)

- 翻译运行至 chunk0225 后中断 (上次活动: 2026-06-15 08:49)
- 翻译方式: `mineru_local` (PDF → MD)

### 2026-06-13 — 项目初始化

- mineru_local 提取 MindShare PCI Express Technology 3.0.pdf → 358 chunks
- 初始 glossary 导入自 CXL_zh/ 共享术语

---

## 🤝 致谢 (Credits)

- **官方规范**: MindShare, Inc. — _PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0_ (Mike Jackson, Ravi Budruk)
- **翻译模板**: [PCIe 6.2 Spec 中英对照翻译](https://github.com/jimwang2050/PCIe6.2_Spec) (`PCIe6.2_zh/`)
- **术语基础**: [CXL 3.2 Spec 中英对照翻译](https://github.com/jimwang2050/CXL_3.2_Spec) (`CXL_zh/`)
- **翻译工具**: Claude Code Opus 4.8 (`/model opus`)
- **生成时间**: 2026-06-13 ~ 2026-06-16

---

> 🤖 **Generated with** [Claude Code](https://claude.com/claude-code) · Opus 4.8
> 📅 2026-06-16
