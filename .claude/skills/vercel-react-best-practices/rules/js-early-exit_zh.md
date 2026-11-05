---
title: 函数中的提前返回
impact: LOW-MEDIUM
impactDescription: 避免不必要的计算
tags: javascript, functions, optimization, early-return
---

## 函数中的提前返回

一旦结果已经确定，就提前返回，以跳过不必要的处理。

**错误做法（即使已找到答案仍处理全部项）：**

```typescript
function validateUsers(users: User[]) {
  let hasError = false
  let errorMessage = ''
  
  for (const user of users) {
    if (!user.email) {
      hasError = true
      errorMessage = 'Email required'
    }
    if (!user.name) {
      hasError = true
      errorMessage = 'Name required'
    }
    // Continues checking all users even after error found
  }
  
  return hasError ? { valid: false, error: errorMessage } : { valid: true }
}
```

**正确做法（遇到第一个错误立即返回）：**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) {
      return { valid: false, error: 'Email required' }
    }
    if (!user.name) {
      return { valid: false, error: 'Name required' }
    }
  }

  return { valid: true }
}
```
