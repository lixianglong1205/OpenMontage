---
name: animations
description: Remotion 基础动画技能
metadata:
  tags: animations, transitions, frames, useCurrentFrame
---

所有动画必须由 `useCurrentFrame()` 钩子驱动。  
请以秒为单位编写动画，再乘以 `useVideoConfig()` 返回的 `fps` 值。

```tsx
import { useCurrentFrame } from "remotion";

export const FadeIn = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  return <div style={{ opacity }}>Hello World!</div>;
};
```

禁止使用 CSS transition 或 animation——它们无法正确渲染。  
禁止使用 Tailwind 动画类名——它们无法正确渲染。
