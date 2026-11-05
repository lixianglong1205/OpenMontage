---
name: motion-blur-streak
description: 在快速入场或镜头穿入时伪造方向性速度模糊——模糊在最大速度处达到峰值，并在落位时归零，使元素先拖影飞入再清晰定格。两条路径：沿运动轴的 SVG feGaussianBlur，或收拢到主元素的回声/残影拖尾。
metadata:
  tags: motion-blur, velocity, streak, entrance, fly-in, ghost, echo, svg-filter, kinetic, camera, snap
---

# 运动模糊拖影（Motion-Blur Streak）

面向可 seek 的渲染器，真实逐帧运动模糊不可用（它依赖快门时间积分，而暂停的时间轴没有这一概念），因此本规则在**快速元素飞入**或**猛烈镜头穿入**时**伪造**该效果。模糊在**最大速度处达到峰值，并在落位时归零**——元素先读成拖影飞入，到达时再清晰「咔」一下定住。关键在于**耦合**：模糊包络与位移动画共用同一缓动与时间窗，峰值模糊与峰值速度对齐，元素一停立刻锐利。

两种实现路径，均有限、确定、且 seek 安全：

- **(A) 方向性 SVG 模糊** — 内联 `<filter>` 配合 `<feGaussianBlur stdDeviation="X 0">`（运动轴为 X，垂直轴为 0）。GSAP 通过代理对象每帧 `setAttribute` 将 `X` 从高 tween 到 0。最干净，单元素，真实方向性涂抹。
- **(B) 回声 / 残影拖尾** — 2–4 个副本，透明度递减，沿运动矢量向后偏移，随落位收拢到主元素。无滤镜开销；读成「速度线」式拖影。更适合需要**有色**或**风格化**拖尾，而非字面光学模糊。

仅用于**入场与中镜头位移**——快速到达、镜头掠过的一拍、卡片 slam 进网格槽、Logo 穿入并 lockup。**绝不在非最终帧上做带模糊的出场**（模糊元素在构图中途飞出画面会像 glitch；场景间硬切是转场的职责，不是单元素模糊）。

## 工作原理

快速移动有速度曲线：起步加速、峰值、再减速落位。`out` 缓动（`expo.out`、`power4.out`）把速度**前置**——开头最快，末尾趋近零。伪造方式是把**模糊（或回声）包络**映射到同一条曲线：

1. **位移动画** — 元素从画外 / 推远起点到静止变换（飞入用 `x`/`y`，穿入用 `scale`），在 `MOVE_DUR` 内用快速 `out` 缓动。
2. **模糊包络** — 在**相同时间窗与缓动**下同步，拖影从 `PEAK_BLUR` → `0`。缓动前置速度且包络共享，最大模糊与最大速度重合，落位时模糊恰为 `0`。
3. **落位即清晰** — 到 `MOVE_START + MOVE_DUR` 时元素处于静止变换，模糊为 `0`（路径 A）或所有回声叠到主元素（路径 B）。随后在高潮停留段保持完全清晰。

路径 A 通过**代理对象** tween 滤镜的 `stdDeviation`（非 DOM 风格数值属性）——GSAP 不能直接 tween SVG 属性，故 tween 普通 `{ v: PEAK_BLUR }`，在 `onUpdate` 里 `setAttribute` 写回。路径 B 将残影放在确定性向后偏移（`i * ECHO_STEP_PX`），在同一包络上淡出/收拢。

## HTML

### 路径 A — 方向性 SVG 模糊（推荐默认）

```html
<div
  class="scene"
  id="streak-scene"
  data-composition-id="streak-scene"
  data-start="0"
  data-duration="DURATION"
  data-track-index="0"
>
  <!-- Inline filter: blur on the X axis only (stdDeviation="X 0"); 0 on Y keeps it a clean horizontal smear. -->
  <svg width="0" height="0" aria-hidden="true" style="position: absolute">
    <defs>
      <filter id="streak" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur id="streak-blur" in="SourceGraphic" stdDeviation="0 0" />
      </filter>
    </defs>
  </svg>

  <div class="streak-stage">
    <div class="streak-el" id="streak-el">{phrase}</div>
  </div>
</div>
```

### 路径 B — 回声 / 残影拖尾

```html
<div
  class="scene"
  id="streak-scene"
  data-composition-id="streak-scene"
  data-start="0"
  data-duration="DURATION"
  data-track-index="0"
>
  <div class="streak-stage">
    <!-- N-1 ghosts BEHIND the lead, then the lead on top. Ghosts are aria-hidden duplicates. -->
    <div class="streak-ghost" data-i="3" aria-hidden="true">{phrase}</div>
    <div class="streak-ghost" data-i="2" aria-hidden="true">{phrase}</div>
    <div class="streak-ghost" data-i="1" aria-hidden="true">{phrase}</div>
    <div class="streak-el" id="streak-el">{phrase}</div>
  </div>
</div>
```

