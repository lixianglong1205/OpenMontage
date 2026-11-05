---
name: endpoints
description: BFL API 端点完整文档
---

# BFL API 端点

BFL FLUX API 全部端点的完整参考。

## 基础 URL

| 区域 | 端点                | 使用场景                           |
| ------ | ----------------------- | ---------------------------------- |
| Global | `https://api.bfl.ai`    | 默认，自动故障转移        |
| EU     | `https://api.eu.bfl.ai` | GDPR 合规、欧盟数据驻留 |
| US     | `https://api.us.bfl.ai` | 美国数据驻留                  |

**建议：** 除非有特定区域要求，否则使用全球端点（`api.bfl.ai`）。

## 身份验证

所有请求均需在 `x-key` 请求头中携带 API 密钥：

```bash
x-key: YOUR_API_KEY
```

## FLUX.2 文生图与图生图端点

### FLUX.2 [klein] 4B

```
POST /v1/flux-2-klein-4b
```

生成速度最快，40 亿参数。

### FLUX.2 [klein] 9B

```
POST /v1/flux-2-klein-9b
```

生成较快且质量更好，90 亿参数。

### FLUX.2 [max]

```
POST /v1/flux-2-max
```

最高质量，支持 grounding search（联网检索增强）。

### FLUX.2 [pro]

```
POST /v1/flux-2-pro
```

生产环境在质量与速度之间平衡。

### FLUX.2 [flex]

```
POST /v1/flux-2-flex
```

针对排版优化，可调整 steps/guidance。

## FLUX.1 端点

### FLUX1.1 [pro]

```
POST /v1/flux-pro-1.1
```

文生图（Text-to-Image，T2I）生成。

### FLUX.1 Kontext

```
POST /v1/flux-kontext
```

### FLUX.1 Kontext Max

```
POST /v1/flux-kontext-max
```

### FLUX.1 Fill

```
POST /v1/flux-fill
```

局部重绘与物体移除——通过特定提示词风格，FLUX.2 模型也能实现局部重绘与物体移除，且表现更好。

## 通用请求参数

### 文生图（T2I）

| 参数          | 类型    | 必填 | 说明                                  |
| ------------------ | ------- | -------- | -------------------------------------------- |
| `prompt`           | string  | 是      | 文本描述（最多 32K tokens）          |
| `width`            | integer | 否       | 图像宽度（16 的倍数，总像素不超过 4MP）  |
| `height`           | integer | 否       | 图像高度（16 的倍数，总像素不超过 4MP） |
| `seed`             | integer | 否       | 随机种子，用于可复现生成              |
| `safety_tolerance` | integer | 否       | 0（严格）到 5（宽松），默认 2      |
| `output_format`    | string  | 否       | `"jpeg"` 或 `"png"`，默认 `"jpeg"`              |
| `webhook_url`      | string  | 否       | 异步通知 URL                   |
| `webhook_secret`   | string  | 否       | Webhook 签名校验密钥                 |

### 图生图（I2I）

> **重要：** 所有 FLUX.2 模型（klein、pro、max、flex）均支持通过 `input_image` 参数进行图生图编辑。编辑任务推荐使用 FLUX.2，而非 FLUX.1 Kontext。

> **首选：直接使用 URL**——API 会自动拉取 URL，比下载后编码为 base64 更简单方便。URL 与 base64 均可，但建议在可用时优先使用 URL。

| 参数                         | 类型    | 必填 | 说明                                                    |
| --------------------------------- | ------- | -------- | -------------------------------------------------------------- |
| `prompt`                          | string  | 是      | 编辑指令                                               |
| `input_image`                     | string  | 是      | **URL（首选）** 或 base64——API 会自动拉取 URL |
| `input_image_2` - `input_image_8` | string  | 否       | 额外参考图 URL 或 base64                            |
| `width`                           | integer | 否       | 输出宽度                                                   |
| `height`                          | integer | 否       | 输出高度                                                  |

### FLUX.2 [flex] 专用参数

| 参数  | 类型    | 默认值 | 说明             |
| ---------- | ------- | ------- | ----------------------- |
| `steps`    | integer | 50      | 推理步数（1-50）  |
| `guidance` | float   | 4.5     | 引导系数（1.5-10） |

## 分辨率约束

- **最小：** 64x64 像素
- **最大：** 总像素 4MP（width x height）
- **倍数：** 16（宽、高均需满足）

### 常用分辨率

| 宽高比    | 分辨率 | 百万像素 |
| --------------- | ---------- | ---------- |
| 1:1（方形）    | 1024x1024  | 1.05 MP    |
| 16:9（宽屏）     | 1920x1080  | 2.07 MP    |
| 9:16（竖屏） | 1080x1920  | 2.07 MP    |
| 4:3（经典）   | 1536x1152  | 1.77 MP    |
| 2:1（全景）  | 2048x1024  | 2.10 MP    |

## 请求示例

### 基础 T2I 请求

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A serene mountain landscape at golden hour",
    "width": 1024,
    "height": 1024
  }'
```

### 响应

```json
{
  "id": "gen_abc123xyz",
  "polling_url": "https://api.bfl.ai/v1/get_result?id=gen_abc123xyz"
}
```

### 带全部选项的 T2I

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-max" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Professional headshot of a business executive",
    "width": 1024,
    "height": 1280,
    "seed": 42,
    "safety_tolerance": 2,
    "output_format": "png",
    "webhook_url": "https://your-server.com/webhook",
    "webhook_secret": "your-secret-key"
  }'
```

### I2I 请求（FLUX.2，推荐）

使用任意 FLUX.2 模型，直接传入源图 URL 即可编辑：

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-klein-9b" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Change the floor color to light blue",
    "input_image": "https://example.com/room-photo.jpg"
  }'
```

如需更高质量编辑，可使用 FLUX.2 [pro] 或 [max]：

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Change the background to a beach sunset",
    "input_image": "https://example.com/portrait.jpg"
  }'
```

### 多参考图 I2I（FLUX.2）

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-max" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Person from image 1 wearing outfit from image 2 in setting from image 3",
    "input_image": "https://example.com/person.jpg",
    "input_image_2": "https://example.com/outfit.jpg",
    "input_image_3": "https://example.com/location.jpg"
  }'
```

### 自定义 steps 的 FLUX.2 [flex]

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-flex" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A poster with text \"SUMMER SALE\" in bold typography",
    "steps": 50,
    "guidance": 7.0
  }'
```

## 轮询端点

### 获取结果

```
GET /v1/get_result?id={generation_id}
```

### 响应状态

```json
// Pending
{ "status": "Pending" }

// Ready
{
  "status": "Ready",
  "result": {
    "sample": "https://bfldeliveryprod.blob.core.windows.net/results/...",
    "prompt": "...",
    "seed": 1234567890
  }
}

// Error
{
  "status": "Error",
  "error": "Error description"
}
```

## 错误响应

| 状态码 | 含义          | 处理方式             |
| ----------- | ---------------- | ------------------ |
| 400         | Bad Request      | 检查参数   |
| 401         | Unauthorized     | 验证 API 密钥     |
| 402         | Payment Required | 充值积分        |
| 429         | Rate Limited     | 实现退避重试  |
| 500         | Server Error     | 退避后重试 |
