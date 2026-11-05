---
name: svg-icon-enrichment
description: 为 SVG 内部元素添加动画（旋转指针、开合刀片、脉冲圆点、虚线流动），在不替换图标的前提下让图标更有生命力。
metadata:
  tags: svg, icon, animation, internal, micro-animation, pulse, rotation
---

# SVG 图标丰富化

将 SVG 图标视为由多个可动画 **部件** 组成的整体，而非一张不透明的位图。每个有意义的内部元素（时针、剪刀刃、录制圆点、数据线等）各自绑定 GSAP 驱动的微动画。与 [svg-path-draw](svg-path-draw.md)（描边轮廓绘制）不同——丰富化针对 **内部部件** 动画，理想情况下在轮廓绘制完成后再启动。

## 工作原理

SVG 应预先为 `<line>`、`<circle>`、`<path>` 或 `<g>` 等子元素命名。GSAP 时间轴通过选择器定位这些元素，并应用以下 4 种典型运动模式之一：

1. **旋转（Rotation）** — 时针、齿轮、加载指示器（`transform: rotate(deg)`）
2. **振荡（Oscillation）** — 剪刀刃、翅膀扇动、开关（对向分组上 `transform: rotate(±sin*amp)`）
3. **脉冲（Pulse）** — 录制圆点、心形、通知（通过 sin 驱动 `scale + opacity`）
4. **虚线流动（Dash flow）** — 沿描边移动的虚线，类似数据流（线性 `strokeDashoffset`）

均在已暂停的 GSAP 时间轴内运行，以便 HyperFrames（HF）可确定性地 seek。

## HTML

```html
<div
  class="scene"
  data-composition-id="enrichment-scene"
  data-start="0"
  data-duration="4"
  data-track-index="0"
>
  <div class="stack">
    <div class="row">
      <!-- Clock icon — minute hand rotates -->
      <svg class="icon-svg" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <circle cx="60" cy="60" r="50" fill="none" stroke="{accentColor}" stroke-width="6" />
        <line
          class="clock-hand"
          id="hand-min"
          x1="60"
          y1="60"
          x2="60"
          y2="22"
          stroke="{textColor}"
          stroke-width="6"
          stroke-linecap="round"
        />
        <line
          class="clock-hand"
          id="hand-sec"
          x1="60"
          y1="60"
          x2="60"
          y2="30"
          stroke="{recordColor}"
          stroke-width="3"
          stroke-linecap="round"
        />
        <circle cx="60" cy="60" r="6" fill="{textColor}" />
      </svg>

      <!-- Recording dot — pulses -->
      <svg class="icon-svg" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <circle
          id="rec-ring"
          cx="60"
          cy="60"
          r="50"
          fill="none"
          stroke="{recordColor}"
          stroke-width="4"
        />
        <circle id="rec-dot" cx="60" cy="60" r="22" fill="{recordColor}" />
      </svg>

      <!-- Data stream — dashes flow along the line -->
      <svg class="icon-svg" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect
          x="14"
          y="48"
          width="92"
          height="24"
          rx="12"
          fill="none"
          stroke="{accentColor}"
          stroke-width="4"
        />
        <line
          id="data-flow"
          x1="14"
          y1="60"
          x2="106"
          y2="60"
          stroke="{accentColor}"
          stroke-width="6"
          stroke-linecap="round"
          stroke-dasharray="14 12"
        />
      </svg>
    </div>
    <div class="brand">{brandPhrase}</div>
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
  gap: 80px;
}
.row {
  display: flex;
  gap: 120px;
}
.icon-svg {
  width: 320px;
  height: 320px;
  filter: drop-shadow(0 12px 32px {shadowColor});
}
.clock-hand {
  /* transform-origin in SVG must be in viewBox units, not pixels */
  transform-origin: 60px 60px;
  transform-box: fill-box;
}
.brand {
  font-size: 64px;
  font-weight: 900;
  letter-spacing: 14px;
  text-transform: uppercase;
  color: {textColor};
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Pattern 1 — Rotation (clock hands)
  // Minute hand: MIN_REVOLUTIONS full rotations over TOTAL_DURATION
  const minState = { deg: 0 };
  tl.to(
    minState,
    {
      deg: 360 * MIN_REVOLUTIONS,
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        document.getElementById("hand-min").style.transform = `rotate(${minState.deg}deg)`;
      },
    },
    0,
  );

  // Second hand: SEC_REVOLUTIONS full rotations over TOTAL_DURATION (faster)
  const secState = { deg: 0 };
  tl.to(
    secState,
    {
      deg: 360 * SEC_REVOLUTIONS,
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        document.getElementById("hand-sec").style.transform = `rotate(${secState.deg}deg)`;
      },
    },
    0,
  );

  // Pattern 2 — Pulse (recording dot, ring opacity inverse)
  const pulseState = { p: 0 };
  tl.to(
    pulseState,
    {
      p: Math.PI * 2 * PULSE_CYCLES,
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        const dotScale = 1 + Math.sin(pulseState.p) * PULSE_DOT_AMP;
        const ringScale = 1 + Math.sin(pulseState.p + Math.PI / 2) * PULSE_RING_AMP;
        const ringOpacity =
          PULSE_RING_OPACITY_BASE + Math.sin(pulseState.p) * PULSE_RING_OPACITY_AMP;
        const dot = document.getElementById("rec-dot");
        const ring = document.getElementById("rec-ring");
        dot.style.transform = `scale(${dotScale})`;
        dot.style.transformOrigin = "60px 60px";
        ring.style.transform = `scale(${ringScale})`;
        ring.style.transformOrigin = "60px 60px";
        ring.style.opacity = String(ringOpacity);
      },
    },
    0,
  );

  // Pattern 3 — Dash flow (data stream)
  const flowState = { offset: 0 };
  tl.to(
    flowState,
    {
      offset: DASH_FLOW_TOTAL_OFFSET, // negative for L→R flow, positive for R→L
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        document.getElementById("data-flow").style.strokeDashoffset = String(flowState.offset);
      },
    },
    0,
  );

  // Brand fades in early
  tl.from(".brand", { opacity: 0, y: 16, duration: 0.6, ease: "power3.out" }, BRAND_AT);

  window.__timelines["enrichment-scene"] = tl;
</script>
```

