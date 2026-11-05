---
name: split-tilt-cards
description: 两张卡片并排、沿 Y 轴反向旋转，形成对称的三维分屏布局，适用于对比或功能配对展示。
metadata:
  tags: 3d, cards, split, tilt, comparison, symmetric, layout
---

# 分屏倾斜卡片

两张卡片并排摆放，各自沿相反 Y 方向旋转。形成对称的「书本展开」式三维效果——自然适合对比、前后对照或功能配对。

## 工作原理

- 左侧卡片旋转 `+Y`（朝向右侧观看角度）
- 右侧卡片旋转 `-Y`（朝向左侧观看角度）
- 两者共享同一 `perspective` 父级 → 相反旋转在视觉上相互平衡
- 每张卡片从外侧进入（左卡从左滑入，右卡从右滑入），以强化各自身份
- 空闲阶段：轻柔的反相浮动（正弦波上 `Math.PI` 相位差）——两张卡片上下起伏方向相反

## HTML

```html
<div
  class="scene"
  id="split-scene"
  data-composition-id="split-scene"
  data-start="0"
  data-duration="4"
  data-track-index="0"
>
  <div class="split-stage">
    <div class="card card-left">
      <div class="card-eyebrow">{leftEyebrow}</div>
      <div class="card-headline">{leftHeadline}</div>
      <div class="card-body">{leftBody}</div>
    </div>
    <div class="card card-right">
      <div class="card-eyebrow">{rightEyebrow}</div>
      <div class="card-headline">{rightHeadline}</div>
      <div class="card-body">{rightBody}</div>
    </div>
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
  perspective: SCENE_PERSPECTIVE; /* REQUIRED — without perspective rotateY flattens */
}
.split-stage {
  display: flex;
  gap: STAGE_GAP;
  transform-style: preserve-3d;
}
.card {
  width: CARD_WIDTH;
  min-height: CARD_MIN_HEIGHT;
  padding: CARD_PADDING;
  display: flex;
  flex-direction: column;
  gap: CARD_INNER_GAP;
  border-radius: CARD_RADIUS;
  background: {cardSurface};
  border: 1px solid {cardBorder};
  color: {textColor};
  font-family: {font};
  transform-style: preserve-3d;
  will-change: transform;
}
.card-left {
  /* Faces right → shadow falls right */
  box-shadow:
    -CARD_SHADOW_OFFSET CARD_SHADOW_DROP CARD_SHADOW_BLUR {shadowColor},
    0 0 CARD_GLOW_BLUR {accentGlowColor};
}
.card-right {
  /* Faces left → shadow falls left */
  box-shadow:
    CARD_SHADOW_OFFSET CARD_SHADOW_DROP CARD_SHADOW_BLUR {shadowColor},
    0 0 CARD_GLOW_BLUR {accentGlowColor};
}
.card-eyebrow {
  font-size: EYEBROW_FONT_SIZE;
  font-weight: 800;
  letter-spacing: EYEBROW_LETTER_SPACING;
  text-transform: uppercase;
  color: {accentColor};
}
.card-headline {
  font-size: HEADLINE_FONT_SIZE;
  font-weight: 900;
  line-height: 1;
  letter-spacing: HEADLINE_LETTER_SPACING;
}
.card-body {
  font-size: BODY_FONT_SIZE;
  font-weight: 500;
  line-height: 1.3;
  color: {bodyColor};
  opacity: BODY_OPACITY;
}
```

