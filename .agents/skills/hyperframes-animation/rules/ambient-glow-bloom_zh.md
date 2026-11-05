---
name: ambient-glow-bloom
description: 无触发的柔和径向光晕，在 hero 元素后方绽放并保持，带有限 idle 呼吸；或单次穿越表面的扫光。无点击、无词同步——只是绽放。有限、确定性、seek 安全。
metadata:
  tags: glow, bloom, ambient, radial, sweep, hero, presence, finite, un-triggered
---

# 环境光晕绽放（Ambient Glow Bloom）

一层柔和的径向光晕在 **hero 元素后方绽放**（卡片、logo、指标等）并保持，赋予其存在感。与 `press-release-spring` 的点击触发爆发或 `asr-keyword-glow` 的按词计时包络不同，此光晕 **无触发**——它随 hero 落定而绽放并保持点亮。两种形式：**hero 绽放**在落定元素后方膨胀并随后呼吸，以及 **traveling glow sweep** 将柔和高光在表面 **精确穿越一次**。二者均为有限、确定性且 seek 安全。

## 工作原理

径向渐变层位于 hero **后方**（`z-index` 低于 hero），起始 `opacity: 0`。在 bloom-in 窗口内，`opacity` 从 0 升至峰值，并配合温和的 `scale` 膨胀（光晕「充气」到位），时序与 hero 落定对齐，使二者读成同一拍。

bloom-in 之后分两种形式：

1. **Hero 绽放** — 点亮后，光晕在 hold 期间做 **有界 idle 呼吸**。用 `onUpdate` 读取 `tl.time()` 驱动（**不要**用 `repeat: -1` yoyo）：对经过时间的 `Math.sin` 在峰值附近微调 `opacity` 与 `scale`。`sin(0) = 0` 时呼吸从 bloom 的 resting 状态开始——无跳变。
2. **Traveling sweep** — 表面一端的窄高光渐变 **一次** 平移到另一端（`x` 从屏外到屏外），单次有限穿越。无循环、无回程。扫光层裁剪到表面，高光仅在重叠处可见。

峰值 opacity 保持克制（≤ ~0.45），光晕提供存在感而不洗白画面；光晕颜色应比所衬元素 **更深、更饱和**。

## HTML

```html
<div
  class="scene"
  id="bloom-scene"
  data-composition-id="bloom-scene"
  data-start="0"
  data-duration="DURATION"
  data-track-index="0"
>
  <div class="bloom-stage">
    <!-- Glow layer sits BEHIND the hero -->
    <div class="bloom-glow" id="bloom-glow"></div>
    <div class="hero-card" id="hero-card">{HeroLabel}</div>
  </div>
</div>
```

traveling-sweep 形式下，扫光层裁剪到所穿越的表面：

