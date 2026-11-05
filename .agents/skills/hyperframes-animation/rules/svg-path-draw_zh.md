---
name: svg-path-draw
description: 使用 stroke-dasharray 与 stroke-dashoffset 让 SVG 路径逐步绘出动画。
metadata:
  tags: svg, stroke, draw, path, reveal, icon, vector
---

# SVG 路径绘制

通过动画描边，让 SVG 形状像被笔实时描摹一样逐渐显现。

## 工作原理

技巧在于同时使用两个 SVG 描边属性：

1. **`stroke-dasharray = <pathLength>`** — 将虚线模式设为与路径总长度相等的单段虚线，使整条路径成为「一段虚线」
2. **`stroke-dashoffset`** — 控制虚线偏移多少从而移出视野。从 `pathLength` 开始（整条路径被偏移出去 → 不可见），动画到 `0`（无偏移 → 完全绘出）

路径长度通过 DOM API `path.getTotalLength()` 计算。

## HTML

```html
<div
  class="scene"
  id="svg-draw-scene"
  data-composition-id="svg-draw-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <svg class="logo-mark" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <!-- Multi-segment glyph; draw all segments sequentially -->
    <path id="bar-left" d="M 60 40 L 60 160" />
    <path id="bar-right" d="M 140 40 L 140 160" />
    <path id="bar-mid" d="M 60 100 L 140 100" />
  </svg>
  <div class="brand-line">{Brand}</div>
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
  background: {bgColor};
  gap: 32px;
}

.logo-mark {
  width: 320px;
  height: 320px;
}

.logo-mark path {
  fill: none;
  stroke: {accentColor};
  stroke-width: 12;
  stroke-linecap: round; /* soften endpoints */
  stroke-linejoin: round;
  /* Initial state: invisible. GSAP fills strokeDasharray + strokeDashoffset
     based on each path's measured length. */
}

.brand-line {
  font-family: {font};
  font-weight: 700;
  font-size: 48px;
  color: {textColor};
  opacity: 0; /* fades in after stroke completes */
  letter-spacing: 0.04em;
}
```

## GSAP 时间轴

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};

  // Named constants — assignments live in the example, not here.
  // See "How to Choose Values" below for ranges and selection criteria.
  const SEGMENT_DRAW_DUR; // per-segment stroke duration
  const FINAL_SEGMENT_DUR; // shorter draw on the last (shorter) segment
  const SEG_1_START; // first segment start time
  const SEG_2_START; // second segment start time (overlaps SEG_1 tail)
  const SEG_3_START; // third segment start time (overlaps SEG_2 tail)
  const BRAND_FADE_DUR; // wordmark fade-in duration
  const BRAND_FADE_START; // wordmark fade-in start (after last stroke settles)

  // Measure each path's total length and set up its dash pattern.
  // getTotalLength() is a real DOM API — its return value is dynamic
  // measured geometry, NOT a magic number.
  const paths = document.querySelectorAll(".logo-mark path");
  paths.forEach((p) => {
    const len = p.getTotalLength();
    p.style.strokeDasharray = `${len}`;
    p.style.strokeDashoffset = `${len}`;
  });

  const tl = gsap.timeline({ paused: true });

  // Stagger draws across segments — each starts before the previous finishes
  // so the eye reads continuous motion.
  tl.to(
    "#bar-left",
    {
      strokeDashoffset: 0,
      duration: SEGMENT_DRAW_DUR,
      ease: "power2.out",
    },
    SEG_1_START,
  );
  tl.to(
    "#bar-right",
    {
      strokeDashoffset: 0,
      duration: SEGMENT_DRAW_DUR,
      ease: "power2.out",
    },
    SEG_2_START,
  );
  tl.to(
    "#bar-mid",
    {
      strokeDashoffset: 0,
      duration: FINAL_SEGMENT_DUR,
      ease: "power2.out",
    },
    SEG_3_START,
  );

  // Brand line fades in after the strokes settle
  tl.to(
    ".brand-line",
    {
      opacity: 1,
      duration: BRAND_FADE_DUR,
      ease: "power1.out",
    },
    BRAND_FADE_START,
  );

  window.__timelines["svg-draw-scene"] = tl;
