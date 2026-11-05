---
name: depth-of-field-blur
description: 选择性对焦 / 移焦（rack focus）——通过对失焦层用 GSAP 补间 filter 模糊（并略微降低 opacity），让焦内元素保持清晰，从而把视线引到焦点上。通过 `--dof` CSS 变量驱动模糊；有限补间、不用 CSS transition、结果可 deterministic 复现。涵盖单次焦内拉焦、两景深平面之间的移焦，以及推进时模糊周围集群。
metadata:
  tags: blur, focus, depth-of-field, dof, rack-focus, filter, dim, spotlight, cinematic, push-in
---

# 景深模糊（选择性对焦 / 移焦）

通过对周围元素**模糊**（并略微**压暗**），让焦内层保持清晰，从而把视线引到单一焦点上——如同相机景深在背景上衰减，或移焦（rack focus）改变哪一层处于对焦平面。动效是 `filter: blur(Npx)` 加上小幅 `opacity` 压暗，在焦移窗口内从清晰(0) 补间到模糊——二者均可 seek 安全，因为 `filter` 与 `opacity` 是纯绘制属性，HF 能逐帧正确插值。

这是蓝图里反复出现的焦外衰减节拍的支撑规则：推进时外围节点模糊（`constellation-hub`）、视差卡片栈上的移焦（`cursor-ui-demo`）、非高亮卡片压暗 + 模糊以聚光英雄指标（`dataviz-countup`）。这些场景都曾标注「景深一半没有支撑规则」——本规则即为其补全。

## 工作原理

每一层都带有 `--dof` 自定义属性（模糊像素值），由 `filter: blur(var(--dof))` 读取，并各自拥有 `opacity`。单个 GSAP 补间在焦移窗口内，将各层的 `--dof` 从 `0` 补到目标模糊值，并将 `opacity` 从 `1` 补到压暗级别。焦内层的补间目标是 `--dof: 0`（保持清晰）；失焦层则为正模糊值。

三种机制，同一原语：

1. **焦内拉焦** — 一个窗口：失焦层从清晰(0) → 模糊，焦内层保持在 0。视线被引到唯一仍清晰的对象。
2. **移焦** — 同一属性上两个相邻窗口：焦点离开平面 A（其模糊 0 → max）的同时，平面 B 的模糊 max → 0。状态连续性与 `press-release-spring` 中完全一致：移焦后 A 的静止模糊必须等于移焦前 B 所持有的值，因此将二者写成同一 `--dof` 上的相邻补间，交接才无缝。
3. **推进时模糊集群** — 景深补间与相机推进（`multi-phase-camera` / `coordinate-target-zoom`）并发：周围集群在与相机向焦心缩放**相同的时间线位置**上模糊 + 压暗，使「世界后退」与「我们推进」读成一次动作。

因为模糊是补间目标（而非 CSS `transition`），渲染器可在任意帧落位——且每层目标由其 index / data 属性推导（绝不用 `Math.random`），每次 seek 的衰减完全一致。

## HTML

