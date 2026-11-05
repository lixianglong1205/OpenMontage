---
name: bfl-api
description: BFL FLUX API 集成指南，涵盖端点、异步轮询模式、速率限制、错误处理、Webhook 与区域端点，并提供 Python 与 TypeScript 代码示例。
metadata:
  author: Black Forest Labs
  version: "1.0.0"
  tags: flux, bfl, api, integration, webhooks, rate-limiting
---

# BFL API 集成指南

在将 BFL FLUX API 集成到应用中以进行图像生成、编辑与处理时，使用本技能。

## 首先：检查 API Key

**在生成图像之前，请确认已设置 API key：**

```bash
echo $BFL_API_KEY
```

若为空或出现 “Not authenticated” 错误，请参阅下文 [API Key 设置](#api-key-setup)。

## 重要：图像 URL 在 10 分钟后过期

API 返回的结果 URL 为临时链接。生成完成后请立即下载图像——不要存储或缓存 URL 本身。

## 适用场景

- 搭建 BFL API 客户端
- 实现异步轮询模式
- 处理速率限制与错误
- 为生产环境配置 Webhook
- 选择区域端点
- 构建可用于生产的集成

## 快速参考

### 基础端点

| 区域 | 端点                    | 用途                         |
| ------ | ----------------------- | --------------------------- |
| Global | `https://api.bfl.ai`    | 默认，自动故障转移           |
| EU     | `https://api.eu.bfl.ai` | GDPR 合规                    |
| US     | `https://api.us.bfl.ai` | 美国数据驻留                 |

### 模型端点与定价

> **积分定价：** 1 credit = $0.01 USD。FLUX.2 按百万像素（megapixel）计费（成本随分辨率变化）。

#### FLUX.2 模型

| 模型              | 路径                  | 首 MP | +MP  | 1MP T2I | 1MP I2I | 最适合                           |
| ----------------- | --------------------- | ------ | ---- | ------- | ------- | -------------------------------- |
| FLUX.2 [klein] 4B | `/v1/flux-2-klein-4b` | 1.4c   | 0.1c | $0.014  | $0.015  | 实时、高并发                     |
| FLUX.2 [klein] 9B | `/v1/flux-2-klein-9b` | 1.5c   | 0.2c | $0.015  | $0.017  | 质量与速度平衡                   |
| FLUX.2 [pro]      | `/v1/flux-2-pro`      | 3c     | 1.5c | $0.03   | $0.045  | 生产环境、快速周转               |
| FLUX.2 [max]      | `/v1/flux-2-max`      | 7c     | 3c   | $0.07   | $0.10   | 最高质量                         |
| FLUX.2 [flex]     | `/v1/flux-2-flex`     | 5c     | 5c   | $0.05   | $0.10   | 排版、可调参数                   |
| FLUX.2 [dev]      | -                     | -      | -    | Free    | Free    | 本地开发（非商业）               |

> **定价公式：** `(firstMP + (outputMP-1) * mpPrice) + (inputMP * mpPrice)`（单位：分）

#### FLUX.1 模型

| 模型                 | 路径                     | 单价/张 | 最适合                        |
| -------------------- | ------------------------ | ----------- | ----------------------------- |
| FLUX.1 Kontext [pro] | `/v1/flux-kontext`       | $0.04       | 带上下文的图像编辑            |
| FLUX.1 Kontext [max] | `/v1/flux-kontext-max`   | $0.08       | 最高质量编辑                  |
| FLUX1.1 [pro]        | `/v1/flux-pro-1.1`       | $0.04       | 标准 T2I，快速可靠            |
| FLUX1.1 [pro] Ultra  | `/v1/flux-pro-1.1-ultra` | $0.06       | 超高分辨率                    |
| FLUX1.1 [pro] Raw    | `/v1/flux-pro-1.1-raw`   | $0.06       | 自然抓拍摄影风格              |
| FLUX.1 Fill [pro]    | `/v1/flux-pro-1.0-fill`  | $0.05       | 局部重绘（inpainting）        |

> **提示：** 所有 FLUX.2 模型均通过 `input_image` 参数支持图像编辑——无需单独的编辑端点。不同分辨率下的精确费用请使用 [bfl.ai/pricing](https://bfl.ai/pricing) 计算器。

### 编辑用的图像输入

**推荐：直接使用 URL**——比 base64 更简单、更方便。

**单图编辑：**

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: $BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Change the background to a sunset",
    "input_image": "https://example.com/photo.jpg"
  }'
```

**多参考图编辑：**

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: $BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The person from image 1 in the environment from image 2",
    "input_image": "https://example.com/person.jpg",
    "input_image_2": "https://example.com/background.jpg"
  }'
```

API 会自动拉取 URL。URL 与 base64 均可，但在可用时建议使用 URL。

### 多参考图 I2I

FLUX.2 模型支持多张输入图像，用于合成元素、风格迁移与角色一致性：

| 模型                  | 最大参考图数量 |
| --------------------- | -------------- |
| FLUX.2 [klein]        | 4 张           |
| FLUX.2 [pro/max/flex] | 8 张           |

**参数：** `input_image`、`input_image_2`、`input_image_3`、… `input_image_8`

**提示词模式：** 在提示词中按编号引用图像：

- "The subject from image 1 in the environment from image 2"
- "Apply the style of image 2 to the scene in image 1"
- "The person from image 1 wearing the outfit from image 2, in the pose from image 3"

> 多参考图模式（角色一致性、风格迁移、姿态引导等）详见 `flux-best-practices/rules/multi-reference-editing.md`

### 速率限制

| 层级                      | 并发请求数 |
| ------------------------- | ------------------- |
| Standard（多数端点）      | 24                  |

### 轮询 vs Webhook

| 方式         | 适用情况                                                                             |
| ------------ | ------------------------------------------------------------------------------------ |
| **Polling**  | 脚本、CLI 工具、本地开发、单次请求、简单集成                                         |
| **Webhooks** | 生产应用、高并发、服务端到服务端、需要即时通知时                                     |

**先从轮询开始**——更简单且随处可用。需要扩展或事件驱动架构时再切换到 Webhook。

### 关键行为

- **Polling**：响应中包含用于异步结果的 `polling_url`
- **URL 过期**：结果 URL 在 10 分钟后失效
- **Webhook 支持**：生产负载可配置 `webhook_url`

## API Key 设置

**必需**：使用 API 前必须设置 `BFL_API_KEY` 环境变量。

### 快速检查

```bash
echo $BFL_API_KEY
```

### 若未设置

1. **获取 key**：打开 https://dashboard.bfl.ai/get-started → 点击 **「Create Key」** → 选择组织
2. **写入 `.env`**（推荐，便于持久化）：
   ```bash
   echo 'BFL_API_KEY=bfl_your_key_here' >> .env
   echo '.env' >> .gitignore  # Don't commit secrets
   ```

详细设置步骤见 [references/api-key-setup.md](references/api-key-setup.md)。

## 认证

```bash
x-key: YOUR_API_KEY
```

## 基本请求流程

```
1. POST request to model endpoint
   └─> Response: { "polling_url": "..." }

2. GET polling_url (repeat until complete)
   └─> Response: { "status": "Pending" | "Ready" | "Error", ... }

3. When Ready, download result URL
   └─> URL expires in 10 minutes - download immediately
```

## 相关资源

- **提示词最佳实践**（T2I、I2I、排版、颜色）：见 **flux-best-practices** 技能
- **多参考图模式**（角色一致性、风格迁移、姿态引导）：见 `flux-best-practices/rules/multi-reference-editing.md`

## 参考文档

- [references/api-key-setup.md](references/api-key-setup.md) - **API key 创建与配置**
- [references/endpoints.md](references/endpoints.md) - 完整端点文档
- [references/polling-patterns.md](references/polling-patterns.md) - 异步轮询实现
- [references/rate-limiting.md](references/rate-limiting.md) - 速率限制处理策略
- [references/error-handling.md](references/error-handling.md) - 错误码与恢复
- [references/webhook-integration.md](references/webhook-integration.md) - Webhook 设置与安全

### 代码示例

> **注意：** 默认优先使用 cURL 示例，因其通用且无需 Python 或 Node.js。构建生产应用时可使用特定语言客户端。

- [references/code-examples/curl-examples.sh](references/code-examples/curl-examples.sh) - **cURL 示例（推荐）**
- [references/code-examples/python-client.py](references/code-examples/python-client.py) - Python 客户端
- [references/code-examples/typescript-client.ts](references/code-examples/typescript-client.ts) - TypeScript 客户端

## 快速开始示例

### 1. 提交生成请求

```bash
curl -s -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: $BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A serene mountain landscape at sunset", "width": 1024, "height": 1024}'
```

响应：

```json
{ "id": "abc123", "polling_url": "https://api.bfl.ai/v1/get_result?id=abc123" }
```

### 2. 轮询结果

```bash
curl -s "POLLING_URL" -H "x-key: $BFL_API_KEY"
```

就绪时的响应：

```json
{ "status": "Ready", "result": { "sample": "https://...", "seed": 1234 } }
```

### 3. 下载图像

```bash
curl -s -o output.png "IMAGE_URL"
```

> **提示：** 结果 URL 在 10 分钟后过期。状态变为 `Ready` 后请立即下载。

### 4. 多参考图示例

从多张图像合成元素：

```bash
curl -s -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: $BFL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The cat from image 1 sitting in the cozy room from image 2",
    "input_image": "https://example.com/cat.jpg",
    "input_image_2": "https://example.com/room.jpg",
    "width": 1024,
    "height": 1024
  }'
```

在提示词中按编号引用图像。限制与模式见 [多参考图 I2I](#multi-reference-i2i)。
