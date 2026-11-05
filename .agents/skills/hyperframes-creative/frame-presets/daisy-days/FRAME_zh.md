---
version: alpha
name: Daisy Days — Frame (video / frame layer)
description: >
  与 Daisy Days 的 design.md 配套的、以视频为先的文档。基本单位是帧（1920×1080）。原子级样式恒定且不可违背——阳光花园 Pastel 色板（奶油色 + 青绿/柔粉/黄油/薄荷/薰衣草/蜜桃/天空 + 珊瑚点缀）、炭灰 3px 描边、硬偏移阴影（6/4px、无模糊）、Fredoka + Quicksand 字体组合、大圆角、彩色底上的标题文字阴影、圆点项目符号，以及手绘 SVG 装饰层。构图与帧尺度已重写。动效不在本文范围。
unit: 帧 — 主尺寸 1920×1080；并文档化 9:16 与 1:1
principle: 原子神圣 · 构图自由 · 数值来自脚本

colors:
  cream: "#F5F0E6"
  turquoise: "#7ECDC0"
  soft-pink: "#F7C8D4"
  butter: "#FDE68A"
  mint: "#A8E6CF"
  lavender: "#D4A5E8"
  peach: "#FFCBA4"
  sky: "#A8D8F0"
  coral: "#F8635F"
  text-dark: "#2D2D2D"
  text-muted: "#6B6B6B"
  white: "#FFFFFF"

borders: { primary: "3px solid text-dark", thin: "2px solid text-dark" }
shadows: { default: "6px 6px 0 text-dark", small: "4px 4px 0 text-dark", text-headline: "3px 3px 0 text-dark", text-headline-soft: "3px 3px 0 rgba(0,0,0,0.2)" }

typography:
  # — 阅读阶梯（Quicksand）—
  body:    { fontFamily: "Quicksand", cqw: 0.95, weight: 500, lineHeight: 1.6 }
  body-strong:{ fontFamily: "Quicksand", cqw: 0.95, weight: 600, lineHeight: 1.5 }
  meta:    { fontFamily: "Quicksand", cqw: 0.78, weight: 600, lineHeight: 1.45 }
  # — 展示阶梯（Fredoka One / Fredoka 600 — 单一字重，禁止斜体）—
  badge:   { fontFamily: "Fredoka One", cqw: 0.9, tracking: "0.02em" }
  label-display:{ fontFamily: "Fredoka One", cqw: 1.3, lineHeight: 1.3, tracking: "0.02em" }
  subtitle:{ fontFamily: "Fredoka One", cqw: 1.8, lineHeight: 1.2, tracking: "0.02em" }
  quote:   { fontFamily: "Fredoka One", cqw: 2.6, lineHeight: 1.35 }
  title:   { fontFamily: "Fredoka One", cqw: 3.0, lineHeight: 1.15, tracking: "0.02em" }
  headline:{ fontFamily: "Fredoka One", cqw: 4.5, lineHeight: 1.1, tracking: "0.02em" }
  display: { fontFamily: "Fredoka One", cqw: 6.5, lineHeight: 1.1, tracking: "0.02em" }

spacing:
  pad-slide: "3cqw"
  radius: "20px"
  radius-lg: "28px"
  radius-pill: "50px"
  radius-round: "50%"

