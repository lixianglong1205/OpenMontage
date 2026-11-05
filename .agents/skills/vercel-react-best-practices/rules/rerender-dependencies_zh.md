---
title: 收窄 Effect 依赖
impact: LOW
impactDescription: 减少 effect 重复执行
tags: rerender, useEffect, dependencies, optimization
---

## 收窄 Effect 依赖

用原始类型（primitive）作为依赖项，而不是整个对象，以减少 effect 的重复执行。

**错误（user 任意字段变化都会重新执行）：**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user])
```

**正确（仅在 id 变化时重新执行）：**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

**对于派生状态，在 effect 外部计算：**

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
