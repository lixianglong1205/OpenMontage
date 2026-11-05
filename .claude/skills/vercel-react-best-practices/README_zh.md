# React 最佳实践

面向 Agent 与 LLM 创建和维护 React 最佳实践的结构化仓库。

## 结构

- `rules/` - 单条规则文件（每条规则一个文件）
  - `_sections.md` - 章节元数据（标题、影响级别、描述）
  - `_template.md` - 创建新规则的模板
  - `area-description.md` - 各条规则文件
- `src/` - 构建脚本与工具
- `metadata.json` - 文档元数据（版本、组织、摘要）
- __`AGENTS.md`__ - 编译输出（生成）
- __`test-cases.json`__ - 用于 LLM 评估的测试用例（生成）

## 入门

1. 安装依赖：
   ```bash
   pnpm install
   ```

2. 从规则构建 AGENTS.md：
   ```bash
   pnpm build
   ```

3. 校验规则文件：
   ```bash
   pnpm validate
   ```

4. 提取测试用例：
   ```bash
   pnpm extract-tests
   ```

## 创建新规则

1. 将 `rules/_template.md` 复制为 `rules/area-description.md`
2. 选择合适的前缀：
   - `async-` 消除瀑布流（第 1 节）
   - `bundle-` 打包体积优化（第 2 节）
   - `server-` 服务端性能（第 3 节）
   - `client-` 客户端数据获取（第 4 节）
   - `rerender-` 重渲染优化（第 5 节）
   - `rendering-` 渲染性能（第 6 节）
   - `js-` JavaScript 性能（第 7 节）
   - `advanced-` 高级模式（第 8 节）
3. 填写 frontmatter 与正文
4. 确保有清晰的对错示例及说明
5. 运行 `pnpm build` 以重新生成 AGENTS.md 和 test-cases.json

## 规则文件结构

每条规则文件应遵循以下结构：

```markdown
---
title: Rule Title Here
impact: MEDIUM
impactDescription: Optional description
tags: tag1, tag2, tag3
---

## Rule Title Here

Brief explanation of the rule and why it matters.

**Incorrect (description of what's wrong):**

```typescript
// Bad code example
```

**Correct (description of what's right):**

```typescript
// Good code example
```

Optional explanatory text after examples.

Reference: [Link](https://example.com)

## 文件命名约定

- 以 `_` 开头的文件为特殊文件（构建时排除）
- 规则文件：`area-description.md`（例如 `async-parallel.md`）
- 章节由文件名前缀自动推断
- 各章节内规则按标题字母序排序
- ID（如 1.1、1.2）在构建时自动生成

## 影响级别

- `CRITICAL` - 最高优先级，显著性能收益
- `HIGH` - 明显性能提升
- `MEDIUM-HIGH` - 中高程度收益
- `MEDIUM` - 中等性能提升
- `LOW-MEDIUM` - 低中程度收益
- `LOW` - 渐进式改进

## 脚本

- `pnpm build` - 将规则编译为 AGENTS.md
- `pnpm validate` - 校验所有规则文件
- `pnpm extract-tests` - 提取 LLM 评估用测试用例
- `pnpm dev` - 构建并校验

## 贡献

添加或修改规则时：

1. 使用对应章节的前缀命名文件
2. 遵循 `_template.md` 结构
3. 包含清晰的对错示例与说明
4. 添加合适的 tags
5. 运行 `pnpm build` 以重新生成 AGENTS.md 和 test-cases.json
6. 规则会按标题自动排序——无需手动维护编号！

## 致谢

最初由 [Vercel](https://vercel.com) 的 [@shuding](https://x.com/shuding) 创建。
