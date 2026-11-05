# Compose Director - 纪录片蒙太奇流水线

## 何时使用

时间线已经就绪。每个切点都有入点/出点，转场已选定，音乐床已锁定。接下来你要渲染成片，并执行「语域平滑」 pass（统一裁切 + LUT + 音频混音），让混合年代的素材库看起来像同一部影片。

输出为单个 mp4，以及一份 `render_report`  artifact。

## 运行时路由（硬性约束）

本流水线当前**要求** `render_runtime="remotion"`。片尾 tag 栈（ProRes 4444 叠加层合成在最终场景上，或 concat 回退方案）依赖 Remotion 的 `CinematicRenderer`  composition 及其保留 alpha 的渲染路径。HyperFrames 片尾 tag 对等能力明确为 Wave 3 / 延后工作（见 `skills/core/hyperframes.md` → "What stays Remotion-only in Phase 1"）。

- 若 `edit_decisions.render_runtime` 不是 `remotion`，则停止。这是**严重**治理违规。向用户暴露冲突，将决策路由回 proposal 以重新锁定 `render_runtime="remotion"`，在 decision_log 中记录 `render_runtime_selection` 修正，然后继续。
- 切勿通过改写 edit_decisions 中的 render_runtime 而静默继续。纪录片承诺（以运动为主导、以情绪驱动、统一调色）由 Remotion 栈保障，且该承诺是用户已批准的。
- 将 `proposal_packet` 传给 `video_compose.execute()`，以便工具内 `runtime_swap_detected` 检查能端到端确认运行时仍为 `remotion`。在本流水线上该检查为 `skipped` 表示你忘记传入 proposal artifact。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Artifact 校验 |
| 前置 artifact | `state.artifacts["edit"]["edit_decisions"]` | 切点、转场、音乐、元数据提示 |
| 前置 artifact | `state.artifacts["assets"]["asset_manifest"]` | 文件路径、时长、提供方 |
| 工具 | `video_compose`（Remotion 优先 + FFmpeg 回退） | 主渲染引擎 |
| 工具 | `audio_mixer` | 音乐淡入淡出、静音窗口、L-cut |
| 工具（可选） | `color_grade` | 跨混合年代片段的统一 LUT |
| 工具（可选） | `video_trimmer`、`video_stitch` | 需要时的底层辅助 |

## 心智模型

多数流水线把 compose 当作无聊的导出步骤。对纪录片蒙太奇而言，compose 是**创作步骤**：最后一遍，用调色与混音把来源迥异的素材调和为一部作品。

有三件事必须在此完成，且无法更早做：

1. **统一画幅与信箱（letterbox）。** Pexels 1920x1080、Prelinger 640x480 4:3、NASA 1280x720 都要落到同一画布上。
2. **统一调色。** 整条时间线使用单一 LUT，才能让 1962 年家庭录像与 2023 年厨房镜头并置而不突兀。
3. **音频混音。** 音乐电平、静音窗口、L-cut 环境声延续、最终淡出——在时间线在手的情况下一次完成。

## 流程

### 0. 硬性要求检查

读取 `brief` 与 `edit_decisions.metadata` 中的任何硬性要求。
若 brief 写明「无旁白」而编辑中 somehow 出现了旁白轨，**停止**并询问。不要在违反契约的情况下渲染。

同时确认 `edit_decisions.renderer_family` 已锁定为
`documentary-montage`，且所选渲染引擎保留该决策。在本仓库的治理模型中，`video_compose` 在 `operation="render"` 时以 Remotion 为先，即使是以实拍为主的成片亦然。

- 若 Remotion 可用，走常规 `render` 路径并保持已批准的 renderer family。
- 若 Remotion 不可用，**不要**悄悄降级到 FFmpeg。暴露引擎变更，在使用更低层的仅 FFmpeg 路径前获得批准。

### 1. 解析画布

读取 `brief.target_platform`：

| 目标 | 画布 | 信箱 |
|--------|--------|-----------|
| `social_short`（Instagram/TikTok） | 1080x1920（9:16） | 上下裁切；各片段中心锚定 |
| `youtube` / `generic` | 1920x1080（16:9） | 无；可选 2.35:1 上下黑边营造电影感 |
| `linkedin` | 1920x1080（16:9） | 无 |

