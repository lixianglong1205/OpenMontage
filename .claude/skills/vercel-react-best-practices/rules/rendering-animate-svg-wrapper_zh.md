---
title: 动画 SVG 包装层而非 SVG 元素本身
impact: LOW
impactDescription: 启用硬件加速
tags: rendering, svg, css, animation, performance
---

## 动画 SVG 包装层而非 SVG 元素本身

许多浏览器无法对 SVG 元素上的 CSS3 动画进行硬件加速。请将 SVG 包在 `<div>` 中，并对包装层施加动画。

**错误做法（直接动画 SVG——无硬件加速）：**

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

**正确做法（动画包装 div——硬件加速）：**

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
