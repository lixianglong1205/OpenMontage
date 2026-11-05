# TTS → 字幕

当不存在已录制的旁白时，生成旁白并获取词级字幕时间轴。具体路径取决于所使用的 TTS 提供商：

## 路径 A — HeyGen（单次调用，无需 Whisper）

HeyGen 会在返回音频的同一响应中提供词级时间戳。传入 `--words` 即可完成：

```bash
npx hyperframes tts script.txt --provider heygen --output narration.wav --words narration.words.json
```

`narration.words.json` 已是字幕流水线所需的 `[{ id, text, start, end }]` 格式——无需单独的转写步骤。

## 路径 B — ElevenLabs / Kokoro（TTS → Whisper）

这些提供商不返回词级数据。先生成音频，再转写：

```bash
npx hyperframes tts script.txt --voice af_heart --output narration.wav
npx hyperframes transcribe narration.wav --model small.en   # voice af_heart is American English
```

Whisper 从生成的音频中提取精确的词边界，因此字幕时间与朗读一致，无需手动微调。将 `--model` 与语音的语言匹配（`a`/`b` 前缀的美式英语使用 `small.en`，否则使用 `small --language <code>`）。随后通过 `captions/` 中的字幕参考文档使用 `transcript.json`。
