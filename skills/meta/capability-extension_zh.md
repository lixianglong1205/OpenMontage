# 能力扩展协议

## 何时使用

当你遇到现有工具无法覆盖的制作需求时。Agent 可以扩展系统——但须遵守护栏。本协议以结构化流程取代笼统的「不得编写临时 Python 脚本」规则。

## 先评估

在编写任何内容之前，对缺口进行分类：

| 缺口类型 | 示例 | 行动 |
|----------|---------|--------|
| **一次性转换** | 自定义图像裁剪、色彩调整、格式转换 | 编写项目范围内的 Python 脚本 |
| **重复出现的视觉需求** | 新插画风格、自定义图表类型 | 生成自定义 playbook 或 Remotion 组件 |
| **缺失的提供商** | 用户需要 registry 中未收录的特定 API | 创建最小化工具包装器 |
| **缺失的知识** | Agent 不知道如何为特定模型编写 prompt | 用网页搜索学习，并记录为 Layer 3 skill |

## 临时脚本规则

**仅当**满足以下条件时才允许编写脚本：
1. 现有工具无法覆盖该需求（通过 preflight 对照 registry 已核实）
2. 脚本具有幂等性（可安全重复运行）
3. 脚本在项目工作区中产出文件制品
4. 脚本已记入决策日志：`category: "capability_extension"`
5. 已告知用户：「因现有工具无法处理 Y，我为 X 编写了自定义脚本」
6. 未经用户批准，脚本**不得**调用外部 API

脚本存放路径：`projects/<project-name>/scripts/`

### 脚本模板

```python
"""<One-line description of what this script does>

Created by capability extension protocol because: <reason no existing tool covers this>
Decision log entry: <decision_id>
"""
import sys
from pathlib import Path

def main(input_path: str, output_path: str) -> None:
    # Idempotent: check if output already exists
    out = Path(output_path)
    if out.exists():
        print(f"Output already exists: {out}")
        return

    # ... transformation logic ...

    print(f"Created: {out}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

## 自定义 Playbook 规则

当现有 playbook 与 brief 不匹配时：
1. 使用 `lib/playbook_generator.py` 创建新 playbook
2. 尽可能基于最接近的现有 playbook
3. 对照 `schemas/styles/playbook.schema.json` 校验
4. 保存至 `styles/custom/<project-name>.yaml`
5. 记入决策：`category: "playbook_selection"`，`subject: "custom playbook created"`

## 新 Skill 规则（技法学习）

当 Agent 在网页调研中发现技法类知识时：
1. 记录为项目范围 skill：`projects/<project-name>/skills/<name>.md`
2. 遵循 Layer 3 skill 格式：
   - 提供商名称与版本
   - 提供商专属的 prompting 模式
   - 该用例下的最优参数
   - 质量技巧与已知失败模式
   - 信息来源 URL
3. 在决策日志中引用
4. 若具有通用价值，建议提升至 `.agents/skills/`

## 工具包装器规则

当用户需要 registry 中不存在的特定提供商时：
1. Agent 可创建最小化 `BaseTool` 子类
2. 保存至 `projects/<project-name>/tools/<name>.py`
3. **必须**继承 `BaseTool` 并实现完整契约（input_schema、execute、capabilities 等）
4. **必须**在使用前完成注册
5. 记入决策：`category: "capability_extension"`
6. 首次付费 API 调用前须获得用户批准

## 仍然禁止的事项

- 绕过 pipeline（所有制作仍须按阶段进行）
- 在用户不知情的情况下调用外部 API
- 修改 `tools/` 中的现有工具（应创建包装器，勿改原版）
- 跳过决策日志
- 编写副作用超出输出文件的脚本（禁止发邮件、推送到远程、删除项目工作区外的文件）

## 决策日志条目格式

每次扩展都必须记录：

```json
{
  "decision_id": "ext-001",
  "stage": "<current stage>",
  "category": "capability_extension",
  "subject": "Created custom <script|playbook|skill|tool> for <purpose>",
  "options_considered": [
    {"option_id": "existing-tool", "label": "<closest existing tool>", "rejected_because": "<why it doesn't work>"},
    {"option_id": "extension", "label": "<what was created>", "reason": "<why this approach>"}
  ],
  "selected": "extension",
  "reason": "<concise justification>",
  "user_visible": true,
  "confidence": 0.8
}
```