components:
  card:
    backgroundColor: "{colors.white}"
    border: "3px solid {colors.text-dark}"
    rounded: "{spacing.radius} (28px featured)"
    shadow: "6px 6px 0 {colors.text-dark}"
    description: "通用容器；白底叠 Pastel 面是标准做法。"
  framed-header:
    backgroundColor: "pastel cap + {colors.white} body"
    border: "3px solid {colors.text-dark} (one continuous)"
    rounded: "{spacing.radius-lg}"
    shadow: "6px 6px 0 {colors.text-dark}"
    description: "Pastel 顶条与白色主体上下衔接——一个单元、一道阴影。"
  badge-pill:
    backgroundColor: "{colors.butter}"
    border: "3px solid {colors.text-dark}"
    rounded: "{spacing.radius-pill}"
    typography: "{typography.badge}"
    shadow: "4px 4px 0 {colors.text-dark}"
    description: "区块标签。white-space:nowrap。"
  circle-marker:
    backgroundColor: "any pastel"
    textColor: "{colors.white} (dark on butter)"
    border: "3px solid {colors.text-dark}"
    rounded: "50%"
    size: "bullet 20 / icon 44 / dot 48 / step 90"
    typography: "Fredoka numeral"
    description: "步骤圆带小阴影。"
  bullet-dot:
    backgroundColor: "{colors.butter}"
    border: "2px solid {colors.text-dark}"
    rounded: "50%"
    size: "20px (::before, 4px from line top)"
    description: "列表禁止使用字形项目符号。"
  ornament:
    type: "hand-drawn SVG (daisy, star, sun, cloud, rainbow)"
    stroke: "2.1px {colors.text-dark}"
    placement: "z-index:1 behind content (z-index:2), cropping past the frame edge"
    description: "每帧 3–7 个，聚在角/边。"
  quote-mark:
    typography: "oversized Fredoka quote glyph"
    color: "{colors.soft-pink} (charcoal stroke)"
    description: "位于引用正文上方。"
  text-headline-shadow:
    shadow: "3px 3px 0 {colors.text-dark} (soft 20% variant on pink/mint)"
    appliesTo: "Fredoka headlines on saturated surfaces (cream headlines sit flat)"
    description: "让标题像形状一样读出「描边」感。"
---

# Daisy Days — Frame（视频 / 帧层）

## 概述

Daisy Days 在帧尺度上是一套**明快、童稚的视觉系统**——绘本插画遇上贴纸风 kawaii。每个形状都有**3px 炭灰描边**，每个抬升元素都有**实心硬偏移阴影**（无模糊），每个面都是阳光花园 Pastel。字体只有一对：**Fredoka One**（粗圆、单一字重）负责所有标题，**Quicksand** 负责正文与元信息。标志特征是**手绘 SVG 装饰层**——雏菊、星星、太阳、云、彩虹聚在角落并裁切超出画框。

色板是**多 Pastel + 一处暖色点缀**：奶油画布、七种 Pastel 面，以及 `{colors.coral}` 仅用于小面积高注意力标记。饱和面上的 Fredoka 标题加 3px 炭灰文字阴影（与形状一样读出「描边」）并改为白字；奶油面上的标题为扁平炭灰。纵深是 2D 图形语言——粗描边 + 硬偏移 = 贴纸贴在纸上。

**帧尺度关键特征：**

- **奶油默认 + 轮换 Pastel 面**；`{colors.coral}` 是标记点缀，不作面。
- **Fredoka One** 标题 + **Quicksand 500/600** 正文——按角色严格分工，不可混用。
- **3px 炭灰描边 + 硬偏移阴影**（6/4px，零模糊）于每个抬升形状。
- **大圆角**——卡片 20px、特色 28px、药丸徽章、全圆标记；无直角。
- **饱和面上的标题文字阴影**（白字）；奶油面上扁平炭灰。
- **圆点项目符号**（描边黄油圆盘，不用字形）+ 每帧 **3–7 个装饰花环**。

## 帧（The Frame）

### 帧工艺条（Frame Craft Bar）

在任何结构检查之前，每帧须通过三项肉眼测试：

- **眯眼（Squint）**——一条 Fredoka 标题或内容卡片在视觉上占邻元素的 3–6 倍。
- **留白（Silence）**——**每帧一个内容容器**，外围装饰花环；**信息卡片网格是唯一允许密集的例外**。空角读成「坏了」。
- **克制（Restraint）**——奶油或**一种** Pastel 面；珊瑚仅小标记点缀（不作面）；仅炭灰描边 + 硬偏移阴影；禁止第九色。
- **参照（Reference）**——对标**儿童绘本 / 贴纸风 kawaii 小志**；失败样像**扁平、直角、模糊阴影的企业幻灯片**。

