---
title: React 19 API 变更
impact: MEDIUM
impactDescription: 更简洁的组件定义与 Context 用法
tags: react19, refs, context, hooks
---

## React 19 API 变更

> **⚠️ 仅适用于 React 19+。** 若你仍在使用 React 18 或更早版本，可跳过本节。

在 React 19 中，`ref` 现为普通 prop（无需 `forwardRef` 包装），且 `use()` 取代 `useContext()`。

**不正确（React 19 中的 forwardRef）：**

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

**不正确（React 19 中的 useContext）：**

```tsx
const value = useContext(MyContext)
```

**正确（用 use 替代 useContext）：**

```tsx
const value = use(MyContext)
```

`use()` 还可以条件调用，而 `useContext()` 不行。