```html
<div class="surface" id="surface">
  <!-- grid / wordmark / card content here -->
  <div class="sweep" id="sweep"></div>
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
.bloom-stage {
  position: relative;
  display: grid;
  place-items: center;
}
.hero-card {
  position: relative;
  z-index: 2;
  width: HERO_WIDTH;
  height: HERO_HEIGHT;
  display: grid;
  place-items: center;
  background: {heroBg};
  border-radius: HERO_RADIUS;
  font-family: {font};
  font-weight: 900;
  font-size: HERO_FONT_SIZE;
  color: {heroTextColor};
}
.bloom-glow {
  /* Radial halo behind the hero — extends past it via negative inset */
  position: absolute;
  z-index: 1;
  inset: GLOW_INSET;
  background: {glowGradient};
  opacity: 0;
  transform: scale(GLOW_START_SCALE);
  transform-origin: 50% 50%;
  pointer-events: none;
  /* will-change because opacity + scale both animate during bloom AND breathe */
  will-change: transform, opacity;
}

/* Traveling-sweep form */
.surface {
  position: relative;
  overflow: hidden; /* clips the sweep to the surface footprint */
  border-radius: SURFACE_RADIUS;
}
.sweep {
  position: absolute;
  top: 0;
  bottom: 0;
  /* A narrow soft band, wider than it needs to be so the falloff is gentle */
  width: SWEEP_WIDTH;
  /* Diagonal highlight: angle the gradient so the sweep reads as raked light */
  background: {sweepGradient};
  opacity: 0;
  pointer-events: none;
  will-change: transform, opacity;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const glow = document.getElementById("bloom-glow");

  // ── Form A: HERO BLOOM ──────────────────────────────────────────────
  // Phase 1 — bloom in. opacity 0 → peak + gentle scale swell, landing on
  // the hero's settle. ease "power2.out" so it arrives soft, not snappy.
  tl.fromTo(
    glow,
    { opacity: 0, scale: GLOW_START_SCALE },
    {
      opacity: GLOW_PEAK_OPACITY,
      scale: 1,
      duration: BLOOM_DUR,
      ease: "power2.out",
    },
    BLOOM_START,
  );

  // Phase 2 — bounded idle breathe during the hold. NOT a yoyo loop:
  // a single finite tween advances `phase` 0 → 2π·CYCLES; onUpdate reads it
  // and nudges opacity + scale a hair around their peak.
  // sin(0) = 0 → breathe starts exactly at the bloom's resting state.
  const phase = { p: 0 };
  tl.to(
    phase,
    {
      p: Math.PI * 2 * BREATHE_CYCLES,
      duration: BREATHE_DUR,
      ease: "none",
      onUpdate: () => {
        const s = Math.sin(phase.p);
        glow.style.opacity = String(GLOW_PEAK_OPACITY + s * OPACITY_AMP);
        glow.style.transform = `scale(${1 + s * SCALE_AMP})`;
      },
    },
    BLOOM_START + BLOOM_DUR, // breathe begins right as the bloom settles
  );

  // ── Form B: TRAVELING SWEEP ─────────────────────────────────────────
  // A single finite pass. opacity fades in, x travels from off one edge to
  // off the other, opacity fades out as it exits. One pass — no repeat.
  const sweep = document.getElementById("sweep");
  tl.fromTo(
    sweep,
    { x: SWEEP_START_X, opacity: 0 },
    {
      x: SWEEP_END_X,
      opacity: SWEEP_PEAK_OPACITY,
      duration: SWEEP_DUR,
      ease: "none", // constant glide reads as a raking light, not an ease-in object
    },
    SWEEP_START,
  );
  // Fade the trailing edge out so it doesn't pop off at the surface edge.
  tl.to(sweep, { opacity: 0, duration: SWEEP_FADE_DUR, ease: "power1.in" }, SWEEP_FADE_START);

  window.__timelines["bloom-scene"] = tl;
</script>
```

## 变体

### Bloom-and-hold（无呼吸）

极短场景（< 3s）或 hero 已有自身 idle 时，完全跳过 Phase 2——绽放至峰值并保持平坦。单个 `fromTo` 即完整配方；光晕只是被点亮的 presence。

### Pulse-on-arrival（一次 swell，再 settle 到较低 hold）

bloom **略过**峰值，再 ease 回到稳定 hold 水平——单次呼吸强调 hero 落地，无持续循环。两个相邻 tween（状态连续，同 `press-release-spring`）：

```js
tl.fromTo(
  glow,
  { opacity: 0, scale: GLOW_START_SCALE },
  { opacity: GLOW_OVERSHOOT_OPACITY, scale: 1.06, duration: BLOOM_DUR, ease: "power2.out" },
  BLOOM_START,
);
tl.to(
  glow,
  { opacity: GLOW_HOLD_OPACITY, scale: 1, duration: SETTLE_DUR, ease: "power2.inOut" },
  BLOOM_START + BLOOM_DUR,
);
```

### Multi-hero relay（一行卡片错开 bloom）

以 stagger 为每张卡的光晕 bloom，presence 扫过整行。每个光晕的 `BLOOM_START` 偏移 `STAGGER`（约 0.15–0.3s）；按下方 concurrent-elements 规则缩小各光晕的 `OPACITY_AMP` / `SCALE_AMP`，避免 N 个呼吸光晕叠成 shimmer。

### Diagonal raked sweep（字标 sheen）

将 `{sweepGradient}` 设角度（如 105° linear gradient），让光带自左向右穿过 wordmark 或 logo lockup。读作光 rake 过表面——经典单次 logo sheen。同一单次 timeline；仅更窄的 `SWEEP_WIDTH` 与更高 `SWEEP_PEAK_OPACITY`（小目标上的 tight highlight）。

## 如何选取数值

### 光晕几何

