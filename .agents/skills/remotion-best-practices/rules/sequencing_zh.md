---
name: sequencing
description: Remotion 时序模式——延迟、裁剪、限制片段时长
metadata:
  tags: sequence, series, timing, delay, trim
---

使用 `<Sequence>` 控制元素在时间轴上何时出现。

```tsx
import { Sequence } from "remotion";

const {fps} = useVideoConfig();

<Sequence from={1 * fps} durationInFrames={2 * fps} premountFor={1 * fps}>
  <Title />
</Sequence>
<Sequence from={2 * fps} durationInFrames={2 * fps} premountFor={1 * fps}>
  <Subtitle />
</Sequence>
```

默认情况下，这会把组件包在一个 absolute fill 元素里。  
若不需要包裹子项，可使用 `layout` 属性：

```tsx
<Sequence layout="none">
  <Title />
</Sequence>
```

## 预挂载（Premounting）

这会在片段真正播放之前，就在时间轴上加载组件。  
请始终为任意 `<Sequence>` 设置预挂载！

```tsx
<Sequence premountFor={1 * fps}>
  <Title />
</Sequence>
```

## Series

当多个元素应依次播放、互不重叠时，使用 `<Series>`。

```tsx
import { Series } from "remotion";

<Series>
  <Series.Sequence durationInFrames={45}>
    <Intro />
  </Series.Sequence>
  <Series.Sequence durationInFrames={60}>
    <MainContent />
  </Series.Sequence>
  <Series.Sequence durationInFrames={30}>
    <Outro />
  </Series.Sequence>
</Series>;
```

与 `<Sequence>` 相同，使用 `<Series.Sequence>` 时默认也会用 absolute fill 元素包裹子项，除非将 `layout` 设为 `none`。

### 带重叠的 Series

使用负的 `offset` 让序列重叠：

```tsx
<Series>
  <Series.Sequence durationInFrames={60}>
    <SceneA />
  </Series.Sequence>
  <Series.Sequence offset={-15} durationInFrames={60}>
    {/* Starts 15 frames before SceneA ends */}
    <SceneB />
  </Series.Sequence>
</Series>
```

## Sequence 内的帧引用

在 Sequence 内部，`useCurrentFrame()` 返回局部帧（从 0 开始）：

```tsx
<Sequence from={60} durationInFrames={30}>
  <MyComponent />
  {/* Inside MyComponent, useCurrentFrame() returns 0-29, not 60-89 */}
</Sequence>
```

## 嵌套 Sequence

可嵌套 Sequence 以实现复杂时序：

```tsx
<Sequence from={0} durationInFrames={120}>
  <Background />
  <Sequence from={15} durationInFrames={90} layout="none">
    <Title />
  </Sequence>
  <Sequence from={45} durationInFrames={60} layout="none">
    <Subtitle />
  </Sequence>
</Sequence>
```

## 在合成中嵌套另一个合成

若要在某个合成内加入另一个合成，可使用带 `width` 与 `height` 属性的 `<Sequence>` 指定内层合成的尺寸。

```tsx
<AbsoluteFill>
  <Sequence width={COMPOSITION_WIDTH} height={COMPOSITION_HEIGHT}>
    <CompositionComponent />
  </Sequence>
</AbsoluteFill>
```
