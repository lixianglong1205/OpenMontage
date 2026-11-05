---
name: captions
description: HeyGen 视频的自动生成字幕与字幕选项
---

# 视频字幕

HeyGen 可为视频自动生成字幕（subtitles），提升可访问性与观看参与度。

## 启用字幕

生成视频时可启用字幕：

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
        input_text: "Hello! This video will have automatic captions.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
  // Caption settings (availability varies by plan)
  caption: true,
};
```

## 字幕配置选项

```typescript
interface CaptionConfig {
  // Enable/disable captions
  enabled: boolean;

  // Caption style
  style?: {
    font_family?: string;
    font_size?: number;
    font_color?: string;
    background_color?: string;
    position?: "top" | "bottom";
  };

  // Language for caption generation
  language?: string;
}
```

## 字幕样式

### 基础字幕

```typescript
const config = {
  video_inputs: [...],
  caption: true, // Enable with default styling
};
```

### 自定义样式字幕

```typescript
const config = {
  video_inputs: [...],
  caption: {
    enabled: true,
    style: {
      font_family: "Arial",
      font_size: 32,
      font_color: "#FFFFFF",
      background_color: "rgba(0, 0, 0, 0.7)",
      position: "bottom",
    },
  },
};
```

## 多语言字幕

针对不同语言的视频，字幕会根据语音语言生成：

```typescript
// Spanish video with Spanish captions
const spanishConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "¡Hola! Este video tendrá subtítulos en español.",
        voice_id: "spanish_voice_id",
      },
    },
  ],
  caption: true,
};
```

## 使用 SRT 文件

### SRT 文件格式

标准 SRT 格式：

```srt
1
00:00:00,000 --> 00:00:03,000
Hello! This video will have

2
00:00:03,000 --> 00:00:06,000
automatic captions generated.

3
00:00:06,000 --> 00:00:09,000
They sync with the audio.
```

### 使用自定义 SRT

进行视频翻译时，可提供自有 SRT：

```typescript
const translationConfig = {
  input_video_id: "original_video_id",
  output_languages: ["es-ES", "fr-FR"],
  srt_key: "path/to/custom.srt", // Custom SRT file
  srt_role: "input", // "input" or "output"
};
```

## 字幕位置

### 底部（默认）

大多数视频的标准位置：

```typescript
caption: {
  enabled: true,
  style: {
    position: "bottom"
  }
}
```

### 顶部

当底部区域已被占用时使用：

```typescript
caption: {
  enabled: true,
  style: {
    position: "top"
  }
}
```

## 无障碍最佳实践

1. **始终启用字幕** — 便于听障或弱听观众观看
2. **使用高对比度** — 深色背景上的白字，或相反配色
3. **可读字号** — 标准视频至少 24px，移动端宜更大
4. **勿遮挡重要画面** — 将字幕放在远离关键视觉元素的位置
5. **同步时间轴** — 确保字幕与音频时间准确对齐

## 字幕辅助函数

```typescript
interface CaptionStyle {
  font_family: string;
  font_size: number;
  font_color: string;
  background_color: string;
  position: "top" | "bottom";
}

const captionPresets: Record<string, CaptionStyle> = {
  default: {
    font_family: "Arial",
    font_size: 32,
    font_color: "#FFFFFF",
    background_color: "rgba(0, 0, 0, 0.7)",
    position: "bottom",
  },
  minimal: {
    font_family: "Arial",
    font_size: 28,
    font_color: "#FFFFFF",
    background_color: "transparent",
    position: "bottom",
  },
  bold: {
    font_family: "Arial",
    font_size: 36,
    font_color: "#FFFFFF",
    background_color: "rgba(0, 0, 0, 0.9)",
    position: "bottom",
  },
  branded: {
    font_family: "Roboto",
    font_size: 30,
    font_color: "#00D1FF",
    background_color: "rgba(26, 26, 46, 0.9)",
    position: "bottom",
  },
};

function createCaptionConfig(preset: keyof typeof captionPresets) {
  return {
    enabled: true,
    style: captionPresets[preset],
  };
}
```

## 社交媒体字幕注意事项

### TikTok / Instagram Reels

- 将字幕放在画面中部或偏上区域
- 避开底部 20%（常被界面元素遮挡）
- 移动端观看宜使用更大字号

```typescript
const socialCaptions = {
  enabled: true,
  style: {
    font_size: 42,
    position: "top", // Avoid bottom UI elements
  },
};
```

### YouTube

- 标准底部字幕效果良好
- YouTube 也支持上传隐藏式字幕（closed captions）

### LinkedIn

- 强烈建议使用字幕（许多用户静音观看）
- 宜采用偏专业的样式

## 限制

- 字幕样式可能因订阅套餐而异
- 部分高级字幕功能可能需在 Web 界面中使用
- 多说话人字幕检测的可用性可能有限
- 字幕准确度取决于音频质量与语音清晰度

## 与视频翻译的集成

使用视频翻译时，字幕会自动处理：

```typescript
// Video translation includes caption generation
const translationConfig = {
  input_video_id: "original_video_id",
  output_languages: ["es-ES"],
  // Captions generated in target language
};
```

更多视频翻译细节请参阅 **video-translate** 技能。
