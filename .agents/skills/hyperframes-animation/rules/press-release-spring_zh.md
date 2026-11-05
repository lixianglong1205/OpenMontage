---
name: press-release-spring
description: 触感式按钮按压：线性压缩、基于弹簧的弹性回弹，以及分层视觉反馈（阴影收缩 + 释放爆发 + 背景光晕）。
metadata:
  tags: spring, press, interaction, button, physics, glow, burst, ui
---

# 按压-释放弹簧链

将输入（线性压缩）与输出（弹簧回弹）分离，以营造触感。 overshoot（过冲）是弹簧配置的自然结果，而非手写代码。在同一触发帧上叠加次级动效（阴影收缩、释放爆发、背景光晕）。

## 工作原理

在 **释放** 时刻分为两个独立阶段：

1. **按压**：线性 ease → 压缩（`scale: 1 → PRESS_SCALE`，阴影收缩）。使用线性而非弹簧——下压必须读作即时/触感，而非软绵绵的挤压。
2. **释放**：`back.out(${BOUNCE_FACTOR})` 弹簧 → 弹性弹回 `1.0`（过冲幅度与 `BOUNCE_FACTOR` 成正比）。可选的爆发光晕环在按钮后方扩散；可选的背景环境光晕淡入。

状态连续至关重要：释放 tween 的起始值必须等于按压 tween 的结束值，否则弹簧会跳到错误位置。当两条 tween 在同一时间轴上相邻位置、针对同一属性时，GSAP 会自动衔接。

## HTML

```html
<div
  class="scene"
  id="press-scene"
  data-composition-id="press-scene"
  data-start="0"
  data-duration="DURATION"
  data-track-index="0"
>
  <div class="press-stage">
    <div class="bg-glow" id="bg-glow"></div>
    <div class="burst" id="burst"></div>
    <button class="btn" id="btn">{buttonLabel}</button>
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
.press-stage {
  position: relative;
  display: grid;
  place-items: center;
}
.btn {
  position: relative;
  z-index: 2;
  /* Visual weight: ≥4% of canvas for the press to read on a 1080p frame */
  width: BTN_WIDTH;
  height: BTN_HEIGHT;
  background: {btnBg};
  border: none;
  border-radius: BTN_RADIUS;
  font-family: {font};
  font-weight: 900;
  font-size: BTN_FONT_SIZE;
  letter-spacing: BTN_LETTER_SPACING;
  color: {btnTextColor};
  text-transform: uppercase;
  /* Anchor compression on the center — see Critical Constraints */
  transform-origin: 50% 50%;
  /* Initial floating shadow — large + diffuse */
  box-shadow: {btnRestShadow};
}
.burst {
  /* Sits BEHIND the button, same footprint */
  position: absolute;
  z-index: 1;
  inset: 0;
  width: BTN_WIDTH;
  height: BTN_HEIGHT;
  background: {burstGradient};
  filter: blur(BURST_BLUR);
  opacity: 0;
  transform: scale(1);
  pointer-events: none;
}
.bg-glow {
  /* Full-stage radial — extends beyond the stage with negative inset */
  position: absolute;
  inset: BG_GLOW_INSET;
  background: {bgGlowGradient};
  opacity: 0;
  pointer-events: none;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Phase 1 — press (linear compression)
  tl.to(
    "#btn",
    {
      scale: PRESS_SCALE,
      boxShadow: "{btnPressedShadow}",
      duration: PRESS_DUR,
      ease: "power1.in",
    },
    PRESS_START,
  );

  // Phase 2 — release (spring back with overshoot)
  // CRITICAL: start scale == end of phase 1 (PRESS_SCALE) to maintain state continuity.
  tl.to(
    "#btn",
    {
      scale: 1,
      boxShadow: "{btnRestShadow}",
      duration: RELEASE_DUR,
      ease: `back.out(${BOUNCE_FACTOR})`,
    },
    RELEASE_START,
  );

  // Phase 3 — burst glow (radial pop behind button), triggered with release
  tl.fromTo(
    "#burst",
    { scale: 1, opacity: 0 },
    {
      scale: BURST_PEAK_SCALE,
      opacity: BURST_PEAK_OPACITY,
      duration: BURST_GROW_DUR,
      ease: "power2.out",
    },
    RELEASE_START,
  );
  // Burst then fades out
  tl.to("#burst", { opacity: 0, duration: BURST_FADE_DUR, ease: "power2.in" }, BURST_FADE_START);

  // Phase 4 — background environmental glow fades in after release
  tl.to(
    "#bg-glow",
    {
      opacity: BG_GLOW_PEAK_OPACITY,
      duration: BG_GLOW_FADE_DUR,
      ease: "power2.out",
    },
    RELEASE_START,
  );

  window.__timelines["press-scene"] = tl;
</script>
```

