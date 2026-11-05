# 安装

## CLI（推荐）

ElevenLabs CLI 是创建和管理智能体的推荐方式：

```bash
npm install -g @elevenlabs/cli
# or
pnpm add -g @elevenlabs/cli
# or
yarn global add @elevenlabs/cli
```

需要 Node.js 16.0.0 或更高版本。

### 身份验证

```bash
elevenlabs auth login          # Authenticate with API key
elevenlabs auth whoami         # Verify current login status
elevenlabs auth logout         # Remove stored credentials
```

API 密钥安全存储在 `~/.agents/api_keys.json`。

### 快速开始

```bash
# Initialize a new project
elevenlabs agents init

# Create an agent from template
elevenlabs agents add "My Assistant" --template complete

# Push to ElevenLabs platform
elevenlabs agents push
```

## JavaScript / TypeScript SDK

用于编程访问和客户端集成：

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
import { Conversation } from "@elevenlabs/client";
import { useConversation } from "@elevenlabs/react";
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

在请求中通过 `xi-api-key` 请求头携带：

```bash
curl -X POST "https://api.elevenlabs.io/v1/convai/agents/create" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Agent", "conversation_config": {"agent": {"prompt": {"prompt": "You are helpful.", "llm": "gemini-2.0-flash"}}, "tts": {"voice_id": "JBFqnCBsd6RMkjVDRZzb"}}}'
```

## 获取 API 密钥

1. 在 [elevenlabs.io](https://elevenlabs.io) 注册
2. 前往 [API Keys](https://elevenlabs.io/app/settings/api-keys)
3. 点击 **Create API Key**
4. 复制并妥善保存

或使用 `setup-api-key` 技能进行引导式配置。

## 环境变量

| 变量 | 说明 |
|----------|-------------|
| `ELEVENLABS_API_KEY` | 你的 ElevenLabs API 密钥（必填） |
