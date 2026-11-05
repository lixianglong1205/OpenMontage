# 输出格式

## 结果 JSON

主脚本（`understand_video.py`）向 stdout 输出 JSON 对象（或使用 `-o` 写入文件），其中包含视频元数据、提取的帧路径以及转写数据。

```json
{
  "video": "video.mp4",
  "duration": 18.076,
  "resolution": {
    "width": 1224,
    "height": 1080
  },
  "mode": "scene",
  "frames": [
    {
      "path": "/absolute/path/to/frames/frame_0001.jpg",
      "timestamp": 0.0,
      "timestamp_formatted": "00:00"
    },
    {
      "path": "/absolute/path/to/frames/frame_0002.jpg",
      "timestamp": 3.2,
      "timestamp_formatted": "00:03"
    }
  ],
  "frame_count": 12,
  "transcript": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "Hello and welcome to this video."
    },
    {
      "start": 2.8,
      "end": 5.1,
      "text": "Today we will discuss..."
    }
  ],
  "text": "Hello and welcome to this video. Today we will discuss...",
  "note": "Use the Read tool to view frame images for visual understanding."
}
```

## 顶层字段

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `video` | string | 原始视频文件名（basename） |
| `duration` | float | 视频时长（秒） |
| `resolution` | object | 视频分辨率，含 `width` 与 `height` |
| `mode` | string | 使用的提取模式：`scene`、`keyframe` 或 `interval` |
| `frames` | array | 已提取帧对象的数组 |
| `frame_count` | integer | 提取的帧数量 |
| `transcript` | array 或 null | 转写片段数组；若跳过转写则为 `null` |
| `text` | string 或 null | 完整转写文本（单字符串）；若跳过则为 `null` |
| `note` | string | 提示 Claude 如何使用帧图像 |

## 帧对象

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `path` | string | 已提取 JPEG 帧的绝对路径 |
| `timestamp` | float | 相对视频起点的帧时间戳（秒） |
| `timestamp_formatted` | string | 人类可读时间戳，格式为 `MM:SS` 或 `HH:MM:SS` |

## 转写片段

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `start` | float | 片段起始时间（秒） |
| `end` | float | 片段结束时间（秒） |
| `text` | string | 该片段的转写文本 |

## 帧路径约定

帧提取到与视频文件相邻的目录中：

```
video.mp4
video_frames/
  frame_0001.jpg
  frame_0002.jpg
  ...
```

目录名为 `{video_stem}_frames`。JSON 输出中所有帧路径均为绝对路径，可直接配合 Read 工具使用。

## 空值字段

- 使用 `--no-transcribe` 或未安装 Whisper 时，`transcript` 与 `text` 为 `null`。
- 若场景检测未发现任何场景，模式会自动回退为 `interval`，且 `mode` 字段反映实际使用的模式。

## 与 Claude 配合使用

若要视觉检查视频内容，请对 `frames` 数组返回的帧路径使用 Read 工具。Claude 可直接查看 JPEG 图像并描述其内容。结合转写文本，即可在不依赖任何云端 API 的情况下完整理解视频。
