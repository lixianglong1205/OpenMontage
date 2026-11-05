---
version: alpha
name: BlockFrame — Frame (video / frame layer)
description: >
  BlockFrame design.md 的视频优先配套文档。基本单位是帧（1920×1080）。原子元素一致且不可违背 ——
  4px 黑色描边 + 8px 硬偏移阴影、五种粉彩糖果色（粉/蓝/绿/黄/奶油）外加黑/白/米白、Inter 800–900
  大写展示字 + Space Grotesk 标签装饰、直角、label-pill、倾斜装饰、星形_burst、条纹块、点阵网格。
  构图与帧尺度已重写。动效不在范围内。
unit: the frame — 1920×1080 primary; 9:16 and 1:1 documented
principle: atoms are sacred · composition is free · numbers come from the script

colors:
  black: "#000000"
  white: "#FFFFFF"
  offwhite: "#FFFDF5"
  pink: "#FE90E8"
  blue: "#C0F7FE"
  green: "#99E885"
  yellow: "#F7CB46"
  cream: "#FFDC8B"

borders: { primary: "4px solid black", thin: "3px solid black" }
shadows: { default: "8px 8px 0 black", small: "4px 4px 0 black", hover: "6px 6px 0 black", close-yellow: "12px 12px 0 yellow", close-white: "6px 6px 0 white" }

typography:
  # — reading + chrome ramp —
  body:    { fontFamily: "Inter", cqw: 0.95, weight: 500, lineHeight: 1.6 }
  card-title:{ fontFamily: "Inter", cqw: 1.15, weight: 700, upper: true, lineHeight: 1.2 }
  label:   { fontFamily: "Space Grotesk", px: 13, weight: 600, tracking: "0.08em", upper: true }
  counter: { fontFamily: "Space Grotesk", px: 14, weight: 700, tracking: "0.1em", upper: true }
  # — display ramp (Inter 800–900, uppercase, negative tracking) —
  heading-md:{ fontFamily: "Inter", cqw: 2.1, weight: 700, lineHeight: 1.1, tracking: "-0.01em", upper: true }
  quote-text:{ fontFamily: "Inter", cqw: 2.7, weight: 900, lineHeight: 1.15, tracking: "-0.02em", upper: true }
  stat-number:{ fontFamily: "Inter", cqw: 3.3, weight: 900, lineHeight: 1.0 }
  heading-lg:{ fontFamily: "Inter", cqw: 3.3, weight: 800, lineHeight: 1.0, tracking: "-0.02em", upper: true }
  close-title:{ fontFamily: "Inter", cqw: 4.2, weight: 900, lineHeight: 0.95, tracking: "-0.03em", upper: true }
  heading-xl:{ fontFamily: "Inter", cqw: 5.0, weight: 900, lineHeight: 0.95, tracking: "-0.03em", upper: true }

spacing:
  slide-pad: "3.1cqw"   # 60px @1920
  gap-md: "1.7cqw"

components:
  card-elevated:
    backgroundColor: "{colors.white}"
    border: "0.4cqw solid {colors.black}"
    rounded: "0"
    shadow: "0.8cqw 0.8cqw 0 {colors.black}"
    description: "主卡片。描边/阴影成对：4px↔8px，3px↔4px。"
  card-small:
    backgroundColor: "{colors.white}"
    border: "0.3cqw solid {colors.black}"
    rounded: "0"
    shadow: "0.4cqw 0.4cqw 0 {colors.black}"
    description: "统计卡片、团队卡片、时间线步骤。"
  label-pill:
    border: "0.3cqw solid {colors.black}"
    backgroundColor: "any pastel / {colors.white}"
    rounded: "9999px"
    shadow: "0.4cqw 0.4cqw 0 {colors.black}"
    typography: "{typography.label}"
    description: "通用眉标 —— 绝不用纯文本。"
  button-primary:
    backgroundColor: "{colors.yellow}"
    textColor: "{colors.black}"
    border: "0.3cqw solid {colors.black}"
    rounded: "0"
    shadow: "0.4cqw 0.4cqw 0 {colors.black}"
    typography: "Inter 700"
    description: "主行动按钮（CTA）。"
  star-burst:
    backgroundColor: "any pastel"
    border: "0.3cqw solid {colors.black}"
    clip: "10-point clip-path star"
    description: "角落吸睛元素。"
  stripe-block:
    backgroundImage: "45° {colors.black} + pastel diagonal stripes"
    border: "0.3cqw solid {colors.black}"
    description: "海报装饰。"
  bg-dot-grid:
    backgroundImage: "radial-dot ~1.2px dots, 24px grid, {colors.black}"
    description: "淡淡的角落/底面叠加。"
  tilt-deco:
    transform: "rotate(±2°–12°)"
    description: "旋转矩形/徽章/星形。统计卡片交替 −2/+2°。刺破网格的标志性手法。"
  stat-deco-dot:
    backgroundColor: "any pastel"
    border: "2px solid {colors.black}"
    rounded: "50%"
    size: "12px"
    description: "唯一的圆形，固定在统计卡片上。"
  close-frame:
    backgroundColor: "{colors.black}"
    textColor: "{colors.white}"
    border: "0.4cqw solid {colors.white}"
    rounded: "0"
    shadow: "1.2cqw 1.2cqw 0 {colors.yellow}"
    description: "反色收尾 —— 唯一带彩色阴影。"
