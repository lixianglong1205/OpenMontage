# Ink Theater

一个确定性的、可 seek 的手绘 **「动态艺术」** 引擎——极简黑白墨水世界，一只面无表情的吉祥物通过操作荒诞的低科技装置，在物理上 *演绎* 抽象概念。为 OpenMontage 的 **atelier** 路径构建，并通过 **HyperFrames**（HTML/SVG/CSS + 一条暂停的 GSAP 时间线 → MP4）渲染。

灵感来自 Ian 的 `小黑 / Xiaohei` 插画技能（MIT — 该技术致谢 Ian）；这是原创、通用、英文、以动作为主的引擎，而非复制品。

## 为何存在

插画风格足够简单，**插画即动画**——无需扩散模型。矢量形状 + 数学即可得到全部效果：免费、确定性、无限可编辑，且角色会真正「演」出概念。本引擎将研究成果（`memory: project_ink_atelier_animation`，关于矢量/物理/隐喻基础的深度研究）落实为可复用原语。

## 五大能力（`ink-theater.js`，全局 `InkTheater`）

| 模块 | 作用 | 关键 API |
|---|---|---|
| **ink strokes** | 自信的手绘线条——可变宽度笔刷带 + 抖动中心线 | `inkPath(pts, opt)`, `inkRibbon(pts, {width,taper,seed})` |
| **boil** | 可 seek 的手绘线条「 boil 」——在时间线上步进 `feTurbulence` 种子（约 9fps），**不是** SMIL | `boil(turbEl, tl, {duration,fps})` |
| **spring physics** | 闭式阻尼弹簧缓动（ anticipation / overshoot / settle）——进度的纯函数，可 seek | `springEase({stiffness,damping,mass})`, `ease.{settle,overshoot,bouncy,soft}` |
| **rig / IK** | 2D FABRIK 逆运动学 + 可装配吉祥物，双臂够向目标 | `fabrik(lengths,origin,target)`, `mascot({x,y,scale})` → `.reachL/.reachR([x,y])` |
| **contraption grammar** | 参数化可组合机械部件 | `parts.{crank,gauge,hopper,slot,lever,box}` |

## 确定性（HyperFrames 渲染契约）

每一帧必须仅由时间可复现。本引擎遵守：

- **闭式弹簧** — `springEase` 计算解析阻尼振荡器阶跃响应，任意进度 `p` 确定性映射（无数值积分、无累积状态）。
- **可 seek 的 boil** — 由时间线上的 GSAP 步进种子 tween 驱动，永不使用 SMIL / 渲染时刻钟。
- **经 `onUpdate` 的 IK 跟随** — 从由时间线设置位置的目标摆臂；GSAP 在 seek 时触发 `onUpdate`，故为时间的纯函数。
- 带种子的 PRNG（`rng`）用于所有「看似随机」的抖动 — 无运行时 `Math.random`。
- 无 `repeat:-1`（仅有限次数），仅动画 transform/opacity/attrs。

## ⚠ 字体陷阱（真正的根因）

自定义手写体在很长一段时间内每次渲染都显示为 **serif**。原因**不是** SVG 与 HTML 之争——而是 **字体子集陷阱**：从 Google Fonts `css2` API 只抓一个 woff2（`grep … | head -1`）会得到单个 *unicode-range 子集*（常为 cyrillic / vietnamese / latin-ext），**缺少 basic-latin（ASCII）**。于是每个英文词静默回退到 serif——而渲染器仍记录 `Fonts: 1 loaded`。（这意味着早期字幕「看起来像手写」的 demo 实际是 serif。）

**修复（已验证）：** 嵌入 **完整字体文件** — TrueType，或真正覆盖 basic-latin 的 woff2：

```html
@font-face { font-family: "InkHand"; src: url("assets/patrickhand.ttf") format("truetype"); font-display: block; }
```

可用的 Patrick Hand TTF 位于 **`ink-theater/assets/patrickhand.ttf`**（SIL Open Font License — 许可证同目录 `assets/OFL.txt`；见 `THIRD_PARTY_NOTICES.md`）——复制到你项目的 `assets/` 并使用 `font-family: "InkHand"`。在普通 **HTML  overlay `<div>`** 上可渲染真实手写（已验证——在 SVG 场景上放字幕 div）。不要热链 Google Fonts（渲染时网络拉取破坏确定性）；本地 `@font-face` 文件会在构建时被编译器自动内联。

