---
name: remotion-integration
description: 在 Remotion 合成中使用 HeyGen 数字人视频
---

# HeyGen + Remotion 集成

本指南介绍生成 HeyGen 数字人视频并在 Remotion 合成中使用的流程。

## 快速开始

```typescript
// 1. Get avatar with default voice
const avatar = await getAvatarDetails(avatarId);

// 2. Generate video (MP4 with background - most common)
const videoId = await generateVideo({
  video_inputs: [{
    character: { type: "avatar", avatar_id: avatar.id, avatar_style: "normal" },
    voice: { type: "text", input_text: script, voice_id: avatar.default_voice_id },
    background: { type: "color", value: "#1a1a2e" },
  }],
  dimension: { width: 1920, height: 1080 },
});

// 3. Poll for completion (10-15+ min)
// 4. Use in Remotion with motion graphics overlaid on top
```

## 概述

典型流程如下：
1. 使用 HeyGen 生成数字人视频
2. 等待完成并获取视频 URL
3. 下载或直接在 Remotion 中使用 URL
4. 与其他元素（背景、叠加层、动画）合成

## 选择合适的输出格式

| 你的合成场景 | 推荐方案 | 原因 |
|------------------|-------------|-----|
| 数字人作为主讲并叠加图层 | MP4 + 背景 | 更简单，叠加层放在上方 |
| Loom 风格（数字人叠在录屏上） | WebM + `closeUp`，在 Remotion 中遮罩 | 需要透明，在 CSS 中应用圆形遮罩 |
| 数字人叠在其他视频/内容上 | WebM（透明） | 需要看到背后的内容 |
| 全屏数字人 | MP4 + 背景 | 标准做法 |

**多数情况使用带背景的 MP4。** 当需要看到数字人*背后*的内容时使用 WebM。

**注意：** WebM 仅支持 `normal` 和 `closeUp` 风格。若要圆形取景，在 Remotion 中使用 CSS `border-radius: 50%`。

## 推荐：并行开发流程

HeyGen 视频生成需要 **10–15 分钟以上**。不要干等——并行工作：

1. **启动 HeyGen 生成** — 将 `video_id` 保存到文件后立即退出
2. **搭建 Remotion 合成** — 使用占位符或数字人的 `preview_video_url`（短循环预览）
3. **定期检查 HeyGen 状态**，或在搭建完成后检查
4. **就绪后**将占位符替换为真实视频 URL

**根据脚本估算时长**：语速约 150 词/分钟，因此 `wordCount / 150 * 60 * fps` 可得到大致帧数。

**合成提示**：设计组件时使其在有无数字人视频时都能工作，以便独立测试动态图形。

## 尺寸对齐

**关键**：使 HeyGen 输出尺寸与 Remotion 合成一致。

### 常用尺寸预设

```typescript
// Shared dimension constants for both HeyGen and Remotion
const DIMENSIONS = {
  landscape_1080p: { width: 1920, height: 1080 },
  landscape_720p: { width: 1280, height: 720 },
  portrait_1080p: { width: 1080, height: 1920 },
  portrait_720p: { width: 720, height: 1280 },
  square_1080p: { width: 1080, height: 1080 },
  square_720p: { width: 720, height: 720 },
} as const;

type DimensionPreset = keyof typeof DIMENSIONS;
```

### HeyGen 视频生成

```typescript
// Generate HeyGen video with specific dimensions
async function generateHeyGenVideo(
  script: string,
  avatarId: string,
  voiceId: string,
  preset: DimensionPreset
): Promise<string> {
  const dimension = DIMENSIONS[preset];

  const response = await fetch("https://api.heygen.com/v2/video/generate", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      video_inputs: [
        {
          character: {
            type: "avatar",
            avatar_id: avatarId,
            avatar_style: "normal",
          },
          voice: {
            type: "text",
            input_text: script,
            voice_id: voiceId,
          },
          background: {
            type: "color",
            value: "#00FF00", // Green screen for compositing
          },
        },
      ],
      dimension,
    }),
  });

  const { data } = await response.json();
  return data.video_id;
}
```

### Remotion 合成设置

```tsx
// remotion/src/Root.tsx
import { Composition } from "remotion";
import { AvatarComposition } from "./AvatarComposition";

const DIMENSIONS = {
  landscape_1080p: { width: 1920, height: 1080 },
  // ... same as above
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="AvatarVideo"
        component={AvatarComposition}
        durationInFrames={300} // Will be set dynamically
        fps={30}
        width={DIMENSIONS.landscape_1080p.width}
        height={DIMENSIONS.landscape_1080p.height}
        defaultProps={{
          avatarVideoUrl: "",
        }}
      />
    </>
  );
};
```

