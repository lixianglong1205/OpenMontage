# grid-card-assemble — 网格 / 卡片组装

**意图**：N 个元素（磁贴 / 卡片 / Logo / 列表行）以交错级联方式自行组装成网格或垂直列表并保持——一种「一眼看全量 / 谁 / 能做什么」的节拍，一次性枚举广度；可选的相机拉远（zoom-OUT）后撤，揭示已组装阵列置身于更宏大的整体之中。

**适用角色**

- Key_Feature（来自 key-feature-card-grid-assemble）：带标签的功能磁贴/胶囊（图标 + 标签）逐个级联进入 2 列砖砌 / 3×3 网格，随后以近静态方式保持并缓慢推近——枚举多项能力，无实时 UI、无光标。
- Key_Feature（来自 key-feature-glass-card-camera-reveal）：开场紧切 2–3 个发光图标；相机拉远展开一行玻璃拟态卡片，自图标后方生长（图标缩小约 50% 成为卡片标题），中心卡片向前放大，整组悬浮，随后扫出——同一组装形态的「支柱一次性揭示」变体。
- Benefits（来自 benefits-vertical-list）：短价值短语以约 1 条/秒填入单一垂直列表，共存并累积；每行通过弹簧标记弹出 + 勾选绘制 + 胶囊遮罩擦除进入，或整栈每拍上滑一格（老虎机式），使最新一行落在明亮焦点槽位。
- Social_Proof（来自 social-proof-logo-grid-zoom-out）：合作伙伴/应用 Logo 墙构建成中心网格（整组进入 / 随机弹出 / 列上滑），可选标题 + 强调渐变证明数字在上方填入，随后连续相机拉远缩小阵列以揭示广阔生态；可选固定 HUD/取景框括号；可选网格上滑飞出退出。

**时长**：3.0–10.5s（Social_Proof 3.0–6s · Key_Feature 网格 5.8–7.3s · Key_Feature 玻璃卡片 6.5s · Benefits 列表 6.5–10.5s，随数量约 1 条/秒缩放）

**镜头结构**（合并模板——具体动作动词，[插槽]）

- **场景 1（0.0–~1.0s）— 开场 + 首批到达。** 在 `[渐变 / 径向 / 深色背景]`（可选 `[点阵 / 漂移水印]` 纹理）上，建立空的 `[网格或列表区域]`，元素以快速交错级联开始组装（间隔约 0.04–0.08s；列表节奏约 1 条/秒）。每个 `[元素：功能磁贴 / 胶囊 / Logo 磁贴 / 利益行]` 淡入并短距滑入/缩放入槽（低戏剧感——无散射、无大弹跳；弹簧过冲保留给强调标记）。相机静态。开场 `[标题 / 钩子]` 可在阵列上方逐行填入，任意 `[证明数字]` 以 `[强调渐变]` 计数上升。
- **场景 2（~1.0s–~Xs）— 阵列收束 + 保持。** 剩余元素完成到达；布局收束为最终 `[2 列砖砌 / 3×3 网格 / 密集马赛克 / 堆叠列表]`。完整阵列保持，有生命但静止：磁贴上轻微连续视差/正弦浮动，和/或缓慢相机推近（轻微放大）。可选 `[强调色]` 光晕在磁贴间/后方流动。
- **场景 3（~Xs–结束）— 落定 / 揭示 / 退出。** 一切落定并保持至结束，或运行可选相机修饰（见下），或 `[收束行 / CTA]` 为阵列收尾。

变体（角色与模板分歧处）：

- **变体 — Key_Feature 网格**：元素为带 `[图标 + 功能标签]` 的磁贴/胶囊，组装成 2 列砖砌 / 3×3 网格；近静态保持 + 缓慢推近 + 可选流动光晕扫过；标题首尾（`[钩子]` → `[CTA]`）。无相机揭示。
- **变体 — Key_Feature 玻璃卡片揭示**：组装由相机驱动，而非元素交错。紧切 `[2–3 发光图标]` 开场；相机拉远自图标后方生长 `[N]` 张玻璃卡片（图标缩小约 50% 成为卡片标题），`[中心卡片]` 放大约 105% 并前移与两侧重叠（快弹簧）；卡片并排保持并连续视差浮动；退出 = 快速运动模糊扫滑将卡片带出画外。
- **变体 — Benefits 垂直列表**：单一垂直 `[利益行]` 栈，约 1 条/秒，两种子模式 — (a) BUILD：每行保持全亮；进入 = `[标记]` 弹簧弹出 + `[勾选/图标]` 绘入 + `[胶囊]` 遮罩擦除文字；(b) SNAP：整栈每拍上滑一格（约 0.1s 缓动），最新行落在明亮焦点槽位，离开槽位的行按位置变暗。相机静态；对侧可选持续 `[装饰轨道/圆盘]`。无相机揭示。
- **变体 — Social_Proof Logo 墙拉远**：引子节拍（`[trusted-by 标题]` 卡片或 `[产品截图]`）交叉淡入/切至中心 Logo 网格构建（整组进入 / 随机弹出 / 列上滑）；连续相机拉远将整个网格向中心缩小以揭示广阔生态并保持；可选固定 HUD/取景框括号；可选退出 = 整网格上滑飞出顶部。

