# 轨道与剪辑片段（Tracks and Clips）

剪辑片段（clip）是 composition 根节点下带时间轴的子元素。轨道（track）是时间重叠概念，而非视觉叠放概念。

## 什么是 Clip

clip 是任意带有 `data-start`、`data-duration`（在需要时）和 `data-track-index` 的 DOM 元素。常见类型：

- **视觉 `<div>` clip** — 场景、卡片、叠加层。始终需要 `data-duration`。
- **子 composition 宿主** — 带 `data-composition-src` 的 `<div>`。始终需要 `data-duration`。
- **视频 clip** — 带 `muted` 和 `playsinline` 的 `<video>`。时长可默认为媒体长度。
- **音频 clip** — `<audio>`。时长可默认为媒体长度。
- **图片 clip** — `<img>`。始终需要 `data-duration`。

为手写视觉 clip 添加 `class="clip"`，以便工具与示例能定位它们。

## 轨道是时间维度的，不是视觉维度的

`data-track-index` 控制的是**时间上的重叠**，而非绘制顺序：

- **同一 `data-track-index` 上的两个 clip** 在时间上不得重叠。`hyperframes lint` 会标记此类问题。
- **视觉层级（前/后）** 由 CSS `z-index` 控制，与轨道索引无关。

轨道 `5` 上的 clip 并不在轨道 `1` 之上 — 只是在时间轴上处于不同的音/视频 lane。叠放用 CSS，排程用轨道。

## 如何选择轨道索引

没有固定约定，但常见模式：

- **轨道 0** — 基底视频（例如 A-roll）。
- **轨道 1 及更高** — 视觉场景、叠加层、字幕。
- **更高轨道（如 10+）** — 音频 clip，与视觉轨道分开以便 lint 清晰。

向已有 composition 添加新 clip 时：

1. 找一条现有轨道，使其与你的新 clip 的 `[data-start, data-start + data-duration)` 区间无重叠。
2. 或选用新的轨道索引。
3. 同一轨道上绝不要重叠两个 clip — linter 会失败，渲染行为未定义。

## Clip 在 Composition 内的时间

`data-start` 单位为秒，从 _composition_ 起点算起。对于子 composition，其内部时间线（自身的 `data-duration` 与子 clip）在宿主的 `data-start` 到 `data-start + data-duration` 之间运行。

`data-media-start`（用于 `<video>`/`<audio>`）是**源媒体内的偏移**。用它可跳过媒体文件前几秒，而无需裁剪文件本身。

## 相对时间

`data-start` 可接受 clip ID 而非数字，表示「在该 clip 结束时开始」。用 `+ N` / `- N` 做偏移；负值产生重叠（适用于 crossfade）。

```html
<video id="intro" data-start="0" data-duration="10" data-track-index="0" src="..."></video>
<video id="main" data-start="intro" data-duration="20" data-track-index="0" src="..."></video>
<video
  id="scene-a"
  data-start="intro + 2"
  data-duration="20"
  data-track-index="0"
  src="..."
></video>
<video
  id="scene-b"
  data-start="intro - 0.5"
  data-duration="20"
  data-track-index="1"
  src="..."
></video>
```

规则：

- 引用仅在**同一 composition 内**解析 — 不能引用父级或兄弟子 composition。
- 被引用的 clip 必须有**已知时长**（显式 `data-duration` 或从媒体推断）。否则引用无法解析。
- **禁止循环引用** — `A → B → A` 会被拒绝。检测到环会报错。
- 能解析为数字的值始终视为绝对秒数。否则解析器期望 `<id>`、`<id> + <number>` 或 `<id> - <number>`（空格可选）。
- 引用可链式（`A → B → C`）。为可读性，链深度建议不超过 3–4 层。
- 负偏移产生重叠；重叠的 clip 必须在**不同轨道**上，同轨重叠会被拒绝。
