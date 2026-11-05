---
version: alpha
name: Blue Professional — Frame (video / frame layer)
description: >
  Blue Professional design.md 的视频优先配套文档。基本单位为帧（1920×1080）。原子级 token 完全一致且不可改动 ——
  暖奶油色画布、单一饱和钴蓝（#1e2bfa）作为唯一强调色、三级灰度文字阶梯、Space Grotesk（展示/数字/界面元素）+
  Inter（正文）、柔和钴蓝着色卡片（4% 填充 / 20% 边框 / 10–14px 圆角）且**无阴影**、胶囊形界面元素，以及钴蓝进度条。
  构图与帧尺度重写。动效不在本文范围。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  bg: "#fdfae7"
  primary: "#1e2bfa"
  text: "#111111"
  text-muted: "#6b6b6b"
  text-light: "#9a9a9a"
  accent-light: "rgba(30,43,250,0.08)"
  accent-medium: "rgba(30,43,250,0.15)"
  border: "rgba(30,43,250,0.2)"
  card-bg: "rgba(30,43,250,0.04)"
  positive: "#059669"
  negative: "#dc2626"

radii:
  pill: "100px"
  card-lg: "14px"
  card-md: "12px"
  card-sm: "10px"
  bar: "6px"
  circle: "50%"

typography:
  # — 阅读阶梯（Inter 正文 + Space Grotesk 界面元素）—
  body:    { fontFamily: "Inter", cqw: 0.85, weight: 400, lineHeight: 1.6, color: "text-muted" }
  h4-eyebrow:{ fontFamily: "Space Grotesk", cqw: 0.8, weight: 600, tracking: "0.08em", upper: true, color: "primary" }
  tag:     { fontFamily: "Space Grotesk", px: 12, weight: 500, color: "primary" }
  counter: { fontFamily: "Space Grotesk", px: 13, weight: 500, tracking: "0.05em", color: "text-muted" }
  # — 展示 / 数字阶梯（Space Grotesk，近黑标题 / 钴蓝数字）—
  h3:      { fontFamily: "Space Grotesk", cqw: 1.25, weight: 500, lineHeight: 1.3, tracking: "-0.02em", color: "text" }
  stat-num:{ fontFamily: "Space Grotesk", cqw: 1.9, weight: 700, lineHeight: 1.0, color: "primary" }
  blockquote:{ fontFamily: "Space Grotesk", cqw: 2.4, weight: 500, lineHeight: 1.35, color: "text" }
  h2:      { fontFamily: "Space Grotesk", cqw: 2.6, weight: 600, lineHeight: 1.1, tracking: "-0.02em", color: "text" }
  metric-value:{ fontFamily: "Space Grotesk", cqw: 3.0, weight: 700, lineHeight: 1.0, color: "primary" }
  h1:      { fontFamily: "Space Grotesk", cqw: 4.2, weight: 700, lineHeight: 1.08, tracking: "-0.02em", color: "text" }
  quote-mark:{ fontFamily: "Space Grotesk", cqw: 8.0, weight: 700, lineHeight: 0.5, color: "primary", opacity: 0.15 }

spacing:
  pad-x: "5cqw"
  pad-y-top: "5cqw"
  gap-cards: "1.4cqw"
  accent-line: "60px × 4px"