## 为 Remotion 生成数字人视频

### 标准：带背景的 MP4

多数 Remotion 合成最适合 MP4 + 背景。叠加层与动态图形放在上方：

```typescript
async function generateAvatarForRemotion(
  script: string,
  avatarId: string,
  voiceId: string,
  options: {
    style?: "normal" | "closeUp" | "circle";
    backgroundColor?: string;
  } = {}
): Promise<string> {
  const { style = "normal", backgroundColor = "#1a1a2e" } = options;

  const response = await fetch("https://api.heygen.com/v2/video/generate", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      video_inputs: [{
        character: {
          type: "avatar",
          avatar_id: avatarId,
          avatar_style: style,
        },
        voice: {
          type: "text",
          input_text: script,
          voice_id: voiceId,
        },
        background: {
          type: "color",
          value: backgroundColor,
        },
      }],
      dimension: { width: 1920, height: 1080 },
    }),
  });

  const { data } = await response.json();
  return data.video_id;
}
```

### 透明背景（WebM）

仅当需要看到数字人*背后*的内容时使用（例如数字人叠在录屏上）：

```typescript
// Use /v1/video.webm endpoint for transparent background
// Note: Different structure than /v2/video/generate
const response = await fetch("https://api.heygen.com/v1/video.webm", {
  method: "POST",
  headers: {
    "X-Api-Key": process.env.HEYGEN_API_KEY!,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    avatar_pose_id: avatarPoseId,  // Required: avatar pose ID
    avatar_style: "normal",        // Required: "normal" or "closeUp" only
    input_text: script,            // Required (with voice_id)
    voice_id: voiceId,             // Required (with input_text)
    dimension: { width: 1920, height: 1080 },
  }),
});
```

## 在 Remotion 中使用 HeyGen 视频

### 重要：使用 OffthreadVideo 实现逐帧精确渲染

**HeyGen 数字人视频请始终使用 `OffthreadVideo`，不要用 `Video`。** 基础 `Video` 组件使用浏览器视频解码器，无法逐帧精确，渲染时会出现抖动。`OffthreadVideo` 通过 FFmpeg 抽帧，播放更平滑、更准确。

`OffthreadVideo` 包含在核心 `remotion` 包中，无需额外安装。

### 基础用法

```tsx
// remotion/src/AvatarComposition.tsx
import { OffthreadVideo, useVideoConfig } from "remotion";

interface AvatarCompositionProps {
  avatarVideoUrl: string;
}

export const AvatarComposition: React.FC<AvatarCompositionProps> = ({
  avatarVideoUrl,
}) => {
  return (
    <div style={{ flex: 1, backgroundColor: "#1a1a2e" }}>
      <OffthreadVideo
        src={avatarVideoUrl}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "contain",
        }}
      />
    </div>
  );
};
```

### 透明背景 WebM（推荐）

使用 `/v1/video.webm` 生成的 WebM — 无需色度键：

```tsx
import { OffthreadVideo, AbsoluteFill, Sequence } from "remotion";

export const AvatarWithMotionGraphics: React.FC<{
  avatarWebmUrl: string
}> = ({ avatarWebmUrl }) => {
  return (
    <AbsoluteFill>
      {/* Layer 1: Your background/content */}
      <AbsoluteFill style={{ backgroundColor: "#1a1a2e" }}>
        <YourMotionGraphics />
      </AbsoluteFill>

      {/* Layer 2: Avatar with transparent background - use OffthreadVideo for frame-accurate rendering */}
      <OffthreadVideo
        src={avatarWebmUrl}
        transparent
        style={{
          position: "absolute",
          bottom: 0,
          right: 0,
          width: "50%",
          height: "auto",
        }}
      />

      {/* Layer 3: Overlays on top of avatar */}
      <Sequence from={30}>
        <AnimatedTitle text="Welcome!" />
      </Sequence>
    </AbsoluteFill>
  );
};
```

### Loom 风格：圆形数字人叠在录屏上

使用 `closeUp` 风格 + WebM，然后在 Remotion 中应用圆形遮罩：

```tsx
import { OffthreadVideo, AbsoluteFill } from "remotion";

export const LoomStyleComposition: React.FC<{
  screenRecordingUrl: string;
  avatarWebmUrl: string; // Generated with avatar_style: "closeUp" via /v1/video.webm
}> = ({ screenRecordingUrl, avatarWebmUrl }) => {
  return (
    <AbsoluteFill>
      {/* Screen recording fills the frame */}
      <OffthreadVideo src={screenRecordingUrl} style={{ width: "100%", height: "100%" }} />

      {/* Avatar with circular mask - transparent bg shows screen behind */}
      <OffthreadVideo
        src={avatarWebmUrl}
        transparent
        style={{
          position: "absolute",
          bottom: 40,
          left: 40,
          width: 180,
          height: 180,
          borderRadius: "50%", // Circular mask applied in CSS
          overflow: "hidden",
          objectFit: "cover",
        }}
      />
    </AbsoluteFill>
  );
};
```

