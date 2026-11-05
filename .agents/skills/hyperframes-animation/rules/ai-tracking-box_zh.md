---
name: ai-tracking-box
description: 沿振荡路径移动的动画边界框，带 L 形角标——模拟 AI 目标检测/跟踪。
metadata:
  tags: ai, tracking, bounding-box, detection, corner, yellow, ml
---

# AI 跟踪框

带角标（「L 形括号」）的边界框跟随移动目标，模拟实时 AI 检测。位置与尺寸沿正弦路径振荡，模仿持续重算。惯例上在深色背景上以「AI 检测黄」（`{detectionYellow}`）绘制，并附带置信度标签。

## 工作原理

- 框的位置 `(x, y)` 与尺寸 `(w, h)` 由合成时间上的正弦 + 漂移推导
- 4 个 L 形角标（每个角一个 `<div>`，双边框）位于框上
- 可选：左上角上方标签，显示类别名 + 置信度百分比

全部由 GSAP 时间轴驱动，以便 HF 可确定性地 seek。

## HTML

```html
<div
  class="scene"
  id="track-scene"
  data-composition-id="track-scene"
  data-start="0"
  data-duration="5"
  data-track-index="0"
>
  <!-- Background — could be a product mockup, hero image, etc. -->
  <div class="bg">
    <div class="bg-content">{Brand}</div>
    <div class="bg-mascot" id="mascot">{targetGlyph}</div>
  </div>

  <!-- Tracking box wraps the target -->
  <div class="track-box" id="track-box">
    <div class="corner tl"></div>
    <div class="corner tr"></div>
    <div class="corner bl"></div>
    <div class="corner br"></div>
    <div class="label" id="label">{targetGlyph} {LABEL} · {confidence}%</div>
  </div>
</div>
```

## CSS

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  background: radial-gradient(ellipse at center, {bgInner} 0%, {bgOuter} 70%);
  font-family: {font};
  overflow: hidden;
}
.bg {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  gap: 60px;
}
.bg-content {
  position: absolute;
  top: 120px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 80px;
  font-weight: 900;
  color: {bgTextColor};
  letter-spacing: 12px;
  text-transform: uppercase;
}
.bg-mascot {
  position: absolute;
  font-size: 240px;
  line-height: 1;
}

