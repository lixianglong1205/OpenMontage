---
title: 在 Script 标签上使用 defer 或 async
impact: HIGH
impactDescription: 消除阻塞渲染
tags: rendering, script, defer, async, performance
---

## 在 Script 标签上使用 defer 或 async

**影响：高（消除阻塞渲染）**

未设置 `defer` 或 `async` 的 script 标签会在脚本下载并执行期间阻塞 HTML 解析，从而延迟首次内容绘制（First Contentful Paint）和可交互时间（Time to Interactive）。

- **`defer`**：并行下载，在 HTML 解析完成后执行，保持脚本执行顺序
- **`async`**：并行下载，就绪后立即执行，不保证执行顺序

依赖 DOM 或其他脚本的脚本应使用 `defer`；分析统计等独立脚本应使用 `async`。

**错误示例（阻塞渲染）：**

```tsx
export default function Document() {
  return (
    <html>
      <head>
        <script src="https://example.com/analytics.js" />
        <script src="/scripts/utils.js" />
      </head>
      <body>{/* content */}</body>
    </html>
  )
}
```

**正确示例（非阻塞）：**

```tsx
export default function Document() {
  return (
    <html>
      <head>
        {/* Independent script - use async */}
        <script src="https://example.com/analytics.js" async />
        {/* DOM-dependent script - use defer */}
        <script src="/scripts/utils.js" defer />
      </head>
      <body>{/* content */}</body>
    </html>
  )
}
```

**注意：** 在 Next.js 中，应优先使用带 `strategy` 属性的 `next/script` 组件，而不是原生 script 标签：

```tsx
import Script from 'next/script'

export default function Page() {
  return (
    <>
      <Script src="https://example.com/analytics.js" strategy="afterInteractive" />
      <Script src="/scripts/utils.js" strategy="beforeInteractive" />
    </>
  )
}
```

Reference: [MDN - Script element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#defer)

