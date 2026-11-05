---
version: alpha
name: Cobalt Grid — Frame (video / frame layer)
description: >
  Cobalt Grid design.md 的视频优先配套文档。基本单位为帧（1920×1080）。原子元素一致且不可改动 — 暖奶油色纸面、电光钴蓝墨色（唯一墨色）、永久方格纸网格、Newsreader 衬线 400 + Hanken Grotesk + DM Mono、顶/底钴蓝细线，以及像素故障 + QR 块签名。构图、帧尺度与宽高比行为按帧重写。动效不在范围内。
unit: 帧 — 主规格 1920×1080；并文档化 9:16 与 1:1
principle: 原子神圣 · 构图自由 · 数值来自脚本

colors:
  paper: "#F0EBDE"
  paper-2: "#E6E0CE"
  ink: "#1F2BE0"
  ink-soft: "#5560E5"
  grid: "rgba(31,43,224,0.10)"
  ink-faint: "rgba(31,43,224,0.18)"

typography:
  # — reading ramp —
  body:        { fontFamily: "Hanken Grotesk", cqw: 0.83, weight: 400, lineHeight: 1.5 }
  body-lede:   { fontFamily: "Hanken Grotesk", cqw: 0.95, weight: 400, lineHeight: 1.5 }
  micro:       { fontFamily: "Hanken Grotesk", px: 13, weight: 600, tracking: "0.16em", upper: true }
  micro-strong:{ fontFamily: "Hanken Grotesk", px: 16, weight: 600, tracking: "0.18em", upper: true }
  mono-tag:    { fontFamily: "DM Mono", cqw: 0.78, weight: 400, tracking: "0.05em" }
  mono-chrome: { fontFamily: "DM Mono", px: 13, weight: 400, tracking: "0.06em" }
  # — display / hero ramp (Newsreader 400, negative tracking) —
  table-name:  { fontFamily: "Newsreader", cqw: 1.5, weight: 400, lineHeight: 1.15 }
  row-headline:{ fontFamily: "Newsreader", cqw: 2.1, weight: 400, lineHeight: 1.05 }
  ed-callout:  { fontFamily: "Newsreader", cqw: 2.6, weight: 400, lineHeight: 1.1, italic: true }
  headline:    { fontFamily: "Newsreader", cqw: 4.6, weight: 400, lineHeight: 0.95 }
  headline-index:{ fontFamily: "Newsreader", cqw: 5.0, weight: 400, lineHeight: 0.95 }
  display-quote:{ fontFamily: "Newsreader", cqw: 5.7, weight: 400, lineHeight: 1.05, tracking: "-0.005em" }
  display-chapter:{ fontFamily: "Newsreader", cqw: 6.8, weight: 400, lineHeight: 1.0, tracking: "-0.005em" }
  display-closing:{ fontFamily: "Newsreader", cqw: 9.4, weight: 400, lineHeight: 0.96, tracking: "-0.005em" }
  display-hero:{ fontFamily: "Newsreader", cqw: 10.4, weight: 400, lineHeight: 0.9, tracking: "-0.008em" }
  vbig-numeral:{ fontFamily: "Newsreader", cqw: 12.5, weight: 400, lineHeight: 0.9, tracking: "-0.015em" }

spacing:
  edge: "4cqw"          # 标准帧边内缩（1920 下约 80px）
  pad-top: "7cqw"
  pad-bottom: "6cqw"
  gap-md: "2cqw"

components:
  graph-grid:
    backgroundImage: "linear-gradient grid, ~2cqw cells, 10% {colors.ink} ({colors.grid})"
    placement: "behind EVERY frame on the ground"
    description: "永久方格纸网格 — 不可关闭；画布基调。"
  hairlines:
    rule: "0.12cqw solid {colors.ink}"
    placement: "≈3cqw from top + bottom, inset {spacing.edge}"
    description: "两条持久钴蓝细线框住每一幅构图。"
  page-chrome:
    typography: "{typography.pagenum}"
    color: "{colors.ink}"
    placement: "page number bottom-right, nav/meta hint bottom-left, above the bottom hairline"
    description: "唯一持久的页面装饰。"
  pixel-glitch:
    backgroundColor: "{colors.paper}"
    fill: "repeating-linear-gradient(90deg, {colors.ink} 0 2px, transparent 2px 8px)"
    size: "14–30cqw wide, full height, stair-stepped"
    placement: "right on cover/data, left on chapter/colophon; z above grid, below headline"
    description: "阶梯状扫描线列。装饰性。"
  qr-block:
    backgroundColor: "{colors.paper}"
    cells: "8×8, {colors.ink} on / {colors.grid} off"
    size: "3–9cqw square"
    shadow: "0 0 0 0.12cqw {colors.paper} (anti-shadow for readability, not elevation)"
    description: "QR 马赛克块 — 角落标点。"
  topbar-rule:
    typography: "{typography.headline-index} + {typography.mono-tag}"
    borderBottom: "0.12cqw solid {colors.ink}"
    description: "索引/数据/表格帧上的区段标题。"
  ledger-row:
    layout: "grid: mono num · Newsreader name · Hanken desc · mono delta"
    borderBottom: "0.06cqw solid {colors.ink-faint} (header 0.12cqw solid {colors.ink})"
    typography: "{typography.mono-tag} + {typography.table-name} + {typography.body}"
    description: "密集矩阵行，带 ↑/↓/— 变化量。"
  pixel-stack-bar:
    cells: "column-reverse, {colors.grid} off / {colors.ink} on"
    baseline: "0.12cqw solid {colors.ink} + {typography.mono-tick} ticks"
    description: "以网格单元格呈现数据；呼应 glitch。"
  vstack-label:
    typography: "{typography.mono-tick}"
    transform: "writing-mode: vertical-rl"
    description: "沿帧边缘的目录装饰。"