```html
<div
  class="scene"
  id="dof-scene"
  data-composition-id="dof-scene"
  data-start="0"
  data-duration="DURATION"
  data-track-index="0"
>
  <div class="world" id="world">
    <!-- Focal layer — stays sharp -->
    <div class="layer focal" id="focal" data-dof="0">{FocalLabel}</div>

    <!-- Off-focus layers — blur + dim. data-depth orders them near→far
         so the falloff can scale blur by depth (see Variations). -->
    <div class="layer ctx" data-depth="1">{Context A}</div>
    <div class="layer ctx" data-depth="2">{Context B}</div>
    <div class="layer ctx" data-depth="3">{Context C}</div>
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
  background: {bgGradient};
}
.world {
  /* Single wrapper so a concurrent camera push-in (multi-phase-camera)
     transforms everything together; DoF is independent of the camera. */
  position: relative;
  width: 100%;
  height: 100%;
  transform-origin: 50% 50%;
}
.layer {
  /* --dof is the px of blur; filter reads it. Starts sharp. */
  --dof: 0px;
  filter: blur(var(--dof));
  /* will-change: filter — promotes the layer so the blur is cheap to
     re-rasterize each frame. See the perf note in Key Principles. */
  will-change: filter;
  font-family: {font};
  font-weight: 900;
  color: {textColor};
}
.focal {
  /* Sits above the context layers and never blurs. */
  z-index: 2;
  font-size: FOCAL_FONT_SIZE;
}
.ctx {
  /* The off-focus plane(s). Smaller / grouped so the blur radius can
     stay modest yet still read — blurring a small layer is cheap. */
  z-index: 1;
  font-size: CTX_FONT_SIZE;
  opacity: 1;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const ctx = gsap.utils.toArray(".ctx");

  // ── Mechanic 1: FOCAL PULL ─────────────────────────────────────────
  // Off-focus layers blur + dim from sharp to defocused over the
  // focus-shift window. Blur scales with data-depth so far planes blur
  // more than near ones (deterministic — derived from the attribute,
  // never Math.random).
  ctx.forEach((el) => {
    const depth = Number(el.dataset.depth) || 1;
    const targetBlur = BLUR_PER_DEPTH * depth; // px
    tl.to(
      el,
      {
        "--dof": `${targetBlur}px`,
        opacity: DIM_LEVEL, // e.g. 0.55 — dim, not gone
        duration: FOCUS_DUR,
        ease: "power2.inOut",
      },
      FOCUS_START,
    );
  });
  // Focal layer is already sharp (--dof:0, opacity:1) and untouched.

  window.__timelines["dof-scene"] = tl;
</script>
```

## 变体

### 两景深平面之间的移焦（前景 ⇄ 背景）

每个平面上 `--dof` 的两个相邻补间——焦点离开平面 A 的同时落在平面 B。状态连续：移焦前 B 的*静止*模糊等于移焦后 A 所持有的值，交接无跳变。

```js
// Start: A sharp, B pre-blurred (set BEFORE the rack so there's no pop).
gsap.set("#planeA", { "--dof": "0px", opacity: 1 });
gsap.set("#planeB", { "--dof": `${MAX_BLUR}px`, opacity: DIM_LEVEL });

// Rack: A defocuses while B comes into focus, same position + duration.
tl.to(
  "#planeA",
  { "--dof": `${MAX_BLUR}px`, opacity: DIM_LEVEL, duration: RACK_DUR, ease: "power2.inOut" },
  RACK_START,
);
tl.to(
  "#planeB",
  { "--dof": "0px", opacity: 1, duration: RACK_DUR, ease: "power2.inOut" },
  RACK_START,
);
```

### 推进时模糊集群（景深 + 相机，同一节拍）

在**相同时间线位置**运行焦内拉焦补间与相机推进，使周围集群在相机向焦心缩放的同时退入模糊。相机变换 `.world`；景深补间各层——属性独立，互不冲突。

```js
// Camera push-in toward the focal core (see multi-phase-camera / coordinate-target-zoom).
tl.to(
  "#world",
  { scale: PUSH_SCALE, x: PUSH_X, y: PUSH_Y, duration: FOCUS_DUR, ease: "power2.inOut" },
  FOCUS_START,
);
// Cluster blurs + dims on the SAME position — "the world recedes as we push in."
ctx.forEach((el) => {
  const depth = Number(el.dataset.depth) || 1;
  tl.to(
    el,
    {
      "--dof": `${BLUR_PER_DEPTH * depth}px`,
      opacity: DIM_LEVEL,
      duration: FOCUS_DUR,
      ease: "power2.inOut",
    },
    FOCUS_START,
  );
});
```

### 在卡片网格中聚光英雄指标（其余压暗 + 模糊）

`dataviz-countup` 节拍：网格中部分卡片保持清晰（英雄指标），其余在同一窗口内压暗 + 模糊。标记 hero，跳过；其余失焦。

```js
gsap.utils.toArray(".card:not(.hero)").forEach((el) => {
  tl.to(
    el,
    { "--dof": `${GRID_BLUR}px`, opacity: DIM_LEVEL, duration: FOCUS_DUR, ease: "power2.out" },
    FOCUS_START,
  );
});
```

### 重新对焦 / 收束（场景结束前释放模糊）

若节拍回到「全部可见」（或交给需要干净出帧的 crossfade），在尾部将模糊 ramp 回 0，使场景以清晰收束而非半失焦结束。

```js
ctx.forEach((el) =>
  tl.to(
    el,
    { "--dof": "0px", opacity: 1, duration: REFOCUS_DUR, ease: "power2.inOut" },
    REFOCUS_START,
  ),
);
```

