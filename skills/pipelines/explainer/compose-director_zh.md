# Compose Director — Explainer 流水线

## 何时使用

你是生成式解说视频的合成师（Compositor）。你拥有包含完整剪辑时间线的 `edit_decisions`，以及包含所有文件路径的 `asset_manifest`。你的任务是渲染最终视频：组装画面、叠加音频、烧录字幕，并编码为目标格式。

这是视频成为可播放文件前的最后一个技术阶段。一切在此汇聚。

## 运行时路由（强制第一步）

在做任何其他事之前，先读取 `edit_decisions.render_runtime`。它在提案阶段已锁定，不得静默更改。本技能后续流程步骤（Remotion public/  staging、词级字幕烧录等）假定 `render_runtime="remotion"` —— 数据驱动解说片的默认选项。

- **`render_runtime="hyperframes"`** — HTML/CSS/GSAP 渲染。不要执行下文 Remotion 专用步骤。改为：阅读 `skills/core/hyperframes.md`、`.agents/skills/hyperframes/SKILL.md` 与 `.agents/skills/hyperframes-cli/SKILL.md`。原样调用 `video_compose` 并传入 `edit_decisions` —— 它将委托给 `hyperframes_compose`，在 `projects/<name>/hyperframes/` 下物化工作区，执行 `lint → validate → render` 并返回 MP4。渲染前 lint 与 validate 均须通过；迭代时可暂缓对比度检查，但最终交付不可省略。
- **`render_runtime="ffmpeg"`** — 简单拼接/裁剪。直接调用 `video_compose`；当运行时显式锁定为 ffmpeg 时，不会自动升级到 Remotion。
- **运行时不可用** — 按 AGENT_GUIDE.md >「明确升级阻塞项」 surfaced 阻塞，并在切换前获得用户批准（在 decision_log 中记录为 `render_runtime_selection` 决策）。

`final_review.checks.promise_preservation.render_runtime_used` 必须等于实际运行的运行时；除非有已批准决策授权切换，否则 `runtime_swap_detected` 必须为 `false`。

**向 `video_compose.execute()` 传入 `proposal_packet`**，以便工具内切换检测能真正触发。未传入时 `runtime_swap_check` 会报告为 `skipped`，你只能依赖 reviewer 技能的跨制品比对。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 制品校验 |
| 前置制品 | `state.artifacts["edit"]["edit_decisions"]`、`state.artifacts["assets"]["asset_manifest"]` | 渲染内容 |
| Playbook | 当前 style playbook | 质量目标 |
| 工具 | `video_compose`、`audio_mixer` | 渲染能力 |
| Media profiles | `lib/media_profiles.py` | 输出格式规格（分辨率、编解码器、码率） |

## 流程

### 步骤 1：选择渲染策略

根据剪辑决策选择渲染方式：

**Remotion 渲染**（默认 —— 除非显式覆盖，否则使用此项）：
- 动画文字卡、数据卡、图表场景
- 复杂转场（morph、zoom、ken-burns）
- 程序化动态图形
- 音频嵌入（旁白 + 音乐，含淡入淡出/音量）
- 通过 CaptionOverlay 组件实现词级字幕
- 最适用于：所有解说视频，无论以图为主还是动画为主

**FFmpeg 流水线**（回退 —— 仅当 Remotion 不可用时）：
- 静态图 + Ken Burns
- 音频叠加
- SRT 字幕烧录
- 最适用于：未安装 Node.js/Remotion 的环境

**重要：使用 Remotion 时，以下全部走 Remotion —— 而非 FFmpeg：**
- 音频（旁白 + 音乐）→ Remotion `audio` prop，不要用外部 `audio_mixer`
- 字幕 → Remotion `captions` prop（词级），不要用 FFmpeg 烧 SRT
- 文字叠加（CTA、标题）→ Remotion `text_card` 切类型，不要用 AI 生成图

