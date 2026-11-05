---
name: core-principles
description: 适用于所有 FLUX 模型的通用提示词原则
---

# FLUX 核心提示词原则

这些原则适用于所有 FLUX 模型，是有效提示词的基础。

## 1. 仅使用正向描述

FLUX 不支持负向提示词（negative prompts）。始终描述你**想要**的内容，而不是你不想要的内容。

### 错误做法
```
a portrait of a woman, no glasses, no hat, no makeup
```

### 正确做法
```
a portrait of a woman with natural skin, clear face, bare head, visible eyes
```

全面的替代策略请参阅 [negative-prompt-alternatives.md](negative-prompt-alternatives.md)。

## 2. 提示词结构公式

按以下结构构建提示词，以获得一致的结果：

```
[Subject] + [Action/Pose] + [Style/Medium] + [Context/Setting] + [Lighting] + [Technical Details]
```

### 示例

```
A young woman with flowing auburn hair (subject)
dancing gracefully in mid-leap (action)
in the style of classical oil painting (style)
in a moonlit garden with roses (context)
soft diffused moonlight with subtle rim lighting (lighting)
medium shot, shallow depth of field (technical)
```

## 3. 具体性至关重要

提示词越具体，效果通常越好。

### 模糊（效果差）
```
a cat sitting
```

### 具体（效果佳）
```
A fluffy orange tabby cat with bright green eyes sitting regally on a vintage
velvet armchair, afternoon sunlight streaming through lace curtains, warm
golden hour lighting, shallow depth of field, shot on medium format film
```

## 4. 自然语言效果最佳

用描述性散文撰写提示词，而不是关键词列表。

### 关键词式（效果较弱）
```
woman, portrait, beautiful, blonde, studio, professional, 8k, detailed
```

### 散文式（效果更好）
```
A professional studio portrait of a beautiful blonde woman in her thirties,
captured with soft studio lighting that accentuates her features, rendered
in stunning detail with natural skin texture and subtle catchlights in her eyes
```

## 5. 光线至关重要

务必指定光线——它对图像质量的影响最大。

### 自然光
- Golden hour - warm, soft, directional
- Overcast - soft, diffused, even
- Harsh midday - high contrast, strong shadows
- Dappled forest light - specular, organic patterns

### 棚拍光
- Softbox - even, professional
- Rim light - edge definition, separation
- Butterfly lighting - beauty, glamour
- Rembrandt lighting - dramatic, classic portraits

### 氛围光
- Volumetric fog - depth, mystery
- God rays - dramatic, spiritual
- Neon glow - urban, cyberpunk
- Candlelight - warm, intimate

### 情绪导向光
- Dramatic shadows - tension, noir
- High key - bright, airy, clean
- Low key - moody, mysterious
- Chiaroscuro - strong contrast, painterly

## 6. 词序很重要

FLUX 会优先处理提示词中靠前的元素。把重要内容放在前面。

### 效果较弱
```
A forest background with soft lighting where a knight in shining armor stands
```

### 效果更好
```
A knight in shining armor stands in a forest, soft dappled lighting filtering
through the canopy
```

## 7. 适中的提示词长度

最佳提示词长度通常为 30–80 个词（FLUX 最多可处理 512 个 token）。

- 过短：缺乏方向，结果泛化
- 过长：可能失焦
- 最佳区间：细节足够引导生成，又不过于冗杂

## 8. 迭代优化

按以下步骤迭代构建提示词：

1. 从核心主体与动作开始
2. 加入风格与媒介
3. 指定光线与氛围
4. 补充技术细节
5. 根据生成结果继续微调

每次只改一个要素，以便了解它对输出的影响。
