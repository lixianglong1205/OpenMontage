---
name: transitions
description: 使用 TransitionSeries 在 Remotion 中实现场景转场与叠加层。
metadata:
  tags: transitions, overlays, fade, slide, wipe, scenes
---

## TransitionSeries

`<TransitionSeries>` 用于编排场景，并支持两种方式增强场景之间的切点：

- **Transitions**（`<TransitionSeries.Transition>`）— 在两个场景之间进行交叉淡化、滑动、擦除等转场。转场期间两个场景同时播放，因此会缩短时间轴总长度。
- **Overlays**（`<TransitionSeries.Overlay>`）— 在切点上方渲染效果（例如光斑泄漏），且不缩短时间轴。

子元素采用绝对定位。

## 前提条件

```bash
npx remotion add @remotion/transitions
```

## 转场示例

```tsx
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>;
```

## 叠加层示例

任意 React 组件都可用作叠加层。现成效果请参阅 **light-leaks** 规则。

```tsx
import { TransitionSeries } from "@remotion/transitions";
import { LightLeak } from "@remotion/light-leaks";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Overlay durationInFrames={20}>
    <LightLeak />
  </TransitionSeries.Overlay>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>;
```

## 混合使用转场与叠加层

转场与叠加层可在同一 `<TransitionSeries>` 中共存，但叠加层不能与转场或另一个叠加层相邻。

```tsx
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { LightLeak } from "@remotion/light-leaks";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Overlay durationInFrames={30}>
    <LightLeak />
  </TransitionSeries.Overlay>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneC />
  </TransitionSeries.Sequence>
</TransitionSeries>;
```

## 转场属性

`<TransitionSeries.Transition>` 需要：

- `presentation` — 视觉效果（例如 `fade()`、`slide()`、`wipe()`）。
- `timing` — 控制速度与缓动（例如 `linearTiming()`、`springTiming()`）。

## 叠加层属性

`<TransitionSeries.Overlay>` 接受：

- `durationInFrames` — 叠加层可见时长（正整数）。
- `offset?` — 相对于切点中心的偏移。正值表示更晚，负值表示更早。默认：`0`。

## 可用的转场类型

从各自模块导入转场：

```tsx
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { flip } from "@remotion/transitions/flip";
import { clockWipe } from "@remotion/transitions/clock-wipe";
```

## 带方向的滑动转场

```tsx
import { slide } from "@remotion/transitions/slide";

<TransitionSeries.Transition
  presentation={slide({ direction: "from-left" })}
  timing={linearTiming({ durationInFrames: 20 })}
/>;
```

方向：`"from-left"`、`"from-right"`、`"from-top"`、`"from-bottom"`

## 时间选项

```tsx
import { linearTiming, springTiming } from "@remotion/transitions";

// Linear timing - constant speed
linearTiming({ durationInFrames: 20 });

// Spring timing - organic motion
springTiming({ config: { damping: 200 }, durationInFrames: 25 });
```

## 时长计算

转场与相邻场景重叠，因此合成总长度**短于**所有序列时长之和。叠加层**不会**影响总时长。

例如，两个 60 帧的序列与 15 帧的转场：

- 无转场：`60 + 60 = 120` 帧
- 有转场：`60 + 60 - 15 = 105` 帧

在两个序列之间添加叠加层不会改变总时长。

### 获取转场的时长

在 timing 对象上使用 `getDurationInFrames()` 方法：

```tsx
import { linearTiming, springTiming } from "@remotion/transitions";

const linearDuration = linearTiming({
  durationInFrames: 20,
}).getDurationInFrames({ fps: 30 });
// Returns 20

const springDuration = springTiming({
  config: { damping: 200 },
}).getDurationInFrames({ fps: 30 });
// Returns calculated duration based on spring physics
```

对于未显式指定 `durationInFrames` 的 `springTiming`，时长取决于 `fps`，因为会根据弹簧物理计算动画何时稳定。

### 计算合成总时长

```tsx
import { linearTiming } from "@remotion/transitions";

const scene1Duration = 60;
const scene2Duration = 60;
const scene3Duration = 60;

const timing1 = linearTiming({ durationInFrames: 15 });
const timing2 = linearTiming({ durationInFrames: 20 });

const transition1Duration = timing1.getDurationInFrames({ fps: 30 });
const transition2Duration = timing2.getDurationInFrames({ fps: 30 });

const totalDuration =
  scene1Duration +
  scene2Duration +
  scene3Duration -
  transition1Duration -
  transition2Duration;
// 60 + 60 + 60 - 15 - 20 = 145 frames
```
