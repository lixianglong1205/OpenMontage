---
version: alpha
name: Editorial Forest — Frame (video / frame layer)
description: >
  Editorial Forest 设计文档 design.md 的视频优先配套说明。基本单位为帧（1920×1080）。原子级元素
  完全一致且不可改动 —— 绿/粉/奶油色编辑三色、Source Serif 4 字重 500（光学尺寸轴）用于全部展示
  层 + JetBrains Mono 500 大写装饰字、扁平纸质景深（无阴影）、2px 细线分隔、6/8px 卡片圆角，以及
  字母组合圆形印章。构图与帧尺度重写。动效不在本文范围。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  green: "#2e4a2a"
  green-deep: "#243a21"
  green-lite: "#3a5a36"
  pink: "#e89cb1"
  pink-deep: "#d27e96"
  cream: "#efe7d4"
  cream-2: "#e6dcc4"
  ink: "#1a1a17"

typography:
  # — 正文 + 装饰字阶 —
  body:    { fontFamily: "Source Serif 4", cqw: 1.56, weight: 400, lineHeight: 1.38 }
  body-card:{ fontFamily: "Source Serif 4", cqw: 1.35, weight: 400, lineHeight: 1.34 }
  label:   { fontFamily: "JetBrains Mono", px: 26, cqw: 1.35, weight: 500, tracking: "0.18em", upper: true }
  caption-mono:{ fontFamily: "JetBrains Mono", px: 24, cqw: 1.25, weight: 500, tracking: "0.14em", upper: true }
  # — 展示字阶（Source Serif 4 字重 500，opsz，负字距）—
  title-card-sm:{ fontFamily: "Source Serif 4", cqw: 2.9, weight: 500, lineHeight: 0.98, tracking: "-0.01em" }
  title-card:{ fontFamily: "Source Serif 4", cqw: 3.5, weight: 500, lineHeight: 0.96, tracking: "-0.01em" }
  headline:{ fontFamily: "Source Serif 4", cqw: 4.4, weight: 500, lineHeight: 1.0, tracking: "-0.02em" }
  headline-xl:{ fontFamily: "Source Serif 4", cqw: 5.0, weight: 500, lineHeight: 0.96, tracking: "-0.02em" }
  display:{ fontFamily: "Source Serif 4", cqw: 7.3, weight: 500, lineHeight: 1.02, tracking: "-0.02em" }
  display-hero:{ fontFamily: "Source Serif 4", cqw: 11.5, weight: 500, lineHeight: 0.92, tracking: "-0.02em" }
  stat-figure:{ fontFamily: "Source Serif 4", cqw: 11.5, weight: 500, lineHeight: 0.92, tracking: "-0.03em" }
  stat-figure-unit:{ fontFamily: "Source Serif 4", cqw: 5.7, weight: 500, lineHeight: 0.92 }
  name:    { fontFamily: "Source Serif 4", cqw: 2.3, weight: 600, lineHeight: 1.0 }

spacing:
  slide-pad: "5cqw"
  rule: "2px"
  rule-card: "2.5px"
  radius-card: "6px"
  radius-step: "8px"

components:
  topbar:
    typography: "{typography.label} (JetBrains Mono) + monogram-circle or counter"
    placement: "top edge, label left, mark right"
    description: "每一帧必有 —— 系统的脊梁；缺少顶栏的帧会显得未完成。"
  footline:
    typography: "{typography.caption-mono} ×2, space-between"
    placement: "absolute bottom edge"
    description: "用于封面/数据/总结类帧。"
  monogram-circle:
    border: "2px solid {colors.pink}"
    rounded: "50%"
    size: "130px"
    typography: "mono monogram"
    description: "身份印章。仅封面/总结。"
  topic-tile:
    backgroundColor: "{colors.green} (pink text) / {colors.pink} (green-deep) / {colors.green-lite} (pink) / {colors.cream-2} + 2px {colors.green} border (green)"
    rounded: "{spacing.radius-card}"
    shadow: "none"
    typography: "{typography.caption-mono} ordinal + {typography.title-card-sm} + mono foot"
    description: "填充色轮换；同一网格内不可重复同一填充。"
  step-tile:
    backgroundColor: "{colors.cream} + green border / {colors.green} / {colors.pink}"
    border: "2.5px solid"
    rounded: "{spacing.radius-step}"
    typography: "mono ordinal + {typography.title-card} + {typography.body-card} + mono marker over a top rule"
    description: "框架/流程卡片。"
  kpi-block:
    typography: "{typography.caption-mono} tag → {typography.stat-figure} (+{typography.stat-figure-unit}) → {typography.body}"
    rule: "2px accent rule above"
    description: "超大衬线数字。"
  meta-dl:
    borderTop: "2px solid {colors.green}"
    typography: "{typography.caption-mono} dt + {typography.meta-value} dd"
    description: "三列 dt/dd 网格。"
  bar:
    backgroundColor: "{colors.pink} / {colors.cream} / {colors.green}"
    rounded: "3px 3px 0 0"
    size: "56px wide"
    typography: "mono value above"
    description: "竖向图表柱。"
  rule-thin:
    rule: "2px solid (green on cream / pink on green / green-deep on pink)"
    description: "唯一分隔线。禁止 1px，禁止 3px 及以上。"
