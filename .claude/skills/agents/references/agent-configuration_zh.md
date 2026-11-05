# Agent 配置

对话式 AI Agent 的完整配置参考。

## 配置结构

```python
agent = client.conversational_ai.agents.create(
    name="My Agent",
    conversation_config={
        "agent": {
            "first_message": "Hello!",
            "language": "en",
            "prompt": {           # LLM, system prompt, tools, and knowledge base
                "prompt": "You are helpful.",
                "llm": "gemini-2.0-flash",
                "tools": [...],
                "built_in_tools": {...}
            }
        },
        "tts": {...},             # Voice and TTS model settings
        "asr": {...},             # Speech recognition settings
        "turn": {...},            # Turn-taking behavior
        "conversation": {...},    # Duration, events, monitoring
        "vad": {...},             # Voice activity detection config
        "language_presets": {...}  # Language-specific overrides
    },
    platform_settings={...}       # Auth, call limits
)
```

## conversation_config

控制实时对话行为。

### agent

```python
conversation_config={
    "agent": {
        "first_message": "Hello! How can I help you today?",
        "language": "en",
        "disable_first_message_interruptions": False,
        "prompt": {
            "prompt": "You are a helpful assistant.",
            "llm": "gemini-2.0-flash",
            "temperature": 0.7
        }
    }
}
```

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `first_message` | string | `""` | 对话开始时 Agent 说的话 |
| `language` | string | `"en"` | ISO 639-1 语言代码（en、es、fr 等） |
| `disable_first_message_interruptions` | bool | `false` | 是否禁止用户打断首条消息 |
| `hinglish_mode` | bool | `false` | 启用且语言为 Hindi 时，Agent 以 Hinglish 回复 |
| `dynamic_variables` | object | - | 配置项，含 `dynamic_variable_placeholders` 键值对 |
| `prompt` | object | - | LLM 配置（见下文 prompt 小节） |

### tts（Text-to-Speech，文本转语音）

```python
conversation_config={
    "tts": {
        "voice_id": "JBFqnCBsd6RMkjVDRZzb",
        "model_id": "eleven_flash_v2_5",
        "stability": 0.5,
        "similarity_boost": 0.8,
        "speed": 1.0,
        "optimize_streaming_latency": 3,
        "expressive_mode": True
    }
}
```

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `voice_id` | string | `"cjVigY5qzO86Huf0OWal"` | 使用的音色 |
| `model_id` | string | - | TTS 模型（见下文） |
| `stability` | float | `0.5` | 0–1，越低越有表现力 |
| `similarity_boost` | float | `0.8` | 0–1，越高越接近原声 |
| `speed` | float | `1.0` | 0.7–1.2，语速倍数 |
| `optimize_streaming_latency` | int | - | 0–4，越高延迟越低但质量可能下降 |
| `expressive_mode` | bool | `true` | 启用富有表现力的语音生成 |
| `agent_output_audio_format` | string | - | 输出音频编解码格式 |
| `pronunciation_dictionary_locators` | array | - | 发音覆盖配置 |

**Agent 可用的 TTS 模型：**

| Model ID | 语言 | 延迟 |
|----------|-----------|---------|
| `eleven_flash_v2_5` | 32 | ~75ms（推荐） |
| `eleven_flash_v2` | English | ~75ms |
| `eleven_turbo_v2_5` | 32 | ~250–300ms |
| `eleven_turbo_v2` | English | ~250–300ms |
| `eleven_multilingual_v2` | 29 | 标准 |
| `eleven_v3_conversational` | 70+ | 标准 |

### asr（Automatic Speech Recognition，自动语音识别）

```python
conversation_config={
    "asr": {
        "quality": "high",
        "keywords": ["ElevenLabs", "TechCorp"],
        "user_input_audio_format": "pcm_16000"
    }
}
```

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `quality` | string | `"high"` | 转写质量级别 |
| `provider` | string | `"elevenlabs"` | ASR 提供商（`elevenlabs` 或 `scribe_realtime`） |
| `keywords` | array | - | 提升识别准确度的关键词 |
| `user_input_audio_format` | string | - | 输入音频格式（如 `pcm_16000`、`ulaw_8000`） |

### turn（话轮转换）

