---
title: 使用 toSorted() 而非 sort() 以保持不可变性
impact: MEDIUM-HIGH
impactDescription: 避免 React state 中的突变 bug
tags: javascript, arrays, immutability, react, state, mutation
---

## 使用 toSorted() 而非 sort() 以保持不可变性

`.sort()` 会就地修改数组，在 React 的 state 和 props 中可能引发 bug。应使用 `.toSorted()` 创建新的已排序数组，而不修改原数组。

**错误（会修改原数组）：**

```typescript
function UserList({ users }: { users: User[] }) {
  // Mutates the users prop array!
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**正确（创建新数组）：**

```typescript
function UserList({ users }: { users: User[] }) {
  // Creates new sorted array, original unchanged
  const sorted = useMemo(
    () => users.toSorted((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**为何在 React 中很重要：**

1. 修改 props/state 会破坏 React 的不可变（immutability）模型——React 期望将 props 与 state 视为只读
2. 会导致陈旧闭包（stale closure）bug——在闭包（回调、effect）内修改数组可能导致意外行为

**浏览器支持（旧浏览器的回退方案）：**

`.toSorted()` 在所有现代浏览器中可用（Chrome 110+、Safari 16+、Firefox 115+、Node.js 20+）。在更旧的环境中，可使用展开运算符：

```typescript
// Fallback for older browsers
const sorted = [...items].sort((a, b) => a.value - b.value)
```

**其他不可变数组方法：**

- `.toSorted()` - 不可变排序
- `.toReversed()` - 不可变反转
- `.toSpliced()` - 不可变 splice
- `.with()` - 不可变元素替换
