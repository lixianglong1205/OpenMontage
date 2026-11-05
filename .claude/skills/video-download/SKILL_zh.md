---
name: video-download
description: |
  使用 yt-dlp 从 YouTube 及 1000+ 站点下载视频与音频。无需 API 密钥。
  适用场景：(1) 从 YouTube 或其他站点下载视频，(2) 从视频 URL 提取音频，
  (3) 下载视频字幕/说明文字，(4) 在不下载的情况下获取视频元数据。
---

# video-download

使用 yt-dlp 直接从 URL 下载视频与音频。无需封装脚本。

## 前提条件

- **yt-dlp**：`brew install yt-dlp` 或 `pip install yt-dlp`
- **ffmpeg**：`brew install ffmpeg` 或 `apt install ffmpeg`（合并视频+音频流时需要）

请定期更新 yt-dlp 以适配站点变更：`yt-dlp -U` 或 `pip install -U yt-dlp`。

## 命令

### 下载最佳画质

```bash
yt-dlp "URL" -o "%(title)s.%(ext)s" --merge-output-format mp4
```

### 下载指定分辨率

```bash
# 720p
yt-dlp "URL" -f "bestvideo[height<=720]+bestaudio/best[height<=720]" --merge-output-format mp4

# 1080p
yt-dlp "URL" -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" --merge-output-format mp4
```

### 仅音频

```bash
yt-dlp "URL" -x --audio-format mp3 --audio-quality 0
```

### 下载字幕

```bash
# 下载带英文字幕的视频
yt-dlp "URL" --write-subs --sub-langs en --merge-output-format mp4

# 下载带多语言字幕的视频
yt-dlp "URL" --write-subs --sub-langs "en,es,fr" --merge-output-format mp4

# 仅下载字幕（不下载视频）
yt-dlp "URL" --write-subs --sub-langs en --skip-download
```

### 获取元数据（不下载）

```bash
yt-dlp "URL" --dump-json --no-download
```

### 列出可用格式

```bash
yt-dlp "URL" -F
```

### 指定输出目录

```bash
yt-dlp "URL" -o "./downloads/%(title)s.%(ext)s" --merge-output-format mp4
```

## 画质预设

| 画质 | 格式参数 |
|---------|-------------|
| 最佳 | `-f "bestvideo+bestaudio/best"`（默认） |
| 1080p | `-f "bestvideo[height<=1080]+bestaudio/best[height<=1080]"` |
| 720p | `-f "bestvideo[height<=720]+bestaudio/best[height<=720]"` |
| 480p | `-f "bestvideo[height<=480]+bestaudio/best[height<=480]"` |
| 最低 | `-f "worstvideo+worstaudio/worst"` |

## 输出模板变量

`-o` 模板常用变量：

| 变量 | 说明 |
|----------|-------------|
| `%(title)s` | 视频标题 |
| `%(ext)s` | 文件扩展名 |
| `%(id)s` | 视频 ID |
| `%(uploader)s` | 频道/上传者名称 |
| `%(upload_date)s` | 上传日期（YYYYMMDD） |
| `%(duration)s` | 时长（秒） |
| `%(resolution)s` | 视频分辨率 |

## 提示

- 始终使用 `--merge-output-format mp4`，避免得到 `.webm` 或 `.mkv` 文件。
- 仅查询元数据时使用 `--no-download` 配合 `--dump-json`——不会写入磁盘文件。
- 若下载因 HTTP 错误失败，请先更新 yt-dlp（`yt-dlp -U`）。
- 不需要完整分辨率时，使用 `-f "bestvideo[height<=720]+bestaudio"` 以节省带宽。
- yt-dlp 会自动处理限速与重试。
- `--dump-json` 输出包含 `title`、`duration`、`uploader`、`view_count`、`description`、`formats`、`subtitles` 等大量字段。

## 故障排除

- **「yt-dlp: command not found」**：安装 yt-dlp（`pip install yt-dlp`），并确保 PATH 包含 pip 的 bin 目录。
- **「ffmpeg: command not found」**：安装 ffmpeg。未安装时，当视频与音频为分离流（YouTube 高清常见）会导致下载失败。
- **下载失败或返回错误**：运行 `yt-dlp -U` 更新。站点变更频繁，yt-dlp 会定期发布修复。
