---
title: 使用 Activity 组件实现显示/隐藏
impact: MEDIUM
impactDescription: 保留 state/DOM
tags: rendering, activity, visibility, state-preservation
---

## 使用 Activity 组件实现显示/隐藏

对于开销较大且需要频繁切换可见性的组件，使用 React 的 `<Activity>` 来保留 state/DOM。

**用法：**

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

可避免昂贵的重新渲染和状态丢失。
