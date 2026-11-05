---
title: 使用 Set/Map 实现 O(1) 查找
impact: LOW-MEDIUM
impactDescription: O(n) 到 O(1)
tags: javascript, set, map, data-structures, performance
---

## 使用 Set/Map 实现 O(1) 查找

将数组转换为 Set/Map，以便在重复进行成员检查时使用 O(1) 查找。

**错误做法（每次检查 O(n)）：**

```typescript
const allowedIds = ['a', 'b', 'c', ...]
items.filter(item => allowedIds.includes(item.id))
```

**正确做法（每次检查 O(1)）：**

```typescript
const allowedIds = new Set(['a', 'b', 'c', ...])
items.filter(item => allowedIds.has(item.id))
```
