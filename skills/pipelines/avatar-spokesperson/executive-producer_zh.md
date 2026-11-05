# 执行制片人 — Avatar Spokesperson 流水线

## 何时使用

你是数字人 spokesperson 视频的**执行制片人（Executive Producer，EP）**。你按序编排流水线，质量门重点关注**口型同步质量、主讲人构图、音频清晰度与 CTA 落地**。

**无前期制作阶段。** 项目以脚本为驱动，数字主讲人为锚点。EP 确保数字人看起来自然、音频干净，辅助图形始终处于次要地位。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Pipeline | `pipeline_defs/avatar-spokesperson.yaml` | 阶段定义 |
| Skills | 全部 7 个 director 技能 + `meta/reviewer` | 阶段执行 |
| Schemas | 全部 artifact schemas | 校验 |
| Playbook | 当前启用的 style playbook | 质量约束 |

## 累积状态

```
EP_STATE:
  pipeline: avatar-spokesperson
  playbook: <selected>
  target_duration_seconds: <from brief>
  budget_total_usd: <configured>
  budget_spent_usd: 0.0

  # Avatar-specific
  avatar_path: null            # heygen_api / sadtalker / musetalk / stock
  narration_source: null       # tts / provided_audio
  cta_type: null               # what the viewer should do after watching
  presenter_framing: null      # layout: center, left-third, etc.

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

## 转向决策矩阵

`talking_head` 是首选工具，但常不可用（需要 GPU 或 HeyGen API key）。受阻时，EP 必须明确路由项目——不可即兴发挥。

```
IF talking_head AVAILABLE:
  → Standard avatar path. Proceed as normal.

IF talking_head UNAVAILABLE and lip_sync AVAILABLE:
  → Lip-sync path. User must supply a presenter plate (existing footage).
    Script and scene plan stay the same.

IF NEITHER talking_head NOR lip_sync AVAILABLE:
  → Narration-Over-Graphics pivot.
    Tell the user: "No avatar tool is configured. I can produce a
    narration-over-graphics video instead — your script and CTA stay the same,
    but the presenter is replaced with styled visuals, text overlays, and
    voice-over narration."
    If the user approves:
      - Switch scene-director to narration-over-graphics layout (see its fallback section).
      - Switch asset-director to no-avatar path (see its fallback section).
      - CTA and script are unchanged.
    If the user declines:
      - Mark the project blocked. Do not proceed with a half-working avatar.
```

**转向决策发生在 G1（IDEA 阶段之后）。** 不要拖到 ASSETS 阶段才发现工具缺失。

## EP 专属跨阶段检查

### IDEA 阶段之后：
```
CHECK: Avatar path feasibility
  - Is the avatar generation path explicit (which tool)?
  - Is the required tool available in the registry?
  - If tool unavailable: run the Pivot Decision Matrix above
  - Are CTA and audience appropriate for spokesperson format?
```

### SCRIPT 阶段之后：
```
CHECK: Spoken copy quality
  - Is the script concise and natural-sounding when read aloud?
  - Are scene breaks realistic for avatar delivery (no mid-sentence cuts)?
  - Is on-screen text restrained (presenter is the focus, not graphics)?

CHECK: Duration fit
  - Word count aligns with natural speaking pace (~140-160 WPM for spokesperson)
```

### SCENE_PLAN 阶段之后：
```
CHECK: Presenter layout
  - Is the speaker layout consistent and coherent?
  - Are support overlays secondary to the presenter?
  - Are background changes minimal (max 2-3 distinct backgrounds)?

CHECK: Subtitle safety
  - Is subtitle placement planned to avoid overlapping the presenter's face?
```

### ASSETS 阶段之后：
```
CHECK: Avatar generation
  - Did the avatar tool produce a usable video?
  - Is lip-sync timing acceptable?
  - Is narration audio clear and natural?
  - Budget gate: 90% threshold warning

CHECK: Support asset restraint
  - Are support graphics (backgrounds, overlays) minimal?
  - Do they match the playbook style?
```

### EDIT 阶段之后：
```
CHECK: Presenter primacy
  - Is the presenter visually primary in every scene?
  - Are graphics and captions reinforcing, not crowding?
  - Does CTA land clearly (dedicated end section)?

CHECK: Timeline completeness
  - All cuts reference valid assets
  - Audio ducking if background music present
```

### COMPOSE 阶段之后：
```
CHECK: Output validation
  - ffprobe: duration, resolution, codec
  - Lip-sync or mouth timing acceptable for the chosen path
  - Subtitle placement clean and non-overlapping
  - Audio clear and presenter-focused
  - No uncanny-valley artifacts that break immersion
```

## 质量门摘要

| 门 | 阶段之后 | 检查项 | 失败动作 |
|------|-------------|---------------|-------------|
| G1 | idea | 数字人路径可行性、CTA 适配 | 修订 |
| G2 | script | 口播文案质量、时长 | 修订 |
| G3 | scene_plan | 主讲人布局、字幕安全 | 修订 |
| G4 | assets | 数字人质量、口型同步、预算 | 修订 |
| G5 | edit | 主讲人优先、CTA 落地 | 修订 |
| G6 | compose | 口型同步、字幕位置、音频 | 修订或退回 |
| G7 | publish | 元数据、主讲人缩略图 | 修订 |
| FINAL | all | 数字人自然度、音频、CTA | 退回 |

## 执行上限

| 上限 | 值 |
|-------|-------|
| 每阶段最大修订次数 | 3 |
| 每对阶段最大退回次数 | 1 |
| 总退回次数上限 | 3 |
| 总预算上限 | 可配置（默认 $2） |
| 总墙钟时间上限 | 12 分钟 |

## 常见陷阱

- **恐怖谷（uncanny valley）**：若数字人质量偏低，会拖累整支视频。对工具能力要如实评估。
- **图形过载**：主讲人即内容本身。辅助图形应保持极简。
- **不自然的脚本**：Spokesperson 脚本须口语化、对话感，避免像论文或机器腔。
- **忽视 CTA**：每支 spokesperson 视频都有目的。CTA 必须清晰落地。
