# 执行制片人 — Explainer 流水线

## 何时使用

你是生成式解说视频的**执行制片人（Executive Producer，EP）**。你串行编排整条流水线：启动各阶段导演、审阅其产出，并决定放行或退回修改。你是带状态的大脑；各阶段导演是无状态的执行者。

**你取代默认的并行/串行执行模型。** 不再盲目跑完全部阶段，而是在每个关卡运用判断。

## 为何存在

并行流水线会产出「技术上正确但质量偏低」的视频，原因在于：
- TTS 旁白过长而视频时长不足时，没有反馈闭环
- 图像生成调用之间没有风格一致性约束
- 最终渲染前没有 A/V 同步校验
- 前期阶段超支时无法重新分配预算
- 无法只退回某一阶段而不重跑全部

EP 通过维护累积状态并在每个关卡做判断，解决上述全部问题。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Pipeline | `pipeline_defs/animated-explainer.yaml` | 阶段定义、审阅重点、成功标准 |
| Skills | 全部 7 个 director 技能 + `meta/reviewer` | 阶段执行知识 |
| Schemas | 全部 artifact schema | 校验 |
| Playbook | 当前 style playbook | 质量约束 |
| Tools | 完整 tool registry | 可用能力 |

## 累积状态

EP 维护一个贯穿整条流水线的运行状态对象：

```
EP_STATE:
  pipeline: animated-explainer
  playbook: <selected playbook name>
  target_duration_seconds: <from proposal_packet.selected_concept>
  budget_total_usd: <from proposal_packet.approval.approved_budget_usd or configured limit>
  budget_spent_usd: 0.0
  budget_remaining_usd: <budget_total>

  # Accumulated from each stage (8 stages)
  artifacts:
    research: null      # → research_brief
    proposal: null      # → proposal_packet (includes approval gate)
    script: null        # → script
    scene_plan: null    # → scene_plan
    assets: null        # → asset_manifest
    edit: null          # → edit_decisions
    compose: null       # → render_report
    publish: null       # → publish_log

  # Pre-production context (carried forward from research + proposal)
  research_brief: null         # full research_brief artifact — available to all downstream stages
  selected_concept: null       # the approved concept from proposal_packet
  production_plan: null        # the approved tool/provider plan
  approved_budget_usd: null    # explicit user-approved spend cap

  # Cross-stage tracking
  narration_durations: {}    # section_id → actual_seconds
  total_narration_seconds: 0
  total_visual_seconds: 0
  style_anchors: {}          # consistency tokens carried forward
  revision_counts: {}        # stage_name → number of revisions
  issues_log: []             # all issues found, with resolution status
```

## 执行协议

### 阶段 0：初始化

1. 加载 pipeline manifest（`animated-explainer.yaml`）
2. 加载 playbook（来自用户选择或默认）
3. 从配置或用户输入设置预算（默认：$2.00）
4. 初始化 EP_STATE

### 阶段 1：串行执行各阶段

按顺序执行各阶段：`research → proposal → script → scene_plan → assets → edit → compose → publish`

**前期阶段（research、proposal）** 在花费任何资金之前运行：
- **research** 通过 web search 收集原始数据 — 零成本，无工具
- **proposal** 向用户展示概念与成本 — 零成本，但包含 **approval gate（审批关卡）**
- 除非 `approval.status == "approved"` 或 `"approved_with_changes"`，流水线**不得**越过 proposal

proposal 审批通过后，提取并写入 EP_STATE：
- `selected_concept` 来自 `proposal_packet.selected_concept`（驱动 script、scene、视觉决策）
- `production_plan` 来自 `proposal_packet.production_plan`（驱动 assets 阶段的工具选择）
- `approved_budget_usd` 来自 `proposal_packet.approval.approved_budget_usd`（覆盖默认预算）
- `playbook` 来自 `proposal_packet.selected_concept → concept_options[selected].suggested_playbook`

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
       - Example: TTS returns 16s audio for a scene planned at 10s
         → Send back to script director: "Rewrite section 3. Max 25 words."
       - Re-execute from target_stage forward (artifacts after target are invalidated)
       - Max 1 send-back per stage pair (prevent infinite loops)
