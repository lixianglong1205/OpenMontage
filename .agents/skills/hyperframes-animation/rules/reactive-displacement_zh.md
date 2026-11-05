---
name: reactive-displacement
description: 物理碰撞式转场：进入元素的弹簧驱动退出元素的位移——单一数据源使运动在因果上相互关联。
metadata:
  tags: transition, physics, collision, displacement, spring, causal
---

# 反应式位移（Reactive Displacement）

元素 A 的退出动画在数学上由元素 B 的进入弹簧推导得出。形成因果链：「A 移动是因为 B 撞到了它。」与 [scale-swap-transition](scale-swap-transition.md)（有重叠但非因果）和 [card-morph-anchor](card-morph-anchor.md)（单一容器变形尺寸）不同。

## 工作原理

单一 0→1 驱动补间（「进入弹簧」）驱动两条派生运动：

- **侵入者**（B，进入）：位置从舞台外插值到落位
- **被挤者**（A，退出）：位置从落位插值到舞台外，方向相反，但在驱动进度比例 `VICTIM_FRACTION` 处完成（而非 1.0）

被挤者比侵入者更早完成退出，形成「撞击后落定」的节奏。两条运动共享同一 eased 驱动，冲击时刻在数学上同步。

## HTML

```html
<div
  class="scene"
  id="collide-scene"
  data-composition-id="collide-scene"
  data-start="0"
  data-duration="3"
  data-track-index="0"
>
  <div class="stage">
    <div class="card victim" id="victim">
      <div class="card-title">{victimHeadline}</div>
      <div class="card-sub">{victimSubline}</div>
    </div>
    <div class="card intruder" id="intruder">
      <div class="card-title">{intruderHeadline}</div>
      <div class="card-sub">{intruderSubline}</div>
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
  background: radial-gradient(ellipse at center, {bgColor} 0%, {bgColorDeep} 70%);
  font-family: {font};
}
.stage {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
}
.card {
  position: absolute;
  /* both at center; transform translates them */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 24px;
  padding: 64px 80px;
  border-radius: 28px;
  will-change: transform, opacity;
}
.victim {
  background: linear-gradient(160deg, {victimTint} 0%, {bgColorDeep} 70%);
  border: 1px solid {victimTint};
  z-index: 1;
}
.intruder {
  background: linear-gradient(160deg, {intruderTint} 0%, {bgColorDeep} 70%);
  border: 2px solid {intruderBorder};
  box-shadow: 0 28px 96px {intruderTint};
  z-index: 2;
}
.card-title {
  font-size: 200px;
  font-weight: 900;
  color: {textColor};
  line-height: 1;
  letter-spacing: -4px;
}
.card-sub {
  font-size: 36px;
  font-weight: 800;
  letter-spacing: 10px;
  text-transform: uppercase;
  color: {accentColor};
  text-align: center;
}
```

