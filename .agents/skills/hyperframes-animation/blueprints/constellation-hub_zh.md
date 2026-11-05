# constellation-hub — 星座 / 中心枢纽 + 卫星

**intent**：带标签/图标的节点弹入环绕中心的环状/簇状布局，随后镜头在核心上收束——要么将镜头推入中心（景深在核心上收拢），要么固定中心枢纽标记而让卫星围绕其**公转**；呈现「一切汇聚于 / 围绕一个中心」的节奏。

**roles served**

- Hook（来自 `hook-cluster-push-in`）：工具/应用节点星座弹入宽环，随后持续镜头推入配合景深在内部核心上收束——「连接一切 / 所有工具的一个枢纽」。
- Social_Proof（来自 `social-proof-orbit-ecosystem`）：产品品牌标记落为中心枢纽，合作伙伴 logo 弹上环并围绕公转——「接入 / 处于你技术栈的中心」。
- CTA（来自 `cta-orbit-collapse`）：环通过**坍缩**而非推入收束——品类图标在空白的中央 CTA 周围漂移，光标点击使轨道向点击点内爆，产品演示从该坍缩中弹出作为答案（范围 → 选择 → 后果 → 产品）。
- Social_Proof（来自 `proof-logo-chain`）：持久中心 logo 累积证明——字标解码、主张 ticker 切换、logo 滑至中心，随后头像级联进入轨道并绘制连接线，同时合作伙伴 logo 滚动底栏；四条主张读成一句陈述。

**duration**：5–8s（Hook 5–6s · Social_Proof 5–8s · CTA orbit-collapse ~6s）

**shot structure**

合并模板——节点环绕中心，随后两种收束之一在核心上落定。

- Scene 1（0.0–~1.5s）：`[bg]`（暗/太空场域，可选缓慢漂移的弥散渐变 blob）。`[primary nodes]`（承载 `[icon]` + 标签的圆）**SPRING-POP** 弹入（scale 0→1，~1.15 弹性过冲，交错）排列于空或已标记中心 `[hub]` 周围的宽环/簇。
- Scene 2（~0.7–2.5s，重叠）：较小 `[secondary nodes]`（平台 / 合作伙伴 logo 芯片）以相同弹性 spring 交错弹入，填补空隙；可选细 `[accent]` 连接线 / 轨道环自 hub→nodes 绘制。镜头保持。
- Scene 3（~2.5–Xs，收束）：见下方 finisher 变体；在放大 / 公转的中心上落定并**保持**至结束。

- Variant — Hook（push-in finisher）：自 Scene 3 起，向中心内簇持续平滑**镜头推入**——内层节点放大并保持清晰，外层节点被推向边缘并渐进**模糊**（景深），背景平滑放大；在核心放大态保持。
- Variant — Social_Proof（orbit finisher）：中心 `[brand mark]` 经快速 3D 旋转减速落定弹入；细 `[accent]` 轨道环围绕其绘制；`[N partner badges]` 弹上环（交错过冲）并**顺时针**公转且保持 upright，配合持续缓慢镜头 **ZOOM-OUT**（生态揭示）。
- Variant — Social_Proof（可选 type-push-through 开场，接在 Scene 1 之前）：居中 `[headline]` 打字/滑入，同词巨大透明填充**描边**副本在其后；描边文字向镜头指数放大（高速 dolly / push-through），突破画幅，随后**硬切**至 Scene 1 的 hub 背景。

**motion vocabulary**：交错弹性 spring-pop 节点入场（~1.15 过冲）；缓慢 gradient-blob 漂移；连接线 / 轨道环 draw-on；hub 标记 3D snap-rotate-settle；持续镜头推入（内清晰、外层景深模糊、背景放大）；upright 徽章顺时针轨道公转；持续缓慢镜头 zoom-out（生态揭示）；可选描边文字 push-through dolly 入场。

**rule mapping**（motion 动词 → `rules/<id>.md`）

- 交错 spring-pop 节点入场 → `spring-pop-entrance`（elastic overshoot）+ `gsap-effects`（stagger recipe）；3D-flip-in 风味 → `orbit-3d-entry`
- 节点围绕中心的环 / 簇布局 → `avatar-cloud-network`（椭圆环上的节点 + 指向中心的 SVG 线）
- 节点上的图标 → `svg-icon-enrichment`
- hub→node 连接线 → `svg-path-draw`
- 轨道环 draw-on → `svg-path-draw`
- 缓慢 gradient-blob 漂移 → `sine-wave-loop`（idle 循环漂移）
- hub 标记 3D snap-rotate-settle → `orbit-3d-entry`（3D-flip entry）；technique CSS-3D
- upright 徽章顺时针轨道公转 → `orbit-3d-entry`（continuous elliptical orbit）；technique MotionPath
- 向中心镜头推入 → `multi-phase-camera`（PUSH-in）+ `coordinate-target-zoom`（target the core）
- 推入期间背景放大 → `multi-phase-camera`
- 持续缓慢 zoom-out（生态揭示）→ `multi-phase-camera`（pull-back）/ `coordinate-target-zoom`
- 描边文字 push-through dolly 开场（Social_Proof）→ `3d-text-depth-layers`（outline copy behind）+ `multi-phase-camera`（push-through）
- 推入期间外层节点景深模糊 → `depth-of-field-blur`（off-center 外层节点 progressive DOF/focus-falloff blur，内核心保持清晰）

**camera modifier**：push-in-with-DOF（Hook）——经 `coordinate-target-zoom` 对准核心的 `multi-phase-camera` PUSH-in；其 focus-falloff blur 一半由 `depth-of-field-blur` 支撑。Orbit finisher（Social_Proof）——卫星公转时经 `multi-phase-camera`（pull-back）持续缓慢 zoom-out。