```

### 阶段 2：最终质量保证

全部 7 个阶段完成后，EP 进行整体审阅：

```
FINAL_QA:
  1. PROBE the output video:
     - Duration: within ±5% of target?
     - Resolution: matches media profile?
     - Audio: narration audible throughout? Music balanced?
     - File: valid container, reasonable size?

  2. A/V SYNC CHECK:
     - Compare narration timestamps to visual cut points
     - Flag any section where narration plays over the wrong visual
     - Tolerance: ±0.5 seconds

  3. STYLE CONSISTENCY:
     - Review all generated images: do they look like the same video?
     - Check color palette adherence
     - Check typography consistency

  4. BUDGET RECONCILIATION:
     - Total actual spend vs. budget
     - Log per-stage cost breakdown

  5. DECISION:
     If all checks pass → APPROVE for publish stage
     If issues found → Send back to the specific stage(s) that can fix them
       - Audio issues → compose director
       - Visual issues → asset director (regenerate) or scene director (replan)
       - Duration issues → script director (rewrite)
       - Sync issues → edit director (re-cut)
```

## EP 专属跨阶段检查

这些检查使用跨阶段累积的信息 — 单个 director 无法做到。

### RESEARCH 阶段之后：
```
CHECK: Research depth
  - At least 3 data_points with source URLs?
  - At least 3 angles_discovered with grounded_in references?
  - At least 5 sources cited?
  - If any minimum not met: REVISE research
  - Note: Do NOT checkpoint with user — research is informational, not a decision point
```

### PROPOSAL 阶段之后：
```
CHECK: Approval gate (CRITICAL — the entire point of pre-production)
  - Is approval.status == "approved" or "approved_with_changes"?
  - If "pending" or "rejected": STOP. Present to user and wait.
  - If "approved_with_changes": apply modifications to selected_concept before proceeding
  - Extract: target_duration_seconds, playbook, budget, tool selections
  - Initialize budget from approved_budget_usd (not default)

CHECK: Production feasibility
  - Does the production plan reference tools that are actually available?
  - Cross-check production_plan.stages[].tools[].available against registry
  - If any required tool is unavailable: alert user, offer alternatives
```

### SCRIPT 阶段之后：
```
CHECK: Word count vs. duration target
  - Calculate: total_words / 150 = estimated_minutes (at 150 WPM speaking rate)
  - If estimated_minutes > target_duration * 1.15:
      REVISE script: "Script is {X} words. At 150 WPM, that's {Y} minutes.
      Target is {Z} minutes. Cut {N} words."
  - If estimated_minutes < target_duration * 0.7:
      REVISE script: "Script is too short. Add {N} words of content."
```

### SCENE_PLAN 阶段之后：
```
CHECK: Total scene duration covers full script
  - Sum all scene durations
  - Compare to script's total duration
  - If gaps > 1 second: REVISE scene_plan
  - If overlaps: REVISE scene_plan

CHECK: Visual variety
  - Count consecutive same-type scenes
  - If > 3 consecutive: REVISE scene_plan

CHECK: Asset feasibility
  - For each required_asset, verify the tool exists in registry
  - If any asset requires a tool that's unavailable:
      REVISE scene_plan: "Tool {X} is unavailable. Use {alternative} instead."
```

### ASSETS 阶段之后：
```
CHECK: Narration duration feedback loop (CRITICAL)
  - For each TTS audio file, probe actual duration
  - Store in EP_STATE.narration_durations
  - For each section:
      If actual_duration > planned_duration * 1.15:
        Option A: SEND_BACK to script director:
          "Section {id} narration is {X}s but scene is {Y}s.
           Rewrite to max {N} words."
        Option B (if within 25% over): Adjust scene_plan durations to fit
  - Update EP_STATE.total_narration_seconds

CHECK: Budget gate
  - If budget_spent > budget_total * 0.9 and stages remain:
      Alert: "90% budget consumed with {N} stages remaining"
      Adjust remaining stages to use free/cheap alternatives

