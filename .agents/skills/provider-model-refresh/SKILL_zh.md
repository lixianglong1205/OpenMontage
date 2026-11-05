---
name: provider-model-refresh
description: 使用 2026 年 9 月版的图像、视频、语音与 Avatar V 适配器，并遵循明确的 model/host 契约。
---

# 提供商模型更新

进行媒体制作时，请先遵循 AGENT_GUIDE.md 与所选流水线。
这些适配器可通过常规的 BaseTool 注册表发现。在发起请求前，请检查
其输入 schema 与状态。API 凭证仅表示已配置，并不表示已验证账户权益。不隐含任何付费线上测试。

## 路由

使用 `preferred_tool` 指定确切的适配器，使用 `hosting_provider` 指定
API 主机。`preferred_provider` 仍为遗留的排名偏好。为图像/视频选择确切的 `model`，
为语音选择确切的 `model_id`。若指定的确切模型不可用，必须失败，不得静默替换为其他模型。

| 模型 | 直接工具 | 聚合工具 |
| --- | --- | --- |
| GPT Image 2.5 Flare / Sunburst | openai_image | openai_fal_image, atlas_refresh_image |
| Gemini 3 Pro Image / Nano Banana Pro | google_imagen | gemini_fal_image, gemini_replicate_image, atlas_refresh_image |
| Ideogram 4.5 / Precise Edit | ideogram_image | ideogram_fal_image |
| Wan 3.0 | — | wan_fal_video, wan_atlas_video, wan_replicate_video |
| H3 Max | — | h3_max_video (fal) |
| LTX-2.5 Fast / Pro | ltx_api_video | — |
| Eleven v4 / v4 Turbo | elevenlabs_tts | fal_elevenlabs_tts (v4 only) |
| Gemini 3.8 Flash / Flash-Lite TTS | gemini_tts | — |
| Lyria 3.5 | google_music | — |
| Sonic 3.6 | cartesia_tts | — |
| Inworld TTS-2 / Flash | inworld_tts | — |
| Qwen Image 2.1 | qwen_image_21 (local) | — |
| HeyGen Avatar V | heygen_avatar | — |

## 图像请求

GPT Image 2.5 使用独立的 `gpt-image-2.5-flare` 与
`gpt-image-2.5-sunburst` ID。追求速度用 Flare，要求高保真编辑用 Sunburst。
说明要改什么、必须保留什么。直接编辑使用本地
`image_path`/`image_paths` 及可选的 `mask_path`。透明输出请保持 PNG 或
WebP。旧的 GPT Image 2 默认仍可用以保持兼容。

Google Pro 的确切 ID 为 `gemini-3-pro-image`；它与
`gemini-3.1-flash-image`（Nano Banana 2）不同。在支持的路由上最多可使用 14 张参考图，
以及 1K/2K/4K。Replicate 回退已禁用。

Ideogram 直接调用时 `generation_mode=precise_edit` 会保留未受影响像素；
先使用 `image_path`，再在 `image_paths` 中最多追加四张参考图。若带
mask，则最多只允许三张参考图。黑色表示编辑区域，白色表示保留。Precise
Edit 不能指定输出尺寸。`dry_run=true` 会校验并对该确切请求计价，但不生成。在 fal 上，`precise_edit` 会设置 `edit_precision=high`。

Qwen Image 2.1 需要真实的本地模型目录及兼容的
Diffusers。它不会隐式下载权重。请查阅 Qwen Research
License 以确认预期用途。透明生成会校验返回的 alpha 通道，而不是附加不透明 alpha 通道。

## 视频与任务

`operation` 选择 text_to_video、image_to_video 或 reference_to_video。
Replicate 上的 Wan 仅支持文本与首帧图像。Atlas 上的 Wan 使用
`refers` 对象，且 `duration=-1` 表示自动时长；fal 使用参考 URL
数组与可空 duration。不要在主机之间照搬原生参数。
将路由专用控制项传入 `provider_params`；`tools/provider_contracts` 下已检入的 schema 会在提交前校验完整请求。

LTX-2.5 支持文本/图像/音频生成，不支持 retake 或 extend。帧率为
24、25、48、50；长时长需使用 Fast，且为 720p/1080p 与 24/25 FPS。
`duration=null` 由模型选择长度，但不能与末帧同时使用。H3 Max 与旧版 H3 端点相互独立。

设置 `job_path` 以持久化检查点。超时后，将返回的
`resume_job` 传给同一工具；这会轮询既有任务，而不会再次付费提交。若无 ID 的提交超时则含义不明：在再次提交前请检查
提供商控制台。保留溯源与输出。
未知定价须明确报告，不得视为免费服务。

## 语音与音乐

Eleven 直接 ID 为 `eleven_v4` / `eleven_v4_turbo`；fal 使用 `eleven-v4`。
fal v4 最多接受 5,000 字符，且无 speed/style 控制。
直接 v4 最多接受 10,000。各主机的音色目录与权利不同。
Gemini TTS 使用带语音标注的 Interactions；请分别为每位对话
说话人配置 voice 与轮次文本。当前适配器输出 WAV。
Cartesia 使用 API 版本 2026-08-14 与 WAV。Inworld 使用门户签发的
Base64 凭证配合 Basic 认证，输出 MP3，且最多 2,000 个 UTF-16 码元。
Lyria 时长为提示目标，不保证精确时长。

## Avatar V

在 avatar-spokesperson 流水线中使用 `heygen_avatar`。先 `list_looks` 或
`inspect_look`；生成前会检查 `avatar_type=digital_twin` 与
`supported_api_engines` 再 POST。须显式以
`engine=avatar_v` 请求 Avatar V；不会回退到 IV。在
`script`（+ `voice_id`）、`audio_url`、`audio_asset_id` 中恰好提供其一。参考 look 必须是同一已验证组内的 digital twin。请使用已授权既有
演示者，并遵守 HeyGen 的同意/账户要求。

## 证据与限制

契约于 2026-10-03 检视；各 schema 记录其官方来源。
发布调研见 docs/provider-update-plan-2026-10-03.md。公开 Kling 4
生成端点仍未验证，因此不要臆造 model ID。实时语音
智能体需要独立于批量旁白的流式/会话集成。

## 10 月 23 日跟进

关于当前 Google 退役处理、Eleven v4 传输方式及新支持的
提供商，请阅读 [provider-refresh-oct23](../provider-refresh-oct23/SKILL.md)。
v4 旁白 HTTP 载荷为 dialogue inputs/settings，而非遗留 TTS
text/voice_settings；v4 Turbo 在直接文件适配器中仅支持 WebSocket。
