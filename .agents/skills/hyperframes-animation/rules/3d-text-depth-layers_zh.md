---
name: 3d-text-depth-layers
description: 多层偏移文字叠加在大号字重上，形成堆叠式 3D 阴影/挤出效果——比 CSS text-shadow 更有冲击力，因为每一层都是完整的 DOM 元素。
metadata:
  tags: text, 3d, depth, layers, shadow, typography, stacked, extrusion
---

# 3D 文字深度层

将同一段文字渲染 N 次，每次递增偏移；后层半透明，最前层完全不透明。营造物理感「堆叠挤出」的深度错觉。与 `text-shadow` 不同（无法为每层单独设置色相/透明度/动画）——每一层都是真实的 DOM 元素。

## 工作原理

- 单个容器内放置 N 份相同文字
- 每份绝对定位，偏移量为 `(i * OFFSET_X, i * OFFSET_Y)`
- 后层（`i` 较大）使用半透明或加深颜色
- 最前层（`i = 0`）为全不透明度、完整品牌色
- 可选：各层错峰淡入，形成「逐层堆叠」的深度动画

## HTML

```html
<div
  class="scene"
  id="depth-scene"
  data-composition-id="depth-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="depth-stack">
    <!-- Layers injected by script — LAYER_COUNT copies of {label} -->
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
.depth-stack {
  position: relative;
  /* Container size set by the front layer; back layers stack behind */
}
.depth-text {
  font-family: {font};
  font-weight: 900;
  font-size: HERO_FONT_SIZE;
  letter-spacing: HERO_LETTER_SPACING;
  line-height: 1;
  color: {frontColor};
  text-transform: uppercase;
}
/* Back layers — absolute, stacked behind */
.depth-text.is-back {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
}
/* Front layer — relative to define container size */
.depth-text.is-front {
  position: relative;
  z-index: 10;
}
```

## GSAP Timeline + Layer Setup

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};

  const TEXT = "{label}";
  const stack = document.querySelector(".depth-stack");

  // Build layers — back-to-front so the FRONT (i=0) is the LAST appended
  // and `position: relative` defines container size.
  for (let i = LAYER_COUNT - 1; i >= 0; i--) {
    const el = document.createElement("div");
    el.className = "depth-text " + (i === 0 ? "is-front" : "is-back");
    el.textContent = TEXT;
    if (i > 0) {
      const alpha = Math.max(BACK_ALPHA_MAX - i * BACK_ALPHA_STEP, BACK_ALPHA_MIN);
      el.style.color = `rgba({backHueRGB}, ${alpha})`;
      el.style.transform = `translate(${i * OFFSET_X}px, ${i * OFFSET_Y}px)`;
    } else {
      el.style.color = "{frontColor}";
    }
    el.dataset.layer = String(i);
    stack.appendChild(el);
  }

  const tl = gsap.timeline({ paused: true });

  // Layered entry — back layers appear first, building forward
  const allLayers = stack.querySelectorAll(".depth-text");
  allLayers.forEach((el) => {
    const i = Number(el.dataset.layer);
    const finalAlpha = el.classList.contains("is-front")
      ? 1
      : Math.max(BACK_ALPHA_MAX - i * BACK_ALPHA_STEP, BACK_ALPHA_MIN);
    tl.fromTo(
      el,
      { opacity: 0 },
      {
        opacity: finalAlpha,
        duration: LAYER_FADE_DUR,
        ease: "power2.out",
      },
      LAYER_CASCADE_START + (LAYER_COUNT - 1 - i) * LAYER_CASCADE_STEP,
    );
  });

  // Optional: depth grows on entry (offset interpolates from 0 → full)
  const depthState = { p: 0 };
  tl.to(
    depthState,
    {
      p: 1,
      duration: DEPTH_GROW_DUR,
      ease: "power2.out",
      onUpdate: () => {
        stack.querySelectorAll(".depth-text.is-back").forEach((el) => {
          const i = Number(el.dataset.layer);
          const x = i * OFFSET_X * depthState.p;
          const y = i * OFFSET_Y * depthState.p;
          el.style.transform = `translate(${x}px, ${y}px)`;
        });
      },
    },
    DEPTH_GROW_START,
  );

  window.__timelines["depth-scene"] = tl;
