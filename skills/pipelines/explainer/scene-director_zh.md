# 场景导演 — 解说类流水线

## 何时使用

你是生成式解说视频的场景规划师。你手头有一份带时间戳章节与增强提示（enhancement cues）的 `script` 制品。你的任务是把脚本转化为视觉方案：观众在每个时刻看到什么、需要创建哪些资产、场景之间如何过渡。

这是从文字到画面的环节。脚本很好但场景规划很差，成片会令人困惑。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | 制品校验 |
| 前置制品 | `state.artifacts["script"]["script"]`, `state.artifacts["proposal"]["proposal_packet"]` | 脚本章节与提案包 |
| Playbook | 当前启用的风格 playbook | 视觉语言、转场、动效规则 |
| Layer 3 | `.agents/skills/flux-best-practices/`, `.agents/skills/beautiful-mermaid/`, `.agents/skills/manim-composer/` | 图像生成、图表、动画知识 |

## 流程

### 步骤 1：分析脚本

通读每个章节。对每个章节记录：
- 正在解释什么概念？
- 脚本作者嵌入了哪些 enhancement cues？
- 情绪节拍是什么？（好奇、揭示、强调、幽默、收束）
- 可用时长多少？（end_seconds - start_seconds）

### 步骤 2：调研视觉手法

**使用网页搜索**查找该主题的视觉技巧：

1. **头部创作者如何可视化这一主题？** 搜索 YouTube 缩略图、博客图解、会议幻灯片。
2. **哪些视觉隐喻有效？** 部分概念有公认视觉表达（例如神经网络为节点图、加密为锁/钥匙）。使用它们——观众能立刻识别。
3. **有什么新意？** 是否有人未尝试过的可视化？新颖呈现能让解说令人难忘。
4. **什么可行？** 将目标与可用工具对齐：`image_selector`（静态图）、`diagram_gen`（Mermaid 流程图/时序图）、`code_snippet`（语法高亮代码）、Remotion（动态图形、文字动画）、Manim（数学动画）。

若遇到现有技能无法覆盖的可视化需求，使用 **Skill Creator**（`skills/meta/skill-creator.md`）创建新技能。

### 步骤 3：拆解为场景

将每个脚本章节转化为 1–3 个视觉场景。每个场景是一个独立的视觉时刻。

```json
{
  "id": "scene-3",
  "type": "diagram",
  "description": "Mermaid flowchart showing query → encode → vector search → rank → return results. Nodes appear one by one as narrator describes each step.",
  "start_seconds": 15,
  "end_seconds": 22,
  "script_section_id": "s3",
  "framing": "full-screen diagram, centered",
  "movement": "progressive reveal left-to-right",
  "transition_in": "fade",
  "transition_out": "dissolve",
  "overlay_notes": "Label each node as it appears",
  "required_assets": [
    {
      "type": "diagram",
      "description": "Mermaid flowchart: query → encode embedding → vector search (ANN) → rank by cosine similarity → return top-k results",
      "source": "generate"
    }
  ]
}
```

#### 渲染模板与场景类型

规范的 `scene_plan.scenes[].type` 词汇为 `talking_head`、`broll`、
`animation`、`character_scene`、`diagram`、`text_card`、`transition`、
`generated` 和 `screen_recording`。诸如 `hero_title`、`stat_card`
以及下文图表/卡片变体等名称是下游 Remotion 的 `cut.type` 模板，
不是合法的场景规划类型。规划阶段请酌情使用 `text_card` 或
`animation`，并在场景描述中写明目标渲染模板；剪辑阶段再将意图转为 `cut.type`。

