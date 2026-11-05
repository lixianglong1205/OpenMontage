# Skill Creator — Meta Skill

## 何时使用

当你遇到现有技能无法覆盖的需求，且该缺口可复用——而非一次性任务时，使用本技能。本技能教你在流水线运行过程中动态创建新技能。

适合创建新技能的示例：
- 某场景需要现有技能未涵盖的可视化技术（例如「交互式地图动画」）
- 有新工具可用但尚无使用技能（例如新的 TTS 提供商）
- 多个阶段反复出现可固化为技能的模式

**不要**为以下情况创建技能：
- 不会再次出现的一次性任务
- 已有技能已覆盖的内容
- 纯工具配置（应写在工具代码中）

## 协议

### 步骤 1：识别缺口

清晰说明：
1. **你需要做什么**，而现有技能未覆盖
2. **为何可复用**——未来流水线是否会受益？
3. **归属位置**——属于哪一层、哪个目录？

### 步骤 2：调研最佳实践

撰写技能前先调研：
1. **网页搜索**该任务的成熟做法
2. 仓库内**现有技能**的结构模式
3. 技能将引用的工具的**文档**

### 步骤 3：选择技能类型

| 类型 | 目录 | 用途 |
|------|-----------|---------|
| 阶段导演（Stage director） | `skills/pipelines/<pipeline>/` | 如何执行特定流水线的某一阶段 |
| 元技能（Meta skill） | `skills/meta/` | 横切协议（审查、检查点等） |
| 工具技能（Tool skill） | `.agents/skills/` | 如何有效使用特定 API 或工具 |
| 风格技能（Style skill） | `styles/` | 视觉/音频风格定义（YAML playbook） |

### 步骤 4：撰写技能

遵循以下结构（按技能类型调整）：

```markdown
# [Skill Name] — [Context]

## When to Use
[1-2 sentences: what situation triggers this skill]

## Prerequisites
[Table of required resources: schemas, prior artifacts, tools, other skills]

## Process

### Step 1: [First action]
[Clear instructions with examples]

### Step 2: [Second action]
[Clear instructions with examples]

...

### Step N: Self-Evaluate
[Quality rubric: scoring table with 1-5 scale]

### Step N+1: Submit
[How to persist the output]

## Common Pitfalls
[Bullet list of mistakes to avoid]
```

### 优秀技能的关键原则

1. **教思考，而不只是教操作。** 只说「生成一张图」的技能毫无用处；说「考虑本场景的情感节拍、调研头部创作者如何可视化该概念，再撰写包含 playbook 风格锚点的 prompt」的技能才有价值。

2. **包含示例。** 展示好输出长什么样、差输出长什么样。对比比单独说明更能教会执行者。

3. **引用具体资源。** 不要说「检查 schema」，要说「对照 `schemas/artifacts/brief.schema.json` 校验」。不要说「用某个工具」，要说「用 `image_selector`，并带上 playbook 的 `image_prompt_prefix`」。

4. **包含自评量表。** 每个技能都应以评分表结尾，迫使 agent 在继续前自检。

5. **记录常见陷阱。** 执行不当时会出什么问题？明确警告。

6. **要有主见。** 说「你可以做 A 或 B」不如说「做 A，因为 [原因]；当 [条件] 时再回退到 B」。

### 步骤 5：注册技能

写完技能文件后：
1. 在 `skills/INDEX.md` 中增加条目
2. 若是流水线阶段技能，确保流水线 manifest 在该阶段的 `skill` 字段中引用它
3. 若是工具技能，放在 `.agents/skills/<tool-name>/`

### 步骤 6：验证

快速检查：
- [ ] 文件为结构清晰的 Markdown，标题层级明确
- [ ] 引用的 schema、工具与资源均存在
- [ ] 流程步骤有编号且可执行
- [ ] 含自评量表
- [ ] 含「常见陷阱」章节
- [ ] 无悬空引用（提及的内容在仓库中均存在）

## 常见陷阱

- **为一次性任务创建技能**：若不会再做，直接内联完成即可。技能用于模式。
- **指令模糊**：「做好一点」不是技能。具体性才使技能有用。
- **无自评**：没有量表，agent 无法判断是否按技能正确执行。
- **缺少前提条件**：引用了 `image_selector` 却未在前提中列出，会困惑后续 agent。
- **过度设计**：简单任务写 500 行技能不如 50 行。复杂度应与任务匹配。
