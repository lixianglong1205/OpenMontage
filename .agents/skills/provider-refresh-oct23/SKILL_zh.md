---
name: provider-refresh-oct23
description: 2026 年 10 月 23 日供应商刷新后的 API 契约与生产路由说明。
---

# 2026 年 10 月 23 日供应商集成

使用前请先阅读该工具的当前输入 schema。在生产环境调用前，须声明工具、宿主、精确模型、操作及报价费用。禁止自动切换宿主/模型。生产项目下须使用显式输出路径。仅配置凭证并不等同于已建立账户访问权限。多数新价格需向账户重新询价；勿将已过期的促销价当作永久价格。

## Google 与 ElevenLabs 迁移

- `gemini_omni_video`：直连 Gemini Interactions API 的模型为
  `gemini-omni-1.1-flash`。旧预览版于 10 月 22 日退役。编辑时继续使用
  `previous_interaction_id`；勿在 Veo 请求中将其替换为其他字段。
- `veo_video`：Google 后端要求 Vertex；fal 保留其自有契约。
  Gemini API 上的 Veo 已退役。替代工作流须显式选择 Omni。
- `google_imagen`：新默认 `gemini-nano-banana-2.1`；Imagen 模型需
  Vertex。原生 Gemini 图像模型使用 generate_content，而非 Imagen predict。
- `elevenlabs_tts`：`eleven_v4` 使用 HTTP Text to Dialogue，含 `inputs` 与
  `settings`。单次旁白请求保持 <=2,000 字符。`next_text` 映射为
  `future_text`；上下文字符串 <=100 字符。风格/语速/speaker boost 不属于对话设置。`eleven_v4_turbo` 使用 dialogue WebSocket；本文件适配器不支持 Turbo 的时间戳或连续性控制。它等待全局 `is_final`，而非逐轮标记。当前官方 realtime 教程文档写的是 Turbo，尽管较旧的 WebSocket 参考仍写仅 v3。

## 旁白与转换

- `heygen_tts`：model_id 为 `heygen-voice-1`、`heygen-voice-1-turbo` 或
  `heygen-voice-1-turbo-free`。须传入 ACTIVE 的原生 public/workspace 音色 ID；
  `operation=list_voices` 可发现原生音色。专业克隆仅非 Turbo 模型可用。`voice_type` 可预校验类别；服务会校验实际归属/状态。完成的语音与 SSE 均写入 WAV。
  SSE 分片为独立 WAV 容器，组装前先解码。时间戳生成 alignment 侧车文件与 word_timestamps。免费访问至 2026 年 11 月 30 日结束；失败不会自动切到付费。速率拒绝的重试有上限，并遵守较短 Retry-After；更长延迟会返回给调用方。
- `heygen_catalog_tts`：独立 catalog ID，`/v3/voices/speech`；须显式选择
  `engine`（starfish、heygen_voice、elevenlabs）。原生专业克隆 ID 不属于此路径。Catalog 输出可为 MP3 或 WAV。可指定任一后缀；返回的 artifact
  路径使用实际响应 codec 后缀并保留音频。
- `heygen_voice_convert`：仅 ACTIVE 的 instant workspace 音色，最长 300 秒。
  恰好一个 audio_path（<=16 MB）、audio_url 或 asset_id。输出 WAV。若在超时状态不明后恢复，请提供稳定的 idempotency_key；无自动重试。
- `grok_tts`：xAI 旁白 `/v1/tts`，非 Grok Voice realtime。默认 `language=auto`，
  voice_id 默认为 eve；list_voices 可发现音色。output_format
  为对象，例如 {"codec":"wav","sample_rate":24000}；本文件适配器暴露 MP3/WAV，不含无头电话 codec。可选保存字符对齐。
- `mistral_tts`：model_id `voxtral-mini-tts-3-0`；恰好一个 voice_id 或本地
  reference_audio_path。mp3/wav/flac/opus。支持内联 emotion/pace 标签与 expressiveness；
  发布时不支持自由格式风格指令。不宣称 realtime TTS。
- `mai_tts`：Azure Speech key/region，model_id MAI-Voice-2.1 或 MAI-Voice-2.1-Flash。
  voice_id 为托管音色基名，如 en-US-Harper（模型后缀会自动追加）。
  TTS 选择器通过 Azure SSML 适配器转换 speed 与 pitch。
  本适配器不开通个人音色克隆，也不授予门控访问。
- `mistral_stt`：Voxtral Mini/Small Transcribe3，本地音频文件；时间戳为
  分段级，非词级。说话人分离隐含分段时间戳。原始转写 JSON 会持久化，含说话人与 usage 元数据。
