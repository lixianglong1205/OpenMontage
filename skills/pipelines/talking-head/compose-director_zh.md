# 合成导演 — 口播视频流水线

## 何时使用

你已有剪辑决策与资产清单。你的任务是渲染最终口播视频：应用增强链、烧录字幕、混音，并按目标配置编码。

## 运行时路由（硬性约束 — 仅 Remotion 或 FFmpeg）

阶段 1 已从 HyperFrames 延期。`edit_decisions.render_runtime` 必须为 `"remotion"`（首选 — 使用 `TalkingHead` 合成 + `remotion_caption_burn`）或 `"ffmpeg"`（用于无合成的源素材拼接）。

- 若 `edit_decisions.render_runtime == "hyperframes"`，则停止。重新打开创意阶段并说明该约束。静默改写属于治理违规。
- 按 AGENT_GUIDE.md →「同时呈现两种合成运行时（硬性规则）」：流水线约束不能跳过对话。向用户说明 HyperFrames 存在但在本场景不可行。记录 `render_runtime_selection` 决策，其中 hyperframes 的 `rejected_because: "TalkingHead + caption parity deferred on talking-head"`。
- 将 `proposal_packet`/`brief` 传给 `video_compose.execute()` 以进行运行时切换检测。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 产物校验 |
| 前置产物 | 剪辑决策、资产清单 | 渲染输入 |
| 工具 | `video_compose`、`audio_mixer` | 渲染 |
| 媒体配置 | `lib/media_profiles.py` | 输出格式 |

## 流程

### 步骤 0：预检

在渲染任何内容之前，校验输入并捕获后续修复成本较高的问题。

1. **静音检测** — 以 mark 模式运行 `silence_cutter`：
   ```
   silence_cutter.execute({
       "input_path": "<raw_footage>",
       "mode": "mark",
       "silence_threshold_db": -35,
       "min_silence_duration": 0.5
   })
   ```
   - 报告所有 > 0.5s 的间隙及时间戳。
   - 若总静音 > 5s，**建议在继续前剪辑**。过长静音浪费渲染时间并在成片中产生空白段。

2. **ASR 置信度检查** — 扫描词级转写中的低置信词：
   - 标记概率 < 0.7 的词。
   - 列出带时间戳的标记词，供用户核对转写是否正确。
   - 常见误识别：专有名词、品牌名、领域术语。

3. **从常见 ASR 错误模式自动构建 corrections 字典**：
   ```python
   corrections = {
       # Indian finance context
       "DMI": "EMI",
       "AMI": "EMI",
       # Common brand misspellings
       "open montage": "OpenMontage",
       "remotion": "Remotion",
       # Numbers that got split by ASR
       "4 -5": "4-5",
       "10 -15": "10-15",
   }
   ```
   根据视频主题用领域相关修正扩展该字典。应用前将 corrections 呈现给用户审阅。

4. **绿幕标记** — 检查 scene-director 步骤 0 是否标记了绿/蓝幕素材。若是，注明需要步骤 3c（绿幕合成）。

### 步骤 1：运行增强链

按此确切顺序应用视频增强。**若工具可用则尝试每一步** — 无理由不得跳过。

1. **面部增强** — 应用 `talking_head_standard` 预设
2. **眼部增强** — 去黑眼圈 + 提亮眼睛
3. **调色** — 应用配置
4. **音频增强** — 降噪、归一化

**眼部增强** — 在 face_enhance 之后始终尝试。对 webcam/手机素材视觉差异明显：
```
eye_enhance.execute({
    "input_path": "<face_enhanced_video>",
    "output_path": "<project>/assets/video/eye_enhanced.mp4",
    "operations": ["dark_circles", "brighten_eyes"],
    "dark_circle_intensity": 0.4,       # 0-1, subtle is better
    "eye_brighten_intensity": 0.3,
})
```
**重要：** 强度保持较低（0.2–0.5）。过度处理会使眼睛不自然。若工具失败（如未安装 MediaPipe），记录回退并继续使用 face_enhanced 视频。