时间线上的每个片段都必须缩放/裁切到该画布。
对 `social_short`，通常意味着对 16:9 素材做中心裁切。
对采用 2.35:1 黑边处理的 `youtube`，在 1920x1080 画布上下各 pad 140px 黑边。

将结果写入 `render_report.metadata.canvas` 与
`render_report.metadata.letterbox`。

### 2. 为 `video_compose` 构建 Concat 计划

编辑 artifact 提供带 in/out、转场与 source asset_id 的切点列表。遍历 asset_manifest 将每个 asset_id 解析为真实文件路径，然后构建渲染计划。

对本流水线而言，最干净的路径是：

```python
video_compose.execute({
    "operation": "render",
    "output_path": "projects/<name>/renders/final.mp4",
    "edit_decisions": edit_decisions_with_renderer_family,
    "asset_manifest": asset_manifest,
})
```

具体字段名以渲染时刻 live 的 `video_compose` schema 为准——若可用，编写调用前先查阅工具的 `agent_skills`。不要臆造参数。

`edit_decisions_with_renderer_family` 指常规编辑 artifact，且完整保留 `renderer_family = "documentary-montage"`。

### 3. 通过 LUT 调色，而非逐片段

读取 `edit_decisions.metadata.grade_profile`。映射到 LUT 文件：

| Profile | LUT | 适用 |
|---------|-----|-------|
| `warm_film_100` | 复古胶片暖调、轻微提亮 | 哀婉、梦幻 |
| `cool_archive_60` | 冷高光、压黑 | 紧迫、冷幽默 |
| `neutral_doc_20` | 几乎不可察觉的中性平衡 | 庄重 |
| `bleach_bypass_80` | 低饱和、高对比 | 冷幽默、纪录片式 harsh |

若 profile 不在 styles 库中，使用 `neutral_doc_20` 并在 `warnings` 中注明。不要尝试自动调色——LUT 正是语域平滑 pass 的意义所在。

在 composition 层级应用 LUT，而非逐 clip。一个 LUT、一条时间线、一种一致观感。这才让 1962 年 Prelinger 片段与 2023 年 Pexels 片段像同一部影片。

### 4. 在 Compose 中一次性混音

编辑 artifact 已决定音量、淡出、静音窗口与 L-cut 音效层。你的任务是忠实执行：

- 音乐床位于 `edit_decisions.audio.music.volume`（默认 0.7）。
- 按 `fade_in_seconds` 淡入，按 `fade_out_seconds` 淡出。
- 静音窗口 = 在窗口时长内 duck 到 0.0，以 0.2s hold-off 回升。
- L-cut 音效层 = 以 0.5–0.7 音量混在音乐之下。
- 除非 `edit_decisions.audio.narration` 中明确存在旁白，否则不要旁白。

**音乐为强制项。** 若编辑中没有 music 条目，检查 brief：

- `brief.metadata.music_plan.source == "none"` 且带有 `opt_out_reason` →
  用户明确选择退出。无声渲染并在
  `render_report.warnings` 中注明。
- 其他情况 → **停止**。这是契约违规。渲染前向用户暴露。在要求音乐的 brief 上无声渲染是本流水线最刺眼的失败模式。

**不要**添加环境噪声「填补空白」。

### 4b. 通过 Remotion 渲染片尾 Tag

片尾 tag 与 FFmpeg 主体**分开**经 Remotion 渲染。这样两种渲染引擎（FFmpeg 负责实拍、Remotion 负责 typography）职责清晰。合成方式取决于 `brief.metadata.end_tag_plan.mode`。

读取 `brief.metadata.end_tag_plan`：

```json
{
  "text": "WE BUILT BOTH WITH THE SAME HANDS.",
  "palette": "warm_ivory_on_black",
  "duration_seconds": 5.5,
  "render_engine": "remotion",
  "component": "EndTag",
  "mode": "overlay"
}
```

#### 路径 A — Overlay 模式（默认）

Tag 在主体实拍最后几个场景上淡入。这是默认方案，电影感更强—— typography 叠在 live 实拍上，而非切到黑卡。

**执行：**

1. 经 FFmpeg 合成主体（切点 + LUT + 音乐 + 静音窗口）。
   保存为 `projects/<name>/renders/body.mp4`。记录主体 fps。
