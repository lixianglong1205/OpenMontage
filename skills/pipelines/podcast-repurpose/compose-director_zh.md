# Compose Director - 播客再利用流水线

## 何时使用

渲染播客衍生输出时，音频保真度为最高优先级。视觉应支撑语音，而非与之竞争。

## 运行时路由（硬性约束 — 仅限 Remotion 或 FFmpeg）

Phase 1 已从 HyperFrames 延期。`edit_decisions.render_runtime` 必须为 `"remotion"`（audiogram、合成输出）或 `"ffmpeg"`（纯音频主导的片段导出）。HyperFrames 字幕烧录对等能力已延期，播客输出依赖 Remotion 的词级字幕栈。

- 若 `edit_decisions.render_runtime == "hyperframes"`，则停止。重新打开 idea 阶段并向用户说明该约束。切勿静默改写运行时。
- 按 AGENT_GUIDE.md →「Present Both Composition Runtimes（硬性规则）」：告知用户 HyperFrames 存在及在本流水线不可行的原因，而非静默锁定 remotion。记录 `render_runtime_selection` 决策，其中 hyperframes 的 `rejected_because: "caption-burn parity deferred on podcast-repurpose"`。
- 将 `proposal_packet`/`brief` 传入 `video_compose.execute()`，用于端到端运行时切换检测。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["edit"]["edit_decisions"]`、`state.artifacts["assets"]["asset_manifest"]` | 输出计划与资源路径 |
| 工具 | `video_compose`、`audio_mixer` | 渲染与混音控制 |
| Playbook | 当前启用的 style playbook | 品牌一致性 |

## 流程

### 1. 优先渲染最高价值输出

优先级顺序：

1. 短高光片段
2. 金句主导片段
3. 可选的长篇配套视频

这样可优先交付最易发布的资源。

### 2. 保持音频质量

- 避免不必要的重新编码，
- 保持语音清晰、稳定，
- 谨慎使用音乐，且仅在不与语音竞争时使用，
- 渲染后验证字幕同步。

### 3. 遵守平台画幅

- `9:16` 用于短视频社交
- `1:1` 用于金句主导或信息流安全片段
- `16:9` 用于长篇 YouTube 配套输出

### 4. 验证每一项交付物

- 时长正确，
- 画幅比例正确，
- 字幕可读，
- 说话人归属准确，
- 音频稳定，
- 品牌处理一致。

### 5. 使用渲染报告元数据

建议的元数据键：

- `deliverable_groups`
- `audio_notes`
- `subtitle_checks`
- `failed_outputs`

## 常见陷阱

- 让视觉处理损害音频质量。
- 先渲染完整配套内容，拖延最重要的片段。
- 忘记：简单、可读的片段优于技术花哨但令人困惑的片段。
