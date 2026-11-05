---
name: "HeyGen AI Video Platform"
version: "1.0"
tags:
  - ai
  - video
  - tech
  - modern
author: "Extracted"
source_url: "https://heygen.com"
created: "2026-03-12"

style_prompt_short: >
  充满活力的 AI 导向设计。干净白底上的青到粉渐变能量。
  亲切易用的科技质感，高级而不冰冷。

style_prompt_full: >
  受 HeyGen 启发的现代 AI 视频平台美学。干净白色背景与充裕留白。
  标志性青粉渐变（#00C3FF 至 #95AAFE 至 #FEA5FE）作为核心视觉元素。
  主强调色 Hey Blue（#00C3FF）用于 CTA 与交互元素。Prism Pink（#F3A6FF）
  作为次要强调色，用于突出与温暖感。字体采用几何无衬线（ABC Solar、
  TT Norms Pro 或类似），层级清晰。卡片与按钮采用大圆角（12–48px）。
  平滑淡入动画与轻微悬停过渡。科技前沿而亲切——创新遇见可及性。
  避免生硬的企业蓝、除非明确要求否则避免暗色模式、避免过于复杂的渐变或 3D 效果。

colors:
  primary:
    - name: "Pure White"
      hex: "#FFFFFF"
      role: "主背景、干净画布"
    - name: "Carbon"
      hex: "#333333"
      role: "正文、标题"
  accent:
    - name: "Hey Blue"
      hex: "#00C3FF"
      role: "CTA、链接、主品牌强调"
    - name: "Prism Pink"
      hex: "#F3A6FF"
      role: "次要强调、渐变端点、重点"
    - name: "Gen Green"
      hex: "#35C838"
      role: "成功状态、正向反馈"
  neutral:
    - name: "Mist"
      hex: "#F2F2F2"
      role: "区块背景、卡片"
    - name: "Cloud"
      hex: "#D9D9D9"
      role: "边框、分隔线"
    - name: "Deep Teal"
      hex: "#033337"
      role: "深色背景、页脚、对比区块"

typography:
  display:
    family: "ABC Solar, TT Norms Pro, system-ui"
    weight: "700-800"
    style: "大号、自信、字距宽松"
  body:
    family: "TT Norms Pro, system-ui, sans-serif"
    weight: "400-500"
    style: "舒适阅读，18px 基准"
  caption:
    family: "TT Norms Pro, system-ui, sans-serif"
    weight: "500"
    style: "14–15px，标签用中等字重"
  rules:
    - "字号阶梯：80px → 60px → 44px → 32px → 24px → 18px → 14px"
    - "行高充裕，便于阅读"
    - "UI 元素用中等字重（500–600）"
    - "仅标题使用粗体（700–800）"

layout:
  grid: "12 列，最大宽度 1200px，基于 flex"
  alignment: "区块居中，内容左对齐"
  aspect_ratio: "视频内容 16:9，功能区比例多样"
  notes:
    - "4px 基准间距单位（8、16、24、32、40、60、80px 阶梯）"
    - "大圆角：卡片 12px，按钮 20px，主视觉元素 48px"
    - "内边距充裕：内部 16–24px，区块间距 60–120px"
    - "卡片细边框，阴影极轻"

motion:
  transitions:
    - "fadeInUp（300ms）用于内容显现"
    - "slideDown（250ms）用于下拉"
    - "平滑悬停过渡（150–200ms）"
  animation_style: >
    平滑现代。元素优雅淡入与滑入。悬停时轻微缩放。
    不弹跳、不幼稚——自信专业，带一点精致感。
  pacing: "快速、响应及时、现代感"
  audio_cues:
    - "electronic ambient"
    - "modern corporate"
    - "upbeat but professional"

mood:
  keywords:
    - "创新"
    - "亲切"
    - "高级"
    - "现代"
    - "创意"
    - "科技前沿"
  era: "2020 年代 AI/SaaS"
  cultural_reference: "现代 AI 工具、创意科技平台、Figma/Notion 式活力"
  avoid:
    - "生硬的企业蓝"
    - "沉重暗色界面"
    - "过于复杂的 3D 效果"
    - "图库摄影感"
    - "杂乱布局"
    - "过小、拥挤的字体"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  brand_gradient: "linear-gradient(328deg, #00c3ff, #95aafe 50%, #fea5fe)"
  orientation: "landscape"
---

## 设计原则

AI 应让人感觉可及，而非令人生畏。
留白传达高级品质。
青粉渐变是主角——少用但要用得大胆。
每次交互都应平滑、响应及时。

## 提取说明

2026-03-12 从 https://heygen.com 提取。
主色采样自 CSS 变量与品牌指南。
字体通过计算样式识别（ABC Solar、TT Norms Pro）。
渐变提取自主视觉区与品牌元素。
间距系统遵循 4px 基准单位。

## 连接器

### HeyGen Video Agent
将标志性渐变用作背景或叠加元素。
Hey Blue 用于文字强调与 CTA。干净白底。
现代、自信的节奏。亲切的 AI 气质。

### HTML Slides
白底配合渐变强调条或主视觉元素。
卡片大圆角。留白充裕。
Hey Blue 用于交互，Prism Pink 用于高亮。

### paper.design
干净布局，渐变作为醒目强调元素。
大字号、层级清晰。圆角卡片模式。
避免重阴影——改用轻微边框。

### Figma
颜色样式：`brand/hey-blue`、`brand/prism-pink`、`brand/gradient`。
文本样式遵循 80-60-44-32-24-18-14px 阶梯。
组件变体大圆角（12–48px）。
