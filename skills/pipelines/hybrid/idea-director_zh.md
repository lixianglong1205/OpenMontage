# Idea Director - 混合管线（Hybrid Pipeline）

## 何时使用

当项目同时包含真实源素材与支持性视觉内容时使用本管线：访谈加图解、实拍加叠加层、录屏加品牌图形，或源素材主导剪辑并插入生成片段。

混合管线不是万能兜底。你的首要任务是明确什么内容保持「主叙事」地位。

## 运行时选择（强制 — 须向用户呈现两种运行时）

在锁定制作计划之前，与用户共同决定 `render_runtime`。混合管线同时支持 Remotion 与 HyperFrames；二者均非自动默认。遵循 AGENT_GUIDE.md →「Present Both Composition Runtimes (HARD RULE)」中的约定：

1. 查询 `video_compose.get_info()["render_engines"]`。若 `remotion` 与 `hyperframes` 均为 `True`，则结合简报向用户呈现二者：
   - **Remotion** — 适用于源实拍占主导、支持层为 React 场景组件（图表、标注、文字卡）的情况。Remotion 通过 `<OffthreadVideo>` 在一遍合成中组合视频片段与 React 叠加层。
   - **HyperFrames** — 适用于支持层为 HTML/GSAP 原生（动态标注、registry 区块、排版叠加层），且源实拍以 `<video class="clip">` 嵌入的情况。
2. 结合锚定媒介与支持层的形态给出推荐及理由。
3. 等待用户明确批准。
4. 在 `decision_log` 中记录为 `render_runtime_selection` 决策，且 `options_considered` 中须包含两种运行时。

当两种运行时均可用时，若 `render_runtime_selection` 决策的 `options_considered` 仅含一种运行时，属于 CRITICAL 级审查发现。

## 参考输入

- `docs/hybrid-video-best-practices.md`
- `skills/creative/storytelling.md`
- `skills/creative/video-editing.md`

## 流程

### 1. 选择锚定媒介

选定叙事锚定媒介：

- `talking_head`
- `broll_footage`
- `screen_recording`
- `still_sequence`
- `narration_led_graphics`

### 2. 定义支持层

可能的支持层包括：

- 字幕，
- 图解，
- 代码可视化，
- 数据卡片，
- 生成插入片段，
- 旁白，
- 音乐。

每一支持层应解决具体问题，而非仅为时间线装饰。

### 3. 决定交付物组合

常见产出：

- 主片（hero cut），
- 竖版精简版，
- 方版精简版，
- 分章节版，
- 广告变体。

### 4. 构建简报

建议的元数据键：

- `anchor_medium`
- `source_inventory`
- `support_layers`
- `deliverable_mix`
- `missing_capabilities`
- `fallback_policy`

### 5. 质量门

- 锚定媒介已明确，
- 支持层有充分理由，
- 交付物组合与源素材清单匹配，
- 缺失能力尽早暴露。

## 常见陷阱

- 未定义主媒介就把一切称为混合。
- 在理解源素材之前就规划支持层。
- 将可选的生成插入片段视为必然可用。

---

## 门控提醒（具有约束力）

本阶段以人工批准为门控（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 创建检查点，呈现摘要（Backlot 看板会渲染该制品），并**结束本轮回复**。勿在同一回复中启动下一阶段。
批准按门控逐项生效 — 此前「继续」并不覆盖本门控。