## 如何选取参数

- **MIN_REVOLUTIONS** — 分针在 TOTAL_DURATION 内的完整旋转圈数
  - 范围：0.5–2.0（连续；更快读起来像延时摄影）
  - 约束：若末帧可见性重要，避免整数圈数（否则会回到起始姿态）

- **SEC_REVOLUTIONS** — 秒针在 TOTAL_DURATION 内的完整旋转圈数
  - 范围：4–10（应明显快于分针）
  - 约束：SEC_REVOLUTIONS > MIN_REVOLUTIONS × 3，速度差才读得出来

- **PULSE_CYCLES** — 在 TOTAL_DURATION 内的脉冲周期数
  - 范围：3–5 秒成片上约 2–4 次
  - 效果：≥ 5 像焦虑闪烁；≤ 1 像被遗忘

- **PULSE_DOT_AMP** — 圆点缩放幅度
  - 范围：0.05–0.20
  - 效果：0.05 = 呼吸感；0.20 = 搏动

- **PULSE_RING_AMP** — 外环缩放幅度（通常低于 DOT_AMP）
  - 范围：0.04–0.12
  - 约束：须 < PULSE_DOT_AMP，否则外环压过圆点

- **PULSE_RING_OPACITY_BASE / PULSE_RING_OPACITY_AMP** — 外环不透明度基线 + 正弦幅度
  - 范围：BASE 0.4–0.6；AMP 0.3–0.5
  - 约束：BASE − AMP ≥ 0 且 BASE + AMP ≤ 1

- **DASH_FLOW_TOTAL_OFFSET** — TOTAL_DURATION 内 stroke-dashoffset 的总变化量
  - 范围：−400 至 −100（左→右为负）或 +100 至 +400（右→左）
  - 效果：|大| = 快流；|小| = 慢漂
  - 约束：须为虚线周期（dash + gap）的整数倍，否则循环末帧会出现相位跳变

- **BRAND_AT** — 品牌文案淡入时刻
  - 范围：0.3–1.0 s
  - 效果：过早与图标入场抢戏；过晚像后贴上去的

