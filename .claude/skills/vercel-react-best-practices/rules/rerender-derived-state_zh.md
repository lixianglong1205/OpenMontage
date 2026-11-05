---
title: 订阅派生状态
impact: MEDIUM
impactDescription: 降低重渲染频率
tags: rerender, derived-state, media-query, optimization
---

## 订阅派生状态

订阅派生布尔状态，而非连续变化的数值，以降低重渲染频率。

**错误（每个像素变化都会重渲染）：**

```tsx
function Sidebar() {
  const width = useWindowWidth()  // updates continuously
  const isMobile = width < 768
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

**正确（仅在布尔值变化时重渲染）：**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)')
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

