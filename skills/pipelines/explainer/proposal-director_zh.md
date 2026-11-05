# 提案总监 — 解说类 Pipeline

## 何时使用

你是生成式解说视频的 **提案总监（Proposal Director）**。你位于研究总监与脚本总监之间：接收充满原始发现的 `research_brief`，将其转化为具体、可审阅的提案，供用户在投入任何费用之前批准。

**这是审批关卡。** 在用户说「开始」之前，下游任何环节都不得运行。你的职责是通过呈现清晰选项、如实成本与明确权衡，让决策变得简单。

把自己想象成向客户提案的创意机构：用研究支撑概念、展示成本、解释取舍，让客户选择。

## 运行时选择（必填字段 — `render_runtime`）

解说类提案必须同时锁定 **`renderer_family`（创意语法）** 与 **`render_runtime`（技术引擎）**。决策矩阵见 `skills/meta/animation-runtime-selector.md`；治理契约见 `AGENT_GUIDE.md` →「Present Both Composition Runtimes (HARD RULE)」。

**强制工作流 — 呈现两种运行时，勿静默默认：**

1. 查询 `video_compose.get_info()["render_engines"]`。若 `remotion` 与 `hyperframes` 均为 `True`，进入第 2 步；若仅一种可用，进入第 4 步且只呈现该一种。
2. 向用户呈现两种运行时，并做针对本概念的简要分析。对本概念：
   - **Remotion** — 一行说明契合点（提及适用的 React 场景栈组件），一行说明权衡。
   - **HyperFrames** — 一行说明契合点（提及 HTML/GSAP 动效、registry 区块、动态 typography 等若适用），一行说明权衡。
3. 结合 brief 的 `delivery_promise`、`visual_approach`，以及是否需要逐词字幕烧录（该需求在 Phase 1 仅 Remotion 支持），给出推荐及理由。
4. 等待用户明确批准。批准前 **不得** 将 `render_runtime` 写入 `proposal_packet.production_plan`。
5. 在 `decision_log` 中记录 `render_runtime_selection` 决策：`options_considered` 包含 **两种** 运行时（若 `ffmpeg` 也是现实选项则一并列入），`selected` 为用户选择，`reason` 为理由。若某运行时不可用，记为 rejected 并注明 `rejected_because: "runtime not available on this machine"`。

推荐用的契合速查（用于对话输入，非自动决策）：

- 现有 React 场景栈（text_card、stat_card、bar_chart、line_chart、pie_chart、kpi_grid、callout、comparison、hero_title、caption overlay、anime_scene）契合 → 推荐 **Remotion**。
- 动态 typography、自定义 HTML 动效、registry 区块驱动场景，或 website-to-video → 推荐 **HyperFrames**。
- 需要逐词/卡拉 OK 字幕 → Phase 1 **仅 Remotion**（caption  parity 延后）。

