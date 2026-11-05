# 视频拼接策略技能

## 何时使用

在将多段视频片段组装为统一输出时应用本技能：
顺序叙事组装、多 take 剪辑、AI 生成片段链式拼接
（例如 LTX-2 单段最长约 8 秒），或并排对比、
画中画解说等空间布局。

## 工具

| 工具 | 作用 |
|------|------|
| `video_trimmer` | 按精确入/出点裁剪片段，拼接片段（`concat` 操作） |
| `video_compose` | 完整合成：叠加层、字幕、音频混音、空间布局 |
| `frame_sampler` | 在拼接边界采样帧，检查视觉连续性 |
| `audio_mixer` | 在拼接点混音、闪避与交叉淡化音频轨 |
| `scene_detect` | 在源素材中查找自然场景边界 |

## 何时拼接 — 决策树

```
Do you have multiple clips that need to become one video?
├── YES: Are they sequential (play one after another)?
│   ├── YES: Are they from the same shoot / same scene?
│   │   ├── YES → Multi-take assembly (pick best takes, stitch)
│   │   └── NO → Sequential narrative (match cuts, handle transitions)
│   └── NO: Do clips need to appear simultaneously on screen?
│       ├── YES → Spatial composition (side-by-side, PIP, stack)
│       └── MIXED → Hybrid (sequential with spatial inserts)
├── AI-generated clips (LTX-2, CogVideo)?
│   └── YES → AI clip chaining (handle 8s boundaries, maintain continuity)
└── NO → No stitching needed. Use video_trimmer for single-clip edits.
```

## 拼接策略

### 1. 顺序拼接

片段按时间线顺序依次播放。这是最常见的策略。

**何时：** 叙事视频、多章节讲解、剪辑 take 合集。

**流程：**
1. 按叙事顺序排列片段（勿按文件名）
2. 通过 `video_trimmer`（操作：`cut`）将每段裁到精确入/出点
3. 为每个接点选择转场类型（见下方「转场选择」）
4. 硬切用 `video_trimmer`（操作：`concat`）拼接；需滤镜的转场用 `video_compose`
5. 验证所有拼接点的音频连续性

**音频连续性规则：**
- 拼接前统一各片段电平（归一化至 -16 LUFS）
- 若背景音乐跨多段，通过 `audio_mixer` 混成单轨，拼接后再 mux
- 切勿在拼接点突然切断音乐 — 应交叉淡化或闪避

### 2. 空间拼接

多段视频同时出现在画面上。

**何时：** 反应、对比、解说、多角度覆盖。

| 布局 | FFmpeg 滤镜 | 用例 |
|--------|---------------|----------|
| 并排（duet） | `hstack` 或 `xstack` | 反应视频、前后对比 |
| 垂直堆叠 | `vstack` 或 `xstack` | 对比（上 vs 下） |
| 画中画（PIP） | `video_compose` 的 `overlay=x:y` | 解说、 webcam + 屏幕 |
| 网格（2x2、3x3） | 带 layout 字符串的 `xstack` | 多角度、合集 |

**空间布局决策树：**
```
What relationship do the clips have?
├── Reaction / response → Side-by-side (duet), main clip 70% width
├── Before / after → Side-by-side, equal 50/50 split
├── Comparison (A vs B) → Vertical stack or side-by-side depending on aspect ratio
├── Commentary over content → PIP, speaker in corner (20-25% frame size)
├── Multi-angle same event → Grid layout, synced to same timecode
└── Screen recording + face → PIP, face cam in bottom-right corner
```

**PIP 放置规则：**
- 默认位置：右下角，内边距 20px
- 尺寸：解说占画面宽度 20–25%，同等重要时 30–35%
- 确保 PIP 不遮挡关键内容（字幕、核心画面）
- 加 2px 描边或轻微阴影，与背景区分

### 3. AI 片段链式拼接（LTX-2 / CogVideo）

AI 视频生成器产出短片段（LTX-2：最长约 8 秒）。拼成更长序列需特别注意
保持视觉连续。

**流程：**
1. 生成时提示词重叠 — 片段 N 末帧描述应与片段 N+1 首帧描述一致
2. 用 `frame_sampler` 提取片段 N 末帧与片段 N+1 首帧
3. 目视检查是否断连（色偏、主体位置、背景变化）
4. 若不连续较轻微 → 用 0.5–1.0s 交叉淡化平滑接点
5. 若不连续较严重 → 插入经黑场淡入淡出（0.5s 出 + 0.5s 入）表示场景切换
6. 拼接后做全局调色，统一各段视觉调性

