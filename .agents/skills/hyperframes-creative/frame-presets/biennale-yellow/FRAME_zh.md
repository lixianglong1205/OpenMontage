---
version: alpha
name: Biennale Yellow — Frame (video / frame layer)
description: >
  以视频为先的双年展黄（Biennale Yellow）design.md 配套文档。基本单元为帧（1920×1080）。原子元素保持一致且不可违背——暖羊皮纸底、单一深靛蓝墨色、以 bloom / panel / tile 底纹形式部署的 solar yellow，Instrument Serif 展示字 + Archivo 无衬线 + JetBrains Mono 数据字，1px 发丝线作为唯一边框，大气式景深（无阴影），以及右下页码。构图与帧尺度重写。克制为法则；动效不在范围内。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  paper: "#E9E5DB"
  paper-deep: "#DCD6C4"
  sun: "#F1EE2E"
  sun-soft: "#F8F39B"
  haze: "#F0DA7C"
  ink: "#1B2566"
  ember: "#E26B4A"

typography:
  # — reading + data ramp —
  body:    { fontFamily: "Archivo", cqw: 0.85, weight: 400, lineHeight: 1.5, color: "ink" }
  body-lede:{ fontFamily: "Archivo", cqw: 0.95, weight: 400, lineHeight: 1.55 }
  micro-label:{ fontFamily: "Archivo", px: 13, weight: 600, tracking: "0.18em", upper: true }
  rail-label:{ fontFamily: "Archivo", px: 13, weight: 600, tracking: "0.32em", upper: true }
  mono-data:{ fontFamily: "JetBrains Mono", cqw: 0.73, weight: 400, tracking: "0.04em" }
  pagenum: { fontFamily: "JetBrains Mono", px: 13, weight: 400, tracking: "0.08em", opacity: 0.75 }
  # — display ramp (Instrument Serif 400, tight, negative tracking) —
  ledger-title:{ fontFamily: "Instrument Serif", cqw: 1.55, weight: 400, lineHeight: 1.15 }
  strand-title:{ fontFamily: "Instrument Serif", cqw: 1.7, weight: 400, lineHeight: 1.1 }
  headline-sm:{ fontFamily: "Instrument Serif", cqw: 2.9, weight: 400, lineHeight: 1.0 }
  headline:{ fontFamily: "Instrument Serif", cqw: 4.6, weight: 400, lineHeight: 1.06, tracking: "-0.005em" }
  date-rail:{ fontFamily: "Instrument Serif", cqw: 5.0, weight: 400, lineHeight: 0.96, tracking: "-0.005em" }
  display-it:{ fontFamily: "Instrument Serif", cqw: 7.0, weight: 400, italic: true, lineHeight: 1.04, tracking: "-0.005em" }
  numeral-md:{ fontFamily: "Instrument Serif", cqw: 7.5, weight: 400, lineHeight: 0.92, tracking: "-0.01em" }
  display:{ fontFamily: "Instrument Serif", cqw: 14.6, weight: 400, lineHeight: 0.86, tracking: "-0.018em" }
  numeral-jumbo:{ fontFamily: "Instrument Serif", cqw: 28.0, weight: 400, lineHeight: 0.84, tracking: "-0.04em" }

spacing:
  pad-edge: "4cqw"
  pad-region: "4.2cqw"
  gap-region: "2.5cqw"

components:
  sun-bloom:
    background: "radial gradient {colors.sun} core → {colors.sun-soft} → {colors.haze} → transparent on {colors.paper}"
    size: "42–70% of the frame, off-center or behind the focal element"
    description: "主景深图层。每帧一个；无 bloom 的平坦羊皮纸帧会显得残缺。"
  ember-bloom:
    background: "radial {colors.ember} at 15–22% opacity"
    placement: "corner opposite the sun-bloom"
    description: "从属的冷暖对位平衡；绝不可喧宾夺主。"
  block-tile:
    backgroundColor: "{colors.sun} at 40–70% opacity"
    layout: "rectangles on an 8×4 grid behind cover/colophon"
    description: "分层海报底纹。"
  yellow-panel:
    backgroundColor: "{colors.sun}"
    textColor: "{colors.ink}"
    rounded: "0"
    border: "none (meets paper directly)"
    description: "满出血列/三分之一——最强色块陈述，墨色叠于其上。"
  hairline-rule:
    rule: "1px solid {colors.ink} (soft variant: {colors.ink} at 18–20%)"
    description: "唯一边框——页眉下划线、页脚顶线、台账分隔。不存在更粗的线条。"
  strand-row:
    borderBottom: "1px {colors.ink} 18–20%"
    typography: "{typography.strand-title} + {typography.body}"
    description: "衬线序号 + 衬线标题 + 无衬线正文。编号式编辑列表。"
  ledger-row:
    borderBottom: "1px {colors.ink} 18–20%"
    typography: "{typography.mono-date} · {typography.ledger-title} · {typography.body} · {typography.mono-data}"
    description: "四列表格——等宽日期 · 衬线标题 · 无衬线场地 · 等宽时长（右对齐）。"
  footer-band:
    borderTop: "1px solid {colors.ink} per cell"
    typography: "{typography.micro-label} + {typography.body-sm}"
    description: "封面/ colophon 底部的四列元数据条带。"
  vertical-rail:
    typography: "{typography.rail-label}"
    transform: "rotated up the left edge"
    description: "章节/分隔帧左侧缘的区块标记。"
  pagenum:
    typography: "{typography.pagenum}"
    color: "{colors.ink} at 75%"
    placement: "bottom-right"
    description: "唯一持久存在的界面元素。"