## GSAP 时间轴

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Phase 1 — entry from outside
  tl.fromTo(
    ".card-left",
    { x: -ENTRY_SLIDE_DIST, rotateY: TILT + TILT_OVERSHOOT, opacity: 0 },
    { x: 0, rotateY: TILT, opacity: 1, duration: ENTRY_DUR, ease: "power3.out" },
    LEFT_AT,
  );
  tl.fromTo(
    ".card-right",
    { x: ENTRY_SLIDE_DIST, rotateY: -TILT - TILT_OVERSHOOT, opacity: 0 },
    { x: 0, rotateY: -TILT, opacity: 1, duration: ENTRY_DUR, ease: "power3.out" },
    RIGHT_AT,
  );

  // Phase 2 — counter-phase idle bob (cards move in opposition for dynamism)
  tl.to(
    ".card-left",
    { y: -FLOAT_AMP, duration: FLOAT_DURATION / 2, ease: "sine.inOut", yoyo: true, repeat: 1 },
    IDLE_START,
  );
  tl.to(
    ".card-right",
    { y: FLOAT_AMP, duration: FLOAT_DURATION / 2, ease: "sine.inOut", yoyo: true, repeat: 1 },
    IDLE_START,
  );

  // Phase 3 — gentle copy reveal (body slides up + fades after cards arrive)
  tl.from(
    ".card-eyebrow, .card-headline, .card-body",
    { opacity: 0, y: COPY_RISE, stagger: COPY_STAGGER, duration: COPY_DUR, ease: "power2.out" },
    COPY_REVEAL_AT,
  );

  window.__timelines["split-scene"] = tl;
