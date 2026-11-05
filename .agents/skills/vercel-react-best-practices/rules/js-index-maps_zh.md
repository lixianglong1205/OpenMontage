---
title: 为重复查找构建索引 Map
impact: LOW-MEDIUM
impactDescription: 100 万次运算降至 2000 次
tags: javascript, map, indexing, optimization, performance
---

## 为重复查找构建索引 Map

按相同键多次调用 `.find()` 时，应改用 Map。

**错误（每次查找 O(n)）：**

```typescript
function processOrders(orders: Order[], users: User[]) {
  return orders.map(order => ({
    ...order,
    user: users.find(u => u.id === order.userId)
  }))
}
```

**正确（每次查找 O(1)）：**

```typescript
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map(u => [u.id, u]))

  return orders.map(order => ({
    ...order,
    user: userById.get(order.userId)
  }))
}
```

先构建一次 map（O(n)），之后每次查找均为 O(1)。
1000 个订单 × 1000 个用户：100 万次运算 → 2000 次。
