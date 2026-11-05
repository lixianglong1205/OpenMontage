---
version: alpha
name: Broadside — Frame (video / frame layer)
description: >
  Broadside design.md 的视频优先配套文档。基本单位为帧（1920×1080）。原子元素一致且不可改动——双寄存器表面系统（深色墨黑 / 火焰橙）、
  作为图形基元的超大号 Barlow 小写 900 字重、IBM Plex Mono 装饰（大写、0.14em 字距）、单一火焰橙强调色、
  平面构图与 1px 发丝线分隔。构图与帧尺度重写。动效不在本文范围。
unit: 帧 — 主尺寸 1920×1080；9:16 与 1:1 见文档说明
principle: 原子不可改动 · 构图自由 · 数字来自脚本

colors:
  ink-black: "#111111"
  ink-black-alt: "#1A1A18"
  fire-orange: "#E85D26"
  cream: "#F0ECE5"
  cream-muted: "#888880"
  cream-hint: "#505048"
  border-dark: "#282826"
  ink-on-orange-muted: "rgba(17,17,17,0.75)"
  ink-on-orange-hint: "rgba(17,17,17,0.55)"
  ink-on-orange-faint: "rgba(17,17,17,0.40)"
  ink-on-orange-border: "rgba(17,17,17,0.20)"

typography:
  # — 阅读层级 —
  body:    { fontFamily: "Barlow", cqw: 1.2, weight: 400, lineHeight: 1.6 }
  lead:    { fontFamily: "Barlow", cqw: 1.6, weight: 400, lineHeight: 1.5 }
  caption: { fontFamily: "Barlow", cqw: 0.9, weight: 400, lineHeight: 1.5 }
  label:   { fontFamily: "IBM Plex Mono", cqw: 0.72, weight: 500, tracking: "0.14em", upper: true }
  # — 展示 / 主视觉层级（Barlow，小写，负字距）—
  h3:      { fontFamily: "Barlow", cqw: 2.8, weight: 600, lineHeight: 1.2, lower: true }
  quote-text:{ fontFamily: "Barlow", cqw: 3.8, weight: 700, lineHeight: 1.15, tracking: "-0.02em", lower: true }
  h2:      { fontFamily: "Barlow", cqw: 4.5, weight: 700, lineHeight: 1.1, tracking: "-0.02em", lower: true }
  stat-value:{ fontFamily: "Barlow", cqw: 5.5, weight: 900, lineHeight: 1.0, tracking: "-0.04em" }
  h1:      { fontFamily: "Barlow", cqw: 7.5, weight: 800, lineHeight: 0.9, tracking: "-0.03em", lower: true }
  fadelist-item:{ fontFamily: "Barlow", cqw: 7.5, weight: 900, lineHeight: 1.0, tracking: "-0.03em", lower: true }
  quote-mark:{ fontFamily: "Barlow", cqw: 10.0, weight: 900, lineHeight: 0.6 }
  fadelist-title:{ fontFamily: "Barlow", cqw: 10.5, weight: 900, lineHeight: 0.9, tracking: "-0.04em", lower: true }
  display: { fontFamily: "Barlow", cqw: 13.0, weight: 900, lineHeight: 0.88, tracking: "-0.04em", lower: true }

spacing:
  pad-x: "5.5cqw"
  pad-y: "5.5cqw"
  gap-lg: "3.5cqw"
  gap-md: "2cqw"
  gap-sm: "1cqw"

components:
  registers:
    dark: "ground {colors.ink-black}, text {colors.cream}, accent {colors.fire-orange}"
    orange: "ground {colors.fire-orange}, text {colors.ink-black}"
    description: "仅两种表面 — 无奶油/纸面寄存器。每帧一种寄存器。"
  slide-chrome:
    rule: "1px solid {colors.border-dark} (dark) / 20% ink (orange)"
    placement: "top + bottom bars (label left, number right)"
    description: "封面/章节/陈述/引用/结尾帧上关闭 — 宣言式帧让字体占满画面。"
  kicker:
    typography: "{typography.label}"
    color: "{colors.fire-orange} (dark) / 55% ink (orange)"
    description: "大写 mono 眉题。"
  rule:
    backgroundColor: "{colors.fire-orange} (dark) / {colors.ink-black} (orange)"
    size: "36×2px"
    description: "短强调条 — 系统唯一的装饰。"
  broadside-num:
    typography: "{typography.label}"
    placement: "top-left of orange cover/chapter, low opacity"
    description: "Mono 目录编号。"
  stat-card:
    borderTop: "1px solid {colors.border-dark}"
    typography: "{typography.stat-value} (orange on dark / ink on orange) + {typography.body} + {typography.label}"
    description: "仅顶边框块，无其他边框。"
  bullet:
    marker: "orange `/` mono via ::before"
    typography: "{typography.lead}"
    description: "最多三项。"
  bar-track:
    borderLeft: "1px solid {colors.border-dark}"
    bars: "{colors.cream-hint}, one .accent {colors.fire-orange}"
    typography: "{typography.label} axis"
    description: "竖向条形图，仅左侧轴。"
  compare-panel:
    layout: "two equal panels split by a 1px vertical rule"
    payoff: "right panel may fill {colors.fire-orange}"
    description: "前后对比。"
  fadelist:
    typography: "{typography.fadelist-item} ×3 at opacity 1.0/0.5/0.22 + {typography.fadelist-title}"
    description: "三个叠词 + 对侧一个超大标题。"
