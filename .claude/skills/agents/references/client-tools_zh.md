# 客户端工具（Client Tools）

用自定义能力扩展你的智能体（agent）。工具让智能体不仅能对话，还能执行操作。

## 工具类型

| 类型 | 执行方式 | 使用场景 |
|------|-----------|----------|
| **Webhook** | 服务端通过 HTTP | 数据库查询、API 调用、需保密的安全操作 |
| **Client** | 浏览器端 JavaScript | UI 更新、本地存储、页面导航 |
| **System** | ElevenLabs 内置 | 结束通话、转接、标准动作 |

## 工具定义位置

工具定义在 `conversation_config.agent.prompt` 内。Webhook 与 client 工具放在 `tools` 数组中；系统工具放在 `built_in_tools` 中：

```python
conversation_config={
    "agent": {
        "prompt": {
            "prompt": "You are helpful.",
            "llm": "gemini-2.0-flash",
            "tools": [...],            # Webhook and client tools
            "built_in_tools": {...}     # System tools (end_call, transfer, etc.)
        }
    }
}
```

## Webhook 工具

当智能体需要外部数据或执行外部操作时，在服务端运行逻辑。

### 基础 Webhook

```python
agent = client.conversational_ai.agents.create(
    name="Weather Assistant",
    conversation_config={
        "agent": {
            "prompt": {
                "prompt": "You are a helpful assistant that can check the weather.",
                "llm": "gemini-2.0-flash",
                "tools": [{
                    "type": "webhook",
                    "name": "get_weather",
                    "description": "Get current weather for a city. Use when user asks about weather.",
                    "api_schema": {
                        "url": "https://api.example.com/weather",
                        "method": "POST",
                        "request_headers": {
                            "Authorization": "Bearer {{API_KEY}}"
                        },
                        "request_body_schema": {
                            "type": "object",
                            "properties": {
                                "city": {
                                    "type": "string",
                                    "description": "City name, e.g., 'San Francisco'"
                                },
                                "units": {
                                    "type": "string",
                                    "enum": ["celsius", "fahrenheit"],
                                    "description": "Temperature units"
                                }
                            },
                            "required": ["city"]
                        }
                    }
                }]
            }
        },
        "tts": {"voice_id": "JBFqnCBsd6RMkjVDRZzb"}
    }
)
```

### Webhook 请求格式

当智能体调用 webhook 工具时，ElevenLabs 会发送：

```json
{
  "tool_call_id": "call_abc123",
  "tool_name": "get_weather",
  "parameters": {
    "city": "San Francisco",
    "units": "fahrenheit"
  },
  "conversation_id": "conv_xyz789"
}
```

### Webhook 响应格式

你的服务端应返回：

```json
{
  "result": "The weather in San Francisco is 68°F and sunny."
}
```

或结构化数据：

```json
{
  "result": {
    "temperature": 68,
    "condition": "sunny",
    "humidity": 45
  }
}
```

### 带认证的 Webhook

```python
# Inside conversation_config.agent.prompt.tools:
{
    "type": "webhook",
    "name": "lookup_order",
    "description": "Look up order status by order ID",
    "response_timeout_secs": 10,
    "api_schema": {
        "url": "https://api.mystore.com/orders/lookup",
        "method": "POST",
        "request_headers": {
            "Authorization": "Bearer {{ORDER_API_KEY}}",
            "X-Store-ID": "store_123"
        },
        "request_body_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "Order ID (e.g., ORD-12345)"
                }
            },
            "required": ["order_id"]
        }
    }
}
```

使用工作区环境变量，让同一套服务端工具配置在预发与生产环境都能工作。`{{system_env__label}}` 可用于服务端工具 URL；密钥类环境变量可填入 `request_headers`；认证连接（auth connection）的环境变量可填入 `api_schema.auth_connection`。同样的环境变量解析模型也适用于 MCP 服务端连接。

```json
{
  "api_schema": {
    "url": "https://{{system_env__api_host}}.example.com/orders",
    "method": "GET",
    "request_headers": {
      "X-Api-Key": { "env_var_label": "orders_api_key" }
    },
    "auth_connection": { "env_var_label": "orders_oauth" }
  }
}
```

工作区认证连接支持 OAuth2 客户端凭证、OAuth2 JWT、私钥 JWT、基本认证（basic auth）、Bearer 认证以及自定义请求头认证。

系统动态变量也可用于工具参数与请求头。当 webhook 或子智能体需要完整对话上下文时，可使用 `{{system__conversation_history}}`——它会以惰性求值的 JSON 历史对象形式提供用户、智能体与工具条目。

