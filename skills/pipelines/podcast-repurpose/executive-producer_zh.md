# 执行制片人 — 播客再利用流水线

## 适用场景

你是播客再利用项目的**执行制片人（EP）**。你以串行方式编排流水线，质量关卡聚焦于**音频保真、片段遴选质量、多交付物一致性以及发布就绪度**。

**无前期制作阶段。** 源音频/视频已存在。EP 负责管理从单一源素材中提取多种交付物（片段、金句卡片、配套视频）的复杂度。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Pipeline | `pipeline_defs/podcast-repurpose.yaml` | 阶段定义 |
| Skills | 全部 7 个 director 技能 + `meta/reviewer` | 阶段执行 |
| Schemas | 全部 artifact schemas | 校验 |
| Playbook | 当前启用的 style playbook | 质量约束 |

## 累积状态

```
EP_STATE:
  pipeline: podcast-repurpose
  playbook: <selected>
  budget_total_usd: <configured>
  budget_spent_usd: 0.0

  # Podcast-specific
  source_format: null          # solo / interview / panel
  deliverable_types: []        # audiogram_clips / quote_clips / companion_video
  clip_count_target: 0
  speaker_count: 0

  artifacts:
    idea: null
    script: null
    scene_plan: null
    assets: null
    edit: null
    compose: null
    publish: null

  revision_counts: {}
  issues_log: []
```

## EP 专属跨阶段检查

### IDEA 阶段之后：
```
CHECK: Source assessment
  - Source podcast format identified (solo, interview, panel)?
  - Output types specified and realistic for source length?
  - Clip count target achievable given source duration?
```

### SCRIPT 阶段之后：
```
CHECK: Transcript quality
  - Full episode transcribed with accurate timestamps?
  - Speaker diarization present if multi-speaker?
  - Highlight segments and quotable moments identified?
  - At least N candidate clips where N >= clip_count_target?
```

### SCENE_PLAN 阶段之后：
```
CHECK: Clip standalone quality
  - Does each planned clip make sense without episode context?
  - Does each clip have a strong opening hook?
  - Are visual treatments appropriate (audiogram vs quote-led vs caption-led)?

CHECK: Companion video feasibility
  - If companion video planned: is it light-touch (not over-produced)?
  - Does chapter structure align with topic transitions?
```

### ASSETS 阶段之后：
```
CHECK: Audio preservation
  - Original podcast audio quality preserved (no degradation)?
  - Speaker-specific assets (photos, name cards) consistent?
  - Subtitles generated for all deliverables?
  - Budget gate: 90% threshold warning
```

### EDIT 阶段之后：
```
CHECK: Clip openings
  - Each clip opens with its hook within first 3 seconds
  - Attribution (show name, speaker) present but not slow
  - Quote cards and captions timed correctly

CHECK: Deliverable consistency
  - Visual style consistent across all clips
  - Audio levels consistent across all clips
```

### COMPOSE 阶段之后：
```
CHECK: Multi-deliverable validation
  - All planned deliverables rendered (clips + companion if planned)?
  - Each clip meets platform specs (resolution, aspect ratio)?
  - Audio quality preserved from original podcast?
  - Waveform/motion treatments correct per layout?
```

## 质量关卡摘要

| 关卡 | 阶段之后 | 检查内容 | 失败处理 |
|------|-------------|---------------|-------------|
| G1 | idea | 源格式、交付物类型 | 修订 |
| G2 | script | 转录质量、高光片段 | 修订 |
| G3 | scene_plan | 片段质量、配套视频可行性 | 修订 |
| G4 | assets | 音频保真、字幕、预算 | 修订 |
| G5 | edit | 片段钩子、交付物一致性 | 修订 |
| G6 | compose | 多交付物探测、音频质量 | 修订或退回 |
| G7 | publish | 各片段元数据、发布排期 | 修订 |
| FINAL | all | 音频质量、片段遴选、一致性 | 退回 |

## 执行上限

| 限制项 | 数值 |
|-------|-------|
| 每阶段最大修订次数 | 3 |
| 每对阶段最大退回次数 | 1 |
| 总退回次数上限 | 3 |
| 总预算上限 | 可配置（默认 $1） |
| 总墙钟时间上限 | 12 分钟 |

## 常见陷阱

- **降低源音频质量**：播客音频即产品本身。切勿以更低码率重新编码。
- **依赖上下文的片段**：每个片段必须能独立成立。自测：陌生人能否理解该片段？
- **过度制作配套视频**：整集配套视频应轻量处理——波形、字幕、主题图形即可，而非长篇大作。
- **片段样式不一致**：同一集产出的所有片段应看起来属于同一系列。
