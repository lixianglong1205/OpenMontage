---
name: kinetic-beat-slam
description: 打击感动态排版——短句在稳定节拍上逐句猛击入场，每句有各自不同的入场方式，可选节奏装饰（节拍器滴答、节拍条），最后以锁定式终场收束。
metadata:
  tags: text, kinetic, typography, beat, rhythm, slam, percussive, punchy
---

# 节拍猛击动态排版（Kinetic Beat Slam）

短句在**稳定节拍**上逐句命中，每句采用_不同_的入场方式，再叠成锁定式终场。这是「有力 / 有节奏」以文字为主的作品（标语、宣言、 hype 开场）的配方。泛泛与有节奏感的差别在于：(1) 用同一套** onset 数组**驱动所有元素，(2) 每句**各不相同**的入场而非复用同一 helper，(3) 可选的**节奏装饰**让节拍在画面上可见。

## 工作原理

1. **节拍只定义一次。** 单一的 `BEATS = [t0, t1, t2, …]` 数组（秒）是节奏骨架。每句入场、强调与装饰滴答都从该数组取时间——整段作品锁在同一脉动上，而不是各自手调偏移后漂移。
2. **入场方式要变化。** 第一句猛击（缩放 + 模糊），第二句从侧面 snap 入，第三句升起并旋转。同样的_能量_、不同的_形态_——三句都复用同一个 `punchIn()` 会显得平淡。
3. **落地终场。** 所有短句锁成左对齐或居中堆叠；强调下划线扫入；可选地以低幅度连续脉冲守住最后一拍。

## 节拍与缓动

按攻击感选入场缓动（选择是离散的）：

| GSAP ease     | 攻击感                                 |
| ------------- | ------------------------------------------- |
| `power4.out`  | 硬猛击、快速落定 ⭐ 命中默认 |
| `expo.out`    | 最硬 snap（侧向 snap、鞭入）         |
| `back.out(2)` | overshoot 弹出——用于强调，非主体词     |
| `circ.out`    | 带惯性的沉重升起                    |

整段至少用 **3 种不同缓动**（入场即其「语气」）。时长要短——命中 0.35–0.6s，退出 ≤0.25s——节拍才保持打击感。

## HTML

```html
<section class="clip" data-start="0" data-duration="15" data-track-index="1">
  <div class="kbs-stage">
    <div class="kbs-line" id="p1"><span class="verb">Notice</span> more.</div>
    <div class="kbs-line" id="p2"><span class="verb">Decide</span> faster.</div>
    <div class="kbs-line" id="p3"><span class="verb">Act</span> now.</div>
  </div>
  <!-- optional rhythm chrome -->
  <div class="kbs-metronome" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
</section>
```

## CSS

```css
.kbs-stage {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
  padding: 120px 160px; /* title-safe margin */
  box-sizing: border-box;
}
.kbs-line {
  font-family: "Archivo Black", "League Gothic", sans-serif; /* embedded display face */
  font-size: 150px;
  line-height: 0.96;
  letter-spacing: -0.03em;
  color: #f5f5f5;
  will-change: transform, filter, opacity;
}
.kbs-line .verb {
  color: #ff5b2e;
} /* one accent hue */
.kbs-metronome {
  position: absolute;
  bottom: 64px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 14px;
}
.kbs-metronome i {
  width: 6px;
  height: 28px;
  background: #ff5b2e;
  opacity: 0.25;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // ONE tempo grid drives everything — phrases AND the metronome read it (no scattered offsets).
  const PULSE = 0.4; // seconds per sub-beat (the grid)
  const BEATS = [PULSE * 1, PULSE * 5, PULSE * 9]; // phrase onsets, on the grid

  // Distinct entrances per phrase (NOT one reused helper).
  tl.fromTo(
    "#p1",
    { scale: 1.5, filter: "blur(16px)", opacity: 0 },
    { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.5, ease: "power4.out" },
    BEATS[0],
  );
  tl.fromTo(
    "#p2",
    { x: -320, opacity: 0 },
    { x: 0, opacity: 1, duration: 0.45, ease: "expo.out" },
    BEATS[1],
  );
  tl.fromTo(
    "#p3",
    { y: 90, rotation: 6, opacity: 0 },
    { y: 0, rotation: 0, opacity: 1, duration: 0.55, ease: "circ.out" },
    BEATS[2],
  );

  // Rhythm chrome: each metronome tick flashes on the SAME grid (PULSE), not a magic offset.
  const ticks = gsap.utils.toArray(".kbs-metronome i");
  ticks.forEach((tick, i) => {
    tl.to(
      tick,
      { opacity: 1, duration: 0.08, yoyo: true, repeat: 1, ease: "none" },
      PULSE * (i + 1),
    );
  });

  // Finale hold: a low-amplitude breath on the locked stack.
  // floor (not ceil) so the repeat never overshoots data-duration; max(0,…) so a short hold
  // never yields a negative repeat (GSAP treats negative repeat as -1 = infinite = non-deterministic).
  const holdStart = BEATS[2] + 0.7,
    cycle = 1.6,
    holdDur = 15 - holdStart;
  tl.to(
    ".kbs-stage",
    {
      scale: 1.01,
      duration: cycle / 2,
      ease: "sine.inOut",
      yoyo: true,
      repeat: Math.max(0, Math.floor(holdDur / cycle) - 1),
    },
    holdStart,
  );

  window.__timelines["main"] = tl;
</script>
```

