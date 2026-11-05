# Idea Director - Clip Factory 流水线

## 适用场景

当素材来源为长视频，且目标是产出多条短视频交付物时使用本流水线：网络研讨会片段、访谈剪辑、直播高光、主题演讲节选或演示片段。

你不是在规划一条视频，而是在规划一组经过排序的片段组合。

## 运行时选择（必填 — 向用户说明约束，勿静默选定）

锁定 `render_runtime = "remotion"`（用于带词级字幕的合成片段）或 `"ffmpeg"`（用于纯拼接/裁剪、无合成）。**HyperFrames 在 Phase 1 中不是本流水线的有效运行时** — clip-factory 依赖 Remotion 的词级字幕烧录，目前尚无 HyperFrames 对等能力。

按 AGENT_GUIDE.md →「Present Both Composition Runtimes (HARD RULE)」：勿静默锁定 remotion。向用户说明约束：「HyperFrames 在你本机是可用的运行时，但 clip-factory 依赖 Remotion 字幕烧录，尚无 HyperFrames 对等能力，因此此处 remotion 是唯一可行选择 — 是否继续？」在 `decision_log` 中记录该决策，类别为 `render_runtime_selection`，并将 hyperframes 记为被拒绝选项（`rejected_because: "caption-burn parity deferred on clip-factory"`）。

## 参考输入

- `docs/clip-factory-best-practices.md`
- `skills/creative/short-form.md`
- `skills/creative/video-editing.md`

## 流程

### 1. 理解素材与目标

记录素材形态：

- webinar
- interview
- panel
- keynote
- stream
- customer story

再记录业务目标：

- awareness
- thought leadership
- lead generation
- product education
- event recap

### 2. 选择片段组合策略

好的批次应混合多种片段类型，而不是反复抽取同一种「能量」。

常见片段族：

- `hook`：令人意外的论断或有力的冷开场
- `insight`：实用要点或经验
- `story`：有情感弧线的叙事时刻
- `proof`：数据、案例、演示结果
- `opinion`：鲜明观点、分歧、反常识立场

在 brief 元数据中定义上述族之间的预期平衡。

### 3. 现实地设定产出目标

经验区间：

- `15-30 min`：3-6 条强片段
- `30-60 min`：5-10 条强片段
- `60+ min`：若素材质量支撑，8-15 条强片段

不要为了凑整数而虚增片段数量。少量高质量批次优于凑数的弱批次。

### 4. 在抽取前规划平台

尽早规划平台适配：

- `9:16`：Shorts、Reels、TikTok
- `1:1`：LinkedIn 及更稳妥的信息流二次利用
- `16:9`：幻灯片、演示或宽画幅上下文重要时

若源画面明显无法承受竖屏裁剪，请在 brief 元数据中现在就说明。

### 5. 构建 Brief

保持 schema 级 brief 简洁，将更丰富的批次计划放在 `brief.metadata`。

建议的 metadata 键：

- `source_type`
- `source_duration_seconds`
- `clip_target_range`
- `clip_families`
- `primary_platforms`
- `secondary_platforms`
- `selection_criteria`
- `known_visual_constraints`
- `distribution_goal`

### 6. 质量门禁

- 片段数量目标现实可行，
- 平台组合与内容匹配，
- brief 在抽取开始前已定义排序标准，
- agent 已确认任何明显的重构图限制。

## 常见陷阱

- 在质量之前按数量规划批次。
- 假设每条素材都能干净地产出竖屏片段。
- 把所有片段当作可互换，而非有意多样化。
- 未定义本批次「好片段」的标准就开始抽取。

---

## 门禁提醒（具约束力）

本阶段需人工审批（`human_approval_default: true`）。评审通过后：
以 `status="awaiting_human"` 设置 checkpoint，呈现摘要（Backlot 看板会渲染 artifact），并**结束本轮回复**。勿在同一回复中启动下一阶段。
审批按门禁逐项进行 — 更早的「继续」不覆盖本门禁。