---

# Editorial Forest — Frame（视频 / 帧层）

## 概述

Editorial Forest 在帧尺度上是一套 **衬线主导的文学编辑风系统** —— 气质接近企鹅经典或安静的
年报。一个自信的声音 —— **Source Serif 4 字重 500**（启用光学尺寸轴）—— 承载所有标题与统计数字，
最大约 12cqw；**JetBrains Mono** 字重 500 大写作为编辑装饰（标签、说明、坐标刻度、页脚行）。三种
表面 —— 森林绿、尘玫瑰、燕麦奶油 —— 仅此而已。景深 **扁平、纸质**：无阴影、无渐变；层次来自色块
对比 + 2px 细线 + 描边与填充的差异。

无可错认的签名是 **字重 500**（展示层不用 400，不用 700）以及 **等宽/衬线角色倒置**
（等宽做装饰，衬线做正文与展示）。正文降至衬线字重 400 —— 500→400 的落差即阅读节奏。每一帧
都有等宽顶栏；字母组合圆是身份印章。

**帧尺度关键特征：**

- **绿 / 粉 / 奶油三色** —— 单帧通常两种表面色，三种则偏喧。
- **Source Serif 4 字重 500**（opsz、负字距）用于全部展示；**衬线 400** 正文；**JetBrains Mono 500** 大写装饰。
- **扁平 —— 无阴影、无渐变**；层次来自色块 + 2px 细线 + 描边与填充。
- **2px 细线** 为唯一分隔（步骤块上 2.5px）；卡片圆角 6/8px；字母组合圆是唯一整圆。
- **每帧顶栏**（等宽标签 + 字母组合/计数）；数据/封面帧有页脚行。
- **疏朗且笃定** —— 深留白中一帧一主题；元素更少、尺寸更大。

## 帧

### 帧工艺检验栏

在任何结构检查之前，每帧须通过三项肉眼检验：

- **眯眼** —— 一处 Source Serif 4 焦点在邻元素 3–6 倍尺度上占主导；表面色块锚定视线。
- **静默** —— 深留白中一帧一主题；**主题块与步骤网格是唯一允许密集的例外**。
- **克制** —— 单帧 **最多两种表面色**（三种则喧）；衬线展示 **500** / 正文 **400**；绿色底面留给庄重时刻。
- **参照** —— 对标 **企鹅经典 / 安静年报 / 艺术书跨页**；失败则像 **带阴影、多色的 Web 仪表盘**。

- **主比例：** 1920×1080（16:9）。展示尺寸用 **`cqw`** 编写（`px ÷ 1920 × 100 = cqw`）。
- **竖版：** 1080×1920（9:16）。**方版：** 1080×1080（1:1）。
- **安全区：** `slide-pad` 5cqw（源稿中宽裕的 96–140px）；顶栏/页脚行在其内。

**容器法则（承重）。** 每帧底面设置 `container-type: size`；所有帧相对单位均为相对它的
`cqw`/`cqh` —— 禁止 `vw`（源为固定 1920 画布，px 可干净映射：`px ÷ 1920 × 100`）。细线保持 2px；
卡片圆角保持 6/8px。

## 色彩

令牌与源一致。默认底 `{colors.cream}` 用于内容；`{colors.green}` 用于封面/陈述/总结等庄重场景。
**标题：** 奶油上的绿、绿上的奶油（或英雄尺度上的粉）、粉上的 green-deep。**正文：** 奶油上的 ink、
绿上的 cream、粉上的 green-deep。标签/分隔线取区域强调色（绿上的粉、奶油上的绿、粉上的 green-deep）。
块填充轮换 green / pink / green-lite / cream-2-with-green-border。**禁止第四色系** —— 三色 +
近重复色即全部色板；表面禁止 `rgba` 透明。

## 字体

两档字阶。**阅读/装饰档**（Source Serif 4 **400** 正文 1.56cqw；JetBrains Mono 标签用 px）承载
文案与装饰；**展示档**（Source Serif 4 **500** `title-card-sm` 2.9cqw → `display-hero`/`stat-figure`
11.5cqw，opsz，负字距）承载所有标题与数字。

