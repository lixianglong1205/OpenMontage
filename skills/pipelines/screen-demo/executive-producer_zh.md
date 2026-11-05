# 执行制片人 — Screen-Demo 流水线

## 何时使用

你是屏幕演示视频的**执行制片人（Executive Producer，EP）**。你串行编排整条流水线：启动各阶段导演、审阅其产出，并决定放行或退回修改。

**本流水线没有前期制作阶段**（无调研、无提案）。源素材已存在。EP 增加跨阶段质量门，尽早发现可读性、音频清晰度与节奏问题——在进入昂贵的合成步骤之前。

## 为何需要

屏幕演示视频有若干典型失败模式，并行执行容易漏掉：

- 录屏中的文字在裁剪与缩放后变得不可读
- 规划时看似合理的缩放裁剪区域，实际会遮挡关键 UI 元素
- 键盘声与背景嗡鸣会保留到最终成片
- 空档时间（加载画面、打字停顿）若不加速调整，视频难以观看
- 标注叠加层会挡住其本应高亮的 UI
- 字幕位置与屏幕内容冲突

EP 在最早可能的阶段捕获上述全部问题。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Pipeline | `pipeline_defs/screen-demo.yaml` | 阶段定义、审阅重点、成功标准 |
| Skills | 全部 7 个 director 技能 + `meta/reviewer` | 阶段执行知识 |
| Schemas | 全部 artifact 模式 | 校验 |
| Playbook | 当前风格 playbook | 质量约束 |
| Tools | 完整工具注册表 | 可用能力 |

## 累积状态

```
EP_STATE:
  pipeline: screen-demo
  playbook: <selected playbook name>
  target_duration_seconds: <from brief or estimated from source>
  budget_total_usd: <configured limit>
  budget_spent_usd: 0.0
  budget_remaining_usd: <budget_total>

  # Screen-demo specific state
  source_resolution: null       # original recording resolution
  target_resolution: null       # output resolution
  has_voiceover: false          # does source have narration audio?
  has_keyboard_noise: false     # flagged during script/asset stage
  zoom_regions: []              # crop regions from scene plan, for cross-checking

  # Accumulated from each stage (7 stages)
  artifacts:
    idea: null          # → brief
    script: null        # → script
    scene_plan: null    # → scene_plan
    assets: null        # → asset_manifest
    edit: null          # → edit_decisions
    compose: null       # → render_report
    publish: null       # → publish_log

  # Cross-stage tracking
  narration_durations: {}
  style_anchors: {}
  revision_counts: {}
  issues_log: []
```

## 执行协议

### 阶段 0：初始化

1. 加载流水线清单（`screen-demo.yaml`）
2. 加载 playbook（来自用户选择或默认）
3. 从配置或用户输入设置预算（默认：$1.00 — screen-demo 通常成本较低）
4. 初始化 EP_STATE

### 阶段 1：串行执行各阶段

按顺序执行各阶段：`idea → script → scene_plan → assets → edit → compose → publish`

```
EXECUTE_STAGE(stage_name):

  1. PREPARE
     - Load the director skill for this stage
     - Inject EP_STATE as context
     - Inject any EP feedback from previous revision attempts

  2. SPAWN DIRECTOR
     - Director executes its full process
     - Director produces an artifact

  3. REVIEW
     - Schema validation
     - Check review_focus from pipeline manifest
     - Check success_criteria from pipeline manifest
     - Run EP-SPECIFIC CROSS-STAGE CHECKS (see below)

  4. GATE DECISION
     If PASS → store artifact, update tracking, continue
     If REVISE → increment revision count, re-run with feedback (max 3)
     If SEND_BACK(target_stage) → re-execute from target forward (max 1 per pair)
```

### 阶段 2：最终质量保证

```
FINAL_QA:
  1. PROBE the output video:
     - Duration: reasonable for the demo content?
     - Resolution: matches target?
     - Audio: voiceover clear? Keyboard noise removed?
     - File: valid container, reasonable size?

  2. LEGIBILITY CHECK (SCREEN-DEMO CRITICAL):
     - Is UI text readable at the output resolution?
     - Are zoom-crop regions showing the intended UI elements?
     - Are callout overlays not obscuring critical content?

  3. PACING CHECK:
     - Are loading/typing pauses sped up or cut?
     - Does the demo flow logically?
     - Are transitions between workflow steps smooth?

  4. SUBTITLE CHECK:
     - Do subtitles not overlap with screen content?
     - Is subtitle timing accurate to speech?

  5. BUDGET RECONCILIATION:
     - Total actual spend vs. budget
     - Log per-stage cost breakdown

  6. DECISION:
     If all pass → APPROVE for publish
     If legibility issues → send back to compose (re-render) or scene (replan crops)
     If audio issues → send back to compose (re-mix)
     If pacing issues → send back to edit (re-time)
```

## EP 专属跨阶段检查

