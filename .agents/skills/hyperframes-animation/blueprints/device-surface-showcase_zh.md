# device-surface-showcase — 设备 / 界面展示

**intent**：产品界面——设备 mockup 或悬浮的浏览器/应用窗口——作为画面中的主角被框住，其屏幕循环展示真实流程；镜头运动从静态定格到连续 3D 推镜，完成展示。

**roles served**

- Key*Feature（来自 key-feature-device-screen-tour、key-feature-floating-window-scroll、key-feature-3d-device-hand-demo）：在真实界面内展示功能被*体验*——界面承载动作，屏幕按流程推进，而非罗列磁贴或在工作流中追逐光标。（注意：三份草案均为 Key_Feature；本 blueprint 角色较窄但机制丰富——变体差异在 MECHANIC，而非 role。）
- Key_Feature（来自 demo-page-scroll-spotlight）：悬浮窗口推滚变体，聚光灯高潮——真实网页渲染为倾斜 3D 卡片滑入（power2，如同举起手机——无 spring），VO 念到关键词时标题关键词卡拉 OK 式发光，页面滚到演示区块，某一元素从表面*抬起*（translateZ + scale），径向聚光灯压暗其余部分。

**duration**：5–9.6s（page-scroll-spotlight 5–9s · floating-window 7.8s · 3d-hand 7.9s · device-tour 9.6s）

**shot structure**
单一产品界面——`[device mockup]` 或 `[floating browser/app window]`——作为持久主角，置于 `[styled backdrop: gradient / radial / stylized 3D void]` 上；其 `[screens/sections]` 在真实 `[product flow]` 中循环，展示镜头（静态定格、推近→拉远，或一次连续推镜）呈现它。每个屏幕状态约保持 ~1.0–1.5s。

- Scene 1（0.0–~1.5s）：界面*建立*——`[slides in from an edge / drifts in from a tilt / dissolves from a full-frame title card]` 并落定，背后 `[accent shape or backdrop]` 解析完成；首个 `[screen]` 可见。展示镜头启动（见变体）。
- Scene 2（~1.5–~Xs）：在界面自身上*操作*——`[tap/select/scroll]` 触发首次屏幕切换：旧内容 `[pushes out / scrolls up]`，新 `[screen/section]` `[pulls up / pushes in from the side]`；同时 `[label / header word / side headline]` 更新。镜头继续运动。
- Scene 3+（~Xs–end，对 `[2–4 screen beats]` 重复）：界面依次*推进*各 `[screens/sections]`，每次为与界面流程同步的离散切换或滚动，副文案 `[swaps out-up / in-up]` 或保持标记以维持阅读位置。在最终 `[screen]` 上*定格*（某一变体为 bloom 退出——见变体）。

- Variant — static-tour（key-feature-device-screen-tour，9.6s）：`[device mockup]` 从屏外滑入并落定（ease-out）；`[accent-color shape]` 在其后放大（spring overshoot）。镜头*全程静态*——所有运动在元素/UI 层：点击*压缩*按钮（95%→100%），UI 滚动/过渡到下一视图（旧内容推出、新内容上拉），`[side headline]` 在设备旁*切换*（旧文案上滑淡出，新文案上滑入）每屏一次。在最终屏幕定格。无镜头运动、无光标。
- Variant — floating-window（key-feature-floating-window-scroll，7.8s）：以全帧 `[title card]` 开场（中心 `[icon]` 绘制入场，下方 `[feature name]`；约保持 2s），*溶解*为 `[vivid gradient]` 上的 `[macOS-style browser/app window]`（traffic-lights + `[URL pill]` + tabs；左导航、中央内容、右 `[sidebar]`）。镜头*推近* `[target region/sidebar]`（当前项高亮 `[accent]`，光标沿列表下移），再*拉远*重框整窗，同时内容*滚动*经过 `[sections]`；`[highlighted item]` 保持标记。一次推近→拉远弧线，由 title-card 开场门控。
- Variant — 3d-hand（key-feature-3d-device-hand-demo，7.9s）：*全 3D*——`[3D device]` 在 `[stylized 3D void / bloom + particles]` 中漂移，开场倾斜并自旋面向镜头近乎平视，同时*一次连续*前推镜头开始（无切）。光泽 `[3D hand]` 自底前景升起并*手势驱动*界面：滑动滚动 `[picker/sidebar panel]` 的 `[option cards]` 并点击 `[option]`（同时 `[header word]` 字母翻转就位）；选择*应用*——`[new layout]` 从中心生长填满设备面，导航翻转，`[marquee]` 水平滚动；手再次滑动使页面上滚经过 `[sections]`，然后漂出。镜头永不停止推近；明亮设备面持续向镜头生长直至 *bloom* 成 `[light]`  wash——zoom-through「portal」退出填满画面。

**motion vocabulary**
surface establish（edge slide-in + settle / tilt drift-in + self-rotate-to-camera / title-card dissolve）；accent shape spring behind surface；element-level screen-cycling（scroll-swap, push-in-from-side, scale-swap）；button tap-compress；staggered side-headline reveal + copy swap（out-up / in-up）；in-place header-word letter-flip；floating browser-window-on-gradient idle float；full-frame title-card opener（icon draw-in + label）；camera push-IN on a region；camera zoom-OUT re-frame；content scroll-through；one continuous 3D camera-follow push（no cuts）；3D device drift + self-rotate；stylized-environment bloom/particles；3D-hand entrance + swipe-scroll + tap（gesture-driven）；picker-panel slide-in；template-apply grow-from-center；horizontal marquee scroll；gesture-driven page scroll；zoom-through bloom/portal exit；static-hold（no camera）作为镜头范围的下限。

