---
name: camera-cursor-tracking
description: 两阶段虚拟摄像机：将视口锁定于移动焦点，并支持可配置的初始定位。
metadata:
  tags: camera, tracking, viewport, two-phase, spring
---

# 两阶段摄像机光标跟踪

通过两种摄像机模式切换，使水平增长的元素（例如带打字动画的搜索栏、逐字显现的长 URL）始终保持在可见区域内。

## 工作原理

区分 **世界空间（World Space）**（包含全部内容的完整目标元素）与 **屏幕空间（Screen Space）**（视口）。两个阶段：

- **阶段 1（静态）** — 世界容器位于固定的初始偏移处，摄像机不移动。在跟踪开始前将观众视线锚定在构图上。
- **阶段 2（跟踪）** — 当焦点（光标、高亮、最后打出的字形）超过目标屏幕位置（例如距视口左缘可配置比例 `CURSOR_TARGET_FRACTION`）时激活。世界容器向左平移（`x: -<delta>`），使焦点固定在该屏幕位置。

偏移量在阶段边界处 **数学上连续** — 跟踪开始的瞬间，世界位置与静态阶段一致，因此过渡无缝。

代码中使用的分段形式为：

```
finalWorldX = Math.min(INITIAL_OFFSET, trackingOffset)
```

`INITIAL_OFFSET` 为静态阶段的值；`trackingOffset` 为将焦点保持在 `CURSOR_TARGET_FRACTION × viewportWidth` 所需的位移。当焦点尚未越过目标屏幕 X 时，`trackingOffset` 大于 `INITIAL_OFFSET`（数值上负得较少），`Math.min` 返回静态值。一旦焦点将要越过目标，`trackingOffset` 会小于 `INITIAL_OFFSET`，跟踪接管。

## HTML

```html
<div
  class="scene"
  id="tracking-scene"
  data-composition-id="tracking-scene"
  data-start="0"
  data-duration="5"
  data-track-index="0"
>
  <div class="viewport">
    <div class="world">
      <div class="search-bar">
        <span class="text" id="reveal-text">{phrase}</span><span class="cursor">|</span>
      </div>
    </div>
  </div>
</div>
```

## CSS（hero-frame 布局）

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
}

.viewport {
  position: absolute;
  inset: 0;
  overflow: hidden; /* clip the world content */
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding-left: VIEWPORT_PAD_LEFT; /* "left margin" — variation: left-aligned init */
}

.world {
  display: flex;
  align-items: center;
  white-space: nowrap; /* keep text on one line for camera-tracking */
  transform: translateX(0); /* GSAP will animate this */
}

.search-bar {
  font-family: {font};
  font-size: BAR_FONT_SIZE;
  font-weight: BAR_FONT_WEIGHT;
  color: {textColor};
  letter-spacing: BAR_LETTER_SPACING;
}

.search-bar .text {
  /* Width grows as more characters reveal */
  display: inline-block;
  overflow: hidden;
  vertical-align: bottom;
}

