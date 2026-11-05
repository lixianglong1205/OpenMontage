# comparison-split — 对比分屏卡片

**意图**：两个权重对等的配对项以镜像 3D「书本展开」式倾斜并排展示——观众将其读作平衡对比，随后药丸形徽章落在各卡片内缘以作点缀。动效即对称：两张卡片从相对两翼飞入并保持展开姿态。

**适用角色**

- Key_Feature（来自 `comparison-split-cards`）：当两个互补特性/能力权重相等、需**同时而非依次**呈现时——A/B、 「X + Y 齐现」、观众需并排权衡的成对概念。不适用于超过 2 项（用 `grid-card-assemble`）或顺序步骤。

**时长**：4–6s

**镜头结构**（承载两个 faint 环境光晕的 `[bg]` 画布——`[accent A]` 约在 30%、`[accent B]` 约在 70%——使两侧在 50% 对称轴上各拥有一种色彩身份；等宽卡片置于同一共享透视父级下）

- **场景 1（0.0–~0.8s）— 标题确立概念。** 居中的 `[title line]` 与 `[accent keyword]` 从略上方**向下滑入**就位（短而平滑的落定）。向下到达是刻意的：与接下来从两侧进入的卡片形成不冲突的 T 形构图。
- **场景 2（~0.4–1.9s）— 分屏倾斜入场（标志性动作）。** 两张等宽特性卡片从相对两翼进入——`[left card]` 自左、`[right card]` 自右且约滞后 ~0.2s——各带**镜像 3D `rotateY` 倾斜**（左面向右、右面向左，如书本翻开）并在落地时缩放约 0.85→1。入场与标题尾部重叠，整体读作**一次**到达而非两拍。各卡片承载 `[image / label / subtitle]`；盒阴影随倾斜**向外**落下（左卡阴影向右、右卡阴影向左）。
- **场景 3（~1.9–结束）— 徽章点缀后保持。** 药丸形 `[badge]` 落在各卡片**内缘**（先左后右，间隔约 ~0.3s），与卡片重叠约 15% 以读作附着而非环绕。这是本镜头唯一的 overshoot——用以赢得点缀感。落定并保持。

**动效词汇**：标题自上向下滑入落定；镜像相对翼卡片入场；静态书本展开式 `rotateY` 倾斜（左 `+tilt`、右 `−tilt`）；与倾斜匹配的外向 box-shadow；内缘徽章 spring-pop；轻柔反相 idle 浮动（左 vs 右，永不同步），登记为 subtle jitter；双侧环境 side-glow。

**规则映射**

- 两卡自相对两翼入场、镜像 `rotateY` 倾斜 + 与倾斜匹配的阴影 → `split-tilt-cards`（标志性；保持双层 split，使入场 `x`/`scale` 与 idle 永不在同一 alias 上冲突）
- 标题向下滑入落定 → `gsap-effects`（长尾 `power3` 上的 translate + opacity）
- 内缘药丸徽章 pop（唯一 overshoot）→ `spring-pop-entrance`（overshoot 登记——赢得点缀）
- 成对反相 idle 浮动 → `sine-wave-loop`（低振幅登记——subtle jitter，非 lazy breathing；左 `sin(t)`、右 `sin(t+π)` 以免 conveyor-belt）
- 卡片后方两道 faint 侧向光晕 → `ambient-glow-bloom`（未触发的 soft bloom，每 accent 一道）

**镜头修饰**：默认 camera-static——对称即主体，运镜会破坏平衡。
