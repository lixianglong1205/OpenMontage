# 剪辑导演 — Talking Head 流水线

## 何时使用

你已有场景计划与素材清单。你的任务是为口播（Talking Head）视频组装剪辑决策列表：主要保留完整 footage，叠加字幕，并可选用增强效果。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | 产物校验 |
| 前置产物 | 场景计划、素材清单、脚本 | 剪辑输入 |
| Playbook | 当前启用的 style playbook | 转场与节奏规则 |

## 流程

### 步骤 1：应用静音剪切（若已规划）

若场景计划包含去静音，在定义 cuts 之前先运行 `silence_cutter`：

```
silence_cutter.execute({
    "input_path": "<raw_footage>",
    "mode": "remove",           # or "speed_up" for less jarring result
    "silence_threshold_db": -35,
    "min_silence_duration": 0.5,
    "padding_seconds": 0.08,    # prevents clipped words
    "output_path": "<project>/assets/video/footage_cut.mp4"
})
```

**选择 mode：**
- `remove` — 硬切跳剪。适合快节奏社交内容（Reels、TikTok、Shorts）
- `speed_up` — 以 6 倍速快进静音段。对较长内容（YouTube、LinkedIn）观感更柔和

向用户展示结果：「已移除 X 秒静音（Y%）— 输出时长现为 Z 秒。」

将剪切后的 footage 作为后续所有步骤的源素材。

### 步骤 2：定义主 cut

对口播视频，主 cut 通常是完整 footage（或修剪后的片段）。创建 cuts 时需：
- 以原始 footage（或去静音后的 footage）为源
- 使用脚本各段对应的时间戳
- 应用修剪决策（剪掉空白、口误重录等）

### 步骤 3：配置字幕

- 启用字幕，样式与 playbook 一致
- 引用素材清单中的字幕资源
- 设置位置（通常为底部居中）

### 步骤 4：配置音频

- 将旁白设为原始 footage 音轨
- 若需要背景音乐，配置 ducking
- 按 playbook 设置音乐音量

### 步骤 5：规划增强项

若场景计划包含 overlay：
- 为文字卡、下三分之一等添加 overlay cuts
- 时间点与讲话内容对齐

### 步骤 6：自评

| 标准 | 问题 |
|-----------|----------|
| **覆盖** | cuts 是否覆盖全部预期时长？ |
| **静音** | 若已规划，是否已应用静音剪切？移除了百分之几？ |
| **字幕** | 字幕是否已启用并完成样式设置？ |
| **音频** | 音频配置是否完整？ |

### 步骤 7：提交

对照 schema 校验 edit_decisions，并通过 checkpoint 持久化。
