---
name: scripts
description: 为 HeyGen AI 数字人视频撰写有效脚本的指南
---

# 为 HeyGen 视频撰写脚本

AI 数字人视频的脚本与人类主讲人不同，有各自的要求。本指南介绍如何撰写听起来自然、渲染效果好的脚本。

## 脚本基础

### 语速与时长

正常语速（1.0x）下，典型语速约为 **每分钟 150 个词**。可据此粗略估算脚本长度。

| 脚本长度 | 大致时长 |
|---------------|---------------------|
| 75 words | 30 seconds |
| 150 words | 1 minute |
| 300 words | 2 minutes |
| 450 words | 3 minutes |
| 750 words | 5 minutes |

```typescript
// Estimate video duration from script
function estimateDuration(script: string, speed: number = 1.0): number {
  const words = script.split(/\s+/).filter(w => w.length > 0).length;
  const wordsPerMinute = 150 * speed;
  return words / wordsPerMinute * 60; // seconds
}

// Estimate frames for Remotion
function estimateFrames(script: string, fps: number = 30, speed: number = 1.0): number {
  const durationSeconds = estimateDuration(script, speed);
  return Math.ceil(durationSeconds * fps);
}
```

### 句子结构

**保持句子简短。** AI 语音对较短句子的处理更自然。

| 指南 | 示例 |
|-----------|---------|
| **推荐**：每句 10–20 个词 | "Our platform helps teams collaborate. It syncs in real-time across all devices." |
| **避免**：30 词以上的长句 | "Our platform helps teams collaborate more effectively by providing real-time synchronization across all devices while also offering offline support and automatic conflict resolution." |

### 标点影响表达

| 标点 | 效果 |
|-------------|--------|
| 句号 `.` | 完整停顿，自然暂停 |
| 逗号 `,` | 短暂停顿 |
| 问号 `?` | 升调 |
| 感叹号 `!` | 强调（慎用） |
| 省略号 `...` | 语尾拖长，略作停顿 |

## 使用 Break 标签添加停顿

使用 SSML 风格的 `<break>` 标签精确控制停顿：

```
<break time="Xs"/>
```

其中 `X` 为秒数（如 `0.5s`、`1s`、`1.5s`、`2s`）。

### 格式规则

| 规则 | 正确 | 错误 |
|------|---------|-----------|
| 标签前留空格 | `word <break time="1s"/>` | `word<break time="1s"/>` |
| 标签后留空格 | `<break time="1s"/> word` | `<break time="1s"/>word` |
| 使用带 "s" 的秒数 | `<break time="1.5s"/>` | `<break time="1500ms"/>` |
| 自闭合标签 | `<break time="1s"/>` | `<break time="1s"></break>` |

### 何时使用停顿

| 场景 | 建议停顿时长 | 示例 |
|-----------|-------------------|---------|
| 问候之后 | 0.5–1s | `Hello! <break time="0.5s"/> Welcome to...` |
| 段落之间 | 1–1.5s | `...that's feature one. <break time="1.5s"/> Now let's look at...` |
| 重点之前 | 0.5s | `The most important thing is <break time="0.5s"/> consistency.` |
| 戏剧效果 | 1.5–2s | `And the winner is... <break time="2s"/> you!` |
| 问句之后 | 1s | `Sound good? <break time="1s"/> Let's get started.` |
| 列举项之间 | 0.5s | `First, speed. <break time="0.5s"/> Second, reliability.` |

### 停顿时长参考

| 时长 | 感受 | 适用 |
|----------|------|---------|
| 0.3–0.5s | 短促换气 | 分句之间、轻度强调 |
| 0.5–1s | 自然停顿 | 句间、过渡 |
| 1–1.5s | 有意停顿 | 换段、引出要点 |
| 1.5–2s | 戏剧性 | 揭晓、重要公告 |
| 2s+ | 长停顿 | 慎用，可能显得不自然 |

### 示例

```typescript
// Section transitions
const script = `
Welcome to our product overview. <break time="1s"/>

Today I'll cover three key features. <break time="0.5s"/>
First, let's look at the dashboard. <break time="1.5s"/>

As you can see, it's designed for simplicity. <break time="0.5s"/>
Every action is just one click away.
`;

// Building suspense
const announcement = `
We've been working on something special. <break time="1s"/>
After months of development... <break time="1.5s"/>
I'm excited to announce <break time="0.5s"/> our new AI assistant.
`;

// List with rhythm
const features = `
Our platform offers three core benefits. <break time="0.5s"/>
Speed. <break time="0.5s"/>
Reliability. <break time="0.5s"/>
And simplicity. <break time="1s"/>
Let me show you each one.
`;
```

### 连续 Break

多个连续的 break 会合并：

```typescript
// These two breaks:
"Hello <break time=\"1s\"/> <break time=\"0.5s\"/> world"

// Are treated as a single 1.5s pause
```

## 脚本结构模板

### 产品演示（60 秒，约 150 词）

```typescript
const productDemo = `
Hi, I'm [Name], and I'm excited to show you [Product]. <break time="1s"/>

[Product] helps you [main benefit] in just [timeframe]. <break time="0.5s"/>

Here's how it works. <break time="1s"/>

