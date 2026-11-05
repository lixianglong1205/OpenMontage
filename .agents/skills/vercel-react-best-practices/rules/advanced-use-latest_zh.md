---
title: 使用 useEffectEvent 实现稳定的回调引用
impact: LOW
impactDescription: 避免 effect 重新运行
tags: advanced, hooks, useEffectEvent, refs, optimization
---

## 使用 useEffectEvent 实现稳定的回调引用

在回调中访问最新值，而无需将其加入依赖数组。可避免 effect 因依赖变化而重新运行，同时防止闭包陈旧。

**不正确（回调每次变化都会导致 effect 重新运行）：**

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
