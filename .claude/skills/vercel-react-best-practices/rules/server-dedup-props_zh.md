---
title: 避免 RSC Props 中的重复序列化
impact: LOW
impactDescription: 通过避免重复序列化减小网络载荷
tags: server, rsc, serialization, props, client-components
---

## 避免 RSC Props 中的重复序列化

**Impact: LOW（通过避免重复序列化减小网络载荷）**

RSC→客户端的序列化按对象引用（object reference）去重，而非按值。同一引用 = 只序列化一次；新引用 = 再次序列化。应在客户端而非服务端做变换（`.toSorted()`、`.filter()`、`.map()`）。

**错误示例（数组被重复序列化）：**

```tsx
// RSC: sends 6 strings (2 arrays × 3 items)
<ClientList usernames={usernames} usernamesOrdered={usernames.toSorted()} />
```

**正确示例（只发送 3 个字符串）：**

```tsx
// RSC: send once
<ClientList usernames={usernames} />

// Client: transform there
'use client'
const sorted = useMemo(() => [...usernames].sort(), [usernames])
```

**嵌套去重行为：**

去重会递归生效。影响因数据类型而异：

- `string[]`、`number[]`、`boolean[]`：**影响大** — 数组及全部原始值会被完整重复
- `object[]`：**影响小** — 数组结构会重复，但嵌套对象仍按引用去重

```tsx
// string[] - duplicates everything
usernames={['a','b']} sorted={usernames.toSorted()} // sends 4 strings

// object[] - duplicates array structure only
users={[{id:1},{id:2}]} sorted={users.toSorted()} // sends 2 arrays + 2 unique objects (not 4)
```

**会破坏去重的操作（会创建新引用）：**

- 数组：`.toSorted()`、`.filter()`、`.map()`、`.slice()`、`[...arr]`
- 对象：`{...obj}`、`Object.assign()`、`structuredClone()`、`JSON.parse(JSON.stringify())`

**更多示例：**

```tsx
// ❌ Bad
<C users={users} active={users.filter(u => u.active)} />
<C product={product} productName={product.name} />

// ✅ Good
<C users={users} />
<C product={product} />
// Do filtering/destructuring in client
```

**例外：** 当变换开销很大，或客户端不需要原始数据时，可以传递派生数据。