---

# Biennale Yellow — Frame（视频 / 帧层）

## 概述

帧尺度下的双年展黄是一套**文学编辑型系统**，气质接近艺术双年展图录：暖羊皮纸、单一深靛蓝墨色，以及作为氛围的 solar yellow。无卡片、无按钮、无阴影、无圆角——结构词汇只有**纸、墨、黄。** 景深由柔和径向 **sun bloom** 提供，而非 elevation。

声音由三种字体承担固定角色：**Instrument Serif**（字重 400、紧凑行高、负字距）承载从 40px 到 720px+ 的所有展示、数字与引文；**Archivo** 承载正文与宽字距大写 micro-label；**JetBrains Mono** 承载所有日期、数字与页码。文字**始终为 ink**——对比来自字号与字重，而非颜色。整体气质介于折叠博物馆手册与慢读文学季刊之间：自信、有氛围、极度克制。

**帧尺度的关键特征：**

- **暖羊皮纸底**贯穿每一帧；绝不用白、绝不用灰。
- **单一 ink**（`{colors.ink}`）用于全部字体与全部线条；**solar yellow** 用于 bloom / panel / tile。
- **Instrument Serif 400** 展示（紧凑、负字距）；**Archivo** 正文 + micro-label；**JetBrains Mono** 数据。
- **1px 发丝线**是唯一边框——不存在更粗线宽；**无阴影、无圆角**。
- **Sun bloom** 是每帧主景深层；ember 对位 bloom 增加冷暖张力。
- **编辑式克制**——稀疏即优雅；拥挤会破坏图录感。

## 帧（The Frame）

### 帧工艺门槛（Frame Craft Bar）

三道肉眼检验优先于任何结构检查：

- **眯眼（Squint）**——一处 Instrument Serif 时刻在 3–6× 邻域字号上占主导；sun bloom 牵引视线中心。
- **留白（Silence）**——帧面约 **55–60% 为空**；**台账（ledger）是唯一密集例外**（密度来自安静的发丝线重复，而非视觉 richness）。
- **克制（Restraint）**——**一种 ink 色**用于全部字体与线条；**一个 sun bloom** 每帧（+ 可选从属 ember）；绝不反色（无黄字 on ink）。
- **参照（Reference）**——对标**艺术双年展图录 / 慢展海报 / 文学季刊**；失败形态像**扁平 CMS 模板**（无 bloom）或**带边框卡片堆**。

- **主比例：** 1920×1080（16:9）。展示尺寸用 **`cqw`** 编写（`px ÷ 1920 × 100 = cqw`）。
- **竖屏：** 1080×1920（9:16）。**方图：** 1080×1080（1:1）。
- **安全区：** `pad-edge` 4cqw（约 40–76px）——优雅依赖边缘负空间；仅 bloom、tile、panel 可出血。

**容器法则（承重）。** 每一帧底图设置 `container-type: size`；所有帧相对单位均为相对它的 `cqw`/`cqh`——绝不用 `vw`。发丝线保持 1px；bloom 尺寸按帧 **%** 缩放。

## 色彩（Colors）

令牌与源文件一致。`{colors.paper}` 为 universal 底；`{colors.ink}`（深靛蓝 navy）是**每一行字与每一条线**——没有次要文字色。`{colors.sun}` 三种用法：**bloom**（径向氛围）、**yellow-panel**（满出血海报填色，ink 在上）、**block-tile** 底纹。`{colors.sun-soft}`/`haze` 为 bloom 中/外圈色标。`{colors.ember}` **仅**以 15–22% 对位 bloom 出现——不作填色、不作文字。**系统从不反色**——ink on sun 正确；黄字 on ink 不存在。

## 字体（Typography）

两条 ramp。**阅读/数据 ramp**（Archivo 正文 0.85cqw ink、px 级 micro-label、JetBrains Mono 数据）承载文案与 chrome；**展示 ramp**（Instrument Serif `ledger-title` 1.55cqw → `numeral-jumbo` 28cqw）承载全部标题、数字与引文。

