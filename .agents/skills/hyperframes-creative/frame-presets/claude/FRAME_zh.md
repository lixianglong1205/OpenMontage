---
version: alpha
name: Claude — Frame (video / frame layer)
description: >
  与 Claude 的 design.md 配套的「视频优先」文档。基本单位是帧（1920×1080）。原子元素一致且不可违背 ——
  暖奶油色纸张（绝不用纯白、绝不用冷色），单一赤陶珊瑚色作为稀缺的「电压」点缀，发丝级墨线抬升（无重阴影），
  全部展示用 EB Garamond + 正文 Inter + 索引/代码声部 JetBrains Mono（置于暖海军蓝代码面），
  展示层 sentence-case，以及 ✱ 珊瑚色 spike 标记。构图与帧尺度已重写。动效不在本文范围。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  ink: "#141413"
  cream: "#FAF9F5"
  tile: "#EFE9DE"
  tile-strong: "#ECE3D4"
  coral: "#CC785C"
  navy: "#181715"
  navy-soft: "#1F1E1B"
  navy-elev: "#252320"

borders: { hairline: "1px solid ink@12%", hairline-strong: "1px solid ink@20%", dark: "1px solid cream@14% (on navy)" }
shadows: { card: "0 1px 3px ink@8%, 0 4px 16px ink@4%", none: "none" }

typography:
  # — 阅读 + 界面 chrome 阶梯 —
  body:    { fontFamily: "Inter", cqw: 1.5, weight: 400, lineHeight: 1.5 }
  lead:    { fontFamily: "Inter", cqw: 2.08, weight: 400, lineHeight: 1.5 }
  card-title:{ fontFamily: "Inter", cqw: 2.3, weight: 500, lineHeight: 1.25, tracking: "-0.005em" }
  button:  { fontFamily: "Inter", cqw: 1.46, weight: 500, lineHeight: 1.0 }
  tag-upper:{ fontFamily: "Inter", cqw: 1.35, weight: 500, tracking: "0.18em", upper: true }
  kicker:  { fontFamily: "JetBrains Mono", px: 28, cqw: 1.46, weight: 500, tracking: "0.16em", upper: true }
  mono-label:{ fontFamily: "JetBrains Mono", px: 26, cqw: 1.35, weight: 500, tracking: "0.02em" }
  code:    { fontFamily: "JetBrains Mono", cqw: 1.67, weight: 400, lineHeight: 1.6 }
  # — 展示阶梯（EB Garamond 400，sentence case，负字距。渲染器仅内嵌 400/700 —— 作者用 400；斜体为合成倾斜） —
  headline:{ fontFamily: "EB Garamond", cqw: 4.6, weight: 400, lineHeight: 1.06, tracking: "-0.018em" }
  quote-pull:{ fontFamily: "EB Garamond", cqw: 5.0, weight: 400, lineHeight: 1.12, tracking: "-0.012em", italic: true }
  display-italic:{ fontFamily: "EB Garamond", cqw: 6.7, weight: 400, lineHeight: 1.05, tracking: "-0.012em", italic: true }
  display:{ fontFamily: "EB Garamond", cqw: 7.3, weight: 400, lineHeight: 1.02, tracking: "-0.022em" }
  number-hero:{ fontFamily: "EB Garamond", cqw: 9.4, weight: 400, lineHeight: 0.95, tracking: "-0.025em" }
  display-cover:{ fontFamily: "EB Garamond", cqw: 9.9, weight: 400, lineHeight: 0.98, tracking: "-0.028em" }
  number-unit:{ fontFamily: "JetBrains Mono", cqw: 2.08, weight: 500, lineHeight: 1.0 }

spacing:
  slide-pad: "4.2cqw"   # ~80px @1920
  gap-md: "1.7cqw"
  hairline: "1px"
  radius-sm: "6px"
  radius-md: "8px"
  radius-lg: "12px"
  radius-pill: "9999px"

