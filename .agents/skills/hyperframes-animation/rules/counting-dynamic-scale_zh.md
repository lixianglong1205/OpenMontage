---
name: counting-dynamic-scale
description: 计数动画随数值增大而放大字号，形成逐渐加重的视觉分量。
metadata:
  tags: counter, counting, scale, font-size, number, dynamic, emphasis
---

# 动态缩放的计数动画

数字从 A 数到 B 的同时，字号同步增大，视觉分量随之抬升，强化「数值很大」的观感。

## 工作原理

单条缓动时间轴驱动 **两个同步属性**：

1. 数值（通过 `onUpdate` 渲染为 DOM 文本）
2. 字号（从 `START_SIZE` 缓动到 `END_SIZE`）

数字变大，文字也变大——视觉上传达「这很 impressive」。

## 缓动

按想要的戏剧感选择（离散选择；系数隐含）：

| GSAP ease    | 效果                                        |
| ------------ | --------------------------------------------- |
| `power1.out` | 温和 — 轻微减速                    |
| `power2.out` | 默认 — ease-out，快起慢收       |
| `power3.out` | 强烈 — 明显减速 ⭐ 推荐 |
| `expo.out`   | 非常 dramatic — 接近终点时几乎停住       |

`power3.out` 对应多项式族 `1 - (1-x)^k` 中 k ≈ 2.5 — 数字快速上冲，在峰值处明显放慢。

## HTML

```html
<div
  class="scene"
  data-composition-id="counter-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="counter-wrap">
    <span class="counter" id="counter">0</span><span class="counter-suffix">{suffix}</span>
  </div>
  <div class="counter-label">{label}</div>
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
}

.counter-wrap {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 8px;
  /* Fixed-width container prevents layout shift as digit count changes */
  width: {counterContainerWidth};
  text-align: center;
}

.counter {
  font-family: {font};
  font-weight: 900;
  color: {textColor};
  /* MANDATORY — tabular-nums keeps digits the same width */
  font-variant-numeric: tabular-nums;
  /* Initial font-size; GSAP will tween this */
  font-size: {startSize};
  letter-spacing: -2px;
  line-height: 1;
}

.counter-suffix {
  font-family: {font};
  font-weight: 800;
  color: {accentColor};
  font-size: {suffixSize};
  opacity: 0;
  transform: translateY(20px);
}

.counter-label {
  margin-top: 24px;
  font-family: {font};
  font-size: {labelSize};
  color: {mutedTextColor};
  text-align: center;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const counter = document.getElementById("counter");
  const state = { value: 0, fontSize: START_SIZE };

  // Synchronized count + font-size tween
  tl.to(
    state,
    {
      value: TARGET_VALUE,
      fontSize: END_SIZE,
      duration: COUNT_DUR,
      ease: COUNT_EASE,
      onUpdate: () => {
        counter.textContent = Math.round(state.value).toLocaleString();
        counter.style.fontSize = `${state.fontSize}px`;
      },
    },
    0,
  );

  // Suffix slides in after count completes
  tl.to(
    ".counter-suffix",
    {
      opacity: 1,
      y: 0,
      duration: SUFFIX_DUR,
      ease: `back.out(${SUFFIX_BOUNCE_FACTOR})`,
    },
    COUNT_DUR,
  );

  // Label fades in early
  tl.from(
    ".counter-label",
    {
      opacity: 0,
      y: 12,
      duration: LABEL_DUR,
      ease: "power2.out",
    },
    LABEL_AT,
  );

  window.__timelines["counter-scene"] = tl;
</script>
```

## 如何选取参数

- **TARGET_VALUE** — 计数最终停下的数值
  - 效果：2–3 位在 hero 尺寸下最好读；4 位及以上需要更宽容器
  - 约束：在 END_SIZE 下必须能水平放进容器内

- **START_SIZE / END_SIZE** — 初始与最终字号
  - 范围：START_SIZE ≈ END_SIZE 的 40–60 %
  - 效果：START_SIZE 越小增长越 dramatic；越大越 subtle
  - 约束：END_SIZE × 位数在容器宽度内不能裁切

- **COUNT_DUR** — 计数 + 缩放缓动时长
  - 范围：1.2–2.5 s
  - 效果：更短 = 更 aggressive；更长 = 更沉稳，留出阅读时间
  - 约束：需让眼睛能跟上滚过的数字；低于 ~0.8 s 会像闪一下

- **COUNT_EASE** — 数值与字号共用的 ease
  - 离散选择：`power2.out`、`power3.out`、`expo.out`（见上表）
  - 约束：避免 `back.out` / `elastic.out` —  overshoot 会像数据不稳定

- **SUFFIX_DUR** — 后缀滑入时长
  - 范围：0.3–0.6 s
  - 效果：更短 = snap；更长 = 飘入感
  - 约束：须在计数落地后触发（在 COUNT_DUR 开始），不能与计数重叠