</script>
```

## 如何选择数值

### 布局 / 排版

- **SCENE_PERSPECTIVE** — 场景根节点上的 perspective。
  - 范围：1000–2400 px
  - 效果：数值越低倾斜越夸张（更锥形）；越高则接近等轴测、旋转更平
- **STAGE_GAP** — 两张卡片之间的水平间距。
  - 范围：40–120 px（≈0.06–0.15× `CARD_WIDTH`）
  - 效果：间距小像「融合的一对」；间距大像「对比但分离」
- **CARD_WIDTH** — 每张卡片的宽度。
  - 范围：1920×1080 下 480–820 px
  - 约束：`2 * CARD_WIDTH + STAGE_GAP ≤ 0.95 * stageWidth`，使满倾斜时两张卡仍在画面内
- **CARD_MIN_HEIGHT** — 卡片最小高度。
  - 范围：≈0.75–1.05× `CARD_WIDTH`（接近方形较均衡；过高像海报）
- **CARD_PADDING / CARD_INNER_GAP / CARD_RADIUS** — 内部留白与圆角。
  - 范围：内边距 40–72 px；内部间距 24–48 px；圆角 24–40 px
- **CARD_SHADOW_OFFSET / CARD_SHADOW_DROP / CARD_SHADOW_BLUR** — 投影几何。
  - 约束：offset 符号与倾斜方向一致（见关键原则）；drop > 0 使卡片「落在」场景上
  - 范围：offset 16–28 px；drop 20–32 px；blur 40–80 px
- **CARD_GLOW_BLUR** — 次要内发光模糊半径（`box-shadow` 的 0 0 blur）。
  - 范围：16–32 px（轻微强调色描边；过大易与正文争抢注意力）
- **EYEBROW_FONT_SIZE / EYEBROW_LETTER_SPACING** — 小号全大写标签。
  - 范围：22–32 px；字距 6–12 px（全大写配合正字距更清晰）
- **HEADLINE_FONT_SIZE / HEADLINE_LETTER_SPACING** — 主标题一行冲击力。
  - 范围：1920×1080 下 72–104 px；字距 -1 至 -3 px（展示字重常用紧字距）
- **BODY_FONT_SIZE / BODY_OPACITY** — 辅助正文。
  - 范围：28–40 px；不透明度 0.8–0.92
  - 约束：正文每张卡 ≤2 行（见关键约束——倾斜长段落会发糊）

### 入场 / 倾斜

- **TILT** — 静态 `rotateY` 角度大小（左 `+`，右 `−`）。
  - 范围：10–18°（低于 10 几乎像平面；超过 18 卡片像合拢，正文难读）
- **TILT_OVERSHOOT** — 在落定到 `TILT` 之前，起始 `rotateY` 上额外加的角度。
  - 范围：4–12°
  - 效果：入场时有轻微「枢转到位」感
- **ENTRY_SLIDE_DIST** — 每张卡从轴外滑入的像素距离。
  - 范围：200–500 px（≈0.3–0.6× `CARD_WIDTH`）
- **ENTRY_DUR** — 单卡滑入时长。
  - 范围：0.6–1.2 s
- **LEFT_AT** — 左卡入场开始时间。
  - 范围：0.0–0.4 s
- **RIGHT_AT** — 右卡入场开始时间。
  - 范围：`LEFT_AT + 0.0` 至 `LEFT_AT + 0.3` s（零错开显机械；错开过大则一对感被拆散）

### 空闲浮动

- **FLOAT_AMP** — 空闲 y 轴正弦浮动幅度（px）。
  - 范围：3–8 px（见 sine-wave-loop 规则——幅度宜小，勿过大）
- **FLOAT_DURATION** — 完整 yoyo 往返时长（一次「呼吸」）。
  - 范围：1.6–3.2 s（≈呼吸节奏）
- **IDLE_START** — 空闲浮动开始时间。
  - 约束：`≥ max(LEFT_AT, RIGHT_AT) + ENTRY_DUR`，避免与入场尾部打架

### 文案显现

- **COPY_REVEAL_AT** — eyebrow/headline/body 淡入开始时间。
  - 约束：通常与卡片落定阶段重叠（叠在入场尾部）——内容不应在卡片已完全静止后才弹出
- **COPY_DUR / COPY_STAGGER / COPY_RISE** — 上浮淡入形态。
  - 范围：时长 0.4–0.7 s；错开 0.04–0.10 s；上浮 12–24 px

### 颜色 / 排版 token

- **{bgGradient}** — 卡片后的径向或线性渐变；比 `{cardSurface}` 更暗，让卡片浮起
- **{cardSurface}** — 卡片背景（常为叠在场景上的低饱和渐变）
- **{cardBorder}** — 1 px 边框色，常为低 alpha 的 `{accentColor}`
- **{shadowColor}** — 投影色，通常近黑、alpha 0.5–0.7
- **{accentGlowColor}** — 内发光色，通常低 alpha 的 `{accentColor}`
- **{accentColor}** — eyebrow 与强调描边色（每场景单一色相）
- **{textColor}** — 主标题色，与 `{cardSurface}` 高对比
- **{bodyColor}** — 正文色，相对 `{textColor}` 略去饱和
- **{font}** — 卡片全部文案的展示字体栈

## 变体

### 中倾斜穿镜（配合镜头运动）

若另有镜头 tween 缩放 `.split-stage`，卡片倾斜会像观众从两卡之间的缝隙穿过。

### 非对称内容密度（徽章 / 标签 / 图标）

可在每张卡旁加浮动徽章补充信息。在父级上绝对定位——不要放在卡片内部，以免继承 3D 旋转：

```html
<div class="badge badge-left">{leftBadge}</div>
<div class="badge badge-right">{rightBadge}</div>
```

### 堆叠变体（3 张及以上）

3 张卡时，中间卡保持平面（`rotateY 0`），外侧两张向内倾——适合「旧方式 / 中间空白 / 我们的方式」类对比。

## 关键原则

- **场景根上必须有 `perspective`** — 没有则 rotateY 变平，分屏倾斜退化为平面并排
- **stage 与每张卡都要 `transform-style: preserve-3d`** — 保留 3D 平面，因卡片各有 transform
- **阴影方向须与倾斜一致** — 左卡朝右，阴影落右侧（正 X），反之亦然。方向错会显「3D 坏了」
- **内容权重对称** — 两卡同宽、垂直居中、行数相近。非对称破坏对比隐喻
- **反相浮动（`Math.PI` 相位差）** — 左上浮时右下沉。同相浮动像同一传送带；反相更有生命感
- **从外侧滑入** — 左卡从左、右卡从右——强化「各来自一方，在此相遇」
- **❗ 倾斜幅度 10–15°** — 低于 10° 像轻微透视偏移（几乎平）；超过 18° 像合拢，正文难读

## 关键约束

- **时间轴必须 paused**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **空闲浮动不要用 `requestAnimationFrame`** — 放在时间轴内以保证 seek 可确定
- **不要把徽章放在 card div 内** — 会继承 rotateY 与卡一起歪。在父级上浮动
- **每张卡正文 ≤ 2 行** — 倾斜文字难读；长段落在透视下糊成一片

## 组合

- [card-morph-anchor.md](card-morph-anchor.md) — 两卡之后可 morph 成单一统一形状
- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 两侧 headline 用数字内容

## 与 HF 技能搭配

- `/hyperframes-animation` — 时间轴 + 空闲浮动的 `yoyo`
- `/hyperframes-core` — composition 接线
- `/hyperframes-cli` — `hyperframes lint`