- **缓动族选择**：旋转 = `none`（线性运动才是要点）；脉冲驱动 = `none`（正弦负责曲线）；品牌 reveal = `power3.out`

## 典型运动模式

| 模式 | 适用场景 | 数学 | 提示 |
| ----------- | ---------------------------------- | ------------------------------------------------ | ----------------------------------- |
| Rotation | 时钟、齿轮、加载器、表盘 | `transform: rotate(deg)`，通过秒计数线性驱动 | `transform-origin` 用 viewBox 单位 |
| Oscillation | 剪刀、翅膀、开关 | 对向分组上 `rotate(±sin*amp)` | 两部分符号相反 |
| Pulse | 录制圆点、心形、通知 | `scale(1 + sin*amp)` + opacity | 外环比圆点滞后 π/2 形成涟漪 |
| Dash flow | 切割线、数据流 | 随时间线性 `strokeDashoffset` | 左→右为负，右→左为正 |

## 变体

### 描边绘制 → 丰富化链式

先用 [svg-path-draw](svg-path-draw.md) 绘制图标轮廓，再启动丰富化。内部动画像「图标组装完成后被唤醒」。

```js
// Phase 1: outline draws (0 → OUTLINE_DUR)
tl.fromTo(
  "#icon-outline",
  { strokeDashoffset: 360 },
  { strokeDashoffset: 0, duration: OUTLINE_DUR, ease: "power2.inOut" },
  0,
);
// Phase 2: enrichment starts at OUTLINE_DUR
```

### 逐图标入场错开

一行图标都在动时，错开它们的入场。每个图标的丰富化在其淡入时才开始，而非同步——更有机。

## 关键原则

- **❗ 在 SVG 内绕显式点旋转时，使用 SVG 的 `transform` 属性，不要用 CSS transform** — `el.setAttribute('transform', `rotate(${deg} ${cx} ${cy})`)`。CSS 组合 `transform: rotate(...)` + `transform-origin: 60px 60px` + `transform-box: fill-box` 会把原点解释在元素 **自身 bbox 局部坐标** 中，而非 viewBox 坐标。对细 `<line>`（bbox 仅为窄包络）而言，bbox 局部的 `60 60` 会落在直线外，指针会沿偏心弧飞转而非原地旋转。小型内部形状（如 rec-dot，bbox 是小圆而非整幅 viewBox）同样踩坑。
- **在 SVG 内绕中心点缩放时**，使用 `el.setAttribute('transform', `translate(${cx} ${cy}) scale(${s}) translate(-${cx} -${cy})`)`。原因相同——避开 CSS bbox 局部原点陷阱。
- **连续动画必须在时间轴内运行** — 禁止 CSS `@keyframes` 或 `requestAnimationFrame`。二者都会与 HF 逐帧 seek 不同步。
- **幅度宜 subtle** — 图标是装饰，不是主标题。脉冲缩放遵循上文范围；旋转速度按成片长度校准，而非绝对时间。
- **同一图标多部件相位不同** — 时钟分针与秒针不同速，外环与圆点脉冲相差 π/2。完全同步显得机械；相位差显得有生命。
- **❗ 高潮停留 ≥ 1 s** — 若丰富化是主节拍，最戏剧化时刻之后成片须再持续 ≥ 1 s。

## 关键约束

- **时间轴必须 paused**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **SVG 子元素禁止 CSS `animation`** — 必须由时间轴驱动
- **每个子元素的 `transform-origin` 须单独设置**
- **流动/虚线描边使用 `stroke-linecap: round`**，虚线边缘更干净
- **按 id 定位 SVG 子元素** — `document.getElementById` 即可；链进 `<svg>` 的选择器与 HTML 等价

## 组合

- [svg-path-draw.md](svg-path-draw.md) — 先画轮廓，再激活丰富化
- [orbit-3d-entry.md](orbit-3d-entry.md) — 轨道上的项为丰富化图标（时钟绕品牌标签公转）
- [sine-wave-loop.md](sine-wave-loop.md) — 整图标浮动，内部部件仍在动

## 与 HF 技能搭配

- `/hyperframes-animation` — onUpdate 逐 SVG 子元素写 transform/opacity
- `/hyperframes-core` — 成片 wiring
- `/hyperframes-cli` — `hyperframes lint`
