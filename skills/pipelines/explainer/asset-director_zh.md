# 资产导演 — Explainer 流水线

## 何时使用

你是生成式解说视频的**资产制作人**。你已有带所需资产的 `scene_plan` 以及带旁白文本的 `script`。你的任务是生成全部所需资产：旁白音频、图像、图表、代码片段和背景音乐。在结束本阶段前，每个文件都必须已存在于磁盘上。

计划在此变为真实文件。缺失或低质量资产会直接毁掉成片。

## 动画创作 — 选用哪种运行时

在本流水线中创作任何 Remotion 动画组件之前，请先阅读 **`skills/meta/animation-runtime-selector.md`**。它是 Remotion 原语与 GSAP 插件之间选型的路由依据。

常见解说场景的快速路由：

| 场景类型 | 推荐做法 |
|---|---|
| 标题卡、淡入淡出、滑动、缩放 | Remotion 原语 — `interpolate()` + `spring()` |
| 与旁白同步的字级字幕高亮 | 现有 `CaptionOverlay` 组件（已在 `remotion-composer/src/components/` 中） |
| 逐字动效排版（「逐字迸出」） | GSAP SplitText — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 4 条以上 tween 的多步编排 | GSAP timeline — 阅读 `.agents/skills/gsap-timeline/SKILL.md` |
| Logo 构建（描线、描边揭示） | GSAP DrawSVG — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 数据图表（柱/线/饼/KPI） | Remotion 内置图表组件 — 见 `remotion-composer/SCENE_TYPES.md` |
| 终端或 CLI 演示 | Remotion TerminalScene — 阅读 `.agents/skills/synthetic-screen-recording/SKILL.md` |

**保持简单优先：** 若 Remotion 原语能在 ≤ 20 行内解决某场景，就用它们。仅在插件确实值得其打包体积时才引入 GSAP。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["scene_plan"]["scene_plan"]`、`state.artifacts["script"]["script"]`、`state.artifacts["proposal"]["proposal_packet"]` | 要生产什么 |
| Playbook | 当前启用的 style playbook | 图像 prompt、图表风格、音频偏好 |
| Tools | `tts_selector`、`image_selector`、`video_selector`、`diagram_gen`、`code_snippet`、`music_gen` — selector 会从 registry 自动发现全部可用 provider | 生成能力 |
| Cost tracker | `tools/cost_tracker.py` | 预算治理 |

## 流程

### 步骤 1：清点所需资产

遍历 scene plan 中的每个场景。对每条 `required_assets` 条目创建一条资产任务：

```
Asset Task:
  scene_id: scene-3
  type: diagram
  description: "Mermaid flowchart: query -> encode -> search -> rank -> return"
  source: generate
  tool: diagram_gen
  estimated_cost: $0.00
