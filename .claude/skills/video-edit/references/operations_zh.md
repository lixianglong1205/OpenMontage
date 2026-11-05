# 操作参考

每种操作的详细 ffmpeg 配方。各节展示命令、说明关键参数，并列出常见变体。

---

## info

使用 ffprobe 获取视频文件的完整元数据。

```bash
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4
```

**关键参数：**
- `-v quiet` — 抑制横幅/日志噪声，仅输出请求的数据。
- `-print_format json` — 以 JSON 输出（便于解析）。也可使用 `csv`、`flat`、`ini`。
- `-show_format` — 容器级信息：时长、码率、格式名、大小。
- `-show_streams` — 各流信息：编解码器、分辨率、帧率、采样率、声道。

**变体：**
```bash
# Duration only (seconds, as plain text)
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 video.mp4

# Resolution only
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 video.mp4
```

---

## trim

使用流复制（不重新编码，非常快）从视频中截取一段。

```bash
ffmpeg -y -ss 00:00:30 -to 00:01:45 -i video.mp4 -c copy trimmed.mp4
```

**关键参数：**
- `-ss <time>` — 定位到起始位置。放在 `-i` 之前可快速输入定位。
- `-to <time>` — 在此时间戳停止（绝对时间）。也可用 `-t <duration>` 表示相对时长。
- `-c copy` — 复制流而不重新编码。速度快，但仅在关键帧处切割（可能偏差几帧）。

**时间戳** 支持 `HH:MM:SS`、`HH:MM:SS.mmm`、`MM:SS` 或纯秒数（`90`、`90.5`）。

**变体：**
```bash
# By duration instead of end time
ffmpeg -y -ss 00:00:30 -t 75 -i video.mp4 -c copy trimmed.mp4

# Frame-accurate trim (re-encodes, slower but exact)
ffmpeg -y -ss 00:00:30 -to 00:01:45 -i video.mp4 -c:v libx264 -c:a aac trimmed.mp4
```

---

## concat

将多个视频文件拼接为一个文件。

```bash
# Step 1: Create a concat list file
printf "file '%s'\n" clip1.mp4 clip2.mp4 clip3.mp4 > list.txt

# Step 2: Concat with stream copy
ffmpeg -y -f concat -safe 0 -i list.txt -c copy joined.mp4
```

**关键参数：**
- `-f concat` — 使用 concat 解复用器。
- `-safe 0` — 允许列表文件中使用绝对路径。
- `-c copy` — 复制流而不重新编码。要求所有输入具有相同编解码器、分辨率和帧率。

**变体：**
```bash
# Re-encode to normalize mismatched clips (slower)
ffmpeg -y -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac joined.mp4

# Inline concat without a file (only for same-format files)
ffmpeg -y -i "concat:part1.ts|part2.ts" -c copy joined.ts
```

---

## resize

将视频缩放到指定尺寸，并保持宽高比填充。

```bash
ffmpeg -y -i video.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:a copy resized.mp4
```

**关键参数：**
- `-vf` — 视频滤镜链。
- `scale=W:H:force_original_aspect_ratio=decrease` — 在 WxH 内缩小以适应，保持宽高比。
- `pad=W:H:(ow-iw)/2:(oh-ih)/2:black` — 填充到精确 WxH，居中黑边。
- `-c:a copy` — 复制音频而不重新编码。

**变体：**
```bash
# Scale to width, auto-calculate height (maintains aspect ratio)
ffmpeg -y -i video.mp4 -vf "scale=1280:-2" -c:a copy resized.mp4

# Scale to height, auto-calculate width
ffmpeg -y -i video.mp4 -vf "scale=-2:720" -c:a copy resized.mp4

# Custom dimensions without padding (stretches)
ffmpeg -y -i video.mp4 -vf "scale=1280:720" -c:a copy resized.mp4
```

---

## speed

同时改变视频与音频的播放速度。

```bash
# 2x faster
ffmpeg -y -i video.mp4 -filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0" fast.mp4

# Half speed (slow motion)
ffmpeg -y -i video.mp4 -filter:v "setpts=2.0*PTS" -filter:a "atempo=0.5" slow.mp4
```

**关键参数：**
- `-filter:v "setpts=N*PTS"` — 乘以呈现时间戳。`0.5` = 2 倍速，`2.0` = 半速。公式：`N = 1 / speed_factor`。
- `-filter:a "atempo=F"` — 调整音频速度。保持音高。仅支持 0.5 至 2.0 之间的值。

**对于 0.5–2.0 之外的倍率**，可串联多个 atempo 滤镜：
```bash
# 4x faster
ffmpeg -y -i video.mp4 -filter:v "setpts=0.25*PTS" -filter:a "atempo=2.0,atempo=2.0" fast4x.mp4

# 0.25x (very slow)
ffmpeg -y -i video.mp4 -filter:v "setpts=4.0*PTS" -filter:a "atempo=0.5,atempo=0.5" slow025x.mp4
```

---

## extract-audio

从视频文件中提取音轨。

```bash
ffmpeg -y -i video.mp4 -vn -acodec libmp3lame audio.mp3
```

**关键参数：**
- `-vn` — 禁用视频（仅输出音频）。
- `-acodec <codec>` — 使用的音频编解码器。