- **可读下限：** 任何承重行 ≥ **1.4cqw**；px 级 mono/label 仅为 chrome。
- **按度量适配：** 标题字号随长度调整。整块上限 **≤ 78cqw**；≤3 词 → `display`；4–6 → `headline`；7+ → `headline-sm`。jumbo 数字是分隔帧的要点——不要缩小。
- **Instrument Serif 仅字重 400**（其对比即字重信号），紧凑行高（0.84–1.06）、负字距；**micro-label 大写 Archivo 600，≥0.16em**；**数字/日期一律 mono**。无粗衬线、无第二文字色、正文/展示不用 mono。

## 景深与表面（Depth & Surface）

大气式，非结构式。景深来自：

- **Sun bloom**——主层：分层径向（sun 70–95% 核心 → sun-soft → haze 18–22% → paper 0%），占帧 42–70%。每帧一个。
- **Ember bloom**——对侧角落 15–22% 桃色对位 bloom；始终从属。
- **Block-tile 底纹**——8×4 网格上半透明黄矩形（封面/colophon）。
- **Yellow panel**——唯一「硬」色块陈述：灌满列/三分之一，ink 在上。
- **Hairline rules**——1px ink 结构分隔（密集行用 soft 18–20% 变体）。

**上限：** 零 box-shadow、零 text-shadow、零圆角、无粗于 1px 的边框。

## 形状（Shapes）

- **一切半径为 0**——严格矩形。Bloom 无硬边（渐隐入 paper）。

## 组件（Components）

- **sun-bloom / ember-bloom / block-tile**——大气景深组。**yellow-panel**——海报填色陈述。
- **hairline-rule**——唯一边框（1px ink；密集行用 soft 变体）。
- **strand-row / ledger-row / footer-band**——编辑列表、表格式日历、元数据条带。
- **vertical-rail**——旋转章节标记。**pagenum**——右下 mono chrome。

## 帧处理（Frame Treatments）

> 配方：底 · 容器 · 组合 · 焦点 · chrome ·  accent · 留白 · 固定/自由 · 密度。
> 每帧必有 sun bloom + 右下 pagenum；稀疏为默认。

### 1 · 封面（身份 · 动势：display + sun bloom · 左）

**底** paper + 大型 sun-bloom（偏左）+ ember 对位 bloom（对角）。**组合** micro-label、display、date-rail、footer-band、pagenum。**焦点** 两行 Instrument Serif `display`（关键词 italic）ink 左对齐，位于 micro-label 下。**Chrome** 右上 serif date-rail；底部四列 footer-band。**Accent** sun bloom + yellow。**留白** bloom 托住开放空间。**固定** ink 字、一 bloom、1px 页脚线、无阴影。**自由** 标题、日期、页脚单元。**密度** 低。

### 2 · 章节分隔（区块 · 动势：jumbo 数字 · 竖向 rail）

**底** paper + 角落锚定 sun-bloom。**组合** vertical-rail、numeral-jumbo、headline-sm。**焦点** 单个巨大 Instrument Serif `numeral-jumbo`（≈28cqw）占主导，下方 serif 标题。**Chrome** 左缘旋转 vertical-rail 标签；pagenum。**Accent** 数字后的 bloom。**留白** ~60%。**固定** serif 400、jumbo 数字、rail 标签。**自由** 序数、标题、rail 文案。**密度** 低。

### 3 · 台账（目录 · 动势：发丝线表格式行 · 密集帧）

**底** paper（bloom 可选、 subtle）。**组合** headline-sm + micro-label 顶栏、ledger-rows。**焦点** 四列表格式日历——mono 日期 · serif 标题 · sans 场地 · mono 时长——在 1px ink 顶栏线下以 hairline-soft 分隔。**Chrome** pagenum。**Accent** 无——密度来自安静重复，而非颜色。**留白** 紧——密度例外（靠重复而非 richness）。**固定** 发丝线、mono 日期、serif 标题。**自由** 行、场地。**密度** dense-exception。

### 4 · 宣言 / 引文（引语 · 动势：italic serif · 居中 bloom）

**底** paper + 居中 sun-bloom。**组合** numeral-lg 引号、display-it、 attribution。**焦点** 两行 Instrument Serif **italic** `display-it` 引文 ink 居中， oversized serif 引号下。**Chrome** micro-label attribution。**Accent** 居中 bloom。**留白** ~60%——刻意开放。**固定** italic serif、一 bloom、ink。**自由** 引文、 attribution。**密度** 低。

### 5 · 海报面板（陈述 · 动势：yellow panel · 分栏）

