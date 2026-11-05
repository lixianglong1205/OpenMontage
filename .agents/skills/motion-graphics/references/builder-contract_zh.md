# Builder 契约 — 组合规则（`agents/builder.md` 的详细说明）

## 根节点必须定尺寸

根 `#stage`（`data-composition-id`）需要 `position: relative; width: <W>px; height: <H>px`。若高度未确定，flex 子项会塌缩到约 0，内容堆在左上角 —— 且 `lint`/`inspect` 也检测不到。

## 先布局后动画

1. 确定 **hero frame**（多数元素同时可见的那一帧）→ 先用纯静态 CSS 搭出该帧，不用 GSAP。
2. `.scene-content` 用 padding 撑满场景，不要用偏移：
   ```css
   display: flex;
   flex-direction: column;
   justify-content: center;
   width: 100%;
   height: 100%;
   padding: 120px 160px;
   gap: 24px;
   box-sizing: border-box;
   ```
   勿对内容容器使用 `position:absolute; top:Npx`（会溢出）。绝对定位仅留给装饰元素。保持 ≥80px 内边距（标题安全区）。
3. **入场**：`gsap.from()` 从屏外/不可见 tween 到 CSS 中的位置（子组件内用 `fromTo()`）。CSS 位置是 ground truth；tween 是到达该位置的过程。
4. **出场**：仅最后一个场景把元素 animate 出去；场景之间，转场本身即出场。

## 时间线 / clip 契约

- 在 `window.__timelines["<id>"]` 上仅一个 `gsap.timeline({paused:true})`；`tl.seek(0)`；禁止 `tl.play()`。
- 定时元素：`class="clip"` + `data-start`/`data-duration`/`data-track-index` + 稳定的 `id`。同一全时长 clip 内、由时间线驱动的组不必各自再加 timing 属性。
- 仅确定性逻辑 —— 禁止 `Date.now()` / `Math.random()` / 网络。计数动画通过 `onUpdate` tween 代理对象（可 seek），不要用挂钟计数器。

## 正确性

- **延迟元素的 seek 安全显隐**：先 `gsap.set(el, {autoAlpha:0})`，入场时用 `gsap.to(el, {autoAlpha:1})`（与仅运动的 `from()` 配对）。**不要**用 `set(opacity:1) + from(opacity:0)` 做门控 —— 在暂停/已 seek 的渲染下元素会**永远**不可见（浏览器播放会掩盖；seek-capture 会暴露）。_（Eval 发现。）_
- **计数动画**通过 `onUpdate` tween 代理；仅当宿主在**启用事件**的情况下推进时间线（`tl.time()` / 未抑制的 seek）时才会渲染。裸 `seek(t, true)` 会冻在 0 —— HF 渲染宿主必须以 events on 的方式 seek。_（Eval 发现。）_
- 在 tween 边界处 clamp；不要让 spring  overshoot 超过应保持的值。
- 允许的 ease：`power1–4`、`back`、`bounce`、`circ`、`elastic`、`expo`、`sine`（`.in/.out/.inOut`）。
- 每场景一个 motif。运行 `hyperframes inspect`；有意溢出则标记 `data-layout-allow-overflow="true"`。
- **调色板纪律**：所有颜色定义在一个 `palette` 对象 / CSS 自定义属性中 —— 不要在 markup 里散落 inline hex（`asset-fusion` 时从素材 eyedropper 取色）。
