# OpenMontage 架构

> 最后更新：2026-03-28 | 源自代码探索，而非既有文档。

OpenMontage 是一个**由 Agent 编排的视频制作平台**。LLM 编程助手（Claude Code、Cursor、Copilot 等）充当编排者——读取流水线清单、遵循技能说明、调用 Python 工具并持久化检查点状态。运行时没有 Python 编排器；Agent _就是_ 控制平面。

---

## 高层流程

```
User gives topic/idea
        |
        v
Agent reads pipeline manifest (YAML)
        |
        v
For each stage:
   1. Agent reads stage-director skill (Markdown)
   2. Agent calls Python tools via tool registry
   3. Agent writes checkpoint (JSON) with artifacts
   4. Agent self-reviews using meta/reviewer skill
   5. Human approval gate (if configured)
        |
        v
Final video output
```

---

## 仓库布局

```
OpenMontage/
├── lib/                    # Core runtime infrastructure (Python)
│   ├── config_model.py     # Pydantic config: LLM, budget, checkpoint, output, paths
│   ├── checkpoint.py       # Pipeline state persistence & stage transitions
│   ├── pipeline_loader.py  # YAML manifest loading & validation
│   ├── media_profiles.py   # Platform-specific render profiles (YouTube, TikTok, etc.)
│   ├── env_loader.py       # .env variable management
│   └── providers/          # (Reserved for future provider abstractions)
│
├── tools/                  # 57+ Python tool implementations
│   ├── base_tool.py        # Abstract base class — the tool contract
│   ├── tool_registry.py    # Auto-discovery singleton registry
│   ├── cost_tracker.py     # Budget governance (estimate → reserve → reconcile)
│   ├── analysis/           # Transcription, scene detection, frame sampling, video understanding
│   ├── audio/              # TTS (ElevenLabs, OpenAI, Piper, Azure, Google), music gen, mixing, enhancement
│   ├── avatar/             # Talking head animation, lip sync
│   ├── enhancement/        # Upscale, bg removal, face enhance/restore, color grading
│   ├── graphics/           # Image gen (FLUX, GPT Image, Recraft, local diffusion), stock, diagrams, code snippets, math animation
│   ├── publishers/         # (Reserved)
│   ├── subtitle/           # SRT/VTT generation from timestamps
│   └── video/              # 13 video gen providers, composition, stitching, trimming
│
├── pipeline_defs/          # YAML pipeline manifests
├── schemas/                # JSON Schema definitions for validation
│   ├── artifacts/          # 11 artifact schemas (brief → publish_log)
│   ├── checkpoints/        # Checkpoint state schema
│   ├── pipelines/          # Pipeline manifest schema
│   ├── styles/             # Style playbook schema
│   └── tools/              # Tool-specific schemas
│
├── skills/                 # Layer 2: OpenMontage-specific agent instructions
│   ├── core/               # FFmpeg, Remotion, WhisperX, color grading skills
│   ├── creative/           # Video editing, enhancement, data viz, prompt engineering
│   ├── meta/               # reviewer, checkpoint-protocol, skill-creator
│   └── pipelines/          # Per-pipeline stage-director skills
│
├── .agents/skills/         # Layer 3: external technology skills (FFmpeg, HyperFrames, GSAP, etc.)
├── styles/                 # Visual style playbooks (YAML) + loader
├── remotion-composer/      # Node.js/React — Remotion video composition renderer
├── tests/                  # Contract tests, QA integration tests, eval harness
├── docs/                   # Best-practices guides, session handoffs, audits
└── config.yaml             # Global runtime configuration
```

---

## 核心架构原则

### 1. Agent 优先编排

**没有 Python 编排器**。LLM Agent：
- 读取流水线清单以了解阶段顺序
- 读取各阶段导演技能以获取详细说明
- 调用工具、评估结果、做出创意决策
- 写入检查点以在阶段之间持久化状态

Python 仅提供**工具与持久化**。所有智能体现在技能说明（Markdown）与流水线清单（YAML）中。

### 2. 运行时无需 LLM API Key