components:
  card-tinted:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    shadow: "none"
    description: "通用内容卡片。禁止纯色填充、禁止不透明边框、禁止阴影。"
  metric-card:
    backgroundColor: "{colors.card-bg}"
    border: "1.5px solid {colors.border}"
    rounded: "{radii.card-lg}"
    typography: "{typography.metric-value} ({colors.primary}) + {typography.metric-label} + {typography.metric-desc}"
    description: "可选内联 ↑/↓ 变化芯片（{colors.positive}/{colors.negative} 文字，无填充）。"
  tag-pill:
    backgroundColor: "{colors.accent-light}"
    textColor: "{colors.primary}"
    rounded: "{radii.pill}"
    typography: "{typography.tag}"
    description: "位于 slide-header 右上角。"
  cta-button:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.bg}"
    rounded: "{radii.pill}"
    typography: "Space Grotesk 600"
    shadow: "soft cobalt on hover only — the system's only shadow"
    description: "系统中唯一的实心元素。"
  accent-line:
    backgroundColor: "{colors.primary}"
    size: "60×4, 2px radius"
    description: "封面标题上方 / 眉题分隔线。"
  bar-track:
    backgroundColor: "{colors.accent-light}"
    fill: "{colors.primary} (display:block so width resolves)"
    rounded: "{radii.bar}"
    description: "28px 轨道；填充条承载数值。"
  step-circle:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.bg}"
    rounded: "50%"
    size: "56px"
    description: "顺序步骤不透明度 1.0→0.85→0.7→0.55。"
  split-highlight:
    backgroundColor: "{colors.accent-light}"
    borderLeft: "4px solid {colors.primary}"
    rounded: "{radii.card-md}"
    description: "内联引语高亮标注。"
  slide-header:
    typography: "{typography.h4-eyebrow} (cobalt) left, tag-pill right; {typography.h2} below"
    description: "每个内容帧顶部的带状区域。"
  atmosphere:
    elements: "clipped diagonal cobalt-tint panel, 3×3 cobalt dot grid, concentric closing rings"
    description: "仅用于封面/结尾。内容帧禁止使用。"
  progress-bar:
    backgroundColor: "{colors.primary}"
    size: "3px tall, bottom edge, width grows with index"
    description: "持久进度条。"
---

# Blue Professional — Frame（视频 / 帧层）

## 概述

Blue Professional 在帧尺度上是一套**咨询级体系：克制之中有一处强承诺。**暖奶油色画布与单一饱和钴蓝承载全部强调 ——
眉题、指标、CTA、图表填充、进度条。无第二品牌色、无 pastel，只有奶油色、钴蓝与紧凑的灰度阶梯。气质贴近投资研究 /
McKinsey 简报：克制、数据密集但不拥挤，远距离仍便于高管阅读。

语气由两种字体固定分工：**Space Grotesk**（展示、一切数字、全部界面元素 —— 眉题大写 0.08em）与 **Inter**（正文、 muted
灰、行高 1.6）。标题近黑；钴蓝保留给强调时刻。层次**柔和且着色** —— 4% 钴蓝卡片填充、20% 钴蓝边框、10–14px 圆角 ——
从不加阴影。无硬阴影正是高级信号。

**帧尺度关键特征：**

- 每一帧 **暖奶油底色**；**单一钴蓝** 为唯一强调色。
- **Space Grotesk**（展示/数字/界面元素）+ **Inter**（正文）— 近黑标题、钴蓝数字。
- **着色卡片** — 钴蓝 4% 填充、钴蓝 20% 1.5px 边框、10–14px 圆角，**无阴影**。
- **胶囊形界面元素**（100px）— 标签胶囊 + 唯一实心钴蓝 CTA；钴蓝 **进度条**。
- **处处柔和圆角**（除进度条外无直角）。
- **氛围元素**（对角面板、点阵、同心环）仅用于封面/结尾。

## 帧（The Frame）

### 帧工艺门槛（Frame Craft Bar）

任意结构检查之前，每一帧须通过三项肉眼测试：

- **眯眼（Squint）** — 一处 **近黑标题或钴蓝数字** 在 3–6× 邻域尺度上占主导。
- **留白（Silence）** — 内容帧 **均衡、不拥挤**；**仪表盘是唯一允许密集的例外**。
- **克制（Restraint）** — **单一钴蓝强调** 承载一切；标题保持近黑（禁止钴蓝标题）；无阴影（着色卡片承担层次）；涨跌仅内联文字。
- **参照（Reference）** — 对标 **投资研究 / McKinsey 季度简报**；失败样例像 **粗描边、多色仪表盘**。

