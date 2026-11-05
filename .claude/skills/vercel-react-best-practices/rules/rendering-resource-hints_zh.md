---
title: 使用 React DOM 资源提示
impact: HIGH
impactDescription: 缩短关键资源的加载时间
tags: rendering, preload, preconnect, prefetch, resource-hints
---

## 使用 React DOM 资源提示

**影响：高（缩短关键资源的加载时间）**

React DOM 提供若干 API，用于向浏览器提示即将需要的资源。在服务端组件中尤其有用——可以在客户端收到 HTML 之前就开始加载资源。

- **`prefetchDNS(href)`**：为预期会连接的域名解析 DNS
- **`preconnect(href)`**：与服务器建立连接（DNS + TCP + TLS）
- **`preload(href, options)`**：预取即将使用的资源（样式表、字体、脚本、图片）
- **`preloadModule(href)`**：预取即将使用的 ES 模块
- **`preinit(href, options)`**：预取并执行样式表或脚本
- **`preinitModule(href)`**：预取并执行 ES 模块

**示例（预连接第三方 API）：**

```tsx
import { preconnect, prefetchDNS } from 'react-dom'

export default function App() {
  prefetchDNS('https://analytics.example.com')
  preconnect('https://api.example.com')

  return <main>{/* content */}</main>
}
```

**示例（预加载关键字体与样式）：**

```tsx
import { preload, preinit } from 'react-dom'

export default function RootLayout({ children }) {
  // Preload font file
  preload('/fonts/inter.woff2', { as: 'font', type: 'font/woff2', crossOrigin: 'anonymous' })

  // Fetch and apply critical stylesheet immediately
  preinit('/styles/critical.css', { as: 'style' })

  return (
    <html>
      <body>{children}</body>
    </html>
  )
}
```

**示例（为代码分割路由预加载模块）：**

```tsx
import { preloadModule, preinitModule } from 'react-dom'

function Navigation() {
  const preloadDashboard = () => {
    preloadModule('/dashboard.js', { as: 'script' })
  }

  return (
    <nav>
      <a href="/dashboard" onMouseEnter={preloadDashboard}>
        Dashboard
      </a>
    </nav>
  )
}
```

**各 API 适用场景：**

| API | 适用场景 |
|-----|----------|
| `prefetchDNS` | 稍后才会连接的第三方域名 |
| `preconnect` | 会立即请求数据的 API 或 CDN |
| `preload` | 当前页面所需的关键资源 |
| `preloadModule` | 用户可能即将导航到的 JS 模块 |
| `preinit` | 需要尽早执行的样式表/脚本 |
| `preinitModule` | 需要尽早执行的 ES 模块 |

Reference: [React DOM Resource Preloading APIs](https://react.dev/reference/react-dom#resource-preloading-apis)
