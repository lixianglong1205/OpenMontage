# titlecard-reveal — 标题卡 / 单卡揭示

**意图**：平静的喘息/落点节拍——用恰好一次克制的动作（上滑交叉淡入，或擦除揭示）呈现一张干净的主标题或单张品牌/证明卡片，随后静止定格。低动效本身就是内容，而非缺陷。

**适用角色**

- Benefits（来自 `benefits-titlecard-crossfade`，#34）：平静的双行价值标题卡——先主标题价值行，再通过一次上滑交叉淡入切换到限定/补充说明行并居中定格。
- Social_Proof（来自 `social-proof-reveal-card`，#35）：用一条对角药丸形扫过，将繁忙的应用拼贴画面擦开，揭示干净的品牌锁定（图标 + 字标），以及居中「深受 [N]+ [audience] 团队喜爱」类社交证明文案，经弹簧式落定后保持。

**时长**：3–5s（Benefits 3–4s；Social_Proof 约 5s / 实测 4.7s）。

**镜头结构**

```
Scene 1 (0.0–~0.4s): static camera on [neutral / dark background]. Establish the opening state.
  Variant — Benefits: empty-to-text — [benefit line 1] is about to fade in centered (no busy open).
  Variant — Social_Proof: a busy intro frame holds briefly — an [app-screenshot / use-case collage] of overlapping cards under a [setup line].

Scene 2 (~0.4–~1.5s): the ONE move executes — a single restrained reveal that brings the calm card to center.
  Variant — Benefits: [benefit line 1] fades in centered while scaling slightly (~95%→100%, smooth ease-out) and holds.
  Variant — Social_Proof: a large [accent-color] rounded pill sweeps diagonally bottom-left → top-right and exits the corner, clip-path wiping the collage away to reveal the [brand logo lockup] beneath as the [logo icon] strokes draw on.

Scene 3 (~1.5s–end): the revealed/settled card holds to the end (the allocated stillness). At most one subtle live element (a slow breathing pulse on the card, or a very slow camera drift). No second development phase.
  Variant — Benefits: [benefit line 1] translates up and fades out as [benefit line 2 — qualifier / elaboration] translates up from below center and fades in to take center; holds. (This single slide-up crossfade IS the one move — Benefits front-loads no Scene-2 wipe.)
  Variant — Social_Proof: the lockup — [logo icon] centered, [wordmark] below, centered [social-proof tagline] "Loved by [N]+ [audience] teams" (the [N]+ may count up) — spring-settles small, then holds.
```

**动效词汇**：单次克制揭示（轻柔淡入 + 轻微放大落定 | 对角 clip-path 药丸擦除）、两行居中文案间的一次上滑交叉淡入（Benefits）、图标描边绘制（Social_Proof）、可选「[N]+ teams」数字递增、logo+标语弹簧落定并保持、定格卡片上的微弱呼吸、保持至结束。平静语域——无弹簧链、无翻滚、无逐拍翻转、无第二阶段。镜头静止（仅可选极慢漂移）。

**规则映射**

- gentle fade-in + subtle scale-up settle（Benefits Scene 2）→ `rules/scale-swap-transition.md`（克制的入画/落定；交叉引用 `techniques.md` 中的淡入缓动）
- single slide-up crossfade between two centered lines（Benefits Scene 3）→ `rules/discrete-text-sequence.md`（一行交接下一行；上移 + 交叉淡入）
- diagonal pill-wipe reveal（Social_Proof Scene 2）→ `rules/techniques.md`（clip-path 揭示遮罩——擦除）
- icon stroke draw-on（Social_Proof Scene 2）→ `rules/svg-path-draw.md`
- "[N]+ teams" count-up（Social_Proof Scene 3，可选）→ `rules/counting-dynamic-scale.md`
- logo + tagline spring-settle-and-hold（Social_Proof Scene 3）→ `rules/spring-pop-entrance.md`（单次柔和落定；刻意单拍，非链式）
- subtle breathing on the held card（定格期间唯一的动态元素）→ `rules/sine-wave-loop.md`

**镜头修饰**：可选——仅在定格阶段使用一次极慢漂移/推进 → `rules/multi-phase-camera.md`。默认为完全静止；除非否则定格会像静帧，否则不要添加。

**静止说明**：这是合法分配的静止节拍。Scene 3 的定格是交付物，而非未动画的空档——不要人为制造发展阶段、额外切换或强行加动画。一次克制动作 + 微弱定格（可选一个呼吸元素或一次慢漂移）即为正确且完整的形态。