---

# Cobalt Grid — Frame（视频 / 帧层）

## 概述

帧尺度的 Cobalt Grid 是一份**双色孔版趋势报告** — 暖奶油纸面、电光钴蓝墨，以及**每一帧背后永久的方格纸网格**。钴蓝是_唯一_墨色：标题、正文、细线、网格、像素故障装饰、QR 补丁。没有强调色，也没有第二层面。

气质是三种字体的对话：**Newsreader** 衬线字重 400（层级靠字号而非字重）承载所有展示与标题；**Hanken Grotesk** 承载正文与大写跟踪标签；**DM Mono** 承载全部装饰 — 页码、标签、刻度、竖排栈。每一帧由顶 + 底钴蓝细线框住；陈述型帧携带**像素故障列**与 **QR-block** 补丁。

**帧尺度关键特征：**

- **严格双色** — 奶油纸 + 钴蓝墨；无强调色、无第二层面。
- **永久 ~2cqw 方格纸网格**（10% 钴蓝）在每一帧背后；不可关闭。
- **顶 + 底 1.5px 钴蓝细线**框住每一构图，按 `edge` 内缩。
- **Newsreader 400** 用于全部展示（负 tracking）；**Hanken 600** 大写 0.16em 标签；**DM Mono** 装饰。
- **像素故障列 + QR-block** 为陈述型帧上的签名装饰补丁。
- **像素堆叠条** 以网格单元格渲染数据（钴蓝开 / 10% 关）。

## 帧

### 帧工艺检验条

在任何结构检查之前，每一帧须通过三项目测检验：

- **眯眼** — 一个 Newsreader 元素在**相对最近邻大 3–6 倍**（`display-hero`/`vbig-numeral`）处占主导；层级靠字号，不靠字重。
- **留白** — 陈述型帧（封面、章节、引语、 colophon）应** 45–60% 留白**，网格可见；**索引台账与数据帧是唯一密集例外**（密度来自安静重复，而非丰富装饰）。
- **克制** — **仅双色**（奶油 + 钴蓝，绝不出现第二色相）；陈述型帧至多一条像素故障列与一个 QR-block。
- **参照** — 对标 **WIRED Japan / Shift 双色孔版专著**；失败样例像**带第二强调色的彩色仪表盘**。

- **主规格：** 1920×1080（16:9）。展示尺寸用 **`cqw`** 编写（`px ÷ 1920 × 100 = cqw`）。
- **竖屏：** 1080×1920（9:16）。**方形：** 1080×1080（1:1）。
- **安全区：** `edge`（4cqw）内缩；细线与页面装饰落在安全线上。

**容器法则（承重）。** 每一帧底面须设 `container-type: size` 并携带方格纸 `background-image`；所有帧相对单位均为相对它的 `cqw`/`cqh` — 绝不用
`vw`。网格 `background-size` 为 `~2cqw 2cqw`，任意渲染尺寸下单元密度一致。

## 色彩

令牌与源文档相同。`{colors.paper}` 为底；`{colors.ink}` 钴蓝为唯一墨色（文字、细线、网格线、故障、QR）。`{colors.ink-soft}` 为次要钴蓝，仅用于编辑副标题；`{colors.grid}`（10%）为永久网格与图表「关」单元；`{colors.ink-faint}`
（18%）为 faint 行分隔。**绝不第二色相** — 强调来自字号、Hanken→Newsreader 切换、mono 变化箭头或透明度，而非颜色。

## 字体

两条 ramp。**阅读 ramp**（Hanken 正文 0.83cqw，mono chrome 用 px）承载文案与标签；
**展示/hero ramp**（Newsreader `headline` 4.6cqw → `vbig-numeral` 12.5cqw）承载每条陈述与数字。