### 步骤 2：音频获取（旁白、音乐、字幕）

渲染前向用户展示音频选项并确认偏好。

**向用户展示：**

> **本视频的音频设置：**
>
> **旁白：** 我可用 OpenAI TTS 生成旁白（`gpt-4o-mini-tts` —— $0.015/分钟，6 种音色，支持 voice direction）。你希望哪种音色与语气？我会根据视频主题推荐，或由你自选：
> - `onyx` — 低沉、权威（纪录片、科技）
> - `echo` — 共鸣、未来感（产品广告、科幻）
> - `nova` — 明亮、有活力（ upbeat、解说）
> - `fable` — 温暖、叙事（故事、教育）
> - `shimmer` — 富有表现力、温暖（有机、生活方式）
> - `alloy` — 中性、均衡（通用）
>
> **音乐：** 我可从 Pixabay 自动查找免版税背景音乐（无需 key）。若配置了 `FREESOUND_API_KEY`，也可从 Freesound 搜索作为备选。
>
> **字幕：** 我将对最终旁白用 WhisperX 转写生成词级字幕，并通过 Remotion captions 烧入视频。
>
> 是否按我的推荐继续，还是需要调整？

**用户确认后：**

1. **撰写带时长预算的旁白稿**（见 scene-director 步骤 4b）：
   - 根据 cuts 计算视频时长
   - 预算为视频时长的 85–90%
   - 纪录片约 2.0–2.5 词/秒， energetic 约 2.5–3.0 词/秒
   - 生成 TTS 前核对词数

2. **生成 TTS 旁白：**
   ```python
   from tools.audio.openai_tts import OpenAITTS
   result = OpenAITTS().execute({
       'text': narration_script,
       'voice': '<user-chosen or agent-recommended>',
       'instructions': '<voice direction matching video tone>',
       'output_path': 'path/to/narration.mp3',
   })
   # CRITICAL: Check result.data['audio_duration_seconds'] vs video duration
   # If narration exceeds video by >1s: shorten script and regenerate
   ```

3. **下载背景音乐：**
   ```python
   from tools.audio.pixabay_music import PixabayMusic
   result = PixabayMusic().execute({
       'query': '<mood/genre matching video topic>',
       'min_duration': video_duration_seconds,
       'max_duration': 300,
       'output_path': 'path/to/music.mp3',
   })
   ```

4. **通过 WhisperX 生成字幕：**
   ```python
   from tools.analysis.transcriber import Transcriber
   result = Transcriber().execute({
       'input_path': 'path/to/narration.mp3',
       'model_size': 'base',
       'language': 'en',
   })
   # Convert word_timestamps to Remotion caption format:
   # [{ "word": "Hello", "startMs": 0, "endMs": 340 }, ...]
   ```

5. **组装含音频配置的 composition JSON：**
   ```json
   {
     "audio": {
       "narration": { "src": "path/to/narration.mp3", "volume": 1 },
       "music": { "src": "path/to/music.mp3", "volume": 0.1, "fadeInSeconds": 2, "fadeOutSeconds": 3 }
     },
     "captions": [ ... word-level captions from WhisperX ... ]
   }
   ```

### 步骤 3：准备渲染输入

对剪辑决策中的每个 cut：
1. 确认源资源在声明路径存在
2. 检查资源尺寸/时长符合预期
3. 准备变换参数（scale、position、crop）

对音频：
1. 确认旁白时长不超过视频时长（使用 `audio_probe`）
2. 确认音乐时长覆盖视频时长
3. 按剪辑决策准备 ducking 参数

### 步骤 3：确定输出 Profile

从 brief 制品读取目标平台。映射到 media profile：

| 平台 | Profile | 分辨率 | 说明 |
|----------|---------|-----------|-------|
| YouTube | `youtube_landscape` | 1920x1080 | 多数解说片默认 |
| TikTok/Reels | `tiktok` | 1080x1920 | 竖屏，需重新构图 |
| Twitter/X | `twitter_landscape` | 1280x720 | 较短格式 |
| LinkedIn | `linkedin` | 1920x1080 | 专业场景 |

