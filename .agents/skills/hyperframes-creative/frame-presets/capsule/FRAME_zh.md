---
version: alpha
name: Capsule — Frame (video / frame layer)
description: >
  Capsule design.md 以视频为先的配套文档。基本单元为帧（1920×1080）。原子元素一致且不可违背 ——
  药丸几何（小元素 9999px / 卡片 2rem），一切皆有 2px 墨线描边，日晒褪色的奶油画布，九色糖果调色板，
  Bodoni Moda + Space Grotesk，柔和硬偏移阴影（8% 墨色下 4/6/8/12px），漂浮装饰药丸壁纸、
  径向强调光晕与颗粒叠加层。构图与帧尺度重写。动效不在范围内。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  cream: "#F5F5F0"
  ink: "#1A1A1A"
  outline: "#1E1E1E"
  white: "#FFFFFF"
  coral: "#E85D4E"
  lime: "#C4D94E"
  lavender: "#C5B5E0"
  sky: "#8BB4F7"
  violet: "#A06CE8"
  yellow: "#F2D160"
  peach: "#F5B895"
  mint: "#A8E6CF"
  shadow: "rgba(26,26,26,0.08)"

typography:
  # — reading ramp (Space Grotesk) —
  body:      { fontFamily: "Space Grotesk", cqw: 0.85, weight: 400, lineHeight: 1.6 }
  subtitle:  { fontFamily: "Space Grotesk", cqw: 0.95, weight: 400, tracking: "0.18em", upper: true }
  pill-text: { fontFamily: "Space Grotesk", cqw: 0.75, weight: 600, tracking: "0.12em", upper: true }
  label:     { fontFamily: "Space Grotesk", px: 14, weight: 500, tracking: "0.1em", upper: true }
  # — display / hero ramp (Bodoni Moda, ink, sentence case) —
  card-headline:{ fontFamily: "Bodoni Moda", cqw: 1.9, weight: 700, lineHeight: 1.1 }
  orbit-numeral:{ fontFamily: "Bodoni Moda", cqw: 2.6, weight: 700, lineHeight: 1.0 }
  quote-display:{ fontFamily: "Bodoni Moda", cqw: 4.2, weight: 600, lineHeight: 1.3, tracking: "-0.01em" }
  stat-number: { fontFamily: "Bodoni Moda", cqw: 3.6, weight: 800, lineHeight: 1.0, tracking: "-0.03em" }
  section-headline:{ fontFamily: "Bodoni Moda", cqw: 4.0, weight: 700, lineHeight: 1.05, tracking: "-0.01em" }
  headline:    { fontFamily: "Bodoni Moda", cqw: 5.0, weight: 700, lineHeight: 1.05, tracking: "-0.02em" }
  closing-display:{ fontFamily: "Bodoni Moda", cqw: 8.5, weight: 800, lineHeight: 0.95, tracking: "-0.03em" }
  display:     { fontFamily: "Bodoni Moda", cqw: 12.0, weight: 800, lineHeight: 0.88, tracking: "-0.03em" }

spacing:
  pad: "5cqw"
  gap-md: "2cqw"
  card-pad: "2cqw 1.6cqw"

components:
  pill:
    rounded: "9999px (small) / 2rem (cards)"
    border: "0.2cqw solid {colors.outline}"
    backgroundColor: "any candy or {colors.white}"
    description: "通用容器 —— 每个芯片/按钮/标签/统计块/节点/条带。不存在无描边的药丸。"
  pill-card:
    backgroundColor: "{colors.white}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "2rem"
    shadow: "0.4cqw 0.4cqw 0 {colors.shadow}"
    typography: "{typography.card-headline} + {typography.body}"
    description: "内含圆形 card-icon、Bodoni 标题与 Space Grotesk 正文。"
  stat-pill:
    backgroundColor: "{colors.white}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "2rem"
    shadow: "0.3cqw 0.3cqw 0 {colors.shadow}"
    typography: "{typography.stat-number} (COLORED) + {typography.pill-text}"
    description: "数字着色的唯一位置；另加 40px 强调条。"
  title-pill:
    backgroundColor: "{colors.yellow}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px"
    shadow: "0.3cqw 0.3cqw 0 {colors.shadow}"
    typography: "{typography.pill-text}"
    description: "置于封面/收尾的 display 标题之上。"
  card-icon:
    backgroundColor: "any candy"
    border: "0.2cqw solid {colors.outline}"
    rounded: "50%"
    size: "60px"
    typography: "Bodoni numeral/letter in {colors.ink}"
    description: "卡片标记。"
  floating-pill:
    backgroundColor: "any candy"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px / 50%"
    transform: "rotate(−20°..+25°)"
    shadow: "none"
    typography: "{typography.pill-text}"
    description: "装饰性壁纸彩纸，陈述型帧每帧 5–8 个。扁平 —— 无阴影。"
  quote-highlight:
    backgroundColor: "{colors.lime} / {colors.sky}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px"
    description: "Bodoni 引语内短语外包的 inline 糖果药丸 —— 强调机制，取代粗体/斜体。"
  bar-track:
    backgroundColor: "{colors.cream}"
    border: "0.2cqw solid {colors.outline}"
    rounded: "9999px"
    fill: "child candy pill, value at right edge"
    description: "36px 药丸形图表轨道。"
  accent-line:
    backgroundColor: "{colors.coral}"
    rounded: "9999px"
    size: "60×4 (80×4 closing)"
    description: "珊瑚色药丸分隔线。"
  atmosphere:
    background: "1–3 radial candy glows (6–15% opacity) over {colors.cream} + 4% grain overlay"
    description: "每帧基线画布层。不可缺失。"
