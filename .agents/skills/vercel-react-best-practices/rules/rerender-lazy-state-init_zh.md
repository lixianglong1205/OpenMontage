---
title: 使用惰性状态初始化
impact: MEDIUM
impactDescription: 每次渲染都会浪费计算
tags: react, hooks, useState, performance, initialization
---

## 使用惰性状态初始化

向 `useState` 传入函数，用于昂贵的初始值。若不使用函数形式，初始化逻辑会在每次渲染时执行，尽管该值只会被使用一次。

**错误（每次渲染都会运行）：**

```tsx
function FilteredList({ items }: { items: Item[] }) {
  // buildSearchIndex() runs on EVERY render, even after initialization
  const [searchIndex, setSearchIndex] = useState(buildSearchIndex(items))
  const [query, setQuery] = useState('')
  
  // When query changes, buildSearchIndex runs again unnecessarily
  return <SearchResults index={searchIndex} query={query} />
}

function UserProfile() {
  // JSON.parse runs on every render
  const [settings, setSettings] = useState(
    JSON.parse(localStorage.getItem('settings') || '{}')
  )
  
  return <SettingsForm settings={settings} onChange={setSettings} />
}
```

**正确（仅在首次渲染时运行）：**

```tsx
function FilteredList({ items }: { items: Item[] }) {
  // buildSearchIndex() runs ONLY on initial render
  const [searchIndex, setSearchIndex] = useState(() => buildSearchIndex(items))
  const [query, setQuery] = useState('')
  
  return <SearchResults index={searchIndex} query={query} />
}

function UserProfile() {
  // JSON.parse runs only on initial render
  const [settings, setSettings] = useState(() => {
    const stored = localStorage.getItem('settings')
    return stored ? JSON.parse(stored) : {}
  })
  
  return <SettingsForm settings={settings} onChange={setSettings} />
}
```

在以下场景使用惰性初始化：从 localStorage/sessionStorage 计算初始值、构建数据结构（索引、映射）、从 DOM 读取，或执行较重的转换。

对于简单原始值（`useState(0)`）、直接引用（`useState(props.value)`）或开销很小的字面量（`useState({})`），无需使用函数形式。
