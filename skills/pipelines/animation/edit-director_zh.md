# 剪辑导演 - 动画流水线

## 何时使用

本阶段将场景计划转化为动画样片级别的剪辑计划。节奏本身就是产品。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["assets"]["asset_manifest"]`, `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]` | 素材、时间计划与节拍 |
| Playbook | 当前启用的风格 playbook | 动效与版式规则 |

## 流程

### 1. 保护停留时间

关键信息揭示之后，要留出足够时间让观众消化画面。不要把每个场景首尾相连、全程塞满动效。

### 2. 错开次要元素

主元素先行，辅助元素随后。剪辑决策应强化层级关系。

### 3. 让动效有意义

动效应传达：

- 强调，
- 过渡，
- 变换，
- 对比。

### 4. 用元数据细化时间

推荐的 metadata 键：

- `hold_windows`
- `stagger_rules`
- `transition_map`
- `scene_timing_notes`

### 5. 质量门禁

- 关键信息有足够的停留时间，
- 运动能厘清层级，
- 转场保持一致，
- 在目标平台上剪辑仍清晰可读。

## 常见陷阱

- 时间轴上堆满连续动效。
- 所有元素同时揭示。
- 风格化动效损害可读性。
