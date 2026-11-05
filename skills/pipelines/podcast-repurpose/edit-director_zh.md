# 剪辑导演 - Podcast Repurpose 流水线

## 使用时机

本阶段为短视频片段以及可选的完整单集配套资产生成实际的时间线逻辑。音频仍是主要内容。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["assets"]["asset_manifest"]`, `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]` | 素材、布局、转录时间轴 |
| Playbook | 当前启用的风格 playbook | 动效与字幕规则 |

## 流程

### 1. 快速构建片段时间线

针对短视频片段：

- 以 hook 开场，
- 字幕立即出现，
- 说话人归属清晰可辨，
- 结尾收束干净利落。

### 2. 让剪辑匹配处理方案

- 源视频类片段应突出说话人构图与反应，
- audiogram 类片段应突出字幕、说话人身份与节奏，
- 以金句为主的片段应在句子落地后保留足够的阅读时间。

### 3. 完整单集配套保持简单

若需制作：

- 使用章节卡片，
- 使用有限且可重复使用的视觉体系，
- 若素材不足，不要强行追求持续不断的视觉新意。

### 4. 用元数据丰富时间线备注

推荐的元数据键：

- `clip_timelines`
- `quote_hold_times`
- `speaker_change_markers`
- `chapter_card_windows`

### 5. 质量门禁

- 每个短视频片段都能快速 hook，
- 字幕与归属信息齐全，
- 金句类片段停留时长足够阅读，
- 长形式配套在编辑上诚实、在技术上可行。

## 常见陷阱

- 制作泛化的 audiogram，却忽略谁在说话。
- 金句片段在音频一结束就切走，文字尚未读完。
- 把长形式配套做成对全制作水准视频播客的拙劣模仿。
