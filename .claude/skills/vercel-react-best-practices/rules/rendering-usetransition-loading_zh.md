---
title: 用 useTransition 替代手动 loading 状态
impact: LOW
impactDescription: 减少重渲染并提高代码清晰度
tags: rendering, transitions, useTransition, loading, state
---

## 用 useTransition 替代手动 loading 状态

用 `useTransition` 替代手动 `useState` 来管理 loading 状态。这样可获得内置的 `isPending` 状态，并自动管理 transition（过渡更新）。

**错误做法（手动 loading 状态）：**

```tsx
function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = async (value: string) => {
    setIsLoading(true)
    setQuery(value)
    const data = await fetchResults(value)
    setResults(data)
    setIsLoading(false)
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isLoading && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

**正确做法（useTransition 与内置 pending 状态）：**

```tsx
import { useTransition, useState } from 'react'

function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  const handleSearch = (value: string) => {
    setQuery(value) // Update input immediately
    
    startTransition(async () => {
      // Fetch and update results
      const data = await fetchResults(value)
      setResults(data)
    })
  }

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </>
  )
}
```

**优势：**

- **自动 pending 状态**：无需手动调用 `setIsLoading(true/false)`
- **错误恢复**：即使 transition 抛出异常，pending 状态也会正确重置
- **更好的响应性**：更新期间 UI 保持可交互
- **中断处理**：新的 transition 会自动取消尚未完成的 transition

Reference: [useTransition](https://react.dev/reference/react/useTransition)