- **GLOW_INSET** — 负 inset，使径向光晕超出 hero 边缘。
  - 范围：1920×1080 画布上 `-200` 至 `-450` px；hero 越大光晕越大
  - 效果：过小则光晕是 tight rim，而非 ambient presence
- **GLOW_START_SCALE** — bloom-in 起始 scale（光晕「充气」至 1）。
  - 范围：0.80（明显 inflation）→ 0.92（ subtle）→ 1.0（无 swell，仅 opacity bloom）
  - 约束：保持 ≤ 1.0—— swell 应长到位，而非缩小

### Bloom-in 动态

- **BLOOM_DUR** — bloom-in 时长。
  - 范围：0.6–1.4s；hero 仍在 settle 时用更长，使二者一起落地
  - 效果：更短 → 光晕「啪」地亮起；更长 → 弥漫进入（ambient 感）
- **BLOOM_START** — bloom 开始时刻。
  - 约束：对齐使 `BLOOM_START + BLOOM_DUR` ≈ hero 的 settle 帧，光晕与 hero 解析为同一拍——而非先光后卡或先卡后光
- **GLOW_PEAK_OPACITY** — 光晕峰值 opacity。
  - 范围：0.15（ subtle）→ 0.30（默认）→ 0.45（ dramatic）
  - **约束：≤ 0.45** — 更高会洗白整帧，hero 相对自身光晕失去对比

### Idle 呼吸（hero-bloom 形式）

- **BREATHE_DUR** — 呼吸 tween 长度。
  - 约束：等于 `TOTAL_DURATION − (BLOOM_START + BLOOM_DUR)`，用 motion 填满 hold
- **BREATHE_CYCLES** — 在 `BREATHE_DUR` 内的完整呼吸次数。
  - 范围：`BREATHE_DUR / 4s ≤ CYCLES ≤ BREATHE_DUR / 2.5s`（2.5–4s 呼吸周期读作慢 ambient pulse——光晕呼吸应比元素呼吸更慢）
- **OPACITY_AMP** — opacity 相对峰值的正弦幅度。
  - **默认：0.02–0.05**（几乎不可察觉的 pulse——多数场景的正确选择）
  - 约束：`GLOW_PEAK_OPACITY + OPACITY_AMP` 须保持 ≤ 0.45
- **SCALE_AMP** — 光晕 scale 的正弦幅度。
  - **默认：0.01–0.03**（光晕「呼吸」而不明显 resize）
  - 仅当光晕是短 isolated 场景中唯一 motion 时可略推高

### Traveling sweep

- **SWEEP_WIDTH** — 柔和高光带宽度。
  - 范围：表面宽度的 15–35%（宽柔带）用于 grid sheen；8–15% 用于 tight wordmark sheen
- **SWEEP_START_X / SWEEP_END_X** —  travel 端点，均在屏外。
  - 约束：start ≈ `-(SWEEP_WIDTH + edge)`，end ≈ `surfaceWidth + edge`——光带须从一侧完全屏外进入、另一侧完全屏外离开，避免在表面中段 spawn/despawn
- **SWEEP_DUR** — 单次穿越时长。
  - 范围：0.8–1.6s；一次 deliberate pass，慢到读作光、快到不 dominate
- **SWEEP_PEAK_OPACITY** — 高光 opacity。
  - 范围：0.10（ whisper sheen）→ 0.25（默认）→ 0.40（ bright rake）
  - 约束：≤ ~0.45（同一 wash 上限）；更 tight 的 sweep 可容忍高端
- **SWEEP_START / SWEEP_FADE_START / SWEEP_FADE_DUR** — pass 运行与 tail out 时机。
  - 约束：`SWEEP_FADE_START + SWEEP_FADE_DUR ≈ SWEEP_START + SWEEP_DUR`，使 opacity 在光带离开远缘时恰为 0

### Tokens

- **{glowGradient}** — radial-gradient，中心饱和向外透明。颜色应 **比 `{heroBg}` 更深、更饱和**——同色光晕会显得 washed out（同 `press-release-spring` burst 规则）。
- **{sweepGradient}** — 柔带：`transparent → highlight → transparent`。sheen 用近白或品牌 tint 低 alpha 高光；可设角度（如 `linear-gradient(105deg, …)`）作 raked 观感。
- **{heroBg} / {heroTextColor}** — 光晕所衬 hero 表面；高对比，使被点亮的 hero 在光晕前仍可读。

## 关键原则

