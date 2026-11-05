---
name: depth-scatter-assemble
description: N 个元素从旋转的 3D 深度云中散开 / 再汇聚成整齐平面布局；每个元素的起始位置为由索引确定的 3D 偏移，并最终落位到干净的平面布局。
metadata:
  tags: 3d, scatter, assemble, depth, cloud, tumble, kinetic, letter, fragment, logo, reassemble
---

# 深度散开 ↔ 汇聚

N 个元素（字形、卡片、图标、Logo 碎片）从旋转的 3D 深度云中飞入并锁定到干净的屏幕布局——或反向播放。每个元素起始于**确定的** 3D 偏移（translateZ 深度 + rotateX/rotateY + 由索引推导的 x/y 散开），再缓动到汇聚后的平面位置（`z: 0, rotation: 0`）。由于每个散开位置都由元素索引上的三角函数计算——从不使用 `Math.random`——因此每一帧渲染结果完全一致。

与 `orbit-3d-entry`（翻转入场后持续轨道运动）和 `center-outward-expansion`（从同一中心点平面 2D 爆发）不同：此处每个元素在 3D 云中拥有**各自**的位置，最终结果是平面汇聚布局，而非轨道或径向喷散。

## 工作原理

每个元素最终落位到平面布局坐标（`targetX/Y`，在 CSS 或 `data-*` 中一次性设定）。其**散开**状态由索引 `i` 推导：

```js
const GOLDEN = Math.PI * (3 - Math.sqrt(5)); // ~2.39943 rad — even angular spread, no clumping
const a = i * GOLDEN; // this element's angle in the cloud
const scatterX = Math.cos(a) * RADIUS; // index-derived, deterministic
const scatterY = Math.sin(a) * RADIUS;
const scatterZ = Z_NEAR - (i / (n - 1)) * (Z_NEAR - Z_FAR); // stepped depth across the cloud
const rotX = Math.sin(a) * TUMBLE; // tumble orientation, also from the angle
const rotY = Math.cos(a) * TUMBLE;
```

单个 0→1 的 `progress` 代理在各通道之间对散开态与汇聚态做插值（lerp）。`progress = 0` 时元素构成深度云；`progress = 1` 时它们平铺在布局中。正向播放为**汇聚**；云本身缓慢旋转（舞台 `rotateY` 缓动），在锁定前让散开态更有动感。

舞台需要 `perspective`，舞台**以及**每个元素都需要 `transform-style: preserve-3d`，否则 z 深度与翻滚会被压成 2D 缩放。

## HTML

```html
<div
  class="scene"
  id="assemble-scene"
  data-composition-id="assemble-scene"
  data-start="0"
  data-duration="4"
  data-track-index="0"
>
  <!-- The cloud rotates; the layout lives inside it. targetX/Y = each
       element's FLAT assembled offset from stage center (px). -->
  <div class="cloud-stage">
    <div class="frag" data-target-x="-260" data-target-y="0">{glyph1}</div>
    <div class="frag" data-target-x="-130" data-target-y="0">{glyph2}</div>
    <div class="frag" data-target-x="0" data-target-y="0">{glyph3}</div>
    <div class="frag" data-target-x="130" data-target-y="0">{glyph4}</div>
    <div class="frag" data-target-x="260" data-target-y="0">{glyph5}</div>
  </div>
</div>
```

Logo 组合时，`targetX/Y` 描述各部分的静止布局；动态排版时，每个字形一个 `.frag`（在 setup 时从短语字符串注入 span，使宽度精确——见「变体」）。

## CSS

