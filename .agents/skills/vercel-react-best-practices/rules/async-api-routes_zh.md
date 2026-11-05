---
title: 防止 API 路由中的瀑布链
impact: CRITICAL
impactDescription: 2-10 倍性能提升
tags: api-routes, server-actions, waterfalls, parallelization
---

## 防止 API 路由中的瀑布链

在 API 路由和 Server Actions 中，应立刻启动彼此独立的操作，即使尚未 await 它们。

**错误（config 等待 auth，data 等待两者）：**

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

对于依赖关系更复杂的操作链，可使用 `better-all` 自动最大化并行度（参见「基于依赖的并行化」）。