**rule mapping**（每个 motion verb → 对应 rule，或标为 special）

- screen-cycling — UI/区块在界面内滚动（device-tour、floating-window scroll、3d-hand page scroll）→ `3d-page-scroll`（网页/应用作为倾斜卡片，内容 `translateY` 滚到各 section；界面屏幕流的主机制）
- floating-window establish + 界面以倾斜/悬浮 UI 卡片呈现 → `3d-page-scroll`（倾斜/透视框）+ `css-3d-transforms`（perspective/`translateZ` 深度）
- screen / side-copy 状态切换（离散屏幕状态；每 beat 侧标题文案切换）→ `discrete-text-sequence`
- side-headline reveal（交错 fade + slide-up）→ `discrete-text-sequence`
- in-place header-word letter-flip（3d-hand）→ `hacker-flip-3d`
- 两屏状态间协调 shrink-out / pop-in 的 screen swap → `scale-swap-transition`
- template-apply「新 layout 从中心生长填满面」（3d-hand）→ `center-outward-expansion`（聚于中心 → 展开填满）
- 界面状态变形 / title-card→window 溶解作为视觉锚过渡 → `card-morph-anchor`
- button tap-compress（95%→100% 按压反馈）→ `press-release-spring`（或更重按压用 `physics-press-reaction`）
- floating-window 光标点击高亮列表项 → `cursor-click-ripple`
- 当前 sidebar/列表项 accent 高亮弹出 → `asr-keyword-glow`（聚焦项 accent 发光）
- 光标沿 sidebar 列表漂移（floating-window）→ `camera-cursor-tracking`（平面光标漂移；与推近配对）
- 悬浮 browser-window  idle float / 3D device drift-breathe → `sine-wave-loop`
- 3D device drift + self-rotate-to-camera + 透视深度（3d-hand）→ `css-3d-transforms`（CSS-3D）**或** `3d.md` technique（真 Three.js/R3F device）；见 camera modifier
- 水平 `[marquee]` 滚动（3d-hand）→ `viewport-change`（marquee 条 PAN 模式）— *thin fit；字面 CSS-marquee/translateX 循环更接近 `gsap-effects`/CSS 配方而非命名 motion rule*
- 3D-hand 入场 + swipe + tap 作为交互*驱动*（手势输入滚动/选择）→ **标为 special — 需 rule 库外更强能力（R3F/Three.js + WebGL），非 motion-shape rule。** 3D 手模型 + WebGL bloom 有 *technique* 支撑（`3d.md` — R3F、`useGLTF` HandModel、`--gl=swiftshader` 用于 shader/bloom），但无 motion-shape rule 将 3D 手建模为 swipe-to-scroll / tap-to-select 手势协议。`context-sensitive-cursor` / `camera-cursor-tracking` 仅建模平面打字/指针光标，非 3D 手势手。
- zoom-through bloom / portal exit（3d-hand）→ **标为 special — 需 rule 库外更强能力（WebGL），非命名 transition rule。** 能力见 `techniques.md` → WebGL shader（经 `3d.md` headless WebGL：`--gl=swiftshader --concurrency=1`），但无命名 transition rule 覆盖 bloom/portal 穿镜。

**camera modifier**：展示镜头按变体跨越一个*范围*，均在单一包裹内容的虚拟镜头（`viewport-change`）上：

- static-tour → 无镜头运动（`viewport-change` 保持 scale 1，或省略）；全部为元素级运动。这是范围下限，也是 device-tour 与其余变体的区别。
- floating-window → 两阶段推近 → 拉远弧线 → `multi-phase-camera`（如 dramatic-reveal 1.1→1.0→0.95 感）：经 `coordinate-target-zoom`（偏靶 = scale + counter-translate）对 `[sidebar/region]` *推近*，再 `multi-phase-camera` *拉远*重框整窗，同时内容滚动。
- 3d-hand → *一次连续*前推（无切）→ `multi-phase-camera` steady-push 模式（1.0→1.03→1.06… 及其 sine 微漂）叠在 `css-3d-transforms`/`3d.md` 上，使设备在推镜中 self-rotate-to-lens；推镜不间断进入 bloom/portal 退出（退出本身为上述 WebGL-shader flagged special）。
  三者共通：`viewport-change` 为虚拟镜头基元；`multi-phase-camera` 编排 push/zoom 阶段（并为即便「静态」 tour 提供常驻微漂，避免死板）；`coordinate-target-zoom` 将推镜对准偏屏细节。

**Overflow（pan/scroll 界面 — `inspect` 干净所必需）：** 平移或滚动的界面刻意使内容越过 framing card 边缘。在 card/window 上裁剪（`overflow: hidden`），并对移动内层（承载截图及 marker/label 的 `.world` / surface wrapper）标记 `data-layout-allow-overflow`——否则 `inspect` 会对滚出部分报 `text_box_overflow` / `container_overflow` *ERROR*（例如 marker label 平移出左缘）。card 在视觉上裁剪；该属性告诉 `inspect` 这是有意为之，非 layout bug。
