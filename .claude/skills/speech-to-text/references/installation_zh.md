# 安装

## JavaScript / TypeScript

```bash
npm install @elevenlabs/elevenlabs-js
```

> **重要：** 请始终使用 `@elevenlabs/elevenlabs-js`。旧的 `elevenlabs` npm 包（v1.x）已弃用，不应再使用。

```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";

// Option 1: Environment variable (recommended)
// Set ELEVENLABS_API_KEY in your environment
const client = new ElevenLabsClient();

// Option 2: Pass directly
const client = new ElevenLabsClient({ apiKey: "your-api-key" });
```

### 从已弃用包迁移

若已安装旧包，请先移除：

```bash
# Remove deprecated packages
npm uninstall elevenlabs

# Install the current packages
npm install @elevenlabs/elevenlabs-js

# For client-side/browser usage, also install:
npm install @elevenlabs/client  # Browser client
npm install @elevenlabs/react   # React hooks
```

**导入变更：**
```javascript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { Scribe } from "@elevenlabs/client";
import { useScribe } from "@elevenlabs/react";
```

## Python

```bash
pip install elevenlabs
```

```python
from elevenlabs import ElevenLabs

# Option 1: Environment variable (recommended)
# Set ELEVENLABS_API_KEY in your environment
client = ElevenLabs()

# Option 2: Pass directly
client = ElevenLabs(api_key="your-api-key")
```

## cURL / REST API

将 API 密钥设置为环境变量：

```bash
export ELEVENLABS_API_KEY="your-api-key"
```

在请求中通过 `xi-api-key` 请求头传入：

```bash
curl -X POST "https://api.elevenlabs.io/v1/speech-to-text" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "file=@audio.mp3" \
  -F "model_id=scribe_v2"
```

## 获取 API 密钥

1. 在 [elevenlabs.io](https://elevenlabs.io) 注册账号
2. 前往 [API Keys](https://elevenlabs.io/app/settings/api-keys)
3. 点击 **Create API Key**
4. 复制并妥善保存

也可使用 `setup-api-key` 技能进行引导式配置。

## 环境变量

| 变量 | 说明 |
|----------|-------------|
| `ELEVENLABS_API_KEY` | 你的 ElevenLabs API 密钥（必填） |
