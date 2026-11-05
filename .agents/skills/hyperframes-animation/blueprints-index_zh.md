# 蓝图（已验证的形态）

> 蓝图层的入口。读本文以找到某一帧的形态；读 `blueprints/<id>.md` 以实例化。Step 4 方法（Reproduce / Adapt / Compose，每帧写什么）在 `visual-design.md` — 本文件是菜单 + 选择器。

**蓝图（blueprint）** 是与产品无关的、**带时间码的镜头模板** — `Scene N (a–b s): …`，含 `[slots]` 与一个命名的 **signature move** — 从 50 段黄金产品发布片段（外加 13 个 hyperframes-animation 蓝图反译为同一 brief 格式）逆向归纳而来。它编码整段镜头在全时长内的结构 — 揭示节奏对齐旁白，而非在 t=0 一次性堆满 — 因此按结构实例化一条时，内容会持续进入画面而非冻结。完整模板在 `blueprints/<id>.md`。**Step 4（视觉设计）为每一帧实例化一条蓝图**（或在无一合适时从 motion vocabulary 组合）。

## 15 条蓝图

<blueprints>
<blueprint id="kinetic-type-beats" roles="Hook, Problem, Product_Intro, Benefits, CTA, Brand_Outro" duration="3.4–12s">
扁平、居中、粗体字镜头，**动效即词语更替** — 固定一行通过硬切就地换词，或全屏分 beat 的陈述逐 beat 叠加各自动效，再以 spring-pop 收束。万金油（6 个 role）。当文案承载镜头、且无场景、界面或点击时优先选用。
</blueprint>

<blueprint id="typewriter-reveal" roles="Hook, Brand_Outro" duration="3.6–7s">
可见文本光标 **像真人一样键入（并编辑）一行**，随后收束该行并弹出品牌收束，或在持久标识下保持该行同时副行键入最终 CTA。当「有人在打这段字」应是引擎时选用 — 可共情的打字式痛点 → 品牌，或常驻 logo + 打字式 CTA 条。
</blueprint>

<blueprint id="spatial-pan-stations" roles="Hook, Problem" duration="7–10s">
在一张超大画布上预先摆好 **带标签的站点**，由单一虚拟摄像机 **一次横移/斜移扫过** — 重复平移将每个站点居中并揭示标注，最后在末站定格。用于里程碑时间线平移到「我们」，或痛点站点互联网收束于乱结。
</blueprint>

<blueprint id="constellation-hub" roles="Hook, Social_Proof" duration="5–6s">
带图标的 **节点弹入成环围住中心**，再收束到核心 — 摄像机推入（景深 collapse 到其上）或定格 hub 标识且卫星环绕。用于「连接一切 / 一个 hub」或「处于你的 stack 中心」。
</blueprint>

<blueprint id="grid-card-assemble" roles="Key_Feature, Benefits, Social_Proof" duration="3.0–10.5s">
N 个条目（tiles / cards / logos / list-lines）**以交错级联自组装** 成网格或竖向列表并定格；可选摄像机 zoom-OUT 在更大整体中揭示阵列。用于一次枚举广度 — 功能网格、累积收益列表或 logo 墙。
</blueprint>

<blueprint id="logo-assemble-lockup" roles="Product_Intro, CTA, Brand_Outro" duration="4.6–11s">
品牌标识 / wordmark **从部件自行构建**（元素 assemble/orbit、字母 cascade、描边绘制，或摄像机穿过负空间），收束为居中 lockup，可延伸至 URL/CTA。用于无声高端品牌 sting，或 logo 构建导向最终行动号召。
</blueprint>

<blueprint id="cursor-ui-demo" roles="Product_Intro, Key_Feature" duration="4.0–9.3s">
可见自定义 **光标驱动重建的应用 UI**，经点击/悬停/拖拽使屏幕逐镜变状态，摄像机追逐每次交互。用于首次光标引领看界面（Product_Intro），或一条工作流端到端演示至操作按钮（Key_Feature）。
</blueprint>

<blueprint id="device-surface-showcase" roles="Key_Feature" duration="7.8–9.6s">
**设备 mockup 或浮动窗口作 hero 定格**，其屏幕循环真实流程，摄像机从静态 hold 到连续 3D 推镜。Role 窄（仅 Key_Feature）但 mechanic 丰富（static tour · floating-window push-scroll · 3D-hand demo）。用于在 *真实界面内* 展示功能体验。
</blueprint>

