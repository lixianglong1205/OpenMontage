---
title: 抑制预期的 Hydration 不匹配
impact: LOW-MEDIUM
impactDescription: 避免因已知差异产生嘈杂的 hydration 警告
tags: rendering, hydration, ssr, nextjs
---

## 抑制预期的 Hydration 不匹配

在 SSR 框架（例如 Next.js）中，某些值在服务端与客户端之间刻意存在差异（随机 ID、日期、区域设置/时区格式化）。对于这些*预期*的不匹配，将动态文本包裹在带有 `suppressHydrationWarning` 的元素中，以避免产生大量警告。不要用此方式掩盖真实 bug。不要滥用。

**错误（已知的不匹配警告）：**

```tsx
function Timestamp() {
  return <span>{new Date().toLocaleString()}</span>
}
```

**正确（仅抑制预期的不匹配）：**

```tsx
function Timestamp() {
  return (
    <span suppressHydrationWarning>
      {new Date().toLocaleString()}
    </span>
  )
}
```
