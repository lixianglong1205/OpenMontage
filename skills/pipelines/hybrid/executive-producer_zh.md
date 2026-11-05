# 执行制片人 — Hybrid 流水线

## 何时使用

你是混合视频（hybrid video）的**执行制片人（Executive Producer，EP）**，该视频将源素材与精心设计或生成的辅助资产相结合。你按序编排流水线，质量门控聚焦于**源素材/辅助层平衡、叠加密度与跨媒介一致性**。

**无前期制作阶段。** 用户提供方向与源素材。EP 确保生成的辅助层起到增强作用，而非盖过源素材。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Pipeline | `pipeline_defs/hybrid.yaml` | 阶段定义 |
| Skills | 全部 7 个 director 技能 + `meta/reviewer` | 阶段执行 |
| Schemas | 全部 artifact schema | 校验 |
| Playbook | 当前启用的 style playbook | 质量约束 |

## 累积状态

```
EP_STATE:
  pipeline: hybrid
  playbook: <selected>
  target_duration_seconds: <from brief>
  budget_total_usd: <configured>
  budget_spent_usd: 0.0

  # Hybrid-specific
  anchor_medium: null         # source footage type (interview, product, screen, etc.)
  support_layers: []          # planned support types (diagrams, overlays, graphics, etc.)
  source_to_support_ratio: null  # target balance (e.g., 70/30 source/support)

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
CHECK: Anchor medium clarity
  - Is the anchor medium explicitly identified?
  - Are support layers justified (filling real gaps, not decorating)?
  - Is the source inventory realistic?
```

### SCRIPT 阶段之后：
```
CHECK: Source/support beat separation
  - Are source-led and support-led beats clearly separated?
  - Does the script avoid relying on unsupported assets?
  - Is narration/dialogue plan realistic?
```

### SCENE_PLAN 阶段之后：
```
CHECK: Source primacy
  - Does source footage remain visually primary where intended?
  - Are overlay and support layers not overloading the frame?
  - Max concurrent overlay layers: 2

CHECK: Variant planning
  - If platform variants planned: are they realistic?
  - Do aspect-ratio variants maintain readability?
```

### ASSETS 阶段之后：
```
CHECK: Source/support quality match
  - Do generated support assets match the quality level of source footage?
  - Are shared template assets reused across scenes?
  - Budget gate: 90% threshold warning
```

### EDIT 阶段之后：
```
CHECK: Anchor-cut coherence
  - Is the anchor cut coherent BEFORE support layers are added?
  - Do support visuals clarify rather than distract?
  - Is variant logic consistent across deliverables?
```

### COMPOSE 阶段之后：
```
CHECK: Output validation
  - ffprobe: duration, resolution, codec
  - Source and support layers remain balanced in the final render
  - Audio stays coherent across footage and generated elements
  - Aspect-ratio variants preserve readability
```

## 质量门控摘要

| 门控 | 阶段之后 | 检查内容 | 失败动作 |
|------|-------------|---------------|-------------|
| G1 | idea | 锚定媒介、辅助层合理性 | 修订 |
| G2 | script | 源/辅助节拍分离、旁白计划 | 修订 |
| G3 | scene_plan | 源素材优先、叠加密度、变体 | 修订 |
| G4 | assets | 质量匹配、复用、预算 | 修订 |
| G5 | edit | 锚定剪辑连贯性、辅助清晰度 | 修订 |
| G6 | compose | 平衡、变体、音频连贯性 | 修订或退回 |
| G7 | publish | 元数据、源混合标注 | 修订 |
| FINAL | all | 源/辅助平衡、可读性 | 退回 |

## 执行限制

| 限制 | 值 |
|-------|-------|
| 每阶段最大修订次数 | 3 |
| 每阶段对最大退回次数 | 1 |
| 总最大退回次数 | 3 |
| 总预算上限 | 可配置（默认 $2） |
| 总墙钟时间上限 | 12 分钟 |

## 常见陷阱

- **辅助层盖过源素材**：生成图形不应占主导。源素材是锚定。
- **叠加过载**：最多 2 层并发叠加层。更多会造成视觉噪音。
- **质量不一致**：若源为 1080p 手持拍摄而辅助为精致 4K 图形，落差会很刺眼。
- **忽视变体可读性**：在 16:9 可用的文字叠加在 9:16 可能无法阅读。
