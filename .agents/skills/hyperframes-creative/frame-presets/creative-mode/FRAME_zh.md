---
version: alpha
name: Creative Mode — Frame (video / frame layer)
description: >
  Creative Mode design.md 以视频为先的配套文档。基本单位是帧（1920×1080），
  而非演示文稿中的单页幻灯片。原子级元素完全一致且不可改动 — 暖奶油色画布、4px 墨色描边、
  硬偏移阴影（无模糊）、Archivo Black 大写 0.92 行高、JetBrains Mono 分类标签、
  Space Grotesk 正文、四色强调 palette。构图、帧尺度与宽高比行为针对帧层重写。
  动效不在本文范围内。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  cream: "#EFE9D9"
  cream-2: "#E4DCC4"
  ink: "#0F0F0F"
  ink-2: "#2A2A2A"
  green: "#1F8A4C"
  green-dark: "#136636"
  pink: "#F06CA8"
  pink-dark: "#D14E8B"
  orange: "#E85A1F"
  yellow: "#F5C518"

typography:
  # — 阅读阶梯（px @ 1920，含 cqw）—
  body-lg:    { fontFamily: "Space Grotesk", px: 28, cqw: 1.46, weight: 400, lineHeight: 1.4 }
  body-md:    { fontFamily: "Space Grotesk", px: 24, cqw: 1.25, weight: 400, lineHeight: 1.3 }
  mono-label: { fontFamily: "JetBrains Mono", px: 24, cqw: 1.25, weight: 400, tracking: "0.06em", upper: true }
  mono-kicker:{ fontFamily: "JetBrains Mono", px: 24, cqw: 1.25, weight: 400, tracking: "0.14em", upper: true }
  table-head: { fontFamily: "Archivo Black", px: 28, cqw: 1.46, weight: 400, upper: true }
  # — 展示 / 主视觉阶梯（帧原生，cqw 优先）—
  step-title: { fontFamily: "Archivo Black", px: 34,  cqw: 1.77, weight: 400, lineHeight: 1.0, upper: true }
  badge-label:{ fontFamily: "Archivo Black", px: 28,  cqw: 1.46, weight: 400, upper: true }
  marker:     { fontFamily: "Archivo Black", cqw: 2.4, weight: 400, lineHeight: 1.0, upper: true }
  stamp-num:  { fontFamily: "Archivo Black", cqw: 2.2, weight: 400, lineHeight: 0.9 }
  stat-num:   { fontFamily: "Archivo Black", cqw: 6.4, weight: 400, lineHeight: 0.88 }
  step-num:   { fontFamily: "Archivo Black", cqw: 7.0, weight: 400, lineHeight: 0.85 }
  display-head: { fontFamily: "Archivo Black", cqw: 4.2, weight: 400, lineHeight: 0.92, tracking: "-0.01em", upper: true }
  display-lg: { fontFamily: "Archivo Black", cqw: 8.0,  weight: 400, lineHeight: 0.9,  tracking: "-0.01em", upper: true }
  display-xl: { fontFamily: "Archivo Black", cqw: 11.0, weight: 400, lineHeight: 0.9,  tracking: "-0.01em", upper: true }
  display-hero:{ fontFamily: "Archivo Black", cqw: 15.5,weight: 400, lineHeight: 0.84, tracking: "-0.02em", upper: true }

spacing:
  frame-pad: "3.3cqw"        # 64px chrome gutter @1920
  content-gutter: "5cqw"     # 96px content gutter @1920
  grid-gap: "1.5cqw"         # 28px
  cell-pad: "1.7cqw"         # 32px

