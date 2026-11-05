---
name: multi-phase-camera
description: 分 2–3 个阶段的顺序镜头缩放（拉远 / 聚焦 / 推进），叠加连续微漂移，营造有机的电影感。
metadata:
  tags: camera, zoom, phase, drift, scale, cinematic
---

# 多阶段镜头（Multi-Phase Camera）

包裹整段场景的镜头层，在脚本化触发点依次推进离散缩放阶段。叠加连续正弦驱动的微漂移，使阶段之间镜头不会显得静止。与单次线性缩放不同，多阶段营造「电影节奏」（ anticipation → reveal → settle，即铺垫 → 揭示 → 落定）。

## 工作原理

镜头是单个包裹用 `<div>`，其 `transform: scale() translate(x, y)` 由以下两部分驱动：

1. **阶段缩放（Phase scale）** — 在触发时刻阶梯式推进的 scale 值（例如 t=0 为 `PHASE_1_SCALE` → `PHASE_2_AT` 时为 `PHASE_2_SCALE` → `PHASE_3_AT` 时为 `PHASE_3_SCALE`）
2. **漂移偏移（Drift offset）** — 基于正弦的连续 `translateX` / `translateY`（小幅振幅、低频），叠加在阶段变换之上

二者均在 GSAP 时间轴内运行，以便 HF（HyperFrames）逐帧确定性 seek。

## HTML

```html
<div
  class="scene"
  data-composition-id="cam-scene"
  data-start="0"
  data-duration="6"
  data-track-index="0"
>
  <div class="camera" id="camera">
    <div class="content">
      <div class="hero">{Brand}</div>
      <div class="tagline">{tagline}</div>
      <div class="cta">{ctaText}</div>
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
  background: {sceneBgColor};
}
.camera {
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
  gap: 32px;
  text-align: center;
}
.hero {
  font-family: {font};
  font-weight: 900;
  font-size: {heroSize};
  letter-spacing: 8px;
  color: {textColor};
  text-transform: uppercase;
}
.tagline {
  font-family: {font};
  font-weight: 600;
  font-size: {taglineSize};
  color: {accentColor};
}
.cta {
  font-family: {monoFont};
  font-weight: 700;
  font-size: {ctaSize};
  letter-spacing: 6px;
  color: {accentColor};
  text-transform: uppercase;
}
```

## GSAP 时间轴

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const camera = document.getElementById("camera");

  // Three-phase scale plan: pullback → focus → push
  const phase = { scale: PHASE_1_SCALE };

  // Phase 1 — start pulled back
  // (no tween needed for the initial value; set via the phase object)

  // Phase 2 — settle to neutral focus
  tl.to(
    phase,
    {
      scale: PHASE_2_SCALE,
      duration: PHASE_2_DUR,
      ease: PHASE_2_EASE,
    },
    PHASE_2_AT,
  );

  // Phase 3 — slow push-in for the climax
  tl.to(
    phase,
    {
      scale: PHASE_3_SCALE,
      duration: PHASE_3_DUR,
      ease: PHASE_3_EASE,
    },
    PHASE_3_AT,
  );

  // Drift driver — continuous sine motion overlaid on the phase scale
  const drift = { p: 0 };

  tl.to(
    drift,
    {
      p: Math.PI * 2 * DRIFT_CYCLES,
      duration: TOTAL_DURATION,
      ease: "none",
      onUpdate: () => {
        const dx = Math.sin(drift.p) * DRIFT_AMP_X;
        const dy = Math.sin(drift.p * DRIFT_FREQ_RATIO) * DRIFT_AMP_Y;
        camera.style.transform = `scale(${phase.scale}) translate(${dx}px, ${dy}px)`;
      },
    },
    0,
  );

  // Content reveals (entry beats inside the camera frame)
  tl.from(".hero", { opacity: 0, y: 32, scale: 0.96, duration: 0.9, ease: "power3.out" }, HERO_AT);
  tl.from(".tagline", { opacity: 0, y: 16, duration: 0.7, ease: "power3.out" }, TAGLINE_AT);
  tl.from(".cta", { opacity: 0, y: 8, duration: 0.7, ease: "power3.out" }, CTA_AT);

  window.__timelines["cam-scene"] = tl;