### 步骤 1b：变速（若用户要求）

若用户希望加速或减速，使用 `video_trimmer`：
```
video_trimmer.execute({
    "operation": "speed",
    "input_path": "<enhanced_video>",
    "output_path": "<project>/assets/video/speed_adjusted.mp4",
    "speed_factor": 1.25    # 0.5x (slow), 1.25x, 1.5x, 2x (fast)
})
```

常用速度系数：
| 系数 | 用途 |
|--------|----------|
| `0.5` | 慢动作，戏剧效果 |
| `1.0` | 正常（不变） |
| `1.25` | 略快 — 节奏更紧且听感仍自然 |
| `1.5` | 明显更快 — 适合回顾或浓缩内容 |
| `2.0` | 双倍速 — 延时效果 |

变速在增强之后、重构图之前应用。

### 步骤 2：自动重构图（若目标平台需要）

若目标平台需要不同宽高比（如 Instagram Reels = 9:16），使用 `auto_reframe`：

```
auto_reframe.execute({
    "input_path": "<enhanced_video>",
    "output_path": "<project>/renders/reframed.mp4",
    "target_aspect": "portrait",       # 9:16 for Reels/TikTok/Shorts
    "smoothing_window": 15,            # smooth camera pan
    "face_padding": 0.4,              # 40% padding around face
})
```

**宽高比预设：**
| 预设 | 比例 | 平台 |
|--------|-------|----------|
| `portrait` | 9:16 | Instagram Reels、TikTok、YouTube Shorts |
| `square` | 1:1 | Instagram Feed |
| `landscape` | 16:9 | YouTube、LinkedIn |
| `vertical_4_5` | 4:5 | Instagram 竖版帖子 |

工具自动做人脸检测并保持讲者居中。若未安装 MediaPipe，回退为中心裁剪。

**重要：** 在 face_enhance 与 color_grade 之后、烧录字幕之前运行 auto_reframe。字幕需按最终宽高比定位。

### 步骤 2b：构建 ASR corrections 字典

烧录字幕前，扫描转写中可能的 ASR 误识别。常见问题：
- 产品/品牌名："cloud" → "Claude"，"co-pilot" → "Copilot"，"remotion" → "Remotion"
- 技术术语："pythonic" 听成 "pathonic"，"API" 听成 "a pie"
- 讲者姓名或公司名
- 领域专用术语

构建 corrections 字典：
```python
corrections = {
    "cloud": "Claude",
    "co pilot": "Copilot",
    "open montage": "OpenMontage",
}
```

将该字典同时传给 `subtitle_gen`（若生成 SRT）与 `remotion_caption_burn`（若用 Remotion 字幕）。即使无需修正，也显式传入空字典 `{}` 以表明已检查。

### 步骤 3：烧录字幕

**始终使用 Remotion TikTok 风格字幕**（逐词高亮）。这是默认且首选方式。除非 Remotion 完全不可用，否则**不要**回退到 FFmpeg ASS 字幕。

**Remotion 字幕要求：**
- **自动检测视频尺寸** — 不要硬编码 width/height。用 `visual_qa` probe 或 ffprobe 获取实际尺寸，再传入渲染。
- **按实际视频时长设置 `--frames`** — 由 probe 计算：`frames = duration_seconds * fps`。勿使用硬编码帧数。
- 逐词高亮，激活词颜色为 `highlight_color`。
- 字幕位于画面底部，远离面部。

```
remotion_caption_burn.execute({
    "input_path": "<reframed_or_enhanced_video>",
    "output_path": "<project>/assets/video/captioned.mp4",
    "segments": <transcript_segments_from_asset_manifest>,
    "corrections": {"cloud": "Claude", "co-pilot": "Copilot"},
    "words_per_page": 4,
    "font_size": 52,
    "highlight_color": "<theme_accent>",
})
```

**仅当 Remotion 完全不可用时的回退：** 使用 `video_compose` 的 `burn_subtitles` 操作。体验降级 — 警告用户无法使用逐词高亮。

