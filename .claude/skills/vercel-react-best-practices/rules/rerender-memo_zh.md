---
title: 提取为 Memo 化组件
impact: MEDIUM
impactDescription: 便于提前 return
tags: rerender, memo, useMemo, optimization
---

## 提取为 Memo 化组件

将耗时工作提取到 memo 化组件中，以便在计算之前提前 return。

**错误（loading 时仍会计算 avatar）：**

```tsx
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => {
    const id = computeAvatarId(user)
    return <Avatar id={id} />
  }, [user])

  if (loading) return <Skeleton />
  return <div>{avatar}</div>
}
```

**正确（loading 时跳过计算）：**

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user])
  return <Avatar id={id} />
})

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return (
    <div>
      <UserAvatar user={user} />
    </div>
  )
}
```

**注意：** 若项目已启用 [React Compiler](https://react.dev/learn/react-compiler)，则无需手动使用 `memo()` 和 `useMemo()` 做 memo 化。编译器会自动优化重渲染。
