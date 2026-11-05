---
title: 将交互逻辑放在事件处理函数中
impact: MEDIUM
impactDescription: 避免 effect 重复运行与重复副作用
tags: rerender, useEffect, events, side-effects, dependencies
---

## 将交互逻辑放在事件处理函数中

若副作用由特定用户操作（提交、点击、拖拽）触发，应在对应的事件处理函数中执行。不要把该操作建模成 state + effect；否则会在无关变化时导致 effect 重新运行，并可能重复执行同一操作。

**错误（将事件建模为 state + effect）：**

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

**正确（在 handler 中处理）：**

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

参考：[Should this code move to an event handler?](https://react.dev/learn/removing-effect-dependencies#should-this-code-move-to-an-event-handler)
