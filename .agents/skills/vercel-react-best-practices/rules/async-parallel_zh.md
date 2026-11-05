---
title: 独立操作用 Promise.all()
impact: CRITICAL
impactDescription: 2–10 倍提升
tags: async, parallelization, promises, waterfalls
---

## 独立操作用 Promise.all()

当异步操作彼此之间没有依赖关系时，应使用 `Promise.all()` 并发执行。

**错误示例（串行执行，3 次往返）：**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**正确示例（并行执行，1 次往返）：**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```
