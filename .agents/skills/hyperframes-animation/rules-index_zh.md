# 规则索引

原子级动效配方。每条规则位于 `rules/<name>.md`。每个场景组合 2–4 条，并配合单一暂停时间轴。

## 文本与排版

<rules>
<hacker-flip-3d path="rules/hacker-flip-3d.md">字符级 3D 旋转，配合确定性字形替换（解密效果）。GSAP `back.out` 缓动 + 逐字形 `onUpdate` 实现闪烁哈希。Tags: text, 3d, reveal, decode</hacker-flip-3d>
<vertical-spring-ticker path="rules/vertical-spring-ticker.md">老虎机式纵向滚动：在带遮罩的列内用分步 GSAP 补间实现。Tags: text, ticker, scroll, vertical</vertical-spring-ticker>
<counting-dynamic-scale path="rules/counting-dynamic-scale.md">数值越大字号越大，以强化递进感。对数值代理对象使用单一 GSAP 补间。Tags: counter, scale, font-size, number, dynamic</counting-dynamic-scale>
<discrete-text-sequence path="rules/discrete-text-sequence.md">在时间点阈值处替换整段文本状态，实现非线性打字（错字、停顿、批量插入、退格）。由 GSAP onUpdate 驱动的反向查找。Tags: text, typing, discrete, threshold, non-linear</discrete-text-sequence>
<asr-keyword-glow path="rules/asr-keyword-glow.md">按 ASR 词级时间戳同步关键词的发光、缩放与颜色。每个词两条 GSAP 补间，经 attack-decay-rest 包络驱动 CSS 自定义属性 `--glow`。Tags: asr, audio-sync, highlight, glow, keyword, text</asr-keyword-glow>
<3d-text-depth-layers path="rules/3d-text-depth-layers.md">多层偏移文本（N 个 div，位置 `(i*dx, i*dy)`、透明度递减）在大字号上叠出 3D 挤出错觉。Tags: text, 3d, depth, layers, shadow, typography, stacked</3d-text-depth-layers>
<context-sensitive-cursor path="rules/context-sensitive-cursor.md">打字光标在片段边界切换 `background-color`，并通过 `(tl.time() % cycle) < cycle/2` 实现方波闪烁。Tags: cursor, color, context, typewriter, styling, segment</context-sensitive-cursor>
<dynamic-content-sequencing path="rules/dynamic-content-sequencing.md">由脚本条目 `{textMain, textAccent, charSpeed, hold}` 预计算扁平数组 `[{startTime, endTime, ...}]`。每句窗口 = `chars × charSpeed + hold`。时长由内容驱动，无需手调偏移。Tags: timeline, sequencing, dynamic, duration, script-driven</dynamic-content-sequencing>
<kinetic-beat-slam path="rules/kinetic-beat-slam.md">打击感动态排版——短句在**同一**节拍数组上猛击入场，各句入口形态不同（scale-slam / side-snap / rise-rotate），可选节奏装饰（节拍 tick、节拍条），最后锁定收束。适用于「punchy / rhythmic」标语。Tags: text, kinetic, typography, beat, rhythm, slam, percussive, punchy</kinetic-beat-slam>
</rules>

## 数据与统计

<rules>
<counting-dynamic-scale path="rules/counting-dynamic-scale.md">数值越大字号越大；可 seek 的 `onUpdate`、`Math.round`、`tabular-nums`、多统计和弦。（亦见「文本与排版」。）Tags: counter, number, stat, count-up</counting-dynamic-scale>
<stat-bars-and-fills path="rules/stat-bars-and-fills.md">数字与图形配对的数据可视化基元——增长条（CSS `scaleY` 交错）、进度填充（条 `scaleX` 或测量 SVG 环）、分数星级擦除（`clip-path`）。仅用变换、可 seek。选定单焦点或分屏并保持一致。Tags: data, stats, chart, bars, progress, ring, stars, rating, infographic</stat-bars-and-fills>
</rules>

## 镜头与视口

