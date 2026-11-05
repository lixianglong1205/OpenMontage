---
name: hyperframes-gsap-adapter
description: HyperFrames 的 GSAP 动画 API 参考。在 HyperFrames 合成中编写可 seek 的 GSAP 时间轴时使用，涵盖 gsap.to()、from()、fromTo()、set()、时间轴 position 参数、标签、缓动、stagger、有限 repeat 以及 transform 性能。
---

# HyperFrames GSAP

面向 HyperFrames 可 seek 驱动渲染模型的 GSAP 用法。本技能是在 HyperFrames 约束下的 GSAP 参考——框架更广泛的合成约定见 `hyperframes-core`。

## HyperFrames 约定

HyperFrames 通过 `gsap` 运行时适配器控制 GSAP。同步创建暂停的时间轴，在 `window.__timelines` 上注册，键名必须与 `data-composition-id` 完全一致，由 HyperFrames 对其 seek。

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  tl.from(".title", { y: 48, opacity: 0, duration: 0.6, ease: "power3.out" }, 0);
  tl.to(".accent", { scaleX: 1, duration: 0.5, ease: "power2.out" }, 0.25);

  window.__timelines["main"] = tl; // key must equal data-composition-id on the composition root
</script>
```

- 注册键必须与合成根节点的 `data-composition-id` 一致。
- 方括号与点号语法均可注册：`window.__timelines["main"] = tl` 与 `window.__timelines.main = tl` 等价（linter 两种都识别）。当 id 不是合法标识符（例如含 `-`）时必须用方括号形式。
- 不要对渲染关键的运动调用 `tl.play()`。
- 不要在异步代码、定时器或事件处理器内构建时间轴。
- 循环保持有限。HyperFrames 渲染的是有限时长的视频。
- **渲染时长来自合成根上的 `data-duration`，而非 GSAP 时间轴长度。** 不要用空 tween 如 `tl.set({}, {}, 283)` 来「拉长」时间轴。（部分外部文档会写这种技巧；在 HyperFrames 中与 seek 驱动的时长模型冲突——应设置 `data-duration`。）

## 核心 Tween 方法

- **gsap.to(targets, vars)** — 从当前状态动画到 `vars`。最常用。
- **gsap.from(targets, vars)** — 从 `vars` 动画到当前状态（入场）。
- **gsap.fromTo(targets, fromVars, toVars)** — 显式指定起点与终点。
- **gsap.set(targets, vars)** — 立即应用（duration 为 0）。

始终使用 **camelCase** 属性名（例如 `backgroundColor`、`rotationX`）。

## 常用 vars（速查）

- **duration** — 秒（默认 0.5）。
- **delay** — 开始前的延迟（秒）。
- **ease** — `"power1.out"`（默认）、`"power3.inOut"`、`"back.out(1.7)"`、`"elastic.out(1, 0.3)"`、`"none"`。见 `./gsap-easing-and-stagger.md`。
- **stagger** — 数字或对象。见 `./gsap-easing-and-stagger.md`。
- **repeat** — 有限次数；在 HyperFrames 中永远不要 `-1`。根据可见时长计算 repeat 次数。
- **yoyo** — 与 repeat 配合交替方向。
- **overwrite** — `false`（默认）、`true` 或 `"auto"`。
- **immediateRender** — 对 from()/fromTo() 默认 `true`。对同一 property+元素 的后续 tween 设为 `false`。
- **onComplete**、**onStart**、**onUpdate** — 回调。

transform、autoAlpha、clearProps 与 SVG 细节见 `./gsap-transforms-and-perf.md`。

## 可动画属性白名单

HyperFrames 比原生 GSAP 更严格。仅动画化：

- **合成器友好**：`opacity`、`x`、`y`、`scale`、`scaleX`、`scaleY`、`rotation`、`rotationX`、`rotationY`、`skewX`、`skewY`、`transformOrigin`
- **视觉填充**：`color`、`backgroundColor`、`borderColor`、`borderRadius`
- **CSS 变量**：`"--hue": 180` 等。
- **媒体 `volume`**（`<audio>` / `<video>`）：用于淡入淡出/ducking，例如 `tl.to("#bgm", { volume: 0, duration: 1 }, "outro")`。运行时从时间轴探测这些关键帧，在预览与渲染中一致驱动（二者匹配）。这设置的是 _作者_ 音量；无 tween 触及该元素时 `data-volume` 为静态基线。
- **DOM 文本 `innerText`**（数字计数器）：直接 tween，例如 `tl.to(el, { innerText: 100, snap: { innerText: 1 } })` — `snap` 保持整数；GSAP inspector 会识别为计数器。与 `../rules/counting-dynamic-scale.md` 中的 `onUpdate` 代理形式等价；若同一 tween 还需驱动 font-size、区域格式（`toLocaleString`）或后缀，优先使用该代理形式。

**避免**（改用 transform 别名）：

- `width` / `height` / `top` / `left` / `right` / `bottom` / `margin*` / `padding*` — 触发布局 reflow。用 `scaleX/Y`（配合 `transformOrigin`）或 `x` / `y`。

**禁止**（破坏渲染器或片段生命周期）：

- `display`、`visibility` — 不要直接 tween。用 `autoAlpha`（在端点同时设置 opacity + visibility，不 tween 离散属性）。
- 由 `Math.random()`、`Date.now()`、`performance.now()` 或事件处理器驱动的任何内容 — 动画状态必须仅由时间确定性决定。

> **注意：** `docs/guides/gsap-animation.mdx` 的「Supported Properties」列出了 `width`/`height`/`visibility` — 该列表对 HyperFrames 合成规则过于宽松。本白名单为准。完整确定性渲染约定见 `hyperframes-core/references/determinism-rules.md`。

## 参考

- `./gsap-timeline-and-labels.md` — 时间轴创建、position 参数（`+=`、`<`、`>`）、标签、嵌套、子合成 `fromTo` 偏好、播放控制。
- `./gsap-easing-and-stagger.md` — 缓动族、stagger 对象、函数式值、`gsap.matchMedia()`、`gsap.defaults()`。
- `./gsap-transforms-and-perf.md` — transform 别名、autoAlpha、`quickTo`、`will-change`、性能规则。
- `../rules/gsap-effects.md` — 即插即用配方：打字机（含光标 / 退格 / 词轮播）+ 音频可视化（使用 `skills/hyperframes-creative/scripts/extract-audio-data.py`）。

## 最佳实践

- 使用 camelCase 属性名；优先 transform 别名与 autoAlpha。
- 优先时间轴而非带 delay 的链式 tween；使用 position 参数。
- 用 `addLabel()` 添加标签以便可读编排。
- 在时间轴构造函数中传入 defaults。
- 需要控制播放时保存 tween/时间轴的返回值。

## 禁止事项

- 能用 transform 时不要动画化布局属性（`width`/`height`/`top`/`left`）。
- 同一 SVG 元素不要同时使用 `svgOrigin` 与 `transformOrigin`。
- 能用时间轴编排时不要用 `delay` 链式动画。
- DOM 存在之前不要创建 tween。
- HyperFrames 合成中不要使用无限 `repeat: -1` — 根据可见时长计算有限 repeat 次数。

## 致谢与参考

- HyperFrames 适配器源码：`packages/core/src/runtime/adapters/gsap.ts`。
- GSAP 文档：https://gsap.com/docs/v3/
- GSAP 时间轴 pause 与 seek 行为：https://gsap.com/docs/v3/GSAP/Timeline/pause%28%29/
