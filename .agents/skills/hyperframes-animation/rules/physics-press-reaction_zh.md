---
name: physics-press-reaction
description: 通过减法式弹簧力实现 Cursor 与元素同步按压——光标落在元素上，二者一起压缩，再一起回弹。与 press-release-spring（无光标）不同。
metadata:
  tags: spring, click, physics, cursor, subtractive, interaction, synchronized
---

# 物理按压反馈（Cursor + 元素同步）

模拟真实点击：光标接近按钮、落下，并与按钮**同步**压缩，再一起回弹。两个明确的时间点（按下帧与抬起帧）由弹簧力约束。与 [press-release-spring](press-release-spring.md)（无光标，仅按压本身）不同；本规则描述**光标 + 元素**的组合行为。

## 工作原理

单个 `PRESS_INTENSITY` 值同时驱动光标与按钮：

- **按下**：二者均压缩至 `1 - PRESS_INTENSITY`
- **释放**：二者以 overshoot 弹回 1.0

在按压开始**之前**的接近阶段，光标还会平移到按钮中心。释放后，光标可继续移动（下一次交互）或保持不动。

## HTML

```html
<div
  class="scene"
  id="press-react-scene"
  data-composition-id="press-react-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="stack">
    <button class="btn" id="btn">
      <span class="btn-icon">{ctaIcon}</span>
      <span class="btn-label">{ctaCopy}</span>
    </button>
    <div class="brand">{Brand}</div>
  </div>
  <!-- Cursor lives at scene-root level so it can translate freely -->
  <svg class="cursor" id="cursor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path
      d="M3 2 L21 12 L12 13 L7 22 Z"
      fill="{cursorFill}"
      stroke="{cursorStroke}"
      stroke-width="1.5"
    />
  </svg>
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
  overflow: hidden;
}
.stack {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: STACK_GAP;
}
.btn {
  display: flex;
  align-items: center;
  gap: BTN_INNER_GAP;
  padding: BTN_PADDING_V BTN_PADDING_H;
  background: {btnBg};
  border: none;
  border-radius: BTN_RADIUS;
  color: {btnTextColor};
  font-family: {font};
  font-weight: 900;
  font-size: BTN_FONT_SIZE;
  letter-spacing: BTN_TRACKING;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: {btnRestingShadow};
  transform-origin: 50% 50%;
  will-change: transform;
}
.btn-icon {
  font-size: BTN_ICON_SIZE;
  line-height: 1;
}
.brand {
  font-size: BRAND_SIZE;
  font-weight: 800;
  letter-spacing: BRAND_TRACKING;
  color: {brandColor};
  text-transform: uppercase;
}
/* Cursor — absolute, positioned by GSAP */
.cursor {
  position: absolute;
  width: CURSOR_SIZE;
  height: CURSOR_SIZE;
  pointer-events: none;
  z-index: 100;
  /* initial position is set by gsap.set() */
  transform-origin: 0 0; /* arrow point is the click point */
  filter: {cursorDropShadow};
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Position cursor initially off-target (off-screen or far corner).
  gsap.set("#cursor", { x: CURSOR_START_X, y: CURSOR_START_Y });

  // The button's screen center, in composition coordinates.
  const BUTTON_CENTER = { x: BUTTON_CENTER_X, y: BUTTON_CENTER_Y };

  // Phase 1 — cursor approaches button
  tl.to(
    "#cursor",
    {
      x: BUTTON_CENTER.x,
      y: BUTTON_CENTER.y,
      duration: APPROACH_DUR,
      ease: "power2.inOut",
    },
    APPROACH_START,
  );

  // Phase 2 — coordinated press down (button + cursor both scale to 1 - PRESS_INTENSITY)
  tl.to(
    ["#btn", "#cursor"],
    {
      scale: 1 - PRESS_INTENSITY,
      duration: PRESS_DOWN_DUR,
      ease: "power1.in",
    },
    PRESS_DOWN_AT,
  );

  // Phase 3 — release (both spring back to 1.0 with overshoot)
  tl.to(
    ["#btn", "#cursor"],
    {
      scale: 1,
      duration: RELEASE_DUR,
      ease: `back.out(${BOUNCE_FACTOR})`,
    },
    RELEASE_AT,
  );

  // Phase 4 — inner glow during press (boxShadow change synced to press scale)
  tl.to(
    "#btn",
    {
      boxShadow: `{btnPressedShadow}`,
      duration: PRESS_DOWN_DUR,
      ease: "power1.in",
    },
    PRESS_DOWN_AT,
  );
  tl.to(
    "#btn",
    {
      boxShadow: `{btnRestingShadow}`,
      duration: RELEASE_DUR,
      ease: "power2.out",
    },
    RELEASE_AT,
  );

  // Brand fades in early (context)
  tl.from(
    ".brand",
    { opacity: 0, y: BRAND_REVEAL_Y_PX, duration: BRAND_REVEAL_DUR, ease: "power3.out" },
    BRAND_REVEAL_AT,
  );

  // Cursor optionally moves off after press (or holds for dwell)
  tl.to(
    "#cursor",
    { x: CURSOR_EXIT_X, y: CURSOR_EXIT_Y, duration: CURSOR_EXIT_DUR, ease: "power2.out" },
    CURSOR_EXIT_AT,
  );

  window.__timelines["press-react-scene"] = tl;
</script>
```

