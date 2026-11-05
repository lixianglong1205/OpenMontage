# dataviz-countup — 数据可视化 / 数字递增

**意图**：让数字与图表成为主角——递增环/数字、趋势图、倾斜统计/卡片网格——镜头穿过（或横向扫过）这些数据「仪器」，最终落在一条英雄指标上，让数据本身承载论证。

**适用角色**

- Problem（来自 `problem-dataviz-pushthrough` / #9 Problem_1）：用逼真的数据仪器量化痛点——递增环 → 趋势图 → 统计网格——镜头依次穿入每个对象并进入下一个， dramatize 不断恶化/大规模问题（「X% 的人正在 struggle with…」）。
- Product_Intro（来自 `product-intro-dataviz-scroll-reveal` / #19 Product_Intro_06）：自信的开场「看结果/看数据」——从 hook 词硬切到透视倾斜的数据可视化卡片网格，然后无手控镜头滚动将一条发光英雄指标落定，同时 kinetic 标语逐词拼合。
- Hook（来自 `hook-counter-burst`）：冷开场只打一条 dramatic 统计——画面从暗空开场，3–5 个主题图标在中心簇状刺入，随后 headline 数字向上 EXPLODE 放大、图标甩向各自锚点（递增与扩散同一 beat），以慢镜头 lean-in 收束。从第 1 帧起即 kinetic。

**时长**：约 4–12s（Hook ~4s · Product_Intro ~6s · Problem ~11–12s）

**镜头结构**
数据可视化场域置于 `[bg color]`（深或浅，柔和角向光晕）；图表/环使用 `[gradient A→B]` 品牌描边；干净 sans-serif 白/深字；底层一条连续镜头运动，横穿 2–3 个数据仪器并解析到英雄指标。每个 beat 一个仪器；镜头承担切镜。

- Scene 1（0.0–Xs）：第一个数据仪器居中建立——`[stat]` 读作英雄。居中粗体数字从 `[start]` 递增到 `[end]`（字号随数值增大），下方 `[stat label]`；配对图形（圆形进度 RING 扫至 `[pct]`、`[gradient]` 描边，或 bar/fill）以同一 ease 入场，数字与图形同一 beat 落定。辅助 `[avatar/object]` 以 spring overshoot 弹入散射发光轨道；`[headline]` 淡入。全程极慢连续 zoom-in。
- Scene 2（Xs–Ys）：镜头穿到下一仪器并该仪器动画——`[gradient]` 趋势线/面积图在网格线上自左向右 DRAW（Problem），或偏心卡片 SCROLL 离场、布局 glide（Product_Intro）。抵达的 `[stat-2]` 数字递增 / 图表解析。
- Scene 3 / Scene N（…–end）：镜头将 `[hero metric card]`（大数字 + 标签 + delta + 上升图表）落至正中心；背后 soft `[accent]` 光晕 bloom；运动达峰后 ease 到更宽 settled 构图，英雄居中、辅助卡片分列两侧。HOLD 最后一帧。

- 变体 — Problem（穿入式，递增环 → 趋势 → 网格）：Scene 1 为居中圆形进度环 + 中心递增数字，散射发光 `[avatar/object]` 轨道。Scene 2 为快速镜头 PUSH-IN 直穿环心（环、数字、轨道元素放大飞出画外）进入圆角 `[card]`，上载 `[stat-2 header]` 与 `[gradient]` 折线图（网格线 + 半透明面积自左向右 draw）；镜头穿过后 settle。Scene 3：镜头 PAN 至第二张 `[card]`，数字递增，内嵌 `[avatar/object]` 网格——子集 dim/blur，其余获得 `[accent]` 圆形 checkmark 徽章 SPRING-POP；镜头 settle 至结尾。仪器间为 z 轴深度穿入式 traversal。
- 变体 — Product_Intro（滚至英雄 + 逐词标语）：短 opener — Scene 0（~0.0–0.85s）：全帧 `[hero-color orb]` 上 bold 白字 `[hook phrase]`；静态 shimmer，然后 HARD CUT。Scene 1 切至略透视 TILTED 的 `[data-viz / product cards]` 网格（图表、热力图、带 delta 与来源脚注的 stat 卡片），居中 `[tagline word 1]`；网格开始 SCROLL（如朝左上），保持 tilt。Scene 2：网格继续 scroll，`[hero metric card]` glide 至正中心、偏心卡片滑离；`[tagline word 1]` translate 离场，`[word 2]` 从画缘 rise in。Scene 3：英雄卡片居中 settle，背后 `[accent]` glow bloom，镜头略 PUSH IN；`[word 2]` 在其旁 hold。Scene 4：`[word 2]` slide out，最终 `[tagline word]` 从对侧 edge 落入仍发光的英雄上方，push-in 达峰。Scene 5：overlay 字清场，镜头 ease BACK OUT 至更宽 settled 倾斜构图——英雄居中带 glow，辅助卡片分列。Traversal 为无手控镜头在倾斜卡片平面上 SCROLL（无 cursor、无点击）+ 逐词 kinetic headline + push-in-then-out 书end。

