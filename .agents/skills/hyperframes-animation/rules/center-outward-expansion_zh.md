---
name: center-outward-expansion
description: 元素从屏幕中心成簇起始，随共享 progress 值向外展开至最终位置。
metadata:
  tags: expansion, scatter, center, reveal, layout, sync, burst
---

# 由中心向外展开

元素从同一中心点出发，辐射至最终布局位置。展开可以是入场节拍本身，也可**由另一段动画的 progress 驱动**（例如数字计数增长），以实现协调运动。

## 工作原理

每个元素有 `targetX/Y`（最终布局位置）和共享的 `centerX/Y`。`progress` 值（0→1）在中心与目标之间插值每个元素：

```js
const x = centerX + (targetX - centerX) * progress;
const y = centerY + (targetY - centerY) * progress;
```

当 `progress = 0` 时，所有元素叠在中心；当 `progress = 1` 时，它们位于最终位置。

## HTML

```html
<div
  class="scene"
  data-composition-id="burst-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="burst-wrap">
    <div class="burst-item" data-target-x="-360" data-target-y="-180">{itemA}</div>
    <div class="burst-item" data-target-x="360" data-target-y="-180">{itemB}</div>
    <div class="burst-item" data-target-x="-360" data-target-y="180">{itemC}</div>
    <div class="burst-item" data-target-x="360" data-target-y="180">{itemD}</div>
    <div class="burst-item" data-target-x="0" data-target-y="-360">{itemE}</div>
    <div class="burst-item" data-target-x="0" data-target-y="360">{itemF}</div>
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
}
.burst-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
}
.burst-item {
  position: absolute;
  /* Items start at the wrap center via the absolute + 50% trick.
     We tween translate offsets via GSAP, not left/top. */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  width: {itemSize};
  height: {itemSize};
  display: grid;
  place-items: center;
  background: {itemBgColor};
  border-radius: 28px;
  font-family: {font};
  font-weight: 900;
  font-size: 96px;
  color: {textColor};
  will-change: transform;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const items = document.querySelectorAll(".burst-item");

  // Each element gets its own from→to that lerps center (translate(-50%, -50%))
  // → target offset. xPercent/yPercent bakes the self-centering; x/y animates
  // toward the target.
  items.forEach((el, i) => {
    const targetX = Number(el.dataset.targetX);
    const targetY = Number(el.dataset.targetY);
    tl.fromTo(
      el,
      { xPercent: -50, yPercent: -50, x: 0, y: 0, scale: 0.6, opacity: 0 },
      {
        x: targetX,
        y: targetY,
        scale: 1,
        opacity: 1,
        duration: EXPAND_DUR,
        ease: EXPAND_EASE,
      },
      i * STAGGER + ENTRY_AT, // stagger; ENTRY_AT offsets the burst beat
    );
  });

  window.__timelines["burst-scene"] = tl;
</script>
```

## 如何选取参数

- **ITEM_COUNT** — 爆发中的元素数量
  - 范围：3–8
  - 效果：3 = 稀疏；8 = 拥挤。> 8 会在展开中途造成卡片重叠的视觉混乱
  - 约束：数量较少时，优先更大的角度分布（目标位置相距更远）

- **EXPAND_DUR** — 每个元素从中心到目标的补间时长
  - 范围：1.0–1.8 s
  - 效果：更短 = 干脆的爆发；更长 = 向外飘浮
  - 约束：若由计数器驱动，必须与计数器时长相同（和弦）

- **EXPAND_EASE** — 所有元素共用的缓动
  - 离散选择：`power2.out`、`power3.out`、`expo.out`
  - 选择：`power3.out` 为默认 — 甩出后落定。`power2.out` 更柔和。`expo.out` 让元素戏剧性停住。避免 `in` 类缓动（会像在半空被吸回去）。
  - 约束：若由另一动画驱动，必须与驱动方缓动完全一致

