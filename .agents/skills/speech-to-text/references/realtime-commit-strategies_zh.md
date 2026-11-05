# 转写文本与提交策略

控制在实时流式场景下何时以及如何定稿转写文本。

## 为何提交（commit）很重要

在实时转写中，随着更多音频到达，模型会持续修正理解。某个词听起来像 “their”，在听到更多上下文后可能变成 “there” 或 “they're”。**提交（commit）** 机制让你决定何时将转写结果「锁定」为定稿。

## 转写类型

| 类型 | 说明 |
|------|------|
| **Partial（部分）** | 处理音频过程中频繁更新的临时「最佳猜测」结果。用于实时反馈（在用户说话时展示文字），但不要保存——它们可能变化。 |
| **Committed（已提交）** | 发生提交后的最终、稳定结果。作为应用的权威来源——不会再变。 |
| **Committed with Timestamps（带时间戳的已提交）** | 与已提交相同，但包含词级时间数据，用于字幕、卡拉 OK 或口型同步。 |

## 手动提交（默认）

由你显式控制转写片段何时定稿。

### Python

```python
async with client.speech_to_text.realtime.connect(
    model_id="scribe_v2_realtime",
) as connection:
    # Send audio
    await connection.send({
        "audio_base_64": audio_base_64,
        "sample_rate": 16000,
    })

    # Commit when ready (e.g., pause in speech, end of sentence)
    await connection.commit()
```

### JavaScript

```javascript
const connection = await client.speechToText.realtime.connect({
  modelId: "scribe_v2_realtime",
});

// Send audio
connection.send({
  audioBase64: audioBase64,
  sampleRate: 16000,
});

// Commit when ready
connection.commit();
```

### 最佳实践

- **每 20–30 秒提交一次** 以获得最佳性能
- **在静音或逻辑断点处提交**（句末、说话人切换）
- 若未发送手动提交，**90 秒后自动提交**

### 提供上下文

在第一个音频块中附带先前文本，以帮助模型：

```python
await connection.send({
    "audio_base_64": first_chunk,
    "sample_rate": 16000,
    "previous_text": "So as I was saying,"  # Keep under 50 characters
})
```

有助于：
- 重连后继续对话
- 提供上下文以提高准确率
- 处理句子片段

## 语音活动检测（VAD）

VAD 监听静音，并在说话人停顿时自动提交。这样会形成与真实说话方式一致的自然转写片段——在句子和意群之间停顿。推荐用于实时麦克风输入。

### 配置

#### React（`useScribe`）

```typescript
import { useScribe, CommitStrategy } from "@elevenlabs/react";

const scribe = useScribe({
  modelId: "scribe_v2_realtime",
  commitStrategy: CommitStrategy.VAD,
  // Optional VAD tuning:
  vadSilenceThresholdSecs: 1.5,    // Silence duration before commit
  vadThreshold: 0.4,               // Speech detection sensitivity (0-1)
  minSpeechDurationMs: 100,        // Minimum speech length required
  minSilenceDurationMs: 100,       // Minimum silence length required
});
```

> **重要：** 默认为 `CommitStrategy.MANUAL`。麦克风输入务必设置 `CommitStrategy.VAD`——否则已提交的转写不会触发，连接可能断开。

#### JavaScript 客户端

```javascript
const connection = await client.speechToText.realtime.connect({
  modelId: "scribe_v2_realtime",
  vad: {
    silenceThresholdSecs: 1.5,    // Silence duration before commit
    threshold: 0.4,               // Speech detection sensitivity (0-1)
    minSpeechDurationMs: 100,     // Minimum speech length required
    minSilenceDurationMs: 100,    // Minimum silence length required
  },
});
```

### 参数

| 参数 | 说明 | 默认值 |
|-----------|-------------|---------|
| `silenceThresholdSecs` | 自动提交前的静音时长（秒） | 1.5 |
| `threshold` | 语音检测灵敏度（越低越敏感） | 0.4 |
| `minSpeechDurationMs` | 忽略短于此值的语音 | 100 |
| `minSilenceDurationMs` | 忽略短于此值的静音 | 100 |

### 何时使用 VAD

- 实时麦克风输入
- 对话类应用
- 需要自然语音边界时
- 客户端实现

### 何时使用手动提交

- 处理音频文件
- 已知片段边界
- 需要对时机有最大控制
- 服务端批处理

## 支持的音频格式

| 格式 | 采样率 | 说明 |
|--------|-------------|-------|
| PCM 16-bit | 16kHz | 推荐，最佳平衡 |
| PCM 16-bit | 8kHz - 48kHz | 支持范围 |
| μ-law 8-bit | 8kHz | 电话系统兼容 |
