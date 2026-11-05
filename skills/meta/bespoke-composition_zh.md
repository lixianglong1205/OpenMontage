# 定制合成（Atelier 模式）

用于**从零手写合成**而非拼装库存 scene-type 的元技能（meta-skill）。这是「每次手工缝制」路径：针对 hero 级作品，每一像素的外观都是全新编写，因此没有两个视频共享同一视觉语言。

每当你为某件作品选择了 **atelier 模式**（见「何时使用」）时阅读本文。它不会直接给你组件——而是把你路由到所需的*原则、引擎机制与工具接线*，使你所构建的内容正确且独特。

> 统领下文一切的一条规则：**复用引擎知识，绝不复用创意组件。** Remotion 如何解析资源是引擎知识——可自由复用。某个过往视频长什么样是创意决策——绝不复用。

## 何时使用本技能（创作模式是提案阶段的决策）

OpenMontage 在提案阶段锁定三个正交轴：

- `renderer_family` — 创意语法
- `render_runtime` — 技术引擎（remotion / hyperframes / ffmpeg）
- **`composition_mode`** — **templated**（拼装库存 `cut.type` 场景）**vs. atelier**（手写）

默认选 **atelier** 的场景：营销、发布、需要打动人的讲解、品牌片，以及任何以质量为重的单次交付物。选 **templated** 的场景：批量产出、本地化变体、快速草稿、低风险的内部片段——可靠的一致性可接受、定制成本不划算的地方。在提案时向用户呈现选择，并像呈现 runtime 一样记入 `decision_log`（`category: "composition_mode"`）。

### Atelier 与两种 runtime

两种 runtime 对「定制」的处理不同——在假设该 doctrine 对两者映射相同之前，先读本节：

- **Remotion** 提供库存场景的 `cut.type` 注册表（`text_card`、`stat_card`、`bar_chart`、…），由 `Explainer`/`CinematicRenderer` 合成调度。那是 templated 默认。**Atelier 模式是逃生舱** — `composition_mode: "atelier"` 将渲染路由到 `_render_via_atelier`，完全绕过注册表，代理在 `projects/<slug>/` 下手写自己的 React 合成。
- **HyperFrames 本质上是 atelier。** HF 中没有 cut-schema — 每个合成都是手写的 `index.html`，带 `data-*` 时序属性和你编写的 GSAP 时间线。注册表（`hyperframes add`）是*块*注册表（颗粒叠加、转场）——是你合成的可选输入，不是调度整段渲染的场景目录。**当选择 `render_runtime: "hyperframes"` 时，作品已是 atelier 风格；`composition_mode: "atelier"` 是隐含的。** 本技能中的原则（艺术指导、场景差异性、无 hero 组件骨架、差异性审查）同样适用。通过 `hyperframes_compose` 渲染（或对手写合成使用 `npx hyperframes render` — 见第 5 节）。

因此：若 `render_runtime == "remotion"` 且作品是 hero 级，记录 `composition_mode: "atelier"` 决策。若 `render_runtime == "hyperframes"`，atelier 是默认行为，无需再论证；本技能仍在你写合成前用相同原则引导你。

若 atelier 生效（任一 runtime），库存 Remotion `cut.type` 目录、作为场景消费的 `hyperframes-registry` 成品块（相对作为原始输入）、fixtures，以及任何预烘焙创意组件均**禁止** — 它们是冻结外观，会重新引入雷同。

## 构建路线

按此顺序创作。每一步路由到既有知识 — 不要跳过第一步。

### 1. 为本主题*承诺*艺术方向 — 发散引擎
在写任何组件之前，决定只适用于**本**主题、不适用于其他的视觉语言。
先读 **`skills/meta/taste-direction.md`** 并撰写 `taste_profile`：设计解读、
`visual_variance`、`motion_intensity`、`information_density`、参考策略与
反模式。然后用 **`visual-style`** Layer 3 技能（CREATE 模式）锁定：色板、字体性格、
动效性格、版式系统，以及**本件独有的一个签名装置**。视频之间的差异在此保证 — 不是靠 withholding 组件，而是每次强制全新方向。写下来（项目中简短的 `art-direction.md`）并据此构建。

