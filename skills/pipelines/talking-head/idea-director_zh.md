# 创意导演 — Talking Head 流水线

## 何时使用

你正在启动一个 talking-head（口播/真人出镜）视频项目。你有一段人物讲话的原始素材。你的任务是分析素材、理解其内容，并撰写一份简报（brief），抓住内容本质与制作目标。

与 explainer 流水线（从主题出发）不同，你从现有素材出发。简报记录你手头有什么，以及成片应呈现的样子。

## 运行时选择（强制 — 呈现约束，勿静默选定）

锁定 `render_runtime = "remotion"`（首选 — 使用 `TalkingHead` + `remotion_caption_burn`）或 `"ffmpeg"`（用于无合成的源素材拼接）。**HyperFrames 在本流水线 Phase 1 中不是有效运行时** — TalkingHead 合成与词级字幕烧录尚无 HyperFrames 对等实现。

按 AGENT_GUIDE.md →「Present Both Composition Runtimes (HARD RULE)」：不要静默默认 remotion。告知用户：「HyperFrames 可用，但 talking-head 依赖 Remotion TalkingHead 合成，因此 remotion 是唯一可行的合成选择（或 ffmpeg 做原始剪辑）— 可以继续吗？」记录 `render_runtime_selection` 决策，并将 hyperframes 列为被拒选项（`rejected_because: "TalkingHead + caption parity deferred on talking-head"`）。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/brief.schema.json` | 产物校验 |
| 输入 | 原始素材文件路径 | 源材料 |
| 工具 | `ffprobe`（通过 shell） | 素材元数据提取 |

## 流程

### 步骤 1：检查素材

使用 ffprobe 提取元数据：
- 时长
- 分辨率
- 帧率
- 音频声道与编解码器
- 文件大小

由此了解素材质量、长度与格式。

### 步骤 2：快速内容评估

观看/扫描素材（若可用 frame_sampler 则采样帧）：
- 讲话者在讲什么？
- 原始素材多长？
- 目标平台是什么？（不清楚则询问用户）
- 音频是否清晰？有无背景噪声？

### 步骤 3：撰写简报

创建 brief 产物，记录：
- **Title**：基于素材内容的描述性标题
- **Hook**：什么让这段内容值得观看？
- **Key points**：素材中涵盖的主要话题
- **Tone**：与讲者实际语气一致（随意、专业、教育性等）
- **Style**：根据素材、讲者人设、受众与平台推导叠加层/视觉方向。`clean-professional` 是稳妥备选，不是每个 talking-head 简报的默认答案。
- **Target platform**：发布渠道
- **Target duration**：可短于原始素材（经修剪）

### 步骤 4：自评

| 标准 | 问题 |
|-----------|----------|
| **准确性** | 简报是否反映素材中的实际内容？ |
| **完整性** | 是否具备简报所需的全部字段？ |
| **平台契合度** | 目标平台是否与内容匹配？ |

### 步骤 5：提交

对照 schema 校验简报，并通过 checkpoint 持久化。

---

## 关卡提醒（具约束力）

本阶段需人工审批（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染产物），并**结束本轮**。勿在同一回复中启动下一阶段。
审批按关卡单独进行 — 此前「继续」不覆盖本关卡。
