---
title: 不要用 useMemo 包裹结果为原始类型的简单表达式
impact: LOW-MEDIUM
impactDescription: 每次渲染都会浪费计算
tags: rerender, useMemo, optimization
---

## 不要用 useMemo 包裹结果为原始类型的简单表达式

当表达式很简单（逻辑或算术运算符很少），且结果为原始类型（boolean、number、string）时，不要用 `useMemo` 包裹。
调用 `useMemo` 并比较 Hook 依赖项的开销，可能大于表达式本身的计算。

**错误：**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = useMemo(() => {
    return user.isLoading || notifications.isLoading
  }, [user.isLoading, notifications.isLoading])

  if (isLoading) return <Skeleton />
  // return some markup
}
```

**正确：**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = user.isLoading || notifications.isLoading

  if (isLoading) return <Skeleton />
  // return some markup
}
```