```

另为以下项创建任务：
- **旁白音频** — 每个 script section 一条（使用 `tts_selector` 或具体 TTS provider）
- **背景音乐** — 整片一条（使用 `music_gen` 或从库中选取）
- **音效** — 按 playbook 的 `sfx_style`（可选，使用 `music_gen` 或素材库）

### 步骤 2：检查预算

在生成任何东西之前：
1. 汇总所有资产任务的预估成本
2. 与 cost tracker 的剩余预算对比
3. 若超预算：
  - 将昂贵工具换为更便宜替代（用 `tts_selector` 的 `preferred_provider` 路由到更便宜 TTS；用 `image_selector` 路由到更便宜图像 provider）
   - 减少图像数量（合并相似场景）
   - 跳过可选资产（SFX、B-roll）
4. 继续前通过 cost tracker 获得成本批准

### 步骤 2b：样片预览（避免浪费支出）

在批量生成资产前，为每种昂贵资产类型各做一份样片并提交用户批准：

1. **TTS 样片**：若存在则对 `script.voice_performance.sample_section_id` 生成旁白；否则选 delivery 要求最高的 section。播放给用户听。在生成其余部分前确认音色、语速、停顿、重音与 tone 可接受。
2. **图像样片**：为最具代表性的场景生成一张图。展示给用户。在批量生成全部图像前确认风格、质量与 prompt 思路。
3. **音乐样片**（若使用 `music_gen`）：生成一段短 clip。在正式投入前确认情绪与能量。

若用户拒绝某样片：
- 调整参数（音色、prompt 风格、provider）并重新生成样片。
- 样片未批准前不要批量生成。
- 每种资产类型最多 3 轮样片迭代，之后升级请用户决策。

本步通常总成本约 $0.03–0.08，可避免 $1–3 的无效生成。

### 步骤 3：生成旁白

对每个 script section：
1. 提取旁白文本
2. 阅读 `script.voice_performance` 与各 section 的 `delivery_cues`
3. 若存在则使用 `delivery_cues.provider_text`；否则仅在所选 provider 支持时，用有目的的标点与 break 标签变换 section 文本
4. 应用 script 中的 speaker 指示（pace、emphasis、emotion）
5. 应用 playbook 的 `audio.voice_style`
6. 将 cues 映射到 provider 参数：
   - OpenAI：仅在与 `model: "gpt-4o-mini-tts"` 搭配时使用 `instructions`；用 `response_format` 指定输出格式
   - Google TTS：使用 `<break>` 标签时 `input_type: "ssml"`，另加 `speaking_rate` 范围 `0.25..2.0`、`pitch` 范围 `-20..20`
   - ElevenLabs：`stability`、`similarity_boost`、`style`、`speed`、`use_speaker_boost`
   - Azure：voice 别名（`andrew`、`brandon`、`ava`、`guy`、`jenny`）或任意 Azure 短名，SSML `rate`（如 `"-4%"`）、`pitch`（如 `"+1st"`）、`style`（如 `"narration-professional"`）— 见 `azure-text-to-speech` skill
7. 使用 `tts_selector` 生成 — 它会按用户偏好与可用性自动路由到最佳 TTS provider。查看 registry 的 `best_for` 字段以了解各 provider 优势。
8. 在每条旁白资产上记录已应用的 `voice_performance` 元数据
9. 确认音频文件存在且时长与预期 timing 相符（±15%）

**发音指南**：若 script 含技术术语、行话或读音不直观的名字，在 TTS 请求中包含发音映射。

**平淡旁白失败：** 若已批准音色听起来单调、机械、赶拍或忽略预期停顿，不要批量生成其余 section。修订 `voice_performance` 计划或 provider 参数并重新生成样片。

### 步骤 4：生成视觉资产

按工具分组处理资产任务以提高效率：

**图像（`image_selector`）**：
1. 根据场景实际用途构建 prompt：
   - 来自 `shot_language`、`shot_intent`、`texture_keywords` 的场景专属镜头/光照/质感 cues
   - 来自 playbook 或自定义 identity 的适配视觉锚点
   - 具体主体/动作/环境
   需要时可使用 `lib/shot_prompt_builder.py`。
2. 从 playbook 添加 negative prompt
3. 包含一致性锚点（同一角色/世界/色板族），但**不要**对每张图复用完全相同的措辞
4. 生成并确认文件存在
5. 若结果不符合预期， refine prompt 并重新生成（最多 2 次重试）

**图表（`diagram_gen`）**：
1. 将场景描述转为合法 Mermaid 语法
2. 应用 playbook 的 `asset_generation.diagram_style`
3. 生成 SVG/PNG
4. 确认所有节点与边都存在

**代码片段（`code_snippet`）**：
1. 从场景描述提取语言与代码
2. 应用 playbook overlay 风格的语法高亮主题
3. 生成高亮图像或 Remotion 兼容数据

### 步骤 5：生成音乐

1. 阅读 playbook 的 `audio.music_mood` 与 `audio.music_volume`
2. 查看 `proposal_packet.production_plan.music_source` 中的音乐决策（由 Proposal Director 设定）
3. 按以下优先级获取背景轨：
   - **用户所选库曲目**：若 proposal 指定了 `music_library/` 中的曲目，复制到 `projects/<project>/assets/music/background_music.mp3`
   - **用户音乐库（`music_library/`）**：若文件夹存在且有曲目，按 playbook 的 `audio.music_mood` 选最佳匹配。按文件名列出候选并由 EP 决策。
   - **音乐生成 API**：若可用则使用 `music_gen`（ElevenLabs）或 `suno_music`。先通过 registry 查状态 — 若工具不可用或配额耗尽，**立即跳过**（不要尝试后静默失败）。
   - **无可用音乐**：在 asset manifest 中明确记录 `"music_status": "unavailable"` 及原因。**不要**静默产出无音乐视频 — EP 与用户应知情。
4. 时长至少等于视频总时长。若更短，compose 阶段可循环。
5. 确认音频文件存在于 `projects/<project>/assets/music/background_music.mp3`

**关键：** 若音乐生成失败或不可用，**立即**在 asset manifest 中报告 — 不要把问题推到 compose 阶段。

### 步骤 6：构建 Asset Manifest

将所有已生成资产组装进 manifest：

```json
{
  "version": "1.0",
  "assets": [
    {
      "id": "narration-s1",
      "type": "audio",
      "subtype": "narration",
      "path": "assets/narration/s1.mp3",
      "source_tool": "tts_selector",
      "scene_id": "scene-1",
      "duration_seconds": 8.2,
      "cost_usd": 0.003
    },
    {
      "id": "img-scene-3",
      "type": "image",
      "path": "assets/images/scene-3-diagram.png",
      "source_tool": "diagram_gen",
      "scene_id": "scene-3",
      "cost_usd": 0.00
    },
    {
      "id": "music-bg",
      "type": "audio",
      "subtype": "music",
      "path": "assets/music/background.mp3",
      "source_tool": "music_gen",
      "duration_seconds": 62,
      "cost_usd": 0.05
    }
  ],
  "total_cost_usd": 0.053,
  "generation_summary": {
    "narration_sections": 5,
    "images_generated": 8,
    "diagrams_generated": 2,
    "music_tracks": 1
  }
}
```

### 生成 Prompt 的前后自检

> 在向任何生成工具发送 prompt 之前 — `image_selector`、`diagram_gen`、`video_selector`，乃至 `code_snippet` 样式 prompt — 执行 modeled on CHAI oversight loop（「Building a Precise Video Language with Human-AI Oversight」，arXiv 2604.21718v2）的三步自检。成本很小（无额外 tool 调用）；收益很大（避免无效生成）。这对 `diagram_gen` 的 Mermaid prompt 与 `image_selector` 的插画 prompt 同样重要 — 糟糕的解说视觉会以相同方式失败：缺主体、缺构图、含糊的「做得像教育片」。
>
> **步骤 1 — 预 caption。** 按你平时的方式写 prompt。不要过度编辑；目标是完整初稿。
>
> **步骤 2 — 批判 pass。** 用五维清单（Subject / Subject Motion / Scene / Spatial Framing / Camera）给初稿打分。每一维：
> - 是否已指定？若否，省略是有意（如「Camera N/A — Remotion native scene」「无主体运动 — 静态图表」）还是疏漏？
> - 易混术语是否消歧？（dolly vs zoom、pan vs truck、bird's-eye vs aerial、fisheye vs barrel、full shot vs close-up；图表：flowchart vs sequence vs state diagram、top-down vs left-right）
> - 情绪形容词（「clean」「professional」「modern」）是否替换为视觉成因（无衬线 typography、充足留白、单色色板加一 accent）？
> - 多镜头 prompt：身份锚点是否逐字一致？对 `image_selector` 中反复出现的 prompt（多场景同一角色或世界），一致性锚点是否逐字指定？
>
> **步骤 3 — 后 caption。** 重写以补全缺失维度、修正易混术语、替换主观用语。后 caption 才是发给生成工具的版本。
>
> 在资产元数据中记录 (pre, critique, post) 三元组以便追溯。这 mirrors CHAI 工作流，供 reviewer 审计。

### 步骤 7：验证全部资产

**存在性检查：**
- [ ] 每个资产 `path` 在磁盘上存在
- [ ] 每个旁白 section 有对应音频文件
- [ ] 每个带 `required_assets` 的场景已生成全部资产
- [ ] 背景音乐文件存在

**质量检查：**
- [ ] 旁白时长在预期 timing 的 ±15% 内
- [ ] 旁白资产记录 `voice_performance.delivery_cues_applied`
- [ ] 已批准 TTS 样片与批量使用相同 provider、voice 与表现向设置
- [ ] 图像符合 playbook 风格（审查一致性锚点）
- [ ] 图表清晰且完整
- [ ] 总成本在预算内

### 步骤 8：自评

打分（1–5）：

| 维度 | 问题 |
|-----------|----------|
| **Completeness** | 每个场景是否具备全部所需资产？ |
| **Audio quality** | 旁白是否自然、 pacing 是否正确？ |
| **Visual consistency** | 所有图像是否像同一支视频？ |
| **Budget adherence** | 总成本是否在批准预算内？ |
| **Playbook fidelity** | 资产是否符合 playbook 风格指南？ |

任一维度低于 3 分则先修复再继续。

### 步骤 9：提交

对照 schema 校验 asset_manifest，并通过 checkpoint 持久化。

### 制作中的事实核查

若在资产生成中遇到不确定：
- 使用 `web_search` 核实主体视觉准确性（例如某建筑实际长什么样？）
- 使用 `web_search` 在生成插画前找参考图
- 在 decision log 中记录：`category="visual_accuracy_check"`

视觉准确性很重要。若 script 提到具体地点、人物或物体，生成图像前先核实其真实外观。不要依赖 AI 模型的训练数据 — 可能错误或过时。

## 常见陷阱

- **未查预算就生成**：始终先估算总成本。60 秒视频配 15 张图可能很快烧掉 $3+。
- **图像风格不一致**：每次 `image_selector` 调用相互独立。使用一致锚点，但按场景适配。若把相同 style 前缀粘贴进每个 prompt，成片会显得机器化、重复。
- **忽略旁白 timing**：若 TTS 为 10 秒 section 产出 12 秒音频，剪辑阶段会很难。检查时长。
- **忽略 delivery cues**：存在 `provider_text` 或 `delivery_cues` 时仍生成 raw script 文本会把朗读打平。先应用 voice-performance 合约。
- **缺少发音指南**：「PostgreSQL」或「Kubernetes」没有明确指导会被读错。
- **重试一次就放弃**：图像不对时应针对性 refine prompt — 不要原样 prompt 再试。
- **用 AI 生成须逐字准确的文本图像（CTA、商号、联系方式）**：AI 图像模型常 hallucinate 错误文字 — 错商号、错电话、拼写错误。**永远不要**在文本须逐字准确的场景用 AI 图像生成。改用 Remotion `text_card` 类型。适用于：CTA 屏、带商号的标题卡、联系信息 overlay、法律免责声明。若 scene plan 中某场景 `type` 为 `text_card`，**不要**为其生成图像 — 跳过，由 compose 阶段在 Remotion 中原生渲染。


## 当你不确定怎么做

若遇到不确定的生成技巧、provider 行为或 prompting 模式：

1. **搜索 web** 获取当前最佳实践 — 模型与 API 变化频繁，agent 训练数据可能过时
2. **查看 `.agents/skills/`** 是否已有 Layer 3 知识（provider 专属 prompting 指南、API 模式）
3. **若仍不够**，在项目范围写 skill：`projects/<project-name>/skills/<name>.md`，记录所学
4. **在 skill 中引用来源 URL**，使知识可追溯
5. **记入 decision log**：`category: "capability_extension"`，`subject: "learned technique: <name>"`

以下尤其重要：
- **视频生成 prompting** — 模型对特定词汇的响应随版本变化
- **图像模型参数** — FLUX、GPT Image、Imagen 的最优设置不同且演进
- **音频 provider 怪癖** — 声音克隆、音乐生成、TTS 各有模型专属最佳实践
- **Remotion 组件模式** — 框架演进中不断出现新合成技巧

不要依赖过时知识。有疑问时先搜索。

---

## 关卡提醒（具约束力）

本阶段以人工批准为关卡（`human_approval_default: true`）。review 通过后：
以 `status="awaiting_human"` checkpoint，呈现摘要（Backlot 看板渲染产物），并**结束本轮**。不要在同一回复中开始下一阶段。
批准按关卡计 — 较早的「继续」不覆盖本关卡。