通过 `ffmpeg_output_args(get_profile(name))` 获取精确编码参数。

### 步骤 4：渲染视频

调用 `video_compose` 工具：
```
{
  "operation": "render",
  "edit_decisions": <edit_decisions artifact>,
  "asset_manifest": <asset_manifest artifact>,
  "output_profile": "youtube_landscape",
  "output_path": "renders/output.mp4",
  "options": {
    "subtitle_burn": true,
    "audio_normalize": true,
    "two_pass_encode": true
  }
}
```

若对动画片段使用 Remotion：
1. 从剪辑决策生成 Remotion composition 数据
2. 对动画片段调用 `video_compose`，`operation: "remotion_render"`
3. 用 FFmpeg 将 Remotion 输出与其余片段组装

**零 key Remotion 渲染（纯组件视频）：**
当所有场景均为 Remotion 组件类型（hero_title、stat_card、bar_chart、line_chart、
pie_chart、kpi_grid、comparison、callout、progress_bar、text_card）时，使用 Explainer 入口将整个视频渲染为单一 Remotion composition。无需 FFmpeg 组装。
`edit_decisions` 的 cuts 数组直接映射为 Remotion props。见 `skills/core/remotion.md`
中的成熟公式 —— 尤其深色主题下全暗背景的视觉一致性规则。

### 步骤 5：音频后处理

**Remotion 路径（默认）：** 完全跳过外部混音。Remotion 通过 `<Audio>` 组件原生处理全部音频。在 composition props 中传入音频源：
```json
{
  "audio": {
    "narration": { "src": "project/narration.mp3", "volume": 1.0 },
    "music": { "src": "project/music.mp3", "volume": 0.12, "fadeInSeconds": 1.5, "fadeOutSeconds": 2.5 }
  }
}
```
Remotion 单次 pass 渲染音视频 —— 无需外部 mux。
经 Remotion 渲染时，不要用 `audio_mixer` 做 ducking/混音。

**FFmpeg 回退（仅当 Remotion 不可用时）：**
调用 `audio_mixer` 工具：
1. 按序叠加旁白片段
2. 按 playbook 音量混入背景音乐
3. 应用 ducking（旁白时段压低音乐）
4. 归一化整体电平
5. 输出最终混音轨
`video_compose` 会将其与视频 mux。

### 步骤 5b：生成字幕（强制）

所有解说内容必须带字幕。从旁白音频生成 —— 不可跳过。

**Remotion 路径（默认 —— 使用 Remotion 渲染时）：**

1. **转写** 完整旁白，使用 `transcriber` 工具（whisperx）：
   ```python
   from tools.analysis.transcriber import Transcriber
   result = Transcriber().execute({
       'input_path': 'projects/<project>/assets/audio/narration_full.mp3',
       'model_size': 'base',
       'language': 'en',
       'output_dir': 'projects/<project>/assets/audio'
   })
   # result.data contains segments with word-level timestamps
   ```

2. **转换为 Remotion WordCaption 格式**（非 SRT）：
   ```python
   captions = []
   for segment in result.data['segments']:
       for word_info in segment.get('words', []):
           captions.append({
               'word': word_info['word'],
               'startMs': int(word_info['start'] * 1000),
               'endMs': int(word_info['end'] * 1000),
           })
   ```

3. **将 captions 加入 composition props** —— 与 `cuts`、`audio` 并列放在 `captions` 数组：
   ```json
   {
     "cuts": [...],
     "audio": {...},
     "captions": [
       { "word": "Root", "startMs": 120, "endMs": 340 },
       { "word": "canals", "startMs": 340, "endMs": 680 }
     ]
   }
   ```

   Remotion 的 CaptionOverlay 以主题 `captionHighlightColor` 与 `captionBackgroundColor` 逐词高亮字幕，优于 FFmpeg SRT 烧录，因与旁白同步的动画词级高亮。

