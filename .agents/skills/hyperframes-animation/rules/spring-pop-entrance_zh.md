---
name: spring-pop-entrance
description: 标准入场弹出——元素（或交错成组）以缩放 0 → 1 到达，采用平滑长尾 settle（默认 power3）；弹跳式 overshoot 是罕见、需明确表达的趣味例外。使用 fromTo，以便在 seek 下 t=0 时状态正确。
metadata:
  tags: spring, entrance, pop, scale, power3, settle, stagger, reveal, arrival
---

# Spring-Pop 入场

> **平滑优于弹跳。** 按动效原则（`references/motion-language.md`），本入场**默认采用平滑长尾 settle — `power3.out`（或 `expo.out` 以更快到达）**，干净减速至静止尺寸，**无 overshoot**。弹跳的 `back.out` overshoot 是 agent 制作视频里**头号 instant turn-off**，几乎从未做好；在此降为**罕见、需明确表达的趣味例外**（消费/趣味品牌），绝非默认。不确定时，平滑 settle。

THE 入场原语：元素（或交错成组）从无到有弹入画面 — `scale: 0 → 1`，可选小幅 `y` 上升 —  riding **平滑长尾 ease（默认 `power3.out`）**，自信地长到静止尺寸并 settle 而不弹跳。这是**到达（arrival）**，不是反应。

与 [press-release-spring.md](press-release-spring.md) 明确区分：该规则是点击/按压 → 释放反馈链（按压阶段，再 spring 回 `1.0`）。本规则**无按压阶段** — 没有先前静止状态，元素此前不在画面上，它弹入存在。许多 blueprint 曾借 `press-release-spring` 伪造入场；应改用本规则。

## 工作原理

单个 `fromTo` 承载整个到达：

1. **起始状态**：`{ scale: 0, opacity: 0 }` — 元素缩成一点且不可见。在 `from` 对象中显式声明，使 seek 到 `t=0` 时落在此确切状态（勿依赖 CSS 隐藏起始 — 见关键约束）。
2. **目标状态（默认）**：`{ scale: 1, opacity: 1, ease: "power3.out" }` — 长尾减速，将元素长到静止尺寸并**平滑 settle，无 overshoot**。需要更猛、前段更快的到达时用 `expo.out`（仍无弹跳）。此平滑 settle 是 house style；弹跳 `back.out` 变体是罕见趣味例外（见变体）。

对**成组**，同一 `fromTo` 按元素运行，**确定性、由 index 推导的 stagger**（`i * STAGGER`），且总入场窗口**有上限**（`ITEM_COUNT × STAGGER ≤ ~0.5s`），使整组读作一次到达节拍，而非慢速琶音。

小幅 `y` 上升（`y: 24 → 0`）在 pop 之上叠加 subtle「抬入位」 — 可选点缀；**平滑 ease 上的 `scale` 生长**才是承重动效。（`rotation` settle 仅属于下方 playful overshoot 变体。）

## HTML

