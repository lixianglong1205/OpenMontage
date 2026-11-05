---
name: polling-patterns
description: 实现 BFL API 响应的异步轮询
---

# 轮询模式

BFL API 采用异步生成。所有请求都会返回用于状态检查的 `polling_url`。

## 基本流程

```
1. POST request to model endpoint
   └─> Immediate response: { "polling_url": "..." }

2. GET polling_url (repeat until complete)
   └─> { "status": "Pending" | "Ready" | "Error" }

3. When "Ready", download result sample URL
   └─> URL expires in 10 minutes
```

## 响应状态

| 状态 | 说明 | 操作 |
|--------|-------------|--------|
| `Pending` | 请求已排队/处理中 | 继续轮询 |
| `Ready` | 生成已完成 | 下载结果 |
| `Error` | 生成错误 | 处理错误 |

## 轮询策略

### 简单固定间隔

```python
import time
import requests

def poll_fixed_interval(polling_url, headers, interval=2, timeout=120):
    """Simple polling with fixed interval."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        response = requests.get(polling_url, headers=headers)
        data = response.json()

        if data["status"] == "Ready":
            return data["result"]
        elif data["status"] == "Error":
            raise Exception(data.get("error", "Generation Error"))

        time.sleep(interval)

    raise TimeoutError("Polling timeout exceeded")
```

### 指数退避（推荐）

```python
import time
import random
import requests

def poll_with_backoff(polling_url, headers, max_attempts=30):
    """Polling with exponential backoff and jitter."""
    base_delay = 0.5  # Start with 500ms
    max_delay = 10    # Cap at 10 seconds

    for attempt in range(max_attempts):
        response = requests.get(polling_url, headers=headers)
        data = response.json()

        if data["status"] == "Ready":
            return data["result"]
        elif data["status"] == "Error":
            raise Exception(data.get("error", "Generation Error"))

        # Exponential backoff with jitter
        delay = min(base_delay * (2 ** attempt), max_delay)
        jitter = random.uniform(0, delay * 0.1)  # 10% jitter
        time.sleep(delay + jitter)

    raise TimeoutError("Max polling attempts exceeded")
```

### 自适应轮询

```python
import time
import requests

def poll_adaptive(polling_url, headers, timeout=120):
    """Adaptive polling that adjusts based on status."""
    start_time = time.time()
    delays = {
        "Pending": 2.0,      # Queue/processing
        None: 1.5            # Unknown/default
    }

    while time.time() - start_time < timeout:
        response = requests.get(polling_url, headers=headers)
        data = response.json()

        status = data.get("status")

        if status == "Ready":
            return data["result"]
        elif status == "Error":
            raise Exception(data.get("error", "Generation Error"))

        delay = delays.get(status, delays[None])
        time.sleep(delay)

    raise TimeoutError("Polling timeout exceeded")
```

## 完整示例：提交与轮询

```python
import time
import requests

class BFLClient:
    def __init__(self, api_key, base_url="https://api.bfl.ai"):
        self.base_url = base_url
        self.headers = {
            "x-key": api_key,
            "Content-Type": "application/json"
        }

    def generate(self, model, prompt, **kwargs):
        """Submit generation request and poll for result."""
        # Submit request
        endpoint = f"{self.base_url}/v1/{model}"
        payload = {"prompt": prompt, **kwargs}

        response = requests.post(endpoint, headers=self.headers, json=payload)
        response.raise_for_status()

        polling_url = response.json()["polling_url"]

        # Poll for result
        return self._poll(polling_url)

    def _poll(self, polling_url, timeout=120):
        """Poll until completion or timeout."""
        start = time.time()
        delay = 1.0

        while time.time() - start < timeout:
            response = requests.get(polling_url, headers=self.headers)
            data = response.json()

            if data["status"] == "Ready":
                return data["result"]
            elif data["status"] == "Error":
                raise Exception(data.get("error"))

            time.sleep(delay)
            delay = min(delay * 1.5, 5.0)  # Gradual backoff

        raise TimeoutError("Generation timed out")

# Usage
client = BFLClient("your-api-key")
result = client.generate(
    model="flux-2-pro",
    prompt="A beautiful sunset over mountains"
)
print(f"Image URL: {result['sample']}")
```

## URL 过期

**关键：** 结果 URL 在 10 分钟后过期。请务必立即下载。

```python
def download_result(result_url, output_path):
    """Download result image before URL expires."""
    response = requests.get(result_url)
    response.raise_for_status()

    with open(output_path, 'wb') as f:
        f.write(response.content)

    return output_path
```

## 批量处理与轮询

```python
import asyncio
import aiohttp

async def generate_batch(client, prompts, model="flux-2-pro"):
    """Generate multiple images concurrently."""
    async with aiohttp.ClientSession() as session:
        # Submit all requests
        tasks = []
        for prompt in prompts:
            task = submit_and_poll(session, client, model, prompt)
            tasks.append(task)

        # Wait for all to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

async def submit_and_poll(session, client, model, prompt):
    """Async submit and poll for single image."""
    # Submit
    async with session.post(
        f"{client.base_url}/v1/{model}",
        headers=client.headers,
        json={"prompt": prompt}
    ) as response:
        data = await response.json()
        polling_url = data["polling_url"]

    # Poll
    while True:
        async with session.get(polling_url, headers=client.headers) as response:
            data = await response.json()

            if data["status"] == "Ready":
                return data["result"]
            elif data["status"] == "Error":
                raise Exception(data.get("error"))

        await asyncio.sleep(2)
```

## 最佳实践

1. **始终实现超时** — 切勿无限轮询
2. **使用指数退避** — 降低服务器负载，应对拥塞
3. **添加抖动（jitter）** — 在轮询多个请求时避免惊群效应
4. **处理所有状态值** — 包括意外状态
5. **立即下载** — URL 在 10 分钟后过期
6. **记录轮询尝试** — 便于调试与监控
7. **遵守速率限制** — 对 429 响应实现适当的退避
