---
name: sound-effects
description: 使用 ElevenLabs 根据文本描述生成音效。适用于创建音效、生成音频纹理、制作环境声、电影冲击声、UI 音效，或任何非语音类音频。支持循环、时长控制与提示词影响度调节。
license: MIT
compatibility: 需要互联网访问及 ElevenLabs API 密钥（ELEVENLABS_API_KEY）。
metadata: {"openclaw": {"requires": {"env": ["ELEVENLABS_API_KEY"]}, "primaryEnv": "ELEVENLABS_API_KEY"}}
---

# ElevenLabs 音效

根据文本描述生成音效 — 支持循环、自定义时长与提示词贴合度控制。

> **设置：** 参见 [安装指南](references/installation.md)。JavaScript 请仅使用 `@elevenlabs/*` 包。

## 快速开始

### Python

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

audio = client.text_to_sound_effects.convert(
    text="Thunder rumbling in the distance with light rain",
)

with open("thunder.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### JavaScript

```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { createWriteStream } from "fs";

const client = new ElevenLabsClient();
const audio = await client.textToSoundEffects.convert({
  text: "Thunder rumbling in the distance with light rain",
});
audio.pipe(createWriteStream("thunder.mp3"));
```

### cURL

```bash
curl -X POST "https://api.elevenlabs.io/v1/sound-generation" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"text": "Thunder rumbling in the distance with light rain"}' \
  --output thunder.mp3
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `text` | string (required) | — | 所需音效的描述 |
| `model_id` | string | `eleven_text_to_sound_v2` | 使用的模型 |
| `duration_seconds` | number \| null | null (auto) | 时长 0.5–30 秒；为 null 时自动计算 |
| `prompt_influence` | number \| null | 0.3 | 与提示词的贴合程度（0–1） |
| `loop` | boolean | false | 生成无缝循环音效（仅 v2 模型） |

## 带参数的示例

```python
# Looping ambient sound, 10 seconds
audio = client.text_to_sound_effects.convert(
    text="Gentle forest ambiance with birds chirping",
    duration_seconds=10.0,
    prompt_influence=0.5,
    loop=True,
)

# Short UI sound, high prompt adherence
audio = client.text_to_sound_effects.convert(
    text="Soft notification chime",
    duration_seconds=1.0,
    prompt_influence=0.8,
)
```

## 输出格式

将 `output_format` 作为查询参数（cURL）或 SDK 参数传入：

| 格式 | 说明 |
|--------|-------------|
| `mp3_44100_128` | MP3 44.1kHz 128kbps（默认） |
| `pcm_44100` | 原始未压缩 CD 品质 |
| `opus_48000_128` | Opus 48kHz 128kbps — 高效压缩 |
| `ulaw_8000` | μ-law 8kHz — 电话语音 |

完整列表：`mp3_22050_32`, `mp3_24000_48`, `mp3_44100_32`, `mp3_44100_64`, `mp3_44100_96`, `mp3_44100_128`, `mp3_44100_192`, `pcm_8000`, `pcm_16000`, `pcm_22050`, `pcm_24000`, `pcm_32000`, `pcm_44100`, `pcm_48000`, `ulaw_8000`, `alaw_8000`, `opus_48000_32`, `opus_48000_64`, `opus_48000_96`, `opus_48000_128`, `opus_48000_192`。

## 提示词技巧

- 尽量具体：「铁皮屋顶上的大雨」优于「雨声」
- 组合元素：「砾石上的脚步声与远处车流」
- 说明风格：「电影感 braam、恐怖」或「8-bit 复古跳跃音效」
- 点明情绪/场景：「废弃建筑中呼啸的诡异风声」

## 错误处理

```python
try:
    audio = client.text_to_sound_effects.convert(text="Explosion")
except Exception as e:
    print(f"API error: {e}")
```

常见错误：
- **401**：API 密钥无效
- **422**：参数无效（检查时长范围、prompt_influence 范围）
- **429**：超出速率限制

## 参考

- [安装指南](references/installation.md)
