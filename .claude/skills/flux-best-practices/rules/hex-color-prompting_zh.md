---
name: hex-color-prompting
description: 使用十六进制色码进行精确颜色指定
---

# 十六进制色码提示（Hex Color Prompting）

FLUX 支持十六进制色码（#RRGGBB），可用于精确指定颜色，对品牌一致性与精确配色至关重要。

## 语法

在提示词中直接写入十六进制色码，并附上描述性颜色名称：

```
A modern living room with walls painted in #2C3E50 (dark blue-gray),
accent pillows in #E74C3C (vibrant red), and a #F39C12 (warm amber)
throw blanket on a #ECF0F1 (off-white) sofa
```

## 信号关键词

使用以下关键词表明你在指定颜色：

```
color #02eb3c
hex #edfa3c
in #FF5733
using color code #3498DB
```

## 最佳实践

### 1. 始终与描述配对

切勿单独使用十六进制色码——务必包含颜色名称：

```
Good: #FF6B6B (coral pink)
Bad: #FF6B6B
```

### 2. 关联到具体对象

明确将颜色与其应用对象对应：

```
A product shot featuring a smartphone with a #1DA1F2 (Twitter blue) case,
resting on a #14171A (near black) matte surface
```

### 3. 限制调色板数量

通常 3–5 种颜色效果最佳；过多会让模型混淆：

```
Color palette for the scene: #2ECC71 (emerald green), #3498DB (sky blue),
#F1C40F (sunflower yellow), #FFFFFF (pure white)
```

## 使用场景

### 品牌色

```
Corporate office reception with brand colors prominently featured:
walls in #0066CC (company blue), accent furniture in #FF6600 (company orange),
logo displayed in #FFFFFF (white) against the blue backdrop
```

### 室内设计

```
Scandinavian minimalist bedroom with #F5F5F5 (warm white) walls,
#8B4513 (saddle brown) wooden headboard and nightstands,
#708090 (slate gray) linen bedding, and #DAA520 (goldenrod) accent lamp
```

### 时尚

```
Editorial fashion photo: model wearing #000000 (black) cashmere turtleneck,
#FF4500 (orange-red) wide-leg wool pants, #C0C0C0 (silver) geometric earrings,
against a #F0F0F0 (light gray) studio backdrop
```

### 产品设计

```
Premium headphones product shot: #1C1C1E (space gray) aluminum body,
#F5F5F7 (silver) mesh ear cups, #FF9500 (iOS orange) accent ring around controls
```

### 数字艺术

```
Synthwave cityscape: #FF00FF (magenta) and #00FFFF (cyan) neon signs,
#1A1A2E (deep navy) night sky, #E94560 (hot pink) setting sun on horizon,
#16213E (dark blue) building silhouettes, rain-slicked streets reflecting lights
```

### 数据可视化

```
Infographic showing market share: segments in #2ECC71 (green) for growth,
#E74C3C (red) for decline, #3498DB (blue) for stable, #95A5A6 (gray) for other,
clean #FFFFFF (white) background
```

## 渐变色

用起始色与结束色描述渐变：

```
Abstract background starting with color #02eb3c (bright green) and
finishing with color #edfa3c (lime yellow), smooth horizontal gradient
```

```
Sunset sky gradient from #FF6B6B (coral) at horizon through
#FFA07A (light salmon) to #87CEEB (sky blue) at top
```

## 配色和谐模式

### 互补色（色轮上相对）
```
Scene using complementary colors: #3498DB (blue) dominant with
#E67E22 (orange) accents for visual pop
```

### 类似色（相邻色）
```
Harmonious palette using analogous colors: #9B59B6 (purple),
#8E44AD (deep purple), #3498DB (blue) - flowing naturally together
```

### 三角配色（等距分布）
```
Vibrant triadic scheme: #E74C3C (red), #F1C40F (yellow),
#3498DB (blue) - balanced and dynamic
```

### 单色（同一色相变化）
```
Sophisticated monochromatic blue: #1A5276 (dark navy), #2980B9 (medium blue),
#85C1E9 (light blue), #D4E6F1 (pale blue) - elegant depth
```

## 与 JSON 结构化提示结合

```json
{
  "scene": {
    "setting": "modern tech startup office",
    "mood": "innovative, energetic"
  },
  "colors": {
    "primary": "#6C5CE7 (electric purple)",
    "secondary": "#00CEC9 (teal)",
    "accent": "#FD79A8 (pink)",
    "neutral": "#DFE6E9 (light gray)",
    "dark": "#2D3436 (charcoal)"
  },
  "application": {
    "walls": "neutral #DFE6E9",
    "furniture": "dark #2D3436",
    "accent_pieces": "primary #6C5CE7",
    "plants": "secondary #00CEC9 pots"
  }
}
```

## 常见品牌色参考

仅供参考——请务必核对当前品牌规范：

```
# Social Media
Twitter/X Blue: #1DA1F2
Facebook Blue: #1877F2
Instagram Gradient: #833AB4 to #FD1D1D
LinkedIn Blue: #0A66C2

# Tech
Apple Gray: #1C1C1E
Google Blue: #4285F4
Microsoft Blue: #00A4EF
Amazon Orange: #FF9900

# Design
Figma Purple: #A259FF
Dribbble Pink: #EA4C89
Behance Blue: #1769FF
```

## 故障排查

### 颜色不准确
- 在十六进制色码旁加上颜色名称
- 明确颜色应用的具体对象
- 减少提示词中的总颜色数量

### 颜色渗色
- 清楚区分各对象对应的颜色
- 使用空间描述：「the LEFT chair in #color」

### 颜色发灰、发脏
- 核对十六进制色码是否正确
- 指定不会偏移颜色的光照
- 使用「maintaining exact color #XXXXXX」加以强调