- **设计上无触发** — 此光晕 **不** 等待点击（`press-release-spring`）或词时间戳（`asr-keyword-glow`）。它在 hero settle 时作为 ambient presence 绽放。若需 triggered burst，改用上述规则。
- **光晕在后、hero 在前** — 光晕 `z-index: 1`，hero `z-index: 2`。光晕在前会在峰值 opacity 时遮挡 hero。
- **光晕颜色比元素更深、更饱和** — 亮 hero → 深、饱和光晕。同色相同明度光晕会融进表面。
- **光晕与 hero 落地为同一拍** — 将 `BLOOM_START + BLOOM_DUR` 对齐 hero settle。光晕早于或晚于卡片读作两事件；同时到达读作卡片「上电」。
- **克制峰值——默认偏低。** 多数场景 `GLOW_PEAK_OPACITY` 0.15–0.30；0.45 为硬上限。 consciously 注意到的光晕过强——应读作 hero 有重量，而非可见光源。
- **呼吸有界，永不 loop** — idle pulse 是有限 `onUpdate` tween 读 `tl.time()`（经 `phase` 代理），非 `repeat: -1` / `yoyo`。`sin(0) = 0` 表示从 bloom resting 无跳变开始。（同 `sine-wave-loop` 理由：无限/CSS loop 与 HF seek 时钟 desync。）
- **Sweep 仅一次 pass** — traveling highlight 从一侧屏外进入、另一侧屏外离开，单次。无回程、无 loop。重复 sweep 读作 loading shimmer，非一次性 reveal accent。
- **并发光晕叠加** — 一行 N 个呼吸光晕会累加。每光晕 `OPACITY_AMP`、`SCALE_AMP` ≤ 默认 `/ √N`，并错开呼吸周期（2.6s / 2.9s / 3.3s）避免 lockstep pulse。（同 `sine-wave-loop` concurrent-elements 的 `/√N` 纪律。）
- **勿将 hero 上 `boxShadow` glow 与此光晕层并用** — 在 layout pipeline 中竞争，结果 muddy。光晕放在专用 `.bloom-glow` 层，而非 hero shadow。

## 关键约束

- **Timeline 须 paused**：`gsap.timeline({ paused: true })`
- **Registry key = `data-composition-id`**
- **光晕 / sweep 上无 CSS `transition`** — 独立于 HF seek 插值并 flicker
- **无 `repeat` / `yoyo` / `repeat: -1`** — 呼吸为有界有限 tween；sweep 为一次 pass
- **无 `Math.random` / `Date.now`** — 呼吸 phase 确定性（固定 duration 上的 `phase.p`）
- **仅 GSAP transform 别名**：`x`、`y`、`scale`、`rotation` — 加 `opacity` / `filter`。勿 tween `width` / `height` / `left` / `top`（光晕 swell 用 `scale`，sweep travel 用 `x`）。
- **光晕上 `will-change: transform, opacity`** — bloom-in 与呼吸均动画二者
- **光晕峰值 `opacity ≤ 0.45`** — 更高洗白 composition
- **Sweep 端点完全屏外** — 光带须在裁剪边缘外进入与离开，避免 mid-frame spawn/despawn

## 组合

- [sine-wave-loop.md](sine-wave-loop.md) — hero-bloom 形式与 hero 元素自身 sine 呼吸配对；光晕呼吸 opacity，hero 呼吸 scale/y，略错相作 layered「alive」hold
- [press-release-spring.md](press-release-spring.md) — 姊妹规则：该规则的 `bg-glow` **点击触发**，本规则无触发。勿在同一元素后同时运行
- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 在 count-up settle 时为 hero 统计卡 bloom accent 光晕（`dataviz-countup` blueprint 的「soft accent glow blooms behind the hero metric」拍）
- [stat-bars-and-fills.md](stat-bars-and-fills.md) — hero 指标与其配对图形一起落地时在其后 bloom 光晕
- [center-outward-expansion.md](center-outward-expansion.md) — 布局 resolve 后对 assembled layout 运行一次 traveling-sweep（`grid-card-assemble` blueprint 的「traveling-glow sweep across the assembled grid」）

## 与 HF skills 配对

- `/hyperframes-animation` — `onUpdate` 写 opacity/transform + 有界 sine 呼吸
- `/hyperframes-core` — composition 接线
- `/hyperframes-cli` — `hyperframes lint`
