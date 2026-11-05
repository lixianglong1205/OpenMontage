# Figma 连接器

将 `visual-style.md` 应用于生成 Figma 样式与组件。

## 概述

本连接器将 `visual-style.md` 中的字段映射到 Figma 的样式体系：颜色样式、文本样式、效果样式与布局网格。

## 字段映射

| visual-style.md 字段 | Figma 输出 |
|-----------------------|--------------|
| `colors.primary` | 颜色样式（`brand/primary`、`brand/secondary`） |
| `colors.accent` | 颜色样式（`accent/primary`、`accent/secondary`） |
| `colors.neutral` | 颜色样式（`neutral/100`、`neutral/200` 等） |
| `typography.display` | 文本样式（`heading/display`） |
| `typography.body` | 文本样式（`body/default`、`body/large`） |
| `typography.caption` | 文本样式（`label/default`、`label/small`） |
| `typography.rules` | 设计评审清单 |
| `layout.grid` | 布局网格预设 |
| `layout.aspect_ratio` | 画框尺寸 |
| `mood.avoid` | 设计评审清单 |
| `assets.reference_images` | 风格指南画框 |

## 颜色样式

根据 `colors` 对象生成 Figma 颜色样式：

```
Folder: brand/
  - brand/black         → colors.primary[0].hex
  - brand/white         → colors.primary[1].hex

Folder: accent/
  - accent/primary      → colors.accent[0].hex
  - accent/secondary    → colors.accent[1].hex (if exists)

Folder: neutral/
  - neutral/light       → colors.neutral[0].hex
  - neutral/dark        → colors.neutral[1].hex
```

**命名规范：** 使用 `role` 字段作为样式描述。

## 文本样式

根据 `typography` 生成 Figma 文本样式：

```
Folder: heading/
  - heading/display
    Font: typography.display.family
    Weight: typography.display.weight
    Size: 48px (or derive from style)

Folder: body/
  - body/default
    Font: typography.body.family
    Weight: typography.body.weight
    Size: 16px

Folder: label/
  - label/default
    Font: typography.caption.family
    Weight: typography.caption.weight
    Size: 12px
```

## 布局网格

根据 `layout.grid` 生成布局网格预设：

```
"12 columns" →
  Columns: 12
  Type: Stretch
  Margin: 64px
  Gutter: 24px

"8-point grid" →
  Rows: Count
  Height: 8px

"Strict modular grid" →
  Both columns AND rows enabled
```

## 风格指南画框

创建一个用于记录设计体系的风格指南画框：

```
┌─────────────────────────────────────────────────────┐
│  [name]                                             │
│  [style_prompt_short]                               │
├─────────────────────────────────────────────────────┤
│  COLORS                                             │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                │
│  │████│ │████│ │████│ │████│ │████│                │
│  └────┘ └────┘ └────┘ └────┘ └────┘                │
│  Primary  Secondary  Accent   Neutral              │
├─────────────────────────────────────────────────────┤
│  TYPOGRAPHY                                         │
│                                                     │
│  Display Heading                                    │
│  [typography.display.family] [weight]               │
│                                                     │
│  Body text paragraph                                │
│  [typography.body.family] [weight]                  │
│                                                     │
│  CAPTION / LABEL                                    │
│  [typography.caption.family] [weight]               │
├─────────────────────────────────────────────────────┤
│  RULES                                              │
│  ✓ [typography.rules[0]]                           │
│  ✓ [typography.rules[1]]                           │
│                                                     │
│  AVOID                                              │
│  ✗ [mood.avoid[0]]                                 │
│  ✗ [mood.avoid[1]]                                 │
└─────────────────────────────────────────────────────┘
```

## 工作流

1. **读取风格** — 加载 `visual-style.md` 文件
2. **创建颜色样式** — 为调色板中的每种颜色各建一个样式
3. **创建文本样式** — Display、正文与 caption 样式
4. **设置布局网格** — 创建网格预设
5. **构建风格指南画框** — 记录设计体系
6. **添加参考图** — 若有 `assets.reference_images` 则导入

## Figma 插件集成

若开发读取 `visual-style.md` 的 Figma 插件：

```typescript
interface VisualStyle {
  name: string;
  version: string;
  style_prompt_short: string;
  style_prompt_full: string;
  colors: {
    primary: Color[];
    accent?: Color[];
    neutral?: Color[];
  };
  typography: {
    display: TypographyStyle;
    body: TypographyStyle;
    caption: TypographyStyle;
    rules?: string[];
  };
  // ... other fields
}

interface Color {
  name: string;
  hex: string;
  role: string;
}

interface TypographyStyle {
  family: string;
  weight: string;
  style?: string;
}
```

## 提示

- **字体可用性** — 确认 `typography.*.family` 中的字体在 Figma 中可用（Google Fonts 或本地安装）
- **颜色组织** — 用文件夹按用途分组颜色样式
- **样式描述** — 以 `role` 字段作为样式描述
- **设计评审** — 由 `typography.rules` 与 `mood.avoid` 生成检查清单
