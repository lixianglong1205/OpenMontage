---
name: azure-speech-to-text
description: 使用 Azure AI Speech（Fast Transcription REST API）将音频转写为文本。适用于在 OpenMontage 中将音频/视频转为文本、生成字幕或处理口播内容。可选的云端 STT 提供商——在已配置 AZURE_SPEECH_KEY 时优先使用；本地 faster-whisper `transcriber` 为默认离线路径。
license: MIT
compatibility: 需要互联网访问以及 Azure AI Speech 资源（AZURE_SPEECH_KEY + AZURE_SPEECH_REGION）。
metadata: {"openclaw": {"requires": {"env": ["AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION"]}, "primaryEnv": "AZURE_SPEECH_KEY"}}
---

# Azure AI Speech — 语音转文本

使用 **Azure Fast Transcription** 将音频转写为文本——同步处理、词级时间戳、说话人分离与多语言识别。
在 OpenMontage 中通过 `azure_stt` 工具暴露（`capability=analysis`，
`provider=azure`）。它是 **可选的云端 STT 提供商**——在已配置
`AZURE_SPEECH_KEY` 时，云端转写优先选用它。本地
`transcriber` 工具（faster-whisper）仍是 **默认离线路径**，并在
Azure 不可用时作为回退。

> 文档：[Fast Transcription](https://learn.microsoft.com/azure/ai-services/speech-service/fast-transcription-create) · [Speech service overview](https://learn.microsoft.com/azure/ai-services/speech-service/spx-overview)

## 为何选用 Fast Transcription（而非 Batch）

Azure 提供三种 STT 接口。OpenMontage 使用 **Fast Transcription**，因为
流水线转写的是 **本地音频文件**：

| 接口 | 输入 | 延迟 | 需要 |
|---------|-------|---------|-------|
| **Fast Transcription**（本文使用） | 本地文件，multipart POST | 同步，快于实时 | key + region |
| Batch Transcription | 位于 URL 的音频（Blob + SAS） | 异步任务 + 轮询 | Blob 存储配套 |
| Speech SDK (`spx`) | 麦克风 / 流 / 文件 | 流式 | 原生 `azure-cognitiveservices-speech` 包 |

Fast Transcription 无需 Blob 存储、SAS URL 或原生 SDK——只需
`requests` 与两个环境变量。

## 设置

在 [Azure portal](https://portal.azure.com) 中创建 **Speech** 资源；
从其 **Keys and Endpoint** 页面复制密钥与区域。

```bash
export AZURE_SPEECH_KEY=your_speech_resource_key
export AZURE_SPEECH_REGION=eastus          # your resource's region
# export AZURE_SPEECH_ENDPOINT=https://...  # optional: overrides region
```

当 `AZURE_SPEECH_KEY` 以及 `AZURE_SPEECH_REGION` 或
`AZURE_SPEECH_ENDPOINT` 之一已设置时，`azure_stt` 会报告为 `AVAILABLE`。

## 在流水线中使用

除非运行必须离线，否则优先使用 `azure_stt` 而非 `transcriber`。其输出
与 `transcriber` 模式完全一致，可无缝用于 `subtitle_gen`
及任何消费转写结果的阶段。

```python
from tools.tool_registry import registry
registry.discover()
stt = registry._tools["azure_stt"]

result = stt.execute({
    "input_path": "projects/my-video/assets/audio/narration.mp3",
    # "language": "en",          # ISO 639-1 or BCP-47 ("en-US"); omit for auto-ID
    # "diarize": True,           # speaker labels, no HuggingFace token needed
    # "max_speakers": 4,
    "output_dir": "projects/my-video/artifacts",
})
if result.success:
    segs = result.data["segments"]          # [{id,start,end,text,words:[...]}]
    words = result.data["word_timestamps"]  # flat [{word,start,end,probability}]
```

若 `azure_stt` 不可用（无密钥）或出错，回退到 `transcriber`
（本地 whisper）——其 `execute` 签名与输出相同。

## 重要参数

- **`language`** — 传入 ISO 代码（`"en"`）或完整区域设置（`"en-US"`）。已知语言时固定它；
  比自动识别更快、更准。
- **`candidate_locales`** — 省略 `language` 时，Azure 在此候选列表上做语言
  识别。收窄为你实际预期的语言；列表过长会拖慢检测并易误判。
- **`diarize` / `max_speakers`** — 多说话人音频（访谈、
  播客）时启用。将 `max_speakers` 设为真实上限。
- **`profanity_filter`** — `None` | `Masked`（默认） | `Removed` | `Tags`。

## 响应结构（映射到 transcriber 模式）

原始 Azure 响应（`phrases[]` 含 `offsetMilliseconds` / `words[]`）会
转换为秒，并符合 OpenMontage 转写模式：

```json
{
  "segments": [
    {"id": 0, "start": 0.0, "end": 2.4, "text": "Hello world",
     "speaker": 1,
     "words": [{"word": "Hello", "start": 0.0, "end": 0.5, "probability": 0.98}]}
  ],
  "word_timestamps": [{"word": "Hello", "start": 0.0, "end": 0.5, "probability": 0.98}],
  "language": "en-US",
  "duration_seconds": 2.4,
  "provider": "azure"
}
```

注意：Fast Transcription 没有 *逐词* 置信度，因此每个词的 `probability` 携带的是
**短语** 置信度。

## 限制与提示

- 单次请求单个文件最长约 2 小时 / 数百 MB。更长或批量
  任务请改用 Azure Batch Transcription。
- 发送干净音频（16 kHz+ 单声道即可）。若只需语音，先将视频转码为音频——
  上传更小，结果相同。
- 校验时间：词级时间戳驱动 `subtitle_gen` 中的字幕 cue。对照源音频抽查
  首尾 cue。