**关键：9:16 竖版视频的字幕位置（仅 FFmpeg 回退）。**
字幕必须在画面下方 20% 区域内。1920 高帧上即 `MarginV=160` 或更大。FFmpeg 默认字幕位置在居中 — **会遮挡面部**。必须覆盖。

竖版口播 FFmpeg 字幕样式字符串：
```
"FontName=Arial,FontSize=22,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=0,MarginV=160,Alignment=2"
```

**切勿**使用默认字幕位置。**切勿**将字幕放在画面中部或上半部分。若 visual QA 发现字幕在脸上，必须用修正后的位置重新渲染。

### 步骤 3b：烧录叠加图形（若场景计划含 overlay）

若场景计划含 overlay 场景（text_cards、stat_cards、charts、comparisons、callouts），与字幕一并传给 `remotion_caption_burn`。**字幕与 overlay 在单次 Remotion  pass 中渲染** — 无需单独 FFmpeg 合成。

**原理：** TalkingHead Remotion 合成渲染三层：
1. **Video**（底层）— 口播素材
2. **Overlays**（中层）— 定位的图表、数据、标注，带淡入淡出
3. **Captions**（顶层）— 逐词高亮，始终可见

**将步骤 3 与 3b 合并为一次 `remotion_caption_burn` 调用：**
```
remotion_caption_burn.execute({
    "input_path": "<reframed_or_enhanced_video>",
    "output_path": "<project>/assets/video/captioned.mp4",
    "segments": <transcript_segments>,
    "corrections": {"cloud": "Claude"},
    "words_per_page": 4,
    "font_size": 52,
    "highlight_color": "<theme_accent>",
    "overlays": [
        {
            "id": "term-agentic-ai",
            "type": "callout",
            "text": "Agentic AI: software that acts autonomously toward goals",
            "callout_type": "info",
            "in_seconds": 22.0,
            "out_seconds": 26.0,
            "position": "lower_third",
            "backgroundColor": "<theme_background>",
            "accentColor": "<theme_accent>"
        },
        {
            "id": "stat-market-size",
            "type": "stat_card",
            "stat": "$4.8B",
            "subtitle": "Global AI Agent Market (2026)",
            "in_seconds": 35.0,
            "out_seconds": 39.0,
            "position": "upper_third",
            "accentColor": "<theme_secondary_accent>"
        },
        {
            "id": "chart-growth",
            "type": "bar_chart",
            "chartData": [
                {"label": "2023", "value": 1.2},
                {"label": "2024", "value": 2.1},
                {"label": "2025", "value": 3.5},
                {"label": "2026", "value": 4.8}
            ],
            "title": "AI Agent Market ($B)",
            "in_seconds": 40.0,
            "out_seconds": 45.0,
            "position": "lower_third",
            "chartColors": ["<theme_accent>", "<theme_secondary_accent>", "<theme_tertiary_accent>", "<theme_supporting_accent>"]
        }
    ]
})
```

**Overlay 位置选项：**
- `lower_third` → 底部区域，字幕上方（默认 — 多数 overlay 最安全）
- `upper_third` → 顶部区域（讲者居中/偏下时适合数据卡）
- `left_panel` → 画面左侧 45%（与讲者并排）
- `right_panel` → 画面右侧 45%
- `full_overlay` → 全帧暗色底（慎用，最多 1–2s）

**Overlay 类型 → 必填属性**（与 asset-director 映射相同）：

| 类型 | 必填属性 |
|------|---------------|
| `text_card` | `text` |
| `stat_card` | `stat`、`subtitle`（可选） |
| `callout` | `text`、`callout_type`（info/warning/tip/quote） |
| `comparison` | `leftLabel`、`rightLabel`、`leftValue`、`rightValue` |
| `bar_chart` | `chartData`（`{label, value}` 数组） |
| `line_chart` | `chartSeries`（`{name, data: number[]}` 数组） |
| `pie_chart` | `chartData`（`{label, value}` 数组） |
| `kpi_grid` | `chartData`（`{label, value}` 数组） |
| `hero_title` | `text`、`subtitle`（可选） |
| `section_title` | `text`、`subtitle`（可选） |
| `stat_reveal` | `text`（数值）、`subtitle`（标签） |

