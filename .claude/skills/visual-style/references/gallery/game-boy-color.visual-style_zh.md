---
name: "Game Boy Color"
version: "1.0"
tags:
  - pixel retro
  - gaming
author: "Visual Style Gallery"
created: "2026-03-12"

style_prompt_short: >
  90 年代末掌机怀旧感。有限色板、粗块像素、
  口袋里的便携冒险。

style_prompt_full: >
  90 年代末 Game Boy Color（GBC）美学。每场景有限色板
  （原版 56 色，精灵图常用 4–10 色）。
  典型 GBC 配色：标志性的青绿渐变（#0F380F 至
  #9BBC0F）、紫色外壳（#663399）、浆果色（#CC3366）、青绿
  （#339999）、原子紫（#6B3FA0）。低分辨率粗块像素
  （原生 160×144）。用抖动（dithering）图案做明暗。
  低帧率简单精灵动画（10–15fps）。UI 带有 GBC 特色边框。
  音效设计为 chiptune——四声道音频美学。便携、多彩、讨喜。
  比初代 Game Boy 限制少，但仍明显受约束。
  参考：《宝可梦 水晶版》《塞尔达传说 梦见岛 DX》《瓦力欧 Land 3》。

colors:
  primary:
    - name: "GBC Dark Green"
      hex: "#0F380F"
      role: "最深色、描边"
    - name: "GBC Light Green"
      hex: "#9BBC0F"
      role: "最亮色、高光"
  accent:
    - name: "GBC Purple"
      hex: "#663399"
      role: "原版外壳色、品牌强调色"
    - name: "Berry Pink"
      hex: "#CC3366"
      role: "浆果色外壳变体"
    - name: "Teal"
      hex: "#339999"
      role: "青绿外壳变体"
    - name: "Atomic Purple"
      hex: "#6B3FA0"
      role: "原子紫外壳、特殊强调"
  neutral:
    - name: "GBC Mid Green"
      hex: "#306230"
      role: "中间调、次要元素"
    - name: "GBC Pale Green"
      hex: "#8BAC0F"
      role: "浅中间调"

typography:
  display:
    family: "Pixel font (8x8 or 16x16)"
    weight: "regular (pixels are pixels)"
    style: "大写或混合，粗块字形"
  body:
    family: "Pixel font"
    weight: "regular"
    style: "对话框风格"
  caption:
    family: "Pixel font"
    weight: "regular"
    style: "小号、菜单文字"
  rules:
    - "所有文字须像素对齐"
    - "有限字符集（如真实 GBC）"
    - "带特色边框的文本框"
    - "文字逐字显示"

layout:
  grid: "8-pixel base unit"
  alignment: "菜单居中、对话左对齐"
  aspect_ratio: "10:9 (GBC native) or 16:9 (modern)"
  notes:
    - "原生 160×144，等比整数倍放大"
    - "HUD 元素贴屏幕边缘"
    - "对话框位于下三分之一"
    - "基于精灵图构图"

motion:
  transitions:
    - "划像转场（圆形、水平、垂直）"
    - "调色板淡入（至白或黑）"
    - "无平滑过渡"
  animation_style: >
    低帧率精灵动画（10–15fps）。两帧行走循环。
    场景切换为即时或经典划像。
    UI 元素出现/消失，不做淡入淡出。
  pacing: "快速、跟手、游戏感"
  audio_cues:
    - "chiptune（芯片音乐）"
    - "四声道音频"
    - "8-bit 音效"
    - "菜单哔哔声与 bloop 声"

mood:
  keywords:
    - "怀旧"
    - "便携"
    - "多彩"
    - "讨喜"
    - "俏皮"
    - "冒险"
  era: "1998-2003"
  cultural_reference: "《宝可梦 水晶版》《塞尔达传说 梦见岛 DX》《瓦力欧 Land 3》、Game Boy Color 硬件"
  avoid:
    - "平滑渐变"
    - "高分辨率画面"
    - "写实元素"
    - "现代 UI 模式"
    - "总色数超过 56"
    - "平滑动画"
    - "抗锯齿"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: "94e43f67cbe546b783e1f5c6f2b66125"
  orientation: "landscape"
---

## 设计原则

约束催生创意。
在 160×144 里每一像素都算数。
颜色是稀缺资源——要有意使用。
魅力来自角色感，而非复杂度。

## 连接器

### HeyGen Video Agent
原样使用 `style_prompt_full`。强调：粗块像素、有限配色、
低帧率动画。划像式转场。Chiptune 音效美学。
不要平滑运动——一切均为离散的像素步进。

### HTML Slides
使用像素字体（Press Start 2P、VT323）。图形仅按整数倍
缩放（2x、3x、4x）以保持像素锐利。默认 GBC 绿色色板，
外壳色作强调。对话框边框。

### paper.design
低分辨率设计再放大。使用 GBC 色板。
抖动图案做明暗。基于精灵图构图。
所有元素对齐 8 像素网格。

### Figma
颜色样式：`gbc/dark-green`、`gbc/mid-green`、`gbc/pale-green`、`gbc/light-green`，
及外壳色变体。8×8 像素网格。使用像素字体或
自行设计像素字体。导出时禁用抗锯齿。
