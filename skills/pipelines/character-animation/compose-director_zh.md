# Compose 阶段导演 - 角色动画流水线

## 目标

渲染已批准的角色动画，并证明已完成审阅。

## 运行时路由

首先读取 `edit_decisions.render_runtime`。除非存在明确变更运行时的 `render_runtime_selection` 决策，否则它必须与提案中锁定的运行时一致。

- `remotion`：将素材放入 `remotion-composer/public`，构建 composition JSON，通过 `video_compose` 渲染。
- `hyperframes`：物化 HyperFrames 工作区，由 `video_compose` 委托给 `hyperframes_compose`。必须通过 `hyperframes lint` 与 `validate`。
- `ffmpeg`：仅用于后处理或简单视频组装；不足以单独完成角色表演。

## 审阅工作流

1. 运行 `character_rig_renderer` 以生成或刷新 HyperFrames 包。浏览器预览仅作 QA/调试产物，不是渲染路径。
2. 确认渲染器输出了 HyperFrames 的 `workspace_path`、composition HTML、`asset_manifest`，以及 `edit_decisions.render_runtime: "hyperframes"` 交接信息。
3. 针对 rig、poses、timeline 与 preview 运行 `character_animation_reviewer`。
4. 使用渲染器交接或已批准的 Remotion/HyperFrames 包，通过 `video_compose` 渲染最终视频。交付物路径为 `projects/<project-name>/renders/final.mp4`，与 OpenMontage 标准项目约定一致。
5. 运行标准 `final_review`：ffprobe、帧采样、视觉抽查、音频抽查、承诺保留（promise preservation）检查。

## 浏览器 QA

当 Playwright 可用时：

- 打开预览，
- 截取开头/中间/结尾帧，
- 检查是否存在控制台错误，
- 确认角色可见，
- 比较帧差异以确认存在运动。

当 Playwright 不可用时，使用静态产物检查与 FFmpeg 帧采样，并说明置信度降低。

## 质量标准

当 `character_qa_report.status` 为 `revise` 或 `fail` 时，不要将输出视为已完成。
