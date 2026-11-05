# Publish Director - 电影感流水线

## 何时使用

打包电影感成片及各类剪辑版本，确保主版本清晰可辨，且分发意图一目了然。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["compose"]["render_report"]`、`state.artifacts["proposal"]["proposal_packet"]`、`state.artifacts["research"]["research_brief"]`、`state.artifacts["script"]["script"]` | 最终输出与节拍图 |
| Playbook | 当前启用的风格 playbook | 语气与命名一致性 |

## 流程

### 1. 区分主版本与衍生版本

典型交付物：

- 主预告片或品牌片，
- teaser 剪辑，
- 社媒短剪，
- 海报帧或缩略图概念。

### 2. 元数据与语气一致

包装应反映实际情绪基调：

- 戏剧性，
- 高端感，
- 神秘感，
- 沉思感，
- 紧迫感。

### 3. 保留剪辑事实

在 `publish_log.metadata` 中存储：

- `hero_output`
- `derivative_outputs`
- `poster_frame_notes`
- `distribution_notes`

### 4. 质量门

- 主版本导出可被明确识别，
- 衍生导出按用途标注，
- 元数据符合语气，
- 整包可直接使用，无需手工清理。

## 常见陷阱

- 未清晰命名即混用 teaser 与主版本输出。
- 撰写忽略情绪的泛化元数据。
- 将所有短剪视为可互换。

---

## 关卡提醒（具约束力）

本阶段需经人工审批（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染
产物），并**结束本轮回复**。勿在同一回复中启动下一阶段。
审批按关卡单独生效——此前「继续」的指令不覆盖本关卡。
