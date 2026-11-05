---
name: "Neville Brody Industrial Type"
version: "1.0"
tags:
  - 标志性设计
  - 利落极简
author: "Teo @ HeyGen"
created: "2026-03-12"

style_prompt_short: >
  暗色工业字体。压缩与扭曲的字形以克制的攻击性
  撞入碎裂网格。Brody 80 年代末广播式粗粝感
  与编辑张力相遇。

style_prompt_full: >
  一套受 Neville Brody 80 年代末至 90 年代字体实验启发的
  暗色、实验性图形系统：工业质感、压缩与拉伸的字形、
  媒介粗粝感、碎裂对齐与克制的攻击性。使用炭黑、钢灰、
  脏白、信号红与 muted 电光蓝。字体应显得经工程化设计、
  扭曲且承载文化重量。字形应压缩、拉伸、分裂并猛撞入网格，
  带着尖锐的工业力量。视觉与文字应碰撞而非礼貌地融合。
  裁切图像碎片、静态纹理与密集标签应通过粗粝的字体切分
  与广播式断裂重组画面。动效应显得媒介感重、紧绷且当代。

colors:
  primary:
    - name: "Charcoal Black"
      hex: "#1A1A1A"
      role: "主背景"
    - name: "Dirty White"
      hex: "#E0E0E0"
      role: "主文字"
  accent:
    - name: "Signal Red"
      hex: "#CC3333"
      role: "强调、打断"
    - name: "Muted Electric Blue"
      hex: "#4488AA"
      role: "次要点缀"
  neutral:
    - name: "Steel Gray"
      hex: "#666666"
      role: "辅助文字、网格线"

typography:
  display:
    family: "Condensed industrial sans-serif"
    weight: "ultra bold / black"
    style: "大写、极端压缩"
  body:
    family: "Neutral sans-serif (Univers, Akzidenz-Grotesk)"
    weight: "regular to medium"
  caption:
    family: "Monospace or condensed sans"
    style: "小号、密集、全大写"
  rules:
    - "字体即视觉——与内容碰撞，而非叠在其上"
    - "碎裂对齐是有意为之"
    - "混用极端字重"
    - "永不居中——始终左对齐或碎裂错位"
    - "字体可溢出画框"

layout:
  grid: "激进不对称网格，刻意打破"
  alignment: "左对齐、碎裂离轴"
  aspect_ratio: "16:9"
  notes:
    - "密集——留白极少"
    - "裁切图像碎片作纹理"
    - "标签像广播控制室叠加层"

motion:
  transitions:
    - "粗粝字体切分"
    - "广播式静态爆发"
    - "垂直/水平面板切换"
  animation_style: "字体猛撞入网格。无柔和缓动。元素相互碰撞。"
  pacing: "紧绷、有节奏、受控"

mood:
  keywords:
    - "industrial"
    - "aggressive"
    - "editorial"
    - "broadcast"
    - "tense"
  era: "1980 年代末–1990 年代"
  cultural_reference: "Neville Brody, The Face magazine, Arena, Fuse"
  avoid:
    - "柔和渐变或 pastel"
    - "居中版式"
    - "友好语气"
    - "圆角字体或手写体"
    - "装饰性插画"
    - "平滑缓动"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: "c22c70a499a048cfa67a1426313ec345"
  orientation: "landscape"
---

## 设计原则

字体不是装饰——它是结构。
张力制造注意力。
有意打破网格。
每一次碰撞都经过编排。

## 连接器

### HeyGen Video Agent
原样使用 `style_prompt_full`。强调：粗粝切分、静态纹理、
猛撞入画面的字体。不要平滑转场。广播控制室美学。

### HTML Slides
深色背景（#1A1A1A）。溢出边缘的压缩字体。
不对称版式。红色点缀作强调。信息密集呈现。

### paper.design
刻意打破网格。让字体与边缘碰撞。
使用图像碎片，而非整幅照片。控制室叠加层美学。

### Figma
Color styles：`brand/charcoal`、`brand/dirty-white`、`accent/signal-red`、`accent/electric-blue`。
Text styles：展示用压缩黑体级字重。允许字体超出画框。
