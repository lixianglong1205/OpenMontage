# Compose Director - 混合管线（Hybrid Pipeline）

## 适用场景

渲染混合项目，使源素材、辅助图形与音频在所有输出中保持连贯一致。

## 运行时路由（必须首先执行）

读取 `edit_decisions.render_runtime`。混合类工作通常仍使用 Remotion，因为源 footage 与 React 辅助叠加层可在一次渲染中干净地合成：

- **`render_runtime="remotion"`** — 默认。源 footage 通过 `<OffthreadVideo>`，辅助图形为 React 组件，一次渲染完成。
- **`render_runtime="hyperframes"`** — 仅当辅助层为 HTML/GSAP 原生（例如动画文字标注、registry 块）时选用。源 footage 仍可通过 `<video class="clip">` 实现，但会失去部分 Remotion 组件栈能力。参见 `skills/core/hyperframes.md`。
- **`render_runtime="ffmpeg"`** — 在本管线中较少见；表示没有生成的辅助层。

静默替换运行时是严重的治理违规。在替换方案之前，须按 AGENT_GUIDE.md 升级阻塞项。

**将 `proposal_packet` 传入 `video_compose.execute()`**，以便工具内置的换栈检测针对提案直接运行，而不是被标记为 `skipped`。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | 制品校验 |
| 前置制品 | `state.artifacts["edit"]["edit_decisions"]`、`state.artifacts["assets"]["asset_manifest"]` | 剪辑逻辑与辅助资产 |
| 工具 | `video_compose`、`audio_mixer`、`video_stitch`、`video_trimmer`、`color_grade`、`audio_enhance` | 最终组装与润色 |
| Playbook | 当前启用的 style playbook | 输出一致性 |

## 流程

### 1. 校验源素材与辅助层平衡

最终渲染仍应呈现为「以源素材为主导、辅以支持元素」的视频，而不是互不相关系统的拼贴。

### 2. 检查变体完整性

针对每个输出变体，验证：

- 裁切安全，
- 文字安全，
- 字幕可读性，
- 音频一致性。

### 3. 保持音频连贯

源对白、旁白、音乐与音效应听起来像同一混音，而非各层争夺空间的分离图层。

### 4. 使用渲染元数据

建议的元数据键：

- `variant_outputs`
- `balance_checks`
- `subtitle_checks`
- `audio_notes`

## 常见陷阱

- 主片剪得不错，平台变体却出问题。
- 竖屏导出中辅助图形被裁切。
- 源素材段与生成段之间响度不一致。
