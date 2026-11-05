---
name: dashscope
description: DashScope（阿里云百炼）集成 — 图像生成（qwen-image-2.0-pro）、文本转语音（qwen3-tts-flash），以及带词级时间戳的 ASR（qwen3-asr-flash-filetrans）。在通过 Qwen-Image 生成图像、通过 Qwen-TTS 旁白，或通过 Qwen-ASR 转写并获取词级时间戳时使用。
---

# DashScope

需要在 `.env` 中配置 `DASHSCOPE_API_KEY`。在 https://dashscope.aliyun.com/ 获取。

## 当前 API

**关键：** DashScope 的 `/compatible-mode/v1/` 仅支持 `/chat/completions` 与 `/embeddings`。图像生成、TTS 与 ASR 均使用 **DashScope 原生端点** — 而非 OpenAI 兼容路径。

三个工具均使用 `Authorization: Bearer $DASHSCOPE_API_KEY`。

### 图像生成

```text
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

- Model: `qwen-image-2.0-pro` (default), `qwen-image-max`, `wan2.7-image`, `z-image-turbo`
- Body: `{model, input: {messages: [{role: "user", content: [{text: "prompt"}]}]}, parameters: {size: "W*H", n, prompt_extend, watermark}}`
- **尺寸格式使用星号：** `"1024*1024"` 而非 `"1024x1024"`
- Response: `output.choices[0].message.content[0].image`（URL，约 24 小时有效）— 需单独下载

### 文本转语音

```text
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

与图像生成同一端点，请求体不同。

- Model: `qwen3-tts-flash` (default), `qwen3-tts-instruct-flash`, `qwen-tts-2025-05-22`
- Body: `{model, input: {text, voice: "Cherry", language_type: "Auto"}}`
- Response: `output.audio.url`（WAV，约 24 小时有效）— 需单独下载

### 带词级时间戳的 ASR

```text
POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription
Header: X-DashScope-Async: enable
```

- Model: `qwen3-asr-flash-filetrans`（**不是** `qwen3-asr-flash` — 同步版无词级时间戳）
- Body: `{model, input: {file_url: "https://public-url/audio.mp3"}, parameters: {enable_words: true, language_hints: ["zh","en"]}}`
- 返回 `task_id` → 轮询 `GET /api/v1/tasks/{task_id}` 直至 `SUCCEEDED` → 下载 `output.result.transcription_url` → JSON 含 `transcripts[].sentences[].words[]`
- `begin_time`/`end_time` 时间戳单位为 **毫秒** — 工具会规范化为秒

## OpenMontage 用法

### 通过 selector 生成图像

```python
from tools.graphics.image_selector import ImageSelector

result = ImageSelector().execute({
    "preferred_provider": "dashscope",
    "prompt": "一只猫坐在沙发上",
    "output_path": "projects/my-video/assets/images/cat.png",
})
```

### 通过 selector 进行 TTS

```python
from tools.audio.tts_selector import TTSSelector

result = TTSSelector().execute({
    "preferred_provider": "dashscope",
    "text": "如果 AI 真的会改变未来，普通人到底该怎么参与？",
    "voice": "Cherry",
    "output_path": "projects/my-video/assets/audio/narration.wav",
})
```

### 直接调用 ASR（词级时间戳用于字幕）

```python
from tools.analysis.dashscope_asr import DashscopeAsr

result = DashscopeAsr().execute({
    "audio_url": "https://example.com/narration.wav",
    "output_path": "projects/my-video/assets/audio/transcription.json",
})

# result.data["words"] is a flat list of {text, begin_time_seconds, end_time_seconds}
```

## 推荐工作流

1. **Image：** 先生成样片。注意 `prompt_extend: true`（默认）— DashScope 会改写提示词以提升效果。若需严格按字面提示词生成，请关闭。
2. **TTS：** 在完整旁白前先生成 10–15 秒样片。确认音色与节奏后再做全长生成。
3. **ASR：** 音频须为 **可公开访问的 URL**。先上传到任意公开托管（如 S3 等）。本地路径会被拒绝并返回明确错误。
4. **Subtitles：** 由 `result.data["words"]` 构建 — 每个词含 `begin_time_seconds` 与 `end_time_seconds`。按语言语义将词分组为字幕短语，而非固定字符数。

## 参数

### Image (`dashscope_image`)
- `prompt` (required): 文本提示词
- `model`: 默认 `qwen-image-2.0-pro`
- `size`: 默认 `"1024*1024"` — **星号分隔，不是 "x"**
- `n`: 1–6 张图
- `negative_prompt`: 需避免的内容（最多 500 字符）
- `prompt_extend`: 默认 `true` — 自动改写提示词以提升效果
- `watermark`: 默认 `false`
- `seed`: 用于可复现性

### TTS (`dashscope_tts`)
- `text` (required): 待合成文本（qwen3-tts-flash 最多 600 字符）
- `model`: 默认 `qwen3-tts-flash`
- `voice`: 默认 `"Cherry"` — 其他音色：`"Ethan"`、`"Chelsie"` 等
- `language_type`: 默认 `"Auto"` — `"Chinese"`、`"English"`、`"Japanese"`、`"Korean"`
- `instructions`: 自然语言表达/风格说明（仅 `qwen3-tts-instruct-flash`）

### ASR (`dashscope_asr`)
- `audio_url` (required): **须为可公开访问的 URL**
- `model`: `qwen3-asr-flash-filetrans`（唯一支持词级时间戳的模型）
- `language_hints`: 默认 `["zh", "en"]`
- `enable_words`: 默认 `true` — 词级时间戳必需
- `poll_interval_seconds`: 默认 `5.0`
- `timeout_seconds`: 默认 `300`

## 故障排查

- **Image size error:** 使用星号的 `"W*H"`，不要用 `"WxH"`。示例：`"2048*2048"`。
- **TTS no audio URL:** 检查 `output.audio.url` — 若为空，模型名或音色可能不正确。
- **ASR "file not accessible":** `audio_url` 须可被公网访问。DashScope 服务器会拉取文件；本地路径与需鉴权的 URL 不可用。
- **ASR poll timeout:** 增大 `timeout_seconds`（默认 300）。长音频转写耗时更长。
- **ASR no word timestamps:** 确保 `enable_words: true` 且模型为 `qwen3-asr-flash-filetrans`（不要用同步版 `qwen3-asr-flash`）。
- **Auth error (401):** 确认已设置 `DASHSCOPE_API_KEY`。使用 `Authorization: Bearer $KEY` 请求头。

## 安全

切勿将 API key 打印或写入日志、元数据、补丁或项目产物。`.env.example` 应只包含空的变量名。工具的 `_safe_error()` 方法会从错误信息中脱敏 key。
