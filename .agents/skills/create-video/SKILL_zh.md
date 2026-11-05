---
name: create-video
description: |
  使用 HeyGen 的 Video Agent 根据文本提示创建视频。适用场景：(1) 根据描述或创意创建视频，(2) 根据提示生成讲解、演示或营销视频，(3) 在不指定具体 avatar、voice 或 scene 的情况下制作视频，(4) 快速视频原型或草稿，(5) 一次性提示到视频生成，(6) 用户说「帮我做个视频」或「做一个关于 X 的视频」。
homepage: https://docs.heygen.com/reference/generate-video-agent
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# 创建视频

根据文本提示生成完整视频。描述你想要的内容，AI 会自动处理脚本撰写、avatar 选择、画面、旁白、节奏和字幕。

## 身份验证

所有请求都需要 `X-Api-Key` 请求头。请设置 `HEYGEN_API_KEY` 环境变量。

```bash
curl -X POST "https://api.heygen.com/v1/video_agent/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a 60-second product demo video."}'
```

## 工具选择

若可用 HeyGen MCP 工具（`mcp__heygen__*`），**优先使用**它们而非直接调用 HTTP API——它们会自动处理身份验证与请求格式。

| 任务 | MCP 工具 | 备选（直接 API） |
|------|----------|----------------------|
| 根据提示生成视频 | `mcp__heygen__generate_video_agent` | `POST /v1/video_agent/generate` |
| 检查视频状态 / 获取 URL | `mcp__heygen__get_video` | `GET /v2/videos/{video_id}` |
| 列出账户视频 | `mcp__heygen__list_videos` | `GET /v2/videos` |
| 删除视频 | `mcp__heygen__delete_video` | `DELETE /v2/videos/{video_id}` |

若没有 HeyGen MCP 工具，请按参考文件中的说明使用直接 HTTP API 调用。

## 默认工作流

始终使用 [prompt-optimizer.md](references/prompt-optimizer.md) 中的指南，用场景、时长和视觉风格来组织提示。

**使用 MCP 工具时：**
1. 按 [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) 撰写优化后的提示
2. 调用 `mcp__heygen__generate_video_agent`，传入提示与 config（duration_sec、orientation、avatar_id）
3. 用返回的 video_id 调用 `mcp__heygen__get_video`，轮询状态并获取下载 URL

**不使用 MCP 工具（直接 API）时：**
1. 按 [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) 撰写优化后的提示
2. `POST /v1/video_agent/generate` — 见 [video-agent.md](references/video-agent.md)
3. `GET /v2/videos/<id>` — 见 [video-status.md](references/video-status.md)

## 快速参考

| 任务 | MCP 工具 | 阅读 |
|------|----------|------|
| 根据提示生成视频 | `mcp__heygen__generate_video_agent` | [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) → [video-agent.md](references/video-agent.md) |
| 检查视频状态 / 获取下载 URL | `mcp__heygen__get_video` | [video-status.md](references/video-status.md) |
| 为提示上传参考文件 | — | [assets.md](references/assets.md) |

## 何时使用本技能 vs Avatar Video

本技能用于**基于提示的视频创建**——描述你想要的内容，由 AI 处理其余部分。

若用户需要**精确控制**特定 avatar、确切脚本、按场景的 voice/背景配置或多场景合成，请改用 **avatar-video** 技能。

| 用户说法 | 本技能 | Avatar Video 技能 |
|-----------|:----------:|:------------------:|
| 「帮我做一个关于 X 的视频」 | ✓ | |
| 「创建一个产品演示」 | ✓ | |
| 「我要 avatar Y 准确说出 Z」 | | ✓ |
| 「多场景、不同背景的视频」 | | ✓ |
| 「用于合成的透明 WebM」 | | ✓ |

## 参考文件

### 核心工作流
- [references/prompt-optimizer.md](references/prompt-optimizer.md) - 撰写有效提示（核心工作流与规则）
- [references/visual-styles.md](references/visual-styles.md) - 20 种命名视觉风格及完整规格
- [references/prompt-examples.md](references/prompt-examples.md) - 完整生产级提示示例与即用模板
- [references/video-agent.md](references/video-agent.md) - Video Agent API 端点详情

### 基础
- [references/video-status.md](references/video-status.md) - 轮询模式与下载 URL
- [references/webhooks.md](references/webhooks.md) - Webhook 端点与事件
- [references/assets.md](references/assets.md) - 上传图片、视频、音频作为参考
- [references/dimensions.md](references/dimensions.md) - 分辨率与宽高比
- [references/quota.md](references/quota.md) - 积分系统与使用限制

## 最佳实践

1. **优化你的提示** — 平庸与专业效果之间的差异完全取决于提示质量。始终使用提示优化器
2. **指定时长** — 使用 `config.duration_sec` 以获得可预期的长度
3. **需要时锁定 avatar** — 使用 `config.avatar_id` 以保持多段视频一致
4. **上传参考文件** — 帮助 agent 理解你的品牌/产品
5. **迭代提示** — 根据结果不断调整；Video Agent 非常适合快速迭代