```css
.scene {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background: {bgColor};
  perspective: 1400px; /* REQUIRED — without it, z-depth + tumble read as flat 2D scale */
}
.cloud-stage {
  position: relative;
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  transform-style: preserve-3d; /* REQUIRED — preserves child 3D context */
  will-change: transform;
}
.frag {
  position: absolute;
  /* Live at stage center; GSAP translates each one to its layout / cloud point. */
  top: 50%;
  left: 50%;
  display: grid;
  place-items: center;
  font-family: {font};
  font-weight: 900;
  font-size: 120px;
  color: {textColor};
  transform-style: preserve-3d; /* each fragment keeps its own 3D context */
  backface-visibility: hidden; /* hides the mirrored face mid-tumble */
  will-change: transform, opacity;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  const frags = Array.from(document.querySelectorAll(".frag"));
  const n = frags.length;
  const GOLDEN = Math.PI * (3 - Math.sqrt(5)); // ~2.39943 — even spread, no clumps

  // RADIUS, Z_NEAR, Z_FAR, TUMBLE, ASSEMBLE_DUR, ASSEMBLE_EASE, STAGGER,
  // CLOUD_SPIN_DEG, CLOUD_SPIN_DUR — named constants per "How to Choose Values".

  // Precompute each fragment's deterministic scattered state from its index.
  const scatter = frags.map((el, i) => {
    const a = i * GOLDEN;
    const depthT = n > 1 ? i / (n - 1) : 0;
    return {
      x: Math.cos(a) * RADIUS,
      y: Math.sin(a) * RADIUS,
      z: Z_NEAR - depthT * (Z_NEAR - Z_FAR),
      rotationX: Math.sin(a) * TUMBLE,
      rotationY: Math.cos(a) * TUMBLE,
    };
  });

  // 1) Park every fragment in the cloud BEFORE any tween fires.
  frags.forEach((el, i) => {
    const s = scatter[i];
    gsap.set(el, {
      xPercent: -50,
      yPercent: -50, // bake self-centering so x/y are offsets from stage center
      x: s.x,
      y: s.y,
      z: s.z,
      rotationX: s.rotationX,
      rotationY: s.rotationY,
      opacity: 0,
    });
  });

  // 2) The cloud rotates so the scatter has life before / during assembly.
  tl.to(
    ".cloud-stage",
    { rotationY: CLOUD_SPIN_DEG, duration: CLOUD_SPIN_DUR, ease: "power1.out" },
    0,
  );

  // 3) ASSEMBLE — each fragment tweens from its cloud point to its flat target.
  frags.forEach((el, i) => {
    tl.to(
      el,
      {
        x: Number(el.dataset.targetX),
        y: Number(el.dataset.targetY),
        z: 0,
        rotationX: 0,
        rotationY: 0,
        opacity: 1,
        duration: ASSEMBLE_DUR,
        ease: ASSEMBLE_EASE, // out-ease — fragments fly in then settle
      },
      i * STAGGER, // index stagger reads as "cloud collapsing inward"
    );
  });

  window.__timelines["assemble-scene"] = tl;
</script>
```

## 变体

### 翻滚切换（镜头中段在两组短语间交接）

`kinetic-type-beats` 节拍切换的标志性用法：一组短语的字形**散入**云的同时，下一组短语的字形从云中**汇聚而出**——两种状态之间的 3D 交接，中间不会出现空帧。两组字形共享同一朵云；用同一个 0→1 的 `progress` 驱动两者，使交叉过程确定可复现。

```js
// outgoing[] and incoming[] are two glyph arrays, each with precomputed scatter[] (above).
const swap = { p: 0 };
tl.to(
  swap,
  {
    p: 1,
    duration: SWAP_DUR,
    ease: "power2.inOut",
    onUpdate: () => {
      const p = swap.p;
      outgoing.forEach((el, i) => {
        // 1 → 0: layout → cloud (scatters AWAY)
        const s = outScatter[i];
        const tx = Number(el.dataset.targetX);
        const ty = Number(el.dataset.targetY);
        el.style.opacity = String(1 - p);
        el.style.transform =
          `translate(-50%,-50%) translate3d(${tx + (s.x - tx) * p}px,${ty + (s.y - ty) * p}px,${s.z * p}px)` +
          ` rotateX(${s.rotationX * p}deg) rotateY(${s.rotationY * p}deg)`;
      });
      incoming.forEach((el, i) => {
        // 0 → 1: cloud → layout (assembles IN)
        const s = inScatter[i];
        const tx = Number(el.dataset.targetX);
        const ty = Number(el.dataset.targetY);
        el.style.opacity = String(p);
        el.style.transform =
          `translate(-50%,-50%) translate3d(${s.x + (tx - s.x) * p}px,${s.y + (ty - s.y) * p}px,${s.z * (1 - p)}px)` +
          ` rotateX(${s.rotationX * (1 - p)}deg) rotateY(${s.rotationY * (1 - p)}deg)`;
      });
    },
  },
  SWAP_AT,
);
```

