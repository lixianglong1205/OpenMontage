---
title: 战略性 Suspense 边界
impact: HIGH
impactDescription: 更快的首屏绘制
tags: async, suspense, streaming, layout-shift
---

## 战略性 Suspense 边界

不要在异步组件里先 `await` 数据再返回 JSX，而应使用 Suspense 边界，在数据加载的同时更快展示外层 UI。

**错误做法（外层 UI 被数据获取阻塞）：**

```tsx
async function Page() {
  const data = await fetchData() // Blocks entire page
  
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <DataDisplay data={data} />
      </div>
      <div>Footer</div>
    </div>
  )
}
```

整个布局都在等数据，尽管只有中间区域需要它。

**正确做法（外层立即展示，数据流式到达）：**

```tsx
function Page() {
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <Suspense fallback={<Skeleton />}>
          <DataDisplay />
        </Suspense>
      </div>
      <div>Footer</div>
    </div>
  )
}

async function DataDisplay() {
  const data = await fetchData() // Only blocks this component
  return <div>{data.content}</div>
}
```

Sidebar、Header 和 Footer 会立即渲染，只有 DataDisplay 等待数据。

**替代方案（在多个组件间共享 promise）：**

```tsx
function Page() {
  // Start fetch immediately, but don't await
  const dataPromise = fetchData()
  
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <Suspense fallback={<Skeleton />}>
        <DataDisplay dataPromise={dataPromise} />
        <DataSummary dataPromise={dataPromise} />
      </Suspense>
      <div>Footer</div>
    </div>
  )
}

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // Unwraps the promise
  return <div>{data.content}</div>
}

function DataSummary({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // Reuses the same promise
  return <div>{data.summary}</div>
}
```

两个组件共享同一个 promise，因此只会发起一次请求。布局立即渲染，两个子组件一起等待。

**不宜使用此模式的场景：**

- 布局决策依赖关键数据（影响定位）
- 首屏 SEO 关键内容
- 查询很快、Suspense 开销不划算
- 希望避免布局偏移（加载中 → 内容跳动）

**权衡：** 更快的首屏绘制 vs 可能的布局偏移。请根据 UX 优先级选择。