2. 计算 `durationInFrames = round(duration_seconds × body_fps)`。
3. 经 Remotion CLI 渲染带 alpha 的片尾 tag：
   ```bash
   npx remotion render src/index.tsx EndTagOverlay \
     projects/<name>/renders/end_tag_overlay.mov \
     --codec=prores --prores-profile=4444 \
     --pixel-format=yuva444p10le --image-format=png \
     --props='{"text":"...","palette":"...","overlay":true,
               "fadeInSeconds":1.0,"holdSeconds":3.0,"fadeOutSeconds":1.5}'
   ```
   使用 `overlay: true` 的 `EndTagOverlay` composition。这会产出带真实 alpha 通道的 ProRes 4444 MOV
   （pix_fmt=yuva444p12le）。画布须与主体画布一致。
4. 计算叠加 offset：
   - 若存在则读取 `edit_decisions.end_tag.offset_seconds`。
   - 否则自动计算：`offset = body_duration - tag_duration`。
     tag 的淡出应与主体的收尾淡出对齐。
5. 经 FFmpeg overlay 与 `-itsoffset` 合成：
   ```bash
   ffmpeg -y \
     -i body.mp4 \
     -itsoffset {offset} -i end_tag_overlay.mov \
     -filter_complex "[0:v][1:v]overlay=0:0:format=auto:eof_action=pass[v]" \
     -map "[v]" -map "0:a" \
     -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
     -c:a aac -b:a 192k \
     projects/<name>/renders/final.mp4
   ```
   `eof_action=pass` 表示 overlay 结束后主体视频继续。overlay 自身的 alpha 处理淡入/保持/淡出。

**验证：** 从 overlay 区域抽帧（例如
`offset + 2s`），确认文字可见于实拍之上，而非黑底。若帧中文字背后是黑底，说明 alpha 通道丢失——用 `--image-format=png` 重新渲染。

#### 路径 B — Concat 模式

经典尾卡：不透明黑卡接在主体之后。仅当 `end_tag_plan.mode == "concat"` 时使用。

**执行：**

1. 如上合成主体。
2. 渲染不透明 MP4 片尾 tag：
   ```bash
   npx remotion render src/index.tsx EndTag \
     projects/<name>/renders/end_tag.mp4 \
     --props='{"text":"...","palette":"...","durationInFrames":132}'
   ```
   （5.5s @ 24fps = 132 帧）。画布须与主体画布一致。
3. 拼接主体 + end_tag：
   ```bash
   ffmpeg -f concat -safe 0 -i list.txt -c copy final.mp4
   ```
   若 codec 不匹配则重新编码。

#### 通用规则（两种模式）

**片尾 tag 为强制项。** 唯一可跳过方式是用户明确退出，并记录为 `end_tag_plan: null` 及 `end_tag_opt_out_reason`。
若 brief 有片尾 tag 计划而你跳过了渲染，属于契约违规。定稿前停止并暴露。

写入 `render_report`：
- `end_tag_rendered: true | false`
- `end_tag_mode: "overlay" | "concat"`
- `end_tag_path: "projects/<name>/renders/end_tag_overlay.mov"`（concat 时为 `.mp4`）
- `end_tag_offset_seconds: <number>`（仅 overlay 模式）
- `end_tag_text: "..."`（审计追踪）

若 brief 写「无音乐」且编辑正确无 music 条目，且 `music_plan.source == "none"` 带有 opt-out 原因，则无声渲染。**不要**添加环境噪声「填补空白」。

### 5. 按纪录片规格渲染

纪录片蒙太奇推荐编码设置：

| 字段 | 值 | 原因 |
|-------|-------|-----|
| Codec | `libx264`（H.264） | 通用、体积小 |
| Pixel format | `yuv420p` | 通用兼容 |
| CRF | `18` | 最终交付物视觉上无损 |
| FPS | `24` | 电影感。不要将 24 上转为 30。 |
| Audio codec | `aac` | 通用 |
| Audio bitrate | `192k` | 适合音乐床 |

若源片段为 30fps 而画布为 24fps，让渲染流水线均匀丢帧——不要混合。对混合来源实拍做运动插值效果很差。

### 6. 渲染后验证

渲染成功后，实际探测输出文件并检查：

