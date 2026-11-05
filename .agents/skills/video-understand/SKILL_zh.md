---
name: video-understand
description: |
  使用 ffmpeg 抽帧与 Whisper 转写，在本地理解视频内容。无需 API 密钥。
  适用场景：(1) 了解视频包含什么内容，(2) 在本地转写视频音频，
  (3) 抽取关键帧用于视觉分析，(4) 在不使用 API 密钥的情况下获取视频内容。
---

# video-understand

使用 ffmpeg 抽帧、Whisper 转写，在本地理解视频内容。完全离线，无需 API 密钥。

## 前提条件

- `ffmpeg` + `ffprobe`（必需）：`brew install ffmpeg`
- `openai-whisper`（可选，用于转写）：`pip install openai-whisper`

## 命令

```bash
# 场景检测 + 转写（默认）
python3 skills/video-understand/scripts/understand_video.py video.mp4

# 关键帧抽取
python3 skills/video-understand/scripts/understand_video.py video.mp4 -m keyframe

# 按固定间隔抽取
python3 skills/video-understand/scripts/understand_video.py video.mp4 -m interval

# 限制抽取帧数
python3 skills/video-understand/scripts/understand_video.py video.mp4 --max-frames 10

# 使用更大的 Whisper 模型
python3 skills/video-understand/scripts/understand_video.py video.mp4 --whisper-model small

# 仅抽帧，跳过转写
python3 skills/video-understand/scripts/understand_video.py video.mp4 --no-transcribe

# 安静模式（仅输出 JSON，无进度信息）
python3 skills/video-understand/scripts/understand_video.py video.mp4 -q

# 输出到文件
python3 skills/video-understand/scripts/understand_video.py video.mp4 -o result.json
```

## CLI 选项

| 标志 | 说明 |
|------|------|
| `video` | 输入视频文件（位置参数，必填） |
| `-m, --mode` | 抽取模式：`scene`（默认）、`keyframe`、`interval` |
| `--max-frames` | 最多保留的帧数（默认：20） |
| `--whisper-model` | Whisper 模型规模：tiny、base、small、medium、large（默认：base） |
| `--no-transcribe` | 跳过音频转写，仅抽取帧 |
| `-o, --output` | 将结果 JSON 写入文件而非 stdout |
| `-q, --quiet` | 不输出进度信息，仅输出 JSON |

## 抽取模式

| 模式 | 工作原理 | 适用场景 |
|------|-------------|----------|
| `scene` | 通过 ffmpeg `select='gt(scene,0.3)'` 检测场景变化 | 大多数视频、内容变化较多 |
| `keyframe` | 抽取 I 帧（编解码关键帧） | 已编码且关键帧分布自然的视频 |
| `interval` | 按时长与 max-frames 均匀采样 | 固定采样、输出可预期 |

若 `scene` 模式未检测到场景变化，会自动回退到 `interval` 模式。

## 输出

脚本将 JSON 输出到 stdout（或使用 `-o` 写入文件）。完整 schema 见 `references/output-format.md`。

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

对帧图片路径使用 Read 工具，可直观查看抽取的帧。

## 参考

- `references/output-format.md` -- 完整 JSON 输出 schema 文档
