---
title: 使用 after() 实现非阻塞操作
impact: MEDIUM
impactDescription: 更快的响应时间
tags: server, async, logging, analytics, side-effects
---

## 使用 after() 实现非阻塞操作

使用 Next.js 的 `after()` 来调度应在响应发送之后执行的工作。这可避免日志、分析统计及其他副作用阻塞响应。

**错误示例（阻塞响应）：**

```tsx
import { logUserAction } from '@/app/utils'

export async function POST(request: Request) {
  // Perform mutation
  await updateDatabase(request)
  
  // Logging blocks the response
  const userAgent = request.headers.get('user-agent') || 'unknown'
  await logUserAction({ userAgent })
  
  return new Response(JSON.stringify({ status: 'success' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  })
}
```

**正确示例（非阻塞）：**

```tsx
import { after } from 'next/server'
import { headers, cookies } from 'next/headers'
import { logUserAction } from '@/app/utils'

export async function POST(request: Request) {
  // Perform mutation
  await updateDatabase(request)
  
  // Log after response is sent
  after(async () => {
    const userAgent = (await headers()).get('user-agent') || 'unknown'
    const sessionCookie = (await cookies()).get('session-id')?.value || 'anonymous'
    
    logUserAction({ sessionCookie, userAgent })
  })
  
  return new Response(JSON.stringify({ status: 'success' }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  })
}
```

响应会立即发送，而日志记录在后台进行。

**常见用例：**

- 分析统计追踪
- 审计日志
- 发送通知
- 缓存失效
- 清理任务

**重要说明：**

- 即使响应失败或发生重定向，`after()` 仍会执行
- 适用于 Server Actions、Route Handlers 和 Server Components

Reference: [https://nextjs.org/docs/app/api-reference/functions/after](https://nextjs.org/docs/app/api-reference/functions/after)