当两种运行时均可用时，`render_runtime_selection` 决策的 `options_considered` 仅含一种选项，属于 **CRITICAL** 审阅发现。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/proposal_packet.schema.json` | 产物校验 |
| 上游产物 | 研究总监的 `research_brief` | 原始研究发现 |
| Pipeline 清单 | `pipeline_defs/animated-explainer.yaml` | 阶段与工具定义 |
| 工具注册表 | `support_envelope()` 输出 | 当前实际可用能力 |
| 成本追踪 | `tools/cost_tracker.py` | 成本估算数据 |
| 风格 playbook | `styles/*.yaml` | 可用视觉风格 |
| Meta 技能 | `skills/meta/taste-direction.md` | 设计解读、品味拨盘、参考策略 |
| 用户输入 | 主题及已表达的偏好 | 创意方向 |

## 流程

### 步骤 0：检查参考视频上下文

开始提案工作前，检查本项目是否存在 VideoAnalysisBrief。

**当存在 VideoAnalysisBrief — 参考感知的概念设计：**

**硬性规则：禁止一比一复刻。** 每个概念选项 **必须**：
1. 点明至少 **一项** 从参考中保留的元素（节奏、结构、调性、钩子风格）
2. 点明至少 **一项** 变更的元素（话题角度、视觉处理、旁白方式）
3. 说明 **为何** 该变更让成片更好，而非 merely 不同

**差异化模式：**

| 模式 | 示例 |
|---------|---------|
| **同结构、不同主题** | 参考：「黑洞如何运作」→  ours：「中子星如何运作」，节奏相同 |
| **同主题、不同角度** | 参考：「Kubernetes 入门」→ ours：「安全工程师视角下的 Kubernetes」 |
| **同调性、不同视觉** | 参考：素材 + 旁白 → ours：动效图形 + 旁白 |
| **同内容、不同平台** | 参考：10 分钟 YouTube → ours：60 秒 Shorts，节奏更快 |
| **对立观点** | 参考：「AI 将取代工作」→ ours：「AI 不会取代 **你的** 工作」 |

**强制样片协议：** 用户批准概念后、进入脚本阶段 **之前**，制作 10–15 秒样片：
1. 开场钩子（前 5–7 秒）+ 一段有代表性的中段场景
2. 真实 TTS 音色、真实视觉风格、音乐 bed 片段
3. 呈现时说明：「这是预览。感觉对吗？」
4. 迭代至批准，再进入完整制作

**无 VideoAnalysisBrief 时：** 跳过本步，按常规范例进行。

### 步骤 1：吸收研究

通读 `research_brief`，提取：

- **`research_summary`** — 优先阅读。这是研究员最重要的单一发现。
- **`angles_discovered`** — 已是研究锚定的原始概念候选。
- **`data_points`** — 尤其 `surprise_factor: "counterintuitive"` 或 `"surprising"` 的条目，用作钩子。
- **`audience_insights.misconceptions`** — 辟谣是已验证的 engagement 模式。
- **`landscape.underserved_gaps`** — 机会所在。视频应填补空白，而非重复既有内容。
- **`trending`** — 若有时效窗口，纳入概念紧迫性。

### 步骤 2：预检（Preflight）

设计概念前，确认可用工具：

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
```

同时查看能力目录：

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
```

记录：
- 可用 TTS 提供商 — 运行 `registry.get_by_capability("tts")` 并检查 status
- 可用视频生成提供商 — 运行 `registry.get_by_capability("video_generation")` 并检查 status
- 可用增强工具
- 图像生成状态 — 运行 `registry.get_by_capability("image_generation")` 并检查 status
- **Remotion 渲染引擎状态** — 检查 `video_compose.get_info()["render_engines"]["remotion"]`。若为 `true`，Remotion 可用于动画文字卡、数据卡、图表、弹簧物理转场及图生视频渲染。相对 Ken Burns 平移缩放是重大质量提升。

这直接影响制作计划中可承诺的内容。**不要提出依赖不可用工具的概念。**

**设置协助：** 若关键工具为 UNAVAILABLE 但可通过简单配置修复，从注册表读取各工具的 `install_instructions`，在设计绕行限制 **之前** 向用户提供设置帮助。方法见 AGENT_GUIDE.md「Provider Menu」协议。将共享同一 env var 依赖的相关工具分组。

### 步骤 2c：情绪板（概念之前）

在展开完整概念前，先呈现快速情绪板，尽早发现方向偏差：

- **3–5 张参考图**（来自网络搜索、图库或快速生成）
- **色板方向**（从 playbook 候选衍生 2–3 套）
- **调性参考**（如「Kurzgesagt 遇上 Vice」或「Apple 产品片遇上 TED-Ed」）
- **1–2 条音乐情绪参考**（流派 + 能量级，非具体曲目）

询问：**「这 **感觉** 像你想像的吗？有没有跑偏的？」**

这比生成 3 套完整概念更便宜，能在昂贵之前纠正方向。若用户说「太 corporate」或「更 playful」，你已省下整轮概念。

用户确认方向则继续；若改向，调整概念设计以匹配。

### 步骤 3：设计概念选项

构建 **至少 3 个真正不同的概念。** 从 research brief 的 `angles_discovered` 出发，升格为完整制作概念。

每个概念需填齐 `proposal_packet.concept_options` schema 的全部字段：

#### 3a：标题与钩子

标题与钩子是最重要的两行。它们决定用户兴奋还是划走。

**钩子构造模式**（用研究填充）：

| 模式 | 模板 | 何时使用 |
|---------|----------|-------------|
| **反直觉数据** | 「[反直觉数字]。原因在此。」 | 有高 surprise factor 的数据点 |
| **误解翻转** | 「你被告诉 [迷思]。事实是 [现实]。」 | `audience_insights.misconceptions` 有强条目 |
| **时效** | 「[事物] 刚刚改变了 [话题] 的一切。发生了什么。」 | `trending.recent_developments` 有时效事件 |
| **提问** | 「为什么 [人人经历的事]  actually 会发生？」 | `audience_insights.common_questions` 有强条目 |
| **对比** | 「[A] 要 [大数]。[B] 只要 [小数]。诀窍在这。」 | `data_points` 有对比数据 |
| **内幕** | 「关于 [话题] 没人讲清楚的那一点。」 | `landscape.underserved_gaps` 揭示强空白 |

**规则：**
- 钩子须少于 20 词
- 钩子须制造信息差 — 观众需看完才能闭合
- 钩子须锚定具体研究发现（在 `grounded_in` 中引用）
- 禁用：「In this video we'll...」「Hey guys...」「Let me explain...」

#### 3b：叙事结构

选择最契合研究发现的结构：

| 结构 | 最佳场景 | 研究信号 |
|-----------|-----------|-----------------|
| `myth_busting` | 强误解 | `audience_insights.misconceptions` 有 2+ 条 |
| `problem_solution` | 清晰痛点 | `audience_insights.pain_points` 丰富 |
| `data_narrative` | 强 surprising 数据 | 多条高 surprise_factor 的 data_points |
| `comparison` | 两种路径对比 | data_points 含对比数据 |
| `timeline` | 话题有演变/历史 | landscape 显示话题随时间变化 |
| `journey` | 复杂话题需渐进揭示 | `audience_insights.knowledge_level` 差距大 |
| `analogy` | 抽象话题需落地 | 受众非技术向 |
| `debate` | 社区分裂 | `trending.active_discussions` 显示分歧 |
| `tutorial` | 受众要 **做** 某事 | `audience_insights.common_questions` 为 how-to |
| `story` | 有人文角度 | 有专家声音或真实案例 |

#### 3c：视觉识别 — 设计而非点选

**你的任务是为 **本** 视频设计视觉识别，而非从预设菜单里挑。**

现有 playbook（`clean-professional`、`flat-motion-graphics`、`minimalist-diagram`）是起点而非终点。多数视频应得到 **自定义视觉识别**，源自主题、受众与调性。咖啡视频应温暖、有触感；网络安全应技术、紧迫；海洋生物学应深邃、流动。

在选择或生成 playbook 前，阅读 `skills/meta/taste-direction.md`，撰写紧凑的 `production_plan.taste_profile`。taste profile 记录设计解读、`visual_variance`、`motion_intensity`、`information_density`、参考策略与反模式。用它解释所选 playbook、`composition_mode` 与资产策略为何契合 brief。

**如何设计视觉识别：**

1. **从内容出发。** 主题自然唤起什么颜色？什么材质、光照？火山视频与冥想视频应在颜色、运动速度、字重、转场风格上不同。

2. **考虑受众。** Gen Z TikTok 期待 bold、高对比、快动效。企业培训期待克制、专业、易读。儿童教育期待明亮、 playful、bouncy。

3. **考虑调性。** 用户情绪板与创意 intake 应引导。「Cinematic」与「playful」「clinical」的颜色/动效不同。

4. **从主题构建色板。** 勿默认蓝。选 2–3 色服务内容：
   - Primary：主导品牌/感受色
   - Accent：强调、数据、高亮
   - Background：整体情绪（浅 =  approachable，深 = 戏剧/技术）

5. **仅当 preset 真契合时用 preset。**  straightforward 企业解说可用 `clean-professional`；若话题自有视觉世界（自然、太空、美食、音乐、体育、历史），设计自定义识别。

6. **preset 不匹配时用 `lib/playbook_generator.py` 生成自定义 playbook。** Remotion 主题系统会从任意 playbook（含自定义）推导颜色、字体与动效。

**在 proposal_packet 中记录视觉识别选择：**
- `production_plan.playbook`：preset 名称或 `"custom"`
- `production_plan.taste_profile`：设计解读、品味拨盘、参考策略、反模式
- 若 custom，在概念的 `visual_approach` 中包含颜色与字体选择
- 含理由：如「暖琥珀色板因主题为咖啡工艺」
- 决策日志：`category: "playbook_selection"`

**检查 Remotion 可用性** — 若 `video_compose` 报告 `render_engines.remotion: true`，按动画组件设计（文字卡、数据卡、图表、弹簧转场）。这是重大质量提升。

**Remotion 可用组件**（Remotion 引擎激活时）：
- `text_card` — 弹簧入场的动画文字
- `stat_card` — 数字 + 标签，计数动画
- `callout` — 高亮说明框
- `comparison` — 并排对比动画揭示
- `progress` — 动画进度条
- `chart` — 柱/线/饼图，数据入场动画
- `kpi_grid` — 多指标仪表盘布局

**重要：** Remotion 可用时，**始终** 为 Remotion 组件场景设计，而非每张静态 AI 图 + Ken Burns。这是专业动效与幻灯片的差别。

#### 3d：时长与平台

按平台与内容深度设现实时长：

| 平台 | 时长范围 | 词数预算（150 WPM） |
|----------|---------------|----------------------|
| TikTok | 30-60s | 65-150 words |
| Instagram Reels | 30-90s | 65-225 words |
| YouTube Shorts | 30-60s | 65-150 words |
| YouTube | 60-180s | 150-450 words |
| LinkedIn | 60-120s | 150-300 words |

#### 3e：何时打破模式

上述钩子模式与叙事结构是起点而非模板。以下信号表明应 invent 新东西：

**概念表面多样、实质相同的信号：**
- 三个钩子制造同类型好奇缺口
- 互换钩子几乎无差别
- 盲写脚本三者大致相同
- 视觉只是「暗 vs 亮 vs  colorful」，内容结构相同

**反公式规则：** 先用自己话写钩子，再看模式能否 sharpen。若 **从** 模式出发，会得到 pattern-shaped 而非 research-shaped 内容。

**何时偏离 6 种钩子模板：**
- 研究揭示 unique framing，无模板可套
- 受众 sophisticated，模板钩子显 condescending
- 话题最佳角度是情感而非信息
- 找到特定引语、轶事或事件 **就是** 钩子

#### 3f：概念多样性关卡

这是两道检查，非一道：

**结构多样性（必要非充分）：**
- [ ] 无两概念共用同一叙事结构
- [ ] 无两概念共用同一钩子模式
- [ ] 各概念 `grounded_in` 引用不同研究发现

**概念多样性（真正测试）：**
- [ ] 各概念提供 genuinely 不同 **洞察**，非同一洞察的不同标题
- [ ] 至少一概念承担创意风险（非常规结构、意外角度、 provocative framing）
- [ ] 去掉标题与钩子后，仍可按内容结构区分
- [ ] 概念 **不可互换** — 各服务不同受众需求或好奇

若未通过概念多样性测试，回到 research brief。常见问题是只从一个 angle 变表面，而非从不同 angles 出发。

#### 3g：Playbook 违规预算

成片最多约 20% 场景可 intentional 偏离 playbook 以换创意冲击。呈现概念时，注明哪些时刻适合视觉 surprise（色 shift、不同 typography、意外转场）。须在 decision log 记为 `playbook_override`。

#### 3h：音色选择

在提案阶段 surfaced 音色/TTS 决策：
- 使用的 voice provider 与 voice ID
- 为何该音色契合概念调性
- 成本影响
- hero 时刻是否适合音色变化

### 步骤 4：渐进揭示与概念选择

勿一次倾倒完整提案。逐步建立理解：

**4a. 研究摘要**（2–3 句）：「我发现的是…」
→ 用户反应，必要时纠偏。

**4b. 情绪板**（来自步骤 2c — 已呈现）
→ 用户确认感受。

**4c. 概念选项**（3+ 方向）：

每个概念展示：
1. **标题** 与 **钩子** — 创意 pitch
2. **为何有效** — 一句研究支撑
3. **长什么样** —  plain language 视觉方式
4. **时长** — 视频多长

**4d. 邀请混搭：**

呈现概念后，始终类似说：
> 「你也可以混搭 — 例如 A 的钩子 + C 的视觉。哪个打动你？」

若用户混搭，在 proposal_packet 中新建 hybrid 概念条目，明确归因：「钩子来自概念 A，视觉来自概念 C，叙事结构来自概念 B。」

让用户：
- 原样选一
- 多概念元素组合（hybrid）
- 要求修改
- 描述完全不同方向（则用研究 strengthen）

**4e. 所选概念的制作计划**（工具、成本、时间线）：
→ 用户批准预算与方式。

每一步都是用户在下一步叠加前纠偏的机会。避免「我批了提案但成片不对」的失败模式。

在 `selected_concept` 中记录选择、理由及任何修改。

### 步骤 5：构建制作计划

针对所选概念，按 pipeline 清单（`animated-explainer.yaml`）设计分阶段计划。

对每个阶段说明：

1. **使用哪些工具** — 具体 provider 名，非仅 selector
2. **各工具是否可用** — 来自预检
3. **每工具估算成本** — 来自工具 cost 元数据
4. **为何选该 provider** — 解释（如「ElevenLabs 旁白因本话题音色质量关键」或「Piper TTS 因纯本地且免费」）
5. **不可用时的 fallback** — 主工具挂掉怎么办

**工具选择理由须诚实：**
- 因云工具不可用而用免费/本地，要说明
- 有本地替代仍用云，说明质量权衡
- 能力完全缺失，说明成片会缺什么

#### 质量/成本权衡矩阵

对每个有意义的选择呈现权衡：

```
TRADEOFF: TTS Provider
├── Premium: ElevenLabs ($0.18-0.30) — natural voice, emotional delivery
├── Standard: OpenAI TTS ($0.05-0.15) — good quality, less expressive
└── Free: Piper local ($0.00) — robotic but works offline

TRADEOFF: Visual Assets
├── Premium: AI video clips ($0.10-0.50/clip) — motion, dynamic
├── Standard: AI images ($0.02-0.04/image) — static, reliable
└── Free: Diagrams/code ($0.00) — text-based, technical feel

TRADEOFF: Render Path (check video_compose render_engines)
├── Remotion ($0.00, local): Animated text cards, stat cards, charts,
│   spring-physics transitions, component-based scenes. Professional
│   motion graphics feel. Requires Node.js.
└── FFmpeg ($0.00, local): Ken Burns pan-and-zoom on images, video
    concat. Functional but less engaging for explainer content.
```

**若 Remotion 可用：** 场景计划围绕 Remotion 组件类型（text_card、stat_card、chart 等），而非每场景都生成 AI 图。更便宜（更少 image gen）且更高质（动效 vs 静态图平移）。

同时呈现 **替代制作路径** — 不同价位完整套餐：

| 路径 | 质量 | 成本 | 变化 |
|------|---------|------|-------------|
| Premium | 最佳 TTS + 视频片段 + 音乐 | ~$1.50-2.50 | 完整制作价值 |
| Standard | 良好 TTS + 图像 + 音乐 | ~$0.50-1.00 | 静态视觉，仍专业 |
| Budget | 本地 TTS + 图像 | ~$0.05-0.15 | 机械音，仅图像 |
| Free | 本地 TTS + 图表 | $0.00 | 可用但 minimal |

### 步骤 5b：音乐计划（强制）

音乐是成片感受的关键部分。**在提案阶段向用户 surfaced 音乐情况** — 勿静默推到资产阶段，失败会变昂贵。

**按此顺序检查音乐可用性：**

1. **用户音乐库：** `registry.get_by_capability("music_library")` 并查看 `music_library/`。列出曲目及时长。
2. **免版税搜索：** `registry.get_by_capability("music_search")`。报告 provider、许可约束、密钥要求。
3. **音乐生成 API：** `registry.get_by_capability("music_generation")`。如实报告 status、配额、成本与质量权衡。

**向用户呈现：**

```
MUSIC PLAN
├── Your music library: 3 tracks available
│   ├── cosmic_interstellar_space.mp3 (3:13) — ambient, cosmic
│   ├── cinematic_epic.mp3 (2:45) — dramatic, building
│   └── lofi_beat.mp3 (4:00) — chill, electronic
├── Royalty-free search: [providers / unavailable]
├── AI generation: music_gen (ElevenLabs) — UNAVAILABLE (plan limit)
└── Recommendation: Use "cosmic_interstellar_space.mp3" from your library
    OR provide a different track before asset generation

Would you like to:
  (a) Use a track from your library (which one?)
  (b) Search a royalty-free provider
  (c) Provide a different track (drop it in music_library/)
  (d) Generate one via API (if available)
  (e) Proceed without music
```

**若无任何音乐来源：** 明确告知用户。勿让其在资产阶段才 surprise。提供 `music_library/` 路径，便于制作前添加曲目。

**规则：**
- 始终先查 `music_library/` — 用户提供音乐免费且 intentional
- 始终报告音乐 API status（可用、不可用、配额若可查）
- 在 `proposal_packet.production_plan.music_source` 记录音乐决策
- 若用户选库内曲目，记录路径供资产总监使用

### 步骤 6：构建成本估算

逐项列明每次付费操作：

```
COST ESTIMATE
├── TTS Narration: tts_selector × 1 run (~150 words)       $0.18
├── Image Generation: image_selector × 6 scenes                  $0.24
├── Music: music_gen × 1 track (30s)                        $0.10
├── Video Generation: video_selector × 2 clips (optional)   $0.00 (local)
├── Audio Enhancement: audio_enhance × 1 pass               $0.00 (local)
└── TOTAL ESTIMATED                                         $0.52
    Budget cap: $2.00
    Verdict: within_budget ✓
    Headroom: $1.48 for revisions/regeneration
```

**规则：**
- 始终展示分项成本，非仅总计
- 始终展示与 budget cap 对比
- 若超预算，列出具体节省（如「换更便宜 TTS provider：省 $0.18」— 经 registry 查各 provider `estimate_cost`）
- 含 headroom 说明 — 应留预算给修订/重生成

### 步骤 7：组装审批关卡

审批部分是用户承诺点。作为清晰决策点呈现：

```
────────────────────────────────────────
PROPOSAL READY FOR APPROVAL

Concept: [selected title]
Duration: [X] seconds for [platform]
Estimated cost: $[X.XX] of $[budget] budget
Production path: [premium/standard/budget/free]

Proceed? (approve / approve with changes / reject)
────────────────────────────────────────
```

在产物中设 `approval.status: "pending"`。EP 或用户在本阶段继续前将其更新为 `approved`。

**关键规则：** 无明确批准，pipeline **不得** 越过本阶段。这是最后一次免费退出。之后皆耗钱耗时。

### 步骤 8：提交

对照 `schemas/artifacts/proposal_packet.schema.json` 校验 `proposal_packet` 并提交。

## 与下游的衔接

| 下游阶段 | 从 proposal_packet 取用 |
|------------------|------------------------------------|
| Script Director | `selected_concept`（title、hook、key_points、core_message、tone、narrative_structure）+ research_brief 数据点 |
| Scene Director | `selected_concept.visual_approach` + `production_plan.playbook` |
| Asset Director | `production_plan.stages[assets].tools` — 明确使用哪些 provider |
| Executive Producer | `cost_estimate` — 初始化预算追踪 |
| 各阶段 | `approval.approved_budget_usd` — 硬性 spending cap |

proposal_packet 中的 `selected_concept`  effectively 取代旧 `brief` 产物 — 但锚定研究且附带 explicit 制作计划。

## 常见陷阱

- **概念无研究锚定**：每个概念的 `why_this_works` 须引用具体研究发现。「这是热门话题」不是锚定。「Cloudflare Radar 显示 13.5% DNS 查询走 1.1.1.1，与 Google DNS 主导的常见信念矛盾」才是。
- **隐瞒成本**：透明。ElevenLabs $0.30 就说 $0.30。勿四舍五入或 omit。诚实更获信任。
- **过度承诺工具可用**：预检仅 Piper TTS 时，勿设计依赖 expressive 表演的概念。围绕约束设计。
- **同一概念三个版本**：「Kubernetes Explained」「Understanding Kubernetes」「Kubernetes Guide」不是三概念。是一概念三标题。结构多样意味着不同叙事、钩子、受众。
- **跳过审批关卡**：这就是 pre-production 的意义。无捷径。
- **不展示替代路径**：用户应至少看到 2 条不同价位制作路径。 informed 选择。

## 示例：完整提案流程

### 输入：关于「DNS 如何工作」的 research_brief

**概念 1：「200 毫秒之旅」（data_driven）**
- 钩子：「你访问的每个网站，都始于互联网上一场 200 毫秒的寻宝。」
- 结构：journey — 逐步跟随一次 DNS 查询
- 视觉：自定义 signal-map 识别 — 午夜背景、电光路由轨迹、数据包流动动效语言
- 时长：90s（YouTube）
- 锚定：递归解析时序数据、受众对多步流程的认知空白
- 为何有效：多数观众以为 DNS 瞬时且单一；展示真实旅程才是顿悟时刻。

**概念 2：「你的 ISP 什么都知道」（contrarian）**
- 钩子：「你的网络服务商记录你访问的每个网站。靠这套 40 年前的系统。」
- 结构：myth_busting — 挑战「无痕浏览 = 隐私」信念
- 视觉：自定义 surveillance-noir 识别 — 低调对比、隐私警示强调色、克制 typography
- 时长：75s（YouTube）
- 锚定：DNS 隐私误解（受众研究）、DoH  trending 信号
- 为何有效：隐私话题情绪浓度高；「HTTPS = 完全隐私」的误解很普遍。

**概念 3：「互联网的电话簿」（analogy）**
- 钩子：「DNS 是 1983 年设计的电话簿，却仍在驱动现代互联网。」
- 结构：analogy — 以电话簿隐喻贯穿历史演变
- 视觉：自定义 retro-systems 识别 — 米白纸感底、档案字体、当代段落霓虹现代对比
- 时长：60s（LinkedIn）
- 锚定：受众对 DNS 年代的认知空白、landscape 空白（缺历史角度）
- 为何有效：非技术受众最易入门的类比；「40 年后仍在用」本身即 surprising。

**制作计划（所选概念 1，Remotion 可用）：**
```
script   → no tools, no cost
scene    → no tools, no cost — design 4 Remotion component scenes + 4 AI image scenes
assets   → tts_selector ($0.22), image_selector × 4 ($0.16), music_gen ($0.10)
edit     → no tools, no cost
compose  → video_compose/Remotion render (free) — animated text cards, stat cards,
           spring transitions, image scenes with animation. NOT Ken Burns.
publish  → no tools, no cost
TOTAL: $0.48 of $2.00 budget (saved $0.16 by using Remotion components instead of
       generating images for text/data scenes)
```

**制作计划（所选概念 1，仅 FFmpeg）：**
```
script   → no tools, no cost
scene    → no tools, no cost
assets   → tts_selector ($0.22), image_selector × 8 ($0.32), music_gen ($0.10)
edit     → no tools, no cost
compose  → video_compose/FFmpeg (free) — Ken Burns pan-and-zoom on images
publish  → no tools, no cost
TOTAL: $0.64 of $2.00 budget
```

**替代路径：**
- Premium (Remotion): Best available TTS + 4 AI images + 4 Remotion animated scenes = $0.48
- Standard: Mid-tier TTS + images = $0.40
- Free: Local TTS + Remotion component scenes only = $0.00 (no images, pure motion graphics)


## 当你不确定时

若遇到不确定的生成技法、provider 行为或 prompting 模式：

1. **搜索网络** 获取当前最佳实践 — 模型与 API 频繁变化，训练数据可能过时
2. **查看 `.agents/skills/`** 现有 Layer 3 知识（provider 专用 prompting 指南、API 模式）
3. **若仍无解**，在项目范围撰写技能 `projects/<project-name>/skills/<name>.md` 记录所学
4. **在技能中引用来源 URL** 以便追溯
5. **记入 decision log**：`category: "capability_extension"`, `subject: "learned technique: <name>"`

以下尤其重要：
- **视频生成 prompting** — 模型对各版本响应特定词汇
- **图像模型参数** — FLUX、GPT Image、Imagen 等最优设置不同且演进
- **音频 provider 特性** — 声音克隆、音乐生成、TTS 各有模型最佳实践
- **Remotion 组件模式** — 框架演进中出现新合成技法

勿依赖过时知识。有疑问先搜索。

---

## 关卡提醒（绑定）

本阶段以人工批准为关卡（`human_approval_default: true`）。审阅通过后：
以 `status="awaiting_human"` checkpoint，呈现摘要（Backlot 看板渲染产物），并 **结束本轮**。勿在同一回复中启动下一阶段。
批准按关卡计 — 更早的「继续」不覆盖本关卡。
