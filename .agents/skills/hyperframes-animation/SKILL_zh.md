---
name: hyperframes-animation
description: "HyperFrames 的全部动画知识 — 原子动效规则、多阶段场景蓝图、场景转场、更广泛的动效设计技巧，以及七种运行时适配器（默认 GSAP，另有 Lottie、Three.js、Anime.js、CSS keyframes、Web Animations API、TypeGPU）。适用于任何动效或动画任务：选取 2–4 条规则组合，或加载蓝图，或查阅运行时专用 API（如 GSAP 缓动 / Lottie 播放器 / Three.js mixer）。HyperFrames 原生：单一暂停时间轴、可 seek、确定性。"
---

# HyperFrames Animation

本技能集中所有动效知识：**rules**（原子配方）、**blueprints**（多阶段场景模板）、**transitions**（场景间转场）、**techniques**（更广泛的动效设计模式）以及 **adapters**（各运行时 API）。

组合契约（data 属性、子组合、确定性）见 `hyperframes-core`。

## 默认：组合原子规则

从 `rules-index.md` 中选取 2–4 条规则，用单一暂停的 GSAP 时间轴串联即可。这比从蓝图起步更快，代码也更少。

## 何时加载蓝图

- 场景与现有预设计多阶段模板（品牌揭示、社会证明等）匹配，复用其阶段流水线能显著节省创作时间
- 你需要复杂 4–5 阶段编排的可运行参考代码

蓝图位于 `blueprints-index.md`。每条入口指向 `blueprints/<id>.md`（配方）。勿在未确定需要前预先阅读；仅在已确定需要场景级编排时再加载。

## 路由

| 想要…                                                                       | 阅读                                                |
| ------------------------------------------------------------------------------ | --------------------------------------------------- |
| 按触发器 / 标签选取原子动效模式                                 | `rules-index.md`                                    |
| 阅读某条规则的完整 HTML / CSS / GSAP 配方                                  | `rules/<name>.md`                                   |
| 选取多阶段场景模板                                              | `blueprints-index.md`                               |
| 阅读某蓝图的完整配方                                               | `blueprints/<id>.md`                                |
| 编写场景转场（CSS 驱动，介于两个片段之间）                      | `transitions/overview.md`、`transitions/catalog.md` |
| 查阅更广泛的动效设计技巧                                      | `techniques.md`                                     |
| 分析现有组合的动画映射                                | `scripts/animation-map.mjs`                         |
| GSAP API — 时间轴 / tween / 位置参数                             | `adapters/gsap.md`                                  |
| GSAP — 即插即用效果配方                                                  | `rules/gsap-effects.md`                             |
| GSAP — 变换 / 性能                                                       | `adapters/gsap-transforms-and-perf.md`              |
| GSAP — 缓动 / 交错                                                         | `adapters/gsap-easing-and-stagger.md`               |
| GSAP — 时间轴 / 标签                                                       | `adapters/gsap-timeline-and-labels.md`              |
| Lottie / dotLottie（After Effects 导出，`window.__hfLottie`）                | `adapters/lottie.md`                                |
| Three.js / WebGL（3D 场景、`AnimationMixer`、`hf-seek`）                      | `adapters/three.md`                                 |
| Anime.js（`window.__hfAnime`）                                                  | `adapters/animejs.md`                               |
| CSS keyframes（`animation-delay` / `play-state` / `fill-mode`）                 | `adapters/css-animations.md`                        |
| Web Animations API（`element.animate()`、`currentTime` seek）                   | `adapters/waapi.md`                                 |
| TypeGPU / WebGPU（`navigator.gpu`、WGSL、compute pipelines）                    | `adapters/typegpu.md`                               |
| HTML 作为纹理 + WebGL/GLSL 后期（通过 `drawElementImage` 捕获 live DOM） | `adapters/html-in-canvas-patterns.md`               |
| 命名文本动画效果（24 个 ID，经外部 `animate-text` skill）        | `adapters/animate-text.md`                          |

## 选择运行时

- **GSAP** 是约 95% 动效工作的默认选择 — 涵盖时间轴编排、变换、缓动、交错。本技能中所有原子规则均基于 GSAP。
- **Lottie** 当资源自带预烘焙时间轴时（通常为 After Effects 导出）。
- **Three.js** 用于 3D 场景、相机运动、着色器驱动画面。
- **Anime.js** 在 GSAP 过重时做轻量 tween。
- **CSS** 用于简单重复母题、装饰、 shimmer — 无 JavaScript 动画开销。
- **WAAPI** 用于不依赖 GSAP 的原生浏览器 keyframes。
- **TypeGPU / WebGPU** 用于 GPU 渲染画布（粒子、liquid glass、自定义着色器）。

同一组合中可并存多种运行时。各运行时将其实例注册到对应的全局对象，以便 HyperFrames 一次 seek 全部。

## 关键约束

**前提条件：`hyperframes-core` → Non-Negotiable Rules**（单一暂停时间轴、`data-duration` 决定时长、禁止 `Math.random` / `Date.now` / `performance.now`、禁止 `repeat: -1`、禁止对后续场景 clip 使用 `gsap.set`、禁止动画 `display` / `visibility`、禁止在 `async` / `setTimeout` / `Promise` 内构建时间轴）。此处不再复述。

在 core 契约之上的动效工艺补充：

- **预计算布局常量** — 切勿在 tween 时刻用 `getBoundingClientRect()` 推导位置。tween 时刻的 DOM 测量会失步，因为渲染器并行采样；在组合 setup 时一次性计算坐标并复用。
- **空间动效仅使用 GSAP 变换别名**（`x`、`y`、`scale`、`rotation`）。Core 的允许列表也允许 `opacity` / `color` / `backgroundColor` / `borderRadius` 用于非空间属性 tween — 但绝不用 `width` / `height` / `top` / `left` 做布局变化。

## Scripts

```bash
node skills/hyperframes-animation/scripts/animation-map.mjs <composition-dir> \
  --out <composition-dir>/.hyperframes/anim-map
```

读取注册在 `window.__timelines` 上的每条 GSAP 时间轴，枚举 tween、采样 bbox、计算标志，输出 `animation-map.json`。创作完成后可用其审计编排（死区、交错一致性、生命周期警告）。

## 另见

- `hyperframes-core` — 组合结构、data 属性、子组合、确定性渲染契约
- `hyperframes-creative` — 调色板、 typography、旁白、节拍规划（非动画创意方向）
- `hyperframes-cli` — `npx hyperframes lint / validate / inspect / preview / render`