- `elevenlabs_soundtrack`：video_paths（<=10，合计 <=200 MB / 600 秒），
  可选 description/tags、add_sfx/use_audio_as_reference/separate_tracks。分轨
  在同级 *_tracks 目录返回可播放文件；切勿将 ZIP 当作音频文件。适配器会拒绝不安全的归档路径与超大归档。

## 图像与视频

| 模型 | 显式工具 / 宿主 |
|---|---|
| Nano Banana2.1 | google_imagen, gemini_fal_image, gemini_replicate_image |
| FLUX3 Image | bfl_image, flux3_fal_image, flux3_replicate_image |
| FLUX3 Max video | flux3_video (fal) |
| Vidu Q4 | vidu_video (fal)，image_to_video 或 reference_to_video；无纯文本路由 |
| Fibo2 | bria_image 直连或 bria_fal_image |
| MAI Image2.6 / Flash | mai_image，已部署的 Foundry 模型 |
| Grok Imagine1.5 / Lite | grok_video 直连 xAI |

fal 与 Replicate 在 tools/provider_contracts 下有检入的 endpoint schema。
仅在该宿主文档允许时传入 provider_params。勿将 fal 字段复制到
Replicate 或直连 API。聚合器上现有 Pro 图像模型默认不变；新模型须显式选择。

BFL 边界框布局按 BFL 文档编码在 prompt 中，而非虚构的
`boxes` endpoint 字段。BFL 最多支持 10 张参考图；width/height 须同时提供。其 API 参考优先于较旧的叙述性示例。
Bria 持久化结构化元数据供后续编辑。其共享 endpoint 可将部分旧组合路由到旧 Fibo 模型；在宣传 Fibo2 时，直连工具会拒绝那些组合。MAI 要求模型身份与已部署配置一致；PNG 输出且 <=2,359,296 像素，每边 >=768。

Grok1.5 参考素材限于 720p。Lite 无参考音频、参考图、
last_frame 或 keyframes。完整 1.5 支持预设音色参考；自定义音频参考仍为 partner 门控。视频中段 pin 须在时长内且占用不同的 1/3 秒槽位。失败时不做模型替换。fal/Replicate/BFL/Grok
任务暴露 resume 元数据；轮询前保存 job_path，恢复 pending 任务而非重复提交付费生成。

## Realtime 与旁白分离

`realtime_audio` 是针对 Grok Voice3、
Eleven Realtime Mini/Max 与 MAI-Transcribe-2-Streaming 的有界单次响应文件运行器。输入为文本或 mono PCM16
WAV（16/24kHz；Eleven 要求 24kHz）。语音输出为 WAV；MAI 输出为 event JSON。
发送输入与接收事件并发执行。MAI 显式 commit 并
等待最终转写，而非 commit 确认。Eleven 使用临时
会话凭证，并对录制文件采用突发式输入 pacing。

对于实时音频、VAD、打断、多轮或 function call，请使用
上下文管理的 `tools.audio._realtime_session.RealtimeAudioSession` 传输层：
`append_audio`、`commit`、`receive`、`request_response`、`cancel`、以及
`submit_tool_result`。调用方拥有会话生命周期与工具审批。
收到的 tool call 绝不会自动执行。有限文件运行器
因关闭 socket 后无法继续而拒绝 tools。该传输层不隐含麦克风
UI、浏览器应用或 voice-agent 编排。
密钥仅保留在内存中。未新增 realtime 翻译或 Kling4 支持。

## 主要参考

- https://ai.google.dev/gemini-api/docs/deprecations
- https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert
- https://elevenlabs.io/docs/eleven-api/guides/how-to/websockets/realtime-tdd
- https://elevenlabs.io/docs/api-reference/music/video-to-music
- https://developers.heygen.com/docs/voices/heygen-voice-speech
- https://developers.heygen.com/docs/voices/speech-to-speech
- https://developers.heygen.com/reference/generate-speech
- https://docs.x.ai/developers/model-capabilities/audio/text-to-speech
- https://docs.x.ai/developers/model-capabilities/video/overview
- https://docs.mistral.ai/studio/audio/overview
- https://docs.bfl.ml/api-reference/utility/generate-an-image-with-flux-3
- https://docs.bria.ai/whats-new/fibo-2
- https://learn.microsoft.com/azure/ai-services/speech-service/mai-voices
- https://learn.microsoft.com/azure/foundry/foundry-models/how-to/use-foundry-models-mai-image
- https://learn.microsoft.com/azure/ai-services/speech-service/mai-transcribe-2-streaming-realtime
- https://elevenlabs.io/docs/eleven-agents/guides/openai-realtime-compatibility
- https://docs.x.ai/developers/rest-api-reference/inference/voice