- **SUFFIX_BOUNCE_FACTOR** — 后缀入场 `back.out` 系数
  - 范围：1.4–2.0
  - 效果：1.4 = 小幅 overshoot；2.0 = 更 bouncy

- **LABEL_AT / LABEL_DUR** — 标签何时、多久淡入
  - 范围：LABEL_AT < COUNT_DUR / 2（标签在计数到顶前出现）；LABEL_DUR 0.4–0.7 s

## 变体

### 直接 tween `innerText`（无代理对象）

GSAP 检查器直接读 `innerText`，纯数字计数可省略 `state` 代理：

```js
tl.to(
  counter,
  { innerText: TARGET_VALUE, duration: COUNT_DUR, ease: COUNT_EASE, snap: { innerText: 1 } },
  0,
);
```

`snap: { innerText: 1 }` 保持整数。只要必须在同一条 tween 里 **协同驱动** 字号、区域格式（`toLocaleString`）或后缀，仍用上文代理 + `onUpdate` 形式 — 单靠 `innerText` 做不到，而动态缩放正是本规则要点，故代理形式为默认。

### 3D 纵深入场

与 `translateZ` 组合，做视差式纵深入场：

```js
tl.from(
  ".counter",
  {
    z: -300,
    duration: 0.6,
    ease: "power2.out",
    // requires parent or .counter itself to have perspective set
  },
  0,
);
```

CSS 前提：

```css
.counter-wrap {
  perspective: 1000px;
}
.counter {
  transform-style: preserve-3d;
}
```

### 多指标协调揭示

3 个指标并行计数时，共用 **相同** ease 与 duration，同时结束 — 视觉上是和弦而非琶音。每个指标通常还需 **配对图形**（条 / 环 / 星形）— 不要只停在数字；见 [stat-bars-and-fills.md](stat-bars-and-fills.md)：

```js
["#stat1", "#stat2", "#stat3"].forEach((sel, i) => {
  const obj = { v: 0 };
  tl.to(
    obj,
    {
      v: TARGETS[i],
      duration: COUNT_DUR,
      ease: COUNT_EASE,
      onUpdate: () => (document.querySelector(sel).textContent = Math.round(obj.v)),
    },
    0,
  ); // same start position — chord
});
```

## 核心原则

- **数值与字号在同一条 tween 中同步**，共用 ease，保持协调
- **`font-variant-numeric: tabular-nums` 为必选项** — 否则位数变化（如 9 → 10 → 100）会因字形宽度变化产生可见抖动
- **固定宽度容器** 作双保险 — 即使有 tabular-nums，字形变化仍可能牵动基线
- **原地放大，不要 bounce** — 数字应显得有分量，而非弹簧感。`power3.out` 精确停在终值；`back.out` overshoot 显得卡通
- **起始足够小以便明显增长**（约终值的 ~50 %）；终值足够大以 decisive，但不裁切视口
- **后缀在计数之后动，而非计数过程中** — 给数字单独一拍
- **❗ 标签是大字，不是页面式小脚注** — 在 VIDEO 里，hero 数字下方小段落式 caption 像视觉噪声。用 display 级、大写、加字距的标签，布局是「两行大字」；标签是标题的一部分，不是页脚。

## 关键约束

- **`tabular-nums` 必选** — 布局稳定所需 CSS
- **时间轴必须 paused**：`gsap.timeline({ paused: true })`。禁止 `tl.play()`
- **注册键 = `data-composition-id`**：`window.__timelines["counter-scene"]` 须与 scene 根一致
- **`onUpdate` 改 DOM**：HF 运行时逐帧 seek 时间轴，每次 seek 都会跑 `onUpdate`。保持 `onUpdate` 为 O(1) — 只设文本 + 字号，不创建 DOM
- **用 `Math.round` 而非 `Math.floor`** — 到达最终整数一半时应短暂显示终值，而非前一个整数
- **计数本身避免 `back.out` / `elastic.out`** — overshoot 让数字像不稳定数据（是数据，不是装饰）

## 组合用法

- [stat-bars-and-fills.md](stat-bars-and-fills.md) — **数字旁的配对图形**（增长条 / 进度环 / 星形 wipe）。统计场景通常是两条规则：本条的 count-up + 那边的 fill。fill 用相同 ease 与 duration，数字与图形同一拍落地。
- [svg-path-draw.md](svg-path-draw.md) — 数字周围图标路径绘制
- [center-outward-expansion.md](center-outward-expansion.md) — 相关图标在计数峰值向外爆开

## 搭配的 HF 技能

- `/hyperframes-animation` — 时间轴 + `onUpdate` API
- `/hyperframes-core` — composition 接线、`data-*` 属性
- `/hyperframes-cli` — `hyperframes lint` 校验 scene
