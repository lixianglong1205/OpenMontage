---
title: 不要在组件内部定义组件
impact: HIGH
impactDescription: 避免每次渲染都 remount
tags: rerender, components, remount, performance
---

## 不要在组件内部定义组件

**影响：HIGH（避免每次渲染都 remount）**

在另一个组件内部定义组件时，每次渲染都会创建新的组件类型。React 每次都会把它当作不同的组件，从而完整 remount，销毁全部 state 与 DOM。

开发者常这样做是为了访问父组件变量而不传 props。应始终改为通过 props 传递。

**错误（每次渲染都会 remount）：**

```tsx
function UserProfile({ user, theme }) {
  // Defined inside to access `theme` - BAD
  const Avatar = () => (
    <img
      src={user.avatarUrl}
      className={theme === 'dark' ? 'avatar-dark' : 'avatar-light'}
    />
  )

  // Defined inside to access `user` - BAD
  const Stats = () => (
    <div>
      <span>{user.followers} followers</span>
      <span>{user.posts} posts</span>
    </div>
  )

  return (
    <div>
      <Avatar />
      <Stats />
    </div>
  )
}
```

每次 `UserProfile` 渲染时，`Avatar` 和 `Stats` 都是新的组件类型。React 会卸载旧实例并挂载新实例，丢失内部 state、重新运行 effect，并重建 DOM 节点。

**正确（改为传递 props）：**

```tsx
function Avatar({ src, theme }: { src: string; theme: string }) {
  return (
    <img
      src={src}
      className={theme === 'dark' ? 'avatar-dark' : 'avatar-light'}
    />
  )
}

function Stats({ followers, posts }: { followers: number; posts: number }) {
  return (
    <div>
      <span>{followers} followers</span>
      <span>{posts} posts</span>
    </div>
  )
}

function UserProfile({ user, theme }) {
  return (
    <div>
      <Avatar src={user.avatarUrl} theme={theme} />
      <Stats followers={user.followers} posts={user.posts} />
    </div>
  )
}
```

**此问题的典型表现：**
- 输入框在每次按键后失去焦点
- 动画意外重新开始
- 父组件每次渲染都会执行 `useEffect` 的 cleanup/setup
- 组件内部滚动位置被重置

