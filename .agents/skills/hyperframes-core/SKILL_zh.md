---
name: hyperframes-core
description: HyperFrames 组合契约 — 构建一个可渲染的项目。适用于组合结构、`data-*` 时序属性、`class="clip"`、轨道、子组合、变量、框架托管的媒体播放、确定性渲染规则以及校验。在编写组合 HTML 之前请先阅读。
---

# HyperFrames Core

HyperFrames 从 HTML 渲染视频。组合（composition）是一份 HTML 文件：其 DOM 用 `data-*` 属性声明时序，动画运行时可 seek，媒体播放由框架托管。

本技能是**技术契约** — 如何构建一个 hyperframes 项目。下文是构建指南；各主题的详细说明在 `references/`（索引见下），按需阅读。其他关注点见同级领域技能 — `hyperframes-animation`、`hyperframes-creative`、`hyperframes-media`、`hyperframes-cli`、`hyperframes-registry`。`/hyperframes` 中的能力图说明各技能覆盖范围。

## 参考资料

| 文件                                 | 阅读目的…                                                                                       |
| ------------------------------------ | ------------------------------------------------------------------------------------------------- |
| `references/minimal-composition.md`  | 从最小可渲染组合骨架起步                                                                           |
| `references/composition-patterns.md` | 选择单体 vs 模块化；组织模块化 `index.html`；选择子组合架构类型                                     |
| `references/data-attributes.md`      | 查阅任意 `data-*`（根 / clip / 子组合宿主 / 旧版别名）；使用 `class="clip"`                         |
| `references/tracks-and-clips.md`     | 选择 `data-track-index`、处理同轨重叠 / z-index、相对另一 clip 的时序                               |
| `references/sub-compositions.md`     | 接入子组合（宿主属性、`<template>`、每实例变量）并在其内部做动画                                     |
| `references/variables-and-media.md`  | 声明变量；放置 `<video>`/`<audio>`、设置音量、裁剪                                                   |
| `references/determinism-rules.md`    | 构建可 seek 的时间线；确定性禁止项；可动画属性白名单；布局 / 文本适配                               |
| `references/full-screen-motion.md`   | 用共享背景编写全帧动效                                                                             |
| `references/storyboard-format.md`    | 编写 `STORYBOARD.md` 计划（及解析后的 manifest）                                                   |
| `references/script-format.md`        | 编写可选的锁定旁白 `SCRIPT.md`                                                                     |
| `references/subagent-dispatch.md`    | 将子 agent 调度动词（并行扇出 / 后台 / 等待）映射到你的 harness                                     |
| `references/tailwind.md`             | 在 Tailwind v4 项目中工作（`init --tailwind`；运行时契约与 Studio 的 v3 不同）                       |

动画运行时细节（GSAP API、Lottie、Three.js 等）请见 `hyperframes-animation` → `adapters/<runtime>.md`。

## 构建组合

### 两种根形式（不可互换）

- **Standalone**（顶层 `index.html`）— 根 `<div data-composition-id="…">` 直接位于 `<body>` 内，**无 `<template>` 包裹**（包裹会隐藏全部内容并破坏渲染）。
- **Sub-composition**（通过 `data-composition-src` 加载）— 根**必须**包在 `<template>` 内。

> ⚠ 传输规则：运行时**仅克隆 `<template>` 内容**；外部一切（含 `<head>` 中的样式/脚本）会被丢弃 — 将 `<style>`/`<script>` 放在 template **内部**。
> ⚠ 宿主 id 规则：宿主槽位的 `data-composition-id` 必须与内部 template 的 `data-composition-id` **以及** `window.__timelines["<id>"]` 键**完全一致** — 不得加 `-mount`/`-slot`/`-host` 等后缀。

文件形态、宿主接线与预渲染检查清单 → `references/sub-compositions.md`。

### 根节点必须定尺寸（静默布局 bug）

Standalone 根需要明确的**定尺寸盒子**（`width`/`height` 为 px），且沿祖先链直到 `height:100%` 的元素都必须有已解析的高度 — 否则 flex/`100%` 子项会塌缩到约 0，内容堆在左上角。`lint`/`validate`/`inspect` **不会**发现此问题。骨架示例 → `references/minimal-composition.md`。

### 一条 paused 时间线

每个组合在页面加载时**同步**注册**恰好一条** `gsap.timeline({ paused: true })` 于 `window.__timelines["<id>"]`（键 = 根 `data-composition-id`）。渲染时长 = 根 `data-duration`，而非时间线长度。不要手动将子时间线嵌套进宿主。完整契约（含非 GSAP 运行时）→ `references/determinism-rules.md` + `hyperframes-animation/adapters/`。

### 不可协商的规则（`lint`/`validate`/`inspect` 抓不到的静默 bug）

此处汇总；完整理由见链接参考。不得违反：

- 无渲染时时钟 / 未设种子的 `Math.random` / 网络 / 输入状态；无 `repeat: -1`（使用有限次数）。→ `determinism-rules.md`
- 仅动画视觉属性白名单内的属性；禁止 `display`/`visibility`；勿对后续场景的 clip 使用 `gsap.set`。→ `determinism-rules.md`
- 正文文本中无 `<br>`；变换过的元素须为块级且定尺寸；脉冲式 absolute 装饰须在峰值留 clearance。→ `determinism-rules.md`
- `<video>`/`<audio>` 必须是**宿主根的直接子节点**（切勿放在子组合 `<template>`/包装器内）；播放由框架托管。→ `variables-and-media.md`
- 每个 `id` 在**组装后**整页中必须唯一；子组合内用组合 id 作前缀（`#<id>-hero`）。重复的 `<video>`/`<img>` id 会渲染为**空白** — 生产端通过 `getElementById` 注入帧，跨文件重复会溜过 `lint`。→ `composition-patterns.md`
- 全屏场景填充应放在全出血**子元素**上（`position:absolute; inset:0`），切勿放在组合根本身 — 生产端帧合成可能丢弃根元素自身的 `background`（帧会渲染为**黑**），尽管预览/`snapshot` 显示正确。→ `composition-patterns.md`

## 编辑已有组合

- 先读文件。保留无关的时序、轨道、ID、变量、媒体路径。
- 与现有组合 ID 及时间线键保持一致。
- 新增 clip：选择不重叠的 `data-track-index`，或有意识地调整周围时序。
- 新增子组合：接线宿主前先核对其内部 `data-composition-id`。

## 校验

命令细节见 `hyperframes-cli`

- [ ] `npx hyperframes lint` 通过（0 错误）
- [ ] `npx hyperframes validate` 通过（0 控制台错误）
- [ ] `npx hyperframes inspect` 通过（0 错误）
- [ ] 含子组合的项目：`npx hyperframes snapshot --at <midpoints>` 并目视检查每一帧
- [ ] `npx hyperframes preview` 用于审阅（用户可在 Studio 时间线中编辑任意内容）
- [ ] 仅在用户批准后执行 `npx hyperframes render`
