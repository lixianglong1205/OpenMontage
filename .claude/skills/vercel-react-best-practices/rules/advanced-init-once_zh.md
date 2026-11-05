---
title: 应用只初始化一次，而非每次挂载
impact: LOW-MEDIUM
impactDescription: 避免在开发环境中重复初始化
tags: initialization, useEffect, app-startup, side-effects
---

## 应用只初始化一次，而非每次挂载

不要把必须在每次应用加载时只运行一次的全局初始化逻辑放在组件的 `useEffect([])` 里。组件可能重新挂载，effect 也会再次执行。应改用模块级守卫，或在入口模块顶层完成初始化。

**错误（开发环境会执行两次，重新挂载时会再次运行）：**

```tsx
function Comp() {
  useEffect(() => {
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

**正确（每次应用加载只执行一次）：**

```tsx
let didInit = false

function Comp() {
  useEffect(() => {
    if (didInit) return
    didInit = true
    loadFromStorage()
    checkAuthToken()
  }, [])

  // ...
}
```

参考：[初始化应用](https://react.dev/learn/you-might-not-need-an-effect#initializing-the-application)
