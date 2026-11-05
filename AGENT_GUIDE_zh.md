# OpenMontage - Agent 指南

从这里开始。这是 OpenMontage 的完整操作指南与 Agent 契约。

架构、关键文件与约定见 [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)。

## 首次交互 — 入门引导

当用户的第一条消息含糊、偏探索、或询问你能做什么（「帮我做个视频」「你能做什么？」「帮我创作内容」「我想做内容」）时，在做任何其他事之前先阅读入门技能：

**阅读：** `skills/meta/onboarding.md`

该技能教你如何开展需求发现、分类用户环境、用通俗语言展示能力，并根据其可用工具提供入门提示。目标：让用户在 60 秒内从「好奇」进入「正在做视频」。

**跳过入门** 当用户带着明确、可执行的请求而来（例如「做一个 60 秒的黑洞科普短片」）。直接进入规则零。

## 参考视频入口

当用户提供 **视频 URL 或本地视频文件作为灵感** — 例如：

- 「能做一个像这样的视频吗？」
- 「我喜欢这个 YouTube Short，帮我做类似的。」
- 「用这个 Reel 当参考。」

— **不要** 把它当作普通的网页搜索或写提示词请求。

这是 OpenMontage 中的一等公民工作流。

### 必需行为

1. **阅读：** `skills/meta/video-reference-analyst.md`
2. **运行参考分析工作流**，使用本地分析工具（`video_analyzer`、转录提取、场景检测、帧采样）
3. **产出有依据的摘要**，说明参考视频在做什么：
   - 内容
   - 节奏
   - 结构
   - 风格
   - 成功要素
4. **然后** 运行常规能力审计与流水线选择
5. 为用户版本呈现 **2–3 个差异化概念** — 而非逐帧复刻

### 重要区分

- **参考驱动请求：**「帮我做类似的」→ 使用 `video-reference-analyst.md`
- **源素材请求：**「剪这段素材」/「切成多个片段」→ 使用 `source_media_review` 及相应的素材主导流水线

若模型混淆二者，常会退化为简单搜索 + 猜测。对 OpenMontage 而言这是错误的。

## 规则零 — 所有制作必须走流水线

**每一个视频制作请求 MUST 通过流水线系统。没有例外。**

当用户要求制作、创建、生产或生成任何视频内容 — 预告片、科普、片段、动画或任何其他视频 — Agent 必须：

1. **识别流水线。** 将请求匹配到 `pipeline_defs/` 中的某条流水线。若不清晰，询问用户。
2. **阅读流水线清单。** `pipeline_defs/<pipeline>.yaml` — 了解阶段、工具与质量门。
3. **运行预检（preflight）。** 通过 registry 发现可用工具。展示能力菜单。
4. **逐阶段执行。** 对 **每个** 阶段，在该阶段做任何工作 **之前** 阅读阶段导演技能（`skills/pipelines/<pipeline>/<stage>-director.md`）。
5. **调用工具前先读 Layer 3 技能。** 在使用任何带 `agent_skills` 字段的工具之前，阅读 `.agents/skills/` 中引用的技能。其中包含供应商特定的提示指导、参数优化与质量技巧，能显著提升产出。

**不要：**
- 写临时 Python 脚本直接调工具
- 跳过流水线直接调 API
- 未读阶段导演技能就生成资产
- 不查 Layer 3 技能中的提示指导就使用工具
- 绕过预检、检查点或审查

智能在技能里，不在即兴代码里。阅读导演技能与 Layer 3 知识的 Agent，产出会明显优于用泛化提示直接调工具的 Agent。

## OpenMontage 是什么

OpenMontage 是指令驱动的视频制作系统。AI Agent **就是** 智能体 — 它阅读指令（流水线清单 + 阶段导演技能 + 元技能）并用工具驱动流水线。

```
Agent 阅读流水线清单 (YAML) -> 阅读阶段导演技能 (MD)
-> 使用工具 (Python BaseTool 子类) -> 自审 (元技能)
-> 检查点 (Python 工具) -> 呈现给人工审批
```

**Python = 工具 + 持久化。** 编排逻辑、创意决策、审查逻辑或检查点策略不在 Python 代码里。Agent 在指令引导下做这些决策。

核心循环：

1. 选择一条流水线。
2. 运行预检。
3. 从 registry 发现真实工具。
4. 向用户呈现概念、工具计划、制作计划与成本。
5. 逐阶段执行并设检查点。

## 决策沟通契约

对任何有意义的制作决策，Agent 必须在行动前沟通决策。用户不应事后才从蛛丝马迹推断选了哪个 provider、model 或渲染路径。

### 执行前宣告

在任何付费或后果重大的生成调用之前，说明：

- 确切的工具名，
- provider，
- model 或 provider 变体，
- 选择理由，
- 是样片还是批量运行。

### 重大变更前先问

Agent 必须在变更任何重大制作选择之前询问用户，包括：

- 切换 provider，
- 切换 model 系列或 provider 变体，
- 从视频主导改为静帧主导处理，
- 切换 composition engine 且会改变产出特征时，
- 去掉旁白、音乐或其他已批准的创意元素，
- 从样片模式改为批量模式。

在已批准的 provider/model 路径内的 minor 提示微调无需单独批准，除非会 materially 改变创意方向。

### 变更决策须重新记录（绑定）

`decision_log` 是看板的 Decisions 栏与运行的审计轨迹。它是 **仅追加的历史，不是草稿本。** 当你已记录的选择在运行中变更 — 用户换音色、你切换 provider/model/runtime/音乐，或 fallback 覆盖先前选择 — 你 **必须追加新的 `decision_log` 条目** 记录新选择，复用 **相同的 `category` 与相同的 `subject`**（例如 `category: "voice_selection"`，`subject: "Narration TTS provider"`），将被取代的选项放入 `options_considered`，在 `rejected_because` 中注明已变更。