## GSAP Timeline

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });

  // Off-stage distances are derived from the stage width.
  const INTRUDER_START_X = STAGE_W; // off-stage right
  const VICTIM_END_X = -STAGE_W; // off-stage left, opposite direction

  // Initial state — victim centered, intruder off-stage right
  gsap.set("#victim", { x: 0, opacity: 1, rotation: 0 });
  gsap.set("#intruder", { x: INTRUDER_START_X, opacity: 0, rotation: -INTRUDER_TILT });

  // Single driver — the entry spring — runs 0→1 over the impact arc
  const driver = { p: 0 };
  tl.to(
    driver,
    {
      p: 1,
      duration: DRIVER_DUR,
      ease: `back.out(${BOUNCE_FACTOR})`, // intruder spring
      onUpdate: () => {
        // Intruder: full 0→1 progress maps to enter (off-stage → center)
        const intruderX = INTRUDER_START_X * (1 - driver.p);
        const intruderOpacity = Math.min(1, driver.p * FADE_IN_SHARPNESS);
        const intruderRot = -INTRUDER_TILT * (1 - driver.p); // settle to 0°
        const intruder = document.getElementById("intruder");
        intruder.style.transform = `translate(-50%, -50%) translateX(${intruderX}px) rotate(${intruderRot}deg)`;
        intruder.style.opacity = String(intruderOpacity);

        // Victim: completes exit at VICTIM_FRACTION of driver (intruder still flying in)
        // so the impact MOMENT is the visual punch — by the time intruder centers,
        // victim is already off-stage.
        const victimP = Math.min(1, driver.p / VICTIM_FRACTION);
        const victimX = VICTIM_END_X * victimP;
        const victimOpacity = 1 - victimP;
        const victim = document.getElementById("victim");
        victim.style.transform = `translate(-50%, -50%) translateX(${victimX}px)`;
        victim.style.opacity = String(victimOpacity);
      },
    },
    DRIVER_AT,
  );

  // Climax dwell — intruder holds at center after settle (no additional motion;
  // composition continues with intruder centered for ≥ DWELL_MIN seconds).

  window.__timelines["collide-scene"] = tl;