**底** paper + 满出血 `{colors.sun}` `yellow-panel`（列或三分之一）。**组合** yellow-panel、micro-label、headline。**焦点** Instrument Serif `headline` ink **落在 sun panel 上**（ink-on-yellow——签名式）。**Chrome** micro-label；pagenum。**Accent** panel 本身。**留白** paper 侧保持开放。**固定** ink-on-sun、panel 直贴 paper（无边框）、无阴影。**自由** 标题、panel 侧/宽。**密度** 低。

### 6 · 脉络列表（ programme · 动势：编号编辑行 · 左）

**底** paper + subtle sun-bloom。**组合** micro-label、headline-sm、strand-rows。**焦点** 编号列表——serif 数字 + serif 标题 + sans 正文，hairline-soft 分隔。**Chrome** micro-label；pagenum。**Accent** bloom。**留白** 适中；行距透气。**固定** serif 数字、hairline-soft 线。**自由** 条目、文案。**密度** standard。

## 构图规则（Composition Rules）

### 应当（Do）

- 从**暖羊皮纸**起；加**一个 sun bloom**（可选 ember 对位）——氛围即景深。
- 全部文字 **ink**；**Instrument Serif 400**（紧凑、负字距）展示，**Archivo** 正文，**JetBrains Mono** 一切数字/日期。
- 分隔一律 **1px ink 发丝线**（密集行 soft）；**yellow panel** 灌满海报时刻（ink 在上）。
- micro-label **大写 Archivo 600，0.16–0.32em**；**pagenum** 钉在右下。
- 偏稀疏；封面/章节/列表左/不对称，宣言居中。

### 禁止（Don't）

- 无投影、无圆角、无边框卡片、无粗于 1px 的边框。
- 无第二文字色；无粗 Instrument Serif；无反色 ink 底。
- 正文/展示不用 mono；不替换字体。
- 勿挤满画布——稀疏即优雅；勿省略 bloom（ flat parchment 像 CMS 模板）。
- 勿让标题顶满边——降一档 ramp。

## 宽高比行为（Aspect-Ratio Behavior）

| 处理            | 16:9                                           | 9:16                       | 1:1                        |
| --------------- | ---------------------------------------------- | -------------------------- | -------------------------- |
| 封面            | display 左，date-rail 右上，footer 底          | display 顶，footer 堆叠    | display 上，footer 底      |
| 章节分隔        | jumbo 数字，rail 左                            | 数字居中，rail 顶          | 数字居中                   |
| 台账            | 四列行                                         | 去掉场地列 → 三列          | 三列                       |
| 宣言            | 居中 italic                                    | 居中、更高                 | 居中                       |
| 海报面板        | 侧 panel + paper                               | 顶/底 panel 条             | panel 三分之一             |
| 脉络列表        | 编号行                                         | 行（更紧）                 | 行                         |

`pad-edge` 沿短边保持；display clamp 用较短轴，竖屏不撑爆标题。承重行保持 ≥ 1.4cqw。9:16 下 ledger/strand 固定首列可收紧。

## 已批准实体（Approved Entities）

源文件未定义真实客户、标识或供应商——此类标记一律占位渲染。 programme 标题、场地、日期为内容；系统提供 paper、ink、yellow。

## 数字与陈述（硬规则）

帧尺度绝不编造数字、日期、时长或计数。槽位渲染为 `— figure —`、`{metric}`、`NN JUN`、`N m`。台账日期/时长与图表数值尤其用占位，直至脚本提供。章节序数（01、02…）为装饰性。

## 渲染前自检（Pre-Render Self-Audit）

- **眯眼**——一处 serif 展示时刻占主导；bloom 牵引视线。
- **留白**——稀疏帧 55–60% 开放；仅 ledger 密集（靠重复而非 richness）。
- **一色**——ink 全部文字 + 线；sun 用于 bloom/panel/tile；ember 仅对位 bloom；无反色。
- **字体**——Instrument Serif 400 紧凑负字距、按度量适配；micro-label 大写 0.16em+；mono 数字；≥1.4cqw 下限。
- **景深**——0 阴影、0 圆角、仅 1px 发丝线；存在 sun bloom。
- **锚点**——封面/章节/列表左对齐，宣言居中；pagenum 右下。
- **编造**——每个数字/日期可追溯到脚本，否则占位。

## 已知缺口（Known Gaps）

- **动效刻意不在范围。** frame.md 仅规定构图；源中 280ms crossfade 为 deck 机制。
- **Instrument Serif + Archivo + JetBrains Mono 经 Google Fonts。** CJK：Smiley Sans（展示）/ Noto Serif SC（正文）/ Noto Sans SC（标签）；italic serif 与 mono 等宽数字无完全等价汉字——台账日期保持 Latin。
- **9:16 / 1:1 为指导**；`min(vw,vh)` clamp 防止 display 撑爆——按比例验证。
- Sun/ember bloom、block tile、yellow panel、发丝线为纯 CSS；无需外部图像。
