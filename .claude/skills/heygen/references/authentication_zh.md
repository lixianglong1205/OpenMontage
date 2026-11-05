---
name: authentication
description: HeyGen 的 API 密钥配置、X-Api-Key 请求头及认证模式
---

# HeyGen 认证

所有 HeyGen API 请求都需要通过 `X-Api-Key` 请求头传入 API 密钥进行认证。

## 获取 API 密钥

1. 打开 https://app.heygen.com/settings?from=&nav=API
2. 若提示登录，请先登录
3. 复制你的 API 密钥

## 环境配置

将 API 密钥安全地存为环境变量：

```bash
export HEYGEN_API_KEY="your-api-key-here"
```

在 `.env` 文件中：

```
HEYGEN_API_KEY=your-api-key-here
```

## 发起已认证请求

### curl

```bash
curl -X GET "https://api.heygen.com/v2/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript/JavaScript (fetch)

```typescript
const response = await fetch("https://api.heygen.com/v2/avatars", {
  headers: {
    "X-Api-Key": process.env.HEYGEN_API_KEY!,
  },
});
const { data } = await response.json();
```

### TypeScript/JavaScript (axios)

```typescript
import axios from "axios";

const client = axios.create({
  baseURL: "https://api.heygen.com",
  headers: {
    "X-Api-Key": process.env.HEYGEN_API_KEY,
  },
});

const { data } = await client.get("/v2/avatars");
```

### Python (requests)

```python
import os
import requests

response = requests.get(
    "https://api.heygen.com/v2/avatars",
    headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]}
)
data = response.json()
```

### Python (httpx)

```python
import os
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(
        "https://api.heygen.com/v2/avatars",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]}
    )
    data = response.json()
```

## 创建可复用的 API 客户端

### TypeScript

```typescript
class HeyGenClient {
  private baseUrl = "https://api.heygen.com";
  private apiKey: string;

  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        "X-Api-Key": this.apiKey,
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || `HTTP ${response.status}`);
    }

    return response.json();
  }

  get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint);
  }

  post<T>(endpoint: string, body: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    });
  }
}

// Usage
const client = new HeyGenClient(process.env.HEYGEN_API_KEY!);
const avatars = await client.get("/v2/avatars");
```

## API 响应格式

所有 HeyGen API 响应均遵循以下结构：

```typescript
interface ApiResponse<T> {
  error: null | string;
  data: T;
}
```

成功响应示例：

```json
{
  "error": null,
  "data": {
    "avatars": [...]
  }
}
```

错误响应示例：

```json
{
  "error": "Invalid API key",
  "data": null
}
```

## 错误处理

常见认证错误：

| 状态码 | 错误 | 原因 |
|-------------|-------|-------|
| 401 | Invalid API key | API 密钥缺失或错误 |
| 403 | Forbidden | API 密钥缺少所需权限 |
| 429 | Rate limit exceeded | 请求过于频繁 |

### 处理错误

```typescript
async function makeRequest(endpoint: string) {
  const response = await fetch(`https://api.heygen.com${endpoint}`, {
    headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
  });

  const json = await response.json();

  if (!response.ok || json.error) {
    throw new Error(json.error || `HTTP ${response.status}`);
  }

  return json.data;
}
```

## 速率限制

HeyGen 对 API 请求实施速率限制：
- 标准速率限制按 API 密钥生效
- 部分端点（如视频生成）限制更严
- 收到 429 错误时使用指数退避（exponential backoff）

```typescript
async function requestWithRetry(
  fn: () => Promise<Response>,
  maxRetries = 3
): Promise<Response> {
  for (let i = 0; i < maxRetries; i++) {
    const response = await fn();

    if (response.status === 429) {
      const waitTime = Math.pow(2, i) * 1000;
      await new Promise((resolve) => setTimeout(resolve, waitTime));
      continue;
    }

    return response;
  }

  throw new Error("Max retries exceeded");
}
```

## 安全最佳实践

1. **切勿在客户端代码中暴露 API 密钥** — 始终从后端服务器发起 API 调用
2. **使用环境变量** — 不要在源代码中硬编码 API 密钥
3. **定期轮换密钥** — 定期生成新的 API 密钥
4. **监控使用情况** — 在 HeyGen 控制台中关注异常活动