只改下游产物（`asset_manifest`、prop）而不更新 log 中的旧决策是缺陷：看板会继续显示过时选择（例如用户改 Chirp3 后仍显示 `voice → openai_onyx`）。看板用 **(category, subject) 对** 识别决策，并将该对的最新条目渲染为当前（标「revised」）— 因此修复方式是追加 subject 相同的新条目，切勿静默改旧条目或改 subject 措辞（改 subject 会被当作不同决策，两条都会显示）。同一 category 内保持不同决策（例如 TTS 与 image 的 `provider_selection`）正是为何 key 是 pair 而非仅 category。这适用于每个阶段，不限于 `idea`。

### 同时呈现两种 Composition Runtime（硬规则）

当机器上 Remotion 与 HyperFrames 均可用（查 `video_compose.get_info()["render_engines"]`）时，Agent **必须在提案阶段锁定 `render_runtime` 之前向用户呈现两种选项**。Agent 可以带理由推荐其一 — 但即使流水线清单或导演技能暗示默认值，也 **禁止** 静默选「默认」。

呈现 **必须** 包含，对每个 runtime：

1. 一句通俗说明它对本 brief **最擅长什么**。
2. 一句诚实权衡（为何此处可能不是最佳）。
3. Agent 的推荐及理由， tied 到 brief 的 delivery_promise 与视觉方案。

然后等待用户明确批准再继续。将完整 shortlist — **两种** runtime 及适用的任何「ffmpeg」选项 — 作为 `options_considered` 记入 `decision_log` 中的 `render_runtime_selection` 决策。当两者可用但 log 只考虑一种 runtime 时，属于 CRITICAL 审查发现。

例外：若机器上只有一种 runtime 可用，Agent 可继续用该 runtime，但 **必须** 明确说明（「本机未安装 HyperFrames；我将继续使用 Remotion。若需要替代方案请安装 HyperFrames。」）。`render_runtime_selection` 决策仍将不可用选项记为 `rejected_because: "runtime not available on this machine"`。

本规则适用于所有调用 `video_compose` 的流水线 — 不限 Wave 1。流水线导演技能可推荐 runtime，但该推荐是与用户对话的输入，不是已做决策。

### Composition 创作模式 — Templated 与 Atelier

与 *runtime* 正交的是 *authoring mode*：**如何** 构建 composition。在提案中作为独立决策呈现，并记入 `decision_log`（`category: "composition_mode"`）。

- **Templated** — 将 stock `cut.type` 场景类型（`text_card`、`stat_card`、`bar_chart`、…）组装进 `Explainer`/`CinematicRenderer` composition。快、省、稳 — 也是多数视频看起来雷同的原因。适合批量产出、本地化变体、快速草稿、低风险内部片段。
- **Atelier** — **从零手写 composition**： bespoke 场景、一次性主题、为本片写的 motion，经 `composition_mode: "atelier"` 渲染（见 `video_compose` → `_render_via_atelier`）。无复用创意组件；每次 fresh 视觉语言。

**hero 工作默认 atelier** — 营销、发布、品牌片、任何必须 impress 的单交付科普。决定规则：*复用引擎知识，永不复用创意组件。* atelier 模式下 stock 场景类型目录、`hyperframes-registry` 块、fixtures 与成品组件 **禁止** — 它们是冻结外观，会重新引入雷同。构建前经 **`skills/meta/taste-direction.md`** 设定 design read 与 taste dials，再经 **`skills/meta/bespoke-composition.md`**，顺序为：美术方向（`visual-style`）→ motion 原则（Disney 12，经 `framer-motion`/`lottie-bodymovin`）→ 引擎机制（`remotion-best-practices` + 仅将 stock 组件当作 *机制法典* 阅读）→ 经 atelier 路径渲染。以 **distinctness review** 收尾：*这会不会是任意其他产品的视频？是否复用了我做过的 look？* — 与「是否匹配参考」相反。Atelier 比 templated 更耗 token 与迭代；提案时说明，让用户知情 opt-in。

### 明确升级阻塞

发生阻塞时，Agent 必须立即用以下结构 surfaced：

1. 尝试了什么
2. 什么失败了
3. 问题是 auth、provider 访问、工具 bug，还是 prompt/设计质量
4. 下一步有哪些选项
5. Agent 推荐哪项及理由

在用户批准前不要用替代路径继续。

### 推荐风格

请用户选择时，不要只列选项。Agent 应：

- 提供 shortlist，
- 简要说明权衡，
- 推荐一项，
- 等待批准再继续。

### 禁止单方面替换

若批准路径被阻塞，Agent 可调查并准备替代，但 **未经用户批准不得执行** 那些替代。

尤其适用于：

- provider 互换，
- model 互换，
- fallback 工具，
- 用仅 prompt 替代 reference 驱动生成，
- 用静帧 animatic 替代真实 motion。

## 编排器

Agent 自身编排制作状态机：

`research -> proposal -> script -> scene_plan -> assets -> edit -> compose`

Agent：

1. 阅读流水线清单（`pipeline_defs/*.yaml`）以了解流程
2. 调用 `checkpoint.get_next_stage()` 找到恢复点
3. 阅读阶段的导演技能（`skills/pipelines/<pipeline>/<stage>-director.md`）以了解 **如何**
4. 使用工具（`tools/`）获得具体能力
5. 用审查元技能（`skills/meta/reviewer.md`）自审
6. 经检查点协议（`skills/meta/checkpoint-protocol.md`）设检查点
7. 当 `human_approval_default: true` 时呈现给人工批准