| 渲染模板或场景类型 | 最适合 | 可用工具 | 时长建议 |
|------|----------|-----------------|-------------------|
| `hero_title` | 片头标题、戏剧性揭示 | Remotion HeroTitle（主题驱动标题） | 3-5s |
| `stat_card` | 大号数字、冲击性指标 | Remotion StatCard（大数字 + 副标题） | 4-6s |
| `bar_chart` | 类别对比、排名 | Remotion BarChart（grow-up/slide-in/pop 动画） | 5-7s |
| `line_chart` | 趋势、时间序列、增长曲线 | Remotion LineChart（draw/fade 动画、多序列） | 5-7s |
| `pie_chart` | 比例、构成、分布 | Remotion PieChart（环形模式、中心标签、spin/expand） | 5-7s |
| `kpi_grid` | 仪表盘、业务牵引指标、一眼数据 | Remotion KPIGrid（2-4 列，count-up/pop/cascade） | 5-7s |
| `comparison` | 前后对比、A/B、对决 | Remotion ComparisonCard（双值 + 分隔） | 4-6s |
| `callout` | 专家引语、提示、警告、重要说明 | Remotion CalloutBox（info/warning/tip/quote 类型） | 4-6s |
| `progress_bar` | 历程可视化、完成度、堆叠指标 | Remotion ProgressBar（fill/pulse/step 动画） | 4-6s |
| `text_card` | 陈述、收束语、关键术语 | Remotion TextCard（居中、spring 动画） | 3-5s |
| `animation` | 需要动效的概念（数据流、数学） | Remotion、Manim | 4-10s |
| `diagram` | 流程、架构、关系 | `diagram_gen`（Mermaid）、`image_selector` | 4-8s |
| `generated` | 插画、隐喻、实景类 imagery | `image_selector`（FLUX/GPT Image） | 3-6s |
| `talking_head` | AI 数字人出镜（若 HeyGen 可用） | HeyGen 工具 | 5-15s |
| `broll` | 情境、真实案例 | 素材或生成镜头 | 3-6s |
| `screen_recording` | 代码演示、UI 逐步演示 | 录制或模拟 | 5-15s |

**零密钥场景选择：** 当无法进行图像/视频生成时，
规划 `text_card`、`animation` 或 `diagram` 场景，并在各描述中命名合适的
下游模板（`hero_title`、`stat_card`、各类 chart、`comparison`、
`callout` 或 `progress_bar`）。这些完全由 Remotion 组件渲染，无外部依赖。

### 步骤 4：应用视觉技巧库

以下为解说类视频已验证的视觉模式。在场景描述中按名称引用：

**Diagram Reveal（图解渐进揭示）**
逐步构建图解——从空白开始，随旁白描述各部件而添加组件与标签。适合架构、流程与系统。
- 工具：Mermaid + Remotion 动画，或 FLUX 生成图解
- 示例："展示向量数据库架构。旁白说到 'embeddings' 时添加 encoder 节点。说到 'search' 时添加 index。"

**Analogy Visualization（类比可视化）**
将抽象概念与真实世界类比并置。分屏或左右对照。
- 工具：`image_selector` 生成两侧画面
- 示例："左：真实向量空间与散点。右：按主题排序的图书馆。"

**Stat Card Punch（数据卡片冲击）**
全屏数字配合冲击动画（放大、轻微弹跳）。使用 `stat_card` 类型，背景与强调色按本视频身份选取。保持 4–5 秒。
- 工具：Remotion StatCard 组件
- 示例：stat="1ms", subtitle="vs 500ms with traditional search", accentColor="<theme_accent>"

**Data Dashboard Sequence（数据仪表盘序列）**
一系列数据可视化场景，用数字讲故事。从 KPI 概览开始，再深入到具体图表。用 section_title 叠层分组相关数据。该模式无需任何外部工具。
- 工具：Remotion 图表组件（bar_chart、line_chart、pie_chart、kpi_grid）
- 示例：kpi_grid（4 个关键指标）→ bar_chart（细分）→ line_chart（趋势）→ pie_chart（分布）
- 背景处理取自视觉身份：戏剧性/技术主题用深色，亲和/教育向用浅色，话题需要时用纹理或暖色。

**Before/After Split（前后对比分屏）**
用 `comparison` 类型展示问题与方案。对比卡片左右双值并排，带动画入场。
- 工具：Remotion ComparisonCard 组件
- 示例：leftLabel="Before", leftValue="500ms", rightLabel="After", rightValue="1ms"

**Timeline Progression（时间线推进）**
自左向右或自上而下展示演变或流程步骤。旁白描述时逐步出现各步。
- 工具：Remotion 动画元素或 Mermaid 时间线
- 示例："1990: keyword search → 2010: semantic search → 2020: vector databases → 2024: multimodal search"

