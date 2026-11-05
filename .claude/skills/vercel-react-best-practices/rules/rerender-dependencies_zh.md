---
title: 缩小 Effect 依赖范围
impact: LOW
impactDescription: 减少 effect 重复执行
tags: rerender, useEffect, dependencies, optimization
---

## 缩小 Effect 依赖范围

用原始值（primitive）作为依赖项，而不是整个对象，以减少 effect 的重复执行。

**错误（user 任一字段变化都会重新运行）：**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user])
```

**正确（仅在 id 变化时重新运行）：**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

**对于派生状态，在 effect 外计算：**

```tsx
// Incorrect: runs on width=767, 766, 765...
useEffect(() => {
  if (width < 768) {
    enableMobileMode()
  }
}, [width])

// Correct: runs only on boolean transition
const isMobile = width < 768
useEffect(() => {
  if (isMobile) {
    enableMobileMode()
  }
}, [isMobile])
```
