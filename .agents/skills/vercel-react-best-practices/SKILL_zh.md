---
name: vercel-react-best-practices
description: 来自 Vercel Engineering 的 React 与 Next.js 性能优化指南。在编写、审查或重构 React/Next.js 代码时应使用本技能，以确保采用最优性能模式。适用于涉及 React 组件、Next.js 页面、数据获取、打包优化或性能改进的任务。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React 最佳实践

由 Vercel 维护的 React 与 Next.js 应用综合性能优化指南。涵盖 8 大类共 65 条规则，按影响优先级排序，用于指导自动化重构与代码生成。

> **扩展参考：** 本目录下的 [`AGENTS.md`](AGENTS.md) 是上游完整长文指南（自 Vercel 引入）。它仅作为本技能的补充参考——`SKILL.md` 是可加载的入口与权威说明。它不会覆盖或扩展仓库根目录的 `AGENTS.md` / `AGENT_GUIDE.md`。

## 何时适用

在以下场景参考本指南：

- 编写新的 React 组件或 Next.js 页面
- 实现数据获取（客户端或服务端）
- 审查代码中的性能问题
- 重构现有 React/Next.js 代码
- 优化打包体积或加载时间

## 按优先级划分的规则类别

| 优先级 | 类别 | 影响 | 前缀 |
|----------|----------|--------|--------|
| 1 | 消除瀑布流（Eliminating Waterfalls） | CRITICAL | `async-` |
| 2 | 打包体积优化（Bundle Size Optimization） | CRITICAL | `bundle-` |
| 3 | 服务端性能（Server-Side Performance） | HIGH | `server-` |
| 4 | 客户端数据获取（Client-Side Data Fetching） | MEDIUM-HIGH | `client-` |
| 5 | 重渲染优化（Re-render Optimization） | MEDIUM | `rerender-` |
| 6 | 渲染性能（Rendering Performance） | MEDIUM | `rendering-` |
| 7 | JavaScript 性能（JavaScript Performance） | LOW-MEDIUM | `js-` |
| 8 | 高级模式（Advanced Patterns） | LOW | `advanced-` |

## 快速参考

### 1. 消除瀑布流（CRITICAL）

- `async-defer-await` - 将 await 移到实际使用的分支中
- `async-parallel` - 对独立操作使用 Promise.all()
- `async-dependencies` - 对部分依赖使用 better-all
- `async-api-routes` - 在 API 路由中尽早启动 Promise，延后 await
- `async-suspense-boundaries` - 使用 Suspense 流式输出内容

### 2. 打包体积优化（CRITICAL）

- `bundle-barrel-imports` - 直接导入，避免 barrel 文件
- `bundle-dynamic-imports` - 对重型组件使用 next/dynamic
- `bundle-defer-third-party` - 在水合后再加载 analytics/日志
- `bundle-conditional` - 仅在功能启用时加载模块
- `bundle-preload` - 在 hover/focus 时预加载以提升感知速度

### 3. 服务端性能（HIGH）

- `server-auth-actions` - 像 API 路由一样对 Server Actions 做认证
- `server-cache-react` - 使用 React.cache() 做单次请求内去重
- `server-cache-lru` - 使用 LRU 缓存做跨请求缓存
- `server-dedup-props` - 避免在 RSC props 中重复序列化
- `server-hoist-static-io` - 将静态 I/O（字体、logo）提升到模块级
- `server-serialization` - 最小化传给客户端组件的数据
- `server-parallel-fetching` - 重组组件以并行拉取数据
- `server-parallel-nested-fetching` - 在 Promise.all 中为每项链式嵌套 fetch
- `server-after-nonblocking` - 使用 after() 做非阻塞操作

### 4. 客户端数据获取（MEDIUM-HIGH）

- `client-swr-dedup` - 使用 SWR 自动去重请求
- `client-event-listeners` - 去重全局事件监听器
- `client-passive-event-listeners` - 滚动场景使用 passive 监听器
- `client-localstorage-schema` - 为 localStorage 数据做版本化并最小化存储