**重要：** 变速后重新计算 overlay 时间戳：`adjusted_time = original_time / speed_factor`。

**回退（无 Remotion）：** 若 Remotion 不可用，`remotion_caption_burn` 仅对字幕回退到 FFmpeg。FFmpeg 回退模式**不**渲染 overlay — 警告用户 overlay 需要 Remotion。

### 步骤 3c：绿幕合成（若为绿幕素材）

若素材为绿/蓝幕（在 scene-director 步骤 0 检测），按此流水线：

1. **运行 `green_screen_processor` 工具** 去除绿/蓝幕：
   ```
   green_screen_processor.execute({
       "input_path": "<enhanced_video>",
       "output_path": "<project>/assets/video/greenscreen_removed.mp4",
       "method": "auto"
   })
   ```
   `auto` 方法检测背景为绿或蓝并应用相应 chroma key。

2. **用 Explainer 合成渲染 Remotion 动画背景**：
   ```
   # Render an AnimatedBackground clip (gradient mesh, floating orbs, subtle grid)
   # Use the Explainer composition — NOT a flat #0F172A solid color
   npx remotion render src/index.ts Explainer --props='{"duration":VIDEO_DURATION}' --output=<project>/assets/video/animated_bg.mp4
   ```
   AnimatedBackground 提供专业渐变网格、浮动光球与 subtle 网格。远优于纯色 #0F172A。

3. **运行 `green_screen_composite` 工具** 将讲者叠到动画背景上：
   ```
   green_screen_composite.execute({
       "foreground_path": "<greenscreen_removed_video>",
       "background_path": "<animated_bg>",
       "output_path": "<project>/assets/video/composited.mp4",
       "layout": "news_anchor"
   })
   ```
   默认 layout 为 `news_anchor`（讲者中下居中，背景铺满）。按步骤 0 检测到的讲者位置调整 layout。

4. **通过 Remotion TalkingHead 合成烧录字幕**（**非** FFmpeg ASS 字幕）：
   ```
   remotion_caption_burn.execute({
       "input_path": "<composited_video>",
       "output_path": "<project>/assets/video/captioned.mp4",
       "segments": <transcript_segments>,
       "corrections": <corrections_dict>,
       "words_per_page": 4,
       "font_size": 52,
        "highlight_color": "<theme_accent>",
       "overlays": <overlay_list_from_scene_plan>
   })
   ```

5. **混入背景音乐**（语音下 duck 至 15% 音量）：
   ```
   audio_mixer.execute({
       "operation": "duck",
       "video_path": "<captioned_video>",
       "music_path": "<bg_music>",
       "music_volume": 0.15,
       "output_path": "<project>/assets/video/with_music.mp4"
   })
   ```

6. **最终编码** 至目标平台规格（见下方步骤 6）。

### 步骤 3d：构建 Showcase 卡片（若为多片段 reel）

若输出为含 showcase 片段的 reel，对每个使用 `showcase_card`：
```
showcase_card.execute({
    "input_path": "<showcase_video>",
    "output_path": "<project>/assets/video/sc_<name>.mp4",
    "title": "VIDEO TITLE",
    "subtitle": "Description | Style | Cost: $0.15",
    "background_color": "0x0A0F1A",
})
```
生成带排版的 9:16 信箱模式卡片。

### 步骤 4：组装多片段（若适用）

若输出有多段（如口播 + showcase），使用 `video_stitch`：
```
video_stitch.execute({
    "operation": "stitch",
    "clips": ["intro.mp4", "showcase1.mp4", ..., "outro.mp4"],
    "output_path": "<project>/renders/assembled.mp4",
    "transition": "crossfade",         # or "fade" for fade-through-black
    "transition_duration": 0.5,
})
```
**转场指引：**
- `crossfade`（fade）：口播与 showcase 之间平滑混合
- `fade`（fade-through-black）：showcase 之间短暂黑场
- 混合转场类型：talk→showcase 用 `crossfade`，showcase 之间用 `fade`

