# FLUX 最佳实践

**Version 1.0.0**  
Black Forest Labs  
January 2026

> **注意：**  
> 本文档供 AI 智能体与 LLM 在处理  
> FLUX 图像生成提示词与工作流时遵循。人类读者也可参考，  
> 但此处指导针对自动化与一致性做了优化。  

---

## 摘要

面向 BFL FLUX 图像生成模型的综合提示词与工作流指南。涵盖全部 FLUX.2 与 FLUX.1 模型，包括文生图、图生图编辑、JSON 结构化提示、色彩指定、排版与多参考编辑。每条规则均含详细说明、有效与无效做法对比示例，以及针对具体模型的指导。

---

## 目录

1. [核心原则](#1-core-principles) - **关键**
   - 1.1 [FLUX 核心提示原则](#11-core-flux-prompting-principles)
2. [模型选择](#2-model-selection) - **高**
   - 2.1 [FLUX 模型选择指南](#21-flux-model-selection-guide)
   - 2.2 [FLUX.1 模型家族](#22-flux1-model-family)
   - 2.3 [FLUX.2 模型家族](#23-flux2-model-family)
3. [文生图提示](#3-text-to-image-prompting) - **高**
   - 3.1 [文生图 (T2I) 提示](#31-text-to-image-t2i-prompting)
4. [图生图编辑](#4-image-to-image-editing) - **高**
   - 4.1 [图生图 (I2I) 提示](#41-image-to-image-i2i-prompting)
5. [JSON 结构化提示](#5-json-structured-prompting) - **中高**
   - 5.1 [JSON 结构化提示](#51-json-structured-prompting)
6. [色彩指定](#6-color-specification) - **中**
   - 6.1 [十六进制色彩提示](#61-hex-color-prompting)
7. [排版与文字](#7-typography-and-text) - **中**
   - 7.1 [排版与文字提示](#71-typography-and-text-prompting)
8. [多参考编辑](#8-multi-reference-editing) - **中**
   - 8.1 [多参考图像编辑](#81-multi-reference-image-editing)
9. [正向提示替代方案](#9-positive-prompt-alternatives) - **中**
   - 9.1 [负向提示替代方案](#91-negative-prompt-alternatives)

---

## 1. 核心原则

**影响：关键**

适用于所有 FLUX 模型的通用提示原则。在深入具体技巧前先掌握这些。

### 1.1 FLUX 核心提示原则

**影响：中**

这些原则适用于所有 FLUX 模型，是有效提示的基础。

FLUX **不支持**负向提示。始终描述你**想要**的内容，而非你不想要的内容。

为获得一致结果，按以下结构构建提示：

**错误做法：**

```text
a portrait of a woman, no glasses, no hat, no makeup
```

**正确做法：**

```text
a portrait of a woman with natural skin, clear face, bare head, visible eyes
```

**示例：**

```text
A young woman with flowing auburn hair (subject)
dancing gracefully in mid-leap (action)
in the style of classical oil painting (style)
in a moonlit garden with roses (context)
soft diffused moonlight with subtle rim lighting (lighting)
medium shot, shallow depth of field (technical)
```

提示越具体，效果通常越好。

**模糊：效果差**

```text
a cat sitting
```

**具体：效果佳**

```text
A fluffy orange tabby cat with bright green eyes sitting regally on a vintage
velvet armchair, afternoon sunlight streaming through lace curtains, warm
golden hour lighting, shallow depth of field, shot on medium format film
```

用描述性散文写提示，而非关键词列表。

**关键词式：较无效**

```text
woman, portrait, beautiful, blonde, studio, professional, 8k, detailed
```

**散文式：更有效**

```text
A professional studio portrait of a beautiful blonde woman in her thirties,
captured with soft studio lighting that accentuates her features, rendered
in stunning detail with natural skin texture and subtle catchlights in her eyes
```

务必指定光照——它对画质影响最大。

**自然光：**

- Golden hour - warm, soft, directional

- Overcast - soft, diffused, even

- Harsh midday - high contrast, strong shadows

- Dappled forest light - specular, organic patterns

**棚拍光：**

- Softbox - even, professional

- Rim light - edge definition, separation

- Butterfly lighting - beauty, glamour

- Rembrandt lighting - dramatic, classic portraits

**氛围光：**

- Volumetric fog - depth, mystery

- God rays - dramatic, spiritual

- Neon glow - urban, cyberpunk

- Candlelight - warm, intimate

**情绪向光照：**

- Dramatic shadows - tension, noir

- High key - bright, airy, clean

- Low key - moody, mysterious

- Chiaroscuro - strong contrast, painterly

FLUX 更重视提示中靠前的元素。把重要内容放在前面。

**较无效：**

```text
A forest background with soft lighting where a knight in shining armor stands
```

**更有效：**

```text
A knight in shining armor stands in a forest, soft dappled lighting filtering
through the canopy
```

最佳提示长度通常为 30–80 词（FLUX 最多约 512 token）。

- 过短：缺乏方向，结果泛化

- 过长：可能失焦

- 甜点：细节足够引导，又不过于杂乱

迭代构建提示：

1. 从主体与动作核心开始

2. 加入风格与媒介

3. 指定光照与氛围

4. 加入技术细节

5. 根据结果微调

一次只改一个元素，以便理解对输出的影响。

参考：[negative-prompt-alternatives.md](negative-prompt-alternatives.md)

---

## 2. 模型选择

**影响：高**

为使用场景选对 FLUX 模型。涵盖 FLUX.2（最新）与 FLUX.1（旧版）两大系列。

### 2.1 FLUX 模型选择指南

**影响：中**

按需求选择最优 FLUX 模型的决策指南。

| 优先级      | 推荐模型               |

| ------------- | ------------------------------- |

| 速度         | FLUX.2 [klein]                  |

| 质量       | FLUX.2 [max]                    |

| 平衡       | FLUX.2 [pro]                    |

| 排版    | FLUX.2 [flex]                   |

| 图像编辑 | FLUX.2 [klein], [pro], or [max] |

| 本地/免费    | FLUX.2 [dev]                    |

| 局部重绘    | FLUX.1 Fill                     |

**注意：** 所有 FLUX.2 模型原生支持通过参考图进行图生图编辑。只需提供源图作为参考并描述期望改动。

**按速度：**

| 模型             | 相对速度 | 最适合                |

| ----------------- | -------------- | ----------------------- |

| FLUX.2 [klein] 4B | 最快        | 快速原型       |

| FLUX.2 [klein] 9B | 很快      | 更高质量预览 |

| FLUX.2 [pro]      | 中等         | 生产工作流    |

| FLUX.2 [flex]     | 中等         | 排版任务        |

| FLUX.2 [max]      | 较慢         | 最终主视觉       |

**按质量：**

| 模型             | 质量等级 | 权衡                  |

| ----------------- | ------------- | -------------------------- |

| FLUX.2 [max]      | 最高       | 最慢、最贵    |

| FLUX.2 [pro]      | 高          | 均衡良好               |

| FLUX.2 [flex]     | 高（文字）   | 专用于排版 |

| FLUX.2 [klein] 9B | 良好          | 快，细节略少 |

| FLUX.2 [klein] 4B | 中等      | 最快，预览质量   |

**按成本：**

> **积分定价：** 1 credit = $0.01 USD。FLUX.2 按百万像素计价。

| 模型             | 首 MP | +MP  | 1MP T2I | 1MP I2I | 批量建议       |

| ----------------- | ------ | ---- | ------- | ------- | --------------------------- |

| FLUX.2 [klein] 4B | 1.4c   | 0.1c | $0.014  | $0.015  | 大批量、预览       |

| FLUX.2 [klein] 9B | 1.5c   | 0.2c | $0.015  | $0.017  | 大批量、更高质量 |

| FLUX.2 [pro]      | 3c     | 1.5c | $0.03   | $0.045  | 生产负载        |

| FLUX.2 [max]      | 7c     | 3c   | $0.07   | $0.10   | 主视觉、高端        |

| FLUX.2 [flex]     | 6c     | 6c   | $0.06   | $0.12   | 排版                  |

| FLUX.2 [dev]      | -      | -    | Free    | Free    | 本地开发（非商用）  |

> **定价公式：** `(firstMP + (outputMP-1) * mpPrice) + (inputMP * mpPrice)`（单位：美分）

| 模型                | 单价/张 | 用例                |

| -------------------- | ----------- | ----------------------- |

| FLUX.1 Kontext [pro] | $0.04       | 上下文感知编辑   |

| FLUX.1 Kontext [max] | $0.08       | 最高质量编辑     |

| FLUX1.1 [pro]        | $0.04       | 标准 T2I            |

| FLUX1.1 [pro] Ultra  | $0.06       | 超高分辨率   |

| FLUX1.1 [pro] Raw    | $0.06       | 快照摄影质感 |

| FLUX.1 Fill [pro]    | $0.05       | 局部重绘              |
| FLUX.1 [pro]         | $0.05       | 原版 pro 模型      |

> 不同分辨率下的精确费用请使用 [bfl.ai/pricing](https://bfl.ai/pricing) 计算器。

**创意探索 / 构思：**

**推荐：FLUX.2 [klein]**

- 快速迭代

- 快速概念验证

- 情绪板生成

- 探索提示变体

**生产级营销素材：**

**推荐：FLUX.2 [pro]**

- 质量稳定

- 速度合理

- 规模化成本可控

- 适合自动化

**主视觉 / 高端内容：**

**推荐：FLUX.2 [max]**

- 细节最多

- 整体一致性最佳

- 支持 grounding search

- 关键视觉值得溢价

**排版 / 标识 / 海报：**

**推荐：FLUX.2 [flex]**

- 文字渲染出色

- 可调质量参数

- 可读文字最佳

- UI 线框与信息图

**角色一致性：**

**推荐：FLUX.2 [max] 或 [pro]**

- 多参考支持（最多 8–10 张图）

- 编辑一致性最佳

- 跨场景保持身份

- 质量优于 FLUX.1 Kontext

**照片编辑 / 修图：**

**推荐：FLUX.2 [klein]、[pro] 或 [max]**

- 通过参考图原生图生图

- 风格迁移

- 物体修改

- 属性变更

- 效果优于 FLUX.1 Kontext

**实时信息：**

**推荐：FLUX.2 [max]**

- Grounding search 功能

- 时事

- 近期新闻可视化

- 天气/位置数据

**本地开发 / 测试：**

**推荐：FLUX.2 [dev]**

- 无 API 费用

- 完全控制

- 微调实验

- 可离线

**带排版的编辑内容：**

```text
1. FLUX.2 [max] - Generate base image (highest quality)
2. FLUX.2 [flex] - Add text overlay pass
```

**角色一致系列：**

```text
1. FLUX.2 [max] - Create character reference
2. FLUX.2 [max]/[pro] - Generate consistent variations using reference images
3. FLUX.2 [klein] - Quick iteration on variations if needed
```

**电商产品流水线：**

```text
1. FLUX.2 [pro] - Bulk product generations
2. FLUX.2 [pro]/[klein] - Product variations (colors, angles) using references
3. FLUX.2 [flex] - Add promotional text/pricing
```

**预算有限：**

- **大批量**：FLUX.2 [klein] 4B

- **需要质量**：FLUX.2 [pro]（性价比最佳）

**时间紧：**

- **任意任务**：FLUX.2 [klein]

- **质量重要**：FLUX.2 [pro]

**必须最高质量：**

- **始终**：FLUX.2 [max]

**文字必须可读：**

- **始终**：FLUX.2 [flex]

**编辑已有图像：**

- **快速编辑**：FLUX.2 [klein] + 参考图

- **质量编辑**：FLUX.2 [max] 或 [pro] + 参考图

- **备选**：FLUX.1 Kontext（更推荐 FLUX.2）

**速率限制敏感：**

```text
Speed?      → FLUX.2 [klein]
Quality?    → FLUX.2 [max]
Balance?    → FLUX.2 [pro]
Text?       → FLUX.2 [flex]
Edit?       → FLUX.2 [klein/pro/max] with reference images
Free?       → FLUX.2 [dev]
```

- **优先**：FLUX.2 模型（24 并发上限）

- **避免**：FLUX.1 Kontext Max（6 并发上限）

**要点：** 所有 FLUX.2 模型均通过参考图原生支持图像编辑。编辑任务推荐 FLUX.2 而非 FLUX.1 Kontext。

### 2.2 FLUX.1 模型家族

**影响：中**

> **提示：** FLUX.2 为最新一代，大多数场景推荐使用。FLUX.1 仍可用于特定需求。

FLUX.1 模型及其专项能力指南。

| 模型 | 用途 | 说明 |

|-------|---------|-------|

| FLUX1.1 [pro] | 文生图 | FLUX.2 [pro] 效果更好 |

| FLUX.1 Kontext | 图生图 | 建议使用带参考图的 FLUX.2 |

| FLUX.1 Kontext Max | 图生图 | 建议使用带参考图的 FLUX.2 [max] |

| FLUX.1 Fill | 局部重绘 | 适用于特定局部重绘任务 |

快速可靠的文生图。

**特点：**

- 提示遵循强

- 生产级架构

- 结果稳定可靠

- 适合高批量

- 定价：$0.04/张

**提示风格：**

标准描述性提示，主体与风格清晰。

**示例提示：**

```text
A golden retriever puppy playing in autumn leaves, warm afternoon sunlight,
shallow depth of field with bokeh background, joyful expression, professional
pet photography style
```

> **建议：** 带参考图的 FLUX.2 模型编辑效果更好。

面向变换与修改的上下文感知图生图模型。

**特点：**

- 理解图像上下文

- 保留未编辑区域

- 风格迁移

- 物体修改

- 从简单到复杂变换

**提示策略：**

```text
Add the text "OPEN" as a neon sign in the window, red glowing letters
with slight reflection on the glass, matching the nighttime atmosphere
```

简单直接的指令最有效：

明确说明要保留的内容：

大幅改动时，具体说明保留项：

引用具体艺术流派：

描述文字位置与融合：

**Kontext 技巧：**

- 明确不应改变的部分

- 从简单编辑做起，逐步复杂化

- 需要时指定风格保留

- 用于增量精修

面向复杂合成的进阶多参考编辑。

**特点：**

- 最多 10 张参考图

- 跨参考编辑一致性最佳

- 复杂场景合成

- 角色一致性维护

- 速率限制：6 并发请求

**多参考提示：**

```text
Replace the top half of the person in image 1 with the clothing
from image 2, maintaining the pose and background
```

用自然语言描述图间关系：

按编号引用参考图以提高精度：

**Kontext Max 技巧：**

- 仔细规划参考图

- 用自然语言描述关系

- 指明各元素来自哪张图

- 用于跨场景角色一致

专用于物体移除与区域补全的工具。

**特点：**

- 干净移除物体
- 智能背景补全

- 感知纹理的填充

- 无缝融合

**使用场景：**

- 从照片移除不需要的物体

- 补全不完整图像

- 替换特定区域

- 清理图像瑕疵

**Fill 提示：**

```text
Complete with matching ocean waves and sandy beach
```

描述蒙版区域应填充的内容：

**Fill 技巧：**

- 提供周围环境上下文

- 指定纹理与图案延续

- 描述光照一致

- 用于清理与移除

### 2.3 FLUX.2 模型家族

**影响：中**

FLUX.2 各变体及最优提示策略完整指南。

> **关键特性：** 所有 FLUX.2 模型原生同时支持文生图与通过参考图的图生图编辑。编辑任务无需再依赖旧版 FLUX.1 Kontext。

| 模型 | 参数量 | 最适合 | 速度 | 参考图 |

|-------|------------|----------|-------|------------------|

| [klein] | 4B/9B | 快速迭代、预览、快速编辑 | 最快 | 最多 4 张 |

| [max] | - | 最高质量生成与编辑 | 最慢 | 最多 8-10 张 |

| [pro] | - | 生产均衡 | 中等 | 最多 8 张 |

| [flex] | - | 排版、文字渲染 | 中等 | 最多 8 张 |

| [dev] | - | 本地开发 | 不定 | 不定 |

最适合快速原型、预览与高批量生成。

**特点：**

- 提供 4B 或 9B 参数版本

- 亚秒级生成

- 为速度优化，非极致细节

- **无提示 upsampling**——需自行写足描述

- 最多 4 张参考图

**提示风格：叙事散文**

Klein 最适合描述性叙事提示，强调光照与氛围。

**示例提示：**

```text
A cozy coffee shop interior bathed in warm afternoon light, steam rising lazily
from ceramic cups, worn leather armchairs arranged around small wooden tables,
bookshelves lining exposed brick walls, the soft atmosphere of a quiet afternoon
with dust motes floating in sunbeams through tall windows
```

**[klein] 技巧：**

- 像小说家一样描写场景

- 主体前置（词序关键）

-  heavily 强调光照描述

- 提示适中详细（40–70 词）

面向最终生产资产与最大细节的 premium 模型。

**特点：**

- 细节与 coherence 最高

- 编辑一致性最佳

- 广博世界知识

- 含 grounding search（实时 web 数据）

- 提示遵循最强

- API 最多 8 张参考图，Playground 10 张

**提示风格：技术 + 描述**

[max] 擅长技术规格与描述散文结合。

**示例提示：**

```text
Portrait of a weathered fisherman, age 70, deep wrinkles telling stories of
decades at sea, salt-and-pepper beard with streaks of white, wearing a navy
cable-knit sweater with visible wool texture. Shot on Hasselblad X2D with
90mm f/2.8 lens at f/4, golden hour natural light from the left creating
strong rim lighting, shallow depth of field with soft bokeh from harbor
lights behind, Kodak Portra 400 color science with natural grain
```

**[max] 技巧：**

- 写实摄影可写机身镜头规格

- 指定胶片或数字传感器特性

- 使用摄影术语（光圈、焦距）

- 时事可用 grounding search："news photo of [recent event]"

生产工作流中质量与速度的最佳平衡。

**特点：**

- 质量/速度比良好

- 输出稳定一致

- 适合批处理

- 支持提示 upsampling

- 最多 8 张参考图

**提示风格：平衡细节**

标准详细提示即可，无需过多技术规格。

**示例提示：**

```text
A modern minimalist living room with floor-to-ceiling windows overlooking
a city skyline at dusk, clean white furniture with subtle textures, a single
statement plant in the corner, warm ambient lighting from hidden sources,
architectural photography style with clean lines and balanced composition
```

**[pro] 技巧：**

- 在 specificity 与生成速度间平衡

- 适合模板化提示系统

- 开启 prompt upsampling 增强效果

- 生产流水线质量稳定

针对文字渲染与排版内容优化。

**特点：**

- 文字渲染质量 superior

- 可处理多段文字

- 可调 steps（1–50）与 guidance（1.5–10）

- 适合招牌、海报、UI mockup

- 最多 8 张参考图

**提示风格：排版导向**

务必引号包裹文字并明确字体特征。

**示例提示：**

```text
A modern minimalist poster design with the headline "DESIGN SUMMIT 2025"
in bold condensed sans-serif typography centered in the upper third,
subtitle "Innovation Meets Creativity" in lighter weight below,
date "MARCH 15-17" in small caps at the bottom, all text in white
on a gradient background transitioning from deep purple #4A0080 to
coral #FF6B6B, clean geometric accent lines, professional print quality
```

**[flex] 技巧：**

- 精确文字始终加引号：`"Your Text Here"`

- 指定字体：serif、sans-serif、script、display、monospace

- 描述层级：标题、副标题、正文

- 说明位置：居中、左对齐、上三分之一

- 调整 steps（越高质量越好）与 guidance（越高越严格）

用于本地开发、测试与非商业用途。

**特点：**

- Hugging Face 开放权重

- 本地运行（建议 ~13GB VRAM）

- 可完全定制

- 非商业免费

- 提供 base（undistilled）变体便于微调

**提示风格：标准**

与 [pro] 相同提示模式即可。

**[dev] 技巧：**

- 上线前开发测试

- 实验提示变体

- 微调实验

- 商业使用查许可证限制

所有 FLUX.2 模型均通过参考图支持编辑，可替代旧版 FLUX.1 Kontext。

**工作流程：**

1. 将源图作为参考图提供

2. 在提示中描述期望改动

3. 模型保留上下文并应用编辑

**示例：风格迁移**

```text
Reference: [your source image]
Prompt: Transform this image into a watercolor painting style,
maintaining the exact composition and subject positioning
```

**示例：物体修改**

```text
Reference: [your source image]
Prompt: Change the car color to red while keeping everything else identical
```

**示例：角色一致**

```text
Reference: [character reference image]
Prompt: The same person from the reference image walking through
a busy Tokyo street at night, neon lights reflecting on wet pavement
```

**编辑模型选择：**

| 用例 | 推荐模型 |

|----------|-------------------|

| 快速迭代/预览 | FLUX.2 [klein] |

| 生产级编辑 | FLUX.2 [pro] |

| 最高质量/复杂编辑 | FLUX.2 [max] |

| 文字/排版编辑 | FLUX.2 [flex] |

---

## 3. 文生图提示

**影响：高**

从文本描述生成图像的有效提示撰写。

### 3.1 文生图 (T2I) 提示

**影响：中**

面向 FLUX 模型的文生图提示完整指南。

**基本公式：**

```text
[Subject] + [Action] + [Style] + [Context] + [Lighting] + [Technical]
```

**扩展框架：**

```text
[Main Subject] - who/what is the focus
[Attributes] - characteristics, details, clothing
[Action/Pose] - what they're doing
[Environment] - where, setting, background
[Style/Medium] - artistic approach
[Lighting] - light source, quality, mood
[Composition] - framing, camera angle
[Technical] - camera, lens, film stock
```

**人物/肖像：**

```text
A distinguished professor in his 60s with silver hair and round spectacles,
wearing a tweed jacket with leather elbow patches, deep-set thoughtful eyes,
slight smile suggesting hidden wisdom
```

**动物：**

```text
A majestic snow leopard with piercing blue-grey eyes, thick spotted fur
dusted with snowflakes, powerful muscular build, alert posture on a
rocky outcrop
```

**物体/产品：**

```text
A vintage Leica M3 camera with worn brass edges showing decades of use,
black leather covering with patina, sitting on weathered wooden table
```

**风景：**

```text
A dramatic fjord at dawn, steep granite cliffs rising from mirror-still
water, wisps of morning mist, distant snow-capped peaks catching first
golden light
```

**建筑：**

```text
A brutalist concrete apartment building in late afternoon light, geometric
shadows creating abstract patterns, warm sunlight contrasting with cool
grey concrete
```

**写实摄影：**

```text
80s film photography, film grain, warm color cast, soft focus, nostalgic
```

**艺术风格：**

```text
anime style, large expressive eyes, clean linework, cel shading, vibrant palette
```

**肖像布光：**

```text
Rembrandt lighting - 45 degree key light creating triangle shadow on cheek
Butterfly lighting - overhead key creating shadow under nose
Split lighting - 90 degree side light, half face in shadow
Loop lighting - slight angle creating small nose shadow
```

**自然光：**

```text
Golden hour - warm, soft, directional light 1 hour before sunset
Blue hour - cool, ambient light just after sunset
Overcast - soft, even, diffused lighting
Harsh midday - strong contrast, defined shadows
```

**氛围：**

```text
Volumetric light - visible light rays through fog/dust
Rim lighting - backlight creating edge glow
Practical lighting - visible light sources in scene
Neon glow - colorful artificial urban lighting
```

**相机机身：**

```text
Shot on Hasselblad X2D - medium format, exceptional detail
Shot on Canon 5D Mark IV - professional DSLR quality
Shot on Leica M10 - rangefinder character, smooth tonality
Shot on iPhone 15 Pro - computational photography look
```

**镜头特性：**

```text
85mm f/1.4 - classic portrait, creamy bokeh
24mm f/2.8 - wide angle, environmental
50mm f/1.2 - natural perspective, shallow DOF
135mm f/2 - compressed perspective, smooth background
Macro lens - extreme close-up detail
Tilt-shift lens - miniature effect or architectural correction
```

**技术参数：**

```text
f/1.4 - extremely shallow depth of field
f/2.8 - moderate background blur
f/8 - sharp throughout, landscape
f/16 - maximum sharpness, long exposure
ISO 100 - clean, no noise
ISO 3200 - visible grain, low light
```

**景别：**

```text
extreme close-up - filling frame with detail
close-up - head and shoulders
medium shot - waist up
full shot - entire body
wide shot - subject in environment
establishing shot - location focus
```

**角度：**

```text
eye level - natural, relatable
low angle - powerful, imposing
high angle - diminished, overview
Dutch angle - tension, unease
bird's eye - pattern, layout
worm's eye - dramatic upward view
```

**构图法则：**

```text
rule of thirds - subject at intersection points
centered composition - symmetry, stability
leading lines - guiding eye to subject
frame within frame - natural framing elements
negative space - minimalist, breathing room
```

**编辑类肖像：**

```text
A fashion editorial portrait of a young woman with striking features and
high cheekbones, wearing an avant-garde geometric collar in silver, dramatic
side lighting creating strong shadows, shot on Hasselblad with 100mm lens
at f/2.8, studio background with subtle gradient, high fashion magazine style
```

**产品摄影：**

```text
A premium wireless headphone product shot, matte black finish with rose gold
accents, floating at slight angle against pure white background, soft even
lighting eliminating harsh shadows, reflection visible on glossy surface below,
commercial catalog style, ultra sharp focus throughout
```

**风景（完整示例）：**

```text
A misty morning in ancient redwood forest, towering trees disappearing into
fog above, ferns covering forest floor in layers of green, single shaft of
golden sunlight breaking through canopy, shot on large format camera, rich
detail in bark textures, Ansel Adams inspired black and white with deep tones
```

**建筑（完整示例）：**

```text
Modern minimalist beach house at golden hour, floor-to-ceiling glass walls
reflecting sunset colors, clean white concrete and natural wood, infinity
pool merging with ocean horizon, architectural photography style, wide angle
showing full structure, warm evening light
```

---

## 4. 图生图编辑

**影响：高**

使用 FLUX.2 模型编辑与变换已有图像的技巧。

### 4.1 图生图 (I2I) 提示

**影响：中**

FLUX 模型图生图编辑有效指南。

所有 FLUX.2 模型均通过参考图支持图生图编辑：

- **FLUX.2 [klein]**：最多 4 张参考图——快速编辑

- **FLUX.2 [pro]**：最多 8 张——质量/速度平衡

- **FLUX.2 [max]**：最多 8–10 张——最高质量编辑

- **FLUX.2 [flex]**：最多 8 张——排版编辑最佳

提供源图作为参考并描述改动即可。模型理解上下文，可改特定元素并保留其余部分。

> **注意：** 图像编辑推荐 FLUX.2，效果优于旧版 FLUX.1 Kontext。

**优先：直接使用 URL**——比 base64 更简单方便。

有图像 URL 时直接传入 `input_image`：

API 会自动拉取 URL。URL 与 base64 均可，有 URL 时推荐 URL。

**简单修改：**

```text
Add snow to the ground
```

直接、单一改动指令：

**属性变更：**

```text
Age the person to appear 20 years older
```

修改特定特征：

**明确保留：**

```text
Transform the daytime photo to nighttime, maintaining the exact
composition, colors of the subject's outfit, and lighting direction
```

需保持特定元素不变时：

**风格保留：**

```text
Add rain effects to the scene while preserving the painting's
impressionist brushwork and color palette
```

避免 unwanted 风格偏移：

**环境变更：**

```text
Change to spring with cherry blossoms, fresh green leaves,
soft warm lighting
```

**风格迁移：**

```text
Transform into a watercolor painting with soft edges,
transparent washes, and paper texture visible
```

**主体修改：**

```text
Make the subject appear younger, around 25 years old
```

**物体编辑：**

```text
Swap the coffee mug for an ornate teacup with floral pattern
```

**添加文字：**

```text
Include a wooden sign with hand-painted text "Welcome Home"
mounted above the door
```

**修改文字：**

```text
Update the poster text to "SUMMER SALE 2025" maintaining the design
```

大幅变换可拆成多步：

**分步做法：**

```text
Transform this modern office into a Victorian library with completely
different furniture, add a fireplace, change the lighting to candlelit,
and age the photograph
```

而非一次完成，可顺序编辑：

1. `Change the furniture style to Victorian antique pieces`

2. `Add a stone fireplace on the right wall`

3. `Transform lighting to warm candlelit atmosphere`

4. `Apply vintage photograph aesthetic with sepia tones`

**避免模糊指令：**

```text
Bad: Make it look better
Good: Increase contrast, add warm color grading, sharpen details
```

**明确改动范围：**

```text
Bad: Change the background
Good: Replace the office background with a tropical beach at sunset,
      maintaining the subject's exact position and lighting direction
```

**明确风格保留：**

```text
Bad: Make it nighttime
Good: Transform to nighttime while maintaining the photorealistic style,
      add appropriate artificial lighting sources
```

1. **从简开始**——先改单一元素

2. **说清改与留**——哪些变、哪些不变

3. **引用上下文**—— relevant 时提及现有元素

4. **迭代**——多次小改优于一次大改

5. **刻意保留**——始终说明风格/构图保留需求

---
## 5. JSON 结构化提示

**影响：中高**

用结构化 JSON 描述复杂多元素场景合成。

### 5.1 JSON 结构化提示

**影响：中**

多元素、空间关系或生产自动化场景，使用 JSON 结构化提示。

- 多角色且属性 distinct

- 精确空间位置

- 复杂场景合成

- 可复现的模板化提示

- 程序化生成提示

- 带变量替换的生产工作流

将 JSON  flatten 成流畅散文再作为实际提示：

**来自 JSON：**

```json
{
  "subjects": [
    {
      "type": "person",
      "description": "elderly craftsman with weathered hands",
      "position": "seated at workbench",
      "action": "carefully carving wood"
    }
  ],
  "scene": { "setting": "traditional workshop", "time": "morning" },
  "technical": { "lighting": "natural window light from right" }
}
```

**转为提示：**

```json
{
  "composition": {
    "layout": "triangular",
    "focal_point": "center-left intersection",
    "depth_layers": [
      {
        "layer": "foreground",
        "elements": ["flowers in vase"],
        "focus": "soft blur"
      },
      {
        "layer": "midground",
        "elements": ["main subject"],
        "focus": "sharp"
      },
      {
        "layer": "background",
        "elements": ["window", "garden view"],
        "focus": "soft blur"
      }
    ]
  }
}
```

用 JSON 结构做模板化生成：

定义 explicit 空间关系：

1. **用 ID 引用**——互动主体赋予 ID

2. **关注点分离**——场景、主体、风格、技术分开

3. **术语一致**——全文统一用词

4. **细节齐全**——勿假设，全部写明

5. **执行前 flatten**——送模型前转为自然语言

6. **模板版本化**——便于复现

---

## 6. 色彩指定

**影响：中**

用十六进制色值精确控色，满足品牌级生成。

### 6.1 十六进制色彩提示

**影响：中**

FLUX 支持 #RRGGBB 精确指定颜色，对品牌一致与精确配色 essential。

在提示中直接写 hex 并附颜色名：

用以下关键词表明色彩指定：

**1. 始终配对描述：**

```text
Good: #FF6B6B (coral pink)
Bad: #FF6B6B
```

勿单独使用 hex——须含颜色名：

**2. 绑定具体物体：**

```text
A product shot featuring a smartphone with a #1DA1F2 (Twitter blue) case,
resting on a #14171A (near black) matte surface
```

明确颜色对应对象：

**3. 限制色板：**

```text
Color palette for the scene: #2ECC71 (emerald green), #3498DB (sky blue),
#F1C40F (sunflower yellow), #FFFFFF (pure white)
```

通常 3–5 色最佳，过多易混淆模型：

**品牌色：**

```text
Corporate office reception with brand colors prominently featured:
walls in #0066CC (company blue), accent furniture in #FF6600 (company orange),
logo displayed in #FFFFFF (white) against the blue backdrop
```

**室内设计：**

```text
Scandinavian minimalist bedroom with #F5F5F5 (warm white) walls,
#8B4513 (saddle brown) wooden headboard and nightstands,
#708090 (slate gray) linen bedding, and #DAA520 (goldenrod) accent lamp
```

**时尚：**

```text
Editorial fashion photo: model wearing #000000 (black) cashmere turtleneck,
#FF4500 (orange-red) wide-leg wool pants, #C0C0C0 (silver) geometric earrings,
against a #F0F0F0 (light gray) studio backdrop
```

**产品设计：**

```text
Premium headphones product shot: #1C1C1E (space gray) aluminum body,
#F5F5F7 (silver) mesh ear cups, #FF9500 (iOS orange) accent ring around controls
```

**数字艺术：**

```text
Synthwave cityscape: #FF00FF (magenta) and #00FFFF (cyan) neon signs,
#1A1A2E (deep navy) night sky, #E94560 (hot pink) setting sun on horizon,
#16213E (dark blue) building silhouettes, rain-slicked streets reflecting lights
```

**数据可视化：**

```text
Sunset sky gradient from #FF6B6B (coral) at horizon through
#FFA07A (light salmon) to #87CEEB (sky blue) at top
```

渐变需写起止色：

**互补色：色轮对立**

```text
Scene using complementary colors: #3498DB (blue) dominant with
#E67E22 (orange) accents for visual pop
```

**类似色：相邻**

```text
Harmonious palette using analogous colors: #9B59B6 (purple),
#8E44AD (deep purple), #3498DB (blue) - flowing naturally together
```

**三色：等距**

```text
Vibrant triadic scheme: #E74C3C (red), #F1C40F (yellow),
#3498DB (blue) - balanced and dynamic
```

**单色：同色相变化**

```text
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

仅供参考——务必核对最新品牌规范：

**颜色不准：**

- hex 旁加颜色名

- 指明颜色作用于何物

- 减少提示中总色数

**颜色渗染：**

- 清楚划分各物体颜色

- 用空间描述："the LEFT chair in #color"

**颜色发灰：**

- 核对 hex

- 指定不偏移颜色的光照

- 强调用 "maintaining exact color #XXXXXX"

---
## 7. 排版与文字

**影响：中**

在生成图像中渲染文字与排版。

### 7.1 排版与文字提示

**影响：中**

FLUX 图像中渲染文字指南。排版最佳用 FLUX.2 [flex]。

始终引号包裹要渲染的 exact 文字：

**1. 使用引号：**

```text
Correct: A poster with "HELLO WORLD" in bold letters
Wrong: A poster with HELLO WORLD in bold letters
```

**2. 指定字体风格：**

```text
"ADVENTURE" in bold sans-serif typography
"Welcome" in elegant cursive script
"CHAPTER ONE" in classic serif typeface
"CODE" in monospace terminal font
"SALE!" in decorative display lettering
```

**3. 描述大小层级：**

```text
Large headline "BREAKING NEWS" above smaller subtext "Details inside"
```

**4. 说明位置：**

```text
"OPEN" sign centered in storefront window
"EXIT" text positioned above doorway
"Page 1" in bottom right corner
```

**5. 文字前置：**

```text
Good: A sign reading "FRESH BREAD" in a bakery window...
Less Good: A bakery window with a sign that says "FRESH BREAD"...
```

文字描述放提示前部更准确：

**无衬线（现代/简洁）：**

```text
"MINIMAL" in clean geometric sans-serif, Swiss modernist style
"TECH SUMMIT" in bold condensed grotesque typeface
"future" in thin uppercase sans-serif, contemporary design
```

**衬线：经典/优雅**

```text
"The New Yorker" in traditional serif typeface, editorial masthead
"LUXURY" in high-contrast Didone serif with thin/thick strokes
"Wisdom" in old-style serif with subtle bracketed serifs
```

**手写/花体（装饰）：**

```text
"With Love" in flowing calligraphic script with flourishes
"Signature" in connected brush script, casual elegance
"Romance" in formal copperplate script, wedding invitation style
```

**展示/装饰体：**

```text
"ROCK CONCERT" in distressed vintage concert poster lettering
"CIRCUS" in ornate Victorian display type with decorative elements
"RETRO" in 1970s rounded bubble letters
```

**手写风：**

```text
"Note to self" in casual handwritten style, slightly imperfect
"Thanks!" in quick marker pen handwriting
"ideas" in sketchy pencil handwriting
```

**等宽：**

```text
"CODE_COMPLETE" in terminal monospace, developer aesthetic
"SYSTEM" in typewriter monospace, vintage tech
"DEBUG" in LCD-style digital monospace
```

**霓虹招牌：**

```text
Glowing neon sign spelling "OPEN 24/7" in pink neon tubes with
blue outline, slight glow and reflection, night scene
```

**金属/3D：**

```text
"GOLD" in three-dimensional metallic gold letters with realistic
reflections and subtle shadows, luxury aesthetic
```

**压印/凹印：**

```text
"PREMIUM" embossed into leather surface, subtle shadows showing
the raised letterforms
```

**描边：**

```text
"MODERN" in outline-only letters, no fill, thin white stroke
on dark background
```

**渐变文字：**

```text
"SUMMER" with gradient fill from #FF6B6B (coral) at top to
#4ECDC4 (teal) at bottom
```

**海报设计：**

```text
Event poster with "SUMMER FEST 2025" as large headline in bold
condensed sans-serif at top, "JULY 15-17" as medium subheading
in regular weight, "Central Park, NYC" as small body text at
bottom, all in white text on #FF6B35 (sunset orange) background
```

**书籍封面：**

```text
Book cover design: "THE GREAT GATSBY" in elegant art deco gold
lettering centered in upper third, author name "F. SCOTT FITZGERALD"
in smaller gold caps below, #1A1A2E (midnight blue) background
with geometric gold accents
```

**杂志封面：**

```text
Fashion magazine cover with "VOGUE" in classic serif masthead at top,
cover line "SPRING COLLECTION" in bold sans-serif, "The New Rules of Style"
in lighter weight italic, all in white against dramatic portrait
```

**标识：**

```text
Vintage diner sign: "MEL'S DINER" in red neon script lettering,
"OPEN" below in separate green neon block letters, chrome border,
1950s Americana aesthetic
```

**名片：**

```text
Minimalist business card with "JOHN SMITH" in medium weight sans-serif,
"Creative Director" in lighter weight below, contact details in small
type at bottom, #2C3E50 (dark blue) text on white background
```

**居中构图：**

```text
Centered text layout: "WELCOME" in large caps at center,
perfectly balanced with equal margins
```

**左对齐：**

```text
Left-aligned text block: "Company Name" as header,
"Tagline goes here" below, flush left alignment
```

**路径文字：**

```text
"GOING IN CIRCLES" text following a circular path around
the center of the design
```

**文字叠加：**

```text
"ADVENTURE AWAITS" in bold white text overlaid on landscape
photograph, positioned in lower third with slight shadow for readability
```

**Steps 参数：**

- 更高 steps（30–50）= 文字质量更好

- 更低 steps（10–20）= 更快、质量更低

**Guidance 参数：**

- 更高 guidance（6–10）= 更严格遵循提示

- 更低 guidance（1.5–4）= 更 creative 解读

**推荐设置：**

```text
For clean typography: steps=50, guidance=7
For artistic text: steps=30, guidance=4
```

**拼写错误：**

- 文字宜短（1–4 词最佳）

- 尽量常用词

- 提示中重复 exact 文字

**难以辨认：**

- 指定更大字号

- 更简单字体（sans-serif）

- 与背景高对比

- 使用 [flex] 模型

**字体风格不对：**

```text
Instead of: "text in a nice font"
Use: "text in bold geometric sans-serif similar to Futura"
```

需更具体：

**文字未出现：**

- 文字描述前置

- 引号包裹

- 精确位置

- 降低提示其他复杂度

---

## 8. 多参考编辑

**影响：中**

组合多张参考图做风格迁移与合成。

### 8.1 多参考图像编辑

**影响：中**

多参考图实现角色一致、风格迁移与复杂合成指南。

FLUX.2 支持多参考 advanced 编辑：

- **FLUX.2 [klein]**：最多 4 张——快速

- **FLUX.2 [pro]**：API 最多 8 张——平衡

- **FLUX.2 [max]**：API 8 张、Playground 10 张——最高质量

- **FLUX.2 [flex]**：API 最多 8 张——排版最佳

> **注意：** 推荐 FLUX.2 而非 FLUX.1 Kontext Max。

**优先：直接使用 URL**——比 base64 更简单。

将 URL 直接传给 `input_image`、`input_image_2` 等：

API 自动拉取。URL 与 base64 均可，有 URL 时推荐 URL。

**自然语言描述：**

```text
The person from image 1 is sitting at the cafe table from image 2,
wearing the outfit from image 3, with the warm lighting style of image 4
```

自然描述图间关系：

**显式编号：**

```text
Combine the face from image 1 with the hairstyle from image 2
on the body pose from image 3
```

按编号引用以提高精度：

**角色一致：**

```text
The same person from image 1, now seated at a desk in a modern office,
same clothing and hairstyle, different environment
```

跨场景保持同一角色：

序列一致时：

**风格迁移：**

```text
Apply the color grading and mood from image 2 to the scene in image 1
```

将一张图风格应用到另一张：

**姿势引导：**

```text
The person from image 1 in the exact pose shown in image 2,
placed in the environment from image 3
```

用参考控制 body 位置：

**物体合成：**

```text
Place the product from image 1 on the table setting from image 2,
using the lighting style from image 3
```

组合多图元素：

**换背景：**

```text
Keep the subject from image 1 exactly as shown, replace the background
with the beach scene from image 2, match the lighting naturally
```

**双角色：**

```text
Image 1 (person A) and image 2 (person B) having a conversation
at a coffee shop table, person A on the left gesturing, person B
on the right listening intently
```

**群像：**

```text
The three people from images 1, 2, and 3 standing together for a
group photo, arranged left to right in that order, friendly poses,
outdoor park setting
```

**选择性属性迁移：**

```text
The face and expression from image 1, the hairstyle from image 2,
wearing the outfit from image 3, in the pose from image 4
```

**部分迁移：**

```text
Arrange the scene using the layout shown in the collage input:
- Person from image 1 in the left position
- Object from image 2 in the center position
- Background element from image 3 filling the right side
```

拼贴输入可指导布局：

**1. 明确各图角色：**

```text
Image 1: face/identity reference
Image 2: pose/body reference
Image 3: style/aesthetic reference
Image 4: environment/background reference
```

说明每张参考提供什么：

**2. 参考图质量：**

- 高清、清晰

- 参考图光照良好

- 避免过度处理或滤镜

**3. 光照一致：**

```text
...ensure the lighting direction matches across all elements,
with main light source from the upper left
```

组合元素时：

**4. 分辨率意识：**

[pro] API 总 9MP 限制：

- 1MP 输出： comfortably 最多 8 张参考

- 计算：输入图 MP + 输出 = 总 MP

**5. 关系写清：**

```text
Create a scene combining:
- The woman from image 1 (keep exact face, expression, hair)
- Wearing the vintage dress from image 2 (exact pattern and cut)
- In the pose from image 3 (seated position, arm placement)
- Set in the library from image 4 (bookshelves, furniture)
- Using the warm lighting style from image 5 (golden hour quality)

Position her in the center of frame, medium shot, looking slightly
to the right with a thoughtful expression.
```

勿假设——写清元素如何关联：

**元素未迁移：**

- 更具体说明哪张图的哪个元素

- 显式索引（"from image 1"）

- 减少参考数量与复杂度

**融合不一致：**

- 指定光照一致

- 描述元素如何互动

- 用风格参考统一合成

**身份漂移：**

- 强调关键识别特征

- 使用 "maintaining exact likeness" 等短语

- 若有条件提供同一主体多角度

---
## 9. 正向提示替代方案

**影响：中**

在 FLUX 不支持负向提示的前提下达成期望结果的策略。

### 9.1 负向提示替代方案

**影响：中**

FLUX 不支持负向提示。本文为常见负向模式提供正向替代。

负向提示反而可能让模型更关注不想要的元素。应精确描述你**想要**的内容——方向更清晰、效果更好。

对任何不想要的元素：

1. 识别不想要的是什么

2. 问：「那里应该有什么？」

3. 描述正向替代

**人物/人群：**

| 不要写 | 改用 |

|-----------|-----|

| "no people" | "empty", "deserted", "solitary", "abandoned" |

| "no crowds" | "quiet", "peaceful", "secluded", "private" |

| "without background people" | "isolated subject", "clean background", "solo figure" |

**示例：**

```text
Bad: A beach scene, no people
Good: A deserted beach at dawn, pristine untouched sand, solitary seagull
```

**皮肤/外观：**

| 不要写 | 改用 |

|-----------|-----|

| "no makeup" | "natural skin", "bare face", "fresh-faced" |

| "no blemishes" | "clear skin", "smooth complexion", "healthy glow" |

| "no wrinkles" | "youthful skin", "smooth features" |

**示例：**

```text
Bad: Portrait of woman, no makeup, no blemishes
Good: Portrait of a woman with natural clear skin, fresh-faced with a healthy glow
```

**配饰：**

| 不要写 | 改用 |

|-----------|-----|

| "no glasses" | "visible eyes", "unobstructed gaze", "clear eye contact" |

| "no hat" | "bare head", "visible hair", "uncovered head" |

| "no jewelry" | "minimal accessories", "understated", "unadorned" |

**示例：**

```text
Bad: Man portrait, no glasses, no hat
Good: Portrait of a man with clear direct gaze, wind-swept visible hair
```

**颜色：**

| 不要写 | 改用 |

|-----------|-----|

| "no color" | "monochrome", "black and white", "grayscale" |

| "not colorful" | "muted tones", "subdued palette", "desaturated" |

| "no bright colors" | "neutral tones", "earth tones", "soft pastels" |

**示例：**

```text
Bad: Landscape photo, no bright colors
Good: Landscape in muted earth tones, soft morning light, desaturated palette
```

**文字/水印：**

| 不要写 | 改用 |

|-----------|-----|

| "no text" | "clean surfaces", "unmarked", "text-free" |

| "no watermark" | "pristine image", "clean composition" |

| "no logos" | "unbranded", "plain", "logo-free surface" |

**示例：**

```text
Bad: Product photo, no watermark, no text
Good: Clean product photography with pristine unmarked surfaces, minimal unbranded design
```

**风格/时代：**

| 不要写 | 改用 |

|-----------|-----|

| "not modern" | "traditional", "classical", "vintage", "historical" |

| "no CGI look" | "photorealistic", "authentic", "natural", "organic" |

| "not cartoonish" | "realistic", "lifelike", "naturalistic" |

**示例：**

```text
Bad: Building design, not modern, no futuristic elements
Good: Traditional Victorian architecture with classical ornate details and period-accurate features
```

**质量/瑕疵：**

| 不要写 | 改用 |

|-----------|-----|

| "no blur" | "sharp focus", "crisp details", "tack-sharp" |

| "no noise" | "clean image", "smooth gradients", "low ISO" |

| "no artifacts" | "pristine quality", "clean render", "flawless" |

**示例：**

```text
Bad: Portrait, no blur, no noise
Good: Tack-sharp portrait with pristine image quality, smooth skin tones, crisp details
```

**物体：**

| 不要写 | 改用 |

|-----------|-----|

| "no cars" | "pedestrian area", "car-free zone", "walking street" |

| "no buildings" | "open landscape", "natural scenery", "wilderness" |

| "no furniture" | "empty room", "bare space", "minimalist interior" |

**示例：**

```text
Bad: Street scene, no cars, no modern buildings
Good: Historic cobblestone walking street lined with traditional stone buildings from the 1800s
```

**天气/环境：**

| 不要写 | 改用 |

|-----------|-----|

| "no rain" | "clear sky", "dry weather", "sunny day" |

| "no clouds" | "clear blue sky", "cloudless", "perfect visibility" |

| "not dark" | "well-lit", "bright", "daylight", "illuminated" |

**示例：**

```text
Bad: Outdoor portrait, no rain, no clouds, not dark
Good: Outdoor portrait under clear blue sky on a bright sunny day, perfect natural lighting
```

**构图：**

| 不要写 | 改用 |

|-----------|-----|

| "no distractions" | "clean composition", "focused framing", "minimal elements" |

| "nothing in background" | "solid background", "isolated subject", "clean backdrop" |

| "no clutter" | "organized", "tidy", "minimal", "streamlined" |

**示例：**

```text
Bad: Product shot, no distractions, nothing in background
Good: Product on clean white seamless backdrop, isolated subject, minimal focused composition
```

**原负向堆砌提示：**

```text
Portrait of a woman, no glasses, no makeup, no wrinkles, no blemishes,
no bright colors, no distracting background, no harsh lighting
```

**正向改写：**

```text
Portrait of a youthful woman with clear natural skin and visible bright eyes,
fresh-faced with a healthy glow, wearing muted earth tones against a soft
blurred neutral background, gentle diffused lighting creating soft shadows
```

**原负向堆砌提示：**

```text
Landscape photo, no people, no buildings, no power lines, no modern elements,
no overcast sky, no dead trees
```

**正向改写：**

```text
Pristine wilderness landscape with lush green living forest, clear blue sky,
untouched natural scenery stretching to the horizon, peaceful solitude with
only birdsong and wind, golden hour sunlight filtering through healthy foliage
```

| 不想要的 | 正向替代 |

|----------|---------------------|

| 无人 | 空镜、 solitary、荒废 |

| 无妆 | 自然、素颜、 bare |

| 无文字 | 干净、无标记、 pristine |

| 无模糊 | 锐利、清晰、tack-sharp |

| 非现代 | 传统、复古、 classical |

| 非暗 | 明亮、well-lit、 luminous |

| 非杂乱 | 极简、干净、 focused |

| 非人工 | 自然、 organic、 authentic |

---

## 参考资料

1. [https://docs.bfl.ai](https://docs.bfl.ai)
2. [https://bfl.ai](https://bfl.ai)
