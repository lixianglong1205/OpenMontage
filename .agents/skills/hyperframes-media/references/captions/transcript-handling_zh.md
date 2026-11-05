# 转录文本指南

关于 `transcribe` CLI 调用、`.en`-translates-non-English 规则以及 Whisper 模型选择，请参阅 [`../transcribe.md`](../transcribe.md)。本文说明在编写字幕时如何处理转录结果：输入格式、必做的质量检查、清理代码，以及外部 API 回退方案。

## 支持的输入格式

CLI 会自动检测并规范化以下格式：

| 格式                | 扩展名 | 来源                                                                      | 词级时间戳？       |
| --------------------- | --------- | --------------------------------------------------------------------------- | ----------------- |
| whisper.cpp JSON      | `.json`   | `hyperframes init --video`、`hyperframes transcribe`                        | 是               |
| OpenAI Whisper API    | `.json`   | `openai.audio.transcriptions.create({ timestamp_granularities: ["word"] })` | 是               |
| SRT 字幕         | `.srt`    | 视频编辑器、字幕工具、YouTube                                      | 否（短语级） |
| VTT 字幕         | `.vtt`    | Web 播放器、YouTube、转录服务                                | 否（短语级） |
| 规范化词数组 | `.json`   | 由任意工具预处理                                                   | 是               |

**词级时间戳能生成更好的字幕。** SRT/VTT 提供短语级时间，可用，但无法实现逐词动画效果。

## 转录质量检查（必做）

每次转录之后，**在继续之前务必阅读转录文本并检查质量问题。** 劣质转录会产生无意义的字幕。切勿跳过此步骤。

### 需要留意的信号

| 信号                       | 示例                                | 原因                                                                        |
| ---------------------------- | -------------------------------------- | ---------------------------------------------------------------------------- |
| 音符标记（`♪`、`�`） | `{ "text": "♪" }` 或 `{ "text": "�" }` | Whisper 检测到的是音乐，而非语音                                           |
| 乱码 / 无意义词     | "Do a chin"、"Get so gay"、"huh"       | 模型误听歌词或背景噪声                                    |
| 长时间无词      | 20 秒以上仅有 `♪` 标记         | 器乐段落 — 属预期，但占比过高说明漏掉了语音 |
| 重复填充词              | 大量 "huh"、"uh"、"oh" 条目         | 模型在音乐上产生幻觉                                              |
| 极短的词跨度        | 词的 `end - start < 0.05`        | 时间戳对齐不可靠                                               |

### 自动重试规则

**若超过 20% 的条目为 `♪`/`�` 标记，或转录文本含明显无意义词，则转录失败。** 不要用劣质转录继续。应：

1. **若原先使用 `small.en` 或更小模型，则用 `medium.en` 重试：**
   ```bash
   npx hyperframes transcribe audio.mp3 --model medium.en
   ```
2. **若 `medium.en` 仍失败**（仍 >20% 音乐标记或乱码），告知用户音频对本地转录而言噪声过大，并建议：
   - 手动提供歌词，格式为 SRT/VTT 文件
   - 使用外部 API（OpenAI 或 Groq Whisper — 见下文）
3. **构建字幕前务必清理转录文本** — 过滤 `♪`/`�` 标记，以及 `text` 仅为单个非词字符的条目。只有真实词语应进入字幕合成。

### 清理转录文本

转录之后（即使模型表现良好），也应剔除非词条目：

```js
var raw = JSON.parse(transcriptJson);
var words = raw.filter(function (w) {
  if (!w.text || w.text.trim().length === 0) return false;
  if (/^[♪�\u266a\u266b\u266c\u266d\u266e\u266f]+$/.test(w.text)) return false;
  if (/^(huh|uh|um|ah|oh)$/i.test(w.text) && w.end - w.start < 0.1) return false;
  return true;
});
```

按内容类型选择模型的指引，见 [`../transcribe.md`](../transcribe.md) →「Picking a model by content type」。

## 使用外部转录 API

为获得最佳准确度，可使用外部 API 并导入结果：

**OpenAI Whisper API**（推荐，质量优先）：

```bash
# Generate with word timestamps, then import
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file=@audio.mp3 -F model=whisper-1 \
  -F response_format=verbose_json \
  -F "timestamp_granularities[]=word" \
  -o transcript-openai.json

npx hyperframes transcribe transcript-openai.json
```

**Groq Whisper API**（速度快，有免费额度）：

```bash
curl https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file=@audio.mp3 -F model=whisper-large-v3 \
  -F response_format=verbose_json \
  -F "timestamp_granularities[]=word" \
  -o transcript-groq.json

npx hyperframes transcribe transcript-groq.json
```

## 若无转录文件

1. 在项目根目录查找 `transcript.json`、`.srt` 或 `.vtt` 文件。
2. 若未找到，运行 [`../transcribe.md`](../transcribe.md) — 起始模型按该文档中「Picking a model by content type」选取。
3. 执行上文质量检查。若未通过，用更大模型重试，或回退到手动歌词 / 外部 API。
