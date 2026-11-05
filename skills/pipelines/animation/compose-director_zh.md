# 合成导演 - 动画流水线

## 何时使用

渲染动画时，重点保证文字锐利、时序完整以及输出节奏一致。对于 `image_animation` 方式，本阶段还包括构建 composition JSON、获取音乐、运行预渲染校验，以及执行渲染后自检。

## 运行时路由（强制第一步）

在做任何其他工作之前，先读取 `edit_decisions.render_runtime`。该值在提案阶段已锁定，**不得**静默修改。本技能其余部分默认 `render_runtime="remotion"`（本流水线的默认值）。若提案锁定了其他运行时：

- **`render_runtime="hyperframes"`** — HTML/CSS/GSAP 渲染。请勿遵循下方 Remotion 专用章节（`public/`  staging、Remotion composition JSON）。改为：
  1. 阅读 `skills/core/hyperframes.md` 了解完整路由模型。
  2. 阅读 `.agents/skills/hyperframes/SKILL.md` 与 `.agents/skills/hyperframes-cli/SKILL.md`，了解编写契约与 CLI 用法。
  3. 调用 `video_compose` 并设置 `edit_decisions.render_runtime="hyperframes"` — 它会委托给 `hyperframes_compose`，后者负责在 `projects/<name>/hyperframes/` 下物化工作区、执行 `hyperframes check → render`，并返回 MP4 路径。
  4. 渲染前 **`hyperframes check` 必须通过**。它统一 lint、运行时、布局、动效与 WCAG 对比度检查；迭代期间可用 `skip_contrast=true` 暂缓对比度，但最终交付不可跳过。
- **`render_runtime="ffmpeg"`** — 简单拼接/裁剪，无 composition。直接调用 `video_compose`；它不会自动升级到 Remotion。
- **运行时不可用** — **不要**静默换用其他引擎。按 AGENT_GUIDE.md >「Escalate Blockers Explicitly」向用户暴露阻塞项并等待批准（在 decision_log 中记录为 `render_runtime_selection` 决策）后再切换。

渲染后自检（final_review）在各运行时上一致 — 相同的 ffprobe 探测、帧采样、音频抽查与承诺保留检查。`final_review.checks.promise_preservation.render_runtime_used` 必须等于实际运行的运行时。

