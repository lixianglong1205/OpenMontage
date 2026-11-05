---
name: avatar-video
description: |
  使用 HeyGen v2 API 精确控制数字人、语音、脚本、场景与背景，创建 AI 数字人视频。适用场景：(1) 为视频选定特定数字人与语音，(2) 编写数字人要说的精确脚本，(3) 构建每场景背景不同的多场景视频，(4) 创建用于合成的透明 WebM 视频，(5) 使用会说话的照片作为视频主讲人，(6) 将 HeyGen 数字人与 Remotion 集成，(7) 按精确规格批量生成视频，(8) 品牌一致、可控的生产级视频。
homepage: https://docs.heygen.com/reference/create-a-video
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# 数字人视频（Avatar Video）

使用 HeyGen 的 `/v2/video/generate` API，完全控制数字人、语音、脚本、场景与背景，按精确配置构建单场景或多场景 AI 数字人视频。

## 身份验证

所有请求需要 `X-Api-Key` 请求头。请设置 `HEYGEN_API_KEY` 环境变量。

```bash
curl -X GET "https://api.heygen.com/v2/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## 工具选择

若可用 HeyGen MCP 工具（`mcp__heygen__*`），**优先使用**它们而非直接 HTTP API 调用——它们会自动处理身份验证与请求格式。

| 任务 | MCP 工具 | 备选（直接 API） |
|------|----------|----------------------|
| 检查视频状态 / 获取 URL | `mcp__heygen__get_video` | `GET /v2/videos/{video_id}` |
| 列出账户视频 | `mcp__heygen__list_videos` | `GET /v2/videos` |
| 删除视频 | `mcp__heygen__delete_video` | `DELETE /v2/videos/{video_id}` |

视频生成（`POST /v2/video/generate`）以及数字人/语音列表需通过直接 API 调用完成——见下方参考文件。

## 默认工作流

1. **列出数字人** — `GET /v2/avatars` → 选择数字人、预览，记录 `avatar_id` 与 `default_voice_id`。见 [avatars.md](references/avatars.md)
2. **列出语音**（如需要）— `GET /v2/voices` → 选择与数字人性别/语言匹配的语音。见 [voices.md](references/voices.md)
3. **编写脚本** — 按场景组织，每场景一个概念。见 [scripts.md](references/scripts.md)
4. **生成视频** — `POST /v2/video/generate`，为每场景配置数字人、语音、脚本与背景。见 [video-generation.md](references/video-generation.md)
5. **轮询直至完成** — `GET /v2/videos/{video_id}`，直到状态为 `completed`。见 [video-status.md](references/video-status.md)

## 快速参考

| 任务 | 阅读 |
|------|------|
| 列出并预览数字人 | [avatars.md](references/avatars.md) |
| 列出并选择语音 | [voices.md](references/voices.md) |
| 编写与组织脚本 | [scripts.md](references/scripts.md) |
| 生成视频（单场景或多场景） | [video-generation.md](references/video-generation.md) |
| 添加自定义背景 | [backgrounds.md](references/backgrounds.md) |
| 添加字幕 / 说明文字 | [captions.md](references/captions.md) |
| 添加文字叠加层 | [text-overlays.md](references/text-overlays.md) |
| 创建透明 WebM 视频 | [video-generation.md](references/video-generation.md)（WebM 章节） |
| 使用模板 | [templates.md](references/templates.md) |
| 从照片创建数字人 | [photo-avatars.md](references/photo-avatars.md) |
| 检查视频状态 / 下载 | [video-status.md](references/video-status.md) |
| 上传素材（图片、音频） | [assets.md](references/assets.md) |
| 与 Remotion 配合使用 | [remotion-integration.md](references/remotion-integration.md) |
| 配置 Webhook | [webhooks.md](references/webhooks.md) |

## 何时使用本技能 vs Create Video

本技能用于**精确控制**——由你选择数字人、编写精确脚本、配置每个场景。

若用户只想**描述视频创意**并由 AI 处理其余部分（脚本、数字人、画面），请改用 **create-video** 技能。

| 用户说法 | Create Video 技能 | 本技能 |
|-----------|:------------------:|:----------:|
| 「帮我做一段关于 X 的视频」 | ✓ | |
| 「创建产品演示」 | ✓ | |
| 「我要数字人 Y 准确说出 Z」 | | ✓ |
| 「多场景、每场景不同背景的视频」 | | ✓ |
| 「用于合成的透明 WebM」 | | ✓ |
| 「用我的脚本指定这条语音」 | | ✓ |
| 「按精确规格批量生成视频」 | | ✓ |

## 参考文件

### 核心视频创建
- [references/avatars.md](references/avatars.md) - 列出数字人、风格、`avatar_id` 选择
- [references/voices.md](references/voices.md) - 列出语音、区域、语速/音高
- [references/scripts.md](references/scripts.md) - 编写脚本、停顿、节奏
- [references/video-generation.md](references/video-generation.md) - `POST /v2/video/generate` 与多场景视频

### 视频定制
- [references/backgrounds.md](references/backgrounds.md) - 纯色、图片、视频背景
- [references/text-overlays.md](references/text-overlays.md) - 添加文字、字体与定位
- [references/captions.md](references/captions.md) - 自动生成字幕与说明文字

### 高级功能
- [references/templates.md](references/templates.md) - 模板列表与变量替换
- [references/photo-avatars.md](references/photo-avatars.md) - 从照片创建数字人
- [references/webhooks.md](references/webhooks.md) - Webhook 端点与事件

### 集成
- [references/remotion-integration.md](references/remotion-integration.md) - 在 Remotion 合成中使用 HeyGen

### 基础
- [references/video-status.md](references/video-status.md) - 轮询模式与下载 URL
- [references/assets.md](references/assets.md) - 上传图片、视频、音频
- [references/dimensions.md](references/dimensions.md) - 分辨率与宽高比
- [references/quota.md](references/quota.md) - 积分系统与用量限制

## 最佳实践

1. **生成前先预览数字人** — 下载 `preview_image_url`，让用户在提交前看到数字人效果
2. **使用数字人默认语音** — 多数数字人有预匹配的 `default_voice_id`，效果更自然
3. **备选：手动匹配性别** — 若无默认语音，确保数字人与语音性别一致
4. **开发时使用测试模式** — 设置 `test: true` 以免消耗积分（输出会带水印）
5. **设置充足超时** — 视频生成常需 5–15 分钟，有时更长
6. **校验输入** — 生成前确认数字人与语音 ID 存在