</script>
```

## 如何选取参数

- **DRIVER_AT** — 进入弹簧开始的时间
  - 范围：依阶段而定（通常为数秒后）
  - 效果：过早会跳过铺垫节拍；过晚会让切镜显得拖沓
  - 约束：须在合成结束前留出 ≥ DWELL_MIN 的高潮停留
  - 参考：示例在上一阅读节拍结束后才调度位移

- **DRIVER_DUR** — 侵入者完整进入时长
  - 范围：0.6-1.4 s
  - 效果：短 = 利落、有冲击感；长 = 沉重、落地感强
  - 约束：与 `BOUNCE_FACTOR` 一起调——高 bounce 配长时长易显得发飘
  - 参考：见对应 blueprint / 示例

- **BOUNCE_FACTOR** — 侵入者弹簧上 `back.out()` 的系数
  - 范围：1.2-2.0（在 `back.out` 族内离散选取）
  - 效果：低 ≈ 稳固落定；高 ≈  overshoot/回弹
  - 约束：缓动族保持 `back.out`（或升级为 `elastic.out` 若需要振荡）；换族会改写整体手感
  - 参考：示例多在 1.4 至 1.6 之间

- **VICTIM_FRACTION** — 被挤者在 `DRIVER_DUR` 的多少比例内完成退出
  - 范围：0.4-0.5
  - 效果：< 0.4 被挤者在冲击可读前消失；> 0.5 运动显得并行而非因果
  - 约束：硬上限约 0.6；超过则碰撞隐喻失效
  - 参考：本规则模式约用 ~0.5

- **STAGE_W** — 舞台宽度（像素），用于把元素放在舞台外
  - 范围：等于合成的 `data-width`
  - 效果：更小会在起始时仍部分可见舞台外元素
  - 约束：须 ≥ 合成宽度
  - 参考：示例直接使用项目渲染宽度

- **INTRUDER_TILT** — 侵入者从初始旋转（度）落定到 0°
  - 范围：5-15°
  - 效果：低 = 干净滑入；高 = 明显的「旋入落定」
  - 约束：符号与进入方向一致（符合动量传递）
  - 参考：~10° 为典型中等冲击倾斜

- **FADE_IN_SHARPNESS** — 控制侵入者不透明度多快达到 1 的倍率
  - 范围：3-8（侵入者在进度 `1/FADE_IN_SHARPNESS` 处达到 opacity 1）
  - 效果：低 = 与运动同步柔和淡入；高 = 早期弹出、读作实体
  - 约束：> 1；低于 1 则到中心时仍半透明
  - 参考：多数示例用较早的锐利显现

- **DWELL_MIN** — 侵入者落定后高潮停留的最短时长
  - 范围：≥ 1.0 s
  - 效果：更短显得仓促难读；更长拖慢合成
  - 约束：冲击后的停留是新内容被阅读的时刻——不可省略
  - 参考：1.0-1.5 s 较常见

## 变体

### 被挤者的冲击旋转

被挤者不只滑出——还会因冲击角旋转：

```js
const victimRot = victimP * -VICTIM_KICK_DEG; // rotates as it slides
victim.style.transform = `translate(-50%, -50%) translateX(${victimX}px) rotate(${victimRot}deg)`;
```

`VICTIM_KICK_DEG` 通常为 15-25°；幅度与感知到的侵入者重量匹配。

### 垂直碰撞

侵入者自上方进入，被挤者向下位移。数学相同，轴改为 Y。视觉上像「重物砸落」。

### 落定后摆动

侵入者居中后，阻尼正弦摆动（`±WOBBLE_AMP_DEG` 旋转，在 `WOBBLE_DUR` 内衰减）再静止。在高潮停留前增加「冲击余波」。

```js
const wobble = { p: 0 };
tl.to(
  wobble,
  {
    p: Math.PI * WOBBLE_CYCLES * 2,
    duration: WOBBLE_DUR,
    ease: "none",
    onUpdate: () => {
      const rot =
        Math.sin(wobble.p) * WOBBLE_AMP_DEG * (1 - wobble.p / (Math.PI * WOBBLE_CYCLES * 2)); // linear decay
      intruder.style.transform = `translate(-50%, -50%) rotate(${rot}deg)`;
    },
  },
  DRIVER_AT + DRIVER_DUR,
);
```

### 多被挤者涟漪

侵入者挤开多张对齐卡片，每个被挤者退出略延迟（级联涟漪）。每个被挤者的 `victimP` 使用不同的驱动相位偏移。

## 核心原则

- **单一驱动 = 单一真相源** — 进入弹簧同时驱动两条运动。侵入者与被挤者各自独立补间会破坏因果链；它们只是时间上接近，而非真正碰撞。
- **被挤者在驱动的一小部分内完成** — 侵入者到中心时，被挤者已离开。「撞击」是二者重叠的瞬间；之后被挤者只是在腾出侵入者将占据的空间。
- **方向动量传递** — 侵入者自正 X 进入 → 被挤者向负 X 移动。同一轴。若不同轴，看起来像擦肩而过而非相撞。
- **侵入者 z-index 高于被挤者** — 重叠时侵入者应在前面（碰撞的「赢家」）。否则被挤者像在穿透。
- **侵入者带旋转进入、落定变平** — 强化动量可视化。小初始倾斜 → 落定 0° 读作「旋入后扎根」。
- **冲击后的高潮停留** — 冲击是 headline 节拍。冲击后的停留是新内容被阅读的时刻。

## 关键约束

- **时间轴须暂停**：`gsap.timeline({ paused: true })`
- **注册键 = `data-composition-id`**
- **单一驱动，同一 onUpdate 内多个派生值** — 不要用两个独立的 `tl.to()` 分别补间侵入者与被挤者；用一个 driver 在其 onUpdate 内同时计算两者
- **`.scene` 上 `overflow: hidden`** — 舞台外运动超出画框
- **两张卡片上 `will-change: transform, opacity`**
- **侵入者 z-index > 被挤者 z-index** — 显式设置，不单靠 DOM 顺序

## 组合

- [hacker-flip-3d.md](hacker-flip-3d.md) — 进入阶段侵入者文字经 hacker-flip 揭示
- [sine-wave-loop.md](sine-wave-loop.md) — 高潮停留期间侵入者 idle 呼吸
- [vertical-spring-ticker.md](vertical-spring-ticker.md) — 侵入者为 ticker，将上一内容「顶出」

## 搭配的 HF 技能

- `/hyperframes-animation` — 单一驱动、多值 onUpdate
- `/hyperframes-core` — 合成接线
- `/hyperframes-cli` — `hyperframes lint`