### 焦内层有界对焦呼吸（可选）

为 subtle 的「移焦落定」感，可在 hold 期间让焦内层模糊在 0 附近轻微呼吸——用*有限* `ease:"none"` 驱动器将 `sin()` 写入 `--dof`（绝不用 `repeat:-1`，绝不用 CSS animation）。振幅远小于 1px，否则会读成「仍在对焦」。

```js
const drift = { p: 0 };
tl.to(
  drift,
  {
    p: Math.PI * 2 * BREATH_CYCLES,
    duration: BREATH_DUR,
    ease: "none",
    onUpdate: () => {
      const b = Math.max(0, Math.sin(drift.p)) * FOCAL_BREATH_PX; // ≤ ~0.6px
      document.getElementById("focal").style.setProperty("--dof", `${b}px`);
    },
  },
  BREATH_START,
);
```

## 如何选取数值

### 几何 / 布局

- **FOCAL_FONT_SIZE / CTX_FONT_SIZE** — 焦内与上下文字号。
  - 范围：焦内为视觉主导；上下文更小， modest 模糊半径仍能读成「失焦」。
  - 效果：较小的上下文层可用更小的 `BLUR_PER_DEPTH`（更省）仍显柔和。
- **z-index** — 焦内 `z-index: 2`，上下文 `z-index: 1`。
  - 约束：清晰焦内层必须在模糊层**之上**，否则锐利边缘会像渗进雾中。

### 模糊量

- **BLUR_PER_DEPTH** — 每个 depth 步（`data-depth`）增加的模糊 px。
  - 范围：每步 3–6 px（三平面栈顶约 9–18 px）
  - 效果：低 → 温和景深；高 → 强微缩/移轴感
  - 约束：**大层上单层模糊 ≤ ~24 px** — 成本随模糊半径与面积增长；全画幅元素上大半径是最贵情况（见核心原则）
- **MAX_BLUR** — 完全失焦平面的终端模糊（移焦 / 焦内拉焦峰值）。
  - 范围：8（柔）→ 16（默认）→ 24（重）px
  - 约束：大面上超过 ~24 px 时，优先缩小层或分组内容以缩小模糊 footprint
- **GRID_BLUR** — 压暗网格卡片上的模糊（聚光变体）。
  - 范围：6–12 px — 足够推后又不丢网格形状

### 压暗量

- **DIM_LEVEL** — 全失焦时失焦层的 opacity。
  - 范围：0.4（强推后）→ 0.55（默认）→ 0.7（ subtle）
  - 效果：更低 → 上下文硬退 / 近聚光；更高 → 仍可读，只是次要
  - 约束：很少低于 0.35 — 全黑失焦层读成「被移除」而非「失焦」

### 时间

- **FOCUS_START / FOCUS_DUR** — 焦内拉焦何时开始、移焦/拉焦持续多久。
  - 范围：`FOCUS_DUR` 0.5–1.2 s — 移焦/拉焦是 deliberate 动作，非 snap
  - 效果：更短 → 急促「snap focus」；更长 → 慵懒电影感移焦
- **RACK_START / RACK_DUR** — 移焦窗口（前景 ⇄ 背景）。
  - 约束：两平面补间共享 `RACK_START` 与 `RACK_DUR`，中点交叉；在 `RACK_START` **之前** `gsap.set` 预模糊平面
- **REFOCUS_START / REFOCUS_DUR** — 回清晰收束窗口。
  - 约束：`REFOCUS_START + REFOCUS_DUR ≤ DURATION`，使场景在结束/交接前真正回到清晰
- **PUSH_SCALE / PUSH_X / PUSH_Y**（推进时模糊集群变体）— `.world` 上的相机移动。
  - 约束：与景深补间共享 `FOCUS_START` + `FOCUS_DUR`，移动与失焦读成一拍；反平移数学在 `coordinate-target-zoom` / `viewport-change`
- **BREATH_CYCLES / BREATH_DUR / FOCAL_BREATH_PX**（对焦呼吸变体）。
  - 范围：`FOCAL_BREATH_PX ≤ 0.6` px；周期 2–3 s； barely-there 点缀，默认可省略

### Tokens

