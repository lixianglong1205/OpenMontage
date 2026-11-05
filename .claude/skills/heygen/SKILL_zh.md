---
name: heygen
description: |
  [已弃用] 请使用 `create-video` 进行基于提示词的视频生成，或使用 `avatar-video` 进行精确的虚拟人/场景控制。本旧版技能将两种工作流合并在一起——较新的专用技能提供更清晰的指引。
homepage: https://docs.heygen.com/reference/generate-video-agent
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# HeyGen API（已弃用）

> **本技能已弃用。** 请改用以下专用技能：
> - **`create-video`** — 通过文本提示词生成视频（Video Agent API）
> - **`avatar-video`** — 使用指定虚拟人、音色、脚本与场景构建视频（v2 API）

本技能仅为向后兼容而保留，将在未来版本中移除。

---

用于生成口播视频、讲解与演示的 AI 虚拟人视频创建 API。

## 工具选择

若可用 HeyGen MCP 工具（`mcp__heygen__*`），**优先使用 MCP**，而非直接调用 HTTP API——MCP 会自动处理认证与请求格式。

| 任务 | MCP 工具 | 备选（直接 API） |
|------|----------|----------------------|
| 从提示词生成视频 | `mcp__heygen__generate_video_agent` | `POST /v1/video_agent/generate` |
| 查询视频状态 / 获取 URL | `mcp__heygen__get_video` | `GET /v2/videos/{video_id}` |
| 列出账户内视频 | `mcp__heygen__list_videos` | `GET /v2/videos` |
| 删除视频 | `mcp__heygen__delete_video` | `DELETE /v2/videos/{video_id}` |

若无 HeyGen MCP 工具，请使用直接 HTTP API 调用，并在请求头中携带 `X-Api-Key: $HEYGEN_API_KEY`，详见参考文件中的说明。

## 默认工作流

**多数视频请求优先使用 Video Agent。**
始终遵循 [prompt-optimizer.md](references/prompt-optimizer.md) 中的指引，用场景、时长与视觉风格来组织提示词。

**使用 MCP 工具时：**
1. 按 [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) 编写优化后的提示词
2. 调用 `mcp__heygen__generate_video_agent`，传入提示词与配置（duration_sec、orientation、avatar_id）
3. 使用返回的 video_id 调用 `mcp__heygen__get_video`，轮询状态并获取下载 URL

**未使用 MCP 工具（直接 API）时：**
1. 按 [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) 编写优化后的提示词
2. `POST /v1/video_agent/generate` — 见 [video-agent.md](references/video-agent.md)
3. `GET /v2/videos/<id>` — 见 [video-status.md](references/video-status.md)

仅在用户明确需要以下能力时使用 v2/video/generate：
- 精确脚本且不经 AI 修改
- 指定 voice_id
- 各场景使用不同虚拟人/背景
- 精确的分场景时长控制
- 带精确规格的编程化/批量生成

## 快速参考

| 任务 | MCP 工具 | 阅读 |
|------|----------|------|
| 从提示词生成视频（简易） | `mcp__heygen__generate_video_agent` | [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) → [video-agent.md](references/video-agent.md) |
| 精确控制生成视频 | — | [video-generation.md](references/video-generation.md)、[avatars.md](references/avatars.md)、[voices.md](references/voices.md) |
| 查询视频状态 / 获取下载 URL | `mcp__heygen__get_video` | [video-status.md](references/video-status.md) |
| 添加字幕或文字叠加 | — | [captions.md](references/captions.md)、[text-overlays.md](references/text-overlays.md) |
| 用于合成的透明视频 | — | [video-generation.md](references/video-generation.md)（WebM 章节） |
| 与 Remotion 配合使用 | — | [remotion-integration.md](references/remotion-integration.md) |

## 参考文件

### 基础
- [references/authentication.md](references/authentication.md) - API 密钥设置与 X-Api-Key 请求头
- [references/quota.md](references/quota.md) - 积分体系与用量限制
- [references/video-status.md](references/video-status.md) - 轮询模式与下载 URL
- [references/assets.md](references/assets.md) - 上传图片、视频、音频

### 核心视频创建
- [references/avatars.md](references/avatars.md) - 列出虚拟人、风格与 avatar_id 选择
- [references/voices.md](references/voices.md) - 列出音色、语言区域、语速/音高
- [references/scripts.md](references/scripts.md) - 撰写脚本、停顿与节奏
- [references/video-generation.md](references/video-generation.md) - POST /v2/video/generate 与多场景视频
- [references/video-agent.md](references/video-agent.md) - 一次性提示词视频生成
- [references/prompt-optimizer.md](references/prompt-optimizer.md) - 编写有效的 Video Agent 提示词（核心工作流与规则）
- [references/visual-styles.md](references/visual-styles.md) - 20 种命名视觉风格及完整规格
- [references/prompt-examples.md](references/prompt-examples.md) - 完整生产级提示词示例与即用模板
- [references/dimensions.md](references/dimensions.md) - 分辨率与宽高比

### 视频定制
- [references/backgrounds.md](references/backgrounds.md) - 纯色、图片、视频背景
- [references/text-overlays.md](references/text-overlays.md) - 添加文字、字体与定位
- [references/captions.md](references/captions.md) - 自动生成字幕与副标题

### 高级功能
- [references/templates.md](references/templates.md) - 模板列表与变量替换
- [references/photo-avatars.md](references/photo-avatars.md) - 从照片创建虚拟人
- [references/webhooks.md](references/webhooks.md) - Webhook 端点与事件

### 集成
- [references/remotion-integration.md](references/remotion-integration.md) - 在 Remotion 合成中使用 HeyGen
