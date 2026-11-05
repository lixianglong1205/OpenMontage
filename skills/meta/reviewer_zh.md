# Reviewer — 元技能

## 何时使用

在完成任意流水线阶段的工作之后、进入 checkpoint 之前。你是「工作已完成」与「工作被接受」之间的质量关卡。本技能以指令驱动的自审协议取代 Python reviewer 类。

每个阶段都必须经过审查。没有例外。审查质量决定最终成片是否值得观看。

## 批评质量（CHAI 规则）

> 发现（findings）≠ 批评（critiques）。发现指出了问题；批评告诉下一阶段如何修复。CMU/Harvard CHAI 研究（「Building a Precise Video Language with Human-AI Oversight」，arXiv 2604.21718v2）表明，沿三个维度衡量的批评质量直接决定下游产出质量。每次 reviewer 通过时都要应用这三条。
>
> **准确（Accurate）。** 每条发现必须指向具体的 artifact 字段、行号或可见素材帧。禁止臆造批评——若指不出问题所在，就是在猜。
>
> **完整（Complete）。** 只抓到一个错误却漏掉第二个的审查，比判为「需要再跑一轮」更糟。若发现一个 critical 问题，在返回前先扫描是否还有同类问题。模式匹配：同一类错误还可能藏在 artifact 的哪些地方？
>
> **建设性（Constructive）。** 每条「critical」发现必须提出具体修复方案，而非仅指出问题。「字幕错了」→「字幕写『右侧的男人』，但男人在画面左侧。改为『画面左侧的男人』。」若无法提出修复，将发现标为「investigation」而非「critical」。
>
> 去掉这三条中的任意一条都会可测地损害流水线产出。reviewer 是 choke point——要严格。

## 协议

### 步骤 1：加载审查上下文

审查前先收集：
1. 本阶段流水线 manifest 中的 **review focus 项**（`review_focus` 字段）
2. 本阶段 manifest 中的 **success criteria**（`success_criteria` 字段）
3. **当前 playbook** 的质量规则
4. 该阶段产出的 **artifact**

### 步骤 2：Schema 校验

首先，不可妥协的检查：
- 对照 JSON schema（`schemas/artifacts/<name>.schema.json`）校验 artifact
- 若 schema 校验失败，记为 **critical** 发现——立即修复，不要继续

### 步骤 3：对照 Focus 项审查

对 manifest 中每个 `review_focus` 项：
1. 按该具体标准评估 artifact
2. 分配严重级别：
   - **critical** — 必须修复后才能继续。artifact 损坏、不完整或危险错误。**按 CHAI 规则，每条 critical 必须带 `proposed_fix`（具体替换文案、精确字段值或明确纠正动作）。无 proposed_fix 的 critical 降级为 `investigation`。**
   - **suggestion** — 应修复。显著提升质量但不阻塞进度。**suggestion 必须带 `proposed_change` 说明如何改进。**
   - **nitpick** — 可修。锦上添花的小 polish。可单独存在，不必带 proposed change。
   - **investigation** — 确有顾虑但无法 pinpoint 修复。留给下一轮；不要因此阻塞。
3. 写出具体、可执行的发现（不要含糊）

**好的发现：**「第 3 段旁白在 10 秒窗口内 180 词——约 1080 wpm，无法念完。砍到 25 词。」
**差的发现：**「脚本可能太长。」

### 步骤 4：对照 Playbook 交叉检查

若有 active style playbook，验证：
- [ ] 颜色引用与 playbook 色板一致
- [ ] 转场类型在 playbook 允许集合内
- [ ] 遵守 pacing 规则（最短/最长时长）
- [ ] 素材描述包含 playbook 风格线索
- [ ] 未违反质量规则

每项违规记为 **suggestion** 级别发现。

### 步骤 4b：品味方向审查

若存在 `proposal_packet.production_plan.taste_profile` 或 active playbook 的 `taste_profile`，验证：
- [ ] `design_read` 解释 brief、受众与交付承诺；不能只是「现代/干净/专业」
- [ ] `visual_variance`、`motion_intensity`、`information_density` 体现在场景布局、pacing、标注密度与素材 prompt 中
- [ ] 当 atelier 工作、AI 图/视频、产品/品牌视觉或 mood board 依赖视觉细节时，存在 `reference_strategy`
- [ ] 列出的 `anti_patterns` 确实被避免
- [ ] 质量关卡足够具体，下一阶段可执行

