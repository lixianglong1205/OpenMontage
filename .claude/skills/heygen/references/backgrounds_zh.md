---
name: backgrounds
description: HeyGen 视频中使用的纯色、图片与视频背景
---

# 视频背景

HeyGen 支持多种背景类型，用于自定义数字人视频的外观。

## 背景类型

| 类型 | 说明 |
|------|-------------|
| `color` | 纯色背景 |
| `image` | 静态图片背景 |
| `video` | 循环播放的视频背景 |

## 纯色背景

最简单的选项——使用单一纯色：

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Hello with a colored background!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "color",
        value: "#FFFFFF", // White background
      },
    },
  ],
};
```

### 常用颜色值

| 颜色 | 十六进制值 | 适用场景 |
|-------|-----------|----------|
| 白色 | `#FFFFFF` | 干净、专业 |
| 黑色 | `#000000` | 戏剧感、电影感 |
| 蓝色 | `#0066CC` | 企业、可信 |
| 绿色 | `#00FF00` | 色键（用于合成） |
| 灰色 | `#808080` | 中性、现代 |

### 使用透明/绿幕

用于后期合成：

```typescript
background: {
  type: "color",
  value: "#00FF00", // Green screen
}
```

## 图片背景

使用静态图片作为背景：

### 来自 URL

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Check out this custom background!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "image",
        url: "https://example.com/my-background.jpg",
      },
    },
  ],
};
```

### 来自已上传资源

先上传图片，再使用资源 URL：

```typescript
// 1. Upload the image
const assetId = await uploadFile("./background.jpg", "image/jpeg");

// 2. Use in video config
const videoConfig = {
  video_inputs: [
    {
      character: {...},
      voice: {...},
      background: {
        type: "image",
        url: `https://files.heygen.ai/asset/${assetId}`,
      },
    },
  ],
};
```

### 图片要求

- **格式**：JPEG、PNG
- **推荐尺寸**：与视频分辨率一致（例如 1080p 为 1920x1080）
- **宽高比**：应与视频宽高比一致
- **文件大小**：建议小于 10MB

## 视频背景

使用循环播放的视频作为背景：

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Dynamic video background!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "video",
        url: "https://example.com/background-loop.mp4",
      },
    },
  ],
};
```

### 视频要求

- **格式**：MP4（建议使用 H.264 编解码器）
- **循环**：若背景视频短于数字人内容，将自动循环
- **音频**：背景视频音频通常会被静音
- **文件大小**：建议小于 100MB

## 每个场景使用不同背景

为每个场景设置不同背景：

```typescript
const multiBackgroundConfig = {
  video_inputs: [
    // Scene 1: Office background
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Let me start with an introduction.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "image",
        url: "https://example.com/office-bg.jpg",
      },
    },
    // Scene 2: Product showcase
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "closeUp",
      },
      voice: {
        type: "text",
        input_text: "Now let me show you our product.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "image",
        url: "https://example.com/product-bg.jpg",
      },
    },
    // Scene 3: Call to action
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Get started today!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
      background: {
        type: "color",
        value: "#1a1a2e",
      },
    },
  ],
};
```

## 背景辅助函数

### TypeScript

```typescript
type BackgroundType = "color" | "image" | "video";

interface Background {
  type: BackgroundType;
  value?: string;
  url?: string;
}

function createColorBackground(hexColor: string): Background {
  return { type: "color", value: hexColor };
}

function createImageBackground(imageUrl: string): Background {
  return { type: "image", url: imageUrl };
}

function createVideoBackground(videoUrl: string): Background {
  return { type: "video", url: videoUrl };
}

// Preset backgrounds
const backgrounds = {
  white: createColorBackground("#FFFFFF"),
  black: createColorBackground("#000000"),
  greenScreen: createColorBackground("#00FF00"),
  corporate: createColorBackground("#0066CC"),
};
```

## 最佳实践

1. **匹配尺寸**——背景应与视频分辨率一致
2. **考虑数字人位置**——为数字人出现区域留出空间
3. **使用对比色**——确保数字人在背景上清晰可见
4. **优化文件大小**——压缩图片/视频以加快处理
5. **用绿幕测试**——适用于专业后期工作流
6. **背景保持简洁**——避免数字人身后出现干扰元素

## 常见问题

### 背景不显示

```typescript
// Wrong: missing url/value
background: {
  type: "image"
}

// Correct
background: {
  type: "image",
  url: "https://example.com/bg.jpg"
}
```

### 宽高比不匹配

若背景与视频尺寸不一致，可能被裁剪或拉伸。请始终让背景宽高比与视频尺寸匹配：

```typescript
// For 1920x1080 video
// Use 1920x1080 background image

// For 1080x1920 portrait video
// Use 1080x1920 background image
```

### 背景视频音频

背景视频的音频通常会被静音，以免与数字人语音冲突。若需要背景音乐，请在后期作为独立音轨添加。