components:
  card-hairline:
    backgroundColor: "{colors.cream} or {colors.tile}"
    border: "1px solid {colors.ink}@12%"
    rounded: "{spacing.radius-lg}"
    shadow: "{shadows.card}"
    typography: "{typography.card-title} + {typography.body}"
    description: "编辑向内容卡片。抬升靠发丝线 + 一道柔和暖阴影 —— 绝不用重投影、光晕或渐变。"
  kicker-spike:
    typography: "{typography.kicker}"
    mark: "✱ coral spike prefix"
    description: "眉题 —— JetBrains Mono 大写，索引式（2–5 词），前缀为珊瑚 ✱。绝不用纯文本，绝不用完整句子。"
  coral-callout:
    backgroundColor: "{colors.coral} (full-bleed) or {colors.cream} with a coral edge"
    textColor: "{colors.cream} on coral"
    rounded: "{spacing.radius-md}"
    typography: "{typography.button} / {typography.h2}"
    description: "每帧唯一的电压时刻 —— CTA、单一内联链接，或全出血色带。一帧内绝不超过一处珊瑚。"
  number-lockup:
    typography: "{typography.number-hero} figure + {typography.number-unit} unit"
    description: "英雄数据 —— EB Garamond 数字配 JetBrains Mono 单位（200K、+1,204、−318、17 files）。数字为衬线；单位始终为 mono，绝不用衬线。"
  pull-quote:
    typography: "{typography.quote-pull} (EB Garamond italic) + {typography.tag-upper} cite"
    description: "提交说明、审阅者原话或论点。EB Garamond 斜体，下方小字 Inter 大写 cite。"
  section-rule:
    rule: "1px solid {colors.ink}@12% (or {colors.cream}@14% on navy)"
    description: "唯一分隔线。可用珊瑚 1px 规则线引入章节。绝不用 2px+，绝不用粗分隔。"
  code-surface:
    backgroundColor: "{colors.navy} body / {colors.navy-elev} title bar + status strip"
    textColor: "{colors.cream} (JetBrains Mono); syntax in coral (keywords) / teal #5DB8A6 (strings) / amber #E8A55A (numbers)"
    border: "1px solid {colors.cream}@14%"
    rounded: "{spacing.radius-md}"
    description: "暖海军蓝代码/终端面。代码本体由 code-* 注册表块（code-diff / code-typing / code-snippet-*）渲染；本预设只负责外围表面、标题栏、状态条与 mono chrome —— 不负责代码渲染本身。"
  spike-mark:
    glyph: "✱ (U+2731), always {colors.coral}"
    description: "品牌标记。在单次强调节拍上淡入 + 缩放 0.92→1；绝不旋转。"
---

# Claude — Frame（视频 / 帧层）

## 概述

Claude 在帧尺度上是一本**活过来的暖色编辑向品牌书** —— 文学出版社或研究笔记的语域。论点是三种颜色：**奶油是地面、墨是声部、珊瑚是电压** —— 第四种（暖海军蓝）仅出现在代码处。每一面都是**暖奶油**（绝不用纯白、绝不用冷灰）；内容聚在**比地面深半阶的 tile 面**上 —— 分界是半阶，绝不是硬对比。抬升是**1px 发丝线**低透明度墨线边框，偶尔再加一道柔和暖阴影。没有重投影、光晕，内容上也没有渐变。

三种编辑声部，各用一款字体：**EB Garamond** 承担全部展示时刻 —— 封面、标题、引文、大统计数字 —— 大号展示、轻微负字距；其**斜体**是表现 register。**Inter** 承担正文、导语、卡片标题、按钮与 UI chrome。**JetBrains Mono** 承担索引层 —— kicker、技术标签、代码窗口、状态条。若某声部换字体，register 即塌：无衬线标题或衬线标签会像另一个品牌。

**帧尺度的关键特征：**

- **奶油 / 墨 / 珊瑚三位一体** + 暖海军蓝代码面；奶油为默认地面，墨为声部，珊瑚为稀缺电压。
- **EB Garamond**（sentence case，负字距）用于全部展示；**Inter** 正文/chrome；**JetBrains Mono** 索引 + 代码。
- **发丝线抬升** —— 1px 低透明度墨线边框 + 至多一道柔和暖阴影。无重投影、光晕或渐变。
- **珊瑚定量配给** —— 每帧至多一处珊瑚（CTA、内联链接，或全出血色带）；珊瑚绝不用于标题或正文跑版。
- **密度自由** —— 按内容需要填满帧；一帧可只有一个焦点，也可密集分层构图。
- **✱ 珊瑚 spike** 打开 kicker；暖海军蓝专留给代码/终端面。

## 帧（The Frame）

### 帧工艺检查条（Frame Craft Bar）

在任何结构检查之前，先用肉眼测试把关每一帧：

- **眯眼** —— 一处 EB Garamond 展示 moment 在 3–6× 邻域尺寸上占主导。
- **三位一体** —— 奶油/tile 地面、墨字、珊瑚**恰好一次**；暖海军蓝仅在代码面；无冷灰 / 纯白 / 第四种色相。
- **字体** —— EB Garamond sentence-case 展示（负字距）；Inter 400 正文；JetBrains Mono kicker（大写 0.16em，珊瑚 ✱）+ 代码。