**注意：** WebM 不支持 `circle` 风格 — 使用 `normal` 或 `closeUp`，并通过 CSS 做圆形遮罩。

### 旧方案：绿幕色度键

若使用绿色背景 MP4（不推荐 — 请改用 WebM）：

```tsx
// Note: True chroma key requires WebGL or post-processing
// WebM transparent background is much simpler
<OffthreadVideo
  src={avatarVideoUrl}
  style={{
    mixBlendMode: "multiply", // Basic compositing only
  }}
/>
```

### 分层合成

```tsx
import { OffthreadVideo, Sequence, useVideoConfig, Img } from "remotion";

interface LayeredAvatarProps {
  avatarVideoUrl: string;
  backgroundUrl: string;
  logoUrl: string;
  title: string;
}

export const LayeredAvatarComposition: React.FC<LayeredAvatarProps> = ({
  avatarVideoUrl,
  backgroundUrl,
  logoUrl,
  title,
}) => {
  const { fps } = useVideoConfig();

  return (
    <div style={{ position: "relative", width: "100%", height: "100%" }}>
      {/* Layer 1: Background */}
      <Img
        src={backgroundUrl}
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />

      {/* Layer 2: Avatar video - use OffthreadVideo to prevent jitter */}
      <OffthreadVideo
        src={avatarVideoUrl}
        style={{
          position: "absolute",
          bottom: 0,
          right: 0,
          width: "40%",
          height: "auto",
        }}
      />

      {/* Layer 3: Title (appears after 1 second) */}
      <Sequence from={fps}>
        <div
          style={{
            position: "absolute",
            top: 50,
            left: 50,
            color: "white",
            fontSize: 48,
            fontWeight: "bold",
          }}
        >
          {title}
        </div>
      </Sequence>

      {/* Layer 4: Logo */}
      <Img
        src={logoUrl}
        style={{
          position: "absolute",
          top: 20,
          right: 20,
          width: 100,
          height: "auto",
        }}
      />
    </div>
  );
};
```

## 完整工作流

### 生成与合成

```typescript
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";

async function generateAvatarVideoForRemotion(
  script: string,
  outputPath: string
) {
  // 1. Generate HeyGen video
  console.log("Generating HeyGen avatar video...");
  const videoId = await generateHeyGenVideo(
    script,
    "josh_lite3_20230714",
    "1bd001e7e50f421d891986aad5158bc8",
    "landscape_1080p"
  );

  // 2. Wait for completion
  console.log("Waiting for HeyGen video...");
  const avatarVideoUrl = await waitForVideo(videoId);
  console.log(`HeyGen video ready: ${avatarVideoUrl}`);

  // 3. Get video duration for Remotion
  const avatarDuration = await getVideoDuration(avatarVideoUrl);
  const durationInFrames = Math.ceil(avatarDuration * 30); // 30 fps

  // 4. Bundle Remotion project
  console.log("Bundling Remotion project...");
  const bundleLocation = await bundle({
    entryPoint: "./remotion/src/index.ts",
  });

  // 5. Select composition
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: "AvatarVideo",
    inputProps: {
      avatarVideoUrl,
    },
  });

  // 6. Render final video
  console.log("Rendering final composition...");
  await renderMedia({
    composition: {
      ...composition,
      durationInFrames,
    },
    serveUrl: bundleLocation,
    codec: "h264",
    outputLocation: outputPath,
    inputProps: {
      avatarVideoUrl,
    },
  });

  console.log(`Final video rendered: ${outputPath}`);
  return outputPath;
}
```

### 使用 calculateMetadata 动态时长

```tsx
// remotion/src/AvatarComposition.tsx
import { CalculateMetadataFunction } from "remotion";

export const calculateAvatarMetadata: CalculateMetadataFunction<
  AvatarCompositionProps
> = async ({ props }) => {
  // Fetch video duration from HeyGen video
  const duration = await getVideoDurationInSeconds(props.avatarVideoUrl);

  return {
    durationInFrames: Math.ceil(duration * 30),
    fps: 30,
    width: 1920,
    height: 1080,
  };
};

// In Root.tsx
<Composition
  id="AvatarVideo"
  component={AvatarComposition}
  calculateMetadata={calculateAvatarMetadata}
  defaultProps={{
    avatarVideoUrl: "",
  }}
/>
```

