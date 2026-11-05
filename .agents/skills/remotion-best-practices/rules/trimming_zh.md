---
name: trimming
description: Remotion 裁剪模式——剪掉动画的开头或结尾
metadata:
  tags: sequence, trim, clip, cut, offset
---

使用负值的 `from` 配合 `<Sequence>`，可裁剪动画的开头部分。

## 裁剪开头

`from` 为负值时，时间会向前偏移，使动画从中间某一帧开始播放：

```tsx
import { Sequence, useVideoConfig } from "remotion";

const fps = useVideoConfig();

<Sequence from={-0.5 * fps}>
  <MyAnimation />
</Sequence>;
```

动画会从其进度的第 15 帧处出现——最前面的 15 帧被裁掉。
在 `<MyAnimation>` 内部，`useCurrentFrame()` 从 15 开始，而不是 0。

## 裁剪结尾

使用 `durationInFrames` 在指定时长后卸载内容：

```tsx
<Sequence durationInFrames={1.5 * fps}>
  <MyAnimation />
</Sequence>
```

动画播放 45 帧后，组件会被卸载。

## 裁剪并延迟

嵌套多个 Sequence，可同时裁剪开头并延迟出现时机：

```tsx
<Sequence from={30}>
  <Sequence from={-15}>
    <MyAnimation />
  </Sequence>
</Sequence>
```

内层 Sequence 从开头裁掉 15 帧，外层 Sequence 再将结果延迟 30 帧出现。
