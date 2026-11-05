---
title: 将 memo 组件的非原始类型默认参数提取为常量
impact: MEDIUM
impactDescription: 通过为默认值使用常量来恢复 memo 化效果
tags: rerender, memo, optimization
---

## 将 memo 组件的非原始类型默认参数提取为常量

当 memo 化的组件为某个非原始类型的可选参数（例如数组、函数或对象）设置了默认值时，在不传入该参数的情况下调用组件会导致 memo 化失效。这是因为每次重渲染都会创建新的值实例，无法在 `memo()` 的严格相等比较中通过。

为解决该问题，应将默认值提取为常量。

**错误示例（`onClick` 在每次重渲染时都是不同的值）：**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```

**正确示例（稳定的默认值）：**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```
