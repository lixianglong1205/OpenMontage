---
title: 将交互逻辑放在事件处理函数中
impact: MEDIUM
impactDescription: 避免因 effect 重复执行与副作用重复触发
tags: rerender, useEffect, events, side-effects, dependencies
---

## 将交互逻辑放在事件处理函数中

若副作用由特定用户操作（提交、点击、拖拽）触发，应在对应的事件处理函数中执行。不要用「状态 + effect」来建模该操作；否则 effect 会在无关变化时重复运行，并可能重复执行同一操作。

**错误（用 state + effect 建模事件）：**

```tsx
function Form() {
  const [submitted, setSubmitted] = useState(false)
  const theme = useContext(ThemeContext)

  useEffect(() => {
    if (submitted) {
      post('/api/register')
      showToast('Registered', theme)
    }
  }, [submitted, theme])

  return <button onClick={() => setSubmitted(true)}>Submit</button>
}
```

**正确（在 handler 中直接处理）：**

```tsx
function Form() {
  const theme = useContext(ThemeContext)

  function handleSubmit() {
    post('/api/register')
    showToast('Registered', theme)
  }

  return <button onClick={handleSubmit}>Submit</button>
}
```

Reference: [这段代码是否应移到事件处理函数中？](https://react.dev/learn/removing-effect-dependencies#should-this-code-move-to-an-event-handler)