```python
conversation_config={
    "turn": {
        "turn_timeout": 7,
        "turn_eagerness": "normal",
        "silence_end_call_timeout": -1
    }
}
```

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `turn_timeout` | number | `7` | 重新唤起用户前等待的秒数 |
| `turn_eagerness` | string | `"normal"` | Agent 响应快慢：`patient`、`normal` 或 `eager` |
| `silence_end_call_timeout` | number | `-1` | 静音多少秒后结束通话（-1 表示禁用） |
| `initial_wait_time` | number | - | 等待用户开始说话的秒数 |
| `spelling_patience` | string | `"auto"` | 实体检测耐心度：`auto` 或 `off` |
| `speculative_turn` | bool | `false` | 启用推测式话轮检测 |
| `soft_timeout_config` | object | - | 用户静默时的消息配置（见下文） |

**soft_timeout_config：**

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `timeout_seconds` | number | `-1` | 软超时前的秒数（-1 表示禁用） |
| `message` | string | `"Hhmmmm...yeah."` | 超时时 Agent 说的话 |
| `use_llm_generated_message` | bool | `false` | 由 LLM 生成超时消息 |

## prompt（嵌套于 conversation_config.agent）

配置 LLM 行为。该对象位于 `conversation_config.agent.prompt`：

```python
conversation_config={
    "agent": {
        "prompt": {
            "prompt": "You are a helpful customer service agent...",
            "llm": "gemini-2.0-flash",
            "temperature": 0.7,
            "max_tokens": 500,
            "tools": [...],
            "built_in_tools": {...},
            "knowledge_base": [...]
        }
    }
}
```

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `prompt` | string | `""` | 定义 Agent 行为的系统提示词 |
| `llm` | string | - | 模型 ID（见下文 LLM 提供商） |
| `temperature` | float | `0` | 0–1，越高越有创意 |
| `max_tokens` | int | `-1` | LLM 回复的最大 token 数（-1 表示不限） |
| `reasoning_effort` | string | - | 推理深度：`none`、`minimal`、`low`、`medium`、`high`（因模型而异） |
| `thinking_budget` | int | - | 推理模型的最大思考 token 数 |
| `tools` | array | - | Webhook 与客户端工具定义 |
| `built_in_tools` | object | - | 系统工具（end_call、transfer 等） |
| `tool_ids` | array | - | 预配置工具的引用 |
| `knowledge_base` | array | - | 用于 RAG 的文档 |
| `custom_llm` | object | - | 自定义 LLM 端点配置 |
| `timezone` | string | - | IANA 时区（如 `America/New_York`） |
| `backup_llm_config` | object | - | 备用 LLM 配置 |
| `cascade_timeout_seconds` | number | `8` | 切换到备用 LLM 前的秒数（2–15） |
| `mcp_server_ids` | array | - | 要连接的 MCP 服务器 ID |
| `native_mcp_server_ids` | array | - | 原生 MCP 服务器 ID |
| `ignore_default_personality` | bool | - | 跳过默认人格指令 |

工作区环境变量可让同一 Agent 配置覆盖多个部署。在服务端工具与 MCP 服务器 URL 中使用
`{{system_env__label}}`；在工具请求头中使用 `{ "env_var_label": "orders_api_key" }`
以绑定密钥；在 `auth_connection` 中使用 `{ "env_var_label": "orders_oauth" }`
可在运行时按环境解析认证连接。

### LLM 提供商

| 提供商 | Model ID |
|----------|-----------|
| OpenAI | `gpt-5`, `gpt-5-mini`, `gpt-5-nano`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo` |
| Anthropic | `claude-sonnet-4-6`, `claude-sonnet-4-5`, `claude-sonnet-4`, `claude-haiku-4-5`, `claude-3-7-sonnet`, `claude-3-5-sonnet`, `claude-3-haiku` |
| Google | `gemini-3.1-flash-lite-preview`, `gemini-3-pro-preview`, `gemini-3-flash-preview`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`, `gemini-2.0-flash`, `gemini-2.0-flash-lite` |
| ElevenLabs | `glm-45-air-fp8`, `qwen3-30b-a3b`, `gpt-oss-120b`（托管，超低延迟） |
| Custom | `custom-llm`（需 `custom_llm` 配置） |

使用 `GET /v1/convai/llm/list` 查看当前模型目录，包括弃用状态、token/上下文上限，以及是否支持图像输入等能力标志。

### 自定义 LLM

`custom_llm` 字段嵌套在 `conversation_config.agent.prompt` 内：

