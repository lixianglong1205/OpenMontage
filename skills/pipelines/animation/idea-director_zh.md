# 创意总监 - 动画流水线

## 何时使用

当视频应主要通过设计好的动效来构建时使用本流水线：动态图形、动态文字（kinetic typography）、以图表为主的讲解片、数学可视化或说明性动画。

若项目实质上是素材驱动、仅带少量叠加层，则不要使用本流水线。那属于 `hybrid`。

## 参考输入

- `docs/animation-best-practices.md`
- `skills/creative/animation-pipeline.md`
- `skills/creative/storytelling.md`
- `skills/creative/ink-theater.md` — 适用于手绘 **ink「涂鸦」** 类简报：角色自绘并表演，或冷面机械装置讲解片（Ink Theater 引擎 + Ink Puppet 动作捕捉；命令 `/ink-art`）。棍状/铅笔角色行走或跳舞应走 `character-animation` 流水线。

## 流程

### 1. 分类动画模式

选择主要模式：

- `diagrammatic`
- `motion_graphics`
- `kinetic_type`
- `math_animation`
- `illustrative`
- `mixed_animation`

### 2. 尽早确定视觉路径

明确应由哪些工具承担工作：

- `diagram_gen`
- `math_animate`
- `code_snippet`
- `image_selector`
- `video_selector` 或具体的视频提供商工具
- 来源提供的素材

若所请求的模式依赖不可用工具，应立刻在简报元数据中说明。

### 3. 选择复用策略

动画在每个场景都独一无二时成本会很高。需定义：

- 复出现的母题，
- 版式体系，
- 转场族，
- 字体层级。

### 4. 撰写简报

建议的元数据键：

- `animation_mode`
- `visual_path`
- `narration_strategy`
- `reuse_strategy`
- `timing_style`
- `blocked_capabilities`

### 5. 质量门禁

- 动画模式已明确，
- 视觉路径可行，
- 项目按复用思路设计，
- 简报对缺失工具路径如实说明。

## 常见陷阱

- 把所有动画都当成一个泛化类别。
- 为每个场景规划一次性定制视觉。
- 直到资产阶段才暴露缺失的工具路径。

---

## 门禁提醒（具约束力）

本阶段需经人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 创建 checkpoint，呈现摘要（Backlot 看板会渲染该 artifact），并 **结束本轮回复**。不要在同一条回复中启动下一阶段。
批准按门禁逐项进行——此前说的「继续」不覆盖本门禁。
