---
name: ai-video-gen
description: |
  通过多个提供商网关，从文本提示生成 AI 视频。适用场景：(1) 根据文本描述生成视频，(2) 为内容制作创建 AI 生成视频片段，(3) 使用参考图进行图生视频，(4) 在视频生成提供商之间选择（VEO、Kling、Sora、Runway、Seedance、MiniMax、Gemini Omni）。支持的网关：HeyGen API、fal.ai API、Kling 官方直连 API，以及 Gemini API（Gemini Omni Flash）。
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env_any:
        - HEYGEN_API_KEY
        - FAL_KEY
        - KLING_API_KEY
        - GEMINI_API_KEY
        - GOOGLE_API_KEY
---

# 视频生成（多网关）

从文本提示生成 AI 视频。通过四条 API 路径支持多个提供商：

| 网关 | 环境变量 | 提供商 | 工具 |
|---------|-------------|-----------|------|
| **fal.ai** | `FAL_KEY` | **Seedance 2.0**（标准版 + 快速版）、Kling v3/v2.1、MiniMax、VEO | `seedance_video`、`kling_video`、`minimax_video`、`veo_video` |
| **HeyGen** | `HEYGEN_API_KEY` | VEO 3.1、Kling Pro、Sora v2、Runway Gen-4、Seedance Pro / Lite (1.x) | `heygen_video` |
| **Kling Official** | `KLING_API_KEY` | Kling 官方 Classic、Turbo 及基础 Omni 视频 | `kling_official_video` |
| **Gemini API** | `GEMINI_API_KEY` / `GOOGLE_API_KEY` | Gemini Omni Flash（生成 + 对话式编辑） | `gemini_omni_video` |

**迭代编辑 — Gemini Omni。** 当需求是*在现有片段上精修*（增删物体、改风格、调整光照或画面文字）而非重新生成时，Gemini Omni Flash 是整套能力中唯一支持有状态多轮编辑的提供商。在为它编写任何提示词之前，请参阅 Layer 3 的 `gemini-omni` 权威提示指南（参考图标签、时间码语法、编辑提示规则）。

**首选高端默认 — Seedance 2.0。** 当任一高端网关已配置（`FAL_KEY` → `seedance_video`，或 HeyGen 的 Video Agent / Avatar Shots 路径）时，Seedance 2.0 是电影感、预告片与高保真片段工作的首选默认。它是整套模型中唯一支持**单次通过原生同步音频、多镜头生成、导演级运镜控制，以及引用对白唇形同步**的模型，截至 2026 年初在 Artificial Analysis Elo 上排名第一。仅在用户有明确理由时再切换（预算、提供商偏好、或 VEO 写实风景 / Kling 特定动漫风格等风格适配）。请参阅 Layer 3 的 `seedance-2-0` 权威提示与参数指南。

**重要：** 始终使用 `video_selector`，不要直接调用各提供商工具。选择器负责可用性检查、成本对比与自动降级；其评分引擎已对电影化意图偏向 Seedance 2.0。

## 身份验证

根据用户可用的提供商以及成本/质量目标，选用已配置且最匹配的网关。

- **HeyGen：** 设置 `HEYGEN_API_KEY` 以访问多模型网关。
- **fal.ai：** 设置 `FAL_KEY`，经 fal.ai 使用 Kling、MiniMax 与 Veo。
- **Kling Official：** 设置 `KLING_API_KEY`，经 `provider="kling_official"` 访问 Kling 官方直连 API。
- **Gemini API：** 设置 `GEMINI_API_KEY` 或 `GOOGLE_API_KEY`，以使用 Gemini Omni 视频生成与对话式编辑。

在未先核对注册表与当前任务匹配度之前，不要将任何网关描述为默认或首选。

fal.ai 上的 Kling（`kling_video`，`provider="kling"`）与 Kling Official（`kling_official_video`，`provider="kling_official"`）是不同路径。选定官方提供商时，不要复用 fal.ai 队列 URL、`FAL_KEY` 或图片上传行为。