- **主画布：** 1920×1080（16:9）。展示尺寸用 **`cqw`** 编写（`px ÷ 1920 × 100 = cqw`）。
- **竖版：** 1080×1920（9:16）。**方图：** 1080×1080（1:1）。
- **安全区：** `pad-x` 5cqw；底部为计数器 + 进度条预留空间。

**容器法则（承重规则）。** 每一帧底色设置 `container-type: size`；所有帧相对单位均为相对它的 `cqw`/`cqh` —— 禁止
`vw`。卡片圆角保持 px（10–14px）；胶囊半径保持 100px；边框保持 1–1.5px。

## 色彩（Colors）

Token 与源文件一致。`{colors.bg}` 奶油色为 universal ground；`{colors.primary}` 钴蓝为 **唯一** 强调 —— 每个眉题、数字、
CTA、图表填充、进度条及 4px 高亮左规则线。标题为 `{colors.text}` 近黑（禁止钴蓝标题）；正文为 `{colors.text-muted}`；第三级为
`{colors.text-light}`。卡片填充 `{colors.card-bg}`（4%），边框 `{colors.border}`（20%）。`{colors.positive}`/`{colors.negative}`
**仅内联** 出现在方向变化芯片上 —— 禁止作为填充色。**禁止第二强调色。**

## 字体（Typography）

两套阶梯。**阅读阶梯**（Inter 正文 0.85cqw muted；Space Grotesk 眉题大写 0.08em 钴蓝）承载文案与界面元素；**展示/数字阶梯**
（Space Grotesk `h3` 1.25cqw → `h1` 4.2cqw 近黑；数字 `stat-num`/`metric-value` 钴蓝）承载标题与 figures。

- **可读性下限：** 任何承重文本行 ≥ **1.4cqw**；px 界面元素（tag/counter）仅作 colophon。
- **按量适配：** 按标题长度定字号。块宽上限 **≤ 78cqw**；≤3 词 → `h1`；4–6 → `h2`；7+ → `h3`。钴蓝数字按卡片尺寸在 `metric-value`→`stat-num` 间缩放。
- **标题近黑、−0.02em**；**眉题钴蓝、大写、0.08em**；**数字钴蓝 600–700**；**正文 Inter 400 muted、行高 1.6**。禁止斜体、禁止正文大写、禁止钴蓝标题。

## 深度与表面（Depth & Surface）

柔和着色 —— 禁止偏移。层次来自：

- **着色卡片** — 4% 钴蓝填充 + 20% 钴蓝 1.5px 边框 + 10–14px 圆角，无偏移即显抬升。
- **左边框强调** — split-highlight 块上 4px 钴蓝规则线将标注前拉。
- **圆角** — 10–14px 圆角是柔和感的一部分；直角会破坏它。

**上限：** 内容零 box-shadow（唯一阴影为柔和钴蓝 CTA _hover_）；禁止不透明钴蓝边框；禁止硬描边。

## 形状（Shapes）

- **100px** — 标签胶囊、CTA、导航按钮（胶囊形界面元素）。
- **14/12/10px** — 按尺寸的卡片（大指标 / 标准 stat / 细节 + mini）。
- **6px** — 条形轨道 + 填充。**50%** — 步骤圆、导航圆、点、结尾环。
- **0** — 仅进度条。内容禁止直角。

## 组件（Components）

- **card-tinted / metric-card** — 通用柔和着色内容卡片（无阴影）。
- **tag-pill / cta-button / accent-line** — 钴蓝胶囊界面 + 唯一实心 CTA + 60×4 规则线。
- **bar-track / step-circle / split-highlight** — 钴蓝数据 + 序列 + 标注模式。
- **slide-header**（眉题 + 标签胶囊）— 结构节奏；**atmosphere**（对角/点阵/环）仅封面/结尾；**progress-bar** 每帧必有。