.track-box {
  position: absolute;
  /* Position + size set by GSAP onUpdate */
  pointer-events: none;
  will-change: transform, width, height;
}
.corner {
  position: absolute;
  width: 48px;
  height: 48px;
}
.corner.tl {
  top: -8px;
  left: -8px;
  border-top: 6px solid {detectionYellow};
  border-left: 6px solid {detectionYellow};
}
.corner.tr {
  top: -8px;
  right: -8px;
  border-top: 6px solid {detectionYellow};
  border-right: 6px solid {detectionYellow};
}
.corner.bl {
  bottom: -8px;
  left: -8px;
  border-bottom: 6px solid {detectionYellow};
  border-left: 6px solid {detectionYellow};
}
.corner.br {
  bottom: -8px;
  right: -8px;
  border-bottom: 6px solid {detectionYellow};
  border-right: 6px solid {detectionYellow};
}
.label {
  position: absolute;
  top: -56px;
  left: -8px;
  padding: 8px 16px;
  background: {detectionYellow};
  color: {labelTextColor};
  font-family: {monoFont};
  font-size: 24px;
  font-weight: 800;
  letter-spacing: 2px;
  border-radius: 6px;
  white-space: nowrap;
}
```

## GSAP 时间轴

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const box = document.getElementById("track-box");
  const mascot = document.getElementById("mascot");
  const label = document.getElementById("label");

  // Initial state — box invisible, will fade in
  gsap.set(box, { opacity: 0, scale: ENTRY_SCALE });

  // Phase 1 — box entry (fade in + scale to 1)
  tl.to(
    box,
    {
      opacity: 1,
      scale: 1,
      duration: ENTRY_DUR,
      ease: `back.out(${ENTRY_BOUNCE})`,
    },
    ENTRY_START,
  );

  // Phase 2 — continuous "AI tracking" — box and mascot move in lock-step on sine paths
  const SCREEN_CENTER = { x: COMP_WIDTH / 2, y: COMP_HEIGHT / 2 };
  // DRIFT_X / DRIFT_Y — target oscillation amplitude (px)
  // SIZE_BASE / SIZE_VAR — box mean size + per-frame jitter amplitude (px)
  // SIZE_FREQ_MULT — multiplier on tracking phase so box "breathes" off-tempo from drift
  // CYCLES — number of full oscillations across TRACK_DUR
  // TRACK_DUR — duration of the tracking phase (s)
  // TRACK_START — when tracking phase begins (s)
  // CONFIDENCE_MEAN / CONFIDENCE_VAR — center + half-range of the flickering confidence %
  // CONFIDENCE_FREQ_MULT — how fast confidence flickers relative to drift

  const tracking = { p: 0 };
  tl.to(
    tracking,
    {
      p: Math.PI * 2 * CYCLES,
      duration: TRACK_DUR,
      ease: "none",
      onUpdate: () => {
        // Target position (the mascot moves on a wider arc)
        const mx = SCREEN_CENTER.x + Math.cos(tracking.p) * DRIFT_X;
        const my = SCREEN_CENTER.y + Math.sin(tracking.p) * DRIFT_Y;
        mascot.style.position = "absolute";
        mascot.style.left = `${mx - MASCOT_SIZE / 2}px`;
        mascot.style.top = `${my - MASCOT_SIZE / 2}px`;

        // Box size oscillates slightly (size confidence variation)
        const w = SIZE_BASE + Math.sin(tracking.p * SIZE_FREQ_MULT) * SIZE_VAR;
        const h = SIZE_BASE + Math.sin(tracking.p * SIZE_FREQ_MULT + Math.PI / 2) * SIZE_VAR;

        // Box position centers on mascot
        box.style.width = `${w}px`;
        box.style.height = `${h}px`;
        box.style.left = `${mx - w / 2}px`;
        box.style.top = `${my - h / 2}px`;

        // Confidence label fluctuates inside [CONFIDENCE_MEAN ± CONFIDENCE_VAR]
        const confidence = Math.round(
          CONFIDENCE_MEAN + Math.sin(tracking.p * CONFIDENCE_FREQ_MULT) * CONFIDENCE_VAR,
        );
        label.textContent = `${TARGET_GLYPH} ${LABEL_TEXT} · ${confidence}%`;
      },
    },
    TRACK_START,
  );

  window.__timelines["track-scene"] = tl;
</script>
```

## 如何选取数值

- **ENTRY_SCALE** — 框弹出前起始缩放
  - 范围：0.5-0.9
  - 效果：偏低 = 更强的弹出 / 更「对焦锁定」；偏高 = 柔和显现
  - 约束：必须 < 1（框放大到位）
  - 参考：示例使用 0.7

- **ENTRY_DUR** — 淡入 + 放大时长（秒）
  - 范围：0.3-0.8 s
  - 效果：偏短 = 干脆 / 权威锁定；偏长 = 柔和 / 观察感
  - 约束：应在 TRACK_START 之前结束
  - 参考：示例使用 0.5

- **ENTRY_START** — 入场 tween 开始时间（秒，时间轴绝对时间）
  - 范围：通常 0-2 s
  - 效果：晚开始 = 先让观众注意到目标再被 AI「发现」；早开始 = AI 已在监视
  - 约束：ENTRY_START + ENTRY_DUR ≤ TRACK_START
  - 参考：示例使用 0.5

- **ENTRY_BOUNCE** — 入场时传给 `back.out(...)` 的系数
  - 范围：1.2-2.5
  - 效果：偏低 = 轻微 overshoot；偏高 = 夸张 snap（读作「激进锁定」）
  - 约束：坚持用 `back.out` 族——`elastic` 像卡通，`power` 显得平淡
  - 参考：示例使用 1.4

- **TRACK_START** — 持续跟踪开始时间（秒）
  - 范围：≥ ENTRY_START + ENTRY_DUR
  - 效果：入场与跟踪之间的间隔 = 强调停顿；无间隔 = 无缝锁定 + 跟随
  - 约束：TRACK_START + TRACK_DUR ≤ 合成时长
  - 参考：示例使用 1.0

