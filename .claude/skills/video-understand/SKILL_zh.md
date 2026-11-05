---
name: video-understand
description: |
  使用 ffmpeg 帧提取与 Whisper 转录在本地理解视频内容。无需 API 密钥。
  适用于：(1) 了解视频包含什么内容，(2) 在本地转录视频音频，
  (3) 提取关键帧以进行视觉分析，(4) 在不使用 API 密钥的情况下获取视频内容。
---

# video-understand

使用 ffmpeg 进行帧提取、Whisper 进行转录，在本地理解视频内容。完全离线，无需 API 密钥。

## 前提条件

- `ffmpeg` + `ffprobe`（必需）：`brew install ffmpeg`
- `openai-whisper`（可选，用于转录）：`pip install openai-whisper`

## 命令

```bash
# Scene detection + transcribe (default)
python3 skills/video-understand/scripts/understand_video.py video.mp4

# Keyframe extraction
python3 skills/video-understand/scripts/understand_video.py video.mp4 -m keyframe

# Regular interval extraction
python3 skills/video-understand/scripts/understand_video.py video.mp4 -m interval

# Limit frames extracted
python3 skills/video-understand/scripts/understand_video.py video.mp4 --max-frames 10

# Use a larger Whisper model
python3 skills/video-understand/scripts/understand_video.py video.mp4 --whisper-model small

# Frames only, skip transcription
python3 skills/video-understand/scripts/understand_video.py video.mp4 --no-transcribe

# Quiet mode (JSON only, no progress)
python3 skills/video-understand/scripts/understand_video.py video.mp4 -q

# Output to file
python3 skills/video-understand/scripts/understand_video.py video.mp4 -o result.json
```

## CLI 选项

| Flag | 说明 |
|------|------|
| `video` | 输入视频文件（位置参数，必需） |
| `-m, --mode` | 提取模式：`scene`（默认）、`keyframe`、`interval` |
| `--max-frames` | 保留的最大帧数（默认：20） |
| `--whisper-model` | Whisper 模型大小：tiny、base、small、medium、large（默认：base） |
| `--no-transcribe` | 跳过音频转录，仅提取帧 |
| `-o, --output` | 将结果 JSON 写入文件而非 stdout |
| `-q, --quiet` | 抑制进度消息，仅输出 JSON |

## 提取模式

| 模式 | 工作原理 | 适用场景 |
|------|-------------|----------|
| `scene` | 通过 ffmpeg `select='gt(scene,0.3)'` 检测场景变化 | 大多数视频、内容变化丰富的素材 |
| `keyframe` | 提取 I 帧（编解码关键帧） | 关键帧分布自然的已编码视频 |
| `interval` | 根据时长与 max-frames 均匀采样帧 | 固定采样、输出可预期 |

若 `scene` 模式未检测到场景变化，将自动回退为 `interval` 模式。

## 输出

脚本将 JSON 输出到 stdout（或使用 `-o` 写入文件）。完整模式见 `references/output-format.md`。

```json
{
  "video": "video.mp4",
  "duration": 18.076,
  "resolution": {"width": 1224, "height": 1080},
  "mode": "scene",
  "frames": [
    {"path": "/abs/path/frame_0001.jpg", "timestamp": 0.0, "timestamp_formatted": "00:00"}
  ],
  "frame_count": 12,
  "transcript": [
    {"start": 0.0, "end": 2.5, "text": "Hello and welcome..."}
  ],
  "text": "Full transcript...",
  "note": "Use the Read tool to view frame images for visual understanding."
}
```

使用 Read 工具打开帧图像路径，对提取的帧进行视觉检查。

## 参考

- `references/output-format.md` -- 完整 JSON 输出模式文档
