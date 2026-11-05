---
title: 数组比较时优先检查长度
impact: MEDIUM-HIGH
impactDescription: 长度不同时避免昂贵操作
tags: javascript, arrays, performance, optimization, comparison
---

## 数组比较时优先检查长度

在比较数组且需要执行昂贵操作（排序、深相等、序列化）时，应先检查长度。若长度不同，两个数组不可能相等。

在实际应用中，当比较发生在热路径（事件处理器、渲染循环）上时，这一优化尤其有价值。

**错误做法（总是执行昂贵的比较）：**

```typescript
function hasChanges(current: string[], original: string[]) {
  // Always sorts and joins, even when lengths differ
  return current.sort().join() !== original.sort().join()
}
```

即使 `current.length` 为 5 而 `original.length` 为 100，仍会执行两次 O(n log n) 的排序。此外还有拼接数组与比较字符串的开销。

**正确做法（先做 O(1) 长度检查）：**

```typescript
function hasChanges(current: string[], original: string[]) {
  // Early return if lengths differ
  if (current.length !== original.length) {
    return true
  }
  // Only sort when lengths match
  const currentSorted = current.toSorted()
  const originalSorted = original.toSorted()
  for (let i = 0; i < currentSorted.length; i++) {
    if (currentSorted[i] !== originalSorted[i]) {
      return true
    }
  }
  return false
}
```

新做法更高效，因为：

- 长度不同时，避免排序与拼接数组的开销
- 避免为拼接字符串占用内存（对大数组尤其重要）
- 避免修改原数组
- 发现差异时可提前返回