OpenMontage 在运行时不调用 LLM API。在用户 IDE 中运行的编程助手 _就是_ LLM。需要生成能力的工具（图像、视频、TTS）直接调用领域专用 API（ElevenLabs、fal.ai、HeyGen 等），而非通用 LLM 端点。

### 3. 双轨 Provider 支持

每项能力必须同时支持 **API Provider**（云端、付费）与**本地/开源替代方案**（免费、依赖 GPU）。选择器（selector）模式通过路由到可用实现来强制这一点。

---

## 工具系统

### BaseTool 契约

所有工具继承 `BaseTool`（ABC）并声明：

| 字段 | 用途 |
|-------|---------|
| `name`, `version` | 身份标识 |
| `tier` | CORE、VOICE、ENHANCE、GENERATE、SOURCE、ANALYZE、PUBLISH |
| `capability` | 功能（如 `tts`、`image_generation`、`video_post`） |
| `provider` | 服务方（如 `elevenlabs`、`ffmpeg`、`selector`） |
| `runtime` | LOCAL、LOCAL_GPU、API、HYBRID |
| `stability` | EXPERIMENTAL、BETA、PRODUCTION |
| `dependencies` | 所需二进制（`cmd:ffmpeg`）、环境变量（`env:ELEVENLABS_API_KEY`）、Python 包（`python:torch`） |
| `input_schema`, `output_schema` | 输入/输出的 JSON Schema |
| `fallback_tools` | 有序降级链 |
| `agent_skills` | 指向 Layer 3 知识技能的链接 |
| `resource_profile` | CPU、RAM、VRAM、磁盘、网络需求 |
| `retry_policy` | 最大重试次数、退避策略 |

**必需方法：** `execute(inputs) -> ToolResult`

`ToolResult` 包含：`success`、`data`、`artifacts`（文件路径）、`error`、`cost_usd`、`duration_seconds`、`seed`、`model`。

### 工具注册表

`ToolRegistry` 是通过 `pkgutil.walk_packages()` 自动发现所有 `BaseTool` 子类的单例。无需手动注册。

主要查询：
- `get_by_capability("tts")` — 全部 TTS 工具
- `get_by_provider("elevenlabs")` — 全部 ElevenLabs 工具
- `get_available()` — 依赖已满足的工具
- `find_fallback("elevenlabs_tts")` — 解析降级链
- `support_envelope()` — 供 Agent 使用的完整能力报告
- `gpu_required_tools()`、`network_required_tools()`

### 选择器模式

三个选择器工具抽象多 Provider 能力：

| 选择器 | 能力 | 选择方式 |
|----------|-----------|---------------------|
| `tts_selector` | 文本转语音 | 按任务匹配、质量、可控性、可靠性、成本、延迟与连续性对已发现 Provider 排序 |
| `image_selector` | 图像生成 | 对实时注册表中的 Provider 排序；无硬编码 Provider 顺序 |
| `video_selector` | 视频生成 | 对实时注册表中的 Provider 排序；用户明确偏好时优先尊重 |
| `atlas_image` / `atlas_video` | Atlas Cloud 生成 | 暴露图像生成/编辑与文本/图像/参考/视频编辑生成的精确逐模型路由目录 |

选择器路由依据：用户明确设置时的偏好，其次是对可用 Provider 的评分排序。它们在 Provider 之间透明适配输入 Schema。

### 按类别的工具清单

**Analysis（5）：** transcriber (WhisperX)、azure_stt、scene_detect、frame_sampler、video_understand (CLIP/BLIP-2)

**Audio（9）：** elevenlabs_tts、google_tts、openai_tts、piper_tts、azure_tts、tts_selector、music_gen、audio_mixer、audio_enhance

**Avatar（2）：** talking_head (SadTalker/MuseTalk)、lip_sync (Wav2Lip)

**Enhancement（5）：** upscale (Real-ESRGAN)、bg_remove (rembg/U2Net)、face_enhance、face_restore (CodeFormer/GFPGAN)、color_grade (FFmpeg LUTs)