基础设施文件：

- `lib/checkpoint.py` — 读写检查点、阶段校验
- `tools/cost_tracker.py` — 预算治理
- `lib/pipeline_loader.py` — 清单加载与辅助

## 项目目录约定

每次制作运行会在 `projects/` 下创建项目工作区。该目录被 gitignore — 所有生成资产可重新生成。

```
projects/<project-name>/
├── artifacts/          # 各阶段 JSON 产物（research_brief、script、scene_plan 等）
├── assets/
│   ├── images/         # 生成图像 (PNG)
│   ├── video/          # 生成视频片段 (MP4)
│   ├── audio/          # 旁白片段 + 最终混音 (MP3/WAV)
│   ├── music/          # 背景音乐轨 (MP3)
│   └── subtitles.srt   # 生成字幕
└── renders/
    └── final.mp4       # 最终渲染视频（交付物）
```

**命名约定**：使用源自视频标题的 kebab-case（例如 `hidden-math-of-nature`、`how-music-rewires-brain`）。

流水线初始化时、任何阶段运行前：

1. **初始化工作区**：`python -c "from lib.checkpoint import init_project; init_project('<project-id>', title='<Title>', pipeline_type='<pipeline>')"` — 创建上述布局并写入 `project.json`（Backlot 看板读取的标记）。
2. **打开看板**：运行 `python -m backlot open <project-id>`。若需要会启动 Backlot 服务并在浏览器打开该项目 live board。若命令失败，继续制作 — 看板是观察者，永非阻塞。这是 Agent 唯一的看板职责；看板其余一切从磁盘推导。

所有工具与 Agent 必须将输出写到这些路径 — **始终传递 `projects/<project-id>/` 下的显式 `output_path`**。写到 repo 根、cwd 或临时目录的资产对用户看板不可见，违反工作区契约。

**atelier 与 HyperFrames 技能运行同样适用**：手写 composition 仍写入其拥有的规范产物（script 或 beats-plan、scene_plan 等价物、asset manifest）及 `projects/<project-id>/` 内的检查点。看板与 runtime 无关；跳过产物的运行只会得到降级看板。

## 音乐库

用户可将免版税音乐轨放入 `music_library/`（gitignore）。资产导演会在回退到 API 音乐生成前检查此文件夹。

```
music_library/
├── ambient_track.mp3
├── cinematic_epic.mp3
└── ...
```

若文件夹有曲目，提案与资产阶段应将其与生成音乐一并作为选项呈现。详见 proposal-director 与 asset-director 技能。

## 可用流水线

| 流水线 | 最适合 | 稳定性 |
|----------|----------|-----------|
| `animated-explainer` | 主题到全生成科普 | production |
| `talking-head` | 素材主导说话人视频 | beta |
| `screen-demo` | 录屏与演练 | production |
| `clip-factory` | 从单一长源切多片段 | beta |
| `podcast-repurpose` | 播客高光与衍生 | beta |
| `cinematic` | 预告、teaser、情绪剪辑 | production |
| `animation` | 动效与动画优先视频 | production |
| `character-animation` | 本地 rig 卡通角色与可复用角色表演 | beta |
| `hybrid` | 源素材 + 辅助画面 | production |
| `avatar-spokesperson` | 主持人 avatar 或 lip-sync 视频 | production |
| `localization-dub` | 字幕、配音、翻译变体 | beta |
| `framework-smoke` | 测试：最小 2 阶段冒烟 | test |

> **Beta 流水线** 尚未完全审计。可用，但可能有毛边。用户选择时提及这一点。

## 强制预检

在任何创意工作之前执行。**优先用 `provider_menu_summary()` — 它是面向人类的汇总。** 原始 `support_envelope()` 是 firehose（配置良好的机器上可达数 MB JSON）；粘贴到聊天会淹没用户。

```bash
python -c "
from tools.tool_registry import registry
import json
registry.discover()
print(json.dumps(registry.provider_menu_summary(), indent=2))
"
```

摘要返回 Agent 应用通俗语言翻译的四个字段：

- `composition_runtimes` — `ffmpeg`、`remotion`、`hyperframes` 的布尔值。这是「同时呈现两种 Composition Runtime（硬规则）」检查的真源。
- `capabilities[]` — 每个能力族一条，`configured / total` 计数与 provider 列表。可直接用于「N of M configured」菜单。
- `setup_offers[]` — 不可用但 1 分钟 env-var 即可安装的工具。提供升级时优先展示。
- `runtime_warnings[]` — 如「hyperframes: npm package not resolvable」等具体信号。原样 surfaced 给用户 — 这类静默失败会破坏治理契约。

然后，需要更深检查时再（摘要不够时）：

```bash
# 完整菜单 — 按能力分组 available/unavailable。
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_menu(), indent=2))"

# 原始 envelope — 每个工具的完整契约。慢/firehose；仅调试用。
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.support_envelope(), indent=2))"
```

然后：

1. 阅读 `pipeline_defs/` 中选中的清单。
2. 对照 registry 检查每个 `required_tools` 条目。
3. 对不可用工具检查 `fallback_tools`。
4. 报告其一：`passed`、`degraded` 或 `blocked`。
5. 在用户理解真实能力 envelope 之前不要开始制作。

### Provider 菜单（预检强制）

上文已通过 `provider_menu_summary()` 获取。阅读该输出并 **以能力菜单呈现给用户**，而非扁平工具列表。仅当需要摘要折叠的 per-tool 细节时用 `provider_menu()`。

**如何呈现：**