```html
<!-- Single hero pop -->
<div
  class="scene"
  data-composition-id="pop-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="pop-hero" id="hero">{heroLabel}</div>
</div>

<!-- Staggered group: nodes / cards / icons / pills / callouts -->
<div
  class="scene"
  data-composition-id="pop-group-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="pop-grid">
    <div class="pop-item">{itemA}</div>
    <div class="pop-item">{itemB}</div>
    <div class="pop-item">{itemC}</div>
    <div class="pop-item">{itemD}</div>
    <div class="pop-item">{itemE}</div>
    <div class="pop-item">{itemF}</div>
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
.pop-hero {
  display: grid;
  place-items: center;
  width: {heroSize};
  height: {heroSize};
  background: {heroBg};
  border-radius: HERO_RADIUS;
  font-family: {font};
  font-weight: 900;
  font-size: HERO_FONT_SIZE;
  color: {heroTextColor};
  /* Pop scales around the center — see Critical Constraints */
  transform-origin: 50% 50%;
  will-change: transform;
}
.pop-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: GRID_GAP;
  place-items: center;
}
.pop-item {
  display: grid;
  place-items: center;
  width: {itemSize};
  height: {itemSize};
  background: {itemBg};
  border-radius: ITEM_RADIUS;
  font-family: {font};
  font-weight: 800;
  font-size: ITEM_FONT_SIZE;
  color: {itemTextColor};
  transform-origin: 50% 50%;
  will-change: transform;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // --- Single hero pop (default: smooth long-tail settle, no overshoot) ---
  // fromTo states the collapsed start explicitly so the hero is correct at t=0
  // under seek. power3.out grows scale into 1.0 and decelerates smoothly.
  tl.fromTo(
    "#hero",
    { scale: 0, opacity: 0 },
    {
      scale: 1,
      opacity: 1,
      duration: POP_DUR,
      ease: "power3.out", // smooth beats bouncy; expo.out for a punchier front
    },
    ENTRY_AT,
  );

  // --- Staggered group pop ---
  // Deterministic, index-derived stagger (no Math.random). The cap keeps the
  // whole group inside one arriving beat: ITEM_COUNT * STAGGER <= ~0.5s.
  const items = gsap.utils.toArray(".pop-item");
  items.forEach((el, i) => {
    tl.fromTo(
      el,
      { scale: 0, opacity: 0, y: Y_RISE },
      {
        scale: 1,
        opacity: 1,
        y: 0,
        duration: POP_DUR,
        ease: "power3.out",
      },
      GROUP_ENTRY_AT + i * STAGGER,
    );
  });

  window.__timelines["pop-scene"] = tl;
</script>
```

## 变体

### 平静 settle（精致 / 企业 /「premium calm」）— 默认

`power3.out`，无 rotation，去掉 `y` 上升或保持很小（~12px）。读作自信、有重量的 settle — 适合 hero wordmark 或单个产品镜头落地。premium / 企业品牌的稳妥默认。

### 坚实 settle（默认产品 reveal）— 默认

日常入场。`power3.out`（或 `expo.out` 更猛前段），可选 `Y_RISE` ~24px。清晰、 deliberate 到达并干净减速 — 卡片、图标、callout 的稳妥默认。**无 overshoot。**

### 弹跳 pop（罕见 — 仅明确趣味）

例外，非默认。**仅**在 deliberately playful 语域（消费/趣味品牌、玩具感图标集）且 bounce 明显是意图时 — 绝不用在产品/企业/严肃发布调性。弹跳是 #1 turn-off，agent 很少做好，故 knowingly 且 sparingly 使用。将 `power3.out` 换为 `back.out(OVERSHOOT)`，（可选）加 `rotation` settle，使各元素像手放到位：

```js
// Playful exception only — default to power3.out (see above).
tl.fromTo(
  el,
  { scale: 0, opacity: 0, rotation: ROT_FROM },
  { scale: 1, opacity: 1, rotation: 0, duration: POP_DUR, ease: `back.out(${OVERSHOOT})` },
  GROUP_ENTRY_AT + i * STAGGER,
);
```

即使在此也保持 `OVERSHOOT` modest（≤ ~2）— 超过则读作卡通 wobble，而非到达。

### 锚点 origin pop（callout 从指针/源点弹出）

当 callout 应从特定点长出（如站点标记或指针尖），将 `transform-origin` 设于该点而非中心，使 `scale: 0 → 1` 读作「从源点涌现」而非「原地充气」。

```css
.callout {
  transform-origin: 0% 100%; /* bottom-left = pointer tip; match to the anchor */
}
```

### Pop 入 held slot — 然后 hold（至多 jitter）