---

# Broadside — Frame（video / frame layer）

## 概述

帧尺度下的 Broadside 是一套**抗议海报式系统：字号大到文字不再像可读文案，而成为图形基元。** Barlow `display` 在 13cqw 时，单个
小写词几乎横跨整帧。系统运行于**两种寄存器**：深色墨黑底 + 奶油色字（文档向），以及火焰橙底 + 深色墨字（宣言向）。火焰橙是
**唯一**彩色 — 在深色上作强调，在橙色上作环境。平面无层次；层级靠字重、尺寸与 1px 发丝线。

**Barlow** 承担从 display 到 body 的全部文本角色 — 表现力来自字重（400–900）与尺寸，而非字体对比。**IBM Plex Mono** 仅作装饰
（数字、眉题、标签、轴标签、`/` 项目符号），始终大写并加字距。展示层为**小写** — 系统最鲜明的一条决策，是对粗野主义惯例的刻意反转。

**帧尺度关键特征：**

- **两种寄存器** — 深色（奶油字）/ 橙色（墨字）。无奶油/纸面寄存器。
- **超大号小写 Barlow 900**，负字距，作为图形基元（display 13cqw）。
- **火焰橙是唯一彩色** — 深色上作强调，橙色上作整屏环境。
- **IBM Plex Mono 装饰** — 大写、0.14em；`/` 项目符号；mono 目录编号。
- **平面** — 无阴影、无圆角（导航点除外）、无渐变；1px 发丝线承担结构。
- **低密度** — 每帧一条陈述，项目符号最多三项，宣言帧上关闭 chrome。

## 帧（The Frame）

### 帧工艺检查条（Frame Craft Bar）

任意结构性检查之前，每帧须通过三项目测：

- **眯眼（Squint）** — 恰好**一个展示时刻**在 3–6× 尺度上占主导；无竞争者。
- **留白（Silence）** — 宣言帧约 **45–55% 空白**；**统计网格是唯一密集例外**。
- **克制（Restraint）** — **每帧一种寄存器**；**火焰橙是唯一彩色**（深色上强调、橙色上环境）；一个展示时刻；项目符号最多三项。
- **参照（Reference）** — 对标 **Broadside 印刷 / SPACE10 报告 / Wim Crouwel 网格加一种高饱和色**；失败形态像 **多强调色企业幻灯片**。

- **主尺寸：** 1920×1080（16:9）。字号以 **`cqw`** 编写（`px ÷ 1920 × 100 = cqw`；或与源文件 `vw` 1:1 沿用）。
- **竖版：** 1080×1920（9:16）。**方图：** 1080×1080（1:1）。
- **安全区：** `pad-x`/`pad-y` 5.5cqw — 刻意收紧，让超大字号贴近帧边。

**容器法则（承重）。** 每帧背景设置 `container-type: size`；所有帧相对单位均为相对它的 `cqw`/`cqh` — 绝不用 `vw`（`vw` 尺寸的帧在非全屏时会膨胀）。1px 发丝线保持 1px。

## 色彩

令牌与源文件一致，分两种寄存器。**深色：** `{colors.ink-black}` 底、`{colors.cream}` 字、`{colors.fire-orange}` 强调（眉题、强调统计、bullet `/`、引导条、引号标记、rule 短条）。**橙色：** `{colors.fire-orange}` 底、`{colors.ink-black}` 标题与正文，暗墨叠加（75/55/40/20%）作弱化色。每帧选一种寄存器并贯彻。**无第二强调色** — 在橙色上，强调靠墨色的字重/透明度，不用新色相。橙色上不存在奶油字（墨上火为绝对规则）。

