---
name: 3d-page-scroll
description: 将完整网页渲染为倾斜的 3D 卡片，通过滚动揭示特定区块。
metadata:
  tags: 3d, page, scroll, webpage, tilt, product-demo, perspective
---

# 3D 页面滚动

将网页（或长内容）呈现为倾斜的 3D 卡片。带弹簧感的滚动会揭示特定区块，而静态 3D 透视则增加物理纵深感。

## 工作原理

两种彼此独立的变换组合在一起：

1. **3D 倾斜** — 在卡片上使用静态 `rotateY` + `rotateX`，并在父级设置 `perspective`。整个场景中角度**不会**变化。
2. **滚动** — 卡片内的内容在裁剪容器内垂直平移（GSAP 中的 `translateY` / `y`），由 GSAP 补间驱动。通过 `ease: "power3.out"` 或 `"power4.out"` 实现类似弹簧的减速。

可选层：

3. **聚光灯遮罩** — 径向渐变遮罩在滚动落定后，除焦点区域外其余部分变暗。用于将注意力引到某一区块。

多步滚动（滚动 → 暂停 → 再滚动）时，在时间轴的不同位置使用多次 `tl.to(".page-content", { y: -<distance>, ... }, <position>)`。

## HTML

```html
<div
  class="scene"
  id="page-scroll-scene"
  data-composition-id="page-scroll-scene"
  data-start="0"
  data-duration="5"
  data-track-index="0"
>
  <div class="tilt-card">
    <div class="page-content">
      <!-- Full {Brand} webpage recreation, taller than card height so
           scrolling matters. Each section is real DOM, not a screenshot. -->
      <section class="page-hero">{heroContents}</section>
      <section class="page-features">{featuresContents}</section>
      <section class="page-target" id="target-section">{targetContents}</section>
      <section class="page-cta">{ctaContents}</section>
    </div>

    <div class="spotlight"></div>
  </div>
</div>
```

## CSS（hero-frame 布局）

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
}

.tilt-card {
  position: absolute;
  left: 50%;
  top: 50%;
  /* tilt + perspective set in CSS only if no other transform tween touches
     this element. If GSAP also tweens scale on .tilt-card, set the tilt
     via gsap.set() to avoid matrix overwrites. */
  transform: translate(-50%, -50%) perspective({perspectivePx}) rotateY({tiltYDeg}) rotateX({tiltXDeg});
  transform-style: preserve-3d;
  width: {cardWidth};
  height: {cardHeight};
  border-radius: 24px;
  background: {cardBackgroundColor};
  overflow: hidden; /* clip the scrolling content */
  /* shadow X-offset sign must match tiltY sign (negative tiltY ⇒ positive X) */
  box-shadow: 40px 30px 80px rgba(0, 0, 0, 0.45);
}

.page-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  /* height is intrinsic from sections — taller than .tilt-card.height */
}

.page-content section {
  height: {sectionHeight}; /* sections sized so cumulative offset = target distance */
  padding: 64px;
  /* section-specific styling … */
}

.spotlight {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0;
  background: radial-gradient(
    ellipse 60% 35% at 50% 50%,
    transparent 50%,
    {spotlightDimColor} 100%
  );
}
```

## GSAP 时间轴

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Phase 1 — Card enters (optional, can skip if card is in from t=0)
  // Phase 2 — Scroll to the target section.
  // SCROLL_DISTANCE is measured at design time from the page layout
  // (top of .page-content origin to vertical center of #target-section,
  // accounting for card height).
  tl.to(
    ".page-content",
    {
      y: -SCROLL_DISTANCE,
      duration: SCROLL_DUR,
      ease: "power3.out",
    },
    SCROLL_AT,
  );

  // Phase 3 — Spotlight fades in on the target after scroll settles
  tl.to(
    ".spotlight",
    {
      opacity: 1,
      duration: SPOTLIGHT_FADE_DUR,
      ease: "power1.inOut",
    },
    SPOTLIGHT_AT,
  );

  window.__timelines["page-scroll-scene"] = tl;
</script>
```

### 多阶段滚动变体

```js
// Scroll to section A → hold → scroll to section B.
// SCROLL_DISTANCE_A and SCROLL_DISTANCE_B are both measured from the
// .page-content origin (NOT delta from previous step).
tl.to(
  ".page-content",
  { y: -SCROLL_DISTANCE_A, duration: SCROLL_DUR, ease: "power3.out" },
  SCROLL_AT_A,
);
tl.to(
  ".page-content",
  { y: -SCROLL_DISTANCE_B, duration: SCROLL_DUR, ease: "power3.out" },
  SCROLL_AT_B,
);
```

