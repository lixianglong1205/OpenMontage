---
title: 长列表的 CSS content-visibility
impact: HIGH
impactDescription: 更快的初始渲染
tags: rendering, css, content-visibility, long-lists
---

## 长列表的 CSS content-visibility

对列表项应用 `content-visibility: auto`，以推迟屏幕外内容的渲染。

**CSS：**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

**示例：**

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map(msg => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  )
}
```

对于 1000 条消息，浏览器会跳过约 990 个屏幕外条目的布局/绘制（初始渲染约快 10 倍）。