</script>
```

## 如何选取参数

- **PHASE_1_SCALE / PHASE_2_SCALE / PHASE_3_SCALE** — 三步缩放值
  - 范围：PHASE_1 0.88–0.96；PHASE_2 0.98–1.02；PHASE_3 1.04–1.15
  - 效果：区间越窄镜头越 subtle；越宽越 cinematic
  - 约束：当 PHASE_1_SCALE < 1 时，`.scene` 必须设置 `overflow: hidden`，否则内层内容边缘会露出画框

- **PHASE_2_AT / PHASE_2_DUR** — 聚焦阶段何时开始、持续多久
  - 范围：PHASE_2_AT 0.3–1.0 s；PHASE_2_DUR 1.0–1.8 s
  - 效果：DUR 越长，落定越慢，电影感越强

- **PHASE_3_AT / PHASE_3_DUR** — 推进阶段何时开始、持续多久
  - 范围：PHASE_3_AT 2.0–4.0 s；PHASE_3_DUR 1.0–2.0 s
  - 约束：PHASE_3_AT 须 ≥ PHASE_2_AT + PHASE_2_DUR（否则会打断聚焦）

- **PHASE_2_EASE / PHASE_3_EASE** — 各段过渡缓动
  - 离散选择：`power2.out`、`power3.out`、`power2.inOut`
  - 选用：偏 cinematic；镜头用 spring/back 类缓动会不舒适。后一阶段应比前一阶段更「落定」（更长 duration 或更偏 out 的 easing）。

- **TOTAL_DURATION** — 合成总时长（与 `data-duration` 一致）
  - 参考：漂移 tween 须覆盖整段合成

- **DRIFT_CYCLES** — 在 TOTAL_DURATION 内的正弦周期数
  - 范围：1–3
  - 效果：1 = 一次慢呼吸；3 = 明显更忙
  - 约束：过高会像机械晃动而非有机漂移

- **DRIFT_AMP_X / DRIFT_AMP_Y** — 漂移峰值偏移（像素）
  - 范围：DRIFT_AMP_X 2–8 px；DRIFT_AMP_Y 1–4 px
  - 效果：单帧几乎不可见，随时间可感知。若像离散抖动，则幅度过大。

- **DRIFT_FREQ_RATIO** — Y 轴正弦频率相对 X 的倍数
  - 范围：1.2–1.5
  - 效果：1.0 = 完美对角（显机械）；约 1.3 = 有机 Lissajous 轨迹

- **HERO_AT / TAGLINE_AT / CTA_AT** — 内容揭示节拍
  - 约束：HERO_AT 宜在 PHASE_1 经 PHASE_2 落定之后（否则主标题淡入时镜头仍在拉远，会像标题在飞走）

## 阶段模式

| 模式 | 缩放序列（阶段 1 → 2 → 3） | 感受 | 适用场景 |
| ------------------- | --------------------------------- | ------------------------------- | ----------------------------- |
| **Focus-in** | 后 → 中性 → 略推 | 靠近 → 落定 → 轻推 | 默认产品揭示 |
| **Dramatic reveal** | 推 → 中性 → 拉 | 广 → 聚焦 → 回弹落定 | 主视觉留呼吸空间 |
| **Steady push** | 中性 → 略推 → 再推 | 持续向前动量 | 连续叙事推进 |
| **Bookend pull** | 中性 → 强推 → 中性 | 落定 → 推进 → 释放 | 强调 CTA 后释放 |

## 变体

### 按内容节拍触发阶段（非固定时间）

若合成有内容阶段（例如入场结束后再开始 orbit），将镜头 tween 的起始时间与内容 tween 的结束时间对齐，而非固定时钟。

### 镜头抖动（panic / impact）

若需短暂抖动而非漂移，用更高振幅、更高频率的 tween 覆盖短窗口，替代漂移 tween：

```js
tl.to(
  drift,
  {
    p: Math.PI * 2 * SHAKE_CYCLES,
    duration: SHAKE_DUR,
    ease: "none",
    onUpdate: () => {
      const dx = Math.sin(drift.p) * SHAKE_AMP_X;
      const dy = Math.sin(drift.p * SHAKE_FREQ_RATIO) * SHAKE_AMP_Y;
      camera.style.transform = `scale(${phase.scale}) translate(${dx}px, ${dy}px)`;
    },
  },
  SHAKE_AT,
);
```

### 对准非居中元素的缩放

若高潮须缩向非居中元素，将 scale 与反向平移组合。计算偏移，使目标在 scale 后落在视口中心：

```js
const target = document.querySelector(".cta");
const tRect = target.getBoundingClientRect();
const viewportCenter = { x: STAGE_W / 2, y: STAGE_H / 2 };
const offsetX = (viewportCenter.x - (tRect.left + tRect.width / 2)) / phase.scale;
const offsetY = (viewportCenter.y - (tRect.top + tRect.height / 2)) / phase.scale;
// then in onUpdate: translate(offsetX + dx, offsetY + dy)
```

## 核心原则

- **漂移单帧不可见、随时间可见** — 若像离散抖动，则振幅过大
- **X、Y 漂移频率略不同** — `DRIFT_FREQ_RATIO ≈ 1.3` 避免完美对角运动（显机械）
- **阶段缓动比 UI spring 更柔** — cinematic 用 `power2.inOut` 或 `power3.out`；镜头不宜 spring/back
- **后一阶段「落定更深」** — 阶段 2 的 ease 应比阶段 1 更落定（更长 duration 或更 out 的 easing）。唤醒 → 落定 → 再深一层落定
- **镜头包裹场景内一切** — 逐元素加镜头会产生视差 bug，破坏「单一视点」
- **❗ `.scene` 上 `overflow: hidden`** — 拉远阶段（`scale < 1`）会露出内层边缘。无 `overflow: hidden` 时边缘会漏出舞台，HF 会将其渲染为可见内容
- **❗ 主标题揭示须在初始拉远 ease 落定之后** — 镜头仍在拉远时标题淡入，会像标题在飞走

## 关键约束

- **时间轴必须 paused**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **`.camera` 上不要用 CSS `transition`** — 会与 GSAP transform 冲突
- **镜头上 `transform-origin: 50% 50%`** — 非中心原点会使阶段间漂移不可预测
- **`.camera` 上 `will-change: transform`** — 镜头 transform 每帧更新
- **`.scene` 上 `overflow: hidden`** — 任阶段 scale < 1 时必需
- **场景背景放在 `.scene` 而非 `.camera`** — 背景若在 camera 上，缩放/平移会露出外侧空白

## 组合

- [orbit-3d-entry.md](orbit-3d-entry.md) — 缓慢漂移镜头内的 orbit 运动
- [counting-dynamic-scale.md](counting-dynamic-scale.md) — 高潮推进与计数峰值同步
- [3d-text-depth-layers.md](3d-text-depth-layers.md) — 景深分层主视觉 + cinematic 镜头
- [sine-wave-loop.md](sine-wave-loop.md) — 镜头内的元素 idle（复合运动）

## 与 HF 技能搭配

- `/hyperframes-animation` — 多阶段 tween + drift onUpdate
- `/hyperframes-core` — 合成接线、scene 包裹
- `/hyperframes-cli` — `hyperframes lint`
