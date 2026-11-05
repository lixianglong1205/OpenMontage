# visual-style.md 格式规范

**版本：** 1.0
**状态：** 草案

## 概述

`visual-style.md` 文件是一种带 YAML frontmatter 的 Markdown 文档，用于定义完整的视觉设计系统。该格式旨在：

- **人类可读** — 可在任意文本编辑器中理解
- **AI 可消费** — 每个字段均可直接被 AI 模型使用
- **可移植** — 适用于任何读取该格式的工具

## 文件结构

```
---
[YAML frontmatter]
---

[Markdown 正文章节]
```

## 必填字段

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `name` | string | 风格的显示名称 |
| `version` | string | 规范版本（当前为 `1.0`） |
| `style_prompt_short` | string | 一两句话的电梯演讲式摘要 |
| `style_prompt_full` | string | 完整的自然语言生成提示 — **最重要的字段** |
| `colors.primary` | array | 至少 2 种颜色，每种含 `name`、`hex`、`role` |

## 可选字段

### 元数据

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `tags` | array | 分类标签（例如 "iconic design"、"retro tech"） |
| `author` | string | 风格创建者署名 |
| `source_url` | string | 提取该风格的来源 URL |
| `created` | string | ISO 日期（YYYY-MM-DD） |

### 颜色

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `colors.accent` | array | 强调色，含 name/hex/role |
| `colors.neutral` | array | 中性色，含 name/hex/role |

**颜色对象 schema：**
```yaml
- name: "Descriptive Name"
  hex: "#RRGGBB"
  role: "how this color is used in the system"
```

### 字体排版

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `typography.display` | object | 展示/标题字体排版 |
| `typography.body` | object | 正文字体排版 |
| `typography.caption` | object | 说明/标签字体排版 |
| `typography.rules` | array | 字体排版规则与约束 |

**Typography 对象 schema：**
```yaml
display:
  family: "Font Family Name"
  weight: "bold"
  style: "uppercase, tight tracking"
```

### 布局

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `layout.grid` | string | 网格系统描述 |
| `layout.alignment` | string | 对齐方式 |
| `layout.aspect_ratio` | string | 默认宽高比（例如 "16:9"） |
| `layout.notes` | array | 其他布局指南 |

### 动效

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `motion.transitions` | array | 使用的转场类型 |
| `motion.animation_style` | string | 整体动画风格 |
| `motion.pacing` | string | 节奏/时序描述 |
| `motion.audio_cues` | array | 声音设计说明 |

### 氛围

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `mood.keywords` | array | 氛围/情绪关键词 |
| `mood.era` | string | 时代参考 |
| `mood.cultural_reference` | string | 文化/历史语境 |
| `mood.avoid` | array | **反模式** — 明确应避免的内容 |

### 资源

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `assets.reference_images` | array | 参考图 URL |
| `assets.gsep_elements` | array | 叠加/图形元素 URL |
| `assets.html_snippets` | array | HTML 组件示例 URL |
| `assets.color_palette_image` | object | 色板可视化 URL |

**重要：** 资源始终为 URL，从不嵌入二进制数据。

### 扩展

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `x_*` | object | 带命名空间的工具专用扩展 |

示例：
```yaml
x_heygen:
  video_id: "abc123"
  orientation: "landscape"

x_figma:
  library_id: "xyz789"
```

## Markdown 正文章节

在 YAML frontmatter 之后，可包含以下可选 Markdown 章节：

### `## Connectors`

工具特定的转换说明：

```markdown
## Connectors

### HeyGen Video Agent
Feed `style_prompt_full` as the visual style block. Use `motion.transitions`
for scene cuts. Orientation: landscape.

### HTML Slides
Map colors to CSS variables. Use `typography.display` for h1-h3.
```

### `## Design Principles`

自由形式的设计哲学：

```markdown
## Design Principles

Typography drives hierarchy. Color is used sparingly and intentionally.
Every element snaps to a baseline grid. White space is a feature.
```

### `## Extraction Notes`

来源文档（从外部提取时）：

```markdown
## Extraction Notes

Extracted from https://example.com on 2026-03-12.
Primary colors sampled from hero section.
Typography identified via browser dev tools.
```

## 完整示例