## 字体

两条层级。**阅读层级**（Barlow body 1.2cqw，mono label 0.72cqw）承载正文与 chrome；**展示层级**（Barlow `h2` 4.5cqw → `display` 13cqw，字重 700–900）承载每条陈述。

- **可读下限：** 任何承重行 ≥ **1.4cqw**；mono 标签仅作 chrome。
- **按量适配：** 按标题长度定字号。整块 ≤ **78cqw**；≤2 词 → `display`；3–4 → `h1`；5+ → `h2`。Broadside 每帧只放一个 display 时刻。
- **Barlow 展示为小写、字重 700–900、负字距**（最大 −0.04em，h2 −0.02em）。**Mono chrome 大写、0.1em+。** 无斜体、无下划线、无大写展示。

## 深度与表面

仅平面一种手法。层级来自：

- **字重 + 尺寸对比** — 主导信号（900 小写 display）。
- **1px 发丝线** — chrome 条、stat-card 顶边、compare 分隔、bar-track 左侧、图表基线。
- **色移** — 橙上墨、墨上奶油、cream-muted 上 cream。
- **负空间** — 大量、有意的空白区域。

**上限：** 无 box-shadow、无 elevation、无圆角表面（导航点除外）、无渐变底。

## 形状

- **全局 0 圆角**，导航点（50%）除外。卡片、面板、标签、统计块、条 — 均为锐角矩形。

## 组件

- **registers** — 双表面系统。**slide-chrome** — 可选发丝线条，宣言帧上关闭。
- **kicker**（mono 眉题）/ **rule**（36×2 短条）/ **broadside-num**（目录标记）— chrome 装饰组。
- **stat-card**（仅顶边）/ **bullet**（橙色 `/`，最多 3）/ **bar-track**（一条强调条）/ **compare-panel**（橙色 payoff）/ **fadelist**（1.0/0.5/0.22 叠层）。

## 帧处理（Frame Treatments）

> 配方：底 · 寄存器 · 组成 · 焦点 · chrome · 强调 · 留白 · Fixed/Free · 密度。
> 每帧一条陈述；宣言帧上关闭 chrome。

### 1 · 封面（identity · move: massive type · ORANGE register · left）

**底** 火焰橙。**组成** broadside-num、rule、kicker、display、lead。**焦点** 1–2 词 Barlow `display`（13cqw）小写墨字，左锚，其下小墨 rule 短条 + mono kicker；下方 Barlow lead 行 75% 墨。**Chrome** 左上 mono 目录号，右上 mono 元信息（无 chrome 条）。**强调** 在橙底上墨字本身即 pop。**留白** ~45%。**Fixed** 墨上火、小写 900、平面。**Free** 词、kicker、lead。**密度** 低。

### 2 · 陈述（declarative · move: type IS composition · DARK register · left）

**底** 墨黑。**组成** kicker、display。**焦点** 2–4 词 Barlow `display`/`h1` 小写奶油字，其中**一句**着 `{colors.fire-orange}` 墨。**Chrome** mono kicker；无条。**强调** 橙色子句。**留白** ~55%。**Fixed** 小写 900、一句橙色、平面。**Free** 陈述、哪句为橙。**密度** 低。

### 3 · 统计网格（data · move: top-border cards · DARK · the dense frame）

**底** 墨黑，有 chrome 条。**组成** slide-chrome、kicker、3× stat-card。**焦点** 一行三个仅顶边框 stat-card — 大号 Barlow-900 数字 `{colors.fire-orange}`、Barlow 标签、mono 注释。**Chrome** 顶 + 底发丝线条（标签 + 编号）。**强调** 橙色数字。**留白** 中等 — 密度例外。**Fixed** 仅顶边框卡片、橙色数字、1px 发丝线。**Free** 数字（来自脚本）、标签。**密度** 密集例外。

### 4 · 渐隐列表（narrative · move: opacity stack · DARK）

**底** 墨黑。**组成** fadelist（3 个叠放 Barlow-900 词 1.0/0.5/0.22）、fadelist-title。**焦点** 三阶词栈对侧超大 display 标题 `{colors.fire-orange}`（前/中/后）。**强调** 橙色标题。**留白** 中等。**Fixed** 透明度阶梯、小写 900。**Free** 三词、标题。**密度** 低–中。

### 5 · 引文（quote · move: oversized mark · DARK · left）

