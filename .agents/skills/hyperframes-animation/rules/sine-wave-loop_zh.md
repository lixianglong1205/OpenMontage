---
name: sine-wave-loop
description: 有界正弦驱动的 idle——在已定格元素上做轻微抖动，或仅在确有需要时对单个元素做有界环境呼吸。弱化说明：用循环缩放当「活感」很廉价；优先采用与旁白同步的逐段揭示，再考虑轻微抖动，最后才用到本规则。
metadata:
  tags: idle, jitter, bounded-ambient, sine, trigonometry, low-amplitude, post-entry
---

# 正弦波循环（轻微抖动 / 有界环境动效）

> **最后再考虑本规则。** 依据动效原则（`references/motion-language.md`）：**循环呼吸——把文字/卡片放大缩小来显得「有生命」——廉价、是 agent 的条件反射式偷懒，观感也弱。**「宁可没有动效，也不要糟糕的动效。」在用本规则让定格画面保持活感之前，优先 (1) **与旁白同步的逐段揭示**——旁白说到哪一行/哪一元素时再揭示，覆盖场景后段约 50%；那才是填充镜头的做法，而不是环境动效。若画面确实已落定仍需要一点生气，**认可的做法是轻微抖动**——小幅、低振幅抖动（本规则，振幅取范围低端）。完整的呼吸循环仅留给极少数「单个定格 hero 确需有界环境动效」的情况；保持弱化、幅度要小。

避免已落定元素显得死板——通过 **轻微抖动**，或极少情况下单次有界环境呼吸——用有限 timeline tween 驱动的 `Math.sin` 实现。这是动效词汇里「轻微抖动」的实现；**不是**给每个 hero 都加呼吸的许可。

## 工作原理

一段长 tween 将 `phase` 从 0 推进到 2π（或 0 到其整数倍）。每次 `onUpdate` 时，phase 输入 `Math.sin()`，得到小幅周期偏移，叠加到元素的 transform（`scale`、`translateY`、`rotate`）上。

从入场到 idle「无跳变」的要点：在 `phase = 0` 时，`sin(0) = 0`——偏移为零，元素处于入场后的静止状态。

## HTML

```html
<div
  class="scene"
  id="idle-scene"
  data-composition-id="idle-scene"
  data-start="0"
  data-duration="6"
  data-track-index="0"
>
  <div class="stack">
    <div class="hero" id="hero">{HeroLabel}</div>
    <div class="dot" id="dot"></div>
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
}
.stack {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: STACK_GAP;
}
.hero {
  font-family: {font};
  font-weight: 900;
  font-size: HERO_FONT_SIZE;
  letter-spacing: HERO_LETTER_SPACING;
  color: {textColor};
  text-transform: uppercase;
  /* Element gets its post-entry resting transform; idle only ADDS to it */
  will-change: transform;
}
.dot {
  width: DOT_SIZE;
  height: DOT_SIZE;
  border-radius: 50%;
  background: {accentColor};
  box-shadow: {accentGlow};
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const hero = document.getElementById("hero");
  const dot = document.getElementById("dot");

  // Phase 1 — entry beat (e.g. headline fade-up)
  tl.fromTo(
    hero,
    { opacity: 0, y: ENTRY_Y, scale: ENTRY_SCALE },
    { opacity: 1, y: 0, scale: 1, duration: ENTRY_DUR, ease: "power3.out" },
    0,
  );
  tl.fromTo(
    dot,
    { opacity: 0, scale: 0 },
    { opacity: 1, scale: 1, duration: DOT_ENTRY_DUR, ease: `back.out(${BOUNCE_FACTOR})` },
    DOT_ENTRY_START,
  );

  // Phase 2 — idle breathing. Starts at IDLE_START_TIME AFTER entry settles.
  // Drive a phase 0 → 2π * CYCLES via a single tween, write sin() into transforms.

  const phase = { p: 0 };
  tl.to(
    phase,
    {
      p: Math.PI * 2 * CYCLES,
      duration: IDLE_DUR,
      ease: "none",
      onUpdate: () => {
        // Hero: scale breathes ±SCALE_AMP, y bobs ±Y_AMP_PX
        const scale = 1 + Math.sin(phase.p) * SCALE_AMP;
        const y = Math.sin(phase.p) * Y_AMP_PX;
        hero.style.transform = `translateY(${y}px) scale(${scale})`;

        // Dot: out-of-phase scale (offset by π/2) — feels alive vs synced
        const dotScale = 1 + Math.sin(phase.p + Math.PI / 2) * DOT_SCALE_AMP;
        dot.style.transform = `scale(${dotScale})`;
      },
    },
    IDLE_START_TIME,
  );

  window.__timelines["idle-scene"] = tl;
</script>
```

## 变体

### 多频率叠加（有机多八度呼吸）

叠加多个频率比纯正弦更有生命感：

```js
const primary = Math.sin(phase.p) * SCALE_AMP_PRIMARY;
const secondary = Math.sin(phase.p * OCTAVE_RATIO) * SCALE_AMP_SECONDARY; // higher-frequency overlay
const scale = 1 + primary + secondary;
```