自问：*什么视觉隐喻属于本主题、且我此前未用过？* 若答案像某件旧作，你尚未找到方向。

### 1.5 将每个场景规划为独立合成 — 无 hero 组件骨架
最隐蔽的 templating 会在*场景*级溜回来：选一个 striking 视觉（蜡烛、浏览器框、分数环），然后在每个场景复用、只换下方文字。作品因 hero 定制而感觉定制 — 但每个场景在机制上是同一合成。那是品牌化幻灯片，不是电影。**不要那样做。**

艺术方向中命名的签名装置应出现在**一个或至多两个节拍** — 通常是高潮时刻 — 而不是每个场景的视觉脚手架。它因稀缺而显得有分量。

在写代码前，对计划中的每个场景具体回答：

- **本场景的主要视觉主体是什么？** 必须与上一场景*不同*。角色。图表。证据。 landscape。字体时刻。签名装置。虚空。每场景的主要主体即其职责。
- **这一节拍为何存在？** 它对叙事做了什么、且没有其他节拍能做的事？若合并两场景不损意义，就应合并。
- **视觉上与前后场景如何不同？** 不同构图（三分法 vs 居中 vs 分屏）。不同尺度（ intimate 特写 vs 广角）。不同动效 register（静 vs 忙）。不同色板 emphasis。不同字体处理。
- **若从本场景移除签名装置，场景是否仍成立？** 若是，签名装置可能不属于本场景 — 它只是 filler。删掉。

审查者以「scene_distinctness」检查强制执行（见
`skills/meta/reviewer.md` → Composition Authoring Mode Review）：记录每场景主要主体 + 首帧清单，并明确回答「是否有两场景共享同一主要视觉主体？」是 ⇒ CRITICAL ⇒ 重新规划。

推论：逐场景计划是*一等产物*，非隐含。在创作 `Composition.tsx` 前写下（在 `art-direction.md` 或并列的 `scenes.md`）。

### 2. 决定动效语言 — 原则，非预设
伸手拿**原则**技能，绝不拿成品动画：
- **`framer-motion`** 与 **`lottie-bodymovin`** — Disney 12 原则（anticipation、staging、
  follow-through、slow-in/out、arc、timing、exaggeration、appeal）。与 runtime 无关；在你自己的 Remotion `spring()`/`interpolate()` 代码中应用*原则*。
- HyperFrames 的 `references/motion-principles.md` — easing 即情绪，timing 即重量。

### 3. 仅在概念需要时启用更丰富的词汇

**在 Remotion 上** — 多数场景是 Remotion 原语。当*想法*需要时升级，非默认：`gsap-*`（经 SplitText 的 kinetic typography、经 MorphSVG 的形状 morph、经 MotionPath 的曲线运动、经 DrawSVG 的线描、自定义 easing）、`threejs-*`（3D）、`d3-viz`
（数据驱动自定义图表 — 手写图表；**不要** drop 库存
`bar_chart`/`line_chart`）、`manim-*`（数学）、`canvas-procedural-animation`（粒子/天气）。

