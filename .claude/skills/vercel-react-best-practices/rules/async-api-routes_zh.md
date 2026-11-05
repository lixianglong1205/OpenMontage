---
title: 避免 API 路由中的瀑布式串行链
impact: CRITICAL
impactDescription: 2-10× 提升
tags: api-routes, server-actions, waterfalls, parallelization
---

## 避免 API 路由中的瀑布式串行链

在 API 路由与 Server Actions 中，即使尚未 `await`，也应立即启动彼此独立的操作。

**错误（config 需等待 auth，data 需等待两者）：**

```typescript
export async function GET(request: Request) {
  const session = await auth()
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return Response.json({ data, config })
}
```

**正确（auth 与 config 立即启动）：**

```typescript
export async function GET(request: Request) {
  const sessionPromise = auth()
  const configPromise = fetchConfig()
  const session = await sessionPromise
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id)
  ])
  return Response.json({ data, config })
}
```

对于依赖关系更复杂的操作，可使用 `better-all` 自动最大化并行度（参见基于依赖的并行化（Dependency-Based Parallelization））。
