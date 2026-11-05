# 剪辑导演 - 纪录片蒙太奇流水线

## 何时使用

每个槽位都已选定片段。接下来要把一堆片段拼成一件作品。本阶段决定入点、出点、转场、音乐同步，以及片段的实际播放顺序。输出为带具体时间线的 `edit_decisions` 制品。

纪录片技法就体现在这里。若素材导演（asset director）工作到位，你已有 raw material；剪辑才是思考所在。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | 制品校验 |
| 前置制品 | `state.artifacts["assets"]["asset_manifest"]` | 已选片段 + 音乐床 |
| 前置制品 | `state.artifacts["scene_plan"]["scene_plan"]` | 槽位顺序、hero 标记、目标 hold |
| 前置制品 | `state.artifacts["idea"]["brief"]` | 调性 register、时长、结构 shape |
| 工具（可选） | `video_analyzer` | 需复核时探测片段运动 |

## 心智模型

纪录片蒙太奇要在四个维度上取得平衡：

1. **节奏（Rhythm）** — 每个 hold 持续多久，以及 hold 之间的关系。
2. **并置（Juxtaposition）** — 哪张画面接哪张，以及接在一起意味着什么。
3. **音乐同步（Music sync）** — 切点落在节拍上，留白（dropout）才有重量。
4. **调性连续（Continuity of register）** — 颗粒、色彩、年代感不要乱跳，除非乱跳本身就是意图。

敌人是「幻灯片感」—— 片段背靠背播放、hold 长度相同、没有声音设计。若像幻灯片，剪辑即失败，与片段本身多优秀无关。

本阶段还会锁定渲染语法（render grammar）。纪录片蒙太奇须将 `renderer_family` 设为 `documentary-montage`，以便 compose 阶段留在已批准的 Remotion 优先路径上。

## 流程

### 0. 护栏 — 禁止静默的重大变更

动时间线之前，重读 brief。若出现以下任一情况，**停止**，并按决策沟通契约（Decision Communication Contract）向用户说明：

- brief 已批准「无旁白」，但剪辑感觉需要画外音。旁白属于**重大变更**。
- brief 已批准某条音乐轨，剪辑导演现在想换掉。换音乐属于**重大变更**。
- brief 批准 90 秒时长，但自然剪接需要 2 分 30 秒。拉长时长属于**重大变更**。

修正剪辑，不要掩盖。若剪辑确实需要其中一项，请先询问。

### 1. 设定节奏网格

读取 `brief.tone` 与 `brief.duration_seconds`。按场景导演的调性表计算 hold 表：

| 调性 | Base hold | Min hold | Max hold |
|------|-----------|----------|----------|
| elegiac | 4.0s | 2.5s | 7.0s |
| reverent | 3.5s | 2.0s | 6.0s |
| dreamlike | 3.0s | 1.5s | 5.5s |
| wry | 2.0s | 1.0s | 4.0s |
| urgent | 1.2s | 0.5s | 2.5s |

**Hero 槽位用 max hold。** 中段 cutaway 用 base。快切过渡用 min。

总 hold 时长须在 `brief.duration_seconds` 的 ±10% 以内。若超出，先压缩非 hero 的 hold — 绝不为凑时长而缩短 hero。

### 2. 按叙事节拍排列，而非按分数

场景导演给了槽位顺序，该顺序即意图。不要按 CLIP 分数、运动分数或分辨率重排。

**可以**重排槽位的情况：

- 音乐床在已知时间戳有 downbeat，重排两个槽位能让 hero 落在节拍上（见步骤 4）。
- 相邻两槽视觉几乎相同，互换其一可打破单调（但见步骤 7 — diversify 本应已处理）。
- 终镜撑不住。最后 5–10 秒权重 disproportionate；若场景导演之选失效，把更强候选移到片尾。

凡重排，须在 `edit_decisions.metadata.reorder_notes` 中记录原因。

### 3. 按节拍 trim 每个片段

对每个已选片段决定 `in_seconds` 与 `out_seconds`。三条规则：

- **找最佳子窗口，而非整段。** 12 秒的 Pexels 片段通常只有约 3 秒值得 hold，其余是铺垫/收束。找到那个 moment。
- **在动作自然结束前切。** 停在目光、而非移开。切点才有意图感，而非「播完了」。
- **两端留 handle。** 4–6 帧 headroom，便于 composer 做 fade 或 dissolve 而不裁掉 moment。

若片段太短，填不满目标 hold，可以：

- 减速（speed 0.5–0.75，静态画面尚可，有 sync 运动或说话人脸则差），
- 提前切，从下一槽 hold 借剩余时长，
- 或换 rejected-picks 日志中的 #2 候选。

**不要**停在最后一帧定帧。纪录片蒙太奇里的定帧像技术失误。

### 4. 与音乐床同步

