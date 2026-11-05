# cursor-ui-demo — Cursor 驱动的 UI 演示

**intent**：可见的自定义光标通过点击 / 悬停 / 拖拽驱动真实（重建的）应用 UI，使画面逐镜变化状态，同时镜头追逐每次交互——产品界面是主体，光标是演员。

**roles served**

- Product*Intro（来自 `product-intro-cursor-ui-demo` / #14 Product_Intro_02、#15 Product_Intro_2、#17 Product_Intro_04）：首次展示产品界面——光标扫过/悬停以 _introduce_ 应用并揭示它是什么，最终停在悬停的英雄元素或刚弹出的结果上。轻快、探索式；背景随步骤推进变换颜色。
- Key*Feature（来自 `key-feature-cursor-ui-demo` / #23 Key_Feature_2、#24 Key_Feature_03、#27 Key_Feature_06）：完整演示某一多步骤工作流 _end-to-end_（跨 2–4 个离散节拍的编辑 / 配置 / 选择），每一节拍都是 UI 实时响应的真实编辑，最终锁定在主操作按钮或产出结果上。
- Key_Feature（来自 `workflow-approve-press`）：以 3D 倾斜侧翼驾驶舱为框架的机构 / 确认工作流——步骤列表从 pending → active → complete  ticking（快照状态机，CSS 响应 `[data-state]`），侧翼按钮承受 PRESS 作为高潮（颜色翻转为成功态，勾选标记盖印）。点击是 climax，而非路过手势。

**duration**：4.0–9.3s（Key_Feature 4.0–7.3s 与 Product_Intro 6.1–9.3s 的并集）

**shot structure**（`[product UI surface]`——固定应用窗口、仪表盘/编辑器、视差 `[content card]` 堆叠，或 `[container object/icon]`——居中置于 `[bg color/gradient]` 之上，以 `[flat]` 或 `[3D-isometric]` 呈现；自定义 `[brand-colored cursor with icon]` 是主角，镜头伺服到它所触及之处；UI 与每次光标动作 _live_ 且同步响应。两种角色调性的节奏并入——Product_Intro **扫过以介绍**，Key_Feature **执行工作流**。）

- **Scene 1（0.0–~Xs）— 界面建立 + 首次触碰。** `[product UI surface]` 在 `[bg color/gradient]` 上居中出现——要么本就存在（固定窗口 / 仪表盘 / 编辑器），要么是 3D 视差 `[content cards]` 堆叠，或带 3D 翻滚飞入并 settle 的 `[container object/icon]`。自定义 `[cursor]` 入场。光标对 `[cursor target 1]` 执行 FIRST action，UI 在同一节拍内 live 响应。镜头保持或开始向被操作区域缓慢推近。
  - _Variant — Product_Intro_：低承诺首次触碰——光标 HOVERS/扫过控件或 SWEEP-HIGHLIGHTS 某字段至 `[accent color]`，或 `[container]` 扇形展开。可选标签/标题淡入/morph 到界面上。要点是 _展示界面存在_ 且可触。
  - _Variant — Key_Feature_：具体编辑——光标 DRAGS 滚动条 / TYPES 入字段 / DRAGS 手柄，UI  materially 响应（`[scroll]` / 数值攀升 / 区域 resize）。若界面以 `[3D-isometric]` 打开，可在此 perspective-FLAT 以便阅读工作流。

- **Scene 2（~Xs–~Ys）— 镜头追逐下一交互（引擎）。** 镜头 MOVES 至下一目标——推近 + 平移 / whip-pan / pan-down 至 `[cursor target k]`——光标执行 action k，UI live 更新。每一节拍是离散交互，由快速镜头移动衔接；界面内部内容随交互 SWAPS。
  - _Variant — Product_Intro_：导航偏探索——慢速镜头平移 + 景深 FOCUS-PULL 扫过视差 `[content card]` 堆叠，或 `[container]` 扇入 `[N option/content cards]` 并 SPRING 到位。内容切换时，支撑 backdrop STEPS 颜色（`[bg step 1]` → step 2 → …）。通常一到两次此类移动。
  - _Variant — Key_Feature_：对 `[2–4 beats total]` 重复，每次为 UI 应答的 distinct 操作——计数器 COUNTS UP、`[pill/swatch]` SELECTS、modal SLIDES UP 并 TYPES——由 whip-pans / progressive zoom 连接。工作流 visibly 朝结果推进。

- **Scene 3（~Ys–end）—  payoff 状态，镜头 settle，HOLD。** 光标落在最终目标，画面到达 payoff 状态；镜头静止（static）并 hold。
  - _Variant — Product_Intro_：光标 HOVERS 英雄元素——`[content card]` 悬停 SCALE UP、节点获得 `[Available]` 风格 pill，或 `[result card]` POP/spring 入场——「这就是产品」payoff。static settle，hold。
  - _Variant — Key_Feature_：锁定 OUTCOME 特写——光标落在 `[primary action button: Export / Save / Reimburse]`，`[hover backdrop / highlight]` SPRING-pop 入场（climax 是 action button / 产出结果）。Hold。