- **主比例：** 1920×1080（16:9）。展示尺寸用 **`cqw`** 编写（`px ÷ 1920 × 100 = cqw`）。
- **竖屏：** 1080×1920（9:16）。**方图：** 1080×1080（1:1）。
- **安全区：** `slide-pad` 约 4.2cqw；kicker/mono chrome 在其内。

**容器法则（承重）。** 每一帧地面设置 `container-type: size`；所有帧相对单位均为相对它的 `cqw`/`cqh` —— 绝不用 `vw`。发丝线保持 1px；卡片圆角保持 6/8/12px；暖纸阅读感必须在各比例下成立。

## 颜色

令牌与源文件一致。默认地面 `{colors.cream}`；内容聚在 `{colors.tile}` / `{colors.tile-strong}`（暖色半阶，非硬对比）。**标题与正文：** 奶油/tile 上 `{colors.ink}`；海军蓝上 `{colors.cream}`。**珊瑚**（`{colors.coral}`）是稀缺电压 —— 每帧一处（CTA、内联链接或全出血色带），绝不用作正文，绝不用作卡片填充。**暖海军蓝**（`{colors.navy}` / `navy-soft` / `navy-elev`）是代码 / 终端 / 深色卡片面 —— 结构锚点，非第四种品牌色。**无冷灰、无纯白、无纯黑。**

**固定语法色（装饰，不可 remix 的品牌色）。** 当代码行是手排而非由 `code-*` 块渲染时，关键字为珊瑚，字符串为 **teal `#5DB8A6`**，数字为 **amber `#E8A55A`**；状态读 success `#5DB872` / warn `#C64545`。这些跟随代码面，不属于品牌三位一体 —— 勿纳入品牌调色板。

## 字体

两条阶梯。**阅读/chrome 阶梯**（Inter `body` 1.5cqw / `lead` 2.08cqw weight 400；JetBrains Mono `kicker`/`mono-label` 用 px）承担文案 + chrome；**展示阶梯**（EB Garamond `headline` 4.6cqw → `display-cover` 9.9cqw，weight 400，负字距）承担全部标题 + 统计。

- **可读性下限：** 任何承重行 ≥ **1.4cqw**；mono px 标签仅为 chrome。
- **按度量适配：** 按标题长度定字号。整块 cap **≤ 78cqw**；≤3 词 → `display-cover`；4–6 → `display`；7+ → `headline`。7.3–9.9cqw 档留给封面 / 陈述 / 统计。
- **EB Garamond 展示为 sentence case**（非 title case，非全大写），weight 400，负字距（−0.012..−0.028em）；当一行是立场或定义时优先**斜体**。**Inter 正文** sentence case weight 400。**JetBrains Mono** kicker 全大写 0.16em 配珊瑚 ✱。无大写衬线展示、无无衬线标题、无衬线标签。

## 深度与表面

发丝线抬升：

- **1px 发丝线** 约 12% 透明度墨线边框是主要抬升（海军蓝上 cream@14%）。
- **一道柔和暖阴影**（`0 1px 3px ink@8%, 0 4px 16px ink@4%`）—— 少用，绝不厚重。
- **半阶表面** —— 奶油上的 `{colors.tile}` 块靠暖色阶差抬升，而非 cast shadow。

**上限：** 无重投影、无光晕、内容上无渐变、无倾斜。系统没有可发射的光；靠暖度与发丝线阅读。

## 形状

- **6px** 小 chrome，**8px** 卡片 / 代码面，**12px** 大卡片 / 引文框，**9999px** 仅用于真 pill。无直角、无大圆角；编辑 register 是温和圆角，绝不生硬。

## 组件

- **card-hairline** —— 编辑向内容卡片（发丝线 + 一道柔阴影）。**section-rule** —— 唯一分隔（1px，可绘入珊瑚）。
- **kicker-spike** —— ✱ 珊瑚眉题。**coral-callout** —— 唯一电压 moment（CTA / 内联链接 / 全出血色带）。
- **number-lockup** —— EB Garamond 数字 + mono 单位（PR 的 `+N / −M`、`200K`、文件数）。**pull-quote** —— EB Garamond 斜体 + cite（提交说明 / 审阅者原话）。
- **code-surface** —— 暖海军蓝代码 / 终端面；代码本体来自 **`code-*` 注册表块**，本预设只拥有表面 + mono chrome。
- **spike-mark** —— ✱ 品牌字形，始终珊瑚色。

## 帧处理（Frame Treatments）

> 配方：地面 · 容器 · 组合 · 焦点 · chrome ·  accent · Fixed/Free · 密度。
> 每帧一处珊瑚；以 kicker-spike 开场。

