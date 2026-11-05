---
title: 合并多次数组遍历
impact: LOW-MEDIUM
impactDescription: 减少遍历次数
tags: javascript, arrays, loops, performance
---

## 合并多次数组遍历

多次调用 `.filter()` 或 `.map()` 会对数组进行多次遍历。应合并为一次循环。

**错误（3 次遍历）：**

```typescript
const admins = users.filter(u => u.isAdmin)
const testers = users.filter(u => u.isTester)
const inactive = users.filter(u => !u.isActive)
```

**正确（1 次遍历）：**

```typescript
const admins: User[] = []
const testers: User[] = []
const inactive: User[] = []

for (const user of users) {
  if (user.isAdmin) admins.push(user)
  if (user.isTester) testers.push(user)
  if (!user.isActive) inactive.push(user)
}
```
