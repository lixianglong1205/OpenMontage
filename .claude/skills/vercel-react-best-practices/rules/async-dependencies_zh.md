---
title: 基于依赖关系的并行化
impact: CRITICAL
impactDescription: 2–10 倍性能提升
tags: async, parallelization, dependencies, better-all
---

## 基于依赖关系的并行化

对于存在部分依赖关系的操作，使用 `better-all` 来最大化并行度。它会在每个任务最早可能的时刻自动启动该任务。

**错误（profile 不必要地等待 config）：**

```typescript
const [user, config] = await Promise.all([
  fetchUser(),
  fetchConfig()
])
const profile = await fetchProfile(user.id)
```

**正确（config 与 profile 并行运行）：**

```typescript
import { all } from 'better-all'

const { user, config, profile } = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id)
  }
})
```

**不引入额外依赖的替代方案：**

也可以先创建所有 promise，最后再执行 `Promise.all()`。

```typescript
const userPromise = fetchUser()
const profilePromise = userPromise.then(user => fetchProfile(user.id))

const [user, config, profile] = await Promise.all([
  userPromise,
  fetchConfig(),
  profilePromise
])
```

Reference: [https://github.com/shuding/better-all](https://github.com/shuding/better-all)
