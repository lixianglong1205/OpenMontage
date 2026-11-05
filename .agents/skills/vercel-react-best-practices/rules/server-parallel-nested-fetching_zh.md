---
title: 并行嵌套数据获取
impact: CRITICAL
impactDescription: 消除服务端瀑布流
tags: server, rsc, parallel-fetching, promise-chaining
---

## 并行嵌套数据获取

并行获取嵌套数据时，应在每一项的 Promise 内链式串联有依赖关系的 fetch，这样单个慢项不会拖住其余请求。

**错误示例（单个慢项会阻塞所有嵌套 fetch）：**

```tsx
const chats = await Promise.all(
  chatIds.map(id => getChat(id))
)

const chatAuthors = await Promise.all(
  chats.map(chat => getUser(chat.author))
)
```

若 100 个 `getChat(id)` 中有 1 个极慢，其余 99 个会话的作者信息即使已就绪，也无法开始加载。

**正确示例（各项独立链式嵌套 fetch）：**

```tsx
const chatAuthors = await Promise.all(
  chatIds.map(id => getChat(id).then(chat => getUser(chat.author)))
)
```

每一项独立串联 `getChat` → `getUser`，某个会话很慢也不会阻塞其他会话的作者 fetch。
