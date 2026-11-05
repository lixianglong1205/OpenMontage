# Executive Producer — Talking Head Pipeline

## 何时使用

你是 talking-head 视频项目的 **Executive Producer（EP，执行制片人）**。你按顺序编排整条流水线：启动各阶段 director、审阅其产出，并决定放行或退回修改。你是带状态的大脑；director 是无状态的执行者。

**你取代默认的并行/顺序执行模型。** 不再盲目跑完全部阶段，而是在每个关口运用判断。

## 为何需要

talking-head 流水线将人物口播原始素材转化为精修、带字幕的视频。没有 EP 时会出现：

- 转录错误在下游各阶段静默传播
- 字幕时间与口播漂移，且无法反馈修正
- 场景覆盖缺口导致成片出现死气
- 最终渲染前缺少 A/V 同步校验
- 无法只退回某一阶段而无需重跑全部
- 增强决策（人脸、调色、音频）缺乏全局上下文

EP 通过维护累积状态并在每个关口做判断，解决上述问题。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Pipeline | `pipeline_defs/talking-head.yaml` | 阶段定义、审阅重点、成功标准 |
| Skills | 全部 7 个 director 技能 + `meta/reviewer` | 阶段执行知识 |
| Schemas | 全部 artifact schema | 校验 |
| Playbook | 用户所选、素材推导或安全兜底 | 质量约束 |
| Tools | 完整 tool registry | 可用能力 |

## 与 Explainer EP 的关键差异

talking-head 流水线是 **footage-first（素材优先）**，而非 idea-first（创意优先）：

| 维度 | Explainer EP | Talking-Head EP |
|--------|-------------|-----------------|
| 源材料 | 无 — 全部生成 | 事先提供原始素材 |
| Script 阶段 | 从零撰写 | 从转录提取 |
| 核心挑战 | 创意生成质量 | 转录准确度 + 时间轴 |
| 预算模型 | 中等（TTS + 图像生成） | 低（多为处理，可选 overlay） |
| 时长来源 | 提案中设定目标 | 由原始素材长度决定 |
| 关键同步 | 旁白 ↔ 画面时长 | 字幕 ↔ 口播时间 |
| 前期制作 | 调研 + 提案（2 阶段） | Idea（1 阶段）— 无需调研 |

## 累积状态

EP 维护贯穿整条流水线的运行状态对象：

```
EP_STATE:
  pipeline: talking-head
  playbook: <selected playbook name, custom identity, or safe fallback>
  raw_footage_path: <path to source footage>
  raw_footage_duration_seconds: <from ffprobe>
  raw_footage_resolution: <from ffprobe>
  target_duration_seconds: <from brief, may be shorter than raw>
  budget_total_usd: <from user or default: $0.50>
  budget_spent_usd: 0.0
  budget_remaining_usd: <budget_total>

  # Accumulated from each stage (7 stages)
  artifacts:
    idea: null          # → brief
    script: null        # → script (transcript-based)
    scene_plan: null    # → scene_plan
    assets: null        # → asset_manifest
    edit: null          # → edit_decisions
    compose: null       # → render_report
    publish: null       # → publish_log

  # Transcript tracking (the core of talking-head quality)
  transcript_segments: []        # word-level timestamped segments from transcriber
  transcript_confidence: null    # average word confidence score
  transcript_language: null      # detected language
  subtitle_sync_offsets: {}      # section_id → drift_seconds (positive = subtitle late)

  # Cross-stage tracking
  total_footage_seconds: 0
  total_edit_seconds: 0        # may differ from footage if trimmed
  style_anchors: {}            # consistency tokens for overlays
  revision_counts: {}          # stage_name → number of revisions
  issues_log: []               # all issues found, with resolution status

  # Enhancement tracking
  enhancements_applied: []     # face_enhance, color_grade, audio_enhance
  audio_profile:               # from raw footage analysis
    has_background_noise: null
    audio_channels: null
    sample_rate: null
```

