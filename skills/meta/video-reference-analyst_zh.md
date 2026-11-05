# 视频参考分析师 — 元技能

## 何时使用

当用户提供视频 URL（YouTube、Shorts、Instagram、TikTok 或任意 URL）
或本地视频文件作为**参考**——即「帮我做类似这种的」，而非
「剪辑这段素材」时。

若用户说「剪辑这个视频」或「切成片段」，应路由到相应的
素材驱动流水线（clip-factory、talking-head、hybrid）。本技能用于
**参考驱动**的制作。

## 检测信号

在以下情况触发本技能：
- 用户粘贴 YouTube/Shorts/Instagram/TikTok URL
- 用户说「类似这种」「受启发」「这种风格」「和……相似」
- 用户上传视频并说「我想要一个像这样的」
- 用户说「我看了这个视频，想做一个类似的」

以下情况**不要**触发：
- 用户提供素材并说「剪辑这个」或「切片段」→ 使用 source_media_review
- 用户提供音频并说「为这个做视频」→ 标准流水线
- 用户只要转录文本 → 直接使用 TranscriptFetcher

## 流程

### 步骤 1：分析参考视频

使用 `analysis_depth: "standard"` 运行 VideoAnalyzer：

```python
video_analyzer.execute({
    "source": "<url or path>",
    "analysis_depth": "standard",
    "max_keyframes": 20
})
```

阅读生成的 VideoAnalysisBrief。继续之前，向用户呈现摘要。
这不是原始数据倾倒，而是对话式解读，且**必须**按 5 个维度结构化，
以便下游阶段可直接提取字段：

```
「我已经看过这个视频。我的观察如下：

**内容：** [2 句话概括视频讲什么]
**风格：** [1 句话 — 节奏、视觉处理、能量]
**结构：** [X 个场景、共 Y 秒，节奏风格]
**运动：** [M 个场景中有 N 个是动态片段 / 动画静帧 / 静态图。
本视频使用 [AI 生成视频片段 / 静帧加平移缩放 / 混合方式]。]

**五维度拆解（按镜头或镜头组）：**
- 主体： [类型、数量、属性；跨镜头主体变化：揭示 / 消失 / 切换 / 复杂交替；或 N/A]
- 主体运动： [按时间顺序的动作；交互；或 N/A]
- 场景： [叠加层（文字/图形）单独列出；POV（无人机/过肩/微距等）；环境；时段；动态]
- 空间构图： [景别；主体位置；景深；相对高度；如何变化]
- 镜头： [播放速度；镜头；高度；角度；对焦/景深；稳定性；运动]

**成功要素：** [2–3 个具体点 — 钩子手法、节奏、
视觉转场、旁白风格]

现在我来根据你当前的配置看看能做什么……」
```

上述五维度块是 `proposal-director`、`script-director` 和 `scene-director` 会读取的**规范形式**。不要把它再压成散文 —— 保留标签。

**运动分类至关重要。** VideoAnalysisBrief 现包含逐场景的
`motion_type`（"motion_clip"、"animated_still"、"static_image"）和 `flow_variance`。
据此确定制作路径：

- 若多数场景为 `motion_clip` → 参考使用**视频生成**（Kling、
  MiniMax 等）→ 围绕视频生成工具规划，而非仅图像生成
- 若多数场景为 `animated_still` → 参考使用**静帧 + Ken Burns / 平移缩放** → 图像生成 + Remotion/FFmpeg 合成合适
- 若混合 → 注明哪些段落用动态、哪些用静帧

**切勿猜测**参考用的是图还是视频。阅读 `motion_type` 字段。
搞错会导致提案错误流水线和错误工具路径。

**视觉分析：** 呈现结构数据后，自行检查提取的关键帧。你是多模态模型 —— 查看关键帧图像并丰富 VideoAnalysisBrief：
- 逐帧描述（主体、文字、构图、色彩）
- 跨帧视觉连续性与风格一致性
- 类型分类与制作质量评估
- 色彩 palette 提取（关键帧主色）
- 若有屏幕文字则分析字体风格
- 连续关键帧间可见的转场模式

用视觉观察更新 brief 的 `content_analysis`、`style_profile` 和 `replication_guidance`
字段。工具提供结构；你的视觉提供理解 —— 分析在此才完整。

### 五维度结构化输出（强制）

分析师报告**必须**将参考视频拆解为 CMU/Harvard CHAI 研究中的**五个维度**（也是 `skills/creative/video-gen-prompting.md` 中的规范结构）。仅叙事式摘要已不足 —— 下游阶段（proposal、script、scene-director）直接消费五维度形式，不再从散文重解析。

**决策树式标注策略。** 对每个检测到的镜头，按顺序走五个维度：

