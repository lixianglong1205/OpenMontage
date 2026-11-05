# 合成总监 — 本地化配音流水线

## 何时使用

渲染本地化输出。质量标准是：各语言包均可理解、时序一致，且版本标注清晰。

## 运行时路由（硬约束 — 仅限 Remotion 或 FFmpeg）

Phase 1 暂不支持 HyperFrames。`edit_decisions.render_runtime` 必须为 `"remotion"` 或 `"ffmpeg"`。本地化依赖 Remotion 的字幕栈（按语言烧录字幕），以及在配音并做唇形同步时依赖 Remotion TalkingHead 流水线。Phase 1 中 HyperFrames 对二者均无对等能力。

- 若 `edit_decisions.render_runtime == "hyperframes"`，应停止。重新打开创意阶段并说明该约束 — 不要静默改写运行时。
- 按 AGENT_GUIDE.md →「Present Both Composition Runtimes（硬规则）」：流水线的约束**不能**跳过与用户沟通。向用户说明 HyperFrames 存在但在本场景不可行。记录 `render_runtime_selection` 决策，其中 hyperframes 的 `rejected_because: "caption + lip-sync parity deferred on localization-dub"`。
- 将 `proposal_packet`/`brief` 传入 `video_compose.execute()`，以便端到端检测运行时切换。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["edit"]["edit_decisions"]`、`state.artifacts["assets"]["asset_manifest"]` | 按语言的渲染指令 |
| 工具 | `video_compose`、`audio_mixer`、`video_trimmer`、`audio_enhance` | 最终渲染与音频收尾 |
| Playbook | 当前启用的 style playbook | 字幕位置与输出质量 |

## 流程

### 1. 按语言渲染

将每种目标语言视为独立交付物集合。名称与输出目录须明确。

### 2. 预期时序调整

需考虑：

- 字幕重排，
- 配音音频时长漂移，
- 更长的 CTA 停留，
- 可选的裁剪或补段。

### 3. 校验各语言版本

将重要发现记入：

- `render_report.verification_notes`
- `render_report.warnings`
- `render_report.metadata.locale_notes`

检查：

- 可理解性，
- 字幕适配，
- 明显音画不同步，
- 版本标注。

### 4. 质量门

- 各语言输出均已存在，
- 配音与字幕时序可接受，
- 标签与文件名无歧义，
- 警告信息已保留。

## 常见陷阱

- 把所有语言当作时序完全一致来渲染。
- 翻译后未重新检查字幕行长度。
- 输出命名掩盖语言或处理模式。