First, [step 1]. <break time="0.5s"/>
Then, [step 2]. <break time="0.5s"/>
And finally, [step 3]. <break time="1s"/>

What used to take [old time] now takes [new time]. <break time="0.5s"/>

Ready to get started? <break time="0.5s"/>
Visit [website] today.
`;
```

### 教程开场（90 秒，约 225 词）

```typescript
const tutorial = `
Welcome to this tutorial on [topic]. <break time="0.5s"/>
I'm [Name], and I'll guide you through everything you need to know. <break time="1s"/>

By the end of this video, you'll be able to [outcome 1], [outcome 2], and [outcome 3]. <break time="1s"/>

Let's start with the basics. <break time="1.5s"/>

[Section 1 content - 2-3 sentences] <break time="1s"/>

Now that you understand [concept], let's move on to [next topic]. <break time="1.5s"/>

[Section 2 content - 2-3 sentences] <break time="1s"/>

And finally, let's cover [last topic]. <break time="1.5s"/>

[Section 3 content - 2-3 sentences] <break time="1s"/>

That's everything you need to get started. <break time="0.5s"/>
If you have questions, leave a comment below. <break time="0.5s"/>
Thanks for watching!
`;
```

### 公告（30 秒，约 75 词）

```typescript
const announcement = `
Big news! <break time="0.5s"/>

We're thrilled to announce [announcement]. <break time="1s"/>

This means [benefit 1] and [benefit 2] for all our users. <break time="0.5s"/>

Starting [date], you'll be able to [new capability]. <break time="1s"/>

Head to [location] to learn more. <break time="0.5s"/>
We can't wait to hear what you think!
`;
```

## AI 语音撰写技巧

### 建议

- **口语化写作** — 大声朗读以检查流畅度
- **使用缩略形式** — 用 "We're" 而非 "We are"，用 "It's" 而非 "It is"
- **拆分长句** — 在自然停顿处断开
- **缩写展开拼读** — "API" 可能被读成 "a pee eye"
- **用停顿强调** — 引导听众注意力
- **段落收尾清晰** — 不要话说到一半戛然而止

### 避免

- **无上下文的行话** — 解释技术术语
- **过长插入语** — 改为独立句子
- **易歧义发音** — "read"（现在时）与 "read"（过去时）
- **过多感叹号** — 整篇脚本通常一个即可
- **流水长句** — 拆成易消化的短句
- **信息过密** — 用停顿隔开事实

### 发音提示

对可能读错的词，可拼读音标或加提示：

```typescript
// Technical terms
const script1 = "Our API (A-P-I) handles authentication...";

// Ambiguous words
const script2 = "I read (red) the documentation yesterday...";

// Brand names
const script3 = "Welcome to HeyGen (hey-jen)...";
```

## 多场景脚本

将脚本拆分到多个场景（不同背景或数字人）时：

```typescript
const multiSceneVideo = {
  video_inputs: [
    {
      // Scene 1: Introduction
      character: { type: "avatar", avatar_id: "josh_lite3_20230714", avatar_style: "normal" },
      voice: {
        type: "text",
        input_text: "Welcome to our quarterly update. <break time=\"1s\"/> I'm Josh, and I'll walk you through the highlights.",
        voice_id: "voice_id_here",
      },
      background: { type: "color", value: "#1a1a2e" },
    },
    {
      // Scene 2: Main content (different background)
      character: { type: "avatar", avatar_id: "josh_lite3_20230714", avatar_style: "normal" },
      voice: {
        type: "text",
        input_text: "Let's start with revenue. <break time=\"0.5s\"/> We grew 25 percent quarter over quarter. <break time=\"1s\"/> Here's what drove that growth.",
        voice_id: "voice_id_here",
      },
      background: { type: "image", url: "https://..." },
    },
    // ... more scenes
  ],
};
```

### 场景切换技巧

- 每个场景以完整意思结束
- 新场景开头简要交代上下文
- 各场景语气保持一致
- 场景开始时用停顿，让画面被注意到

## 测试脚本

生成完整视频前：

1. **大声朗读** — 计时，检查拗口表述
2. **统计词数** — 核对预期时长
3. **检查 break 标签** — 确认间距与语法正确
4. **短片段预览** — 若担心发音，先生成约 10 秒测试

```typescript
// Test a small portion first
const testScript = script.split('.').slice(0, 2).join('.') + '.';
const testVideoId = await generateVideo({
  video_inputs: [{
    character: { type: "avatar", avatar_id: avatarId, avatar_style: "normal" },
    voice: { type: "text", input_text: testScript, voice_id: voiceId },
  }],
  dimension: { width: 1280, height: 720 }, // Lower res for test
});
```

## 语音语速调整

在语音配置中调整播报速度：

```typescript
voice: {
  type: "text",
  input_text: script,
  voice_id: "voice_id",
  speed: 1.1,  // Slightly faster (range: 0.5 - 2.0)
}
```

| 语速 | 效果 | 适用场景 |
|-------|--------|----------|
| 0.8–0.9 | 较慢、从容 | 复杂主题、年长受众 |
| 1.0 | 正常 | 通用 |
| 1.1–1.2 | 略快 | 有活力内容、年轻受众 |
| 1.3+ | 很快 | 慎用，可能降低清晰度 |

完整语音配置选项见 [voices.md](voices.md)。
