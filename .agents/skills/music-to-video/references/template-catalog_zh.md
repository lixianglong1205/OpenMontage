# 模板目录 — 选型菜单（第 3 步）

逆向工程、无资产的**组模板（group templates）**。本文件是规划器（planner）**唯一**用来挑选模板的一览——**不要**为选型去打开模板的 `index.html`。一个模板实现一帧中的**一组**（一帧可叠多组；品牌主线统一它们）。

**如何挑选。** 对每一组，读该帧的 `pacing` + `mood` + 骨架里的一行音乐情境，再扫下面的 **适用场景** + **最佳时长**，取最接近的一项。若没有合适项，从 [`motion-primitive-catalog.md`](motion-primitive-catalog.md) **自由编排**——这是正当选择，不是失败。

**品牌来自 `frame.md`，而非模板。** 模板自带演示调色板（`theme` / `palette` / 颜色类参数）。用项目 `frame.md`（所选预设的颜色 + 字体）填这些参数，使各组读成一体——模板提供**动效 + 版式**，预设提供**外观**。

**Params** 列出以便在分镜里填内容槽位。精确语义与默认值在各模板的 `index.html`（`data-composition-variables`）——frame-worker 在构建时读取；你只需给出取值。

节奏标签：下列模板除 `held-message-living-field` 为 **phrase_flow** 外，均为 **beat_cut**。切勿把 beat_cut 模板放在 phrase_flow 帧上。

## 组时长纪律

模板按**组**选，不是按帧。帧长于模板的**最佳时长**时，通常应在真实 audiomap 锚点（`SURGE`、`DROP`、roll 边缘、hard_stop、phrase 边缘）拆成多组，而不是把同一模板拉满整帧。

- 下面的**最佳时长**指有效处理跨度：模板系统在做出有意义动效的那一段。末尾短可读 hold 可以；若出现长空白尾段，应换一组。
- **超过约 6s 的帧**通常需要 2+ 组。beat-cut 例外是有真实子阶段的丰富程序（`poster-tile-mosaic`，有时 `card-flyby`）；phrase-flow 例外用 `held-message-living-field`。
- **Roll 类模板是一次 roll 工具。** 若一帧有两个 roll 或 roll 间有 drop，拆成两组。
- 不要靠放慢所有 tween 来拉长。保留模板动效感，再用 hold / 调色变化 / 新组填多余时间。

---

### card-flyby

- **是什么** — 一列有深度的卡片在透视中向前滚动；每次 landing beat 把下一张卡片 tumbling 进前排槽位并做纯色 wipe，旧前排向镜头落下；dwell 缩短 card-to-card 间隔使牌组加速，最后停在一张 held 卡片上。
- **适用场景** — 离散 onset **加速**（间隔缩短 / build 进 downbeat），且要按 hit **闪一系列条目**——标题、项目、海报、tile——每张一次 hit， climax 为 held 卡片。
- **最佳时长** — **4–6.5s**（4–7 次 landing + 短 final hold）；若需 **>7s**，在下一 downbeat 拆分。
- **Params** — `theme`, `bgColor`, `cards`, `landings`, `yaw`

### held-message-living-field · phrase_flow

- **是什么** — 可读标记（logo / 词 / 标题）在柔和、变色的模糊场域上完全静止；仅场域在呼吸。
- **适用场景** — **平静 / 稀疏**段且 onset 荒漠——有能量但 onset 少或没有（held pad 或 riser）；有一个词或标记要 hold 并让它呼吸。
- **最佳时长** — **6–16s**；这是长组例外。低于 4s 显得未展开；超过约 20s 需要状态变化或另一组。
- **Params** — `markText`, `titleText`, `tagText`, `palette`, `flowSpeed`, `duration`

### held-text-strobe-burst

- **是什么** — 完全静止的词，字母每约 3 帧在纹理填充帧间切换（texture-clipped fill + 每帧 tint + 背景色），短 burst 钉在 roll 上。
- **适用场景** — **密集、重击的 roll / fill**，且有一个词要在几小节里用纹理 strobe。纹理遮罩 PNG 在 `assets/` 下随模板提供。
- **最佳时长** — **1.2–3.5s**；strobe 疲劳来得快，上限约 4s 后切到更干净的系统。
- **Params** — `markText`, `fontStyle`, `markScale`, `idleColor`, `idleInk`, `frames`, `strobePlan`, `decor`, `duration`

