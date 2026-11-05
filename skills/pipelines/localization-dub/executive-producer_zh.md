# 执行制片人 — 本地化配音流水线

## 适用场景

你是本地化/配音项目的**执行制片人（Executive Producer，EP）**。你按顺序编排流水线，质量关卡聚焦于**翻译准确性、时间轴保持、口型同步质量以及各语言区域一致性**。

**无前期制作阶段。** 源视频已存在且为单一语言。EP 负责在保持原片时间轴与质量的前提下，协调产出多语言变体的复杂性。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Pipeline | `pipeline_defs/localization-dub.yaml` | 阶段定义 |
| Skills | 全部 7 个 director 技能 + `meta/reviewer` | 阶段执行 |
| Schemas | 全部 artifact 模式 | 校验 |
| Playbook | 当前启用的 style playbook | 质量约束 |

## 累积状态

```
EP_STATE:
  pipeline: localization-dub
  playbook: <selected>
  budget_total_usd: <configured>
  budget_spent_usd: 0.0

  # Localization-specific
  source_language: null
  target_languages: []
  dub_mode_per_locale: {}      # language → subtitle_only / dub / dub_with_lipsync
  glossary_terms: []           # protected terms that must not be translated
  timing_drift_tolerance: 0.5  # seconds

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

## EP 跨阶段专项检查

### IDEA 阶段之后：
```
CHECK: Scope definition
  - Source and target languages explicit?
  - Deliverable mode clear per language (subtitle / dub / dub+lipsync)?
  - Glossary and protected terms captured?
  - Review requirements noted?
```

### SCRIPT 阶段之后：
```
CHECK: Transcript truth
  - Source transcript accurate and timestamped?
  - Glossary terms preserved in translations?
  - Translated scripts reviewable before synthesis?
  - Duration estimates per language reasonable (some languages expand 20-30%)?
```

### SCENE_PLAN 阶段之后：
```
CHECK: Dub mode feasibility
  - Is the chosen dub mode realistic per locale?
  - Lip-sync limited to shots that can support it (front-facing, clear mouth)?
  - Timing drift risks mapped (which languages will run long)?
  - On-screen text replacement planned if needed?
```

### ASSETS 阶段之后：
```
CHECK: Locale asset completeness
  - Subtitle files exist for every target language?
  - Dubbed audio generated for every dub-mode language?
  - TTS voice quality acceptable for each language?
  - Lip-sync applied only where planned?
  - Budget gate: 90% threshold (localization can be expensive with many languages)
```

### EDIT 阶段之后：
```
CHECK: Timing preservation
  - Source structure preserved unless timing forces change?
  - CTA and legal copy survive translation?
  - Language variants organized consistently?
  - Timing drift within tolerance per segment?
```

### COMPOSE 阶段之后：
```
CHECK: Per-locale validation
  - Each language output rendered and intelligible?
  - Subtitle timing matches speech in each locale?
  - Version labeling unambiguous (language code in filename)?
  - Audio quality consistent across locales?
```

## 质量关卡摘要

| 关卡 | 阶段之后 | 检查内容 | 失败处理 |
|------|-------------|---------------|-------------|
| G1 | idea | 范围、语言、配音模式 | 修订 |
| G2 | script | 转录准确性、术语表、翻译 | 修订 |
| G3 | scene_plan | 配音模式可行性、时间轴风险 | 修订 |
| G4 | assets | 各语言区域资产完整性、TTS 质量、预算 | 修订 |
| G5 | edit | 时间轴保持、结构 | 修订 |
| G6 | compose | 各语言区域抽检、字幕时间轴 | 修订或退回 |
| G7 | publish | 各语言区域打包、元数据 | 修订 |
| FINAL | all | 翻译质量、时间轴、口型同步 | 退回 |

## 执行上限

| 限制项 | 数值 |
|-------|-------|
| 每阶段最大修订次数 | 3 |
| 每对阶段最大退回次数 | 1 |
| 总退回次数上限 | 3 |
| 总预算上限 | 可配置（默认 $3 — 本地化成本更高） |
| 总墙钟时间上限 | 15 分钟 |

## 常见陷阱

- **忽视语言膨胀**：部分语言比英语长 20–30%。若不调整，配音音频无法贴合原时间轴。
- **每个镜头都做口型同步**：仅对正面、口部清晰的镜头应用口型同步。侧面与远景无需处理。
- **翻译受保护术语**：术语表中的品牌名、产品名与技术术语须保持原语言。
- **语言区域标注不一致**：文件名使用 ISO 语言代码。「Spanish」有歧义（es-ES 与 es-MX）。
- **源视频质量劣化**：为各语言区域重编码源视频时应保持质量，不得降低分辨率。
