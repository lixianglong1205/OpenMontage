---
name: viewport-change
description: 虚拟摄像机 — 通过变换包裹全部场景内容的 wrapper 模拟缩放 / 平移 / 焦点锁定。摄像机向右移动 → 世界向左平移。
metadata:
  tags: viewport, camera, zoom, pan, focus-lock, virtual-camera
---

# 视口变化（虚拟摄像机）

通过变换包裹**全部**场景内容的 wrapper，模拟摄像机效果（缩放 / 平移 / 对移动元素焦点锁定）。「世界」与感知到的摄像机运动方向相反。与 [multi-phase-camera](multi-phase-camera.md)（2–3 个离散阶段 + 漂移）不同 — viewport-change 是单次连续的缩放/平移，常用于跟随移动元素的焦点锁定。

## 工作原理

摄像机意图 → 世界变换：

- 摄像机**向右平移** → 世界 `translateX(-distance)`
- 摄像机**放大** → 世界 `scale(>1)`
- 摄像机**跟随元素 X** → 每帧更新世界 `translateX(viewportCenter - elementWorldX)`

wrapper 承载摄像机变换；内部元素仍在「世界空间」中定位，本身不变。

**单元素复合变换（本规则的形态）。** scale 与 translate 都在**同一个** wrapper 上，形式为 `translate(x, y) scale(S)`。CSS 先应用 scale，再应用 translate（矩阵从右到左组合），因此世界偏移 `(ox, oy)` 处的点落在屏幕 `(S × ox + x, S × oy + y)`。要将目标对准视口中心：

```
T = -offset × S
```

这与 [coordinate-target-zoom](coordinate-target-zoom.md) **不同** — 后者使用两层嵌套 wrapper（外层 scale、内层 translate），并导出 `T = -offset`（与 S 无关）。当你希望用单一事实来源维护摄像机状态（`cam.scale`、`cam.x`、`cam.y`）并通过 `onUpdate` 更新时，使用本规则的单 wrapper 形态；当 scale 与 translate 可独立缓动且共享同一 ease 时，使用嵌套 wrapper。

## HTML

```html
<div
  class="scene"
  id="viewport-scene"
  data-composition-id="viewport-scene"
  data-start="0"
  data-duration="5"
  data-track-index="0"
>
  <div class="world" id="world">
    <div class="content">
      <div class="hero" id="hero">{Brand}</div>
      <div class="tagline">{tagline}</div>
      <div class="cta-row">
        <div class="cta" id="cta">{ctaUrl}</div>
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
  overflow: hidden;
  background: {bgGradient};
  font-family: {font};
}
.world {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  transform-origin: 50% 50%;
  will-change: transform;
}
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: CONTENT_GAP;
  text-align: center;
}
.hero {
  font-size: HERO_FONT_SIZE;
  font-weight: 900;
  letter-spacing: HERO_LETTER_SPACING;
  text-transform: uppercase;
  color: {textColor};
}
.tagline {
  font-size: TAGLINE_FONT_SIZE;
  font-weight: 600;
  color: {labelColor};
}
.cta {
  display: inline-block;
  padding: CTA_PADDING_Y CTA_PADDING_X;
  font-family: {monoFont};
  font-size: CTA_FONT_SIZE;
  font-weight: 700;
  letter-spacing: CTA_LETTER_SPACING;
  color: {accentColor};
  text-transform: uppercase;
  background: {ctaBg};
  border: 1px solid {ctaBorder};
  border-radius: CTA_BORDER_RADIUS;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const world = document.getElementById("world");

  // Camera state — single source of truth. World transform is composed from
  // this object inside applyCamera() so the transform string order is stable.
  const cam = { scale: 1, x: 0, y: 0 };

  function applyCamera() {
    world.style.transform = `translate(${cam.x}px, ${cam.y}px) scale(${cam.scale})`;
  }
  applyCamera();

  // Phase 1 — content reveal at neutral camera
  tl.from(".hero", { opacity: 0, y: HERO_Y, duration: HERO_DUR, ease: "power3.out" }, HERO_START);
  tl.from(
    ".tagline",
    { opacity: 0, y: TAGLINE_Y, duration: TAGLINE_DUR, ease: "power3.out" },
    TAGLINE_START,
  );

  // Phase 2 — zoom in on CTA (single-element composite transform)
  // CSS applies scale FIRST then translate: world point (ox, oy) lands at
  // (S × ox + x, S × oy + y). Solve S × offset + T = 0 → T = -offset × S.
  // This is DIFFERENT from coordinate-target-zoom (nested wrappers, T = -offset).
  const counterY = -TARGET_OFFSET_Y * TARGET_SCALE;

  tl.to(
    cam,
    {
      scale: TARGET_SCALE,
      y: counterY,
      duration: ZOOM_DUR,
      ease: "power3.inOut",
      onUpdate: applyCamera,
    },
    ZOOM_START,
  );

  // Phase 3 — CTA reveals/dwells after zoom settles
  tl.from(
    "#cta",
    {
      opacity: 0,
      scale: CTA_REVEAL_SCALE,
      duration: CTA_REVEAL_DUR,
      ease: `back.out(${BOUNCE_FACTOR})`,
    },
    CTA_REVEAL_START,
  );

  window.__timelines["viewport-scene"] = tl;
</script>
```

