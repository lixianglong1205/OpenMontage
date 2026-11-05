---
name: text-to-speech
description: HeyGen 原生 Voice1 与目录语音、音色发现、时间戳与流式传输。
---

# HeyGen 语音

请使用已注册的工具，勿再使用已废弃的 /v1/audio 语音端点。

- `heygen_tts`：原生 HeyGen Voice1 / Turbo / Turbo Free。原生 ACTIVE 公开、
  即时或专业音色来自 `/v3/models/audio/voices`。专业音色需要 Voice1（非 Turbo）。
  输出为 44.1 kHz WAV；文本上限 5,000 字符。
- `heygen_catalog_tts`：目录音色来自 `/v3/voices`；在 `/v3/voices/speech` 上
  显式选择引擎（Starfish、HeyGen Voice 或 ElevenLabs）。这些 voice ID
  与原生 clone ID 不可互换。
- `heygen_voice_convert`：通过 `/v3/models/audio/sts` 使用 ACTIVE 即时
  工作区音色进行保留时长的转换。

阅读 [October23 提供商指南](../provider-refresh-oct23/SKILL.md) 了解当前
请求字段、输出路径、时间戳/SSE 处理、定价与重试行为。
勿在原生模型、目录引擎或主机之间静默降级。
Turbo Free 为促销至 2026 年 11 月 30 日，且有共享容量限制。

官方文档：
https://developers.heygen.com/docs/voices/heygen-voice-speech
https://developers.heygen.com/reference/generate-speech
https://developers.heygen.com/docs/voices/speech-to-speech
