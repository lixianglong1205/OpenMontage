---
title: 避免水合不匹配且消除闪烁
impact: MEDIUM
impactDescription: 避免视觉闪烁与水合错误
tags: rendering, ssr, hydration, localStorage, flicker
---

## 避免水合不匹配且消除闪烁

当渲染内容依赖客户端存储（localStorage、cookies）时，可通过注入在 React 水合（hydration）之前同步更新 DOM 的脚本，同时避免 SSR 崩溃与水合后的闪烁。

**错误（会破坏 SSR）：**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  // localStorage is not available on server - throws error
  const theme = localStorage.getItem('theme') || 'light'
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

服务端渲染会失败，因为 `localStorage` 在服务端为 undefined。

**错误（视觉闪烁）：**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState('light')
  
  useEffect(() => {
    // Runs after hydration - causes visible flash
    const stored = localStorage.getItem('theme')
    if (stored) {
      setTheme(stored)
    }
  }, [])
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

组件会先用默认值（`light`）渲染，水合后再更新，导致错误内容短暂闪现。

**正确（无闪烁、无水合不匹配）：**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  return (
    <>
      <div id="theme-wrapper">
        {children}
      </div>
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              try {
                var theme = localStorage.getItem('theme') || 'light';
                var el = document.getElementById('theme-wrapper');
                if (el) el.className = theme;
              } catch (e) {}
            })();
          `,
        }}
      />
    </>
  )
}
```

内联脚本在元素展示前同步执行，确保 DOM 已具备正确值。无闪烁，无水合不匹配。

该模式尤其适用于主题切换、用户偏好、认证状态，以及任何应在不闪现默认值的情况下立即呈现的仅客户端数据。
