---
name: card-morph-anchor
description: 容器在镜头之间平滑变换尺寸与圆角，作为视觉转场锚点。
metadata:
  tags: morph, anchor, transition, border-radius, container, shape
---

# 卡片变形锚点

容器在两种视觉状态之间平滑变换宽度、高度、圆角以及（可选的）背景。变形本身**就是镜头转场**——无需单独的转场效果。观众视线会跟随变形中的容器，作为镜头之间的锚点。

## 工作原理

单个 GSAP 补间同时动画化多个容器属性（width / height / border-radius / background）。与此同时：

1. **旧内容**在变形前约 40% 的时间内淡出
2. **新内容**在变形后约 40% 的时间内淡入
3. **可选的最终淡出**——变形容器本身淡出至 0，露出其后渲染的实际下一镜头元素

持久存在的容器在内容与形状变化时仍提供视觉连续性。

## HTML

```html
<div
  class="scene"
  id="morph-scene"
  data-composition-id="morph-scene"
  data-start="0"
  data-duration="4"
  data-track-index="0"
>
  <!-- The persistent morph container -->
  <div class="morph-card">
    <div class="content-old">
      <h2>{shotOneHeadline}</h2>
      <p>{shotOneSubcopy}</p>
    </div>
    <div class="content-new">
      <img src="{shotTwoIcon}" alt="logo" />
    </div>
  </div>

  <!-- Optional: actual next-shot element behind the morph -->
  <div class="next-shot-anchor">
    <img src="{nextShotAnchor}" alt="anchor" />
  </div>
</div>
```

## CSS（hero-frame 布局）

卡片起始为宽矩形（镜头 1 状态）。所有属性从一开始就存在；仅透明度不同：

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
}

.morph-card {
  position: relative;
  width: {SHOT_ONE_W}px;
  height: {SHOT_ONE_H}px;
  border-radius: {SHOT_ONE_RADIUS}px;
  background: {surfaceShotOne};
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  display: grid;
  place-items: center;
}

.content-old,
.content-new {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  padding: 32px;
}

.content-old {
  opacity: 1;
}
.content-new {
  opacity: 0;
}

.next-shot-anchor {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  opacity: 0; /* GSAP fades this in as morph card fades out */
  /* Use DOM ORDER for stacking — render .next-shot-anchor BEFORE .morph-card
     in markup so the morph card is naturally on top. Do NOT use z-index: -1
     and then snap it positive mid-fade — that causes a visible pop. */
}
```

## GSAP 时间轴

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Named constants — assign in your example only. See "How to Choose Values".
  const HOLD_BEAT; // s — pre-morph dwell on shot 1
  const MORPH_START; // s — usually = HOLD_BEAT
  const MORPH_DUR; // s — full container morph length
  const SHOT_TWO_W; // px — final container width
  const SHOT_TWO_H; // px — final container height
  const SHOT_TWO_RADIUS; // px — ≤ min(SHOT_TWO_W, SHOT_TWO_H) / 2
  const OLD_FADE_FRAC; // 0..0.5 — fraction of MORPH_DUR for old content fade
  const NEW_FADE_FRAC; // 0..0.5 — fraction of MORPH_DUR for new content fade
  const FINAL_FADE_FRAC; // 0..0.3 — optional tail fade for handoff
  // {surfaceShotTwo} is a CSS background token (solid or gradient).

  // Hold shot 1 — let the viewer register the wide banner before morphing.

  // Phase 1 — Morph container properties simultaneously
  tl.to(
    ".morph-card",
    {
      width: SHOT_TWO_W,
      height: SHOT_TWO_H,
      borderRadius: SHOT_TWO_RADIUS,
      background: "{surfaceShotTwo}",
      duration: MORPH_DUR,
      ease: "power2.inOut",
    },
    MORPH_START,
  );

  // Phase 2 — Old content fades during the FIRST OLD_FADE_FRAC of the morph
  tl.to(
    ".content-old",
    {
      opacity: 0,
      duration: MORPH_DUR * OLD_FADE_FRAC,
      ease: "power1.in",
    },
    MORPH_START,
  );

  // Phase 3 — New content fades in during the LAST NEW_FADE_FRAC of the morph
  tl.to(
    ".content-new",
    {
      opacity: 1,
      duration: MORPH_DUR * NEW_FADE_FRAC,
      ease: "power1.out",
    },
    MORPH_START + MORPH_DUR * (1 - NEW_FADE_FRAC),
  );

  // Optional Phase 4 — Final fade: morph container disappears at the very end,
  // revealing the actual next-shot element behind it.
  tl.to(
    ".morph-card",
    {
      opacity: 0,
      duration: MORPH_DUR * FINAL_FADE_FRAC,
      ease: "power1.in",
    },
    MORPH_START + MORPH_DUR * (1 - FINAL_FADE_FRAC),
  );

  window.__timelines["morph-scene"] = tl;
</script>
```