components:
  frame-chrome:
    typography: "{typography.mono-label}"
    placement: "topbar 2.5cqw from top, meta 2.5cqw from bottom, both inset {spacing.frame-pad}"
    rounded: "0"
    shadow: "none"
    description: "Mono 顶栏（左侧分区标签 + 右侧 999px 墨色描边 pill）+ meta 页脚（左侧描述 + 右侧 NN • NN 计数，0.5cqw 墨色圆点分隔）。多数帧均出现。"
  stat-cell:
    backgroundColor: "{colors.green} · {colors.pink} · {colors.orange} · {colors.cream}"
    textColor: "{colors.cream} on accent · {colors.ink} on cream"
    border: "0.4cqw solid {colors.ink}"
    rounded: "0"
    padding: "{spacing.cell-pad}"
    typography: "{typography.stat-num} + {typography.mono-label}"
    shadow: "none"
    description: "扁平强调色/奶油色统计块，直角，无阴影。"
  step-card:
    backgroundColor: "{colors.cream} · {colors.pink} · {colors.yellow} · {colors.green}"
    border: "0.4cqw solid {colors.ink}"
    rounded: "0"
    padding: "{spacing.cell-pad}"
    typography: "{typography.step-num} + {typography.step-title} + {typography.body-md}"
    shadow: "none"
    description: "墨色描边卡片；顶部巨型 step-num。序列在奶油色与强调色间交替，并以 green 结束。"
  marker-block:
    backgroundColor: "{colors.pink}"
    textColor: "{colors.ink}"
    border: "0.4cqw solid {colors.ink}"
    rounded: "0"
    typography: "{typography.marker}"
    shadow: "1.25cqw 1.25cqw 0 {colors.orange}, 1.25cqw 1.25cqw 0 0.2cqw {colors.ink}"
    description: "每帧唯一带硬偏移的 featured callout。"
  kicker-block:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream}"
    typography: "{typography.mono-kicker}"
    padding: "0.5cqw 1cqw"
    rounded: "0"
    description: "反色眉题 chip。"
  badge-rotated:
    backgroundColor: "{colors.yellow}"
    border: "0.4cqw solid {colors.ink}"
    typography: "{typography.badge-label}"
    rounded: "0"
    transform: "rotate(-4deg)"
    description: "刻意不完美的标注。"
  pill-badge:
    backgroundColor: "{colors.cream}"
    border: "0.2cqw solid {colors.ink}"
    rounded: "999px"
    typography: "{typography.mono-label}"
    description: "唯一圆角元素；读作 chip，而非 card。"
  stamp:
    backgroundColor: "{colors.pink}"
    border: "0.4cqw solid {colors.cream}"
    size: "~18cqw square"
    rounded: "0"
    transform: "rotate(-6deg)"
    typography: "{typography.stamp-num}"
    description: "收尾印章，内圈为奶油色圆环。"
  comparison-table:
    backgroundColor: "{colors.cream-2}"
    border: "0.4cqw solid {colors.ink}"
    rule: "0.3cqw solid {colors.ink}"
    rounded: "0"
    typography: "{typography.table-head} + {typography.body-md}"
    shadow: "none"
    description: "墨色表头行 + 奶油色 Archivo 标签；粉/绿列填充变体。"
  decorative-circle:
    backgroundColor: "{colors.yellow}"
    border: "0.4cqw solid {colors.ink}"
    rounded: "50%"
    description: "装饰图形；与 green 面板配对以形成形状对比。"
---

# Creative Mode — Frame（视频 / 帧层）

## 概述

帧尺度的 Creative Mode 是 **披着动态外衣的新粗野主义编辑海报** — 暖奶油纸面、近黑墨色，
以及四种满饱和度相撞的强调色。每一帧都是一块扁平色块构图：无渐变、无模糊阴影、无圆角卡片
（唯一的 pill chip 除外）。纵深来自 **硬偏移阴影**（同色同向的实体副本）或 **色块对比**，
而非光照。

展示语气是 **Archivo Black 严格大写、0.92 行高** — 字母叠过自身 cap height；这种紧凑即品牌。
**JetBrains Mono** 承担全部标签、kicker、计数与轴线的「技术物证」语域。**Space Grotesk** 承担少量正文行。
帧在构造上响亮、在克制上平静：每帧两三种强调色，green 底仅留给单一收尾 plate，硬阴影只花在
一个 featured 元素上。

**帧尺度的关键特征：**

- **奶油底**（`{colors.cream}`）几乎每帧；`{colors.green}` 专用于收尾 plate。
- **0.4cqw（@1920 为 4px）墨色描边** 于每个结构元素；内部规则 0.3cqw。
- **硬偏移阴影**（≈1.25cqw，orange+ink）每帧一个 featured 块 — 永不模糊。
- **Archivo Black 大写**，0.92 行高，始终；不存在 sentence-case 的 Archivo Black。
- **每帧两三种强调色**，永非四种齐上；碰撞即设计。
- **每帧一个 pill chip**（999px）为唯一圆角元素。