**Graphics（13）：** flux_image、grok_image、google_imagen、openai_image、recraft_image、local_diffusion、pexels_image、pixabay_image、image_selector、code_snippet、diagram_gen、math_animate (ManimCE)、image_gen (deprecated)

**Subtitle（1）：** subtitle_gen

**Video（18）：** grok_video、heygen_video、higgsfield_video、veo_video、kling_video、runway_video、minimax_video、wan_video、hunyuan_video、cogvideo_video、ltx_video_local、ltx_video_modal、pexels_video、pixabay_video、video_selector、video_compose (FFmpeg)、video_stitch、video_trimmer

---

## 流水线系统

### 流水线清单

每条流水线是 `pipeline_defs/` 中的 YAML 文件，定义：

```yaml
name: animated-explainer
version: "2.0"
category: generated          # talking_head | generated | hybrid | screen_recording | animation | cinematic | custom
default_checkpoint_policy: guided

orchestration:
  mode: executive-producer
  skill: pipelines/explainer/executive-producer
  budget_default_usd: 2.00
  max_revisions_per_stage: 3

compatible_playbooks:
  - clean-professional
  - flat-motion-graphics

stages:
  - name: research
    skill: pipelines/explainer/research-director
    produces: [research_brief]
    tools_available: []
    checkpoint_required: false
    human_approval_default: false
    review_focus: [...]
    success_criteria: [...]
  # ... through publish
```

### 可用流水线

| 流水线 | 类别 | 说明 |
|----------|----------|-------------|
| `animated-explainer` | generated | AI 制作的讲解片：调研、旁白、画面、音乐 |
| `animation` | animation | 动态图形、 kinetic typography |
| `avatar-spokesperson` | talking_head | 虚拟形象驱动的 presenter 视频 |
| `character-animation` | animation | 本地绑定卡通角色：SVG 绑定、姿势库、GSAP 时间轴与 HyperFrames 渲染 |
| `cinematic` | cinematic | 预告片、teaser、情绪驱动剪辑 |
| `clip-factory` | custom | 从长源素材批量生成短视频 |
| `hybrid` | hybrid | 源 footage + AI 生成辅助画面 |
| `localization-dub` | custom | 字幕、配音与现有视频翻译 |
| `podcast-repurpose` | hybrid | 播客高光转视频 |
| `screen-demo` | screen_recording | 软件录屏与 walkthrough |
| `talking-head` | talking_head | 以 footage 为主的讲者视频 |
| `framework-smoke` | custom | 框架验证的最小冒烟测试 |

### 标准阶段 progression

多数制作流水线遵循规范的 8 阶段流程：

```
research → proposal → script → scene_plan → assets → edit → compose → publish
```

每个阶段：
1. 拥有**阶段导演技能**（给 Agent 的 Markdown 说明）
2. 声明 **tools_available**（Agent 可调用的工具）
3. **产出**一个或多个规范工件（artifact）
4. 具备 **review_focus** 标准与 **success_criteria**
5. 可要求继续前 **人工审批**

专用流水线可插入领域阶段。例如，
`character-animation` 在 `scene_plan` 之前增加 `character_design` 与 `rig_plan`，
随后在 `projects/<project-name>/renders/final.mp4` 输出 HyperFrames 工作区与最终交付物。

---

## 检查点系统

检查点将流水线状态以 JSON 持久化在项目 `pipeline/` 目录。

```json
{
  "version": "1.0",
  "project_id": "my-video",
  "stage": "script",
  "status": "completed",
  "timestamp": "2026-03-28T10:00:00Z",
  "checkpoint_policy": "guided",
  "human_approval_required": false,
  "human_approved": true,
  "artifacts": { "script": { ... } },
  "review": { ... },
  "cost_snapshot": { ... }
}
```

**状态值：** `pending` | `in_progress` | `awaiting_human` | `completed` | `failed`

**检查点策略：**
- `guided` — 关键创意阶段写检查点，机械阶段自动继续
- `manual_all` — 每个阶段都需人工批准
- `auto_noncreative` — 除非阶段为创意类（assets、edit），否则自动继续

