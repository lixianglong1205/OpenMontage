---
title: 抑制预期的 Hydration 不匹配
impact: LOW-MEDIUM
impactDescription: 避免对已知的差异产生冗长的 hydration 警告
tags: rendering, hydration, ssr, nextjs
---

## 抑制预期的 Hydration 不匹配

在 SSR 框架（例如 Next.js）中，某些值在服务端与客户端上刻意不同（随机 ID、日期、区域/时区格式化等）。对于这些*预期*的不匹配，将动态文本包在带有 `suppressHydrationWarning` 的元素中，以避免冗长的警告。不要用此属性掩盖真实 bug，也不要滥用。

**错误（已知的 mismatch 警告）：**

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
