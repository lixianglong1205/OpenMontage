---
name: multi-reference-editing
description: 使用多张参考图进行复杂合成
---

# 多参考图图像编辑

介绍如何使用多张参考图实现角色一致性、风格迁移与复杂合成。

## 概述

FLUX.2 模型支持多张参考图以实现高级编辑：

- **FLUX.2 [klein]**：最多 4 张参考图 — 快速编辑
- **FLUX.2 [pro]**：通过 API 最多 8 张 — 质量与速度均衡
- **FLUX.2 [max]**：通过 API 最多 8 张，Playground 中最多 10 张 — 最高质量
- **FLUX.2 [flex]**：通过 API 最多 8 张 — 最适合排版

> **注意：** 相比 FLUX.1 Kontext Max，更推荐使用 FLUX.2 模型以获得更好效果。

## 提供图像

**首选：直接使用 URL** — 比 base64 更简单、更方便。

将图像 URL 直接传入 `input_image`、`input_image_2` 等字段：

```json
{
  "prompt": "Person from image 1 wearing outfit from image 2",
  "input_image": "https://example.com/person.jpg",
  "input_image_2": "https://example.com/outfit.jpg"
}
```

API 会自动拉取 URL。URL 与 base64 均可，但在可用时更推荐 URL。

## 引用方式

### 自然语言描述

用自然语言描述各张图之间的关系：

```
The person from image 1 is sitting at the cafe table from image 2,
wearing the outfit from image 3, with the warm lighting style of image 4
```

### 显式编号

按图像编号引用以提高精确度：

```
Replace the background of image 1 with the landscape from image 2,
maintaining the subject's exact position and lighting
```

```
Combine the face from image 1 with the hairstyle from image 2
on the body pose from image 3
```

## 使用场景

### 角色一致性

在多个场景中保持同一角色：

```
Input: Reference image of character
Prompt: The character from image 1 walking through a busy Tokyo street
at night, neon lights reflecting on wet pavement
```

用于序列化一致性：

```
The same person from image 1, now seated at a desk in a modern office,
same clothing and hairstyle, different environment
```

### 风格迁移

将一张图的风格应用到另一张：

```
Transform image 1 into the artistic style of image 2,
maintaining the original composition and subject
```

```
Apply the color grading and mood from image 2 to the scene in image 1
```

### 姿态引导

用参考图约束身体姿态：

```
The person from image 1 in the exact pose shown in image 2,
placed in the environment from image 3
```

### 物体合成

组合多张图中的元素：

```
Place the product from image 1 on the table setting from image 2,
using the lighting style from image 3
```

### 背景替换

```
Keep the subject from image 1 exactly as shown, replace the background
with the beach scene from image 2, match the lighting naturally
```

## 多角色场景

### 两个角色

```
Image 1 (person A) and image 2 (person B) having a conversation
at a coffee shop table, person A on the left gesturing, person B
on the right listening intently
```

### 群组构图

```
The three people from images 1, 2, and 3 standing together for a
group photo, arranged left to right in that order, friendly poses,
outdoor park setting
```

## 属性混合

### 选择性属性迁移

```
The face and expression from image 1, the hairstyle from image 2,
wearing the outfit from image 3, in the pose from image 4
```

### 部分迁移

```
Apply only the color palette from image 2 to image 1,
keeping all other aspects (style, composition, lighting) unchanged
```

## 拼贴方法

使用拼贴输入来指导布局：

```
Arrange the scene using the layout shown in the collage input:
- Person from image 1 in the left position
- Object from image 2 in the center position
- Background element from image 3 filling the right side
```

## 最佳实践

### 1. 明确各图角色

说明每张参考图提供什么：

```
Image 1: face/identity reference
Image 2: pose/body reference
Image 3: style/aesthetic reference
Image 4: environment/background reference
```

### 2. 参考图质量

- 使用高质量、清晰的参考图
- 确保参考图光照良好
- 避免过度处理或重度滤镜的图像

### 3. 光照一致

组合元素时：

```
...ensure the lighting direction matches across all elements,
with main light source from the upper left
```

### 4. 分辨率意识

[pro] API 总像素上限为 9MP 时：

- 1MP 输出：可较轻松地使用最多 8 张参考图
- 计算方式：输入图像 + 输出 = 总 MP

### 5. 明确关系

不要假设 — 精确说明元素如何关联：

```
Vague: The person and the background together
Better: The person from image 1 standing in the foreground,
the beach from image 2 visible behind them at a distance
```

## 复杂合成示例

```
Create a scene combining:
- The woman from image 1 (keep exact face, expression, hair)
- Wearing the vintage dress from image 2 (exact pattern and cut)
- In the pose from image 3 (seated position, arm placement)
- Set in the library from image 4 (bookshelves, furniture)
- Using the warm lighting style from image 5 (golden hour quality)

Position her in the center of frame, medium shot, looking slightly
to the right with a thoughtful expression.
```

## 故障排查

### 元素未迁移

- 更具体说明哪个元素来自哪张图
- 使用显式编号（如「from image 1」）
- 减少参考图数量与复杂度

### 融合不一致

- 指定光照一致
- 描述元素应如何互动
- 用风格参考统一整体构图

### 身份漂移

- 强调关键识别特征
- 使用如「maintaining exact likeness」等表述
- 若有可能，提供同一主体的多角度参考