### 帧工艺门槛

任何结构性检查之前，三项目测把关每一帧：

- **眯眼** — 恰好一个元素主导，为 **最近邻的 3–6×**（是鸿沟，不是缓坡）：`display-hero`/`display-xl` 主张或 `stat-num` 数字，永非两个 rival 标题。
- **留白** — 稀疏帧（封面、主张、收尾）读作 **45–60% 空**；**统计网格与对比 ledger 是唯一密集例外**。勿为「看起来完整」而填满稀疏帧。
- **克制** — 稀缺手势 **每帧至多一次**：至多一个硬偏移阴影、两至三种强调色（永非四种齐上），green 底专用于单一收尾 plate。
- **参照** — 瞄准 **Risograph 编辑海报 / punk-zine 跨页**（扁平墨色块、一句大主张、大片 cream）；失败则像 **圆角、软阴影的 SaaS 功能网格**。

## 帧（The Frame）

- **主比例：** 1920×1080（16:9）。所有展示尺寸以 **`cqw`** 编写（`px ÷ 1920 × 100 = cqw`）。
- **竖屏：** 1080×1920（9:16）。**方形：** 1080×1080（1:1）。
- **安全区：** chrome 内缩 `3.3cqw`（64px）；内容沟槽 `5cqw`（96px）。无承重元素越过 `3.3cqw` 线。

**容器法则（承重）。** 每一帧底设置 `container-type: size`。所有帧相对单位均为 `cqw`/`cqh`（1cqw = 帧宽的 1%），相对该底解析 — **永不用 `vw`。** `vw` 度量页面视口，帧非全屏渲染时会膨胀；`cqw` 在任意渲染尺寸下相对帧解析。故展示阶梯中每一尺寸均为 `cqw`。

## 色彩

令牌与源文档一致。帧尺度：`{colors.cream}` 为 **底**，`{colors.ink}` 为描边 + 字色，四强调色（`green` / `pink` / `orange` / `yellow`）为 **扁平填充，每帧 ration 两至三种。** `{colors.orange}` 亦为硬阴影色。`{colors.green}` 兼作唯一收尾 plate 底 — 稀缺即冲击。勿引入第五强调色；勿用纯白；勿渐变。

## 字体

两档阶梯。**阅读阶梯**（正文、mono 标签、表头）为 chrome 与文案保留 px+cqw。**展示/主视觉阶梯** 帧原生、以 `cqw` 编写 — 自 `display-head`（4.2cqw）至封面 wordmark 的 `display-hero`（15.5cqw）。

- **可读下限：** 任何承重行 ≥ **1.4cqw（@1920 ≈27px）**。1.15cqw 的 mono chrome 仅作 colophon。
- **按量适配：** 标题字号随行长。标题块上限 **≤ 78cqw**，勿触安全边距。≤3 词 → `display-hero`/`display-xl`；4–6 词 → `display-lg`；7+ 词 → `display-head`。短行做大；长行降档。
- **全部 Archivo Black 大写 + 0.92 行高**，始终。Mono 用 0.06–0.14em 字距。勿将 Archivo Black 字距超出编码的 −0.01em；勿居中排正文。

## 纵深与表面

零模糊。仅两种纵深手段：

- **硬偏移阴影** — 实体副本在 X、Y 各偏移 ≈1.25cqw（`box-shadow: 1.25cqw 1.25cqw 0 {colors.orange}, 1.25cqw 1.25cqw 0 0.2cqw {colors.ink}`）。**每帧一个 featured 块**（marker、stamp）。图示堆叠可用仅 ink 的 0.95cqw 偏移。
- **色块对比** — cream 上 cream-2、ink 上 cream、强调色上 cream。对比足够时无需阴影。

**上限：** 无模糊阴影、无渐变、无 glow，任何地方皆然。

## 形状

- **0 圆角** 于每个结构元素 — stat cell、step card、表格单元、marker、面板。
- **50%** 于装饰圆、stamp 内环、meta 圆点。
- **999px** 仅顶栏 pill chip — 唯一圆角例外。
- **旋转** 仅于固定品牌角：badge −4deg，stamp −6deg。

## 组件