<rules>
<coordinate-target-zoom path="rules/coordinate-target-zoom.md">通过缩放（外层包裹）+ 反向平移（内层包裹） zoom 到非居中元素。Tags: camera, zoom, scale, translate</coordinate-target-zoom>
<camera-cursor-tracking path="rules/camera-cursor-tracking.md">两阶段虚拟镜头：视口锁定移动焦点（打字光标）——先静态初始构图，再焦点锁定跟踪。在 `document.fonts.ready` 后用浏览器原生 `getBoundingClientRect()` / `ctx.measureText()`。Tags: camera, tracking, viewport, two-phase, typing</camera-cursor-tracking>
<multi-phase-camera path="rules/multi-phase-camera.md">顺序镜头缩放（拉远 / 聚焦 / 推近）加连续微漂移。Tags: camera, zoom, phase, drift, scale, cinematic</multi-phase-camera>
<viewport-change path="rules/viewport-change.md">虚拟镜头——对包含全部场景内容的单一 `.world` 包裹层做变换，模拟 zoom / pan / 焦点锁定。单一元素复合变换 `translate(x,y) scale(S)`；反向平移公式为 `T = -offset × S`（与 coordinate-target-zoom 的 `T = -offset` **不同**）。Tags: viewport, camera, zoom, pan, focus-lock</viewport-change>
<depth-of-field-blur path="rules/depth-of-field-blur.md">选择性 rack-focus——对失焦层用 GSAP 补间 `filter: blur()`（略降 opacity），经 `--dof` 变量驱动，焦点元素保持清晰；单次拉焦、两平面 rack，或推近时模糊簇。有限、确定性、可 seek。Tags: blur, depth-of-field, focus, rack-focus, dim, spotlight</depth-of-field-blur>
</rules>

## 布局与网络

<rules>
<avatar-cloud-network path="rules/avatar-cloud-network.md">头像分布在椭圆环上，SVG 连线至中心点，交错入场。云中心坐标须与中心元素完全一致。Tags: avatar, cloud, network, social-proof, stagger</avatar-cloud-network>
<3d-page-scroll path="rules/3d-page-scroll.md">整页网页渲染为倾斜 3D 卡片，内部内容滚动以露出指定区块。可与 asr-keyword-glow 配合做页内关键词高亮。Tags: 3d, page, scroll, webpage, tilt, perspective, product-demo</3d-page-scroll>
<center-outward-expansion path="rules/center-outward-expansion.md">元素先聚于屏幕中心，再向外扩至最终位置。各元素目标位仅用 CSS 设一次；GSAP 将 transform 的 `x` / `y` 偏移补间至 0，与共享驱动同步。Tags: expansion, scatter, center, reveal, layout, sync</center-outward-expansion>
<split-tilt-cards path="rules/split-tilt-cards.md">两张卡片并排，rotationY 倾斜相反（± baseTilt），自各自一侧滑入。持续浮动相位相反（`Math.PI` 偏移）。Tags: 3d, cards, split, tilt, comparison, symmetric</split-tilt-cards>
<orbit-3d-entry path="rules/orbit-3d-entry.md">元素自 3D 空间翻入（`rotateX` + `rotateY` + `translateZ`），再落入连续椭圆轨道。**关键**：入场须在轨道起点原位翻入（阶段 1 前 `gsap.set`），而非场景中心。Tags: orbit, 3d, flip, ellipse, circular, icon, entry, continuous</orbit-3d-entry>
<ai-tracking-box path="rules/ai-tracking-box.md">AI 检测叠层——黄色 `#facc15` L 形角标 + 置信度标签（95–99% 波动），沿正弦弧路径跟随目标。每帧由目标位置重算框位（勿单独补间框）。Tags: ai, tracking, bounding-box, detection, corner, ml</ai-tracking-box>
<depth-scatter-assemble path="rules/depth-scatter-assemble.md">N 个元素在旋转 3D 深度云中散开 / 重组——各元素从确定性索引导出的 3D 偏移（translateZ + rotateX/Y + scatter）出发，收束为平整布局；含 tumble-swap、径向爆开变体。preserve-3d + perspective，仅 transform、可 seek。Tags: 3d, scatter, assemble, tumble, depth, perspective, glyphs</depth-scatter-assemble>
</rules>

## SVG 与图标

<rules>
<svg-icon-enrichment path="rules/svg-icon-enrichment.md">动画 SVG 内部元素（旋转指针、摆动叶片、脉冲点、虚线流动）使图标更活。**关键**：用 SVG `setAttribute('transform', 'rotate(deg cx cy)')` 指定旋转中心——CSS `transform-origin` + `transform-box: fill-box` 在 bbox 局部坐标解释原点（细线会偏中心）。Tags: svg, icon, animation, micro-animation, rotation, pulse</svg-icon-enrichment>
<svg-path-draw path="rules/svg-path-draw.md">SVG 轮廓逐笔描边：`stroke-dasharray` / `stroke-dashoffset`。在 composition 设置时用 `getTotalLength()` 测量，初始 dashoffset = 长度，GSAP 补间至 0。圆环进度条将 stroke 旋转 `-90deg` 使绘制从 12 点开始。Tags: svg, stroke, draw, vector, path, dasharray</svg-path-draw>
</rules>

## 空闲与环境

