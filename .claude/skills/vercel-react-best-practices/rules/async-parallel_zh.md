---
title: 独立操作使用 Promise.all()
impact: CRITICAL
impactDescription: 2-10× 提升
tags: async, parallelization, promises, waterfalls
---

## 独立操作使用 Promise.all()

当异步操作彼此没有依赖关系时，使用 `Promise.all()` 并发执行它们。

**错误（顺序执行，3 次往返）：**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**正确（并行执行，1 次往返）：**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```

