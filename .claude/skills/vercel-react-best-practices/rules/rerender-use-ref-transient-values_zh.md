---
title: 用 useRef 保存瞬时值
impact: MEDIUM
impactDescription: 避免频繁更新时不必要的重渲染
tags: rerender, useref, state, performance
---

## 用 useRef 保存瞬时值

当某个值变化很频繁，且你不希望每次更新都触发重渲染（例如鼠标跟踪、定时器、临时标志位）时，用 `useRef` 存储它，而不是 `useState`。组件 state 留给 UI；与 DOM 紧邻的临时值用 ref。更新 ref 不会触发重渲染。

**错误（每次更新都会重渲染）：**

```tsx
function Tracker() {
  const [lastX, setLastX] = useState(0)

  useEffect(() => {
    const onMove = (e: MouseEvent) => setLastX(e.clientX)
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: lastX,
        width: 8,
        height: 8,
        background: 'black',
      }}
    />
  )
}
```

**正确（跟踪时不触发重渲染）：**

```tsx
function Tracker() {
  const lastXRef = useRef(0)
  const dotRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      lastXRef.current = e.clientX
      const node = dotRef.current
      if (node) {
        node.style.transform = `translateX(${e.clientX}px)`
      }
    }
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div
      ref={dotRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: 8,
        height: 8,
        background: 'black',
        transform: 'translateX(0px)',
      }}
    />
  )
}
```
