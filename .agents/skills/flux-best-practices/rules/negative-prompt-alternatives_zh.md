---
name: negative-prompt-alternatives
description: 负向提示词的正向替代写法
---

# 负向提示词替代方案

FLUX 不支持负向提示词。本指南为常见的负向提示模式提供正向替代写法。

## 为何不用负向提示词？

负向提示词反而可能让模型更关注你不想要的元素。应改为精确描述你**想要**的内容——这样方向更清晰，效果也更好。

## 替换策略

针对任何不想要的元素：
1. 明确你不想要什么
2. 自问：「那里本来应该有什么？」
3. 用正向表述描述替代方案

## 常见替换对照

### 人物/人群

| 不要写 | 改用 |
|-----------|-----|
| "no people" | "empty", "deserted", "solitary", "abandoned" |
| "no crowds" | "quiet", "peaceful", "secluded", "private" |
| "without background people" | "isolated subject", "clean background", "solo figure" |

**示例：**
```
Bad: A beach scene, no people
Good: A deserted beach at dawn, pristine untouched sand, solitary seagull
```

### 皮肤/外貌

| 不要写 | 改用 |
|-----------|-----|
| "no makeup" | "natural skin", "bare face", "fresh-faced" |
| "no blemishes" | "clear skin", "smooth complexion", "healthy glow" |
| "no wrinkles" | "youthful skin", "smooth features" |

**示例：**
```
Bad: Portrait of woman, no makeup, no blemishes
Good: Portrait of a woman with natural clear skin, fresh-faced with a healthy glow
```

### 配饰

| 不要写 | 改用 |
|-----------|-----|
| "no glasses" | "visible eyes", "unobstructed gaze", "clear eye contact" |
| "no hat" | "bare head", "visible hair", "uncovered head" |
| "no jewelry" | "minimal accessories", "understated", "unadorned" |

**示例：**
```
Bad: Man portrait, no glasses, no hat
Good: Portrait of a man with clear direct gaze, wind-swept visible hair
```

### 色彩

| 不要写 | 改用 |
|-----------|-----|
| "no color" | "monochrome", "black and white", "grayscale" |
| "not colorful" | "muted tones", "subdued palette", "desaturated" |
| "no bright colors" | "neutral tones", "earth tones", "soft pastels" |

**示例：**
```
Bad: Landscape photo, no bright colors
Good: Landscape in muted earth tones, soft morning light, desaturated palette
```

### 文字/水印

| 不要写 | 改用 |
|-----------|-----|
| "no text" | "clean surfaces", "unmarked", "text-free" |
| "no watermark" | "pristine image", "clean composition" |
| "no logos" | "unbranded", "plain", "logo-free surface" |

**示例：**
```
Bad: Product photo, no watermark, no text
Good: Clean product photography with pristine unmarked surfaces, minimal unbranded design
```

### 风格/时代

| 不要写 | 改用 |
|-----------|-----|
| "not modern" | "traditional", "classical", "vintage", "historical" |
| "no CGI look" | "photorealistic", "authentic", "natural", "organic" |
| "not cartoonish" | "realistic", "lifelike", "naturalistic" |

**示例：**
```
Bad: Building design, not modern, no futuristic elements
Good: Traditional Victorian architecture with classical ornate details and period-accurate features
```

### 画质/瑕疵

| 不要写 | 改用 |
|-----------|-----|
| "no blur" | "sharp focus", "crisp details", "tack-sharp" |
| "no noise" | "clean image", "smooth gradients", "low ISO" |
| "no artifacts" | "pristine quality", "clean render", "flawless" |

**示例：**
```
Bad: Portrait, no blur, no noise
Good: Tack-sharp portrait with pristine image quality, smooth skin tones, crisp details
```

### 物体

| 不要写 | 改用 |
|-----------|-----|
| "no cars" | "pedestrian area", "car-free zone", "walking street" |
| "no buildings" | "open landscape", "natural scenery", "wilderness" |
| "no furniture" | "empty room", "bare space", "minimalist interior" |

**示例：**
```
Bad: Street scene, no cars, no modern buildings
Good: Historic cobblestone walking street lined with traditional stone buildings from the 1800s
```

### 天气/环境

| 不要写 | 改用 |
|-----------|-----|
| "no rain" | "clear sky", "dry weather", "sunny day" |
| "no clouds" | "clear blue sky", "cloudless", "perfect visibility" |
| "not dark" | "well-lit", "bright", "daylight", "illuminated" |

**示例：**
```
Bad: Outdoor portrait, no rain, no clouds, not dark
Good: Outdoor portrait under clear blue sky on a bright sunny day, perfect natural lighting
```

### 构图

| 不要写 | 改用 |
|-----------|-----|
| "no distractions" | "clean composition", "focused framing", "minimal elements" |
| "nothing in background" | "solid background", "isolated subject", "clean backdrop" |
| "no clutter" | "organized", "tidy", "minimal", "streamlined" |

**示例：**
```
Bad: Product shot, no distractions, nothing in background
Good: Product on clean white seamless backdrop, isolated subject, minimal focused composition
```

## 复杂替换示例

### 原负向堆砌提示词
```
Portrait of a woman, no glasses, no makeup, no wrinkles, no blemishes,
no bright colors, no distracting background, no harsh lighting
```

### 正向改写
```
Portrait of a youthful woman with clear natural skin and visible bright eyes,
fresh-faced with a healthy glow, wearing muted earth tones against a soft
blurred neutral background, gentle diffused lighting creating soft shadows
```

### 原负向堆砌提示词
```
Landscape photo, no people, no buildings, no power lines, no modern elements,
no overcast sky, no dead trees
```

### 正向改写
```
Pristine wilderness landscape with lush green living forest, clear blue sky,
untouched natural scenery stretching to the horizon, peaceful solitude with
only birdsong and wind, golden hour sunlight filtering through healthy foliage
```

## 速查卡

| 不想要 | 正向替代 |
|----------|---------------------|
| No people | Empty, solitary, deserted |
| No makeup | Natural, fresh-faced, bare |
| No text | Clean, unmarked, pristine |
| No blur | Sharp, crisp, tack-sharp |
| No modern | Traditional, vintage, classical |
| No dark | Bright, well-lit, luminous |
| No busy | Minimal, clean, focused |
| No artificial | Natural, organic, authentic |