## 执行协议

### Phase 0：初始化

1. 加载 pipeline manifest（`talking-head.yaml`）
2. 从用户选择、品牌系统或素材推导的视觉 identity 加载 playbook。仅在没有更强 identity 时使用 `clean-professional`。
3. 从配置或用户输入设定预算（默认：$0.50 — talking-head 多为处理）
4. 用 ffprobe 探测原始素材：duration、resolution、fps、audio channels、codec
5. 将素材元数据写入 EP_STATE
6. 初始化 EP_STATE

### Phase 1：顺序执行各阶段

各阶段顺序：`idea → script → scene_plan → assets → edit → compose → publish`

```
EXECUTE_STAGE(stage_name):

  1. PREPARE
     - Load the director skill for this stage
     - Inject EP_STATE as context (prior artifacts, budget remaining, style anchors)
     - Inject any EP feedback from previous revision attempts

  2. SPAWN DIRECTOR
     - The director executes its full process (as defined in its skill MD)
     - Director produces an artifact

  3. REVIEW (EP performs this, not a separate reviewer)
     - Schema validation against artifact schema
     - Check review_focus items from pipeline manifest
     - Check success_criteria from pipeline manifest
     - Cross-check against playbook constraints
     - Run EP-SPECIFIC CROSS-STAGE CHECKS (see below)

  4. GATE DECISION
     If PASS:
       - Store artifact in EP_STATE
       - Update cumulative tracking (budget, durations, etc.)
       - Log: "[stage] PASSED — moving to next stage"
       - Continue to next stage

     If REVISE:
       - Increment revision_counts[stage_name]
       - If revision_counts[stage_name] >= 3:
           - PASS WITH WARNINGS (never block forever)
           - Log unresolved issues
       - Else:
           - Compose specific feedback for the director
           - Re-run SPAWN DIRECTOR with feedback injected
           - Re-run REVIEW

     If SEND_BACK(target_stage):
       - This is the EP's special power: send work BACK to a prior stage
       - Only used when a downstream discovery invalidates upstream work
       - Example: Subtitle sync check reveals transcript has wrong timestamps
         → Send back to script director: "Re-transcribe section 3. Timestamps are off."
       - Re-execute from target_stage forward (artifacts after target are invalidated)
       - Max 1 send-back per stage pair (prevent infinite loops)
```

### Phase 2：最终质量保证

7 个阶段全部完成后，EP 做整体审阅：

```
FINAL_QA:
  1. PROBE the output video:
     - Duration: within ±5% of target (or raw footage duration)?
     - Resolution: matches target or raw footage resolution?
     - Audio: speech audible throughout? No clipping? Balanced levels?
     - File: valid container, reasonable size?

  2. SUBTITLE SYNC CHECK (CRITICAL for talking-head):
     - Play-check subtitle timestamps against speech
     - For each subtitle cue: does it appear within ±0.3s of the spoken word?
     - Flag any section where subtitles are visibly out of sync
     - Tolerance: ±0.3 seconds (tighter than explainer because speech is the content)

  3. AUDIO QUALITY:
     - Was noise reduction applied if footage had background noise?
     - Are audio levels normalized? (target: -16 LUFS for speech)
     - If background music was added: is ducking configured correctly?

  4. VISUAL QUALITY:
     - If face_enhance was available and applied: does it look natural?
     - If color_grade was available and applied: is it consistent?
     - If overlays were added: do they appear at the right timestamps?

  5. BUDGET RECONCILIATION:
     - Total actual spend vs. budget
     - Log per-stage cost breakdown

  6. DECISION:
     If all checks pass → APPROVE for publish stage
     If issues found → Send back to the specific stage(s) that can fix them
       - Subtitle timing → asset director (regenerate subtitles)
       - Audio issues → compose director (remix)
       - Visual enhancement issues → compose director (re-render)
       - Coverage gaps → scene director (replan) or edit director (re-cut)
       - Transcript errors → script director (re-transcribe)
```

