# 创意总监 - 虚拟形象代言人管线

## 适用场景

当交付物是主持人主导的虚拟形象视频时使用本管线：代言人短片、产品介绍、入门引导消息、内部沟通更新，或演讲者作为视觉锚点的短脚本讲解类内容。

你的首要任务是在任何人针对不可行的制作方案撰写精修文案之前，如实分类虚拟形象路径。

## 运行时选择（强制 — 呈现约束，勿静默选定）

锁定 `render_runtime = "remotion"`。**HyperFrames 在本管线 Phase 1 中不是有效运行时** — avatar-spokesperson 依赖 Remotion 的 `TalkingHead` 合成与 `remotion_caption_burn`，二者尚未具备 HyperFrames 对等能力。

按 AGENT_GUIDE.md →「Present Both Composition Runtimes（HARD RULE）」：勿静默默认。告知用户：「您的机器上可用 HyperFrames，但 avatar-spokesperson 依赖 Remotion TalkingHead 合成与字幕烧录，因此此处唯一可行运行时为 remotion — 是否继续？」记录 `render_runtime_selection` 决策，hyperframes 侧 `rejected_because: "TalkingHead + caption parity deferred on avatar-spokesperson"`。

## 参考输入

- `docs/avatar-spokesperson-best-practices.md`
- `skills/creative/storytelling.md`
- `skills/creative/short-form.md`

## 流程

### 1. 分类虚拟形象路径

记录项目实际具备的制作模式：

- `platform_avatar`
- `photo_talking_head`
- `presenter_plate_lip_sync`

同时记录虚拟形象是否已存在，或仍需在当前运行之外创建。

### 2. 定义信息形态

记录：

- 受众，
- 核心卖点或 CTA，
- 目标时长，
- 目标平台，
- 视频是以销售、入门引导、支持还是公告为主导。

代言人视频在承担单一清晰任务时效果最佳。

### 3. 把握素材现状

简报应明确说明：

- 是否提供干净旁白，
- TTS 是否可接受，
- 是否存在品牌背景或叠加层，
- 是否需要字幕，
- 是否预期多语言变体。

### 4. 构建简报

建议的元数据键：

- `avatar_path`
- `avatar_exists`
- `narration_source`
- `target_audience`
- `cta_type`
- `background_strategy`
- `deliverable_mix`
- `missing_capabilities`

### 5. 质量门

- 虚拟形象路径明确，
- 信息足够聚焦以适配代言人格式，
- 缺失的旁白或虚拟形象依赖在早期可见，
- 交付物与真实素材配置匹配。

## 常见陷阱

- 将通用生成视频请求当作确定性虚拟形象工作流处理。
- 在确认虚拟形象与旁白路径之前撰写 CTA。
- 在验证主版式之前规划多种宽高比。

---

## 门控提醒（具约束力）

本阶段以人工审批为门控（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染该产物），并**结束本轮**。勿在同一回复中启动下一阶段。
审批按门控逐项进行 — 较早的「继续」不覆盖本门控。
