---
name: text-to-speech
description: |
  使用 HeyGen 的 Starfish TTS 模型从文本生成语音音频。适用于：(1) 从文本生成独立语音音频文件，(2) 在可选音色、语速与音高下将文本转为语音，(3) 为旁白、解说或播客制作音频，(4) 使用 HeyGen 的 /v1/audio 端点，(5) 按语言或性别列出可用 TTS 音色。
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# 文本转语音（HeyGen Starfish）

使用 HeyGen 自研 Starfish TTS 模型从文本生成语音音频文件。本技能用于独立音频生成，与视频创建流程分离。

## 身份验证

所有请求需携带 `X-Api-Key` 请求头。请设置 `HEYGEN_API_KEY` 环境变量。

```bash
curl -X GET "https://api.heygen.com/v1/audio/voices" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## 工具选择

若可用 HeyGen MCP 工具（`mcp__heygen__*`），**优先使用 MCP**，而非直接调用 HTTP API。

| 任务 | MCP 工具 | 回退（直接 API） |
|------|----------|----------------------|
| 列出 TTS 音色 | `mcp__heygen__list_audio_voices` | `GET /v1/audio/voices` |
| 生成语音音频 | `mcp__heygen__text_to_speech` | `POST /v1/audio/text_to_speech` |

## 默认工作流

1. 使用 `mcp__heygen__list_audio_voices`（或 `GET /v1/audio/voices`）列出音色
2. 选择符合目标语言、性别与特性的音色
3. 调用 `mcp__heygen__text_to_speech`（或 `POST /v1/audio/text_to_speech`），传入文本与 `voice_id`
4. 使用返回的 `audio_url` 下载或播放音频

## 列出 TTS 音色

获取与 Starfish TTS 模型兼容的音色列表。

> **注意：** 此处使用 `GET /v1/audio/voices`，与视频音色 API（`GET /v2/voices`）不同。并非所有视频音色都支持 Starfish TTS。

### curl

```bash
curl -X GET "https://api.heygen.com/v1/audio/voices" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface TTSVoice {
  voice_id: string;
  language: string;
  gender: "female" | "male" | "unknown";
  name: string;
  preview_audio_url: string | null;
  support_pause: boolean;
  support_locale: boolean;
  type: string;
}

interface TTSVoicesResponse {
  error: null | string;
  data: {
    voices: TTSVoice[];
  };
}

async function listTTSVoices(): Promise<TTSVoice[]> {
  const response = await fetch("https://api.heygen.com/v1/audio/voices", {
    headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
  });

  const json: TTSVoicesResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.voices;
}
```

### Python

```python
import requests
import os

def list_tts_voices() -> list:
    response = requests.get(
        "https://api.heygen.com/v1/audio/voices",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]}
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]["voices"]
```

### 响应格式

```json
{
  "error": null,
  "data": {
    "voices": [
      {
        "voice_id": "f38a635bee7a4d1f9b0a654a31d050d2",
        "name": "Chill Brian",
        "language": "English",
        "gender": "male",
        "preview_audio_url": "https://resource.heygen.ai/text_to_speech/WpSDQvmLGXEqXZVZQiVeg6.mp3",
        "support_pause": true,
        "support_locale": false,
        "type": "public"
      }
    ]
  }
}
```

## 生成语音音频

使用指定音色将文本转换为语音音频。

### 端点

`POST https://api.heygen.com/v1/audio/text_to_speech`

### 请求字段

| 字段 | 类型 | 必填 | 说明 |
|-------|------|:---:|-------------|
| `text` | string | Y | 要转换为语音的文本内容 |
| `voice_id` | string | Y | 来自 `GET /v1/audio/voices` 的音色 ID |
| `speed` | number | | 语速，0.5–1.5（默认：1） |
| `pitch` | integer | | 音高，-50 至 50（默认：0） |
| `locale` | string | | 多语言音色的口音/区域（例如 `en-US`、`pt-BR`） |
| `elevenlabs_settings` | object | | ElevenLabs 音色的高级设置 |

### ElevenLabs 设置（可选）

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `model` | string | 模型选择（`eleven_v3`、`eleven_turbo_v2_5` 等） |
| `similarity_boost` | number | 音色相似度，0.0–1.0 |
| `stability` | number | 输出一致性，0.0–1.0 |
| `style` | number | 风格强度，0.0–1.0 |

### curl

```bash
curl -X POST "https://api.heygen.com/v1/audio/text_to_speech" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello! Welcome to our product demo.",
    "voice_id": "YOUR_VOICE_ID",
    "speed": 1.0
  }'
```

### TypeScript

