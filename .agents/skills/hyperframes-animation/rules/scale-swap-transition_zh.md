---
name: scale-swap-transition
description: 两个元素之间协调的缩小退出与弹簧弹入、类 morph 的过渡效果——无需 SVG 路径插值。
metadata:
  tags: transition, morph, scale, swap, spring, pop
---

# 缩放交换过渡

通过在退出与入场缩放动画上叠加，模拟两个 DOM 元素之间的「morph」效果。比 [card-morph-anchor](card-morph-anchor.md)（对容器尺寸做 morph）更轻量，也比分 SVG 路径插值更简单。

## 工作原理

在同一触发时刻，启动两条协调的 tween：

1. **Outgoing 元素**：scale `1.0 → EXIT_SCALE` + opacity `1 → 0`（快速的 `power2.in`）
2. **Incoming 元素**：scale `EXIT_SCALE → 1.0` + opacity `0 → 1`（带 overshoot 的弹性 `back.out(${BOUNCE_FACTOR})`）

在两者都处于 tween 中途的一小段 `OVERLAP` 窗口内，会形成「morph」的错觉。Incoming 通过 z-index 置于上层，避免 outgoing 淡出尾迹透出。

## HTML

```html
<div
  class="scene"
  id="swap-scene"
  data-composition-id="swap-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="stack">
    <div class="swap-wrap">
      <div class="card outgoing" id="outgoing">
        <div class="icon">{outgoingIcon}</div>
        <div class="title">{outgoingLabel}</div>
      </div>
      <div class="card incoming" id="incoming">
        <div class="icon">{incomingIcon}</div>
        <div class="title">{incomingLabel}</div>
        <div class="sub" id="sub">{incomingSubline}</div>
      </div>
    </div>
    <div class="brand">{Brand}</div>
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
}
.stack {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: STACK_GAP;
}
.swap-wrap {
  position: relative;
  width: SWAP_WRAP_W;
  height: SWAP_WRAP_H;
}
.card {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: CARD_INNER_GAP;
  border-radius: CARD_RADIUS;
  padding: CARD_PADDING;
  /* Both elements share transform-origin so they "morph" around the same anchor */
  transform-origin: 50% 50%;
  will-change: transform, opacity;
}
.card .icon {
  font-size: ICON_SIZE;
}
.card .title {
  font-size: TITLE_SIZE;
  font-weight: 900;
  letter-spacing: TITLE_TRACKING;
  text-transform: uppercase;
}
.card .sub {
  font-size: SUB_SIZE;
  font-weight: 700;
  color: {accentColor};
  opacity: 0;
}
.outgoing {
  z-index: 1;
  background: {outgoingBg};
  border: 1px solid {outgoingBorder};
  color: {textColor};
}
.incoming {
  /* Incoming starts hidden + smaller, will pop in */
  z-index: 2;
  background: {incomingBg};
  border: 1px solid {incomingBorder};
  color: {textColor};
  opacity: 0;
  transform: scale(EXIT_SCALE);
}
.brand {
  font-size: BRAND_SIZE;
  font-weight: 900;
  letter-spacing: BRAND_TRACKING;
  text-transform: uppercase;
  color: {brandColor};
}
```

## GSAP 时间轴

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Outgoing: shrink + fade fast
  tl.to(
    "#outgoing",
    {
      scale: EXIT_SCALE,
      opacity: 0,
      duration: EXIT_DUR,
      ease: "power2.in",
    },
    TRIGGER,
  );

  // Incoming: scale up + fade in with overshoot, starts slightly BEFORE outgoing
  // finishes (OVERLAP creates the morph illusion).
  tl.to(
    "#incoming",
    {
      scale: 1.0,
      opacity: 1,
      duration: ENTER_DUR,
      ease: `back.out(${BOUNCE_FACTOR})`,
    },
    TRIGGER + EXIT_DUR - OVERLAP,
  );

  // Subline reveals AFTER the incoming card settles
  tl.fromTo(
    "#sub",
    { opacity: 0, y: SUB_REVEAL_Y_PX },
    { opacity: 1, y: 0, duration: SUB_REVEAL_DUR, ease: "power3.out" },
    TRIGGER + EXIT_DUR + SUB_REVEAL_DELAY,
  );

  // Brand fades in early for context
  tl.from(
    ".brand",
    { opacity: 0, y: BRAND_REVEAL_Y_PX, duration: BRAND_REVEAL_DUR, ease: "power3.out" },
    BRAND_REVEAL_AT,
  );

  window.__timelines["swap-scene"] = tl;