### 5. 重渲染优化（MEDIUM）

- `rerender-defer-reads` - 不要订阅仅在回调中使用的 state
- `rerender-memo` - 将昂贵计算提取到 memo 化组件
- `rerender-memo-with-default-value` - 提升默认非原始类型 props
- `rerender-dependencies` - 在 effect 中使用原始类型依赖
- `rerender-derived-state` - 订阅派生布尔值，而非原始连续值
- `rerender-derived-state-no-effect` - 在渲染时派生 state，而非 effect
- `rerender-functional-setstate` - 使用函数式 setState 获得稳定回调
- `rerender-lazy-state-init` - 对昂贵初始值向 useState 传入函数
- `rerender-simple-expression-in-memo` - 简单原始表达式避免 useMemo
- `rerender-split-combined-hooks` - 拆分依赖独立的 hook
- `rerender-move-effect-to-event` - 将交互逻辑放在事件处理器中
- `rerender-transitions` - 对非紧急更新使用 startTransition
- `rerender-use-deferred-value` - 延迟昂贵渲染以保持输入响应
- `rerender-use-ref-transient-values` - 对频繁变化的瞬时值使用 ref
- `rerender-no-inline-components` - 不要在组件内部定义组件

### 6. 渲染性能（MEDIUM）

- `rendering-animate-svg-wrapper` - 动画 div 包装层，而非 SVG 元素
- `rendering-content-visibility` - 长列表使用 content-visibility
- `rendering-hoist-jsx` - 将静态 JSX 提取到组件外
- `rendering-svg-precision` - 降低 SVG 坐标精度
- `rendering-hydration-no-flicker` - 客户端专属数据使用内联 script
- `rendering-hydration-suppress-warning` - 抑制预期的 hydration 不匹配警告
- `rendering-activity` - 显隐切换使用 Activity 组件
- `rendering-conditional-render` - 条件渲染用三元，而非 &&
- `rendering-usetransition-loading` - 加载态优先 useTransition
- `rendering-resource-hints` - 使用 React DOM 资源提示预加载
- `rendering-script-defer-async` - script 标签使用 defer 或 async

### 7. JavaScript 性能（LOW-MEDIUM）

- `js-batch-dom-css` - 通过 class 或 cssText 批量 CSS 变更
- `js-index-maps` - 重复查找时构建 Map
- `js-cache-property-access` - 在循环中缓存对象属性访问
- `js-cache-function-results` - 在模块级 Map 中缓存函数结果
- `js-cache-storage` - 缓存 localStorage/sessionStorage 读取
- `js-combine-iterations` - 将多次 filter/map 合并为一次循环
- `js-length-check-first` - 昂贵比较前先检查数组长度
- `js-early-exit` - 函数中尽早 return
- `js-hoist-regexp` - 在循环外创建 RegExp
- `js-min-max-loop` - 用循环求 min/max，而非 sort
- `js-set-map-lookups` - 用 Set/Map 做 O(1) 查找
- `js-tosorted-immutable` - 使用 toSorted() 保持不可变
- `js-flatmap-filter` - 用 flatMap 一次完成 map 与 filter
- `js-request-idle-callback` - 将非关键工作推迟到浏览器空闲时

### 8. 高级模式（LOW）

- `advanced-event-handler-refs` - 将事件处理器存入 ref
- `advanced-init-once` - 每个应用加载只初始化一次
- `advanced-use-latest` - 用 useLatest 获得稳定回调 ref

## 如何使用

阅读各条规则的独立文件以获取详细说明与代码示例：

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

每条规则文件包含：

- 简要说明其重要性
- 错误示例及解释
- 正确示例及解释
- 补充背景与参考链接

## 完整汇编文档

所有规则展开后的完整指南见：`AGENTS.md`
