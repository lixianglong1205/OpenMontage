---
name: flux1-models
description: FLUX.1 模型系列的提示词指南
---

# FLUX.1 模型系列

> **提示：** FLUX.2 模型为最新一代，在大多数场景下推荐使用。FLUX.1 模型仍可用于特定需求。

FLUX.1 模型及其专项能力指南。

## 模型概览

| 模型 | 用途 | 说明 |
|-------|---------|-------|
| FLUX1.1 [pro] | 文生图（Text-to-image） | FLUX.2 [pro] 效果更好 |
| FLUX.1 Kontext | 图生图（Image-to-image） | 推荐使用带参考图的 FLUX.2 |
| FLUX.1 Kontext Max | 图生图（Image-to-image） | 推荐使用带参考图的 FLUX.2 [max] |
| FLUX.1 Fill | 局部重绘（Inpainting） | 适用于特定局部重绘任务 |

## FLUX1.1 [pro]

快速、可靠的文生图生成。

### 特性
- 提示词遵循度高
- 生产级架构
- 输出稳定、可靠
- 适合大批量扩展
- 定价：每张 $0.04

### 提示词风格

采用标准描述式提示词，明确主体与风格。

### 示例提示词
```
A golden retriever puppy playing in autumn leaves, warm afternoon sunlight,
shallow depth of field with bokeh background, joyful expression, professional
pet photography style
```

## FLUX.1 Kontext - 图像编辑

> **建议：** 使用带参考图的 FLUX.2 模型可获得更好的编辑效果。

面向变换与修改的上下文感知图生图编辑模型。

### 特性
- 理解图像上下文
- 保留未编辑区域
- 风格迁移能力
- 物体修改
- 从基础到复杂的各类变换

### 提示词策略

#### 基础编辑
简单、直接的指令效果最好：

```
Change the color of the car to red
```

```
Make the sky sunset orange and pink
```

#### 受控编辑
明确说明需要保留的内容：

```
Change the setting to nighttime while maintaining the exact same
composition and the painting's artistic style
```

#### 复杂变换
大幅改动时，具体说明保留项：

```
Transform the modern office into a Victorian library with the same
furniture arrangement. Keep the window positions and overall room
proportions identical.
```

#### 风格迁移
引用具体艺术流派：

```
Transform this photograph into a Bauhaus art style with geometric
shapes and primary colors, maintaining the original composition
and subject positioning
```

#### 文字编辑
描述文字位置与融入方式：

```
Add the text "OPEN" as a neon sign in the window, red glowing letters
with slight reflection on the glass, matching the nighttime atmosphere
```

### Kontext 使用技巧
- 明确说明不应改变的部分
- 从简单编辑入手，逐步增加复杂度
- 需要时指定风格保留
- 适合增量式精修

## FLUX.1 Kontext Max

面向复杂构图的高级多参考图编辑。

### 特性
- 最多支持 10 张参考图
- 跨参考图编辑一致性最佳
- 复杂场景构图
- 角色一致性维护
- 速率限制：6 个并发请求

### 多参考图提示词

#### 自然语言引用
用自然语言描述各图之间的关系：

```
The person from image 1 is sitting in the cafe from image 2,
wearing the outfit from image 3, with the lighting style of image 4
```

#### 显式编号
按图片编号引用以提高精度：

```
Replace the top half of the person in image 1 with the clothing
from image 2, maintaining the pose and background
```

### Kontext Max 使用技巧
- 提前规划参考图
- 用自然语言描述关系
- 指明各元素来自哪张图
- 用于跨场景的角色一致性

## FLUX.1 Fill - 局部重绘

专用于物体移除与区域补全的工具。

### 特性
- 干净地移除物体
- 智能背景补全
- 感知纹理的填充
- 无缝融合

### 使用场景
- 从照片中移除不需要的物体
- 补全不完整图像
- 替换特定区域
- 清理图像瑕疵

### Fill 提示词

描述蒙版区域应填充的内容：

```
Fill with continuation of the brick wall texture and ivy
```

```
Complete with matching ocean waves and sandy beach
```

### Fill 使用技巧
- 提供周围区域的上下文
- 说明纹理与图案的延续
- 描述光照一致性
- 用于清理与移除类任务