**运动词汇**
随数值增大的递增数字字号；圆形 progress-ring sweep；growth bar / progress fill；gradient 趋势线 + 面积自左向右 draw；散射发光 avatar/object 的 spring-overshoot pop-in；透视倾斜卡片网格；定向网格 scroll（卡片 glide 进出中心）；hero-card 居中；英雄背后 soft accent glow bloom；慢连续 zoom-in；快速镜头 push-IN / push-THROUGH 仪器中心；卡片间 lateral/vertical pan；gentle push-in 达峰后 ease back out 至更宽 settle；子集 selective dim/blur + spring-pop checkmark 徽章；全帧 hook orb → hard cut；kinetic 标语逐词拼合（每词从画缘 drop/rise，前词 slide out）。

**规则映射**（motion 动词 → `rules/<id>.md`）

- 字号随数值增大的递增数字 → `counting-dynamic-scale`（主文本规则）
- 圆形 progress-ring sweep（环填充）→ `stat-bars-and-fills`（环形态）——绘制机制委托 → `svg-path-draw`
- 数字旁配 growth bars / progress fill → `stat-bars-and-fills`（主数据规则）
- gradient 趋势线 / 面积图自左向右 draw → `svg-path-draw`（路径/线自绘）
- avatar/object 的 spring-overshoot pop-in → `spring-pop-entrance`（弹性 overshoot）；发光 avatar/object 散射环布局 → `avatar-cloud-network`；若持续 drift/orbit → `orbit-3d-entry`
- spring-pop `[accent]` checkmark 徽章 → `spring-pop-entrance`
- 透视倾斜卡片网格（tilt 静态、内容动）→ `3d-page-scroll`
- 倾斜卡片平面定向 scroll（卡片 glide 进出中心）→ `3d-page-scroll`（scroll）+ `viewport-change`（lateral/vertical pan 形态）
- 英雄指标卡片居中（scroll/pan 将目标落至视口中心）→ `coordinate-target-zoom`（目标落至视口中心）/ `viewport-change`
- hook orb 硬切至网格 → `scale-swap-transition`
- kinetic 标语逐词拼合 → `kinetic-beat-slam`（单一 onset 网格，每词 distinct 入场）
- 慢连续 zoom-in + push-THROUGH 仪器 + 卡片间 lateral/vertical pan + push-in-then-out 书end → `multi-phase-camera`（见 camera modifier）
- 英雄卡片背后 soft accent glow BLOOM → `ambient-glow-bloom`（静态英雄元素背后未触发 soft glow/bloom——区别于 `press-release-spring` 的按压触发 glow 与 `asr-keyword-glow` 的按词 timed envelope）
- 网格子集 selective dim/blur（非高亮卡片上的 focus-falloff）→ `depth-of-field-blur`（按元素 blur/dim 以 spotlight 高亮卡片——与 `constellation-hub` 中相同 focus-falloff 规则）

**camera modifier**：镜头是横穿数据仪器的主线——一个由 `multi-phase-camera` 编排的 camera wrapper，每站经 `coordinate-target-zoom` 对准 focal 仪器/卡片。

- Problem — push-THROUGH：慢连续 zoom-in（drift overlay）外加 fast PUSH-IN 直穿一仪器中心进入下一个（`multi-phase-camera`，Steady-push 模式），再 lateral/vertical PAN 至最终卡片。Z 轴深度穿入为 signature（区别于 flat pan-tour）。
- Product_Intro — scroll-to-hero + bookend push：无手控定向 SCROLL 横穿倾斜卡片平面（`3d-page-scroll` scroll / `viewport-change` pan）将英雄卡片落至中心，再 gentle push-in 达峰并 ease BACK OUT 至更宽 settle（`multi-phase-camera`，Bookend-pull 模式）。无 cursor、无点击——由镜头导航。
