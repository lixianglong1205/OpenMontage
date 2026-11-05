# 确定性、动画运行时与布局

HyperFrames 逐帧渲染合成。每一帧必须仅由其时间值即可复现——相同输入时间 → 相同像素。三项契约共同保证这一点：**动画运行时契约**、**确定性规则**与**布局契约**。

## 动画运行时契约

GSAP 是主要运行时。核心要求是通用的：动画状态必须能从 HyperFrames 时间进行 seek。

对于 GSAP：

- 在页面初始化期间**同步**创建时间线。
- 使用 `gsap.timeline({ paused: true })`。
- 将其注册到 `window.__timelines["<composition-id>"]`。
- 键必须与合成根节点上的 `data-composition-id` 一致。
- **不要**为渲染关键的运动调用 `tl.play()`。
- **不要**在 `async`、`Promise`、`setTimeout` 或事件处理器内构建时间线——渲染器可能在它们完成之前就采样。
- **不要**仅为了设置时长而创建空 tween；改用 clip 上的 `data-duration`。
- **不要**对后续场景中的 clip 元素使用 `gsap.set()`——页面加载时它们尚不在 DOM 中。在 clip 的 `data-start` 时刻或之后，在时间线内使用 `tl.set(selector, vars, time)`。

tween 语法、位置参数、ease 与性能规则请参阅 `hyperframes-animation` 技能。

## 确定性规则

渲染帧必须能从请求的时间复现。**不要**将以下任何项用于视觉状态：

- `Date.now()`、`performance.now()` 或任何渲染时刻钟。
- 未设种子的 `Math.random()`。若需要看似随机的布局，请使用带种子的 PRNG。
- 为必需资源在渲染时进行网络请求。应内联或预打包它们。
- 悬停、滚动、指针或焦点状态。渲染器没有输入事件。
- 诸如 `repeat: -1` 的无限循环。计算有限次数：`repeat: Math.max(0, Math.floor(duration / cycleDuration) - 1)`——使用 **`floor`，而非 `ceil`**（`ceil` 会超出 `data-duration` 并触发 `gsap_repeat_ceil_overshoot` lint；`max(0, …)` 可避免负 repeat = 无限）。

还应避免：

- 对视觉属性允许列表之外的任何属性做动画：`opacity`、`x`、`y`、`scale`、`rotation`、`color`、`backgroundColor`、`borderRadius`、transform。永远不要对 `display` 或 `visibility` 做动画——改用 opacity/transform 与按时的 clip 可见性。
- 在同一时刻从多个时间线对同一元素的同一属性做动画——GSAP 的 overwrite 行为依赖顺序，可能在不同渲染之间翻转。

## 布局契约

先在静态 HTML 与 CSS 中构建可见的最终状态，再在该状态之间做 from/to 动画。

- 合成根节点具有固定的像素帧尺寸。
- 场景容器应通过 `width: 100%; height: 100%; box-sizing: border-box` 填满场景。
- 使用 padding、flex、grid 与 `max-width` 做布局。当布局容器能胜任时，避免用硬编码的 `top`/`left` 偏移定位主内容。
- 对图层与装饰元素使用 `position: absolute`，不要将其作为默认的内容布局策略。
- 动画优先使用 transform 与 opacity。
- 将文本保留在其预期容器内。对于动态文本，使用 `max-width`、换行，或 `window.__hyperframes.fitTextFontSize(text, { maxWidth, fontFamily, fontWeight })`。
- 在不触发 DOM reflow 的情况下测量文本，使用 `window.__hyperframes.pretext`：`pretext.prepare(text, font)` 然后 `pretext.layout(prepared, maxWidth, lineHeight)`。纯算术运算，每次调用约 0.0002 ms——适用于逐帧文本 reflow、shrinkwrap 容器以及在渲染前计算布局。`fitTextFontSize` 基于它实现。
- **不要**在正文文本中使用 `<br>`。强制换行会忽略实际渲染的字宽，并在行已自然换行时产生额外断行，导致重叠。通过 `max-width` 让文本换行。例外：短展示标题，每个词刻意独占一行。
- **带 transform 的元素必须是块级且有尺寸。** 在 inline 的 `<span>` 上 `transform`/`scaleX`/`scaleY` 无效，缩放 auto-width（0px）元素则不可见 → 条形/填充消失。为其设置 `display: block`/`inline-block`/flex 子项**并**赋予真实的 `width`/`height`（例如在已设定尺寸的父级内 `width: 100%`）。_（静默问题——lint/inspect 可能漏检。）_
- **绝对定位且会脉冲或 overshoot 的装饰元素**（`yoyo` scale、`back.out`）在**峰值**尺寸时需要留白，且不得跨在 `overflow: hidden` 边缘——否则会与相邻元素重叠或被裁切。按最大帧定位，而非静止态。_（静默问题。）_

## 为何重要

渲染器接收时间值并产出像素缓冲。不存在「播放」概念——每一帧都是一次全新的 seek。任何依赖「通过先前帧到达本帧」的状态（定时器、累积状态、事件驱动动画）在渲染器乱序或并行采样时都会失步。

若你发现自己要用 `setTimeout`、`requestAnimationFrame` 或 `addEventListener` 驱动视觉效果，请改为在时间线上重建为 tween。