.search-bar .cursor {
  display: inline-block;
  width: CURSOR_WIDTH;
  margin-left: CURSOR_GAP;
  background: {accentColor};
  height: CURSOR_HEIGHT_EM;
  vertical-align: bottom;
  /* No `animation: blink` CSS keyframe here — HF renders by seeking a paused
     timeline, and CSS animation clocks are NOT synced to that seek. A CSS
     blink will flicker non-deterministically. Drive cursor blink as a finite
     yoyo tween on the GSAP timeline instead — see GSAP Timeline section. */
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Pre-measure target text width to compute tracking distance.
  // Build the timeline SYNCHRONOUSLY — see Critical Constraints for why
  // a fonts.ready gate causes worker-race flicker.
  const textEl = document.getElementById("reveal-text");
  const fullText = textEl.textContent;
  const targetCursorScreenX = CURSOR_TARGET_FRACTION * VIEWPORT_WIDTH;
  const fullWidth = textEl.scrollWidth; // total text width after full reveal
  const trackingDelta = Math.max(0, VIEWPORT_PAD_LEFT + fullWidth - targetCursorScreenX);

  // Phase 1 — text reveals progressively; camera holds.
  // Reveal via max-width tween (no layout-property tweens on width/left/top).
  tl.fromTo(
    ".search-bar .text",
    { maxWidth: 0 },
    {
      maxWidth: fullWidth,
      duration: REVEAL_DUR,
      ease: "none", // linear typing rate
    },
    REVEAL_START,
  );

  // Phase 2 — camera tracks. Begin BEFORE full reveal so the boundary feels
  // continuous (text is still revealing as camera starts moving). The
  // Math.min(INITIAL_OFFSET, trackingOffset) formulation makes the handoff
  // mathematically continuous; see How It Works.
  tl.to(
    ".world",
    {
      x: -trackingDelta,
      duration: TRACK_DUR,
      ease: "power2.inOut",
    },
    TRACK_START,
  );

  // Cursor blink — GSAP-driven (NEVER CSS @keyframes infinite, which doesn't
  // sync with HF's seek-by-frame). Finite yoyo, repeats computed from scene
  // length so blinks land deterministically across frames.
  const blinkRepeats = Math.ceil(SCENE_DURATION / BLINK_HALF_PERIOD) - 1;
  tl.to(
    ".search-bar .cursor",
    {
      opacity: 0,
      duration: BLINK_HALF_PERIOD,
      ease: "steps(1)", // hard on/off, no fade
      yoyo: true,
      repeat: blinkRepeats,
    },
    0,
  );

  window.__timelines["tracking-scene"] = tl;
</script>
```

### 变体

- **居中 → 居中跟踪**：设置 `.viewport { justify-content: center; padding: 0; }`。当焦点越过中线（`CURSOR_TARGET_FRACTION = 0.5`）时开始跟踪。
- **左对齐 → 向右跟踪**：如上所述。当内容从一开始就超出视口宽度时效果最佳。
- **连续打字驱动**：用带 `onUpdate` 的打字时钟（`charsTyped = Math.floor(progress)`）配合每帧 `measureNodeWidth` 驱动光标屏幕 X，替代 `maxWidth` 补间。当所打文字在场景别处被消费时（例如父级条带的摄像偏移）必须使用此方式。

## 如何选取参数

- **VIEWPORT_PAD_LEFT** — 视口内世界左缘的内边距（阶段 1 锚点 X）。
  - 范围：0 → 约视口宽度的 10%
  - 效果：0 贴左缘；更大内缩更像居中 hero 画幅
  - 约束：须与 `.viewport` 上 CSS 的 `padding-left` 一致，否则摄像机会算偏
- **VIEWPORT_WIDTH** — 构图的 `data-width`，单位为 CSS 像素。
  - 约束：须等于场景根节点的 `data-width`；不可补间
- **CURSOR_TARGET_FRACTION** — 阶段 2 中焦点锁定的视口宽度比例。
  - 范围：0.5（居中跟踪）→ 0.75（偏右，光标后可见更多文字）
  - 效果：较小值帧内已显现文字更少；较大值延迟开始跟踪
- **BAR_FONT_SIZE** — hero 元素字号。
  - 范围：约视口高度的 8–12%；低于约 6% 会像 UI 控件而非电影感元素
- **BAR_FONT_WEIGHT** — 搜索栏文字字重。
  - 范围：离散值；400 为中性演示文字，700 为 hero / 标题级构图
- **BAR_LETTER_SPACING** — 栏文字的 `letter-spacing`。
  - 范围：略负（更紧、更电影感）→ 0（默认）
- **CURSOR_WIDTH** — 光标笔画宽度，CSS 像素。
  - 范围：1080p 下约 4–10 px；更细像打字光标，更粗像块状插入符
- **CURSOR_GAP** — 文字与光标之间的 `margin-left`。
  - 范围：少量 px 留白；勿超过光标宽度，否则会视觉脱节
- **CURSOR_HEIGHT_EM** — 光标高度相对字号的 em 倍数。
  - 范围：0.85–1.0；与已打字形视觉高度一致
- **REVEAL_START** — 阶段 1 打字开始时刻。
  - 约束：通常为 0；若前有其他阶段，≥ 该阶段结束 + 小缓冲
- **REVEAL_DUR** — 阶段 1 显现补间时长。
  - 范围：随字符数缩放（目标平均每字 0.05–0.15s 节奏）
  - 约束：须在 `SCENE_DURATION` 结束前，并宜与跟踪阶段略重叠
- **TRACK_START** — 阶段 2 摄像机运动开始时刻。
  - 范围：通常早于显现完成以保持衔接感；若 t=0 焦点已过目标可与 `REVEAL_START` 相同
  - 约束：`TRACK_START < REVEAL_START + REVEAL_DUR` 以实现平滑交叉
- **TRACK_DUR** — 摄像机平移时长。
  - 范围：0.8–2.0s；低于 0.5s 像瞬移，超过 2.5s 显拖沓
- **SCENE_DURATION** — 须与场景根 `data-duration` 一致。
  - 约束：用于闪烁重复次数；不一致会导致闪烁截断或超出结尾
- **BLINK_HALF_PERIOD** — 光标闪烁半周期（一次亮或一次灭）。
  - 范围：0.2–0.4s；0.3s 较自然
  - 约束：派生值 `Math.ceil(SCENE_DURATION / BLINK_HALF_PERIOD) - 1` 须 ≥ 0
- **缓动选择** — 离散：
  - 摄像机平移：`power2.inOut` 或 `power3.inOut` 电影感落位；避免 `back.out`（过冲像 UI 弹跳而非摄像机）
  - 显现：`"none"` 线性打字；任何缓动都会扭曲逐键节奏
  - 闪烁：`"steps(1)"` 硬开关；任何缓动会让光标渐隐并破坏插入符感

## 核心原则

- **用 `getBoundingClientRect()` / 探测节点测量**，不要用字符数 × 字号。比例字体字形宽度可变。
- **世界层 `white-space: nowrap`** — 文字须单行，摄像数学才成立
- **预分配世界宽度**：将 `maxWidth` 设为目标全宽 — 避免补间中途布局跳动
- **缓动摄像机**（`power2.inOut` / `power3.inOut`），非线性 — 自然平移感
- **用缓动近似弹簧感**，不用刚度/阻尼参数 — GSAP 无内置 spring，但 `back.out(${BOUNCE_FACTOR})` 或 `power4.out` 可近似落位感

## 关键约束

- **同步构建时间轴，不要用 fonts.ready 门闩** — HF 在并行 worker 中逐帧渲染，每个都是全新浏览器。若用 `document.fonts.ready.then(...)` 包裹时间轴构建，部分 worker 会在 Promise  resolve 前 seek 帧且找不到已注册时间轴 → 那些帧以 CSS 初始态渲染（如 `max-width: 0` ⇒ 空文字），其他 worker 正常 → 空/满之间可见闪烁。在脚本解析时即注册 `window.__timelines[id] = tl`，即使字体尚未加载 — 摄像数学可容忍回退字体测量几 percent 误差，但 worker 竞态闪烁不可接受。
- **若字体加载后精确测量很重要**，在补间 `onUpdate` 内重新测量（每帧 seek 仍确定），勿用 Promise 门闩。或在 @font-face 上设 `font-display: block` 强制浏览器在绘制任何文字前等待字体。
- **时间轴须暂停**：`gsap.timeline({ paused: true })`。切勿 `tl.play()`
- **注册键 = `data-composition-id`**：`window.__timelines["tracking-scene"]` 须与场景根一致
- **阶段边界数学连续**：跟踪开始瞬间世界的 `x` 须等于静态阶段偏移。`Math.min(INITIAL_OFFSET, trackingOffset)` 保证这一点；勿改用硬分支 `if (typingProgress > threshold)`，否则摄像机会明显跳变。
- **内联光标，非绝对定位**：光标应为文字兄弟节点（inline-block）以自然跟随流式排版 — 绝对定位会与摄像数学错位
- **`.viewport` 上 `overflow: hidden`**：世界左缘平移出屏时裁剪
- **光标闪烁用 GSAP，勿用 CSS `@keyframes ... infinite`** — HF 通过 seek 暂停时间轴渲染；CSS 动画时钟与该 seek 不同步，CSS 驱动闪烁会在帧间非确定闪烁。始终在暂停 GSAP 时间轴上用有限 yoyo 补间驱动闪烁（重复次数由场景长度计算）。

## 组合

- [context-sensitive-cursor.md](context-sensitive-cursor.md) — 打字过程中按文本段改变光标颜色/样式
- [discrete-text-sequence.md](discrete-text-sequence.md) — 与本摄像机搭配的非线性文字显现

## 搭配的 HF 技能

- `/hyperframes-animation` — 时间轴 + 补间 API
- `/hyperframes-core` — 构图接线 + `data-*` 属性
- `/hyperframes-cli` — `hyperframes lint` 校验注册键与时长