### 条件启用（仅在入场落定后）

若入场可交互或可跳过，对 idle 加门控：

```js
const idleActive = entryProgress >= GATE_THRESHOLD;
const scale = idleActive ? 1 + Math.sin((time - IDLE_START_TIME) / PERIOD) * SCALE_AMP : 1;
```

### 落定并淡出（长 idle 门控——当 `IDLE_DUR > 6s` 时强烈建议）

用包络把振幅在 idle 最后约 20% 内淡出到零，使场景在场景间过渡前明显落定：

```js
const phase = { p: 0 };
const FADE_FRAC = 0.2; // last 20% of idle = amplitude ramps to 0
tl.to(
  phase,
  {
    p: Math.PI * 2 * CYCLES,
    duration: IDLE_DUR,
    ease: "none",
    onUpdate: () => {
      const t = phase.p / (Math.PI * 2 * CYCLES); // 0 → 1 across idle
      const env = t < 1 - FADE_FRAC ? 1 : (1 - t) / FADE_FRAC; // 1 → 0 in tail
      const scale = 1 + Math.sin(phase.p) * SCALE_AMP * env;
      const y = Math.sin(phase.p) * Y_AMP_PX * env;
      hero.style.transform = `translateY(${y}px) scale(${scale})`;
    },
  },
  IDLE_START_TIME,
);
```

元素在 idle 前 80% 仍在动，最后 20% 静止。与 break-boundary Tier-B 过渡自然搭配（淡出/推入开始时，离场画面已是静态）。

### 周期与循环数学

若要精确 N 秒一个循环：

```js
const divisor = (idleDurationSec * fps) / (Math.PI * 2);
const value = Math.sin(frame / divisor) * amplitude;
```

在 HF 中（`onUpdate` 不直接暴露 frame），用 tween 的 `phase`：在 `duration: idleDurationSec` 内驱动 `p: Math.PI * 2 * cyclesWanted`。

## 如何选取数值

### 布局 / 版式

- **STACK_GAP** — hero 与 dot 之间的垂直间距。
  - 范围：0.2-0.4× `HERO_FONT_SIZE`
- **HERO_FONT_SIZE / HERO_LETTER_SPACING** — 版式强调。
  - 范围：全幅构图 100-240 px；字距 0.04-0.06em
- **DOT_SIZE** —  accent 指示点尺寸。
  - 范围：约 0.15-0.25× `HERO_FONT_SIZE`，使 dot 读作 accent 而非同级元素
- **{accentGlow}** — dot 上的 `box-shadow` 光晕；通常为 `0 0 (DOT_SIZE) rgba(accentColor, 0.5-0.7)`

### 入场阶段

- **ENTRY_Y / ENTRY_SCALE** — 淡入上升前的初始状态。
  - 范围：`ENTRY_Y` 16-32 px（轻微上升），`ENTRY_SCALE` 0.94-0.98（轻微放大）
- **ENTRY_DUR** — hero 淡入上升时长。
  - 范围：0.6-1.2s；更大的 hero 需要更长落定
- **DOT_ENTRY_START** — dot 相对 hero 弹入的时刻。
  - 约束：通常 `≈ 0.4-0.6× ENTRY_DUR`，使 dot 在 hero 仍在落定过程中出现，而非之后
- **DOT_ENTRY_DUR** — dot back-out 弹入时长。
  - 范围：0.4-0.7s
- **BOUNCE_FACTOR** — dot 弹入上 `back.out(BOUNCE_FACTOR)` 的过冲强度。
  - 范围：1.4（柔和）→ 2.0（有力）→ 2.8（卡通）

### Idle 阶段

- **IDLE_START_TIME** — 呼吸开始时刻。
  - 约束：`≥ ENTRY_DUR + 小缓冲（约 0.1s）`，避免与入场尾部打架。此刻 `sin(0) = 0`，偏移恰为入场静止态——无跳变
- **IDLE_DUR** — 呼吸 tween 长度。
  - 约束：应等于 `TOTAL_DURATION − IDLE_START_TIME`，以用动效填满 composition 剩余时长
- **CYCLES** — 在 `IDLE_DUR` 内的完整呼吸循环次数。
  - 范围：`IDLE_DUR / 3s ≤ CYCLES ≤ IDLE_DUR / 1.5s`（循环周期 1.5-3s 读作自然呼吸）
- **SCALE_AMP** — hero 缩放的正弦振幅。
  - **默认：0.008-0.015**（几乎不可察觉的呼吸——多数场景的正确选择）
  - 仅当元素 **单独占满画布**、场景 **较短（< 6s）** 或 brief 明确要求 **动感 / 俏皮** 时推到 0.02-0.04
  - 长 idle / 多元素并发缩放见「关键原则」
- **Y_AMP_PX** — hero 垂直位移的正弦振幅。
  - **默认：2-3 px**（几乎不可察觉——多数场景的正确选择）
  - 仅 isolated / 短场景 / kinetic 时推到 4-6 px——与 `SCALE_AMP` 同一门控
- **DOT_SCALE_AMP** — dot 缩放的正弦振幅（π/2 相位差，不同步）。
  - 范围：0.04-0.12——可大于 hero 振幅，因 dot 是小 accent
