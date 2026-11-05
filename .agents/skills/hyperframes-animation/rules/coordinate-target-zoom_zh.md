---
name: coordinate-target-zoom
description: 通过将缩放与反向平移组合，放大特定非居中元素——缩放完成后目标落在视口中心。
metadata:
  tags: camera, zoom, scale, translate, target, off-center, focus
---

# 坐标目标缩放（Coordinate Target Zoom）

在包装层上单纯使用 `scale > 1` 会把偏离中心的内容推出可见画布。若要 _放大_ 某个非居中元素，需同步施加缩放与反向平移，使目标在缩放结束后落在视口中心。

## 工作原理

两层嵌套包装，职责分离：

1. **外层包装** 施加 `scale`（缩放）
2. **内层包装** 施加 `translate(x, y)`（反向位移）

平移量是目标相对中心 **偏移的取反**。内层平移在外层缩放生效前，先把目标移回外层的变换原点，因此以中心为基准的缩放会把目标映射到 0。

```
T = -offset
```

推导（外层缩放内层已平移的内容）：

1. 内层平移在缩放前单位下移动目标 T → 目标位于 `offset + T`
2. 外层缩放 S（绕中心 0,0）将其映射为 `S × (offset + T)`
3. 要使目标落在视口中心：`S × (offset + T) = 0` → **`T = -offset`**

注意：该公式 **不依赖** S。只要 **外层** 是缩放、**内层** 是平移，且缩放使用 `transform-origin: 50% 50%`，平移量无论是 1.5×、2× 还是 3× 都相同。

## 获取偏移量

`T = -offset` 的好坏完全取决于 `offset`。此模式上线后最常坏掉的方式，是用布局公式 **手算** `offset`，**符号** 或量级错了，缩放再把小误差放大到画外。**默认应测量目标真实布局后的中心；对称行才保留公式。**

### 默认 — 测量目标实际中心（适用于任意布局）

在 setup 时读取目标真实位置一次。因来自渲染后的 DOM 而非心智模型，不会搞错符号：

```js
await document.fonts.ready; // metrics final; fallback fonts are 10–30px off → tens of px after a 3×+ zoom
const W = 1920,
  H = 1080;
const r = document.getElementById("target-card").getBoundingClientRect();
const TARGET_OFFSET_X = r.left + r.width / 2 - W / 2;
const TARGET_OFFSET_Y = r.top + r.height / 2 - H / 2;
// bake these; feed counterX/Y = -TARGET_OFFSET_X/Y to the inner tween
```

此 `getBoundingClientRect` 在 **setup 时运行一次**，早于时间轴注册 — **不要** 每帧调用（每帧读 DOM 会与渲染器并行采样不同步；见 SKILL 通用约束）。因测量是异步的（`fonts.ready`），在同一 `async` setup 内构建并注册时间轴，确保在发布 `window.__timelines[id]` 前偏移已烘焙完成。

### 快捷 — 仅对称等宽行

当且仅当目标是居中行内 N 张 **等宽** 卡片之一、间距均匀时，可跳过测量：

```js
const index_offset = targetIndex - (N - 1) / 2;
const TARGET_OFFSET_X = index_offset * (CARD_WIDTH + CARD_GAP);
```

⚠️ 这假设每个兄弟节点 **宽度相同**。行一旦不对称 — 宽 companion 标签旁窄 chip、两侧不等宽的 wordmark — 就会算错，常是 **符号** 反了：较重一侧会把居中目标往与直觉 _相反_ 的方向推。（真实例子：`companion(220) + gap + wordmark + gap + chip(110)` 使 wordmark 相对中心偏 **右** ~55px，但「chip − companion」直觉会猜左。）除等宽卡片外，**请测量**。

### 余量预算 — 由测量尺寸限制缩放

缩放会放大任何居中误差，因此要留边距。峰值时目标约占画布 ≤ ~88%；用测量尺寸推导上限，不要凭感觉取整：

