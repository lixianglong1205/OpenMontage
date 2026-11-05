---
name: "Style Name"
version: "1.0"
tags:
  - tag1
  - tag2
author: "Your Name"
source_url: ""
created: "YYYY-MM-DD"

style_prompt_short: >
  用一两句话概括该风格的视觉本质。
  这是电梯演讲式的简述。

style_prompt_full: >
  详细的生成提示词。包含具体的十六进制色值、字体名称、
  布局结构、动效模式与整体氛围。这是最重要的字段——
  任何 AI 工具都应能据此生成一致的视觉。请明确说明该做什么、
  不该做什么。在文中内联写出 hex 色码（如 #FF5500），便于工具提取。

colors:
  primary:
    - name: "描述性颜色名称"
      hex: "#000000"
      role: "主背景、结构元素"
    - name: "描述性颜色名称"
      hex: "#FFFFFF"
      role: "主文字、负空间"
  accent:
    - name: "强调色名称"
      hex: "#FF5500"
      role: "CTA、强调、关键高亮"
  neutral:
    - name: "中性色名称"
      hex: "#888888"
      role: "辅助文字、边框、次要元素"

typography:
  display:
    family: "Font Family Name"
    weight: "bold"
    style: "大写、紧凑字距"
  body:
    family: "Font Family Name"
    weight: "regular"
    style: "句首大写、舒适行高"
  caption:
    family: "Font Family Name"
    weight: "medium"
    style: "小号、标签用大写"
  rules:
    - "排版规则或约束"
    - "另一条排版指南"
    - "字体使用限制"

layout:
  grid: "网格系统描述（例如 12 列、8px 基准单位）"
  alignment: "对齐方式（例如左对齐、居中主视觉）"
  aspect_ratio: "默认宽高比（例如 16:9、4:3）"
  notes:
    - "其他布局指南"
    - "间距或构图说明"

motion:
  transitions:
    - "过渡类型 1"
    - "过渡类型 2"
  animation_style: >
    元素如何移动与动画的说明。包含缓动、
    时长与整体感受。
  pacing: "整体节奏描述"
  audio_cues:
    - "声音设计说明"

mood:
  keywords:
    - "氛围词 1"
    - "氛围词 2"
    - "氛围词 3"
    - "氛围词 4"
  era: "时代参考（例如 1990 年代、当代）"
  cultural_reference: "启发本风格的设计师、运动或作品"
  avoid:
    - "明确要避免的事物"
    - "另一种反模式"
    - "不符合该风格的设计元素"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: ""
  orientation: "landscape"

x_figma:
  library_id: ""
---

## 设计原则

用于设计哲学与指导原则的自由段落。
哪些信念驱动这套视觉系统？
它有意做了哪些取舍？

## 连接器

### HeyGen Video Agent
如何将本风格应用于 HeyGen Video Agent 的说明。
在提示词中应强调什么、使用哪些动效模式。

### HTML Slides
关于 CSS 映射、布局方式、字体加载的说明。

### paper.design
关于文档设置、网格配置、AI 指导的说明。

### Figma
关于风格生成、组件模式、设计令牌的说明。

## 提取说明

若本风格从某来源提取，在此记录。
包含来源 URL、提取日期及任何重要决策。
