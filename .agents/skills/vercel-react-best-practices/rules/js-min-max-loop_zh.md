---
title: 用循环求最小/最大值，而非排序
impact: LOW
impactDescription: O(n) 而非 O(n log n)
tags: javascript, arrays, performance, sorting, algorithms
---

## 用循环求最小/最大值，而非排序

查找最小或最大元素只需对数组遍历一次。排序既浪费又更慢。

**错误示例（O(n log n)——排序以找最新项）：**

```typescript
interface Project {
  id: string
  name: string
  updatedAt: number
}

function getLatestProject(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => b.updatedAt - a.updatedAt)
  return sorted[0]
}
```

为了找最大值而对整个数组排序。

**错误示例（O(n log n)——排序求最旧与最新）：**

```typescript
function getOldestAndNewest(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => a.updatedAt - b.updatedAt)
  return { oldest: sorted[0], newest: sorted[sorted.length - 1] }
}
```

仅需最小/最大值时仍然做了不必要的排序。

**正确示例（O(n)——单次循环）：**

```typescript
function getLatestProject(projects: Project[]) {
  if (projects.length === 0) return null
  
  let latest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt > latest.updatedAt) {
      latest = projects[i]
    }
  }
  
  return latest
}

function getOldestAndNewest(projects: Project[]) {
  if (projects.length === 0) return { oldest: null, newest: null }
  
  let oldest = projects[0]
  let newest = projects[0]
  
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt < oldest.updatedAt) oldest = projects[i]
    if (projects[i].updatedAt > newest.updatedAt) newest = projects[i]
  }
  
  return { oldest, newest }
}
```

单次遍历数组，无需复制，无需排序。

**替代方案（小数组可用 Math.min/Math.max）：**

```typescript
const numbers = [5, 2, 8, 1, 9]
const min = Math.min(...numbers)
const max = Math.max(...numbers)
```

对小数组可用，但由于展开运算符（spread operator）的限制，在超大数组上可能更慢或直接报错。在 Chrome 143 中数组长度上限约为 124000，Safari 18 中约为 638000；精确数值可能有所不同——参见 [the fiddle](https://jsfiddle.net/qw1jabsx/4/)。为稳妥起见请用循环方案。