**Zoom and Focus（缩放聚焦）**
先展示系统全景，再 zoom 到特定组件细讲。建立空间语境。
- 工具：Remotion 对生成图像做 scale 动画
- 示例："展示完整系统架构。zoom 到 'embedding model' 组件。"

**Code Walkthrough（代码 walkthrough）**
语法高亮展示代码。旁白解释时高亮对应行。可打字或渐进揭示动画。
- 工具：`code_snippet` 工具 + Remotion
- 示例："Python 代码：`results = collection.query(embedding, n_results=5)`。旁白说到 'vector' 时高亮 `embedding` 参数。"

### 步骤 4b：按时长预算撰写旁白

若视频含旁白，脚本**必须**适配视频时长。

**时长预算公式：**
1. 根据场景时间（最后一个 cut 的 `out_seconds`）计算总时长。
2. 旁白目标为视频时长的 **85–90%**，为片头/片尾留呼吸空间。
3. 字数预算：纪录片风格含自然停顿 **2.0–2.5 词/秒**；快节奏 **2.5–3.0 词/秒**。
4. 示例：53s 视频 → 旁白目标 45–48s → 最多 90–120 词（纪录片）或 112–144 词（快节奏）。

**分场景字数预算：**
- 按各场景时长比例分配字数。
- 5s 场景约 10–12 词。6s 场景约 12–15 词。
- 场景转场间留 0.5–1s 静音，给画面呼吸。

**校验（TTS 生成前必做）：**
- [ ] 总词数在目标时长预算内
- [ ] 无单场景旁白超出其时间槽
- [ ] 开场与收束场景旁白简短（让画面呼吸）

**TTS 生成之后：**
- TTS 工具返回 `audio_duration_seconds`——与视频时长对比。
- 若旁白超出视频 >1s，要么 trim 脚本并重新生成，要么延长视频收束场景。
- 渲染前务必运行 `composition_validator` 自动发现不匹配。

### 步骤 4c：场景规划五维清单

> 每个场景必须明确全部五个维度。对 diagram、chart 与 Remotion 原生场景，「Subject」可映射为前景数据元素，「Camera」可标 N/A——但须**显式**标注（例如 `"camera": "N/A — Remotion native scene, no virtual camera"`）。静默省略是最常见失败模式，会导致模型输出不可预测、提示词脆弱、评审反复。
>
> 1. **Subject（主体）** — 类型 + 关键视觉属性；若多个，如何区分。对 diagram/chart 场景，指被强调的数据元素（节点、柱、被高亮的 KPI）。对生成图像，指被插画的人/物/概念。
> 2. **Subject Motion（主体动效）** — 按时间顺序的动作；对动画图解，节点/边/数值出现或变化的顺序。
> 3. **Scene（场景）** — 叠层（单独列出！）+ POV + 设定 + 时段 + 场景动态。对 Remotion 场景，「设定」映射为背景处理 + 主题。
> 4. **Spatial Framing（空间构图）** — 景别 + 画内位置 + 景深（FG/MG/BG）+ 相对机位高度；以及这些如何**变化**。对静态 Remotion 场景，记录布局网格 + 视觉中心元素。
> 5. **Camera（镜头）** — 播放速度 → 镜头畸变 → 高度 → 角度 → 焦点/景深 → 稳定性 → 运动。原生 Remotion 场景标 N/A；对 `generated`/`broll`/`image_animation` 场景完整指定。
>
> 原始词汇见 `skills/creative/video-gen-prompting.md`。

> **叠层说明。** 叠层（标题、字幕、HUD、水印、框图、lower-thirds、section_title 条、stat_reveal 芯片、hero_title 叠层、provider 芯片）不属于场景前景/中景/背景景深轴。在场景元数据中单独列出（`overlays: [...]`），含内容与位置。勿将叠层描述为「在前景」——那会混淆下游工具与任何重新分析输出的视频理解模型。

### 步骤 5：对照 Playbook 校验

风格 playbook 约束你的视觉选择：