## 缩放取值指南

| 效果   | Scale       | 观感                                |
| ------ | ----------- | ----------------------------------- |
| 轻微   | 1.02 - 1.05 | 几乎察觉不到 — 「专业感」           |
| 中等   | 1.05 - 1.15 | 「Ta-da」式强调                     |
| 明显   | 1.15 - 1.30 | 聚焦某一区域                        |
| 戏剧化 | 1.5 - 2.5   | 元素占满画面                        |
| 全屏   | 3.0+        | 元素覆盖视口                        |

| 感知阈值 | 结果                 |
| -------- | -------------------- |
| < 5%     | 难以察觉             |
| 10-15%   | 舒适的强调感         |
| > 30%    | 电影感 / 戏剧化      |

## 变体

### 焦点锁定（摄像机跟随移动光标/角色）

对于在世界中横向移动的元素，将其保持在固定的屏幕 X 位置。每帧计算世界偏移：

```js
const focusEl = document.querySelector(".moving-cursor");
const targetScreenX = VIEWPORT_WIDTH * FOCUS_SCREEN_X_FRAC;
const focusUpdate = { p: 0 };
tl.to(
  focusUpdate,
  {
    p: 1,
    duration: FOLLOW_DUR,
    ease: "power2.inOut",
    onUpdate: () => {
      const rect = focusEl.getBoundingClientRect();
      const focusWorldX = rect.left + rect.width / 2;
      cam.x = targetScreenX - focusWorldX;
      applyCamera();
    },
  },
  FOLLOW_START,
);
```

### 复合缩放（多阶段）

将两个 scale 缓动相乘，得到叠加效果：

```js
const scaleUp = { v: 1 };
const scaleDown = { v: 1 };
function applyCompositeCamera() {
  cam.scale = scaleUp.v * scaleDown.v;
  applyCamera();
}
tl.to(
  scaleUp,
  { v: SCALE_UP_TARGET, duration: SCALE_UP_DUR, onUpdate: applyCompositeCamera },
  SCALE_UP_START,
);
tl.to(
  scaleDown,
  { v: SCALE_DOWN_TARGET, duration: SCALE_DOWN_DUR, onUpdate: applyCompositeCamera },
  SCALE_DOWN_START,
);
```

### 摄像机模式切换（居中 → 跟随）

通过 0→1 的权重缓动，在两种摄像机模式间交叉淡入。权重为 0 时为模式 A；为 1 时为模式 B；中间值为插值结果。

## 如何选取参数

### 布局（CSS）

- **CONTENT_GAP** — hero、tagline 与 CTA 之间的垂直间距。
  - 范围：16-48 px
  - 效果：偏小 → 紧凑堆叠（logo 组合感）；偏大 → 疏朗、编辑感
