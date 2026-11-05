# Ink Theater — 手绘「动态艺术」（创意技能）

> 风格 id：`ink-sketch` · 引擎：`ink-theater/ink-theater.js` · 运行时：HyperFrames（atelier）
> 技法致谢：受 Ian 的 `小黑/Xiaohei` MIT 技能启发。通用、英文、动效优先。

**它是什么：** 一个极简的**黑墨白底**世界，一只面无表情的吉祥物通过操作荒诞的**低科技装置**，*身体力行*地演绎一个抽象概念。不是固定场景目录——而是通用方法 + 参数化引擎。在 atelier 模式下运行于 `animation` 管线；它**不是**独立管线。

## 通用方法（概念 → 动态场景）

研究与 Xiaohei 构图规则的「解锁点」是一个三步隐喻生成器——在 agent 里做，不要写进代码：

1. **抽象概念 → 一个物理动作** — 卡住、泄漏、复利、分拣、发酵、推、沉、散开（unraveling）。
2. **系统 → 一个低科技物体** — 压榨机、漏斗、井、罐、传送带、梯子、桥、柜子、巨石、门、秤。
3. **吉祥物在物体上执行该动作** — 它摇柄 / 推 / 泵 / 盖章 / 捞出。*若删掉吉祥物隐喻仍成立，那就是装饰——重做。*

然后在一张连续白页上按节拍编排，配合镜头（平移 / 推进）。

## 提炼的原型（选一个，发明新鲜细节）

| 原型 | 吉祥物动作 | 动效配方 |
|---|---|---|
| **Contraption（装置）** | 操作机器（曲柄/杠杆/泵） | 喂入 → 摇柄 → 机器运转（蒸汽/仪表）→ 产出弹出 |
| **Before/after load-shift（前后负载转移）** | 被混乱压垮 → 放松，一个关键动作 | 左侧混乱 → 橙色扫过 → 右侧结构组装 |
| **Journey / pitfalls（旅程/陷阱）** | 沿路径走；掉入坑或撞上节点 | 路径画出 → 行走 → 坑吞没 / 节点弹出 → 蓝色返回环 |
| **One → many fan（一对多扇出）** | 分裂/切分单一来源 | 来源分裂 → 箭头画向 N 条分支 → 各分支动作 |
| **Push / momentum（推/动量）** | 把巨石推上山，又滚落 | 缓慢吃力上推（power1）→ 登顶 → 快速滚落（power2.in） |
| **Well / extract（井/提取）** | 把桶降入噪声，舀出宝石 | 桶下降 → 舀取 → 拉起唯一的好东西 |

## 色彩语法（严格）

- **black** = 结构与吉祥物 · **orange** = 仅用于流动 / 箭头 · **red** = 问题 / 警告 · **blue** = 良好终态。
- 纯白纸面，≥35% 留白，主体约占 40–60%。面无表情吉祥物（白点眼），绝不卖萌。

## 引擎速查（`InkTheater`）

- 线条：`inkPath(pts)`、`inkRibbon(pts,{width,taper})`（笔刷）。Boil：`boil(turbEl, tl, {duration})`。
- 动效：`ease.{settle,overshoot,bouncy,soft}`（seek 安全弹簧）— 弹出用 overshoot，落位用 settle，着地用 bounce。
- 角色：`mascot({x,y,scale})` → `.reachL/.reachR([x,y])`（FABRIK）。经 GSAP `onUpdate` 跟随移动目标。
- 机械：`parts.{crank,gauge,hopper,slot,lever,box}` — 组合使用。
- 完整 API + 确定性规则：`ink-theater/README.md`。

## 角色 — Ink Puppet + 真实动捕（切勿手调动作）

需要行走 / 跳舞等角色时，**不要**手写动作（正弦曲线、手摆关键帧）。用 puppet + **动捕动作库**：

- `InkPuppet.create(mount,{cx,ground,boil})` → `p.drawIn(tl,{start})`（自绘 reveal）→ `InkPuppet.choreograph(tl, p, [{clip:'walk'},{clip:'dance_spin'},{clip:'wave'}], {start})`。
- **阅读 `ink-theater/mocap/catalog.json`，为每个节拍选合适动作 — 要变化，且切勿循环同一 clip**（循环是让视频显得重复的原因）。现有 12 个（均来自 CMU）：walk、run、climb、march、shuffle、jump、kick、sit、wave、twist、dance_spin、dance_glide。
- **目录里没有的动作？** `node ink-theater/mocap/add-motion.mjs <name> <cmu-id|url|path> <category> "<desc>"` — 拉取、转换（自动映射 fair1 / CMU / Mixamo 骨骼）、重新打包并更新目录。免费 CMU 动捕（`una-dinosauria/cmu-mocap`）有数千条。然后把 `mocap/clips.js` 复制进项目。
- **Speech balloons（对白气泡）**（角色「说话」）：`InkTheater.balloon(tl, {into, overlay, at, dur, text, mouth:[x,y], center:[x,y], boil})` — 用 HTML 文本以便 webfont 生效。

## ⚠ 不可协商项

- **手写字体：嵌入完整字体，不要用 Google Fonts 子集 woff2**（`css2` API 子集缺 basic-latin → 各处静默回退衬线）。用内置 `ink-theater/assets/patrickhand.ttf`（`@font-face … format("truetype")`）写在 **HTML overlay `<div>`** 上用于字幕/对白气泡。不要 Google 热链（破坏确定性）。见 `ink-theater/README.md` → "font gotcha"。
- 确定性：闭式弹簧、时间轴外 seed-stepped boil、禁止 `repeat:-1`、仅 seeded PRNG。
- 在 `window.__timelines` 上挂一条 paused 的 `gsap.timeline`。渲染前用 `lint` + `snapshot`（读 contact-sheet）校验。
- **管线豁免**：这是 `animation` / `character-animation` 管线上的风格 + 引擎 — **不是** Rule-Zero 管线。别卡住去找 `.yaml` manifest。

## 参考构建

- `projects/ink-theater-reel/` — 能力集锦。 · `projects/ink-theater-momentum/` — 「Momentum」故事（手写体经 HTML div）。
