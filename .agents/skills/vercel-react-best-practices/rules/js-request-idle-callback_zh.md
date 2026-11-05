---
title: 使用 requestIdleCallback 推迟非关键工作
impact: MEDIUM
impactDescription: 在后台任务期间保持 UI 响应
tags: javascript, performance, idle, scheduling, analytics
---

## 使用 requestIdleCallback 推迟非关键工作

**Impact: MEDIUM（在后台任务期间保持 UI 响应）**

使用 `requestIdleCallback()` 在浏览器空闲时段调度非关键工作。这样主线程可以优先处理用户交互与动画，减少卡顿并提升感知性能。

**错误做法（在用户交互期间阻塞主线程）：**

```typescript
function handleSearch(query: string) {
  const results = searchItems(query)
  setResults(results)

  // These block the main thread immediately
  analytics.track('search', { query })
  saveToRecentSearches(query)
  prefetchTopResults(results.slice(0, 3))
}
```

**正确做法（将非关键工作推迟到空闲时段）：**

```typescript
function handleSearch(query: string) {
  const results = searchItems(query)
  setResults(results)

  // Defer non-critical work to idle periods
  requestIdleCallback(() => {
    analytics.track('search', { query })
  })

  requestIdleCallback(() => {
    saveToRecentSearches(query)
  })

  requestIdleCallback(() => {
    prefetchTopResults(results.slice(0, 3))
  })
}
```

**为必须完成的工作设置 timeout：**

```typescript
// Ensure analytics fires within 2 seconds even if browser stays busy
requestIdleCallback(
  () => analytics.track('page_view', { path: location.pathname }),
  { timeout: 2000 }
)
```

**分块处理大型任务：**

```typescript
function processLargeDataset(items: Item[]) {
  let index = 0

  function processChunk(deadline: IdleDeadline) {
    // Process items while we have idle time (aim for <50ms chunks)
    while (index < items.length && deadline.timeRemaining() > 0) {
      processItem(items[index])
      index++
    }

    // Schedule next chunk if more items remain
    if (index < items.length) {
      requestIdleCallback(processChunk)
    }
  }

  requestIdleCallback(processChunk)
}
```

**不支持该 API 的浏览器降级方案：**

```typescript
const scheduleIdleWork = window.requestIdleCallback ?? ((cb: () => void) => setTimeout(cb, 1))

scheduleIdleWork(() => {
  // Non-critical work
})
```

**适用场景：**

- 分析与遥测
- 将状态保存到 localStorage/IndexedDB
- 为可能的下一步操作预取资源
- 处理非紧急的数据转换
- 非关键功能的懒初始化

**不适用场景：**

- 需要即时反馈的用户发起操作
- 用户正在等待的渲染更新
- 时间敏感的操作
