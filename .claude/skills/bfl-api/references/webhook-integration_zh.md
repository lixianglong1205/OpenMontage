---
name: webhook-integration
description: 为生产环境 BFL API 集成配置 Webhook
---

# Webhook 集成

在生产工作负载中，应使用 Webhook 而非轮询（polling）来接收生成结果。

## 相对轮询的优势

- **减少 API 调用** - 无需重复发起轮询请求
- **即时通知** - 生成完成时立即获知
- **更高资源效率** - 避免轮询造成的无效计算
- **可扩展架构** - 事件驱动设计

## 设置

### 带 Webhook 的请求

在请求中包含 `webhook_url`，并可选择包含 `webhook_secret`：

```bash
curl -X POST "https://api.bfl.ai/v1/flux-2-pro" \
  -H "x-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "webhook_url": "https://your-server.com/api/bfl-webhook",
    "webhook_secret": "your-secret-key-here"
  }'
```

### Webhook 载荷

生成完成时，BFL 会向你的 Webhook URL 发送 POST 请求：

```json
{
  "id": "gen_abc123xyz",
  "status": "Ready",
  "result": {
    "sample": "https://bfldeliveryprod.blob.core.windows.net/results/...",
    "prompt": "...",
    "seed": 1234567890
  },
  "timestamp": "2025-01-15T10:30:00Z"
}
```

失败时：

```json
{
  "id": "gen_abc123xyz",
  "status": "Error",
  "error": "content_policy_violation",
  "message": "The prompt violated content policy",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

## 安全

### 签名校验

提供 `webhook_secret` 时，BFL 使用 HMAC-SHA256 对载荷签名：

```
X-BFL-Signature: sha256=<hex-encoded-signature>
```

### 校验实现

```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    """Verify the webhook came from BFL."""
    if not signature or not signature.startswith('sha256='):
        return False

    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    provided_signature = signature[7:]  # Remove 'sha256=' prefix

    return hmac.compare_digest(expected_signature, provided_signature)
```

### 带校验的 Flask 处理器

```python
from flask import Flask, request, jsonify
import hmac
import hashlib
import requests

app = Flask(__name__)
WEBHOOK_SECRET = "your-secret-key-here"

@app.route('/api/bfl-webhook', methods=['POST'])
def handle_webhook():
    # Verify signature
    signature = request.headers.get('X-BFL-Signature')
    if not verify_webhook_signature(request.data, signature, WEBHOOK_SECRET):
        return jsonify({'error': 'Invalid signature'}), 401

    data = request.json

    if data['status'] == 'Ready':
        handle_completion(data)
    elif data['status'] == 'Error':
        handle_failure(data)

    return jsonify({'status': 'received'}), 200

def handle_completion(data):
    generation_id = data['id']
    result_url = data['result']['sample']

    # Download image immediately (URL expires in 10 min)
    image_data = requests.get(result_url).content

    # Store to your storage
    store_image(generation_id, image_data)

    # Update your database
    update_generation_status(generation_id, 'completed')

    # Notify your application/users
    notify_completion(generation_id)

def handle_failure(data):
    generation_id = data['id']
    error = data.get('error', 'unknown')

    # Log the failure
    log_generation_failure(generation_id, error)

    # Update your database
    update_generation_status(generation_id, 'failed', error)

    # Maybe retry or notify
    handle_generation_error(generation_id, error)
```

### Express.js 处理器

```javascript
const express = require('express');
const crypto = require('crypto');
const axios = require('axios');

const app = express();
app.use(express.raw({ type: 'application/json' }));

const WEBHOOK_SECRET = 'your-secret-key-here';

function verifySignature(payload, signature, secret) {
  if (!signature || !signature.startsWith('sha256=')) {
    return false;
  }

  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');

  const providedSignature = signature.slice(7);

  return crypto.timingSafeEqual(
    Buffer.from(expectedSignature),
    Buffer.from(providedSignature)
  );
}