- **可读下限：** 任何承重行 ≥ **1.4cqw**；mono px 标签仅作装饰。
- **按字数适配：** 按标题长度定字号。块宽 **≤ 78cqw**；≤3 词 → `display-hero`；4–6 → `headline-xl`；
  7+ → `headline`。7.3–11.5cqw 档留给陈述/统计/封面。
- **衬线展示 500、正文 400**（节奏），600 仅用于署名。负字距（−0.01..−0.03em），紧行高（0.92–1.02）。
  **等宽大写，0.08–0.18em。** 无斜体、无下划线、无第三字体、正文不用 500 衬线。

## 景深与表面

扁平、纸质。层次来自：

- **色块对比** —— 奶油上的绿块因墨块分离而显得抬高。
- **2px 细线** —— 区域强调色的章节分隔。
- **描边 vs 填充** —— cream-2 块 + 2px 绿描边与纯色块的层次感不同。

**上限：** 零阴影（禁止 —— 加 `box-shadow` 会破坏纸质感），无渐变、无光晕；表面为实色纸墨。

## 形状

- **6px** 主题块，**8px** 步骤块，**2px** 图例色块，**3px 3px 0 0** 柱顶，**50%** 字母组合圆。
  无直角、无大圆角。

## 组件

- **topbar**（脊梁）+ **footline** + **monogram-circle**（身份印章）—— 装饰套件。
- **topic-tile**（6px，填充轮换）/ **step-tile**（8px，2.5px 描边）—— 目录与框架模式。
- **kpi-block**（超大衬线数字）/ **meta-dl**（三列，2px 线）/ **bar** / **rule-thin** —— 数据与结构。

## 帧处理

> 配方：底面 · 容器 · 组成 · 焦点 · 装饰 · 强调 · 留白 · 固定/自由 · 密度。
> 每帧顶栏；深留白中一帧一主题。

### 1 · 封面（身份 · 动作：超大衬线 · 绿 · 左）

**底面** `{colors.green}`，`slide-pad`。**组成** 顶栏（等宽标签 + monogram-circle）、display-hero、
正文导语、页脚行。**焦点** 两行 Source Serif 4 `display-hero` 粉色（一词 cream），左对齐。**装饰**
等宽顶栏；等宽页脚行。**强调** 粉色展示 + 字母组合圆。**留白** ~50%。**固定** 衬线 500、扁平、
monogram 2px 粉。**自由** 标题、哪一词为 cream。**密度** 低。

### 2 · 主题块（目录 · 动作：填充轮换网格 · 奶油 · 密集帧）

**底面** `{colors.cream}`，`slide-pad`。**组成** 顶栏、headline-xl、3–4× topic-tile。**焦点** 一行
6px 块，填充轮换 green / pink / cream-2-with-border，各为等宽序号 + 衬线标题。**装饰** 等宽顶栏。
**强调** 块填充（四取三混用，不重复）。**留白** 紧 —— 密度例外。**固定** 6px 圆角、填充轮换、无阴影。
**自由** 块标题、哪些填充。**密度** 密集例外。

### 3 · KPI 统计（数据 · 动作：超大数字 · 绿）

**底面** `{colors.green}`，`slide-pad`。**组成** 顶栏、kpi-block（等宽 tag + 220px stat-figure + 衬线说明）、
页脚行。**焦点** Source Serif 4 `stat-figure`（~11.5cqw，+单位）粉色，上覆 2px 粉线。**装饰** 等宽顶栏 +
页脚行。**强调** 粉色数字。**留白** ~55%。**固定** 衬线 500 数字、2px 强调线、扁平。**自由** 数字（来自脚本）、
tag、说明。**密度** 低。

### 4 · 陈述（引语 · 动作：展示衬线 · 奶油 · 左）

**底面** `{colors.cream}`，宽裕内边距。**组成** 顶栏、display、name（600）、caption-mono 角色。
**焦点** 两行 Source Serif 4 `display`（~7.3cqw）绿色；其下 600 署名 + 等宽角色。**装饰** 等宽顶栏。
**强调** 无 —— 衬线自身承载。**留白** ~55%。**固定** 衬线 500 展示 + 600 署名，无斜体。**自由** 引文、
署名、角色。**密度** 低。

### 5 · 步骤框架（流程 · 动作：8px 步骤块 · 奶油/绿）

**底面** `{colors.cream}`（或 green），`slide-pad`。**组成** 顶栏、headline、3–4× step-tile。**焦点** 一行
8px 步骤块（2.5px 描边）—— 等宽序号 + 衬线 68px 标题 + 正文 + 顶线上的等宽标记；填充轮换
cream-with-green-border / green / pink。**强调** 块填充。**留白** 适中。**固定** 8px 圆角、2.5px 描边、
等宽标记。**自由** 步骤、填充。**密度** 标准。

