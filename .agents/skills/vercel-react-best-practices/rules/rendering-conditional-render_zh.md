---
title: 使用显式条件渲染
impact: LOW
impactDescription: 避免渲染 0 或 NaN
tags: rendering, conditional, jsx, falsy-values
---

## 使用显式条件渲染

当条件可能是 `0`、`NaN` 或其他会在 JSX 中渲染出来的假值时，请用显式三元运算符（`? :`）做条件渲染，而不要使用 `&&`。

**错误（count 为 0 时会渲染出 "0"）：**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count && <span className="badge">{count}</span>}
    </div>
  )
}

// When count = 0, renders: <div>0</div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```

**正确（count 为 0 时不渲染任何内容）：**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count > 0 ? <span className="badge">{count}</span> : null}
    </div>
  )
}

// When count = 0, renders: <div></div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```
