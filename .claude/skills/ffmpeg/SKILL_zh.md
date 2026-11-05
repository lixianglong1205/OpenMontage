---
name: ffmpeg
description: 使用 FFmpeg 进行视频与音频处理。适用于格式转换、缩放、压缩、提取音频，以及为 Remotion 准备素材。触发场景包括将 GIF 转为 MP4、调整视频尺寸、提取音频、压缩文件或任意媒体转换任务。
---

# 用于视频制作的 FFmpeg

FFmpeg 是视频/音频处理的核心工具。本技能涵盖 Remotion 视频项目中的常见操作。

## 快速参考

### GIF 转 MP4（兼容 Remotion）

```bash
ffmpeg -i input.gif -movflags faststart -pix_fmt yuv420p \
  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4
```

**为何使用这些参数：**
- `-movflags faststart` - 将元数据移到文件开头，便于网页流式播放
- `-pix_fmt yuv420p` - 确保与大多数播放器兼容
- `scale=trunc(...)` - 强制偶数宽高（多数编解码器要求）

### 调整视频尺寸

```bash
# To 1920x1080 (maintain aspect ratio, add black bars)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4

# To 1920x1080 (crop to fill)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" output.mp4

# Scale to width, auto height
ffmpeg -i input.mp4 -vf "scale=1280:-2" output.mp4
```

### 压缩视频

```bash
# Good quality, smaller file (CRF 23 is default, lower = better quality)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4

# Aggressive compression for web preview
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 96k output.mp4

# Target file size (e.g., ~10MB for 60s video = ~1.3Mbps)
ffmpeg -i input.mp4 -c:v libx264 -b:v 1300k -c:a aac -b:a 128k output.mp4
```

### 提取音频

```bash
# Extract to MP3
ffmpeg -i input.mp4 -vn -acodec libmp3lame -q:a 2 output.mp3

# Extract to AAC
ffmpeg -i input.mp4 -vn -acodec aac -b:a 192k output.m4a

# Extract to WAV (uncompressed)
ffmpeg -i input.mp4 -vn output.wav
```

### 转换音频格式

```bash
# M4A to MP3 (for ElevenLabs voice samples)
ffmpeg -i input.m4a -codec:a libmp3lame -qscale:a 2 output.mp3

# WAV to MP3
ffmpeg -i input.wav -codec:a libmp3lame -b:a 192k output.mp3

# Adjust volume
ffmpeg -i input.mp3 -filter:a "volume=1.5" output.mp3
```

### 裁剪/剪切视频

```bash
# Cut from timestamp to duration (recommended - reliable)
ffmpeg -i input.mp4 -ss 00:00:30 -t 00:00:15 -c:v libx264 -c:a aac output.mp4

# Cut from timestamp to timestamp
ffmpeg -i input.mp4 -ss 00:00:30 -to 00:00:45 -c:v libx264 -c:a aac output.mp4

# Stream copy (faster but may lose frames at cut points)
# Only use when source has frequent keyframes
ffmpeg -i input.mp4 -ss 00:00:30 -t 00:00:15 -c copy output.mp4
```

**注意：** 裁剪时建议重新编码。流复制（`-c copy`）若 seek 点未对齐关键帧，可能静默丢失画面。

### 加速 / 减速

```bash
# 2x speed (video and audio)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" output.mp4

# 0.5x speed (slow motion)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" output.mp4

# Video only (no audio)
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" -an output.mp4
```

### 拼接视频

```bash
# Create file list
echo "file 'clip1.mp4'" > list.txt
echo "file 'clip2.mp4'" >> list.txt
echo "file 'clip3.mp4'" >> list.txt

# Concatenate (same codec/resolution)
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# Concatenate with re-encoding (different sources)
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac output.mp4
```

### 添加淡入/淡出

```bash
# Fade in first 1 second, fade out last 1 second (30fps video)
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1,fade=t=out:st=9:d=1" -c:a copy output.mp4

# Audio fade
ffmpeg -i input.mp4 -af "afade=t=in:st=0:d=1,afade=t=out:st=9:d=1" -c:v copy output.mp4
```

### 获取视频信息

```bash
# Duration, resolution, codec info
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4

# Full info
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
```

## Remotion 专用模式

### Remotion 中的视频调速

**何时用 FFmpeg、何时用 Remotion `playbackRate`：**

| 场景 | 使用 FFmpeg | 使用 Remotion |
|----------|------------|--------------|
| 恒定倍速（1.5x、2x） | 均可 | ✅ 更简单 |
| 极端倍速（>4x 或 <0.25x） | ✅ 更可靠 | 可能有问题 |
| 变速（随时间加速） | ✅ 预处理 | 需要复杂变通 |
| 需要完美音画同步 | ✅ 有保证 | 通常够用 |
| 演示需匹配旁白时长 | ✅ 预先计算 | 运行时调整 |

