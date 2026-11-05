# 实时事件参考

实时语音转文字（speech-to-text）流式传输中事件的完整参考。

## 发送事件（客户端 → 服务器）

### input_audio_chunk

发送待转写的音频数据。

```json
{
  "message_type": "input_audio_chunk",
  "audio_base_64": "<base64-encoded-pcm-audio>",
  "commit": false,
  "sample_rate": 16000
}
```

| 字段 | 类型 | 必填 | 说明 |
|-------|------|----------|-------------|
| `message_type` | string | 是 | 固定为 `"input_audio_chunk"` |
| `audio_base_64` | string | 是 | Base64 编码的 PCM 音频数据 |
| `commit` | boolean | 是 | 是否在本块之后提交 |
| `sample_rate` | number | 否 | 采样率（Hz），范围 8000–48000 |
| `previous_text` | string | 否 | 先前转写文本的上下文（仅首块，最多 50 个字符） |

### commit

结束当前转写片段。

```json
{
  "message_type": "commit"
}
```

## 接收事件（服务器 → 客户端）

所有接收事件均使用 `message_type` 作为判别字段。

### session_started

连接已成功建立。

```json
{
  "message_type": "session_started",
  "session_id": "0b0a72b57fd743ebbed6555d44836cf2",
  "config": {
    "sample_rate": 16000,
    "audio_format": "pcm_16000",
    "language_code": "en",
    "model_id": "scribe_v2_realtime",
    "commit_strategy": "manual",
    "include_timestamps": true
  }
}
```

### partial_transcript

中间转写结果，随音频处理频繁更新。

```json
{
  "message_type": "partial_transcript",
  "text": "Hello, how are"
}
```

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `message_type` | string | `"partial_transcript"` |
| `text` | string | 当前部分转写文本 |

### committed_transcript

提交后的最终转写结果。

```json
{
  "message_type": "committed_transcript",
  "text": "Hello, how are you today?"
}
```

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `message_type` | string | `"committed_transcript"` |
| `text` | string | 已确定的转写文本 |

### committed_transcript_with_timestamps

带词级时间戳的最终转写。当 `include_timestamps=true` 时，在 `committed_transcript` 之后发送。

```json
{
  "message_type": "committed_transcript_with_timestamps",
  "text": "Hello, how are you today?",
  "language_code": "en",
  "words": [
    {"text": "Hello", "start": 0.0, "end": 0.32, "type": "word"},
    {"text": " ", "start": 0.32, "end": 0.35, "type": "spacing"},
    {"text": "how", "start": 0.40, "end": 0.55, "type": "word"}
  ]
}
```

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `message_type` | string | `"committed_transcript_with_timestamps"` |
| `text` | string | 完整转写文本 |
| `language_code` | string | 检测到的语言代码 |
| `words` | array | 词级时间数据 |
| `words[].text` | string | 词或 token |
| `words[].start` | number | 开始时间（秒） |
| `words[].end` | number | 结束时间（秒） |
| `words[].type` | string | `"word"`、`"spacing"` 或 `"audio_event"` |
| `words[].speaker_id` | string | 说话人标识（启用说话人分离时） |

## 错误事件

### error

发生错误时发送。

```json
{
  "message_type": "error",
  "error": "input_error"
}
```

### 错误码

| 代码 | 说明 |
|------|-------------|
| `auth_error` | API 密钥或 token 无效 |
| `quota_exceeded` | 已达用量上限 |
| `input_error` | 不支持的音频格式或无效输入 |
| `rate_limited` | 请求过于频繁 |
| `commit_throttled` | 提交操作过于频繁 |
| `session_time_limit_exceeded` | 会话超过最大时长 |
| `unaccepted_terms` | 控制台中尚未接受服务条款 |
| `resource_exhausted` | 服务器容量已满 |
| `queue_overflow` | 服务器队列已满 |
| `chunk_size_exceeded` | 音频块过大 |
| `insufficient_audio_activity` | 检测到的语音不足 |
| `transcriber_error` | 内部处理错误 |

## 连接事件

### open

WebSocket 连接已建立（标准 WebSocket 事件，非 JSON 消息）。

### close

WebSocket 连接已关闭（标准 WebSocket 关闭帧，含 code 与 reason）。

## 事件处理示例

### Python

Python SDK 封装了底层协议。使用 SDK 事件对象时，可使用 `event.type`（而非 `message_type`）：

```python
async for event in connection:
    if event.type == "session_started":
        print(f"Session: {event.session_id}")
    elif event.type == "partial_transcript":
        print(f"Partial: {event.text}")
    elif event.type == "committed_transcript":
        print(f"Final: {event.text}")
    elif event.type == "committed_transcript_with_timestamps":
        for word in event.words:
            print(f"  {word.text}: {word.start}s - {word.end}s")
    elif event.type == "error":
        print(f"Error: {event.error}")
```

### JavaScript

JavaScript SDK 使用与 `message_type` 值一致的事件名：

```javascript
connection.on("session_started", (data) => {
  console.log("Session:", data.sessionId);
});

connection.on("partial_transcript", (data) => {
  console.log("Partial:", data.text);
});

connection.on("committed_transcript", (data) => {
  console.log("Final:", data.text);
});

connection.on("committed_transcript_with_timestamps", (data) => {
  for (const word of data.words) {
    console.log(`  ${word.text}: ${word.start}s - ${word.end}s`);
  }
});

connection.on("error", (error) => {
  console.error("Error:", error);
});
```
