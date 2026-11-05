---
name: stat-bars-and-fills
description: 将数字与图形配对的数据可视化原语 — 增长柱（CSS scaleY 交错）、进度填充（条或环），以及部分星级评分的擦除效果。可 seek、确定性。
metadata:
  tags: data, stats, chart, bars, progress, ring, stars, rating, infographic, number
---

# 统计柱与填充

在数字旁赋予统计量**视觉重量**的图形：小型柱状图、按百分比填充的进度条/环，或按小数评分从左向右填充的星级行。与 [counting-dynamic-scale.md](counting-dynamic-scale.md)（数字部分）搭配，构成完整的统计场景。

**版式蓝图 — 选一种并在所有统计项中保持一致：**

- **单焦点** — 一个居中画幅，数字为主角，环或条在其下方/周围。最适合顺序揭示（同一画幅内 stat 1 → stat 2 → stat 3）。
- **分屏** — 左侧大数字，右侧配对图形。更适合多项统计同时展示，或每项需要 distinct 视觉时。

同一作品中不要在不同统计项之间混用蓝图 — 会显得不一致。

## 1 — 增长柱（CSS `scaleY` 交错）

柱从基线向上增长并交错；最后一根为强调色。

```css
.bars {
  display: flex;
  align-items: flex-end;
  gap: 14px;
  height: 280px;
}
.bar {
  width: 48px;
  background: #3a4a64;
  transform: scaleY(0);
  transform-origin: bottom center; /* grow UP from the baseline, not from center */
}
.bar:last-child {
  background: #ffc300;
} /* accent the final/current bar */
```

```js
// Heights are authored in CSS (e.g. inline height per bar); GSAP only reveals scaleY 0→1.
tl.to(".bar", { scaleY: 1, duration: 0.7, ease: "power3.out", stagger: 0.08 }, 0.3);
```

> 使用 `scaleY`（变换），切勿动画 `height` — 运行时禁止对 height 做补间。在 CSS 中设定每根柱的最终高度，从 0 缩放。

## 2 — 进度填充

**条形** — 从左原点 `scaleX`：

```css
.track {
  width: 520px;
  height: 16px;
  background: #1b263b;
  border-radius: 8px;
  overflow: hidden;
}
/* width:100% is REQUIRED — an absolutely-positioned fill with no width is 0px, and scaleX of 0 is
   still 0 → the bar renders invisible (and no lint/inspect check catches a zero-width scaled element). */
.fill {
  width: 100%;
  height: 100%;
  background: #ffc300;
  transform: scaleX(0);
  transform-origin: left center;
}
```

```js
const PCT = 0.92; // 92%
tl.to(".fill", { scaleX: PCT, duration: 1.0, ease: "power2.out" }, 0.3);
```

**环形** — 按测量描边绘制（详见 [svg-path-draw.md](svg-path-draw.md)）：

```js
const ring = document.querySelector("#ring");
const LEN = ring.getTotalLength(); // measure, don't hard-code the circumference
ring.style.strokeDasharray = LEN;
ring.style.strokeDashoffset = LEN; // empty
// rotate the <circle> -90deg in CSS so the fill starts at 12 o'clock
tl.to(ring, { strokeDashoffset: LEN * (1 - 0.92), duration: 1.1, ease: "power2.out" }, 0.3);
```

## 3 — 星级评分填充（小数）

通过灰色层上的金色层 clip 擦除，从左向右揭示至小数评分（例如 4.6 / 5）。

```html
<div class="stars">
  <div class="stars-gray">★★★★★</div>
  <div class="stars-gold" id="goldStars">★★★★★</div>
</div>
```

```css
.stars {
  position: relative;
  font-size: 64px;
  letter-spacing: 8px;
}
.stars-gray {
  color: #2b3548;
}
.stars-gold {
  position: absolute;
  inset: 0;
  color: #ffc300;
  width: 100%;
  clip-path: inset(0 100% 0 0);
}
```

```js
const RATING = 4.6,
  MAX = 5;
tl.to(
  "#goldStars",
  { clipPath: `inset(0 ${100 - (RATING / MAX) * 100}% 0 0)`, duration: 1.0, ease: "power2.out" },
  0.3,
);
```

## 如何选取数值

- **柱数量** — 4–6 根读起来像「趋势」且不杂乱；最后一根为当前/强调值。
- **填充时长** — 0.8–1.2s，与配对的数字递增对齐，使数字与图形同时落定（共用 ease）。
- **强调色** — 仅一种；柱/填充/星均用同一强调色，其余为 muted 色。
- **交错** — 柱上 0.06–0.1s；更大显得拖沓，0 则失去递进感。

## 核心原则

- **仅变换** — `scaleY` / `scaleX` / `clipPath`，勿对 `width`/`height` 补间（运行时禁止）。
- **与数字时序一致** — 填充与 count-up 应同时到达峰值（相同起点 + ease），使统计作为一拍落定，而非两拍。
- **测量，勿硬编码** — 环长用 `getTotalLength()`；硬编码周长在半径变化时会失效。
- **一种强调色、一致蓝图** — 见 `hyperframes-creative/references/data-in-motion.md`。

## 关键约束

- **时间轴暂停**；同步构建；registry key = `data-composition-id`。
- **`onUpdate`（若配对计数器）必须为 O(1)** — 运行时逐帧 seek（见 [counting-dynamic-scale.md](counting-dynamic-scale.md)）。
- **禁止 `height`/`width` 补间、禁止 `repeat: -1`** — 仅变换 + 有限重复。
- **`transform-origin`** 必须为 `bottom`（柱向上长）/ `left`（条/填充向右长）— 默认中心原点会从中间缩放，观感错误。

## 组合

- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 图形旁的数字（配对；相同 ease/时长）
- [svg-path-draw.md](svg-path-draw.md) — 进度环绘制机制

## 搭配的 HF 技能

- `/hyperframes-animation` — 时间轴 + 变换补间
- `/hyperframes-creative` — `references/data-in-motion.md`（统计布局 + 视觉重量）
- `/hyperframes-core` — 合成接线；禁止对 `width`/`height` 补间的规则