```yaml
---
name: "Josef Müller-Brockmann Swiss International Style"
version: "1.0"
tags:
  - iconic design
  - sleek minimal
author: "Bin"
source_url: ""
created: "2026-03-12"

style_prompt_short: >
  Grid-locked Swiss precision. Black and white base with electric blue
  accent. Helvetica only. Data visualizations as hero elements.

style_prompt_full: >
  Josef Müller-Brockmann Swiss International Style. Grid-locked layouts
  with mathematical precision. Black and white base with ONE accent color
  (electric blue #0066FF). Strong diagonal compositions. Helvetica
  typography only. Data visualizations are the hero — animated charts,
  counters, grids. Every frame snaps to a grid. Transitions are horizontal
  grid wipes. No organic shapes. No gradients. No stock photography.
  Everything is geometric, systematic, precise.

colors:
  primary:
    - name: "Pure Black"
      hex: "#000000"
      role: "dominant ground, text, structural elements"
    - name: "Pure White"
      hex: "#FFFFFF"
      role: "background fields, negative space"
  accent:
    - name: "Electric Blue"
      hex: "#0066FF"
      role: "the ONE accent — data highlights, key emphasis"
  neutral:
    - name: "Grid Gray"
      hex: "#CCCCCC"
      role: "grid lines, secondary structure"

typography:
  display:
    family: "Helvetica"
    weight: "bold"
    style: "uppercase or sentence case, tight tracking"
  body:
    family: "Helvetica"
    weight: "regular"
    style: "flush left, ragged right, generous leading"
  caption:
    family: "Helvetica"
    weight: "light"
    style: "small, uppercase, wide tracking"
  rules:
    - "Helvetica ONLY — no other typeface"
    - "Type sizes follow a mathematical scale"
    - "Always flush left — never centered"

layout:
  grid: "Strict modular grid — 12 columns"
  alignment: "Flush left, grid-snapped"
  aspect_ratio: "16:9"
  notes:
    - "Every element locked to the grid"
    - "Data visualizations are the hero elements"

motion:
  transitions:
    - "horizontal grid wipes"
    - "elements snapping to grid positions"
    - "clean hard cuts"
  animation_style: >
    Geometric precision. Elements snap to grid positions.
    Charts animate systematically. Nothing bounces.
  pacing: "Measured, confident, unhurried"

mood:
  keywords:
    - "precise"
    - "systematic"
    - "authoritative"
    - "geometric"
  era: "1950s–1970s (timeless)"
  cultural_reference: "Müller-Brockmann, Grid Systems in Graphic Design"
  avoid:
    - "organic or curved shapes"
    - "gradients"
    - "stock photography"
    - "centered text"
    - "decorative elements"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""
---

## Design Principles

Typography and the grid are the only design elements needed.
Mathematical relationships create visual harmony.
Restraint is the ultimate sophistication.

## Connectors

### HeyGen Video Agent
Use `style_prompt_full` verbatim. No avatar, no b-roll — pure motion graphics.
Hard cuts between scenes.

### HTML Slides
Map to CSS: `--color-bg: #000`, `--color-text: #FFF`, `--color-accent: #0066FF`.
Use Helvetica via system fonts or Google Fonts equivalent.
```

## 校验

有效的 `visual-style.md` 必须满足：

1. 在 `---` 分隔符之间有合法的 YAML frontmatter
2. 包含所有必填字段
3. `colors.primary` 至少包含 2 个颜色对象
4. 每个颜色对象包含 `name`、`hex` 和 `role`
5. `version` 设为 `1.0`

## 版本管理

`version` 字段指规范版本，而非风格本身的版本。当规范变更时：

- **次要变更**（新增可选字段）：版本保持 `1.0`
- **破坏性变更**（必填字段变更）：版本递增至 `2.0`

## 设计决策

### 为何 `style_prompt_full` 为必填

许多 AI 工具只接受文本提示。通过要求完整、自然语言的风格描述，我们确保每个 `visual-style.md` 文件都能被任意工具立即使用 — 即使该工具不解析结构化字段。

### 为何不嵌入二进制数据

URL 使文件保持小巧、可版本化且可移植。二进制资源应托管在外部并通过 URL 引用。

### 为何使用 `x_*` 命名空间

不同工具有不同能力。`x_` 前缀允许工具专用配置，而不污染核心 schema。示例：`x_heygen`、`x_figma`、`x_paper`。

### 为何有 `mood.avoid`

否定约束与肯定约束同样重要。告诉 AI **不要做什么**，往往比告诉它做什么更有效。
