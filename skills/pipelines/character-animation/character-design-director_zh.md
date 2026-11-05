# 角色设计导演 - 角色动画流水线

## 目标

产出 `character_design`：一小群角色，具有清晰的剪影、角色定位、情感、动作与风格锚点。

> **手绘墨水「涂鸦」角色？**（会先自画再行走/跳舞/挥手/跳跃的棍人/铅笔小人）→ 使用 **Ink Puppet** 系统：`skills/creative/ink-theater.md` + `ink-theater/README.md`。该绑定与比例无关，并通过 `InkPuppet.choreograph([{clip:'wave'},{clip:'twist'},…])` 播放**真实动捕**片段——片段名称来自 `ink-theater/mocap/catalog.json`（12 个 CMU 来源动作）；智能体只选择命名动作，**从不手工微调动作**；用 `node ink-theater/mocap/add-motion.mjs` 添加动作。命令：`/ink-art`。

## 流程

1. 列出每个角色的 `id`、角色定位、体型与风格。
2. 确定故事所需的最小情感范围。
3. 确定故事所需的最小动作列表。
4. 决定所需视角：正面、3/4、侧面、背面。MVP 限制为一到两个视角。
5. 记录角色携带的道具，如围巾、羽毛、包、眼镜。

## 约束

- 一到两个角色是 MVP 的最佳点。
- 动物角色需要物种特定的部件与动作循环。
- 更多视角会成倍增加资产与姿势需求。
- 不要设计超过已批准时长能使用的姿势数量。

## 工具使用

使用 `character_spec_generator` 生成结构化草案。仅在视觉风格与角色表需求明确后，才使用 `image_selector`。在使用图像生成之前，从 registry 阅读该工具的 Layer 3 skills。

## 质量门槛

只有当动画师或工具能推断出必须存在哪些部件、表情与动作时，角色设计才算就绪。

---

## 门控提醒（具约束力）

本阶段门控于人工审批（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染该产物），并**结束本轮**。不要在同一回复中开始下一阶段。
审批按门控逐项进行——更早的「继续」不代表覆盖本门控。