```python
conversation_config={
    "agent": {
        "prompt": {
            "prompt": "You are helpful.",
            "llm": "custom-llm",
            "custom_llm": {
                "url": "https://your-llm-endpoint.com/v1/chat/completions",
                "model_id": "your-model-id",
                "api_key": {"secret_id": "your-secret-id"},
                "api_type": "chat_completions"  # or "responses"
            }
        }
    }
}
```

## platform_settings

平台级配置：安全、限额、摘要与 Widget 行为。

```python
platform_settings={
    "summary_language": "en",
    "widget": {
        "show_agent_status": True,
        "show_conversation_id": True
    },
    "auth": {
        "enable_auth": True,
        "allowlist": [{"hostname": "example.com"}]
    },
    "call_limits": {
        "agent_concurrency_limit": 10,
        "daily_limit": 100
    }
}
```

### 顶层字段

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `summary_language` | string | 对话分析输出（摘要、标题、评估理由、数据采集理由等）的语言。省略时 ElevenLabs 从对话推断。 |
| `widget` | object | 托管 Widget 与可分享页面配置。部分选项见下表。 |
| `auth` | object | Agent 访问的认证与来源限制 |
| `call_limits` | object | 并发与每日用量限制 |
| `guardrails` | object | Agent 交互的内置安全与策略控制 |
| `privacy` | object | 录音、保留与对话历史脱敏设置 |

### auth

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `enable_auth` | bool | 连接需签名 URL/令牌 |
| `allowlist` | array | CORS 允许的来源 |
| `shareable_token` | string | 公开对话令牌 |

### call_limits

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `agent_concurrency_limit` | int | 最大同时对话数（默认 -1，不限） |
| `daily_limit` | int | 每日最大对话数（默认 100000） |
| `bursting_enabled` | bool | 允许以 2 倍成本超限（默认 true） |

### guardrails

使用 `platform_settings.guardrails` 配置用户输入与 Agent 行为的内置安全控制。下列字段为 Agent 配置中最相关的当前 schema 扩展。

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `version` | string | 护栏配置版本。当前 schema 使用 `"1"`。 |
| `focus` | object | 使 Agent 紧扣主题并与配置任务一致。 |
| `prompt_injection` | object | 检测提示注入与指令覆盖尝试。 |
| `custom` | object | 用户定义的响应校验护栏。 |
| `content` | object | 按类别的内容审核护栏。 |

**focus / prompt_injection：**

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `is_enabled` | bool | 启用该护栏。 |

**content：**

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `execution_mode` | string | 执行模式：`streaming` 或 `blocking`。 |
| `config` | object | 内容审核的类别阈值设置。 |

**content.config：**

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `sexual` | object | 色情内容阈值。 |
| `violence` | object | 暴力内容阈值。 |
| `harassment` | object | 骚扰内容阈值。 |
| `self_harm` | object | 自残内容阈值。 |
| `profanity` | object | 粗俗用语阈值。 |
| `religion_or_politics` | object | 宗教或政治内容阈值。 |
| `medical_and_legal_information` | object | 医疗或法律信息阈值。 |

**content.config.\<category\>：**

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `is_enabled` | bool | 启用该类别的审核。 |
| `threshold` | number or string | 数值分数或 `low`、`medium`、`high` 之一。 |

阻塞式内容护栏与自定义护栏支持 `trigger_action`：立即结束会话，或重试响应。重试会移除被拦截的回复、将你的反馈作为系统消息注入，并在平台回退为结束会话前最多重新生成 3 次。反馈模板可使用 `{{trigger_reason}}` 与 `{{agent_message}}`。

### privacy

使用 `platform_settings.privacy` 控制录音、保留与脱敏。与脱敏相关的字段为：

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `conversation_history_redaction` | object | 从存储的转写、音频与分析中脱敏配置的实体类型。 |

**conversation_history_redaction：**

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `enabled` | bool | `false` | 是否启用对话历史脱敏 |
| `entities` | array | - | 要脱敏的实体类型。可用父类型如 `name`，或具体值如 `name.name_given`、`email_address`、`contact_number`、`dob`、`age`。 |

### widget

