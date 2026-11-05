---
version: alpha
name: Cartesian — Frame (video / frame layer)
description: >
  Cartesian design.md 的视频优先配套文档。基本单位为帧（1920×1080）。原子元素一致且不可改动——五色调暖石色板、
  Playfair Display 400 + Inter、作为唯一结构手段的 universal 1px 灰褐细线、圆规绘制的几何环，
  以及零阴影 / 零填充。构图、帧尺度与宽高比行为为帧层重写。克制是准则；动效不在范围内。
unit: 帧 — 主尺寸 1920×1080；并文档化 9:16 与 1:1
principle: 原子神圣 · 构图自由 · 数值来自脚本

colors:
  bg-primary: "#EDE8E0"
  bg-secondary: "#E2DBD1"
  text-primary: "#1A1A1A"
  text-secondary: "#5A5A5A"
  accent: "#8A8178"
  line: "#B8B0A4"
  white-overlay: "rgba(255,255,255,0.3)"

typography:
  # — 阅读梯度（Inter）—
  body:        { fontFamily: "Inter", cqw: 1.0,  weight: 400, lineHeight: 1.6, color: "text-secondary" }
  body-sm:     { fontFamily: "Inter", cqw: 0.85, weight: 400, lineHeight: 1.6 }
  subtitle:    { fontFamily: "Inter", cqw: 1.3,  weight: 400, lineHeight: 1.5 }
  label:       { fontFamily: "Inter", px: 14, weight: 500, tracking: "3px", upper: true, color: "accent" }
  attribution: { fontFamily: "Inter", px: 15, weight: 400, tracking: "2px", upper: true, color: "accent" }
  micro:       { fontFamily: "Inter", px: 12, weight: 400, tracking: "2px", upper: true, color: "accent" }
  # — 展示 / 主视觉梯度（Playfair Display 400，句首大写）—
  h3:          { fontFamily: "Playfair Display", cqw: 1.8, weight: 400, lineHeight: 1.1 }
  timeline-headline:{ fontFamily: "Playfair Display", cqw: 1.9, weight: 400, lineHeight: 1.1 }
  card-headline:{ fontFamily: "Playfair Display", cqw: 2.0, weight: 400, lineHeight: 1.15 }
  stat-figure: { fontFamily: "Playfair Display", cqw: 3.0, weight: 400, lineHeight: 1.0 }
  quote-mark:  { fontFamily: "Playfair Display", cqw: 9.0, weight: 400, lineHeight: 0.5, color: "line" }
  h2:          { fontFamily: "Playfair Display", cqw: 4.0, weight: 400, lineHeight: 1.1 }
  h1:          { fontFamily: "Playfair Display", cqw: 6.2, weight: 400, lineHeight: 1.06 }
  display:     { fontFamily: "Playfair Display", cqw: 8.0, weight: 400, lineHeight: 1.04 }

spacing:
  pad-x: "7cqw"
  pad-y: "5cqw"
  gap-xl: "6cqw"
  gap-lg: "5cqw"

components:
  hairline:
    rule: "0.07cqw solid {colors.line}"
    description: "通用结构手段——每条分隔线（议程线、时间轴连接线、卡片边框、统计顶线）都是这条 1px 灰褐线。不存在粗边框。"
  card:
    backgroundColor: "{colors.white-overlay}"
    border: "0.07cqw solid {colors.line}"
    rounded: "0"
    shadow: "none"
    description: "淡 white-overlay 填充（画布透出）使卡片与裸区域区分开。"
  card-icon:
    border: "0.07cqw solid {colors.line}"
    rounded: "50%"
    size: "40px circle"
    textColor: "{colors.accent}"
    typography: "Playfair numeral/letter"
    description: "环形圆标记。"
  agenda-row:
    borderBottom: "0.07cqw solid {colors.line}"
    typography: "{typography.h3} (numeral {colors.accent}, label {colors.text-primary})"
    description: "左侧数字、右侧标签，下方灰褐线。"
  timeline:
    borderTop: "0.07cqw solid {colors.line}"
    typography: "{typography.timeline-headline} + {typography.body-sm}"
    description: "条目上方一条灰褐顶线——无节点、无圆点。"
  stats-cluster:
    borderTop: "0.07cqw solid {colors.line}"
    typography: "{typography.stat-figure} + uppercase {colors.accent} labels"
    description: "内联 适中 统计数字（无 hero 大数）。"
  geo-ring:
    border: "1px solid {colors.line} (inner dashed ::before ~70–80%)"
    rounded: "50%"
    size: "10–50cqw"
    opacity: "0.2–0.5"
    description: "内容后方的圆规构造环。每帧 1–2 个，不超过。"
  horizontal-accent:
    backgroundColor: "{colors.text-primary}"
    size: "~18cqw × 1px"
    description: "系统中唯一的墨色线——封面/收尾上的强终点强调， 节制地 使用。"
  vertical-line:
    backgroundColor: "{colors.line}"
    size: "1px × full height, ~5cqw from edge"
    opacity: "0.3–0.4"
    description: "绘图纸对齐参考线。可选。"
  image-placeholder:
    backgroundColor: "{colors.bg-secondary}"
    mark: "crossed +30°/−30° 1px taupe diagonals (an X)"
    typography: "small uppercase {typography.micro}"
    description: "标志性的未接图占位标记。"
  team-photo:
    backgroundColor: "{colors.bg-secondary}"
    border: "0.07cqw solid {colors.line}"
    rounded: "50%"
    typography: "Playfair initial in {colors.accent}"
    description: "圆形肖像框。"
