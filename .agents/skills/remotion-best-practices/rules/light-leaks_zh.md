---
name: light-leaks
description: 使用 @remotion/light-leaks 在 Remotion 中实现的光斑叠加效果。
metadata:
  tags: light-leaks, overlays, effects, transitions
---

## 光斑（Light Leaks）

仅适用于 Remotion 4.0.415 及更高版本。使用 `npx remotion versions` 检查 Remotion 版本，使用 `npx remotion upgrade` 升级 Remotion 版本。

来自 `@remotion/light-leaks` 的 `<LightLeak>` 组件渲染基于 WebGL 的光斑效果。效果在其持续时间的前半段显现，在后半段收回。

通常放在 `<TransitionSeries.Overlay>` 内，在两个场景之间的切点上方播放。有关 `<TransitionSeries>` 与叠加层用法，请参阅 **transitions** 规则。

## 前提条件

```bash
npx remotion add @remotion/light-leaks
```

## 与 TransitionSeries 的基本用法

```tsx
import { TransitionSeries } from "@remotion/transitions";
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
</TransitionSeries>;
```

## 属性（Props）

- `durationInFrames?` — 默认为父级 sequence/composition 的时长。效果在前半段显现，在后半段收回。
- `seed?` — 决定光斑图案的形状。不同 seed 产生不同图案。默认：`0`。
- `hueShift?` — 以度为单位旋转色相（`0`–`360`）。默认：`0`（黄到橙）。`120` = 绿色，`240` = 蓝色。

## 自定义外观

```tsx
import { LightLeak } from "@remotion/light-leaks";

// Blue-tinted light leak with a different pattern
<LightLeak seed={5} hueShift={240} />;

// Green-tinted light leak
<LightLeak seed={2} hueShift={120} />;
```

## 独立用法

`<LightLeak>` 也可在 `<TransitionSeries>` 之外使用，例如作为任意 composition 中的装饰性叠加层：

```tsx
import { AbsoluteFill } from "remotion";
import { LightLeak } from "@remotion/light-leaks";

const MyComp: React.FC = () => (
  <AbsoluteFill>
    <MyContent />
    <LightLeak durationInFrames={60} seed={3} />
  </AbsoluteFill>
);
```
