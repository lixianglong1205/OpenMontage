# cta-morph-press — CTA 形态变换与按压

**意图**：静止的品牌标识在同一屏幕中心凝缩为更小、更亮的 CTA，随后光标从画面外进入并落在其上，完成一次拟人化的点击。观众视线从「这是谁」被引导至「该做什么」。形态变换与点击是两大核心节拍。

**适用角色**

- CTA（来自 `cta-morph-press`）：当片尾从品牌识别过渡到单一用户行动、两个元素在同一中心先后出现（形态变换而非硬切）、并以带物理反馈的模拟点击收尾时使用。适合聚焦的「点这里」式收束——无空间场景、无多步 UI（那是 `cursor-ui-demo`）。

**时长**：4–6s

**镜头结构**（`[bg]` 画布；hero 与 CTA 为 flex 居中兄弟节点，共享同一 `transform-origin`）

- **场景 1（0.0–~1.4s）— 在场。** `[hero mark / brand lockup]` 稳守正中，有生命感但静止——仅标识上有极轻微的旋转呼吸；其下标题文字保持完全稳定。镜头静止。
- **场景 2（~1.4–2.4s）— 形态变换（标志性动作）。** hero 在同一屏幕中心凝缩为更小、更亮的 `[CTA]`（按钮 / 卡片）：原标识缩小淡出，与 CTA 在原位放大进入完全同步。因共享同一 `transform-origin`，视觉上读作同一元素在变形，而非切换。
- **场景 3（~2.4–3.4s）— 接近。** `[cursor]` 从画面外沿 **减速** 路径进入（是「抵达」而非「穿过」），落在 CTA 几何中心偏几 px，使瞄准感拟人、非脚本化。
- **场景 4（~3.4–结束）— 按压。** 光标完成带物理感的点击——光标与 CTA 同步压缩，再随反馈释放（可选涟漪 / 光晕绽放）。定格于点击后状态。

**动效词汇**：仅旋转的极轻微静止呼吸（限定在 logo 范围）；同中心 morph-swap（缩小淡出 ↔ 放大进入，共享 `transform-origin`）；光标自画面外减速抵达；偏中心拟人瞄准；同步按压压缩；释放反馈涟漪 / 光晕。

**规则映射**

- hero → CTA 同中心凝缩 → `scale-swap-transition`（共享 `transform-origin: 50% 50%` 强化 morph 感；CTA `position: absolute` 以免短暂重叠时顶开 hero）
- 静止 hero 活感（仅旋转，作用域在标识上，避免与 Phase-2 scale 冲突）→ `sine-wave-loop`（低幅度旋转档位——轻微抖动，非 scale 呼吸）
- 光标按压与释放同步（single-target-array 使二者同步压缩）→ `physics-press-reaction`（PRESS_DOWN + RELEASE 段）
- 光标接近（自画面外减速、偏中心落点、opacity 硬切进入）→ `gsap-effects`（`power2.out` 上的 translate）
- 点击涟漪 / 释放光晕 → `cursor-click-ripple`（attack-decay 环）和/或 `ambient-glow-bloom`（释放 bloom）

**镜头修饰**：camera-static—— morph 与点击发生在元素空间；镜头运动会与点击高潮抢戏。