**在 HyperFrames 上** — 词汇在 `/hyperframes-animation`：36+ 原子动效
**规则**（`kinetic-beat-slam`、`3d-text-depth-layers`、`motion-blur-streak`、
`physics-press-reaction`、`multi-phase-camera`、`depth-of-field-blur`、…），15+ 场景
**蓝图**（`kinetic-type-beats`、`comparison-split`、`dataviz-countup`、
`constellation-hub`、`ticker-takeover`、`device-surface-showcase`、…），16 **转场**
族（`css-distortion`、`css-destruction`、`css-radial`、`css-light`、`css-mechanical`、
…），以及单一合成下 **7 个 runtime 适配器**：GSAP 默认，外加 Lottie、Three.js、
Anime.js、CSS keyframes、WAAPI、TypeGPU（GPU compute）。 headline 能力是
`adapters/html-in-canvas-patterns.md` — 将 live HTML/CSS 捕获为 GPU 纹理并经 WebGL/Three.js 渲染以实现 cinematic bloom、shatter、liquid、portal 效果。每视频 1–3 个 hero 节拍使用，非每个节拍。**每节拍组合 2–4 条不同原子规则**，且
**全片至少使用 3 种不同 easing** — 这是 animation 技能中 baked 的 doctrine，非可选 polish。

HF 创意方向（色板/字体/旁白/节拍规划）读 `/hyperframes-creative`。
HF 资源（TTS/BGM/SFX/转写/抠图）读 `/hyperframes-media` 或
`/media-use`。HF CLI 工作流（init/lint/validate/inspect/snapshot/beats/render）读
`/hyperframes-cli`。`/hyperframes` 路由技能映射全部。

### 4. 把引擎机制做对 — gotcha 法典
这是你唯一「复用」之处：引擎已解决的问题。这些是框架如何工作的事实，不是外观。

**对于 Remotion**，研读 `.agents/skills/remotion-best-practices`（19 个规则文件：timing、
transitions、text-animations、transparent video、fonts、audio、sequencing、measuring text）。
也可读 `remotion-composer/src/components/` 中的库存组件 **作为机制法典 — 学 idiom，绝不 import 或模仿外观。**

**对于 HyperFrames**，合成契约在 `/hyperframes-core`（`data-*`
时序属性 — `data-start`、`data-duration`、`data-track-index` — 以及
必需的 `class="clip"`、`data-composition-id`、`window.__timelines` 注册、子
合成 mount）。每次改动后运行 `npx hyperframes lint && npx hyperframes validate` — 在渲染前捕获缺失 root attrs、缺失 clip id、GSAP target 未解析、重叠
tween、对比度失败。用 `npx hyperframes snapshot . --at <times>`
在 commit 全量渲染前视觉 spot-check 节拍。

若不知会咬人的 recurring 机制：
- **确定性**：每帧不用 `Math.random()` / `Date.now()` — 用 Remotion `random(seed)` 或
  seeded helper，否则粒子/easing 在渲染间 flicker。
- **每场景时长**：`useVideoConfig().durationInFrames` 返回*合成*长度，非
  你的场景。用传入的 `durationInFrames`/`Sequence` 驱动场景局部 timing，非全局。
- **资源路径**：URL 与 `staticFile()`（public/）处处可用；**`<Audio>` 拒绝 `file://`**
  （仅 `<OffthreadVideo>`/`<Img>` 接受绝对 `file://`）。把音视频放在 per-project
  public 目录并经 `staticFile` 引用。镜像 `resolveAsset` helper。
- **Remotion 中的 GSAP**：用 `paused` timeline 与 `.seek(frame/fps)` — 绝不用 `requestAnimationFrame`
  — 使帧确定性渲染。
- **字体（Remotion）**：在 module scope 用 `@remotion/google-fonts/<Name>` 的 `loadFont()`，一次。
- **HF data-* 契约**：每个 timed 元素需要 `data-start`、`data-duration`、
  `data-track-index`，**以及** `class="clip"` — 无 `clip` 则框架不管理
  visibility，元素会整段 timeline 在屏上。Root `<body>` 需要
  `data-composition-id`、`data-start="0"`、`data-duration`、`data-width`、`data-height`。
  每个 timeline 须为 `gsap.timeline({ paused: true })` 并注册为
  `window.__timelines["<composition-id>"]`。clip 与 GSAP target 使用稳定 `id` — `nth-of-type` 选择器在 validate 时不稳定。
