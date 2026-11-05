---
title: Split Combined Hook Computations
impact: MEDIUM
impactDescription: avoids recomputing independent steps
tags: rerender, useMemo, useEffect, dependencies, optimization
---

## 拆分合并的 Hook 计算

当某个 hook 包含多个彼此独立、且依赖项不同的任务时，应拆成多个 hook。合并在一起后，任意依赖变化都会重跑全部任务，即便某些任务并不使用该变化项。

**不正确（更改 `sortOrder` 会重新计算 filtering）：**

```tsx
const sortedProducts = useMemo(() => {
  const filtered = products.filter((p) => p.category === category)
  const sorted = filtered.toSorted((a, b) =>
    sortOrder === "asc" ? a.price - b.price : b.price - a.price
  )
  return sorted
}, [products, category, sortOrder])
```

**正确（仅当 `products` 或 `category` 变化时才重新计算 filtering）：**

```tsx
const filteredProducts = useMemo(
  () => products.filter((p) => p.category === category),
  [products, category]
)

const sortedProducts = useMemo(
  () =>
    filteredProducts.toSorted((a, b) =>
      sortOrder === "asc" ? a.price - b.price : b.price - a.price
    ),
  [filteredProducts, sortOrder]
)
```

在 `useEffect` 中合并互不相关的副作用时，同样适用这一模式：

**不正确（任一依赖变化时两个副作用都会执行）：**

```tsx
useEffect(() => {
  analytics.trackPageView(pathname)
  document.title = `${pageTitle} | My App`
}, [pathname, pageTitle])
```

**正确（副作用彼此独立执行）：**

```tsx
useEffect(() => {
  analytics.trackPageView(pathname)
}, [pathname])

useEffect(() => {
  document.title = `${pageTitle} | My App`
}, [pageTitle])
```

**注意：** 若项目已启用 [React Compiler](https://react.dev/learn/react-compiler)，它会自动优化依赖追踪，并可能在部分场景下替你处理上述情况。