- **TRACK_DUR** — 跟踪阶段长度（秒）
  - 范围：2-8 s
  - 效果：短 = 「快速扫描」；长 = 「持续观察」
  - 约束：至少容纳一个完整 CYCLE 才能读作振荡
  - 参考：示例使用 4.0

- **CYCLES** — TRACK_DUR 内目标完整正弦振荡次数
  - 范围：0.5-3
  - 效果：低 = 慵懒漂移；高 = 抖动 / 目标过于活跃
  - 约束：CYCLES / TRACK_DUR 设定漂移有效 Hz；保持 < ~0.6 Hz 否则运动糊成一片
  - 参考：示例使用 1.5

- **DRIFT_X / DRIFT_Y** — 目标相对画面中心振荡幅度（px，1920×1080 基准）
  - 范围：40-200 px
  - 效果：小 = 轻微悬停；大 = 大范围追逐，框贴近画面边缘
  - 约束：SCREEN_CENTER ± DRIFT 在 MASCOT_SIZE 下须保持 mascot 完全在屏内
  - 参考：示例使用 80 / 50

- **SIZE_BASE** — 边界框平均宽/高（px）
  - 范围：200-500 px
  - 效果：小 = 「标本标签」；大 = 「框即主体」
  - 约束：在所有置信度尺寸下须明显包住目标 glyph
  - 参考：示例使用 320

- **SIZE_VAR** — 逐帧尺寸抖动半幅（px）
  - 范围：SIZE_BASE 的 5-10%
  - 效果：偏低 = 稳定 / 自信检测器；偏高 = 抖动 / 反复拟合。超出此范围会像「坏了」（过多）或「静态 UI」（无抖动）
  - 约束：保持 < 0.15 × SIZE_BASE，避免破坏 L 形括号错觉
  - 参考：示例使用 30（约 320 的 9%）

- **SIZE_FREQ_MULT** — 尺寸振荡相对跟踪相位的倍数
  - 范围：1.5-3
  - 效果：1 = 尺寸与漂移同拍（显得机械）；非整数比 = 有机重拟合
  - 约束：避免整数比；非整数读作持续重算
  - 参考：示例使用 2.3

- **MASCOT_SIZE** — mascot 元素渲染宽度（px）；用于在 (mx, my) 居中
  - 范围：与 `.bg-mascot` 的 CSS `font-size` 一致
  - 效果：须与实际渲染尺寸一致，否则 mascot 会偏离框
  - 约束：MASCOT_SIZE / 2 = 应用于 top/left 的偏移
  - 参考：示例使用 240（对应 `font-size: 240px`）

- **CONFIDENCE_MEAN** — 标签显示的中心置信度 %
  - 范围：95-99
  - 效果：< 95 读作「不确定」；100 读作「假精确」。97 是「自信 AI」的甜区
  - 约束：保持 CONFIDENCE_MEAN + CONFIDENCE_VAR ≤ 99
  - 参考：示例使用 97

- **CONFIDENCE_VAR** — 围绕 CONFIDENCE_MEAN 的闪烁半幅
  - 范围：1-3
  - 效果：0 = 静态（像截图）；>3 = 不稳定（像坏了）
  - 约束：CONFIDENCE_MEAN ± CONFIDENCE_VAR ⊂ [95, 99]
  - 参考：示例使用 2

- **CONFIDENCE_FREQ_MULT** — 标签闪烁相对跟踪相位的倍数
  - 范围：3-6
  - 效果：低 = 与漂移同步（机械）；高 = 快速 nervous 闪烁（读作「实时推理」）
  - 约束：保持高于 SIZE_FREQ_MULT，使标签比框「呼吸」更快
  - 参考：示例使用 4

- **COMP_WIDTH / COMP_HEIGHT** — 合成像素尺寸（用于推导 SCREEN_CENTER）
  - 范围：由 HF 合成决定（`data-width` / `data-height`）
  - 效果：非创意选择——须匹配父合成
  - 约束：SCREEN_CENTER = (COMP_WIDTH/2, COMP_HEIGHT/2)
  - 参考：示例使用 1920 × 1080

