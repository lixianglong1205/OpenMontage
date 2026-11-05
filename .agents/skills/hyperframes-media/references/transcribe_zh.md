# 转录

创建规范化的词级时间戳。**务必显式指定 `--model`** — CLI 默认是 `small.en`，会静默将非英语音频转成英语。

```bash
npx hyperframes transcribe audio.mp3  --model small.en             # known English
npx hyperframes transcribe video.mp4  --model small --language es  # known Spanish
npx hyperframes transcribe audio.mp3  --model small                # unknown language (auto-detect)
npx hyperframes transcribe subtitles.srt                           # import existing
npx hyperframes transcribe subtitles.vtt
npx hyperframes transcribe openai-response.json
```

## 语言规则（不可违背）

`.en` 模型（`tiny.en` / `base.en` / `small.en` / `medium.en`）会将非英语音频**翻译**成英语，从而静默破坏原始语言。

1. **已知为英语** → `--model small.en`（音乐或嘈杂音频可用 `medium.en`）
2. **已知为非英语** → `--model small --language <iso-code>`（不要加 `.en` 后缀）
3. **语言未知** → `--model small`（Whisper 自动检测）

**CLI 默认是 `small.en`** — 不要依赖默认值；始终传入 `--model` 以明确选择。`--language` 还会从混合语言音频中过滤掉非目标语言的片段。

## 模型规格

| 模型       | 大小   | 速度     | 适用场景                              |
| ---------- | ------ | -------- | ------------------------------------- |
| `tiny`     | 75 MB  | 最快     | 快速预览、冒烟测试                    |
| `base`     | 142 MB | 快       | 短片段、清晰音频                      |
| `small`    | 466 MB | 中等     | 多数多语言内容的默认选择              |
| `medium`   | 1.5 GB | 慢       | 带人声的音乐、嘈杂音频                |
| `large-v3` | 3.1 GB | 最慢     | 生产级质量                            |

### 按内容类型选择模型

1. 静音或轻背景上的语音 → `small.en`
2. 音乐上的语音，或带人声的音乐 → 从 `medium.en` 开始
3. 成品音乐轨（人声 + 完整编曲）→ 从 `medium.en` 开始；通常还需手动歌词或外部 API（见 [`captions/transcript-handling.md`](captions/transcript-handling.md) → “Using External Transcription APIs”）
4. 多语言 → `medium` 或 `large-v3`（不要 `.en` 后缀），配合 `--language`

## 输出结构

合成（Compositions）消费扁平的词对象数组。`id`（`w0`、`w1` …）在规范化阶段添加，用于字幕覆盖中的稳定引用；为向后兼容可选。

```json
[
  { "id": "w0", "text": "Hello", "start": 0.0, "end": 0.5 },
  { "id": "w1", "text": "world.", "start": 0.6, "end": 1.2 }
]
```

关于强制性的字幕质量检查、重试规则以及 OpenAI/Groq Whisper API 导入路径，见 `captions/transcript-handling.md`。
