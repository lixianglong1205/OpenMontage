---
title: 对瞬态值使用 useRef
impact: MEDIUM
impactDescription: 避免频繁更新时不必要的重渲染
tags: rerender, useref, state, performance
---

## 对瞬态值使用 useRef

当某个值变化很频繁，且你不希望每次更新都触发重渲染（例如鼠标跟踪、定时器、瞬态标志）时，用 `useRef` 存储它，而不是 `useState`。组件 state 留给 UI；与 DOM 相邻的临时值用 ref。更新 ref 不会触发重渲染。

**错误示例（每次更新都会渲染）：**

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

**正确示例（跟踪时不触发重渲染）：**

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