**motion vocabulary**：cursor-driven click / hover / sweep-highlight / drag / type；每次交互的 live UI 响应（scroll、value climb、region resize、content swap）；镜头 push-in + pan / whip-pan / pan-down 伺服至各目标；coordinate zoom 至被操作区域；点击控件的 press-and-ripple；button press-compress；screen-state swap shot-to-shot；card fan-out 至角落（spring）；3D container fly-in & tumble-settle；perspective-flatten（3D→2D snap）；paginated/stepped backdrop color advance；景深 focus-pull 扫过视差 card stack；counter count-up；pill/swatch select；modal slide-up + typing；label/title morph 于状态间；UI-keyword highlight glow；terminal hover-scale 或 result-card pop-in；最终 action button 上的 spring hover-backdrop。

**rule mapping**

- viewport 跟随光标 / 镜头伺服至所触之处（primary）→ `camera-cursor-tracking`
- 光标移向目标、按下、发出 ripple（点击本身——primary interaction primitive）→ `cursor-click-ripple`
- screen-state swap shot-to-shot（界面内部内容在节拍间变化）→ `scale-swap-transition`
- 镜头 push-in + pan / whip-pan / pan-down 至下一目标 → `viewport-change`（pan/zoom 横越 UI）
- 将追逐编排为离散交互节拍 → `multi-phase-camera`
- zoom 至具体被操作 UI 区域 → `coordinate-target-zoom`
- 光标 icon/状态随上下文变化（如 draggable handle 上 pointer↔grab）→ `context-sensitive-cursor`
- 每节拍出现的内容 / 逐步 UI 状态推进 / 每交互 swap → `dynamic-content-sequencing`
- sweep-highlight 字段、将 UI keyword 高亮至 `[accent color]` → `asr-keyword-glow`（所触元素上的 keyword glow）
- 点击按钮按下 compress、释放 spring 回弹 → `press-release-spring`
- 较重 press 时光标与按钮一起 compress → `physics-press-reaction`
- panel/card 于两状态间 morph（如 card → expanded card、surface state A → B）→ `card-morph-anchor`
- terminal hover-scale、`[result card]` pop-in、最终 action button 上 spring hover-backdrop → `spring-pop-entrance`
- card fan-out 至角落 / option cards spring 到位 → `split-tilt-cards`（fan/spread 至 tilted positions）+ `spring-pop-entrance`（spring settle）
- 3D-parallax content-card stack 作为 surface；UI 以 3D-isometric 展示 → `3d-page-scroll`（UI 作为 tilted scrolling/parallax card）
- 节点获得 `[Available]` 风格 pill / 元素上出现 tracked badge → `ai-tracking-box`
- UI 响应时 counter / value count-up → `counting-dynamic-scale`
- 工作流 outcome 的 result bar / number FILLS → `stat-bars-and-fills`
- 以 live `[video]` 录屏 clip 作为 surface → technique: video compositing
- perspective-flatten（3D-isometric → flat 2D snap）及 3D-isometric tilt 本身 → technique: CSS-3D（无专用 rule；tilt/flatten transform 为 CSS-3D primitive）
- 镜头 static settle 于 payoff 并 HOLD →（payoff 元素上 `spring-pop-entrance` 的 settle 阶段；static hold 本身无需 rule）
- 3D container/object fly-in & tumble-settle → `depth-scatter-assemble`（自由翻滚的 3D object/container 入场飞入并 tumble-settle；`orbit-3d-entry` 仅将 flat 元素 orbit 到位）
- 视差 card stack 上的景深 focus-pull → `depth-of-field-blur`（near 与 far cards 间 rack-focus / DoF blur transition；`3d-page-scroll` 提供 tilted parallax stack，`viewport-change` 提供 pan）
- 与交互同步的 paginated/stepped backdrop 颜色推进（`[bg step 1]`→step 2→…）→ `discrete-text-sequence`（离散状态步进，此处应用于 background-color state 而非 text）
- modal slide-up + 模态内 typing 作为 combined beat → `card-morph-anchor` / `scale-swap-transition`（panel slide-in）+ `discrete-text-sequence`（模态内 typed text）

**camera modifier**：定义性动作为镜头 CHASE——viewport 经 `camera-cursor-tracking`（primary）从目标到目标跟随光标，具体实现为 `viewport-change` 下的 push-in + pan / whip-pan / pan-down，`multi-phase-camera` 将节拍编排为离散交互，每节拍目的地经 `coordinate-target-zoom`（zoom 至被操作区域）瞄准。Product_Intro 偏向慢速探索式 pan + focus-pull 扫过 surface；Key_Feature 偏向更利落的 whip-pans / progressive zoom 贯穿工作流并 static 锁定 action button。这种镜头伺服光标将本 blueprint 与 hands-off 镜头 scroll（dataviz-scroll-reveal）及 static device/window tour 区分开来。
