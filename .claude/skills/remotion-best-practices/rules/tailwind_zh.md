---
name: tailwind
description: 在 Remotion 中使用 TailwindCSS。
metadata:
---

你可以在 Remotion 中使用（并且应当使用）TailwindCSS，前提是项目中已安装 TailwindCSS。

不要使用 `transition-*` 或 `animate-*` 类——始终使用 `useCurrentFrame()` 钩子来实现动画。

必须先在 Remotion 项目中安装并启用 Tailwind——请通过 WebFetch 访问 https://www.remotion.dev/docs/tailwind 获取说明。
