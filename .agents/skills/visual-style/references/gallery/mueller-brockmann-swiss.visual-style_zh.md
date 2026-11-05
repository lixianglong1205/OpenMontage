---
name: "Josef Müller-Brockmann Swiss International Style"
version: "1.0"
tags:
  - 标志性设计
  - 利落极简
author: "Bin"
source_url: ""
created: "2026-03-12"

style_prompt_short: >
  网格锁定的瑞士式精确。黑白基底搭配电光蓝强调色。仅使用 Helvetica。
  数据可视化为视觉主角。每一帧都贴合数学网格。几何、系统、精确。

style_prompt_full: >
  Josef Müller-Brockmann 瑞士国际主义风格。网格锁定版式，数学级精确。
  黑白基底加单一强调色（电光蓝 #0066FF）。强对角线构图。仅 Helvetica
  字体。数据可视化为英雄元素——动画图表、计数器、网格。每一帧贴合网格。
  转场为横向网格擦除。无有机形态。无渐变。无图库摄影。一切几何、系统、精确。

colors:
  primary:
    - name: "纯黑"
      hex: "#000000"
      role: "主色底、文字、结构元素"
    - name: "纯白"
      hex: "#FFFFFF"
      role: "背景面、负空间"
  accent:
    - name: "电光蓝"
      hex: "#0066FF"
      role: "唯一强调色——数据高亮、关键强调"
  neutral:
    - name: "网格灰"
      hex: "#CCCCCC"
      role: "网格线、次级结构"
    - name: "深灰"
      hex: "#333333"
      role: "辅助文字、次级标签"

typography:
  display:
    family: "Helvetica"
    weight: "bold"
    style: "全大写或句首大写，字距紧凑"
  body:
    family: "Helvetica"
    weight: "regular"
    style: "左对齐、右参差、行距宽松"
  caption:
    family: "Helvetica"
    weight: "light"
    style: "小号、全大写、字距加宽"
  rules:
    - "仅 Helvetica——不得使用其他字体"
    - "字号遵循数学比例尺"
    - "始终左对齐——禁止居中"
    - "字重对比建立层级"

layout:
  grid: "严格模块化网格——12 列"
  alignment: "左对齐、贴合网格"
  aspect_ratio: "16:9"
  notes:
    - "每个元素锁定在网格上"
    - "在正交网格内形成强对角线构图"
    - "数据可视化为视觉主角"

motion:
  transitions:
    - "横向网格擦除"
    - "元素吸附至网格位置"
    - "干净硬切"
  animation_style: >
    几何精确。元素吸附至网格位置。图表系统化动画。计数器机械式跳动。无弹跳。
  pacing: "从容、自信、不仓促"

mood:
  keywords:
    - "精确"
    - "系统化"
    - "权威"
    - "几何"
  era: "1950 年代–1970 年代（历久弥新）"
  cultural_reference: "Müller-Brockmann、《平面设计中的网格系统》、苏黎世学派"
  avoid:
    - "有机或曲线形态"
    - "渐变"
    - "图库摄影"
    - "超过一种强调色"
    - "居中文字"
    - "装饰性元素"
    - "手写或衬线字体"
    - "投影或发光"
    - "圆角"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: ""
  orientation: "landscape"
---

## 设计原则

字体与网格即所需的全部设计元素。
数学关系创造视觉和谐。
克制是至高的精致。
网格不是限制——结构带来自由。

## 连接器

### HeyGen Video Agent
原样使用 `style_prompt_full`。指定：无数字人、无 B-roll——纯动态图形。
场景间硬切。数据可视化应系统化动画。

### HTML Slides
CSS 变量：`--color-bg: #000`、`--color-text: #FFF`、`--color-accent: #0066FF`。
所有文字左对齐。12 列网格。Helvetica 或系统无衬线后备字体。

### paper.design
设置 12 列网格。背景黑、文字白。单一强调色。
每个元素应吸附在网格交点上。

### Figma
颜色样式：`brand/black`、`brand/white`、`accent/electric-blue`、`neutral/grid-gray`。
文字样式：`heading/display`（Helvetica Bold）、`body/default`（Helvetica Regular）。
布局网格：12 列，严格对齐。
