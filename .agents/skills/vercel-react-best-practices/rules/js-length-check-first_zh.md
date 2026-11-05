---
title: 数组比较时先做长度检查
impact: MEDIUM-HIGH
impactDescription: 长度不同时可避免昂贵操作
tags: javascript, arrays, performance, optimization, comparison
---

## 数组比较时先做长度检查

当使用昂贵操作（排序、深比较、序列化）比较数组时，应先检查长度。若长度不同，数组不可能相等。

在实际应用中，当比较出现在热路径（事件处理器、渲染循环）时，这一优化尤其有价值。

**错误（总是执行昂贵比较）：**

```typescript
function hasChanges(current: string[], original: string[]) {
  // Always sorts and joins, even when lengths differ
  return current.sort().join() !== original.sort().join()
}
```

即使 `current.length` 为 5 而 `original.length` 为 100，仍会执行两次 O(n log n) 排序。此外还有将数组合并为字符串并比较字符串的开销。

**正确（先进行 O(1) 长度检查）：**

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
- 长度不同时可避免排序与合并数组的开销
- 可避免为合并后的字符串占用内存（对大数组尤其重要）
- 不会修改原始数组
- 一旦发现差异即可提前返回
