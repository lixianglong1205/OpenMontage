# overwhelm-surround — 压迫感 / 逼近

**intent**：通过堆积传达压迫感。可识别的主体依次组装，密度标记物飞入以放大「看有多少」，随后中央主体变形为观众自身的 `[avatar]`，元素从**四面八方**逼近——画面应呈现被包围感，而非镜头推近。情绪弧线为：识别 → 幽闭恐惧。

**roles served**

- Problem（来自 `problem-mockup-overwhelm`）：当问题节拍需先呈现「工具太多 / 界面面积太大」，再把**观众置于其中**——主体字面替换（产品 → 人），随后逼近感应具侵入性。适用于痛点是「你被淹没了」，而非「这项指标很差」（后者用 `dataviz-countup`）。

**duration**：6–9s

**shot structure**（`[bg]` 画布；先呈现可识别界面，再露出观众 avatar，最后径向 crowd）

- **Scene 1（0.0–~1.6s）— 可识别组装。** 三个 `[product mockups / surfaces]`  stagger 缩放入场，组装成观众能认出的整体——**中央**为全尺寸，两侧略小（约 0.86）。各自带低幅度 float，像活场景而非静态拼贴。镜头静止。
- **Scene 2（~1.6–3.0s）— 密度放大。** `[platform icons / logos]` 在 mockup 周围 stagger 飞入，纯作**密度标记**——强调「界面面积有多大」，而非动画仪表盘。
- **Scene 3（~3.0–4.6s）— 变形（signature move）。** 中央 mockup **变形**：内容淡出，容器 reshape，观众 `[avatar]` 在**下方**显露——主体字面替换，产品 → 人。
- **Scene 4（~4.6–end）— 逼近。** `[task bubbles / demands]` 从**各方向**向 avatar 径向 stagger 入场。Avatar **保持不动**，气泡侵入——幽闭感来自被包围，而非镜头 push。定格于拥挤状态。

**motion vocabulary**：stagger 缩放入场组装；保留 resting scale 的低幅度 float；密度标记 icon 飞散；内容淡出 → 容器 reshape → 下方 reveal anchor 变形；自各方位径向逼近入场；定格拥挤终态。

**rule mapping**

- stagger mockup + icon 入场（smooth settle 至 resting scale）→ `spring-pop-entrance`（smooth-settle register），由 `gsap-effects` 支撑
- 平台 icon 作密度标记（位置预烘焙，仅 scale/opacity——**非**内部部件动画）→ `svg-icon-enrichment`（仅其 DOM contract）
- 中央 mockup → avatar 变形（HF 禁止 `width`/`height` tween → 用 `scaleX`/`scaleY` 驱动 reshape，anchor = 下方渲染的 avatar 层）→ `card-morph-anchor`
- 径向 bubble 逼近（位置经 `cos`/`sin` 一次性烘焙，stagger 入场）→ `gsap-effects`（径向布局）+ `spring-pop-entrance`（逐 bubble 到达）
- 背景 mockup/icon 低幅度 float → `sine-wave-loop`（低幅度 register—— subtle jitter 叠在各元素 resting scale 上，绝不用 `fromTo` yoyo 重 tween 回起点）

**camera modifier**：camera-static——逼近须读成世界挤向主体，故画面固定；推镜会把「被包围」变成「被放大」，破坏幽闭感。