## 建议变形的属性

| 属性               | 变化形态                                                       | 视觉效果                     |
| ------------------ | -------------------------------------------------------------- | ---------------------------- |
| `width` / `height` | `SHOT_ONE_W × SHOT_ONE_H` → `SHOT_TWO_W × SHOT_TWO_H`          | 宽卡片缩小为图标尺寸         |
| `borderRadius`     | `SHOT_ONE_RADIUS` → `SHOT_TWO_RADIUS`（≤ 较短边的一半）        | 矩形变为圆形                 |
| `background`       | `{surfaceShotOne}` → `{surfaceShotTwo}`（纯色或渐变）          | 容器视觉身份切换             |
| `boxShadow`        | 基础阴影 → 强调光晕 token                                      | 强调程度变化                 |

当这些属性包含在同一次 `tl.to(...)` 调用中时，GSAP 会同时补间它们。

## 如何选取数值

- **HOLD_BEAT** — 变形前的停留，让观众在变化前认清镜头 1
  - 范围：0.6–1.5 s
  - 效果：偏低显得仓促/像 glitch；偏高拖慢节奏
  - 约束：必须 ≥ 镜头 1 内容入场 settle 时间
- **MORPH_START** — 容器变形开始时刻
  - 范围：规范模式中等于 `HOLD_BEAT`
  - 约束：必须大于任意镜头 1 入场补间结束时间
- **MORPH_DUR** — 容器同步变形的总时长
  - 范围：0.6–1.2 s
  - 效果：偏低像 snap；偏高失去动量
  - 约束：过短变形（<0.5s）无法容纳旧内容淡出与新内容淡入
- **SHOT_TWO_W / SHOT_TWO_H** — 容器最终尺寸
  - 范围：交接至图标级锚点时 80–400 px
  - 约束：若交接（`.next-shot-anchor`），**必须**与锚点尺寸完全一致，否则会出现可见 pop
- **SHOT_TWO_RADIUS** — 最终圆角（用于呈现圆形 / 胶囊 / 软矩形）
  - 范围：0 至 `min(SHOT_TWO_W, SHOT_TWO_H) / 2`
  - 效果：较短边的一半 = 正圆；更小 = 软矩形
  - 约束：大于一半会被视觉 clamp——浪费补间
- **OLD_FADE_FRAC** — 镜头 1 内容在 `MORPH_DUR` 中所占淡出比例，自 `MORPH_START` 起算
  - 范围：0.3–0.5
  - 效果：偏低过早切走镜头 1；偏高与镜头 2 内容重叠
  - 约束：`OLD_FADE_FRAC + NEW_FADE_FRAC ≤ 1`（中间空隙为「仅形状变化」时刻）
- **NEW_FADE_FRAC** — 镜头 2 内容在 `MORPH_DUR` 中所占淡入比例，于 `MORPH_START + MORPH_DUR` 结束
  - 范围：0.3–0.5
  - 效果：与 OLD_FADE_FRAC 对称
- **FINAL_FADE_FRAC** — 可选尾部比例，变形容器本身淡出至 0 以完成交接
  - 范围：0（无交接）或 0.1–0.2
  - 约束：仅当 `.next-shot-anchor` 与变形最终视觉完全一致时使用
- **Ease 族** — 离散选择
  - 选项：`power2.inOut`（规范、均衡）、`power3.inOut`（更利落）、`expo.inOut`（最电影感，但低时长下可能显 sluggish）
  - 避免在变形本身使用 `back.out` / `elastic.out` —  overshoot 与尺寸变化冲突

