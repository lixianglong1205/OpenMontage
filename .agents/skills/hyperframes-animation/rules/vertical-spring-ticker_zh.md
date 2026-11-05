---
name: vertical-spring-ticker
description: 在带遮罩的容器内用叠加式 spring 物理实现老虎机式垂直滚动——每个 spring 贡献一次「步进」位移。
metadata:
  tags: text, ticker, spring, scroll, vertical, slot-machine, sequence
---

# 垂直 Spring Ticker（老虎机）

多个 spring 补间**叠加**得到总 Y 向平移。每个 spring 贡献一个离散的「步进」。组合运动呈现干脆的分段位移与自然 settling——而非单次线性滚动，你会得到老虎机「咔、咔、咔」的节奏。

## 工作原理

容器固定高度 `ITEM_HEIGHT`，`overflow: hidden`。内部是垂直堆叠的条目，每条也是 `ITEM_HEIGHT` 高。内层堆栈的 translate 计算为：

```
translateY = -ITEM_HEIGHT * sum(spring_i.progress for each spring)
```

每个 spring 在不同时刻触发、settle，再触发下一个。求和后堆栈逐步向前「咔哒」推进。`spring` 缓动让每一步带有轻微 overshoot/settle，与线性跑马灯区分开。

## HTML

```html
<div
  class="scene"
  id="ticker-scene"
  data-composition-id="ticker-scene"
  data-start="0"
  data-duration="5"
  data-track-index="0"
>
  <div class="stack">
    <div class="eyebrow">{eyebrow}</div>
    <div class="ticker" id="ticker">
      <div class="stack-inner" id="stack-inner">
        <!-- One .item per state the ticker rolls through.
             The example file lists concrete labels; for the rule, treat
             these as positional slots ({item0} … {itemN}). -->
        <div class="item">{item0}</div>
        <div class="item">{item1}</div>
        <div class="item">{item2}</div>
        <div class="item">{item3}</div>
        <div class="item">{itemN}</div>
      </div>
    </div>
    <div class="brand">{footerLine}</div>
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
  background: {bgColor};
  font-family: {font};
}
.stack {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: STACK_GAP;
}
.eyebrow {
  font-size: EYEBROW_FONT_SIZE;
  font-weight: 800;
  letter-spacing: 14px;
  text-transform: uppercase;
  color: {accentColor};
}
/* MANDATORY: container height matches the per-item height exactly */
.ticker {
  width: TICKER_WIDTH;
  height: ITEM_HEIGHT;       /* MUST match .item height */
  overflow: hidden;
  border-top: 2px solid {dividerColor};
  border-bottom: 2px solid {dividerColor};
  position: relative;
}
.stack-inner {
  display: flex;
  flex-direction: column;    /* MANDATORY for vertical ticker */
  will-change: transform;
}
.item {
  height: ITEM_HEIGHT;       /* MUST equal .ticker height */
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: ITEM_FONT_SIZE;
  font-weight: 900;
  letter-spacing: 8px;
  text-transform: uppercase;
  color: {textColor};
  /* font-variant-numeric: tabular-nums; — for numeric tickers */
}
.brand {
  font-size: BRAND_FONT_SIZE;
  font-weight: 800;
  letter-spacing: 10px;
  color: {accentColor};
  text-transform: uppercase;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const innerEl = document.getElementById("stack-inner");

  // Each spring object holds a 0→1 progress; they accumulate to a step-counter.
  // Sum * -ITEM_HEIGHT becomes translateY.
  const springs = Array.from({ length: STEPS }, () => ({ p: 0 }));

  function applyTransform() {
    const sumP = springs.reduce((acc, s) => acc + s.p, 0);
    innerEl.style.transform = `translateY(${-sumP * ITEM_HEIGHT}px)`;
  }
  applyTransform(); // initial state

  // Fire each spring sequentially with overlap — each one snaps in one step
  springs.forEach((spring, i) => {
    tl.to(
      spring,
      {
        p: 1,
        duration: STEP_DUR,
        ease: `back.out(${BOUNCE_FACTOR})`,
        onUpdate: applyTransform,
      },
      STEP_START + i * STEP_SPACING,
    );
  });

  // Footer reveals after the ticker settles on the final item.
  tl.from(
    ".brand",
    { opacity: 0, y: BRAND_Y, duration: BRAND_FADE_DUR, ease: "power3.out" },
    STEP_START + STEPS * STEP_SPACING + BRAND_DELAY,
  );

  window.__timelines["ticker-scene"] = tl;
</script>
```

## 如何选取参数

- **ITEM_HEIGHT** — 每个 ticker 槽位与遮罩窗口的 px 高度。
  - 范围：约 `ITEM_FONT_SIZE × 1.25`；行高需容纳大写 descender 且不被裁切
  - 约束：**`.ticker` 高度必须与 `.item` 高度完全一致**——不一致会导致条目在遮罩上下露出部分
  - 参考：../../examples/proof-logo-chain.html 使用 `204px`
- **TICKER_WIDTH** — 遮罩窗口的 px 宽度。
  - 范围：足够容纳最长条目、无需省略号；通常为视口宽度的 30–60%
- **STEPS** — 叠加 spring 的数量（状态切换次数，不是条目总数）。
  - 范围：通常 1–4；每一步对应老虎机节奏中的一次「咔哒」
  - 约束：`STEPS ≤ itemCount − 1`（最多只能滚到当前可见条目下方还有的条目数）
  - 参考：../../examples/proof-logo-chain.html 使用 `1`（两态之间单次滚动）