```bash
curl -X POST "https://api.heygen.com/v1/workflows/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"workflow_type": "GenerateVideoNode", "input": {"prompt": "A drone shot flying over a coastal city at sunset"}}'
```

## 默认工作流

1. 调用 `POST /v1/workflows/executions`，传入 `workflow_type: "GenerateVideoNode"` 与你的提示词
2. 在响应中获得 `execution_id`
3. 每 10 秒轮询 `GET /v1/workflows/executions/{id}`，直至状态为 `completed`
4. 使用输出中的 `video_url`

## 执行视频生成

### 端点

`POST https://api.heygen.com/v1/workflows/executions`

### 请求字段

| 字段 | 类型 | 必填 | 说明 |
|-------|------|:---:|-------------|
| `workflow_type` | string | Y | 必须为 `"GenerateVideoNode"` |
| `input.prompt` | string | Y | 待生成视频的文本描述 |
| `input.provider` | string | | 视频生成提供商（默认：`"veo_3_1"`）。见下方「提供商」。 |
| `input.aspect_ratio` | string | | 宽高比（默认：`"16:9"`）。常用值：`"16:9"`、`"9:16"`、`"1:1"` |
| `input.reference_image_url` | string | | 图生视频的参考图 URL |
| `input.tail_image_url` | string | | 末帧引导用的尾帧图 URL |
| `input.config` | object | | 提供商专属配置覆盖 |

### 提供商

| 提供商 | 值 | 说明 |
|----------|-------|-------------|
| VEO 3.1 | `"veo_3_1"` | Google VEO 3.1（默认，最高质量） |
| VEO 3.1 Fast | `"veo_3_1_fast"` | 更快的 VEO 3.1 变体 |
| VEO 3 | `"veo3"` | Google VEO 3 |
| VEO 3 Fast | `"veo3_fast"` | 更快的 VEO 3 变体 |
| VEO 2 | `"veo2"` | Google VEO 2 |
| Kling Pro | `"kling_pro"` | Kling Pro 模型 |
| Kling V2 | `"kling_v2"` | Kling V2 模型 |
| Sora V2 | `"sora_v2"` | OpenAI Sora V2 |
| Sora V2 Pro | `"sora_v2_pro"` | OpenAI Sora V2 Pro |
| Runway Gen-4 | `"runway_gen4"` | Runway Gen-4 |
| Seedance Lite | `"seedance_lite"` | Seedance Lite |
| Seedance Pro | `"seedance_pro"` | Seedance Pro |
| LTX Distilled | `"ltx_distilled"` | LTX Distilled（最快） |

### curl

```bash
curl -X POST "https://api.heygen.com/v1/workflows/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "GenerateVideoNode",
    "input": {
      "prompt": "A drone shot flying over a coastal city at golden hour, cinematic lighting",
      "provider": "veo_3_1",
      "aspect_ratio": "16:9"
    }
  }'
```

### TypeScript

```typescript
interface GenerateVideoInput {
  prompt: string;
  provider?: string;
  aspect_ratio?: string;
  reference_image_url?: string;
  tail_image_url?: string;
  config?: Record<string, any>;
}

interface ExecuteResponse {
  data: {
    execution_id: string;
    status: "submitted";
  };
}

async function generateVideo(input: GenerateVideoInput): Promise<string> {
  const response = await fetch("https://api.heygen.com/v1/workflows/executions", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      workflow_type: "GenerateVideoNode",
      input,
    }),
  });

  const json: ExecuteResponse = await response.json();
  return json.data.execution_id;
}
```

### Python

```python
import requests
import os

def generate_video(
    prompt: str,
    provider: str = "veo_3_1",
    aspect_ratio: str = "16:9",
    reference_image_url: str | None = None,
    tail_image_url: str | None = None,
) -> str:
    payload = {
        "workflow_type": "GenerateVideoNode",
        "input": {
            "prompt": prompt,
            "provider": provider,
            "aspect_ratio": aspect_ratio,
        },
    }

    if reference_image_url:
        payload["input"]["reference_image_url"] = reference_image_url
    if tail_image_url:
        payload["input"]["tail_image_url"] = tail_image_url

    response = requests.post(
        "https://api.heygen.com/v1/workflows/executions",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json=payload,
    )

    data = response.json()
    return data["data"]["execution_id"]
```