对同一属性连续使用 `y:` 补间时，GSAP 会叠加组合——每次补间都从前一次补间结束时的值开始。

## 如何选取参数

- **tiltYDeg** — CSS 中的静态 Y 轴旋转（或通过 `gsap.set()` 设置）。
  - 范围：-12 至 -4（向左倾）或 4 至 12（向右倾）；0 表示无透视旋转。
  - 效果：绝对值越大 3D 越 dramatic；接近 0 则退化为平面。
  - 约束：阴影 X 偏移符号须匹配（负 tiltY ⇒ 正 box-shadow X）。
- **tiltXDeg** — 静态 X 轴旋转。
  - 范围：0-6
  - 效果：正值使上边缘远离观者。
- **perspectivePx** — 透视距离。
  - 范围：800-2000 px
  - 效果：越小 foreshortening 越明显；越大越接近正交视图。
- **cardWidth / cardHeight** — 卡片外框尺寸。
  - 约束：卡片高度 < 内容总高度，否则滚动没有可揭示的内容。
- **sectionHeight** — 各滚动区块的高度。
  - 约束：所有 section 高度之和 ≥ cardHeight + SCROLL_DISTANCE，滚动后目标区块才能落在框内。
- **SCROLL_AT** — 滚动补间开始的时间轴秒数。
  - 约束：须 ≥ `.page-content` 上任何先前淡入补间的结束时间。
- **SCROLL_DUR** — 单次滚动补间时长。
  - 范围：0.8-1.8 s
  - 效果：更短像硬切；更长像程序化滚动。
- **SCROLL_DISTANCE** — `.page-content` 向上平移的像素数。
  - 约束：设计时根据目标区块偏移量测量一次；不是可随意调的参数。
- **SPOTLIGHT_AT** — 聚光灯开始淡入的时间轴秒数。
  - 约束：宜 ≥ SCROLL_AT + SCROLL_DUR（或略早以重叠过渡），以便聚光照在刚滚到的区块上。
- **SPOTLIGHT_FADE_DUR** — 聚光灯不透明度淡入时长。
  - 范围：0.4-0.8 s
- 多阶段变体 — **SCROLL_AT_A / SCROLL_AT_B**：须满足 `SCROLL_AT_A + SCROLL_DUR ≤ SCROLL_AT_B`，避免两次滚动争抢 `y` 属性。

缓动族 — 离散选择：

- `power3.out` — 强减速；读作程序化滚动并「落定」。默认。
- `power4.out` — 更强；读作带惯性的滚动。
- `power2.inOut` — 对称；读作电影感平移而非 UI 滚动。

选定一种并在场景中所有滚动上统一使用——同一场景混用多种缓动会显得顿挫。

## 核心原则

- **倾斜是静态的**，不做动画。整张卡片全程保持同一角度。
- **阴影方向与倾斜一致**：左倾的卡片阴影投向右方（正 X 阴影偏移）。不一致会破坏 3D 错觉。
- **页面内容是真实 HTML**，不是截图。截图无法精确高亮或滚动到某一区块。
- **用真实布局算距离**：滚动目标距离来自实际累计的 section 高度，而非估算像素。
- **聚光灯作为 overlay**，不要放在 page-content 内 — overlay 位于滚动内容之上，相对卡片保持固定。

## 关键约束

- **`.tilt-card` 上 `overflow: hidden`** — 滚动内容必须在卡片边界内裁剪，否则会溢出圆角
- **`.tilt-card` 上 `transform-style: preserve-3d`** — 3D 子元素（或干净地组合 `perspective` 与旋转）所必需
- **时间轴必须暂停**：`gsap.timeline({ paused: true })`。切勿 `tl.play()` — HF 逐帧 seek
- **注册表键 = `data-composition-id`**：`window.__timelines["page-scroll-scene"]` 须与场景根节点的 `data-composition-id` 一致
- **有限滚动距离** — 根据实际内容几何计算；不要用可能越过内容末尾的任意值
- **多阶段滚动使用同一缓动** — 混用 `power3.out` 与 `power1.inOut` 会显得顿挫；整场选一种

## 组合用法

- [asr-keyword-glow.md](asr-keyword-glow.md) — 按旁白词时间戳同步高亮页面元素
- [multi-phase-camera.md](multi-phase-camera.md) — 页面滚动时整体相机缩放（目标区块落定时 zoom-in）
- [cursor-click-ripple.md](cursor-click-ripple.md) — 光标落在滚入视野的区块内 UI 元素上

## 搭配的 HF 技能

- `/hyperframes-animation` — 时间轴与缓动参考；`y:` 补间基础
- `/hyperframes-core` — composition 接线、`data-*` 属性
- `/hyperframes-cli` — `hyperframes lint` 校验注册表键与 duration
