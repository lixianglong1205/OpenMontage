---
title: 将静态 I/O 提升到模块级
impact: HIGH
impactDescription: 避免每个请求重复进行文件/网络 I/O
tags: server, io, performance, next.js, route-handlers, og-image
---

## 将静态 I/O 提升到模块级

**Impact: HIGH（避免每个请求重复进行文件/网络 I/O）**

在 Route Handler 或 Server 函数中加载静态资源（字体、Logo、图片、配置文件）时，应将 I/O 操作提升到模块级。模块级代码在模块首次被导入时执行一次，而不是在每次请求时执行。这样可以消除本会在每次调用时重复发生的文件系统读取或网络请求。

**错误：每个请求都读取字体文件**

```typescript
// app/api/og/route.tsx
import { ImageResponse } from 'next/og'

export async function GET(request: Request) {
  // Runs on EVERY request - expensive!
  const fontData = await fetch(
    new URL('./fonts/Inter.ttf', import.meta.url)
  ).then(res => res.arrayBuffer())
  
  const logoData = await fetch(
    new URL('./images/logo.png', import.meta.url)
  ).then(res => res.arrayBuffer())

  return new ImageResponse(
    <div style={{ fontFamily: 'Inter' }}>
      <img src={logoData} />
      Hello World
    </div>,
    { fonts: [{ name: 'Inter', data: fontData }] }
  )
}
```

**正确：在模块初始化时加载一次**

```typescript
// app/api/og/route.tsx
import { ImageResponse } from 'next/og'

// Module-level: runs ONCE when module is first imported
const fontData = fetch(
  new URL('./fonts/Inter.ttf', import.meta.url)
).then(res => res.arrayBuffer())

const logoData = fetch(
  new URL('./images/logo.png', import.meta.url)
).then(res => res.arrayBuffer())

export async function GET(request: Request) {
  // Await the already-started promises
  const [font, logo] = await Promise.all([fontData, logoData])

  return new ImageResponse(
    <div style={{ fontFamily: 'Inter' }}>
      <img src={logo} />
      Hello World
    </div>,
    { fonts: [{ name: 'Inter', data: font }] }
  )
}
```

**替代方案：使用 Node.js fs 同步读取文件**

```typescript
// app/api/og/route.tsx
import { ImageResponse } from 'next/og'
import { readFileSync } from 'fs'
import { join } from 'path'

// Synchronous read at module level - blocks only during module init
const fontData = readFileSync(
  join(process.cwd(), 'public/fonts/Inter.ttf')
)

const logoData = readFileSync(
  join(process.cwd(), 'public/images/logo.png')
)

export async function GET(request: Request) {
  return new ImageResponse(
    <div style={{ fontFamily: 'Inter' }}>
      <img src={logoData} />
      Hello World
    </div>,
    { fonts: [{ name: 'Inter', data: fontData }] }
  )
}
```

**通用 Node.js 示例：加载配置或模板**

```typescript
// Incorrect: reads config on every call
export async function processRequest(data: Data) {
  const config = JSON.parse(
    await fs.readFile('./config.json', 'utf-8')
  )
  const template = await fs.readFile('./template.html', 'utf-8')
  
  return render(template, data, config)
}

// Correct: loads once at module level
const configPromise = fs.readFile('./config.json', 'utf-8')
  .then(JSON.parse)
const templatePromise = fs.readFile('./template.html', 'utf-8')

export async function processRequest(data: Data) {
  const [config, template] = await Promise.all([
    configPromise,
    templatePromise
  ])
  
  return render(template, data, config)
}
```

**适用场景：**

- 为 OG 图片生成加载字体
- 加载静态 Logo、图标或水印
- 读取运行时不会变化的配置文件
- 加载邮件模板或其他静态模板
- 任意在所有请求间相同的静态资源

**不适用场景：**

- 随请求或用户变化的资源
- 运行期间可能变化的文件（应改用带 TTL 的缓存）
- 常驻内存会占用过多内存的大文件
- 不应持久保留在内存中的敏感数据

**配合 Vercel 的 [Fluid Compute](https://vercel.com/docs/fluid-compute)：** 模块级缓存在此尤其有效，因为多个并发请求会共享同一函数实例。静态资源可在多次请求间保留在内存中，且无需承担冷启动的重复加载成本。

**在传统 Serverless 中：** 每次冷启动都会重新执行模块级代码，但后续温启动会复用已加载的资源，直到实例被回收。
