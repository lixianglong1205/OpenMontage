# 创意总监 - 本地化配音流水线

## 何时使用

当用户拥有源视频并需要翻译交付物时使用本流水线：字幕、配音音频，或一种或多种目标语言的本地化视频。

你的首要职责是明确实际所需的本地化类型，因为仅字幕、配音音频与口型同步翻译是不同工作。

## 运行时选择（强制 — 向用户说明约束，勿静默选定）

锁定 `render_runtime = "remotion"`（含各语言字幕烧录 / 口型同步的合成交付物）或 `"ffmpeg"`（在源视频上纯字幕烧录、无合成）。**HyperFrames 在本流水线 Phase 1 中不是有效运行时** — 本地化依赖 Remotion 的字幕栈，而配音+口型同步则依赖 Remotion TalkingHead 流水线。

按 AGENT_GUIDE.md →「Present Both Composition Runtimes (HARD RULE)」：勿静默默认 remotion。告知用户：「HyperFrames 可用，但 localization-dub 依赖 Remotion 字幕 + TalkingHead 对等能力，Phase 1 尚未具备 — remotion 是唯一可行选择」。记录 `render_runtime_selection` 决策，hyperframes 的 `rejected_because: "caption + lip-sync parity deferred on localization-dub"`。

## 参考输入

- `docs/localization-dubbing-best-practices.md`
- `skills/creative/short-form.md`
- `skills/creative/long-form.md`

## 流程

### 1. 定义本地化范围

记录：

- 源语言，
- 目标语言，
- 审核负责人，
- 是否需要术语表或法务审核，
- 用户需要的是字幕、配音音频、口型同步，或组合。

### 2. 对源素材分类

记录源模式：

- `single_speaker`
- `multi_speaker`
- `voiceover_led`
- `speaker_led_on_camera`

同时记录画面文字或动态图形是否需要人工替换或遮盖处理。

### 3. 选择符合实际的交付物

可能的交付物：

- 仅字幕包，
- 无口型同步的配音视频，
- 口型同步的本地化视频，
- 按语言导出的打包 bundle。

### 4. 构建简报

建议的元数据键：

- `source_language`
- `target_languages`
- `deliverable_mode_map`
- `glossary_terms`
- `protected_terms`
- `review_requirements`
- `timing_risks`

### 5. 质量门

- 本地化范围明确，
- 目标产出切合实际，
- 术语表与审核要求已记录，
- 说话人数量或可见口部带来的风险已暴露。

## 常见陷阱

- 把所有翻译需求都称为配音需求。
- 在生成音频之后才考虑术语表管控。
- 在视觉困难的源素材上承诺口型同步却不事先警告。

---

## 门控提醒（具有约束力）

本阶段以人工批准为门控（`human_approval_default: true`）。审核通过后：
以 `status="awaiting_human"` 做检查点，呈现摘要（Backlot 看板会渲染该制品），并**结束本轮**。勿在同一回复中启动下一阶段。
批准按门控逐项进行 — 较早的「继续」不覆盖本门控。