**Remotion 限制：** `playbackRate` 必须为常量。像 `playbackRate={interpolate(frame, [0, 100], [1, 5])}` 这样的动态插值无法正确工作，因为 Remotion 是逐帧独立求值的。

```bash
# Speed up demo to fit a scene (e.g., 60s demo into 20s = 3x speed)
ffmpeg -i demo-raw.mp4 \
  -filter_complex "[0:v]setpts=0.333*PTS[v];[0:a]atempo=3.0[a]" \
  -map "[v]" -map "[a]" \
  public/demos/demo-fast.mp4

# Slow motion for emphasis (0.5x speed)
ffmpeg -i action.mp4 \
  -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" \
  -map "[v]" -map "[a]" \
  public/demos/action-slow.mp4

# Speed up without audio (common for screen recordings)
ffmpeg -i demo.mp4 -filter:v "setpts=0.5*PTS" -an public/demos/demo-2x.mp4

# Timelapse effect (10x speed, drop audio)
ffmpeg -i long-demo.mp4 -filter:v "setpts=0.1*PTS" -an public/demos/timelapse.mp4
```

**计算速度系数：**
- 将 X 秒视频放进 Y 秒场景：`speed = X / Y`
- setpts 乘数 = `1 / speed`（例如 3 倍速 = setpts=0.333*PTS）
- atempo 值 = `speed`（例如 3 倍速 = atempo=3.0）

**极端倍速（音频 >2x）：** 串联 atempo 滤镜（每个限制在 0.5–2.0 范围）：
```bash
# 4x speed audio
-filter_complex "[0:a]atempo=2.0,atempo=2.0[a]"

# 8x speed audio
-filter_complex "[0:a]atempo=2.0,atempo=2.0,atempo=2.0[a]"
```

### 为 Remotion 准备演示录制

```bash
# Standard 1080p, 30fps, Remotion-ready
ffmpeg -i raw-recording.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -crf 18 -preset slow \
  -c:a aac -b:a 192k \
  -movflags faststart \
  public/demos/demo.mp4
```

### 录屏转为 Remotion 素材

```bash
# From iPhone/iPad recording (usually 60fps, variable resolution)
ffmpeg -i iphone-recording.mov \
  -vf "scale=1920:-2,fps=30" \
  -c:v libx264 -crf 20 \
  -an \
  public/demos/mobile-demo.mp4
```

### 批量转换 GIF

```bash
for f in assets/*.gif; do
  ffmpeg -i "$f" -movflags faststart -pix_fmt yuv420p \
    -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
    "public/demos/$(basename "$f" .gif).mp4"
done
```

## 常见问题

### “Height not divisible by 2”（高度不能被 2 整除）
添加缩放滤镜：`-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`

### 浏览器无法播放视频
使用：`-movflags faststart -pix_fmt yuv420p -c:v libx264`

### 变速后音画不同步
使用 filter_complex 配合 atempo：`-filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]"`

### 文件过大
提高 CRF（23→28）或降低分辨率

## 质量指南

| 用途 | CRF | Preset | 说明 |
|----------|-----|--------|-------|
| 归档/母版 | 18 | slow | 最佳质量，文件较大 |
| 成片 | 20-22 | medium | 平衡较好 |
| 网页/预览 | 23-25 | fast | 文件更小 |
| 草稿/快速 | 28+ | veryfast | 编码更快 |

## 各平台输出优化

Remotion 渲染完成后（通常为 `out/video.mp4`），可用 FFmpeg 针对各分发平台优化。

### 工作流集成

```
Remotion render (master)     FFmpeg optimization      Platform upload
       ↓                            ↓                       ↓
   out/video.mp4  ────────→  out/video-youtube.mp4  ───→  YouTube
                  ────────→  out/video-twitter.mp4  ───→  Twitter/X
                  ────────→  out/video-linkedin.mp4 ───→  LinkedIn
                  ────────→  out/video-web.mp4      ───→  Website embed
```

### YouTube（推荐设置）

YouTube 会重新编码所有上传内容，因此应上传高质量源文件：

```bash
# YouTube optimized (1080p)
ffmpeg -i out/video.mp4 \
  -c:v libx264 -preset slow -crf 18 \
  -profile:v high -level 4.0 \
  -bf 2 -g 30 \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart \
  out/video-youtube.mp4

# YouTube Shorts (vertical 1080x1920)
ffmpeg -i out/video.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -crf 18 -c:a aac -b:a 192k \
  out/video-shorts.mp4
```

### Twitter/X

Twitter 限制严格：最长 140 秒、512MB、1920x1200：

