---
title: 对非紧急更新使用 Transitions
impact: MEDIUM
impactDescription: 保持 UI 响应性
tags: rerender, transitions, startTransition, performance
---

## 对非紧急更新使用 Transitions

将频繁、非紧急的状态更新标记为 transition（过渡），以保持 UI 响应性。

**错误示例（每次滚动都会阻塞 UI）：**

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => setScrollY(window.scrollY)
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```

**正确示例（非阻塞更新）：**

```tsx
import { startTransition } from 'react'

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => {
      startTransition(() => setScrollY(window.scrollY))
    }
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```