### intro-kinetic-cascade

- **是什么** — 一行拆成一系列大号编辑式**短语**（每条为叠放海报，一个放大 hero 词），在各自锚点上逐词 reveal，短语间 hard cut， climax 为带可换 ringing **icon**（bell / cursor / sparkle / emoji / SVG）滑入的短语。
- **适用场景** — **片头 / 开场陈述**：短句按词 landing 成大字号， climax 为一个关键词 + icon。中等及以上能量、稳定 grid。
- **最佳时长** — **3.5–7s**（2–4 个 phrase beat）；若陈述需要更久，下一句做成新组。
- **Params** — `theme`, `icon`, `phrases`, `climax`

### logo-split-lockup-pulse

- **是什么** — 中心拼接的两段 mark 左右↔分裂开 gap，每个 onset 在 gap 中 grow 一个 center word-lockup（关键词在 downbeat surge 上 landing），hit 上 snap 闭合，随后随 beat pulse。
- **适用场景** — 短 **logo / 品牌 sting**（非打字句子）：快而密的 onset +  sustained roll bed 用来 pulse，左右 bracket 式 mark。
- **最佳时长** — **2–4s**；**>4.5s** 会像 sting 被拉太长。之后接单独的 held-lockup / 下一概念组。
- **Params** — `bgColor`, `markColor`, `textColor`, `leftMark`, `rightMark`, `word1`, `word2`, `word3`, `word4`

### poster-tile-mosaic

- **是什么** —  packed **马赛克**：不同尺寸色块 tessellate 填满画面（无重叠），由可互换的 beat 同步操作驱动：staggered enter/exit、锁定全局 recolor、snake-fill + overlay。
- **适用场景** — 许多离散、可单独放置的 onset（每次 tile 移动一次 hit），且子阶段要用不同方式 articulation（accumulate → recolor-on-roll → fill-then-drop）。密集段最好作为**一个**丰富 tile 程序持有，而非拆分。
- **最佳时长** — **4–7s**，仅当程序有清晰子阶段时可到 **8s**。若音乐换 regime，即使 tile 系统还能继续也要拆分。
- **Params** — `bgColor`, `tiles`, `bands`, `gap`, `showText`, `labels`, `program`

### roll-flipbook-word-cycle

- **是什么** — hi-hat roll 驱动居中词每 16 分音符在词表间 flip；可选 flicker 解析并 lock 成最终短语。
- **适用场景** — **快而 sustained 的 fill roll**（每分钟数百 hit，约 16 分音符），无单一可读信息——用快速循环的词 flipbook 填 roll。
- **最佳时长** — **1.2–3.8s**，一次 roll 进一次 resolve。两个 roll，或 roll 间有 drop，即两组。
- **Params** — `bgColor`, `textColor`, `accentColor`, `flipWords`, `resolveText`, `periodChar`

### split-anchor-word-slot

- **是什么** — 左侧 held anchor 列为固定词行，右侧撕纸 word-slot 盒，由 beat 同步算子驱动：anchor lock-in、slot 词组 cycle（in/out + 每行颜色）、全场景背景 flip、每 beat jitter、box-zoom exit wipe。行数与 flip 次数为数据。
- **适用场景** — 短段：**held 概念**（品牌 / 名称 anchor 在左）**且** onset 流在右侧弹出独立词，另有 dense run 可 ride shake、强 downbeat wipe 出。
- **最佳时长** — **3–6s**；超过约 6.5s 固定 anchor 会 stale，除非右侧 slot 进入新 group/program。
- **Params** — `bgColor`, `anchors`, `theme`, `showText`, `program`

### typewriter-phrase-keyword-shuffle

- **是什么** — 词按每个 onset 打字拼成短语，随后一个 keyword 在 beat 上循环 typeface，其余完全静止。
- **适用场景** — 稳定 grid、**连续 onset 流**（非 desert）：先打出短语，再 shuffle keyword。与 `held-message-living-field`（要 onset desert）相反。
- **最佳时长** — **2.5–5s**；若短语无法在约 5s 内打完并 shuffle，减词或把句子拆到多组。
- **Params** — `bgColor`, `textColor`, `accentColor`, `lead1`, `lead2`, `lead3`, `keyword`, `periodChar`