**函数：** `write_checkpoint()`、`read_checkpoint()`、`get_latest_checkpoint()`、`get_completed_stages()`、`get_next_stage()`

### 规范工件（11 种，均经 JSON Schema 校验）

| 工件 | 阶段 | 内容 |
|----------|-------|----------|
| `research_brief` | research |  landscape 分析、数据点、受众洞察、角度 |
| `proposal_packet` | proposal | 概念选项、制作计划、成本估算、审批关卡 |
| `brief` | idea | 标题、hook、要点、调性、风格、平台、时长 |
| `script` | script | 带时间戳的段落、增强提示、发音指南 |
| `scene_plan` | scene_plan | 场景定义：类型、描述、时序 |
| `asset_manifest` | assets | 生成资产：路径、来源工具、场景关联 |
| `edit_decisions` | edit | 剪辑决策：入出点 |
| `render_report` | compose | 输出元数据（格式、分辨率、时长） |
| `publish_log` | publish | 平台发布条目及状态 |
| `review` | (any) | 审阅反馈与批准记录 |
| `cost_log` | (any) | 预算跟踪条目 |

---

## 预算治理

`CostTracker` 在整条流水线上强制执行支出控制。

### 生命周期

```
estimate(tool, operation, $) → entry_id
        |
reserve(entry_id)          # locks budget
        |
reconcile(entry_id, $)     # records actual spend
```

### 预算模式

| 模式 | 行为 |
|------|----------|
| `observe` | 跟踪成本，不强制 |
| `warn` | 超支时记录警告，仍允许执行 |
| `cap` | 拒绝超出剩余预算的操作 |

### 控制项
- **总预算**（默认：$10.00）
- **预留 holdback**（默认：10%）— 安全余量
- **单次操作审批阈值**（默认：$0.50）— 超过则暂停待批
- **新付费工具审批** — 任何付费工具首次使用需确认
- 按项目持久化到 `cost_log.json`

---

## 三层知识架构

```
Layer 3: .agents/skills/          External technology knowledge (47 skills)
         "How the technology works"    FFmpeg, ElevenLabs API, FLUX, Remotion, Three.js, etc.
              ^
              | agent_skills[] references
              |
Layer 2: skills/                  OpenMontage conventions
         "How this project uses the tech"  Pipeline integration, quality checklists, artifact mappings
              ^
              | stage skill references
              |
Layer 1: tools/ + pipeline_defs/  Executable capabilities + orchestration definitions
         "What exists and when to use it"  BaseTool contracts, pipeline manifests
```

每个工具的 `agent_skills[]` 将 Layer 1 链到 Layer 2 与 3。例如：
- `video_compose.agent_skills = ["remotion-best-practices", "remotion", "ffmpeg"]`
- `tts_selector.agent_skills = ["text-to-speech", "elevenlabs", "openai-docs"]`

---

## 配置

### config.yaml

```yaml
llm:
  provider: anthropic
  temperature: 0.7
  max_tokens: 4096

budget:
  mode: warn
  total_usd: 10.00
  reserve_pct: 0.10
  single_action_approval_usd: 0.50

checkpoint:
  policy: guided
  storage_dir: pipeline

output:
  default_format: mp4
  default_codec: libx264
  default_audio_codec: aac
  default_resolution: 1920x1080
  default_fps: 30
  default_crf: 23

paths:
  pipeline_dir: pipeline
  library_dir: library
  styles_dir: styles
  skills_dir: skills
  output_dir: output
```

所有配置通过 `lib/config_model.py` 中的 Pydantic 模型校验。

### 环境变量 (.env)