使用 `platform_settings.widget` 配置托管 Widget 与可分享页面默认值。客户端嵌入属性见 Widget 嵌入参考。

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `dismissible` | bool | `false` | 用户是否可关闭 Widget |
| `show_agent_status` | bool | `false` | 工具运行中是否显示 working、done 或 error 状态 |
| `show_conversation_id` | bool | `true` | 断开后是否显示对话 ID |
| `strip_audio_tags` | bool | `true` | 是否从消息中剥离音频标记 |
| `syntax_highlight_theme` | string | auto | 代码块高亮主题（`light` 或 `dark`）；省略则由 Widget 自动检测 |

### conversation（位于 conversation_config 内）

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `max_duration_seconds` | int | `600` | 最大对话时长 |
| `text_only` | bool | `false` | 纯文本模式（避免音频计费） |
| `monitoring_enabled` | bool | `false` | 启用实时 WebSocket 监控 |

## 其他顶层字段

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `tags` | array | 用于筛选的分类标签（如 `["production"]`、`["test"]`） |
| `workflow` | object | 对话流程定义与工具交互序列 |

## 知识库 / RAG

知识库在 `conversation_config.agent.prompt` 内配置：

```python
agent = client.conversational_ai.agents.create(
    name="Support Agent",
    conversation_config={
        "agent": {
            "prompt": {
                "prompt": "You are a support agent. Use the knowledge base to answer questions.",
                "llm": "gemini-2.0-flash",
                "knowledge_base": [
                    {"type": "file", "id": "doc-id", "name": "Product Guide", "usage_mode": "auto"}
                ],
                "rag": {
                    "enabled": True,
                    "embedding_model": "qwen3_embedding_4b",
                    "max_documents_length": 50000,
                    "max_retrieved_rag_chunks_count": 20
                }
            }
        },
        "tts": {"voice_id": "JBFqnCBsd6RMkjVDRZzb"}
    }
)
```

`rag.embedding_model` 支持 `e5_mistral_7b_instruct`、`multilingual_e5_large_instruct` 与 `qwen3_embedding_4b`。

## CRUD 操作

### 使用 CLI（推荐）

```bash
# Initialize project
elevenlabs agents init

# Create agent from template
elevenlabs agents add "My Agent" --template complete
elevenlabs agents add "Support Bot" --template customer-service

# List agents
elevenlabs agents list

# Check status
elevenlabs agents status

# Push local changes to platform
elevenlabs agents push
elevenlabs agents push --dry-run    # Preview changes first

# Import agents from platform
elevenlabs agents pull                      # Import all
elevenlabs agents pull --agent <agent-id>   # Import specific agent
elevenlabs agents pull --update             # Override local configs

# View available templates
elevenlabs agents templates list
elevenlabs agents templates show <template-name>

# Add tools
elevenlabs tools add-webhook "API Tool"
elevenlabs tools add-client "UI Tool"

# Generate widget code
elevenlabs agents widget <agent-id>
```

### SDK：列出 Agent

```python
agents = client.conversational_ai.agents.list()
for agent in agents.agents:
    print(f"{agent.name}: {agent.agent_id}")
```

```javascript
const agents = await client.conversationalAi.agents.list();
```

```bash
curl -X GET "https://api.elevenlabs.io/v1/convai/agents" -H "xi-api-key: $ELEVENLABS_API_KEY"
```

### SDK：获取 Agent

```python
agent = client.conversational_ai.agents.get(agent_id="your-agent-id")
```

```javascript
const agent = await client.conversationalAi.agents.get("your-agent-id");
```

```bash
curl -X GET "https://api.elevenlabs.io/v1/convai/agents/your-agent-id" -H "xi-api-key: $ELEVENLABS_API_KEY"
```

### SDK：更新 Agent

仅包含要修改的字段，其余设置保持不变。

**Python：**
```python
# Update name
client.conversational_ai.agents.update(agent_id="id", name="New Name")

# Update TTS voice
client.conversational_ai.agents.update(agent_id="id", conversation_config={
    "tts": {"voice_id": "EXAVITQu4vr4xnSDxMaL", "model_id": "eleven_flash_v2_5"}
})

# Update prompt/LLM (nested in agent)
client.conversational_ai.agents.update(agent_id="id", conversation_config={
    "agent": {"prompt": {"prompt": "New instructions.", "llm": "claude-sonnet-4", "temperature": 0.8}}
})

# Update first message
client.conversational_ai.agents.update(agent_id="id", conversation_config={
    "agent": {"first_message": "Welcome back!"}
})

# Update platform settings
client.conversational_ai.agents.update(agent_id="id", platform_settings={
    "auth": {"enable_auth": True, "allowlist": [{"hostname": "myapp.com"}]}
})
```