**AI 片段链式拼接陷阱：**
- AI 片段 FPS 可能不一致 — 拼接前将所有片段归一化为相同 FPS
- 各次生成色温常漂移 — 拼接后做一致调色
- 运动方向可能不匹配 — 检查末/首帧是否有突兀反向运动
- 音频（若有）不会连续 — 去掉 AI 音频，使用单一音乐/旁白轨

### 4. 混合拼接

顺序流中在特定时刻插入空间布局。

**何时：** 讲解在对比时切并排、教程演示时用 PIP、
纪录片偶发分屏等。

**流程：**
1. 规划时间线：标出哪些段为顺序、哪些为空间
2. 每段空间布局通过 `video_compose`（overlay 操作）单独渲染成成片
3. 将渲染好的空间片段当作普通片段参与顺序拼接
4. 按顺序拼接流程串联全部内容

## 转场选择

### 决策树

```
What is the relationship between clip N and clip N+1?
│
├── Same scene, continuous action?
│   └── HARD CUT (0ms)
│
├── Same topic, different angle or take?
│   └── HARD CUT (0ms) — use J-cut or L-cut for audio smoothing
│
├── Topic change or new section?
│   └── CROSSFADE (0.5-1.0s)
│
├── Time passage or mood shift?
│   └── CROSSFADE (1.0-1.5s)
│
├── Major section break (intro→body, body→outro)?
│   └── FADE THROUGH BLACK (0.5-1.0s)
│
├── Dialogue transition between speakers?
│   └── L-CUT or J-CUT (audio leads or trails by 0.3-0.5s)
│
└── AI clip boundary (LTX-2 chain)?
    ├── Continuity is good → HARD CUT or short CROSSFADE (0.3-0.5s)
    └── Continuity is broken → FADE THROUGH BLACK (0.5s)
```

### 转场参考

| 转场 | 时长 | 实现 | 适用 |
|-----------|----------|----------------|----------|
| 硬切 | 0ms | `video_trimmer` concat（codec: copy） | 同场景、快节奏、延续 |
| 交叉淡化 | 0.5-1.5s | `video_compose` 的 `xfade` 滤镜 | 换题、时间流逝、情绪转变 |
| 经黑场淡入淡出 | 各 0.5-1.0s | `video_compose`：淡出 → 黑 → 淡入 | 大段分界、片头片尾 |
| L-cut | 0.3-0.5s | 片段 N 的音频延续到片段 N+1 的画面 | 对话平滑结束、情绪余韵 |
| J-cut | 0.3-0.5s | 片段 N+1 的音频在片段 N 画面下提前进入 | 对话预告、蓄势 |

### 按内容节奏的转场时长

| 节奏 | 交叉淡化 | 经黑场淡入淡出 |
|--------|-----------|-------------------|
| 快（短视频，< 60s） | 0.3-0.5s | 0.3-0.5s |
| 中（1-10 min） | 0.5-1.0s | 0.5-0.8s |
| 慢（纪录片，> 10 min） | 1.0-1.5s | 0.8-1.0s |

## 音频协调

### 拼接点音频

```
What audio exists at the stitch boundary?
│
├── Both clips have narration/dialogue?
│   ├── Hard cut → Ensure no audio pop (cut at zero-crossing or apply 5ms fade)
│   ├── Crossfade → Duck outgoing audio -6dB during overlap, bring in incoming
│   └── L-cut/J-cut → Blend: outgoing audio fades -∞dB over 0.3-0.5s
│
├── Music spans the stitch?
│   ├── Same track continues → Do not re-encode audio; use stream copy
│   ├── Track changes → Crossfade music 1.0-2.0s centered on the cut point
│   └── Music + narration → Duck music -12dB under narration at all times
│
├── One clip has audio, the other is silent?
│   └── Add a 0.3s fade-in/fade-out to avoid abrupt silence transitions
│
└── No audio on either clip?
    └── No audio coordination needed. Add music/narration as a single track post-stitch.
```

### 音频电平目标

