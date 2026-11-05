---
name: flux2-models
description: 专属于 FLUX.2 模型系列的提示词撰写指南
---

# FLUX.2 模型系列

FLUX.2 各变体的完整指南及其最佳提示词策略。

> **核心特性：** 所有 FLUX.2 模型均原生支持通过参考图进行文生图（text-to-image）与图生图（image-to-image）编辑。编辑任务无需再使用旧版 FLUX.1 Kontext 模型。

## 模型概览

| 模型 | 参数量 | 最佳用途 | 速度 | 参考图 |
|-------|------------|----------|-------|------------------|
| [klein] | 4B/9B | 快速迭代、预览、快速编辑 | 最快 | 最多 4 张 |
| [max] | - | 最高质量生成与编辑 | 最慢 | 最多 8–10 张 |
| [pro] | - | 生产级均衡 | 中等 | 最多 8 张 |
| [flex] | - | 排版、文字渲染 | 中等 | 最多 8 张 |
| [dev] | - | 本地开发 | 因环境而异 | 因环境而异 |

## FLUX.2 [klein] - 快速生成

适合快速原型、预览与高批量生成。

### 特性
- 提供 4B 或 9B 参数量版本
- 亚秒级生成
- 优先速度而非极致细节
- **无提示词上采样（prompt upsampling）** — 需自行写足描述
- 最多支持 4 张参考图

### 提示词风格：叙事散文

Klein 对强调光线与氛围的叙事式描述提示响应最佳。

### 示例提示词
```
A cozy coffee shop interior bathed in warm afternoon light, steam rising lazily
from ceramic cups, worn leather armchairs arranged around small wooden tables,
bookshelves lining exposed brick walls, the soft atmosphere of a quiet afternoon
with dust motes floating in sunbeams through tall windows
```

### [klein] 使用技巧
- 像小说家描写场景一样写作
- 把主体放在句首（词序很关键）
- 着重描写光线
- 提示词保持中等详略（约 40–70 词）

## FLUX.2 [max] - 最高质量

面向最终生产资产与最大细节的高端模型。

### 特性
- 细节与连贯性最高
- 编辑一致性最佳
- 广博世界知识
- 含 grounding search（实时网页数据）
- 提示词遵循能力最强
- 最多 8 张参考图（API），10 张（playground）

### 提示词风格：技术参数 + 描述

[max] 擅长将详细技术规格与描述性散文结合。

### 示例提示词
```
Portrait of a weathered fisherman, age 70, deep wrinkles telling stories of
decades at sea, salt-and-pepper beard with streaks of white, wearing a navy
cable-knit sweater with visible wool texture. Shot on Hasselblad X2D with
90mm f/2.8 lens at f/4, golden hour natural light from the left creating
strong rim lighting, shallow depth of field with soft bokeh from harbor
lights behind, Kodak Portra 400 color science with natural grain
```

### [max] 使用技巧
- 为写实效果写明机身与镜头规格
- 指定胶片型号或数字传感器特性
- 使用摄影术语（光圈、焦距等）
- 结合 grounding search 做时事：「news photo of [recent event]」

## FLUX.2 [pro] - 生产均衡

在生产工作流中平衡质量与速度。

### 特性
- 良好的质量/速度比
- 输出稳定可靠
- 适合批量处理
- 支持提示词上采样
- 最多 8 张参考图

### 提示词风格：均衡详略

标准详细提示即可，无需过多技术规格。

### 示例提示词
```
A modern minimalist living room with floor-to-ceiling windows overlooking
a city skyline at dusk, clean white furniture with subtle textures, a single
statement plant in the corner, warm ambient lighting from hidden sources,
architectural photography style with clean lines and balanced composition
```

### [pro] 使用技巧
- 在具体程度与生成速度间取平衡
- 适合基于模板的提示词系统
- 开启提示词上采样以提升效果
- 生产流水线质量稳定

## FLUX.2 [flex] - 排版专精

针对文字渲染与排版内容优化。

### 特性
- 文字渲染质量优异
- 可处理多段文字
- 可调 steps（1–50）与 guidance（1.5–10）
- 适合招牌、海报、UI mockup
- 最多 8 张参考图

### 提示词风格：以排版为中心

务必用引号标出文字，并明确字体特征。

### 示例提示词
```
A modern minimalist poster design with the headline "DESIGN SUMMIT 2025"
in bold condensed sans-serif typography centered in the upper third,
subtitle "Innovation Meets Creativity" in lighter weight below,
date "MARCH 15-17" in small caps at the bottom, all text in white
on a gradient background transitioning from deep purple #4A0080 to
coral #FF6B6B, clean geometric accent lines, professional print quality
```

### [flex] 使用技巧
- 始终引用准确文字：`"Your Text Here"`
- 指定字体风格：serif、sans-serif、script、display、monospace
- 描述文字层级：标题、副标题、正文
- 说明位置：居中、左对齐、上三分之一等
- 调整 steps（越高质量越好）与 guidance（越高越严格）

## FLUX.2 [dev] - 本地开发

用于本地开发、测试与非商业用途。

### 特性
- Hugging Face 开放权重
- 可本地运行（建议约 13GB VRAM）
- 可完全自定义
- 非商业使用免费
- 提供基础（未蒸馏）变体供微调

### 提示词风格：标准

与 [pro] 相同的提示模式效果良好。

### [dev] 使用技巧
- 上线前用于开发与测试
- 尝试不同提示变体
- 适合微调实验
- 商业使用前请查阅许可限制

## 使用 FLUX.2 进行图生图编辑

所有 FLUX.2 模型均可通过参考图编辑图像，可替代旧版 FLUX.1 Kontext。

### 工作原理

1. 将源图作为参考图提供
2. 在提示词中描述期望的改动
3. 模型在保留上下文的同时应用编辑

### 示例：风格迁移
```
Reference: [your source image]
Prompt: Transform this image into a watercolor painting style,
maintaining the exact composition and subject positioning
```

### 示例：物体修改
```
Reference: [your source image]
Prompt: Change the car color to red while keeping everything else identical
```

### 示例：角色一致性
```
Reference: [character reference image]
Prompt: The same person from the reference image walking through
a busy Tokyo street at night, neon lights reflecting on wet pavement
```

### 编辑场景下的模型选择

| 使用场景 | 推荐模型 |
|----------|-------------------|
| 快速迭代/预览 | FLUX.2 [klein] |
| 生产级质量编辑 | FLUX.2 [pro] |
| 最高质量/复杂编辑 | FLUX.2 [max] |
| 文字/排版编辑 | FLUX.2 [flex] |