- **主比例：** 1920×1080（16:9）。展示尺寸用 **`cqw`** 编写（`px ÷ 1920 × 100 = cqw`）。
- **竖屏：** 1080×1920（9:16）。**方图：** 1080×1080（1:1）。
- **安全区：** `pad-slide` 约 3cqw；装饰刻意 bleed 出画框。

**容器法则（承重）。** 每帧底图设置 `container-type: size`；所有帧相对单位均为相对它的 `cqw`/`cqh`——不用 `vw`。描边保持 3px/2px；圆角保持 20/28/50px；阴影偏移用 `cqw` 缩放，贴纸偏移按比例保持。

## 颜色

令牌与源文件一致。默认底 `{colors.cream}`；轮换饱和 Pastel（turquoise / soft-pink / butter / mint / lavender / peach / sky）营造色调。 **卡片在任何面上均为白底**。 **描边与阴影永远是 `{colors.text-dark}` 炭灰**——不用彩色、不模糊、不用 `rgba`（软文字阴影变体除外）。`{colors.coral}` 是唯一高饱和点缀——小标记（步骤圆、圆点、顶条）**仅**此用途，不作面。正文为炭灰/弱化色；Pastel 无**语义**含义。禁止第九色。

## 字体

两条阶梯。**阅读阶梯**（Quicksand 500 正文 0.95cqw、600 强调、meta）承载文案；**展示阶梯**（Fredoka One `label-display` 1.3cqw → `display` 6.5cqw，单一字重）承载标题、题名、引用与标记数字。

- **可读下限：** 任何承载信息的行 ≥ **1.4cqw**；meta 仅为装饰性 chrome。
- **按量适配：** 标题字号随长度调整。整块 ≤ **78cqw**；≤3 词 → `display`；4–6 → `headline`；7+ → `title`。
- **Fredoka One 管全部展示，Quicksand 管全部正文——不可交叉。** Fredoka 单一字重（无斜体、无下划线、无其他字重）；Quicksand 保持 500/600/700。Fredoka 字距 0.02em；Quicksand 正文不全大写。

## 纵深与表面

2D 图形纵深——硬偏移阴影、实心炭灰、零模糊、右下方向：

- **`shadows.default` 6px** 卡片、框、徽章、图表容器。
- **`shadows.small` 4px** 小卡片、步骤圆、头像。
- **标题文字阴影**——饱和面上 Fredoka 标题 3px 炭灰（粉/ mint 上 20% 软变体）；奶油标题扁平。
- **描边 + 偏移** 共同构成贴纸-on-纸 签名。

**上限：** 无模糊阴影、无 `rgba`（软文字阴影除外）、无渐变、无光晕；元素要么投硬炭灰偏移，要么无阴影。

## 形状

- **20px** 卡片、**28px** 特色、**50px** 药丸（徽章、计数器）、**50%** 全部圆形、**4px** 图例色块。零直角——每个区域都圆角。

## 组件

- **card / framed-header**——白底描边容器（一道阴影）。**badge-pill**——黄油区块标签。
- **circle-marker** 系列（bullet 20 / icon 44 / dot 48 / step 90）+ **bullet-dot**——描边 Pastel 圆盘，Fredoka 数字。
- **ornament**——手绘 SVG 贴纸层（每帧 3–7）。**quote-mark**——柔粉 Fredoka 锚点。**text-headline-shadow**——彩色底标题处理。

## 帧处理（Frame Treatments）

> 配方：底 · 容器 · 组合 · 焦点 · chrome · 点缀 · 留白 · 固定/自由 · 密度。
> 每帧一个内容容器 + 3–7 装饰花环；空角读成「坏了」。

### 1 · 封面（身份 · 手法：装饰花环 · 饱和 · 居中）

