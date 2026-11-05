# 剪辑导演 - 混合流水线（Hybrid Pipeline）

## 适用场景

本阶段为「以源素材为主导、辅以支持元素」的视频建立分层剪辑逻辑。顺序很重要：先锁定主剪辑（anchor cut），再叠加支持层。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["assets"]["asset_manifest"]`, `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]` | 源/支持素材与时间线意图 |
| Playbook | 当前启用的风格 playbook | 字体与动效一致性 |

## 流程

### 1. 先锁定主剪辑（Anchor Cut）

观众应在加入支持层叠加之前就能理解故事。若主剪辑薄弱，支持层救不回来。

### 2. 按优先级叠加支持层

典型顺序：

1. 字幕，
2. 讲者或情境标签，
3. 示意图或数据卡片，
4. 可选插入镜头，
5. CTA 元素。

### 3. 保护可读性

同一时刻不要堆叠过多支持层。若字幕、标签、图表与叠加层互相冲突，应做简化。

### 4. 用元数据表达分层逻辑

建议的 metadata 键：

- `anchor_cut_notes`
- `layer_order`
- `overlay_windows`
- `variant_edit_rules`

### 5. 质量门禁

- 主剪辑单独成立即可观看，
- 支持层是澄清信息而非分散注意力，
- 移动端可读性仍过关，
- 各平台变体保持一致的剪辑思路。

## 常见陷阱

- 试图用额外图形弥补薄弱剪辑。
- 让支持层与源素材抢戏。
- 把每个平台变体当成一套独立的剪辑哲学来制作。
