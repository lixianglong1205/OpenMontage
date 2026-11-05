# React 组合模式

面向可扩展场景的 React 组合模式结构化仓库。这些模式通过复合组件、状态提升与内部组合，帮助避免布尔 props 泛滥。

## 结构

- `rules/` - 单条规则文件（每条规则一个文件）
  - `_sections.md` - 章节元数据（标题、影响级别、描述）
  - `_template.md` - 创建新规则所用的模板
  - `area-description.md` - 单条规则文件
- `metadata.json` - 文档元数据（版本、组织、摘要）
- **`AGENTS.md`** - 编译输出（生成物）

## 规则

### 组件架构（CRITICAL）

- `architecture-avoid-boolean-props.md` - 不要用布尔 props 来定制行为
- `architecture-compound-components.md` - 以带共享上下文的复合组件来组织

### 状态管理（HIGH）

- `state-lift-state.md` - 将状态提升到 Provider 组件
- `state-context-interface.md` - 定义清晰的上下文接口（state/actions/meta）
- `state-decouple-implementation.md` - 将状态管理与 UI 解耦

### 实现模式（MEDIUM）

- `patterns-children-over-render-props.md` - 优先使用 children，而非 renderX props
- `patterns-explicit-variants.md` - 创建显式的组件变体

## 核心原则

1. **组合优于配置** — 与其堆 props，不如让使用者自行组合
2. **提升状态** — 状态放在 Provider 中，而非困在组件内部
3. **组合内部结构** — 子组件通过 context 访问，而非 props
4. **显式变体** — 使用 ThreadComposer、EditComposer，而不是带 isThread 的 Composer

## 创建新规则

1. 将 `rules/_template.md` 复制为 `rules/area-description.md`
2. 选择合适的前缀：
   - `architecture-` 用于组件架构
   - `state-` 用于状态管理
   - `patterns-` 用于实现模式
3. 填写 frontmatter 与正文
4. 确保有清晰示例及说明

## 影响级别

- `CRITICAL` - 基础模式，可避免难以维护的代码
- `HIGH` - 显著改善可维护性
- `MEDIUM` - 使代码更整洁的良好实践
