---
name: timing
description: Remotion 中的插值曲线——线性、缓动与弹簧动画
metadata:
  tags: spring, bounce, easing, interpolation
---

使用 `interpolate` 函数可完成简单的线性插值。

```ts title="Going from 0 to 1 over 100 frames"
import { interpolate } from "remotion";

const opacity = interpolate(frame, [0, 100], [0, 1]);
```

默认情况下，数值不会被钳制（clamp），因此结果可能超出 [0, 1] 范围。  
可按如下方式钳制：

```ts title="Going from 0 to 1 over 100 frames with extrapolation"
const opacity = interpolate(frame, [0, 100], [0, 1], {
  extrapolateRight: "clamp",
  extrapolateLeft: "clamp",
});
```

## 弹簧动画

弹簧动画的运动更自然。  
它们会随时间从 0 过渡到 1。

```ts title="Spring animation from 0 to 1 over 100 frames"
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const scale = spring({
  frame,
  fps,
});
```

### 物理属性

默认配置为：`mass: 1, damping: 10, stiffness: 100`。  
这会使动画在稳定前带有一点回弹。

可按如下方式覆盖配置：

```ts
const scale = spring({
  frame,
  fps,
  config: { damping: 200 },
});
```

若希望运动自然且不回弹，推荐使用：`{ damping: 200 }`。

以下是一些常见配置：

```tsx
const smooth = { damping: 200 }; // Smooth, no bounce (subtle reveals)
const snappy = { damping: 20, stiffness: 200 }; // Snappy, minimal bounce (UI elements)
const bouncy = { damping: 8 }; // Bouncy entrance (playful animations)
const heavy = { damping: 15, stiffness: 80, mass: 2 }; // Heavy, slow, small bounce
```

### 延迟

默认情况下动画会立即开始。  
使用 `delay` 参数可将动画延迟若干帧。

```tsx
const entrance = spring({
  frame: frame - ENTRANCE_DELAY,
  fps,
  delay: 20,
});
```

### 时长

`spring()` 的时长由物理属性自然决定。  
若要将动画拉伸到指定时长，请使用 `durationInFrames` 参数。

```tsx
const spring = spring({
  frame,
  fps,
  durationInFrames: 40,
});
```

### 将 spring() 与 interpolate() 结合

将弹簧输出（0–1）映射到自定义范围：

```tsx
const springProgress = spring({
  frame,
  fps,
});

// Map to rotation
const rotation = interpolate(springProgress, [0, 1], [0, 360]);

<div style={{ rotate: rotation + "deg" }} />;
```

### 叠加弹簧

弹簧函数只返回数值，因此可以进行数学运算：

```tsx
const frame = useCurrentFrame();
const { fps, durationInFrames } = useVideoConfig();

const inAnimation = spring({
  frame,
  fps,
});
const outAnimation = spring({
  frame,
  fps,
  durationInFrames: 1 * fps,
  delay: durationInFrames - 1 * fps,
});

const scale = inAnimation - outAnimation;
```

## 缓动

可在 `interpolate` 函数上添加缓动（easing）：

```ts
import { interpolate, Easing } from "remotion";

const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

默认缓动为 `Easing.linear`。  
还有其他凸性（convexity）可选：

- `Easing.in`：起步慢、随后加速
- `Easing.out`：起步快、随后减速
- `Easing.inOut`

以及曲线（由接近线性到弯曲程度递增）：

- `Easing.quad`
- `Easing.sin`
- `Easing.exp`
- `Easing.circle`

凸性与曲线需组合使用才能构成缓动函数：

```ts
const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

也支持三次贝塞尔曲线：

```ts
const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.bezier(0.8, 0.22, 0.96, 0.65),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```