> 注意：HyperFrames 还预打包约 18 种字体（无手写体）——见 `hyperframes-creative/references/typography.md`。手写体必须按上文嵌入完整字体。

## 在 HyperFrames 项目中的用法

1. 将 `ink-theater.js` 复制到项目根；在 gsap 之后 `<script src="ink-theater.js">`。
2. 程序化构建场景到挂载 `<g>`，保留节点引用。
3. 对 ink 组应用 `filter="url(#boil)"`；调用一次 `InkTheater.boil(...)`。
4. 字幕 = HTML overlay div（见字体陷阱）。
5. 在 `window.__timelines["<id>"]` 上注册一条 `gsap.timeline({paused:true})`。

## Ink Puppet — 手绘角色上的真实动捕（角色动画推荐）

让涂鸦 *角色* 动起来（走 / 舞 / 挥 / 跳）的正确方式**不是**手调数学——而是 **真实动作捕捉重定向到 stick figure**。Agent 只需选角色并编排命名动作；绝不应手调运动。两部分：

- **`mocap/bvh2clip.mjs`** — 离线转换：3D BVH 动捕文件 → 紧凑 2D「clip」（每帧关节轨，相对髋部姿态 + 根运动，缩放到固定身高）。每个动作运行一次；与 `clips.js` 打包。
- **`ink-puppet.js`** — 运行时：构建 stick figure、播放 clip，暴露 **声明式编排 API**：

```js
var p = InkPuppet.create(mount, { cx: 960, ground: 902, boil: "boil" });
p.drawIn(tl, { start: 0.4 });                         // pencil sketches the figure limb-by-limb
InkPuppet.choreograph(tl, p, [                          // then plays named mocap clips — zero hand-tuning
  { clip: "walk" }, { clip: "dance_spin" }, { clip: "kick" }, { clip: "wave" }
], { start: 3.7 });

// speak — comic balloon tethered to the mouth (HTML text = webfont works)
InkTheater.balloon(tl, { into: fxGroup, overlay: htmlOverlay, at: 5, dur: 2, text: "hello!", boil: "boil" });
```

确定性 + 可 seek（姿态为各段局部时间的纯函数）。

**动作库（`mocap/catalog.json`）** 内置 12 种多样动作，Agent 按名选取—— locomotion（`walk`, `run`, `climb`, `march`, `shuffle`）、action（`jump`, `kick`）、posture（`sit`）、gesture（`wave`）、dance（`dance_spin`, `dance_glide`, `twist`）。每个 clip 来自 CMU（任意用途免费）。**阅读 catalog 并选符合剧情的动作——不要循环单一 clip。**

**一条命令扩展**（自扩展，无需改代码）——转换器自动映射 fair1 / CMU / Mixamo 骨骼：
```
node mocap/add-motion.mjs backflip 05_20 dance "a backflip"   # CMU id, or a URL, or a local .bvh
```
免费 **CMU mocap**（`una-dinosauria/cmu-mocap`）有数千条。这与 Meta 的 *Animated Drawings* 类似，但此处保持 **矢量、白墨、带绘制显现**（AD 为栅格、仅人形、无显现）。来源（所有 clip 为 CMU，任意用途免费）：`mocap/NOTE.md` · `THIRD_PARTY_NOTICES.md`。

### Speech balloons — `InkTheater.balloon(tl, opts)`
从嘴部生长的漫画气球，HTML overlay 文字（以便 webfont 生效）。`opts`：`into`（SVG `<g>`）、`overlay`（HTML div）、`at`、`dur`、`text`、`mouth:[x,y]`、`center:[x,y]`、`w`、`size`、`boil`。

## 示例

- `examples/mocap-figure/` — 铅笔角色逐 limb 自绘，随后通过 **真实 CMU 动捕** 走 / 跑 / 舞 / 踢 / 坐 / 挥。自包含且可 lint（`npx hyperframes lint ink-theater/examples/mocap-figure`）；见 `examples/README.md`。