**JavaScript：**
```javascript
await client.conversationalAi.agents.update("id", { name: "New Name" });
await client.conversationalAi.agents.update("id", {
  conversationConfig: { tts: { voiceId: "EXAVITQu4vr4xnSDxMaL" } }
});
await client.conversationalAi.agents.update("id", {
  conversationConfig: { agent: { prompt: { prompt: "New instructions.", llm: "claude-sonnet-4" } } }
});
```

**cURL：**
```bash
curl -X PATCH "https://api.elevenlabs.io/v1/convai/agents/your-agent-id" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"name": "New Name"}'
```

#### 可更新字段

| 分区 | 字段 |
|---------|--------|
| Root | `name`, `tags` |
| `conversation_config.agent` | `first_message`, `language`, `disable_first_message_interruptions`, `dynamic_variables` |
| `conversation_config.agent.prompt` | `prompt`, `llm`, `temperature`, `max_tokens`, `reasoning_effort`, `tools`, `built_in_tools`, `knowledge_base`, `custom_llm`, `timezone` |
| `conversation_config.tts` | `voice_id`, `model_id`, `stability`, `similarity_boost`, `speed`, `optimize_streaming_latency`, `expressive_mode` |
| `conversation_config.asr` | `quality`, `provider`, `keywords`, `user_input_audio_format` |
| `conversation_config.turn` | `turn_timeout`, `turn_eagerness`, `silence_end_call_timeout`, `soft_timeout_config` |
| `conversation_config.conversation` | `max_duration_seconds`, `text_only`, `monitoring_enabled` |
| `platform_settings` | `summary_language`, `guardrails`, `privacy` |
| `platform_settings.widget` | `dismissible`, `show_agent_status`, `show_conversation_id`, `strip_audio_tags`, `syntax_highlight_theme` |
| `platform_settings.auth` | `enable_auth`, `allowlist` |
| `platform_settings.call_limits` | `agent_concurrency_limit`, `daily_limit`, `bursting_enabled` |

### SDK：删除 Agent

```python
client.conversational_ai.agents.delete(agent_id="your-agent-id")
```

```javascript
await client.conversationalAi.agents.delete("your-agent-id");
```

```bash
curl -X DELETE "https://api.elevenlabs.io/v1/convai/agents/your-agent-id" -H "xi-api-key: $ELEVENLABS_API_KEY"
```

## CI/CD 集成

在部署流水线中使用 CLI：

```bash
# Set API key as environment variable
export ELEVENLABS_API_KEY="your-api-key"

# Push changes (non-interactive)
elevenlabs agents push
```

## 配置示例

### 客户支持 Agent

```python
agent = client.conversational_ai.agents.create(
    name="Support Agent",
    conversation_config={
        "agent": {
            "first_message": "Hi! Thanks for calling TechCorp support.",
            "language": "en",
            "prompt": {
                "prompt": "You are a customer support agent. Be helpful, professional, concise.",
                "llm": "gemini-2.0-flash",
                "temperature": 0.5,
                "built_in_tools": {
                    "end_call": {},
                    "transfer_to_number": {
                        "transfers": [{"transfer_destination": {"type": "phone", "phone_number": "+1234567890"}, "condition": "User asks for human support"}]
                    }
                }
            }
        },
        "tts": {"voice_id": "XB0fDUnXU5powFXDhCwa", "model_id": "eleven_flash_v2_5"},
        "turn": {"turn_eagerness": "normal", "turn_timeout": 7},
        "conversation": {"max_duration_seconds": 900}
    }
)
```

### 低延迟助手

```python
agent = client.conversational_ai.agents.create(
    name="Quick Assistant",
    conversation_config={
        "agent": {
            "first_message": "Hey! What do you need?",
            "prompt": {
                "prompt": "Fast, efficient assistant. Brief answers.",
                "llm": "gemini-2.0-flash",
                "temperature": 0.3,
                "max_tokens": 100
            }
        },
        "tts": {"voice_id": "JBFqnCBsd6RMkjVDRZzb", "model_id": "eleven_flash_v2_5", "optimize_streaming_latency": 4},
        "turn": {"turn_eagerness": "eager", "turn_timeout": 3}
    }
)
```