| 变量 | 使用者 | 用途 |
|----------|---------|---------|
| `ELEVENLABS_API_KEY` | elevenlabs_tts, music_gen | TTS、音乐、音效 |
| `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION` | azure_stt, azure_tts | Azure AI Speech 云端转写 + 神经 TTS（同一资源，双向） |
| `OPENAI_API_KEY` | openai_tts, openai_image | TTS 降级、GPT Image 2 |
| `XAI_API_KEY` | grok_image, grok_video | Grok 图像编辑/生成、Grok 视频生成 |
| `FAL_KEY` | flux_image, kling_video, veo_video, minimax_video, recraft_image | fal.ai 托管模型（FLUX、Veo、Kling、MiniMax、Recraft） |
| `KLING_API_KEY` | kling_official_video, kling_official_image, kling_tts, kling_avatar, kling_lip_sync | Kling 官方直连 API：视频、图像、TTS、虚拟形象、口型同步 |
| `KLING_API_BASE_URL` | kling_official_video, kling_official_image, kling_tts, kling_avatar, kling_lip_sync | 可选的官方 Kling API 端点覆盖 |
| `HEYGEN_API_KEY` | heygen_video | 多 Provider 视频生成 |
| `PEXELS_API_KEY` | pexels_image, pexels_video | 图库素材 |
| `PIXABAY_API_KEY` | pixabay_image, pixabay_video | 图库素材 |
| `GOOGLE_API_KEY` | google_imagen, google_tts | Google Imagen 图像、Google Cloud TTS |
| `RUNWAY_API_KEY` | runway_video | Runway Gen-3/Gen-4 直连 |
| `HIGGSFIELD_API_KEY` + `HIGGSFIELD_API_SECRET` | higgsfield_video | Higgsfield 多模型视频 |
| `MODAL_LTX2_ENDPOINT_URL` | ltx_video_modal | 自托管 LTX-2 |
| `VIDEO_GEN_LOCAL_ENABLED` | local video tools | 启用本地 GPU 生成 |
| `VIDEO_GEN_LOCAL_MODEL` | wan, hunyuan, ltx, cogvideo | 选择本地模型 |

Kling Official 支持仍落在既有 Provider 与 capability 模型内。
`kling_official_video` 与 `kling_official_image` 处理 Classic、Turbo、Omni
请求形态，而 Elements 与 Account Usage 位于 `tools/_kling/` 下作为
元素 ID 引用与低频账户诊断的内部辅助；它们不是独立的流水线阶段、选择器或生成资产能力。

Kling Official 仅在 OpenMontage 已有对应 capability 槽位处增加 Provider 工具：
`kling_tts` 对应 `tts`，以及 `kling_avatar`、`kling_lip_sync` 对应 `avatar`。
官方 Kling 音频特效与视频特效未注册为工具，因为当前流水线未定义稳定的
`sound_effects` 或 `video_effects` capability 路由。

---

## 视觉风格系统

`styles/` 中的风格 playbook 为流水线定义视觉语言：

- `clean-professional.yaml` — 企业、 polished 观感
- `flat-motion-graphics.yaml` — 现代扁平设计
- `minimalist-diagram.yaml` — 技术向、极简图示

由 `styles/playbook_loader.py` 加载。每条流水线在清单中声明 `compatible_playbooks`。对照 `schemas/styles/playbook.schema.json` 校验。

---

## 媒体配置（Media Profiles）

`lib/media_profiles.py` 中的平台专用渲染配置：

| 配置 | 分辨率 | 宽高比 | 备注 |
|---------|-----------|--------|-------|
| `youtube_landscape` | 1920x1080 | 16:9 | 标准 YouTube |
| `youtube_4k` | 3840x2160 | 16:9 | 4K YouTube |
| `youtube_shorts` | 1080x1920 | 9:16 | 最长 60s |
| `instagram_reels` | 1080x1920 | 9:16 | 最长 90s |
| `instagram_feed` | 1080x1080 | 1:1 | 方形 |
| `tiktok` | 1080x1920 | 9:16 | 竖屏 |
| `linkedin` | 1920x1080 | 16:9 | 横屏 |
| `cinematic` | 2560x1080 | 21:9 | 超宽 |

每项配置指定编解码器、音频编解码器、CRF、像素格式、最大文件大小、最大时长与字幕格式。`ffmpeg_output_args(profile)` 生成对应 FFmpeg 参数。

---

## 合成运行时