## 变体

### 多元素链式按压

光标按下按钮 A → 按钮 A 触发切换 → 光标移向按钮 B → 再次按下。每次按压都是完整的按下-释放子流程。

### 按住按压（持续施力）

在按下与释放之间插入 `HOLD_DUR` 窗口。光标与按钮的 scale 均保持 `1 - PRESS_INTENSITY`，内发光保持开启。传达「思考中」或「加载中」。

### 同步内发光脉冲

在按住阶段，内发光按正弦脉冲（sin 驱动）。传达「处理中」：

```js
const holdGlow = { p: 0 };
tl.to(
  holdGlow,
  {
    p: Math.PI * GLOW_PULSE_CYCLES * 2,
    duration: HOLD_DUR,
    ease: "none",
    onUpdate: () => {
      const alpha = GLOW_BASE_ALPHA + Math.sin(holdGlow.p) * GLOW_PULSE_AMP;
      document.getElementById("btn").style.boxShadow =
        `inset 0 0 GLOW_BLUR rgba(255, 255, 255, ${alpha})`;
    },
  },
  HOLD_START_AT,
);
```

## 如何选取数值

### 时间（秒）

- **APPROACH_START** — 光标开始向按钮移动的时刻。
  - 范围：0–0.3 s（短前置即可；过长会像死帧）
- **APPROACH_DUR** — 光标接近时长。
  - 范围：0.7–1.3 s；更快显紧迫，更慢显从容
- **PRESS_DOWN_AT** — 按下触发的时刻。
  - 约束：必须等于 `APPROACH_START + APPROACH_DUR`，使光标在按下开始时刚好到达（避免「点空气」）
- **PRESS_DOWN_DUR** — 压缩时长。
  - 范围：0.1–0.25 s
- **RELEASE_AT** — 释放触发的时刻。
  - 约束：须大于 `PRESS_DOWN_AT + PRESS_DOWN_DUR`；可选短暂按住（0.05–0.4 s，或按住变体中的 `HOLD_DUR`）以表达「思考」类交互
- **RELEASE_DUR** — 释放弹簧时长。
  - 范围：0.4–0.7 s（足够 overshoot 落定）
- **BRAND_REVEAL_AT** — 品牌行淡入时刻。
  - 约束：须小于 `PRESS_DOWN_AT`（上下文先于交互）
- **BRAND_REVEAL_DUR** — 品牌淡入时长。
  - 范围：0.4–0.8 s
- **CURSOR_EXIT_AT / CURSOR_EXIT_DUR** — 释放后可选的光标离场运动。
  - 约束：`CURSOR_EXIT_AT` 须 ≥ `RELEASE_AT + RELEASE_DUR`，使光标在按压落定**之后**离场，而非进行中

### 物理

- **PRESS_INTENSITY** — 按压压缩深度。
  - 范围：0.05（轻微）– 0.10（标准）– 0.15（重）
  - 对光标与按钮同时应用 `scale: 1 - PRESS_INTENSITY`（单一 GSAP 目标数组）
- **BOUNCE_FACTOR** — 释放时 `back.out(${BOUNCE_FACTOR})` 的 overshoot。
  - 范围：1.6（软）– 2.0（偏硬）– 2.4（卡通）

### 定位

- **CURSOR_START_X / CURSOR_START_Y** — 合成坐标系中的初始光标位置。
  - 约束：屏外或远离按钮的角落，使接近读作「移入」而非瞬移
- **BUTTON_CENTER_X / BUTTON_CENTER_Y** — 按钮测得的屏幕空间中心。
  - 来源：合成坐标下测量；1920×1080 且 `place-items: center` 时为 `(960, 540)`
- **CURSOR_EXIT_X / CURSOR_EXIT_Y** — 释放后光标移动目标（若使用）。
  - 范围：任意离场或不妨碍画面的位置
- **BRAND_REVEAL_Y_PX** — 品牌行初始 y 偏移。
  - 范围：8–20 px

### 布局 / 字体

- **STACK_GAP** — 按钮与品牌行间距。
  - 范围：40–96 px
