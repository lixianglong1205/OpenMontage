---
title: 避免布局抖动
impact: MEDIUM
impactDescription: 防止强制同步布局并减少性能瓶颈
tags: javascript, dom, css, performance, reflow, layout-thrashing
---

## 避免布局抖动

避免在样式写入与布局读取之间交替进行。若在修改样式后又读取布局相关属性（例如 `offsetWidth`、`getBoundingClientRect()` 或 `getComputedStyle()`），浏览器会被迫触发同步 reflow。

**这样是可以的（浏览器会批量处理样式变更）：**
```typescript
function updateElementStyles(element: HTMLElement) {
  // Each line invalidates style, but browser batches the recalculation
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
}
```

**错误做法（读写交错会强制触发 reflow）：**
```typescript
function layoutThrashing(element: HTMLElement) {
  element.style.width = '100px'
  const width = element.offsetWidth  // Forces reflow
  element.style.height = '200px'
  const height = element.offsetHeight  // Forces another reflow
}
```

**正确做法（先批量写入，再统一读取）：**
```typescript
function updateElementStyles(element: HTMLElement) {
  // Batch all writes together
  element.style.width = '100px'
  element.style.height = '200px'
  element.style.backgroundColor = 'blue'
  element.style.border = '1px solid black'
  
  // Read after all writes are done (single reflow)
  const { width, height } = element.getBoundingClientRect()
}
```

**正确做法（先批量读取，再写入）：**
```typescript
function avoidThrashing(element: HTMLElement) {
  // Read phase - all layout queries first
  const rect1 = element.getBoundingClientRect()
  const offsetWidth = element.offsetWidth
  const offsetHeight = element.offsetHeight
  
  // Write phase - all style changes after
  element.style.width = '100px'
  element.style.height = '200px'
}
```

**更好：使用 CSS 类**
```css
.highlighted-box {
  width: 100px;
  height: 200px;
  background-color: blue;
  border: 1px solid black;
}
```
```typescript
function updateElementStyles(element: HTMLElement) {
  element.classList.add('highlighted-box')
  
  const { width, height } = element.getBoundingClientRect()
}
```

**React 示例：**
```tsx
// Incorrect: interleaving style changes with layout queries
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  const ref = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    if (ref.current && isHighlighted) {
      ref.current.style.width = '100px'
      const width = ref.current.offsetWidth // Forces layout
      ref.current.style.height = '200px'
    }
  }, [isHighlighted])
  
  return <div ref={ref}>Content</div>
}

// Correct: toggle class
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  return (
    <div className={isHighlighted ? 'highlighted-box' : ''}>
      Content
    </div>
  )
}
```

在可行时优先使用 CSS 类而非内联样式。CSS 文件会被浏览器缓存，类名也更利于关注点分离与维护。

更多信息请参阅 [this gist](https://gist.github.com/paulirish/5d52fb081b3570c81e3a) 与 [CSS Triggers](https://csstriggers.com/) 中关于触发布局（layout-forcing）操作的说明。
