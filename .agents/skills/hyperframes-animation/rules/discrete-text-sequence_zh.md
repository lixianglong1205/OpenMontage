---
name: discrete-text-sequence
description: 在帧阈值处替换整段文本状态，实现非线性打字效果——错字、批量插入、停顿、退格、模拟思考。
metadata:
  tags: text, typing, discrete, threshold, non-linear, sequence
---

# 离散文本序列（Discrete Text Sequence）

不必逐字符打字机效果，而是在时间阈值处替换整段字符串状态。可实现非线性效果（错字、批量添加、停顿、「思考」间隙），平滑逐字打字无法做到这些。

## 工作原理

使用 `{ text, t }` 对象数组，其中 `t` 为秒级时间。在每次 onUpdate 中扫描数组，找出已通过其 `t` 的最新条目并渲染该文本。显示在状态之间跳转；状态之间不做动画。

若需要连续逐字打字机（无停顿、无编辑），请使用文末的 **smooth-slice** 变体。

## HTML

```html
<div
  class="scene"
  id="seq-scene"
  data-composition-id="seq-scene"
  data-start="0"
  data-duration="6"
  data-track-index="0"
>
  <div class="terminal">
    <div class="prompt">$</div>
    <div class="text-wrap">
      <span class="text" id="text">|</span>
      <span class="cursor" id="cursor">_</span>
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
  background: {bgColor};
  font-family: {monoFont}; /* monospace is required — see Critical Constraints */
}
.terminal {
  display: flex;
  align-items: baseline;
  gap: GUTTER;
  font-weight: 800;
  font-size: TERMINAL_FONT_SIZE;
  color: {textColor};
}
.prompt {
  color: {accentColor};
}
.text-wrap {
  display: inline-flex;
  align-items: baseline;
  /* Fixed-width container prevents the right side from jittering as
     content changes length. Choose width ≥ longest state's width. */
  min-width: TEXT_WRAP_MIN_WIDTH;
  white-space: nowrap;
}
.text {
  color: {textColor};
}
.cursor {
  display: inline-block;
  width: CURSOR_WIDTH;
  color: {accentColor};
  margin-left: CURSOR_GAP;
}
```

## GSAP 时间轴 + 离散状态逻辑

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};

  // SEQUENCE — each entry shows from t to the NEXT entry's t.
  // Non-linear: typos, corrections, bulk additions, pauses.
  // Shape (one realization):
  //   [warm-up keystrokes] → [typo] → [backspaces back to fork] →
  //   [bulk-paste of the corrected continuation] → [completion mark]
  const SEQUENCE = [
    { t: 0.0, text: "" },
    { t: T_K1, text: "{p1}" }, // first keystrokes (~3-5 chars, 0.1-0.2s apart)
    { t: T_K2, text: "{p1 + ' ' + p2_typo}" }, // continuation containing a typo
    { t: T_BS, text: "{p1 + ' ' + p2_partial}" }, // backspace(s) — peel back to the fork
    { t: T_BULK, text: "{fullCorrectedText}" }, // bulk paste — replaces several chars at once
    { t: T_DONE, text: "{fullCorrectedText + ' ✓'}" }, // completion marker
  ];

  // Reverse-search for the latest entry whose t has passed.
  function textAt(time) {
    for (let i = SEQUENCE.length - 1; i >= 0; i--) {
      if (time >= SEQUENCE[i].t) return SEQUENCE[i].text;
    }
    return "";
  }

  const textEl = document.getElementById("text");
  const cursorEl = document.getElementById("cursor");
  const tl = gsap.timeline({ paused: true });

  // Drive the discrete display via a 0→TOTAL_DURATION tween's onUpdate
  const driver = { t: 0 };
  tl.to(
    driver,
    {
      t: TOTAL_DURATION,
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        textEl.textContent = textAt(driver.t);
      },
    },
    0,
  );

  // Cursor blink — deterministic via sin, not CSS animation
  const blinkDriver = { p: 0 };
  tl.to(
    blinkDriver,
    {
      p: Math.PI * 2 * BLINK_CYCLES, // BLINK_CYCLES = blinks across composition
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        cursorEl.style.opacity = Math.sin(blinkDriver.p) > 0 ? "1" : "0";
      },
    },
    0,
  );

  window.__timelines["seq-scene"] = tl;
</script>
```

## 变体

### 平滑字符切片（连续打字机——无停顿、无编辑）

若只需直进直出的打字机、不要非线性混乱：

```js
const fullText = "{fullPhrase}";
const len = { v: 0 };
tl.to(
  len,
  {
    v: fullText.length,
    duration: TYPE_DUR,
    ease: "power1.inOut",
    onUpdate: () => {
      textEl.textContent = fullText.substring(0, Math.floor(len.v));
    },
  },
  0,
);
```

编写更快，但观感偏均匀的「机器打字」——缺少真人打字的真实感。

### 思考停顿（在某状态上长时间保持）

插入一个在 `THINK_HOLD_DUR` 秒内不变的状态——像用户停下来思考：

```js
{ t: T_PRE_PAUSE, text: '{partialPhrase}' },        // last state before the pause
// ... no entries for THINK_HOLD_DUR seconds ...
{ t: T_PRE_PAUSE + THINK_HOLD_DUR, text: '{resumedPhrase}' },
```

### 完成时的状态脉冲

最终状态落地时（如「✓」），对整行做短暂脉冲缩放以强调：

```js
tl.to(
  ".text",
  { scale: COMPLETION_PULSE_SCALE, duration: COMPLETION_PULSE_DUR, yoyo: true, repeat: 1 },
  T_DONE,
);
```

### 按状态变色

按阶段着色（例如编辑时变暗、完成标记后用成功色、错字可选警告色）：

```js
// In onUpdate after setting textContent:
if (driver.t > T_DONE) textEl.style.color = "{successColor}";
else if (driver.t < T_K2)
  textEl.style.color = "{textColor}"; // normal typing