在 proposal 阶段，preset/低 stakes 工作缺少 `taste_profile` 为 **suggestion**；atelier、产品/品牌、launch、hero 或 custom-playbook 工作为 **critical**。在 scene_plan/edit/compose，拨盘违规为 **suggestion**，除非破坏已批准的交付承诺。

### 步骤 5：评估 Success Criteria

对 manifest 中每个 `success_criteria` 项：
- 标准是否满足？（yes/no/partial）
- 未满足则创建 **critical** 发现

### 步骤 6：做出决策

按严重级别统计发现：

| 场景 | 动作 |
|------|------|
| 0 critical，任意 suggestion/nitpick | **Pass** — 进入 checkpoint。记录 suggestion。 |
| 1+ critical 发现 | **Revise** — 修复全部 critical，再审查（最多 2 轮）。 |
| 2 轮修订后仍有 critical | **Pass with warnings** — 仍继续，记录未解决问题。永不无限阻塞。 |

### 步骤 7：记录审查

将审查结构化为：

```
## Review: [stage_name] — Round [N]

**Decision:** PASS / REVISE / PASS_WITH_WARNINGS

### Findings

1. [CRITICAL] Title of finding
   - Description: What's wrong
   - Action: What to fix
   - Status: pending / fixed / accepted / deferred

2. [SUGGESTION] Title of finding
   - Description: What could be better
   - Action: How to improve
   - Status: pending / accepted / deferred

### Summary
- Critical: N (N fixed)
- Suggestions: N
- Nitpicks: N
- Playbook violations: N
- Success criteria met: N/M
```

## 关键原则

1. **具体，不要含糊。**「hook 弱」没用。「hook 是提问但没有紧迫感——试试用 key_point #2 的惊人数据开场」才可执行。

2. **Critical 就是 critical。**不要夸大严重度。缺 schema 字段是 critical。略啰嗦的段落是 suggestion。逗号 splice 是 nitpick。

3. **最多两轮。**目标是交付，不是完美。两轮修订后带 warnings 通过并继续。完美主义会拖死流水线。

4. **审 artifact，不审过程。**你检查的是产出，不是怎么做的。若 brief 有说服力，agent 用了非常规路径也无所谓。

5. **Playbook 即法。**若 playbook 说「屏幕上不超过 3 种颜色」，那是约束不是建议。违规一律标出。

## 阶段专项审查指引

| 阶段 | 最重要的事 |
|-------|-------------------|
| research | 来源多样性、主张可验证性、视觉参考质量 |
| proposal | 交付承诺清晰、renderer family 与 render runtime 选择、音乐/旁白计划、decision log 已启动 |
| idea | Hook 独特性、研究深度、角度多样性 |
| script | 时间准确、叙事弧、enhancement cue 密度 |
| scene_plan | 全覆盖、视觉多样性、素材可行性、slideshow 风险分 |
| assets | 文件存在、风格一致、预算遵守 |
| edit | 时间线覆盖、音画同步、字幕存在、交付承诺合规 |
| compose | 可播放、时长准确、音频质量、pre-compose 校验通过 |
| publish | SEO 质量、元数据完整、导出打包 |

## 参考对齐审查

存在 VideoAnalysisBrief 时（参考驱动制作），在 **每个阶段** 运行。

### 检查：

1. **Grounding 检查：** 产出是否引用 VideoAnalysisBrief 的具体发现，还是在臆造参考？
   - Proposal 说「快节奏」但 reference 的 pacing_style 是 `slow_contemplative` → **CRITICAL**
   - 脚本声称参考有旁白但 VideoAnalysisBrief 显示无旁白 → **CRITICAL**

2. **差异化检查：** 每个 concept/场景相对参考是否有清晰创意差异，还是照抄？
   - Proposal 与参考一模一样（同题、同结构、同处理）→ **CRITICAL**
   - 每个 concept 至少一点必须与参考不同 → 弱则为 **SUGGESTION**
   - brief 中的创意差异化 seed 应体现在 proposal 中

