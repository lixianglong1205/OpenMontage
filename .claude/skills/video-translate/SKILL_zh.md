---
name: video-translate
description: |
  使用 HeyGen 将现有视频翻译并配音为多种语言。适用于：(1) 将视频翻译为另一种语言，(2) 对视频内容进行口型同步配音，(3) 为现有视频制作多语言版本，(4) 仅翻译音频、不做口型同步，(5) 使用 HeyGen 的 /v2/video_translate 端点。
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# 视频翻译（HeyGen）

将现有视频翻译并配音为多种语言，保留口型同步与自然语音节奏。提供视频 URL 或 HeyGen 视频 ID 即可——无需先在 HeyGen 上创建该视频。

## 身份验证

所有请求都需要 `X-Api-Key` 请求头。请设置 `HEYGEN_API_KEY` 环境变量。

```bash
curl -X POST "https://api.heygen.com/v2/video_translate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video_url": "https://example.com/video.mp4", "output_language": "es-ES"}'
```

## 默认工作流

1. 提供视频 URL 或 HeyGen 视频 ID
2. 调用 `POST /v2/video_translate`，指定目标语言
3. 轮询 `GET /v2/video_translate/{translate_id}`，直到状态为 `completed`
4. 从返回的 URL 下载翻译后的视频

## 创建翻译任务

### 请求字段

| 字段 | 类型 | 必填 | 说明 |
|-------|------|:---:|-------------|
| `video_url` | string | Y* | 待翻译视频的 URL（*或 `video_id`） |
| `video_id` | string | Y* | HeyGen 视频 ID（*或 `video_url`） |
| `output_language` | string | Y | 目标语言代码（例如 `"es-ES"`） |
| `title` | string | | 翻译后视频的名称 |
| `translate_audio_only` | boolean | | 仅音频、无口型同步（更快） |
| `speaker_num` | number | | 视频中的说话人数量 |
| `callback_id` | string | | 用于 Webhook 跟踪的自定义 ID |
| `callback_url` | string | | 完成通知的 URL |

**必须**提供 `video_url` **或** `video_id` 其中之一。

### curl

```bash
curl -X POST "https://api.heygen.com/v2/video_translate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://example.com/original-video.mp4",
    "output_language": "es-ES",
    "title": "Spanish Version"
  }'
```

### TypeScript

```typescript
interface VideoTranslateRequest {
  video_url?: string;
  video_id?: string;
  output_language: string;
  title?: string;
  translate_audio_only?: boolean;
  speaker_num?: number;
  callback_id?: string;
  callback_url?: string;
}

interface VideoTranslateResponse {
  error: null | string;
  data: {
    video_translate_id: string;
  };
}

async function translateVideo(config: VideoTranslateRequest): Promise<string> {
  const response = await fetch("https://api.heygen.com/v2/video_translate", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(config),
  });

  const json: VideoTranslateResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.video_translate_id;
}
```

### Python

```python
import requests
import os

def translate_video(config: dict) -> str:
    response = requests.post(
        "https://api.heygen.com/v2/video_translate",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json"
        },
        json=config
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]["video_translate_id"]
```

## 支持的语言

| 语言 | 代码 | 备注 |
|----------|------|-------|
| English (US) | en-US | 默认源语言 |
| Spanish (Spain) | es-ES | 欧洲西班牙语 |
| Spanish (Mexico) | es-MX | 拉丁美洲西班牙语 |
| French | fr-FR | 标准法语 |
| German | de-DE | 标准德语 |
| Italian | it-IT | 标准意大利语 |
| Portuguese (Brazil) | pt-BR | 巴西葡萄牙语 |
| Japanese | ja-JP | 标准日语 |
| Korean | ko-KR | 标准韩语 |
| Chinese (Mandarin) | zh-CN | 简体中文 |
| Hindi | hi-IN | 标准印地语 |
| Arabic | ar-SA | 现代标准阿拉伯语 |

## 翻译选项

### 基础翻译（含口型同步）

```typescript
const config = {
  video_url: "https://example.com/original.mp4",
  output_language: "es-ES",
  title: "Spanish Translation",
};
```

### 仅音频翻译（更快，无口型同步）

```typescript
const config = {
  video_url: "https://example.com/original.mp4",
  output_language: "es-ES",
  translate_audio_only: true,
};
```

### 多说话人视频

```typescript
const config = {
  video_url: "https://example.com/interview.mp4",
  output_language: "fr-FR",
  speaker_num: 2,
};
```

## 高级选项（v4 API）

如需更精细的翻译控制：

```typescript
interface VideoTranslateV4Request {
  input_video_id?: string;
  google_url?: string;
  output_languages: string[];        // Multiple languages in one call
  name: string;
  srt_key?: string;                  // Custom SRT subtitles
  instruction?: string;
  vocabulary?: string[];             // Terms to preserve as-is
  brand_voice_id?: string;
  speaker_num?: number;
  keep_the_same_format?: boolean;
  input_language?: string;
  enable_video_stretching?: boolean;
  disable_music_track?: boolean;
  enable_speech_enhancement?: boolean;
  srt_role?: "input" | "output";
  translate_audio_only?: boolean;
}
```