---

# BlockFrame — Frame（视频 / 帧层）

## 概述

BlockFrame 在帧尺度上是一套**极繁新粗野主义（maximalist neobrutalist）**系统，遵循五条法则：每个区域都有
4px 黑色描边，每个抬升元素都有 8px 硬偏移阴影，每个角都是直角，每个强调色都是饱和粉彩，每个版式都可以略歪一点。乐趣来自
刻意的碰撞 —— 带描边的卡片彼此相接、阴影叠压、倾斜装饰刺破网格。

声线由 **Inter** 800–900 字重、紧排大写、负字距（展示）+ 500 字重正文句读，以及 **Space Grotesk** 600 字重、大写、0.08em 字距的标签/装饰声线构成。五种糖果粉彩（粉/蓝/绿/黄/奶油）在各帧间循环作为满铺底色 ——
色彩轮换是主要节奏。深度来自**硬偏移阴影**（8px/4px、纯黑、零模糊、右下）；close-frame 的 12px 黄色阴影是唯一彩色例外。

**帧尺度的关键特征：**

- **4px 黑描边 + 8px 硬阴影**用于主卡片；装饰件为 3px + 4px（权重成对）。
- **五种粉彩**循环作满铺底色；黑/白/米白为结构色。
- **Inter 800–900 大写**、负字距展示；**Space Grotesk** 标签装饰。
- **直角** everywhere（仅 stat-deco dot 为圆）；**倾斜装饰**刺破网格。
- **label-pill** 开启每个区域；星形_burst、条纹块、点阵为可复用吸睛单元。
- **适度密集** —— 满铺显得权威；空角显得残缺。

## 帧（The Frame）

### 帧工艺条（Frame Craft Bar）

三道肉眼检验在任何结构性检查之前把关每一帧：

- **眯眼（Squint）** —— 一处 Inter 展示瞬间在 3–6× 邻域内占主导；卡片读成系统，而非互抢。
- **留白（Silence）** —— 封面/引用/收尾保留气口（装饰，非内容）；**功能卡片与统计网格是刻意密集的例外**。
- **克制（Restraint）** —— 4px→8px / 3px→4px 成对关系成立；仅黑描边（收尾为白）；粉彩底色**每帧轮换一种**；无第六种粉彩。
- **参照（Reference）** —— 对标**杂志/zine、1990 年代贴纸书、玩具包装 spread**（带框块、倾斜装饰）；失败样像是**扁平、无描边、模糊阴影的网页卡片网格**。

- **主比例：** 1920×1080（16:9）。展示尺寸用 **`cqw`** 编写（`px ÷ 1920 × 100 = cqw`）。
- **竖版：** 1080×1920（9:16）。**方形：** 1080×1080（1:1）。
- **安全区：** `slide-pad` 约 3.1cqw；装饰可出血至边缘。

**容器法则（承重）。** 每一帧底色设置 `container-type: size`；所有
帧相对单位均为相对它的 `cqw`/`cqh` —— 绝不用 `vw`。描边/阴影用 `cqw` 缩放，使
4px↔8px 成比例成立；角保持直角。

## 色彩

令牌与源文档一致。`{colors.offwhite}` 为默认底色，但各帧**轮换**
`{colors.cream}`/`blue`/`pink`/`green`/`yellow` 底色 —— 轮换即节奏。
`{colors.black}` 用于所有描边 + 结构文本；`{colors.white}` 为卡片填充。五种粉彩
可互换、**无语义绑定** —— 靠并置搭配（粉+蓝+绿 trio、
奶油+黄暖色对）。`{colors.yellow}` 用于 CTA + 唯一彩色（收尾）阴影；
`{colors.black}` 底色用于收尾面。**无第六种粉彩。**

