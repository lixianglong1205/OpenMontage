---
title: 跨请求 LRU 缓存
impact: HIGH
impactDescription: 跨请求缓存
tags: server, cache, lru, cross-request
---

## 跨请求 LRU 缓存

`React.cache()` 仅在单次请求内有效。若数据需要在连续多次请求之间共享（例如用户先点击按钮 A，再点击按钮 B），应使用 LRU 缓存（Least Recently Used cache）。

**实现：**

```typescript
import { LRUCache } from 'lru-cache'

const cache = new LRUCache<string, any>({
  max: 1000,
  ttl: 5 * 60 * 1000  // 5 minutes
})

export async function getUser(id: string) {
  const cached = cache.get(id)
  if (cached) return cached

  const user = await db.user.findUnique({ where: { id } })
  cache.set(id, user)
  return user
}

// Request 1: DB query, result cached
// Request 2: cache hit, no DB query
```

当用户的连续操作在几秒内触发多个端点、且都需要相同数据时，适合采用此方式。

**配合 Vercel 的 [Fluid Compute](https://vercel.com/docs/fluid-compute)：** LRU 缓存尤其有效，因为多个并发请求可以共享同一函数实例与缓存。这意味着缓存可在请求之间持久存在，无需 Redis 等外部存储。

**在传统 serverless 环境下：** 每次调用相互隔离，跨进程缓存可考虑使用 Redis。

Reference: [https://github.com/isaacs/node-lru-cache](https://github.com/isaacs/node-lru-cache)