### 多种输出语言

```typescript
const config = {
  input_video_id: "original_video_id",
  output_languages: ["es-ES", "fr-FR", "de-DE"],
  name: "Multi-language translations",
};
```

### 自定义词汇（保留特定术语）

```typescript
const config = {
  video_url: "https://example.com/product-demo.mp4",
  output_language: "ja-JP",
  vocabulary: ["SuperWidget", "Pro Max", "TechCorp"],
};
```

### 自定义 SRT 字幕

```typescript
const config = {
  video_url: "https://example.com/video.mp4",
  output_language: "es-ES",
  srt_key: "path/to/custom-subtitles.srt",
  srt_role: "input",
};
```

## 查询翻译状态

### curl

```bash
curl -X GET "https://api.heygen.com/v2/video_translate/{translate_id}" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface TranslateStatusResponse {
  error: null | string;
  data: {
    id: string;
    status: "pending" | "processing" | "completed" | "failed";
    video_url?: string;
    message?: string;
  };
}

async function getTranslateStatus(translateId: string): Promise<TranslateStatusResponse["data"]> {
  const response = await fetch(
    `https://api.heygen.com/v2/video_translate/${translateId}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const json: TranslateStatusResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data;
}
```

## 轮询直至完成

翻译耗时通常长于标准视频生成——请预留最多 30 分钟。

```typescript
async function waitForTranslation(
  translateId: string,
  maxWaitMs = 1800000,
  pollIntervalMs = 30000
): Promise<string> {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWaitMs) {
    const status = await getTranslateStatus(translateId);

    switch (status.status) {
      case "completed":
        return status.video_url!;
      case "failed":
        throw new Error(status.message || "Translation failed");
      default:
        console.log(`Status: ${status.status}...`);
        await new Promise((r) => setTimeout(r, pollIntervalMs));
    }
  }

  throw new Error("Translation timed out");
}
```

## 完整工作流

```typescript
async function translateAndDownload(
  videoUrl: string,
  targetLanguage: string
): Promise<string> {
  console.log(`Starting translation to ${targetLanguage}...`);
  const translateId = await translateVideo({
    video_url: videoUrl,
    output_language: targetLanguage,
  });
  console.log(`Translation ID: ${translateId}`);

  console.log("Processing translation...");
  const translatedVideoUrl = await waitForTranslation(translateId);
  console.log(`Translation complete: ${translatedVideoUrl}`);

  return translatedVideoUrl;
}

const spanishVideo = await translateAndDownload(
  "https://example.com/my-video.mp4",
  "es-ES"
);
```

## 批量翻译

并行翻译为多种语言：

```typescript
async function translateToMultipleLanguages(
  sourceVideoUrl: string,
  targetLanguages: string[]
): Promise<Record<string, string>> {
  const results: Record<string, string> = {};

  const translatePromises = targetLanguages.map(async (lang) => {
    const translateId = await translateVideo({
      video_url: sourceVideoUrl,
      output_language: lang,
    });
    return { lang, translateId };
  });

  const translationJobs = await Promise.all(translatePromises);

  for (const job of translationJobs) {
    try {
      const videoUrl = await waitForTranslation(job.translateId);
      results[job.lang] = videoUrl;
    } catch (error) {
      results[job.lang] = `error: ${error.message}`;
    }
  }

  return results;
}

const translations = await translateToMultipleLanguages(
  "https://example.com/original.mp4",
  ["es-ES", "fr-FR", "de-DE", "ja-JP"]
);
```

## 功能特性

- **口型同步（Lip Sync）** — 自动调整说话人口型以匹配翻译后的音频
- **声音克隆（Voice Cloning）** — 翻译后的音频保留原说话人的音色特征
- **音轨控制** — 可通过 `disable_music_track: true` 可选移除背景音乐
- **语音增强** — 通过 `enable_speech_enhancement: true` 提升音频质量

## 最佳实践

1. **源视频质量很重要** — 使用高质量源视频以获得更好效果
2. **清晰人声** — 语音清晰的视频翻译效果更好
3. **单人出镜** — 单人内容效果最佳
4. **适中语速** — 语速过快可能影响质量
5. **先小规模试译** — 长视频翻译前先用较短片段测试
6. **预留更多时间** — 翻译比视频生成更耗时（最多约 30 分钟）

## 错误处理

常见错误及处理方式：

```typescript
async function safeTranslate(
  videoUrl: string,
  targetLanguage: string
): Promise<{ success: boolean; result?: string; error?: string }> {
  try {
    const url = await translateAndDownload(videoUrl, targetLanguage);
    return { success: true, result: url };
  } catch (error) {
    if (error.message.includes("quota")) {
      return { success: false, error: "Insufficient credits" };
    }
    if (error.message.includes("duration")) {
      return { success: false, error: "Video too long" };
    }
    if (error.message.includes("format")) {
      return { success: false, error: "Unsupported video format" };
    }
    return { success: false, error: error.message };
  }
}
```