3. **承诺保留：** 用户说爱参考的要素在产出中是否仍在？
   - 用户说「我爱这个 pacing」但 scene_plan 场景时长约 2 倍 → **SUGGESTION**
   - 用户说「保留 hook 风格」但脚本用了不同 hook → **SUGGESTION**

4. **成本对齐：** 成本估算是否仍准，范围是否蔓延？
   - 实际花费超估算 >30% 且用户未再批准 → **CRITICAL**
   - 在已批 proposal 外新增素材 → **SUGGESTION**

### 严重级别：
- 关于参考视频的事实错误：**CRITICAL**
- 无差异化的照抄：**CRITICAL**
- 弱差异化（仅表面改动）：**SUGGESTION**
- 未尊重用户偏好：**SUGGESTION**
- 成本漂移 >30%：**CRITICAL**

## Slideshow 风险审查

在 **scene_plan** 与 **edit** 阶段运行。用 `lib/slideshow_risk.py` 计算分数。

### scene_plan 阶段：
1. 计算 `score_slideshow_risk(scenes, renderer_family=renderer_family)`
2. verdict 为 **"fail"**（平均 ≥ 4.0）：**CRITICAL** — 必须修订 scene plan 才能继续
3. verdict 为 **"revise"**（平均 ≥ 3.0）：**SUGGESTION** — 标出得分 ≥ 3.5 的维度
4. verdict 为 **"strong"** 或 **"acceptable"**：写入审查摘要，无需发现项

### edit 阶段：
1. 用完整 edit_decisions 重算：`score_slideshow_risk(scenes, edit_decisions, renderer_family)`
2. 同样阈值——若 edit 阶段变差（比 scene_plan 分更高），标出

### 各维度得分 ≥ 3.0 时怎么说：
| 维度 | 说法 |
|-----------|------------------------------|
| repetition | 「X 个场景用相同 layout/shot size — 变化视觉语法」 |
| decorative_visuals | 「X 个场景无 stated purpose（无 information_role 或 shot_intent）」 |
| weak_motion | 「有镜头运动但缺叙事理由」 |
| weak_shot_intent | 「X 个场景缺 shot_intent — 这一帧为何存在？」 |
| typography_overreliance | 「X% 场景是文字/stat 卡 — 像 animated slides」 |
| unsupported_cinematic_claims | 「声称 cinematic 但缺 hero moments / lighting / movement」 |

## Decision Log 审查

在 **proposal 之后每个阶段** 运行。decision log（`schemas/artifacts/decision_log.schema.json`）是累积审计轨迹。

### 检查：
1. **存在性**：checkpoint 是否引用 `decision_log_ref`？proposal 之后若没有，标 **SUGGESTION**。
2. **覆盖度**：每个重大选择是否有条目？必须记录的关键决策：
   - Provider 选择（用哪个图/视频/音频工具及原因）
   - Style/playbook 选择
   - 音乐轨选择
   - 声音选择
   - Renderer family 选择
   - 任何 fallback 或降级（如 motion → still）
3. **质量**：每条 decision 应有：
   - 至少 2 个 `options_considered`（不只是选中的）
   - 非套话的 `reason`（「best option」不是理由）
   - 正确的 `confidence`（0.0–1.0）——若全是 1.0 标出（不现实）
4. **用户可见性**：`user_visible: true` 的应是用户真会在意的（非内部路由）

### 严重级别：
- proposal 后缺 decision log：**SUGGESTION**（首次），**CRITICAL**（edit 阶段仍缺）
- 只有 1 个 option considered：**SUGGESTION** — 「记录被拒绝的备选以便审计」
- 全部 confidence 1.0：**SUGGESTION** — 「confidence 不现实 — 至少 provider 选择有 tradeoff」

## 创意差异化审查

在 **scene_plan** 与 **edit** 阶段运行。防止「每个视频看起来一样」的失败模式。

### 检查：
1. **Variation 检查**（仅 scene_plan）：用 `lib/variation_checker.py` → `check_scene_variation(scenes)`。
   - verdict 为 "poor"（score ≤ 2）：**CRITICAL** — 「Scene plan 缺 variety：[列出 violations]」
   - verdict 为 "fair"（score ≤ 3）：**SUGGESTION** — 注明 checker 的具体建议

