---
name: context-sensitive-cursor
description: 光标颜色与样式随当前正在输入的文本片段自适应——高亮段落用强调色，占位符段落变暗等。
metadata:
  tags: cursor, color, context, typewriter, styling, segment
---

# 上下文敏感光标

在打字机序列中，光标的颜色（以及可选的高度/闪烁频率）与**当前活跃的文本片段**一致。若打字机正在输入品牌名，光标为品牌强调色；在占位符上则变暗为灰色。相比在所有文本状态下使用单一固定光标颜色，这能增强视觉一致性。

## 工作原理

文本按 `{text, t, segment}` 条目的**序列**编写，其中 `segment` 为字符串标识（'main' / 'highlight' / 'brand' / 'success'）。驱动 tween 的 onUpdate 根据 `time` 判定当前片段，再将光标的 CSS 颜色（及可选的其他属性）设为与该片段调色板一致。

## HTML

```html
<div
  class="scene"
  id="cursor-scene"
  data-composition-id="cursor-scene"
  data-start="0"
  data-duration="{DURATION}"
  data-track-index="0"
>
  <div class="terminal">
    <div class="prompt">$</div>
    <div class="text-wrap">
      <span class="text" id="text"></span><span class="cursor" id="cursor">_</span>
    </div>
  </div>
</div>
```

## CSS

