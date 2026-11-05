---
name: vercel-composition-patterns
description:
  可扩展的 React 组合模式。适用于重构布尔 props 泛滥的组件、构建灵活的组件库或
  设计可复用 API。涉及复合组件、render props、Context Provider 或组件架构的任务
  时触发。包含 React 19 API 变更说明。
license: MIT
metadata:
  author: vercel
  version: '1.0.0'
---

# React 组合模式

用于构建灵活、可维护 React 组件的组合模式。通过复合组件、状态提升与内部组合，
避免布尔 props 泛滥。这些模式让代码库在规模扩大时更便于人类与 AI 智能体协作。

> **扩展参考：** 本目录下的 [`AGENTS.md`](AGENTS.md) 是上游完整指南的长文版（来自 Vercel 的 vendored 副本）。它仅作为本技能的补充参考——`SKILL.md` 是可加载的入口与权威说明。它不会覆盖或扩展仓库根目录的 `AGENTS.md` / `AGENT_GUIDE.md`。

## 适用场景

在以下情况下参考本指南：

- 重构带有大量布尔 props 的组件
- 构建可复用的组件库
- 设计灵活的组件 API
- 审查组件架构
- 使用复合组件或 Context Provider

## 规则分类（按优先级）

| 优先级 | 分类           | 影响程度 | 前缀            |
| ------ | -------------- | -------- | --------------- |
| 1      | 组件架构       | 高       | `architecture-` |
| 2      | 状态管理       | 中       | `state-`        |
| 3      | 实现模式       | 中       | `patterns-`     |
| 4      | React 19 API   | 中       | `react19-`      |

## 快速参考

### 1. 组件架构（高）

- `architecture-avoid-boolean-props` - 不要用布尔 props 定制行为；改用组合
- `architecture-compound-components` - 用共享 Context 组织复杂组件

### 2. 状态管理（中）

- `state-decouple-implementation` - 仅 Provider 知晓状态如何管理
- `state-context-interface` - 定义含 state、actions、meta 的通用接口以支持依赖注入
- `state-lift-state` - 将状态移入 Provider，便于兄弟组件访问

### 3. 实现模式（中）

- `patterns-explicit-variants` - 用显式变体组件替代布尔模式
- `patterns-children-over-render-props` - 用 children 组合，而非 renderX props

### 4. React 19 API（中）

> **⚠️ 仅适用于 React 19+。** 若使用 React 18 或更早版本，请跳过本节。

- `react19-no-forwardref` - 不要使用 `forwardRef`；用 `use()` 替代 `useContext()`

## 如何使用

阅读各条规则文件以获取详细说明与代码示例：

```
rules/architecture-avoid-boolean-props.md
rules/state-context-interface.md
```

每条规则文件包含：

- 简要说明其重要性
- 错误代码示例及说明
- 正确代码示例及说明
- 附加上下文与参考资料

## 完整编译文档

若要查看所有规则展开的完整指南，请参阅：`AGENTS.md`