> - **主体：** 类型、属性（数量、年龄、角色、服装、 distinguishing features）、多主体消歧、跨镜头过渡（revealing / disappearing / switching / complex-alternating）。
> - **主体运动：** 按时间顺序的动作；群体/交互模式（并行、顺序、反应）； locomotion vs 手势 vs 面部。
> - **场景：** **叠加层单独列出**（文字、下三分之一、图形、水印 —— 作为独立层，不要并入环境）+ POV（无人机、航拍、过肩、微距、俯拍、行车记录仪、FPV、手持、锁定）+ 环境 + 时段 + 动态（天气、粒子、人群运动）。
> - **空间构图：** 景别（ECU/CU/MS/WS/EWS）、主体在画框中的位置、景深（前景/中景/背景运用）、相对高度（高于/平齐/低于主体）—— 以及镜头或主体运动时各要素**如何变化**。
> - **镜头：** 播放速度（实时 / 慢动作 / 延时）、镜头畸变（变形宽银幕、鱼眼、移轴）、高度（地面 / 眼平 / 俯视）、角度（俯 / 仰 / 荷兰角）、对焦 / 景深（ rack focus、深焦、浅景深）、稳定性（锁定 / 手持 / 稳定器）、运动（推 / 拉 / 摇 / 俯仰 / 滑轨 / 横移 / 升降 / 环绕）。
>
> **不适用的维度明确标 N/A**（例如「主体：N/A — 纯风景镜头」，或「场景叠加层：N/A — 无图形」）。**静默省略是最常见的分析师失误**，会导致下游 prompt 含糊。

各维度的 primitive 定义与规范词汇见 `skills/creative/video-gen-prompting.md`。

### 步骤 2：能力审计

运行标准 preflight：

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
```

将参考视频需求与可用能力对照：

```
参考需求                 你的能力                   缺口
─────────────────────    ─────────────────────      ──────────
视频片段（科幻）         视频生成：0/12 已配置      无密钥则 BLOCKED
旁白（低沉男声）         TTS：ElevenLabs 可用       READY
背景音乐                 音乐：MusicGen 可用        READY
合成引擎                 Remotion：可用             READY
                         HyperFrames：可用          READY
                         FFmpeg：可用               READY（独立操作）
```

**合成引擎选择：** Remotion 与 HyperFrames 是并行、无优劣排序的
合成运行时 —— **不要**在此预先锁定其一。两者皆可用时，
`AGENT_GUIDE.md` 中「同时呈现两种合成运行时（硬规则）」在提案阶段生效：
向用户呈现两种选项及权衡，等待明确批准后再锁定 `render_runtime`。
静默默认禁止。FFmpeg 在本流程中不是合成运行时 —— 仅用于
合成流水线外的独立操作（裁剪、转码、烧录字幕）。

如实说明缺口。若需要视频生成但不可用，明确说明：

```
「这个参考使用生成的科幻画面。你目前没有配置任何视频
生成提供商。可选方案：

• 按 `provider_menu()` 建议添加 gateway 或提供商密钥以启用视频生成
• 若有多个提供商，总结权衡并根据用户 brief 推荐其一
• 不做视频生成继续 → 我会用素材库 footage + Remotion 动画代替
  （观感不同，但仍可行）

你更倾向哪种？」
```

从 registry 读取各不可用工具的 install_instructions —— **不要**
硬编码密钥名、提供商名或设置 URL。

### 步骤 3：提出关键问题

提案前先收集 VideoAnalysisBrief 未覆盖的信息：

1. 「你的版本要旁白，还是纯画面加音乐？」
2. **若需要旁白：此时锁定音频架构。** 询问：
   「故事如何讲述？选项：
   • **单一旁白** — 一个声音讲完整故事（类似皮克斯短片）
   • **角色对白** — 角色互相对话，无旁白
   • **旁白 + 角色声** — 旁白推动叙事，角色偶有对白」
   此决定塑造脚本、选角与预算。**必须**在提案前敲定 —— 不要推迟到脚本或合成阶段。
3. 「你的视频要多长？参考为 [X] 秒。」
4. 「有指定主题/主体，还是沿参考同一主题发挥？」
5. 「参考里有没有特别喜欢或特别想避开的元素？」

不要一次问完。从最重要的缺口问起。若用户首条消息已回答部分问题，跳过那些。

### 步骤 3b：轻量调研

**本步骤强制。** 即使有清晰参考与用户方向，
代理也必须在提案前做针对性调研。**不要**跳过而仅依赖参考分析 + 自身知识。

调研范围（聚焦 —— 不是完整 research-director 阶段）：

1. **内容 landscape：** 搜索 3–5 个与用户目标相近的现有视频。
   什么有效？什么已泛滥？哪些角度新鲜？让提案 grounded 于真实生态，而非想象。

2. **风格/技法调研：** 搜索与制作路径相关的最佳实践：
   - 若 AI 视频生成：哪些模型更适合该主体？已知 prompt 模式？角色一致性技法？
   - 若动画：哪些动画风格适合该内容？
   - 若参考有 distinctive 技法：如何实现？

3. **主题调研：** 若用户话题含事实内容（科学、
   历史、原理说明），收集 3–5 个可让视频更有趣的数据点或事实。娱乐/喜剧同样可调研同类内容为何 engaging（套路、钩子、 payoff 模式）。

**如何呈现：** 不要倾倒 raw 调研。融入提案：
- 「我看了类似频道 —— 多数食物拟人视频用 X，我们 twist 成 Y 会更突出」
- 「Kling 在用 [具体技法] 时 anthropomorphic 角色表现好」
- 「表现最好的 60 秒喜剧 Shorts 都用三拍结构：setup、
  escalation、意外 payoff」

**时间预算：** 2–3 分钟网页搜索。轻量 pass，非深度调查。完整 research-director 阶段在流水线内按需再跑。

### 步骤 4：创意提案（2–3 个变体）

**强制：** 代理**不得**提案一比一复刻。参考是灵感，
不是模板。每个提案须有清晰创意差异。

每个变体使用如下结构：

```
## 选项 [A/B/C]：「[标题]」

