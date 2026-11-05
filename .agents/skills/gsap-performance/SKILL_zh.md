---
name: gsap-performance
description: 官方 GSAP 性能技能 — 优先使用 transform、避免布局抖动、will-change、批处理。在优化 GSAP 动画、减少卡顿，或用户询问动画性能、FPS、流畅 60fps 时使用。
license: MIT
---

# GSAP 性能

## 何时使用本技能

在优化 GSAP 动画以实现流畅 60fps、降低布局/绘制成本，或用户询问性能、卡顿或快速动画最佳实践时使用。

**相关技能：** 使用 **gsap-core**（transform、autoAlpha）和 **gsap-timeline** 构建动画；ScrollTrigger 性能请参阅 **gsap-scrolltrigger**。

## 优先使用 Transform 和 Opacity

对 **transform**（`x`、`y`、`scaleX`、`scaleY`、`rotation`、`rotationX`、`rotationY`、`skewX`、`skewY`）和 **opacity** 做动画时，工作留在合成器上，可避免布局及大部分绘制。若 transform 能达到相同效果，应避免对易触发布局的属性做动画。

- ✅ 优先：**x**、**y**、**scale**、**rotation**、**opacity**。
- ❌ 尽量避开：**width**、**height**、**top**、**left**、**margin**、**padding**（会触发布局并可能导致卡顿）。

GSAP 的 **x** 和 **y** 默认使用 transform（translate）；移动时请用它们，而非 **left**/**top**。

## will-change

对将要动画的元素在 CSS 中使用 **will-change**，提示浏览器提升图层。

```css
will-change: transform;
```

## 批量读取与写入

GSAP 会在内部批量更新。当 GSAP 与直接 DOM 读写或依赖布局的代码混用时，避免交错读写导致反复布局抖动。优先先完成所有读取再写入（或让 GSAP 一次性处理写入）。

## 大量元素（Stagger、列表）

- 动画相同时，用 **stagger** 代替多个带手动延迟的独立 tween，更高效。
- 长列表可考虑**虚拟化**或仅动画可见项；避免同时创建数百个 tween 导致卡顿。
- 尽量复用时间轴；避免每帧创建新时间轴。

## 频繁更新的属性（如鼠标跟随）

对经常更新的属性（如鼠标跟随的 x/y），优先使用 **gsap.quickTo()**。它在每次更新时复用单个 tween，而不是新建 tween。

```javascript
let xTo = gsap.quickTo("#id", "x", { duration: 0.4, ease: "power3" }),
    yTo = gsap.quickTo("#id", "y", { duration: 0.4, ease: "power3" });

document.querySelector("#container").addEventListener("mousemove", (e) => {
  xTo(e.pageX);
  yTo(e.pageY);
});
```

## ScrollTrigger 与性能

- **pin: true** 会提升被固定元素；仅固定必要部分。
- **scrub** 使用较小值（如 `scrub: 1`）可在滚动时减少计算；在低端设备上测试。
- 仅在布局实际变化时（如内容加载后）调用 **ScrollTrigger.refresh()**，不要每次 resize 都调用；尽可能防抖。

## 减少同时运行的工作

- 不可见时暂停或 kill 屏外或非活动动画（如用户离开页面时）。
- 避免同时对大量元素的众多属性做动画；必要时简化或分序执行。

## 最佳实践

- ✅ 动画 **transform** 和 **opacity**；仅对会动画的元素在 CSS 中使用 **will-change**。
- ✅ 动画相同时，用 **stagger** 代替多个带手动延迟的独立 tween。
- ✅ 对频繁更新的属性（如鼠标跟随）使用 **gsap.quickTo()**。
- ✅ 清理或 kill 屏外动画；布局变化时调用 **ScrollTrigger.refresh()**，并尽可能防抖。

## 请勿

- ❌ 能用 **x**/**y**/**scale** 达到相同视觉效果时，不要用 **width**/**height**/**top**/**left** 做移动动画。
- ❌ 不要「以防万一」给每个元素设置 **will-change** 或 **force3D**；只用于实际会动画的元素。
- ❌ 不要未经低端设备测试就创建数百个重叠 tween 或 ScrollTrigger。
- ❌ 不要忽略清理；游离的 tween 和 ScrollTrigger 会持续运行，损害性能与正确性。