```
YOUR CAPABILITIES

  Video Generation:  0/13 configured
  Image Generation:  1/7 configured
  Text-to-Speech:    1/3 configured
  Music Generation:  1/1 configured
  Composition:       3/3 configured (FFmpeg, video_stitch, video_trimmer)

  You can produce videos now with images + TTS + FFmpeg.
  Quick upgrades available — see below.
```

对 **每个** 有不可用 provider 的能力，从菜单输出读取 `install_instructions` 并按工作量分组呈现设置选项：

```
QUICK SETUP OPTIONS (1-minute each — set an env var in .env)

  Video Generation (0/13 -> unlock the biggest upgrade):
    Each unavailable provider lists its own install_instructions.
    Read them from the provider_menu output and present grouped by env var.
    Example: if 3 tools need FAL_KEY, group them: "FAL_KEY unlocks 3 providers"

  Image Generation (1/7 -> more style options):
    Same pattern — read install_instructions from each unavailable tool.

  Text-to-Speech (1/3):
    Same pattern.

LOCAL OPTIONS (free, needs hardware):
  Tools with runtime=LOCAL or runtime=LOCAL_GPU — read from the menu.

Already Available:
  List what's working. The user should feel good about what they have.
```

**规则：**
- **不要** 在 prompt 中硬编码 provider 名、API key 名或设置 URL。
  从 registry 每个工具的 `install_instructions` 字段读取。
- 始终显示比例：「X of Y configured」— 让广度可见。
- 按能力分组，而非单个工具。
- 展示 **现在能做什么**，再展示 **可解锁什么**。
- 用户拒绝设置时，用最佳可用路径继续 — 不纠缠。
- 若工具共享 env var，分组展示（从 `dependencies` 字段读取）。

### 设置提供协议

当工具为 `UNAVAILABLE` 但可通过简单配置修复时，**提供设置帮助而非静默绕过限制。** 许多工具只差一个 env var。

| 修复复杂度 | 行动 |
|----------------|--------|
| **1 分钟修复**（env var） | 提议现在协助配置 — 从工具读取 `install_instructions` |
| **5 分钟修复**（安装） | 说明安装什么及原因 — 从工具读取 `install_instructions` |
| **复杂修复**（GPU、模型下载） | 说明限制、会解锁什么，然后继续 |

**规则：**
- 始终告诉用户缺什么 **以及** 会得到什么
- 展示成本差异（免费本地 vs 付费 API）
- 用户拒绝设置时，用最佳可用路径继续 — 不纠缠
- 分组相关修复（共享同一 env var 依赖的工具）

### Composition Runtime（在 video_compose 内）

`video_compose` 有 **三种** 渲染引擎 / runtime。它们并行，非排序 — 选择在提案做出并锁定在 `edit_decisions.render_runtime`。检查哪些可用：

```bash
python -c "
from tools.tool_registry import registry
registry.discover()
info = registry._tools['video_compose'].get_info()
print('Render engines:', info.get('render_engines'))
print('Remotion note:', info.get('remotion_note'))
print('HyperFrames note:', info.get('hyperframes_note'))
"
```

| 引擎 | 用途 | 需要 |
|--------|----------|----------|
| **FFmpeg** | 纯视频剪切、拼接、trim、字幕烧录 | `ffmpeg` 二进制（始终可用） |
| **Remotion** | 基于 React 的 composition：静帧 → 动画视频、text cards、stat cards、charts、callouts、comparisons、spring 物理转场、词级 caption 烧录、TalkingHead avatar | Node.js (`npx`) + `remotion-composer/` + `node_modules` |
| **HyperFrames** | HTML/CSS/GSAP composition： kinetic typography、产品 promo、发布 reel、website-to-video、registry-block 驱动场景、SVG 角色 rig | Node.js ≥ 22 + FFmpeg + `npx`（经 `npx hyperframes` 消费） |

`render_runtime` **在提案锁定**（`proposal_packet.production_plan.render_runtime`）并 **经 edit_decisions 原样携带**。`video_compose` 按此字段路由；禁止静默 runtime 互换。若所选 runtime 在 compose 时不可用，按上文「明确升级阻塞」structured blocker。**Remotion 与 HyperFrames 决策矩阵** 见 `skills/core/hyperframes.md`。

### 关键规则：依赖 Motion 的请求

对交付物 inherently 依赖 motion 而非静态 coverage 的任何请求，将 motion 视为硬要求。例如：

- 科幻预告，
- 由生成片段构建的电影 teaser，
- hype 剪辑，
- avatar 或 agent 视频，
- 任何 promise 依赖 moving shots 而非静帧的 brief。

对此类请求：

- 若计划视觉处理依赖它，提案所选 `render_runtime`（Remotion、HyperFrames 或 FFmpeg）须 upfront 确认可用。
- **禁止** 静帧 fallback。不要悄悄把 job 变成 Ken Burns teaser、animatic 或 slide 视频。
- 当会把已批准交付从 motion-led 变为 still-led 时，**禁止** 仅 FFmpeg fallback。
- **禁止静默 runtime 互换。** 若锁定 `render_runtime="hyperframes"` 而 HyperFrames 不可用，**不要** 改路由到 Remotion。 surfaced 阻塞、提议选项、获用户批准、记录 `render_runtime_selection` 决策 — 然后继续。
- 立即 bubble 关键问题。若所选 runtime 不可用、渲染失败，或 provider 片段生成以阻塞已批准 treatment 的方式失败，在继续前停止并告知用户。
- 除非用户明确批准降级为 animatic 或 proof-of-concept，不要在降级产出上花更多 token 或时间。

