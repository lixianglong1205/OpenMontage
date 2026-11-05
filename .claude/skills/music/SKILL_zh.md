---
name: music
description: 使用 ElevenLabs Music API 生成音乐。适用于创建纯音乐曲目、带歌词的歌曲、背景音乐、短广告音乐或任何 AI 生成的音乐作品。支持基于提示的生成、用于精细控制的作曲计划，以及带元数据的详细输出。
license: MIT
compatibility: 需要互联网访问和 ElevenLabs API 密钥（ELEVENLABS_API_KEY）。
metadata: {"openclaw": {"requires": {"env": ["ELEVENLABS_API_KEY"]}, "primaryEnv": "ELEVENLABS_API_KEY"}}
---

# ElevenLabs 音乐生成

根据文本提示生成音乐——支持纯音乐曲目、带歌词的歌曲，以及通过作曲计划实现的精细控制。

> **设置：** 参见 [安装指南](references/installation.md)。对于 JavaScript，请仅使用 `@elevenlabs/*` 包。

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
| `music.compose` | 根据提示或作曲计划生成音频 |
| `music.composition_plan.create` | 生成用于精细控制的结构化计划 |
| `music.compose_detailed` | 生成音频、作曲计划及元数据 |
| `music.upload` | 上传音频文件以供后续 inpainting 工作流使用，并可选择提取其作曲计划 |

完整参数说明见 [API 参考](references/api_reference.md)。

`music.upload` 面向已开通 inpainting 功能的企业客户。

## 作曲计划

如需精细控制，可先生成作曲计划，修改后再进行合成：

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

## 参考资料

- [安装指南](references/installation.md)
- [API 参考](references/api_reference.md)