### 响应格式

```json
{
  "data": {
    "execution_id": "node-gw-v1d2e3o4",
    "status": "submitted"
  }
}
```

## 查询状态

### 端点

`GET https://api.heygen.com/v1/workflows/executions/{execution_id}`

### curl

```bash
curl -X GET "https://api.heygen.com/v1/workflows/executions/node-gw-v1d2e3o4" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### 响应格式（已完成）

```json
{
  "data": {
    "execution_id": "node-gw-v1d2e3o4",
    "status": "completed",
    "output": {
      "video": {
        "video_url": "https://resource.heygen.ai/generated/video.mp4",
        "video_id": "abc123"
      },
      "asset_id": "asset-xyz789"
    }
  }
}
```

## 轮询直至完成

```typescript
async function generateVideoAndWait(
  input: GenerateVideoInput,
  maxWaitMs = 600000,
  pollIntervalMs = 10000
): Promise<{ video_url: string; video_id: string; asset_id: string }> {
  const executionId = await generateVideo(input);
  console.log(`Submitted video generation: ${executionId}`);

  const startTime = Date.now();
  while (Date.now() - startTime < maxWaitMs) {
    const response = await fetch(
      `https://api.heygen.com/v1/workflows/executions/${executionId}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );
    const { data } = await response.json();

    switch (data.status) {
      case "completed":
        return {
          video_url: data.output.video.video_url,
          video_id: data.output.video.video_id,
          asset_id: data.output.asset_id,
        };
      case "failed":
        throw new Error(data.error?.message || "Video generation failed");
      case "not_found":
        throw new Error("Workflow not found");
      default:
        await new Promise((r) => setTimeout(r, pollIntervalMs));
    }
  }

  throw new Error("Video generation timed out");
}
```

## 使用示例

### 简单文生视频

```bash
curl -X POST "https://api.heygen.com/v1/workflows/executions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "GenerateVideoNode",
    "input": {
      "prompt": "A person walking through a sunlit park, shallow depth of field"
    }
  }'
```

### 图生视频

```json
{
  "workflow_type": "GenerateVideoNode",
  "input": {
    "prompt": "Animate this product photo with a slow zoom and soft particle effects",
    "reference_image_url": "https://example.com/product-photo.png",
    "provider": "kling_pro"
  }
}
```

### 社交媒体竖屏格式

```json
{
  "workflow_type": "GenerateVideoNode",
  "input": {
    "prompt": "A trendy coffee shop interior, camera slowly panning across the counter",
    "aspect_ratio": "9:16",
    "provider": "veo_3_1"
  }
}
```

### 使用 LTX 快速生成

```json
{
  "workflow_type": "GenerateVideoNode",
  "input": {
    "prompt": "Abstract colorful shapes morphing and flowing",
    "provider": "ltx_distilled"
  }
}
```

## 最佳实践

1. **提示词要具体** — 包含运镜、光照、风格与氛围细节
2. **电影化与运动主导任务在已设置 `FAL_KEY` 时默认优先 Seedance 2.0（经 `seedance_video`）** — 单次通过同步音频、多镜头、唇形同步、导演级运镜。用户明确要 Google 或 OpenAI 运动特征时用 VEO 3.1 / Sora V2 Pro；仅在速度是硬约束时用 `ltx_distilled` 或 `veo3_fast`
3. **图生视频使用参考图** — 适合为产品照或静帧做动画
4. **视频生成是最慢的工作流之一** — 最多等待约 5 分钟，每 10 秒轮询一次
5. **宽高比很重要** — 社媒 Story/Reels 用 `9:16`，横屏用 `16:9`，方形用 `1:1`
6. **输出包含 `asset_id`** — 可在其他 HeyGen 工作流中引用生成的视频
7. **输出 URL 为临时链接** — 请及时下载或保存生成的视频
