---
name: speech-to-text
description: 使用 ElevenLabs Scribe v2 将音频转写为文本。适用于将音频/视频转为文字、生成字幕、会议转录或处理口语内容。
license: MIT
compatibility: 需要互联网访问以及 ElevenLabs API 密钥（ELEVENLABS_API_KEY）。
metadata: {"openclaw": {"requires": {"env": ["ELEVENLABS_API_KEY"]}, "primaryEnv": "ELEVENLABS_API_KEY"}}
---

# ElevenLabs 语音转文字

使用 Scribe v2 将音频转写为文本——支持 90 多种语言、说话人分离（speaker diarization）以及词级时间戳。

> **设置：** 参见[安装指南](references/installation.md)。在 JavaScript 中请仅使用 `@elevenlabs/*` 包。

## 快速开始

### Python

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

with open("audio.mp3", "rb") as audio_file:
    result = client.speech_to_text.convert(file=audio_file, model_id="scribe_v2")

print(result.text)
```

### JavaScript

```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { createReadStream } from "fs";

const client = new ElevenLabsClient();
const result = await client.speechToText.convert({
  file: createReadStream("audio.mp3"),
  modelId: "scribe_v2",
});
console.log(result.text);
```

### cURL

```bash
curl -X POST "https://api.elevenlabs.io/v1/speech-to-text" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -F "file=@audio.mp3" -F "model_id=scribe_v2"
```

## 模型

| Model ID | 说明 | 适用场景 |
|----------|-------------|----------|
| `scribe_v2` | 业界领先的准确率，支持 90+ 语言 | 批量转录、字幕、长音频 |
| `scribe_v2_realtime` | 低延迟（约 150ms） | 实时转录、语音智能体 |

## 带时间戳的转录

词级时间戳包含类型分类与说话人识别：

```python
result = client.speech_to_text.convert(
    file=audio_file, model_id="scribe_v2", timestamps_granularity="word"
)

for word in result.words:
    print(f"{word.text}: {word.start}s - {word.end}s (type: {word.type})")

```

## 说话人分离

识别「谁说了什么」——模型为每个词标注说话人 ID，适用于会议、访谈或任意多说话人音频：

```python
result = client.speech_to_text.convert(
    file=audio_file,
    model_id="scribe_v2",
    diarize=True
)

for word in result.words:
    print(f"[{word.speaker_id}] {word.text}")
```

## 关键词提示（Keyterm Prompting）

帮助模型识别可能听错的特定词汇——产品名、专业术语或特殊拼写（最多 100 个词）：

```python
result = client.speech_to_text.convert(
    file=audio_file,
    model_id="scribe_v2",
    keyterms=["ElevenLabs", "Scribe", "API"]
)
```

## 语言检测

自动检测，并可选提供语言提示：

```python
result = client.speech_to_text.convert(
    file=audio_file,
    model_id="scribe_v2",
    language_code="eng"  # ISO 639-1 or ISO 639-3 code
)

print(f"Detected: {result.language_code} ({result.language_probability:.0%})")
```

## 支持的格式

**音频：** MP3、WAV、M4A、FLAC、OGG、WebM、AAC、AIFF、Opus  
**视频：** MP4、AVI、MKV、MOV、WMV、FLV、WebM、MPEG、3GPP

**限制：** 单文件最大 3GB，最长 10 小时

## 响应格式

```json
{
  "text": "The full transcription text",
  "language_code": "eng",
  "language_probability": 0.98,
  "words": [
    {"text": "The", "start": 0.0, "end": 0.15, "type": "word", "speaker_id": "speaker_0"},
    {"text": " ", "start": 0.15, "end": 0.16, "type": "spacing", "speaker_id": "speaker_0"}
  ]
}
```

**词类型：**
- `word` - 实际说出的词
- `spacing` - 词与词之间的空白（用于精确计时）
- `audio_event` - 模型检测到的非语音声音（笑声、掌声、音乐等）

## 错误处理

```python
try:
    result = client.speech_to_text.convert(file=audio_file, model_id="scribe_v2")