OpenMontage 具备多运行时合成层。三个引擎位于 `video_compose` 之后，在提案阶段选定并锁定于 `edit_decisions.render_runtime`：

### Remotion（基于 React）

`remotion-composer/` 中的独立 Node.js/React 子项目，使用 [Remotion](https://www.remotion.dev/)。

- **React 18** + **Remotion 4.0** + **TypeScript 5.3**
- 处理既有场景组件栈（`text_card`、`stat_card`、图表、字幕、`TalkingHead`、`CinematicRenderer`）
- 脚本：`start`（studio）、`build`（render）、`upgrade`

### HyperFrames（HTML/CSS/GSAP）

通过 `npx hyperframes` 使用（无需 monorepo checkout）。运行时要求：Node.js ≥ 22、FFmpeg、`npx`。

- 处理 kinetic typography、产品 promo、launch reel、website-to-video、registry 块与 SVG/GSAP 角色绑定
- 驱动：`tools/video/hyperframes_compose.py` 在 `projects/<name>/hyperframes/` 下物化工作区，然后执行 `lint → validate → render`
- Layer 3 技能 vendored 于 `.agents/skills/hyperframes*/`；Layer 2 指南于 `skills/core/hyperframes.md`
- `character-animation` 流水线以 HyperFrames 作为制作渲染包。浏览器预览仅为 QA/调试产物，非渲染路径。

### FFmpeg（降级 / 简单剪切）

- 无需合成时处理纯 concat/trim
- 亦作为事后操作处理字幕烧录

`video_compose` 读取 `edit_decisions.render_runtime`，经 `_render_via_hyperframes`、`_remotion_render` 或 `_render_via_ffmpeg` 分发。禁止静默切换运行时——所选运行时不可用时工具返回结构化 blocker。完整决策矩阵见 `AGENT_GUIDE.md` →「Composition Runtimes (Inside video_compose)」与 `skills/core/hyperframes.md`。

---

## 测试架构

```
tests/
├── contracts/              # Phase 0-3: tool contract validation, schema checks, registry tests
├── qa/                     # Integration tests: TTS, image gen, music, audio mix, video compose/stitch, E2E
├── eval/                   # Golden scenario replay harness for regression testing
├── pipelines/              # Pipeline-level tests
├── tools/                  # Individual tool tests
└── styles/                 # Style playbook tests
```

**契约测试**验证每个工具满足 `BaseTool` 契约：身份字段、Schema、依赖声明、继承关系。

**QA 测试**调用真实工具（真实 API/二进制）并检查输出质量。

**Eval  harness**（`tests/eval/replay_harness/`）以容差比较重放 golden 场景，用于随机性输出的回归测试。

---

## 系统依赖

**必需：**
- Python >= 3.10
- FFmpeg（约 15 个工具使用）

**可选（扩展能力）：**
- Node.js（Remotion composer）
- GPU + CUDA（本地视频/图像生成）
- Piper（离线 TTS）
- ManimCE（数学动画）
- Mermaid CLI（图示生成）

**Python 包：** pyyaml、pydantic、jsonschema、python-dotenv（核心）；pytest、pytest-asyncio（开发）；torch、torchvision、torchaudio（GPU）

---

## 关键设计决策

1. **无运行时编排器** — LLM Agent 读取 YAML + Markdown 驱动一切。系统可调试（读技能即可）且与模型无关。

2. **基于检查点的恢复** — 任一阶段失败可从最后检查点恢复。无需重跑已完成阶段。

3. **Schema 校验的工件** — 每个阶段输出写入检查点前对照 JSON Schema 校验。防止垃圾数据向下传播。

4. **预算为一等公民** — 执行前成本估算、预算预留与 reconciliation。Agent 不能静默超支。

5. **选择器模式优于硬编码 Provider** — 能力优雅降级。缺 API Key？选择器落到下一 Provider 或本地替代。

6. **智能在技能而非代码** — 创意决策、质量清单、审阅标准与 prompt 模板在 Markdown 技能中，不在 Python。Agent 行为可通过改文本文件调优，无需改代码。