### Webhook 工具选项

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `response_timeout_secs` | int | `20` | 超时秒数（5–120） |
| `disable_interruptions` | bool | `false` | 工具执行期间禁止用户打断 |
| `execution_mode` | string | `"immediate"` | `immediate`、`post_tool_speech` 或 `async` |
| `tool_call_sound` | string | - | 执行时的提示音：`typing`、`elevator1`–`elevator4` |
| `force_pre_tool_speech` | bool | `false` | 强制智能体在执行工具前先说话 |
| `tool_error_handling_mode` | string | `"auto"` | `auto`、`summarized`、`passthrough` 或 `hide` |

**注意：** `api_schema.method` 默认为 `GET`。对于需要发送请求体的 webhook 工具，请显式设置 `"method": "POST"`。

### 服务端实现（Node.js）

```javascript
app.post("/webhook/get_weather", async (req, res) => {
  const { parameters, conversation_id } = req.body;
  const { city, units = "fahrenheit" } = parameters;

  // Fetch weather from your data source
  const weather = await weatherService.get(city, units);

  res.json({
    result: `It's ${weather.temp}°${units === "celsius" ? "C" : "F"} and ${weather.condition} in ${city}.`,
  });
});
```

### 服务端实现（Python）

```python
@app.post("/webhook/get_weather")
async def get_weather(request: Request):
    data = await request.json()
    city = data["parameters"]["city"]
    units = data["parameters"].get("units", "fahrenheit")

    # Fetch weather from your data source
    weather = weather_service.get(city, units)

    return {
        "result": f"It's {weather['temp']}°{'C' if units == 'celsius' else 'F'} and {weather['condition']} in {city}."
    }
```

## Client 工具

在用户浏览器中执行 JavaScript。适用于 UI 更新、导航或访问浏览器 API。

### 定义 Client 工具

Client 工具在启动对话时注册：

```javascript
import { Conversation } from "@elevenlabs/client";

const conversation = await Conversation.startSession({
  agentId: "your-agent-id",
  clientTools: {
    show_product: async ({ productId }) => {
      // Update UI to show product
      const modal = document.getElementById("product-modal");
      modal.innerHTML = await fetchProductCard(productId);
      modal.showModal();
      return { success: true, message: "Showing product" };
    },

    navigate_to: async ({ page }) => {
      // Navigate to a page
      window.location.href = `/${page}`;
      return { success: true };
    },

    save_preference: async ({ key, value }) => {
      // Store in localStorage
      localStorage.setItem(key, value);
      return { saved: true };
    },
  },
});
```

### 向智能体注册 Client 工具

在 `conversation_config.agent.prompt.tools` 中告知智能体可用的 client 工具：

```python
agent = client.conversational_ai.agents.create(
    name="Shopping Assistant",
    conversation_config={
        "agent": {
            "prompt": {
                "prompt": """You are a shopping assistant.
When users want to see a product, use show_product.
When users want to go somewhere, use navigate_to.""",
                "llm": "gemini-2.0-flash",
                "tools": [
                    {
                        "type": "client",
                        "name": "show_product",
                        "description": "Display a product card to the user",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "productId": {
                                    "type": "string",
                                    "description": "Product ID to display"
                                }
                            },
                            "required": ["productId"]
                        }
                    },
                    {
                        "type": "client",
                        "name": "navigate_to",
                        "description": "Navigate user to a different page",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "page": {
                                    "type": "string",
                                    "enum": ["cart", "checkout", "account", "home"],
                                    "description": "Page to navigate to"
                                }
                            },
                            "required": ["page"]
                        }
                    }
                ]
            }
        },
        "tts": {"voice_id": "JBFqnCBsd6RMkjVDRZzb"}
    }
)
```

### Client 工具选项

| 字段 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `expects_response` | bool | `false` | 工具是否向智能体返回数据 |

### Client 工具返回值

返回智能体可在对话中使用的数据：

```javascript
clientTools: {
  check_cart: async () => {
    const cart = JSON.parse(localStorage.getItem("cart") || "[]");
    return {
      itemCount: cart.length,
      total: cart.reduce((sum, item) => sum + item.price, 0),
      items: cart.map((item) => item.name),
    };
  };
}
```

智能体会收到这些数据，例如可以说：「您的购物车里有 3 件商品，合计 $45.99。」

## 系统工具（built_in_tools）

ElevenLabs 提供的内置工具。配置在 `conversation_config.agent.prompt.built_in_tools`（不在 `tools` 数组中）：

```python
"built_in_tools": {
    "end_call": {},
    "transfer_to_number": {...},
    "transfer_to_agent": {...},
    "language_detection": {},
    "skip_turn": {},
    "voicemail_detection": {...},
    "play_keypad_touch_tone": {}
}
```

当前 API 模式还在 `built_in_tools` 中提供 `agent_prompt_change`、`memory_entry_create`、`memory_entry_delete`、`memory_entry_search` 与 `memory_entry_update`。

### end_call

结束当前对话：

```python
"built_in_tools": {
    "end_call": {}
}
```

智能体可以说「再见！」然后通过程序结束通话。

### transfer_to_number

转接到电话号码（需要电话集成）：

```python
"built_in_tools": {
    "transfer_to_number": {
        "transfers": [{
            "transfer_destination": {"type": "phone", "phone_number": "+1234567890"},
            "condition": "User asks to speak with a human agent"
        }]
    }
}
```

### transfer_to_agent

转接到另一个 ElevenLabs 智能体：

```python
"built_in_tools": {
    "transfer_to_agent": {
        "transfers": [{
            "agent_id": "other-agent-id",
            "condition": "User asks about sales"
        }]
    }
}
```

## 最佳实践

### 工具描述

编写清晰的描述，让 LLM 知道何时使用工具：

```python
# Good - specific and actionable
"description": "Look up order status. Use when customer asks about their order, delivery, or shipping."

