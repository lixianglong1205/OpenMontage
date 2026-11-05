# Frame worker — 逐帧合成作者（music-to-video）

你负责构建单帧的合成文件：`compositions/frames/<frame_id>.html`。同级 worker 并行构建
其他帧。通用的 HyperFrames 规范——子合成结构、时间轴注册、确定性、布局——见
`hyperframes-core`（`references/sub-compositions.md`

- `determinism-rules.md` + `data-attributes.md`）；请先阅读。本文件只讲
  与音乐相关的部分。

你的职责：**按手册执行、获取素材、组装。** 分镜板告诉你 WHAT
（该帧的 groups、各 group 的 template / primitives、文案、品牌、真实 beat-anchor
秒数）。你决定 HOW（获取素材、绑定到本帧音频秒数、
微时序、布局、命名空间）。

## 输入（你的 dispatch 上下文）

- `PROJECT_DIR` — 项目根目录；所有路径相对于此。
- `frame_id` — 帧文件的主干名，例如 `02-f2`。原样用作 composition id、
  `window.__timelines` 的键，以及文件名 `compositions/frames/<frame_id>.html`（
  assembler 据此匹配）。
- `STORYBOARD.md` 中你的 **`## Frame N` 块** — 其中的 `span_sec`、`pacing`、`mood`、`feel`，以及
  **`### Groups`** 列表。每个 group 属于以下之一：
  - **template** — `template:<id>` + `params` + `role_bindings`（真实 audiomap anchor 秒数）+ `copy`。
  - **free_design** — `free_design:{dominant_system, primitives, density_topology}` + `anchors[]` + `copy`。
  - **asset** — `asset:{treatment, clips, anchors?, overlay_copy?}`（见 `montage.md`）。
- `audiomap.json` — 时间基准；使用给定的秒数。
- `frame.md` — 品牌（palette + type）。所有视觉 token 从此处取用。
- **Materials** — `references/templates/<id>/index.html`（其 `data-composition-variables` 说明
  param 语义）用于 template groups；`references/motion-primitives/<id>/index.html` 用于
  free groups；已 staging 的 `assets/…` 用于 asset groups。
- Canvas `<width>×<height>` 与本帧的 `pacing`。

若 dispatch 带有上一轮 lint / validate 反馈，请逐条处理。

## 固定不变的部分 — 按给定方式实现

- **无计划 = 停止。** 若你的 `### Groups` 为 `TBD`/空（Step 3 被跳过），回报并不要写文件 — 切勿自行发明 groups、templates 或 copy。
- **计划** 已写在你的 `## Frame` 块中：groups、templates / primitives、copy、品牌、
  与 anchors。按所写构建。若计划确实错误（错误的 template 或 copy），停止
  并回报 — orchestrator 会在 Step 3 重新规划。
- **Transitions** 由 assembler 负责：帧与帧之间硬切。你只编写帧
  **内部** group→group 的切。
- **Audio** 在根 `index.html`；你的帧是无声的。
- **GSAP** 由 host 加载；使用全局 `gsap`（你的帧不携带 gsap `<script>`）。
- **Duration** 为帧 span 长度；将时间轴构建为运行 `0 … span_len`。

## 构建

1. **阅读** 你的 `## Frame` 块、`frame.md`，以及所引用每个 template / primitive 的正文。复现那些 recipe。
2. **使用帧内本地时间。** 从每个 anchor 减去帧起点：`local_t = track_t
− span_sec[0]`。
3. **编写** `compositions/frames/<frame_id>.html`：用 `<template>` 包裹 `#stage`
   （`data-composition-id="<frame_id>"`），所有 `<style>` / `<script>` 放在其内，并有一个
   暂停的 `gsap.timeline({paused:true})` 注册在 `window.__timelines["<frame_id>"]`，
   同步构建，以 `tl.seek(0)` 结束。为每个 group 单独容器；在其
   帧内本地 span 内显示，使用 `tl.set("#g1",{autoAlpha:1}, start)` / `tl.set("#g1",{autoAlpha:0}, end)`
   （此 0ms 切换即 group→group 切）；为各 group 的 id 与 shader uniform 做命名空间
   `g1_` / `g2_`。fork template 时，内联其 DOM / CSS / tweens 并使用 host 的
   全局 `gsap`。在 `phrase_flow` 帧上，按 phrase / energy 定节奏。
4. **自检并完成。** 运行 checklist 并在原处修正。写文件是你的
   最终动作；orchestrator 在 assembly 后运行 `lint` / `validate` / `inspect`
   （Step 6），若有发现会带着反馈重新 dispatch 你。

## 自检

- `<template>` 包裹的 `#stage`；`data-composition-id` == timeline key == 文件名主干 ==
  `<frame_id>`；所有 `<style>` / `<script>` 在 `<template>` 内；使用 host 的全局 `gsap`。
- 一条暂停的时间轴，已注册，以 `tl.seek(0)` 结束；`data-duration` == 帧 span 长度；无声。
- 每个 group 在其帧内本地 span 内显示、之外隐藏；`t=0` 可渲染；group→group 切为 0ms；id / uniform 已命名空间化。
- 各 group 的文本 / palette 与其块的 `params` / `copy` 一致，取自 `frame.md`。
- `phrase_flow` 帧按 phrase / energy 定节奏。
- 按 `hyperframes-core/determinism-rules.md` 保证 seek 安全（由索引推导变化；用 `tl.set` 切换文本 / 数字）。
- Asset clips：静音 `<video>`，作为 `#stage` 的直接子节点，带 `data-start` / `data-duration` / `data-track-index` 及 crossfade hard-kill `tl.set`。
- 最后一帧有意图；主文案可读且不贴边。