2. **Playbook 对齐**：active playbook 是否适合本内容？
   - 电影 trailer 用 "clean-professional" theme → 标 mismatch
   - 教育 explainer 用 "anime-ghibli" theme 且无用户要求 → 标出

3. **Shot language 完整度**（scene_plan）：
   - 每场景至少应有 `shot_size` 与 `shot_intent`
   - Hero moments 应有完整 shot_language（6 字段全）
   - shot_language 为空的场景标 **SUGGESTION**

4. **Renderer family 匹配**（edit 阶段）：
   - edit_decisions 中 `renderer_family` 是否与 proposal 设定一致？
   - 无 decision log  documented 原因而变更 → **CRITICAL**

5. **Render runtime 匹配**（edit 与 compose 阶段）：
   - edit_decisions 中 `render_runtime` 须与 proposal_packet.production_plan.render_runtime 一致
   - 无 `render_runtime_selection` decision 记录而变更 → **CRITICAL**
   - compose 阶段 `final_review.checks.promise_preservation.runtime_swap_detected` 须为 `false`。若为 `true` 且无批准的 `render_runtime_selection` decision → **CRITICAL**
   - compose 时 runtime 不可用不是静默 swap 的借口——正确做法是升级、获批准、记 decision，再跑。

6. **Runtime 选择须呈现两个选项**（proposal 阶段，**强制**）：
   - 查询 `video_compose.get_info()["render_engines"]`。若 `remotion` 与 `hyperframes` 均为 `True`，`decision_log` 中 `render_runtime_selection` 的 `options_considered` **必须**包含两种 runtime。
   - 机器上两种可用但 `options_considered` 只有一种 → **CRITICAL**。Agent 静默默认；用户未看到备选。重开 proposal 阶段并呈现两者。
   - 若只有一种可用，`options_considered` 仍须列出不可用项并 `rejected_because: "runtime not available on this machine"` — 否则审计轨迹丢失「选择受约束而非随意」的事实。
   - 按 AGENT_GUIDE.md >「Present Both Composition Runtimes (HARD RULE)」：流水线建议的「默认」runtime **不是**跳过与用户对话的许可。

## 交付承诺审查

在 **edit** 与 **compose** 阶段运行。使用 `lib/delivery_promise.py`。

### edit 阶段：
1. 从 proposal packet 或 edit_decisions metadata 提取 delivery promise
2. 对 resolved cut list 运行 `promise.validate_cuts(cuts)`
3. 若 `valid` 为 False：**CRITICAL** — 「Delivery promise violation: [violations]」
4. 检查 `motion_ratio`：motion-led 承诺但 motion cuts < 50%，即使 technically valid 也标出

### compose 阶段：
1. `video_compose.py` 中 `_pre_compose_validation()` 自动强制执行
2. 审查应确认未绕过校验（查 render report 的 warnings）
3. 若 motion-led 承诺 motion ratio 低但 render 仍成功，标 **SUGGESTION**

## 源素材理解审查

存在用户提供的媒体文件时，在 **research** 与 **proposal** 阶段运行。

### 检查：
1. **存在性**：若项目有用户文件，是否存在 `source_media_review` artifact？
   - 有用户媒体但无 `source_media_review`：**CRITICAL** — 「用户提供了媒体但 agent 规划前未检查。继续前运行 `lib/source_media_review.review_source_media()`。」
2. **实际检查**：每个文件条目是否 `reviewed: true` 且 `technical_probe` 非空？
   - `reviewed` 缺失或 `technical_probe` 空：**CRITICAL** — 「source_media_review 声称已审但无 probe 数据。文件未实际检查。」
3. **规划反映**：`planning_implications` 是否出现在 proposal 的 production plan？
   - 已识别质量风险（如低分辨率、mono 音频）但 proposal 未提及：**SUGGESTION** — 「源媒体有风险但 proposal 未处理。」
4. **内容准确**：计划是否依赖源媒体实际没有的内容？
   - 如计划假设访谈对话但 transcript_summary 无 speech：**CRITICAL** — 「计划假设对话但源媒体无 speech。」
