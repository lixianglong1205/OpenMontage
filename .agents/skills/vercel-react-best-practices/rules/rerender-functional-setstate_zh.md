---
title: 使用函数式 setState 更新
impact: MEDIUM
impactDescription: 避免陈旧闭包和不必要的回调重建
tags: react, hooks, useState, useCallback, callbacks, closures
---

## 使用函数式 setState 更新

当更新依赖当前 state 值的状态时，应使用 setState 的函数式更新形式，而不是直接引用 state 变量。这样可以避免陈旧闭包、减少不必要的依赖，并创建稳定的回调引用。

**错误（需要将 state 作为依赖）：**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  // Callback must depend on items, recreated on every items change
  const addItems = useCallback((newItems: Item[]) => {
    setItems([...items, ...newItems])
  }, [items])  // ❌ items dependency causes recreations
  
  // Risk of stale closure if dependency is forgotten
  const removeItem = useCallback((id: string) => {
    setItems(items.filter(item => item.id !== id))
  }, [])  // ❌ Missing items dependency - will use stale items!
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

第一个回调会在每次 `items` 变化时重新创建，可能导致子组件不必要的重渲染。第二个回调存在陈旧闭包问题——它始终引用初始的 `items` 值。

**正确（稳定的回调，无陈旧闭包）：**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)
  
  // Stable callback, never recreated
  const addItems = useCallback((newItems: Item[]) => {
    setItems(curr => [...curr, ...newItems])
  }, [])  // ✅ No dependencies needed
  
  // Always uses latest state, no stale closure risk
  const removeItem = useCallback((id: string) => {
    setItems(curr => curr.filter(item => item.id !== id))
  }, [])  // ✅ Safe and stable
  
  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

**收益：**

1. **稳定的回调引用** — state 变化时无需重建回调
2. **无陈旧闭包** — 始终基于最新的 state 值操作
3. **更少的依赖** — 简化依赖数组，降低内存泄漏风险
4. **预防 bug** — 消除 React 闭包问题最常见的来源

**何时使用函数式更新：**

- 任何依赖当前 state 值的 setState
- 在 useCallback/useMemo 中需要 state 时
- 引用 state 的事件处理函数
- 更新 state 的异步操作

**何时可以直接更新：**

- 将 state 设为静态值：`setCount(0)`
- 仅根据 props/参数设置 state：`setName(newName)`
- 新 state 不依赖先前的值

**注意：** 若项目已启用 [React Compiler](https://react.dev/learn/react-compiler)，编译器可以自动优化部分场景，但为正确性并避免陈旧闭包 bug，仍建议使用函数式更新。