---

# Capsule — Frame（视频 / 帧层）

## 概述

Capsule 在帧尺度上是一套**玩味十足的编辑体系：每个容器都是药丸。** `border-radius: 9999px`（小元素）/ `2rem`（卡片）规则，加上 2px 墨线描边，包裹每个芯片、卡片、图标、条带与节点 —— 膨胀、友好、图形感鲜明。画布是日晒褪色的奶油色，由柔和的径向糖果光晕与常驻 4% 颗粒叠加层加温。

视觉语气是双面协作：**Bodoni Moda**（Didone 衬线，字重 700–800，始终墨色、始终句首大写/sentence case）承载所有标题、统计与引语；**Space Grotesk** 承载正文与全部大写、加字距的药丸/标签文字。九种糖果强调色可互换填充药丸，**无语义映射**。深度仅来自**柔和硬偏移阴影**（8% 墨色下 4/6/8/12px）—— 抬起而非压印 —— 仅用于承载内容的容器；装饰性漂浮药丸保持扁平。

**帧尺度关键特征：**

- **处处药丸几何** —— 小元素 9999px、卡片 2rem —— 皆包 2px `{colors.outline}` 描边。
- **Bodoni Moda** 展示（墨色、sentence case）+ **Space Grotesk** 正文/药丸（大写、加字距）。
- **九色糖果强调**，可互换；颜色用于统计数字与药丸填充，**从不用于标题**。
- **柔和偏移阴影**（4/6/8/12px，8% 墨）仅内容容器；漂浮药丸扁平。
- **漂浮装饰药丸壁纸**（5–8 个、倾斜）+ 径向光晕 + 陈述型帧 4% 颗粒。
- **奶油画布** 由氛围加温 —— 裸角会显得残缺。

## 帧（The Frame）

### 帧工艺条（Frame Craft Bar）

在任何结构检查之前，每帧须通过三项肉眼测试：

- **眯眼（Squint）** —— 一条 Bodoni 标题或统计在视觉上须为**最近邻的 3–6 倍**。
- **留白（Silence）** —— 陈述型帧承载**氛围而非 clutter**（药丸作壁纸而非内容）；**支柱卡片与统计网格是密集例外**。
- **克制（Restraint）** —— 每个药丸带 2px 描边；颜色仅触**填充 + 统计数字**（从不触标题）；柔和阴影仅内容药丸（漂浮药丸扁平）；无第十种强调色。
- **参照（Reference）** —— 对标 **Memphis / 冰淇淋店编辑 spread**；失败态像**无贴纸的扁平 SaaS 卡片网格**。

- **主比例：** 1920×1080（16:9）。Display 以 **`cqw`** 编写（`px ÷ 1920 × 100 = cqw`）。
- **竖版：** 1080×1920（9:16）。**方图：** 1080×1080（1:1）。
- **安全区：** `pad`（5cqw）；漂浮药丸可越边作壁纸。

**容器法则（承重）。** 每帧地面须设 `container-type: size` **且** 携带径向光晕 + 颗粒氛围；**所有**帧相对单位均为相对它的 `cqw`/`cqh` —— **禁止** `vw`。药丸圆角保持 `9999px`/`2rem`（形状非缩放）；阴影偏移以 `cqw` 缩放。

## 颜色

令牌与源文件一致。`{colors.cream}` 为地面；`{colors.ink}`/`{colors.outline}` 为字型与 universal 2px 描边；九种糖果强调填充药丸，**无语义映射** —— 暖色（coral/yellow/peach）+ 冷色（sky/lavender/violet/mint）+ 中性亮（lime）搭配；禁止同族相邻。颜色仅出现在**统计数字与药丸填充** —— **从不**出现在 Bodoni 标题。阴影恒为 `{colors.shadow}`（8% 墨）。无第十色。

## 排版