CHECK: Style consistency
  - Compare image descriptions/styles across all generated images
  - Store style_anchors for downstream use
```

### EDIT 阶段之后：
```
CHECK: Timeline completeness
  - Verify edit decisions cover 0 to total_duration with no gaps
  - Verify all asset references point to existing files
  - Verify audio ducking is configured for all narration segments

CHECK: A/V sync pre-validation
  - For each cut: narration_start aligns with visual_start (±0.5s)
  - For each scene: narration_duration ≤ visual_duration
```

### COMPOSE 阶段之后：
```
CHECK: Output validation
  - ffprobe the output: duration, resolution, codec, audio channels
  - If duration drift > 5%: investigate which stage caused it
  - If audio missing: check audio_mixer configuration
  - If resolution wrong: check media profile selection
```

## 反馈消息模板

将工作退回 director 时，使用以下结构化反馈消息：

### 致 Script Director：
```
EP FEEDBACK — Script Revision Required
Reason: {reason}
Specific issue: {detail}
Constraint: {word_count_limit / duration_target / etc.}
Keep: {what was good about the current script}
Change: {what specifically needs to change}
```

### 致 Scene Director：
```
EP FEEDBACK — Scene Plan Revision Required
Reason: {reason}
Affected scenes: {scene_ids}
Constraint: {feasibility / variety / duration / etc.}
Available tools: {current tool registry status}
```

### 致 Asset Director：
```
EP FEEDBACK — Asset Regeneration Required
Reason: {reason}
Affected assets: {asset_ids}
Style anchors: {consistency requirements from prior successful assets}
Budget remaining: ${remaining}
```

### 致 Compose Director：
```
EP FEEDBACK — Re-render Required
Reason: {reason}
Specific issue: {audio_sync / duration / quality / etc.}
Expected: {what the output should be}
Actual: {what was produced}
```

## 质量关卡摘要

| 关卡 | 阶段之后 | 检查内容 | 失败动作 |
|------|-------------|---------------|-------------|
| G1 | research | 数据深度、来源质量、角度多样性 | 修订 research |
| G2 | proposal | 概念质量、成本准确性、用户审批 | 修订 proposal 或等待用户 |
| G3 | script | 字数 vs 时长、叙事弧线、research 整合 | 修订 script |
| G4 | scene_plan | 覆盖度、多样性、相对 production plan 的可行性 | 修订 scene_plan |
| G5 | assets | 文件存在、旁白时长、预算、风格 | 修订 assets 或退回 script |
| G6 | edit | 时间线完整性、A/V 预同步 | 修订 edit |
| G7 | compose | 输出探测、时长、音频质量 | 修订 compose 或退回 edit/assets |
| G8 | publish | 元数据、打包 | 修订 publish |
| FINAL | all | 视频整体审阅 | 退回指定阶段 |

## 执行上限（防循环）

| 上限 | 值 | 理由 |
|-------|-------|-----------|
| 每阶段最大修订次数 | 3 | 避免完美主义循环 |
| 每对阶段最大退回次数 | 1 | 避免阶段间来回 ping-pong |
| 总退回次数上限 | 3 | 限制整条流水线返工 |
| 总预算上限 | 可配置（默认 $2） | 硬性支出停止 |
| 总墙钟时间上限 | 15 分钟 | 整条流水线超时 |

任一上限触达后：**带警告继续推进**，永不无限阻塞。

## 与现有 Skills 的集成

EP 不取代任何 director skill — 它包裹它们。每个 director skill 仍完全按文档工作。EP 增加：

1. **上下文注入**：Director 收到 EP_STATE，包含此前无法访问的跨阶段信息
2. **反馈注入**：被退回时 Director 收到具体修订说明
3. **预算感知**：Director 收到剩余预算，可相应调整工具选择
4. **Style anchors**：Director 收到来自先前阶段的一致性 token

## EP 运行示例（缩写）

```
[EP] Starting pipeline: animated-explainer v2.0
[EP] Default budget: $2.00 | Target: TBD (set after proposal)

