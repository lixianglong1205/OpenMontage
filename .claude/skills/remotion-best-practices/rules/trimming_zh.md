---
name: trimming
description: Remotion 裁剪模式 - 剪切动画的开头或结尾
metadata:
  tags: sequence, trim, clip, cut, offset
---

使用负值 `from` 的 `<Sequence>` 来裁剪动画的开头。

## 裁剪开头

负的 `from` 值会将时间向后偏移，使动画从中间某处开始播放：

```tsx
import { Sequence, useVideoConfig } from "remotion";

const fps = useVideoConfig();

<Sequence from={-0.5 * fps}>
  <MyAnimation />
</Sequence>;
```

动画从第 15 帧处开始显示——前 15 帧被裁掉。
在 `<MyAnimation>` 内部，`useCurrentFrame()` 从 15 开始而不是 0。

## 裁剪结尾

使用 `durationInFrames` 在指定时长后卸载内容：

```tsx
<Sequence durationInFrames={1.5 * fps}>
  <MyAnimation />
</Sequence>
```

动画播放 45 帧后，组件卸载。

## 裁剪并延迟

嵌套 Sequence 可同时裁剪开头并延迟出现时机：

```tsx
<Sequence from={30}>
  <Sequence from={-15}>
    <MyAnimation />
  </Sequence>
</Sequence>
```

内层 Sequence 从开头裁掉 15 帧，外层 Sequence 将结果延迟 30 帧。