占位符说明：`{monoFont}` 为项目的等宽字体栈（比例字体会导致片段中途光标漂移）；`{bgColor}` 为深色背景；`{textColor}` 为可读前景色；`{promptColor}` 为行首提示符的默认片段颜色。

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: {bgColor};
  font-family: {monoFont};
}
.terminal {
  display: flex;
  align-items: baseline;
  gap: 24px;
  font-size: 72px;
  font-weight: 800;
  color: {textColor};
  white-space: pre;
}
.prompt {
  color: {promptColor};
}
.text-wrap {
  display: inline-flex;
  align-items: baseline;
  min-width: 1200px;
}
.text {
  color: {textColor};
  white-space: pre;
}
/* Cursor highlights based on active segment via per-frame background swap */
.cursor {
  display: inline-block;
  width: {cursorWidth}px;
  height: {cursorHeight}px;
  background: {textColor}; /* default — overridden per segment in onUpdate */
  margin-left: {cursorGap}px;
  vertical-align: {cursorBaselineFix}px;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Sequence with per-entry segment label.
  // Each entry: { t: absoluteSeconds, text: cumulative visible string, segment: paletteKey, color: hex }.
  // As the driver crosses each `t`, the cursor color swaps to that segment's accent —
  // viewer's eye locks onto the keyword being typed.
  // Shape: a monotonic timeline of N entries where adjacent entries usually share text-prefix
  // but may differ in `segment` (which is what makes the cursor color shift mid-line).
  const SEQUENCE = [
    { t: 0, text: "", segment: "main", color: "{mainColor}" },
    { t: T_LEADIN_END, text: "{leadInChunk}", segment: "main", color: "{mainColor}" },
    { t: T_BRAND_IN, text: "{leadInBrandPrefix}", segment: "brand", color: "{brandColor}" }, // brand segment starts
    { t: T_BRAND_OUT, text: "{leadInBrandFull}", segment: "main", color: "{mainColor}" }, // back to main
    { t: T_CMD_IN, text: "{leadInCmdPrefix}", segment: "cmd", color: "{cmdColor}" }, // command segment
    { t: T_BRAND_2, text: "{leadInCmdBrand}", segment: "brand", color: "{brandColor}" }, // brand again (e.g. filename)
    { t: T_SUCCESS, text: "{leadInDone}", segment: "success", color: "{successColor}" }, // completion mark
  ];

  function entryAt(time) {
    for (let i = SEQUENCE.length - 1; i >= 0; i--) {
      if (time >= SEQUENCE[i].t) return SEQUENCE[i];
    }
    return SEQUENCE[0];
  }

  const textEl = document.getElementById("text");
  const cursorEl = document.getElementById("cursor");

  // Discrete state driver — writes text + cursor color
  const driver = { t: 0 };
  tl.to(
    driver,
    {
      t: DURATION,
      duration: DURATION,
      ease: "none",
      onUpdate: () => {
        const entry = entryAt(driver.t);
        textEl.textContent = entry.text;
        cursorEl.style.background = entry.color;
      },
    },
    0,
  );

  // Deterministic blink via sin (NOT CSS animation).
  // Phase sweep = (2π) × BLINK_CYCLES_PER_SCENE drives a square wave at sign(sin(p)).
  const blink = { p: 0 };
  tl.to(
    blink,
    {
      p: Math.PI * 2 * BLINK_CYCLES_PER_SCENE,
      duration: DURATION,
      ease: "none",
      onUpdate: () => {
        cursorEl.style.opacity = Math.sin(blink.p) > 0 ? "1" : "0";
      },
    },
    0,
  );

  window.__timelines["cursor-scene"] = tl;
</script>
```

## 变体

### 输入活跃时不闪烁

当正在追加字符时（驱动在最近 `TYPING_GRACE` 秒内前进），抑制闪烁——光标保持实心。若无输入活动（`driver.t - lastChangeTime > TYPING_GRACE`），恢复闪烁。

```js
let lastChangeTime = 0,
  lastText = "";
// In onUpdate:
if (entry.text !== lastText) {
  lastChangeTime = driver.t;
  lastText = entry.text;
}
const isTyping = driver.t - lastChangeTime < TYPING_GRACE;
cursorEl.style.opacity = isTyping ? "1" : Math.sin(blink.p) > 0 ? "1" : "0";
```

### 片段切换时光标高度变化

品牌片段上使用更高光标以强调（`cursorHeightEmphasis > cursorHeight`）：

```js
cursorEl.style.height =
  entry.segment === "brand" ? `${cursorHeightEmphasis}px` : `${cursorHeight}px`;
```

### 深色文本时光标反色

若某片段为浅色背景上的深色文字，光标也应变为深色。通过 `entry.color` 作为**唯一真相来源**并从中读取。

## 核心原则

- **光标颜色切换让品牌时刻更醒目**——视线会落在品牌名上，因为光标颜色切换到品牌强调色。否则光标只是视觉噪声。
- **光标 div 使用 `background` 属性**——而非 `color`（光标是色块，不是字形）
- **用 sin 实现确定性闪烁**——不要用 CSS `@keyframes blink`。HF seek 会失步。
- **光标 `display: inline-block`**——`display: inline` 会忽略 width/height。
- **`vertical-align: -8px`**（或类似值）——在视觉上将光标锚定到文本基线，而非整行行高。
- **文本及父级使用 `white-space: pre`**——保留尾部空格，使光标位于片段末尾，而非被折叠空格之后。
- **调色板与品牌体系一致**——片段最多 3–4 种颜色（main / brand / cmd / success）。再多分段会像随机切换。

## 如何选取数值

- **DURATION**——场景总时长（秒）
  - 范围：单行输入约 4–8 s；行很长时可更长
  - 影响：过短会截断打字感；过长会在 success 状态后留下冗长空档
  - 约束：须满足 `≥ SEQUENCE[last].t + (closing dwell)`
  - 参考：见对应 blueprint 的示例 HTML

- **SEQUENCE 各条目的 `t` 值**——每条新可见文本 + 片段生效的绝对秒数
  - 范围：单调递增；微增（按词或按 token）间隔 0.2–0.5 s，片段切换间隔更长
  - 影响：过密会像幻灯片而非打字；过疏则拖沓
  - 约束：按升序排列；条目间距不必均匀——高亮处可放慢
  - 参考：见对应 blueprint 的示例 HTML

- **片段调色板：mainColor / brandColor / cmdColor / successColor**——光标填充色
  - 范围：最多 3–4 种可区分色；在窄光标宽度下仍应可辨
  - 影响：片段过多切换像随机；过少则品牌时刻不够突出
  - 约束：`brandColor` 与 `successColor` 色相可接近，但饱和度/明度应不同，以便 brand→success 过渡可见
  - 参考：见对应 blueprint 的示例 HTML

- **cursorWidth / cursorHeight / cursorGap / cursorBaselineFix**——光标块几何
  - 范围：cursorWidth 8–24 px；cursorHeight ≈ 0.85–1.0 × fontSize；cursorGap 4–12 px；cursorBaselineFix 为小幅负值以低于基线
  - 影响：过细在压缩渲染中消失；过高在视觉上压过文字
  - 约束：须使用 `display: inline-block`（`display: inline` 上的 `width` 会被忽略）
  - 参考：见对应 blueprint 的示例 HTML

- **cursorHeightEmphasis**（变体）——活跃片段为 brand 时的高度
  - 范围：1.1–1.25 × `cursorHeight`
  - 影响：轻微增大读作强调；过大读作 glitch
  - 约束：`cursorHeightEmphasis > cursorHeight`
  - 参考：见对应 blueprint 的示例 HTML

- **BLINK_CYCLES_PER_SCENE**——`DURATION` 内完整闪烁周期数
  - 范围：使周期 `DURATION / BLINK_CYCLES_PER_SCENE` ≈ 0.6–1.2 s；例如 8 秒场景约 1 s 周期则 BLINK_CYCLES_PER_SCENE = 8
  - 影响：周期短（周期多）像 glitch/焦躁；周期长像终端空闲
  - 约束：`DURATION` 固定时须为整数——否则 sin 扫掠在周期中途结束，最后一帧光标会跳变
  - 参考：见对应 blueprint 的示例 HTML

- **TYPING_GRACE**（变体）——文本变化后抑制闪烁的秒数
  - 范围：0.15–0.3 s
  - 影响：偏低时字符仍在出现时仍闪烁；偏高时长停期间光标一直实心
  - 约束：须小于相邻两条 SEQUENCE 条目间最短停留——否则光标永不闪烁
  - 参考：见对应 blueprint 的示例 HTML

## 关键约束

- **时间轴须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **光标上不要用 CSS 动画**——须由时间轴驱动（闪烁 + 颜色）
- **光标 `display: inline-block`**——width/height 所必需
- **文本容器与文本使用 `white-space: pre`**——保留尾部空格
- **等宽字体**——比例字体会导致片段中途光标漂移

## 组合

- [discrete-text-sequence.md](discrete-text-sequence.md)——使用相同的 SEQUENCE 数组模式；本规则增加光标样式层
- [camera-cursor-tracking.md](camera-cursor-tracking.md)——镜头跟随打字过程中的光标
- [press-release-spring.md](press-release-spring.md)——打字完成后，按钮按下确认命令

## 搭配的 HF 技能

- `/hyperframes-animation`——onUpdate 驱动光标颜色 + sin 闪烁
- `/hyperframes-core`——composition 接线
- `/hyperframes-cli`——`hyperframes lint`