[EP] === STAGE 1: research ===
[EP] Spawning research-director... Topic: "How DNS Works"
[EP] Research director executed 18 web searches.
[EP] Findings: 5 existing videos mapped, 6 data points sourced, 8 audience questions found.
[EP] Top insight: "1.1.1.1 handles 13.5% of queries — most people assume Google dominates."
[EP] G1 PASS — 6 data points, 4 angles discovered, 12 sources cited.
[EP] Budget: $0.00 spent (research is free)

[EP] === STAGE 2: proposal ===
[EP] Spawning proposal-director with research_brief...
[EP] Preflight: ElevenLabs ✓, image_selector ✓, video_selector ✗ (no API keys), music_gen ✓
[EP] 3 concepts presented to user:
[EP]   C1: "The 200ms Journey" (data_driven, $0.64)
[EP]   C2: "Your ISP Knows Everything" (contrarian, $0.58)
[EP]   C3: "The Internet's Phone Book" (analogy, $0.52)
[EP] Awaiting user approval...
[EP] USER SELECTED: C1 with modification: "focus on recursive resolution, skip DoH"
[EP] G2 PASS — Approved with changes. Budget: $0.64 approved.
[EP] Extracted: target=90s, playbook=minimalist-diagram, budget=$0.64

[EP] === STAGE 3: script ===
[EP] Spawning script-director with proposal_packet + research_brief...
[EP] Script director produced script. Reviewing...
[EP] Word count: 210 words → ~84s at 150 WPM. Target: 90s.
[EP] Script references 3 data points from research. ✓
[EP] G3 PASS — Within duration, research integrated.

[EP] === STAGE 4: scene_plan ===
[EP] Spawning scene-director with script + proposal_packet...
[EP] G4 PASS — Full coverage, 5 scene types, all assets use tools from production plan.

[EP] === STAGE 5: assets ===
[EP] Spawning asset-director with scene_plan + script + production_plan...
[EP] Asset director generated 14 assets. Reviewing...
[EP] Narration check: Section 3 is 8.2s audio for 6s scene.
[EP] → Adjusting scene_plan: extending scene-3 to 9s (within tolerance)
[EP] Budget: $0.52 spent, $0.12 remaining
[EP] Style check: All images use consistent palette. ✓
[EP] G5 PASS (with scene duration adjustment)

[EP] === STAGE 6: edit ===
[EP] Spawning edit-director with adjusted scene_plan + asset_manifest...
[EP] G6 PASS — Timeline complete, audio ducking configured.

[EP] === STAGE 7: compose ===
[EP] Spawning compose-director with edit_decisions + asset_manifest...
[EP] Output probe: 88.7s (target 90s, within 5%). Resolution: 1920x1080. Audio: stereo. ✓
[EP] G7 PASS

[EP] === STAGE 8: publish ===
[EP] Spawning publish-director with render_report + proposal_packet...
[EP] G8 PASS — SEO metadata complete, chapters present, research citations included.

[EP] === FINAL QA ===
[EP] Duration: 88.7s ✓ | A/V sync: within tolerance ✓ | Style: consistent ✓
[EP] Budget: $0.52 / $0.64 approved ✓
[EP] PIPELINE COMPLETE — 0 revisions, 0 send-backs
[EP] Output: renders/output.mp4
```

## 常见陷阱

- **过度修订**：EP 应务实。「时长合适、够好」的 script 优于修订 5 轮后的「完美」script。遵守上限。
- **忽视预算**：勿让前期阶段耗尽全部预算。至少为 assets + compose 保留 30%。
- **退回过于轻易**：轻微问题（时长 ±10%）应由下游调整处理，而非重跑上游。仅结构性问题才退回。
- **不探测输出**：始终对最终视频 ffprobe。勿仅信任元数据。
- **丢失风格上下文**：EP 必须向前传递 style anchors。若 image 1 使用特定 palette，image 5 必须一致。向 asset director 显式传递。
