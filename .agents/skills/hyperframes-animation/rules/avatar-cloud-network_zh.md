---
name: avatar-cloud-network
description: 头像沿椭圆环分布，经 SVG 虚线连接至中心 hub —— 分步入场的「社区」式社交证明（social proof）揭示。
metadata:
  tags: avatar, cloud, network, social-proof, ellipse, connection, stagger
---

# 头像云网络（Avatar Cloud Network）

头像围绕中心元素（logo / 计数器 / 品牌）排列在椭圆环上。从中心到每个头像绘制 SVG 虚线连接。头像以交错弹簧动画入场，随后连接线向外绘制 —— 传达「社区」或「社交证明」感。与 [orbit-3d-entry](orbit-3d-entry.md)（持续轨道运动）不同 —— avatar-cloud 是静态构图揭示。

## 工作原理

三层渲染：

1. **SVG 连接线**（z-index 1，位于最底层）— 从中心 hub 到各头像位置的线段
2. **头像**（z-index 2）— 位于椭圆位置上的 `<div>` 圆形
3. **中心 hub**（z-index 5）— 品牌计数器或 logo（位于汇聚于其上的连线之上）

动画阶段：

- `HUB_FADE_START → HUB_FADE_START + HUB_FADE_DUR`：hub 淡入
- `AVATAR_ENTRY_START → AVATAR_ENTRY_START + (AVATAR_COUNT − 1) × AVATAR_STAGGER + AVATAR_ENTRY_DUR`：头像依次级联入场
- `LINES_START → LINES_START + (AVATAR_COUNT − 1) × LINE_STAGGER + LINES_DUR`：连接线向外绘制
- 高潮停留：头像可选 idle 呼吸（见变体 / sine-wave-loop）

## HTML

```html
<div
  class="scene"
  id="cloud-scene"
  data-composition-id="cloud-scene"
  data-start="0"
  data-duration="4"
  data-track-index="0"
>
  <!-- Connection lines layer -->
  <svg class="lines" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
    <!-- Lines injected by script — center to each avatar -->
  </svg>

  <!-- Avatars + center hub -->
  <div class="hub-wrap">
    <div class="hub" id="hub">
      <div class="hub-num" id="hub-num">{counterValue}</div>
      <div class="hub-label">{counterLabel}</div>
    </div>
    <!-- Avatars injected by script — AVATAR_COUNT around the ellipse -->
  </div>

  <div class="brand">{footerLine}</div>
</div>
```

占位符 token：

- `{counterValue}` / `{counterLabel}` — hub 文案（数字证明 + 类别）
- `{footerLine}` — 云图下方可选署名行
- `{avatar[i]}` — 各头像图片源（若使用下方 emoji 变体则为 emoji 字形）

## CSS

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  background: {bgColor};
  font-family: {font};
  overflow: hidden;
}
.lines {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}
.hub-wrap {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
}
.hub {
  position: relative;
  z-index: 5;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 48px 64px;
  border-radius: 28px;
  background: {hubBg};
  border: 1px solid {hubBorder};
}
.hub-num {
  font-size: HUB_NUM_FONT_SIZE;
  font-weight: 900;
  color: {textColor};
  letter-spacing: -4px;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}