## 变体

### 轻量按压（保存状态 / 低调 CTA）

压缩更小、过冲更柔、爆发更弱。`PRESS_SCALE` 取范围高端（约 0.96），`BOUNCE_FACTOR` 取低端（约 1.4），降低 `BURST_PEAK_SCALE` 与 `BURST_PEAK_OPACITY`。

### 强烈按压（主 CTA /「发布」时刻）

压缩更深、过冲更大、爆发更强。`PRESS_SCALE` 取范围低端（约 0.88），`BOUNCE_FACTOR` 取高端（约 2.5），`BURST_PEAK_SCALE` 与 `BURST_PEAK_OPACITY` 拉满。

### 按压期间变色

按压中段加深按钮色，释放时恢复。与 scale tween 相同的时间轴位置——在 `#btn` 上插值 `backgroundColor`。状态连续规则仍适用：释放颜色 tween 的起始等于按压颜色 tween 的结束。

```js
tl.to("#btn", { backgroundColor: "{btnPressedColor}", duration: PRESS_DUR }, PRESS_START);
tl.to("#btn", { backgroundColor: "{btnRestColor}", duration: RELEASE_DUR }, RELEASE_START);
```

### 释放时状态变更（批准 / 确认模式）

当按压表示确认时，在 `RELEASE_START` 将按钮 resting 色换为 success token（而非回到 `{btnRestColor}`），并在同一位置用单独的 `back.out(${CHECK_BOUNCE})` tween 弹出对勾。按钮进入终态——不再预期后续按压。

```js
tl.to("#btn", { backgroundColor: "{successColor}", duration: RELEASE_DUR }, RELEASE_START);
tl.to(
  ".btn-check",
  { scale: 1, duration: CHECK_POP_DUR, ease: `back.out(${CHECK_BOUNCE})` },
  RELEASE_START,
);
```

## 如何选取数值

### 几何

- **BTN_WIDTH / BTN_HEIGHT** — 按钮 footprint。
  - 范围：按钮面积 ≥ 画布的 3–5%（1080p 下 320×68 约 1%，视觉上几乎读不出）
  - 效果：更小 → 按压几乎不可见；更大 → 按压占满画面
  - 约束：`BTN_WIDTH × BTN_HEIGHT / (canvasW × canvasH) ≥ 0.03`
- **BTN_RADIUS** — 圆角半径。
  - 范围：`BTN_HEIGHT × 0.15`（锐利/现代）→ `BTN_HEIGHT / 2`（药丸形）
- **BTN_FONT_SIZE / BTN_LETTER_SPACING** — 字重感。
  - 范围：`BTN_FONT_SIZE ≈ BTN_HEIGHT × 0.4-0.5`；字间距 4–10 px 读作「可行动标签」

### 按压动力学

- **PRESS_SCALE** — 压缩深度。
  - 范围：0.88（dramatic）→ 0.92（默认）→ 0.96（subtle）
  - 效果：更低 → 更触感/更重；更高 → 几乎只是轻触确认
  - 约束：勿 <0.85（像坏了）或 >0.98（看不出下压）
- **PRESS_DUR** — 压缩时长。
  - 范围：0.10–0.30 s
  - 效果：更短 → 更利落/「即时感」；更长 → 慢速挤压
  - 约束：短于 `RELEASE_DUR`（输入快于弹簧回弹）
- **RELEASE_DUR** — 弹簧回弹时长。
  - 范围：0.40–0.90 s
  - 效果：更短 → 紧凑 pop；更长 → 松散、晃悠落定
- **BOUNCE_FACTOR** — `back.out(BOUNCE_FACTOR)` 过冲强度。
  - 范围：1.4（柔和）→ 2.0（坚实 pop）→ 2.8（卡通感）
  - 效果：低端几乎不过冲；高端偏卡通；凭手感调
  - 替代：改用 `elastic.out(amplitude, period)` 得到橡胶式振荡而非单次过冲
- **PRESS_START / RELEASE_START** — 时间轴位置。
  - 约束：`RELEASE_START = PRESS_START + PRESS_DUR`（状态连续——见 Critical Constraints）

### 爆发光晕

- **BURST_PEAK_SCALE** — 径向 pop 最大 scale。
  - 范围：3（subtle）→ 6（默认）→ 8（dramatic）
  - 约束：≤ ~8——再大径向渐变会明显像素化