| 内容类型 | 目标 LUFS | 余量 |
|-------------|-------------|----------|
| 旁白 / 对话 | -16 LUFS | -1 dB true peak |
| 背景音乐（有旁白时） | -28 至 -24 LUFS | -1 dB true peak |
| 仅音乐（无旁白） | -14 LUFS | -1 dB true peak |
| 音效 | -20 LUFS | -1 dB true peak |

## 质量检查清单

在宣布拼接完成前，逐项确认：

- [ ] **分辨率一致：** 所有输入片段分辨率相同（或拼接前缩放一致）
- [ ] **FPS 一致：** 所有输入片段帧率相同（或用 `fps` 滤镜 conform）
- [ ] **宽高比一致：** 无混用 16:9 / 9:16 / 4:3，除非刻意空间布局
- [ ] **色彩一致：** 拼接边界无可见色温或曝光跳变
- [ ] **音频电平一致：** 拼接前各段归一化至目标 LUFS
- [ ] **无音频爆音或咔嗒：** 拼接点有微淡入淡出或在过零点切割
- [ ] **转场恰当：** 转场类型与内容关系匹配（见决策树）
- [ ] **总时长核对：** 成片时长与预期总和一致（计入转场重叠）
- [ ] **编码一致：** 各段同编码以便 stream copy；仅在必要时重编码
- [ ] **播放测试：** 在成片中逐段 scrub 每个拼接点，确认播放流畅

## 常见陷阱

### 编码不一致导致全盘重编码

**问题：** 混用不同编码的片段（如 H.264 + H.265）或不同编码参数，
会在 concat 时迫使 FFmpeg 全部重编码。

**解决方案：** 拼接前用 `ffprobe` 探测所有片段。若编码不同，将少数片段
重编码为与多数一致的编码。这比全盘重编码更快。

```
Check: ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate -of csv=p=0 input.mp4
```

### 长拼接中的音频漂移

**问题：** 拼接很多短片段（10+）时，微小时间误差累积，
导致末尾音频与画面不同步。

**解决方案：**
1. 拼接前以恒定帧率重编码每段（`-vsync cfr`）
2. 若使用独立音频轨，在拼接后按成片时长对齐
3. AI 片段链拼接时，concat 使用 `-async 1` 重同步音频

### 宽高比混用

**问题：** 将 16:9 与 9:16 拼接会产生黑边或拉伸。

**解决方案：** 事先确定目标宽高比。不合规片段用黑边填充（`pad` 滤镜）
或裁剪（`crop` 滤镜）— 切勿拉伸。

### 可变帧率（VFR）源

**问题：** 录屏与手机素材常用 VFR，与 CFR 内容拼接会导致
不同步与卡顿。

**解决方案：** 拼接前将 VFR 转为 CFR：
`ffmpeg -i vfr_input.mp4 -vsync cfr -r 30 cfr_output.mp4`

### Stream Copy 拼接失败

**问题：** `video_trimmer` 在 `codec: copy` 下 concat 失败或输出 glitch，
常因片段 GOP 结构或编码参数不同。

**解决方案：** 若 stream copy 失败，回退为统一参数重编码：
`-c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k`
使用 CRF 18（近无损）以减轻重编码画质损失。

## 拼接规划模板

规划拼接时，在 `edit_decisions` 中产出如下结构：

```yaml
stitch_plan:
  strategy: sequential | spatial | hybrid | ai_chain
  target_resolution: "1920x1080"
  target_fps: 30
  target_codec: libx264

  clips:
    - id: clip_01
      source: "assets/intro.mp4"
      in_seconds: 0.0
      out_seconds: 5.0
      transition_out: crossfade
      transition_duration: 0.8

    - id: clip_02
      source: "assets/section_1.mp4"
      in_seconds: 0.0
      out_seconds: 8.0
      transition_out: hard_cut

    - id: clip_03
      source: "assets/section_2.mp4"
      in_seconds: 0.0
      out_seconds: 8.0
      transition_out: fade_black
      transition_duration: 0.5

  audio:
    narration: "assets/narration_full.wav"
    music: "assets/bg_music.mp3"
    music_volume: -24  # LUFS
    ducking: true

  spatial_inserts:  # Only for hybrid strategy
    - at_clip: clip_02
      at_seconds: 3.0
      layout: pip
      overlay_source: "assets/webcam.mp4"
      position: bottom_right
      size_percent: 25
```
