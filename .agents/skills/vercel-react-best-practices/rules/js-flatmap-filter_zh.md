---
title: 使用 flatMap 在一次遍历中同时映射与过滤
impact: LOW-MEDIUM
impactDescription: 消除中间数组
tags: javascript, arrays, flatMap, filter, performance
---

## 使用 flatMap 在一次遍历中同时映射与过滤

**影响：低-中（消除中间数组）**

链式调用 `.map().filter(Boolean)` 会生成中间数组并遍历两次。使用 `.flatMap()` 可在单次遍历中完成转换与过滤。

**错误做法（两次遍历，存在中间数组）：**

```typescript
const userNames = users
  .map(user => user.isActive ? user.name : null)
  .filter(Boolean)
```

**正确做法（一次遍历，无中间数组）：**

```typescript
const userNames = users.flatMap(user =>
  user.isActive ? [user.name] : []
)
```

**更多示例：**

```typescript
// Extract valid emails from responses
// Before
const emails = responses
  .map(r => r.success ? r.data.email : null)
  .filter(Boolean)

// After
const emails = responses.flatMap(r =>
  r.success ? [r.data.email] : []
)

// Parse and filter valid numbers
// Before
const numbers = strings
  .map(s => parseInt(s, 10))
  .filter(n => !isNaN(n))

// After
const numbers = strings.flatMap(s => {
  const n = parseInt(s, 10)
  return isNaN(n) ? [] : [n]
})
```

**适用场景：**
- 在转换元素的同时过滤掉部分项
- 条件映射中，部分输入不产生任何输出
- 解析/校验时需要跳过无效输入
