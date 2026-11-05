---
title: 避免水合不匹配且消除闪烁
impact: MEDIUM
impactDescription: 避免视觉闪烁与水合错误
tags: rendering, ssr, hydration, localStorage, flicker
---

## 避免水合不匹配且消除闪烁

当渲染内容依赖客户端存储（localStorage、cookies）时，通过注入在 React 水合（hydration）之前同步更新 DOM 的脚本，可同时避免 SSR 崩溃与水合后的闪烁。

**不正确（会破坏 SSR）：**

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

**不正确（视觉闪烁）：**

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

组件先以默认值（`light`）渲染，水合后再更新，导致错误内容短暂可见的闪烁。

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

内联脚本在元素展示前同步执行，确保 DOM 已是正确值。无闪烁，无水合不匹配。

该模式尤其适用于主题切换、用户偏好、认证状态，以及任何应在首屏立即呈现、且不应先闪一下默认值的纯客户端数据。