## CSS

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: {sceneBg};
  font-family: {font};
  overflow: hidden; /* the smear/echo extends past the resting position before settling */
}
.streak-stage {
  position: relative;
  display: grid;
  place-items: center;
}
.streak-el {
  position: relative;
  z-index: 2;
  font-size: EL_FONT_SIZE;
  font-weight: 900;
  letter-spacing: EL_TRACKING;
  color: {textColor};
  /* Path A only — reference the directional filter. (Omit for Path B.) */
  filter: url(#streak);
  will-change: transform, filter;
}

/* Path B ghosts — identical glyphs behind the lead, decreasing opacity */
.streak-ghost {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  z-index: 1;
  font-size: EL_FONT_SIZE;
  font-weight: 900;
  letter-spacing: EL_TRACKING;
  color: {textColor};
  opacity: 0;
  will-change: transform, opacity;
  pointer-events: none;
}
```

## GSAP Timeline

### 路径 A — 方向性 SVG 模糊

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // GSAP can't tween an SVG attribute directly — tween a proxy and write it back each frame.
  const blurNode = document.getElementById("streak-blur");
  const blurProxy = { v: PEAK_BLUR };
  const writeBlur = () => blurNode.setAttribute("stdDeviation", `${blurProxy.v} 0`); // X-axis only
  writeBlur(); // seed frame 0 so a seek to t=0 shows the streaked start, not a sharp pre-frame

  // Position: travel from off-frame to rest on a fast `out` ease (velocity front-loaded).
  tl.fromTo(
    "#streak-el",
    { x: ENTER_FROM_X, opacity: 0 },
    { x: 0, opacity: 1, duration: MOVE_DUR, ease: MOVE_EASE },
    MOVE_START,
  );

  // Blur envelope: SAME window + SAME ease so peak-blur == peak-speed, resolving to 0 at the settle.
  tl.to(blurProxy, { v: 0, duration: MOVE_DUR, ease: MOVE_EASE, onUpdate: writeBlur }, MOVE_START);

  window.__timelines["streak-scene"] = tl;
</script>
```

### 路径 B — 回声 / 残影拖尾

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Lead element: same fast `out` move as Path A.
  tl.fromTo(
    "#streak-el",
    { x: ENTER_FROM_X, opacity: 0 },
    { x: 0, opacity: 1, duration: MOVE_DUR, ease: MOVE_EASE },
    MOVE_START,
  );

  // Ghosts: each starts FURTHER back along the motion vector (deterministic, by index),
  // dimmer, and collapses onto the lead — all on the SAME ease/window so they vanish at the settle.
  const ghosts = gsap.utils.toArray(".streak-ghost");
  ghosts.forEach((g) => {
    const i = Number(g.dataset.i); // 1..N-1, set in HTML (no Math.random)
    tl.fromTo(
      g,
      { x: ENTER_FROM_X - i * ECHO_STEP_PX, opacity: GHOST_BASE_OPACITY / i },
      { x: 0, opacity: 0, duration: MOVE_DUR, ease: MOVE_EASE },
      MOVE_START,
    );
  });

  window.__timelines["streak-scene"] = tl;
</script>
```

## 变体

### 垂直拖影（上升 / 下落入场）

交换运动轴：位移动画用 `y` 代替 `x`，路径 A 用 `stdDeviation="0 Y"`（Y 轴模糊、X 为 0），路径 B 用 `ENTER_FROM_Y` 与垂直回声偏移。短语**向上**拖影落位可与 `kinetic-type-beats` 的 rise-rotate 拍配合。

### 镜头穿入（缩放拖影进入 lockup）

不位移而冲向镜头：在快速 `out` 缓动下 `scale: SCALE_FROM → 1`，用对称 `stdDeviation="B B"` 包络近似**径向 / 变焦模糊**（深度向涂抹，非方向性）。即 `logo-assemble-lockup` 穿入——字标从柔焦冲出，在 lock 处清晰定格。

```js
tl.fromTo(
  "#streak-el",
  { scale: SCALE_FROM, opacity: 0 },
  { scale: 1, opacity: 1, duration: MOVE_DUR, ease: MOVE_EASE },
  MOVE_START,
);
tl.to(
  blurProxy,
  {
    v: 0,
    duration: MOVE_DUR,
    ease: MOVE_EASE,
    onUpdate: () => blurNode.setAttribute("stdDeviation", `${blurProxy.v} ${blurProxy.v}`),
  },
  MOVE_START,
);
```

### 交错网格拖影入场（卡片组装）

用于 `grid-card-assemble`：每张卡片从各自向后偏移拖影进槽，交错延迟。同一缓动/时间窗驱动所有卡片，按索引延迟；从卡片索引推导入场偏移与开始时间（不用 `Math.random`）。每张卡片进槽瞬间即清晰。

```js
gsap.utils.toArray(".grid-card").forEach((card, i) => {
  const at = MOVE_START + i * CARD_STAGGER;
  tl.fromTo(
    card,
    { x: ENTER_FROM_X, opacity: 0 },
    { x: 0, opacity: 1, duration: MOVE_DUR, ease: MOVE_EASE },
    at,
  );
  // + a per-card blur proxy tween at the same `at` (Path A), or per-card ghosts (Path B)
});
```

### 保持拖影（单拍鞭击强调）

单个 kinetic 短语「掠过」时，可让拖影多留一两帧：模糊用略**慢于**位移的缓动（如位移 `expo.out`、模糊 `power3.out`）——元素先到位，最后一缕涂抹再消散。慎用；默认是锁定的包络。

## 如何选取数值

### 运动

- **MOVE_EASE** — 位移与模糊/回声共用缓动。
  - 范围：`expo.out`（最硬 snap）、`power4.out`（硬 slam，默认）、`power3.out`（硬但稍软）
  - 效果：更硬的 `out` → 速度更前置 → 拖影更锐、在窗口后半段才消散
  - 约束：必须是 `out` 系缓动（速度前置）。`inOut` 或 `in` 会把峰值速度放在中/后段，模糊-速度耦合失效。**位移与模糊必须用同一缓动**（「保持拖影」变体除外）。
- **MOVE_DUR** — 位移 + 模糊消散时长。
  - 范围：0.25–0.6 s
  - 效果：更短 → 更猛的鞭击；更长 → 滑行感，拖影失去冲击力
  - 约束：拖影要**快**——超过约 0.7 s 不再像速度模糊，而像对焦拉动
- **MOVE_START** — 入场在时间轴上的位置。
  - 约束：在 `MOVE_START + MOVE_DUR` 之后、合成结束前留 **≥1 s 停留**（高潮停留——若拖影在 `t = DURATION − 0.2 s` 才落地，会读成「闪一下就没」）
- **ENTER_FROM_X / ENTER_FROM_Y** — 沿运动轴的画外起点偏移。
  - 范围：该轴上元素自身尺寸的 40–120%（足够远以读成「从画外来」）
  - 效果：更大 → 行程更长 → 拖影有更多跑道；太小则没有速度感

### 路径 A — SVG 模糊

- **PEAK_BLUR** — 最大速度处（窗口起点）的 `stdDeviation`。
  - 范围：8（轻微）→ 18（默认）→ 30（极端鞭击）
  - 效果：更高 → 峰值速度处涂抹更重；过高会在起始帧完全抹掉字形
  - 约束：≤ ~30 — 再大会在前几帧不可读，像「消失再出现」；滤镜区域（`<filter>` 的 `x/y/width/height`）须足够大（≥`-50% … 200%`），否则涂抹被盒边裁切
- **SCALE_FROM**（穿入变体） — 镜头推近的起点 scale。
  - 范围：1.3（轻推）→ 2.5（猛穿）

### 路径 B — 回声拖尾

- **N（残影数量）** — 主元素后的残影数（由编写的 `.streak-ghost` 数量决定）。
  - 范围：2–4
  - 效果：更多 → 更长、更顺的涂抹；>4 像 stutter / 频闪而非拖影
- **ECHO_STEP_PX** — 沿运动矢量每个残影的向后偏移。
  - 范围：12–40 px
  - 效果：更大 → 拖尾更散、更明显；更小 → 紧密似模糊簇
  - 约束：`(N) × ECHO_STEP_PX` 应 ≲ `ENTER_FROM_X`，最远残影仍在行程跑道内
- **GHOST_BASE_OPACITY** — 最近残影（`i = 1`）的不透明度；按 `BASE / i` 递减。
  - 范围：0.3（淡）→ 0.6（明显）
  - 约束：≤ ~0.6 — 过不透明像重复元素，不像拖尾

### 版式与字体

- **EL_FONT_SIZE / EL_TRACKING** — 拖影元素的字重（短语时）。
  - 约束：粗 display（1080p 下 ≥120 px、字重 ≥800），涂抹才有质量；细字拖成看不见
- **CARD_STAGGER**（网格变体） — 相邻卡片间隔。
  - 范围：0.05–0.12 s — 够紧以读成一波组装，而非逐个到达

### 令牌

- **{sceneBg}** — 背景；纯色 / 低细节底拖影最清晰（杂乱背景与涂抹打架）
- **{font}** — 字体栈（拖影为文字时用内嵌 display 面，见 typography 参考）
- **{textColor}** — 元素色；路径 B 残影继承，可单独给 `.streak-ghost` 上色做略 desaturated 拖尾
- **{phrase}** — 飞入的词 / 字形 / 字标

## 核心原则

- **模糊在峰值速度处最大，落位归零** — 即本规则全部。位移 tween 与模糊/回声包络共享缓动与时间窗并锁定。模糊在元素停后仍 linger，或在已慢时才峰值，会读成对焦拉动而非速度。
- **始终 `out` 系缓动** — 速度须前置（起步快、减速入位）。`expo.out` / `power4.out` / `power3.out`。`in` 或 `inOut` 会把峰值速度放错位置，耦合崩坏。
- **沿运动轴方向模糊**（路径 A）— 水平 `"X 0"`，垂直 `"0 Y"`，仅深度/scale 推近用 `"B B"`。横向移动用对称模糊像散焦，不像速度。
- **代理 tween、写回属性**（路径 A）— GSAP tween 普通 `{ v }`；`onUpdate` 调用 `setAttribute("stdDeviation", …)`。不能直接 tween SVG 属性，且**须在 setup 时 seed 一次**，seek 到 `t=0` 才显示拖影起点。
- **残影按索引确定性**（路径 B）— 偏移 `i * ECHO_STEP_PX`，不透明度 `BASE / i`。拖尾不用 `Math.random`；索引驱动各残影差异，每次 seek 一致。
- **仅入场，非合成中途出场** — 拖影是**到达**。非最终帧模糊离开像 glitch；场景间出场是转场职责（见 `../../transitions/overview.md`）。
- **挣得清晰停留** — snap 之后清晰元素须停留 ≥1 s。猛烈拖影与静止锐利落位的对比**就是**效果。
- **重元素、纯色底** — 细字或 busy 底都会吞涂抹。大粗质量在干净画面上才读得出来。

## 关键约束

- **时间轴必须 paused**：`gsap.timeline({ paused: true })`。禁止 `tl.play()`。
- **注册键 = 根节点 `data-composition-id`**。
- **拖影元素（及残影）禁止 CSS `transition`** — 会与 HF seek 独立插值并闪烁。仅 GSAP 驱动位移与模糊。
- **禁止 `repeat` / `yoyo` / infinite** — 拖影是单次有限到达。仅有限 tween。
- **禁止 `Math.random` / `Date.now`** — 残影偏移/不透明度及任意 stagger 由元素索引推导；每次 seek 确定。
- **仅 GSAP 变换别名**：`x`、`y`、`scale`、`rotation`。禁止 tween `width` / `height` / `left` / `top`。tween `filter`（代理 → `stdDeviation`）与 `opacity` 对 seek 安全且可用。
- **setup 时 seed SVG `stdDeviation`**（路径 A）— 播放前写一次，seek 首帧才渲染拖影起点，而非瞬间清晰的 pre-frame。
- **滤镜区域须宽裕**（路径 A）— `<filter x="-50%" y="-50%" width="200%" height="200%">`，避免涂抹被元素盒边裁切。
- **场景上 `overflow: hidden`** — 移动中涂抹 / 最远残影会超出落位；裁切以免溢出画框。

## 组合

- [kinetic-beat-slam.md](kinetic-beat-slam.md) — 在 beat 序列中为某一短语用本拖影作入场（scale-slam beat **即** motion-blur 飞入）；从共享 `BEATS[]` 读取 onset
- [center-outward-expansion.md](center-outward-expansion.md) — 网格拖影入场是中心扩张，每个元素行程带速度模糊包络
- [3d-text-depth-layers.md](3d-text-depth-layers.md) — 飞入短语的挤出深度（深度层跟随主元素变换）
- [scale-swap-transition.md](scale-swap-transition.md) — 同 footprint 状态互换的替代（本规则用于从画外/深度**快速到达**，非 morph）

## 搭配的 HF 技能

- `/hyperframes-animation` — `out` 系缓动、代理驱动 `onUpdate` 属性 tween、锁定包络协调（`../../adapters/gsap-easing-and-stagger.md`）
- `/hyperframes-creative` — `references/typography.md`（文字拖影的内嵌 display 面）、`references/video-composition.md`（涂抹后的纯色场）
- `/hyperframes-core` — 合成接线、确定性（有限 tween、无 `Math.random`）
- `/hyperframes-cli` — `hyperframes lint` / `hyperframes validate`（校验缺失 `#streak-blur` 节点或未引用滤镜）