- **PERIOD**（条件启用变体）——使用 `(time - IDLE_START_TIME) / PERIOD` 形式时每周期秒数。
  - 范围：1.5-3s
- **GATE_THRESHOLD**（条件启用变体）——启动 idle 所需的 entryProgress。
  - 范围：0.85-1.0；较低门槛可在入场完成前略早启动 idle 以重叠

### 多八度变体

- **SCALE_AMP_PRIMARY / SCALE_AMP_SECONDARY** — 两个叠加正弦的振幅。
  - 约束：`SCALE_AMP_PRIMARY > SCALE_AMP_SECONDARY`（次项为高频叠加，非同级）；合成最大振幅仍应在上述 SCALE_AMP 范围内
- **OCTAVE_RATIO** — 次项相对主项的频率倍数。
  - 范围：2.0-4.0（接近整数的比例听感更「音乐/协调」；非整数更有机/不可预测）

### 颜色 token

- **{bgGradient}** — 通常为暗色径向渐变，使 lit hero 突出
- **{textColor}** — 与 `{bgGradient}` 高对比
- **{accentColor}** — 单一 accent 留给 dot；`{accentGlow}` 中的光晕为同色色相

## 关键原则

- **优先揭示，再抖动，最后呼吸**——用循环缩放当「活感」廉价且弱；「没有动效胜过糟糕动效」。先用 **与旁白同步的逐段揭示** 填充镜头后段；若确已落定仍显死，用本规则在 **振幅范围低端作轻微抖动**；完整呼吸循环是单个定格 hero 的罕见最后手段，不要批量盖在每个元素上。
- **`sin(0) = 0`**——idle 开始时偏移必须为零，从入场静止态到 idle 无可见跳变。phase tween 从 `phase = 0` 开始。
- **振幅要 subtle——默认取范围低端。** 缩放 `0.008-0.015`（仅 isolated / 短场景 / kinetic brief 时推到 0.02-0.04），旋转 `±0.3-0.8°`（很少需要），位移 `±2-3px`（仅 isolated 时推到 4-6px）。过大则读作「还在动」而非「活着但休息」——连续看 5+ 场景且取上限时，整片会像在微微闪动。
- **循环时长：idle 较长时每息 2.5-4s，否则 1.5-3s**——2.5-3s 是舒适呼吸节奏；长 idle 窗口下低于 1.5s 显得急促；短场景超过 4s 显呆板。
- **长 idle 窗口（`IDLE_DUR > 6s` 或 idle 占 composition > 30%）：** 将 `SCALE_AMP`、`Y_AMP_PX` 减半，放慢 `CYCLES` 使每息 3-4s。考虑在 idle 最后约 20% 将振幅门控淡出到零，使场景在 **过渡前真正落定**，而不是仍在漂移时交接。这是 finalize 快照里「结尾一切还在动」时最有效的单点修复。
- **N 个元素并发 idle**（三联三列、卡片网格、多 stat 行、并排面板）：单元素振幅 ≤ 默认 `/ √N`。三列各 `±6px` 视觉上叠加成 `±18px+` 的竞争动效；三列各 `±2-3px` 读作一次集体呼吸。元素间 **周期** 错开（2.1s / 1.9s / 2.4s）更有机——但 **振幅** 也要更小，不能只错周期。
- **不同元素不同相位**——次元素偏移 `Math.PI / 2`（90°），避免同步。同步显机械；错相显活。
- **叠加，不替换**——idle 动效 **叠加** 在元素静止 transform 上，不替换。若入场落定在 `translateY(0)`，idle 应产出 `translateY(0 + sin*4)`。不要覆盖入场的最终位移。
- **❗ idle 循环不要用 CSS `@keyframes`**——CSS animation 跑在浏览器渲染时钟上，与 HF seek 时钟独立。HF 逐帧 seek 时，CSS 驱动的 idle 会闪烁/不同步。idle 必须在 GSAP timeline 内驱动。

## 关键约束

- **Timeline 必须 paused**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **idle 不用 CSS `animation`**——必须 timeline 驱动
- 若 idle 与同元素其他 tween 叠加，使用 **`will-change: transform`**
- **Phase tween `ease: 'none'`**——正弦本身提供 easing；phase 非线性 tween 会产生非正弦运动
- **不要重启 idle tween**——从 composition idle 窗口起点到终点是单一长 tween

## 组合

- 在 [press-release-spring.md](press-release-spring.md) 之后——按钮 release 落定后 idle 呼吸
- 在 [counting-dynamic-scale.md](counting-dynamic-scale.md) 之后——最终数字呼吸
- 在 [card-morph-anchor.md](card-morph-anchor.md) 之后——落定卡片 idle 轻摆
- 在 [orbit-3d-entry.md](orbit-3d-entry.md) 之后——中心标签 idle 呼吸，元素继续 orbit

## 与 HF 技能搭配

- `/hyperframes-animation` — `onUpdate` 写入 transform
- `/hyperframes-core` — composition 接线
- `/hyperframes-cli` — `hyperframes lint`