当 pop 出的元素随后**占据** ongoing slot（星座节点、持久 badge），**勿**在本入场中 bake idle loop — 必须保持有限。完成 pop 后静止 hold；若 held 帧确需生气，交给 [sine-wave-loop.md](sine-wave-loop.md) 在**单独、更晚**的 tween 上做 **subtle jitter**（低振幅）— 不是 breathing loop。优先在 VO cue 上 reveal 下一元素，而非让本元素一直动。

## 如何选取数值

- **EASE** — settle 曲线（承重决策）
  - 默认：**`power3.out`** — 平滑长尾 settle，无 overshoot；产品/企业/严肃调性的 house style。需要更猛、前段更快到达用 `expo.out`（仍平滑）。
  - 仅 playful 例外：`back.out(OVERSHOOT)` — 见 Bouncy pop 变体；仅当 bounce 明显是品牌意图时使用。

- **OVERSHOOT** — `back.out(OVERSHOOT)` overshoot 强度 — **仅用于罕见弹跳变体**；平滑默认无 overshoot 旋钮
  - 范围（仅 playful）：~1.3（ barely）→ ~2.0（明显弹跳）
  - 约束：保持 ≤ ~2 — 超过则 overshoot 超出元素边界，读作卡通 wobble 而非到达。若非 explicitly-playful，勿用 — 用 `power3.out`。

- **POP_DUR** — 每个元素 `scale: 0 → 1` tween 的时长
  - 范围：0.4 – 0.7 s
  - 效果：更短 = 紧 snap；更长 = 更松、更 floating 的 pop
  - 约束：主体须在 **`t ≤ 0.5s`** 可见 — 保持 `ENTRY_AT + POP_DUR` 的可读中点靠前；勿让 hero 在半秒后才完成到达

- **STAGGER** —  successive 项起始间隔（仅成组）
  - 范围：0.04 – 0.08 s
  - 效果：< 0.04 读作同时和弦；> 0.08 感觉 lazy / 琶音化
  - 约束：**`ITEM_COUNT × STAGGER ≤ ~0.5s`**（上限）— 超过则整组不再读作一拍。大组 cap 每项 stagger：`STAGGER = min(0.06, 0.5 / ITEM_COUNT)`

- **ITEM_COUNT** — 组 pop 元素数量
  - 范围：3 – 9
  - 效果：3 = 稀疏；9 = 满 grid。超过 ~9 会迫使 `STAGGER` 过小以致 stagger 消失 — 改用 wipe/sweep reveal

- **Y_RISE** — 可选向上偏移（`y: Y_RISE → 0`）
  - 范围：0（纯 pop）– 32 px
  - 效果：subtle「抬入位」；保持小，使 `scale` pop 仍 dominant
  - 约束：calm-settle 变体为 0；勿大到读作 slide-up（那是另一原语）

- **ROT_FROM** — 可选起始 rotation，**仅 playful（弹跳）变体**（`rotation: ROT_FROM → 0`）
  - 范围：−10° – +10°
  - 效果：小幅倾斜 resolve 使元素像手放
  - 约束：若要交替 tilt，从 index 确定性推导符号/大小（如 `i % 2 ? 6 : -6`）— 勿 `Math.random`

- **ENTRY_AT / GROUP_ENTRY_AT** —（组）pop 开始前的时间线偏移
  - 范围：0 – 0.4 s
  - 效果：> 0 在到达前留 quiet beat；保持小，使主体仍在 `t ≤ 0.5s` 落地

### 几何与 token

- **{heroSize} / {itemSize}** —  footprint。hero 入场应占画面清晰可读比例；组项缩小以使 grid 在 `GRID_GAP` 呼吸空间内 fit。
- **HERO_RADIUS / ITEM_RADIUS** — `height × 0.15`（尖）→ `height / 2`（pill）。
- **{heroBg} / {itemBg} / {\*TextColor}** — 表面 + 标签 token；继承 composition 调色板。

## 关键原则

