---
title: 在 RSC 边界最小化序列化
impact: HIGH
impactDescription: 减小数据传输体积
tags: server, rsc, serialization, props
---

## 在 RSC 边界最小化序列化

React 服务端/客户端边界会把对象的所有属性序列化为字符串，并嵌入 HTML 响应及后续的 RSC 请求中。这些序列化数据会直接影响页面体积与加载时间，因此**体积非常关键**。只传递客户端实际会用到的字段。

**错误（序列化全部 50 个字段）：**

```tsx
async function Page() {
  const user = await fetchUser()  // 50 fields
  return <Profile user={user} />
}

'use client'
function Profile({ user }: { user: User }) {
  return <div>{user.name}</div>  // uses 1 field
}
```

**正确（仅序列化 1 个字段）：**

```tsx
async function Page() {
  const user = await fetchUser()
  return <Profile name={user.name} />
}

'use client'
function Profile({ name }: { name: string }) {
  return <div>{name}</div>
}
```
