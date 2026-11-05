# paper.design 连接器

将 `visual-style.md` 应用于 paper.design 文档。

## 概述

paper.design 是用于创建用户界面的专业设计工具。本连接器将 `visual-style.md` 中的字段映射到 paper.design 的文档默认值与 AI 布局指导。

## 字段映射

| visual-style.md 字段 | paper.design 用途 |
|-----------------------|-------------------|
| `colors.primary` | 文档调色板（主色） |
| `colors.accent` | 文档调色板（强调色） |
| `colors.neutral` | 文档调色板（中性色） |
| `typography.display.family` | 默认展示字体 |
| `typography.body.family` | 默认正文字体 |
| `typography.caption.family` | 默认说明文字字体 |
| `style_prompt_full` | AI 布局建议提示词 |
| `mood.keywords` | 设计方向关键词 |
| `mood.avoid` | 设计约束检查清单 |
| `assets.reference_images` | 风格板参考 |
| `layout.grid` | 画板网格系统 |
| `layout.alignment` | 默认对齐规则 |

## 应用风格

### 1. 设置调色板

创建新画板时，应用风格中的颜色：

```
Background: colors.primary[0].hex
Text: colors.primary[1].hex
Accent elements: colors.accent[0].hex
Secondary elements: colors.neutral[0].hex
```

### 2. 配置 typography

加载指定字体并设置默认值：

```
Display/Headlines: typography.display.family, typography.display.weight
Body text: typography.body.family, typography.body.weight
Labels/Captions: typography.caption.family, typography.caption.weight
```

### 3. 应用布局规则

按 `layout.grid` 组织画板结构：

- "12 columns" → 设置 12 列网格
- "Strict modular grid" → 启用网格吸附
- "Flush left" → 所有文本块左对齐

### 4. 使用 style_prompt_full 作为 AI 指导

在 paper.design 中使用 AI 功能时，在提示词中包含 `style_prompt_full`：

```
Create a landing page hero section.

Visual style:
[PASTE style_prompt_full HERE]

Constraints:
[ITEMS FROM mood.avoid]
```

## 示例：应用瑞士风格

给定 `mueller-brockmann-swiss.visual-style.md`：

**颜色设置：**
- Background: `#000000` (Pure Black)
- Text: `#FFFFFF` (Pure White)
- Accent: `#0066FF` (Electric Blue)
- Grid lines: `#CCCCCC` (Grid Gray)

**Typography：**
- All text: Helvetica family
- Headlines: Helvetica Bold, uppercase
- Body: Helvetica Regular, flush left
- Captions: Helvetica Light, small, uppercase

**布局：**
- 12 列模块化网格
- 所有元素吸附到网格
- 不使用居中文本
- 在正交结构内采用强对角线构图

**设计约束（来自 mood.avoid）：**
- 无有机或曲线形状
- 无渐变
- 无图库摄影
- 无圆角
- 无装饰性元素

## 工作流

1. **阅读风格** — 加载 `visual-style.md` 文件
2. **创建画板** — 按 `layout.aspect_ratio` 设置尺寸
3. **应用背景** — 使用 `colors.primary[0].hex`
4. **设置网格** — 遵循 `layout.grid` 规范
5. **配置字体** — 加载 `typography.*` 字体族
6. **构建内容** — 按 `mood.keywords` 把握方向
7. **审查** — 对照 `mood.avoid` 约束检查

## 设计简报格式

在 paper.design 中开始新设计时，从风格生成简报：

```markdown
## Design Brief

**Style:** [name]

**Color Palette:**
- [colors.primary[0].name]: [hex] — [role]
- [colors.primary[1].name]: [hex] — [role]
- [colors.accent[0].name]: [hex] — [role]

**Typography:**
- Display: [typography.display.family] [weight]
- Body: [typography.body.family] [weight]

**Layout:** [layout.grid], [layout.alignment]

**Mood:** [mood.keywords joined]

**Avoid:** [mood.avoid joined]
```

## 提示

- **从网格开始** — 在放置元素前先设置 `layout.grid`
- **Typography 优先** — 用 `typography.rules` 指导层级决策
- **定期核对约束** — 设计过程中参考 `mood.avoid`
- **使用参考图** — 若 `assets.reference_images` 含 URL，导入为风格板
