---
name: orbit-3d-entry
description: 元素从 3D 空间翻转进入，随后围绕焦点持续沿椭圆轨道运动。
metadata:
  tags: orbit, 3d, flip, ellipse, circular, icon, entry, continuous
---

# 带 3D 进入的轨道动画

元素从 3D 空间翻转进入（`rotateX` + `rotateY` + `translateZ`），随后过渡到围绕焦点的持续椭圆轨道运动。与一次性揭示不同——轨道会持续运行。

## 工作原理

每个元素分两个阶段：

1. **进入（逐元素）**：GSAP 从隐藏的 3D 朝向（`rotateX`、`rotateY`、负 `z`）补间到平面状态（`rotateX: 0, rotateY: 0, z: 0`）。使用弹簧感缓动（`back.out`）实现翻转进入。
2. **轨道（进入之后）**：围绕中心点的连续三角函数位置。元素的 `x`、`y` 平移由较慢角速度下的 `cos(t)` 和 `sin(t)` 驱动。

轨道在**时间轴内部**运行——而非通过 `requestAnimationFrame`——因此 HF 按帧 seek 保持确定性。

## HTML

```html
<div
  class="scene"
  id="orbit-scene"
  data-composition-id="orbit-scene"
  data-start="0"
  data-duration="5"
  data-track-index="0"
>
  <div class="orbit-stage">
    <div class="orbit-item" data-angle="0">{glyph1}</div>
    <div class="orbit-item" data-angle="60">{glyph2}</div>
    <div class="orbit-item" data-angle="120">{glyph3}</div>
    <div class="orbit-item" data-angle="180">{glyph4}</div>
    <div class="orbit-item" data-angle="240">{glyph5}</div>
    <div class="orbit-item" data-angle="300">{glyph6}</div>
    <div class="orbit-center">{centerLabel}</div>
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
  background: {sceneBackground};
  perspective: 1800px; /* REQUIRED — without perspective, rotateX/Y flatten */
}
.orbit-stage {
  position: relative;
  width: 1000px;
  height: 700px;
  display: grid;
  place-items: center;
  transform-style: preserve-3d;
}
.orbit-item {
  position: absolute;
  /* Items live at stage center; GSAP translates them along the orbit. */
  top: 50%;
  left: 50%;
  width: 140px;
  height: 140px;
  display: grid;
  place-items: center;
  background: {accentColor};
  border-radius: 50%;
  font-family: {font};
  font-weight: 900;
  font-size: 64px;
  color: {itemTextColor};
  transform-style: preserve-3d;
  will-change: transform;
  box-shadow: 0 12px 36px {accentShadowColor};
}
.orbit-center {
  position: relative;
  z-index: 5;
  font-family: {font};
  font-weight: 900;
  font-size: 96px;
  letter-spacing: 8px;
  color: {centerTextColor};
  text-transform: uppercase;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const items = document.querySelectorAll(".orbit-item");
  // RADIUS_X, RADIUS_Y, ORBIT_DURATION, ENTRY_DUR, STAGGER, FLIP_BACK, CENTER_BACK
  // — all named constants; values per "How to Choose Values" below.
  const RADIUS_Y = RADIUS_X * Y_TO_X_RATIO; // perspective-flattened ellipse

  items.forEach((el, i) => {
    const initialAngleDeg = Number(el.dataset.angle);
    const initialAngleRad = (initialAngleDeg / 360) * Math.PI * 2;
    const startX = Math.cos(initialAngleRad) * RADIUS_X;
    const startY = Math.sin(initialAngleRad) * RADIUS_Y;

    // 1) Place at orbital position with opacity 0 — BEFORE any tween fires
    gsap.set(el, {
      xPercent: -50,
      yPercent: -50,
      x: startX,
      y: startY,
      rotateX: ROTATE_X_FROM,
      rotateY: ROTATE_Y_FROM,
      z: Z_FROM,
      opacity: 0,
      scale: SCALE_FROM,
    });

    // 2) Phase 1 — flip in IN PLACE at orbital position
    tl.to(
      el,
      {
        rotateX: 0,
        rotateY: 0,
        z: 0,
        opacity: 1,
        scale: 1,
        duration: ENTRY_DUR,
        ease: `back.out(${FLIP_BACK})`,
      },
      i * STAGGER,
    );

    // 3) Phase 2 — continuous orbit driven via a 0→1 progress tween
    const orbitState = { p: 0 };
    tl.to(
      orbitState,
      {
        p: 1,
        duration: ORBIT_DURATION,
        ease: "none",
        onUpdate: () => {
          const angle = initialAngleRad + orbitState.p * Math.PI * 2;
          const x = Math.cos(angle) * RADIUS_X;
          const y = Math.sin(angle) * RADIUS_Y;
          // z-index by orbit Y — see "Center label clearance" in Key Principles
          // for the capped-range form when a center label is present.
          el.style.zIndex = String(Math.round(y + RADIUS_Y));
          el.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px)`;
        },
      },
      i * STAGGER + ENTRY_DUR,
    );
  });

  // Center label fades in once a few orbit items have landed
  tl.from(
    ".orbit-center",
    { opacity: 0, scale: 0.6, duration: ENTRY_DUR, ease: `back.out(${CENTER_BACK})` },
    CENTER_FADE_AT,
  );

  window.__timelines["orbit-scene"] = tl;