## EP 专属跨阶段检查

这些检查使用跨阶段累积的信息 — 单个 director 无法做到。

### IDEA 阶段之后：
```
CHECK: Footage viability
  - Does the footage have audio? (No audio = cannot proceed with talking-head pipeline)
  - Is the audio quality sufficient? (Signal-to-noise ratio)
  - Is the footage duration reasonable for target platform?
  - If duration > 3x target: flag that significant trimming is needed
  - Note: Idea stage DOES checkpoint with user — this is the approval gate
```

### SCRIPT 阶段之后：
```
CHECK: Transcript quality (CRITICAL — everything downstream depends on this)
  - Average word confidence score (from transcriber output)
  - If avg_confidence < 0.8:
      REVISE: "Transcript confidence is low ({X}). Try model: large-v3 if not already used.
      If still low, flag specific low-confidence sections for manual review."
  - Spot-check: do timestamps increase monotonically?
  - Spot-check: are there gaps > 2 seconds with no words? (may indicate missed speech)
  - Store transcript_segments in EP_STATE for downstream subtitle generation

CHECK: Section boundaries
  - Do sections align with natural topic changes?
  - Are timestamps within the raw footage duration?
  - Any section longer than 60s? (May need splitting for better scene planning)
```

### SCENE_PLAN 阶段之后：
```
CHECK: Full coverage
  - Sum all scene durations
  - Compare to raw footage duration (or target edit duration)
  - Gaps > 1 second: REVISE scene_plan
  - Overlaps: REVISE scene_plan

CHECK: Enhancement feasibility
  - For each planned enhancement (face, color, overlay):
      Verify the required tool exists in the registry
  - If face_enhance planned but unavailable: remove from plan, log warning
  - If overlay images planned: verify image tools are available

CHECK: Overlay alignment
  - If overlays are planned at specific timestamps, verify those timestamps
    fall within actual scene boundaries from the transcript
```

### ASSETS 阶段之后：
```
CHECK: Subtitle sync (CRITICAL for talking-head)
  - Compare subtitle cue timestamps to transcript word timestamps
  - For each cue: |subtitle_start - word_start| < 0.3s
  - Store sync offsets in EP_STATE.subtitle_sync_offsets
  - If any offset > 0.5s: REVISE assets: "Subtitle cue {id} is {X}s off.
    Re-generate from original transcript segments."

CHECK: Audio extraction
  - Was audio extracted from raw footage?
  - Was noise reduction applied if needed?
  - Are audio levels in a reasonable range?

CHECK: Budget gate
  - If budget_spent > budget_total * 0.8 and stages remain:
      Alert: "80% budget consumed with {N} stages remaining"
      Adjust remaining stages to skip optional enhancements
```

### EDIT 阶段之后：
```
CHECK: Timeline completeness
  - Verify edit decisions cover 0 to total_edit_duration with no gaps
  - Verify all cut source files reference existing paths from asset_manifest
  - Verify subtitle configuration is present and points to valid subtitle file

CHECK: Trim validation
  - If footage was trimmed (edit is shorter than raw): are the right sections kept?
  - Do the kept sections match the scene_plan?
  - Are transitions between cuts smooth (no jump cuts unless intentional)?
```

### COMPOSE 阶段之后：
```
CHECK: Output validation
  - ffprobe the output: duration, resolution, codec, audio channels
  - Duration drift > 5%: investigate which stage caused it
  - Audio missing: check audio extraction and mixing
  - Resolution wrong: check if face_enhance or color_grade changed it
  - Subtitles: if burn-in was requested, verify they're visible in output
```

## 反馈消息模板

将工作退回 director 时，使用以下结构化反馈：

### 致 Script Director：
```
EP FEEDBACK — Script Revision Required
Reason: {reason}
Specific issue: {transcript_quality / timestamp_error / section_boundary}
Affected sections: {section_ids}
Action: {re-transcribe / re-segment / re-align}
Transcriber settings: {model / language hints if applicable}
```