**当 Remotion 可用时**，Agent 应用其设计制作计划：
- 带 `flat-motion-graphics` playbook 的科普 → Remotion 动画场景，非 Ken Burns
- 数据驱动视频 → Remotion stat cards 与 charts，非静帧截图
- 任何使用静帧的流水线 → Remotion spring 动画，非 FFmpeg pan-and-zoom
- **CLI/终端/安装流程的 screen demo → `TerminalScene`（合成录屏），非 OS 级捕获。** 见 `.agents/skills/synthetic-screen-recording/SKILL.md`。更快、确定、隐私安全。仅当 demo 是真实 app UI 或需要不可预测 live 行为时用真实捕获（`screen_recorder`、`cap_recorder`、`playwright-recording`）。

### Remotion 在 `remotion-composer/` 中可用的 scene types

权威列表与 cut schema 见 `remotion-composer/SCENE_TYPES.md`。当前经 `cut.type` 可用的 scene types：
`text_card`、`stat_card`、`callout`、`comparison`、`hero_title`、`terminal_scene`、`anime_scene`、`bar_chart`、`line_chart`、`pie_chart`、`kpi_grid`、`progress_bar`。Overlay types 含 `section_title`、`stat_reveal`、`hero_title`、`provider_chip`。

这些 stock scene-types 是 **templated** 路径 — 快且稳，但也是视频看起来雷同的原因。**hero 工作优先 atelier 模式**（手写 composition）而非此目录；将这些类型当作 *机制法典* 阅读，而非组装菜单。见上文「Composition 创作模式」与 `skills/meta/bespoke-composition.md`。

**当 Remotion 不可用** 且 **未** 锁定 `render_runtime="remotion"` 时，`video_compose` 可对静帧用 FFmpeg Ken Burns motion。仍可用但视觉吸引力较低。在提案中说明此权衡。当 **已** 锁定 `render_runtime="remotion"` 而 Remotion 不可用，那是阻塞 — 升级，不要静默互换。

当锁定 `render_runtime="hyperframes"` 而 HyperFrames 不可用（Node < 22、缺 `ffmpeg`/`npx`，或 `hyperframes doctor` 报错），同样是阻塞。未经用户批准 + 记录的 `render_runtime_selection` 决策，不要 substitute Remotion 或 FFmpeg。

路由自动 — `video_compose` 读 `edit_decisions.render_runtime` 并 dispatch 到匹配引擎（`_render_via_hyperframes`、`_remotion_render` 或 `_render_via_ffmpeg`）。但 **Agent 在提案时必须知道 Remotion 与 HyperFrames 都存在**，以便有意设计视觉方案。不要对 HTML/GSAP 更自然表达的 motion-graphics-heavy 概念默认 Remotion，也不要对复用现有 React scene stack 的 brief 默认 HyperFrames。

## 能力发现

OpenMontage 用两层做能力选择：

- selector 工具：能力级路由如 `tts_selector`、`video_selector`
- provider 工具：经 registry 发现、调用具体后端的工具

始终先 inspect registry：

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_catalog(), indent=2))"
```

对 finalist 工具 inspect：

- `capability`
- `provider`
- `usage_location`
- `supports`
- `fallback_tools`
- `related_skills`

registry 能回答时不要依赖记忆或旧文档。

## 工具族

**不要维护硬编码工具列表。** 始终在运行时查询 registry：

```bash
# 按 capability 分组的所有工具（TTS、video_generation、image_generation 等）
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"