</script>
```

## 如何选取参数

- **RADIUS_X** — 轨道椭圆的水平半径，单位 px
  - 范围：300–900 px
  - 效果：较小半径呈现紧密簇状；较大半径让环铺满画面，并为较大的中心元素留出空间
  - 约束：在任意角度都必须与中心元素在水平方向错开——见「关键原则」中的 `RADIUS_X * min(|cos(θ)|) ≥ L_w + I_w + breathing_room` 规则
  - 参考：../../examples/cta-orbit-collapse.html 使用 480

- **Y_TO_X_RATIO** — `RADIUS_Y / RADIUS_X`，轨道的透视压扁比
  - 范围：0.4–0.7
  - 效果：较低数值像从上方看到的近水平圆盘；接近 1 则像正对镜头的平面
  - 约束：保持 < 1——轨道应像倾斜的环，而非正面的光晕
  - 参考：../../examples/cta-orbit-collapse.html 使用 ≈ 0.58

- **ORBIT_DURATION** — 完整一圈的秒数
  - 范围：4–25 s（环境背景用更长，主动功能动效用更短）
  - 效果：过短显得急促；过长显得漂移/平静
  - 约束：必须 ≥ 轨道在画面上的可见时长，否则补间结束元素会停住
  - 参考：../../examples/cta-orbit-collapse.html 有效约 25 s（轨道角速度 0.25 rad/s）

- **ENTRY_DUR** — 每个元素翻转进入的时长
  - 范围：0.4–0.8 s
  - 效果：短则有力；长则庄重
  - 约束：必须 ≤ 首尾元素启动间隔，避免层叠混乱
  - 参考：../../examples/cta-orbit-collapse.html 使用 0.55 s

- **STAGGER** — 相邻元素进入之间的延迟
  - 范围：0.06–0.12 s
  - 效果：低于约 0.06 s 像「爆米花」；高于约 0.12 s 显得拖沓
  - 约束：总层叠 `(n - 1) * STAGGER` 应在下一场景阶段开始前完成
  - 参考：../../examples/cta-orbit-collapse.html 使用 0.10 s

- **FLIP_BACK** — 翻转进入的 `back.out(<n>)`  overshoot
  - 范围：1.2–2.0
  - 效果：低端柔和落位；高端带明显 overshoot 的 snap
  - 约束：若与 `CENTER_BACK` 几乎同时触发，后者宜更 calm—— competing overshoot 会互相抵消
  - 参考：../../examples/cta-orbit-collapse.html 使用 1.4

- **CENTER_BACK** — 中心标签淡入的 `back.out(<n>)` overshoot
  - 范围：1.2–1.8
  - 效果：低端让标签在繁忙轨道下保持平静；高端给到达一点小「pop」
  - 参考：../../examples/cta-orbit-collapse.html 使用 1.4

- **CENTER_FADE_AT** — 中心标签淡入时刻，单位秒
  - 范围：在前 2–4 个元素落位之后
  - 效果：过早与层叠争抢；过晚轨道中心留空
  - 参考：../../examples/cta-orbit-collapse.html 在场景前段启动中心品牌

- **ROTATE_X_FROM / ROTATE_Y_FROM / Z_FROM / SCALE_FROM** — 初始 3D 朝向
  - 范围：rotateX ±60° 至 ±120°；rotateY ±45° 至 ±120°；z −200 至 −400；scale 0.2–0.6
  - 效果：绝对旋转更大 + z 更深负值 = 更 dramatic 的「卡片从深度翻出」；更低 =  subtle 重定向
  - 约束：方向与场景透视一致；各 item 混用正负 rotateY 会显得杂乱
  - 参考：../../examples/cta-orbit-collapse.html 使用 rotateX 90、rotateY −45、z −100、scale 0

## 变体

### 向中心坍缩

若要反转——先轨道再向内坍缩——在最终阶段用 1→0 的驱动将 `RADIUS_X` 和 `RADIUS_Y` 插值到 0：

```js
const collapse = { r: 1 };
tl.to(
  collapse,
  {
    r: 0,
    duration: COLLAPSE_DUR,
    ease: "power3.inOut",
    onUpdate: () =>
      items.forEach((el) => {
        const a = (Number(el.dataset.angle) / 360) * Math.PI * 2;
        const x = Math.cos(a) * RADIUS_X * collapse.r;
        const y = Math.sin(a) * RADIUS_Y * collapse.r;
        el.style.transform = `translate(-50%,-50%) translate(${x}px,${y}px) scale(${collapse.r})`;
      }),
  },
  COLLAPSE_AT,
);
```

### 倾斜轨道平面

若要更 dramatic 的 3D 轨道，将整个 `.orbit-stage` 绕 X 轴旋转：

```css
.orbit-stage {
  transform: rotateX(25deg);
}
```

赤道上下渲染的元素会在视觉上穿过该平面形成弧线。

## 关键原则

- **场景根节点必须有 `perspective`** — 没有它 rotateX/Y 会像 2D 缩放，翻转进入显得扁平
- **stage 与每个 item 都要 `transform-style: preserve-3d`** — 在各自 transform 下保留 3D 上下文
- **错开进入** — 层叠像「蜂群成形」，同时进入像「爆米花」。见「如何选取参数」中的 `STAGGER`
- **元素数量 4–12** — 更少显得空，更多挤占中心
- **❗ 中心标签 clearance — translateZ +  capped item z-index** — 在 `transform-style: preserve-3d` 的 stage 内，单靠 `z-index` 不可靠（绘制顺序跟 Z 位置，而非 stacking context 的 z-index）。要让轨道**绝不**遮挡标题：
  1. 将中心标签推前：`transform: translateZ(220px); z-index: 9999;`
  2. 将 orbit-item 动态 z-index 限制在 `[1, 50]`，使轨道底部 item 仍相对顶部 item 像「在前」，但**永不超过中心标签**。例如：`el.style.zIndex = String(1 + Math.round((y + RADIUS_Y) / (2 * RADIUS_Y) * 49));`
  3. **选取 `RADIUS_X` 使 item 在所有角度也在水平方向避开中心标签。** 若标签半宽为 `L_w`、item 半宽为 `I_w`，则须满足 `RADIUS_X * min(|cos(θ_minimum)|) ≥ L_w + I_w + breathing_room`。6 个 item、60° 角距时，最坏情况为 item 之间 `cos(30°) ≈ 0.866`。按中心标签宽度缩放 `RADIUS_X`——更重的 wordmark 需要更宽的环。
- **❗ 中心元素是标题** — 轨道是围绕它的装饰性动效。若轨道抢视线，增大中心元素或降低 orbit item 不透明度

## 关键约束

- **禁止 `requestAnimationFrame`** — 轨道必须在时间轴内运行，HF 才能逐帧确定性 seek
- **时间轴必须 paused**：`gsap.timeline({ paused: true })`
- **注册表键 = `data-composition-id`**
- **每个 item 独立 orbit tween** — 不要用 `targets: '.orbit-item'` 共享一个 tween，因为各 item 的 `initialAngle` 不同
- **`will-change: transform`** — 大量同时轨道 transform 受益于 compositor 提示
- **不要动画 `left`/`top`** — 使用 `translate()`（与 `translate(-50%, -50%)` 居中叠加）
- **❗ 进入必须在轨道位置原地翻转，而非在中心** — fromTo 的 from 与 to 都是 `x: 0, y: 0` 会让 item 在阶段 1 停在 stage 中心，翻转时与中心标签碰撞（阶段 2 开始再 snap 到轨道——可见 teleport）。

  正确模式（见上文 GSAP Timeline）是在添加 tween **之前**用 `gsap.set()` 将每个 item 置于 `(cos(initialAngle)*RADIUS_X, sin(initialAngle)*RADIUS_Y)` 且 `opacity: 0`，阶段 1 只动画 rotation/opacity/scale——**不要**动画 translate。item 在其轨道起点原地淡入，阶段 2 从该处平滑接上轨道。

## 组合

- [center-outward-expansion.md](center-outward-expansion.md) — 另一种进入模式（爆发而非轨道）；也是 orbit-collapse 结束的反向驱动
- [cursor-click-ripple.md](cursor-click-ripple.md) — 当中心元素是用户「点击」触发坍缩的 CTA 时自然搭配
- [sine-wave-loop.md](sine-wave-loop.md) — 在轨道上叠加每个 item 的 idle  wobble

## 搭配的 HF 技能

- `/hyperframes-animation` — 时间轴 + `onUpdate` API
- `/hyperframes-core` — composition 接线
- `/hyperframes-cli` — `hyperframes lint`