</script>
```

## 如何选取数值

- **SEGMENT_DRAW_DUR** — 每段描边的时长
  - 范围：0.3–0.8s
  - 效果：偏低像快速一划（适合短段）；偏高像刻意描线（适合长曲线）
  - 约束：须足够短，使整段链（最后一段结束）早于 BRAND_FADE_START；超过约 1s 在 logo 揭示中会显得拖沓
  - 参考：短轮廓段约 0.5s

- **FINAL_SEGMENT_DUR** — 最短 / 最后一段的时长
  - 范围：0.25–0.6s
  - 效果：应与段长成正比 — 短连接段若用 SEGMENT_DRAW_DUR 会显得比更长的段更慢
  - 约束：当该段明显短于其他段时，通常为 SEGMENT_DRAW_DUR 的 60–80%
  - 参考：长度约为竖条约 2/3 的中横条约 0.35s

- **SEG_1_START** — 第一段开始时间
  - 范围：0–0.4s
  - 效果：0 表示播放即动；>0 在动之前留空场一拍
  - 约束：应 ≥ 0
  - 参考：约 0.2s 的短前奏让观众在动之前安定下来

- **SEG_2_START** — 第二段开始时间
  - 范围：SEG_1_START + (0.5 \* SEGMENT_DRAW_DUR) 至 SEG_1_START + SEGMENT_DRAW_DUR
  - 效果：越接近 SEG_1_START + 0.5\*SEGMENT_DRAW_DUR 越急促/重叠；越接近 SEG_1_START + SEGMENT_DRAW_DUR 越顺序
  - 约束：错开约为 SEGMENT_DRAW_DUR 的 70–80% 读起来像连续运动（而非 3 段孤立动画）
  - 参考：SEG_1_START + ~0.25s（约为 SEGMENT_DRAW_DUR 的一半）

- **SEG_3_START** — 第三段开始时间
  - 范围：SEG_2_START + (0.5 \* SEGMENT_DRAW_DUR) 至 SEG_2_START + SEGMENT_DRAW_DUR
  - 效果：同 SEG_2_START — 控制感知节奏
  - 约束：应保持 SEG_1 与 SEG_2 之间相同的错开比例
  - 参考：SEG_2_START + ~0.4s

- **BRAND_FADE_DUR** — 字标淡入时长
  - 范围：0.3–0.8s
  - 效果：偏低快速出现（急促）；偏高缓缓进入（偏品牌/高级感）
  - 约束：须在合成的 `data-duration` 结束前完成
  - 参考：沉稳的 logo 定版约 0.5s

- **BRAND_FADE_START** — 字标淡入开始时间
  - 范围：max(SEG_3_START + FINAL_SEGMENT_DUR, …) 至该值 + 0.4s
  - 效果：恰在最后描边结束时启动感觉紧密衔接；略加一拍让描边先「落定」再出现字标
  - 约束：必须 ≥ SEG_3_START + FINAL_SEGMENT_DUR（否则字标在绘制过程中出现，与描边争抢注意力）
  - 参考：SEG_3_START + FINAL_SEGMENT_DUR + ~0.2s

此处使用的缓动族是离散选择，不是可调标量：

- **描边绘制** 使用 `power2.out` — 轻微减速模拟收笔。不要用 `back.out` 或 `elastic.out`（笔不会弹）。
- **品牌淡入** 使用 `power1.out` — 透明度补间上的柔和尾部。
- 若要恒定速度的「真笔描摹」感，可改为 `none`（见变体）。

## 变体

### 旋转起点（从顶部而非 3 点钟方向开始）

默认 `<circle>` 与 `<rect>` 的描边从 3 点钟方向开始。旋转元素可从顶部开始：

```html
<circle
  cx="100"
  cy="100"
  r="60"
  id="ring"
  style="transform-origin: 100px 100px; transform: rotate(-90deg);"
/>
```

### 线性（恒定速度）绘制

使用 `ease: 'none'` 实现匀速绘制（像真实笔迹）：

```js
tl.to("#path", { strokeDashoffset: 0, duration: SEGMENT_DRAW_DUR, ease: "none" }, SEG_1_START);
```

### 先描边后填充

对有填充色的 SVG 形状，在描边完成后再动画填充透明度：

```js
tl.to(
  "#path",
  { strokeDashoffset: 0, duration: SEGMENT_DRAW_DUR, ease: "power2.out" },
  SEG_1_START,
);
tl.to(
  "#path",
  { fillOpacity: 1, duration: FILL_FADE_DUR, ease: "power1.out" },
  SEG_1_START + SEGMENT_DRAW_DUR,
);
```

需在 CSS 中初始 `fill-opacity: 0`，并设置真实的 `fill` 颜色。

## 关键原则

- **将 `strokeDasharray` 设为路径的 `getTotalLength()` 值**，不要用任意数字 — 猜错会导致有动画但与几何不匹配
- **初始 `strokeDashoffset` 设为相同长度**，再动画降至 `0`
- **在时间轴设置里测量，而非模块顶层** — 某些环境下模块代码运行时 SVG 可能尚未渲染。HF 运行时内联 SVG 在顶层也可工作，但宜稳妥处理
- **`stroke-linecap: round`** 使端点更柔和（结束不那么突兀）
- **多路径顺序绘制时，错开约为上一段时长的 70–80%** — 视觉上像连续运动，而非 N 段独立动画
- **不要搭配 `back.out` 或 `elastic.out`** — 描边弹跳感觉不对（笔不会弹）

## 关键约束

- **仅描边绘制时 CSS 中 `fill: none`** — 否则填充区会立刻出现，破坏揭示效果
- **路径长度在浏览器中测量**：要求 SVG 在 DOM 中。HF 内联 SVG 没问题；加载的 `<image>` SVG 可能不行
- **时间轴必须暂停**：`gsap.timeline({ paused: true })`
- **注册表键 = `data-composition-id`**
- **适用于**：`<path>`、`<circle>`、`<rect>`、`<line>`、`<polyline>`、`<polygon>`、`<ellipse>`（任何有描边的元素）
- **复杂路径**若 `getTotalLength()` 看起来不对，可略高估 `strokeDasharray`（如 `len * 1.05`）— 过大在动画开始时不可见（无可见缺口），过小会裁切末端

## 组合

- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 组合：描边绘制图标，旁边数字同步计数
- [hacker-flip-3d.md](hacker-flip-3d.md) — 组合：SVG logo 描边绘制，其下 hacker-flip 字标再揭示

## 搭配的 HF 技能

- `/hyperframes-animation` — 时间轴 + 描边属性补间
- `/hyperframes-core` — 合成接线
- `/hyperframes-cli` — `hyperframes lint`