## 帧处理（Frame Treatments）

> 配方：ground · container · composes · focal · chrome · accent · silence · Fixed/Free · density。
> 氛围仅封面/结尾；内容帧遵循 slide-header 节奏。

### 1 · 封面（identity · move: diagonal accent · left）

**Ground** 奶油色 + 裁剪对角钴蓝着色面板（右侧约 36%）+ 3×3 钴蓝点阵。**Composes** accent-line、meta、h1、body sub。**Focal**
2 行 Space Grotesk `h1` 近黑、左对齐，位于钴蓝 accent-line + meta 之下。**Chrome** counter + progress bar。**Accent** 钴蓝线 +
对角面板。**Silence** 对角面板占据右三分之一。**Fixed** 近黑 h1、钴蓝强调、仅此处有 atmosphere。**Free** 标题、meta。**Density** 低。

### 2 · 仪表盘（data · move: 3-up metric grid · 密集帧）

**Ground** 奶油色、`pad-x`。**Composes** slide-header（眉题 + tag-pill）、h2、3× metric/tinted card。**Focal** 一行着色卡片 ——
钴蓝 `metric-value` + Inter 标签 + muted 说明 + 可选绿/红变化芯片。**Chrome** 眉题左、tag-pill 右；progress bar。**Accent** 钴蓝数字。
**Silence** 紧凑 —— 密度例外。**Fixed** 4% 着色卡片、20% 边框、无阴影、钴蓝数字。**Free** 数字（来自脚本）、标签。**Density** dense-exception。

### 3 · 条形排序（data · move: cobalt bars · left）

**Ground** 奶油色、`pad-x`。**Composes** 眉题、h2、bar-track 行。**Focal** 3–5 条带标签的钴蓝填充条，置于钴蓝 8% 轨道上并带钴蓝百分比。
**Chrome** 眉题；progress bar。**Accent** 钴蓝填充 + 数字。**Silence** 中等。**Fixed** 6px 轨道、钴蓝填充。**Free** 行、数值（来自脚本）。**Density** standard。

### 4 · 引语（quote · move: concentric rings · centered）

**Ground** 奶油色、居中， faint 同心 closing-rings 在背后。**Composes** quote-mark、blockquote、cite。**Focal** Space Grotesk `blockquote`
近黑，其下 15% 不透明度钴蓝 quote-mark；再下 uppercase 钴蓝-muted cite。**Accent** faint 环 + quote-mark。**Silence** ~55%。**Fixed**
近黑引语、柔和环。**Free** 引语、cite。**Density** 低。

### 5 · 分栏 + 高亮（content · move: asymmetric split · left）

**Ground** 奶油色、两列。**Composes** 眉题、h2、body、split-highlight 块。**Focal** Inter 正文列旁为钴蓝 8% 高亮块（4px 钴蓝左规则线）承载内联引语。
**Accent** 高亮左规则线。**Silence** 宽 gutter。**Fixed** 着色高亮、4px 钴蓝规则线。**Free** 正文、标注。**Density** standard。

### 6 · 结尾 / CTA（closer · move: centered rings + CTA）

**Ground** 奶油色 + 同心 closing-rings。**Composes** accent-line、h1、body、cta-button。**Focal** Space Grotesk `h1` 近黑、居中，其下唯一实心钴蓝 `cta-button` 胶囊。
**Accent** CTA + 环。**Silence** ~60%。**Fixed** 一个 CTA、近黑 h1、柔和环。**Free** 结语、CTA 文案。**Density** 低。

## 构图规则（Composition Rules）

### 应当（Do）