else textEl.style.color = "{mutedColor}"; // mid-edit dim
```

## 如何选取数值

### 布局

- **TERMINAL_FONT_SIZE** — 打字行的字号。
  - 范围：全幅构图 48–96 px；终端细节风格可更小
  - 约束：与 `TEXT_WRAP_MIN_WIDTH` 合计须能放进视口
- **TEXT_WRAP_MIN_WIDTH** — 承载文本的固定宽度容器。
  - 约束：须 `≥ widthOf(longest SEQUENCE state) at TERMINAL_FONT_SIZE`。不确定时在 `document.fonts.ready` 后用隐藏探针测量
  - 效果：过小 → 状态长度变化时右缘抖动；过大 → 构图两侧多余留白
- **GUTTER** — 提示符（`$`、`>`）与文本之间的 flex 间距。
  - 范围：约 0.3–0.5× `TERMINAL_FONT_SIZE`
- **CURSOR_WIDTH / CURSOR_GAP** — 块状光标尺寸。
  - 范围：宽度约 0.3× `TERMINAL_FONT_SIZE`；间距宜小（个位数 px），让光标紧贴文字

### 序列时序

- **TOTAL_DURATION** — 构图总时长。
  - 约束：须 ≥ `T_DONE` + 约 1s 收尾停留，让观众看到完成标记
- **T_K1 / T_K2 / T_BS / T_BULK / T_DONE** — SEQUENCE 内里程碑时间戳。
  - 范围：按键间隔 0.06–0.20s 像「人手打字」；自然断词处停顿 0.3–0.6s；批量粘贴一次跳多个字符
  - 约束：单调递增；`T_DONE ≤ TOTAL_DURATION - dwell`
- **TYPE_DUR**（smooth-slice 变体）— 连续打字机总时长。
  - 范围：`chars × 0.06s`（快）到 `chars × 0.12s`（从容）
- **THINK_HOLD_DUR**（思考停顿变体）— 两个 SEQUENCE 状态之间的保持时间。
  - 范围：0.8–2.0s；低于 0.5s 像卡顿而非思考
- **COMPLETION_PULSE_SCALE / COMPLETION_PULSE_DUR**（脉冲变体）。
  - 范围：缩放 1.03–1.08（轻微），时长 0.15–0.30s

### 光标

- **BLINK_CYCLES** — 在 `TOTAL_DURATION` 内的完整闪烁周期数。
  - 范围：`TOTAL_DURATION / 0.8s ≤ BLINK_CYCLES ≤ TOTAL_DURATION / 0.5s`（每 0.5–0.8s 一周期像自然光标）

### 颜色令牌

- **{bgColor} / {textColor} / {accentColor} / {successColor} / {mutedColor}** — 离散选择，非数值区间。从构图调色板选取；提示符与光标共用 `{accentColor}`，读作同一「系统」元素。

## 核心原则

- **阈值序列驱动真实感** — 快速连续按键成组（间隔 0.1–0.2s），词间断点停顿（0.3–0.5s），单次条目批量粘贴（一条替换多字符），加一两处错字增强人手打字感
- **每帧反向搜索数组** — 每帧 O(n)，n 很小（通常 ≤30）。不要按帧索引；序列是稀疏的
- **固定宽度容器必选** — 没有 `min-width` 时，状态长度变化会让文本容器右缘抖动。宽度须 ≥ 最长预期状态
- **光标必须确定性** — 基于 sin 或序列驱动的闪烁，不要用 CSS 动画。HF 逐帧寻址；CSS 动画会不同步
- **文本元素不要用 `transition`** — 离散跳转须**瞬时**。CSS transition 会把跳转糊成拖影，破坏「打字」感
- **❗ 区分离散与平滑** — 若效果是「逐字打出、无编辑」→ 用 smooth-slice 变体。那种情况用离散序列过重。仅在需要非线性状态（错字、停顿、批量粘贴）时用离散

## 关键约束

- **时间轴须暂停**：`gsap.timeline({ paused: true })`
- **注册表键 = `data-composition-id`**
- **文本及其父级均不用 CSS `transition`**
- **光标 `display: inline-block`** — `display: inline` 忽略 width/transform
- **终端风格须等宽字体** — 比例字体即使用固定宽度容器也会视觉抖动
- **文本容器 `white-space: nowrap`** — 状态中途换行会破坏错觉

## 组合

- [3d-text-depth-layers.md](3d-text-depth-layers.md) — 分层深度渲染离散文本（厚重、戏剧化）
- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 标签用离散文本，计数器平滑动画
- [press-release-spring.md](press-release-spring.md) — 序列完成后整行像按钮「按下」确认成功

## 搭配的 HF 技能

- `/hyperframes-animation` — onUpdate 驱动的离散状态查找
- `/hyperframes-core` — 构图接线
- `/hyperframes-cli` — `hyperframes lint`