except Exception as e:
    print(f"Transcription failed: {e}")
```

常见错误：
- **401**：API 密钥无效
- **422**：参数无效
- **429**：超出速率限制

## 费用追踪

通过响应头 `request-id` 监控用量：

```python
response = client.speech_to_text.convert.with_raw_response(file=audio_file, model_id="scribe_v2")
result = response.parse()
print(f"Request ID: {response.headers.get('request-id')}")
```

## 实时流式转录

需要极低延迟（约 150ms）的实时转录时，请使用实时 API。实时 API 会产出两类转录结果：

- **部分转录（Partial transcripts）**：音频处理过程中频繁更新的 interim 结果——用于实时反馈（例如用户说话时即时显示文字）
- **已提交转录（Committed transcripts）**：在你「提交（commit）」之后的最终、稳定结果——作为应用的权威文本来源

「提交（commit）」会指示模型定稿当前片段。你可以手动提交（例如用户停顿时），或使用语音活动检测（VAD）在静音时自动提交。

### Python（服务端）

```python
import asyncio
from elevenlabs import ElevenLabs

client = ElevenLabs()

async def transcribe_realtime():
    async with client.speech_to_text.realtime.connect(
        model_id="scribe_v2_realtime",
        include_timestamps=True,
    ) as connection:
        await connection.stream_url("https://example.com/audio.mp3")

        async for event in connection:
            if event.type == "partial_transcript":
                print(f"Partial: {event.text}")
            elif event.type == "committed_transcript":
                print(f"Final: {event.text}")

asyncio.run(transcribe_realtime())
```

### JavaScript（客户端 + React）

```typescript
import { useScribe, CommitStrategy } from "@elevenlabs/react";

function TranscriptionComponent() {
  const [transcript, setTranscript] = useState("");

  const scribe = useScribe({
    modelId: "scribe_v2_realtime",
    commitStrategy: CommitStrategy.VAD, // Auto-commit on silence for mic input
    onPartialTranscript: (data) => console.log("Partial:", data.text),
    onCommittedTranscript: (data) => setTranscript((prev) => prev + data.text),
  });

  const start = async () => {
    // Get token from your backend (never expose API key to client)
    const { token } = await fetch("/scribe-token").then((r) => r.json());

    await scribe.connect({
      token,
      microphone: { echoCancellation: true, noiseSuppression: true },
    });
  };

  return <button onClick={start}>Start Recording</button>;
}
```

### 提交策略

| 策略 | 说明 |
|----------|-------------|
| **Manual** | 在合适时机调用 `commit()`——适用于文件处理或你控制音频片段的场景 |
| **VAD** | 语音活动检测在检测到静音时自动提交——适用于实时麦克风输入 |

```typescript
// React: set commitStrategy on the hook (recommended for mic input)
import { useScribe, CommitStrategy } from "@elevenlabs/react";

const scribe = useScribe({
  modelId: "scribe_v2_realtime",
  commitStrategy: CommitStrategy.VAD,
  // Optional VAD tuning:
  vadSilenceThresholdSecs: 1.5,
  vadThreshold: 0.4,
});
```

```javascript
// JavaScript client: pass vad config on connect
const connection = await client.speechToText.realtime.connect({
  modelId: "scribe_v2_realtime",
  vad: {
    silenceThresholdSecs: 1.5,
    threshold: 0.4,
  },
});
```

### 事件类型

| 事件 | 说明 |
|-------|-------------|
| `partial_transcript` | 实时 interim 结果 |
| `committed_transcript` | 提交后的最终结果 |
| `committed_transcript_with_timestamps` | 带词级时间的最终结果 |
| `error` | 发生错误 |

完整文档请参阅实时相关参考。

## 参考

- [安装指南](references/installation.md)
- [转录选项](references/transcription-options.md)
- [实时客户端流式传输](references/realtime-client-side.md)
- [实时服务端流式传输](references/realtime-server-side.md)
- [提交策略](references/realtime-commit-strategies.md)
- [实时事件参考](references/realtime-events.md)
