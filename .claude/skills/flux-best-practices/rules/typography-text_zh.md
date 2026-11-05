---
name: typography-text
description: 在 FLUX 图像中渲染文字与排版的提示词指南
---

# 排版与文字提示词

在 FLUX 图像中渲染文字的指南。排版效果最佳请使用 FLUX.2 [flex]。

## 基本语法

始终用引号标出希望渲染的确切文字：

```
A coffee shop chalkboard sign displaying "TODAY'S SPECIAL" in decorative script
```

## 核心规则

### 1. 使用引号

```
Correct: A poster with "HELLO WORLD" in bold letters
Wrong: A poster with HELLO WORLD in bold letters
```

### 2. 指定字体风格

```
"ADVENTURE" in bold sans-serif typography
"Welcome" in elegant cursive script
"CHAPTER ONE" in classic serif typeface
"CODE" in monospace terminal font
"SALE!" in decorative display lettering
```

### 3. 描述字号层级

```
Large headline "BREAKING NEWS" above smaller subtext "Details inside"
```

### 4. 说明位置

```
"OPEN" sign centered in storefront window
"EXIT" text positioned above doorway
"Page 1" in bottom right corner
```

### 5. 文字描述前置

将文字相关描述放在提示词靠前位置，可提高准确度：

```
Good: A sign reading "FRESH BREAD" in a bakery window...
Less Good: A bakery window with a sign that says "FRESH BREAD"...
```

## 字体风格类别

### 无衬线（Sans-Serif，现代/简洁）
```
"MINIMAL" in clean geometric sans-serif, Swiss modernist style
"TECH SUMMIT" in bold condensed grotesque typeface
"future" in thin uppercase sans-serif, contemporary design
```

### 衬线（Serif，经典/优雅）
```
"The New Yorker" in traditional serif typeface, editorial masthead
"LUXURY" in high-contrast Didone serif with thin/thick strokes
"Wisdom" in old-style serif with subtle bracketed serifs
```

### 手写体/草书（Script/Cursive，装饰性）
```
"With Love" in flowing calligraphic script with flourishes
"Signature" in connected brush script, casual elegance
"Romance" in formal copperplate script, wedding invitation style
```

### 展示/装饰体（Display/Decorative）
```
"ROCK CONCERT" in distressed vintage concert poster lettering
"CIRCUS" in ornate Victorian display type with decorative elements
"RETRO" in 1970s rounded bubble letters
```

### 手写风格（Handwritten）
```
"Note to self" in casual handwritten style, slightly imperfect
"Thanks!" in quick marker pen handwriting
"ideas" in sketchy pencil handwriting
```

### 等宽（Monospace）
```
"CODE_COMPLETE" in terminal monospace, developer aesthetic
"SYSTEM" in typewriter monospace, vintage tech
"DEBUG" in LCD-style digital monospace
```

## 文字效果

### 霓虹灯牌
```
Glowing neon sign spelling "OPEN 24/7" in pink neon tubes with
blue outline, slight glow and reflection, night scene
```

### 金属/立体
```
"GOLD" in three-dimensional metallic gold letters with realistic
reflections and subtle shadows, luxury aesthetic
```

### 压印/凹印
```
"PREMIUM" embossed into leather surface, subtle shadows showing
the raised letterforms
```

### 描边
```
"MODERN" in outline-only letters, no fill, thin white stroke
on dark background
```

### 渐变文字
```
"SUMMER" with gradient fill from #FF6B6B (coral) at top to
#4ECDC4 (teal) at bottom
```

## 多文字组合

### 海报设计
```
Event poster with "SUMMER FEST 2025" as large headline in bold
condensed sans-serif at top, "JULY 15-17" as medium subheading
in regular weight, "Central Park, NYC" as small body text at
bottom, all in white text on #FF6B35 (sunset orange) background
```

### 书籍封面
```
Book cover design: "THE GREAT GATSBY" in elegant art deco gold
lettering centered in upper third, author name "F. SCOTT FITZGERALD"
in smaller gold caps below, #1A1A2E (midnight blue) background
with geometric gold accents
```

### 杂志封面
```
Fashion magazine cover with "VOGUE" in classic serif masthead at top,
cover line "SPRING COLLECTION" in bold sans-serif, "The New Rules of Style"
in lighter weight italic, all in white against dramatic portrait
```

### 招牌标识
```
Vintage diner sign: "MEL'S DINER" in red neon script lettering,
"OPEN" below in separate green neon block letters, chrome border,
1950s Americana aesthetic
```

### 名片
```
Minimalist business card with "JOHN SMITH" in medium weight sans-serif,
"Creative Director" in lighter weight below, contact details in small
type at bottom, #2C3E50 (dark blue) text on white background
```

## 文字布局策略

### 居中构图
```
Centered text layout: "WELCOME" in large caps at center,
perfectly balanced with equal margins
```

### 左对齐
```
Left-aligned text block: "Company Name" as header,
"Tagline goes here" below, flush left alignment
```

### 沿路径文字
```
"GOING IN CIRCLES" text following a circular path around
the center of the design
```

### 文字叠加
```
"ADVENTURE AWAITS" in bold white text overlaid on landscape
photograph, positioned in lower third with slight shadow for readability
```

## [flex] 的技术考量

### Steps 参数
- 较高 steps（30–50）= 文字质量更好
- 较低 steps（10–20）= 更快，质量较低

### Guidance 参数
- 较高 guidance（6–10）= 更严格遵循提示词
- 较低 guidance（1.5–4）= 更具创意、解读更自由

### 推荐设置
```
For clean typography: steps=50, guidance=7
For artistic text: steps=30, guidance=4
```

## 故障排查

### 拼写错误
- 文字尽量简短（1–4 个词效果最佳）
- 尽量使用常见词汇
- 在提示词中重复写出确切文字

### 文字难以辨认
- 指定更大的字号
- 使用更简单的字体（无衬线）
- 确保与背景对比度足够
- 使用 [flex] 模型

### 字体风格不对
请写得更具体：
```
Instead of: "text in a nice font"
Use: "text in bold geometric sans-serif similar to Futura"
```

### 文字未出现
- 在提示词中前置文字描述
- 用引号包住文字
- 指定确切位置
- 降低提示词中其他内容的复杂度