- **BURST_PEAK_OPACITY** — 爆发峰值不透明度。
  - 范围：0.4（subtle）→ 0.8（默认）→ 1.0（dramatic）
- **BURST_GROW_DUR / BURST_FADE_DUR** — 增长 vs. 淡出 timing。
  - 范围：各 0.4–0.7 s；默认 grow ≈ fade
- **BURST_BLUR** — 爆发层高斯 blur。
  - 范围：40–100 px；更小像硬环，更大像环境雾

### 背景光晕

- **BG_GLOW_PEAK_OPACITY** — 环境光峰值。
  - 范围：0.1（subtle）→ 0.25（默认）→ 0.45（dramatic）
  - 约束：≤ 0.45——更高会 wash 整幅构图
- **BG_GLOW_FADE_DUR** — 淡入时长。
  - 范围：0.6–1.0 s
- **BG_GLOW_INSET** — 负 inset，使径向超出 stage 边缘。
  - 范围：1920×1080 画布上通常 `-300` 至 `-500` px

### 可选「批准」变体

- **CHECK_BOUNCE** — 对勾 pop 过冲。
  - 范围：1.4–2.0；比按钮主 `BOUNCE_FACTOR` 更硬，读作 punctuation 式「盖章」
- **CHECK_POP_DUR** — 对勾 scale-up 时长。
  - 范围：0.3–0.6 s

### Tokens

- **{btnBg} / {btnRestColor} / {btnPressedColor}** — 主按钮表面；按压态比 resting 更深
- **{btnRestShadow} / {btnPressedShadow}** — resting 阴影大且 diffuse；按压小且 tight（按钮「沉向表面」）
- **{burstGradient}** — 径向；中心饱和、向外透明（颜色应比 `{btnBg}` 更深更饱和——同色光晕会发灰）
- **{bgGlowGradient}** — 全 stage 径向，`{btnBg}` 色相族的低不透明度 tint
- **{successColor}** — 确认绿 / 品牌 success，用于批准变体

## 核心原则

- **状态连续** — 释放起始值 MUST 与按压结束值完全一致。GSAP 时间轴上，当两条 tween 在相邻时刻针对同一属性时，前一条的结束值自动成为后一条的起始。
- **视觉重量** — 按钮面积应 **≥ 画布的 3–5%**。更小则按压在视觉上无足轻重。
- **线性按压、弹簧释放** — 压缩用 `power1.in/out`，回弹用 `back.out`。双弹簧 → 软绵；双线性 → 机械/无过冲 punch。
- **以中心为压缩锚点** — `transform-origin: 50% 50%`（默认）。否则按钮不对称塌陷。
- **爆发在后方，不在前方** — burst `z-index: 1`，按钮 `z-index: 2`。爆发在前会遮挡峰值不透明度下的按钮。
- **光晕色比元素更深更饱和** — 亮表面 → 深、饱和光晕。同色光晕发灰。
- **勿在同一元素上同时 tween `boxShadow` 与 `filter`** — 在 layout pipeline 中竞争；二选一。阴影在按钮，blur 在独立 burst 层。
- **高潮节拍需要 dwell** — 爆发峰值 + 标签/字标 reveal 后，构图结束前须再跑 **≥1s**（dramatic 变体 **≥2s**）。在 `t=DURATION−0.2s` reveal 会读成「闪一下就没了」。

## 关键约束

- **时间轴必须 paused**：`gsap.timeline({ paused: true })`
- **Registry key = `data-composition-id`**
- **按钮上无 CSS `transition`** — 会与 HF seek 独立插值并引起 flicker
- **与其他动画层叠加时对按钮使用 `will-change: transform`**
- **`RELEASE_START = PRESS_START + PRESS_DUR`** — 同一属性上的相邻才是状态连续自动化的原因；间隙或重叠会破坏
- **Burst 最大 scale ≤ ~8** — 再大径向渐变明显像素化
- **背景光晕 `opacity ≤ 0.45`** — 更高会 wash 整幅构图
- **仅 GSAP transform 别名**：`x`、`y`、`scale`、`rotation`。勿 tween `width` / `height` / `left` / `top`。

## 组合

- [sine-wave-loop.md](sine-wave-loop.md) — 按压前按钮 idle 微浮动（轻微呼吸，传达「就绪」）
- [center-outward-expansion.md](center-outward-expansion.md) — 与按压释放同步的 badge 向外爆发
- [cursor-click-ripple.md](cursor-click-ripple.md) — 触发按压的光标点击

## 搭配的 HF skills

- `/hyperframes-animation` — `back.out` ease + 多 tween 协调
- `/hyperframes-core` — composition 接线
- `/hyperframes-cli` — `hyperframes lint`