### 致 Scene Director：
```
EP FEEDBACK — Scene Plan Revision Required
Reason: {reason}
Affected scenes: {scene_ids}
Constraint: {coverage / feasibility / timing}
Available tools: {current tool registry status}
```

### 致 Asset Director：
```
EP FEEDBACK — Asset Regeneration Required
Reason: {reason}
Affected assets: {asset_ids}
Specific fix: {subtitle_resync / audio_renormalize / overlay_regen}
Transcript reference: {original transcript segments for re-alignment}
Budget remaining: ${remaining}
```

### 致 Edit Director：
```
EP FEEDBACK — Edit Revision Required
Reason: {reason}
Specific issue: {gap_at_timestamp / invalid_reference / missing_subtitle_config}
Asset manifest: {current valid asset paths}
```

### 致 Compose Director：
```
EP FEEDBACK — Re-render Required
Reason: {reason}
Specific issue: {subtitle_sync / audio_quality / resolution / duration}
Expected: {what the output should be}
Actual: {what was produced}
Enhancement adjustments: {skip/add face_enhance, color_grade, etc.}
```

## 质量关口摘要

| 关口 | 阶段之后 | 检查内容 | 失败动作 |
|------|-------------|---------------|-------------|
| G1 | idea | 素材可行性、是否有音频、用户批准 | 修订 brief 或停止流水线 |
| G2 | script | 转录置信度、时间戳、章节边界 | 修订 script（重新转录） |
| G3 | scene_plan | 全覆盖、增强可行性、overlay 对齐 | 修订 scene_plan |
| G4 | assets | 字幕同步、音频提取、预算 | 修订 assets 或 send-back 至 script |
| G5 | edit | 时间线完整、裁剪校验、字幕配置 | 修订 edit |
| G6 | compose | 输出探测、时长、音频、字幕烧录 | 修订 compose 或 send-back 至 edit/assets |
| G7 | publish | 元数据、打包 | 修订 publish |
| FINAL | all | 字幕同步、音频质量、画面质量 | send-back 至指定阶段 |

## 执行上限（防循环）

| 限制 | 值 | 理由 |
|-------|-------|-----------|
| 每阶段最大修订次数 | 3 | 避免完美主义死循环 |
| 每对阶段最大 send-back 次数 | 1 | 避免阶段间 ping-pong |
| send-back 总次数上限 | 3 | 限制整条流水线返工 |
| 总预算上限 | 可配置（默认 $0.50） | 硬性支出上限 |
| 总墙钟时间上限 | 10 分钟 | 整条流水线超时（短于 explainer — 生成更少） |

任一上限触达后：**带警告继续**，永不无限阻塞。

## 与现有技能的集成

EP 不取代任何 director 技能 — 而是包裹它们。各 director 技能仍按文档工作。EP 额外提供：

1. **上下文注入**：director 收到 EP_STATE，获得此前无法访问的跨阶段信息
2. **反馈注入**：被退回时 director 收到具体修订说明
3. **预算感知**：director 获知剩余预算并可调整工具选择
4. **转录连续性**：EP 将转录数据一路带到 asset 生成，确保字幕与剪辑使用同一事实来源

## EP 运行示例（缩写）

