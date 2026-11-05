---
title: 并行嵌套数据获取
impact: CRITICAL
impactDescription: 消除服务端瀑布式请求
tags: server, rsc, parallel-fetching, promise-chaining
---

## 并行嵌套数据获取

并行获取嵌套数据时，应在每个条目的 Promise 内链式串联有依赖关系的请求，这样某个慢条目不会拖住其余条目的嵌套请求。

**错误做法（单个慢条目会阻塞所有嵌套请求）：**

```tsx
const chats = await Promise.all(
  chatIds.map(id => getChat(id))
)

const chatAuthors = await Promise.all(
  chats.map(chat => getUser(chat.author))
)
```

若 100 次 `getChat(id)` 中有 1 次极慢，其余 99 个会话的数据虽已就绪，其作者信息仍无法开始加载。

**正确做法（每个条目各自链式嵌套请求）：**

```tsx
const chatAuthors = await Promise.all(
  chatIds.map(id => getChat(id).then(chat => getUser(chat.author)))
)
```

每个条目独立串联 `getChat` → `getUser`，某个会话很慢也不会阻塞其他条目的作者请求。
