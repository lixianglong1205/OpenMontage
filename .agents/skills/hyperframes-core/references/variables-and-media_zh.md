# 变量与媒体

两个独立关注点，归为一组是因为二者都控制「从 HTML 外部流入的内容」：运行时参数（变量）与外部媒体文件（视频/音频）。

## 变量

在 `<html>` 元素上通过 `data-composition-variables` 声明变量。每条声明需要 `id`、`type`、`label` 和 `default`：

```html
<html
  data-composition-variables='[
    {"id":"title","type":"string","label":"Title","default":"Hello"},
    {"id":"accent","type":"color","label":"Accent","default":"#66d9ef"}
  ]'
></html>
```

在初始化阶段一次性读取解析后的值：

```js
const { title, accent } = window.__hyperframes.getVariables();
document.getElementById("title").textContent = title;
document.documentElement.style.setProperty("--accent", accent);
```

### 变量规则

- 支持的类型及其额外选项（由 Studio 编辑 UI 消费）：
  - `string` — 可选 `placeholder`、`maxLength`
  - `number` — 可选 `min`、`max`、`step`、`unit`
  - `color` — 无
  - `boolean` — 无
  - `enum` — **必填** `options: [{ "value": "...", "label": "..." }, ...]`
- 始终提供有意义的 `default` 值，以便在未使用 CLI 覆盖时预览仍可用。
- 在子 composition 宿主上使用 `data-variable-values='{"title":"Pro"}'` 做按实例覆盖。
- 渲染时使用 `npx hyperframes render --variables '{"title":"Q4 Report"}'` 或 `--variables-file` 做覆盖。
- 在 CI 中加入 `--strict-variables`：将未声明的键、类型不匹配、以及不在 `options` 中的 enum 值从警告提升为错误。
- 在 init 时读取一次，不要在每个动画 tick 上读 — 变量在单次渲染过程中不会变化。
- 媒体调色可在 `data-color-grading` JSON 内使用精确的变量引用。整字段可使用 `$gradingPreset` 或 `${gradingIntensity}`；运行时在应用 shader 调色前会从当前 composition 的变量解析。

### 两种 JSON 形态（易混淆）

- `data-composition-variables` 是**声明数组**（schema）：`[{id, type, label, default}, ...]`
- `--variables` 与 `data-variable-values` 是**按 id 键的对象**（值）：`{ title: "Q4", accent: "#fff" }`

## 媒体

**不可协商：`<video>`/`<audio>` 必须是宿主 composition 根节点（`index.html`）的直接子元素。** 运行时只注册并驱动作为根直接子元素的媒体。放在子 composition `<template>` 内、或包在任何中间 `<div>` 里的媒体不会被 seek/解码 → 渲染为空白（纸白）或黑屏。`lint`/`validate`/`inspect` 抓不到这一点；逐帧 `snapshot` 会显示空白面板。

后果：

- 场景专属片段仍放在宿主根上，而不是场景的 sub-comp 里。sub-comp 只保留画框/外壳；媒体是与之间级对齐的宿主元素，叠在其上。
- 子 composition **无法触及或动画宿主元素** — 无论 `document.querySelector("#host-id")` 还是 gsap 选择器字符串（`tl.to("#host-id", …)`）都无法跨边界解析；sub-comp 时间线只能驱动其自身子树。因此 **宿主媒体上所有按场景的运动（scale/opacity/morph/tilt/breathing）必须在 `index.html` 的主时间线上、以全局时间编写**（场景局部时间 + 该场景槽位的 `data-start`）。若无 perspective 父节点却要做 3D tilt，对该元素使用 gsap 的 `transformPerspective`。见 `composition-patterns.md` 原型 B。

`<video>` 必须 muted 且 inline。音频必须是独立的 `<audio>` 元素，即使与视频同源文件。

```html
<video
  id="a-roll"
  class="clip"
  src="assets/demo.mp4"
  data-start="0"
  data-duration="12"
  data-track-index="0"
  muted
  playsinline
></video>

<audio
  id="a-roll-audio"
  src="assets/demo.mp4"
  data-start="0"
  data-duration="12"
  data-track-index="10"
  data-volume="1"
></audio>
```

### 媒体规则

- **不要**在 composition 代码里调用 `video.play()`、`audio.play()`、pause 或 seek。HyperFrames 拥有播放控制权。
- **不要**把媒体放在 sub-comp `<template>` 或任何包装 `<div>` 内 — 只能是宿主根直接子元素（见上），否则永远不会解码。
- **不要**从 sub-comp 时间线驱动宿主媒体 — 无效。在主时间线上以全局时间驱动。
- **不要**动画带时序的媒体元素尺寸；改为动画非时序的包装层。
- **不要**把 video 嵌套在带时序的包装层内。时序放在媒体元素上，或保持包装层不带时序。
- 需要 canvas 捕获或像素检查的外部媒体加上 `crossorigin="anonymous"`。
- 音频始终在单独的 `<audio>` 元素上 — 即使源文件与 `<video>` 相同。`<video>` 静音；`<audio>` 承载声音。
- 音量淡入淡出/ducking 请在时间线上动画 `volume`（`tl.to("#bgm", { volume: 0, duration: 1 }, "outro")`），而不是改 `data-volume`。运行时探测时间线上的 volume 关键帧，在预览与渲染中一致应用；`data-volume` 是没有 tween 的元素上的静态基线。

关于媒体时长：若 `<video>` 和 `<audio>` 的内生长度已知且要用整段，可省略 `data-duration`。否则请显式提供 `data-duration`。
