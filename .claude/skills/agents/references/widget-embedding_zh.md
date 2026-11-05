# Widget 嵌入

使用 ElevenLabs 对话 widget，将语音 AI Agent 添加到任意网站。

## 基础嵌入

```html
<elevenlabs-convai agent-id="your-agent-id"></elevenlabs-convai>
<script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
```

这会创建一个浮动按钮，用户点击即可开始语音对话。

> **注意：** 目前 widget 需要公开 Agent 且关闭身份验证。若需带认证的流程，请使用 SDK。

## Widget 属性

### 必填

| Attribute | Description |
|-----------|-------------|
| `agent-id` | 你的 ElevenLabs Agent ID |
| `signed-url` | 使用签名 URL 时，作为 `agent-id` 的替代项 |

### 外观

| Attribute | Description | Default |
|-----------|-------------|---------|
| `avatar-image-url` | Agent 头像图片 URL | ElevenLabs logo |
| `avatar-orb-color-1` | 光球渐变主色 | `#2792dc` |
| `avatar-orb-color-2` | 光球渐变次色 | `#9ce6e6` |

### 文本标签

| Attribute | Description | Default |
|-----------|-------------|---------|
| `action-text` | 悬停时的提示文字 | "Talk to AI" |
| `start-call-text` | 开始通话按钮 | "Start call" |
| `end-call-text` | 结束通话按钮 | "End call" |
| `expand-text` | 展开聊天按钮 | "Open" |
| `collapse-text` | 收起聊天按钮 | "Close" |
| `listening-text` | 聆听状态标签 | "Listening..." |
| `speaking-text` | 说话状态标签 | "Assistant speaking" |

### 行为

| Attribute | Description | Default |
|-----------|-------------|---------|
| `variant` | Widget 样式：`compact` 或 `expanded` | `compact` |
| `server-location` | 服务器区域（`us`、`eu-residency`、`in-residency`、`global`） | `us` |
| `dismissible` | 是否允许用户最小化 widget | `false` |
| `disable-banner` | 是否隐藏「Powered by ElevenLabs」 | `false` |

## 示例

### 自定义头像

```html
<elevenlabs-convai
  agent-id="your-agent-id"
  avatar-image-url="https://example.com/your-avatar.png"
></elevenlabs-convai>
```

### 自定义颜色

```html
<elevenlabs-convai
  agent-id="your-agent-id"
  avatar-orb-color-1="#ff6b6b"
  avatar-orb-color-2="#ffd93d"
></elevenlabs-convai>
```

### 自定义文案

```html
<elevenlabs-convai
  agent-id="your-agent-id"
  action-text="Chat with our AI assistant"
  start-call-text="Begin conversation"
  end-call-text="Hang up"
></elevenlabs-convai>
```

### expanded 变体

```html
<elevenlabs-convai
  agent-id="your-agent-id"
  variant="expanded"
></elevenlabs-convai>
```

### 完整自定义

```html
<elevenlabs-convai
  agent-id="your-agent-id"
  avatar-image-url="https://example.com/support-agent.png"
  avatar-orb-color-1="#4f46e5"
  avatar-orb-color-2="#818cf8"
  action-text="Talk to Support"
  start-call-text="Start voice chat"
  end-call-text="End conversation"
  expand-text="Open assistant"
  collapse-text="Minimize"
></elevenlabs-convai>
```

## CSS 自定义

Widget 使用 Shadow DOM，但暴露 CSS 自定义属性：

```css
elevenlabs-convai {
  --elevenlabs-convai-widget-width: 400px;
  --elevenlabs-convai-widget-height: 600px;
}
```

### 定位

默认 widget 出现在右下角。可用 CSS 覆盖：

```css
elevenlabs-convai {
  position: fixed;
  bottom: 20px;
  right: 20px;
  /* Or position differently */
  left: 20px;
  right: auto;
}
```

### Z-Index

```css
elevenlabs-convai {
  z-index: 9999;
}
```

## JavaScript 控制

获取 widget 元素以编程方式控制：

```html
<elevenlabs-convai id="my-widget" agent-id="your-agent-id"></elevenlabs-convai>

<script>
  const widget = document.getElementById("my-widget");

  // Start a conversation
  widget.startConversation();

  // End the conversation
  widget.endConversation();

  // Listen for events
  widget.addEventListener("conversationStarted", () => {
    console.log("Conversation started");
  });

  widget.addEventListener("conversationEnded", () => {
    console.log("Conversation ended");
  });
</script>
```

