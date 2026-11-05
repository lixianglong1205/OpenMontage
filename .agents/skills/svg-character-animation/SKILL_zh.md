---
name: svg-character-animation
description: 使用 GSAP、CSS 变换、Remotion 帧控制以及兼容 HyperFrames 的浏览器预览，为 SVG 角色绑定（rig）制作动画。
license: MIT
---

# SVG 角色动画

当你需要为由 SVG 部件组成的角色绑定制作动画时，使用本技能。

## 运行时规则

- 优先对变换属性（`x`、`y`、`scale`、`rotation`）做动画，而非布局。
- 多部件表演节拍请使用时间轴（timeline）。
- 对 SVG 元素使用稳定的枢轴点（`svgOrigin` 或作用域正确的 transform origin）。
- 在 Remotion 中，不要让 GSAP 通过 `requestAnimationFrame` 自行推进；应根据当前帧驱动已暂停的时间轴。

## 浏览器模式

```js
gsap.set("#arm_right", { svgOrigin: "390 310" });
const tl = gsap.timeline({ defaults: { ease: "power2.inOut" } });
tl.to("#head", { rotation: -8, duration: 0.2 })
  .to("#arm_right", { rotation: 35, duration: 0.4 }, "<");
```

## Remotion 模式

```tsx
const frame = useCurrentFrame();
const progress = frame / durationInFrames;
timeline.progress(progress);
```

## HyperFrames 模式

使用 HTML/SVG/GSAP 组件与确定性时间轴，在最终渲染前通过 HyperFrames CLI 进行校验。

## 质量检查清单

- 运动过程中各部件在枢轴点处保持连接。
- 眨眼、视线与口型足够独立，便于辨认。
- 姿势保持时长足以传达情绪。
- 帧采样应显示有意义的差异，而非静止不动的动画。

## 参考来源

- GSAP 核心变换属性与 SVG 处理：
  https://gsap.com/docs/v3/GSAP/CorePlugins/CSS/
- GSAP 时间轴与序列：
  https://gsap.com/docs/v3/GSAP/Timeline/
- Remotion `useCurrentFrame`：
  https://www.remotion.dev/docs/use-current-frame
