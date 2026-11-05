# FFmpeg 技能

## 使用场景

对于不需要 AI 推理的视频/音频处理，使用基于 FFmpeg 的工具：
裁剪、修剪、调速、拼接、音频提取、混音、
字幕烧录、叠加合成、编码、人脸增强、调色、
以及音频清理。

## 使用 FFmpeg 的工具

### 核心流水线

| 工具 | 能力 |
|------|------|
| `video_trimmer` | 裁剪、修剪、调速、拼接视频片段 |
| `video_compose` | 完整合成：剪辑 + 字幕 + 叠加 + 编码 |
| `audio_mixer` | 混合语音/音乐/音效，侧链闪避，淡入淡出，提取音频 |
| `frame_sampler` | 从视频中提取代表性帧 |

### 增强层

| 工具 | 能力 | 关键预设 |
|------|-----------|-------------|
| `face_enhance` | 磨皮、锐化、暖/冷色调 | `talking_head_standard`, `soft_skin`, `sharpen` |
| `color_grade` | 电影感调色，强度可控 | `cinematic_warm`, `cinematic_cool`, `moody_dark` |
| `audio_enhance` | 降噪、响度归一化、均衡 | `clean_speech`, `voice_clarity`, `podcast` |

## 关键模式

### 增强链顺序

按以下顺序应用增强，以避免滤镜相互干扰：

1. **字幕优先** — 烧录到基础视频
2. **人脸增强** — 磨皮/锐化在未调色的素材上效果最好
3. **调色** — 在人脸已增强后再套用风格
4. **音频增强** — 与视频独立，最后应用

每一步均为可选；若工具不可用则自动跳过。

### 无损 vs 重编码

- 仅需裁剪或拼接、不改动画面时，使用 `-c copy`（编解码器拷贝）。即时且无损。
- 应用滤镜（变速、字幕、叠加、缩放）时需重编码（`-c:v libx264`）。
- 默认 CRF 为 23。若输出为最终交付物，可使用 18–20 以获得更高画质。

### 字幕烧录

- 简单逐词字幕优先使用 SRT 格式。
- 在 `force_style` 中使用完整 ASS 颜色格式：`&H00FFFFFF`（不要用 `&HFFFFFF`）。
- 在 subtitles 滤镜中务必转义 Windows 路径（`C\:` 而非 `C:`）。
- 竖屏视频：`font_size: 18`，`max 3 words/cue`，`margin_v: 50`。
- 横屏视频：`font_size: 22`，`max 6 words/cue`，`margin_v: 40`。

### 音频增强目标

| 平台 | 目标 LUFS | 响度范围 |
|----------|-------------|----------------|
| 社交媒体（TikTok、Reels） | -14 LUFS | 5–7 LU |
| YouTube | -14 至 -16 LUFS | 7–11 LU |
| 播客 | -16 LUFS | 7–11 LU |
| 广播电视 | -24 LUFS | 7 LU |

`clean_speech` 预设目标为 -16 LUFS、11 LU 范围 — 适用于 YouTube/社交媒体。

### 调色强度

- `intensity: 0.85` — 口播场景下 `cinematic_warm` 的推荐默认值
- `intensity: 0.5` — 轻微，几乎察觉不到
- `intensity: 1.0` — 完整效果，部分素材可能显得过度处理

### 音频闪避（Ducking）

- 使用 `sidechaincompress`，以语音为 sidechain 信号，在对话时降低音乐音量。
- 典型参数：threshold=0.02，ratio=9，attack=200ms，release=500ms。

### 拼接

- 相同编解码器的片段使用 concat demuxer（`-f concat -safe 0`）。
- 编解码器或分辨率不一致时，先统一重编码所有片段。

## 质量检查清单

- [ ] 输出在桌面和移动端播放无伪影
- [ ] 处理后音画同步
- [ ] 字幕位于画面下方 20% 区域，不遮挡人脸
- [ ] 音频响度在目标平台规定范围内
- [ ] 增强效果可见但自然 — 肤色健康，不偏橙
- [ ] 切点处无音频削波或静音间隙
- [ ] 文件大小适合目标平台
