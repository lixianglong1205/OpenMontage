---
title: 将事件处理函数存入 Ref
impact: LOW
impactDescription: 稳定的订阅
tags: advanced, hooks, refs, event-handlers, optimization
---

## 将事件处理函数存入 Ref

在 effect 中使用回调、且不希望因回调变化而重新订阅时，应把回调存入 ref。

**错误（每次渲染都会重新订阅）：**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler])
}
```

**正确（订阅保持稳定）：**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  const handlerRef = useRef(handler)
  useEffect(() => {
    handlerRef.current = handler
  }, [handler])

  useEffect(() => {
    const listener = (e) => handlerRef.current(e)
    window.addEventListener(event, listener)
    return () => window.removeEventListener(event, listener)
  }, [event])
}
```

**替代方案：若使用最新版 React，可使用 `useEffectEvent`：**

```tsx
import { useEffectEvent } from 'react'

function useWindowEvent(event: string, handler: (e) => void) {
  const onEvent = useEffectEvent(handler)

  useEffect(() => {
    window.addEventListener(event, onEvent)
    return () => window.removeEventListener(event, onEvent)
  }, [event])
}
```

`useEffectEvent` 为同一模式提供了更简洁的 API：它会创建一个稳定的函数引用，并始终调用处理函数的最新版本。
