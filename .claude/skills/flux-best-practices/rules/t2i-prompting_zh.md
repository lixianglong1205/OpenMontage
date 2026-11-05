---
name: t2i-prompting
description: 文生图（Text-to-Image）提示词模式与技巧
---

# 文生图（T2I）提示词

面向 FLUX 模型撰写有效文生图提示词的全面指南。

## 提示词结构框架

### 基本公式
```
[Subject] + [Action] + [Style] + [Context] + [Lighting] + [Technical]
```

### 扩展框架
```
[Main Subject] - who/what is the focus
[Attributes] - characteristics, details, clothing
[Action/Pose] - what they're doing
[Environment] - where, setting, background
[Style/Medium] - artistic approach
[Lighting] - light source, quality, mood
[Composition] - framing, camera angle
[Technical] - camera, lens, film stock
```

## 主体类型

### 人物/肖像
```
A distinguished professor in his 60s with silver hair and round spectacles,
wearing a tweed jacket with leather elbow patches, deep-set thoughtful eyes,
slight smile suggesting hidden wisdom
```

### 动物
```
A majestic snow leopard with piercing blue-grey eyes, thick spotted fur
dusted with snowflakes, powerful muscular build, alert posture on a
rocky outcrop
```

### 物体/产品
```
A vintage Leica M3 camera with worn brass edges showing decades of use,
black leather covering with patina, sitting on weathered wooden table
```

### 风景
```
A dramatic fjord at dawn, steep granite cliffs rising from mirror-still
water, wisps of morning mist, distant snow-capped peaks catching first
golden light
```

### 建筑
```
A brutalist concrete apartment building in late afternoon light, geometric
shadows creating abstract patterns, warm sunlight contrasting with cool
grey concrete
```

## 风格类别

### 照片写实

#### 现代数码
```
shot on Sony A7IV, clean and sharp, high dynamic range, professional color grading
```

#### 胶片摄影
```
shot on Kodak Portra 400, natural film grain, organic colors, slight warmth
```

#### 复古数码（2000 年代）
```
early digital camera aesthetic, slight noise, flash photography, candid feel
```

#### 80 年代胶片
```
80s film photography, film grain, warm color cast, soft focus, nostalgic
```

### 艺术风格

#### 油画
```
classical oil painting style, visible brushstrokes, rich colors, dramatic lighting
```

#### 水彩
```
delicate watercolor painting, soft edges, transparent washes, paper texture visible
```

#### 数字艺术
```
polished digital illustration, clean lines, vibrant colors, professional concept art
```

#### 动漫/漫画
```
anime style, large expressive eyes, clean linework, cel shading, vibrant palette
```

## 布光模式

### 肖像布光
```
Rembrandt lighting - 45 degree key light creating triangle shadow on cheek
Butterfly lighting - overhead key creating shadow under nose
Split lighting - 90 degree side light, half face in shadow
Loop lighting - slight angle creating small nose shadow
```

### 自然光
```
Golden hour - warm, soft, directional light 1 hour before sunset
Blue hour - cool, ambient light just after sunset
Overcast - soft, even, diffused lighting
Harsh midday - strong contrast, defined shadows
```

### 氛围光
```
Volumetric light - visible light rays through fog/dust
Rim lighting - backlight creating edge glow
Practical lighting - visible light sources in scene
Neon glow - colorful artificial urban lighting
```

## 相机与镜头模拟

### 机身
```
Shot on Hasselblad X2D - medium format, exceptional detail
Shot on Canon 5D Mark IV - professional DSLR quality
Shot on Leica M10 - rangefinder character, smooth tonality
Shot on iPhone 15 Pro - computational photography look
```

### 镜头特性
```
85mm f/1.4 - classic portrait, creamy bokeh
24mm f/2.8 - wide angle, environmental
50mm f/1.2 - natural perspective, shallow DOF
135mm f/2 - compressed perspective, smooth background
Macro lens - extreme close-up detail
Tilt-shift lens - miniature effect or architectural correction
```

### 技术参数
```
f/1.4 - extremely shallow depth of field
f/2.8 - moderate background blur
f/8 - sharp throughout, landscape
f/16 - maximum sharpness, long exposure
ISO 100 - clean, no noise
ISO 3200 - visible grain, low light
```

## 构图技巧

### 景别
```
extreme close-up - filling frame with detail
close-up - head and shoulders
medium shot - waist up
full shot - entire body
wide shot - subject in environment
establishing shot - location focus
```

### 机位角度
```
eye level - natural, relatable
low angle - powerful, imposing
high angle - diminished, overview
Dutch angle - tension, unease
bird's eye - pattern, layout
worm's eye - dramatic upward view
```

### 构图法则
```
rule of thirds - subject at intersection points
centered composition - symmetry, stability
leading lines - guiding eye to subject
frame within frame - natural framing elements
negative space - minimalist, breathing room
```

## 完整提示词示例

### 时尚编辑肖像
```
A fashion editorial portrait of a young woman with striking features and
high cheekbones, wearing an avant-garde geometric collar in silver, dramatic
side lighting creating strong shadows, shot on Hasselblad with 100mm lens
at f/2.8, studio background with subtle gradient, high fashion magazine style
```

### 产品摄影
```
A premium wireless headphone product shot, matte black finish with rose gold
accents, floating at slight angle against pure white background, soft even
lighting eliminating harsh shadows, reflection visible on glossy surface below,
commercial catalog style, ultra sharp focus throughout
```

### 风景
```
A misty morning in ancient redwood forest, towering trees disappearing into
fog above, ferns covering forest floor in layers of green, single shaft of
golden sunlight breaking through canopy, shot on large format camera, rich
detail in bark textures, Ansel Adams inspired black and white with deep tones
```

### 建筑
```
Modern minimalist beach house at golden hour, floor-to-ceiling glass walls
reflecting sunset colors, clean white concrete and natural wood, infinity
pool merging with ocean horizon, architectural photography style, wide angle
showing full structure, warm evening light
```