```
[EP] Starting pipeline: talking-head v2.0
[EP] Default budget: $0.50 | Playbook: footage-derived identity (or safe fallback)

[EP] Probing raw footage: interview_raw.mp4
[EP] → Duration: 4m22s | Resolution: 1920x1080 | FPS: 30 | Audio: stereo AAC
[EP] Footage looks viable. Audio present. Proceeding.

[EP] === STAGE 1: idea ===
[EP] Spawning idea-director... Footage: interview_raw.mp4
[EP] Brief: "Interview with CTO on API security" | Target: 3m00s (trim from 4m22s)
[EP] Platform: YouTube Shorts → wait, that's < 60s. User said LinkedIn.
[EP] G1 PASS — Brief references footage, duration target realistic, user approved.

[EP] === STAGE 2: script ===
[EP] Spawning script-director with brief...
[EP] Transcriber: WhisperX large-v3. Processing 4m22s audio...
[EP] Transcript: 612 words, avg confidence 0.91. Language: en.
[EP] 8 sections identified. Timestamps monotonic. ✓
[EP] G2 PASS — Confidence good, sections align with topic changes.

[EP] === STAGE 3: scene_plan ===
[EP] Spawning scene-director with script...
[EP] 8 scenes planned. Total duration: 3m02s (target 3m00s).
[EP] Enhancements: face_enhance on all scenes, color_grade, lower-third overlay at 0:00-0:05.
[EP] face_enhance: checking registry... AVAILABLE ✓
[EP] G3 PASS — Full coverage, enhancements feasible.

[EP] === STAGE 4: assets ===
[EP] Spawning asset-director with scene_plan + script...
[EP] Subtitles generated: 82 cues, SRT format.
[EP] Sync check: max offset 0.18s. All within 0.3s tolerance. ✓
[EP] Audio extracted and normalized to -16 LUFS. ✓
[EP] Lower-third overlay generated via recraft_image. Cost: $0.02.
[EP] Budget: $0.02 spent, $0.48 remaining.
[EP] G4 PASS — Subtitles synced, audio clean, assets on disk.

[EP] === STAGE 5: edit ===
[EP] Spawning edit-director with scene_plan + asset_manifest...
[EP] Timeline: 3m02s with 7 cuts. Subtitles enabled.
[EP] Trim: removed 0:00-0:12 (dead air) and 3:45-4:22 (off-topic).
[EP] G5 PASS — Timeline complete, all references valid.

[EP] === STAGE 6: compose ===
[EP] Spawning compose-director with edit_decisions + asset_manifest...
[EP] face_enhance applied: 8 scenes processed.
[EP] color_grade applied: unified warm tone.
[EP] audio_enhance: noise reduction applied.
[EP] video_compose: final render → output/talking-head-final.mp4
[EP] Output probe: 3m01s, 1920x1080, stereo audio, H.264. ✓
[EP] Budget: $0.18 spent (face_enhance + color_grade + overlays).
[EP] G6 PASS

[EP] === STAGE 7: publish ===
[EP] Spawning publish-director with render_report...
[EP] G7 PASS — Title, description, chapters, thumbnail configured.

[EP] === FINAL QA ===
[EP] Duration: 3m01s ✓ | Subtitle sync: max drift 0.18s ✓ | Audio: -16.2 LUFS ✓
[EP] Face enhance: natural ✓ | Color: consistent ✓ | Overlays: timed correctly ✓
[EP] Budget: $0.18 / $0.50 ✓
[EP] PIPELINE COMPLETE — 0 revisions, 0 send-backs
[EP] Output: output/talking-head-final.mp4
```

## 常见陷阱

- **忽视转录质量**：下游一切依赖转录。置信度低时在 script 阶段修复 — 不要让错误时间戳传播到字幕与剪辑。
- **过度增强**：face enhance 与 color grade 可选。原始素材已好则跳过，不要为处理而处理。
- **字幕样式不匹配**：字幕样式须来自 playbook。勿让 asset director 在 playbook 已指定字体/颜色/位置时仍用默认 SRT 样式。
- **未探测原始素材**：开始前务必 ffprobe。无音轨或容器损坏会在下游浪费全部阶段。
- **裁剪过猛**：edit director 可能切掉看似离题但含重要上下文的段落。EP 应对照 brief 确认被裁内容确属多余。
- **丢失转录数据**：EP 须将 `transcript_segments` 从 script 阶段一直带到 asset 生成。字幕时间依赖 transcriber 产出的同一词级数据。