**底** 饱和 Pastel（如 `{colors.turquoise}`）。**组合** badge-pill、display、正文副标题、3–7 装饰、计数器。**焦点** 1–2 行 Fredoka `display`，**白字 + 3px 炭灰文字阴影**，居中，位于 butter badge-pill 下。**Chrome** 计数药丸。**点缀** 装饰花环（角上雏菊 + 星，裁切出边）。**留白** 内容居中；装饰填边。**固定** 彩色底文字阴影、3px 描边、炭灰阴影。**自由** 面色、装饰组合/位置、文案。**密度** 满但不挤。

### 2 · 信息卡片（目录 · 手法：三列白卡片 · 奶油 · 唯一密集帧）

**底** `{colors.cream}`，`pad-slide`。**组合** 标题（扁平炭灰）、3× card（圆图标 + Fredoka 标题 + Quicksand 正文）、少量装饰。**焦点** 三张白底 3px 描边、6px 阴影卡片。**Chrome** 扁平标题。**点缀** Pastel 圆图标（轮换 turquoise/coral/lavender）。**留白** 紧——密度例外（此处装饰更少）。**固定** 白卡片、3px + 6px、20px 圆角。**自由** 卡片内容、图标色相。**密度** 密集例外。

### 3 · 流程步骤（序列 · 手法：轮换圆标记 · 蜜桃 · 居中）

**底** `{colors.peach}`（或其他 Pastel）。**组合** 标题（白 + 文字阴影）、3–4 步骤圆 + `→` 箭头、装饰。**焦点** 一行 90px 描边步骤圆，填充**轮换 coral → mint → sky → lavender**，Fredoka 白数字，Fredoka 箭头串联。**Chrome** 白标题 + 文字阴影。**点缀** 轮换圆填充色。**留白** 中等。**固定** 3px 圆 + 小阴影、轮换填充、箭头字形。**自由** 步骤数、标签。**密度** 标准。

### 4 · 引用（quote · 手法：quote-mark 锚点 · 柔粉 · 居中）

**底** `{colors.soft-pink}`。**组合** 白引用卡（28px 圆角、6px 阴影）、quote-mark、Fredoka 引用、Quicksand 署名、装饰。**焦点** 白卡内炭灰 Fredoka `quote`， oversized 柔粉 quote-mark 上方。**Chrome** Quicksand 700 署名。**点缀** quote-mark + 一两颗星。**留白** 卡片居中，装饰在角。**固定** quote-mark 锚点、白卡。**自由** 引用、署名。**密度** 中等。

### 5 · 框式区块（feature · 手法：顶条+主体卡 · 奶油）

**底** `{colors.cream}`。**组合** framed-header（Pastel 顶 + 白主体）、bullet-dot 列表、装饰。**焦点** framed-header——Pastel 顶条（Fredoka 标题，可选文字阴影）+ 白主体 butter 圆点列表。**点缀** 顶条色 + 圆点。**留白** 中等。**固定** 连续 3px 描边 + 一道阴影、butter 圆点。**自由** 顶条色、列表。**密度** 标准。

### 6 · 收尾（closer · 手法：装饰花环 · 饱和 · 居中）

**底** 饱和 Pastel（如 `{colors.lavender}`）。**组合** badge-pill、display（白 + 文字阴影）、3–7 装饰。**焦点** 居中 Fredoka `display` 结语，白字 + 炭灰文字阴影。**点缀** 装饰花环。**留白** 内容居中。**固定** 彩色底文字阴影、装饰填角。**自由** 结语、面、装饰。**密度** 满。

## 构图规则

### 应当

