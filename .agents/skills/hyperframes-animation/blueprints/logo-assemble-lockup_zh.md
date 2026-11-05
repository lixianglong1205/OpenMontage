# logo-assemble-lockup — Logo 组装 → 定稿（Lockup）

**intent**：品牌标识 / 字标从部件自行构建（元素组装或轨道飞入、字母级联、描边绘制，或镜头穿过负空间），最终定格为居中的 logo 定稿 — 可选延伸至最终 URL / CTA。

**roles served**

- Product_Intro（来自 product-intro-logo-system-assemble）：无文案、高端品牌 STING — 抽象元素系统脉动 / 生长 / 轨道运动并围绕**固定**中心 logo 组装，由一次电影感镜头倾斜贯穿；无文案、无 UI。
- CTA（来自 cta-camera-push-lockup）：logo 构建作为最终诉求的**前奏** — 3D 标识组装 + 字标级联，随后快速镜头**穿过**标识负空间，巨型 CTA 字母掠过镜头，定格于 `[url]` / `[CTA verb]` 定稿。
- CTA（来自 cta-button-wordmark-build）：「自绘描边 → 字标逐字构建」子形态 — `[CTA button]` 药丸按钮自绘发光描边边框，对角带状 WIPE 翻转画面，`[wordmark]` 在斜杠旁逐字出现以落地定稿。镜头静态。
- Brand_Outro（来自 brand-outro-assemble-logo-lockup）：收尾标识 — 由 `[feature pills / UI elements]` 组成的阵列从四边**清场**离场，空镜上 `[logo mark]` 逐笔描边绘制，`[wordmark]` 显现完成定稿，随后淡出。
- Product_Intro（来自 brand-reveal-assemble-zoom）：先语境后聚焦的揭示 —  companion 标语**逐字打出**设定语境，主标识在旁弹出，companion 退出时布局重新居中，镜头**推近**至标识特写并 hold（宽构图收窄为 tight focus）。

**duration**：约 4.6–11.0s（Brand_Outro 约 4.6s · brand-reveal 约 5s · Product_Intro 约 7s · CTA 5.4–11.0s）

**shot structure**（单一合并时间码模板；`[slots]` 与具体产品无关）

- Scene 1 — 清场 / 点燃（0.0–~1.0s）：为标识构建准备舞台。
  - _Variant — Product_Intro_：以干净 `[light bg]` 开场，俯视平视角下 faint 同心引导环；环从中心**脉动**并外扩；中段背景 crossfade `[light]→[dark gradient: hero→secondary]`，环上 tiny 种子点出现，中心 `[logo mark]` 光晕**点燃**（标识自 t=0 即存在、固定、正面朝向）。
  - _Variant — CTA push_：在 `[bg gradient]` 上，`[logo mark]` 在物体空间中落定（带细线框 edge-guides + 中心后 faint 括号 motif 的 3D 标识）；极慢的持续镜头推近可能已在 creep。
  - _Variant — CTA button-build_：在 `[dark grid bg]` 上，圆角 `[CTA button "label"]` 药丸升起 / 缩放至中心（此前标题已清出顶部）；细边框以动画发光描边 **DRAW ON**，左侧边缘 small `[accent]` 彗星 / 火花图标。
  - _Variant — Brand_Outro_：预排 `[feature pills / element grid]` 阵列（各 `[icon]`+`[label]`）**散开** — 元素从布局位置向外滑出并飞离四边（edge-clearing drift，非中心爆发），清空画面至干净 `[bg]`。

- Scene 2 — 组装标识（~1.0–~Ys）：标识由部件自行构建。
  - _Variant — Product_Intro_：种子点 **SCALE UP** 为环上排列的 flat `[accent]` 形状；同心带向外 ripple（tunneling 感），形状开始围绕仍固定的中心 **ORBIT** / drift。
  - _Variant — CTA push_：`[wordmark]` 从标识后方 **CASCADE** 而出（字母左→右带 overshoot）形成完整 `[brand lockup]`；3D 标识可分 beat 组装（末端 detach + spring dot 弹出、部件 hinge 打开 elastic  snap 闭合）。可选 beat：`[cursor]` 弧线飞入并「点击」字标，或 holding 中间 `[CTA line]` 的 frosted-glass 药丸 spring 入画同时分层 mark shell fan 至边缘。
  - _Variant — CTA button-build_：图形 **WIPE** 翻转画面至 `[contrast bg]` — 细 `[accent]` 对角线 sweep 入画，膨胀为全画幅对角 **BAND**，再 collapse 为 small `[accent]` slash。
  - _Variant — Brand_Outro_：在已清空的画面上，`[logo mark]` 通过 stroke **DRAW ON**（逐弧 / 逐段构建）。

