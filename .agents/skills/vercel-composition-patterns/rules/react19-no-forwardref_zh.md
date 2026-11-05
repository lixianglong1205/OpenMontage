---
title: React 19 API 变更
impact: MEDIUM
impactDescription: 更简洁的组件定义与 Context 用法
tags: react19, refs, context, hooks
---

## React 19 API 变更

> **⚠️ 仅适用于 React 19+。** 若你仍在使用 React 18 或更早版本，可跳过本节。

在 React 19 中，`ref` 已成为普通 prop（无需 `forwardRef` 包装），且 `use()` 取代了 `useContext()`。

**错误（React 19 中仍使用 forwardRef）：**

```tsx
const ComposerInput = forwardRef<TextInput, Props>((props, ref) => {
  return <TextInput ref={ref} {...props} />
})
```

**正确（ref 作为普通 prop）：**

```tsx
function ComposerInput({ ref, ...props }: Props & { ref?: React.Ref<TextInput> }) {
  return <TextInput ref={ref} {...props} />
}
```

**错误（React 19 中仍使用 useContext）：**

```tsx
const value = useContext(MyContext)
```

**正确（用 use 替代 useContext）：**

```tsx
const value = use(MyContext)
```

与 `useContext()` 不同，`use()` 也可以在条件分支中调用。
