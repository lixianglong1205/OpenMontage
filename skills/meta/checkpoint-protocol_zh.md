# Checkpoint Protocol — Meta Skill

## 何时使用

在完成某阶段工作并通过审查之后使用。本技能说明何时以及如何创建 checkpoint，以及何时需要请求人工审批。它用指令驱动的协议取代了 Python 的 `checkpoint_policy.py`。

Checkpoint 是流水线的存档点，支持失败后恢复、人工监督与审计追踪。

## 协议

### 步骤 1：查阅 Manifest 策略

从 pipeline manifest 读取当前阶段的配置：

```yaml
- name: idea
  checkpoint_required: true      # Must we checkpoint?
  human_approval_default: true   # Must we ask the human?
```

| `checkpoint_required` | `human_approval_default` | 操作 |
|----------------------|------------------------|--------|
| true | true | 创建 checkpoint + 提交人工审批 |
| true | false | 创建 checkpoint + 自动继续 |
| false | * | 完全跳过 checkpoint（少见） |

### 步骤 2：准备 Checkpoint 数据

汇总 checkpoint 所需的一切：

1. **Stage name** — 刚完成的阶段名称
2. **Status** — `"completed"`（若需审批则为 `"awaiting_human"`）
3. **Artifacts** — 该阶段产出的规范 artifact
4. **Metadata** — 审查结论、成本快照、耗时信息

### 步骤 3：写入 Checkpoint

调用 checkpoint 工具：

```python
write_checkpoint(
    pipeline_dir,      # Project working directory
    project_name,      # Project identifier
    stage_name,        # e.g., "idea"
    status,            # "completed" or "awaiting_human"
    artifacts,         # {"brief": {...}} — the stage's output
)
```

checkpoint 工具将：

- 按 schema 校验 artifact
- 执行审批门控（门控阶段在未设 `human_approved=True` 时不能写入 `completed`）
- 将被取代的 checkpoint 归档到 `projects/<id>/history/`（阶段版本与门控转换不会被销毁）
- 将 checkpoint JSON 写入磁盘
- 包含时间戳与阶段元数据

规范路径：`projects/<project_id>/checkpoint_<stage>.json` — 始终
将仓库的 `projects/` 目录作为 `pipeline_dir` 传入（或使用
`lib.checkpoint.PROJECTS_DIR`）。始终传入 `pipeline_type` — 门控校验
通过它读取 manifest。

在流水线初始化时（任何阶段之前），调用 `init_project()`：

```python
from lib.checkpoint import init_project
init_project("my-project", title="My Project", pipeline_type="cinematic")
```

这会创建规范目录布局并写入 `project.json` —
Backlot 看板在首个 checkpoint 之前展示项目所需的标记。
然后启动看板：`python -m backlot open my-project`
（若不可用则非致命 — 看板是观察者，从不是阻塞项）。

### 步骤 4：阶段内 Checkpoint（恢复支持 + 存活信号）

**进入任一阶段时，先写入 `in_progress` checkpoint。** 这
通过 Backlot 看板告诉用户该阶段正在运行而非卡住 —
确定性比速度更重要。

长时间运行的阶段（如 `assets` 或 `compose` 循环）可能因 API 错误、限流或会话中断而中途失败。为从失败点精确恢复（例如场景 4）：

1. **写入部分进度**：每成功生成一项重要产出（例如一个场景的资产、一个片段），就写入 `in_progress` checkpoint。

   `in_progress` checkpoint 可省略阶段的规范 artifact，但存放在已知 artifact 名称下的任何 artifact 仍会按 schema 校验。若部分数据尚非有效规范 artifact，则存入 `metadata.partial_progress`，而非 `artifacts`。
   ```python
   write_checkpoint(
       pipeline_dir, project_name,
       stage="assets",
       status="in_progress",
       artifacts={},  # no incomplete canonical artifact yet
       metadata={
           "partial_progress": {
               "asset_manifest_draft": partial_manifest_dict,
               "completed_scene_ids": completed_scene_ids,
           }
       },
   )
   ```
   若部分 artifact 已满足 schema（例如带 `version: "1.0"` 且有效 `assets[]` 的 `asset_manifest`），可直接存入 `artifacts`。
2. **从部分进度恢复**：启动阶段时，**始终**检查是否存在该阶段的 `in_progress` checkpoint。处理方式见步骤 7（恢复协议）。

### 步骤 5：人工审批（若需要）

**Manifest 中的值为约束。** pipeline manifest 里的 `human_approval_default`
是阶段是否设门的唯一真相来源。本技能不会覆盖它，你也不能 —
不存在「这次情况不同」。
（`lib/checkpoint.py` 会强制执行：对门控阶段在未设 `human_approved=True` 时写入 `status="completed"` 会抛出 `GATE VIOLATION` 错误。）

当 `human_approval_default: true` 时：

1. **以 `status="awaiting_human"` 写入 checkpoint**（不是 `completed`）。

2. **向人工呈现摘要**：
   ```
   ## Stage Complete: [stage_name] — awaiting your approval

   ### Artifact Summary
   [Key details from the artifact — title, duration, key decisions]
   [If the Backlot board is running, point to it: the artifact renders there]

   ### Review Findings
   [Summary from reviewer: N critical (all fixed), N suggestions]

   ### Cost So Far
   [Budget spent / total, breakdown by tool]

   ### Action Required
   Please review and approve to continue, or provide feedback for revision.
   ```