- Scene 3 — 定格定稿（~Ys–end）：定稿完成并 hold（Product_Intro / Brand_Outro），或飞入 / 延伸至 CTA（CTA 变体）。
  - _Variant — Product_Intro（唯一镜头运动）_：整系统从 flat 俯视平滑 **TILT** 至 angled 等距视角（ease-in-out），略 zoom-out — flat 形状变为 luminous 3D 形态，带变为 glowing 轨道线，中心 `[logo mark]` **不** tilt（保持 2D、正面、固定）。镜头 ease 至停；元素持续 orbit/drift（内圈快于外圈）；标识保持 steady glow。最终 settled 帧。
  - _Variant — CTA push（signature）_：单次快速 **CAMERA PUSH-THROUGH** 标识负空间 / 穿过 glass pill — 强烈水平 motion-blur，巨型 `[CTA]` 字母掠过镜头（cursor 退出）。在饱和 `[bg]` 上定格最终定稿：`[url badge]` / `[CTA line]` 由左→右 **WIPE** 带 `[accent]` leading edge 揭示（或 clean fade），solid mark-shapes 在后方 parallax slide-in。Dead-static hold（慢 zoom-out / settle）。
  - _Variant — CTA button-build_：`[wordmark]` 在 slash 右侧 **BUILDS** 逐字，落地 final "`[slash] [WORDMARK]`" 定稿居中于新 bg。慢 settle 至 static。
  - _Variant — Brand_Outro_：`[wordmark]` 在已绘标识旁 reveal（slide / fade）完成 `[lockup]`；定稿 hold，随后 fade 至 `[black / bg]`。

**motion vocabulary**：ring pulse / expand；background crossfade（light→dark）；glow ignite；seed-dot scale-up；continuous orbit / drift（内快于外）；单次 3D perspective tilt（flat→isometric）+ slight zoom-out 围绕 fixed 2D anchor；3D logo assemble（part detach + spring dot、clapperboard hinge / snap、shell fan-out）；wordmark cascade with overshoot（字母左→右）；button pill rise / scale-in；animated stroke-outline DRAW + glow（button border 与 logo mark）；comet / spark accent；diagonal-band wipe（sweep → swell → collapse-to-slash）；letter-by-letter wordmark build；pre-formed grid DISPERSE 四边；logo-mark stroke-draw（sequential arcs / segments）；fast CAMERA PUSH-THROUGH with motion-blur（CTA spine）；continuous slow push-in / push-out；cursor arc-in + click；parallax shape slide-in；left→right URL/badge wipe with glowing leading edge；static / fade-out end-lockup hold；held mark 可选 idle breathe。

**rule mapping**（按 motion verb → `rules/<id>.md`）

