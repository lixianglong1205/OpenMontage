# 外呼电话

通过 Twilio 集成，使用 ElevenLabs 智能体发起外呼电话。

## 前提条件

1. 已配置 ElevenLabs 智能体
2. 已与智能体关联的 Twilio 电话号码（从 ElevenLabs 控制台获取 `agent_phone_number_id`）
3. ElevenLabs API 密钥

## 基本用法

基本 Python、JavaScript 与 cURL 示例见[主 agents 技能文档](../SKILL.md#outbound-calls)。

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|-----------|------|----------|-------------|
| `agent_id` | string | 是 | ElevenLabs 智能体 ID |
| `agent_phone_number_id` | string | 是 | 与智能体关联的 Twilio 电话号码 ID |
| `to_number` | string | 是 | 目标电话号码（E.164 格式） |
| `conversation_initiation_client_data` | object | 否 | 覆盖本次通话的会话设置 |
| `call_recording_enabled` | boolean | 否 | 是否由 Twilio 录制通话 |
| `telephony_call_config` | object | 否 | 电话呼叫设置（如振铃超时） |

## 响应

```json
{
  "success": true,
  "message": "Call initiated successfully",
  "conversation_id": "conv_abc123",
  "callSid": "CA1234567890abcdef"
}
```

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `success` | boolean | 是否成功发起呼叫 |
| `message` | string | 状态消息 |
| `conversation_id` | string | 用于跟踪的 ElevenLabs 会话 ID |
| `callSid` | string | 供参考的 Twilio Call SID |

## 自定义通话

使用 `conversation_initiation_client_data` 为单次通话覆盖智能体设置：

### Python

```python
response = client.conversational_ai.twilio.outbound_call(
    agent_id="your-agent-id",
    agent_phone_number_id="your-phone-number-id",
    to_number="+1234567890",
    call_recording_enabled=True,
    conversation_initiation_client_data={
        "conversation_config_override": {
            "agent": {
                "first_message": "Hello! This is a reminder about your appointment tomorrow.",
                "language": "en"
            },
            "tts": {
                "voice_id": "JBFqnCBsd6RMkjVDRZzb"
            }
        },
        "dynamic_variables": {
            "customer_name": "John",
            "appointment_time": "2:00 PM"
        }
    }
)
```

### JavaScript

```javascript
const response = await client.conversationalAi.twilio.outboundCall({
  agentId: "your-agent-id",
  agentPhoneNumberId: "your-phone-number-id",
  toNumber: "+1234567890",
  callRecordingEnabled: true,
  conversationInitiationClientData: {
    conversationConfigOverride: {
      agent: {
        firstMessage: "Hello! This is a reminder about your appointment tomorrow.",
        language: "en",
      },
      tts: {
        voiceId: "JBFqnCBsd6RMkjVDRZzb",
      },
    },
    dynamicVariables: {
      customer_name: "John",
      appointment_time: "2:00 PM",
    },
  },
});
```

## 配置覆盖

### 智能体设置

| 选项 | 类型 | 说明 |
|--------|------|-------------|
| `first_message` | string | 本次通话的自定义问候语 |
| `language` | string | 语言代码（例如 `"en"`、`"es"`、`"fr"`） |
| `prompt` | object | 覆盖智能体提示词与 LLM 设置 |

### TTS 设置

| 选项 | 类型 | 说明 |
|--------|------|-------------|
| `voice_id` | string | 本次通话使用的语音 ID |
| `stability` | number | 语音稳定性（0.0–1.0） |
| `similarity_boost` | number | 语音相似度增强（0.0–1.0） |
| `speed` | number | 语速倍数 |

### 电话呼叫配置

| 选项 | 类型 | 说明 |
|--------|------|-------------|
| `ringing_timeout_secs` | integer | 振铃多久后放弃（默认：`60`） |

### 动态变量

通过 `dynamic_variables` 向智能体提示词传入自定义数据。在智能体提示词中使用 `{{variable_name}}` 语法引用。

分配动态变量时，可使用 `sanitize` 选项：在将工具响应发送给 LLM 与转录文本之前移除敏感值，同时仍完成变量赋值：

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `sanitize` | boolean | `false` | 若为 true，赋值值在发送给 LLM/转录前会从工具响应中移除，但仍会用于变量赋值 |

## 完整示例

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

# Make personalized outbound calls
customers = [
    {"name": "Alice", "phone": "+1234567890", "balance": "$150.00"},
    {"name": "Bob", "phone": "+0987654321", "balance": "$75.50"},
]

for customer in customers:
    try:
        response = client.conversational_ai.twilio.outbound_call(
            agent_id="payment-reminder-agent",
            agent_phone_number_id="your-phone-number-id",
            to_number=customer["phone"],
            call_recording_enabled=True,
            conversation_initiation_client_data={
                "conversation_config_override": {
                    "agent": {
                        "first_message": f"Hello {customer['name']}, this is a friendly reminder about your account."
                    }
                },
                "dynamic_variables": {
                    "customer_name": customer["name"],
                    "balance": customer["balance"]
                }
            }
        )
        print(f"Called {customer['name']}: {response.conversation_id}")
    except Exception as e:
        print(f"Failed to call {customer['name']}: {e}")
```
