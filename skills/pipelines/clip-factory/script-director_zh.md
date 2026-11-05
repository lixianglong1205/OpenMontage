# 脚本导演 - Clip Factory 流水线

## 何时使用

本阶段将长格式源素材转化为带排名的候选列表，再确定最终选片。你要挖掘的是 standout（高光）时刻，而不是整段源内容的摘要。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/script.schema.json` | 产物校验 |
| 上游产物 | `state.artifacts["idea"]["brief"]` | 批次目标与平台定向 |
| Tools | `transcriber`, `scene_detect` | 以转写为先的选片与视觉核对 |

## 流程

### 1. 转写完整源素材

优先使用 `transcriber`。转写稿是寻找 hook 的检索面，不是事后补做项。

仅在需要时调用 `scene_detect`，用于核对有潜力的片段附近的视觉边界、说话人切换或幻灯片切换。

### 2. 为候选时刻打分

依据 brief 中的排名标准，对每个时刻在以下维度上评估：

- `hook`
- `coherence`
- `value`
- `energy`
- `platform_fit`

这与现代切片产品讨论传播力与 clip 质量的方式一致，同时保持判断过程透明。

### 3. 应用「独立成片」测试

每条通过审核的 clip 必须对从未看过原内容的观众也说得通。

拒绝或放宽以下类型的 clip：

- 未解析的代词指代，
- 依赖前文语境的引用，
- 要点出现前过长的铺垫，
- 在 payoff 之前就结束的结尾。

### 4. 选定最终批次

选出满足批次目标的最小集合。

在以下方面保持多样性：

- 源素材区段，
- 说话人，
- clip 类型族，
- 能量层级。

### 5. 用元数据承载排名依据

script schema 体量较小，因此将更完整的批次分析存入 `script.metadata`。

建议的 metadata 键：

- `candidate_clips`
- `selected_clip_ids`
- `ranking_model`
- `rejected_candidates`
- `source_coverage_map`
- `platform_assignments`

每个候选应记录：

- 源素材 in/out，
- hook 文案，
- 选中或拒绝的原因，
- 各打分维度，
- 裁剪可行性评估。

### 6. 质量门

- 排名靠前的 clip 确实是最强片段，而非仅仅最早找到的，
- 每条入选 clip 均通过独立成片测试，
- 选片集有目的地覆盖源素材，而非扎堆于单一区段，
- 低质量候选被如实拒绝。

### 制作过程中的事实核查

若在撰写脚本时遇到不确定之处：
- 使用 `web_search` 在写入脚本前核实事实性陈述
- 使用 `web_search` 查找参考图以保证视觉准确性
- 在决策日志中记录核查：`category="visual_accuracy_check"`

脚本中的每条事实性陈述都应能追溯到 `research_brief`。
若你提出的陈述不在研究材料中，需补充调研并注明来源。不得编造统计数据、日期或归属信息。

## 常见陷阱

- 未经转写级复核就信任首轮候选时间戳。
- 选中过多平静、能量层级雷同的 clip。
- 按时间顺序保留而非按质量排名。
- 将转写质量问题视为次要，而它们会影响选片准确性。

---

## 关卡提醒（具约束力）

本阶段需经人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染产物），并**结束本轮回复**。勿在同一轮回复中启动下一阶段。
批准按关卡单独生效——此前说的「继续」不覆盖本关卡。