CSS 侧占位符（`SHOT_ONE_W`、`SHOT_ONE_H`、`SHOT_ONE_RADIUS`、`{surfaceShotOne}`、`{surfaceShotTwo}`）在示例中填入真实值。选择 `{surfaceShotOne}` 与 `{surfaceShotTwo}` 时，渐变/纯色 stop 数量需一致（GSAP 仅在 stop 数量相同时才能插值 background 渐变）。

## 核心原则

- **所有目标属性放在一次补间里** — 共享同一 ease 与 duration，同步变形
- **旧内容早淡出、新内容晚淡入** — 中间发生容器形状变化，形成自然的「眨眼」瞬间
- **最终淡出可选** — 下一镜头有真实锚点元素可交接时使用（例如图标变形「成为」的头像）
- **形状与交叉淡入淡出用同一 easing** — 避免 `power2.inOut` 变形配 `bounce.out` 内容，会显得不同步
- **❗ 若用 `.next-shot-anchor` 交接，其视觉必须与 `.morph-card` 最终状态像素级一致** — 相同 `width` / `height`、相同 `border-radius`、相同 `background`、相同 `box-shadow`、相同内部图标尺寸。二者任何视觉差异 = 交叉淡入淡出时的可见 pop。若无法完全一致，**放弃交接**，让变形卡片停在最终状态（必要时加 breath 增加生气）。

## 关键约束

- 变形容器使用 **`overflow: hidden`** — 形状变化时内容必须裁剪，否则内容会溢出变形的圆角
- **变形前先停留一拍** — 让观众认清镜头 1 内容；即时变形会像 glitch
- **时间轴必须 paused**：`gsap.timeline({ paused: true })`。切勿 `tl.play()`
- **注册键 = `data-composition-id`**：`window.__timelines["morph-scene"]` 须与场景根一致
- **用 `background` 补间，而非 `background-color`**：渐变需要 `background`（目标为 stop 数量相同的渐变时 GSAP 支持渐变插值）。纯色 → 纯色时 `backgroundColor` 可用。
- **结束态 `borderRadius` 应 ≤ 较短维度的一半** — 否则圆角被视觉 clamp，边界处变形显得突兀
- **❗ 勿在淡入淡出中途 snap `z-index`** — 若需 `.next-shot-anchor` 从变形卡片后方出现，用 **DOM 顺序**（在 markup 中先渲染 `.next-shot-anchor` 再 `.morph-card`，使变形卡片自然在上层），再交叉淡入淡出 opacity。在活跃 opacity 补间中调用 `tl.set({ zIndex: ... })` 会在堆叠顺序翻转时、opacity 过渡完成前产生可见 flicker。

## 变体：变形至目标元素位置

当镜头 2 不在居中（例如变形卡片「落」在 dock、侧栏或网格中的某个图标上）时，从**目标元素的元素位置**计算目标 `top` / `left`，而非其视觉中心。常见错误：减去 `height/2` 得到中心，再赋给 morph-card 的 `top` —— 但若 `.morph-card` 使用绝对定位且 `top` + `margin: 0`（无 transform 居中），`top` 表示**元素上边缘**，而非中心。

数学模板（示例：变形卡片落到底部 dock 的图标上）：

```
target_element_top = viewport_height − dock_bottom_offset − dock_padding_y − icon_height
                   = 1080 − 60 − 22 − 110 = 888 px
```

然后将 `.morph-card { top: 888 }` 补间，使其元素顶边与目标图标元素顶边对齐。若误补间到 `888 + icon_height/2 = 943` 会落得更低；补间到诸如 `top: 933` 的「中心」值（算术 off-by）会更糟。

时间轴开始前务必用 **`getBoundingClientRect()` 测量目标元素**，并使用测得数值 —— 不要从 CSS 值手算，padding、border 与父级 transform 会叠加。

## 组合

- [scale-swap-transition.md](scale-swap-transition.md) — 更简单的变形，无尺寸变化（仅 scale + 内容切换）
- [sine-wave-loop.md](sine-wave-loop.md) — 最终状态的轻柔呼吸（例如最终小圆图标 idle 时带 breath）

## 搭配的 HF 技能

- `/hyperframes-animation` — 时间轴与多属性补间参考
- `/hyperframes-core` — 合成编排、`data-*` 属性
- `/hyperframes-cli` — `hyperframes lint` 校验场景结构