**FFmpeg 回退（仅当 Remotion 不可用时）：**

若 Remotion 不可用，回退为 SRT 生成 + FFmpeg 烧录：
   ```python
   from tools.subtitle.subtitle_gen import SubtitleGen
   SubtitleGen().execute({
       'segments': transcription_data['segments'],
       'format': 'srt',
       'output_path': 'projects/<project>/assets/subtitles.srt',
       'max_words_per_cue': 8,
       'max_chars_per_line': 42
   })
   # Then burn with video_compose operation='burn_subtitles'
   ```

**最终交付物必须含字幕** —— 经 Remotion captions 或 FFmpeg 烧录均可。

### 步骤 5c：渲染前校验（强制）

**渲染前务必运行 composition validator。** 可捕获浪费渲染时间的问题。

```python
from tools.analysis.composition_validator import CompositionValidator
result = CompositionValidator().execute({
    'composition_path': 'path/to/composition.json',
    'assets_root': 'remotion-composer/public',
})
# result.data['valid'] MUST be True before proceeding to render
# If False: fix the reported errors first (missing assets, audio-video mismatch, etc.)
```

常见捕获项：
- 旁白长于视频（会被截断）
- 缺失图片/音频文件（渲染会失败）
- 音乐短于视频（结尾静音）

**不可跳过。** 校验失败则修复并重新校验后再渲染。

### 步骤 6：渲染后自检（强制 —— 须完成全部步骤）

渲染后，代理**必须**在向用户展示前审查自己的输出。可发现 validator 看不到的问题（画面质量、音画同步、字幕可读性）。

**关键：必须完成 6a 至 6e 全部步骤。不可跳过任一步。
最常见失败是只做 6a（帧）和 6c（视觉）而跳过 6b（音频转写）—— 会漏掉整段缺失音频等严重问题。**

**6a. 探测渲染文件（首先 —— 后续检查的门槛）：**
```bash
ffprobe -v quiet -print_format json -show_format -show_streams rendered_video.mp4
```
验证：
- 存在视频流（codec_type: "video"）且分辨率正确
- **存在音频流（codec_type: "audio"）** —— 若无音频流，立即停止并修复
- 时长在目标 ±5% 内
- 文件大小合理（非 0 字节）

**若缺少音频流：渲染未嵌入音频。不要向用户展示该视频。修复音频配置并重新渲染。**

**6b. 提取审查帧：**
```python
from tools.analysis.frame_sampler import FrameSampler
midpoints = [(cut['in_seconds'] + cut['out_seconds']) / 2 for cut in cuts]
FrameSampler().execute({
    'input_path': 'path/to/rendered_video.mp4',
    'strategy': 'timestamps',
    'timestamps': midpoints,
    'output_dir': 'path/to/review-frames',
    'format': 'png',
})
```

**6c. 转写渲染后音频（强制 —— 不可跳过）：**
```python
from tools.analysis.transcriber import Transcriber
result = Transcriber().execute({
    'input_path': 'path/to/rendered_video.mp4',
    'model_size': 'base',
    'language': 'en',
    'output_dir': 'path/to/review-frames',
})
# If result returns 0 words: audio is silent/missing — STOP and fix
# If word count < 80% of script word count: audio is cut off — investigate
```

**6d. 视觉检查 —— 逐帧审查：**
- 背景色/渐变是否符合意图？（深色主题视频避免出现白底）
- 图片是否正确渲染？（非空白、非拉伸）
- 字幕/caption 是否可见且间距合理？
- 叠加层（章节标题、数据揭示）位置是否正确？
- 开场画面是否足够强？（社交媒体缩略图重要）
- CTA/结尾屏文字是否正确？（AI 生成图内文字常 hallucinate —— 需精确的文字用 Remotion text_card）