- 每一帧从 **暖奶油色** 起；让 **钴蓝承载全部强调**（眉题、数字、CTA、条、进度）。
- 标题 **近黑、−0.02em**；眉题 **钴蓝大写 0.08em**；数字 **钴蓝 600–700**。
- 使用 **着色卡片**（4% 填充、20% 边框、10–14px 圆角、无阴影）；正文 Inter 400 muted、行高 1.6。
- 全部界面元素 **胶囊形（100px）**；每个结尾帧一个实心钴蓝 CTA。
- **氛围**（对角面板、点阵、环）仅封面/结尾；内容帧保持 slide-header 节奏。
- 封面/仪表盘/分栏偏左，引语/结尾居中。

### 禁止（Don't）

- 禁止第二强调色；禁止钴蓝标题。
- 内容禁止 drop shadow（仅柔和钴蓝 CTA hover）；禁止不透明钴蓝边框。
- 禁止直角（进度条除外）；禁止替换字体；禁止正文大写。
- 禁止将绿/红变化芯片当作通用强调 —— 仅用于方向对比。
- 禁止用更粗边框填空间 —— 应增加实质内容；禁止标题撑满至边缘。

## 宽高比行为（Aspect-Ratio Behavior）

| 处理类型          | 16:9                       | 9:16                           | 1:1                      |
| ----------------- | -------------------------- | ------------------------------ | ------------------------ |
| 封面              | 标题左、对角右             | 标题上、对角带在下             | 标题偏上、点阵角落       |
| 仪表盘            | 3 卡横排                   | 3 卡竖叠                       | 2×2                      |
| 条形排序          | 3–5 条                     | 3–5 条（更紧）                 | 3 条                     |
| 引语              | 居中、环在背后             | 居中、更高                     | 居中                     |
| 分栏 + 高亮       | 并排                       | 竖叠                           | 竖叠                     |
| 结尾 / CTA        | 居中 + CTA                 | 居中 + CTA                     | 居中 + CTA               |

`pad-x` 在短边保持；在 1.4cqw 下限之上重新定展示字号。9:16 时对角封面面板变为上/下带。CJK 构建中数字仍为拉丁阿拉伯数字。

## 已批准实体（Approved Entities）

源文件未定义真实客户、标识或供应商 —— 此类标记一律渲染为占位。数字、指标、引语为内容；系统提供奶油色 + 钴蓝 + 灰度。

## 数字与声明（硬性规则）

帧尺度禁止编造数字、财务数据、百分比或日期。槽位渲染为 `— figure —`、`{metric}`、`+NN%`、`↑ —`。指标卡片、条值与 stat 单元尤其使用占位，直至脚本提供。**方向芯片须有脚本中的真实对比。**

## 渲染前自检（Pre-Render Self-Audit）

- **Squint** — 每帧一处近黑标题或钴蓝数字占主导。
- **Silence** — 内容帧均衡不拥挤；仅仪表盘可密集。
- **Single accent** — 仅钴蓝；标题近黑；涨跌仅内联。
- **Type** — Space Grotesk 标题 −0.02em 近黑，钴蓝眉题 0.08em + 数字；Inter 正文 muted 行高 1.6；≥1.4cqw 下限。
- **Depth** — 着色卡片（无阴影）、柔和圆角、20% 钴蓝边框；内容无直角。
- **Anchor** — 封面/仪表盘/分栏偏左，引语/结尾居中；氛围仅封面/结尾。
- **Fabrication** — 每个数字可追溯到脚本，否则占位。

## 已知缺口（Known Gaps）

- **动效 intentionally 不在范围。** frame.md 仅规定构图；源文件 500ms translateX 过渡 + 条填充动画属于 deck 机制。
- **Space Grotesk + Inter 经 Google Fonts。** CJK 配对（Noto Sans SC 700 展示 / Noto Serif SC 400 正文）沿用；眉题大写+字距在 CJK 中信号减弱 —— 与 accent-line 搭配使用。
- **9:16 / 1:1 为指导性说明**；须验证下限及对角面板是否 reflow 为带状。
- 对角面板（clip-path）、点阵、同心环与条均为纯 CSS；无需外部图像。