- **HERO_FONT_SIZE / TAGLINE_FONT_SIZE / CTA_FONT_SIZE** — 字体层级。
  - 范围：hero >> tagline > CTA（hero 为品牌标识，CTA 为可操作的页脚）
  - 约束：在中性摄像机下缩小显示时，以及缩放过程中放大时，hero 仍须可读 — 在中性摄像机下选定字号，缩放只会放大
- **HERO_LETTER_SPACING / CTA_LETTER_SPACING** — 大写字的字距。
  - 范围：大写展示字体 4-10 px；句子大小写为 0
- **CTA_PADDING_X / CTA_PADDING_Y / CTA_BORDER_RADIUS** — CTA 文字周围的胶囊形几何。
  - 约束：`CTA_BORDER_RADIUS ≥ CTA_FONT_SIZE`，以保证胶囊两端完全圆角

### 阶段 1 — 内容显现

- **HERO_START** — hero 开始淡入的时刻。
  - 范围：0.2-0.5s（内容出现前留一小段黑场）
- **HERO_DUR** — hero 上滑淡入时长。
  - 范围：0.6-1.2s
- **HERO_Y** — 淡入前 hero 的初始 Y 偏移（px）。
  - 范围：16-48 px
- **TAGLINE_START** — tagline 开始淡入的时刻。
  - 约束：`≥ HERO_START + 0.3`（先让 hero 落定，视线自上而下阅读）
- **TAGLINE_DUR / TAGLINE_Y** — 与 hero 同形，通常更小（`TAGLINE_Y` 约为 `HERO_Y` 的一半）。

### 阶段 2 — 缩放

- **TARGET_OFFSET_Y** — 中性摄像机下 CTA 相对视口中心的 Y 偏移（px）。
  - 约束：由布局推导，非自由参数。通过 `getBoundingClientRect()` 测量，或由 `CONTENT_GAP + (HERO_HEIGHT + TAGLINE_HEIGHT) / 2` 计算。符号重要 — 正数表示在中心下方。
- **TARGET_SCALE** — 世界的最终放大倍数。
  - 范围：1.3×（温和）→ 1.6-2.0×（典型 CTA 缩放）→ 3×+（电影感）
  - 约束：栅格源媒体需 `sourceResolution ≥ rendered × TARGET_SCALE`；文字任意缩放仍清晰
- **ZOOM_START** — 缩放开始的时刻。
  - 约束：`≥ TAGLINE_START + TAGLINE_DUR + viewer-scan-time`（内容落定后约 0.5s 再动摄像机）
- **ZOOM_DUR** — 缩放缓动时长。
  - 范围：1.0-2.0s；低于 0.8s 像瞬移，超过 2.5s 显得拖沓

### 阶段 3 — CTA 显现 + 停留

- **CTA_REVEAL_START** — CTA 弹入的时刻。
  - 约束：`≥ ZOOM_START + ZOOM_DUR × 0.9`（接近缩放尾声开始，使 CTA 与摄像机一起「落定」）
- **CTA_REVEAL_DUR** — CTA 淡入 / 弹出时长。
  - 范围：0.4-0.8s
- **CTA_REVEAL_SCALE** — 弹出前 CTA 的初始 scale。
  - 范围：0.85-0.95（小于 1 → 长到位置）；>1.0 反转为缩进到位的感觉
- **BOUNCE_FACTOR** — `back.out(${BOUNCE_FACTOR})` 的过冲系数。
  - 范围：1.2-2.5；越低落定越轻微，越高过冲越明显。ease 族（`back.out`）已定；该数值调节强度。
  - 参考：ease 族选项：`back.out`（过冲后落定）、`elastic.out`（振荡）、`power3.out`（干净减速、无过冲）
- **DWELL_DUR** — 在 `CTA_REVEAL_START + CTA_REVEAL_DUR` 之后到 `data-duration` 结束前的隐含停留。
  - 范围：≥ 1.0s（见关键原则中的「高潮停留」）

### 焦点锁定变体

- **VIEWPORT_WIDTH** — 合成宽度（px）。真实值（根节点上的 `data-width`）；非抽象量。
- **FOCUS_SCREEN_X_FRAC** — 焦点元素锁在屏幕上的横向位置。
  - 范围：0.4-0.7（三分法位置）；0.5 为正中心