```typescript
interface TTSRequest {
  text: string;
  voice_id: string;
  speed?: number;
  pitch?: number;
  locale?: string;
  elevenlabs_settings?: {
    model?: string;
    similarity_boost?: number;
    stability?: number;
    style?: number;
  };
}

interface WordTimestamp {
  word: string;
  start: number;
  end: number;
}

interface TTSResponse {
  error: null | string;
  data: {
    audio_url: string;
    duration: number;
    request_id: string;
    word_timestamps: WordTimestamp[];
  };
}

async function textToSpeech(request: TTSRequest): Promise<TTSResponse["data"]> {
  const response = await fetch(
    "https://api.heygen.com/v1/audio/text_to_speech",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  const json: TTSResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data;
}
```

### Python

```python
import requests
import os

def text_to_speech(
    text: str,
    voice_id: str,
    speed: float = 1.0,
    pitch: int = 0,
    locale: str | None = None,
) -> dict:
    payload = {
        "text": text,
        "voice_id": voice_id,
        "speed": speed,
        "pitch": pitch,
    }

    if locale:
        payload["locale"] = locale

    response = requests.post(
        "https://api.heygen.com/v1/audio/text_to_speech",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json=payload,
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]
```

### 响应格式

```json
{
  "error": null,
  "data": {
    "audio_url": "https://resource2.heygen.ai/text_to_speech/.../id=365d46bb.wav",
    "duration": 5.526,
    "request_id": "p38QJ52hfgNlsYKZZmd9",
    "word_timestamps": [
      { "word": "<start>", "start": 0.0, "end": 0.0 },
      { "word": "Hey", "start": 0.079, "end": 0.219 },
      { "word": "there,", "start": 0.239, "end": 0.459 },
      { "word": "<end>", "start": 5.526, "end": 5.526 }
    ]
  }
}
```

## 使用示例

### 基础 TTS

```typescript
const result = await textToSpeech({
  text: "Welcome to our quarterly earnings call.",
  voice_id: "YOUR_VOICE_ID",
});

console.log(`Audio URL: ${result.audio_url}`);
console.log(`Duration: ${result.duration}s`);
```

### 调整语速

```typescript
const result = await textToSpeech({
  text: "We're thrilled to announce our newest feature!",
  voice_id: "YOUR_VOICE_ID",
  speed: 1.1,
});
```

### 多语言音色的 locale

```typescript
const result = await textToSpeech({
  text: "Bem-vindo ao nosso produto.",
  voice_id: "MULTILINGUAL_VOICE_ID",
  locale: "pt-BR",
});
```

### 查找音色并生成音频

```typescript
async function generateSpeech(text: string, language: string): Promise<string> {
  const voices = await listTTSVoices();
  const voice = voices.find(
    (v) => v.language.toLowerCase().includes(language.toLowerCase())
  );

  if (!voice) {
    throw new Error(`No TTS voice found for language: ${language}`);
  }

  const result = await textToSpeech({
    text,
    voice_id: voice.voice_id,
  });

  return result.audio_url;
}

const audioUrl = await generateSpeech("Hello and welcome!", "english");
```

## 使用 Break 标签插入停顿

在文本中使用 SSML 风格的 break 标签控制停顿：

```
word <break time="1s"/> word
```

规则：
- 使用带 `s` 后缀的秒数：`<break time="1.5s"/>`
- 标签前后必须有空格
- 使用自闭合标签格式

## 表现力与旁白指导

制作旁白时，在生成音频前先写一份简短的「配音表演」计划：

- 旁白人设与情感意图
- 节奏轮廓
- 全稿能量曲线
- 停顿应落在何处
- 需要强调的词语或短语

使用具体提示，避免空泛指令。例如「温暖但果断；在对比句前停顿；最后一句放慢」是有用的；「听起来自然」则不够。

若所选音色支持停顿，用 break 标签把最重要的停顿直接写进文本。先对表演最密集的片段生成样本；若样本听起来平淡、仓促或未按预期停顿，不要批量生成剩余部分。

## 最佳实践

1. **使用 `GET /v1/audio/voices`** 查找兼容音色——并非 `GET /v2/voices` 中的全部音色都支持 Starfish TTS
2. **设置 `locale` 前先查看 `support_locale`**——仅多语言音色支持区域选择
3. **语速保持在 0.8–1.2** 以获得更自然的效果
4. **生成前用 `preview_audio_url` 试听音色**（部分音色可能为 null）
5. **使用响应中的 `word_timestamps`** 做字幕同步或定时文字叠加
6. **在文本中使用 SSML break 标签** 控制停顿：`word <break time="1s"/> word`