<rules>
<sine-wave-loop path="rules/sine-wave-loop.md">持续呼吸/ idle 环境动效。两种形式：GSAP `sine.inOut` 有限次 yoyo（独立时优先），或 onUpdate 读取 `tl.time()`（叠加到其他实时值时优先）。Tags: idle, loop, breathing, sine, ambient</sine-wave-loop>
<ambient-glow-bloom path="rules/ambient-glow-bloom.md">无触发的柔和径向光晕在 hero 元素后绽放并保持，带 bounded idle 呼吸；或单次掠过表面的旅行高光。无点击、无词同步；峰值 opacity ≤ ~0.45，有限/确定性。Tags: glow, bloom, ambient, radial, sheen, hero</ambient-glow-bloom>
</rules>

## 过渡与动效

<rules>
<reactive-displacement path="rules/reactive-displacement.md">物理碰撞式过渡：入场元素的 GSAP 补间驱动退场元素位移。同一时间轴位置三条并发补间，被挤元素时长为侵入者的 40–50%。Tags: transition, physics, collision, displacement, push</reactive-displacement>
<press-release-spring path="rules/press-release-spring.md">触觉按钮按下：线性压缩后弹簧回弹，同一属性上相邻两条 GSAP 补间。变体：颜色过渡、CSS 变量阴影深度、释放 burst、背景光晕。Tags: spring, press, button, interaction, physics, glow, burst</press-release-spring>
<physics-press-reaction path="rules/physics-press-reaction.md">物理点击模拟——两条顺序 GSAP scale 补间（降至 0.9、回至 1.0）近似带过冲的弹簧。传单一 targets 数组 `["#cta", "#cursor"]` 使二者同步压缩，增强接触感。Tags: spring, click, physics, press, interaction, cursor</physics-press-reaction>
<cursor-click-ripple path="rules/cursor-click-ripple.md">动画光标移向目标，点击时光标与目标一并下压，发出扩散 ripple，opacity 经 attack-decay 包络。元素从 t=0 即在 DOM 中且 `opacity: 0`（勿条件渲染）。Tags: cursor, click, ripple, interaction, mouse, button, keyframes</cursor-click-ripple>
<scale-swap-transition path="rules/scale-swap-transition.md">同一屏幕中心两 DOM 元素协调 morph。退场簇缩小 + 淡出；入场以 `back.out(2)` 过冲弹出。Tags: transition, morph, scale, swap</scale-swap-transition>
<card-morph-anchor path="rules/card-morph-anchor.md">容器在两镜头间 morph 表观尺寸、圆角与表面，再淡出露出真实目标。HyperFrames 用统一 `scale` 替代禁止的 `width`/`height` 补间，并仅绘制 `borderRadius`/`background`/`boxShadow`。Tags: morph, anchor, transition, border-radius, container, shape, handoff</card-morph-anchor>
<spring-pop-entrance path="rules/spring-pop-entrance.md">标准**入场**弹出——元素（或交错组）以 `back.out` 过冲从 `scale: 0 → 1` 弹入，`fromTo` 保证 seek 下 t=0 正确。单 hero、交错组（≤500ms 上限）、按性格调过冲。区别于 `press-release-spring`（点击/按下反应）。Tags: spring, entrance, pop, scale-in, overshoot, stagger, arrival</spring-pop-entrance>
<motion-blur-streak path="rules/motion-blur-streak.md">快速入场/镜头穿过的方向速度模糊——模糊在最大速度达峰，落位时归 0。两路径：运动轴 SVG `feGaussianBlur` stdDeviation（代理补间），或确定性 echo/ghost 拖尾收束为前导。仅入场/镜中。Tags: motion-blur, streak, velocity, ghost, echo, fast</motion-blur-streak>
</rules>

## 效果配方（自 hyperframes-creative 迁入）

<rules>
<gsap-effects path="rules/gsap-effects.md">即插即用 GSAP 时间轴模式——打字机、音频可视化等可复用编排块。Tags: gsap, recipe, drop-in, typewriter, audio-visualizer</gsap-effects>
<css-marker-patterns path="rules/css-marker-patterns.md">纯 CSS + GSAP 实现标记高亮绘制模式——高亮（黄色扫过）、圆圈（手绘椭圆）、burst（放射线）、涂鸦、sketchout（粗略矩形轮廓）。Tags: css, marker, highlight, text, emphasis</css-marker-patterns>
</rules>

## 另见

- `blueprints-index.md` — 场景形态模板（本技能的「blueprints」），将上述规则组合为完整镜头
- `techniques.md` — 更广的运动设计技法（SVG 路径绘制、Canvas 2D、CSS 3D、动态字、可变字体、合成）；部分规则会引用
- `transitions/` — 场景过渡目录（共享技能；故事侧拥有 `transition_in`， harness 注入）