5. **无臆造内容**：Agent 不得仅凭文件名推断无依据内容。若 `content_summary` 说「interview footage」但 probe 只有 3s 静音视频，标 **CRITICAL**。

### 严重级别：
- 有用户文件但缺 `source_media_review`：proposal 阶段 **CRITICAL**
- 未 review 的文件（无 probe）：**CRITICAL**
- 计划未反映质量风险：**SUGGESTION**
- 计划假设源中不存在的内容：**CRITICAL**

## 最终自审审查

在 **compose** 与 **publish** 阶段运行。确保 agent 审查了实际渲染输出。

### compose 阶段：
1. **存在性**：`render_report` 旁是否有 `final_review` artifact？
   - 缺失：**CRITICAL** — 「Compose 产出 render_report 但无 final_review。呈现前 agent 必须检查渲染输出。」
2. **状态检查**：`final_review.status` 是什么？
   - `pass` → OK，继续
   - `revise` → agent 应在呈现前修复。若流水线仍继续：**CRITICAL** — 「自审发现需 revise 的问题但 agent 仍呈现。」
   - `fail` → 流水线**不得**继续。若继续：**CRITICAL**
3. **检查完整度**：5 项必需检查须有数据：
   - `technical_probe` 须显示有效 container 与 plausible duration/resolution
   - `visual_spotcheck` 须 `frames_sampled >= 4`
   - `audio_spotcheck` 须报告旁白/音乐存在
   - `promise_preservation` 须确认 `delivery_promise_honored`
   - `subtitle_check` 须报告有/无
   - 任一项数据缺失：**SUGGESTION** — 「自审检查 [X] 数据不完整」
4. **承诺保留**：若 `promise_preservation.silent_downgrade_detected` 为 true：**CRITICAL** — 「自审检测到从 motion-led 静默降级为 still-led。」

### publish 阶段：
1. 确认 `final_review` 作为必需 artifact 传递
2. 若 `final_review.status` 不是 `pass`：**CRITICAL** — 「不能带着未通过的自审发布」
3. 若 `final_review.issues_found` 非空且 `recommended_action` 不是 `present_to_user`：**SUGGESTION** — 「自审发现问题；发布前确认已解决」

## 合成创作模式审查

模板→atelier 反转（`AGENT_GUIDE.md` →「Composition Authoring Mode」+ `skills/meta/bespoke-composition.md`）是治理，不是建议。reviewer 是 enforcement 点：没有这些检查，下一 agent 会悄悄回到 stock cut-schema，每个视频又开始长得一样。

### proposal 阶段：
1. `decision_log` 须有 `composition_mode` decision，`options_considered: ["templated","atelier"]` 及 tied 到 brief 的真实 `selected` 与 reason。
   - 完全缺 `composition_mode` decision：**CRITICAL** — 「Proposal 缺 composition_mode 选择。Atelier vs templated 是强制呈现决策（见 AGENT_GUIDE.md → Composition Authoring Mode）。」
   - 只记录一个 option considered：**CRITICAL** — 「composition_mode decision 未呈现 templated 与 atelier 两种备选。」
2. 对 **hero 工作**（brief 标 marketing / launch / brand piece / explainer-with-quality-bar / 任何以质量为点的单交付物）且 `selected == "templated"`：**CRITICAL** — 「Hero brief 锁定 composition_mode='templated'。按 doctrine 默认是 atelier；templated 须在 `decision_log.<entry>.reason` 有明确理由（如 localization variant、batch、time-boxed draft）。」仅当 reason 字段命名 sanctioned 例外时可 suppress。
3. 若 `composition_mode == "atelier"` 且 `proposal_packet` 缺 `art_direction` 声明（palette、type、motion、signature device）：**CRITICAL** — 「Atelier proposal 缺 art-direction 承诺。按 `skills/meta/bespoke-composition.md` 步骤 1，art direction 须在写场景*之前*落笔。」

