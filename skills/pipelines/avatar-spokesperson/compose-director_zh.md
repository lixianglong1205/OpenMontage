# Compose Director - Avatar Spokesperson Pipeline

## 何时使用

渲染最终代言人输出。标准很简单：主讲人画面必须稳定、语音必须清晰，字幕或辅助卡片不得挤占画面。

## 运行时路由（硬性约束 — 仅 Remotion）

Phase 1 已从 HyperFrames 推迟。`edit_decisions.render_runtime` 必须为 `"remotion"`。本流水线依赖 Remotion 的 `TalkingHead` 合成与 `remotion_caption_burn` — Phase 1 中二者在 avatar-spokesperson 上均无 HyperFrames 对等实现。

- 若 `edit_decisions.render_runtime == "hyperframes"`，则停止。重新打开 idea 阶段并说明该约束。静默改写属于治理违规。
- 依据 AGENT_GUIDE.md →「Present Both Composition Runtimes（硬性规则）」：锁定 remotion 不能成为跳过对话的借口。用户应知晓 HyperFrames 作为运行时存在，以及为何对 avatar-spokesperson 不可行。记录 `render_runtime_selection` 决策，hyperframes 的 `rejected_because: "TalkingHead + caption parity deferred on avatar-spokesperson"`。
- 将 `proposal_packet`/`brief` 传入 `video_compose.execute()`，以便在工具内检测运行时切换。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["edit"]["edit_decisions"]`, `state.artifacts["assets"]["asset_manifest"]` | 待渲染内容 |
| 工具 | `video_compose`, `audio_mixer`, `video_stitch`, `audio_enhance` | 渲染与音频收尾 |
| Playbook | 当前 style playbook | 版式与布局规则 |

## 流程

### 1. 先渲染主片（Hero Cut）

在衍生版本之前优先完成一条强主片。合成内容包括：

- 主讲人视频，
- 字幕，
- 下三分之一条（lower-thirds），
- CTA 卡片，
- 混音旁白。

### 2. 保持画面简洁

字幕与 CTA 位置在此比花哨转场更重要。勿遮挡面部与嘴部区域。

### 3. 核对口型与音频

若 avatar 路径使用了唇形同步或音频驱动 talking head，检查：

- 口型时序，
- 面部伪影，
- 长段落漂移，
- 音频清晰度。

### 4. 校验每一项输出

将重要发现记入：

- `render_report.verification_notes`
- `render_report.warnings`
- `render_report.metadata.variant_notes`

### 5. 质量门

- 输出文件有效，
- 语音清晰，
- 字幕可读，
- 主讲人视觉稳定。

## 常见陷阱

- 字幕遮挡下巴或嘴部。
- 长唇形同步成片未抽检漂移即交付。
- 衍生裁剪切掉主讲人或 CTA。