### 6 · 图表（数据 · 动作：柱 + meta · 绿）

**底面** `{colors.green}`，`slide-pad`。**组成** 顶栏、headline、柱 + 2px 轴线、meta-dl。**焦点** 56px
粉/奶油/绿柱于内缘 2px 轴线上，等宽刻度；可选下方三列 meta-dl。**装饰** 等宽顶栏。**强调** 柱填充。
**留白** 适中。**固定** 56px 柱、3px 顶、2px 轴、等宽刻度。**自由** 数值（来自脚本）、标签。**密度** 标准。

## 构图规则

### 应当

- 所有展示用 **Source Serif 4 字重 500**，opsz，负字距，紧行高；**正文 400**。
- 所有标签/说明/轴/页脚行用 **JetBrains Mono 500 大写，0.08–0.18em**。
- 每帧 **顶栏**（等宽标签 + 字母组合或计数）；数据/封面有页脚行。
- 每帧 **一种主导表面**（最多两色）；**块填充轮换**，网格内不重复。
- 用区域强调色 **2px 细线** 分节；字母组合圆仅封面/总结。
- 陈述/统计/封面大幅放大展示（7.3–11.5cqw）；偏左编辑风，一帧一主题。

### 禁止

- 无 box-shadow、渐变或光晕 —— 仅扁平纸质景深。
- 无第三字体；无斜体/下划线；正文不用 500 衬线；展示尺度不用等宽。
- 无第四色系；表面无 `rgba`；分隔线非 1px 或 4px+（仅 2px / 2.5px）。
- 无两个竞争内容块；不可省略顶栏。
- 标题勿铺满边缘 —— 按字阶下调。

## 宽高比行为

| 处理           | 16:9                             | 9:16                        | 1:1                      |
| -------------- | -------------------------------- | --------------------------- | ------------------------ |
| 封面           | 展示居左，字母组合右上           | 展示居上，字母组合下方      | 展示，字母组合角位       |
| 主题块         | 3–4 横排                         | 纵向堆叠                    | 2×2                      |
| KPI 统计       | 数字居左                         | 数字居中、更高              | 居中                     |
| 陈述           | 引文居左                         | 引文堆叠                    | 居中                     |
| 步骤框架       | 3–4 横排                         | 纵向堆叠                    | 2×2                      |
| 图表           | 柱 + meta                        | 柱更高，meta 堆叠           | 方图                     |

`slide-pad` 在短边保持；在 1.4cqw 下限之上重新定展示档。各比例顶栏均跨顶；字母组合可降至角位。

## 已批准的真实实体

源中未定义真实客户、标识或供应商 —— 此类标记一律用占位渲染。字母组合、页脚字符串与块计数承载
每套 deck 身份；数字为内容。

## 数字与主张（硬规则）

帧尺度禁止臆造数字、KPI、日期或计数。槽位渲染为 `— figure —`、`{metric}`、`— %`。KPI 块、柱与
meta 值尤其须占位，直至脚本提供。期号/计数为装饰性 chrome。

## 渲染前自检

- **眯眼** —— 一处衬线焦点占主导；表面块锚定视线。
- **静默** —— 深留白一帧一主题；仅主题块/步骤网格可密集。
- **三色** —— 最多两表面色；标题/正文/标签用对表面色；无第四色系。
- **字体** —— Source Serif 4 **500** 展示（opsz，负字距）/ **400** 正文；等宽大写 0.08–0.18em；≥1.4cqw 下限。
- **景深** —— 0 阴影、0 渐变；2px 细线；6/8px 圆角；字母组合为唯一整圆。
- **装饰** —— 每帧有顶栏；数据/封面有页脚行。
- **捏造** —— 每个数字可追溯到脚本，否则占位。

## 已知缺口

- **动效有意不在范围。** frame.md 仅规定构图；源依赖 `deck-stage.js` 做缩放/导航，无过渡规范。
- **Source Serif 4（opsz 8..60）+ JetBrains Mono 经 Google Fonts** —— 光学尺寸轴关键；无 opsz 回退会
  压平随尺寸变化的字形。CJK：LXGW WenKai（展示）/ Noto Serif SC（正文）/ Noto Sans Mono CJK（装饰）。
- **9:16 / 1:1 为指导**；须验证下限及各比例下两色纪律。
- 柱、细线、块与字母组合圆纯 CSS；无需外部图。
- **对比度：** 绿上粉 / 粉上绿仅用于展示尺度（84px+）；小字保持 cream-on-green 或 ink-on-cream。