- **时长。** 应匹配 `sum(out - in for cut in cuts) + fade in/out`，误差 ±0.5s 内。
- **分辨率。** 应匹配画布。
- **音频存在。** 若计划中有音乐，输出必须有音频流。若计划为静音，确认之。
- **首帧与末帧。** 打开文件，seek 到 0s 与 duration-0.1s。首帧应为淡入。末帧应为（或正在淡入）黑场。
- **静音窗口。** Seek 到 silence_window 起点。波形中音频电平应明显下降。

将验证结果写入 `render_report.verification_notes`。

### 7. 输出 Render Report

```json
{
  "version": "1.0",
  "outputs": [
    {
      "path": "projects/<name>/renders/final.mp4",
      "format": "mp4",
      "codec": "h264",
      "audio_codec": "aac",
      "resolution": "1920x1080",
      "fps": 24,
      "duration_seconds": 89.8,
      "file_size_bytes": 18234112,
      "platform_target": "youtube"
    }
  ],
  "render_time_seconds": 42.3,
  "warnings": [],
  "verification_notes": [
    "Duration within +0.2s of planned",
    "First frame is black fade-in as specified",
    "Silence window 54-56s confirmed (music -60dB)",
    "Last frame fades to black at 89.0s"
  ],
  "render_grammar": "documentary-montage",
  "metadata": {
    "pipeline": "documentary-montage",
    "canvas": { "width": 1920, "height": 1080 },
    "letterbox": "2.35:1",
    "lut": "warm_film_100",
    "music_present": true
  }
}
```

### 8. 质量门

- 输出文件存在且可播放。
- 时长在 `brief.duration_seconds`（含主体 + 片尾 tag）±1s 内。
- 分辨率匹配 `target_platform` 画布。
- 已应用 LUT（或已记录 warning）。
- **除非** `brief.metadata.music_plan.source == "none"` 且带有明确 opt-out 原因，否则**必须有音乐**。
- **除非** `brief.metadata.end_tag_plan` 为 null 且带有明确 opt-out 原因，否则**必须渲染并拼接片尾 tag MP4**。该情况下最终 MP4 末帧必须是片尾 tag 卡。
- 首帧与末帧已验证。
- 静音窗口（若有）已在波形中验证。
- 无旁白，除非 brief 批准。
- `render_report.warnings` 列出每一次替换。
- `render_report.metadata.music_mixed = true` 且 `render_report.metadata.end_tag_rendered = true`（或已记录明确 opt-out）。

## 常见陷阱

- **让混合年代片段未经调色就渲染。** 成片会像互联网片段的 PowerPoint 幻灯片。LUT **不可协商**。
- **为匹配画布而放大而非信箱。** Prelinger 640x480 放大到 1920x1080 会像素化且错误。
  用信箱黑边居中，或把方形裁切当作设计选择。
- **添加旁白或环境音效「填补空白」。** 重大变更，需用户批准。
- **逐 clip 调色。** 整部作品一个 LUT。不要试图单独平衡每个 clip——耗时约 10 倍，且语域**更不一致**，而非更一致。
- **悄悄 FFmpeg 降级。** 若 Remotion 被阻断而你未暴露就路由到 FFmpeg，你已改变已批准的渲染路径。
  渲染前停止并暴露该降级。
- **在渲染时覆盖编辑决策。** 若你在 render 调用中调整音量、淡出或 trim，你是在 compose 阶段编辑。回到编辑阶段修正决策、重新输出 artifact，再渲染。
- **跳过验证。** 「成功」但实际无声、淡出错误或裁掉最后一格 hero 帧的渲染，比失败更糟。打开文件看。

## 渲染失败时

若 `video_compose` 返回错误：

1. 按 Decision Communication Contract 检查错误类别
   （auth / provider / tool bug / plan quality）。
2. 若是路径错误，在 asset manifest 中校验每个 asset_id → path 解析。
   单个缺失文件会导致整次渲染失败。
3. 若是 codec 错误，输入 clip 可能为 exotic 容器
   （Archive.org 有时提供 Matroska）。可先经 `video_trimmer` 将各输入规范为 mp4/h264。
4. 若是内存或超时错误，将渲染拆成两半，最后用 `video_stitch` 拼接。
5. 在切换到更低保真路径前向用户暴露。
   本流水线以实拍为主导；没有生成静帧回退。