**动作词汇**：元素交错组装（淡入 + 短距滑入/缩放入槽）· 砖砌/网格/列表布局收束 · 随机弹出 · 列上滑入网格 · 垂直列表步进（老虎机 snap-and-hold）· 弹簧过冲标记弹出 · 勾选/图标绘入 · 胶囊/标签遮罩擦除揭示 · 按位置变暗弱化 · 标题逐行填入 · 强调渐变数字计数上升 · 近静态保持 · 保持时轻微视差/正弦浮动 · 缓慢相机推近 · 相机拉远揭示（连续或分阶段后撤）· 卡片自图标后方生长 · 图标缩小为标题 · 中心卡片放大 + 前移重叠（弹簧）· 流动光晕扫过 · 固定 HUD/取景框括号 · 运动模糊扫滑退出 · 网格上滑飞出（退出）· 首尾标题淡入 · 持续装饰轨道/循环。

**规则映射**（动作动词 → `rule-id`）

- item stagger-assemble into slot → `center-outward-expansion`（per-item stagger + short-path slide variant; for a wall too dense for a true center burst, use it in its "starting partially-spread"/direct-into-slot form — see merge tension）
- brick/grid/list layout resolve → `center-outward-expansion`（target positions = final layout slots）
- randomized pop-in stagger → `gsap-effects`（stagger recipe; randomized `from`/order）
- column slide-up into grid → `gsap-effects`（per-column staggered slide-up）
- vertical-list step / slot-machine snap-and-hold → `vertical-spring-ticker`（STEPS = number of line advances）
- spring-overshoot marker pop → `spring-pop-entrance`（back.out spring）— also `gsap-effects` for the staggered pop chain
- check / icon draw-in inside marker → `svg-path-draw`
- live line-art icon in a tile (internal parts) → `svg-icon-enrichment`
- pill / label mask-wipe text reveal → `techniques.md`（clip-path reveal）
- dim-by-position de-emphasis → `gsap-effects`（per-line opacity by slot position; no dedicated rule）
- line-by-line headline fill → `discrete-text-sequence`
- accent-gradient proof number count-up → `counting-dynamic-scale`
- gentle parallax / sine float on hold → `sine-wave-loop`（apply the concurrent-elements amplitude `/√N` rule for a held grid）
- slow camera push-in → `multi-phase-camera`（steady-push phase pattern）
- center-card scale-up + forward overlap → `spring-pop-entrance`（the quick spring）+ `techniques.md` CSS-3D（z-depth overlap）
- cards-grow-from-behind-icons / icon-shrink-to-header → driven by the camera reveal（`multi-phase-camera`）— the grow/shrink are scale tweens chorded to the pull-back phase; no separate rule
- fixed HUD / viewfinder brackets → `ai-tracking-box`（static-bracket variant — overlay frame, not tracking）
- book-end headline fade → `discrete-text-sequence`（or `gsap-effects` fade）
- perpetual decorative orbit / disc / loop → `sine-wave-loop`（or `orbit-3d-entry` if it's an orbiting badge ring）
- traveling-glow sweep across/behind tiles → `ambient-glow-bloom`（one-pass traveling glow sweep across the tiles）
- motion-blur slide-out sweep (glass-card exit) → `motion-blur-streak`（directional velocity blur on the fast sweep that carries the cards off-frame）
- grid slide-up fly-out exit → `gsap-effects`（plain staggered translate-off-frame; no dedicated rule needed — a basic exit tween, not a missing capability）

**相机修饰 — 拉远揭示**（可选；玻璃卡片与 Logo 墙变体的角色定义动作）：包裹整阵列的相机 wrapper 在保持阶段缩小，揭示已组装网格/卡片处于更大环境之中（生态尺度，或自紧切图标展开的一行卡片）。

- Continuous single-pass zoom-out (Social_Proof ecosystem pull-back) → `viewport-change`（one wrapper, `cam.scale` ↓ via onUpdate — single source of truth）
- Phased pull-back → focus → settle, with built-in drift (Key_Feature tight-icons → cards-unfold) → `multi-phase-camera`（use the "Dramatic reveal: push → neutral → pull" / pull-back phase pattern; grow/shrink of cards chords to the pull-back phase）

---

```
BLUEPRINT: grid-card-assemble — serves Key_Feature, Benefits, Social_Proof (folded 4 drafts)
RULE GAPS: none — traveling-glow sweep → ambient-glow-bloom; motion-blur slide-out sweep (exit) → motion-blur-streak; grid slide-up fly-out (exit) → gsap-effects (plain translate)
```

合并张力：`center-outward-expansion`（交错组装的自然支撑）在 3–8 项内收束清晰，并明确警告 8+ 会导致飞行中途重叠混乱——但 Social_Proof Logo 墙故意密集（12+ 磁贴），故该变体元素不得从共享中心爆发；它们短距直接滑入各自槽位（规则的「起始部分展开」/短路径形式，或 `gsap-effects` 逐元素交错），合并场景 1 动词已规定为「短距直接入槽」。
