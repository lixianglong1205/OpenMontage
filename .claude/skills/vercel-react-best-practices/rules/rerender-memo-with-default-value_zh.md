---
title: 将 memo 化组件的非原始可选参数默认值提取为常量
impact: MEDIUM
impactDescription: 通过常量作为默认值恢复 memo 化效果
tags: rerender, memo, optimization
---

## 将 memo 化组件的非原始可选参数默认值提取为常量

当 memo 化组件为某个非原始类型的可选参数（例如数组、函数或对象）设置了默认值时，若不传入该参数就调用组件，memo 化会失效。这是因为每次重新渲染都会创建新的值实例，无法在 `memo()` 中通过严格相等比较。

为解决该问题，应将默认值提取为常量。

**错误（`onClick` 在每次重新渲染时都是不同的值）：**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```

**正确（稳定的默认值）：**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```
