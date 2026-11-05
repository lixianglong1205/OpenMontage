# 合成导演 - 屏幕演示流水线

## 适用场景

渲染最终的屏幕演示输出。质量门槛很简单：界面必须可读、节奏必须有意图感，且结果必须符合已规划的平台形态。

## 运行时路由（强制第一步）

先读取 `edit_decisions.render_runtime`。屏幕演示合成根据演示形态使用三种不同的运行时：

- **`render_runtime="remotion"` 且 `TerminalScene`** — 合成终端/CLI/安装流程的首选路径。参见 `.agents/skills/synthetic-screen-recording/`。
- **`render_runtime="remotion"`**（其他场景）— 用于混合屏幕录制与动画叠加层。
- **`render_runtime="hyperframes"`** — 用于可用 CSS + GSAP 自然表达界面的自定义合成 HTML UI 演示。阅读 `skills/core/hyperframes.md`。渲染前 `hyperframes lint` 与 `hyperframes validate` 必须均通过。
- **`render_runtime="ffmpeg"`** — 用于无合成需求的实拍屏幕录制简单剪切/拼接。

在运行时之间静默替换属于**严重**治理违规。若锁定的运行时不可用，在替换前按 AGENT_GUIDE.md 升级处理。

**将 `proposal_packet` 传入 `video_compose.execute()`**，以便工具直接确认提案阶段锁定的运行时与 `edit_decisions` 一致。未传入则工具内交换检查会被跳过，完全依赖审查技能发现漂移。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["edit"]["edit_decisions"]`、`state.artifacts["assets"]["asset_manifest"]` | 渲染内容 |
| 工具 | `video_compose`、`audio_mixer`、`video_trimmer` | 渲染能力 |
| Playbook | 当前风格 playbook | 质量目标 |

## 流程

### 1. 优先保证可读性渲染

优先采用最简单可靠的渲染链：

- 裁剪并调速源素材，
- 合成叠加层与字幕，
- 仅在必要时混音，
- 以适合文字密集内容的码率编码。

### 2. 务实选择输出形态

| 平台 | 宽高比 | 分辨率 | 说明 |
|----------|--------------|------------|-------|
| YouTube / 文档 | `16:9` | 1920x1080 或更高 | 密集 UI 最稳妥的默认 |
| LinkedIn 动态 | `1:1` | 1080x1080 | 竖版过紧时的折中 |
| Shorts / Reels / TikTok | `9:16` | 1080x1920 | 仅当裁剪方案实际可读 |

若源为 4K 且文字过小，在可行时保持更高分辨率。

### 3. 按正确顺序合成

1. 应用裁剪与变速，
2. 应用裁剪与构图策略，
3. 放置遮罩与叠加层，
4. 烧录字幕，
5. 混音，
6. 使用保文字编码设置输出。

使用锐利缩放，避免过度压缩。编码质量下降时，屏幕文字是观众最先察觉的。

### 4. 保持音频真实

- 保持原始语音清晰，
- 勿过度压缩，
- 静音或简化无意义的加速噪声，
- 谨慎使用音乐，能不用则不用。

### 5. 逐项验证输出

**文件检查：**
- [ ] 输出文件存在且为有效 MP4 容器
- [ ] 时长与有效目标相差在 +/-5% 以内
- [ ] 分辨率与所选配置一致

**视觉抽查：**
- [ ] 抽样帧上文字清晰可读
- [ ] 裁剪过渡足够平滑可跟
- [ ] 标注叠加层出现与消失干净
- [ ] 模糊遮罩完全覆盖敏感数据
- [ ] 无黑场或时序故障
- [ ] 字幕不压在关键 UI 上

**音频抽查：**
- [ ] 旁白/画外音清晰、音量一致
- [ ] 若使用音乐，不与语音争抢
- [ ] 变速边界无明显音频故障
- [ ] 无削波或失真

将重要发现记入：

- `render_report.verification_notes`
- `render_report.warnings`
- `render_report.metadata.variant_notes`

## 常见陷阱

- 导出技术上成功但实际不可读的 `9:16` 版本。
- 用通用低码率社交默认设置编码屏幕文字。
- 装饰背景或留白过度压缩可用 UI 区域。
