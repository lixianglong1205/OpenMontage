# 剪辑总监 - 电影感流水线

## 何时使用

本阶段将节拍图（beat map）转化为有节奏的电影感时间线。节奏与克制比特效数量更重要。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | 产物校验 |
| 先前产物 | `state.artifacts["assets"]["asset_manifest"]`、`state.artifacts["scene_plan"]["scene_plan"]`、`state.artifacts["script"]["script"]` | 资产、主帧、节拍图 |
| Playbook | 当前风格手册 | 字体与转场一致性 |

## 流程

### 1. 先按情绪剪辑

剪辑应遵循：

- 情绪重点，
- 揭晓时机，
- 音乐转折，
- 视觉对比。

不要只为信息密度而优化。

### 2. 保护强时刻

若某个画面、台词或手势本身已足够有力，就让它留足呼吸空间。不要用额外插入镜头过度覆盖。

### 3. 用声音推动剪辑

环境声、冲击音、骤停以及音乐变化，应帮助在场景之间建立动势。

### 4. 用元数据承载 timing 逻辑

推荐的 metadata 键：

- `beat_timing`
- `audio_turns`
- `title_card_windows`
- `reframe_notes`

### 5. 质量门禁

- 情绪弧线完整，
- 揭晓清晰落地，
- 标题卡稀疏且有意图地卡点，
- 强时刻未被覆盖镜头淹没。

## 常见陷阱

- 对情绪向素材过度剪辑。
- 默认使用变速或花哨转场。
- 用标题卡替代剪辑层面的清晰度。
