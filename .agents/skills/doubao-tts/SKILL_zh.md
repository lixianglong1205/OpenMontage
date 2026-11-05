---
name: doubao-tts
description: 使用火山引擎豆包 Speech 2.0 生成普通话及多语言旁白。适用于制作中文配音、用户偏好豆包/火山引擎 TTS，或旁白需要字级时间戳元数据以生成字幕时。
---

# 豆包 TTS

需要在 `.env` 中配置 `DOUBAO_SPEECH_API_KEY`。
通过 `DOUBAO_SPEECH_VOICE_TYPE` 设置默认音色，或在调用工具时传入 `voice_id`。

## 当前 API

使用新控制台 API Key 鉴权方式：

```text
X-Api-Key: ${DOUBAO_SPEECH_API_KEY}
X-Api-Resource-Id: seed-tts-2.0
```

请勿将新控制台 API Key 与 `X-Api-App-Id`、`X-Api-Access-Key` 混用。若 API 返回 `load grant: requested grant not found`，多半是 Key 类型或鉴权头不正确。

长视频旁白优先使用异步端点：

```text
POST https://openspeech.bytedance.com/api/v3/tts/submit
POST https://openspeech.bytedance.com/api/v3/tts/query
```

该流程会返回 `audio_url` 以及 `sentences[].words[]` 时间元数据，可用于生成字幕。

## OpenMontage 用法

通过 TTS 选择器生成：

```python
from tools.audio.tts_selector import TTSSelector

result = TTSSelector().execute({
    "preferred_provider": "doubao",
    "text": "如果 AI 真的会改变未来，普通人到底该怎么参与？",
    "voice_id": "zh_female_vv_uranus_bigtts",
    "output_path": "projects/my-video/assets/audio/narration.mp3",
    "speech_rate": 0,
    "enable_timestamp": True,
})
```

或直接调用 Provider：

```python
from tools.audio.doubao_tts import DoubaoTTS

result = DoubaoTTS().execute({
    "text": "短样本试听文本。",
    "voice_id": "zh_female_vv_uranus_bigtts",
    "output_path": "projects/my-video/assets/audio/doubao_sample.mp3",
})
```

Provider 会写入：

- `output_path`：下载后的音频文件
- `metadata_path`：完整 query 响应 JSON，默认路径为 `<output_path>.json`

## 推荐工作流

1. 在生成完整付费旁白前，先生成 10–15 秒试听样本。
2. 请用户确认音色自然度、口音与语速。
3. 仅在用户确认后再生成完整旁白。
4. 保留 query JSON，它是字幕时间戳的权威来源。
5. 从 `sentences[].words[]` 构建字幕，不要按估算文本长度切分。
6. 应用时间戳前，按中文语义短语分组字幕；不要仅按固定字数切分，否则会拆坏如「在不押单个公司的情况下」或「可能会被慢慢稀释」等短语，影响理解。
7. 除非用户明确要求匹配既有时长，否则让视频时长跟随已确认的配音节奏。

## 参数

- `voice_id`：豆包 `speaker` / 音色类型。默认取自 `DOUBAO_SPEECH_VOICE_TYPE`。
- `resource_id`：豆包 Speech 2.0 音色使用 `seed-tts-2.0`。
- `speech_rate`：`0` 为正常语速，`100` 为 2 倍速，`-50` 为 0.5 倍速。
- `sample_rate`：默认 `24000`。
- `enable_timestamp`：默认 `true`。
- `return_usage`：默认 `true`，在可用时请求用量元数据。

默认不要传 `additions.explicit_language`。部分端点/Key 组合会因 `zh-cn` 返回 `unsupported additions explicit language zh-cn`。

制作沉稳的中文讲解类旁白时，建议从 `speech_rate: 0` 开始。若结果超出已确认版式的时长，在重新生成完整旁白前，先用 `speech_rate: 25` 或 `50` 做短对比试听。若用户更偏好豆包自然语速，不要仅为对齐其他 Provider 的时长而加速。

## 故障排查

- `load grant: requested grant not found`：Key 类型错误或鉴权头错误。新控制台 API Key 应使用 `X-Api-Key`。
- `speaker permission denied`：`voice_id` 错误或当前 resource 未授权该音色。
- `quota exceeded`：配额、终身字符数或并发超限。
- 缺少时间戳：确认 `enable_timestamp: true`，保留 query JSON，并核实所选端点是否返回了 `sentences`。

## 安全

切勿将 API Key 打印或写入日志、元数据、补丁或项目产物。`.env.example` 中应只保留空的变量名。
