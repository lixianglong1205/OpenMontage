# 合成导演 - Clip Factory 流水线

## 何时使用

独立渲染每个 clip 及各平台变体。此处关键行为是：一致性、批量任务的容错能力，以及对部分失败的清晰报告。

## 运行时路由（硬性约束 — 仅 Remotion 或 FFmpeg）

本流水线处于 HyperFrames 采用计划的第一阶段延后项。`edit_decisions.render_runtime` 必须为 `"remotion"`（默认）或 `"ffmpeg"`（无合成、仅纯拼接的 clip 任务）。HyperFrames 在此**不是**合法运行时 — clip-factory 依赖 Remotion 的词级字幕烧录，HyperFrames 的字幕对等能力属于延后工作。

- 若 `edit_decisions.render_runtime == "hyperframes"`，则停止。重新打开 idea 阶段，向用户展示真实约束，并以 `render_runtime_selection` 决策锁定 `remotion`，其中记录 `hyperframes` 为 `rejected_because: "caption-burn parity deferred on clip-factory"`。
- 按 AGENT_GUIDE.md →「Present Both Composition Runtimes（硬性规则）」：该约束**不能**作为跳过对话的借口。用户仍应了解 HyperFrames 存在，以及为何在此不可行。
- 将 `proposal_packet`/`brief` 传入 `video_compose.execute()`，以便工具内运行时切换检查端到端执行。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["edit"]["edit_decisions"]`、`state.artifacts["assets"]["asset_manifest"]` | Clip 编辑与素材 |
| 工具 | `video_trimmer`、`video_compose`、`audio_mixer`、`color_grade` | 渲染流水线 |
| 媒体配置 | `lib/media_profiles.py` | 平台目标 |

## 流程

### 1. 将每个输出视为独立任务

一个 clip 在三个平台上即三个渲染任务。明确命名并跟踪它们。

### 2. 复用可共享部分

- 在可能处共享音频混音，
- 共享字幕样式，
- 共享叠加素材，
- 若源素材需要，共享调色。

### 3. 软失败

若某个 clip 或某个平台变体失败：

- 清晰记录日志，
- 继续批内其余任务，
- 不要阻塞已成功导出的结果。

### 4. 校验每个输出

每次渲染检查：

- 时长正确，
- 分辨率/宽高比正确，
- 无黑屏首帧，
- hook 按时出现，
- 字幕渲染正确，
- 音频存在且一致。

### 5. 使用渲染报告元数据

建议的元数据键：

- `job_index`
- `failed_jobs`
- `shared_intermediates`
- `platform_groupings`

## 常见陷阱

- 在任务彼此独立时仍无理由地顺序渲染。
- 因单个 clip 失败而停止整批任务。
- 让某一平台变体在 framing 或字幕区域上静默使用错误配置。