- **平滑优于弹跳** — 默认 `power3.out`（或 `expo.out`）：长尾 settle 至 `scale: 1`，无 overshoot。弹跳 `back.out` 是罕见、需明确表达的趣味例外（#1 turn-off，agent 很少做好）。不确定时，平滑 settle。
- **始终 fromTo** —  collapsed `{ scale: 0, opacity: 0 }` 起始写在 `from` 中，seek 到 `t=0` 精确落位。基于 CSS 隐藏起始的入场（如 CSS `opacity:0` + `.to()`）在 HF seek 下 flicker — tween 认领前元素已可见渲染。
- **Easing 承载动效，非 keyframes** — 让 ease 免费产生 settle。勿手 key `scale: 1.1` 中间态；那会 double-bounce 并与曲线打架。（playful 变体中，overshoot 是 `back.out` 副产品，非手 key bounce。）
- **生长即动效** — `scale` 承重；`y` 上升（playful 变体中的 `rotation` settle）是叠在上面的点缀。若只留 `scale` 生长，仍应读作干净入场。
- **Cap stagger 窗口** — 整组须在 ~0.5s 内到达，否则不再读作一拍而像慢列表 reveal。从 `ITEM_COUNT` 推导 stagger 以自 cap。
- **按 index 确定性** — 所有 stagger 及 rotation/tilt 变化来自 loop index，never `Math.random` — 渲染器每次 seek 必须产出相同帧。
- **尽早可见** — 主体须在 `t ≤ 0.5s` 上屏。`t=1s` 才完成到达的 hero 浪费开场 beat。
- **勿在此 bake idle loop** — 本入场有限。若元素随后 hold slot，在更晚 tween 交给 `sine-wave-loop`；此处的 infinite `repeat`/`yoyo` 破坏 seek。

## 关键约束

- **时间线必须 paused**：`gsap.timeline({ paused: true })`
- **Registry key = `data-composition-id`**
- **入场用 `fromTo`** — 显式 `{ scale: 0, opacity: 0 }` from 状态；勿依赖 CSS 隐藏起始
- **pop 元素上无 CSS `transition`** — 那些独立于 HF seek 插值并导致 flicker
- **无 `repeat` / `yoyo` / infinite tween** — 有限到达；idle 动效是单独的 `sine-wave-loop` tween
- **无 `Math.random` / `Date.now`** — stagger 与 tilt 由 index 推导且确定性
- **仅 GSAP transform 别名**：`x`, `y`, `scale`, `rotation`。勿 tween `width` / `height` / `left` / `top`
- **原位 pop 用 `transform-origin: 50% 50%`**（默认）；仅 origin-anchored 变体设于源点
- **默认 ease `power3.out`**（平滑，无 overshoot）；`back.out(OVERSHOOT)` 仅 explicitly-playful 变体，且 **`OVERSHOOT ≤ ~2`** — 超过读作卡通 wobble 而非到达
- **`ITEM_COUNT × STAGGER ≤ ~0.5s`** — 整组须在一拍内落地
- pop 元素上 **`will-change: transform`**，尤其成组 — 多路同时 spring tween 受益于 compositor hint

## 组合

- [sine-wave-loop.md](sine-wave-loop.md) — pop 落地后，held 节点/badge 上**至多 subtle jitter**（勿在入场中 bake 任何 loop；优先 VO 定时 reveal 而非 ambient 动效 — 见该规则 caution）
- [center-outward-expansion.md](center-outward-expansion.md) — 元素从中心 pop 入并辐射至 slot
- [press-release-spring.md](press-release-spring.md) — 反应对应：pop 入后，按钮可走 press→release；本规则供到达，该规则供点击反馈

## 与 HF skills 搭配

- `/hyperframes-animation` — `power3.out` settle（平滑默认）、`fromTo` 入场、确定性 stagger
- `/hyperframes-core` — composition 接线
- `/hyperframes-cli` — `hyperframes lint`