## 字体

两条 ramp。**阅读/装饰 ramp**（Inter 正文 0.95cqw 500、Space Grotesk 标签用 px）
承载文案 + 装饰；**展示 ramp**（Inter `heading-md` 2.1cqw → `heading-xl` 5cqw，800–900 大写）
承载所有标题 + 统计数字。

- **可读下限：** 任何承重行 ≥ **1.4cqw**；px 标签仅作装饰。
- **按量适配：** 按标题长度定字号。整块上限 **≤ 78cqw**；≤3 词 → `heading-xl`；4–6 → `heading-lg`；7+ → `heading-md`。
- **Inter 展示为大写、800–900、负字距**（−0.01..−0.03em）；正文 500 句首大写；**Space Grotesk 标签大写 0.08em**。禁止句首大写展示、禁止无字距展示。

## 深度与表面

硬偏移阴影、纯黑、零模糊、右下：

- **0.8cqw（8px）** 主卡片；**0.4cqw（4px）** 装饰；**0.6cqw（6px）** 悬停。
- **描边深度** —— 4px/3px 描边承担大量抬升感；阴影使其「浮起」。
- **倾斜** —— ±2°–12° 旋转打破网格以感知维度。
- **反色收尾** —— 12px 黄色阴影（close-btn 上 6px 白）—— 唯一彩色阴影。

**上限：** 无模糊阴影、无圆角（stat-deco dot 除外）、无渐变深度。

## 形状

- **处处 0 圆角**，除 12px stat-deco dot（50%）。直角是结构身份。

## 组件

- **card-elevated / card-small** —— 带描边+阴影的内容卡片（权重成对）。
- **label-pill** —— 通用眉标（描边+阴影+粉彩）。**button-primary** —— 黄色 CTA。
- **star-burst / stripe-block / bg-dot-grid / tilt-deco** —— 可复用装饰单元（每帧至少 1 个）。
- **stat-deco-dot** —— 唯一圆形。**close-frame** —— 反色黑+白+黄阴影收尾。

## 帧处理（Frame Treatments）

> 配方：底色 · 容器 · 组合 · 焦点 · 装饰 · 强调 · 留白 · 固定/自由 · 密度。
> 轮换底色；每帧 ≥1 装饰；以 label-pill 开场。

### 1 · 封面（身份 · 动势：装饰刺破 · 左对齐）

**底色** `{colors.cream}`（或 offwhite）+ 淡点阵。**组合** label-pill、heading-xl、tilt-deco 矩形、star-burst、counter。**焦点** 2–3 行 Inter `heading-xl` 大写、左对齐、位于 label-pill 下；右侧倾斜粉彩矩形 + 星形_burst 刺破。**装饰** counter pill。**强调** 装饰的粉彩。**留白** 右三分之一留给装饰。**固定** 4px/8px 成对、大写展示、直角。**自由** 标题、装饰位置/色。**密度** 舒适。

### 2 · 功能卡片（目录 · 动势：三列带框网格 · 蓝底）

**底色** `{colors.blue}`，`slide-pad`。**组合** label-pill、heading-lg、3× card-elevated（icon-square + card-title + body）。**焦点** 三张白底带框+阴影卡片。**装饰** label-pill 眉标。**强调** 粉彩 icon-square（粉/绿/黄）。**留白** 紧 —— 刻意密集。**固定** 4px 描边 + 8px 阴影、直角、大写 card-title。**自由** 卡片内容、图标色相。**密度** 密集例外。

### 3 · 统计网格（数据 · 动势：倾斜统计卡 · 绿底）

**底色** `{colors.green}`，`slide-pad`。**组合** label-pill、heading-lg、3× card-small（倾斜 −2/+2°、stat-deco dot、stat-number + label）。**焦点** 三张倾斜带框统计卡。**强调** deco-dot 粉彩 + 黑色统计数字。**留白** 适中。**固定** 交替倾斜、3px+4px、仅 deco-dot 为圆。**自由** 数字（来自脚本）、dot 色相。**密度** 密集例外。

### 4 · 收尾板（Closer · 动势：反色黑 · 居中）

**底色** `{colors.black}`。**组合** close-frame（4px 白描边、12px 黄阴影）、label-pill（反色）、close-title、star-burst。**焦点** 白描边框内白色 `close-title`，带黄色偏移阴影；粉星刺破一角。**强调** 黄阴影 + 粉星。**留白** 约 50%。**固定** 白上黑、12px 黄阴影（仅此处）、直角。**自由** 结语、星位。**密度** 低。

