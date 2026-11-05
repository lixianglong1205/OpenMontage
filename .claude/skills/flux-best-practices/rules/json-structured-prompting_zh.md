---
name: json-structured-prompting
description: 使用 JSON 格式进行复杂场景构图
---

# JSON 结构化提示

对于包含多个元素、空间关系或需要生产自动化的复杂场景，请使用 JSON 结构化提示。

## 适用场景

- 多个角色且各自属性不同
- 精确的空间定位
- 复杂场景构图
- 可复现的、基于模板的提示
- 程序化生成提示
- 带变量替换的生产工作流

## 基本结构

```json
{
  "scene": {
    "setting": "description of environment",
    "time": "time of day/period",
    "mood": "atmospheric quality"
  },
  "subjects": [
    {
      "type": "person/object/animal",
      "description": "detailed description",
      "position": "location in frame",
      "action": "what they're doing"
    }
  ],
  "style": {
    "medium": "photography/painting/illustration",
    "technique": "specific style details",
    "reference": "artist or style reference"
  },
  "technical": {
    "camera": "camera and lens",
    "lighting": "lighting setup",
    "composition": "framing details"
  },
  "colors": ["#hex1", "#hex2"]
}
```

## 单主体示例

```json
{
  "scene": {
    "setting": "cozy home office with bookshelves",
    "time": "late afternoon",
    "mood": "focused, peaceful"
  },
  "subjects": [
    {
      "type": "person",
      "description": "woman in her 30s, dark curly hair in loose bun, wearing casual cream sweater",
      "position": "seated at desk, center frame",
      "action": "typing on laptop, slight smile of concentration"
    }
  ],
  "style": {
    "medium": "photography",
    "technique": "lifestyle editorial",
    "reference": "kinfolk magazine aesthetic"
  },
  "technical": {
    "camera": "Sony A7III with 50mm f/1.8",
    "lighting": "soft natural window light from left",
    "composition": "medium shot, rule of thirds"
  }
}
```

## 多角色场景

```json
{
  "scene": {
    "setting": "Victorian-era drawing room with ornate wallpaper and antique furniture",
    "time": "evening, candlelit",
    "mood": "tense, mysterious"
  },
  "subjects": [
    {
      "id": "detective",
      "type": "person",
      "description": "tall man in his 50s, sharp features, grey at temples, wearing brown tweed suit",
      "position": "standing center-left, facing right",
      "action": "examining a letter with magnifying glass, intense focus"
    },
    {
      "id": "lady",
      "type": "person",
      "description": "elegant woman in her 40s, auburn hair in Victorian updo, emerald green evening dress",
      "position": "seated on chaise lounge, right side",
      "action": "watching the detective with concealed anxiety, hands clasped"
    },
    {
      "id": "butler",
      "type": "person",
      "description": "elderly man in formal butler attire, stoic expression",
      "position": "background, near doorway",
      "action": "standing at attention, observing"
    }
  ],
  "style": {
    "medium": "oil painting",
    "technique": "classical realism with dramatic lighting",
    "reference": "Victorian narrative painting, John Singer Sargent"
  },
  "technical": {
    "lighting": "warm candlelight as key, cool moonlight through window as fill",
    "composition": "triangular arrangement of figures, detective at apex"
  }
}
```

## 带颜色的产品场景

```json
{
  "scene": {
    "setting": "minimalist product photography studio",
    "mood": "clean, premium, aspirational"
  },
  "subjects": [
    {
      "type": "product",
      "description": "sleek wireless earbuds in charging case",
      "position": "center, slightly angled",
      "details": "matte finish, subtle branding"
    }
  ],
  "style": {
    "medium": "commercial photography",
    "technique": "high-end product shot",
    "reference": "Apple product photography"
  },
  "technical": {
    "camera": "Phase One with 120mm macro",
    "lighting": "large softbox overhead, subtle fill from below",
    "composition": "centered, hero product shot"
  },
  "colors": {
    "product": "#1A1A2E",
    "accent": "#E94560",
    "background": "#FFFFFF"
  }
}
```

## 将 JSON 转换为自然语言

在提交实际提示前，将 JSON 展平为流畅的散文描述：

### 从 JSON
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

### 转为提示
```
An elderly craftsman with weathered hands seated at his workbench in a
traditional workshop, carefully carving wood with focused precision.
Morning natural light streams through the window from the right,
illuminating the wood shavings and tools scattered across the worn surface.
```

## 模板变量

使用 JSON 结构进行基于模板的生成：

```json
{
  "template": "product_hero",
  "variables": {
    "product_name": "{{PRODUCT_NAME}}",
    "product_color": "{{PRODUCT_COLOR}}",
    "brand_primary": "{{BRAND_HEX_1}}",
    "brand_secondary": "{{BRAND_HEX_2}}",
    "background_style": "{{BG_STYLE}}"
  },
  "prompt_template": "Professional product photography of {{PRODUCT_NAME}} in {{PRODUCT_COLOR}}, brand colors {{BRAND_HEX_1}} and {{BRAND_HEX_2}} accents, {{BG_STYLE}} background, commercial quality"
}
```

## 空间关系

明确定义空间关系：

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

## 最佳实践

1. **用 ID 做引用** — 当主体之间会互动时，为主体分配 ID
2. **关注点分离** — 将 scene、subjects、style 与 technical 分开维护
3. **保持一致** — 全文使用相同术语
4. **写全细节** — 不要假设，把一切写清楚
5. **执行前展平** — 发送给模型前先转为自然语言
6. **模板版本化** — 跟踪模板版本以保证可复现
