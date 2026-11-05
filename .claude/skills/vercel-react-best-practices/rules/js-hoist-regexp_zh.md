---
title: 提前创建 RegExp
impact: LOW-MEDIUM
impactDescription: 避免重复创建
tags: javascript, regexp, optimization, memoization
---

## 提前创建 RegExp

不要在 render 内创建 RegExp。将其提升到模块作用域，或使用 `useMemo()` 做 memoize。

**错误做法（每次渲染都 new RegExp）：**

```tsx
function Highlighter({ text, query }: Props) {
  const regex = new RegExp(`(${query})`, 'gi')
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**正确做法（memoize 或提升到模块级）：**

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function Highlighter({ text, query }: Props) {
  const regex = useMemo(
    () => new RegExp(`(${escapeRegex(query)})`, 'gi'),
    [query]
  )
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**警告（全局正则具有可变状态）：**

带全局标志（`/g`）的正则具有可变的 `lastIndex` 状态：

```typescript
const regex = /foo/g
regex.test('foo')  // true, lastIndex = 3
regex.test('foo')  // false, lastIndex = 0
```