<blueprint id="dataviz-countup" roles="Problem, Product_Intro" duration="6–12s">
数字与图表为 hero — **count-up ring/number、trend chart、tilted stat grid** — 摄像机 push THROUGH（或 scroll 横过）并落于一个 hero metric。当数据承载论点时选用：量化恶化中的问题，或自信开场「看结果」。
</blueprint>

<blueprint id="titlecard-reveal" roles="Benefits, Social_Proof" duration="3–5s">
平静的 **breather/landing beat** — 一条干净 title 或单张品牌/证明卡片，以 **恰好一种** 克制动效 reveal（slide-up crossfade 或 wipe-away-to-reveal），随后静止 hold。低动效即 payload，非缺陷。用于两行价值标题，或 busy open wipe 至 clean lockup +「loved by N+ teams」统计。
</blueprint>

<blueprint id="comparison-split" roles="Key_Feature" duration="4–6s">
两个等权配对项从对侧进入，**镜像 3D「book-open」tilt** 并排 hold，随后 inner-edge pill badge 各 spring-pop 以强调。用于 A/B 或「X + Y together」— 两种互补能力同时权衡（非 >2 项，非顺序步骤）。
</blueprint>

<blueprint id="overwhelm-surround" roles="Problem" duration="6–9s">
以累积制造 overwhelm — 可识别界面 assemble，密度标记图标 scatter in，中心一项 **morph 为观众自己的 avatar**，随后元素从四面 close in（surrounded，非 zoom-into）。当痛点是「被工具埋没」时选用，收束于 claustrophobic crowd。
</blueprint>

<blueprint id="ticker-takeover" roles="Hook, Brand_Outro" duration="5–7s">
打字式 lead-in + accent word 在选项间 cycle，随后 hero **从画外 crash in 并物理推开文案** — collision，非 fade — 独自 settle。当「可以是很多种」的 build 应被暴力替换为「就是这个」时选用。
</blueprint>

<blueprint id="video-text-pivot" roles="Product_Intro, Key_Feature" duration="6–8s">
产品视频居中 hold 并 breathe，随后 **slide aside 把重量交给 hero stat**，随后两者 clear，kinetic text 键入 vacated center，由 gradient pill  seal。用于「看功能 → 看影响」，视频须保持可见（slide，never cut）。
</blueprint>

<blueprint id="cta-morph-press" roles="CTA" duration="4–6s">
静止品牌标识 **在同一 center condense 为更亮的 CTA**，随后 cursor 到达并以 human-aimed click 带 feedback land。用于聚焦的「点这里」sign-off，视线从 identity 到 action — 无 spatial set，无 multi-step UI。
</blueprint>
</blueprints>

## Role → 蓝图菜单

**SOFT** 菜单：故事真实优先。Story-design **仅在产品自身节拍需要该形态时** 才介入 — 它建议已验证形态，从不规定必须有哪些节拍。每个 role 有 2–4 个选项；若无合适项，可自由 compose（菜单不是 checklist）。每一行是应让你 **选用该 blueprint** 的 **触发条件**。

此处 role 与 storyboard frame `type` enum 1:1 对应：**Hook**=`hook` · **Problem**=`pain_point` · **Product_Intro**=`product_intro` · **Key_Feature**=`feature_showcase` · **Benefits**=`benefit_highlight` · **Social_Proof**=`social_proof` · **CTA**=`cta` · **Brand_Outro**=`branding`。

**Hook**

- `kinetic-type-beats` — 有力修辞句 /「你一直在做 X」式 callout，就地换词即笑点，或逐 beat 升级的陈述以 spring-pop 收束。
- `typewriter-reveal` — 键入可共情一行，收束，弹出品牌（logo 或 product-UI）—「日常痛点，这是我们。」
- `spatial-pan-stations` — 里程碑时间线平移到当下（「演化 leading up to us」）。
- `constellation-hub` — 工具/节点星座 + 摄像机推入（「连接一切」）。
- `ticker-takeover` — 循环 accent word（「可以是 X，或 Y…」）被画外冲入的 hero 暴力替换。

**Problem**

- `kinetic-type-beats` — 3–5 条短痛点陈述，各在空白画布单独落定，尚无产品。
- `spatial-pan-stations` — 平移互联痛点「站点」网，收束于乱结。
- `dataviz-countup` — count-up ring / chart / stat grid 推穿而过， dramatize 恶化或巨大的问题。
- `overwhelm-surround` — 可识别工具 morph 为观众，随后任务气泡从四面收拢（「你被埋没」）。

**Product_Intro**