### 步骤 5：混音

使用 `audio_mixer` 叠加背景音乐：

**多片段 reel** — 用 `segmented_music` 仅在口播段落播放音乐：
```
audio_mixer.execute({
    "operation": "segmented_music",
    "video_path": "<assembled_video>",
    "music_path": "<bg_music>",
    "music_volume": 0.20,
    "segments": [
        {"start": 0, "end": 17.0},       # intro speech
        {"start": 167.0, "end": 175.0}    # outro speech
    ],
    "fade_duration": 0.5,
    "output_path": "<project>/renders/final.mp4",
})
```

**单段口播** — 使用 `duck` 或 `full_mix`：
- 将原声与背景音乐叠加
- 若有音乐则 duck
- 归一化最终电平

### 步骤 6：最终编码 — 必选

**不可跳过此步。** 无最终编码时，输出体积过大且可能在目标平台无法正常播放。

使用 `video_compose` 的 `encode` 操作：
- 应用目标 media profile（youtube_landscape、tiktok、instagram_reels 等）
- 双 pass 编码以保证质量

**目标文件大小：**
| 平台 | 最长时长 | 目标大小 |
|----------|-------------|-------------|
| Instagram Reels | 90s | < 50 MB |
| TikTok | 10 min | < 100 MB |
| YouTube Shorts | 60s | < 40 MB |
| YouTube | unlimited | < 25 MB/min |

若输出超过目标，以更低码率重新编码。66 秒 Instagram Reel 若 76 MB 不可接受 — 应低于 30 MB。

```
video_compose.execute({
    "operation": "encode",
    "input_path": "<mixed_video>",
    "output_path": "<project>/renders/final.mp4",
    "media_profile": "instagram_reels",
    "video_bitrate": "4M",
    "audio_bitrate": "192k",
})
```

### 步骤 7：Visual QA

在宣告成功前用 `visual_qa` 校验输出：
```
visual_qa.execute({
    "operation": "review",
    "input_path": "<final_video>",
    "timestamps": [3.0, 10.0, 25.0, 50.0, 100.0, 170.0],
})
```
然后**逐帧查看**提取画面以确认：
- 字幕可见且位于底部（不在脸上）
- 已应用面部增强（皮肤平滑且未过度）
- 转场干净（转场点无伪影）
- Showcase 卡片排版可读

并运行 probe 校验：
```
visual_qa.execute({
    "operation": "probe",
    "input_path": "<final_video>",
    "expected": {
        "width": 1080, "height": 1920,
        "has_audio": true,
        "pixel_format": "yuv420p"
    },
})
```

并检查音频电平：
```
visual_qa.execute({
    "operation": "audio_levels",
    "input_path": "<final_video>",
    "timestamps": [5.0, 50.0, 170.0],
})
```
确认：语音段音量高于 showcase 段（验证音乐放置）。

### 步骤 8：构建渲染报告

记录输出：路径、格式、分辨率、时长、文件大小、QA 结果。

### 步骤 9：自评

| 标准 | 问题 |
|-----------|----------|
| **Playability** | 视频能否无错误播放？ |
| **Quality** | 增强是否正确应用？ |
| **Framing** | 若已重构图 — 面部是否居中？重要内容是否未被裁切？ |
| **Audio** | 语音是否清晰、电平是否平衡？音乐是否仅在预期段落？ |
| **Subtitles** | 字幕是否在底部可见？未遮挡面部？逐词高亮是否正常？ |
| **Transitions** | 转场是否干净？类型是否正确（crossfade vs fadeblack）？ |
| **Showcase** | Showcase 卡片是否正确信箱化且排版可读？ |

### 步骤 10：提交

按 schema 校验 render_report 并通过 checkpoint 持久化。