- **STAGGER** — 相邻元素开始时间的间隔
  - 范围：0.04–0.08 s
  - 效果：< 0.04 = 同时和弦；> 0.08 显得拖沓 / 琶音感
  - 约束：ITEM_COUNT × STAGGER 须 < EXPAND_DUR，否则最后几个元素仍在移动而其他已落地，会显得参差

- **ENTRY_AT** — 整段爆发开始的偏移
  - 范围：0 – 0.5 s
  - 效果：> 0 在爆发前留出构图上的静息节拍

- **START_PROGRESS** — 元素起始时在中心→目标路径上的比例（用于部分已散开变体）
  - 范围：0（正中心）– 0.5
  - 效果：0 = 完全聚簇、展开戏剧性强；0.3 = 避免初始在中心堆叠

## 变体

### 同步展开（由计数器驱动）

若爆发应镜像计数动画的 progress：

```js
// Counter tween defines a state.value 0 → TARGET over COUNT_DUR
const counterState = { value: 0 };
const burstState = { p: 0 };

// Shared tween — same duration, same ease — visually a "chord"
tl.to(
  counterState,
  {
    value: COUNT_TARGET,
    duration: COUNT_DUR,
    ease: COUNT_EASE,
    onUpdate: () => (counterEl.textContent = Math.round(counterState.value).toLocaleString()),
  },
  0,
);

tl.to(
  burstState,
  {
    p: 1,
    duration: COUNT_DUR,
    ease: COUNT_EASE,
    onUpdate: () =>
      items.forEach((el) => {
        const tx = Number(el.dataset.targetX) * burstState.p;
        const ty = Number(el.dataset.targetY) * burstState.p;
        el.style.transform = `translate(-50%, -50%) translate(${tx}px, ${ty}px)`;
      }),
  },
  0,
);
```

### 从部分散开状态起始

为避免初始聚簇混乱（6+ 元素叠在中心），从 `START_PROGRESS` 开始：

```js
{ x: targetX * START_PROGRESS, y: targetY * START_PROGRESS, scale: 0.4, opacity: 0 }
```

### 落位后的 idle 微浮动

展开落定后搭配 `sine-wave-loop` — 让元素保持生动而非静止。

## 核心原则

- **驱动 vs 被驱动** — 若爆发独立存在，用逐元素 stagger；若跟随另一动画（计数器、音频节拍），共享同一 eased progress，读起来像同一节拍
- **Stagger 落在 0.04–0.08 s 区间** — 过紧则聚簇在视觉上分不开，过松则爆发显得懒
- **展开用 out 缓动** — out 缓动让元素「甩出」后落定。in 缓动像在半空被吸回
- **元素数量：3–8** — 更少显得空，更多会在中心造成展开中途卡片重叠的混乱
- **❗ 不要在爆发下方放标签当「真正标题」** — 若这样做，视线会跳到标签而忽略爆发。爆发本身就是节拍。若需要标签，用大写块字并在爆发后再揭示，且保持同一堆叠布局。

## 关键约束

- **时间轴必须 paused**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **用 translate，不用 left/top** — translate 与居中 `translate(-50%, -50%)` 技巧组合干净；改 `left`/`top` 会与居中冲突并引起像素抖动
- **爆发项上设 `will-change: transform`** — 大量同时 transform 受益于合成层提示
- **`burst-wrap` 内除子项外不要有其他 `position: absolute` 父级** — 兄弟绝对定位元素会抢走居中基线

## 组合

- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 计数峰值驱动爆发峰值（和弦）
- [sine-wave-loop.md](sine-wave-loop.md) — 爆发落定后的 idle 运动
- [card-morph-anchor.md](card-morph-anchor.md) — 从变形卡片中爆发

## 搭配的 HF 技能

- `/hyperframes-animation` — 时间轴 + stagger
- `/hyperframes-core` — 合成（composition）接线
- `/hyperframes-cli` — `hyperframes lint`
