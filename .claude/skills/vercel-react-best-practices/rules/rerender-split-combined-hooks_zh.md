---
title: 拆分合并的 Hook 计算
impact: MEDIUM
impactDescription: 避免重复计算彼此独立的步骤
tags: rerender, useMemo, useEffect, dependencies, optimization
---

## 拆分合并的 Hook 计算

当某个 hook 包含多个依赖项不同的独立任务时，应拆成多个 hook。合并在一起时，任一依赖变化都会导致所有任务重新执行，即使某些任务并不依赖该变化的值。

**错误（修改 `sortOrder` 会重新执行过滤）：**

```tsx
const sortedProducts = useMemo(() => {
  const filtered = products.filter((p) => p.category === category)
  const sorted = filtered.toSorted((a, b) =>
    sortOrder === "asc" ? a.price - b.price : b.price - a.price
  )
  return sorted
}, [products, category, sortOrder])
```

**正确（仅当 products 或 category 变化时才重新过滤）：**

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

这一模式也适用于 `useEffect` 中合并互不相关的副作用：

**错误（任一依赖变化时两个 effect 都会运行）：**

```tsx
useEffect(() => {
  analytics.trackPageView(pathname)
  document.title = `${pageTitle} | My App`
}, [pathname, pageTitle])
```

**正确（effect 彼此独立运行）：**

```tsx
useEffect(() => {
  analytics.trackPageView(pathname)
}, [pathname])

useEffect(() => {
  document.title = `${pageTitle} | My App`
}, [pageTitle])
```

**注意：** 若项目已启用 [React Compiler](https://react.dev/learn/react-compiler)，它会自动优化依赖追踪，并在部分场景下替你处理这些情况。