- **{detectionYellow}** — 角标 + 标签背景色
  - 这是**离散惯例**，不是可调范围。行业内在深色背景上 AI 检测叠加层均为黄色（自动驾驶 HUD、安防 CV、ML 演示）。红色像「警告」，绿色像「成功」，蓝色像「信息」——都不读作「检测」。
  - 建议：饱和暖黄（`#facc15` / `#FCD34D` 一族）配深海军蓝或近黑背景。换任何其他色相都会损失类型可读性。
  - 参考：示例使用 `#facc15`（Tailwind `yellow-400`）

- **{bgInner} / {bgOuter}** — 径向渐变背景色标
  - 应深色、低彩度，使黄色角标突出
  - 约束：与 {detectionYellow} 对比度足够（角与标签须可读）
  - 参考：示例使用 `#161a3a`（内）→ `#0b0d1f`（外）

- **{labelTextColor}** — 黄色标签内文字色
  - 约束：须与 {detectionYellow} 形成对比；通常与 {bgOuter} 同款近黑
  - 参考：示例使用 `#0b0d1f`

- **{font} / {monoFont}** — 场景字体与标签字体
  - {font}：{Brand} 背景的无衬线正文字体
  - {monoFont}：置信度标签等宽字体（等宽强化「机器读数」 affordance）
  - 参考：示例使用 `"Inter", sans-serif` 与 `"JetBrains Mono", monospace`

## 变体

### 多目标检测

多个框处于不同相位（各自跟踪自己的 mascot）。各自独立的 onUpdate 驱动；相位偏移 `Math.PI / N`，避免同步 tick。

### 丢失后重新捕获

框淡至 {LOST_OPACITY}（约 {LOST_DUR}），再 snap 到新位置并闪「REACQUIRED」标签：

```js
tl.to(box, { opacity: LOST_OPACITY, duration: LOST_DUR }, LOST_START);
tl.to(
  box,
  { opacity: 1.0, duration: REACQUIRE_DUR, ease: `back.out(${REACQUIRE_BOUNCE})` },
  REACQUIRE_START,
);
tl.to(label, { textContent: "REACQUIRED · 99%", duration: 0 }, REACQUIRE_START);
```

（LOST_OPACITY ≈ 0.2-0.4；REACQUIRE_BOUNCE ≈ 1.8-2.5，比初次入场更 snap 的重锁定。）

### 跟踪后缩放

跟踪结束后，通过 [viewport-change](viewport-change.md) 将「镜头」缩放到被跟踪框。组合效果：「AI 发现了东西，现在展示它。」

## 核心原则

- **深色背景上的黄色是检测惯例**——见 {detectionYellow} 条目。其他颜色会失去类型信号。
- **框必须始终包含目标**——每帧从目标位置重算框位置；切勿落后。框滞后读作「坏掉的跟踪器」，而非「聪明 AI」。
- **轻微尺寸变化（约 SIZE_BASE 的 5-10%）**——过多像跟踪器困惑；恰到好处读作「实时重算」。
- **角标而非完整边框**——L 形括号是类型签名。完整边框像通用 UI 框。
- **置信度标签在窄范围内闪烁（CONFIDENCE_MEAN ± CONFIDENCE_VAR 落在 [95, 99]）**——超出读作「不确定」；≥100 读作「假精确」。
- **跟踪不用 CSS 动画——用 timeline onUpdate**——HF 逐帧 seek 与 CSS 动画不同步。

## 关键约束

- **时间轴须暂停**：`gsap.timeline({ paused: true })`
- **注册表键 = `data-composition-id`**
- **`.track-box` 或 `.corner` 上无 CSS 动画**——须由时间轴驱动
- **`.track-box` 上 `will-change: transform, width, height`**
- **`.track-box` 上 `pointer-events: none`**——装饰性叠加层
- **每帧从目标重算框位置**——切勿与目标分开 tween 框位置

## 组合

- [viewport-change.md](viewport-change.md) — 检测阶段后缩放到被跟踪框
- [multi-phase-camera.md](multi-phase-camera.md) — 跟踪时广角，锁定后推近
- [sine-wave-loop.md](sine-wave-loop.md) — mascot 在框内 idle 呼吸

## 搭配的 HF 技能

- `/hyperframes-animation` — onUpdate 写入多元素位置
- `/hyperframes-core` — 合成接线
- `/hyperframes-cli` — `hyperframes lint`
