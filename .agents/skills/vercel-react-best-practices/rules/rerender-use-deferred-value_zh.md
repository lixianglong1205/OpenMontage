---
title: 对高开销派生渲染使用 useDeferredValue
impact: MEDIUM
impactDescription: 在重计算期间保持输入响应
tags: rerender, useDeferredValue, optimization, concurrent
---

## 对高开销派生渲染使用 useDeferredValue

当用户输入会触发高开销的计算或渲染时，使用 `useDeferredValue` 保持输入响应。延迟值会滞后于最新输入，让 React 优先处理输入更新，并在空闲时再渲染高开销结果。

**错误示例（过滤时输入会感觉卡顿）：**

```tsx
function Search({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('')
  const filtered = items.filter(item => fuzzyMatch(item, query))

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <ResultsList results={filtered} />
    </>
  )
}
```

**正确示例（输入保持流畅，结果就绪后再渲染）：**

```tsx
function Search({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('')
  const deferredQuery = useDeferredValue(query)
  const filtered = useMemo(
    () => items.filter(item => fuzzyMatch(item, deferredQuery)),
    [items, deferredQuery]
  )
  const isStale = query !== deferredQuery

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <div style={{ opacity: isStale ? 0.7 : 1 }}>
        <ResultsList results={filtered} />
      </div>
    </>
  )
}
```

**适用场景：**

- 过滤/搜索大型列表
- 随输入变化的高开销可视化（图表、图形等）
- 任何会导致明显渲染延迟的派生状态

**注意：** 将高开销计算包在 `useMemo` 中，并以延迟值作为依赖项，否则仍会在每次渲染时执行。

Reference: [React useDeferredValue](https://react.dev/reference/react/useDeferredValue)