- `kinetic-type-beats` —「Introducing…」硬切 name-drop 落于品牌名/logo。
- `logo-assemble-lockup` — 无声高端品牌 sting（元素 pulse/orbit 并 assemble 于 mark 周围）。
- `cursor-ui-demo` — 首次看产品界面；光标扫入介绍 app。
- `dataviz-countup` — 硬切进入 data-viz 卡片网格，摄像机 scroll 至 glowing hero metric + kinetic tagline。
- `video-text-pivot` — 产品视频侧滑把视觉重量交给 hero stat，随后让出中心给 kinetic impact text。

**Key_Feature**

- `grid-card-assemble` — 带 label 的功能 tile/pill 网格自组装（或 glass card 由 camera zoom-out 揭示）。
- `cursor-ui-demo` — 特定多步工作流端到端演示，落于操作按钮/结果。
- `device-surface-showcase` — 设备/窗口 hero，屏幕循环（static tour · floating-window push-scroll · 3D-hand demo）。
- `comparison-split` — 两种配对能力并排，镜像 book-open tilt（A/B /「X + Y together」）。
- `video-text-pivot` — 功能片段侧滑至满帧 metric，随后 typographic impact line。

**Benefits**

- `kinetic-type-beats` — 8–12 条短价值短语的快速 staccato montage。
- `grid-card-assemble` — 竖向收益列表累积或逐步呈现。
- `titlecard-reveal` — 平静两行价值标题卡（breather/stillness beat）。

**Social_Proof**

- `constellation-hub` — 产品 mark 为 hub，partner logo 环绕（「works with your stack」）。
- `grid-card-assemble` — logo 墙构建后 pull back 揭示 vast ecosystem。
- `titlecard-reveal` — wipe busy open 至 clean brand lockup +「loved by N+ teams」统计。

**CTA**

- `kinetic-type-beats` — 有力 closing line（或短 value stack）逐 beat snap 至 logo/URL。
- `logo-assemble-lockup` — logo build → camera push-through 进入最终 URL/CTA 动词。
- `cta-morph-press` — 品牌 mark 在同一 center condense 为 CTA，随后光标 human-aimed click 落定。

**Brand_Outro**

- `kinetic-type-beats` — 快速动词连发落于品牌的一个 defining word。
- `typewriter-reveal` — 持久品牌 mark，下方 typed/swapping CTA rail。
- `logo-assemble-lockup` — 功能/UI 元素清场，lockup 自行绘制进入。
- `ticker-takeover` — 选项循环，随后品牌 mark crash in 占有画面。

> 覆盖：每个 role ≥2 选项；每条 blueprint 服务 ≥1 role。`kinetic-type-beats` 为 workhorse（6 roles）；`device-surface-showcase` role-narrow（仅 Key_Feature）但 mechanic-rich。五条形态 — `comparison-split`、`overwhelm-surround`、`ticker-takeover`、`video-text-pivot`、`cta-morph-press` — 来自 hyperframes-animation blueprints 增补。

## 选择指引

1. 在上文菜单中找到该帧的 **role**；选 **形态 fit 此 beat** 的 blueprint（story 可能已命名 candidate id — 确认或 override）。若两条都 fit，优先动效更接近你方案的那条。
2. 打开 `blueprints/<id>.md` — 读其 time-coded template、`[slots]` 与 named **signature move**。
3. 选 posture — **Reproduce**（slots 干净映射）、**Adapt**（结构 fit，content/surface 不同；保留 signature move）、或 **Compose**（无一 fit → 从 motion vocabulary 构建）。每帧怎么写 — 保留/改动、per-frame fields — 属 `visual-design.md`；defer 到该文。
4. 若菜单无一 fit 该 beat，从 `motion-language.md` 的 motion vocabulary **compose** — 仍按 VO 在镜头全长 pace reveals。勿硬套错误 blueprint。

## Motion 覆盖

黄金 vocabulary 中每个 recurring move 由本 skill 本地 `rules/` 支撑 — 含为补全语料增补的五条：`depth-of-field-blur`、`motion-blur-streak`、`depth-scatter-assemble`、`spring-pop-entrance`（canonical entrance pop，区别于 click/press 的 `press-release-spring`）、`ambient-glow-bloom`。每条 blueprint 的 `rule mapping` 引用真实 rule。

仍有一处 genuine out-of-scope special：`device-surface-showcase` 的 **3D-hand gesture-input + WebGL bloom/portal** 需 R3F/Three.js + WebGL — 重于 rule library。请 sparingly 使用，或选更简单的 `device-surface-showcase` variant。