### 1 · 封面（identity · 手法：超大 EB Garamond · cream）

**地面** `{colors.cream}`，`slide-pad`。**组合** kicker-spike、display-cover、lead、mono-label 索引。**焦点** 珊瑚 ✱ kicker 下 2–3 行 EB Garamond `display-cover`（sentence case，ink）。**Chrome** mono 索引条（repo · branch）。**Accent** 唯一珊瑚 ✱。**Fixed** EB Garamond 400 sentence case、发丝线、cream 地面。**Free** 标题、mono 索引、版式 + 帧饱满度。**密度** 自由。

### 2 · 陈述（statement · 手法：单行 EB Garamond · cream 或 navy）

**地面** `{colors.cream}`（或 `{colors.navy}` 求庄重）。**组合** kicker-spike、display、可选 lead。**焦点** 一行 2 行 EB Garamond `display` 承载变化 —— 若是立场则用**斜体**。**Chrome** mono kicker。**Accent** 无 —— 衬线承担（或一词珊瑚）。**Fixed** sentence-case 衬线。**Free** 文案、地面、版式 + 密度。**密度** 自由。

### 3 · 代码面（code · 手法：暖海军蓝代码窗 · PR 关键帧）

**地面** `{colors.cream}` 框住 `{colors.navy}` **code-surface**（8px，cream@14% 发丝线，`navy-elev` 标题栏 + mono 文件名）。**组合** mono-label 文件名、**`code-*` 块**（code-diff / code-typing / code-snippet-_）、可选 `section-rule`。**焦点** 代码面板 —— diff / before→after / 逐字打出片段。**Chrome** mono 文件名 + 状态条。**Accent** 面板内语法 coral/teal/amber；外侧至多一处珊瑚标记（如 `+`/`−` 槽 cue）。**Fixed** 暖海军蓝面、mono 代码、发丝线。**Free** 哪个 code-_ 块、代码（来自 diff）、面板多大。**密度** 密集。

### 4 · 数字 / 冲击（data · 手法：超大数字 · cream）

**地面** `{colors.cream}`，`slide-pad`。**组合** kicker-spike、number-lockup、lead/caption、可选 `section-rule`。**焦点** EB Garamond `number-hero` 数字配 mono 单位，压 1px 规则线 —— PR 冲击（`+1,204 / −318`、`17 files`、`2.1× faster`）。**Chrome** mono 标签。**Accent** 数字 ink；至多一处珊瑚单位。**Fixed** 衬线数字 + mono 单位、发丝线规则。**Free** 数字（来自脚本）、标签、版式 + 密度。**密度** 自由。

### 5 · 引文（quote · 手法：EB Garamond 斜体 · cream）

**地面** `{colors.cream}`。**组合** kicker-spike、pull-quote、tag-upper cite。**焦点** EB Garamond **斜体** `quote-pull` —— 提交说明、审阅者原话或论点 —— 下方小字 Inter 大写 cite（author · role）。**Chrome** mono kicker。**Accent** 无，或一处珊瑚标记。**Fixed** EB Garamond 斜体引文 + 大写 cite。**Free** 引文、署名、版式 + 密度。**密度** 自由。

### 6 · 收尾 / CTA（closer · 手法：珊瑚电压 · cream 或 navy）

**地面** `{colors.cream}`（或 `{colors.navy}`）。**组合** display  sign-off、coral-callout、可选贡献者行（`assets/<login>.png` 头像 + mono 名）。**焦点** 短 EB Garamond sign-off 配唯一 **coral-callout**（CTA 或全出血色带）；「shipped-by」收尾时为一行发丝线环头像 chip。**Chrome** mono 索引。**Accent** 唯一珊瑚电压。**Fixed** 一处珊瑚、发丝线头像环、sentence-case 衬线。**Free** sign-off、谁 ship、版式 + 密度。**密度** 自由。

## 构图规则

### 应当

- 每一帧站在**暖奶油地面**上；内容聚在**半阶 tile** 面。
- 全部展示用 **EB Garamond、sentence case**、负字距；**Inter 400** 正文；**JetBrains Mono** kicker（大写、0.16em、珊瑚 ✱）+ 代码。
- **珊瑚每帧一处** —— CTA、内联链接，或全出血色带。
- 用 **1px 发丝线** + 至多一道柔和暖阴影抬升；**暖海军蓝**专留给代码/终端面。
- **一个清晰焦点**领先；用 **kicker-spike** 打开区域。按内容需要填满帧。
- 每个统计 EB Garamond 数字配 **mono 单位**；在海军蓝面上用 **`code-*` 块** 渲染代码。

### 禁止

