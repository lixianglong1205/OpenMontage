---
name: video-agent
description: 使用 HeyGen Video Agent API 通过单次提示词生成视频
---

# Video Agent API

Video Agent API 可根据单条文本提示词生成完整视频。与需要逐场景精细配置的标准视频生成 API 不同，Video Agent 会自动处理脚本撰写、数字人选择、画面、旁白、节奏与字幕。

## MCP 工具（首选）

若已连接 HeyGen MCP 服务器，请使用 `mcp__heygen__generate_video_agent`，而非直接调用 API：

```
Tool: mcp__heygen__generate_video_agent
Parameters:
  prompt: "<optimized prompt from prompt-optimizer.md>"
  config:
    duration_sec: 90          # optional, 5-300
    avatar_id: "avatar_id"    # optional, agent selects if omitted
    orientation: "landscape"   # optional, "landscape" or "portrait"
  files:                       # optional
    - asset_id: "uploaded_asset_id"
```

然后使用返回的 `video_id` 调用 `mcp__heygen__get_video` 查询状态。

提示词质量仍是关键因素——无论使用 MCP 还是直接 API，都应始终遵循 [prompt-optimizer.md](prompt-optimizer.md)。

## 何时使用 Video Agent 与标准 API

| 使用场景 | 推荐 API |
|----------|-----------------|
| 从创意快速出片 | Video Agent |
| 对场景、数字人、时间轴精确控制 | Standard v2/video/generate |
| 大规模自动化内容生成 | Video Agent |
| 指定数字人且脚本固定 | Standard v2/video/generate |
| 原型或草稿视频 | Video Agent |
| 品牌规范一致的生产级视频 | Standard v2/video/generate |

## 调用本 API 之前

**必做步骤：** 生成视频前请使用 [prompt-optimizer.md](prompt-optimizer.md) 优化提示词。平庸与专业效果之间的差异完全取决于提示词质量。

快速清单：
1. 定义视觉风格（色彩、美学）——见 [visual-styles.md](visual-styles.md)
2. 用具体场景类型组织场景结构
3. 旁白脚本按约 150 词/分钟撰写
4. 为每个场景指定媒体类型（Motion Graphics、Stock、AI-generated）

## 直接 API 端点

```
POST https://api.heygen.com/v1/video_agent/generate
```

## 请求字段

| 字段 | 类型 | 必填 | 说明 |
|-------|------|:---:|-------------|
| `prompt` | string | ✓ | 描述所需视频的文本提示词 |
| `config` | object | | 配置选项（见下文） |
| `files` | array | | 生成时引用的资源文件 |
| `callback_id` | string | | 用于追踪的自定义 ID。**须同时设置 `callback_url`**——若不需要 Webhook 则两者均省略 |
| `callback_url` | string | | 完成通知的 Webhook URL |

### Config 对象

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `duration_sec` | integer | 大致时长（秒）（5-300） |
| `avatar_id` | string | 指定使用的数字人（可选——未提供时由 Agent 选择） |
| `orientation` | string | `"portrait"` 或 `"landscape"` |

### Files 数组

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `asset_id` | string | 已上传文件的资源 ID，供引用 |

## 响应格式

```json
{
  "error": null,
  "data": {
    "video_id": "abc123"
  }
}
```

## curl 示例

```bash
curl -X POST "https://api.heygen.com/v1/video_agent/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a 60-second product demo video for a new AI-powered calendar app. The tone should be professional but friendly, targeting busy professionals. Highlight the smart scheduling feature and time zone handling."
  }'
```

## TypeScript

```typescript
interface VideoAgentConfig {
  duration_sec?: number;      // 5-300 seconds
  avatar_id?: string;         // Optional: specific avatar
  orientation?: "portrait" | "landscape";
}

interface VideoAgentFile {
  asset_id: string;
}

interface VideoAgentRequest {
  prompt: string;             // Required
  config?: VideoAgentConfig;
  files?: VideoAgentFile[];
  callback_id?: string;       // Requires callback_url if set
  callback_url?: string;
}

interface VideoAgentResponse {
  error: string | null;
  data: {
    video_id: string;
  };
}

async function generateWithVideoAgent(
  prompt: string,
  config?: VideoAgentConfig
): Promise<string> {
  const request: VideoAgentRequest = { prompt };

  if (config) {
    request.config = config;
  }

  const response = await fetch(
    "https://api.heygen.com/v1/video_agent/generate",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  const json: VideoAgentResponse = await response.json();

  if (json.error) {
    throw new Error(`Video Agent failed: ${json.error}`);
  }

  return json.data.video_id;
}
```

