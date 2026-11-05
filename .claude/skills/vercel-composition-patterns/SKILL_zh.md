---
name: vercel-composition-patterns
description:
  可扩展的 React 组合模式。在重构带有布尔 prop 泛滥的组件、构建灵活的组件库或
  设计可复用 API 时使用。涉及复合组件、render props、context provider 或
  组件架构的任务会触发。包含 React 19 API 变更。
license: MIT
metadata:
  author: vercel
  version: '1.0.0'
---

# React 组合模式

用于构建灵活、可维护 React 组件的组合模式。通过复合组件、状态提升与内部组合，
避免布尔 prop 泛滥。随着规模增长，这些模式让人类与 AI 智能体都更容易协作维护代码库。

> **扩展参考：** 本目录下的 [`AGENTS.md`](AGENTS.md) 是完整的上游长文指南（来自 Vercel 的 vendored 版本）。它仅作为本 skill 的补充参考——`SKILL.md` 是可加载的入口与权威来源，不会覆盖或扩展仓库根目录的 `AGENTS.md` / `AGENT_GUIDE.md`。

## 何时适用

在以下场景中参考这些指南：

- 重构带有大量布尔 prop 的组件
- 构建可复用的组件库
- 设计灵活的组件 API
- 审查组件架构
- 使用复合组件或 context provider

## 按优先级划分的规则类别

| 优先级 | 类别           | 影响   | 前缀            |
| ------ | -------------- | ------ | --------------- |
| 1      | 组件架构       | HIGH   | `architecture-` |
| 2      | 状态管理       | MEDIUM | `state-`        |
| 3      | 实现模式       | MEDIUM | `patterns-`     |
| 4      | React 19 API   | MEDIUM | `react19-`      |

## 快速参考

### 1. 组件架构（HIGH）

- `architecture-avoid-boolean-props` - 不要用布尔 prop 定制行为；改用组合
- `architecture-compound-components` - 用共享 context 组织复杂组件结构

### 2. 状态管理（MEDIUM）

- `state-decouple-implementation` - Provider 是唯一知道状态如何管理的地方
- `state-context-interface` - 定义含 state、actions、meta 的通用接口以支持依赖注入
- `state-lift-state` - 将状态移入 provider 组件，供兄弟节点访问

### 3. 实现模式（MEDIUM）

- `patterns-explicit-variants` - 创建显式变体组件，而非布尔模式
- `patterns-children-over-render-props` - 用 children 做组合，而非 renderX props

### 4. React 19 API（MEDIUM）

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
- 额外背景与参考

## 完整编译文档

所有规则展开后的完整指南见：`AGENTS.md`
