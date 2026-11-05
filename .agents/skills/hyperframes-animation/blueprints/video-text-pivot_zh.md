# video-text-pivot — 视频 → 文字轴心

**intent**：产品视频居中夺眼，随后滑开让位，把视觉重心交给腾出的空间中的 hero 统计数字，然后视频与数字一并清场，动感文字逐字打入中央——强调词承载视频曾承载的含义——最后用渐变 pill 盖章。弧线为「展示 → 让位 → 轴心 → 盖章」，每次交接都是退场与同锚点入场配对，读起来是两个节拍而非四个。

**roles served**

- Product_Intro（来自 `metric-video-text-pivot`）：开场是「先看功能」再「看影响」，且 `[product video]` 在统计数字 reveal 全程保持可见——它是滑开，不是硬切。
- Key_Feature：功能片段让位于铺满画面的 metric 与排印 impact 行。

**duration**：6–8s

**shot structure**（`[bg]` 画布；一条 `[product video]` 为真实静音 `.mp4` 片段、一个 hero stat、随后 kinetic 文字——每对共用屏幕锚点，让交接读成重心转移）

- **Scene 1（0.0–~1.6s）— 视频登场。** `[product video]` 居中 smooth scale-up 落地并呼吸（小幅 y-bob），占满注意力。镜头 static。
- **Scene 2（~1.6–3.2s）— 让位 + stat（招牌动作）。** 视频 SLIDE 侧移（x + scale down）**进入** `[hero stat]` 此刻填满的**同一空间**，stat 以 3D-depth 字效 pop in——一次重心转移读成单一事件，而非两次。stat 在此窗口内呼吸。
- **Scene 3（~3.2–5.0s）— 轴心转向文字。** 视频与 stat 一并清场，kinetic `[impact text]` 在腾出的中央 TYPES 入场，逐字；其 `[accent words]` 承载视频曾承载的含义。
- **Scene 4（~5.0–end）— 盖章。** 渐变 `[pill]` 在收束句周围 scaleX snap 合拢（`scaleX` 0→1），glow halo 晚一拍 resolve，轮廓先于 bloom 可读——把陈述封成单一图形。Hold。

**motion vocabulary**：video scale-in + 小幅 breath；weight-transfer slide（video x + scale-down 在同锚点交给 stat）；3D-depth stat type；character-stream typing；gradient pill scaleX-snap；glow-halo bloom 尾随 silhouette。

**rule mapping**

- video entrance（smooth）与 weight-transfer slide → `gsap-effects`（scale/opacity 随后 x + scale，long-tail `power3`）；video 本身为 root 下静音 `<video class="clip">` 直接子节点
- hero stat 铺满画面的 3D 字 → `3d-text-depth-layers`（static-depth 变体——setup 时建层，无 cascade 与入场打架）
- 同锚点 video-exit ↔ stat-entry 交接（若作 morph）→ `scale-swap-transition`（shared center）
- 经 segmented spans 逐字 impact typing → `dynamic-content-sequencing`（干净 character stream）或 `discrete-text-sequence`
- pill `scaleX` snap + 尾随 glow halo → `gsap-effects`（scaleX）+ `ambient-glow-bloom`（halo，晚一拍 resolve）
- video / stat 在各自窗口内 breath → `sine-wave-loop`（低振幅档—— subtle jitter， gated 到各元素窗口，非 forever loop）

**camera modifier**：camera-static——所有动效在元素空间（video 平移），故「轴心」是元素在动，不是镜头。