# 按 provider 分组的所有工具（elevenlabs、openai、ffmpeg 等）
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.provider_catalog(), indent=2))"
```

在输出中关注的主要 capability 族：

- **tts** — 文本转语音 provider。经 `tts_selector` 路由。
- **video_generation** — 视频生成 provider（云、本地 GPU、stock）。经 `video_selector` 路由。
- **image_generation** — 图像生成 provider（云、本地 GPU、stock）。经 `image_selector` 路由。
- **music_generation** — 音乐与音效生成。
- **video_post** — 合成、拼接、trim（基于 FFmpeg，始终本地）。
- **audio_processing** — 混音、增强（基于 FFmpeg，始终本地）。
- **analysis** — 转录、场景检测、帧采样。
- **avatar** — Talking head 与 lip sync 生成。
- **character_animation** — 本地角色 spec、SVG rig、pose library、action timeline、预览与 QA。
- **3d_world_generation** — 本地语义地形、程序化 biome 散布、显式 landmark、诊断 pass、确定性 HyperFrames/Three.js 相机 fly-through。经 `threejs_world` 路由，阅读 `skills/creative/3d-world-generation.md` 与 `.agents/skills/threejs-world-generation/SKILL.md`。
- **3d_asset_acquisition** — 生产级 Three.js 世界的 rights-safe GLTF/GLB 目录。经 `threejs_asset_catalog` 路由；请求 detailed 或 reference-grade 环境时勿用 blockout  primitive 替代。
- **3d_asset_generation** — 从文本或概念图生成 unique textured/PBR mesh。文本描述 hero 资产经 `atlas_3d`，image-conditioned 资产与区域物体提取经 `fal_3d`，阅读 `.agents/skills/3d-asset-generation/SKILL.md`。每次首次付费调用前宣告 provider/model/单位成本，批量前先 sample。
- **3d_world_rendering** — Blender 中的生产组装、地形、光照、材质、相机与图像序列渲染。经 `blender_world` 路由；交互/blockout 审查用 Three.js，请求 reference-grade 场景密度时勿用 Three.js 替代 Blender。
- **enhancement** —  upscale、背景移除、人脸增强、调色。

registry 中每个工具声明 `best_for`、`install_instructions`、`runtime`（LOCAL、API、LOCAL_GPU、HYBRID）与 `status`。阅读这些字段 — 不要凭记忆假设工具优势。

### 工具类命名约定

所有工具类使用 **PascalCase，无 "Tool" 后缀**。在 Python 中 import 工具时：

| 模块 | 类名 | 非 |
|--------|-----------|-----|
| `tools.audio.music_gen` | `MusicGen` | ~~MusicGenTool~~ |
| `tools.video.video_compose` | `VideoCompose` | ~~VideoComposeTool~~ |
| `tools.audio.audio_mixer` | `AudioMixer` | ~~AudioMixerTool~~ |
| `tools.tts.elevenlabs_tts` | `ElevenLabsTTS` | ~~ElevenLabsTTSTool~~ |
| `tools.analysis.transcriber` | `Transcriber` | ~~TranscriberTool~~ |
| `tools.subtitle.subtitle_gen` | `SubtitleGen` | ~~SubtitleGenTool~~ |

不确定时检查：`grep "^class " tools/<path>.py`

所有工具经 `.execute(params_dict)` 调用（返回带 `.success`、`.data`、`.error` 的 `ToolResult`），**非** `.run()`。

### Selector 模式

三个 selector 工具抽象多 provider 能力。**Selector 从 registry 自动发现 provider。** 新增 provider 工具会自动经 selector 可用 — 无需改 selector 代码。

| Selector | 路由到 | 发现方式 |
|----------|-----------|-----------------|
| `tts_selector` | 所有 `capability="tts"` 的工具（ElevenLabs、Google TTS、OpenAI、Piper、Azure、fish.audio） | `registry.get_by_capability("tts")` |
| `image_selector` | 所有 `capability="image_generation"` 的工具（FLUX、Google Imagen、GPT Image、Recraft 等） | `registry.get_by_capability("image_generation")` |
| `video_selector` | 所有 `capability="video_generation"` 的工具 | `registry.get_by_capability("video_generation")` |

Selector 按：用户偏好 > 可用性 > 发现顺序 路由。它们在 provider 间透明适配输入 schema。

## 面向用户的规划协议

提交执行前，呈现：

1. brief 仍开放时 `4-5` 个概念方向。
2. 推荐流水线。
3. 推荐工具路径。
4. 实际可用的替代工具路径。
5. 成本估计与质量权衡。
6. **音乐计划** — 任何含音频的流水线强制。见下文。
7. 分阶段制作计划。
8. 资产生成前的批准门。

若用户偏好特定 vendor 且该工具可用，直接 surfaced。不要隐藏 provider 选择。

### 音乐计划（强制）

音乐是任何视频的关键部分。**在提案/idea 时向用户 surfaced 音乐情况** — 不要静默推迟到资产阶段，失败会变得昂贵。

按此顺序检查音乐可用性并呈现选项：

1. **用户音乐库：** 检查 `registry.get_by_capability("music_library")` 并 inspect `music_library/`。若有曲目，列出时长让用户选。
2. **免版税搜索：** 检查 `registry.get_by_capability("music_search")` 中已配置的搜索/下载工具。报告许可约束及是否需要 key。
3. **音乐生成 API：** 检查 `registry.get_by_capability("music_generation")`。诚实报告 status、quota、成本与质量权衡。
4. **自带：** 说明用户可通过 `music_library/` drop 路径提供曲目（例如来自 YouTube Audio Library 或 Jamendo）。

**始终向用户呈现明确选择：**
- 使用库中曲目（哪一首？）
- 提供不同曲目（放入 `music_library/`）
- 经 API 生成（若可用 — 说明 provider 与成本）
- 无音乐继续

**若无任何音乐来源：** 明确告知用户。不要在资产阶段才 surprise。

在 proposal/brief 产物中记录音乐决策，以便资产导演知道做什么。

## 流水线资产期望

每条流水线清单的 `tools_available` 字段声明阶段可用工具。多 provider 能力用 selector — selector 路由到任何可用项。各阶段权威列表读流水线清单。

## 阶段 Agent

每个阶段产出一份规范产物，成为下一阶段契约。阶段导演技能教 Agent **如何** 产出。

| 阶段 | 导演技能 | 规范输出 | 核心质量栏 |
|------|---------------|------------------|------------------|
| `idea` | `*-director.md` | `brief` | 清晰 hook、目标平台、时长、tone、用户意图 |
| `script` | `*-director.md` | `script` | 结构化章节、有效 timing、连贯旁白 |
| `scene_plan` | `*-director.md` | `scene_plan` | 有序场景、timing、资产需求 |
| `assets` | `*-director.md` | `asset_manifest` | 出处、路径、model/工具元数据、场景关联 |
| `edit` | `*-director.md` | `edit_decisions` | 具体 cut、overlay、字幕/音乐决策 |
| `compose` | `*-director.md` | `render_report` | 输出路径、编码 profile、验证说明 |

阶段契约规则：

- 已完成或 awaiting-human 的检查点必须包含该阶段规范产物。
- 规范产物必须对 `schemas/artifacts/` 中 JSON schema 校验。
- 非规范输出如媒体文件属于阶段特定目录。
- 工具应记录 seed/model 版本以便复现。

## 审查者协议

审查者是元技能（`skills/meta/reviewer.md`）—  advisory，从不直接阻塞进展。

- 每个阶段执行后、检查点前自审。
- 从流水线清单加载当前阶段的 `review_focus` 项。
- 最多两轮审查。之后带 warning 通过并继续。
- 发现分类：critical（必须修）、suggestion（应修）、nitpick（最好有）。
- Critical 发现 → 修复并重审。Suggestion → 记录并继续。
- 将 playbook `quality_rules` 当作约束，非建议。

## 人工检查点协议

检查点协议元技能（`skills/meta/checkpoint-protocol.md`）教 Agent 何时暂停：

- 从流水线清单读每阶段 `human_approval_default`。**清单值具有约束力** —  never 重新判断。`lib/checkpoint.py` 强制执行：gated 阶段不能在没有 `human_approved=True` 时写成 `completed`。
- 典型 gated 阶段：`idea`/`proposal`、`script`、`scene_plan`、**`assets`**（compose 锁定前逐场景审查生成资产 — Backlot 看板 filmstrip），以及流水线有的 `publish`。多数流水线在 `edit` 与 `compose` 自动继续，但并非全部（documentary-montage 在 `edit` gate）— 你加载的清单是唯一权威。
- 需要批准时：将检查点写成 `awaiting_human`，呈现产物摘要、审查发现与成本快照 — 然后 **结束你的回合**。同一响应中继续流水线工作是 gate 违规。
- **批准按 gate 计。** 早期「继续」不覆盖后续 gate；明确的全 run 预授权须记为 `decision_log` 条目（`category: "approval_policy"`）才有效。
- 等待人工批准、请求修订或中止。

## 通信协议

Agent 经规范 JSON 产物、检查点、流水线清单与工具 registry 协调。

主要文件：

- 产物 schema：`schemas/artifacts/`
- 检查点 schema：`schemas/checkpoints/checkpoint.schema.json`
- 流水线清单 schema：`schemas/pipelines/pipeline_manifest.schema.json`
- 流水线清单：`pipeline_defs/`
- 风格 playbook：`styles/*.yaml`（由 `schemas/styles/playbook.schema.json` 校验）
- 工具契约：`tools/base_tool.py`
- 工具 registry：`tools/tool_registry.py`
- 阶段导演技能：`skills/pipelines/<pipeline>/<stage>-director.md`
- 元技能：`skills/meta/*.md`

检查点规则：

- 检查点位于 `projects/<project_id>/checkpoint_<stage>.json`（项目工作区 — Backlot 看板监视的对象）。
- `status` 可为 `completed`、`failed`、`awaiting_human` 或 `in_progress`。
- 进入每阶段写 `in_progress` 检查点；在 `assets`/`compose` 期间，每完成一个 scene/asset 单元后刷新 `metadata.partial_progress` — 驱动看板 live 进度。
- `completed` 与 `awaiting_human` 检查点必须含规范产物。
- gated 阶段（`human_approval_default: true`）仅能在 `human_approved=True` 时写成 `completed` — 否则 writer 抛出 GATE VIOLATION。
- 被取代的检查点自动归档到 `projects/<project_id>/history/` — 阶段重跑永不销毁运行历史。
- 无效检查点或无效规范产物是契约违规，应 fail fast。

流水线清单规则：

- 流水线是 `pipeline_defs/` 中的声明式 YAML 清单。
- 阶段声明：`skill`（导演技能路径）、`produces`、`tools_available`、`review_focus`、`success_criteria`、`human_approval_default`。
- 新增流水线需要清单 + 阶段导演技能。

工具规则：

- 每个制作工具必须继承 `BaseTool`。
- 工具发现经 registry，非 ad hoc import。
- Support-envelope 报告是 capability、status 与资源需求的真源。

## 风格 Playbook

| Playbook | 最适合 |
|----------|----------|
| `clean-professional` | 企业、教育、SaaS |
| `premium-minimalist` | 投资者更新、专家科普、产品叙事 |
| `flat-motion-graphics` | 社交媒体、TikTok、初创 |
| `minimalist-diagram` | 技术深度、架构 |
| `ink-sketch` (Ink Theater) | 手绘 ink-on-white doodle 动画；角色自画、行走、跳舞；contraption 科普 |

custom、atelier、品牌、发布或 hero 工作前，选 playbook 前读 `skills/meta/taste-direction.md`。将其 `taste_profile` 带入 proposal，以便后续阶段保留 design read、visual variance、motion intensity、information density、reference strategy 与 anti-patterns。

### 手绘「doodle」动画 → Ink Theater / Ink Puppet

对任何想要 **手绘 ink doodle** 外观的 brief —「sketch 活过来」「铅笔/ stick figure 走或跳」「小角色演绎想法」、白板 doodle 科普 — 使用 **Ink Theater** 引擎 + **Ink Puppet** mocap 系统（`skills/creative/ink-theater.md`、`ink-theater/README.md`）。它是 **风格 + 可复用引擎，非新流水线**：插画/contraption 片走 `animation` 流水线；mocap 角色（自画 → 经 `InkPuppet.choreograph([...])` 走/跳/挥）走 `character-animation`。跨工具入口：**`/ink-art`**（从零创建 vector doodle）与 **`/animated-drawing`**（用 mocap 动画 *提供的* 画 — raster；`skills/creative/animated-drawing.md`）。Never 手调角色 motion — Agent 只选命名 mocap clip。

## 层级地图

OpenMontage 有三层指令：

1. `tools/`
   有什么、什么可用、成本、runtime、fallback、相关技能。
2. `skills/`
   OpenMontage 希望如何在流水线中使用那些工具。
3. `.agents/skills/`
   原始 vendor 或技术知识。

阅读顺序：

1. registry / 工具契约 — 发现有什么
2. 相关 pipeline 或 creative 技能（Layer 2）— 知在此上下文 **如何** 用
3. 底层 vendor 技能（Layer 3）— **调用任何生成工具前强制**

**工具用法优先技能而非源码。** 技能存在正是为了常见情况不需要实现细节。Layer 2 告诉你 *什么* 与 *何时*。Layer 3 告诉你 *如何*。撰写 prompt、选参数或理解用法模式时，应读技能 — 而非 `.py` 文件。

**例外：调试、审计与验证治理契约。** 当技能与工具不一致，或行为与技能声称不同时，读工具源码是合理的 — 常常是捕获静默可用 bug 或 stale doc string 的唯一方式。拒绝看实现的审计会错过最重要的 bug。若为调试读源码，考虑发现是否应后续更新技能，以免下个 Agent 重复 dive。

**Layer 3 非可选。** 每个生成工具（video、image、TTS、music）有 `agent_skills` 字段列出 Layer 3 技能。含 provider 特定 prompt 工程、参数调优与质量技巧。写 prompt 前阅读。泛化 prompt 与 skill-informed prompt 之差，是「可用」与「电影感」之差。

示例：调用 `kling_video` 前，读其 `agent_skills` → `ai-video-gen` → 获取 Kling 特定 prompt 结构、镜头方向语法与 model 最佳响应的质量关键词。

### Layer 3 技能，按类别

`.agents/skills/` 目录很大。若非经工具的 `agent_skills` 指针进入，用下表按 *你要做什么* 找文件：

| 类别 | 技能 |
|---|---|
| **Composition runtime** | `remotion`、`remotion-best-practices`、`synthetic-screen-recording`（经 Remotion TerminalScene 的假终端/UI demo）、`threejs-world-generation`（语义地形与自由视点 HyperFrames 世界） |
| **Animation knowledge (generic)** | `gsap-core`、`gsap-timeline`、`gsap-plugins`（SplitText / MorphSVG / DrawSVG / MotionPath / Flip / CustomEase）、`gsap-utils`、`gsap-react`、`gsap-performance`、`gsap-scrolltrigger`、`gsap-frameworks`、`framer-motion`（Disney 12 原则）、`lottie-bodymovin`（Lottie 导出） |
| **Character animation** | `character-rigging`、`svg-character-animation`、`pose-library-design`、`canvas-procedural-animation`、`character-animation-qa` |
| **Image generation** | `bfl-api`、`flux-best-practices` |
| **Video generation** | `seedance-2-0`（首选 premium 默认 — cinematic、trailer、multi-shot、synced audio、lip-sync）、`gemini-omni`（对话式视频编辑、reference tag、timecoded beats）、`ai-video-gen`、`ltx2` |
| **Audio** | `elevenlabs`、`music`、`sound-effects`、`acestep`、`text-to-speech`、`azure-text-to-speech`（可选云 TTS — 工具 `azure_tts`，与 `azure_stt` 同 Speech key）、`setup-api-key` |
| **Speech-to-text** | `speech-to-text`（whisper `transcriber` — 默认，离线）、`azure-speech-to-text`（可选云 STT — 工具 `azure_stt`，设置 `AZURE_SPEECH_KEY` 时优先） |
| **Avatar / lip-sync** | `avatar-video`、`heygen`、`create-video`、`faceswap`、`video-translate`、`agents` |
| **Capture** | `playwright-recording`（浏览器流程）、`ffmpeg`（后期） |
| **Visualization** | `beautiful-mermaid`、`d3-viz`、`manim-composer`、`manimce-best-practices`、`manimgl-best-practices` |
| **Media editing** | `video-edit`、`video-download`、`video-understand`、`video-toolkit`、`visual-style` |

**不确定时，先读该类别的 meta 路由文件：**
- 选 animation runtime？→ `skills/meta/animation-runtime-selector.md` 在 Remotion primitive、GSAP plugin、framer-motion、Lottie、Manim、D3 间路由。
- 选录屏模式（真实捕获 vs 合成终端）？→ `pipeline_defs/screen-demo.yaml` + `skills/pipelines/screen-demo/idea-director.md`。

## 快速查找

| 问题 | 查看位置 |
|----------|---------------|
| 有哪些工具？ | `tools/tool_registry.py` 与 `registry.support_envelope()` |
| 某 capability 有哪些 provider？ | `registry.capability_catalog()` |
| 某 vendor 有哪些工具？ | `registry.provider_catalog()` |
| 工具实际如何工作？ | registry 中的 `usage_location` |
| 此流水线阶段应如何行为？ | `skills/pipelines/<pipeline>/...` |
| 检查点/审查策略是什么？ | `skills/meta/` |

## 禁止事项

- **不要绕过流水线。** Never 写 ad-hoc 脚本直接调工具。所有制作经带导演技能的流水线阶段。见规则零。
- **不要未读 Layer 3 技能就调用生成工具。** 查工具的 `agent_skills` 字段，读引用技能，再用该指导 craft prompt。
- **不要跳过阶段导演技能。** 执行任何流水线阶段前，读其导演技能。技能含质量栏、工作流与审查标准。
- 不要使用已删除的遗留名如 `tts_cloud`、`tts_engine` 或 `video_gen`。
- 不要硬编码 provider 名、API key 名或设置 URL。从 registry 的 `install_instructions` 与 `dependencies` 字段读取。
- 不要告诉受限共享安装用户手动加凭证、创建 `.env` 或 export key。将不可用 provider 作为管理员设置请求 surfaced，仅继续 centrally provisioned 的能力。
- 在提供直接 vendor 凭证前，检查 registry 是否已有通过已配置 provider 的可用 wrapper（例如 fal.ai 托管的 partner model）。
- 不要在用户对制作计划批准前开始资产生成。
- 不要隐藏 degraded 路径。明确记录替换与 blocked 选项。
- 不要孤立呈现单个不可用工具。始终展示完整能力图景：「此 capability 的 Y 个 provider 中 X 个已配置。」
- 不要在预检跳过 Provider 菜单。用户必须看到有什么 **以及** 可解锁什么。
- 不要在未先告知用户并在变更 material 时获批准的情况下更改 provider、model 或 render path。