**借鉴自参考：** [保留什么 — 节奏、结构、调性]
**创意 twist：** [改变什么 — 角度、主体、视觉处理、钩子]

**视觉计划：**
- Playbook：[最接近匹配 + 定制]
- 视觉处理：[如何制作画面 — 哪些工具、哪些提供商]
- 合成：[Remotion（可用时默认）/ FFmpeg（仅后备）]
- 运动：[视频生成片段 / Remotion 静帧 spring 动画 / 等]
- 片段时长策略：[尽量拉长单片段以减少 API 调用与成本。
  多数提供商支持 5s 与 10s。优先 10s，叙事连贯时合并相邻场景为单片段。60 秒视频
  需要 6×10s 而非 12×5s —— 成本减半、切点更少、运动更顺。]

**音频计划：**
- 音频架构：[单一旁白 / 角色对白 / 旁白 + 角色]
- 选角：[各角色 voice 名称 + ID — 旁白、角色 A 等]
- TTS 提供商：[经 tts_selector preflight 从可用项选择 —
  Google Chirp3-HD（性价比最佳：近乎免费、表现力强、24kHz），
  ElevenLabs（仅 voice cloning），OpenAI gpt-4o-mini-tts（instructions 参数表现好），
  Piper（离线/免费）。**不要**硬编码提供商 —
  跑 preflight 看已配置项并推荐最佳可用。
  **默认推荐 Google Chirp3-HD**，除非需要 voice cloning。]
- 音乐：[曲库 / 生成 / 无]
- 声音设计：[特殊音频需求]

**时长：** [X 秒]
**各提供商选项预估成本：**
呈现提供商对比表供用户选择：
```
Provider        Quality    Speed      Cost (N clips)    Total
─────────      ────────   ─────      ──────────────    ─────
VEO 3.1        Highest    Slow       $X.XX             $X.XX
Kling Pro      High       Medium     $X.XX             $X.XX
Sora V2        High       Medium     $X.XX             $X.XX
LTX Distilled  Lower      Fastest    $X.XX             $X.XX
```
+ 图像生成：$X.XX（N 张 × 每张 $X.XX，经 [provider]）
+ TTS 旁白：$X.XX（N 词，经 [provider]）
+ 音乐：$X.XX（[source]）

**不要替用户选提供商。** 呈现选项与
成本，简要推荐其一并说明理由，由用户决定。

**诚实评估：** [ realistically 会是什么样 — 不要 oversell]

**Layer 3 技能：** [列出将用各工具的 agent_skills。
  写任何生成 prompt 前**必须**阅读。例如：
  - 视频生成：`ai-video-gen` 提供商 prompt 模式
  - 图像生成：`flux-best-practices` FLUX prompt 工程
  - TTS：`elevenlabs` 或 `openai-docs` 声音调校
  跳过 Layer 3 技能属治理违规。]
