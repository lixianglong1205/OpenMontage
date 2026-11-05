# 剪辑导演 — 解说类 Pipeline

## 何时使用

你是已生成解说视频的剪辑师。你拥有包含全部生成文件的 `asset_manifest`、描述视觉结构的 `scene_plan`，以及带时间信息的 `script`。你的任务是组装剪辑决策列表（EDL，Edit Decision List）：什么在何时播放、元素如何叠层、字幕放在哪里，以及音乐与旁白如何配合。

这里是原始素材变成连贯成片的地方。好的剪辑能让普通素材出彩；差的剪辑会浪费优质素材。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["assets"]["asset_manifest"]`、`state.artifacts["scene_plan"]["scene_plan"]`、`state.artifacts["script"]["script"]` | 素材、视觉方案、时间轴 |
| Playbook | 当前启用的风格 playbook | 转场、节奏规则、叠加层样式 |

## 流程

### 步骤 1：将素材映射到时间轴

对 scene plan 中的每个场景：
1. 从 asset manifest 中找到对应素材（按 `scene_id`）
2. 找到对应的旁白音频（按 script 段落）
3. 记录该场景的时间（`start_seconds`、`end_seconds`）

构建时间轴映射：
```
0s-10s: scene-1 (talking_head) | narration-s1 | img-intro.png
10s-18s: scene-2 (diagram) | narration-s2 | diagram-flow.svg
18s-22s: scene-3 (text_card) | narration-s3 | [text overlay]
...
```

### 步骤 2：定义镜头（Cuts）

每个 cut 定义在何时展示何种画面：

```json
{
  "id": "cut-1",
  "source": "img-scene-1",
  "in_seconds": 0,
  "out_seconds": 10,
  "layer": "primary",
  "transform": {
    "scale": 1.0,
    "position": "center",
    "animation": "ken-burns-slow-zoom"
  },
  "transition_in": "fade",
  "transition_out": "dissolve",
  "transition_duration": 0.4
}
```

**叠层规则：**
- `primary` — 主画面（同一时刻仅一个）
- `overlay` — 文字卡、数据卡、关键术语（叠在主画面上方）
- `background` — 纯色或纹理，位于最底层

### 步骤 3：配置字幕

所有解说类内容必须启用字幕：

```json
{
  "subtitles": {
    "enabled": true,
    "style": "word-by-word",
    "font": "Inter",
    "font_size": 48,
    "color": "#FFFFFF",
    "background": "#00000088",
    "position": "bottom-center",
    "max_words_per_line": 8
  }
}
```

**字幕时间**：从旁白音频时间戳推导。每个词应在被念出时高亮（逐词 style）或按短语成块显示（phrase style）。

字体选用 playbook 中的 typography 设置。

### 步骤 4：配置音频层

```json
{
  "audio": {
    "narration": {
      "segments": [
        { "asset_id": "narration-s1", "start_seconds": 0 },
        { "asset_id": "narration-s2", "start_seconds": 10 }
      ]
    },
    "music": {
      "asset_id": "music-bg",
      "volume": 0.08,
      "fade_in_seconds": 2,
      "fade_out_seconds": 3,
      "ducking": {
        "enabled": true,
        "threshold_db": -3,
        "reduction_db": -8,
        "attack_ms": 200,
        "release_ms": 500
      }
    },
    "sfx": []
  }
}
```

**音乐闪避（ducking）**：旁白播放时降低音乐音量，停顿处回升。使用 playbook 的 `audio.ducking_threshold_db`。

### 步骤 5：应用节奏规则

查阅 playbook 的 `motion.pacing_rules`：
- 单个 cut 时长不得短于 `min_scene_hold_seconds`
- 单个 cut 时长不得长于 `max_scene_hold_seconds`
- 文字卡停留 `text_card_hold_seconds`
- 转场使用 `transition_duration_seconds`

若有 cut 违反上述规则，调整其时间。

### 步骤 6：校验剪辑完整性

**时间轴覆盖：**
- [ ] Cuts 覆盖整段视频时长（无黑场）
- [ ] 无重叠的 primary cuts
- [ ] scene_plan 中每个场景至少对应一个 cut

**素材引用：**
- [ ] 每个 cut 的 `source` 引用 manifest 中有效的 asset_id
- [ ] 每个旁白段落引用有效的音频素材
- [ ] 音乐素材存在

**音画同步：**
- [ ] 旁白段落有序且不重叠
- [ ] 旁白时间与对应画面 cut 对齐
- [ ] 已配置音乐 ducking

**字幕：**
- [ ] 字幕已启用
- [ ] 字幕样式使用与 playbook 兼容的字体与颜色

### 步骤 7：自评

打分（1–5）：

| 维度 | 问题 |
|-----------|----------|
| **连贯性** | 视频每一秒是否都有画面？ |
| **节奏** | Cuts 是否遵循 playbook 的时间规则？ |
| **音画同步** | 所见是否与所闻在每一刻一致？ |
| **字幕质量** | 字幕是否易读且时间准确？ |
| **转场一致性** | 转场是否在 playbook 允许集合内？ |

任一维度低于 3 分则修订。

### 步骤 8：提交

对照 schema 校验 edit_decisions 产物，并通过 checkpoint 持久化。

## 常见陷阱

- **遗漏空隙**：若 scene-1 在 10s 结束而 scene-2 在 10.5s 才开始，会出现 0.5s 黑场。务必检查空隙。
- **音频漂移**：旁白实际时长可能略长或略短于计划。应按实际旁白时长调整画面 cut，而非仅按计划时长。
- **未做 ducking**：旁白下音乐全音量会让视频难以观看。务必配置 ducking。
- **处处同一转场**：变化转场能形成节奏。使用 playbook 允许集合，但不要每个 cut 都用同一种。
- **字幕字体不一致**：字幕应使用 playbook 的正文字体，而非随意默认字体。