## 如何选取数值

- **BEATS 间距** — 命中间隔 1.2–1.8s 读作自信节拍；<0.8s 显 frantic，>2.5s 失去脉动。间距保持均匀（这是_节拍_）。
- **入场时长** — 0.35–0.6s。命中须在下一拍前落定。
- **各异入场** — 每句指定不同变换轴（scale / x / y+rotate）。可复用_缓动族_，变化_运动_。
- **强调色** — 仅一种（动词）。其余为单色白/近黑。
- **节奏装饰** — 可选但对「有节奏」高影响：5 格节拍器、居中节拍条，或 `// label` 等宽标签随拍脉冲。凡需在 shader 转场后仍保留的装饰，按 `../../transitions/overview.md` 规则标记。

## 核心原则

- **一个节拍数组，而非零散偏移** — 所有元素以 `BEATS[]` 计时。这是「有节奏」最大杠杆。
- **每句不同入场** — 所有行复用 `punchIn()` 是「平但合格」的典型信号。
- **短攻击** — 打击感即快入、短、果断。长 fade 会杀死节拍。
- **一种强调色、粗字重** — 内嵌展示字体（Archivo Black、League Gothic、Oswald）150px+；见 `hyperframes-creative/references/typography.md`。
- **终场值得 hold** — 堆叠 + 下划线扫过 + 可选呼吸；不要只让最后一句停在那里。

## 关键约束

- **时间轴暂停**：`gsap.timeline({ paused: true })`。切勿 `tl.play()`。
- **hold/装饰禁止无限 repeat** — 使用 `repeat: Math.max(0, Math.floor(dur / cycle) - 1)`（不用 `repeat: -1`）。用 **`Math.floor`，不用 `Math.ceil`** — `ceil` 会超出 `data-duration` 并触发 `gsap_repeat_ceil_overshoot` lint；`Math.max(0, …)` 防止 hold 短于两周期时出现负 repeat（GSAP 将负 repeat 当作 `-1` = 无限 = 非确定性）。
- **场景间禁止 banned 退出动画** — 若为多场景之一，_转场_即退出（见 `../../transitions/overview.md`）；仅最终场景可淡出。
- **展示字体必须内嵌**，否则渲染时静默回退（Anton/Bebas 字面名未内嵌 — `Bebas Neue` 别名 League Gothic；在 `typography.md` 中验证）。
- **Registry key = 根节点上的 `data-composition-id`**。

## 组合

- [3d-text-depth-layers.md](3d-text-depth-layers.md) — 猛击文字上的挤出深度
- [css-marker-patterns.md](css-marker-patterns.md) — 终场下划线扫过 / 圈选
- [sine-wave-loop.md](sine-wave-loop.md) — 终场呼吸/脉冲

## 与 HF 技能搭配

- `/hyperframes-animation` — 时间轴 + 缓动词汇（`../../adapters/gsap-easing-and-stagger.md`）
- `/hyperframes-creative` — `references/video-composition.md`（前景节奏装饰）、`references/typography.md`（内嵌展示字体）
- `/hyperframes-core` — composition 接线、确定性（有限 repeat）