**音频编解码器对照：**

| 格式 | 编解码器参数       |
|--------|------------------|
| mp3    | `libmp3lame`     |
| wav    | `pcm_s16le`      |
| aac    | `aac`            |
| flac   | `flac`           |

**变体：**
```bash
# Extract as WAV (lossless)
ffmpeg -y -i video.mp4 -vn -acodec pcm_s16le audio.wav

# Extract as AAC
ffmpeg -y -i video.mp4 -vn -acodec aac audio.aac

# Copy audio codec as-is (fastest, keeps original format)
ffmpeg -y -i video.mp4 -vn -acodec copy audio.aac
```

---

## replace-audio

用另一段音频替换视频中的音轨。

```bash
ffmpeg -y -i video.mp4 -i audio.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -shortest output.mp4
```

**关键参数：**
- `-i video.mp4 -i audio.mp3` — 两个输入：视频（索引 0）与音频（索引 1）。
- `-c:v copy` — 复制视频流而不重新编码。
- `-map 0:v:0` — 取自第一个输入的视频。
- `-map 1:a:0` — 取自第二个输入的音频。
- `-shortest` — 在较短的输入结束时停止。

**变体：**
```bash
# Remove audio entirely (silent video)
ffmpeg -y -i video.mp4 -c:v copy -an silent.mp4

# Mix original audio with new audio (overlay, not replace)
ffmpeg -y -i video.mp4 -i music.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" -c:v copy mixed.mp4
```

---

## overlay

在视频上叠加图像（水印、标识）。

```bash
# Bottom-right corner (10px padding)
ffmpeg -y -i video.mp4 -i logo.png \
  -filter_complex "overlay=W-w-10:H-h-10" -c:a copy watermarked.mp4
```

**关键参数：**
- `-filter_complex "overlay=X:Y"` — 在坐标 X,Y 处放置叠加图像。
- `-c:a copy` — 复制音频而不重新编码。

**位置表达式：**

| 位置     | 表达式              |
|--------------|-------------------------|
| 左上     | `overlay=10:10`         |
| 右上    | `overlay=W-w-10:10`     |
| 左下  | `overlay=10:H-h-10`    |
| 右下 | `overlay=W-w-10:H-h-10` |
| 居中       | `overlay=(W-w)/2:(H-h)/2` |

`W`/`H` = 视频尺寸，`w`/`h` = 叠加图尺寸。

**变体：**
```bash
# With opacity (semi-transparent watermark)
ffmpeg -y -i video.mp4 -i logo.png \
  -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.5[ovr];[0:v][ovr]overlay=W-w-10:10" \
  -c:a copy watermarked.mp4

# Overlay only during a time range (show from 5s to 15s)
ffmpeg -y -i video.mp4 -i logo.png \
  -filter_complex "overlay=10:10:enable='between(t,5,15)'" -c:a copy watermarked.mp4
```

---

## compress

减小视频文件体积。

### 基于 CRF（简单，推荐）

```bash
ffmpeg -y -i video.mp4 -crf 23 -preset medium -c:a copy compressed.mp4
```

**关键参数：**
- `-crf <int>` — 恒定速率因子（Constant Rate Factor）。数值越低 = 质量越好、文件越大。0 = 无损，18 = 视觉无损，23 = 默认，28 = 更小/质量更低。
- `-preset <speed>` — 编码速度与压缩权衡：`ultrafast`、`superfast`、`veryfast`、`faster`、`fast`、`medium`、`slow`、`slower`、`veryslow`。越慢 = 相同质量下文件越小。
- `-c:a copy` — 原样复制音频。

### 目标文件大小

若要达到指定文件大小，需计算所需视频码率：

```bash
# Formula: video_bitrate = (target_MB * 8 * 1024) / duration_seconds - audio_bitrate
# Example: 25MB target, 120s video, 128kbps audio
# video_bitrate = (25 * 8 * 1024) / 120 - 128 = 1578 kbps

ffmpeg -y -i video.mp4 \
  -b:v 1578k -maxrate 1578k -bufsize 3156k \
  -c:a aac -b:a 128k \
  compressed.mp4
```

**变体：**
```bash
# Aggressive compression (smaller, lower quality)
ffmpeg -y -i video.mp4 -crf 28 -preset slow -c:a copy small.mp4

# High quality (larger file)
ffmpeg -y -i video.mp4 -crf 18 -preset slow -c:a copy hq.mp4
```

---

## convert

将视频转换为不同容器格式。

```bash
ffmpeg -y -i video.mov output.mp4
```

ffmpeg 根据文件扩展名推断输出格式。多数转换只需这一条命令。

**支持的格式：** mp4、mov、avi、mkv、webm、gif。

### GIF 转换（高质量，两遍调色板）

```bash
# Step 1: Generate optimized palette
ffmpeg -y -i video.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,palettegen" palette.png

# Step 2: Use palette for high-quality GIF
ffmpeg -y -i video.mp4 -i palette.png \
  -filter_complex "fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif

# Clean up
rm palette.png
```

**变体：**
```bash
# Quick GIF (lower quality, single pass)
ffmpeg -y -i video.mp4 -vf "fps=10,scale=320:-1" output.gif

# Convert to WebM (VP9)
ffmpeg -y -i video.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm
```