---

# Cartesian — Frame（视频 / 帧层）

## 概述

帧尺度的 Cartesian 是一套**安静的博物馆图录式编辑系统**——以 1px 线条实现克制。每条结构分隔都是单条 1px 灰褐细线；没有粗边框、
没有填充（淡 white-overlay 卡片除外）、没有阴影、没有圆角矩形。层级来自**字体对比与负空间**，氛围来自**圆规绘制的几何环**
在内容后方飘浮。

气质是文学式配对：**Playfair Display** 字重 400（细笔画 Didone，从不加粗，始终句首大写）以墨色承载所有标题、数字与引号；**Inter**
以暖灰承载正文、以灰褐大写标签（字距 2–3px）承载标注。色板为五暖石色加墨色——不存在 流行 强调色。正确密度是**疏朗可呼吸**：
石纹纸上，一个清晰想法，框定得当。

**帧尺度的关键特征：**

- **1px 灰褐细线**作为通用结构手段——每条分隔都是这一条线。
- **Playfair Display 400**（墨色、句首大写）用于展示；**Inter** 正文（灰）+ 标签（灰褐、加字距）。
- **五暖石 + 墨**——无红/蓝/绿；唯一的「色彩」是字体对比。
- **圆规几何环**（实线 + 虚线，20–50% 不透明度）在内容后方营造情绪。
- **扁平**——零阴影、零圆角矩形（仅圆形）；唯一的墨线是 `horizontal-accent`。
- **疏朗可呼吸**——大量负空间；拥挤即视为破损。

## 帧（The Frame）

### 帧工艺门槛（Frame Craft Bar）

任意结构检查之前，每帧须通过三项目测测试：

- **眯眼（Squint）**——一个 Playfair 元素在视觉上比最近邻大 **3–6 倍**；衬线/无衬线 + 字号对比承载层级，而非字重。
- **留白（Silence）**——陈述型帧约 **55–60% 为空**；Cartesian **没有密集帧**——即便议程/目录也留呼吸（拥挤即系统失效）。
- **克制（Restraint）**——每帧**最多两个 geo 环**；唯一的墨色 `horizontal-accent` 线 节制地 使用；永不使用 流行 强调色。
- **参照（Reference）**——对标 **Vignelli 编辑风 / Cooper Hewitt 图录 / 铅笔与描图纸方案**；失败形态像 **带阴影、圆角卡片的 SaaS 演示稿**。

- **主尺寸：** 1920×1080（16:9）。展示尺寸用 **`cqw`** 编写（`px ÷ 1920 × 100 = cqw`）。
- **竖屏：** 1080×1920（9:16）。**方图：** 1080×1080（1:1）。
- **安全区：** `pad-x`（7cqw）宽页边；几何可出血至边缘。

**容器法则（承重）。** 每帧底图设置 `container-type: size`；所有帧相对单位均为相对它的 `cqw`/`cqh`——
绝不用 `vw`。1px 细线与 geo 环在任意渲染尺寸下保持与帧的比例。

## 色彩

令牌与源文档一致。`{colors.bg-primary}` 为底；`{colors.text-primary}` 墨色用于标题与唯一黑色强调线；`{colors.text-secondary}` 灰用于正文；`{colors.accent}`
灰褐用于标签、数字、小字；`{colors.line}` 灰褐用于每条 1px 结构边框。`{colors.bg-secondary}` 为唯一次级填充（占位、相框）。**无 流行
强调色**——需要强调时，放大字号、无衬线→衬线，或加一条 `horizontal-accent` 墨线。标题永不为灰褐；小字永不为墨色。

## 字体

