---
title: 动画作用于 SVG 包装层而非 SVG 元素本身
impact: LOW
impactDescription: 可启用硬件加速
tags: rendering, svg, css, animation, performance
---

## 动画作用于 SVG 包装层而非 SVG 元素本身

许多浏览器无法对 SVG 元素上的 CSS3 动画启用硬件加速。将 SVG 包在 `<div>` 中，对包装层做动画即可。

**错误（直接对 SVG 做动画——无硬件加速）：**

```tsx
function LoadingSpinner() {
  return (
    <svg 
      className="animate-spin"
      width="24" 
      height="24" 
      viewBox="0 0 24 24"
    >
      <circle cx="12" cy="12" r="10" stroke="currentColor" />
    </svg>
  )
}
```

**正确（对包装 div 做动画——硬件加速）：**

```tsx
function LoadingSpinner() {
  return (
    <div className="animate-spin">
      <svg 
        width="24" 
        height="24" 
        viewBox="0 0 24 24"
      >
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  )
}
```

这适用于所有 CSS 变换与过渡（`transform`、`opacity`、`translate`、`scale`、`rotate`）。包装 div 能让浏览器使用 GPU 加速，使动画更流畅。