</script>
```

## 变体

### 延迟的内层内容揭示

经典模式：先 morph 容器，待容器稳定后再揭示内层文字（如上例中的 `.sub`）。morph 结束与内容揭示之间约 0.2–0.4 s 的间隔，让观众视线先落在新容器形状上，再阅读内容。

### 三重交换（三态循环）

链式：A→B→C，使用两个触发点 `TRIGGER_AB` 与 `TRIGGER_BC`。每次过渡需要各自一对 tween，上一轮的 incoming 成为下一轮的 outgoing。适用于状态演进叙事（例如 early-state → mid-state → final-state 标签）。

```js
tl.to("#stateA", { scale: EXIT_SCALE, opacity: 0, duration: EXIT_DUR }, TRIGGER_AB);
tl.to(
  "#stateB",
  { scale: 1.0, opacity: 1, duration: ENTER_DUR, ease: `back.out(${BOUNCE_FACTOR})` },
  TRIGGER_AB + EXIT_DUR - OVERLAP,
);
tl.to("#stateB", { scale: EXIT_SCALE, opacity: 0, duration: EXIT_DUR }, TRIGGER_BC);
tl.to(
  "#stateC",
  { scale: 1.0, opacity: 1, duration: ENTER_DUR, ease: `back.out(${BOUNCE_FACTOR})` },
  TRIGGER_BC + EXIT_DUR - OVERLAP,
);
```

### 颜色变化过渡（无缩放）

若要在两个同形状状态之间做扁平 morph，可去掉缩放，仅保留 opacity 与短暂的背景色相 tween。戏剧感较弱，但更贴近产品 UI 气质。

## 如何选取数值

### 时间（秒）

- **TRIGGER** — 交换触发的时刻。
  - 约束：须 ≥ outgoing 元素落定时间 + 一段停留，使 outgoing 在变形前已「落地」
- **EXIT_DUR** — outgoing 缩小与淡出时长。
  - 范围：0.3–0.5 s
- **ENTER_DUR** — incoming 弹入时长。
  - 范围：0.45–0.7 s（长于 `EXIT_DUR`，以便 overshoot 落定）
- **OVERLAP** — 入场比退场提前开始的重叠量。
  - 范围：0.1–0.2 s
  - 约束：过大（>0.3 s）时两者同时清晰可见（失去 morph 感）；过小（<0.05 s）会出现明显空档
- **SUB_REVEAL_DELAY** — incoming 落定与副标题揭示之间的间隔。
  - 范围：0.2–0.4 s；在 morph 期间揭示会与交换争抢注意力
- **SUB_REVEAL_DUR** — 副标题淡入时长。
  - 范围：0.3–0.5 s
- **BRAND_REVEAL_AT** — 品牌/上下文行淡入时刻。
  - 约束：须 < `TRIGGER`（品牌为交换提供上下文，而非与交换同步）
- **BRAND_REVEAL_DUR** — 品牌淡入时长。
  - 范围：0.4–0.8 s

### 物理参数

- **EXIT_SCALE** — outgoing 的目标缩放（也是 incoming 的起始缩放）。
  - 范围：0.6–0.8；缩得更小更戏剧，但易被读成「消失」而非「morph」
- **BOUNCE_FACTOR** — incoming 上 `back.out(${BOUNCE_FACTOR})` 的 overshoot。
  - 范围：1.4（柔和）– 1.8（坚实）– 2.2（卡通感）

### 位置偏移

- **SUB_REVEAL_Y_PX** — 副标题初始 y 偏移（正数 = 在静止位置下方）。
  - 范围：8–20 px
- **BRAND_REVEAL_Y_PX** — 品牌行初始 y 偏移。
  - 范围：10–24 px

### 布局

- **STACK_GAP** — 交换容器与品牌行之间的间距。
  - 范围：40–96 px
- **SWAP_WRAP_W / SWAP_WRAP_H** — 交换容器的固定宽高；两张卡片在其内均为 `inset: 0`。
  - 约束：尺寸须容纳两种状态的内容；交换过程中 wrap 不 resize
- **CARD_INNER_GAP** — 卡片内图标与标题间距。
  - 范围：16–32 px
- **CARD_RADIUS / CARD_PADDING** — 卡片圆角与内边距。
  - 范围：圆角 24–40 px；内边距 32–64 px
- **ICON_SIZE / TITLE_SIZE / SUB_SIZE / BRAND_SIZE** — 字号。
  - 约束：标题占主导（1080p 下约 80–120 px）；副标题与品牌为 accent 尺寸
- **TITLE_TRACKING / BRAND_TRACKING** — 大写标签的字间距。
  - 范围：4–16 px（大写配合正 tracking 更易读）

### 令牌

- **{sceneBg}** — 背景渐变/颜色
- **{font}** — 字体栈
- **{textColor}** / **{accentColor}** / **{brandColor}** — 语义颜色令牌
- **{outgoingBg}** / **{outgoingBorder}** — outgoing 卡片表面与边框（常为暖色或动作前色相）
- **{incomingBg}** / **{incomingBorder}** — incoming 卡片表面与边框（常为冷色或动作后色相）
- **{outgoingIcon}** / **{incomingIcon}** — 各状态单一 glyph/emoji
- **{outgoingLabel}** / **{incomingLabel}** — 状态标签
- **{incomingSubline}** — incoming 落定后淡入的辅助文案
- **{Brand}** — 显示在交换下方的品牌行

## 核心原则

- **Incoming 的 z-index 高于 outgoing** — 否则 outgoing 淡出尾迹（opacity 0.3–0.5）会透过 incoming 较低的不透明度，产生「双重曝光」的糊帧
- **两者共用 `transform-origin: 50% 50%`** — 原点不一致会让 morph 像物体瞬移到别处
- **`OVERLAP` 落在 0.1–0.2 s 窗口** — 重叠过多则两者同时清晰（无 morph）；过少则出现明显空档
- **弹性 ease 仅用于 incoming** — outgoing 用 `power2.in`（快速离开），incoming 用 `back.out(${BOUNCE_FACTOR})`（有重量地到达）。反过来会显得机械
- **内层内容在容器落定后再揭示** — 见 `SUB_REVEAL_DELAY`。在 morph 期间揭示会与交换争抢注意力并落败
- **高潮停留：最终状态落定后 ≥1 s** — 见 SKILL 通用约束。incoming 与副标题均落定后，至少保持 ≥1 s
- **品牌应早揭示，而非与交换同步** — 上下文（品牌、眉题）铺垫舞台；交换才是 headline。若品牌与交换同时出现，会互相竞争

## 关键约束

- **时间轴须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **两个交换元素上均勿用 CSS `transition`** — 会与 GSAP 冲突
- **两个交换元素均设置 `will-change: transform, opacity`**
- **两者在同一 wrapper 内使用 `position: absolute; inset: 0`** — 占据同一 footprint，通过淡出其一、弹入另一完成交换
- **淡出后勿对 outgoing 使用 `display: none`** — 保持 `opacity: 0`，避免布局 reflow

## 组合

- [press-release-spring.md](press-release-spring.md) — 按钮按下触发交换（因果）
- [sine-wave-loop.md](sine-wave-loop.md) — 最终状态的 idle 呼吸
- [card-morph-anchor.md](card-morph-anchor.md) — 形状变化过渡的替代方案（本规则适用于同形状状态交换）

## 与 HF 技能配合

- `/hyperframes-animation` — 带重叠的两条协调 tween
- `/hyperframes-core` — composition 接线
- `/hyperframes-cli` — `hyperframes lint`