- **字幕 vs 屏上文字 — 选一角色，同一内容绝不两者兼有。** 创作前每作品决定一次：字幕是在 spoken words 无法承载处增加含义
  （数字、姓名、翻译、引用 attribution），还是 echo 旁白的 accessibility 字幕？若场景已显示 verbatim 读稿的 SerifLine，**不要**再 emit 相同文字的 auto-caption — 重复短语即使其余场景很美也显业余。props 中 `captions=[]`，或
  仅 scope 到屏上文字与所说不同的场景。

### 5. 经 runtime 适当的定制路径渲染
定制合成是**一次性且项目本地** — 永不进入任何共享注册表。

#### Remotion atelier 路径
- 在 `projects/<slug>/` 创作（gitignored）。渲染工具经 mtime-skip copy 自动将你的 `.tsx`/`.ts`
  源 staging 到 `remotion-composer/projects/<slug>/`，以便 webpack 解析
  `node_modules` — 你的 source-of-truth 仍在 `projects/` 下。
- 用 `python scripts/scaffold_atelier_project.py <slug>` 脚手架 — 仅 emit 引擎
  plumbing（entry / Root / 空白 `Composition.tsx` / `art-direction.md` / props
  template / README）。零创意内容；占位符是故意丑陋的黑屏，使 post-render 审查正确拒绝未创作的脚手架出货。
- 媒体放在 `projects/<slug>/public/`，并作为 `bespoke.public_dir` 传入。
- 经 `video_compose` `operation="render"` 渲染：

```json
edit_decisions = {
  "render_runtime": "remotion",
  "composition_mode": "atelier",
  "bespoke": {
    "entry": "projects/<slug>/index.tsx",
    "composition_id": "<id registered in that entry's Root>",
    "props_path": "<absolute path to artifacts/props.json>",
    "public_dir": "<absolute path to projects/<slug>/public/>",
    "art_direction": "<short note or path to art-direction.md — REQUIRED>",
    "scale": 0.5,          // 0.5 for a fast draft; drop for the 1080p final
    "crf": 18,             // crisp final
    "concurrency": 8
  }
}
```

atelier 模式不需要 `asset_manifest` 或 `cuts` — 合成自有资源。
工具的 `_run_atelier_checks` 若任何源文件从库存
注册表 import（`src/components`、`src/Explainer` 等）则 render 失败，且 `art_direction` 缺失时 warn。

#### HyperFrames 路径
- 用 `npx hyperframes init <slug>` 脚手架（从 `projects/` 运行）。HF init 生成
  `index.html`、`meta.json`、`package.json`，以及 per-project `CLAUDE.md`，自动路由
  代理到 `/hyperframes` — 下一 session 确切知道加载哪些子技能。
- 手写 `index.html`。每个 clip 需要 `class="clip"` + 三个 `data-*` timing
  attrs + 稳定 `id`。当单文件 timeline 超过 4 clips 时用 `data-composition-src` mount 子合成（lint 会 catch 密度）。
- 对 music-driven 作品，在 `assets/` 放入音轨后运行 `npx hyperframes beats .` — emit `beats/<audio>.json`，含每 beat 的 `{time, strength}`，代理可将场景落在真实 drop（非猜测）。
- 渲染前验证：`npx hyperframes lint . && npx hyperframes validate . && npx hyperframes snapshot . --at <times>`。
  Snapshot 是 HF 原生 visual-spotcheck（所选时间戳 PNG 帧 contact-sheet）— 与 atelier `final_review.visual_spotcheck` 同样用法。
- **渲染**：调用 `video_compose`，`render_runtime: "hyperframes"`、
  `composition_mode: "atelier"` 及已创作的 `workspace_path`。路由到
  `hyperframes_compose.render_existing`，保留 `index.html` 并运行
  统一 check gate、strict render 与 post-render review。仅在 pipeline 外调试 runtime 时直接调用 `npx
  hyperframes render`。

## 护栏以免适得其反

