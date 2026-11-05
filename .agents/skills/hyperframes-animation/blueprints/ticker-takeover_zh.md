# ticker-takeover — 滚动条位替换 / 接管

**意图**：先以打字机效果输入一句语境短语，再用强调词像老虎机一样在若干选项间竖向滚动切换，暗示「这可以是很多种东西」；随后一位 hero 从画外猛冲入场，把整段文字物理推开——「其实，就是它。」是碰撞，不是淡入淡出。

**适用角色**

- Hook（来自 `takeover-ticker-displace`）：当静态引导语 + 循环切换的强调词需要被 hero 以动量**物理替换**（而非交叉叠化）时，且终帧只剩 hero。若接管应读成「撞击感」，选此蓝图。
- Brand_Outro：同一碰撞用作片尾——选项循环切换，品牌标识猛冲入画并占据画面。

**时长**：5–7s

**镜头结构**（`[bg]` 画布；左侧/居中一组文字，被入场的 hero 顶出画面）

- **Scene 1（0.0–~1.4s）— 语境铺垫。** 打字机逐字打出 `[lead-in phrase]`（流畅、无打错——卖的是笃定，不是人为混乱）。镜头静止。
- **Scene 2（~1.4–3.0s）— 循环节拍。** 行内 `[accent word]` 槽位以竖向弹簧滚动在 2–3 个 `[options]` 间切换（每跳一词），暗示广度——「这可以是很多种东西」。（超过约 3 个会像 filler。）
- **Scene 3（~3.0–4.2s）— 碰撞（招牌动作）。** `[hero]` 从画外带 momentum 猛冲入画，整组文字被**物理推开**——文字随撞击位移，不淡出。hero **重重**落地——更长的 settle，不是一闪即停——读成质量感，不是纯速度。
- **Scene 4（~4.2–end）— 只剩 hero。** hero 在正中落定并保持静止。hold。

**动效词汇**：流畅单句打字机引导；竖向弹簧 ticker 词滚动（2–3 步）；画外 hero 猛冲入画；被击文字组的 reactive displacement；偏重、长尾 landing（非弹跳）；落定 hero 的双轴 subtle jitter。

**规则映射**

- 流畅单句打字机引导 → `discrete-text-sequence`（smooth-slice / 连续 `floor(progress)` 形式——无打错 machinery）
- 强调词槽位在选项间老虎机式循环 → `vertical-spring-ticker`（`STEPS` = hero 将替换的选项数；该规则的 footer-reveal 不用——由 Scene 3 取代）
- hero 撞击时推开文字组 → `reactive-displacement`（文字为被位移质量；hero 的「重落地」用更长的 `power2` settle 表达，而非规则默认的 `back.out`）
- hero 快速画外冲入 → `motion-blur-streak`（方向性速度模糊，落地时收束为清晰）
- 落定 hero 的「活感」→ `sine-wave-loop`（低幅度双频 register——scale + rotation jitter 叠在 hero 最终落地 scale 上；绝不对 1 做 yoyo）

**镜头修饰**：camera-static——位移发生在元素空间（hero 推动文字），无真实镜头运动；撞击即唯一动势。