双 ramp。**阅读 ramp**（Space Grotesk 正文 0.85cqw、大写加字距药丸/标签）承载文案与芯片；**展示 ramp**（Bodoni `card-headline` 1.9cqw → `display` 12cqw，均 700–800）承载所有标题、统计与引语。

- **可读下限：** 任何承载内容的行 ≥ **1.4cqw**；px 标签仅为 chrome。
- **按量适配：** 按标题长度定字号。块宽上限 **≤ 78cqw**；≤3 词 → `display`/`closing-display`；4–6 → `headline`；7+ → `section-headline`。
- **Bodoni 700+ 墨色、sentence case**（斜体仅 `<em>`，斜体关键词可用糖果色）；**Space Grotesk 药丸/标签大写、≥0.08em 字距**；Bodoni 展示负字距。

## 深度与表面

柔和硬偏移阴影是唯一深度，使用 `{colors.shadow}`（8% 墨），右下：

- **0.2cqw（4px）** 小节点；**0.3cqw（6px）** stat-pill、orbit pill、diagram 节点；**0.4cqw（8px）** pillar-card；**0.6cqw（12px）** 视觉框。
- **2px 描边** 在奶油上承担大部分「抬起」；阴影增加漂浮感。
- **装饰漂浮药丸无阴影** —— 一眼区分内容与氛围。

**上限：** 无模糊阴影、无改色阴影、无渐变深度。

## 形状

- **9999px** —— 所有小药丸（芯片、按钮、条、节点、漂浮药丸、引语高亮、accent line）。
- **2rem** —— 较大卡片（pillar-card、stat-pill、图表容器、视觉框）。
- **50%** —— 圆形药丸（card-icon 60px、step-node 56px、orbit-center 160px、导航点）。
- **0** —— 仅颗粒叠加与视觉框内渐变区域。**不存在**尖角文本容器。

## 组件

- **pill** —— universal 2px 描边容器。**pill-card / stat-pill / title-pill** —— 带柔和阴影的白/黄内容药丸。
- **card-icon** —— 圆形糖果标记；**floating-pill** —— 扁平倾斜壁纸彩纸；**quote-highlight** —— inline 糖果强调药丸。
- **bar-track** —— 药丸形图表条；**accent-line** —— 珊瑚药丸规则线；**atmosphere** —— 每帧基线光晕 + 颗粒。

## 帧处理（Frame Treatments）

> 配方：地面 · 容器 · 组合 · 焦点 · chrome · 强调 · 留白 · 固定/自由 · 密度。
> 每帧有氛围（光晕 + 颗粒）；陈述型帧带漂浮药丸壁纸。

### 1 · 封面（身份 · 动势：title pill + display · 居中）

**地面** 奶油 + 氛围、漂浮药丸壁纸。**组合** title-pill、display、accent-line、floating-pills（5–8）。**焦点** 1–2 行 Bodoni `display` 墨色标题（斜体关键词为糖果色），居中，黄色 title-pill 之下；其下 coral accent-line。**Chrome** 大写 Space Grotesk 副标。**强调** 斜体词 + 糖果漂浮药丸。**留白** 内容居中；药丸填边缘。**固定** 药丸描边、Bodoni 墨、漂浮药丸扁平。**自由** 标题、糖果色相、药丸词/位置。**密度** 中等-氛围。

### 2 · 支柱卡片（目录 · 动势：三列网格 · 左对齐 —— 密集帧）

**地面** 奶油 + 氛围。**组合** title-pill（lavender）、section-headline、3× pill-card。**焦点** 三张白 2rem pill-card（圆形糖果 card-icon、Bodoni card-headline、Space Grotesk 正文），0.4cqw 阴影，置于 Bodoni section-headline 下。**Chrome** lavender 头 tag-pill。**强调** 三 card-icon 填充（coral/sky/lime 序列）。**留白** 紧凑 —— 密度例外（此处无漂浮药丸）。**固定** 2px 描边、柔和阴影、墨色标题。**自由** 卡片内容、图标色相。**密度** 密集-例外。

### 3 · 统计网格（数据 · 动势：stat pills · 标题居中）

**地面** 奶油 + 氛围。**组合** section-headline、3–4× stat-pill。**焦点** 一排白 stat-pill，各为 **着色** Bodoni stat-number + 大写标签 + accent bar。**强调** 着色数字 + 条（颜色触类型的唯一处）。**留白** 中等。**固定** 2rem 药丸、仅数字着色、柔和阴影。**自由** 数值（来自脚本）、色相。**密度** 标准。

### 4 · 引语拉引（quote · 动势：highlight pill · 左）

**地面** 奶油 + 氛围、少量漂浮药丸。**组合** quote-display、quote-highlight、accent-line。**焦点** Bodoni 墨色引语，一句外包 lime/sky `quote-highlight` 药丸（强调机制 —— **禁止**单独粗体）。**Chrome** 大写 attribution。**强调** highlight 药丸。**留白** ~50%。**固定** Bodoni 600、highlight-pill 强调。**自由** 引语、高亮色/短语。**密度** 稀疏。