**6e. 音频检查 —— 将转写与稿本比对：**
- 旁白是否完整？（最后转写词 vs 稿本最后词）
- 结尾是否有词被截断？（旁白超出视频时长）
- 时间对齐 —— 旁白段落是否大致对应 intended 场景？
- 背景音乐是否可闻？（转写器可能录不到音乐，但 ffprobe 可确认音频流）

**6f. 汇总并向用户展示审查：**

> **「[视频标题]」渲染后审查：**
>
> **文件：** [duration]s，[resolution]，[file size] —— 音频流：[present/MISSING]
> **音频：** [Complete/Cut off at Xs] —— 从渲染输出转写 [N]/[M] 词
> **画面：** [N scenes inspected] —— [issues 或「all scenes rendering correctly」]
> **字幕：** [Remotion CaptionOverlay / FFmpeg SRT / MISSING] —— [词级高亮正常 / 问题]
> **发现问题：** [列出问题及严重程度]
>
> **建议：** [需修复项，若有]
>
> 需要我修复并重新渲染，还是可以直接交付？

**仅在用户批准（或代理未发现任何问题）后，视频才可视为定稿。**

### 步骤 6-old：文件与内容验证

**文件验证：**
- [ ] 输出文件存在于声明路径
- [ ] 文件大小合理（非 0 字节、非异常偏小）
- [ ] 容器有效（ffprobe 成功）

**内容验证：**
- [ ] 时长在目标 ±5% 内
- [ ] 分辨率匹配所选 profile
- [ ] 存在音频声道（立体声）
- [ ] 无 clipping 或 >1s 静音间隙

**质量检查（由上文的自检覆盖）：**
- [ ] 视觉：已检查所有场景帧
- [ ] 音频：已验证完整转写
- [ ] 字幕：可见且时间正确

### 步骤 7：构建 Render Report

```json
{
  "version": "1.0",
  "outputs": [
    {
      "path": "renders/output.mp4",
      "format": "mp4",
      "codec": "h264",
      "resolution": "1920x1080",
      "fps": 30,
      "duration_seconds": 62.4,
      "file_size_mb": 45.2,
      "audio_codec": "aac",
      "audio_channels": 2,
      "render_strategy": "ffmpeg",
      "render_time_seconds": 180
    }
  ],
  "render_summary": {
    "total_cuts_rendered": 12,
    "subtitles_burned": true,
    "audio_tracks_mixed": 3,
    "target_duration_seconds": 60,
    "actual_duration_seconds": 62.4
  }
}
```

### 步骤 8：自评

打分（1–5）：

| 维度 | 问题 |
|-----------|----------|
| **Playability** | 视频在标准播放器中能否无错播放？ |
| **Duration accuracy** | 实际时长是否在目标 ±5% 内？ |
| **Audio quality** | 旁白是否清晰、音乐是否平衡、有无 clipping？ |
| **Visual quality** | 图像是否锐利、转场是否顺滑、有无伪影？ |
| **Subtitle accuracy** | 字幕是否存在、可读且同步？ |

任一维度低于 3 分则调查并重新渲染。

### 步骤 9：提交

对照 schema 校验 render_report，并通过 checkpoint 持久化。

## 常见陷阱

- **缺失资源文件**：渲染开始前务必确认每个引用文件存在。渲染中途缺文件会浪费时间。
- **音频同步漂移**：旁白片段累积计时误差会导致音画不同步。使用绝对时间戳，而非相对偏移。
- **字幕编码**：为最大兼容性将字幕烧入视频（硬字幕）。社交媒体不要依赖软字幕。
- **单 pass 编码**：双 pass 在相同文件大小下质量更好，值得额外渲染时间。
- **忽略 media profile**：YouTube 与 TikTok 要求差异很大。务必核对目标 profile。