3. **结束本轮。** 在同一回复中继续任何流水线工作都属于门控违规。「呈现并继续」不算等待 —
   本轮必须以问题结束，下一流水线动作必须由用户回复触发。

4. **收到用户回复后：**
   - **已批准** → 以 `status="completed"`、`human_approved=True` 重新写入 checkpoint，然后进入下一阶段
   - **要求修订** → 带着人工反馈回到阶段 director skill，产出修订 artifact，重新审查、重新 checkpoint
     （被取代的 checkpoint 会自动保留在 `history/`）
   - **中止** → 停止流水线

5. **审批按门逐次进行。** 先前的批准，无论多宽泛（「看起来不错，整片都做吧」），
   都不覆盖后续门。若用户明确预授权整次运行，在其说出时以
   `decision_log` 条目（`category: "approval_policy"`）记录 —
   若无该条目，每个门都必须停下。

6. **assets 门审查分镜 — 在任何草稿渲染之前。**
   各 pipeline 中 `assets` 现已设门：按场景呈现生成的资产
   （Backlot 看板的胶片条是自然审查界面），包括迄今花费与 compose 预估成本。在此发现坏资产可避免整片重渲染。

   **不要通过渲染草稿/完整合成来「换取」这次审查。** 审查界面是填充了逐场景资产的胶片条 — 素材挑选、
   生成静帧、旁白波形 — *不是* 已渲染视频。对「资产」为定制/atelier 合成（无可缩略图文件）的场景，
   agent 将**逐场景审查静帧**写入
   `projects/<id>/snapshots/<scene_id>.png`（代表性帧的 `remotion still` — 见 `skills/meta/bespoke-composition.md`）；看板在胶片条上展示它们。静帧就绪后刷新 `metadata.partial_progress`，然后在门处 **STOP**。草稿/终稿渲染属于 **compose**
   阶段 — 仅在 assets 门批准之后运行。在 assets 阶段内渲染完整草稿等于跳过用户应持有的门。

### 步骤 6：确定下一阶段

checkpoint 写入且（若需要）已批准后：

```python
next_stage = get_next_stage(pipeline_dir, project_name)
```

这会读取所有已有 checkpoint，返回下一个待运行阶段；若流水线已完成则返回 `None`。

### 步骤 7：恢复协议

在**任何**流水线运行开始时（不限于某阶段之后），始终检查已有进度：

```python
next_stage = get_next_stage(pipeline_dir, project_name)
```

若 `next_stage` 不是第一阶段：

1. 告知人工：「发现已有进度。从阶段恢复：[next_stage]」
2. **检查部分进度**：读取 `next_stage` 的 checkpoint：
   ```python
   current_cp = read_checkpoint(pipeline_dir, project_name, next_stage)
   ```
   若 `current_cp` 存在且状态为 `"in_progress"`，告知人工你正从阶段中途恢复。
3. **加载 artifact**：从 checkpoint 加载先前 artifact 作为上下文。若从 `"in_progress"` 恢复，先从 `current_cp["artifacts"]` 加载任何符合 schema 的部分 artifact。若部分数据在 `current_cp["metadata"]["partial_progress"]`，使用该草稿数据及其完成标记（如 `completed_scene_ids`）跳过已完成子任务。
4. **继续**：从下一成功步骤继续生成，追加到部分 artifact。

若存在状态为 `"awaiting_human"` 的 checkpoint：

1. 告知人工：「阶段 [name] 等待你的批准」
2. 呈现 checkpoint 数据供审查
3. 批准前等待

### 样片 Checkpoint（参考驱动制作）

当制作为参考驱动（存在 VideoAnalysisBrief）时，在提案批准与完整制作之间还有额外 checkpoint：

| Stage | checkpoint_required | human_approval_default | 说明 |
|-------|--------------------|-----------------------|-------|
| `sample` | true | true | 始终需要人工批准 |

样片 checkpoint：

1. 呈现：已渲染样片（10–15 秒）
2. 成本：样片成本 vs 全片预估成本
3. 操作：批准（→ 进入 script）、修订（→ 重新生成样片）、中止

样片 checkpoint **不是** pipeline 阶段 — 它是 proposal 阶段内的子 checkpoint。不产出规范 artifact。产出存放在 `projects/<name>/assets/sample/sample_v{N}.mp4` 的预览片段。

**呈现格式：**
```
## Sample Preview Ready

**Sample clip:** [path to sample_v1.mp4]
- Duration: [X] seconds (hook + 1 middle scene)
- Voice: [TTS provider + voice name]
- Visuals: [description — AI images, Remotion animations, etc.]
- Music: [source]

**Sample cost:** $[X.XX]
**Projected full video cost:** $[X.XX]

Does this feel right? I can adjust: voice, visual style, pacing, music, colors.
```

## 核心原则

1. **始终为已完成工作创建 checkpoint。** 即使 `checkpoint_required: false`，若阶段耗时或成本显著，仍应考虑 checkpoint。丢失工作比多一个磁盘文件更糟。

2. **创意阶段切勿跳过人工批准。** `idea` 与 `script` 决定一切。为省时间跳过它们会得到没人想要的视频。

3. **包含成本快照。** 人工在批准昂贵下游阶段（assets、compose）前应知道已花费与剩余预算。

4. **Checkpoint 使恢复成为可能。** 若流水线在 `compose` 崩溃，人工可重启并从 `compose` 继续 — 而非从 `idea` 重来。这就是其意义。

5. **审批请求要透明。** 不要只展示 artifact — 还要展示审查结论、成本与顾虑。帮助人工做出知情决策。
