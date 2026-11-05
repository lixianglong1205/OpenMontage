---
title: 使用 Passive 事件监听器提升滚动性能
impact: MEDIUM
impactDescription: 消除由事件监听器引起的滚动延迟
tags: client, event-listeners, scrolling, performance, touch, wheel
---

## 使用 Passive 事件监听器提升滚动性能

为 touch 与 wheel 事件监听器添加 `{ passive: true }`，以启用即时滚动。浏览器通常会等待监听器执行完毕，以检查是否调用了 `preventDefault()`，从而造成滚动延迟。

**不正确：**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX)
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY)
  
  document.addEventListener('touchstart', handleTouch)
  document.addEventListener('wheel', handleWheel)
  
  return () => {
    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('wheel', handleWheel)
  }
}, [])
```

**正确：**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX)
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY)
  
  document.addEventListener('touchstart', handleTouch, { passive: true })
  document.addEventListener('wheel', handleWheel, { passive: true })
  
  return () => {
    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('wheel', handleWheel)
  }
}, [])
```

**在以下情况使用 passive：** 埋点/分析、日志，以及任何不会调用 `preventDefault()` 的监听器。

**在以下情况不要使用 passive：** 实现自定义滑动手势、自定义缩放控件，或任何需要 `preventDefault()` 的监听器。
