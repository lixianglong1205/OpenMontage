---
title: 基于用户意图的预加载
impact: MEDIUM
impactDescription: 降低感知延迟
tags: bundle, preload, user-intent, hover
---

## 基于用户意图的预加载

在实际需要之前预加载体积较大的 bundle，以降低感知延迟。

**示例（悬停/聚焦时预加载）：**

```tsx
function EditorButton({ onClick }: { onClick: () => void }) {
  const preload = () => {
    if (typeof window !== 'undefined') {
      void import('./monaco-editor')
    }
  }

  return (
    <button
      onMouseEnter={preload}
      onFocus={preload}
      onClick={onClick}
    >
      Open Editor
    </button>
  )
}
```

**示例（功能开关启用时预加载）：**

```tsx
function FlagsProvider({ children, flags }: Props) {
  useEffect(() => {
    if (flags.editorEnabled && typeof window !== 'undefined') {
      void import('./monaco-editor').then(mod => mod.init())
    }
  }, [flags.editorEnabled])

  return <FlagsContext.Provider value={flags}>
    {children}
  </FlagsContext.Provider>
}
```

通过 `typeof window !== 'undefined'` 检查可避免将预加载模块打入 SSR bundle，从而优化服务端 bundle 体积与构建速度。
