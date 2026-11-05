---
name: cursor-click-ripple
description: 动画鼠标光标移动到目标处，点击时产生缩放下压与向外扩散的涟漪环。
metadata:
  tags: cursor, click, ripple, interaction, mouse, button
---

# 光标点击涟漪

动画光标移动到目标元素，执行点击并伴随视觉下压，从点击点向外发射扩散的涟漪环。

## 工作原理

由单条 GSAP 时间轴驱动的三个连续阶段：

1. **移动**：光标从入口点缓动平移到目标元素中心
2. **点击**：光标与目标同时缩放下压（yoyo：缩小后回弹）
3. **涟漪**：从点击点向外扩散的圆环并淡出。1–3 个错开的环增强点击反馈

使用 GSAP 时间轴，因为阶段顺序（移动 → 停稳 → 点击 → 涟漪）正是时间轴能清晰表达的内容。

## HTML

```html
<div
  class="scene"
  id="cursor-click-scene"
  data-composition-id="cursor-click-scene"
  data-start="0"
  data-duration="2"
  data-track-index="0"
>
  <button class="target-button">{ctaLabel}</button>

  <div class="cursor">
    <svg width="24" height="24" viewBox="0 0 24 24">
      <path
        d="M5 3L19 12L12 13L9 20L5 3Z"
        fill="{cursorFill}"
        stroke="{cursorStroke}"
        stroke-width="1.5"
      />
    </svg>
  </div>

  <!-- Ripple rings — centered on click target, hidden until trigger -->
  <div class="ripple ripple-1"></div>
  <div class="ripple ripple-2"></div>
  <div class="ripple ripple-3"></div>
</div>
```

## CSS

将光标置于入口点。按钮位于最终位置。涟漪位于点击目标中心，使用 `scale: 0` 与 `opacity: 0`，在时间轴触发前保持不可见：

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
}

.target-button {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  /* ...button styling (background, color, font from project tokens) */
}

.cursor {
  position: absolute;
  left: 10%;
  top: 80%; /* entry corner */
  pointer-events: none;
  z-index: 999;
}

.ripple {
  position: absolute;
  left: 50%;
  top: 50%; /* click target center */
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px solid {rippleColor};
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  pointer-events: none;
}
```

## GSAP 时间轴

构建一条暂停的时间轴。在 `window.__timelines` 上注册，键名与场景根上的 `data-composition-id` 相同。所有调参值均为命名常量——见下文「如何选取数值」。

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // MOVE_DUR, MOVE_EASE, CLICK_AT, PRESS_DUR, CURSOR_PRESS_SCALE, TARGET_PRESS_SCALE,
  // RIPPLE_AT, RIPPLE_DUR, RIPPLE_SCALE, RIPPLE_STAGGER, RIPPLE_EASE
  // — all named; values per How to Choose Values.

  // Phase 1 — Move cursor to target center (eased, not linear)
  tl.to(
    ".cursor",
    {
      x: TARGET_X,
      y: TARGET_Y,
      duration: MOVE_DUR,
      ease: MOVE_EASE,
    },
    0,
  );

  // Phase 2 — Click: cursor + target depress together, then return
  tl.to(
    ".cursor",
    {
      scale: CURSOR_PRESS_SCALE,
      duration: PRESS_DUR,
      ease: "power2.in",
      yoyo: true,
      repeat: 1,
    },
    CLICK_AT,
  );
  tl.to(
    ".target-button",
    {
      scale: TARGET_PRESS_SCALE,
      duration: PRESS_DUR,
      ease: "power2.in",
      yoyo: true,
      repeat: 1,
    },
    CLICK_AT,
  );

  // Phase 3 — Ripple burst, N rings staggered from the click point
  tl.set([".ripple-1", ".ripple-2", ".ripple-3"], { opacity: 1 }, RIPPLE_AT);
  tl.to(
    [".ripple-1", ".ripple-2", ".ripple-3"],
    {
      scale: RIPPLE_SCALE,
      opacity: 0,
      duration: RIPPLE_DUR,
      ease: RIPPLE_EASE,
      stagger: RIPPLE_STAGGER,
      immediateRender: false,
    },
    RIPPLE_AT,
  );

  window.__timelines["cursor-click-scene"] = tl;
</script>
```

## 如何选取数值

- **MOVE_DUR** — 光标从入口移动到目标所需时间（秒）
  - 范围：0.4–1.0 s
  - 效果：较短显得敏捷；较长显得从容 /「深思熟虑的点击」
  - 约束：必须在 `CLICK_AT` 之前结束——否则点击发生时光标仍在移动，会被读成误点
  - 参考：../../examples/cta-orbit-collapse.html 使用 0.5 s

- **MOVE_EASE** — 移动补间的缓动族
  - 离散选择。选项：
    - `power2.inOut` — 对称、平稳；适合「用户有意识地移动光标」
    - `back.out(<n>)` — 落点时略 overshoot；适合希望光标「落到」按钮上并带轻微可见回弹的场景。配合较低 overshoot 系数（约 1.2–1.4）——更高会显得卡通
    - `power3.out` — 起步快、落地软；适合「果断」的移动
  - 参考：../../examples/cta-orbit-collapse.html 使用 `back.out(1.3)`

- **CLICK_AT** — 点击触发时间（秒）
  - 范围：必须 ≥ `MOVE_DUR`（光标已停稳）；通常为 `MOVE_DUR + 0.0–0.3 s` 的「决策停顿」
  - 效果：零停顿像自动播放；停顿 >0.3 s 像犹豫
  - 参考：../../examples/cta-orbit-collapse.html 在光标停稳后 0.2 s 点击