- **可读下限：** 任何承重行 ≥ **1.4cqw**；mono chrome（px）仅用于 colophon。
- **按度量适配：** 按行长度定标题字号。整块上限 **≤ 78cqw**；≤3 词 → `display-hero`/`vbig-numeral`；4–6 → `display-chapter`；7+ → `headline`。
- **Newsreader 仅 400**，钴蓝色，负 tracking（hero −0.008em，numeral −0.015em）。**Hanken 标签大写，0.16–0.18em。** **DM Mono 0.04–0.08em。** 衬线不加粗。

## 深度与表面

扁平。深度仅来自结构：

- **1.5px 钴蓝细线** — 滑动 hairlines、顶栏 rule、图表基线。
- **1px ink-faint 分隔** — 密集列表 / 台账行。
- **方格纸网格** — 一切背后的度量平面基调。
- **像素故障 + QR** — 纹理与图形标点，无 z 轴。

**上限：** 无投影（QR 的 1.5px 纸面外扩仅为可读性反阴影，非 elevation）、无渐变、无圆角、无第二色。

## 形状

- **处处 0 圆角** — 帧、台账行、QR 单元、故障块、图表。零圆形元素；这种方正是身份的一部分。

## 组件

- **graph-grid / hairlines / page-chrome** — 永久帧家具，每一构图继承。
- **pixel-glitch**（边缘列）+ **qr-block**（角落补丁） — 陈述型帧上的签名装饰。
- **topbar-rule** — 索引/数据/表格区段标题。**ledger-row** — 带变化箭头的密集矩阵行。
- **pixel-stack-bar** — 以网格单元格呈现数据。**vstack-label** — 竖排 mono 目录装饰。

## 帧处理

> 配方：底面 · 容器 · 组合 · 焦点 · 装饰 · 强调 · 留白 · 固定/自由 · 密度。
> 网格 + hairlines 出现在每一帧。按类型选密度：陈述型 = 稀疏，索引/数据 = 密集。

### 1 · Hero 封面（身份 · 动作：衬线 + glitch · 左对齐）

**底面** 纸 + 网格，hairlines。**组合** pixel-glitch（右，~26cqw），qr-block（右上），display-hero，ed-callout。**焦点** 1–2 行 `display-hero` Newsreader 钴蓝标题，左锚定，italic `ed-callout` 副标题用 `{colors.ink-soft}`。**装饰** Hanken kicker；mono meta 顶 + 页码。**强调** 无（钴蓝为唯一墨）。**留白** ~45% 纸面。**固定** Newsreader 400，glitch + QR 在场，网格 + hairlines。**自由** 标题、glitch 阶梯图案、QR 位置。**密度** 稀疏。

### 2 · 索引台账（目录 · 动作：密集矩阵 · 左 — 密集帧）

**底面** 纸 + 网格，hairlines，`pad-top`/`pad-bottom`。**组合** topbar-rule，ledger-rows。**焦点** 顶栏（`headline-index` + mono lab-tag，1.5px rule）下 4–6 行台账（mono num · Newsreader name · Hanken desc），ink-faint 分隔。**装饰** 页码。**强调** mono 变化箭头。**留白** 紧 — 密度例外（网格需要填满）。**固定** 1.5px 顶栏 rule，1px ink-faint 分隔，Newsreader 名称。**自由** 行、lab-tag、变化量。**密度** dense-exception。

### 3 · 章节开篇（区段 · 动作：尺度 · 稀疏 · 左）

**底面** 纸 + 网格，hairlines。**组合** pixel-glitch（左，~14cqw，低不透明度），mono index，display-chapter，body-lede。**焦点** `display-chapter` Newsreader 标题，上方小号 mono `CHAPTER NN` 索引，可选 Hanken lede ≤42cqw。**强调** 无。**留白** ~60% — 让网格呼吸。**固定** Newsreader 400，glitch 低不透明度，网格可见。**自由** 标题、lede、glitch 侧。**密度** 稀疏。

### 4 · 数据帧（图表 · 动作：pixel-stack · 左）

**底面** 纸 + 网格，hairlines，`pad-top`。**组合** topbar-rule，pixel-stack-bar 行。**焦点** 6–8 个 pixel-stack 条（钴蓝开 / 10% 关）在 1.5px 钴蓝基线上，带 mono 刻度。**装饰** 顶栏标题 + mono fig-tag；页码。**强调** 无 — 数据即钴蓝单元。**留白** 中等。**固定** 网格单元、钴蓝基线、mono 刻度。**自由** 条值（来自脚本）、刻度标签。**密度** 标准/密集。

### 5 · 宣言 / 引语（引语 · 动作：居中陈述 · 稀疏）