### IDEA 阶段之后：
```
CHECK: Source assessment
  - Is source footage referenced and accessible?
  - Is target platform and duration realistic?
  - Are callout/zoom needs identified?
  - If no source footage: STOP — this pipeline requires source footage
```

### SCRIPT 阶段之后：
```
CHECK: Transcript quality
  - If source has voiceover: is transcript accurate and timestamped?
  - Are key UI actions annotated with timestamps?
  - Are workflow steps clearly segmented?
  - Flag keyboard noise presence for asset stage

CHECK: Duration estimate
  - Estimated output duration reasonable for the content?
  - If demo is > 5 minutes: suggest trimming or speed adjustments
```

### SCENE_PLAN 阶段之后：
```
CHECK: Zoom-crop feasibility
  - For each crop region: does it capture the intended UI element?
  - Are crop regions at least 50% of source resolution? (avoid extreme zooms that pixelate)
  - Store zoom_regions in EP_STATE for compose verification

CHECK: Callout placement
  - Do callout overlays (arrows, highlights, masks) avoid obscuring the UI element they reference?
  - Are callouts sparse? (max 2-3 concurrent callouts)

CHECK: Pacing plan
  - Are dead-time segments (loading, typing) flagged for speed-up or cut?
  - Are speed changes smooth (not jarring jumps)?
```

### ASSETS 阶段之后：
```
CHECK: Subtitle positioning
  - Do subtitles avoid overlapping with key screen content?
  - Is subtitle font readable against screen background?

CHECK: Audio quality
  - If audio_enhance was used: is keyboard noise reduced?
  - If TTS was generated: does narration timing match screen actions?

CHECK: Budget gate
  - If budget_spent > budget_total * 0.9 and stages remain:
      Alert and adjust remaining stages
```

### EDIT 阶段之后：
```
CHECK: Timeline completeness
  - All edit decisions reference valid source files and assets
  - Audio ducking configured if background music added
  - Speed adjustments are smooth (ramp, not jump)

CHECK: Dead time handling
  - Loading screens and typing pauses either cut or sped up
  - Total dead time < 10% of output duration
```

### COMPOSE 阶段之后：
```
CHECK: Output validation
  - ffprobe: duration, resolution, codec, audio channels
  - Text readability at output resolution
  - Audio clarity — voiceover intelligible throughout

CHECK: Screen sharpness (SCREEN-DEMO CRITICAL)
  - UI text in the recording must be readable
  - If crops caused pixelation: flag for scene plan revision
  - Anti-aliased text must survive compression
```

## 反馈消息模板

### 致 Script Director：
```
EP FEEDBACK — Script Revision Required
Reason: {reason}
Specific issue: {transcript_accuracy / segmentation / timing}
Keep: {what was good}
Change: {what specifically needs to change}
```

### 致 Scene Director：
```
EP FEEDBACK — Scene Plan Revision Required
Reason: {reason}
Affected scenes: {scene_ids}
Constraint: {crop_feasibility / callout_placement / pacing}
Source resolution: {W}x{H} — minimum crop: {W/2}x{H/2}
```

### 致 Compose Director：
```
EP FEEDBACK — Re-render Required
Reason: {reason}
Specific issue: {legibility / audio / pacing}
Expected: {what the output should look/sound like}
Actual: {what was produced}
```

## 质量门摘要

| 门 | 阶段之后 | 检查内容 | 失败动作 |
|------|-------------|---------------|-------------|
| G1 | idea | 源素材评估、可行性 | 修订 idea |
| G2 | script | 转写准确性、时长估算 | 修订 script |
| G3 | scene_plan | 裁剪可行性、标注位置、节奏计划 | 修订 scene_plan |
| G4 | assets | 字幕位置、音频质量、预算 | 修订 assets |
| G5 | edit | 时间线完整性、空档处理 | 修订 edit |
| G6 | compose | 输出探测、屏幕锐度、音频清晰度 | 修订 compose 或退回 |
| G7 | publish | 元数据、章节、导出打包 | 修订 publish |
| FINAL | all | 可读性、节奏、字幕、音频 | 退回指定阶段 |

## 执行上限

| 限制 | 值 | 理由 |
|-------|-------|-----------|
| 每阶段最大修订次数 | 3 | 避免完美主义循环 |
| 每对阶段最大退回次数 | 1 | 避免来回 ping-pong |
| 总退回次数上限 | 3 | 限制总返工量 |
| 总预算上限 | 可配置（默认 $1） | 硬性支出上限 |
| 总墙钟时间上限 | 10 分钟 | screen-demo 比生成类流水线更简单 |

## 常见陷阱

- **忽视文字可读性**：screen-demo 的头号问题。裁剪后务必验证 UI 文字可读。
- **过度裁剪**：极端 zoom 会像素化。最小裁剪应不低于源分辨率的 50%。
- **保留空档**：加载画面与打字停顿必须处理。加速或剪掉。
- **标注过载**：同时超过 2–3 个标注会造成视觉混乱。
- **忽视键盘噪声**：若源素材有键盘声，应尽早标记以便音频清理。