- **FOLLOW_START / FOLLOW_DUR** — 跟随摄像机何时介入及持续多久。
  - 约束：`FOLLOW_DUR` 与焦点元素处于运动中的时长一致

### 复合缩放变体

- **SCALE_UP_TARGET / SCALE_DOWN_TARGET** — 通过 `cam.scale = scaleUp.v * scaleDown.v` 组合的乘性因子。
  - 效果：慢速推近（`SCALE_UP_TARGET` ~1.15）与短暂回弹（`SCALE_DOWN_TARGET` ~0.9）组合，形成呼吸/冲击形
- **SCALE_UP_START / SCALE_UP_DUR / SCALE_DOWN_START / SCALE_DOWN_DUR** — 各乘数的阶段时序。

### 颜色 token

- **{bgGradient}** — 场景背景（通常为暗色径向晕影，缩放时边缘自然淡出）
- **{textColor}** — hero 文字；与 `{bgGradient}` 对比最高
- **{labelColor}** — tagline / 次要文案；比 `{textColor}` 柔和一档
- **{accentColor}** — CTA 文字 + 边框；显现时跳出的保留色相
- **{ctaBg} / {ctaBorder}** — 由 `{accentColor}` 衍生的半透明填充（典型 alpha 10-15% / 35-45% 的 `rgba`）

### 字体 token

- **{font}** — 无衬线正文 / hero 栈（如 `"Inter", sans-serif`）
- **{monoFont}** — 等宽 CTA 栈（如 `"JetBrains Mono", monospace`）；专用于 URL/代码感 CTA，读起来可点击

## 关键原则

- **世界与感知摄像机反向运动** — 摄像机向右平移 = 世界 wrapper 上 `translateX(-x)`。符号弄反则一切朝错误方向移动。
- **单 wrapper 变换顺序很重要** — `translate(x, y) scale(S)` 先 scale； counter-translate 为 `T = -offset × S`。与嵌套 wrapper 形态（`T = -offset`）混用会在 scale 变化时把目标带离中心。
- **`.scene` 上必须 `overflow: hidden`** — scale 非 1.0 时，世界变换会露出边缘或把内容推出画外。
- **世界 wrapper 上 `transform-origin: 50% 50%`** — 居中缩放是公式所假设的。
- **背景在 `.scene` 上，不在 `.world` 上** — 背景若在 world 上，变换 world 会扭曲/平移背景。
- **通过 `cam` 对象 + `applyCamera()` 单一事实来源** — scale 与 translate 同时变化时，只在一处写入。否则 transform 字符串组合顺序不可预测。
- **轻微连续运动 > 突然大缩放** — 要自然的产品视频感，用 2-3s 内 1.05-1.15×。大于 1.3× 的大缩放读作戏剧叙事时刻，留到需要时用。
- **高潮停留 >=1s** — 缩放落定后，合成须再持续 >=1s，观众才能读清焦点。

## 关键约束

- **时间线须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **`.world` 上不要用 CSS `transition`** — 与 GSAP 冲突
- **`.world` 上 `will-change: transform`**
- **`.scene` 上 `overflow: hidden`**
- **`.world` 上 `transform-origin: 50% 50%`**
- **背景在 `.scene` 上** — 绝不在 `.world` 上
- **scale 与 translate 共用一个 `onUpdate`** — 均从 `cam` 读取并一起写入复合 transform 字符串；切勿拆成直接改 `world.style.transform` 的多个缓动

## 组合

- [multi-phase-camera.md](multi-phase-camera.md) — 多阶段摄像机某一阶段内使用 viewport-change
- [coordinate-target-zoom.md](coordinate-target-zoom.md) — 偏中心缩放的替代方案（嵌套 wrapper、`T = -offset` 形态）
- [sine-wave-loop.md](sine-wave-loop.md) — 视口落定后的 idle 微漂移

## 搭配的 HF 技能

- `/hyperframes-animation` — 单次缓动写入复合 transform
- `/hyperframes-core` — 合成接线
- `/hyperframes-cli` — `hyperframes lint`