### 自定义触发按钮

隐藏默认 widget，使用自己的按钮：

```html
<style>
  elevenlabs-convai {
    display: none;
  }
</style>

<button onclick="document.getElementById('widget').startConversation()">
  Talk to AI
</button>

<elevenlabs-convai id="widget" agent-id="your-agent-id"></elevenlabs-convai>
```

## 身份验证

对已启用身份验证的 Agent，传入签名 URL：

```html
<elevenlabs-convai id="widget" agent-id="your-agent-id"></elevenlabs-convai>

<script>
  async function startAuthenticatedConversation() {
    // Get signed URL from your backend
    const response = await fetch("/api/get-signed-url");
    const { signedUrl } = await response.json();

    const widget = document.getElementById("widget");
    widget.setAttribute("signed-url", signedUrl);
    widget.startConversation();
  }
</script>
```

后端示例：

```python
@app.get("/api/get-signed-url")
def get_signed_url():
    signed_url = client.conversational_ai.conversations.get_signed_url(
        agent_id="your-agent-id"
    )
    return {"signedUrl": signed_url.signed_url}
```

## 移动端注意事项

### 响应式定位

```css
/* Desktop: bottom-right */
elevenlabs-convai {
  position: fixed;
  bottom: 20px;
  right: 20px;
}

/* Mobile: full-width bottom */
@media (max-width: 768px) {
  elevenlabs-convai {
    bottom: 0;
    right: 0;
    left: 0;
    --elevenlabs-convai-widget-width: 100%;
  }
}
```

### 触控友好

Widget 默认已针对触控优化。若要更好的移动端体验：

```css
@media (max-width: 768px) {
  elevenlabs-convai {
    /* Larger touch target */
    transform: scale(1.1);
    transform-origin: bottom right;
  }
}
```

## 多个 Widget

可为不同 Agent 放置多个 widget：

```html
<elevenlabs-convai
  agent-id="support-agent-id"
  action-text="Support"
  style="right: 20px"
></elevenlabs-convai>

<elevenlabs-convai
  agent-id="sales-agent-id"
  action-text="Sales"
  style="right: 100px"
></elevenlabs-convai>
```

## 框架集成

### React

```jsx
function App() {
  useEffect(() => {
    // Load widget script
    const script = document.createElement("script");
    script.src = "https://unpkg.com/@elevenlabs/convai-widget-embed";
    script.async = true;
    document.body.appendChild(script);

    return () => document.body.removeChild(script);
  }, []);

  return (
    <div>
      <elevenlabs-convai agent-id="your-agent-id"></elevenlabs-convai>
    </div>
  );
}
```

### Vue

```vue
<template>
  <div>
    <elevenlabs-convai agent-id="your-agent-id"></elevenlabs-convai>
  </div>
</template>

<script setup>
import { onMounted } from "vue";

onMounted(() => {
  const script = document.createElement("script");
  script.src = "https://unpkg.com/@elevenlabs/convai-widget-embed";
  script.async = true;
  document.body.appendChild(script);
});
</script>
```

### Next.js

```jsx
import Script from "next/script";

export default function Page() {
  return (
    <>
      <Script
        src="https://unpkg.com/@elevenlabs/convai-widget-embed"
        strategy="lazyOnload"
      />
      <elevenlabs-convai agent-id="your-agent-id"></elevenlabs-convai>
    </>
  );
}
```

## 故障排查

### Widget 不显示

1. 检查 Agent ID 是否正确
2. 确认脚本已加载（查看 Network 面板）
3. 检查控制台是否有 JavaScript 错误
4. 确认没有 CSS 将 widget 隐藏

### 音频问题

1. 确保使用 HTTPS（麦克风需要安全上下文）
2. 检查浏览器麦克风权限
3. 在支持的浏览器中测试（Chrome、Firefox、Safari、Edge）

### CORS 错误

若使用身份验证，请确保你的域名在 Agent 允许列表中：

```python
platform_settings={
    "auth": {
        "enable_auth": True,
        "allowlist": ["https://yourdomain.com"]
    }
}
```
