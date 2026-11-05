---
title: 用循环求最小/最大值，而非排序
impact: LOW
impactDescription: O(n) 而非 O(n log n)
tags: javascript, arrays, performance, sorting, algorithms
---

## 用循环求最小/最大值，而非排序

求数组中的最小或最大元素只需遍历一次。排序既浪费又更慢。

**错误做法（O(n log n)——排序只为找最新项）：**

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

仅为求最大值就对整个数组排序。

**错误做法（O(n log n)——排序求最旧与最新）：**

```typescript
function getOldestAndNewest(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => a.updatedAt - b.updatedAt)
  return { oldest: sorted[0], newest: sorted[sorted.length - 1] }
}
```

仅需 min/max 时仍不必要地排序。

**正确做法（O(n)——单次循环）：**

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

对小数组可行，但数组很大时可能更慢，或因展开运算符（spread operator）限制而直接抛错。Chrome 143 中数组长度上限约为 124000，Safari 18 约为 638000；具体数值可能因环境而异——参见 [the fiddle](https://jsfiddle.net/qw1jabsx/4/)。需要可靠行为时请用循环写法。