- **差异性审查（取代一致性审查）。** 最终渲染前问：*这可以是任何其他产品的视频吗？是否复用了我曾做过的外观？* 若是，艺术方向失败 — 回到第 1 步。这与「是否匹配参考」相反。
- **禁止静默回退库存。** 「保持简单」适用于*机制*（10 行 spring 可以），绝不适用于*设计*（简单 ≠ 伸手 `text_card`）。若发现自己在 hero 作品上加 stock `cut.type`，停。
- **成本诚实。** Atelier 比 templated 消耗更多 agent token 与迭代。提案时说清，使用户知情 opt-in。无库存 baseline 时质量波动更大 — 用强原则技能（上文）与差异性审查缓解，而非重新引入复用。
- **检查点节奏。** 遵循 `skills/meta/checkpoint-protocol.md`：在生成资源**前**呈现脚本 + 场景计划供批准，然后 **assets gate**，再 first-render checkpoint。
  不要在 sign-off 前批量生成，且**不要为通过 assets 审查而渲染 draft** —
  assets gate 在 compose **之前**举行（见下）。

- **在 assets gate 用逐场景 still 填充 filmstrip。** 定制场景的「资源」是 `.tsx` 合成 — 不可缩略 — 因此 board 在 still 存在前无法展示。一旦合成可编译，在每个场景代表帧渲染一 still 到
  `projects/<slug>/snapshots/<scene_id>.png`，使 assets-gate filmstrip 显示真实帧而非「◆ BESPOKE」占位。用 Remotion still renderer（快 — 每场景一帧），由
  scene_plan timing 驱动：

  ```bash
  # one still per scene at mid-scene frame (fps * mid_seconds), into snapshots/<scene_id>.png
  npx remotion still projects/<slug>/index.tsx <CompositionId> \
    projects/<slug>/snapshots/<scene_id>.png \
    --frame=<mid_frame> --props=<abs artifacts/props.json> --public-dir=<abs public/>
  ```

  读取 scene_plan 并渲染全部 still 的 helper 在
  `scripts/atelier_snapshots.py`（`python scripts/atelier_snapshots.py <slug>`）。然后在 assets gate **STOP**。全量/draft 渲染是批准后的 **compose** 阶段。

## 工作先例（学*流程*，非外观）

两件参考作品 — 每 runtime 一件 — 只研究**过程**，绝不学视觉语言：

- **Remotion atelier** — Phantom Reach explainer（`projects/phantom-reach-explainer/`）：
  Playwright 捕获的应用 footage 加 PII-blur 层 → 逐句 TTS 与 silence beat 拼接 →
  免费 Pixabay 音乐 → 手写 Remotion 场景（custom intro、
  score-ring、agentic flow、CTA）于一次性 violet 主题。
  Compound Snowball（`projects/compound-snowball/`）与 Library of Alexandria
 （`projects/alexandria-fire/`）另两件 — 三件 Remotion atelier，三种
  完全不同的视觉语言。

- **HyperFrames** — `in-a-hurry`（`projects/in-a-hurry/`）：music-driven kinetic-typography
  作品，用 HF 0.7 的 `beats` 命令将场景 timing 锁在真实 drop。演练
  **5 类** `/hyperframes-animation`：`kinetic-beat-slam`、`3d-text-depth-layers`
 （stacked extrusion）、`motion-blur-streak`（echo-ghost trails）、`transitions/css-distortion`
 （chromatic-aberration RGB-split）、`adapters/html-in-canvas-patterns`（Three.js +
  UnrealBloom 于 hero punchline）。每 beat 用 distinct easing（`expo.out`、
  `back.out(2)`、`circ.out`、`sine.inOut`）。

**不要复现其中任一视觉语言** — 下一件必须与它们都不像。
这就是要点。只学*过程*（决策、顺序、gates、
验证）。

另见：`skills/meta/animation-runtime-selector.md`（runtime + 库路由）、
`AGENT_GUIDE.md` → "Composition Authoring Mode"、`/hyperframes`（HF 路由与
能力图）。