**底** 墨黑，chrome 关闭。**组成** quote-mark、quote-text、attribution。**焦点** Barlow `quote-text`（700，小写）≤78cqw，其下超大火焰橙 `quote-mark`（10cqw，line-height 0.6）。**Chrome** mono 署名（姓名 + 角色）。**强调** 橙色引号标记。**留白** ~50%。**Fixed** 橙色标记、小写引文。**Free** 引文、署名。**密度** 低。

### 6 · 对比（argument · move: split + orange payoff · DARK→ORANGE）

**底** 左 panel 墨黑 + 右 panel 火焰橙（payoff），1px 分隔。**组成** compare-panel 对、kicker、h3。**焦点** 两 panel — 左文档（深色上奶油），右宣言（橙上墨）。**Chrome** mono panel 标签。**强调** 橙色 payoff panel。**留白** 中等。**Fixed** 右侧墨上火、1px 分隔、平面。**Free** 前后内容。**密度** 标准。

## 构图规则

### 应当

- 所有 Barlow 展示设为**小写字重 900**、负字距 — 系统签名。
- **宣言帧上火焰橙作整屏环境**，**深色上作唯一强调**。
- Chrome 保持 **IBM Plex Mono 大写、0.14em**；使用 `/` mono 项目符号。
- **项目符号最多三项；每帧一条陈述**；用字重、尺寸、1px 发丝线建层级。
- 封面/章节/陈述/引用/结尾上关闭 chrome 条；让字体占满画面。
- 多数帧左对齐；字体即构图。

### 禁止

- 禁止 Barlow 展示大写；禁止第二强调色。
- 禁止橙色上奶油字（墨上火绝对）；禁止奶油/纸面寄存器。
- 无投影、无圆角表面（导航点除外）、无渐变底。
- 无衬线 companion；chrome 从不用 Barlow。
- 禁止一帧两个 display 时刻；禁止长行撑满边 — 应降档。

## 宽高比行为

| 处理       | 16:9                       | 9:16                       | 1:1              |
| ---------- | -------------------------- | -------------------------- | ---------------- |
| 封面       | 词左，lead 下              | 词上，lead 下              | 词居中           |
| 陈述       | display 左                 | display 更高叠放           | display 居中     |
| 统计网格   | 3 横排                     | 3 竖叠                     | 2+1              |
| 渐隐列表   | 栈 + 标题并排              | 栈在标题上                 | 栈在标题上       |
| 引文       | 标记 + 引文左              | 标记上，引文下             | 居中             |
| 对比       | 左右 panel                 | 竖叠（深上橙下）           | 竖叠             |

短边 `pad-x` 保持收紧；重新分档 display，使唯一大行 ≤78cqw 且高于 1.4cqw 下限。Mono chrome 仅拉丁/数字。

## 已批准实体

源文件未定义真实客户、标识或供应商 — 此类标记渲染为占位（虚线 `img-placeholder` 55cqh）。系统提供字体与一种颜色，不提供品牌。

## 数字与主张（硬规则）

帧尺度禁止编造数字、百分比、日期或计数。槽位渲染为 `— figure —`、`{metric}`、`NN%`。stat-card 数字与条高度在脚本提供前用占位。目录号（No. 01）为装饰性 chrome，可顺序编号。

## 渲染前自检

- **眯眼** — 恰好一个 display 时刻占主导；无竞争。
- **留白** — 宣言帧 ~45–55% 空；仅统计网格可密。
- **寄存器** — 每帧一种；橙上墨上火、深上奶油；无第二色相。
- **字体** — Barlow 小写 900 负字距、按量适配；mono chrome 大写 0.14em；≥1.4cqw 下限。
- **深度** — 0 阴影、0 圆角（导航点除外）；仅 1px 发丝线。
- **项目符号** — 最多三项，橙色 `/` 标记。
- **编造** — 每个数字可追溯到脚本，否则占位。

## 已知缺口

- **动效刻意不在范围。** frame.md 仅规定构图；源文件 0.8s  deck 滑入与各元素入场为 deck 机制。
- **Barlow + IBM Plex Mono 经 Google Fonts**；Noto Sans SC 为 CJK 回退（小写 display 信号无 CJK 等价 — 双寄存器色彩系统承担识别，依源文件）。
- **9:16 / 1:1 为指导**；各比例下验证唯一大行 ≤78cqw 且高于下限。
- 条、compare panel、虚线图像占位均为纯 CSS；无需外部图像。
