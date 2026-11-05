---
name: "Saul Bass Cinematic Titles"
version: "1.0"
tags:
  - 标志性设计
  - 电影感
author: "Visual Style Gallery"
created: "2026-03-12"

style_prompt_short: >
  大胆图形化电影语言。鲜明剪影、撕纸边缘、
  强烈对比。希区柯克时代片头序列的活灵活现。

style_prompt_full: >
  Saul Bass 电影片头序列风格。大胆、图形化、戏剧化。
  高对比黑白配单一强调色（橙红 #FF4500 或黄色 #FFD700）。
  鲜明剪影与粗体造型。撕纸边缘与剪纸美学。几何精准却
  带手工感。戏剧化揭示与变形。字体与画面融为一体，而非
  浮于其上。《迷魂记》螺旋、《桃色血案》剪纸、《金臂人》
  字体。强对角线。动效具剧场感——元素揭示、旋转、变形。
  爵士影响下的节奏。禁止照片写实、柔边、渐变。

colors:
  primary:
    - name: "深黑"
      hex: "#000000"
      role: "剪影、戏剧化基底"
    - name: "纯白"
      hex: "#FFFFFF"
      role: "负空间、对比"
  accent:
    - name: "Saul Bass 橙"
      hex: "#FF4500"
      role: "单一戏剧强调色"
    - name: "金黄"
      hex: "#FFD700"
      role: "备选强调色（每个项目择一）"
  neutral:
    - name: "暖灰"
      hex: "#8B8680"
      role: "细腻纹理、旧纸质感"

typography:
  display:
    family: "粗体几何无衬线或手绘体"
    weight: "black"
    style: "常为定制，与图像融合"
  body:
    family: "简洁无衬线"
    weight: "medium"
    style: "仅用于辅助演职员表"
  caption:
    family: "与 display 相同"
    weight: "bold"
    style: "融入构图"
  rules:
    - "字体是画面的一部分，而非独立元素"
    - "鼓励定制或改写字形"
    - "字重对比强烈"
    - "字体可碎片化、撕裂或变形"

layout:
  grid: "构图导向，非严格栏格"
  alignment: "居中或强烈对角"
  aspect_ratio: "2.39:1（电影宽银幕）或 16:9"
  notes:
    - "满幅构图"
    - "剪影作为主要视觉元素"
    - "撕纸边缘、剪纸美学"
    - "强对角线制造张力"

motion:
  transitions:
    - "戏剧化揭示"
    - "旋转螺旋（《迷魂记》）"
    - "剪纸动画"
    - "剪影变形"
  animation_style: >
    剧场式揭示。元素有目的地变形与旋转。
    剪纸美学——元素组装与拆解。
    爵士影响下的时序：切分、出其不意、有节奏。
  pacing: "戏剧化、层层蓄力、点睛时刻"
  audio_cues:
    - "爵士配乐"
    - "管弦乐张力"
    - "Bernard Herrmann 风格影响"

mood:
  keywords:
    - "戏剧化"
    - "大胆"
    - "电影感"
    - "图形化"
    - "永恒"
    - "神秘"
  era: "1950–1960 年代好莱坞（历久弥新）"
  cultural_reference: "Saul Bass、《迷魂记》、《桃色血案》、《金臂人》、《惊魂记》"
  avoid:
    - "照片写实画面"
    - "柔和渐变"
    - "多种强调色并用"
    - "通用库存素材"
    - "3D 效果"
    - "镜头光晕"
    - "现代 UI 模式"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: "2e4dfda94a3341fb849571bb7449b4c2"
  orientation: "landscape"
---

## 设计原则

片头序列本身就是电影，而非铺垫。
每一帧都可以是一张海报。
剪影在不露面的情况下揭示人物。
几何造型制造情绪。

## 连接器

### HeyGen Video Agent
原样使用 `style_prompt_full`。强调：剪影、大胆造型、
戏剧化揭示。剪纸美学。爵士影响下的时序。
不使用数字人——纯图形化电影。

### HTML Slides
黑底配纯白与单一强调色。满幅剪影。
与画面融合的戏剧化字体。强对角构图。

### paper.design
造型优先于照片写实。剪影作为主要元素。
字体与图像统一构图。撕纸边缘效果。

### Figma
颜色样式：`brand/deep-black`、`brand/stark-white`、`accent/bass-orange`。
将剪影形状做成可复用组件。
定制字体处理优于标准文本样式。