从 `asset_manifest` 读取音乐资源及其时长。纪录片蒙太奇的情感重量常来自切点落在音乐事件上。三种同步手法：

- **Downbeat 切。** 若有 bars/beats 元数据（来自提供的轨）或能听出，把 hero 切点放在 downbeat 上。否则，对 60bpm 床以约 4s 间隔均匀切是稳妥默认。
- **一次 held silence。** 在作品情感中心约 2s 让音乐 dropout。沉默是工具。用一次，用狠。
- **尾部 fade。** 最后 3–5s 音乐渐弱，让终镜呼吸，不与 musical resolution 打架。

在 `edit_decisions.audio.music` 中记录音乐配置：

```json
{
  "asset_id": "asset_music_bed",
  "volume": 0.7,
  "fade_in_seconds": 1.0,
  "fade_out_seconds": 4.0,
  "ducking": false
}
```

本流水线默认 `ducking: false` — 无旁白可 duck。若用户批准旁白轨，设 `ducking: true`，在段落期间压低音乐。

### 5. 从小词汇表选转场

纪录片蒙太奇整片大概只用四种转场：

| 转场 | 用途 |
|------------|-----|
| `cut`（硬切） | 默认。多数切为硬切。 |
| `dissolve`（0.5–1.0s） | 情感相近的 sibling 片段、时间流逝 |
| `fade_to_black`（0.5s，再升起） | 三幕结构中的幕间，或片尾附近用一次 |
| `fade_in`（首镜）/ `fade_out`（末镜） | 0.5–1.0s 片头片尾 |

**不要使用：**

- wipe，
- push/slide 转场，
- zoom blur，
- RGB split，
- light leak，
- glitch 效果。

这些像社交媒体剪辑语言，会破坏纪录片调性 register。若成片乏味，改选片或节奏 pacing，不要加转场花哨效果。

按 schema 记录每个 cut 的 `transition_in` / `transition_out`。多数切默认 `transition_in: "cut"`。

### 6. 应用调性连续

混合年代语料视觉差异极大。Pexels 2023 干净、锐利、调色；Prelinger 1962 颗粒、暖、方画幅；NASA 档案常低清带字卡。若 raw 硬拼，会像 Wikipedia 条目。

两种平滑手段：

1. **裁成统一画幅。** 选一：16:9 电影感（hero 用上下 `2.35:1` letterbox），或 9:16 社交。在每个 cut 的 `transform.crop` 中强制。
2. **在 compose 时标统一调色。** 在 `edit_decisions.metadata` 放 `grade_profile` 提示，compose 导演会对整时间线套 LUT。

不要在此对单 clip 调色，那是 compose 阶段。你的工作是标出需求。

### 7. 再次强制相邻多样性

成对 walk 时间线。对每个连续 (cut_n, cut_n+1)：

- 是否同一主体、同一 scale？若是，即 slideshow moment。换其一为不同 scale（wide vs close）。
- 是否同一色盘（两个 night-blue 连播）？若是，至少每 4 切打破一次。
- 是否同一运动方向（两个左→右 pan）？若是，翻转第二段的 horizontal axis 或重排。

在 `metadata.diversity_swaps` 记录任何互换。

### 8. L-Cut 手法（可选但有力）

任两 clip 之间，若出画 clip 有强环境声（雨、脚步、车流），将音频 carry 到入画 clip 下 0.5–1.5s。这是 L-cut，比任何视觉转场更能焊合两镜。

通过 schema：短 `dissolve` 转场，或在 `edit_decisions.audio.sfx`  layering 出画 clip 音频为 SFX，延迟 end。

带 L-cut 的纪录片蒙太奇比没有的连贯约多 50%。在片中最难的三四个过渡上使用。

### 8b. 放置 End-Tag 叠加

若 `brief.metadata.end_tag_plan.mode == "overlay"`（默认），end-tag 在 compose 时叠在最终 body 画面上。剪辑导演要决定**何时**出现 tag。

计算偏移：`offset_seconds = body_duration - tag_duration`。使 tag 的 fade-out 与 body 收尾 fade-out（最后一 cut 的 `transition_out: fade_out`）对齐。若最终 cut 的 hold 短于 tag 时长，可更早开始 tag，与倒数第二 cut 重叠 — 常更好看。

记录在 `edit_decisions.end_tag`：

```json
{
  "end_tag": {
    "offset_seconds": 84.5,
    "notes": "Tag starts at body_duration - tag_duration. Aligns tag fade-out with final cut fade-out."
  }
}
```

若 `mode == "concat"`，省略本节 — compose-director 会在 body 后 append tag，无需 timing offset。

### 9. 输出 Edit Decisions

本流水线规范形态：