两条梯度。**阅读梯度**（Inter 正文 1.0cqw 灰、px 标签灰褐）承载文案与 chrome；**展示梯度**（Playfair `h3` 1.8cqw → `display` 8.0cqw，均字重 400）承载所有标题。

- **可读下限：** 任何承重行 ≥ **1.4cqw**；px 标签仅为 chrome。
- **按量适配：** 按标题长度定字号。块宽上限 **≤ 78cqw**；≤3 词 → `display`/`h1`；4–6 → `h2`；7+ → `h3`。Cartesian 无主视觉统计大数——统计保持 适中（`stat-figure` 3cqw）。
- **Playfair 400、墨色、句首大写**——不加粗、不全大写、不用灰褐。**Inter 标签大写、字距 2–3px、灰褐。** 强调仅用 Playfair 斜体。

## 深度与表面

唯一手法是扁平平面。层级来自：

- **字体对比**——Playfair 衬线 vs Inter 无衬线；8cqw→0.7cqw 尺度。
- **1px 灰褐细线**——每条分隔、卡片轮廓、时间轴线、相框环。
- **色调**——墨 vs 灰 vs 灰褐。
- **负空间**——宽裕内边距。
- **几何氛围**——圆规环暗示深度而不真正造深。

**上限：** 无 box-shadow、无浮起卡片、无渐变、无圆角矩形。唯一非灰褐线是 `horizontal-accent` 墨线。

## 形状

- **50%（圆）**——card-icon、team-photo、nav-dot、每个 geo 环。
- **0**——其余一切；软圆角不存在。

## 组件

- **hairline**——通用 1px 灰褐分隔（身份标识）。
- **card**（1px 灰褐 + white-overlay）/ **card-icon**（环圆）/ **agenda-row** / **timeline**（线、无节点）/ **stats-cluster**——均建立在 hairline 上。
- **geo-ring**——圆规装饰（实线 + 虚线），每帧 1–2 个。**horizontal-accent**——唯一墨线， 节制地。**vertical-line**——绘稿参考线。
- **image-placeholder**（交叉 X）/ **team-photo**（环内首字母）——石色填充占位。

## 帧处理（Frame Treatments）

> 配方：底 · 容器 · 组合 · 焦点 · chrome · 强调 · 留白 · 固定/自由 · 密度。
> 每帧疏朗可呼吸；geo 装饰最多 1–2 个。

### 1 · 封面（identity · move: serif + compass ring · left）

**底** `{colors.bg-primary}`，`pad-x`。**组合** geo-ring（右，~34cqw，实线+虚线），vertical-line（左），label，display/h1。**焦点** 2–3 行 Playfair `display`/`h1` 墨色标题（关键词斜体），左锚，上方灰褐 `label`、下方 Inter 副标题。**Chrome** 可选底栏 meta（Playfair 值 + 灰褐 label）。**强调** geo 环；可选一条 `horizontal-accent` 墨线（若不与 meta 冲突）。**留白** ~55% 空。**固定** Playfair 400 墨色句首大写、≤2 geo 元素、1px 线。**自由** 标题、环位置、meta。**密度** 稀疏。

### 2 · 议程 / 目录（index · move: hairline list · left）

**底** `{colors.bg-primary}`，`pad-x`。**组合** label，h2，agenda-rows。**焦点** Playfair `h2` 下 4–6 行议程（Playfair 数字灰褐 + Playfair 标签墨色），每行 1px 灰褐线。**Chrome** 灰褐 `label` 眉题。**强调** 无——灰褐数字承担。**留白** 适中；行距宽裕。**固定** 1px 灰褐线、Playfair 400。**自由** 条目、数量。**密度** 标准（稀疏行）。

### 3 · 引语（quote · move: centered statement · compass ring）

**底** `{colors.bg-primary}`，居中。**组合** geo-ring（居中虚线，~26cqw），quote-mark，h2/display-quote，attribution。**焦点** 2 行 Playfair 引文墨色居中，50% 灰褐 Playfair quote-mark 之上；下方灰褐大写 attribution。**强调** 淡居中环。**留白** ~60%——刻意开阔。**固定** Playfair 400、一环、居中。**自由** 引文、 attribution。**密度** 稀疏。

### 4 · 收尾板（closer · move: centered ring · centered）

**底** `{colors.bg-primary}`，居中。**组合** geo-ring（居中，~40cqw，实线+虚线），label，h1/display，horizontal-accent。**焦点** 1–2 行 Playfair 结语墨色（关键词斜体）居中于最大圆规环内；下方短墨色 `horizontal-accent`。**强调** 环 + 唯一墨线。**留白** ~60%。**固定** Playfair 400、居中、≤2 geo。**自由** 结语、环尺度。**密度** 稀疏。