app.post('/api/bfl-webhook', async (req, res) => {
  const signature = req.headers['x-bfl-signature'];

  if (!verifySignature(req.body, signature, WEBHOOK_SECRET)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  const data = JSON.parse(req.body);

  if (data.status === 'Ready') {
    // Download image (URL expires in 10 min)
    const imageResponse = await axios.get(data.result.sample, {
      responseType: 'arraybuffer'
    });

    // Store the image
    await storeImage(data.id, imageResponse.data);
  }

  res.json({ status: 'received' });
});
```

## 要求

### 必须使用 HTTPS

生产环境中 Webhook URL **必须使用 HTTPS**。BFL 不会向 HTTP 端点发送 Webhook。

### 响应要求

- 返回 2xx 状态码以确认已收到
- 在 30 秒内响应
- 保持处理器轻量——将耗时处理放到异步任务

### 重试策略

BFL 会对失败的 Webhook 投递进行重试：

| 尝试 | 延迟 |
|---------|-------|
| 第 1 次重试 | 1 秒 |
| 第 2 次重试 | 5 秒 |
| 第 3 次重试 | 30 秒 |

3 次失败后放弃该 Webhook。若业务关键，请回退到轮询。

## 幂等性

处理重复的 Webhook 投递：

```python
from functools import lru_cache
import redis

redis_client = redis.Redis()

def is_duplicate_webhook(generation_id):
    """Check if we've already processed this webhook."""
    key = f"webhook:processed:{generation_id}"

    # Try to set with NX (only if not exists)
    was_set = redis_client.set(key, "1", nx=True, ex=3600)  # 1 hour TTL

    return not was_set  # If we couldn't set it, it's a duplicate

@app.route('/api/bfl-webhook', methods=['POST'])
def handle_webhook():
    # ... signature verification ...

    data = request.json
    generation_id = data['id']

    if is_duplicate_webhook(generation_id):
        return jsonify({'status': 'already_processed'}), 200

    # Process webhook...
```

## 混合方案

将 Webhook 与轮询回退结合：

```python
class HybridClient:
    def __init__(self, api_key, webhook_url, webhook_secret):
        self.api_key = api_key
        self.webhook_url = webhook_url
        self.webhook_secret = webhook_secret
        self.pending = {}  # Track pending generations

    def generate(self, prompt, timeout=300):
        """Generate with webhook, fall back to polling."""
        response = self._submit(prompt)
        generation_id = response['id']
        polling_url = response['polling_url']

        # Wait for webhook (with timeout)
        result = self._wait_for_webhook(generation_id, timeout=timeout)

        if result is None:
            # Webhook didn't arrive, fall back to polling
            result = self._poll(polling_url, timeout=60)

        return result

    def _submit(self, prompt):
        return requests.post(
            "https://api.bfl.ai/v1/flux-2-pro",
            headers={"x-key": self.api_key},
            json={
                "prompt": prompt,
                "webhook_url": self.webhook_url,
                "webhook_secret": self.webhook_secret
            }
        ).json()

    def receive_webhook(self, data):
        """Called by webhook handler."""
        generation_id = data['id']
        if generation_id in self.pending:
            self.pending[generation_id].set_result(data)
```

## 监控

跟踪 Webhook 健康状态：

```python
import time

class WebhookMetrics:
    def __init__(self):
        self.received = 0
        self.processed = 0
        self.failed = 0
        self.avg_latency = 0

    def record_webhook(self, generation_id, submit_time):
        self.received += 1
        latency = time.time() - submit_time
        self.avg_latency = (self.avg_latency * (self.received - 1) + latency) / self.received

    def record_success(self):
        self.processed += 1

    def record_failure(self):
        self.failed += 1

    def get_stats(self):
        return {
            "received": self.received,
            "processed": self.processed,
            "failed": self.failed,
            "success_rate": self.processed / max(self.received, 1),
            "avg_latency_seconds": self.avg_latency
        }
```