**调用 `video_compose.execute()` 时传入 `proposal_packet`**。这样工具可直接对比提案锁定的运行时与 `edit_decisions` 中记录的运行时；若不一致则设置 `runtime_swap_detected=true`。未传入时，该检查为 `skipped`，需由 reviewer 技能通过跨产物对比发现运行时被替换。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["edit"]["edit_decisions"]`、`state.artifacts["assets"]["asset_manifest"]` | 时序计划与资源文件 |
| 工具 | `video_compose`、`audio_mixer`、`video_stitch` | 最终组装 |
| 工具 | `composition_validator` | 预渲染校验（强制） |
| 工具 | `audio_probe` | 音乐时长检查 |
| Playbook | 当前 style playbook | 渲染一致性 |
| 参考 | `remotion-composer/public/demo-props/mori-no-seishin.json` | Composition JSON 格式参考 |
| 参考 | `skills/core/remotion.md` | Remotion 模式、`anime_scene` 类型、关键约束 |

## 流程

### 1. 确保资源位于 Remotion 的 public 目录

**关键：** Remotion 仅能通过 `staticFile()` 访问文件，其解析根目录为 `remotion-composer/public/`。渲染前**必须**将生成的图片与音乐文件复制或符号链接到该目录。

```
Project structure:
  projects/<name>/assets/images/*.png     ← where images were generated
  remotion-composer/public/<name>/*.png   ← where Remotion reads them

Required: Copy or symlink images AND music into public/<project-name>/
```

composition JSON 中的图片路径相对于 `remotion-composer/public/`：
```json
"images": ["deep-ocean/scene1-a.png", "deep-ocean/scene1-b.png"]
"src": "deep-ocean/ambient-music.mp3"
```

**若跳过此步，渲染会因缺少文件失败，或产生黑帧。**

### 2. 构建 Composition JSON（image_animation 方式）

对于 `anime_scene` composition，在 `remotion-composer/public/demo-props/<name>.json` 构建 JSON 文件。

**必需结构：**

```json
{
  "cuts": [
    {
      "id": "scene-1-name",
      "source": "",
      "in_seconds": 0,
      "out_seconds": 5,
      "type": "anime_scene",
      "images": ["<project>/<image-a>.png", "<project>/<image-b>.png"],
      "animation": "<camera-motion>",
      "particles": "<particle-type>",
      "particleColor": "#HEXCOLOR",
      "particleCount": 20,
      "particleIntensity": 0.5,
      "backgroundColor": "#0A0A1A",
      "vignette": true,
      "lightingFrom": "rgba(r,g,b,a)",
      "lightingTo": "transparent"
    }
  ],
  "overlays": [...],
  "audio": { "music": { "src": "<project>/music.mp3", "volume": 0.15, "fadeInSeconds": 2, "fadeOutSeconds": 3 } }
}
```

**属性名对照（JSON 字段 → AnimeScene prop）：**

| JSON 字段 | 类型 | 取值 | 必填 |
|------------|------|--------|----------|
| `type` | string | `"anime_scene"` | 是 |
| `images` | string[] | 相对 `public/` 的 1–4 个图片路径 | 是 |
| `animation` | string | `zoom-in`, `zoom-out`, `pan-left`, `pan-right`, `ken-burns`, `drift-up`, `drift-down`, `parallax`, `static` | 否（默认：`ken-burns`） |
| `particles` | string | `fireflies`, `petals`, `sparkles`, `mist`, `light-rays` | 否 |
| `particleColor` | string | 十六进制颜色 | 否（默认：`#FFE082`） |
| `particleCount` | number | 1-50 | 否（默认：20） |
| `particleIntensity` | number | 0-1 | 否（默认：0.6） |
| `backgroundColor` | string | 场景背景十六进制颜色 | 否（默认：`#0A0A1A`） |
| `vignette` | boolean | 电影感暗角叠加 | 否（默认：true） |
| `lightingFrom` | string | 渐变起始色（`rgba(...)` 或 `transparent`） | 否 |
| `lightingTo` | string | 渐变结束色 | 否 |

**参考：** 完整可运行示例见 `mori-no-seishin.json`（吉卜力森林）与 `deep-ocean.json`（水下生物发光）。

### 3. 获取音乐并寻找最佳偏移

使用 `tools/audio/pixabay_music.py` 查找与情绪匹配的免版税 ambient 音乐。

**下载后必须运行音频能量分析：**

```python
from tools.analysis.audio_energy import AudioEnergy
result = AudioEnergy().execute({
    "input_path": "path/to/music.mp3",
    "video_duration_seconds": 30,  # your video duration
})
data = result.data
print(f"Recommended offset: {data['recommended_offset_seconds']}s")
print(f"Reason: {data['offset_reason']}")
print(f"Needs loop: {data['needs_loop']}")
```

该工具会：
1. **找到最佳片段** — 分析每秒响度，找出平均能量最高的 N 秒窗口。Ambient 曲目常有 10–30 秒的安静前奏才进入主旋律。
2. **建议是否循环** — 若从偏移点起的音乐短于视频，会提示启用循环。

**在 composition JSON 中应用偏移：**

```json
"audio": {
  "music": {
    "src": "project/music.mp3",
    "volume": 0.15,
    "fadeInSeconds": 2,
    "fadeOutSeconds": 3,
    "offsetSeconds": 55,
    "loop": false
  }
}
```

- `offsetSeconds` — 从曲目该时间点开始播放（跳过安静前奏）
- `loop` — 若剩余音乐短于视频则设为 `true`

**若工具返回 `needs_loop: true`：** 在 composition JSON 中设置 `"loop": true`。Remotion 会无缝循环音频，并在每次循环时重置音量淡入淡出。

### 4. 预渲染校验（强制 — 无例外）

每次渲染前运行 `composition_validator`：

```python
from tools.analysis.composition_validator import CompositionValidator
result = CompositionValidator().execute({
    "composition_path": "remotion-composer/public/demo-props/<name>.json",
    "assets_root": "remotion-composer/public",
})
# result.data["valid"] MUST be True before proceeding
```

可发现：
- 会导致黑帧或渲染错误的缺失图片/音频文件
- 无效的 cut 时序（out ≤ in）
- 音频长于视频时长

**校验失败则先修复再渲染。不要渲染无效 composition。**

### 5. 保持动效时序

勿因导出设置或粗心的 composition 改变 hold、stagger 或场景切换的感知时序。

### 6. 保护文字与图表清晰度

动画常在导出后出现文字发糊、细线浑浊或移动端构图拥挤等问题。

### 7. 渲染

```bash
cd remotion-composer
npx remotion render Explainer \
  --props="public/demo-props/<name>.json" \
  --output="<output-path>/final.mp4" \
  --codec=h264 --crf=18
```

**注意：** composition 名称为 `Explainer`（不是 `ExplainerVideo`）。**不要**指定 `src/index.ts` 作为入口 — Remotion 会自动发现。

### 8. 渲染后自检（强制）

渲染完成后，抽取场景中段帧并目视检查：

```bash
# Extract one frame from the middle of each scene
ffmpeg -y -i final.mp4 \
  -vf "select='eq(n\,75)+eq(n\,225)+eq(n\,375)+eq(n\,525)+eq(n\,675)+eq(n\,825)'" \
  -vsync vfr frames/scene_%02d.png
```

**逐帧检查：**
- [ ] 图片可见（非黑/暗帧）
- [ ] 粒子在渲染（可见 sparkles、fireflies 等）
- [ ] 镜头运动明显（构图非静态）
- [ ] overlay 在正确时刻显示且文字清晰
- [ ] 各场景色板一致
- [ ] 暗角营造电影感景深

**同时验证输出文件：**
```bash
ffprobe -v quiet -print_format json -show_format -show_streams final.mp4
```
- 时长在目标 ±5% 内？
- 分辨率为 1920×1080？
- 存在音频流？

**若发现问题：** 定位原因（缺图、时序错误、渲染故障）并在呈现给用户前修复。

### 9. 使用渲染元数据

建议的 metadata 键：

- `render_fps`
- `sharpness_checks`
- `safe_zone_checks`
- `variant_outputs`

## 常见陷阱

- **忘记将资源复制到 `remotion-composer/public/`** — 渲染失败的头号原因。图片生成在 `projects/<name>/assets/`，Remotion 从 `public/` 读取。
- 渲染后文字发软或锯齿。
- 压缩选项损害图表。
- 预览与成片之间场景节奏变化。
- **跳过 `composition_validator`** — 在浪费渲染时间前捕获缺文件、错误时序、音频不匹配。
- **不抽帧自检** — 渲染视频在帧目视检查完成前不算「完成」。黑帧、缺失粒子或不可见图片未必能从文件大小看出。
- **用 `useVideoConfig()` 的 `durationInFrames` 做场景级时序** — 它返回**整个** composition 时长，而非场景的 Sequence 时长。见 `skills/core/remotion.md` Critical Constraints。
