---
name: music
description: 使用 ElevenLabs Music API 生成音乐。适用于创作纯器乐、带歌词歌曲、背景音乐、广告短曲或任何 AI 生成的音乐作品。支持基于提示词生成、用于精细控制的 composition plan，以及带元数据的详细输出。
license: MIT
compatibility: 需要联网访问以及 ElevenLabs API 密钥（ELEVENLABS_API_KEY）。
metadata: {"openclaw": {"requires": {"env": ["ELEVENLABS_API_KEY"]}, "primaryEnv": "ELEVENLABS_API_KEY"}}
---

# ElevenLabs 音乐生成

根据文本提示词生成音乐——支持纯器乐、带歌词歌曲，以及通过 composition plan 实现的精细控制。

> **设置：** 参见 [安装指南](references/installation.md)。JavaScript 请仅使用 `@elevenlabs/*` 系列包。

## 快速开始

### Python

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

audio = client.music.compose(
    prompt="A chill lo-fi hip hop beat with jazzy piano chords",
    music_length_ms=30000
)

with open("output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### JavaScript

```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { createWriteStream } from "fs";

const client = new ElevenLabsClient();
const audio = await client.music.compose({
  prompt: "A chill lo-fi hip hop beat with jazzy piano chords",
  musicLengthMs: 30000,
});
audio.pipe(createWriteStream("output.mp3"));
```

### cURL

```bash
curl -X POST "https://api.elevenlabs.io/v1/music" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"prompt": "A chill lo-fi beat", "music_length_ms": 30000}' --output output.mp3
```

## 方法

| 方法 | 说明 |
|--------|-------------|
| `music.compose` | 根据提示词或 composition plan 生成音频 |
| `music.composition_plan.create` | 生成用于精细控制的结构化 plan |
| `music.compose_detailed` | 生成音频、composition plan 及元数据 |
| `music.upload` | 上传音频文件供后续 inpainting 工作流使用，并可选择提取其 composition plan |

完整参数说明见 [API 参考](references/api_reference.md)。

`music.upload` 面向已开通 inpainting 功能的企业客户。

## Composition Plan

如需精细控制，可先生成 composition plan，修改后再进行 compose：

```python
plan = client.music.composition_plan.create(
    prompt="An epic orchestral piece building to a climax",
    music_length_ms=60000
)

# Inspect/modify styles and sections
print(plan.positiveGlobalStyles)  # e.g. ["orchestral", "epic", "cinematic"]

audio = client.music.compose(
    composition_plan=plan,
    music_length_ms=60000
)
```

## 内容限制

- 不得提及具体艺术家、乐队或受版权保护的歌词
- `bad_prompt` 错误会附带 `prompt_suggestion`，提供替代表述
- `bad_composition_plan` 错误会附带 `composition_plan_suggestion`

## 错误处理

```python
try:
    audio = client.music.compose(prompt="...", music_length_ms=30000)
except Exception as e:
    print(f"API error: {e}")
```

常见错误：401（密钥无效）、422（参数无效）、429（速率限制）。

## 参考

- [安装指南](references/installation.md)
- [API 参考](references/api_reference.md)