| Playbook 字段 | 对场景的影响 |
|----------------|-------------|
| `visual_language.color_palette` | 所有生成图像与图解须使用这些颜色 |
| `visual_language.composition` | 构图规则（三分法、居中等等） |
| `motion.transitions` | 允许的转场类型（如 `gentle-fade`、`soft-dissolve`） |
| `motion.animation_style` | 动画气质（如 `ease-in-out, organic curves`） |
| `motion.pacing_rules` | 最短停留时间（如「建立镜头至少 hold 2s」） |
| `asset_generation.image_prompt_prefix` | 提炼为短视觉锚点；勿原样粘贴进所有提示词 |
| `asset_generation.consistency_anchors` | 所有图像须保持一致的内容（色板、光照、风格） |

**提交前清单：**
- [ ] 每个场景使用 playbook 兼容的转场
- [ ] 所有 required_asset 描述含 playbook 风格提示
- [ ] 无场景违反 pacing 规则（最短/最长时长）
- [ ] 图像描述引用本视频真实视觉身份，而非仅预设名称

### 步骤 6：核对覆盖与多样性

**覆盖检查：**
- [ ] 场景覆盖完整脚本时长（首场景从 0s 开始，末场景在 total_duration 结束）
- [ ] 每个脚本章节至少对应一个场景
- [ ] 场景间无 >1s 空隙（除非有意节拍）
- [ ] 脚本中所有 enhancement cues 均有场景或 required_asset 承接

**多样性检查：**
- [ ] 同类型场景连续不超过 3 个
- [ ] 全片至少使用 3 种不同场景类型
- [ ] 视觉节奏在高信息场景（diagram、animation）与呼吸空间（text_card、generated 图像）间交替

**可行性检查：**
- [ ] 每个 `source: "generate"` 的 required_asset 可用现有工具实现
- [ ] 图解描述足够具体以生成 Mermaid 语法
- [ ] 图像描述足够具体以进行 FLUX/GPT Image 提示词工程
- [ ] 无场景依赖工具注册表中不存在的工具

### 步骤 7：自评

打分（1–5）：

| 标准 | 问题 |
|-----------|----------|
| **视觉叙事** | 每个场景是否在推进理解，而非仅装饰？ |
| **脚本对齐** | 每个场景是否与该时刻旁白一致？ |
| **技巧多样性** | 是否使用多种视觉技巧，而非单一手法？ |
| **Playbook 一致性** | 每个场景是否像同一支视频？ |
| **资产可行性** | 每个 required_asset 是否可用现有工具生成？ |
| **节奏** | 视觉节奏是否自然？高信息场景与呼吸空间是否平衡？ |

任一维度低于 3 分则修订。

### 步骤 8：提交

将 `scene_plan_json` 按规范 scene-plan schema 校验，经 checkpoint 协议持久化，
并附上阶段评审。无单独的 explainer 提交函数。

## 常见陷阱

- **一节一景**：脚本章节常含多个概念。10 秒一节可能需要 2–3 个视觉场景，避免单调静止。
- **忽略 enhancement cues**：脚本作者在 `enhancement_cues` 中嵌入了视觉提示。勿忽略——代表作者的视觉意图。
- **动画目标过高**：「数据中心 photorealistic 3D 飞越」当前工具无法生成。保持可实现。
- **无转场策略**：随机转场显得混乱。一致使用 playbook 转场规则。特殊转场留给话题切换。
- **required_assets 含糊**：「关于数据库的图」对提示词工程无用。「使用 playbook 蓝绿色板的向量数据库等距插画，embedding 向量浮于 3D 空间」才可执行。
- **预设思维**：场景规划只说「做成 flat-motion-graphics」不够。规划者须说明**本视频**动态图形有何独特之处。
- **动态概念用静态景**：旁白描述流程或变换时，画面应动。用 animation 或 progressive reveal，而非静态图。
- **CTA/收束屏用 `generated` 且需精确文案**：AI 图像模型会臆造文字——错误商名、拼写、电话。任何需逐字准确的场景（CTA、商户信息、联系方式、法律文案）**必须** `type: "text_card"`，由 Remotion 精确渲染文字。切勿为文字准确性关键的场景规划 `generated` 图像。

---

## 关卡提醒（具约束力）

本阶段需人工批准（`human_approval_default: true`）。评审通过后：
以 `status="awaiting_human"` checkpoint，呈现摘要（Backlot 看板渲染制品），并**结束本轮**。勿在同一回复中启动下一阶段。
批准按关卡单独生效——此前的「继续」不覆盖本关卡。