- **{bgGradient}** — 通常偏暗，使清晰焦内层读成被照亮、靠前
- **{textColor}** — 在 `{bgGradient}` 上高对比；模糊会柔化边缘，勿依赖发丝级对比
- **{font}** — display 字重；失焦文案需粗字重才能在 defocus 时保持形状可读

## 核心原则

- **`--dof` 驱动模糊；补间变量，绝不用 CSS `transition`。** 读 `filter: blur(var(--dof))` 并在 GSAP 时间线上补间 `--dof`，模糊留在 HF seek 时钟上。CSS `transition` 在 `filter` 上按浏览器自己的时钟插值，逐帧 seek 会闪烁/不同步。
- **模糊 SMALL / GROUPED 层，而非巨型层。** Filter-blur 成本随半径与被模糊元素的像素面积缩放。全画幅背景上 20 px 模糊是最坏情况；同样模糊在小上下文卡片或单一分组 wrapper 上很便宜。优先把焦平面**推前并保持清晰**，而非猛加背景模糊半径。
- **每层 animating blur 的 `will-change: filter`** — 提升到独立层，每帧重栅格便宜。模糊落定后若层还有重 transform，可去掉。
- **半径保持 modest。** 大面 ≤ ~24 px；靠 `opacity` **压暗**与较小 blur 一起做「推后」，而非单靠 blur。压暗 + modest blur 比 blur 拉满更像真实景深。
- **焦内层保持真正清晰** — `--dof` 为 `0` 且不动（或呼吸 ≤0.6 px）。焦内元素任何可见模糊都会破坏「这就是重点」的阅读。
- **移焦上的状态连续** — 失焦平面在移焦开始时必须持有 incoming 平面*原先*的模糊，反之亦然；在同一位置对同一 `--dof` 写两个补间，交叉才无缝（同 `press-release-spring` 的 press↔release）。
- **景深与相机独立** — 模糊层，transform `.world` 做推进。不同属性通道，可组合不打架。勿用相机 transform 假景深或反之。
- **交接前收束为清晰** — 若下一拍是 crossfade/push，尾部 refocus 到 `--dof:0`，出帧 crisp；半失焦交接读成「渲染 glitch」。

## 关键约束

- **时间线必须 paused**：`gsap.timeline({ paused: true })`
- **Registry key = `data-composition-id`**
- **勿在 `filter` / `opacity` 上用 CSS `transition`** — 改在时间线上补间 `--dof` 与 `opacity`
- **无 `repeat` / `yoyo` / 无限补间** — 焦内拉焦是有限补间；任何呼吸是有界 `onUpdate` 读驱动相位（或有限补间），绝不用 `repeat:-1`
- **无 `Math.random` / `Date.now`** — 每层模糊由 `data-depth` / 元素 index 推导，每次 seek 一致
- **此处仅补间 `filter`（blur）+ `opacity`** — 二者 paint-only 且 seek-safe。并发相机移动用 GSAP transform 别名（`x`, `y`, `scale`）；勿补间 `width` / `height` / `left` / `top`
- **animating blur 的层上 `will-change: filter`**；保持模糊 footprint 小
- **大面上单层模糊半径 ≤ ~24 px** — 超过则成本（与可见 banding）上升；应缩小/分组层

## 组合

- [multi-phase-camera.md](multi-phase-camera.md) — 本规则提供其焦外衰减的 push-in / push-through；DoF 补间与 PUSH 阶段同位置
- [coordinate-target-zoom.md](coordinate-target-zoom.md) — 向焦心 zoom 同时 off-center 层模糊（`constellation-hub` 钩子）
- [viewport-change.md](viewport-change.md) — 在倾斜卡片平面上 pan，近远卡片间移焦（`cursor-ui-demo` focus-pull）
- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 英雄指标清晰 count up，周围卡片压暗 + 模糊（`dataviz-countup` 聚光）
- [3d-page-scroll.md](3d-page-scroll.md) — 可在其间移焦的视差卡片栈平面
- [sine-wave-loop.md](sine-wave-loop.md) — 移焦落定后焦内层 idle 呼吸（idle 振幅与 focus-breath 都保持 tiny）

## 与 HF skills 搭配

- `/hyperframes-animation` — 补间 CSS 自定义属性 + 多补间协调
- `/hyperframes-core` — composition 接线
- `/hyperframes-cli` — `hyperframes lint`
