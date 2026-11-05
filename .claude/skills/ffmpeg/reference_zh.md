# FFmpeg 参考

## 滤镜语法

### 视频滤镜 (-vf)

```bash
# Chain filters with comma
-vf "scale=1920:1080,fps=30,crop=1280:720"

# Complex filters with labels
-filter_complex "[0:v]scale=1920:1080[scaled];[scaled]fps=30[out]" -map "[out]"
```

### 常用视频滤镜

| 滤镜 | 语法 | 示例 |
|--------|--------|---------|
| scale | `scale=w:h` | `scale=1920:1080` 或 `scale=1280:-1`（高度自动） |
| crop | `crop=w:h:x:y` | `crop=1280:720:320:180` |
| fps | `fps=N` | `fps=30` |
| pad | `pad=w:h:x:y:color` | `pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black` |
| fade | `fade=t=in/out:st=N:d=N` | `fade=t=in:st=0:d=1` |
| setpts | `setpts=N*PTS` | `setpts=0.5*PTS`（2 倍速） |
| drawtext | `drawtext=text='Hi':fontsize=24` | 添加文字叠加 |
| overlay | `overlay=x:y` | 合成多个视频 |

### 常用音频滤镜 (-af)

| 滤镜 | 语法 | 示例 |
|--------|--------|---------|
| volume | `volume=N` | `volume=1.5` 或 `volume=0.5` |
| afade | `afade=t=in/out:st=N:d=N` | `afade=t=in:st=0:d=1` |
| atempo | `atempo=N` | `atempo=2.0`（2 倍速，范围 0.5–2.0） |
| loudnorm | `loudnorm` | 标准化音量 |

## 编解码器选项

### 视频编解码器 (-c:v)

| 编解码器 | 用途 | 说明 |
|-------|----------|-------|
| libx264 | 通用 H.264 | 兼容性最好 |
| libx265 | H.265/HEVC | 压缩更好，兼容性略差 |
| libvpx-vp9 | WebM | 适合 Web |
| prores | ProRes | 专业剪辑 |
| copy | 流复制 | 不重编码，最快 |

### 音频编解码器 (-c:a)

| 编解码器 | 用途 | 说明 |
|-------|----------|-------|
| aac | MP4 容器 | 兼容性最好 |
| libmp3lame | MP3 | 通用 |
| libvorbis | WebM/OGG | 开源 |
| pcm_s16le | WAV | 未压缩 |
| copy | 流复制 | 不重编码 |

## 质量设置

### x264/x265 的 CRF（恒定码率因子，Constant Rate Factor）

| CRF | 质量 | 用途 |
|-----|---------|----------|
| 0 | 无损 | 归档 |
| 17-18 | 视觉无损 | 母版 |
| 19-22 | 高质量 | 制作 |
| 23 | 默认 | 一般用途 |
| 24-27 | 中等 | Web 分发 |
| 28+ | 较低 | 预览/草稿 |

### 预设 (-preset)

预设越快 = 文件越大、编码越快

`ultrafast` → `superfast` → `veryfast` → `faster` → `fast` → `medium` → `slow` → `slower` → `veryslow`

## 容器格式

| 格式 | 扩展名 | 最适合 |
|--------|-----------|----------|
| MP4 | .mp4 | 通用、Web、移动端 |
| MOV | .mov | Apple 生态、ProRes |
| WebM | .webm | Web（VP9） |
| MKV | .mkv | 归档、多路流 |
| GIF | .gif | 短动画（无音频） |

## 输入/输出选项

### 输入选项（在 -i 之前）

| 选项 | 作用 | 示例 |
|--------|---------|---------|
| -ss | 定位到时间点 | `-ss 00:01:30` |
| -t | 限制时长 | `-t 00:00:30` |
| -r | 输入帧率 | `-r 30` |
| -f | 强制格式 | `-f gif` |

### 输出选项（在 -i 之后）

| 选项 | 作用 | 示例 |
|--------|---------|---------|
| -y | 覆盖输出文件 | `-y` |
| -n | 永不覆盖 | `-n` |
| -movflags faststart | Web 流式播放 | `-movflags faststart` |
| -pix_fmt | 像素格式 | `-pix_fmt yuv420p` |
| -an | 无音频 | `-an` |
| -vn | 无视频 | `-vn` |

## 实用模式

### 获取时长（秒）

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 input.mp4
```

### 获取分辨率

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 input.mp4
```

### 获取帧数

```bash
ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of csv=p=0 input.mp4
```

### 创建缩略图

```bash
# At specific time
ffmpeg -i input.mp4 -ss 00:00:05 -vframes 1 thumbnail.jpg

# Best quality
ffmpeg -i input.mp4 -ss 00:00:05 -vframes 1 -q:v 2 thumbnail.jpg
```

### 从视频创建 GIF

```bash
# Simple (large file)
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1" output.gif

# With palette (better quality, smaller)
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

### 画中画

```bash
# Overlay small video in corner
ffmpeg -i main.mp4 -i overlay.mp4 \
  -filter_complex "[1:v]scale=320:-1[pip];[0:v][pip]overlay=W-w-20:H-h-20" \
  -c:a copy output.mp4
```

### 并排视频

```bash
ffmpeg -i left.mp4 -i right.mp4 \
  -filter_complex "[0:v][1:v]hstack=inputs=2[v]" \
  -map "[v]" -c:v libx264 output.mp4
```

## Remotion 集成说明

- Remotion 使用 `<OffthreadVideo>`，可处理大多数格式
- 优先使用 MP4 容器中的 H.264（libx264）
- Web 播放务必使用 `-movflags faststart`
- 帧率与合成一致（通常为 30fps）
- 分辨率应与合成一致（常见为 1920×1080）