## 最佳实践

### 1. 使用绿幕以获得灵活性

若需要后期合成，生成带绿幕背景的 HeyGen 视频：

```typescript
background: {
  type: "color",
  value: "#00FF00", // Pure green for chroma key
}
```

### 2. 匹配帧率

HeyGen 默认为 25 fps。设置 Remotion 帧率时需考虑：

```typescript
// Option 1: Match HeyGen's 25 fps
fps: 25

// Option 2: Use 30 fps with playback rate adjustment
<OffthreadVideo
  src={avatarVideoUrl}
  playbackRate={25/30} // Slow down slightly to match
/>
```

### 3. URL 与下载：何时用哪种

**直接使用 URL** 当：
- 在 Remotion Studio 中预览（`npm run dev`）
- URL 在渲染完成前不会过期
- 开发阶段希望更快迭代

```tsx
// Direct URL usage - simpler, faster for dev
<OffthreadVideo src={avatarVideoUrl} />
```

**先下载** 当：
- URL 会过期（HeyGen URL 约 24 小时后过期）
- 稍后再渲染或多次渲染
- 网络可靠性是问题
- 需要离线渲染

```typescript
// Download with retry for reliability
async function downloadVideoWithRetry(
  url: string,
  outputPath: string,
  maxRetries = 5
): Promise<string> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const buffer = await response.arrayBuffer();
      await fs.promises.writeFile(outputPath, Buffer.from(buffer));
      return outputPath;
    } catch (error) {
      const delay = 2000 * Math.pow(2, attempt);
      console.log(`Retry ${attempt + 1}/${maxRetries} in ${delay}ms...`);
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  throw new Error("Download failed after retries");
}

// Use local file in Remotion
const localPath = await downloadVideoWithRetry(avatarVideoUrl, "./public/avatar.mp4");
```

**混合方案**（生产环境推荐）：
```typescript
// Save both URL and local path in metadata
const metadata = {
  videoUrl: result.video_url,           // For quick preview
  localPath: "./public/avatar.mp4",     // For reliable rendering
  expiresAt: Date.now() + 24 * 60 * 60 * 1000, // URL expiration
};

// In Remotion component, prefer local if available
const videoSrc = fs.existsSync(localPath) ? staticFile("avatar.mp4") : avatarVideoUrl;
```

### 4. 处理数字人位置

合成中常见的数字人位置：

```typescript
const AVATAR_POSITIONS = {
  fullscreen: { width: "100%", height: "100%", position: "center" },
  bottomRight: { width: "40%", bottom: 0, right: 0 },
  bottomLeft: { width: "40%", bottom: 0, left: 0 },
  pictureInPicture: { width: "25%", bottom: 20, right: 20 },
  leftThird: { width: "33%", left: 0, height: "100%" },
};
```

## 输出格式

### HeyGen 输出
- 格式：MP4 (H.264)
- 音频：AAC
- 分辨率：按请求中指定

### Remotion 输出
- 编解码器：H.264（默认）、VP8、VP9、ProRes
- 与 HeyGen 质量设置匹配或更高

```typescript
await renderMedia({
  codec: "h264",
  crf: 18, // High quality
  // ...
});
```

## 故障排查

### Remotion 中视频无法播放

1. 检查 URL 是否可访问（CORS 问题）
2. 确认视频格式兼容
3. 先尝试下载到本地

### 尺寸不匹配

确保 HeyGen 与 Remotion 使用相同尺寸：

```typescript
// Shared config
const VIDEO_CONFIG = {
  width: 1920,
  height: 1080,
  fps: 30,
};

// HeyGen
dimension: { width: VIDEO_CONFIG.width, height: VIDEO_CONFIG.height }

// Remotion
<Composition width={VIDEO_CONFIG.width} height={VIDEO_CONFIG.height} />
```

### 渲染时视频抖动

若渲染输出中数字人视频抖动或卡顿：

1. **使用 `OffthreadVideo` 替代 `Video`** — 基础 `Video` 使用浏览器解码器，无法逐帧精确
2. 更新 import（无需额外安装 — 在核心 `remotion` 中）：
   ```tsx
   // Before (causes jitter)
   import { Video } from "remotion";

   // After (frame-accurate)
   import { OffthreadVideo } from "remotion";
   ```
3. 透明 WebM 需添加 `transparent` 属性：
   ```tsx
   <OffthreadVideo src={avatarWebmUrl} transparent />
   ```

### 音画不同步

若数字人音频漂移：
- 核对源视频帧率
- 检查编码问题
- 考虑用一致设置重新编码
