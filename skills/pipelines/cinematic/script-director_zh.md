# 脚本导演 - 电影感流水线

## 适用场景

本阶段为电影感作品构建节拍图、选定台词、标题卡文案与揭示结构。你在塑造节奏，而非撰写冗长的解说稿。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/script.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["proposal"]["proposal_packet"]` | 情感弧线与事实来源 |
| 工具 | `transcriber`, `scene_detect` | 可选：对白挖掘与源素材审阅 |

## 流程

### 1. 先构建节拍图

采用简单结构：

- hook（开场钩子），
- escalation（递进），
- reveal（揭示），
- landing（收束）。

若篇幅更长，可增加一个中点转折。勿写成 essay 式长文结构。

### 2. 谨慎使用对白

若源素材中有语音，使用 `transcriber` 查找：

- 可独立成句的强台词，
- 情感化短语，
- 简洁宣言，
- 揭示性短语。

若无可用对白，则保持以标题卡或旁白为主导，并在 metadata 中说明。

### 3. 标题卡宜短

标题卡文案应具预告片感：

- 字更少，
- 对比更强，
- 留白更多，
- 时间点更准。

### 4. 在 Metadata 中保存节拍事实

建议 metadata 键：

- `beat_map`
- `dialogue_selects`
- `title_card_copy`
- `music_turns`
- `silence_windows`

### 5. 质量门

- 节拍图递进清晰，
- 对白与标题卡不重复解释同一件事，
- 揭示时刻区分明确，
- 收束给观众明确的最终感受或行动。

### 制作过程中的事实核查

若在撰写脚本时遇到不确定之处：
- 使用 `web_search` 在写入脚本前核实事实性陈述
- 使用 `web_search` 查找参考图以保证视觉准确
- 在决策日志中记录核查：`category="visual_accuracy_check"`

脚本中的每条事实性陈述应可追溯到 `research_brief`。
若陈述不在研究简报中，需补充调研并添加来源。勿编造统计数据、日期或归属。

## 常见陷阱

- 写成完整说明性段落而非节拍。
- 标题卡过多。
- 最佳时刻揭示过早。

---

## 关卡提醒（具有约束力）

本阶段需经人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 创建 checkpoint，呈现摘要（Backlot 看板会渲染产物），并**结束本轮回复**。勿在同一回复中启动下一阶段。
批准按关卡单独生效——此前「继续」的口头许可不覆盖本关卡。
