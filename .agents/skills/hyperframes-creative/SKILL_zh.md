---
name: hyperframes-creative
description: HyperFrames 视频的非动画创意指导。适用于设计规范（frame.md / design.md）处理、调色板、 typography、旁白、节拍规划、音频响应式视觉、构图模式以及品牌/风格决策。原子级动效模式与场景蓝图请使用 `hyperframes-animation`。
---

# HyperFrames 创意

品牌、节奏、风格、旁白与构图方向。在 `hyperframes-core` 的技术契约就位后使用。

动效模式、场景蓝图、转场与 CSS 标记效果请使用 `hyperframes-animation` — 本技能刻意不涉及动画。

> **任何非平凡构图请先阅读以下两篇 — 它们会覆盖网页式直觉：**
>
> - `references/house-style.md` — 「解读提示词、生成真实内容」、惰性默认清单，以及背景/前景层配方。这是把字面换皮变成 _概念_ 的关键。
> - `references/video-composition.md` — 视频媒介密度、尺度、前景元数据（「制作感而非生成感」的细节：数据条、注册标记、等宽读数、每场景 8–10 个元素）。
>
> 跳过这两篇是输出泛化、像网页的最主要原因。它们不是下面路由表里的可选项 — 只要超出单行编辑，在选色或写 HTML 之前务必打开两篇。

## 工作流

1. 若项目有设计规范，**先阅读**并将其 frontmatter 令牌视为品牌真理（颜色、字体、间距、调性、约束）。读哪个文件（优先级 `frame.md` → `design.md` → `DESIGN.md`）以及如何解析（frontmatter = 规范，正文 = 语境）在 [`references/design-spec.md`](references/design-spec.md) 中统一定义 — 按该文档解析并加载。
2. 若无设计规范且用户需要视觉方向，选择一条路径：
   - 现成 frame 预设（可选）→ `frame-presets/`（将 `FRAME.md` 采纳为 `frame.md`；见 `references/design-spec.md`）
   - 具名风格或情绪 → `references/visual-styles.md`
   - 快速默认 → `references/house-style.md`
   - 交互式选择 → `references/design-picker.md`
3. 多场景工作：在写 HTML 之前规划节拍与节奏 → `references/beat-direction.md`。场景转场请跳转 `hyperframes-animation/transitions/`。
4. 动效密集的工作：阅读 `references/motion-principles.md`（高层护栏），再前往 `hyperframes-animation` 查看原子规则。

## 路由

| 主题                                                                     | 阅读                                           |
| ------------------------------------------------------------------------ | ---------------------------------------------- |
| 将现成 frame 预设采纳为 `frame.md`（可选）                               | `frame-presets/` · `references/design-spec.md` |
| 默认调色板、动效、 typography、应质疑的惰性默认                            | `references/house-style.md`                    |
| 具名风格预设、情绪到风格的路由                                           | `references/visual-styles.md`                  |
| 调色板专用颜色令牌                                                       | `palettes/*.md`                                |
| 构图模式 — PiP、文字在主体后、标题卡、幻灯片                              | `references/composition-patterns.md`           |
| 统计 / 信息图呈现                                                        | `references/data-in-motion.md`                 |
| 开放式提示的结构化扩展                                                   | `references/prompt-expansion.md`               |
| 视频媒介密度、尺度、颜色、画面构图                                       | `references/video-composition.md`              |
| 逐节拍方向、节奏规划、转场时机                                           | `references/beat-direction.md`                 |
| 创作后规范核验（颜色、字体、圆角、间距、景深）                             | `references/design-adherence.md`               |
| 高层动效护栏与 GSAP 质量规则                                             | `references/motion-principles.md`              |
| 字体选择、配对、渲染视频 typography 护栏                                 | `references/typography.md`                     |
| 脚本节奏、调性、开场、数字读法                                           | `references/narration.md`                      |
| 预计算音频频段映射到动效                                                 | `references/audio-reactive.md`                 |

## 脚本

- `scripts/contrast-report.mjs` — 检查渲染帧的对比度警告。
- `scripts/extract-audio-data.py` — 为音频响应式构图预提取音频频段。
- `scripts/package-loader.mjs` — 捆绑创意工具链的支持脚本。

在仓库根目录用显式路径运行，例如：

```bash
python skills/hyperframes-creative/scripts/extract-audio-data.py <audio-file>
```

动画分析（`animation-map.mjs`）位于 `hyperframes-animation/scripts/`。

## 边界

- 不得覆盖 `hyperframes-core` 的技术规则。
- 不得为最小技术构图强制要求设计系统。
- 除非请求明确要求，或你先提议扩展，否则不得额外添加场景、旁白、音乐、字幕或转场。
- 配方类引用应任务相关；简单编辑不必读完所有 reference。