### 5 · 引用（Quote · 动势：带框引用 · 粉底）

**底色** `{colors.pink}`（或 offwhite）。**组合** label-pill、card-elevated 内 quote-text、署名。**焦点** 白底带框+阴影框内 Inter `quote-text`（900 大写）。**强调** 底色 + 一处装饰。**留白** 适中。**固定** 大写引用、4px/8px。**自由** 引文、底色。**密度** 舒适。

### 6 · 时间线（流程 · 动势：阶梯带框卡 · offwhite）

**底色** `{colors.offwhite}`。**组合** label-pill、heading-lg、3–4 张 card-small 步骤 + step-connectors。**焦点** 一行带框步骤卡，黑连接条串联，每步一粉彩 + step-num。**强调** 步骤粉彩。**留白** 适中。**固定** 3px+4px 步骤、直角、连接器。**自由** 步骤、色相。**密度** 标准。

## 构图规则

### 应当（Do）

- **4px 描边配 8px 阴影**、**3px 配 4px** —— 成对关系不可协商。
- **轮换粉彩底色**跨帧；保持 deck 视觉节奏。
- Inter 展示设**大写、800–900、负字距**；每个区域以 **label-pill** 开场。
- 阴影**纯黑、零模糊、右下**；每帧 **≥1 装饰**（倾斜/星/条纹/点）。
- **黄色**用于 CTA；收尾用 **反色黑 + 12px 黄阴影** close-frame。
- 装饰倾斜 ±2°–12°；多数帧左倾。

### 禁止（Don't）

- 无圆角（stat-deco dot 除外）；无模糊阴影。
- 无彩色描边（仅黑，收尾白除外）；无第六种粉彩。
- 无句首大写 Inter 展示；无无字距展示；标签不得为纯文本。
- 勿一切完美对齐（倾斜是签名）；勿留空角。
- 勿标题撑满边缘 —— 按量适配。

## 宽高比行为

| 处理类型     | 16:9                          | 9:16                         | 1:1                      |
| ------------- | ----------------------------- | ---------------------------- | ------------------------ |
| 封面         | 标题左、装饰右 | 标题上、装饰下 | 标题，装饰更少 |
| 功能卡片                      | 3 列横排                      | 3 列竖叠                    | 2+1                      |
| 统计网格     | 3 张倾斜横排               | 3 张倾斜竖叠             | 2×2                      |
| 收尾       | 居中 close-frame          | 居中、更高             | 居中                 |
| 引用         | 引用框                   | 引用竖排                | 居中                 |
| 时间线      | 水平步骤              | 垂直（连接器隐藏） | 2×2                      |

短边保留 `slide-pad`；在 1.4cqw 下限之上重设展示尺寸。更紧比例时减少装饰数量，使帧保持带框而非杂乱。

## 已批准实体

源文档未定义真实客户、Logo 或供应商 —— 此类标记一律渲染为
占位。粉彩填充、装饰与倾斜与具体内容无关。

## 数字与主张（硬规则）

帧尺度上绝不编造数字、统计或计数。槽位渲染为 `— figure —`、`{metric}`、
`N×`。统计卡与图表在脚本提供数值前使用占位。幻灯片计数与列表编号为装饰性。

## 渲染前自检

- **眯眼** —— 一处 Inter 展示占主导；卡片读成系统。
- **留白** —— 仅功能/统计网格密集；封面/引用/收尾以装饰保气口。
- **描边/阴影** —— 4px↔8px / 3px↔4px 成对；纯黑、零模糊。
- **色彩** —— 粉彩底色轮换；仅黑描边（收尾白）；无第六粉彩。
- **字体** —— Inter 大写 800–900 负字距、按量适配；Space Grotesk 标签 0.08em；≥1.4cqw 下限。
- **形状** —— 直角（仅 stat-deco dot 圆）；每帧 ≥1 倾斜/装饰。
- **编造** —— 每个数字可追溯到脚本，否则占位。

## 已知缺口

- **动效刻意不在范围内。** frame.md 仅规定构图；源文档通过 display 切换幻灯片，无过渡。
- **Inter + Space Grotesk 经 Google Fonts。** CJK：Noto Sans SC 900（句首大写 —— 大写信号减弱）；更依赖描边/阴影/装饰承载粗野身份。
- **9:16 / 1:1 为指导**；验证下限及装饰数量随比例缩减。
- 星形_burst（clip-path）、条纹块、点阵与倾斜纯 CSS；无需外部图像。