- **BTN_PADDING_V / BTN_PADDING_H** — 按钮内边距。
  - 范围：V 24–40 px，H 60–100 px（水平约为垂直 2–3× 时呈药丸形 CTA）
- **BTN_INNER_GAP** — 按钮内图标与标签间距。
  - 范围：16–32 px
- **BTN_RADIUS** — 按钮圆角。
  - 范围：20–40 px，或 `BTN_PADDING_V + BTN_FONT_SIZE/2` 以完全圆角端
- **BTN_FONT_SIZE / BTN_ICON_SIZE** — 按钮内字号。
  - 范围：1080p 下字体 60–100 px；图标约为字号的 1.0–1.1×
- **BTN_TRACKING** — 大写按钮文字字距。
  - 范围：4–12 px
- **BRAND_SIZE / BRAND_TRACKING** — 品牌行字体样式。
  - 范围：40–60 px，tracking 8–16 px
- **CURSOR_SIZE** — 光标 SVG 尺寸。
  - 范围：1080p 下 48–96 px

### 按住按压变体

- **HOLD_DUR** — 按下与释放之间的按住窗口。
  - 范围：0.3–0.8 s
- **HOLD_START_AT** — 发光脉冲开始时刻。
  - 约束：通常等于 `PRESS_DOWN_AT + PRESS_DOWN_DUR`
- **GLOW_PULSE_CYCLES** — `HOLD_DUR` 内完整正弦周期数。
  - 范围：1–4（周期越多越像快速「处理中」）
- **GLOW_BASE_ALPHA** — alpha 脉冲中心值。
  - 范围：0.15–0.3
- **GLOW_PULSE_AMP** — 相对 `GLOW_BASE_ALPHA` 的峰值偏差。
  - 范围：0.1–0.2；须满足 `GLOW_BASE_ALPHA - GLOW_PULSE_AMP ≥ 0`
- **GLOW_BLUR** — 内发光模糊半径（px）。
  - 范围：24–48 px

### Tokens

- **{sceneBg}** — 背景渐变/颜色
- **{font}** — 字体栈
- **{btnBg}** — 按钮背景（通常渐变至 accent 色相）
- **{btnTextColor}** — 按钮文字颜色
- **{btnRestingShadow}** / **{btnPressedShadow}** — 静止与按下状态的外阴影 + 内阴影字符串
- **{brandColor}** — 品牌 accent 色
- **{cursorFill}** / **{cursorStroke}** — 光标 SVG 填充与描边
- **{cursorDropShadow}** — 光标深度的 `filter: drop-shadow(...)` 值
- **{Brand}** — 品牌行文案
- **{ctaCopy}** / **{ctaIcon}** — 按钮标签与行内图标 glyph

## 核心原则

- **光标与按钮使用相同按压 scale** — 物理同步。仅按钮缩放则光标像「点空气」；仅光标缩放则按钮脱节。
- **按压开始前光标须先到达** — 在 scale 变化前须有清晰的「光标在目标上」瞬间，否则按压无法归因。
- **释放使用 `back.out(${BOUNCE_FACTOR})`** — 二者需一起弹簧 overshoot。线性释放会失去触觉感。
- **内发光在按压中出现、释放时淡出** — 接触的视觉确认。外阴影缩小（压入），内发光出现（能量集中）。
- **光标 `pointer-events: none`** — 光标为装饰；若捕获事件，会破坏下方按钮的 hover/click。
- **光标 `transform-origin: 0 0`** — 箭头尖端为点击点，非中心。绕尖端缩放可稳定点击点。
- **高潮停留 ≥1 s** — 释放后合成须继续 ≥1 s。按压是一个节拍；观众需要时间看到结果。

## 关键约束

- **时间线须 paused**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **光标与按钮均勿用 CSS `transition`** — 会与 GSAP 冲突
- **光标 SVG 设置 `pointer-events: none`**
- **按钮（及可选光标）使用 `will-change: transform`**
- **`up-frame > down-frame`** — 释放必须在按下之后；否则会出现无按下的释放
- **勿使用真实 `mouseenter` / `click` 事件** — HF 为渲染上下文而非 UI；一切须通过时间线驱动

## 组合

- [press-release-spring.md](press-release-spring.md) — 仅按钮的按压变体；本规则在其上叠加光标
- [cursor-click-ripple.md](cursor-click-ripple.md) — 在点击点添加 ripple 效果
- [scale-swap-transition.md](scale-swap-transition.md) — 按压**触发**切换

## 搭配的 HF 技能

- `/hyperframes-animation` — 通过数组协调多目标 tween
- `/hyperframes-core` — 合成 wiring
- `/hyperframes-cli` — `hyperframes lint`