**底面** 纸 + 网格，hairlines。**组合** display-quote（或 display-manifesto），归属 rule，可选紧凑 glitch。**焦点** 2–3 行 Newsreader 钴蓝 pull，上方 Hanken kicker，下方 1px 钴蓝归属 rule + mono 署名。**强调** 无。**留白** ~55% — 刻意开阔。**固定** Newsreader 400，归属 rule，网格可见。**自由** 引语、署名。**密度** 稀疏。

### 6 · Colophon（收尾 · 动作：右对齐结束 · 稀疏）

**底面** 纸 + 网格，hairlines。**组合** pixel-glitch（左缘，镜像封面），display-closing，mono 致谢列。**焦点** 右对齐 `display-closing` Newsreader 标题，上方 Hanken kicker。**装饰** 底部 3–4 列 mono 致谢网格；页码。**强调** 无。**留白** ~50%。**固定** glitch 在左，Newsreader 400。**自由** 收尾行、致谢。**密度** 稀疏。

## 构图规则

### 应当

- 每一帧保留**方格纸网格 + 顶/底 hairlines** — 它们是系统。
- **Newsreader 400 钴蓝**；用字号建层级，不用字重；展示负 tracking。
- **Hanken 标签大写 0.16em**；**DM Mono 装饰 0.04–0.08em**。
- 数据渲染为 **pixel-stack 单元**（钴蓝开 / 10% 关）；呼应 glitch 语言。
- 陈述型帧（封面、章节、引语、colophon）使用 **pixel-glitch 列 + QR 补丁**。
- 倾向：陈述型稀疏透气；索引/数据密集。变化锚点（索引/章节左对齐，引语/收尾居中）。

### 不要

- 不要引入第二墨色 — 仅奶油 + 钴蓝。
- 不要加粗 Newsreader、任何圆角或投影（QR 外扩仅为反阴影）。
- 不要关闭网格或隐藏 hairlines。
- 不要挤满章节 / 引语 / colophon — 那些应让网格显露。
- 不要让衬线标题顶满边缘 — 按度量适配。

## 宽高比行为

| 处理              | 16:9                        | 9:16                                 | 1:1                          |
| ----------------- | --------------------------- | ------------------------------------ | ---------------------------- |
| Hero 封面         | 标题左，glitch 右           | 标题上，glitch 全宽条带              | 标题上，glitch 下            |
| 索引台账          | 顶栏 + 行                   | 顶栏 + 较少行                        | 双列压成单列                 |
| 章节开篇          | 标题左，glitch 左           | 标题上，glitch 侧                    | 标题居中                     |
| 数据帧            | 6–8 条                      | 4–5 条更高                           | 方形图表                     |
| 宣言 / 引语       | 居中 pull                   | 居中，更高                           | 居中                         |
| Colophon          | 右对齐，glitch 左           | 堆叠，glitch 上                      | 居中收尾                     |

网格 + hairlines 在各比例短边上保持；重新分档展示，使无承重行低于 1.4cqw。Mono chrome 保持拉丁/数字 only。

## 已批准实体

源文档未定义真实客户、标识或供应商 — 此类标记渲染为占位。趋势名、信号与数字为内容；系统提供网格与装饰。

## 数字与主张（硬规则）

帧尺度切勿编造数字、变化量、日期或信号计数。槽位渲染为 `— figure —`、
`{metric}`、`↑ —`。pixel-stack 条高度与台账变化量在脚本提供数值前尤其使用占位。Mono 目录序号（001、002…）为装饰，可顺序编号。

## 渲染前自检

- **眯眼** — 一个 Newsreader 元素相对邻元素大 3–5 倍。
- **留白** — 陈述型 45–60% 空；仅索引/数据密集。
- **双色** — 仅奶油 + 钴蓝；任何地方无第二色相。
- **家具** — 网格在场，顶/底 hairlines 在场，页面装饰在 hairline 之上。
- **字体** — Newsreader 400 负 tracking，按度量适配；Hanken 标签 0.16em；≥1.4cqw 下限。
- **深度** — 0 投影（QR 外扩除外），0 圆角。
- **锚点** — 索引/章节/封面左对齐，引语/收尾居中；连续 3 帧不共用锚点。
- **编造** — 每个数字/变化量可追溯到脚本，否则占位。

## 已知缺口

- **动效有意不在范围内。** frame.md 仅规定构图；源文档中 280ms 交叉淡入为 deck 机制。
- **此处 pixel-glitch 用 CSS 渲染**（堆叠扫描线块），而非源文档内联 SVG，以保持展示无 SVG；保真度保留。
- **三款 Google 字体**（Newsreader、Hanken Grotesk、DM Mono）；CJK 配对（Noto Serif SC 700/400）沿用源文档。
- **9:16 / 1:1 为指导**；各比例须验证可读下限与网格密度。
- QR 马赛克与 glitch 阶梯图案为手工编写；无生成层。