### 5 · 轨道（概念 · 动势：引力药丸 · 居中）

**地面** 奶油 + 氛围。**组合** orbit-center（160px lime 圆、Bodoni 序数）、4–6 颗 orbit-pill 卫星（糖果、倾斜、柔和阴影）。**焦点** lime 中心由轨道糖果药丸锚定。**强调** 卫星色相。**留白** 中等。**固定** 圆心、带阴影描边卫星。**自由** 序数、卫星词/位。**密度** 中等。

### 6 · 收尾板（closer · 动势：title pill + display · 居中）

**地面** 奶油 + 氛围、漂浮药丸壁纸。**组合** title-pill（yellow）、closing-display、accent-line、floating-pills。**焦点** Bodoni `closing-display` 墨色 sign-off（斜体词 violet/糖果），居中。**强调** 斜体词 + 药丸。**留白** 内容居中。**固定** Bodoni 墨、扁平药丸。**自由** sign-off、药丸词。**密度** 中等-氛围。

## 构图规则

### 应当（Do）

- 每个文本容器为**药丸**（9999px / 2rem），带 **2px 墨线描边**。
- **Bodoni 标题墨色、sentence case**；颜色在统计数字 + 药丸填充。
- 内容容器用**柔和偏移阴影**（4/6/8/12px，8% 墨）；漂浮药丸保持扁平。
- 陈述型帧漂浮 **5–8 颗糖果药丸** + 径向光晕 + 颗粒；裸角显残缺。
- inline 强调用**糖果 quote-highlight 药丸**，禁止单独 bold/italic。
- 暖+冷+中性亮强调配对；封面/收尾偏居中，卡片/引语偏左。

### 禁止（Don't）

- 无尖角文本容器；无无描边药丸。
- 无着色 Bodoni 标题；无大写 Bodoni。
- 无模糊或改色阴影；无第十强调色。
- 装饰漂浮药丸无阴影。
- 勿让标题撑满宽 —— 按量适配。

## 宽高比行为

| 处理         | 16:9                           | 9:16                        | 1:1                   |
| ------------ | ------------------------------ | --------------------------- | --------------------- |
| Cover        | display 居中，药丸环绕         | display 在上，药丸带        | 居中，药丸更少        |
| Pillar Cards | 标题 + 三列                    | 标题 + 三行堆叠             | 标题 + 2+1            |
| Stat Grid    | 3–4 横排                       | 2×2                         | 2×2                   |
| Pull Quote   | 引语左对齐                     | 引语在上，高亮 inline       | 居中                  |
| Orbit        | 中心 + 4–6 卫星                | 中心 + 3 卫星               | 中心 + 4              |
| Closing      | 居中 + 药丸                    | 居中，药丸带                | 居中                  |

`pad` 沿短边保持；在 1.4cqw 下限之上重设 display。更紧比例时减少漂浮药丸数量，保持壁纸感而非 clutter。

## 已批准实体

源文件未定义真实客户、logo 或供应商 —— 此类标记一律占位渲染。漂浮药丸词为中性氛围（「VISION」「FUTURE」「NEXT」），**从不**内容专属。

## 数字与主张（硬规则）

帧尺度**禁止**臆造数字、统计或计数。槽位渲染为 `— figure —`、`{metric}`、`N%`。stat-pill 数字与 bar-track 宽度在脚本供值前保持占位。

## 渲染前自检

- **眯眼** —— 一条 Bodoni 元素为邻元素的 3–5 倍。
- **留白** —— 陈述型帧有氛围无 clutter；仅 pillar/stat 网格可密。
- **药丸** —— 每容器为带 2px 描边的药丸；无尖角文本容器。
- **颜色** —— 糖果仅填充 + 统计数字；标题墨；无第十色。
- **深度** —— 柔和偏移阴影仅内容；漂浮药丸扁平；无 blur。
- **字型** —— Bodoni 墨 sentence-case、按量适配；药丸大写加字距；≥1.4cqw 下限。
- **锚点** —— 封面/收尾/orbit 居中，卡片/引语左；禁止连续 3 帧同布局。
- **捏造** —— 每个数字可追溯到脚本，否则占位。

## 已知缺口

- **动效刻意不在范围。** frame.md 仅规定构图；源中 0.6s fade 为 deck 机制。
- **Bodoni Moda + Space Grotesk 经 Google Fonts。** CJK 配对（ZCOOL XiaoWei / Yozai）沿用源文件。
- **9:16 / 1:1 为指导**；须验证下限与漂浮药丸数量随比例缩减。
- 颗粒叠加、径向光晕、漂浮药丸与条填充均为纯 CSS；无需外部图。
