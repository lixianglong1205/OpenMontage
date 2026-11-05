---
name: visual-style
description: |
  通过 visual-style.md 文件创建、提取并应用可移植的视觉设计系统。适用场景：(1) 从零创建 visual-style.md 设计系统，(2) 从网站 URL、视频或 PDF 品牌指南中提取视觉风格，(3) 将视觉风格应用于 HeyGen 视频、HTML 幻灯片、Figma 或 paper.design，(4) 浏览预置视觉风格图库（Swiss、Saul Bass、Game Boy 等），(5) 用户提到「visual style」「design system」「brand style」或「style guide」，(6) 用一致的设计语言为 HeyGen 视频定调。
---

# Visual Style（视觉风格）

创建、提取并应用可移植的视觉设计系统。`visual-style.md` 文件在单一文件中定义颜色、字体、版式、动效与氛围，任何 AI 工具均可直接消费。

## 快速参考

| 模式 | 触发方式 | 作用 |
|------|---------|------|
| **Create（创建）** | 「Create a visual-style.md for...」 | 通过引导式提问从零构建风格 |
| **Extract（提取）** | 「Extract a visual-style.md from [URL/image/video]」 | 分析来源并生成风格文件 |
| **Apply（应用）** | 「Apply this visual-style.md to [tool]」 | 通过指定连接器使用该风格 |
| **Gallery（图库）** | 「Show me available visual styles」 | 浏览并使用示例风格 |

## 默认工作流

### Create（创建）

1. **Gather vibe（收集氛围）** — 询问情绪、时代、参考与灵感
2. **Define colors（定义颜色）** — 主色（至少 2 个）、强调色、中性色，含 hex 值与用途
3. **Set typography（设定字体）** — 展示、正文、说明字体族及字重/样式规则
4. **Layout & motion（版式与动效）** — 网格系统、转场、节奏
5. **Generate（生成）** — 使用 [references/templates/minimal.visual-style.md](references/templates/minimal.visual-style.md) 或 [references/templates/full.visual-style.md](references/templates/full.visual-style.md) 输出完整 `visual-style.md`
6. **Preview（预览）** — 展示小型 HTML 色板或描述视觉效果
7. **Optionally apply（可选应用）** — 询问是否要通过连接器使用

可批量提问：
1. 氛围如何？（情绪关键词、时代、参考）
2. 有指定颜色吗？（或从氛围推导？）
3. 字体偏好？（简洁、编辑感、技术感、 playful？）
4. 将用于什么工具？（HeyGen、幻灯片、paper.design、Figma？）

### Extract（提取）

1. **Receive source（接收来源）** — URL、图片、视频或 PDF
2. **Load extractor（加载提取器）** — 阅读对应的提取器参考文件
3. **Analyze（分析）** — 识别颜色、字体、版式、动效、氛围
4. **Generate（生成）** — 输出完整 `visual-style.md`，并设置 `source_url`
5. **Validate（校验）** — 确保所有必填字段齐全

### Apply（应用）

1. **Read the style（读取风格）** — 加载 `visual-style.md` 文件
2. **Ask which connector（选择连接器）** — 或从上下文推断
3. **Load connector（加载连接器）** — 阅读对应的连接器参考文件
4. **Transform（转换）** — 将风格字段映射为工具专用格式
5. **Generate output（生成输出）** — 产出可直接用于工具的说明或代码

### Gallery（图库）

1. **List styles（列出风格）** — 展示 [references/gallery/](references/gallery/) 中的可用风格
2. **Preview（预览）** — 描述所选风格的视觉特征
3. **Load（加载）** — 阅读完整 `visual-style.md`
4. **Apply（应用）** — 通过连接器使用

## 格式快速参考

### 必填字段

```yaml
name: "Style Name"
version: "1.0"
style_prompt_short: "1-2 sentence elevator pitch"
style_prompt_full: "Detailed generation prompt — THE most important field"
colors:
  primary:
    - name: "Color Name"
      hex: "#000000"
      role: "how this color is used"
```

**`style_prompt_full` 是核心。** 若工具只能读一个字段，就读这个。其余均为结构化数据，供需要更细控制的工具使用。

完整规范：[references/spec.md](references/spec.md)

## 参考文件

### Connectors（Apply 模式）

| 连接器 | 用例 | 文件 |
|-----------|----------|------|
| HeyGen Video Agent | AI 视频生成 | [references/connectors/heygen-video-agent.md](references/connectors/heygen-video-agent.md) |
| HTML Slides | 网页演示 | [references/connectors/html-slides.md](references/connectors/html-slides.md) |
| paper.design | 设计文档 | [references/connectors/paper-design.md](references/connectors/paper-design.md) |
| Figma | 设计工具样式 | [references/connectors/figma.md](references/connectors/figma.md) |

### Extractors（Extract 模式）

| 来源 | 文件 |
|--------|------|
| Website URL | [references/extractors/from-website.md](references/extractors/from-website.md) |
| Video keyframes | [references/extractors/from-video.md](references/extractors/from-video.md) |
| PDF / Brand guide | [references/extractors/from-pdf.md](references/extractors/from-pdf.md) |

### Gallery（预置风格）

| 风格 | 时代 | 文件 |
|-------|-----|------|
| Müller-Brockmann Swiss | 1950s–70s | [references/gallery/mueller-brockmann-swiss.visual-style.md](references/gallery/mueller-brockmann-swiss.visual-style.md) |
| Neville Brody Industrial | Late 1980s–90s | [references/gallery/neville-brody-industrial.visual-style.md](references/gallery/neville-brody-industrial.visual-style.md) |
| Saul Bass Cinematic | 1950s–60s | [references/gallery/saul-bass-cinematic.visual-style.md](references/gallery/saul-bass-cinematic.visual-style.md) |
| Game Boy Color | 1998–2003 | [references/gallery/game-boy-color.visual-style.md](references/gallery/game-boy-color.visual-style.md) |
| HeyGen AI Video | 2020s | [references/gallery/heygen-ai-video.visual-style.md](references/gallery/heygen-ai-video.visual-style.md) |

### Templates & Spec（模板与规范）

- [references/templates/minimal.visual-style.md](references/templates/minimal.visual-style.md) — 最小模板
- [references/templates/full.visual-style.md](references/templates/full.visual-style.md) — 含全部字段的完整模板
- [references/spec.md](references/spec.md) — 完整格式规范

## 最佳实践

1. **`style_prompt_full` 是核心** — 始终可作为独立生成提示使用
2. **一种风格，一个文件** — 不要打包多种风格
3. **资源用 URL** — 切勿嵌入二进制数据
4. **Show, don't tell（用预览说话）** — 创建风格时生成预览
5. **有主见的默认值，可扩展的扩展项** — 核心 schema 固定；工具专用配置用 `x_*`
