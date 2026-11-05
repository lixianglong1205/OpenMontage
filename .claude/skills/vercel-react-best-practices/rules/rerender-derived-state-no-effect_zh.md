---
title: 在渲染期间计算派生状态
impact: MEDIUM
impactDescription: 避免多余渲染与状态漂移
tags: rerender, derived-state, useEffect, state
---

## 在渲染期间计算派生状态

若某值可由当前的 props/state 计算得出，就不要把它存进 state，也不要在 effect 里更新它。在渲染期间直接派生，可避免额外渲染和状态漂移。不要仅为响应 prop 变化而在 effect 里 setState；优先使用派生值或通过 key 重置组件。

**错误（冗余 state 与 effect）：**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const [fullName, setFullName] = useState('')

  useEffect(() => {
    setFullName(firstName + ' ' + lastName)
  }, [firstName, lastName])

  return <p>{fullName}</p>
}
```

**正确（在渲染期间派生）：**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const fullName = firstName + ' ' + lastName

  return <p>{fullName}</p>
}
```

参考：[You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