- 无纯白、无冷灰、无纯黑；无第四种品牌色（海军蓝是结构色，语法色是装饰）。
- 无重投影、光晕、内容渐变或倾斜 —— 仅发丝线抬升。
- 无大写或 title-case EB Garamond 展示；无无衬线标题；无衬线标签；无衬线数字单位。
- 一帧内无两处珊瑚；珊瑚绝不设标题或正文跑版。
- 勿让标题超出度量 —— 降一档 ramp。

## 宽高比行为

| 处理          | 16:9                    | 9:16                        | 1:1                    |
| ------------- | ----------------------- | --------------------------- | ---------------------- |
| Cover         | display left, index top | display top, index below    | display, index corner  |
| Statement     | line left/centered      | line stacked                | centered               |
| Code Surface  | panel framed in cream   | panel taller, fewer lines   | panel centered, square |
| Number/Impact | figure left             | figure centered, taller     | centered               |
| Pull-quote    | quote left              | quote stacked               | centered               |
| Closing/CTA   | sign-off + avatar row   | sign-off top, avatars below | centered, avatars wrap |

`slide-pad` 沿短边保持；在 1.4cqw 下限之上重定展示阶梯。代码面在各比例保持发丝线 + mono chrome；头像行换行而非缩小到不可读。

## 已批准的真实实体

源文件中未定义真实客户、标识或厂商 —— 此类标记请用占位渲染。贡献者头像来自项目 `assets/<login>.png`（自 PR 人员图 staging）；✱ spike、发丝线与代码面仅 CSS，无需外部图。

## 数字与声明（硬规则）

帧尺度上绝不捏造数字、统计、diff 或计数。槽位渲染为 `— figure —`、`{metric}`、`+N / −M`。number-lockup、代码面板与冲击统计在脚本（来自 PR ingest）提供真实值之前保持占位。分支名、文件数与 `+/−` 合计追溯 diff；commit/issue 编号为 chrome。

## 渲染前自检

- **眯眼** —— 一处 EB Garamond 展示 moment 占主导。
- **三位一体** —— 奶油地面 + tile 阶 + 墨声部；珊瑚恰好一次；暖海军蓝仅在代码面；无冷灰 / 纯白 / 第四种色。
- **字体** —— EB Garamond sentence-case 展示（负字距）；Inter 400 正文；JetBrains Mono kicker（大写 0.16em，珊瑚 ✱）+ 代码；≥1.4cqw 下限。
- **深度** —— 1px 发丝线 + 至多一道柔和暖阴影；无重投影 / 光晕 / 渐变 / 倾斜；6/8/12px 圆角。
- **代码** —— 由 `code-*` 块在暖海军蓝面渲染；语法 coral/teal/amber；数字配 mono 单位。
- **捏造** —— 每个数字 / diff 追溯 PR，否则占位。

## 已知缺口

- **动效有意不在范围。** frame.md 仅规定构图。Claude 动效 register —— 短 cross-dissolve、无 overshoot/bounce/elastic、仅珊瑚「draw-on」、数字 count up、代码逐行打出 —— 在工作流的 `motion-language.md` + `hyperframes-animation`，不在本文。
- **EB Garamond + Inter + JetBrains Mono 均打包在 HyperFrames 渲染器（`@fontsource` 内嵌数据）—— 按名称离线解析，不依赖 Google Fonts。** 有意为之：此处每一款字体在干净机器或 AWS Lambda 上确定性渲染，帧无需捕获 `.woff2` 或 `@font-face`。内嵌集仅 **400 + 700 字重且无真斜体** —— 故作者展示用 **weight 400**（700 读作粗 bold，偏离 register），斜体视为浏览器合成倾斜（pull-quote register 可接受；仅当项目重度依赖时再 ship 真 EB Garamond italic `.woff2` + `@font-face`）。EB Garamond 是暖 old-style 衬线（低对比、人文）；若失败，回退 Georgia 或其他 old-style 衬线 —— 绝不用 sans。CJK：Noto Serif SC（展示）/ Noto Sans SC（正文）/ Noto Sans Mono CJK（代码）；衬线落下时 sentence-case 暖感仍可延续。
- **语法色（teal `#5DB8A6` / amber `#E8A55A` / status）为固定装饰**，在 §Colors 声明 —— **不在**可 remix 的 `colors:` 块，品牌 remix 不会重绘它们。
- **代码本体是 `code-*` 注册表块**，非本预设 —— 本预设只拥有外围暖海军蓝面 + mono chrome。
- **9:16 / 1:1 为指导**；须验证可读性下限，且各比例下 cream/tile 暖感 + 单珊瑚纪律成立。
