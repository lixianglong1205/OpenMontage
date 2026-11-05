# Idea Director - 播客再利用流水线

## 何时使用

当源素材为播客单集（纯音频或视频播客），且用户需要片段、社交素材或配套长视频方案时，使用本流水线。

你的首要职责是：根据**实际存在的**源素材，判断哪些产出是可行的。

## 运行时选择（强制 — 向用户说明约束，勿静默选定）

锁定 `render_runtime = "remotion"`（audiogram 与合成输出）或 `"ffmpeg"`（纯音频主导的片段导出）。**HyperFrames 在本流水线 Phase 1 中不是有效运行时** — 播客产出依赖 Remotion 的词级字幕能力，HyperFrames 尚无对等实现。

按 AGENT_GUIDE.md →「Present Both Composition Runtimes (HARD RULE)」：向用户说明约束 — 「HyperFrames 在你的机器上可用，但 podcast-repurpose 依赖 Remotion 字幕烧录，因此此处 remotion 是唯一可行选择」。记录 `render_runtime_selection` 决策，hyperframes 的 `rejected_because: "caption-burn parity deferred on podcast-repurpose"`。

## 参考输入

- `docs/podcast-repurposing-best-practices.md`
- `skills/creative/short-form.md`
- `skills/creative/long-form.md`

## 流程

### 1. 对源素材分类

记录源素材模式：

- `audio_only`
- `video_podcast`
- `hybrid`（音频加静态图、封面、嘉宾照片）

同时记录对话形式：

- solo
- interview
- panel
- narrative / produced show

### 2. 选择与现实相符的交付物

默认交付物应能在现有源素材与工具条件下完成。

稳妥选项：

- 短视频高光片段，
- audiogram 或字幕主导片段，
- 金句/引用主导片段，
- 可选的一整套单集配套版式。

除非源视频、品牌素材与可选图像确实存在，否则不要假定高制作水准的整集 YouTube 方案。

### 3. 设定合理的交付物组合

典型起点：

- `3-5` 条高光片段
- 若单集金句突出，则 `1-3` 条引用主导素材
- 若源素材支撑，可选长视频配套

### 4. 尊重平台差异

- `9:16` 用于 Shorts、Reels、TikTok
- `1:1` 用于 LinkedIn 及更稳妥的信息流再利用
- `16:9` 用于 YouTube 配套视频

若源素材为纯音频，在 brief 中明确说明。下游阶段不应规划不存在的说话人框景视频。

### 5. 编写 Brief

在 `brief.metadata` 中使用更完整的播客专用约定：

- `source_mode`
- `show_name`
- `episode_title`
- `episode_number`
- `speakers`
- `conversation_format`
- `deliverable_mix`
- `brand_assets_available`
- `full_episode_companion_feasible`

### 6. 质量门禁

- 交付物组合与实际源素材一致，
- 片段数量与单集时长相称、现实可行，
- brief 说明视觉将走源素材主导、引用主导还是 audiogram 主导，
- 长视频目标按可用素材规模收敛。

## 常见陷阱

- 将纯音频与视频播客源当作同一制作问题处理。
- 从内容薄弱的单集规划过多交付物。
- 在无素材支撑时承诺丰富的整集视觉方案。

---

## 门禁提醒（具有约束力）

本阶段以人工审批为门禁（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染该 artifact），并**结束本轮**。勿在同一回复中启动下一阶段。
审批按门禁逐项进行 — 更早的「继续」并不覆盖本门禁。
