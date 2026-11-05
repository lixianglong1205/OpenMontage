---
title: useEffectEvent 实现稳定的回调引用
impact: LOW
impactDescription: 避免 effect 重复执行
tags: advanced, hooks, useEffectEvent, refs, optimization
---

## useEffectEvent 实现稳定的回调引用

在回调中访问最新值，而无需将其加入依赖数组。既能避免 effect 重复执行，又能防止闭包陈旧（stale closure）。

**错误（每次 callback 变化都会重新运行 effect）：**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')

  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300)
    return () => clearTimeout(timeout)
  }, [query, onSearch])
}
```

**正确（使用 React 的 useEffectEvent）：**

```tsx
import { useEffectEvent } from 'react';

function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')
  const onSearchEvent = useEffectEvent(onSearch)

  useEffect(() => {
    const timeout = setTimeout(() => onSearchEvent(query), 300)
    return () => clearTimeout(timeout)
  }, [query])
}
```

