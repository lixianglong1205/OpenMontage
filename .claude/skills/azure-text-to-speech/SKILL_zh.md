---
name: azure-text-to-speech
description: 使用 Azure AI Speech（REST 文本转语音）生成神经语音旁白。在 OpenMontage 中合成配音或旁白时使用。可选的云 TTS 提供商——在已配置 AZURE_SPEECH_KEY 时优先使用；本地 piper_tts 仍是默认离线路径。与 azure_stt 共用同一 Speech 资源。
license: MIT
compatibility: 需要互联网访问以及 Azure AI Speech 资源（AZURE_SPEECH_KEY + AZURE_SPEECH_REGION）。
metadata: {"openclaw": {"requires": {"env": ["AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION"]}, "primaryEnv": "AZURE_SPEECH_KEY"}}
---

# Azure AI Speech — 文本转语音（Text-to-Speech）

使用 **Azure 神经 TTS** 生成旁白——高质量多语言音色、SSML 韵律控制与 express-as 风格，由 REST
`/cognitiveservices/v1` 端点同步提供（无需令牌交换、Blob 存储或作业轮询）。在 OpenMontage 中通过 `azure_tts` 工具暴露
（`capability=tts`，`provider=azure`）。这是 **可选的云 TTS 提供商**——
当已配置 `AZURE_SPEECH_KEY` 时，优先用于高质量云端旁白。本地 `piper_tts` 仍是 **默认离线路径** 以及
Azure 不可用时的回退；需要声音克隆时仍选用 `elevenlabs_tts`。

> 文档：[REST 文本转语音](https://learn.microsoft.com/azure/ai-services/speech-service/rest-text-to-speech) · [音色库](https://speech.microsoft.com/portal/voicegallery)

## 设置

与 `azure_stt` 使用同一 Speech 资源——**一组密钥/区域即可双向解锁**
（STT 与 TTS）。在
[Azure 门户](https://portal.azure.com) 创建 **Speech** 资源；从其
**密钥和终结点** 页面复制密钥与区域。

```bash
export AZURE_SPEECH_KEY=your_speech_resource_key
export AZURE_SPEECH_REGION=eastus        # your resource's region
# export AZURE_TTS_ENDPOINT=https://...  # optional: full custom TTS host
#   (the TTS host is https://<region>.tts.speech.microsoft.com — a different
#    subdomain than the STT endpoint, hence the separate override var)
```

在设置 `AZURE_SPEECH_KEY` 以及 `AZURE_SPEECH_REGION` 或 `AZURE_TTS_ENDPOINT` 之一后，
`azure_tts` 会报告 `AVAILABLE`。

## 在流水线中使用

照常通过 `tts_selector` 路由（它会自动发现 `azure_tts`），或在用户已批准 Azure 时
直接调用提供商工具：

```python
from tools.tool_registry import registry
registry.discover()
tts = registry._tools["azure_tts"]

result = tts.execute({
    "text": "Every design decision in this dashboard has a reason.",
    "voice": "andrew",                 # alias or full Azure short name
    "rate": "-4%",                     # slightly slower for narration
    # "style": "narration-professional",  # for voices that support styles
    "output_path": "projects/my-video/assets/audio/seg_001.mp3",
    "output_format": "mp3",            # or "wav" (48kHz PCM) for mixing
})
```

若 `azure_tts` 不可用（无密钥）或出错，按其声明的回退链处理：`elevenlabs_tts` → `openai_tts` → `piper_tts`。

## 音色选择

精选短列表（`voice` 参数接受别名）：

| 别名 | 音色 | 特点 |
|-------|-------|-----------|
| `andrew` | en-US-AndrewMultilingualNeural | 温暖、自信、对话感——默认；创始人/讲解者气质 |
| `brandon` | en-US-BrandonMultilingualNeural | 更低沉、沉稳 |
| `ava` | en-US-AvaMultilingualNeural | 自信、明亮的女声 |
| `guy` | en-US-GuyNeural | 权威感 |
| `jenny` | en-US-JennyNeural | 友好、清晰 |

任何有效的 Azure 音色短名均可原样传入（例如
`de-DE-KatjaNeural`）；*Multilingual* 多语言音色对非英文文本表现良好——
将 `locale` 设为与文本语言一致以生成正确的 SSML。

## 重要参数

- **`rate` / `pitch`** — SSML 韵律。旁白通常略慢更自然（`"-4%"` 至 `"-8%"`）；除非修正音色，否则音高保持 `"0%"`。
- **`style`** — 支持 express-as 的音色可用风格
  （`narration-professional`、`calm`、`newscast`）。Azure 会静默忽略不支持的风格，
  批量生成前请先试听样本。
- **`output_format`** — 交付用 `mp3`（48kHz/192kbit），若片段需进入 `audio_mixer` 做后续处理则用 `wav`（48kHz PCM）。
- 确定性：固定音色 + SSML 重复渲染音频基本一致——
  可安全地只重新生成单个片段，无需整段重录。

## 费用

Azure 神经 TTS 标准层约 **每 100 万字符 $16**（约每 1k 字符 $0.016；
约 150 词的旁白片段 ≈ $0.015）。工具会在每次调用中报告
`cost_usd` 供成本追踪。当前费率见
[Azure AI Speech 定价](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)。

## 限制与提示

- 一次 `execute` 调用 = 一段旁白。按脚本章节生成（符合资源阶段约定），而非整篇大段——
  较小片段更易对齐场景时长，且重新生成成本低。
- 同步端点单次请求音频上限为 10 分钟——远高于 OpenMontage 生成的任何片段。
- 文本会自动进行 XML 转义；请勿预先转义或包裹 SSML——传入纯文本及 `rate`/`pitch`/`style` 参数即可。
- 验证质量：批量跑完整脚本前先试听第一段（音色/风格是否合适属于创意决策——
  按 Decision Communication Contract 在提案阶段向用户说明）。