.hub-label {
  font-size: HUB_LABEL_FONT_SIZE;
  font-weight: 800;
  letter-spacing: 12px;
  color: {accentColor};
  text-transform: uppercase;
}
.avatar {
  position: absolute;
  z-index: 2;
  width: AVATAR_SIZE;
  height: AVATAR_SIZE;
  border-radius: 50%;
  border: 3px solid {avatarBorder};
  box-shadow:
    0 12px 32px rgba(0, 0, 0, 0.5),
    0 0 24px {avatarGlow};
  display: grid;
  place-items: center;
  font-size: AVATAR_GLYPH_SIZE;
  background: {avatarBg};
  will-change: transform, opacity;
  /* Top-left positioned by script; transform centers via -50% trick */
  transform: translate(-50%, -50%);
}
.brand {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  font-size: BRAND_FONT_SIZE;
  font-weight: 900;
  letter-spacing: 14px;
  color: {accentColor};
  text-transform: uppercase;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // CENTER_X / CENTER_Y must match the hub's rendered center exactly.
  // For a hub-wrap with place-items:center on a 1920×1080 canvas these are
  // (compositionWidth/2, compositionHeight × CENTER_Y_FACTOR).
  const SCREEN_CENTER = { x: CENTER_X, y: CENTER_Y };

  const hubWrap = document.querySelector(".hub-wrap");
  const linesSvg = document.querySelector(".lines");

  // Build avatars + lines
  const avatarPositions = [];
  for (let i = 0; i < AVATAR_COUNT; i++) {
    const angle = (i / AVATAR_COUNT) * Math.PI * 2 - Math.PI / 2; // start at top
    const x = SCREEN_CENTER.x + Math.cos(angle) * RADIUS_X;
    const y = SCREEN_CENTER.y + Math.sin(angle) * RADIUS_Y;
    avatarPositions.push({ x, y, angle });

    // Avatar
    const av = document.createElement("div");
    av.className = "avatar";
    av.style.left = `${x}px`;
    av.style.top = `${y}px`;
    // assign avatar image / glyph from your authoring data (see {avatar[i]})
    hubWrap.appendChild(av);

    // Line from hub to avatar
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", SCREEN_CENTER.x);
    line.setAttribute("y1", SCREEN_CENTER.y);
    line.setAttribute("x2", x);
    line.setAttribute("y2", y);
    line.setAttribute("stroke", "{lineColor}");
    line.setAttribute("stroke-width", "2");
    line.setAttribute("stroke-dasharray", "6 8");
    const len = Math.hypot(x - SCREEN_CENTER.x, y - SCREEN_CENTER.y);
    line.style.strokeDashoffset = String(len);
    line.dataset.length = String(len);
    line.dataset.index = String(i);
    linesSvg.appendChild(line);
  }

  // Phase 1 — hub fade in
  tl.from(
    ".hub",
    { opacity: 0, scale: 0.8, duration: HUB_FADE_DUR, ease: `back.out(${HUB_BOUNCE})` },
    HUB_FADE_START,
  );

  // Phase 2 — avatars cascade-in (staggered spring)
  const avatars = document.querySelectorAll(".avatar");
  avatars.forEach((av, i) => {
    tl.from(
      av,
      {
        opacity: 0,
        scale: 0,
        duration: AVATAR_ENTRY_DUR,
        ease: `back.out(${AVATAR_BOUNCE})`,
      },
      AVATAR_ENTRY_START + i * AVATAR_STAGGER,
    );
  });

  // Phase 3 — connection lines draw outward (staggered) — starts after most avatars land
  const lines = linesSvg.querySelectorAll("line");
  lines.forEach((line, i) => {
    tl.to(
      line,
      {
        strokeDashoffset: 0,
        duration: LINES_DUR,
        ease: "power2.out",
      },
      LINES_START + i * LINE_STAGGER,
    );
  });

  // Phase 4 — climax dwell (network fully formed), idle breathing on avatars
  // (see sine-wave-loop.md for the multiplicative onUpdate form)
  const breathDriver = { p: 0 };
  tl.to(
    breathDriver,
    {
      p: Math.PI * 2 * BREATH_CYCLES,
      duration: BREATH_DUR,
      ease: "none",
      onUpdate: () => {
        avatars.forEach((av, i) => {
          const phase = breathDriver.p + (i / avatars.length) * Math.PI * 2;
          const s = 1 + Math.sin(phase) * BREATH_AMP;
          av.style.transform = `translate(-50%, -50%) scale(${s})`;
        });
      },
    },
    BREATH_START,
  );

  window.__timelines["cloud-scene"] = tl;
</script>
```

## 如何选取参数

### 几何

- **CENTER_X / CENTER_Y** — hub 中心的 px 坐标；连线与头像位置由此推导。
  - 约束：**必须等于 hub 实际渲染中心** — 当本规则与其他场景组合（例如已重新居中的 logo）时，`CENTER_X / CENTER_Y` 须与 hub 最终位置来自同一数据源
  - 参考：../../examples/proof-logo-chain.html 使用 `(W/2, H × 0.47)`，使云图略位于画布中线之上
- **RADIUS_X / RADIUS_Y** — 椭圆半径（px）（RADIUS_X ≥ RADIUS_Y 更有透视感）。
  - 范围：`RADIUS_X` 约为视口宽度的 20–30%；`RADIUS_Y` 约为视口高度的 18–25%
  - 约束：`RADIUS_X / RADIUS_Y` 在 1.5 至 3.0 之间较自然；比值为 1（正圆）则像平面 2D 布局
  - 参考：../../examples/proof-logo-chain.html 使用 `W * 0.25`（`480px`）与 `H * 0.22`（`237.6px`）
- **AVATAR_COUNT** — 环上分布的头像数量。
  - 范围：8–12；更少显稀疏，更多则椭圆拥挤
  - 参考：../../examples/proof-logo-chain.html 使用 `10`
- **AVATAR_SIZE / AVATAR_GLYPH_SIZE** — 各头像圆直径及（可选）内部字形尺寸的 px 值。
  - 范围：1920 宽下 `AVATAR_SIZE` 约 80–120 px；需足够小以便 10+ 头像在环上不重叠
- **HUB_NUM_FONT_SIZE / HUB_LABEL_FONT_SIZE / BRAND_FONT_SIZE** — hub 排版字号。
  - 约束：hub-num 为视觉焦点，字号约为 label 的 2–4 倍

### Hub 淡入

- **HUB_FADE_START** — hub 开始淡入的时刻。
  - 范围：通常为 `0`（hub 先确立焦点）；若场景前另有节拍可偏移
- **HUB_FADE_DUR** — hub 淡入时长。
  - 范围：0.4–0.6s
- **HUB_BOUNCE** — hub 缩放入场的 `back.out(HUB_BOUNCE)` 系数。
  - 范围：1.4（轻微）→ 1.8（有力）

### 头像级联

- **AVATAR_ENTRY_START** — 第一个头像弹入的时刻。
  - 约束：`≥ HUB_FADE_START + HUB_FADE_DUR × 0.6`，以便 hub 先确立再出现卫星头像
- **AVATAR_ENTRY_DUR** — 单个头像放大时长。
  - 范围：0.4–0.7s
- **AVATAR_STAGGER** — 相邻头像入场间隔。
  - 范围：0.06–0.10s；级联像「陆续加入」；同时出现则像「本来就在」
- **AVATAR_BOUNCE** — 各头像弹入的 `back.out(AVATAR_BOUNCE)` 系数。
  - 范围：1.4（柔和）→ 1.8（有力）；略强于 hub 以作区分

### 连接线

- **LINES_START** — 连线开始向外绘制的时刻。
  - 约束：`LINES_START + (AVATAR_COUNT − 1) × LINE_STAGGER` 应与最后一个头像落定重叠约 0.1–0.2s，使绘制像头像落地的结果
- **LINES_DUR** — 单条连线绘制时长（strokeDashoffset → 0）。
  - 范围：0.4–0.7s
- **LINE_STAGGER** — 相邻连线开始绘制的间隔。
  - 范围：0.02–0.05s；紧凑交错像向外扩散的波

### Idle 呼吸

- **BREATH_START** — idle 呼吸开始的时刻。
  - 约束：`≥ LINES_START + (AVATAR_COUNT − 1) × LINE_STAGGER + LINES_DUR + ~0.2s`（让连线先落定）
- **BREATH_DUR** — 呼吸 tween 总时长。
  - 范围：填满剩余 composition 时间窗
- **BREATH_CYCLES** — 在 `BREATH_DUR` 内的完整正弦周期数。
  - 范围：1.0–2.0；低于 1 像一次 sigh，高于 2 开始显得焦虑
- **BREATH_AMP** — 缩放上正弦幅度（乘法形式）。
  - 范围：0.02–0.06；真人头像偏小，风格化字形可偏大

### 颜色 token

- **{bgColor}** — 舞台背景（常为深色渐变，使云图像星座）
- **{textColor}** — hub-num 颜色（主文案）
- **{accentColor}** — hub-label + 页脚（品牌语气）
- **{hubBg} / {hubBorder}** — hub 卡片表面；渐变 + 1px 边框显浮起感
- **{avatarBg} / {avatarBorder} / {avatarGlow}** — 头像圆样式；柔和边框 + 光晕在深色背景上更易读
- **{lineColor}** — SVG 描边色（半透明 accent 更有网络感）
- **{font}** — 基础字体栈

## 变体

### 头像尺寸变化（有机感）

按索引变化头像尺寸 — 例如用小数组存各档尺寸 — 避免环上过于机械重复。

### 实线替代虚线

去掉 `stroke-dasharray`，使用实线描边。去掉 dash 绘制动画；连线改为 opacity 淡入。更偏企业风，网络感更弱。

### 多轨道（同心环）

两层头像：较小内环（更少头像、略大尺寸）、较大外环（更多、更小）。连线仅连接内环与 hub；外环为「光晕」。

### 国家 / 角色字形（地理或 persona 分布）

用人脸图换为国旗 / emoji / 图标。传达「全球社区」或「多元角色」。

## 关键原则

- **Hub 在连线上方（`z-index: 5` vs 连线 `z-index: 1`）** — 连线应止于 hub 边缘，而非穿过。hub 必须在最前。
- **连线向外绘制（dash offset 0）** — 从中心向外画是视觉叙事：「hub 连接其社区」。
- **8–12 个头像** — 更少显稀疏，更多则椭圆拥挤。
- **`RADIUS_X > RADIUS_Y`** — 横向椭圆有透视；相等半径（圆）像平面 2D。
- **头像入场 stagger 0.06–0.10s** — 级联像「加入」；同时像「本来就在」。
- **头像大致落定后再 stagger 连线** — 绘制约在最后一个头像落定前 0.1–0.2s 开始以重叠。
- **成形后 idle 呼吸** — 各头像略错相位。高潮停留时留住视线。
- **❗ 高潮停留 ≥1s** — 连线完成后至少保持 ≥1s，便于读清已成形的网络。

## 关键约束

- **时间线必须 paused**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **头像与连线不用 CSS animation**
- **头像上 `will-change: transform, opacity`**
- **SVG `pointer-events: none`** — 装饰性叠加层
- **直线不必 `getTotalLength()`** — 用 `Math.hypot` 求线长（更省、更准）
- **Hub `z-index` > 连线 z-index** — 明确分层

## 组合

- [counting-dynamic-scale.md](counting-dynamic-scale.md) — hub 即为递增计数器
- [sine-wave-loop.md](sine-wave-loop.md) — 头像 idle 呼吸模式
- [3d-text-depth-layers.md](3d-text-depth-layers.md) — 带深度层的 hub label

## 搭配的 HF skills

- `/hyperframes-animation` — 交错弹簧入场 + SVG dash 绘制
- `/hyperframes-core` — composition 接线
- `/hyperframes-cli` — `hyperframes lint`