```bash
# Twitter optimized (under 15MB target for fast upload)
ffmpeg -i out/video.mp4 \
  -c:v libx264 -preset medium -crf 24 \
  -profile:v main -level 3.1 \
  -vf "scale='min(1280,iw)':'min(720,ih)':force_original_aspect_ratio=decrease" \
  -c:a aac -b:a 128k -ar 44100 \
  -movflags +faststart \
  -fs 15M \
  out/video-twitter.mp4

# Check file size and duration
ffprobe -v error -show_entries format=duration,size -of csv=p=0 out/video-twitter.mp4
```

### LinkedIn

LinkedIn 偏好带 AAC 音频的 MP4，最长 10 分钟：

```bash
# LinkedIn optimized
ffmpeg -i out/video.mp4 \
  -c:v libx264 -preset medium -crf 22 \
  -profile:v main \
  -vf "scale='min(1920,iw)':'min(1080,ih)':force_original_aspect_ratio=decrease" \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart \
  out/video-linkedin.mp4
```

### 网站/嵌入（优化快速加载）

```bash
# Web-optimized MP4 (small file, progressive loading)
ffmpeg -i out/video.mp4 \
  -c:v libx264 -preset medium -crf 26 \
  -profile:v baseline -level 3.0 \
  -vf "scale=1280:720" \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  out/video-web.mp4

# WebM alternative (better compression, wider browser support)
ffmpeg -i out/video.mp4 \
  -c:v libvpx-vp9 -crf 30 -b:v 0 \
  -vf "scale=1280:720" \
  -c:a libopus -b:a 128k \
  -deadline good \
  out/video-web.webm
```

### GIF（预览/缩略图）

```bash
# High-quality GIF (first 5 seconds)
ffmpeg -i out/video.mp4 -t 5 \
  -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  out/preview.gif

# Smaller file GIF
ffmpeg -i out/video.mp4 -t 3 \
  -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  out/preview-small.gif
```

### 各平台要求速查

| 平台 | 最大分辨率 | 最大体积 | 最大时长 | 音频 |
|----------|---------------|----------|--------------|-------|
| YouTube | 8K | 256GB | 12 hours | AAC 48kHz |
| Twitter/X | 1920x1200 | 512MB | 140s | AAC 44.1kHz |
| LinkedIn | 4096x2304 | 5GB | 10 min | AAC 48kHz |
| Instagram Feed | 1080x1350 | 4GB | 60s | AAC 48kHz |
| Instagram Reels | 1080x1920 | 4GB | 90s | AAC 48kHz |
| TikTok | 1080x1920 | 287MB | 10 min | AAC |

### 批量导出全平台

```bash
#!/bin/bash
# save as: export-all-platforms.sh
INPUT="out/video.mp4"

# YouTube (high quality)
ffmpeg -i "$INPUT" -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k -movflags +faststart \
  out/video-youtube.mp4

# Twitter (compressed)
ffmpeg -i "$INPUT" -c:v libx264 -crf 24 \
  -vf "scale='min(1280,iw)':'-2'" \
  -c:a aac -b:a 128k -movflags +faststart \
  out/video-twitter.mp4

# LinkedIn
ffmpeg -i "$INPUT" -c:v libx264 -crf 22 \
  -c:a aac -b:a 192k -movflags +faststart \
  out/video-linkedin.mp4

# Web embed (small)
ffmpeg -i "$INPUT" -c:v libx264 -crf 26 \
  -vf "scale=1280:720" \
  -c:a aac -b:a 128k -movflags +faststart \
  out/video-web.mp4

echo "Exported:"
ls -lh out/video-*.mp4
```

## 错误处理

处理视频时的常见错误与修复：

```bash
# Check if FFmpeg succeeded
ffmpeg -i input.mp4 -c:v libx264 output.mp4 && echo "Success" || echo "Failed: check input file"

# Validate output file is playable
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 output.mp4

# Get detailed error info
ffmpeg -v error -i input.mp4 -f null - 2>&1 | head -20
```

### 常见失败处理

| 错误 | 原因 | 修复 |
|-------|-------|-----|
| "No such file" | 输入路径错误 | 检查路径，路径含空格时使用引号 |
| "Invalid data" | 输入损坏 | 重新下载或重新录制源文件 |
| "height not divisible by 2" | 奇数尺寸 | 添加带 trunc 的 scale 滤镜 |
| "encoder not found" | 缺少编解码器 | 安装完整编解码器的 FFmpeg |
| Output 0 bytes | 静默失败 | 查看完整 ffmpeg 输出中的错误 |

---

## 反馈与贡献

若本技能缺少信息或可改进：

- **缺少某条命令？** 说明你需要什么
- **发现错误？** 告知哪里不对
- **想要贡献？** 我可以协助你：
  1. 更新本技能
  2. 向 github.com/digitalsamba/claude-code-video-toolkit 提交 PR

只需说「improve this skill」，我会引导你更新 `.claude/skills/ffmpeg/SKILL.md`。