- **frame-chrome** — mono 顶栏 + meta 页脚。多数帧出现；仅在与 pure full-bleed wordmark 节拍冲突时省略。
- **stat-cell / step-card** — 墨色描边扁平填充块；step 序列以 green 结束。
- **marker-block** — 每帧唯一带硬阴影的 featured callout。
- **kicker-block** — 反色 ink 眉题 chip；**badge-rotated** — −4deg 黄色标注；**pill-badge** — 唯一圆角 chip。
- **stamp** — −6deg 收尾印章。**comparison-table** — cream-2 ledger，墨色表头行。
- **decorative-circle** — 黄色圆盘，与 green 面板形成形状对比。

## 帧处理（Frame Treatments）

> 每 plate 配方：底 · 容器 · 组合 · 焦点 · chrome · 强调 · 留白 · Fixed/Free · 密度。
> 按 1920×1080 编写。默认居中偏置；变换锚点；每帧一个想法。

### 1 · Wordmark 封面（identity · move: full-frame lockup · centered）

**Ground** `{colors.cream}`，`frame-pad`。**Container** grid，chrome 上下，焦点居中。
**Composes** frame-chrome、wordmark。**Focal** 两行 wordmark 于 `display-hero`
（15.5cqw），居中，第二行用强调色（`{colors.pink}`/`orange`）。**Chrome** mono 顶栏
（分区标签 + pill）与 meta 页脚（描述 + 01•NN）。**Accent** 仅第二行色；
可选一角 decorative-circle 出血出边。**Silence** ~55% 空 cream。
**Fixed** Archivo Black 大写 0.84 lh，wordmark 上一处强调，直角。**Free** 哪一强调色、
换行、圆是否出血角。**Density** sparse。

### 2 · Big Claim（超大陈述 · move: scale · left）

**Ground** 全出血单一强调色（`{colors.pink}`/`green`/`orange`），`content-gutter`。**Container**
flex，主张左锚、垂直居中。**Composes** kicker-block、主张。**Focal**
2–3 行主张于 `display-xl`/`display-lg`，强调底上的 ink（ink-on-fire — 永非白字）。
**Chrome** 主张上方小 ink kicker-block；mono meta 页脚。**Accent** 底即强调色；无第二强调竞争。
**Silence** ~45% 色域空。**Fixed** 强调底上 ink 字、按量适配、类型无阴影。**Free** 主张文案、哪一强调底、哪词断行。
**Density** sparse — 一个想法。

### 3 · Stat Grid（目录 · move: density — 唯一密集帧 · centered）

**Ground** `{colors.cream}`，`content-gutter`。**Container** grid：居中 `display-head` 下
3-up stat-cell 行。**Composes** frame-chrome，3× stat-cell。**Focal** 三个
墨色描边单元行（green / pink / orange），各为 `stat-num` + mono 标签。**Chrome** mono 顶栏 +
meta。**Accent** 三格填充（命名的密度例外 — 此处允许三种强调）。
**Silence** ~25% — 刻意紧。**Fixed** 0.4cqw 描边、直角、格无阴影、
mono 标签。**Free** 三个数字+标签、头文案、哪三种强调。**Density** dense-exception。

### 4 · Closing Plate（收尾 · move: ground-swap · centered）

**Ground** `{colors.green}`（整段唯一 green 帧），`frame-pad`。**Focal** 2 行
sign-off 于 `display-lg`，`{colors.cream}`，居中。**Composes** frame-chrome（cream 变体）、
stamp。**Chrome** cream mono 顶栏 + meta。**Accent** 一角 `{colors.pink}` stamp 旋转 −6deg，
cream 环 + stamp-num。**Silence** ~55% 空 green。**Fixed** green 底专用于此节拍，
cream-on-green 字，一枚 stamp。**Free** sign-off 文案、stamp 文字、stamp 角。**Density** sparse。

### 5 · Featured Marker（callout · move: hard-shadow focal · left/asymmetric）

**Ground** `{colors.cream}`。**Composes** frame-chrome、marker-block、可选 body-md 支撑行。
**Focal** 粉色 marker-block 带 signature orange+ink 硬偏移阴影，非对称放置。
**Accent** 粉块 + orange 阴影（两强调）。**Silence** ~50%。**Fixed** 帧上恰一硬
阴影，0.4cqw 描边。**Free** marker 文案、块位置、可选支撑行。**Density** sparse。