在 setup 时为每个短语注入按字分的 span 集合（使每个字形的 `targetX` 等于精确排版后的前进宽度——在 `document.fonts.ready` 之后测量），并在各自时间窗之前将对应集合的 opacity 设为 0。

### 径向字母爆发 → 汇聚

平面特例（`kinetic-type-beats` 中「字母径向爆发再汇聚」的 GAP）：设 `Z_NEAR = Z_FAR = 0` 且 `TUMBLE` 较小，使云呈 2D 环，再反向播放汇聚以实现爆发——碎片甩向 `scatter[i]` 再弹回布局。纯平面内运动，无深度。

### 向外散开（仅最后一帧退场）

仅在整个合成的最后一拍反向播放汇聚（布局 → 云，opacity 1→0）。镜头中段向外散开会被读成退场并破坏镜头——入场与交接请用汇聚或翻滚切换。

### 视差深度滑入（Logo 组合）

用于 `logo-assemble-lockup` 时，给后层更大的 `|Z_FAR|` 和更长的 `ASSEMBLE_DUR`，前景部分较浅的深度和更短时长——不同深度的部分以不同表观速度滑入（视差）并锁定成组合。

## 如何选取参数

- **n (ELEMENT_COUNT)** — 云中的碎片 / 字形数量
  - 范围：4–14（字形组随词长；碎片/卡片保持 4–9）
  - 效果：少则像刻意组装；多则像密集虫群凝结
  - 约束：超过约 14 个时云会挤占中心，单条轨迹难以辨认

- **RADIUS** — 云在 x/y 平面上的 spread，px
  - 范围：250–700 px
  - 效果：小 = 紧结几乎不分；大 = 碎片从画面边缘飞入
  - 约束：在最远散开点仍须落在当前 `perspective` 下的画面内，否则碎片在屏外闪现、缺少飞行感

- **Z_NEAR / Z_FAR** — 云的深度带，px（前 / 后）
  - 范围：Z_NEAR +150 至 +450；Z_FAR −150 至 −500
  - 效果：带宽大（如 +400 / −400）纵深飞向/远离镜头感强；带宽窄则近乎平面
  - 约束：`perspective` 较短时 `|z|` 过大易过度透视（碎片先巨大再极小）——需加大 `perspective` 匹配

- **TUMBLE** — 散开碎片的 rotateX/rotateY 峰值，deg
  - 范围：40–110°
  - 效果：低 = 碎片近乎 upright 漂入；高 = 在空中翻滚并在到达时转正
  - 约束：配合 `backface-visibility: hidden`，字形超过 90° 时 tween 中段会露空白（翻滚预期）；单面内容的卡片建议 cap 在约 80°

- **ASSEMBLE_DUR** — 单碎片 云 → 布局 缓动时长，s
  - 范围：0.7–1.4 s
  - 效果：短 = 利落锁定；长 = 漂浮式凝结
  - 约束：`(n − 1) × STAGGER + ASSEMBLE_DUR` 须落在场景的汇聚时间窗内

- **ASSEMBLE_EASE** — 各碎片共用 ease
  - 离散选择：`power3.out`、`expo.out`、`back.out(1.4)`
  - 选取：`power3.out` 默认（飞入后落定）。`expo.out` 末端硬收。`back.out` 落位时略 overshoot。避免 `in` 类 ease——碎片会像被吸回云中。

- **STAGGER** — 相邻碎片开始汇聚的间隔，s
  - 范围：0.03–0.09 s
  - 效果：< 0.03 = 和弦式（整朵云同时塌缩）；> 0.09 = 慢滴失去「虫群」感
  - 约束：`n × STAGGER` 应小于 `ASSEMBLE_DUR`，使云作为一次运动塌缩，而非排队

