# Scene Director - Hybrid Pipeline

## 适用场景

你要把 hybrid 结构转译成一套视觉体系：源素材保持可见，辅助层受控。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["script"]["script"]`, `state.artifacts["idea"]["brief"]` | Hybrid 结构与源素材事实依据 |
| 工具 | `frame_sampler`, `scene_detect` | 可选的源素材检视 |
| Playbook | 当前启用的 style playbook | 版式一致性 |

## 流程

### 1. 让锚定媒介保持可见

若作品以源素材为主导，场景计划中源素材必须在视觉上占主位。不要用持续叠加层把锚定内容藏起来。

### 2. 辅助层只做明确分工

辅助场景用于：

- 章节转场，
- 说明性示意图，
- 数据/统计强调，
- CTA 或总结时刻，
- 填补空白的插入镜头。

### 3. 规划多画幅变体安全区

若项目需要多种宽高比，需明确：

- 字幕位置，
- 讲者标签位置，
- 图表或代码安全区，
- 哪些源素材在裁剪后不再适用。

### 4. 用元数据定义平衡规则

建议的 metadata 键：

- `anchor_rules`
- `support_rules`
- `safe_zones`
- `variant_rules`
- `overlay_density_limits`

### 5. 质量门禁

- 锚定媒介在预期处仍为主视觉，
- 辅助层数量受限且目的明确，
- 宽高比规划写清楚，
- 没有任何场景依赖「以后再说」的隐形能力。

## 常见陷阱

- 把源素材主导场景做成叠加层堆叠。
- 到 compose 阶段才想起变体安全区。
- 每个转场都用生成插入镜头。

---

## 门禁提醒（具约束力）

本阶段需人工审批（`human_approval_default: true`）。评审通过后：
以 `status="awaiting_human"` 做 checkpoint，提交摘要（Backlot 看板会渲染该产物），并**结束本轮**。不要在同一回复里启动下一阶段。
审批按门禁单独计算——此前说的「继续」不覆盖本门禁。
