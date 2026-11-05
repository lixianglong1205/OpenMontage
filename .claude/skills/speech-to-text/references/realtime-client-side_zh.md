# 客户端实时流式传输

在浏览器中直接将音频流式传输至 ElevenLabs，实现实时转录。

## 安装

```bash
# React
npm install @elevenlabs/react @elevenlabs/elevenlabs-js

# JavaScript
npm install @elevenlabs/client @elevenlabs/elevenlabs-js
```

> **警告：** 客户端包请始终使用 `@elevenlabs/*` 命名空间。

## 令牌生成

客户端流式传输需要一次性令牌（single-use token）以保护 API 密钥。请在后端生成令牌：

```typescript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";

const elevenlabs = new ElevenLabsClient({
  apiKey: process.env.ELEVENLABS_API_KEY,
});

app.get("/scribe-token", yourAuthMiddleware, async (req, res) => {
  const token = await elevenlabs.tokens.singleUse.create("realtime_scribe");
  res.json(token);
});
```

**注意：** 一次性令牌在 15 分钟后过期。

## React 实现

```typescript
import { useScribe, CommitStrategy } from "@elevenlabs/react";

function TranscriptionComponent() {
  const [transcript, setTranscript] = useState("");

  const scribe = useScribe({
    modelId: "scribe_v2_realtime",
    commitStrategy: CommitStrategy.VAD, // Auto-commit on silence for mic input
    onPartialTranscript: (data) => {
      // Show live feedback as user speaks
      console.log("Partial:", data.text);
    },
    onCommittedTranscript: (data) => {
      // Final transcript for this segment
      setTranscript((prev) => prev + data.text);
    },
  });

  const startRecording = async () => {
    const tokenResponse = await fetch("/scribe-token");
    const { token } = await tokenResponse.json();

    await scribe.connect({
      token,
      microphone: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
      },
    });
  };

  const stopRecording = () => {
    scribe.disconnect();
  };

  return (
    <div>
      <div>Status: {scribe.status}</div>
      <button onClick={startRecording}>Start</button>
      <button onClick={stopRecording}>Stop</button>
      <p>{transcript}</p>
    </div>
  );
}
```

> **重要：** 默认提交策略为 `CommitStrategy.MANUAL`，需要显式调用 `scribe.commit()`。对于麦克风输入，请始终设置 `CommitStrategy.VAD`，以便在检测到静音时由服务器自动提交。否则已提交的转录回调不会触发，连接也可能断开。

### `scribe.status` 取值

| 状态 | 含义 |
|--------|---------|
| `"disconnected"` | 无活动连接 |
| `"connecting"` | 正在建立连接 |
| `"connected"` | 已连接，可接收音频 |
| `"transcribing"` | 正在处理语音（检测到音频或 VAD 提交时，由 `"connected"` 切换而来） |
| `"error"` | 发生错误 |

> **重要：** 判断会话是否处于活动状态时，务必同时检查 `"connected"` 与 `"transcribing"`。处理语音期间状态会变为 `"transcribing"`，若仅检查 `"connected"`，会导致 UI 元素（按钮、波形、指示器）在会话中途错误重置。

```typescript
// Correct - handles both active states
const isListening = scribe.status === "connected" || scribe.status === "transcribing";

// Wrong - will flicker/reset when VAD commits
const isListening = scribe.status === "connected";
```

## JavaScript 实现

```typescript
import { Scribe, RealtimeEvents } from "@elevenlabs/client";

async function startTranscription() {
  const tokenResponse = await fetch("/scribe-token");
  const { token } = await tokenResponse.json();

  const connection = Scribe.connect({
    token,
    modelId: "scribe_v2_realtime",
    includeTimestamps: true,
    microphone: {
      echoCancellation: true,
      noiseSuppression: true,
      autoGainControl: true,
    },
  });

  connection.on(RealtimeEvents.OPEN, () => {
    console.log("Connected");
  });

  connection.on(RealtimeEvents.PARTIAL_TRANSCRIPT, (data) => {
    console.log("Partial:", data.text);
  });

  connection.on(RealtimeEvents.COMMITTED_TRANSCRIPT, (data) => {
    console.log("Committed:", data.text);
  });

  connection.on(RealtimeEvents.COMMITTED_TRANSCRIPT_WITH_TIMESTAMPS, (data) => {
    for (const word of data.words) {
      console.log(`${word.text}: ${word.start}s - ${word.end}s`);
    }
  });

  connection.on(RealtimeEvents.ERROR, (error) => {
    console.error("Error:", error);
  });

  connection.on(RealtimeEvents.CLOSE, () => {
    console.log("Disconnected");
  });

  return connection;
}
```

## 手动音频分块

对于文件上传或自定义音频源，请编码为 PCM-16 并分块发送：

```typescript
const chunkSize = 4096;

for (let offset = 0; offset < pcmData.length; offset += chunkSize) {
  const chunk = pcmData.slice(offset, offset + chunkSize);
  const bytes = new Uint8Array(chunk.buffer);
  const base64 = btoa(String.fromCharCode(...bytes));

  scribe.sendAudio(base64);

  // Simulate real-time streaming
  await new Promise((resolve) => setTimeout(resolve, 50));
}

// Finalize transcription
scribe.commit();
```

## 麦克风选项

| 选项 | 说明 |
|--------|-------------|
| `echoCancellation` | 消除扬声器回声 |
| `noiseSuppression` | 过滤背景噪声 |
| `autoGainControl` | 归一化音量 |

## 安全

- 切勿将 API 密钥暴露给客户端
- 始终在后端生成一次性令牌
- 使用身份验证中间件保护令牌端点