### 5 · 双栏编辑（content · move: asymmetric split · left）

**底** `{colors.bg-primary}`，`pad-x`，双栏 `gap-xl`。**组合** label，h2，body，image-placeholder（交叉 X）或 card。**焦点** 文本栏 Playfair `h2` + Inter body；另一栏 image-placeholder 或 card。**强调** 无。**留白** 宽栏间距。**固定** 1px 灰褐 card/placeholder 边、white-overlay 填充。**自由** 哪侧文本、正文。**密度** 标准。

### 6 · 统计 / 时间轴（data · move: hairline rail · left）

**底** `{colors.bg-primary}`，`pad-x`。**组合** label，h3，stats-cluster 或 timeline。**焦点** 适中 Playfair 统计行（或 1px 线时间轴：年 + 标题 + 正文，无节点），上方 1px 灰褐顶线框定。**强调** 无。**留白** 适中。**固定** 适中 统计尺度、hairline、无节点。**自由** 数字、阶段。**密度** 标准。

## 构图规则

### 应当

- 每条分隔使用**单条 1px 灰褐线**——hairline 即身份。
- 所有 **Playfair 标题** 设为 400、墨色、句首大写；标签灰褐、大写、字距 2–3px。
- 在内容后方叠 **一至两个圆规环**（实线 + 虚线，20–50% 不透明度）营造氛围。
- 让帧**可呼吸**——稀疏、宽裕负空间；陈述型帧 55–60% 空。
- 引语/收尾偏居中；封面/议程/编辑偏左/不对称。占位填充用 `bg-secondary`。

### 禁止

- 勿引入 流行 强调色——仅石色与墨。
- 勿加粗 Playfair、标题用灰褐、或使用粗（2px+）边框。
- 勿加阴影、浮起卡片或圆角矩形（仅圆）。
- 勿挤满帧——拥挤布局视为破损。
- 每帧 geo 装饰不超过两个；勿让标题顶满边到边。

## 宽高比行为

| 处理                 | 16:9                       | 9:16                                | 1:1                         |
| -------------------- | -------------------------- | ----------------------------------- | --------------------------- |
| 封面                 | 标题左、环右               | 标题上、环下                        | 标题偏上、环在后            |
| 议程 / 目录          | h2 + 行                    | h2 + 行（更紧）                     | h2 + 行                     |
| 引语                 | 居中、环在后               | 居中、更高                            | 居中                        |
| 收尾板               | 环内居中                   | 居中、环缩放                        | 居中                        |
| 双栏编辑             | 文 + 视觉并排              | 堆叠（折叠）                        | 堆叠                        |
| 统计 / 时间轴        | 水平轨                     | 垂直堆叠（去掉时间轴线）            | 紧凑                        |

短边保持宽裕 `pad-x`；在 1.4cqw 下限之上按上表重设 display。9:16 下时间轴线在堆叠时失去意义——改为垂直列表（依源文档）。

## 已批准实体

源文档未定义真实客户、标识或供应商——此类标记一律渲染为占位（交叉 X 的 image-placeholder，或肖像用环内首字母）。

## 数字与陈述（硬规则）

帧尺度永不捏造数字、日期或计数。槽位渲染为 `— figure —`、`{metric}`。统计与时间轴年份在脚本提供前保持占位。议程序号（01、02…）为装饰，可顺序编号。

## 渲染前自检

- **眯眼**——一个 Playfair 元素主导；衬线/无衬线对比承载层级。
- **留白**——陈述型帧 55–60% 空；无拥挤。
- **色板**——仅五石 + 墨；无 流行 强调；标题墨色、标签灰褐。
- **线条**——每条分隔为 1px 灰褐 hairline；唯一墨线为 `horizontal-accent`。
- **字体**——Playfair 400 句首大写、按量适配；标签大写字距 2–3px；≥1.4cqw 下限。
- **深度**——0 阴影、0 圆角矩形；每帧 ≤2 geo 环。
- **锚点**——引语/收尾居中，封面/议程/编辑左/不对称；勿连续三帧相同。
- **捏造**——每个数字可追溯到脚本，否则占位。

## 已知缺口

- **动效有意不在范围内。** frame.md 仅规定构图；源文档中 0.6s 淡入为演示稿机制。
- **Playfair Display + Inter 经 Google Fonts。** CJK 配对（Noto Serif SC 700/400）沿用；Playfair 无汉字斜体——强调改用字重/灰褐。
- **9:16 / 1:1 为指导**；须验证可读下限且时间轴折叠为垂直列表。
- Geo 环、交叉 X 占位、内虚线环均为纯 CSS；无需外部图像。