- **CLOUD_SPIN_DEG / CLOUD_SPIN_DUR** — 汇聚过程中舞台 rotateY，deg / s
  - 范围：15–60°，时长 ≥ `ASSEMBLE_DUR`
  - 效果：轻旋让散开态有生命，不像冻结的爆炸图；过快会与汇聚抢戏
  - 约束：保持有限并在落定前结束——不要 `repeat`

- **SWAP_DUR / SWAP_AT**（翻滚切换）— 交接时长 / 触发时刻，s
  - 范围：SWAP_DUR 0.5–1.0 s；SWAP_AT 在节拍边界
  - 效果：短 = 硬切交叉；长 = 可见的穿云溶解
  - 约束： outgoing 与 incoming **必须**共享一个 `progress`（单次 tween），才能在同一瞬间交叉

## 核心原则

- **场景根上的 `perspective` + 舞台与每个 fragment 上的 `preserve-3d`** — 三者缺一，z 深度与翻滚会塌成平面缩放
- **每个散开值均由索引推导** — `cos/sin(i × GOLDEN)`、按 `i/(n−1)` 分档的 `z`。黄金角均匀散布、无簇，且（关键）**无 `Math.random`**，云在每次渲染中字节级一致
- **添加 tween 前用 `gsap.set` 摆好云** — 先将每个 fragment 停在散开点且 `opacity: 0`；汇聚 tween 从该处开始。跳过 set 会导致第 0 帧已是汇聚布局，首个 tween 开始时瞬移
- **平面落定** —  settled 状态为布局中的 `z: 0, rotationX: 0, rotationY: 0`。仍倾斜的云读作未完成
- **仅汇聚 / 交接；向外散开是退场** — 镜头中段碎片离云而去像镜头结束。入场用正向汇聚，节拍切换用翻滚切换；向外散开留给最后一帧
- **深度排序自动** — 在 `preserve-3d` 内绘制顺序随真实 Z，近处正确遮挡远处，无需手动 z-index（不同于轨道情形：轨道在 2D 中伪造，需要 cap z-index）

## 关键约束

- **禁止 `Math.random` / `Date.now`** — 每个散开坐标由索引推导（黄金角三角 + 分档深度）。本条规则的意义正在于此：随机云每帧不同，seek 会失效
- **禁止 CSS `transition`** — 所有运动均为暂停时间轴上的 GSAP tween
- **禁止 `repeat` / `yoyo` / infinite** — 云旋转与每次汇聚均为有限、单次 tween，在落定前结束
- **时间轴必须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **仅使用 transform 别名** — `x`、`y`、`z`、`scale`、`rotation`/`rotationX`/`rotationY`。不要用 `width`/`height`/`left`/`top`；`x`/`y` 与 `xPercent/yPercent -50` 自居中叠加
- **舞台 + fragment 上 `will-change: transform`** — 大量同时 3D transform 需要合成层提示
- **翻滚切换中两组字形共享一个 `progress`** — 两个独立 tween 在 seek 下可能相位漂移，交叉不再像一次交接

## 组合

- [orbit-3d-entry.md](orbit-3d-entry.md) — 另一种 3D 入场（落定后持续轨道而非平面锁定）；共享 `perspective` + `preserve-3d` 舞台设置
- [hacker-flip-3d.md](hacker-flip-3d.md) — 碎片落位时的按字 3D 翻转/解码；可叠加以获得「字翻滚飞入且到达时解码」
- [3d-text-depth-layers.md](3d-text-depth-layers.md) — 锁定后为组合字标叠加挤出层
- [center-outward-expansion.md](center-outward-expansion.md) — 平面 2D 近亲（单一共享中心、无深度），不需要 perspective 时用
- [press-release-spring.md](press-release-spring.md) — 云汇聚后在组合锁上加 spring 落定
- [sine-wave-loop.md](sine-wave-loop.md) — 汇聚后的布局做 idle 呼吸，而非静止 hold

## 与 HF skills 搭配

- `/hyperframes-animation` — 时间轴 + `onUpdate` API（共享 progress 的翻滚切换）
- `/hyperframes-core` — 合成 wiring
- `/hyperframes-cli` — `hyperframes lint`
