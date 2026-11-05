---
title: 缓存 Storage API 调用
impact: LOW-MEDIUM
impactDescription: 减少昂贵的 I/O
tags: javascript, localStorage, storage, caching, performance
---

## 缓存 Storage API 调用

`localStorage`、`sessionStorage` 和 `document.cookie` 是同步的且开销较大。应在内存中缓存读取结果。

**错误（每次调用都读取 storage）：**

```typescript
function getTheme() {
  return localStorage.getItem('theme') ?? 'light'
}
// Called 10 times = 10 storage reads
```

**正确（Map 缓存）：**

```typescript
const storageCache = new Map<string, string | null>()

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key))
  }
  return storageCache.get(key)
}

function setLocalStorage(key: string, value: string) {
  localStorage.setItem(key, value)
  storageCache.set(key, value)  // keep cache in sync
}
```

使用 Map（而非 hook），以便在工具函数、事件处理器等各处生效，而不仅限于 React 组件。

**Cookie 缓存：**

```typescript
let cookieCache: Record<string, string> | null = null

function getCookie(name: string) {
  if (!cookieCache) {
    cookieCache = Object.fromEntries(
      document.cookie.split('; ').map(c => c.split('='))
    )
  }
  return cookieCache[name]
}
```

**重要（外部变更时失效缓存）：**

若 storage 可能在外部被修改（其他标签页、服务端设置的 cookie），应使缓存失效：

```typescript
window.addEventListener('storage', (e) => {
  if (e.key) storageCache.delete(e.key)
})

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    storageCache.clear()
  }
})
```