```

**差异化模式：**

| 模式 | 示例 |
|---------|---------|
| **同结构、不同主体** | 参考：「黑洞如何工作」→  ours：「中子星如何工作」，同节奏 |
| **同主体、不同角度** | 参考：「Kubernetes 讲解」→ ours：「安全工程师视角的 Kubernetes」 |
| **同调性、不同视觉** | 参考：素材 + 旁白 → ours：动态信息图 + 旁白 |
| **同内容、不同平台** | 参考：10 分钟 YouTube → ours：60 秒 Shorts，更快节奏 |
| **反向观点** | 参考：「AI 将取代工作」→ ours：「AI 不会取代**你的**工作」 |

**成本透明强制。** 每个概念须包含：
- 用户请求时长下的分项成本估算
- 分项：图像生成、视频生成、TTS、音乐、合计
- 每行成本的提供商名
- 诚实说明预算能买到什么、买不到什么

**推荐：** 始终推荐一个选项并简述理由。不要让用户在同等选项间 paralysis。

### 步骤 4b：Layer 3 技能门（强制）

**在任何资产生成之前**（样片或完整制作），代理**必须**：

1. 从 `skills/` 目录阅读各工具的 **Layer 2 技能**（用法、输入 schema、最佳实践）
2. 检查将用每个工具的 `agent_skills` 字段
3. 阅读 `.agents/skills/` 中引用的 **Layer 3 技能**（提供商 prompt）
4. 将所有生成 prompt 应用提供商专用指导

**切勿通过阅读工具源码 (*.py) 来学用法。**
技能的存在正是为了避免读实现代码。
Layer 2 描述*做什么*和*何时*。Layer 3 描述*如何*。

**非可选。** AGENT_GUIDE 规定：*「Layer 3 非可选。
每个生成工具都有 agent_skills 字段。写 prompt 前必须阅读。」*

生成前示例清单：
```
Tool              agent_skills              Read?
────────────      ────────────────────      ─────
video_selector    ai-video-gen              [ ]
flux_image        flux-best-practices       [ ]
elevenlabs_tts    elevenlabs, text-to-speech [ ]
video_compose     remotion-best-practices   [ ]
```

在读完所有相关 Layer 3 技能前**不要**进入步骤 5。
通用 prompt 与 skill-informed prompt 的差别是
「能用」与「电影感」的差别。

### 步骤 5：样片优先制作（强制）

用户选定变体后，**始终**说：

```
「好选择。在投入完整 [X] 秒视频前，我会先做
10–15 秒样片 —— 开场钩子 + 一个中间场景。这样你可以在全面投入前
听声音、看视觉风格、感受节奏。

样片预估成本：$[X.XX]
是否继续样片？」
```

样片**非可选**。即使用户说「直接做完整版」，温和坚持：

```
「我强烈建议先做样片 —— 成本只占一小部分，
能尽早发现风格不匹配。若满意，我会立刻继续完整视频。」
```

仅在用户被建议后仍坚持时可跳过样片。

**样片内容：**
- 1–2 个代表性场景（钩子 + 一个中间场景）
- 实际 TTS 旁白与选定声音
- 实际生成/素材画面
- 音乐 bed 片段
- 字幕风格预览

**样片检查点：**
呈现样片并说明：「这是预览。感觉对吗？可调整：声音、视觉风格、节奏、音乐、色彩。」

根据样片反馈迭代至批准。样片存放于：
`projects/<name>/assets/sample/sample_v{N}.mp4`

### 步骤 6：进入流水线（硬重定向）

样片批准后，代理**必须**进入流水线。非可选。

**强制步骤：**
1. 阅读流水线 manifest：`pipeline_defs/animation.yaml`（或匹配制作类型的流水线）
2. **逐阶段**按序执行 —— research → proposal → script →
   scene_plan → assets → edit → compose → publish
3. **每个阶段前**阅读 `skills/pipelines/<pipeline>/<stage>-director.md`
4. 各阶段产出所需 artifact
5. 在 `checkpoint_required: true` 处通过每个检查点
6. 在 `human_approval_default: true` 处获得用户批准

**不要合并阶段。** 不要从「用户批准提案」直接跳到
「生成全部资产」。流水线阶段用于质量门、
artifact 依赖与审查检查点。跳过属治理违规。

**带入流水线的上下文：**
- VideoAnalysisBrief 作为 research/proposal 阶段的 grounding
- 用户选定变体作为批准方向
- 样片反馈并入 brief
- 所有创意差异决策记入 decision_log
- 步骤 3 的音频架构与选角决策
- 步骤 4b 已读的 Layer 3 技能

此后由流水线接管。VideoAnalysisBrief 与标准 artifact 同行，
在各阶段提供参考 grounding。

## 多个参考视频

用户提供多个参考 URL 时：

1. 分别分析每个视频（对每个运行 VideoAnalyzer）
2. 呈现对比摘要：「视频 A 在 X 做得好，视频 B 在 Y 做得好」
3. 提案中注明各元素受哪条参考启发
4. 主参考的 VideoAnalysisBrief 随流水线传递；
   次参考记在 research_brief

## 错误处理

| 失败 | 动作 |
|---------|--------|
| URL 下载失败 | 报告错误，建议：换 URL、提供本地文件，或无参考继续 |
| 无字幕 | 下载视频，本地 Whisper 转录 |
| 场景检测失败 | 回退为均匀帧采样 |
| 分析全部失败 | 请用户口头描述参考视频，走标准创意 intake |

切勿静默跳过分析步骤。若某步失败，告知用户发生了什么
以及对分析质量的影响。