- ring pulse / expand from center → `center-outward-expansion`（从共享中心辐射；复用 0→1 progress driver）
- background crossfade（light→dark gradient）→  plain opacity/background tween via `gsap-effects`（无需专用 rule）
- glow ignite on the mark → `asr-keyword-glow`（品牌元素上 envelope-driven glow）
- seed-dot scale-up into shapes → `spring-pop-entrance`（scale-in pop；若 dot morph 为 shape 可用 `scale-swap-transition`）
- continuous orbit / drift around fixed center → `orbit-3d-entry`（flip-in 后 continuous elliptical orbit；center label = fixed mark）
- single 3D perspective tilt（flat→isometric）+ slight zoom-out → `multi-phase-camera`（scene-wrapping camera 上 scripted scale phases，用于 zoom-out）— 见 camera modifier；整舞台 FLAT→ISOMETRIC 平面 tilt 为 CSS-3D perspective move（`techniques.md` CSS-3D，动画 stage 的 `rotateX`）— 无 plane-tilt 的 exact camera rule，用 CSS-3D 近似（最近参考为 `orbit-3d-entry` 的 "Tilted orbit plane" variation 随时间动画）
- fixed 2D anchor logo amid moving universe → 无需 motion rule（static anchor；有意为之 — 标识不动，宇宙围绕它动）
- 3D logo assemble — part detach + spring dot → `spring-pop-entrance`（spring pop，`back.out` overshoot）
- 3D logo assemble — hinge open / snap（clapperboard）→ `hacker-flip-3d`（3D-rotate 轴）+ `techniques.md` CSS-3D（elastic open-and-snap-shut hinge 为 3D-rotate 的 adaptation）
- 3D logo assemble — shell fan-out to edges → `center-outward-expansion`（从 mark center 向外 run）
- wordmark cascade with overshoot（letters left→right）→ recipe `gsap-effects`（per-element staggered slide）+ `spring-pop-entrance`（每字母 `back.out` overshoot）
- button pill rise / scale-in → `spring-pop-entrance`（scale-in；alt `scale-swap-transition`）
- animated stroke-outline draw + glow（button border）→ `svg-path-draw`（stroke-dashoffset draw）+ `asr-keyword-glow`（drawn stroke 上的 glow）
- comet / spark accent on button → `asr-keyword-glow`（small glow accent）；motion path via `techniques.md` GSAP MotionPathPlugin (#9)
- diagonal-band wipe（sweep → swell → collapse-to-slash）→ `techniques.md` clip-path reveal (#12，animate `polygon(...)` diagonal 横穿画面；swell-then-collapse-to-slash 为同一 clip-path reveal 经 grow→shrink keyframes 驱动）
- letter-by-letter wordmark build → `discrete-text-sequence`（smooth-slice / per-state build）；recipe `gsap-effects`（typewriter / appending words）
- pre-formed grid disperse off all four edges → 非 rule gap：formation 飞离画外为 EXIT，pipeline 禁止 mid-video exits — harness transition **即** exit（仅最终帧可 exit stage）。视为 transition-handled / final-frame-only，而非 in-scene motion rule。（若 in-scene  staged 为 reveal-the-mark clear，复用 `center-outward-expansion` run OUTWARD — center→target machinery 插值 formation→offscreen targets，out-easing。）
- logo-mark stroke-draw（sequential arcs / segments）→ `svg-path-draw`（canonical multi-segment stagger draw）
- wordmark slide / fade reveal beside drawn mark → `svg-path-draw`（「brand-line fades in after stroke」tail）；slide via `spring-pop-entrance`
- fast camera push-through with motion-blur → `multi-phase-camera`（hard push phase）— 见 camera modifier；heavy motion-blur streak 本身 → `motion-blur-streak`（fast push-through 上 directional velocity blur）
- continuous slow push-in / push-out → `multi-phase-camera`（phase scale + drift）
- cursor arc-in + click on the wordmark → `cursor-click-ripple`（move → click → ripple）；arc path via `techniques.md` MotionPathPlugin (#9)
- parallax shape slide-in behind lockup → `depth-scatter-assemble`（不同深度 parallax depth slide-in；与 `3d-text-depth-layers` 配对做 depth ordering）
- left→right URL / badge wipe with glowing leading edge → `techniques.md` clip-path reveal (#12，animate `inset()` left→right）；glowing leading edge → `asr-keyword-glow`
- static / fade-out end-lockup hold → 无需 motion rule（terminal hold / opacity fade；有意为之）
- idle breathe on held mark（optional）→ `sine-wave-loop`（post-settle breathing）

**camera modifier**（push / tilt）

- **CTA push-through**（CTA spine）：scene-wrapping camera 上 scripted hard zoom phase → `multi-phase-camera`（「Steady push」/「Bookend pull」pattern；push phase = climax）。当 mark OFF-center 且镜头须飞过特定 negative space 点时，与 `coordinate-target-zoom` 组合（外层 scale，内层 counter-translate 使 target negative-space 点随 scale ramp 落于 viewport center；setup 时测量 offset）。signature 强烈水平 MOTION-BLUR on streak → `motion-blur-streak`（push 上 directional velocity blur）；push 窗口内用 CSS `filter: blur()` / duplicated-streak layer 实现。
- **Product_Intro tilt**（唯一电影感 move）：flat→isometric perspective tilt + slight zoom-out 为单次 scripted camera beat → `multi-phase-camera`（scale phase + 「Targeted zoom into off-center element」/ drift machinery）用于 zoom-out。`multi-phase-camera` 仅 scale+translate+drift，故整舞台 perspective-PLANE rotateX（flat top-down → angled isometric）为上述 CSS-3D move — 经 `techniques.md` CSS-3D 近似，动画 stage 的 `rotateX`（最近参考为 `orbit-3d-entry` 的 "Tilted orbit plane" variation 随时间动画）。
