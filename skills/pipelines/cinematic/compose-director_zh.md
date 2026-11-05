# Compose Director - 电影感流水线

## 何时使用

渲染电影感成片时，需格外关注调色、音频动态与画面处理。这不是一次泛泛的导出步骤。

## 运行时路由（必须首先执行）

读取 `edit_decisions.render_runtime`。电影感类工作路由如下：

- **`render_runtime="remotion"`** — 使用 `CinematicRenderer` 的视频主导预告片默认选项。在单次基于 React 的渲染中保留视频片段、转场与环境叠加层。
- **`render_runtime="hyperframes"`** — 适用于动感标题卡、HTML/GSAP 驱动预告片、发布 reel 风格合成，或明确的 Three.js 世界飞越镜头。参见 `skills/core/hyperframes.md`。渲染前必须通过 `hyperframes check`。
- **`render_runtime="ffmpeg"`** — 无合成的简单源素材拼接。

对于 Blender 世界影片，FFmpeg 是已编号 Blender 图像序列与音频的批准封装方式。它不得合成镜头运动，也不得用平移/缩放效果替代缺失的 Blender 帧。

### 快速全曲节拍蒙太奇（BMTS-Lite）

当已批准的 brief 要求基于一条提供的音乐轨与已选视频片段快速蒙太奇——且无参考匹配、旁白、标题或语义选片——将 `bgm_montage_lite` 作为完整渲染路径。传入源音频、全部拟用源片段、项目目录及请求的宽高比（默认 `auto`）。工具在流、尺寸、时长与全解码检查通过后返回 MP4、时间线、audiomap 及 OpenMontage 渲染报告。

这与专业参考引导的 BGM Montage 集成不同：Lite 不需要参考视频或 API 密钥，并有意保留 BMTS-Lite 的源复用与自动构图。不要在此路径上增加语义选片、严格复用限制、Agent 视觉审查依赖或第二套渲染引擎。已创作场景与混合媒体工作仍使用现有合成运行时；专业 BGM Montage 路径仍是参考风格匹配及其更严格质量门的选择。

`delivery_promise.motion_required=true` 表示锁定的运行时是一项承诺。静默切换到另一运行时（含 FFmpeg Ken Burns）属于 CRITICAL 治理违规。若锁定的运行时失败，按 AGENT_GUIDE.md >「Escalate Blockers Explicitly」升级处理。

**向 `video_compose.execute()` 传入 `proposal_packet`**，以便工具的 `runtime_swap_detected` 检查直接与 `proposal_packet.production_plan.render_runtime` 对比。未传入时，工具内会跳过交换检查，仅由 reviewer 技能捕获漂移。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["edit"]["edit_decisions"]`, `state.artifacts["assets"]["asset_manifest"]` | 剪辑方案与媒体资产 |
| 工具 | `video_compose`, `audio_mixer`, `video_stitch`, `video_trimmer`, `color_grade`, `audio_enhance` | 渲染与成片 |
| Playbook | 当前风格 playbook | 成片一致性 |

## 流程

### 0. 渲染前检查硬性要求

若已批准的 brief 或场景计划将运动作为硬性要求，须确认渲染路径仍兑现该承诺。

- 若必须使用 Remotion 但不可用或失败，立即停止并将问题上报用户。
- 不要为以运动为主的预告片、teaser 或 agent 视频切换到仅 FFmpeg 的静图回退方案。
- 除非用户明确批准降级，否则不要将成片改为 animatic。
- 若渲染引擎发生实质性变更，渲染前告知用户并说明原因。

**Remotion 强制预检（当场景计划包含任意 Remotion 场景类型——标题卡、数据卡、anime/hero_title、片尾 tag、叠加层——每次渲染前执行）：**

```bash
python -c "
from tools.tool_registry import registry
registry.discover()
info = registry.get('video_compose').get_info()
print('Render engines:', info.get('render_engines'))
print('Remotion note:', info.get('remotion_note'))
"
```

若可用渲染引擎中不包含 Remotion，按 Decision Communication Contract 停止并报告用户。未经批准不得替换为降保真渲染路径。

### 1. 审慎使用画面处理

仅在有助于成片时使用 letterbox、24fps 意图或重调色；不要仅因流水线名为 cinematic 就套用。

### 2. 保留音频动态

混音应支持：

- 安静段落，
- 冲击时刻，
- 清晰的对话或旁白，
- 可控的音乐起伏。

### 3. 验证最终情绪

检查：

- 开场帧，
- 揭示节拍，
- 最终落点，
- 相关场景下的字幕可读性。

### 4. 使用渲染元数据

建议的 metadata 键：

- `frame_treatment`
- `grade_profile`
- `mix_notes`
- `variant_outputs`

## 常见陷阱

- 把音频压平导致成片失去动态。
- 对需要每一寸像素的素材加 letterbox。
- 让调色或锐化损伤人脸或文字。
- 在 Remotion 渲染受阻时静默换成更低保真的静图导出。