## Python

```python
import requests
import os
from typing import Optional

def generate_with_video_agent(
    prompt: str,
    duration_sec: Optional[int] = None,
    avatar_id: Optional[str] = None,
    orientation: Optional[str] = None
) -> str:
    request_body = {"prompt": prompt}

    config = {}
    if duration_sec:
        config["duration_sec"] = duration_sec
    if avatar_id:
        config["avatar_id"] = avatar_id
    if orientation:
        config["orientation"] = orientation

    if config:
        request_body["config"] = config

    response = requests.post(
        "https://api.heygen.com/v1/video_agent/generate",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json"
        },
        json=request_body
    )

    data = response.json()
    if data.get("error"):
        raise Exception(f"Video Agent failed: {data['error']}")

    return data["data"]["video_id"]
```

## 示例

### 基础：仅提示词

```typescript
const videoId = await generateWithVideoAgent(
  "Create a 30-second welcome video for new employees at a tech startup. Keep it energetic and modern."
);
```

### 含时长与方向

```typescript
const videoId = await generateWithVideoAgent(
  "Explain the benefits of cloud computing for small businesses. Use simple language and real-world examples.",
  {
    duration_sec: 90,
    orientation: "landscape"
  }
);
```

### 指定数字人

```typescript
const videoId = await generateWithVideoAgent(
  "Present quarterly sales results. Professional tone, data-focused.",
  {
    duration_sec: 120,
    avatar_id: "josh_lite3_20230714",
    orientation: "landscape"
  }
);
```

### 含参考文件

先上传资源，再引用：

```typescript
// 1. Upload reference materials (see assets.md)
const logoAssetId = await uploadFile("./company-logo.png", "image/png");
const productImageId = await uploadFile("./product-screenshot.png", "image/png");

// 2. Generate video with references
const response = await fetch(
  "https://api.heygen.com/v1/video_agent/generate",
  {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt: "Create a product demo video showcasing our new dashboard feature. Use the uploaded screenshots as visual references.",
      config: {
        duration_sec: 60,
        orientation: "landscape"
      },
      files: [
        { asset_id: logoAssetId },
        { asset_id: productImageId }
      ]
    }),
  }
);
```

## 撰写有效提示词

详见 **[prompt-optimizer.md](prompt-optimizer.md)** 中的完整提示词撰写指南。

提示词优化器涵盖：
- 提示词复杂度层级（基础 → 逐场景）
- 视觉风格分类与色彩指定
- 媒体类型选择（Motion Graphics 与 Stock 与 AI-generated）
- 场景结构与时长计算
- 常见视频类型的即用模板

## 查询视频状态

Video Agent 返回 `video_id`——使用标准状态端点查询进度：

```typescript
// Same polling as standard video generation
const videoUrl = await waitForVideo(videoId);
```

轮询实现见 [video-status.md](video-status.md)。

## 对比：Video Agent 与标准 API

### Video Agent 请求
```typescript
// Simple: describe what you want
const videoId = await generateWithVideoAgent(
  "Create a 60-second tutorial on setting up two-factor authentication. Professional tone, step-by-step."
);
```

### 等效的标准 API 请求
```typescript
// Complex: specify every detail
const videoId = await generateVideo({
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Welcome to this tutorial on two-factor authentication...",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "color",
        value: "#1a1a2e",
      },
    },
    // ... more scenes for each step
  ],
  dimension: { width: 1920, height: 1080 },
});
```

## 限制

- 对脚本措辞的控制较弱
- 未指定时数字人选择可能变化
- 场景构图由系统自动完成
- 可能无法完全符合精确的品牌规范
- 时长为近似值，非精确值

## 最佳实践

1. **提示词要具体**——细节越多，效果越好
2. **指定时长**——使用 `config.duration_sec` 以获得可预期的长度
3. **需要时锁定数字人**——使用 `config.avatar_id` 保持一致性
4. **上传参考文件**——帮助 Agent 理解你的品牌/产品
5. **迭代提示词**——根据结果持续优化
6. **用于草稿**——Video Agent 适合在最终制作前快速迭代
