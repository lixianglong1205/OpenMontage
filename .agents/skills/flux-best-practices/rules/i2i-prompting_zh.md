---
name: i2i-prompting
description: 使用 FLUX 模型进行图生图（Image-to-Image）编辑的提示词指南
---

# 图生图（Image-to-Image, I2I）提示词

使用 FLUX 模型进行高效图生图编辑的指南。

## 概述

所有 FLUX.2 模型均支持通过参考图进行图生图编辑：
- **FLUX.2 [klein]**：最多 4 张参考图 — 快速编辑
- **FLUX.2 [pro]**：最多 8 张参考图 — 质量与速度平衡
- **FLUX.2 [max]**：最多 8–10 张参考图 — 最高质量编辑
- **FLUX.2 [flex]**：最多 8 张参考图 — 最适合排版类编辑

只需将源图作为参考并提供期望的修改描述即可。模型理解图像上下文，可在保留其他元素的同时修改特定部分。

> **注意：** 推荐使用 FLUX.2 模型进行图像编辑，效果优于较旧的 FLUX.1 Kontext 模型。

## 提供图像

**首选：直接使用 URL** — 比 base64 更简单、更方便。

若有图像 URL，可直接传入 `input_image`：

```json
{
  "prompt": "Change the background to a beach sunset",
  "input_image": "https://example.com/photo.jpg"
}
```

API 会自动拉取 URL。URL 与 base64 均可，但在可用时建议使用 URL。

## 基础编辑模式

### 简单修改
直接、单一变更的指令：

```
Change the car color to red
```

```
Make the sky a dramatic sunset
```

```
Add snow to the ground
```

### 属性变更
修改特定特征：

```
Change her hair color to platinum blonde
```

```
Make the building taller
```

```
Age the person to appear 20 years older
```

## 可控编辑

### 明确保留
需要保持特定元素不变时：

```
Change the background to a beach scene while keeping the subject's
pose, clothing, and expression exactly the same
```

```
Transform the daytime photo to nighttime, maintaining the exact
composition, colors of the subject's outfit, and lighting direction
```

### 风格保留
避免非预期的风格偏移：

```
Change the season to autumn with falling leaves, but maintain
the photograph's realistic style and color grading
```

```
Add rain effects to the scene while preserving the painting's
impressionist brushwork and color palette
```

## 变换类型

### 环境变更

#### 时段
```
Convert to golden hour lighting with warm tones and long shadows,
keeping all other elements identical
```

```
Transform to blue hour with city lights beginning to glow,
maintaining the exact composition
```

#### 天气
```
Add heavy rain with wet reflections on surfaces, dark overcast sky
```

```
Create a foggy atmosphere with reduced visibility, mysterious mood
```

#### 季节
```
Transform to winter with snow covering surfaces, bare trees,
cold blue color cast
```

```
Change to spring with cherry blossoms, fresh green leaves,
soft warm lighting
```

### 风格迁移

#### 艺术流派
```
Transform into Art Nouveau style with flowing organic lines,
decorative patterns, and muted earth tones
```

```
Convert to Pop Art style with bold primary colors, halftone dots,
and high contrast graphic treatment
```

#### 艺术家参考
```
Reimagine in the style of Monet with visible brushstrokes,
soft focus, and impressionist color harmony
```

```
Transform to match Edward Hopper's style with dramatic lighting,
urban isolation feeling, and muted palette
```

#### 媒介转换
```
Convert this photograph to a detailed pencil sketch with
careful shading and visible line work
```

```
Transform into a watercolor painting with soft edges,
transparent washes, and paper texture visible
```

### 主体修改

#### 服装变更
```
Change the outfit to a formal black suit with white shirt and red tie
```

```
Replace the casual clothes with traditional Japanese kimono in blue floral pattern
```

#### 表情变更
```
Change the expression to a warm genuine smile
```

```
Make the expression more serious and contemplative
```

#### 年龄调整
```
Age the subject to appear as a wise elderly person with grey hair and wrinkles
```

```
Make the subject appear younger, around 25 years old
```

### 物体编辑

#### 添加
```
Add a vintage leather briefcase in the subject's left hand
```

```
Place a steaming cup of coffee on the table
```

#### 移除
```
Remove the background people, replace with empty street
```

```
Remove the text/logo from the shirt, replace with solid color
```

#### 替换
```
Replace the modern car with a 1960s vintage Mustang in cherry red
```

```
Swap the coffee mug for an ornate teacup with floral pattern
```

## 文字编辑

### 添加文字
```
Add a neon sign reading "OPEN 24 HOURS" in the window,
glowing red letters with blue outline
```

```
Include a wooden sign with hand-painted text "Welcome Home"
mounted above the door
```

### 修改文字
```
Change the store sign to read "BAKER'S DOZEN" in the same style
```

```
Update the poster text to "SUMMER SALE 2025" maintaining the design
```

## 复杂多步编辑

对于大幅变换，可考虑分步进行：

### 分步方法
不要一次性写：
```
Transform this modern office into a Victorian library with completely
different furniture, add a fireplace, change the lighting to candlelit,
and age the photograph
```

可尝试顺序编辑：
1. `Change the furniture style to Victorian antique pieces`
2. `Add a stone fireplace on the right wall`
3. `Transform lighting to warm candlelit atmosphere`
4. `Apply vintage photograph aesthetic with sepia tones`

## 常见误区

### 避免模糊指令
```
Bad: Make it look better
Good: Increase contrast, add warm color grading, sharpen details
```

### 明确修改范围
```
Bad: Change the background
Good: Replace the office background with a tropical beach at sunset,
      maintaining the subject's exact position and lighting direction
```

### 明确保留风格
```
Bad: Make it nighttime
Good: Transform to nighttime while maintaining the photorealistic style,
      add appropriate artificial lighting sources
```

## 最佳实践

1. **从简单开始** — 先做单元素变更
2. **表述明确** — 说明要改什么、要保留什么
3. **引用上下文** — 在相关时提及现有元素
4. **迭代优化** — 用多次小改代替一次大改
5. **刻意保留** — 始终说明风格/构图保留需求