### scene_plan / edit 阶段（当 composition_mode == "atelier"）：
1. `edit_decisions.composition_mode` 须等于 `"atelier"`，且 `edit_decisions.bespoke.{entry, composition_id, art_direction}` 均须设置。
   - 缺 `entry`/`composition_id` 任一：**CRITICAL** — 「Atelier compose 合约不完整；`_render_via_atelier` 会拒绝 render。」
   - 缺 `art_direction`：**CRITICAL** — 「Atelier 无 art-direction 声明；reviewer 无法评估 distinctness。」
2. `edit_decisions.cuts` 中出现 stock `cut.type` 场景类型（`text_card`、`stat_card`、`bar_chart`、`kpi_grid`、`callout`、`comparison`、`hero_title`、`terminal_scene`、`anime_scene`、`progress_bar`、`pie_chart`、`line_chart`）：**CRITICAL** — 「Atelier 作品使用 stock cut.type {name}。手写场景；stock registry 是 mechanics codex，不是零件箱（`skills/meta/bespoke-composition.md`）。」

### compose 阶段（当 composition_mode == "atelier"）：
1. compose 阶段的 `final_review.checks.atelier` 块必须存在。若缺失：**CRITICAL** — 「Atelier render 跳过 doctrine 检查 — `_render_via_atelier` 返回但无 `atelier` checks；查 tool wiring。」
2. 若 `final_review.checks.atelier.stock_reuse_detected == true`：**CRITICAL** — 「Bespoke 项目内 import stock registry（{offending_imports[0].file} → {offending_imports[0].import}）。手写场景；不要从 stock src/ import。」
3. 若 `final_review.checks.atelier.art_direction_declared == false`：**CRITICAL** — 「Atelier render 无 art-direction 声明。重 render 前设置 `edit_decisions.bespoke.art_direction`。」
4. **场景 distinctness — 无 hero-component spine（强制记录）。** 每场景采样一帧代表（如各 `props.sections[i]` 窗口中点），在审查记录中回答：
   - *每个场景是否有 distinct 主视觉主体？* 若两场景以上共享主视觉（同一 hero 元素仅改 caption — 永不离开的蜡烛、每 beat 的 browser frame、当脚手架的 score ring）：**CRITICAL** — 「检测到 hero-component spine：场景 {ids} 共享主视觉主体。按 `skills/meta/bespoke-composition.md` 步骤 1.5，每场景须 earn 自己的 composition；signature device 属于一个 climactic beat，不是脚手架。重规划受影响场景。」
   - *`art_direction` 中命名的 signature device 是否至少出现在一个 beat？*（否 ⇒ CRITICAL，重写或更新声明以匹配实际构建）
   - *signature device 是否出现在**大多数** beat？*（是 ⇒ CRITICAL — 见 hero-component-spine；signature 应稀缺）
   此检查不能静默跳过；未记录 scene-by-scene inventory 本身为 **CRITICAL**（「scene_distinctness inventory 未记录」）。
5. **字幕 / 屏上文字去重（强制检查）。** 比较 active caption 与同一时间窗内渲染的屏上文字：
   - 若内容相同（caption 复读场景 title/headline 而旁白已在念）：**CRITICAL** — 「{t}s 处 caption 与屏上文字重复（'{text}'）。整片决定一次：caption 是增义（数字、人名、翻译）还是 accessibility 字幕；同一行不要两者兼有。要么这些场景 `captions=[]`，要么去掉冗余 on-screen SerifLine。」
6. **Distinctness 审查（人工判断，强制）。** 批准 render 前 reviewer 须在审查记录中明确回答：
   - *「这视频会不会是任意其他产品的视频？」*（是 ⇒ CRITICAL，重写 art direction）
   - *「其视觉语言是否复用我之前某片的 look？」*（是 ⇒ CRITICAL，重写）
   Distinctness 是 tool 无法自动化的 taste  territory；未回答此问题本身为 **CRITICAL**（「distinctness review 未记录」）。

### publish 阶段（当 composition_mode == "atelier"）：
1. 上述六项 atelier compose 检查（`atelier` 块存在、stock_reuse、art_direction_declared、scene_distinctness、captions/text dedup、人工 distinctness review）须在审查记录中显示 `resolved`。任一项未 resolved：**CRITICAL** — 「不能发布仍有未 resolved doctrine 或 distinctness 发现的 atelier 作品。」
