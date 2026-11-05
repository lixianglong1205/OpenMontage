---
title: 使用 React.cache() 实现单次请求内去重
impact: MEDIUM
impactDescription: 在单个请求内去重
tags: server, cache, react-cache, deduplication
---

## 使用 React.cache() 实现单次请求内去重

在服务端使用 `React.cache()` 实现单次请求内的去重。认证与数据库查询收益最大。

**用法：**

```typescript
import { cache } from 'react'

export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({
    where: { id: session.user.id }
  })
})
```

在同一请求内多次调用 `getCurrentUser()` 时，查询只会执行一次。

**避免使用内联对象作为参数：**

`React.cache()` 通过浅比较（`Object.is`）判断是否命中缓存。内联对象每次调用都会创建新引用，导致无法命中缓存。

**错误示例（始终缓存未命中）：**

```typescript
const getUser = cache(async (params: { uid: number }) => {
  return await db.user.findUnique({ where: { id: params.uid } })
})

// Each call creates new object, never hits cache
getUser({ uid: 1 })
getUser({ uid: 1 })  // Cache miss, runs query again
```

**正确示例（缓存命中）：**

```typescript
const getUser = cache(async (uid: number) => {
  return await db.user.findUnique({ where: { id: uid } })
})

// Primitive args use value equality
getUser(1)
getUser(1)  // Cache hit, returns cached result
```

若必须传入对象，请传入同一引用：

```typescript
const params = { uid: 1 }
getUser(params)  // Query runs
getUser(params)  // Cache hit (same reference)
```

**Next.js 专项说明：**

在 Next.js 中，`fetch` API 会自动扩展请求 memoization。相同 URL 与选项的请求会在单次请求内自动去重，因此 `fetch` 调用不必再包一层 `React.cache()`。但对其他异步任务，`React.cache()` 仍然必不可少：

- 数据库查询（Prisma、Drizzle 等）
- 重计算
- 认证检查
- 文件系统操作
- 任意非 fetch 的异步工作

使用 `React.cache()` 在组件树中对上述操作去重。

Reference: [React.cache documentation](https://react.dev/reference/react/cache)