- **PRESS_DUR** — 下压半周期时长（yoyo 完整周期为两倍）
  - 范围：0.06–0.12 s
  - 效果：短则干脆；长则发黏
  - 约束：总按压 = `2 * PRESS_DUR`；必须在下一阶段需要光标/目标恢复常规模之前结束
  - 参考：../../examples/cta-orbit-collapse.html 使用 0.08 s

- **CURSOR_PRESS_SCALE / TARGET_PRESS_SCALE** — 点击时各自压缩幅度
  - 范围：光标 0.80–0.90；目标 0.92–0.97
  - 效果：数值越小「这次点击很重要」感越强；接近 1 像轻触
  - 约束：光标应比目标压得更深——光标是执行者，目标是承受者
  - 参考：../../examples/cta-orbit-collapse.html 使用 cursor 0.85 / target 0.95

- **RIPPLE_AT** — 环开始扩散的时间（秒）
  - 范围：`CLICK_AT + 0.0–0.08 s`
  - 效果：与按压同时显得因果直接；略延迟像声学效果（「先点击，再波向外辐射」）
  - 参考：../../examples/cta-orbit-collapse.html 恰好在 `CLICK_AT` 启动涟漪

- **RIPPLE_DUR** — 每个环完全扩散并淡出的时长
  - 范围：0.5–1.0 s
  - 效果：短环锐利；长环像柔和声呐
  - 约束：必须在依赖环已消失的阶段（如屏幕擦除）之前完成
  - 参考：../../examples/cta-orbit-collapse.html 使用 0.7 s

- **RIPPLE_SCALE** — 淡出前每个环的最终 scale
  - 范围：3–6
  - 效果：3 让环留在点击附近；6 可扫过周围区域
  - 约束：若环在 opacity 到 0 前就离开可见区域，应降低 scale 或缩短 duration
  - 参考：../../examples/cta-orbit-collapse.html 使用 5

- **RIPPLE_STAGGER** — 相邻环之间的延迟
  - 范围：0.06–0.12 s（单环时可为 0；见「变体」）
  - 效果：低于约 0.06 s 像一条厚环；高于约 0.12 s 像独立事件
  - 参考：../../examples/cta-orbit-collapse.html 使用单环（无 stagger）

- **RIPPLE_EASE** — 扩散的缓动族
  - 离散选择。选项：
    - `power2.out` — 起步快、尾部软；标准「ping」感
    - `power3.out` — 更锐的攻击、更长的尾
    - `expo.out` — 几乎瞬间扩张加长 quiet 淡出；像强而远的脉冲
  - 参考：../../examples/cta-orbit-collapse.html 使用 `power2.out`

- **TARGET_X / TARGET_Y** — 点击目标相对光标 CSS 原点的像素偏移
  - 这些由布局推导，不是创意旋钮——必须与实际点击目标的视觉质心一致。偏差 4 px 就会被读成没点到按钮
  - 参考：../../examples/cta-orbit-collapse.html 将白色按钮对准 `CENTER_X + 130, CENTER_Y + 15`

## 变体

- **单环** — 只保留一个 `.ripple` 元素，去掉 stagger；场景其余部分较忙时更雅致
- **关键帧 attack-decay** — 用 `keyframes` 块替代简单 expand-and-fade，在 duration 内将 opacity 0 → 峰值 → 0；能量辐射再消散的包络更清晰（../../examples/cta-orbit-collapse.html 中使用）
- **多环 expanding pulse** — 3 个环、0.08 s stagger；当点击是场景高潮时刻时层次更丰富

## 核心原则

- **先移动再点击**：仅在移动 tween 停稳后触发点击——移动中点击会被读成无意
- **同步下压**：光标与目标在同一 `position` 时间、相同 duration 下压（并都 yoyo 回弹）
- **涟漪从点击点发出**：涟漪从精确点击位置（按钮视觉中心）扩散，而非任意元素 bounding-box 原点
- **微妙缩放**：光标比目标压得更深——见 `CURSOR_PRESS_SCALE` / `TARGET_PRESS_SCALE`
- **光标高 z-index**：整个序列中光标渲染在所有内容之上

## 关键约束

- **时间轴必须 paused**：`gsap.timeline({ paused: true })`。切勿调用 `tl.play()`——HyperFrames 逐帧 seek 时间轴以保持确定性
- **注册键 = `data-composition-id`**：`window.__timelines["<id>"]` 必须与场景根上的 `data-composition-id` 完全一致
- **涟漪 expand 上 `immediateRender: false`**：在点击时刻之前保持初始状态（`scale: 0`、`opacity: 0`），否则 tween 会预渲染，环在 t=0 以错误尺寸出现
- **有限 duration**：确认 `tl.duration()` 与场景的 `data-duration` 一致
- **光标与涟漪 `pointer-events: none`**：纯视觉；不阻挡底层交互（对可 hover 的导出很重要）
- **不用 CSS transitions / animations**：所有动效在 GSAP 时间轴中，以便 seek 保持确定性

## 组合

- [orbit-3d-entry.md](orbit-3d-entry.md) — 当点击是枢纽，使轨道元素向光标目标收拢时
- [center-outward-expansion.md](center-outward-expansion.md) — 点击可作为从点击点向外爆发的触发
- [press-release-spring.md](press-release-spring.md) 用于目标按钮更强的物理感
- [scale-swap-transition.md](scale-swap-transition.md) 用于点击后按钮状态变化（按钮 morph 成成功态、下一视图等）

## 搭配的 HF 技能

- `/hyperframes-animation` — 时间轴 + tween API 参考（eases、stagger、`immediateRender` 等）
- `/hyperframes-core` — 合成接线（`data-*` 属性、场景结构、注册约定）
- `/hyperframes-cli` — `hyperframes lint` 校验注册键与 duration 是否匹配
