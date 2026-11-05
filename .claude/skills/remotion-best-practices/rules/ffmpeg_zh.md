---
name: ffmpeg
description: 在 Remotion 中使用 FFmpeg 与 FFprobe
metadata:
  tags: ffmpeg, ffprobe, video, trimming
---

## Remotion 中的 FFmpeg

无需单独安装 `ffmpeg` 和 `ffprobe`。可通过 `bunx remotion ffmpeg` 与 `bunx remotion ffprobe` 使用：

```bash
bunx remotion ffmpeg -i input.mp4 output.mp3
bunx remotion ffprobe input.mp4
```

### 裁剪视频

裁剪视频有两种方式：

1. 使用 FFmpeg 命令行。必须重新编码视频，否则视频开头可能出现定格帧。

```bash
# Re-encodes from the exact frame
bunx remotion ffmpeg -ss 00:00:05 -i public/input.mp4 -to 00:00:10 -c:v libx264 -c:a aac public/output.mp4
```

2. 使用 `<Video>` 组件的 `trimBefore` 与 `trimAfter` 属性。优点是非破坏性编辑，可随时调整裁剪范围。

```tsx
import { Video } from "@remotion/media";

<Video
  src={staticFile("video.mp4")}
  trimBefore={5 * fps}
  trimAfter={10 * fps}
/>;
```