# Bad - vague
"description": "Order tool"
```

### 参数描述

帮助 LLM 正确抽取参数值：

```python
"parameters": {
    "type": "object",
    "properties": {
        "order_id": {
            "type": "string",
            "description": "Order ID in format ORD-XXXXX (e.g., ORD-12345)"
        },
        "email": {
            "type": "string",
            "description": "Customer email address for verification"
        }
    }
}
```

### 错误处理

使用 `tool_error_handling_mode` 配置工具错误如何传递给智能体：

| 模式 | 行为 |
|------|----------|
| `auto` | ElevenLabs 自动决定如何处理错误 |
| `summarized` | 错误在发给智能体前先被摘要 |
| `passthrough` | 完整错误详情直接传给智能体 |
| `hide` | 对智能体隐藏错误 |

返回有助于排查的错误信息：

```javascript
// Server webhook
app.post("/webhook/lookup_order", async (req, res) => {
  const { order_id } = req.body.parameters;

  const order = await db.orders.find(order_id);

  if (!order) {
    return res.json({
      result: {
        error: true,
        message: `Order ${order_id} not found. Please verify the order ID.`,
      },
    });
  }

  res.json({ result: order });
});
```

### 超时

使用 `response_timeout_secs` 为 webhook 设置合理超时（5–120 秒，默认 20）：

```python
{
    "type": "webhook",
    "name": "slow_operation",
    "description": "Run a slow operation",
    "response_timeout_secs": 30,
    "api_schema": {
        "url": "https://api.example.com/slow-operation",
        "method": "POST"
    }
}
```

## 完整示例

```python
agent = client.conversational_ai.agents.create(
    name="E-commerce Assistant",
    conversation_config={
        "agent": {
            "first_message": "Hi! How can I help you today?",
            "language": "en",
            "prompt": {
                "prompt": """You are an e-commerce support assistant.

Available actions:
- lookup_order: Check order status
- show_product: Display products to customer
- end_call: End conversation politely
- transfer_to_number: Transfer to human support

Always verify order ID before lookup. Offer transfer for complex issues.""",
                "llm": "gemini-2.0-flash",
                "tools": [
                    # Webhook: Server-side order lookup
                    {
                        "type": "webhook",
                        "name": "lookup_order",
                        "description": "Look up order status by order ID or email",
                        "api_schema": {
                            "url": "https://api.mystore.com/orders/lookup",
                            "method": "POST",
                            "request_headers": {"Authorization": "Bearer {{API_KEY}}"},
                            "request_body_schema": {
                                "type": "object",
                                "properties": {
                                    "order_id": {"type": "string"},
                                    "email": {"type": "string"}
                                }
                            }
                        }
                    },
                    # Client: Browser-side product display
                    {
                        "type": "client",
                        "name": "show_product",
                        "description": "Display product details to the customer",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "product_id": {"type": "string"}
                            },
                            "required": ["product_id"]
                        }
                    }
                ],
                "built_in_tools": {
                    "end_call": {},
                    "transfer_to_number": {
                        "transfers": [{
                            "transfer_destination": {"type": "phone", "phone_number": "+1234567890"},
                            "condition": "User asks for human support"
                        }]
                    }
                }
            }
        },
        "tts": {"voice_id": "JBFqnCBsd6RMkjVDRZzb", "model_id": "eleven_flash_v2_5"}
    }
)
```