- **Fredoka One 标题 + Quicksand 正文** 严格按角色配对。
- 每个形状 **3px 炭灰描边 + 硬偏移阴影**（6/4px、无模糊）；任何面上白卡片填充。
- 饱和面上 Fredoka 标题 **3px 炭灰文字阴影 + 白字**；奶油上扁平炭灰。
- 使用 **描边黄油圆盘项目符号**（不用字形）；每帧聚 **3–7 手绘装饰**（角、裁切出边）。
- **每帧一个内容容器**；标记色轮换（coral → mint → sky → lavender → butter）；珊瑚仅小标记。
- 多数帧居中；内容密帧偏奶油，封面/收尾/引用偏饱和。

### 禁止

- 无直角；无模糊或 `rgba` 阴影（软文字阴影除外）。
- 无彩色描边（仅炭灰）；无珊瑚作面；无第九色。
- 无第三字体；无 Quicksand 标题或 Fredoka 正文；Fredoka 无斜体/下划线；Quicksand 正文无全大写。
- 无字形项目符号；无空角（装饰填满）；无两个竞争内容面板。
- 标题不要撑满整宽——按量适配。

## 宽高比行为

| 处理           | 16:9                           | 9:16                               | 1:1        |
| -------------- | ------------------------------ | ---------------------------------- | ---------- |
| 封面           | 居中，角上装饰                 | 居中、更高、更多装饰               | 居中       |
| 信息卡片       | 横排三列                       | 纵向堆叠                           | 2+1        |
| 流程步骤       | 横向 + 箭头                    | 纵向，箭头向下                     | 2×2        |
| 引用           | 居中卡片                       | 居中、更高                         | 居中       |
| 框式区块       | 顶条 + 主体                    | 顶条 + 更高主体                    | 顶条 + 主体 |
| 收尾           | 居中、花环                     | 居中、花环                         | 居中       |

`pad-slide` 沿短边保持；在更紧比例上重新抬升 display，仍 ≥ 1.4cqw 下限。更紧比例时装饰数量偏上限（5–7），角永不显空。

## 已批准的真实实体

源文件未定义真实客户、标识或供应商——此类标记一律占位渲染。装饰与 Pastel 与内容无关；计数器/徽章承载每 deck 文案。

## 数字与主张（硬规则）

帧尺度禁止臆造数字、日期或计数。槽位渲染为 `— figure —`、`{metric}`、`N`。步骤号与图表值在脚本提供前用占位；幻灯片计数器为装饰 chrome。

## 渲染前自检

- **眯眼**——每帧一条 Fredoka 标题或内容卡片占主导。
- **留白**——每帧一个容器 + 装饰花环；仅信息卡片网格可密集。
- **颜色**——奶油或一种 Pastel 面；仅珊瑚标记；炭灰描边/阴影；无第九色相。
- **字体**——Fredoka 标题（饱和面文字阴影 + 白，奶油扁平炭灰），Quicksand 正文；≥1.4cqw 下限。
- **纵深**——3px 描边 + 硬偏移（无 blur，无 rgba 除软文字阴影）；仅圆角。
- **装饰**——每帧 3–7，裁切出边；无空角。**项目符号**——描边圆盘，不用字形。
- **杜撰**——每个数字可追溯到脚本，否则占位。

## 已知缺口

- **动效刻意不在范围。** frame.md 仅规定构图；源使用 scroll-snap 导航，无过渡规格。
- **字体：** 源称 _Fredoka One_；Google 现提供 **Fredoka** 可变族——请求 `Fredoka:wght@500;600;700` 并将展示字重设为 600（视觉等同 Fredoka One），栈中仍保留 `Fredoka One` 以兼容仍提供该字体的环境。Quicksand 正常加载。CJK：ZCOOL XiaoWei（展示）/ Yozai（正文）。
- **9:16 / 1:1 为指导性**；按比例保持高装饰数，角保持填满。
- 装饰（daisy/star/sun/cloud/rainbow）、标记与 framed header 仅 CSS/SVG；重着色 SVG 装饰须改 stroke 值。
- **对比度：** `{colors.text-muted}` 勿用于 Pastel 面（仅奶油/白卡片）；饱和底小字应为炭灰或白。
