# OpenMontage 中的 GSAP 技能

> **范围：** 本目录没有 `SKILL.md` — **不可**作为可加载技能。本文件是八个可加载 `gsap-*` 技能（位于同级目录 `gsap-core`、`gsap-timeline` 等）的导航图。阅读本文件以找到合适的 `gsap-*` 技能；Agent 加载的是那些技能，而非本 README。

八个 Layer 3 技能，用于教 Agent 正确使用 GSAP（GreenSock Animation Platform）。来源：[greensock/gsap-skills](https://github.com/greensock/gsap-skills)，MIT 许可。

## 为何本仓库包含 GSAP

OpenMontage 目前并不直接使用 GSAP — Remotion 合成由 `useCurrentFrame()` + `interpolate()` + `spring()` 驱动。GSAP 在以下两种具体场景中变得相关：

1. **在 Remotion 组件内进行高级文本 / SVG / 运动路径动画。** GSAP 的插件族（SplitText、MorphSVG、DrawSVG、MotionPath、CustomEase）可解决用原始 `interpolate()` 手写很痛苦的问题。当你需要逐字符揭示、沿 SVG 的曲线相机路径，或在两个任意形状之间 morph — 请使用 GSAP。
2. **HyperFrames 合成。** HyperFrames 是 OpenMontage 中的生产级合成运行时（通过 `hyperframes_compose` 渲染；见 `skills/core/hyperframes.md` 与 `AGENT_GUIDE.md`）。GSAP 通过 Frame Adapter 模式是其原生动画运行时 — 时间轴在创建时暂停并注册到 `window.__timelines`，引擎逐帧 seek。GSAP 时间轴编写是 HyperFrames 场景的 day-1 技能。

## 何时阅读哪一份

| 你在做… | 先读 |
|---|---|
| 任何 GSAP 动画，从零开始 | [`gsap-core`](../gsap-core/SKILL.md) |
| 多步序列或编排 | [`gsap-timeline`](../gsap-timeline/SKILL.md) |
| 逐词或逐字符文本动画 | [`gsap-plugins`](../gsap-plugins/SKILL.md)（SplitText 章节） |
| SVG 形状 morph | [`gsap-plugins`](../gsap-plugins/SKILL.md)（MorphSVG 章节） |
| 物体沿曲线路径运动 | [`gsap-plugins`](../gsap-plugins/SKILL.md)（MotionPath 章节） |
| 自定义贝塞尔缓动 | [`gsap-plugins`](../gsap-plugins/SKILL.md)（CustomEase 章节） |
| React 组件内的 GSAP（Remotion） | [`gsap-react`](../gsap-react/SKILL.md) |
| 数学辅助（clamp、mapRange、interpolate、random） | [`gsap-utils`](../gsap-utils/SKILL.md) |
| 调试慢动画 | [`gsap-performance`](../gsap-performance/SKILL.md) |
| 滚动驱动动画（仅 Web 预览，非视频渲染） | [`gsap-scrolltrigger`](../gsap-scrolltrigger/SKILL.md) |
| Vue / Svelte / 非 React 宿主 | [`gsap-frameworks`](../gsap-frameworks/SKILL.md) |

## 如何从 Layer 2 发现这些技能

这些技能不会自动触发。触发点：

- **`skills/meta/animation-runtime-selector.md`** — 调度元技能。编写任何动画场景时先读它；它会根据你需要的运动类型路由到正确的 Layer 3 技能。
- **流水线 asset-director 技能** — `animated-explainer`、`animation` 与 `cinematic` 流水线在适用处引用这些技能（文本用 SplitText、Logo 用 MorphSVG、相机移动用 MotionPath）。
- **`hyperframes_compose` 工具** — 声明 `agent_skills: ["gsap-timeline", "gsap-core"]`，以便 Agent 在编写 HyperFrames 合成前自动读取它们。

## 在 Remotion 内确定性运行 GSAP

标准 GSAP 通过 `requestAnimationFrame` 驱动动画 — 非确定性，与 Remotion 不兼容。要在 Remotion 组件内使用 GSAP：

- **创建时暂停时间轴**：`const tl = gsap.timeline({ paused: true })`
- **由 `useCurrentFrame()` 驱动进度**：`tl.progress(frame / durationInFrames)`
- 或 **按时间 seek**：`tl.seek(frame / fps)` 到特定时刻
- 或 **仅将 GSAP 用作数值计算器** — 通过 `gsap.parseEase(...)` 与 `gsap.utils.interpolate(...)` 调用 tween 数学，在不运行真实动画循环的情况下计算数值

HyperFrames 内部即采用此模式。在 Remotion 内，简单场景优先使用原生 `interpolate()`；当你明确需要 SplitText / MorphSVG / MotionPath / CustomEase 时再使用 GSAP。

## 致谢

Source: https://github.com/greensock/gsap-skills
License: MIT
Copied: 2026-04-16（提交 `{{source_commit}}` — 最新版本见上游）