### 6 · Comparison Ledger（数据 · move: matrix · left）

**Ground** `{colors.cream}`，`content-gutter`。**Composes** frame-chrome、comparison-table。
**Focal** cream-2 表，墨色表头行；一列填充（pink 或 green）标胜者。
**Accent** 单一列填充。**Silence** 紧 — 第二密度例外。**Fixed**
cream-2 填充、0.3cqw 内规则、墨色表头行 + cream Archivo 标签。**Free** 行、哪列填充、文案。
**Density** dense-exception。

## 构图规则

### 应当

- 围绕 **每帧一个想法** 构图，焦点 **为邻元素的 3–5×**（眯眼测试）。
- **默认居中偏置** — 封面、主张、统计网格、收尾均居中焦点；marker 与 ledger 保留左/非对称。
- 稀疏帧保持 **45–60% 空**；仅统计网格与 ledger 跑密集。
- **每帧两至三种强调**；`{colors.green}` 底专用于收尾 plate。
- 硬偏移阴影花在 **每帧一个 featured 块**。
- 标题 **按量适配**；Archivo Black 大写 0.92 lh 渲染。

### 禁止

- 勿圆角（pill chip 除外）；勿渐变、模糊或 glow。
- 勿 sentence-case 的 Archivo Black，勿字距超出 −0.01em。
- 勿一帧四种强调齐上、第五强调或纯白。
- 勿居中正文，勿非 JetBrains Mono 的标签。
- 勿标题顶满边 — 长行降阶梯。
- 勿一帧两个硬阴影。

## 宽高比行为

| 处理              | 16:9                            | 9:16                         | 1:1                      |
| ----------------- | ------------------------------- | ---------------------------- | ------------------------ |
| Wordmark Cover    | 两行居中                        | 更高堆叠，圆在上方           | 居中，更紧               |
| Big Claim         | 主张居左，全强调底              | 主张在上，强调全幅           | 主张居中                 |
| Stat Grid         | 标题下 3 列行                   | 标题上，3 行堆叠             | 标题上，2×2（第 4 格）   |
| Closing Plate     | sign-off 居中，stamp 角         | 堆叠，stamp 在下             | 居中，stamp 角           |
| Featured Marker   | marker 非对称                   | marker 居中，阴影向下        | marker 居中              |
| Comparison Ledger | 全宽表                          | 表滚动为更少列               | 2 列表                   |

安全区在各比例短边保持 `3.3cqw` chrome 内缩；按比例重设展示，使无承重行低于 1.4cqw 下限。

## 已批准实体

源文档未定义真实客户、logo 或供应商 — 此类标记一律作占位渲染。产品/分区与内容无关；系统提供几何，非品牌。

## 数字与主张（硬规则）

帧尺度勿臆造数字、百分比、计数或日期。数据槽渲染为
`— figure —`、`{metric}`、`N×`。真实数字仅当脚本提供 — 统计网格与 ledger 尤其用占位，非捏造值。

## 渲染前自检

- **眯眼** — 一元素以 3–5× 主导邻元素，否则 rescale。
- **留白** — 稀疏帧 45–60% 空；仅统计网格 / ledger 密集。
- **强调** — 每帧两至三种，永非四种齐上；green 底仅收尾。
- **纵深** — 0 模糊；至多一硬偏移阴影；否则色块对比。
- **几何** — 直角除 pill；旋转仅 −4/−6deg。
- **字** — Archivo Black 大写 0.92 lh，按量适配，承重行 ≥1.4cqw。
- **锚点** — 默认居中；左/非对称仅 marker + ledger；勿连续 3 帧同锚。
- **捏造** — 每个数字可溯至脚本，否则占位。

## 已知缺口

- **动效刻意不在范围。** frame.md 仅规定构图；时序与转场为后续阶段。收尾 green 描述为 _plate_，非转场。
- **Archivo Black 需 Google Fonts**；回退为 `sans-serif`。CJK 配对（Noto Serif SC 900 / NSC 400）沿用源文档 CJK 章节。
- **9:16 / 1:1 为指导**，非像素锁定；各比例验证可读下限。
- 装饰几何（圆、stamp、堆叠块）仅 CSS；无需外部图像。