- **STEP_DUR** — 每个 spring 补间的时长。
  - 范围：0.3–0.7s；低于 0.3 overshoot 几乎看不见，高于 0.7 则「咔哒」像滑动
  - 参考：../../examples/proof-logo-chain.html 使用 `0.45s`
- **STEP_SPACING** — 相邻 spring 开始时间间隔（秒）。
  - 范围：0.3–0.5s；过近则步骤糊成一体（像线性滚动），过远则 ticker 显得拖沓
  - 约束：`STEP_SPACING ≤ STEP_DUR`，使上一步仍在 settling 时下一步已触发（这才形成「叠加」）
- **STEP_START** — 第一个 spring 触发时刻。
  - 范围：0 及以上；可排在任意前置节拍之后
- **BOUNCE_FACTOR** — 每步 `back.out(BOUNCE_FACTOR)` 的 overshoot 强度。
  - 范围：1.4（轻柔咔哒）→ 2.0（有力咔哒）→ 2.5+（高潮步的卡通式 spin-and-land）
  - 效果：偏低像精致 UI，偏高像赌场 / 游戏节目
- **BRAND_DELAY** — 最后一步之后、页脚行出现前的间隔（秒）。
  - 范围：0.2–0.5s；让最后 overshoot settle 后再让下一元素抢注意力
- **BRAND_FADE_DUR** — 页脚淡入时长。
  - 范围：0.4–0.7s
- **BRAND_Y** — 页脚淡入前初始垂直偏移（px）。
  - 范围：8–24 px；更大像「砸入」，更小更柔和
- **EYEBROW_FONT_SIZE / ITEM_FONT_SIZE / BRAND_FONT_SIZE / STACK_GAP** — 排版与布局缩放。
  - 约束：条目是视觉焦点，约为 eyebrow/页脚的 4–8 倍
- **{bgColor} / {accentColor} / {textColor} / {dividerColor}** — 语义色 token；accent 留给 eyebrow 与页脚，ticker 条目保持中性。
- **{font}** — 基础字体栈。数字 ticker 可加 `font-variant-numeric: tabular-nums` 保持数字等宽。

## 变体

### 数字 ticker（价格 / 计数滚动）

用数字序列替换文本条目，对小数各位（个、十、百……）使用相同 spring 步进模式。加 `font-variant-numeric: tabular-nums` 稳定数字宽度。

### 反向（倒计时）

交换 translate 符号：`transform: translateY(${sumP * ITEM_HEIGHT}px)`，并按反序排列条目。读起来像倒计时。

### 连续无限 ticker（无 settling）

永久循环（如新闻 ticker）——在单条长补间上用 linear ease，复制条目列表，平移超过总高度时重置。**不属于本规则**——连续运动见 [sine-wave-loop](sine-wave-loop.md)，与本规则的离散步进语义不同。

### 组间停顿

营造「先转后停」：多步快速 spring（`STEP_SPACING` 小）+ 较长类 `BRAND_DELAY` 停顿 + 最后一步更大 `BOUNCE_FACTOR`。停顿是让视线锁定的时刻。

## 核心原则

- **容器高度必须等于条目高度**——否则条目无法干净对齐可见窗口。容器 200px、条目 220px 时，每步都会在上下露出条目边缘。
- **在容器上 `overflow: hidden`，不在内层 stack 上**——遮罩是窗口；内部 stack 可向下延伸。
- **内层 stack 使用 `flex-direction: column`**——垂直堆叠必需；row 会变成横向。
- **步进间隔小于步进时长**——重叠使 spring 叠加并产生「咔、咔」节奏；不重叠则像线性滚动。
- **每步 `back.out`**——overshoot 让每步像一次「咔哒」。linear 或仅 out 的 ease 会失去老虎机感。
- **在 onUpdate 中求和 spring，不要直接 tween 最终位置**——这是「叠加」技巧；每个 spring 贡献自己的 snap，形成老虎机 pacing。
- **❗ 不要在步进之间用 `innerHTML` 换条目**——ticker 通过 translate 移动**同一批**条目；替换内容会让旧条目在新内容出现时仍可见（illusion 破坏）。
- **❗ 最后一步后高潮停留 ≥1s**——见 SKILL 通用约束。

## 关键约束

- **Timeline 必须 paused**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **stack-inner 上不要用 CSS `transition`**——会与叠加 transform 冲突
- **stack-inner 上 `will-change: transform`**——每秒多次小 transform 更新
- **所有条目同高（像素级一致）**——高度不一导致累计漂移
- **数字场景：`font-variant-numeric: tabular-nums`**——可变数字宽度会破坏对齐

## 组合

- [reactive-displacement.md](reactive-displacement.md) — ticker 被 incoming 元素「推」动
- [scale-swap-transition.md](scale-swap-transition.md) — ticker 停在终态后 scale out，放大字幕替换
- [press-release-spring.md](press-release-spring.md) — 按钮 press 触发 ticker 旋转

## 搭配的 HF skills

- `/hyperframes-animation` — 通过共享 onUpdate 的叠加 spring 补间
- `/hyperframes-core` — composition 接线
- `/hyperframes-cli` — `hyperframes lint`