```json
{
  "version": "1.0",
  "renderer_family": "documentary-montage",
  "cuts": [
    {
      "id": "cut_01",
      "source": "asset_slot_01",
      "in_seconds": 1.2,
      "out_seconds": 5.2,
      "layer": "primary",
      "transform": { "scale": 1.0, "position": "center" },
      "transition_in": "fade_in",
      "transition_out": "cut",
      "transition_duration": 0.8,
      "reason": "opening hero — raindrop on asphalt, 4s hold, slow-motion streetlamp glow"
    },
    {
      "id": "cut_02",
      "source": "asset_slot_02",
      "in_seconds": 2.0,
      "out_seconds": 5.5,
      "layer": "primary",
      "transition_in": "cut",
      "transition_out": "cut",
      "reason": "umbrella opening in doorway, hard cut from raindrop → street"
    }
  ],
  "audio": {
    "music": {
      "asset_id": "asset_music_bed",
      "volume": 0.7,
      "fade_in_seconds": 1.0,
      "fade_out_seconds": 4.0,
      "ducking": false
    }
  },
  "end_tag": {
    "offset_seconds": 84.5,
    "notes": "Tag starts at body_duration - tag_duration. Aligns tag fade-out with final cut fade-out."
  },
  "metadata": {
    "pipeline": "documentary-montage",
    "tone": "elegiac",
    "shape": "list",
    "total_duration_seconds": 90.0,
    "hold_table_used": { "base": 4.0, "min": 2.5, "max": 7.0 },
    "grade_profile": "warm_film_100",
    "reorder_notes": [],
    "diversity_swaps": [
      { "at": "cut_07-cut_08", "reason": "two wide rooftops-in-rain adjacent, swapped 08 for #2 pick" }
    ],
    "silence_window": { "start_seconds": 54.0, "end_seconds": 56.0 },
    "l_cuts": [
      { "from_cut": "cut_05", "to_cut": "cut_06", "carry_seconds": 1.2, "channel": "ambient_rain" }
    ]
  }
}
```

### 10. 质量门

- `sum(out - in for cut in cuts)` 在 `brief.duration_seconds` 的 ±10% 内。
- `renderer_family = "documentary-montage"` 存在且未改。
- Hero 槽位 hold 最长。
- 无两个相邻 cut 同时相同 subject **且** scale。
- 转场词汇表至多 4 个 distinct 值。
- 存在 music config（或 brief 明确无音乐）。
- 时长 ≥ 60s 的作品至少一条 `silence_window`。
- 每个 cut 有一行 `reason` — 写不出则说明 cut 随意，应重考。
- `metadata.total_duration_seconds` 与 cut 时长之和一致。

## 常见陷阱

- **按信息密度切而非按节奏。** 纪录片蒙太奇不是 Wikipedia 条目。「但我必须展示这个」不是理由 — 若画面撑不住 hold，就不该留。
- **过度 dissolve。** 每切都 dissolve 像在说不愿 commit。要 commit。
- **到最后才管音乐床。** 音乐不是 compose 时撒的糖，而是你要切上去的 timing grid。
- **终镜选弱。** 最后一帧被记住的比例 disproportionate。若弱，换掉 — 场景导演的槽位顺序是强建议，不是契约。
- **定帧结尾。** 像技术错误。改用 fade-to-black。
- **因剪辑偏薄静默加旁白。** 重大变更。要问。
- **在 cuts 里隐藏 clip provider。** 每个 `cut.source` 必须是 `asset_manifest` 的 asset_id，溯源才能保留。
- **前 15 秒三种不同转场。** 观众会感到剪辑在「表演」。克制才是品牌。

## 节奏示例 — 「雨中一分钟」

90 秒，elegiac，list shape，15 个 hero 标记槽位。

- Base hold 4.0s × 15 = 60s。缺 30s。
- 在 3 个 hero 槽（1、11、15）各 +10s：hero_1 = 5.5s，hero_11 = 6.0s，hero_15 = 7.0s。
- 槽 4、7、13 收紧到 3.0s（小 cutaway）。
- 插入 silence_window 54.0–56.0s（hero_11 之前）。
- L-cut slot_10（靴踩水洼）→ slot_11（街对面亮窗），carry rain-on-glass ambient 1.2s。
- 首 cut `fade_in` 1.0s，末 cut `fade_out` 1.5s。
- 其余全硬切。
- 音乐 fade in 1.0s，在 hero_15 + black 下 fade out 4.0s。

得到 90s 作品，三个呼吸点（fade_in、silence、fade_out），清晰 hero 弧（槽 1 → 11 → 15），无相邻 scale 碰撞。

---

## 关卡提醒（具约束力）

本阶段关卡需人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` checkpoint，呈现摘要（Backlot board 渲染制品），并**结束本轮**。勿在同一回复中启动下一阶段。
批准按关卡计 — 较早的「继续」不覆盖本关卡。