```js
const maxScale = Math.min((0.88 * W) / r.width, (0.88 * H) / r.height);
const ZOOM_SCALE = Math.min(DESIRED_SCALE, maxScale);
```

占帧 97%+ 的目标，中心稍偏就会显得被裁切 — 手烘焙偏移几乎总会偏一点。（感知门会标为 `primary-offscreen`，`data-layout-allow-overflow` **不能** 豁免。）

## HTML

```html
<div
  class="scene"
  id="zoom-scene"
  data-composition-id="zoom-scene"
  data-start="0"
  data-duration="5"
  data-track-index="0"
>
  <div class="zoom-outer" id="zoom-outer">
    <div class="zoom-inner" id="zoom-inner">
      <div class="content">
        <!-- Several layout elements; one is the "target" -->
        <div class="card other">
          <div class="label">{label1}</div>
          <div class="price">{price1}</div>
        </div>
        <div class="card other">
          <div class="label">{label2}</div>
          <div class="price">{price2}</div>
        </div>
        <div class="card target" id="target-card">
          <div class="label">{targetLabel}</div>
          <div class="price">{targetPrice}</div>
          <div class="tag">{targetTagline}</div>
        </div>
        <div class="card other">
          <div class="label">{label4}</div>
          <div class="price">{price4}</div>
        </div>
      </div>
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
  overflow: hidden;        /* REQUIRED — see Critical Constraints */
  background: {bgGradient};
}
.zoom-outer {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  transform-origin: 50% 50%;
  will-change: transform;
}
.zoom-inner {
  display: grid;
  place-items: center;
  will-change: transform;
}
.content {
  display: flex;
  gap: CARD_GAP;
}
.card {
  width: CARD_WIDTH;
  padding: CARD_PADDING;
  border-radius: CARD_RADIUS;
  background: {cardBg};
  border: 1px solid {cardBorder};
  text-align: center;
  font-family: {font};
}
.card.target {
  background: {targetCardBg};       /* slightly brighter than .card */
  border: 2px solid {targetBorder};
  box-shadow: {targetGlow};
}
.label {
  font-size: LABEL_FONT_SIZE;
  font-weight: 800;
  letter-spacing: 6px;
  text-transform: uppercase;
  color: {labelColor};
}
.price {
  font-size: PRICE_FONT_SIZE;
  font-weight: 900;
  color: {textColor};
  margin: 16px 0;
  font-variant-numeric: tabular-nums;
}
.tag {
  font-size: TAG_FONT_SIZE;
  font-weight: 700;
  letter-spacing: 4px;
  color: {accentColor};
  opacity: 0;
}
```

## GSAP 时间轴

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // TARGET_OFFSET_X / TARGET_OFFSET_Y and ZOOM_SCALE come from the "Getting the
  // offset" section above — MEASURED at setup (after fonts.ready) and baked. Do NOT
  // hand-derive the offset for a non-symmetric layout (wrong sign → the zoom shoves
  // the target off-frame). For a measured target, build the timeline inside that
  // async setup so the offset is ready before window.__timelines[id] is published.

  // Counter-translation = -offset (inner translate cancels target offset BEFORE outer scales)
  const counterX = -TARGET_OFFSET_X;
  const counterY = -TARGET_OFFSET_Y;

  // Phase 1 — cards reveal
  tl.from(
    ".card",
    { opacity: 0, y: REVEAL_Y, stagger: REVEAL_STAGGER, duration: REVEAL_DUR, ease: "power3.out" },
    REVEAL_START,
  );

  // Phase 2 — pause to let viewer scan the layout

  // Phase 3 — zoom into target
  tl.to(
    "#zoom-outer",
    {
      scale: ZOOM_SCALE,
      duration: ZOOM_DUR,
      ease: "power3.inOut",
    },
    ZOOM_START,
  );
  tl.to(
    "#zoom-inner",
    {
      x: counterX,
      y: counterY,
      duration: ZOOM_DUR,
      ease: "power3.inOut",
    },
    ZOOM_START,
  );

  // Phase 4 — target "tag" reveals inside the zoomed-in target
  tl.to(
    ".target .tag",
    { opacity: 1, duration: TAG_REVEAL_DUR, ease: "power2.out" },
    TAG_REVEAL_START,
  );

  // Phase 5 — climax dwell — viewer reads the target content
  // (no additional motion; the zoomed-in state holds for DWELL_DUR seconds)

  window.__timelines["zoom-scene"] = tl;