</script>
```

## 变体

### 静态深度（无动画，单帧 hero）

跳过层叠入场——从 t=0 起所有层已在最终位置，可选整栈淡入：

```js
tl.from(
  stack,
  { opacity: 0, scale: STATIC_ENTRY_SCALE, duration: STATIC_ENTRY_DUR, ease: "power3.out" },
  0,
);
```

### 动态深度脉冲

按心跳节奏驱动 `OFFSET_X` / `OFFSET_Y`——深度有节奏地伸缩：

```js
const beat = { p: 0 };
tl.to(
  beat,
  {
    p: Math.PI * 2 * BEAT_CYCLES,
    duration: BEAT_DUR,
    ease: "none",
    onUpdate: () => {
      const mult = 1 + Math.sin(beat.p) * BEAT_AMP;
      stack.querySelectorAll(".is-back").forEach((el) => {
        const i = Number(el.dataset.layer);
        el.style.transform = `translate(${i * OFFSET_X * mult}px, ${i * OFFSET_Y * mult}px)`;
      });
    },
  },
  BEAT_START,
);
```

### 后层色相偏移

不淡化为半透明，而改为色相渐变——深度读作「投下有色阴影」：

```js
el.style.color = `hsla(${HUE_BASE - i * HUE_STEP}, ${SAT_PCT}%, ${LIGHT_BASE - i * LIGHT_STEP}%, 1)`;
```

## 如何选取参数

### 层几何

- **LAYER_COUNT** — 堆叠副本数量（后层 + 1 个前层）。
  - 范围：4–6。少于 4 层难以读出 3D；多于 6 在紧字距下视觉杂乱
  - 效果：低端偏 subtle 阴影；高端偏 chunky 挤出
- **OFFSET_X / OFFSET_Y** — 每层平移偏移，单位 px。
  - 范围：各轴 1–3 px。超过 4 px 更像 glitch / 色差而非深度
  - 效果：偏移方向暗示光源方向。`(+x, +y)` = 光从左上方来；`(-x, +y)` = 光从右上方来。选定一种并在整段合成中保持一致
  - 约束：整段合成使用相同符号约定

### 后层颜色衰减

- **BACK_ALPHA_MAX** — 最靠近前层的后层 alpha。
  - 范围：0.6–0.85。低于 0.5 时即使最近的后层也几乎消失；高于 0.9 会与 front 层争抢视觉主导
- **BACK_ALPHA_STEP** — 每向更后一层 alpha 的递减量。
  - 范围：0.08–0.15。步长小读作柔和渐变；步长大读作离散 plate
  - 约束：满足 `BACK_ALPHA_MAX − (LAYER_COUNT − 2) × BACK_ALPHA_STEP ≥ BACK_ALPHA_MIN`
- **BACK_ALPHA_MIN** — 后层不再继续变淡的下限。
  - 范围：0.1–0.2。低于 0.1 时最深层在深色背景上完全消失

### 字体排版

- **HERO_FONT_SIZE** — 前层字号，单位 px。
  - 范围：至少 60 px 才能读出分层；全幅 hero 常用 200–340 px。细字会失去分层错觉
- **HERO_LETTER_SPACING** — 字间距。
  - 范围：−0.03em（紧）到 0（正常）。负间距收紧堆叠，使偏移读作深度而非重复
- **{font}** — 字体；选用 black/900 字重、横笔画有力的 family
- **{frontColor}** — 前层颜色；品牌或强调色
- **{backHueRGB}** — 后层 RGB 三元组（例如与品牌 glow 匹配）。用于 `rgba({backHueRGB}, ${alpha})`

### 层叠入场（默认形态）

- **LAYER_CASCADE_START** — 层叠开始的时间轴偏移。
  - 约束：≥ 0；若前面还有 beat，≥ 该 beat 结束时刻
- **LAYER_CASCADE_STEP** — 各层淡入之间的延迟。
  - 范围：0.04–0.10 s。更小几乎同时；更大呈阶梯感、偏机械
- **LAYER_FADE_DUR** — 单层淡入时长。
  - 范围：0.3–0.6 s

### 深度生长 tween

- **DEPTH_GROW_START** — 偏移开始从 0 增长到满值的时刻。
  - 约束：通常 `≈ LAYER_CASCADE_START`；与第一层淡入和深度生长同步起步
- **DEPTH_GROW_DUR** — 偏移从 0 插值到满值的时长。
  - 范围：0.4–0.8 s。大致匹配 `LAYER_FADE_DUR × LAYER_COUNT / 2`，使最后一层淡入时深度到位

### 静态深度变体

- **STATIC_ENTRY_SCALE** — 整栈淡入前的初始 scale。
  - 范围：0.94–0.98 — 轻微膨胀；更大则像独立的「pop」效果
- **STATIC_ENTRY_DUR** — 整栈淡入时长。
  - 范围：0.5–0.8 s

### 动态脉冲变体

- **BEAT_CYCLES** — 在 `BEAT_DUR` 内的完整 beat 周期数。
  - 范围：`BEAT_DUR / 1.5s ≤ BEAT_CYCLES ≤ BEAT_DUR / 0.7s`（每 0.7–1.5 s 一个 beat 读作心跳）
- **BEAT_DUR** — 脉冲 tween 时长。
  - 约束：与深度栈的可见窗口绑定
- **BEAT_AMP** — 偏移脉冲的相对振幅。
  - 范围：0.2–0.6。较小为柔和呼吸式深度；较大像 kick 鼓冲击
- **BEAT_START** — 脉冲开始时刻。
  - 约束：`≥ DEPTH_GROW_START + DEPTH_GROW_DUR`，使脉冲作用在已完全长成的栈上

### 色相偏移变体

- **HUE_BASE / HUE_STEP** — 基础色相（前层）与每层色相旋转。
  - 范围：`HUE_STEP` 4–12°。步长大则绕色轮更远，偏 glitch
- **SAT_PCT** — 各层固定饱和度。
  - 范围：60–85%
- **LIGHT_BASE / LIGHT_STEP** — 基础明度与每层变暗量。
  - 范围：`LIGHT_STEP` 3–8 个百分点，使后层向背景加深

## 关键原则

- **层数 4–6** — 少于 4 读不出 3D，多于 6 在紧字距下视觉杂乱
- **每轴偏移 1–3 px** — subtle 即 dramatic。`OFFSET = 6+` 像 glitch 而非深度
- **偏移方向暗示光源** — `(+x, +y)` = 光从左上方；`(-x, +y)` = 光从右上方。选定一种并在合成中一致
- **后层半透明或更暗** — 不要比前层更饱和（会像 halo）。每层后层应略更透明（`alpha -= BACK_ALPHA_STEP per layer`）或略更暗
- **最后（前）层 `position: relative`** 以定义容器尺寸；其余 `position: absolute` 堆在后侧
- **粗黑字重 + 大号** — 900 字重，至少 60 px。细字失去分层错觉
- **不要在层叠之上再做逐字动画** — 6 层深度之上再加字符动画（hacker-flip、typewriter）= 混乱。若两种都要，深度减至 2–3 层，或仅在静态 reveal 后状态应用层叠

## 关键约束

- **时间轴必须 paused**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **不要与层叠深度同时使用 CSS `text-shadow`** — 会叠加过度挤出
- **偏移用 `transform: translate()`，不用 `top`/`left`** — translate 与父级居中组合干净，避免 reflow
- **后层 `pointer-events: none`** — 装饰性；不拦截 hover 或选中
- **层颜色用 `rgba()` 而非 opacity** — 元素整体 opacity 会连同阴影一起淡；`color` 里的 rgba 只淡字形

## 组合

- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 用深度层渲染计数数字
- [sine-wave-loop.md](sine-wave-loop.md) — reveal 后在前层做 idle 呼吸
- [center-outward-expansion.md](center-outward-expansion.md) — burst 落定后 depth-stacked 字标 reveal

## 搭配的 HF 技能

- `/hyperframes-animation` — 错峰淡入 + onUpdate 实现动态深度
- `/hyperframes-core` — 合成 wiring
- `/hyperframes-cli` — `hyperframes lint`
