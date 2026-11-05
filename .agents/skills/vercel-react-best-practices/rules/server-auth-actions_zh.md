---
title: 像 API 路由一样对 Server Actions 做身份验证
impact: CRITICAL
impactDescription: 防止未授权访问服务端变更操作
tags: server, server-actions, authentication, security, authorization
---

## 像 API 路由一样对 Server Actions 做身份验证

**Impact: CRITICAL（防止未授权访问服务端变更操作）**

Server Actions（带 `"use server"` 的函数）会像 API 路由一样作为公开端点暴露。务必在**每个** Server Action **内部**校验身份验证（authentication）与授权（authorization）——不要仅依赖中间件、布局守卫或页面级检查，因为 Server Actions 可以被直接调用。

Next.js 文档明确说明：「应以与面向公众的 API 端点相同的安全考量来对待 Server Actions，并验证用户是否被允许执行该变更。」

**错误示例（无身份验证检查）：**

```typescript
'use server'

export async function deleteUser(userId: string) {
  // Anyone can call this! No auth check
  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**正确示例（在 action 内部做身份验证）：**

```typescript
'use server'

import { verifySession } from '@/lib/auth'
import { unauthorized } from '@/lib/errors'

export async function deleteUser(userId: string) {
  // Always check auth inside the action
  const session = await verifySession()
  
  if (!session) {
    throw unauthorized('Must be logged in')
  }
  
  // Check authorization too
  if (session.user.role !== 'admin' && session.user.id !== userId) {
    throw unauthorized('Cannot delete other users')
  }
  
  await db.user.delete({ where: { id: userId } })
  return { success: true }
}
```

**配合输入校验：**

```typescript
'use server'

import { verifySession } from '@/lib/auth'
import { z } from 'zod'

const updateProfileSchema = z.object({
  userId: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email()
})

export async function updateProfile(data: unknown) {
  // Validate input first
  const validated = updateProfileSchema.parse(data)
  
  // Then authenticate
  const session = await verifySession()
  if (!session) {
    throw new Error('Unauthorized')
  }
  
  // Then authorize
  if (session.user.id !== validated.userId) {
    throw new Error('Can only update own profile')
  }
  
  // Finally perform the mutation
  await db.user.update({
    where: { id: validated.userId },
    data: {
      name: validated.name,
      email: validated.email
    }
  })
  
  return { success: true }
}
```

Reference: [https://nextjs.org/docs/app/guides/authentication](https://nextjs.org/docs/app/guides/authentication)