</script>
```

## 变体

### 通过 `getBoundingClientRect` 动态查找目标

这已是 **默认做法**，而非变体 — 见 [获取偏移量](#getting-the-offset)。测量前务必 `await document.fonts.ready`（回退字体会差 10–30px，3×+ 缩放会放大成数十像素可见误差），且 **仅在 setup 时测量一次**，不要每帧测量。

### 缩小（目标 → 广角）

阶段反转 — 从已放大状态开始，再 `scale: 1` + `x: 0, y: 0` 拉回。「揭示」节拍就是全景。

### 多目标缩放序列

链式多次缩放：目标 A（1.5–2.5s）→ 停顿 → 目标 B（3–4s）→ 拉回（4.5–5s）。每段需要各自的反向平移对。

## 如何选取数值

### 布局

- **CARD_WIDTH / CARD_GAP / CARD_PADDING / CARD_RADIUS** — 几何布局。
  - 约束：`N × CARD_WIDTH + (N-1) × CARD_GAP < viewportWidth`，缩放前所有卡片能放下
  - 效果：卡片更小 → 同屏兄弟更多 → 构图更忙；更大 → 兄弟更少、单卡更突出
- **LABEL_FONT_SIZE / PRICE_FONT_SIZE / TAG_FONT_SIZE** — 字级层次。
  - 范围：tag < label < price（缩放后 price 是焦点；最大字号强化这一点）

### 揭示阶段

- **REVEAL_START** — 卡片开始淡入的时刻。
  - 约束：通常略偏移（~0.2s），内容出现前留一 beat 黑场
- **REVEAL_DUR** — 单卡淡入上移时长。
  - 范围：0.4–0.8s
- **REVEAL_Y** — 淡入前每卡初始垂直偏移（px）。
  - 范围：16–48 px；更大像「扔进来」，更小更柔和
- **REVEAL_STAGGER** — 相邻卡片揭示间隔。
  - 范围：0.06–0.15s；校准到全部在 `ZOOM_START` 前结束

### 缩放阶段

- **ZOOM_START** — 缩放开始时刻。
  - 约束：`≥ REVEAL_START + REVEAL_DUR + (N-1) × REVEAL_STAGGER + viewer-scan-time`（缩放前给观者 0.5–1.5s 读布局）
- **ZOOM_DUR** — 缩放 tween 时长。
  - 范围：1.0–2.0s；低于 0.8s 像瞬移，超过 2.5s 拖沓
  - 约束：scale tween 与 counter-translate tween **必须** 共用此时长 **且** ease
- **ZOOM_SCALE** — 最终倍率。
  - 范围：1.5×（适度强调）→ 3×（主导焦点）→ 5×+（电影感极端）
  - 约束：该倍率下卡片内容仍清晰；栅格源媒体需 `sourceResolution ≥ rendered × ZOOM_SCALE`
  - **余量预算**：由测量目标尺寸封顶，峰值目标 ≤ 画布 ~88% — `ZOOM_SCALE = Math.min(DESIRED, 0.88×W/r.width, 0.88×H/r.height)`。凭感觉取整（如 585px wordmark 用 3.2× → 1872px = 1920 的 97%）没有余量，居中稍偏就会裁切文字。

### 目标揭示与停留

- **TAG_REVEAL_START** — 目标隐藏 tag 淡入时刻。
  - 约束：`≥ ZOOM_START + ZOOM_DUR`（缩放落定后再揭示，观者视线已在目标上）
- **TAG_REVEAL_DUR** — tag 淡入时长。
  - 范围：0.3–0.6s
- **DWELL_DUR** — 缩放后停留供阅读。
  - 范围：tag 揭示后 ≥ 1.0s（见「关键原则」中的 Climax dwell）

### 颜色 token

- **{bgGradient}** — 通常为暗色径向渐变，卡片四周 vignette
- **{cardBg} / {cardBorder}** — 非目标卡（低调、退后）
- **{targetCardBg} / {targetBorder} / {targetGlow}** — 目标卡更亮 / 光晕，缩放前 eye 就落上去
- **{labelColor} / {textColor} / {accentColor}** — 文本层次色；`{accentColor}` 留给 tag（揭示时弹出）

## 关键原则

- **测量偏移，不要手推** — 除对称等宽行外，setup 时（`fonts.ready` 后）用 `getBoundingClientRect` 读目标真实中心并烘焙（见 [获取偏移量](#getting-the-offset)）。手算偏移在不对称布局上常 **符号** 静默错误，缩放把误差放大到画外 — 此模式最常见的上线故障。
- **变换顺序 — 外层 scale，内层 translate** — **不要** 在同一元素上同时 scale 与 translate。变换数学会缠在一起（CSS 中 `translate * scale` ≠ `scale * translate`）。嵌套包装干净分离职责。
- **Counter-translate = -offset** — 与 scale 无关。推导：外层绕中心缩放把 `(offset + T)` 映射为 `S × (offset + T)`，令其为零得 `T = -offset`。常见错误直觉是 `T = -offset × (S - 1)` — S=2 时碰巧相同，其他 S 都错。
- **外层 `transform-origin: 50% 50%`** — 非中心原点会导致内层偏移不可预测；始终居中。
- **`.scene` 上 `overflow: hidden` 必需** — zoom > 1 时外层缩放内容可能溢出 1920×1080 帧。
- **scale 与 counter-translate 一起 tween** — **必须** 共用 `duration` 与 `ease`，否则缩放过程中目标漂移（可见「游移」）。最简单：同一时间位置给两个 tween 相同参数。
- **❗ Climax dwell：缩放完成后 ≥1s** — 见 SKILL 通用约束。若 3.5s 成片在 t=3.0 结束缩放，观者几乎看不清目标；目标缩放后停留 1.5–2s。

## 关键约束

- **时间轴必须 paused**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **`.zoom-outer` / `.zoom-inner` 上不要用 CSS `transition`** — 与 GSAP 冲突
- **两层包装 `will-change: transform`** — 缩放阶段每帧更新变换
- **`.zoom-outer` 上 `transform-origin: 50% 50%`** — counter-translate 数学假设以中心缩放
- **目标偏移 setup 时测量一次并烘焙** — `fonts.ready` 后测目标中心并烘焙（见 [获取偏移量](#getting-the-offset)）；勿在 onUpdate 每帧重算，勿对非对称布局手估偏移
- **缩放落在余量预算内** — 峰值目标 ≤ 画布 ~88%，由测量尺寸推导（`maxScale = 0.88 × W / measuredWidth`）；占满帧的目标中心稍偏即被裁

## 组合

- [multi-phase-camera.md](multi-phase-camera.md) — 含 coordinate-target-zoom 阶段的多相位镜头
- [sine-wave-loop.md](sine-wave-loop.md) — 缩放落定后目标上的 idle 呼吸
- [discrete-text-sequence.md](discrete-text-sequence.md) — 缩放完成 **前** 在目标内组装文本

## 搭配的 HF 技能

- `/hyperframes-animation` — 两个协调 tween
- `/hyperframes-core` — 合成体接线
- `/hyperframes-cli` — `hyperframes lint`
