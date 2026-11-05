---
title: 订阅派生状态
impact: MEDIUM
impactDescription: 降低重新渲染频率
tags: rerender, derived-state, media-query, optimization
---

## 订阅派生状态

订阅派生布尔状态，而不是连续变化的数值，以降低重新渲染频率。

**错误示例（每次像素变化都会重新渲染）：**

```tsx
function Sidebar() {
  const width = useWindowWidth()  // updates continuously
  const isMobile = width < 768
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

**正确示例（仅在布尔值变化时重新渲染）：**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)')
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```
