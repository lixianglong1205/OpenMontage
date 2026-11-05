# OpenMontage — 技能索引

> 完整的 Agent 入门指南见项目根目录 [`AGENT_GUIDE.md`](../AGENT_GUIDE.md)。

本文件列出所有可用的 Layer 2 技能，并说明三层知识架构。

## 知识架构

```
Layer 1: tools/tool_registry.py          "有哪些工具、能做什么"
         tools/base_tool.py               每个工具声明：capabilities、tier、status、
                                          dependencies、cost，以及 agent_skills[]

         ↓ agent_skills[] 指向 ↓

Layer 2: skills/                          "OpenMontage 如何使用这些工具"
         项目特定约定：                     流水线集成、产物映射、
         {core,creative,meta,pipelines}/   增强链顺序、质量检查清单

         ↓ 引用底层技术于 ↓

Layer 3: .agents/skills/                  "技术本身如何工作"
         来自 skills.sh 的通用 API 知识   正确 import 路径、代码模式、
         （已安装 47 个技能）              约束与参数 — 与技术栈无关
```

**Agent 如何使用：**
1. 编排器查询 Layer 1（`tool_registry.support_envelope()`）以了解可用能力
2. 每个工具的 `agent_skills[]` 字段指向其依赖的 Layer 3 技能
3. Layer 2 技能（本目录）教 Agent OpenMontage 特定约定
4. Layer 3 技能（`.agents/skills/`）提供通用 API 知识，按需加载

## 能力族与工具发现

每个工具声明 `capability`（做什么）和 `provider`（由谁/什么驱动）。注册表按 capability 分组，便于 Agent 发现某类任务的全部选项。

### 选择器 / Provider 模式

对于有多 provider 的能力族（TTS、视频生成），架构采用：
- **选择器工具**（`tts_selector`、`video_selector`、`image_selector`）— 根据需求、API Key 可用性与成本路由到最佳可用 provider。选择器从注册表自动发现 provider。用户未指定 provider 时，Agent 应默认使用选择器。
- **Provider 工具** — 直接调用特定 provider。用户明确要求某 provider，或选择器路由不合适时使用。

### 能力族参考

**不要维护硬编码工具列表。** 注册表是唯一真相来源。运行时查询：

```bash
python -c "from tools.tool_registry import registry; import json; registry.discover(); print(json.dumps(registry.capability_catalog(), indent=2))"
```

在输出中关注这些能力族：

| Capability | Selector | Discovery |
|---|---|---|
| `tts` | `tts_selector` | 自动发现所有 `capability="tts"` 的工具 |
| `video_generation` | `video_selector` | 自动发现所有 `capability="video_generation"` 的工具 |
| `image_generation` | `image_selector` | 自动发现所有 `capability="image_generation"` 的工具 |
| `audio_processing` | — | 基于 FFmpeg 的本地工具 |
| `enhancement` | — | 混合 provider |
| `analysis` | — | 混合 provider |
| `character_animation` | — | 本地角色规格、SVG 绑定、姿势库、动作时间线、预览与 QA |
| `3d_world_generation` | — | 本地语义地形、程序化散布、显式地标、诊断，以及 HyperFrames/Three.js 飞越工作区 |
| `3d_asset_acquisition` | — | 权利安全的本地 GLTF/GLB 目录与溯源 |
| `3d_asset_generation` | — | Atlas/fal 纹理网格生成与重建，用于独特场景资产 |
| `3d_world_rendering` | — | Blender 组装与详细世界的生产级渲染 |
| `graphics` | — | 本地渲染工具 |
| `music_library` | — | 发现用户提供的本地音轨 |
| `music_search` | — | 发现免版税搜索/下载 provider |
| `music_generation` | — | 发现付费/本地生成 provider |
| `subtitle` | — | 纯 Python |
| `avatar` | — | 本地 GPU 模型 |
| `video_post` | — | 基于 FFmpeg 的本地工具 |

### 添加新工具

1. 将工具放在正确的 capability 文件夹（或在 `tools/` 下新建）
2. 在类定义中设置 `capability` 与 `provider`
3. 若加入多 provider 能力族，现有选择器会自动发现
4. 通过 `agent_skills[]` 挂载相关 Layer 2 与 Layer 3 技能
5. 注册表自动发现工具 — 无需手动注册
6. **无需更新其他文件** — 选择器、清单与说明均从注册表派生

## 核心技能

| Skill | File | Trigger | Agent Skills (Layer 3) |
|-------|------|---------|----------------------|
| FFmpeg | `core/ffmpeg.md` | 视频编码、滤镜、合成 | `ffmpeg`, `video-toolkit` |
| Remotion | `core/remotion.md` | 基于 React 的合成，Phase 3+ | `remotion-best-practices`, `remotion` |
| HyperFrames | `core/hyperframes.md` | HTML/CSS/GSAP 合成运行时 — kinetic typography、music-to-video、产品宣传片、网站捕获。Vendored v0.7.17 (2026-06-27)。 | `hyperframes` (router) → `hyperframes-core` (contract), `hyperframes-creative` (palette/type/narration), `hyperframes-media` (TTS/BGM/SFX/captions), `hyperframes-animation` (all motion), `hyperframes-cli`, `hyperframes-registry`, `media-use`, `motion-graphics`, `music-to-video` (beats-driven), `website-to-video`, `remotion-to-hyperframes` (migration), `gsap-core`, `gsap-timeline` |
| WhisperX | `core/whisperx.md` | 带词级时间戳的转写 — 默认 STT（离线、免费） | `speech-to-text` |
| Azure STT | (tool: `azure_stt`) | 可选云端语音转文字，词级时间戳 — 设置 `AZURE_SPEECH_KEY` 时优先 | `azure-speech-to-text` |
| Azure TTS | (tool: `azure_tts`) | 可选云端神经旁白（SSML 韵律、express-as 风格）— 与 `azure_stt` 共用 Speech key | `azure-text-to-speech` |
| Subtitle Sync | `core/subtitle-sync.md` | 字幕时序与对齐 | `remotion-best-practices` |
| Color Grading | `core/color-grading.md` | FFmpeg 色彩配置、LUT 工作流、无障碍 | `ffmpeg` |

## 创意技能

| Skill | File | Trigger | Agent Skills (Layer 3) |
|-------|------|---------|----------------------|
| Video Editing | `creative/video-editing.md` | 剪辑决策、节奏、韵律 | `ffmpeg`, `video-toolkit` |
| Enhancement Strategy | `creative/enhancement-strategy.md` | 叠加层位置与密度 | `ffmpeg` |
| Data Visualization | `creative/data-visualization.md` | 图表类型选择、动画、标签位置 | `d3-viz`, `remotion-best-practices` |
| Video Stitching | `creative/video-stitching.md` | 多片段组装、AI 片段链接、空间合成 | `ffmpeg`, `video-toolkit` |
| Video Gen Prompting | `creative/video-gen-prompting.md` | 通用视频生成提示词词汇；**规范五维规格**（Subject / Motion / Scene / Spatial / Camera）；约 200 个电影摄影基元 | `ai-video-gen`, `ltx2`, `create-video` |
| ↳ Seedance Prompting | `creative/prompting/seedance-prompting.md` | **首选高级默认。** Seedance 2.0 八组件结构、多镜头、口型同步、参考图生视频 | `seedance-2-0`, `ai-video-gen` |
| ↳ Grok Prompting | `creative/prompting/grok-prompting.md` | Grok 图像/视频提示、编辑流程、参考图视频 | `grok-media` |
| ↳ Sora Prompting | `creative/prompting/sora-prompting.md` | Sora 2 结构化模板、高级字段 | `ai-video-gen` |
| ↳ VEO Prompting | `creative/prompting/veo-prompting.md` | VEO 3.1 十四组件结构、艺术流派 | `ai-video-gen` |
| ↳ LTX Prompting | `creative/prompting/ltx-prompting.md` | LTX-2 六要素结构、音频提示 | `ltx2` |
| ↳ HunyuanVideo Prompting | `creative/prompting/hunyuan-prompting.md` | HunyuanVideo 公式、I2V 最佳实践 | — |
| Storytelling | `creative/storytelling.md` | 叙事结构、钩子、节奏、Mayer 原则 | — |
| Sound Design | `creative/sound-design.md` | 音频闪避、LUFS 目标、SFX 时序、AI TTS 混音 | `elevenlabs` |
| Typography | `creative/typography.md` | 字体选择、字号、安全区、字幕样式 | — |
| ManimCE Usage | `creative/manim-usage.md` | 场景构图、动画时序、色彩运用 | `manimce-best-practices` |
| Image Gen Usage | `creative/image-gen-usage.md` | 提示一致性、主参考图、批量策略 | `flux-best-practices`, `bfl-api` |
| Image Provider Usage | `creative/image-provider-usage.md` | Provider 选择（FLUX/Grok/OpenAI/Recraft/stock）、成本质量权衡 | `flux-best-practices`, `bfl-api`, `grok-media` |
| 3D World Generation | `creative/3d-world-generation.md` | 语义世界规划、资产采购/生成、Blender 组装与保真度审查 | `3d-asset-generation`, `threejs-world-generation` |
| B-Roll Planning | `creative/broll-planning.md` | 素材库 vs 生成决策、查询构造、素材评估 | — |
| Stock Sourcing Usage | `creative/stock-sourcing-usage.md` | Pexels/Pixabay 用法、参数、许可、集成 | — |
| Scene Detect Usage | `creative/scene-detect-usage.md` | 阈值调节、算法选择、内容预设 | — |
| Diagram Gen Usage | `creative/diagram-gen-usage.md` | 复杂度上限、渐进构建、主题 | `beautiful-mermaid` |
| Music Gen Usage | `creative/music-gen-usage.md` | BPM 选择、提示工程、时长匹配 | `music`, `elevenlabs` |
| Background Removal | `creative/bg-remove-usage.md` | 模型选择、alpha matting、合成工作流 | — |
| Upscaling | `creative/upscale-usage.md` | 放大倍数、模型选择、人脸感知放大 | — |
| Face Restoration | `creative/face-restore-usage.md` | CodeFormer/GFPGAN 选择、保真度调节、与 face_enhance 对比 | — |
| Lip Sync | `creative/lip-sync-usage.md` | Wav2Lip 模型选择、配音工作流、输入要求 | `faceswap` |
| Talking Head Gen | `creative/talking-head-gen-usage.md` | SadTalker/MuseTalk、照片生视频、表情调节 | `avatar-video` |
| Video Understanding | `creative/video-understand-usage.md` | 视觉 QA、质量门禁、场景分类 | `video-understand` |

## 流水线类型技能

流水线类型技能为特定视频格式提供制作指导，与动画讲解或 talking-head 流水线相互独立。

| Skill | File | When to Use |
|-------|------|-------------|
| Short-Form | `creative/short-form.md` | TikTok、Reels、Shorts — 竖屏 9:16，60 秒内 |
| Long-Form | `creative/long-form.md` | YouTube 10+ 分钟 — 章节、留存、片尾画面 |
| Screen Recording | `creative/screen-recording.md` | 代码讲解、教程、软件演示 |
| Animation Pipeline | `creative/animation-pipeline.md` | 动态图形、缓动、转场、构图 |
| 3D World Generation | `creative/3d-world-generation.md` | 连续 Three.js 地形世界：语义区域、显式 blockout/生产档位、许可 GLTF/PBR 资产、诊断与确定性相机路径 |
| Character Animation Pipeline | `pipelines/character-animation/` | 本地绑定卡通角色、姿势库、动作时间线、SVG/Canvas/Remotion/HyperFrames 渲染 |
| Cinematic | `creative/cinematic.md` | 宽银幕、电影节奏、分层音频、调色 |

## 流水线阶段导演技能

阶段导演技能教 Agent 如何执行各流水线阶段。每个技能是详细的 Markdown 文件，含流程步骤、质量量表与自评标准。

### 动画讲解流水线（`pipelines/explainer/`）— v2.0

| Skill | File | Stage | Key Capabilities |
|-------|------|-------|-----------------|
| **Executive Producer** | `pipelines/explainer/executive-producer.md` | `all` | **8 阶段串行编排、质量门禁、跨阶段检查、退回** |
| **Research Director** | `pipelines/explainer/research-director.md` | `research` | **网络调研方法、5 批搜索、格局/趋势/数据/受众/专家分析** |
| **Proposal Director** | `pipelines/explainer/proposal-director.md` | `proposal` | **基于调研的概念选项、制作计划、成本估算、审批门禁** |
| Script Director | `pipelines/explainer/script-director.md` | `script` | 叙事架构、时序、增强提示、调研整合 |
| Scene Director | `pipelines/explainer/scene-director.md` | `scene_plan` | 视觉规划、技法库、可行性 |
| Asset Director | `pipelines/explainer/asset-director.md` | `assets` | TTS、图像生成、图表生成、音乐、预算 |
| Edit Director | `pipelines/explainer/edit-director.md` | `edit` | 时间线组装、字幕、音频闪避 |
| Compose Director | `pipelines/explainer/compose-director.md` | `compose` | FFmpeg/Remotion 渲染、音频混音 |
| Publish Director | `pipelines/explainer/publish-director.md` | `publish` | SEO 元数据、章节、导出打包 |

> **注意：** 旧版 `idea-director.md` 仍作参考，但在 v2.0 中已被 research + proposal 两阶段流程取代。Talking-head 流水线仍使用各自的 `idea-director`。

### Talking Head 流水线（`pipelines/talking-head/`）

| Skill | File | Stage | Key Capabilities |
|-------|------|-------|-----------------|
| Idea Director | `pipelines/talking-head/idea-director.md` | `idea` | 素材检视、内容评估 |
| Script Director | `pipelines/talking-head/script-director.md` | `script` | 转写、段落切分 |
| Scene Director | `pipelines/talking-head/scene-director.md` | `scene_plan` | 增强规划、叠加层位置 |
| Asset Director | `pipelines/talking-head/asset-director.md` | `assets` | 字幕生成、音频提取 |
| Edit Director | `pipelines/talking-head/edit-director.md` | `edit` | 剪辑组装、字幕配置 |
| Compose Director | `pipelines/talking-head/compose-director.md` | `compose` | 增强链、渲染 |
| Publish Director | `pipelines/talking-head/publish-director.md` | `publish` | 元数据、导出打包 |

### 屏幕演示流水线（`pipelines/screen-demo/`）— v2.0

| Skill | File | Stage | Key Capabilities |
|-------|------|-------|-----------------|
| **Executive Producer** | `pipelines/screen-demo/executive-producer.md` | `all` | **7 阶段串行编排、可读性门禁、音频清晰度、节奏检查** |
| Idea Director | `pipelines/screen-demo/idea-director.md` | `idea` | 工作流范围、UI 密度评估、输出形态选择 |
| Script Director | `pipelines/screen-demo/script-director.md` | `script` | 动作映射、程序化旁白、速度规划 |
| Scene Director | `pipelines/screen-demo/scene-director.md` | `scene_plan` | 裁剪规划、标注克制、宽高比可行性 |
| Asset Director | `pipelines/screen-demo/asset-director.md` | `assets` | 字幕优先资产包、音频清理、可复用叠加层 |
| Edit Director | `pipelines/screen-demo/edit-director.md` | `edit` | 紧凑时间线规划、速度备注、字幕区域控制 |
| Compose Director | `pipelines/screen-demo/compose-director.md` | `compose` | 可读性优先渲染、清晰屏幕输出、验证 |
| Publish Director | `pipelines/screen-demo/publish-director.md` | `publish` | 可搜索元数据、章节打包、缩略图概念 |

### 片段工厂流水线（`pipelines/clip-factory/`）— v2.0

| Skill | File | Stage | Key Capabilities |
|-------|------|-------|-----------------|
| **Executive Producer** | `pipelines/clip-factory/executive-producer.md` | `all` | **7 阶段串行编排、片段选择门禁、批次一致性、钩子位置** |
| Idea Director | `pipelines/clip-factory/idea-director.md` | `idea` | 批次策略、片段族、产出规划 |
| Script Director | `pipelines/clip-factory/script-director.md` | `script` | 转写挖掘、排序、独立成片验证 |
| Scene Director | `pipelines/clip-factory/scene-director.md` | `scene_plan` | 平台画幅、安全区、裁剪可行性规划 |
| Asset Director | `pipelines/clip-factory/asset-director.md` | `assets` | 共享品牌包、重基准字幕、批次音频一致性 |
| Edit Director | `pipelines/clip-factory/edit-director.md` | `edit` | 钩子优先微剪辑、系列一致性 |
| Compose Director | `pipelines/clip-factory/compose-director.md` | `compose` | 多任务渲染、批次容错、逐输出验证 |
| Publish Director | `pipelines/clip-factory/publish-director.md` | `publish` | 发布顺序、平台文案、批次目录 |

### 播客再利用流水线（`pipelines/podcast-repurpose/`）— v2.0

| Skill | File | Stage | Key Capabilities |
|-------|------|-------|-----------------|
| **Executive Producer** | `pipelines/podcast-repurpose/executive-producer.md` | `all` | **7 阶段串行编排、音频保真门禁、片段质量、多交付物** |
| Idea Director | `pipelines/podcast-repurpose/idea-director.md` | `idea` | 按源模式划分交付物组合、务实的长片规划 |
| Script Director | `pipelines/podcast-repurpose/script-director.md` | `script` | 说话人分离转写真相、高光排序、章节映射 |
| Scene Director | `pipelines/podcast-repurpose/scene-director.md` | `scene_plan` | 忠实于源的视觉处理、audiogram vs 引语 vs 伴生内容规划 |
| Asset Director | `pipelines/podcast-repurpose/asset-director.md` | `assets` | 字幕优先打包、说话人资产、可选主题图 |
| Edit Director | `pipelines/podcast-repurpose/edit-director.md` | `edit` | 钩子导向播客片段、引语停留时长、伴生内容简洁性 |
| Compose Director | `pipelines/podcast-repurpose/compose-director.md` | `compose` | 音频优先渲染、交付物优先级 |
| Publish Director | `pipelines/podcast-repurpose/publish-director.md` | `publish` | 单集交叉链接、嘉宾署名、错峰发布逻辑 |

### 电影感流水线（`pipelines/cinematic/`）— v2.0

| Skill | File | Stage | Key Capabilities |
|-------|------|-------|-----------------|
| **Executive Producer** | `pipelines/cinematic/executive-producer.md` | `all` | **7 阶段串行编排、情感节奏门禁、色彩一致性、音频动态** |
| Idea Director | `pipelines/cinematic/idea-director.md` | `idea` | 情感弧选择、源素材真相、交付形态规划 |
| Script Director | `pipelines/cinematic/script-director.md` | `script` | 节拍映射、对白选段、标题卡克制 |
| Scene Director | `pipelines/cinematic/scene-director.md` | `scene_plan` | 英雄帧规划、揭示结构、转场上限 |
| Asset Director | `pipelines/cinematic/asset-director.md` | `assets` | 源选段、辅助插入克制、音乐/环境声规划 |
| Edit Director | `pipelines/cinematic/edit-director.md` | `edit` | 情感优先节奏、揭示时序、音频驱动韵律 |
| Compose Director | `pipelines/cinematic/compose-director.md` | `compose` | 调色与混音成片、画幅处理判断 |
| Publish Director | `pipelines/cinematic/publish-director.md` | `publish` | 主片 vs 预告包装、海报帧概念 |

### 动画流水线（`pipelines/animation/`）— v2.0

| Skill | File | Stage | Key Capabilities |
|-------|------|-------|-----------------|
| **Executive Producer** | `pipelines/animation/executive-producer.md` | `all` | **8 阶段串行编排、质量门禁、运动一致性、数学准确性检查** |
| **Research Director** | `pipelines/animation/research-director.md` | `research` | **主题 + 动画技法调研、视觉参考扫描、模式导向角度** |
| **Proposal Director** | `pipelines/animation/proposal-director.md` | `proposal` | **动画模式选择（Manim/Remotion/AI/图表）、复用策略、成本估算、审批门禁** |
| Script Director | `pipelines/animation/script-director.md` | `script` | 动画就绪节拍、文字克制、调研整合、模式感知写作 |
| Scene Director | `pipelines/animation/scene-director.md` | `scene_plan` | 动画小样规划、转场系统、工具路径映射 |
| Asset Director | `pipelines/animation/asset-director.md` | `assets` | 确定性资产选择、可复用母题、可行性真相 |
| Edit Director | `pipelines/animation/edit-director.md` | `edit` | 停留时序、交错规则、可读运动规划 |
| Compose Director | `pipelines/animation/compose-director.md` | `compose` | 清晰渲染输出、时序完整性、安全区检查 |
| Publish Director | `pipelines/animation/publish-director.md` | `publish` | 动画模式包装、缩略图系统对齐 |

> **注意：** 旧版 `idea-director.md` 仍作参考，但在 v2.0 中已被 research + proposal 两阶段流程取代。

### 混合流水线（`pipelines/hybrid/`）— v2.0

| Skill | File | Stage | Key Capabilities |
|-------|------|-------|-----------------|
| **Executive Producer** | `pipelines/hybrid/executive-producer.md` | `all` | **7 阶段串行编排、源/辅助平衡门禁、叠加密度、连贯性** |
| Idea Director | `pipelines/hybrid/idea-director.md` | `idea` | 锚定媒介选择、辅助层规划、降级可见性 |
| Script Director | `pipelines/hybrid/script-director.md` | `script` | 源 vs 辅助节拍映射、对白保留、辅助合理性 |
| Scene Director | `pipelines/hybrid/scene-director.md` | `scene_plan` | 源优先版式规则、叠加密度控制、变体安全规划 |
| Asset Director | `pipelines/hybrid/asset-director.md` | `assets` | 共享辅助包、源 vs 生成资产追踪 |
| Edit Director | `pipelines/hybrid/edit-director.md` | `edit` | 锚定剪辑优先工作流、分层辅助时序、可读变体 |
| Compose Director | `pipelines/hybrid/compose-director.md` | `compose` | 源/辅助平衡检查、变体验证、连贯混音 |
| Publish Director | `pipelines/hybrid/publish-director.md` | `publish` | 主片 vs 衍生包装、源混合元数据 |

### 虚拟代言人流水线（`pipelines/avatar-spokesperson/`）— v2.0

| Skill | File | Stage | Key Capabilities |
|-------|------|-------|-----------------|
| **Executive Producer** | `pipelines/avatar-spokesperson/executive-producer.md` | `all` | **7 阶段串行编排、口型同步质量门禁、 presenter 构图、CTA 落点** |
| Idea Director | `pipelines/avatar-spokesperson/idea-director.md` | `idea` | Avatar 路径分类、CTA 范围、能力真相 |
| Script Director | `pipelines/avatar-spokesperson/script-director.md` | `script` | 口播文案塑形、场景安全节奏、文字克制 |
| Scene Director | `pipelines/avatar-spokesperson/scene-director.md` | `scene_plan` | Presenter 版式、背景克制、变体真实感 |
| Asset Director | `pipelines/avatar-spokesperson/asset-director.md` | `assets` | Avatar 路径锁定、旁白解析、最小辅助包 |
| Edit Director | `pipelines/avatar-spokesperson/edit-director.md` | `edit` | Presenter 优先剪辑规划、叠加时序、CTA 落点 |
| Compose Director | `pipelines/avatar-spokesperson/compose-director.md` | `compose` | 口型同步验证、字幕安全构图、干净渲染检查 |
| Publish Director | `pipelines/avatar-spokesperson/publish-director.md` | `publish` | 受众导向包装、 presenter 优先缩略图概念 |

### 本地化配音流水线（`pipelines/localization-dub/`）— v2.0

| Skill | File | Stage | Key Capabilities |
|-------|------|-------|-----------------|
| **Executive Producer** | `pipelines/localization-dub/executive-producer.md` | `all` | **7 阶段串行编排、翻译准确性门禁、时序保持、逐语言 QA** |
| Idea Director | `pipelines/localization-dub/idea-director.md` | `idea` | 范围定义、语言区域规划、术语表与审校捕获 |
| Script Director | `pipelines/localization-dub/script-director.md` | `script` | 转写真相、译稿打包、术语保留 |
| Scene Director | `pipelines/localization-dub/scene-director.md` | `scene_plan` | 配音模式选择、时序风险映射、屏幕文字规划 |
| Asset Director | `pipelines/localization-dub/asset-director.md` | `assets` | 字幕优先本地化包、配音音频生成、可选口型同步 |
| Edit Director | `pipelines/localization-dub/edit-director.md` | `edit` | 逐语言时间线、覆盖规划、时序调整 |
| Compose Director | `pipelines/localization-dub/compose-director.md` | `compose` | 逐语言渲染、字幕适配检查、输出标注 |
| Publish Director | `pipelines/localization-dub/publish-director.md` | `publish` | 语言区域打包、元数据精度、QA 备注保留 |

## 元技能

适用于所有流水线的横切技能：

| Skill | File | Purpose |
|-------|------|---------|
| Onboarding | `meta/onboarding.md` | 首次交互问候、能力发现、入门提示 |
| Reviewer | `meta/reviewer.md` | 每阶段后的自审协议 |
| Checkpoint Protocol | `meta/checkpoint-protocol.md` | 何时/如何 checkpoint 并请求人工审批 |
| Skill Creator | `meta/skill-creator.md` | 流水线运行中动态创建新技能 |
| Animation Runtime Selector | `meta/animation-runtime-selector.md` | 按场景选择渲染运行时与动画库 |
| Taste Direction | `meta/taste-direction.md` | 将 brief 转为品味拨盘、反模式与参考策略，用于 proposal/playbook/atelier 工作 |
| Bespoke Composition (Atelier) | `meta/bespoke-composition.md` | 从零手写合成（hero 级作品）— 无库存场景类型；路由 art-direction → motion principles → engine mechanics → atelier render |

## 风格 Playbook

风格 playbook（`styles/*.yaml`）定义视觉语言、版式、motion、audio 与资产生成约束。对照 `schemas/styles/playbook.schema.json` 校验。

| Playbook | Category | Mood | Best For |
|----------|----------|------|----------|
| `clean-professional` | motion-graphics | polished, trustworthy | 企业、教育、SaaS |
| `premium-minimalist` | minimalist | calm, editorial | 投资者更新、专家讲解、产品叙事 |
| `flat-motion-graphics` | motion-graphics | energetic, bold | 社交媒体、TikTok、初创 |
| `minimalist-diagram` | whiteboard | focused, technical | 技术深度、架构 |

通过 `styles/playbook_loader.py` 加载：`load_playbook("clean-professional")`

## 已安装的 Agent 技能（Layer 3）

所有 agent 技能位于 `.agents/skills/`，通过 `npx skills add` 管理。
Claude Code 通过 `.claude/skills/` 中的符号链接访问。

| Category | Installed Skills | Source |
|----------|-----------------|--------|
| **Video Composition** | `remotion-best-practices`, `remotion`, `hyperframes` (router), `hyperframes-core`, `hyperframes-creative`, `hyperframes-media`, `hyperframes-animation`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `motion-graphics`, `music-to-video`, `remotion-to-hyperframes`, `website-to-video` | `remotion-dev/skills`, `digitalsamba/claude-code-video-toolkit`, `heygen-com/hyperframes` (vendored v0.7.17, see `.agents/skills/hyperframes/PROVENANCE.md`) |
| **Video Processing** | `ffmpeg`, `video-toolkit` | `digitalsamba/claude-code-video-toolkit` |
| **TTS & Audio** | `text-to-speech`, `speech-to-text` (whisper, default STT), `azure-speech-to-text` (optional cloud STT), `music`, `sound-effects`, `elevenlabs`, `fish-audio-tts`, `agents`, `setup-api-key` | `elevenlabs/skills`, `digitalsamba/claude-code-video-toolkit`, local OpenMontage skill |
| **Image Generation** | `flux-best-practices`, `bfl-api`, `grok-media` | `black-forest-labs/skills`, local OpenMontage skill |
| **Math Animation** | `manimce-best-practices`, `manimgl-best-practices`, `manim-composer` | `adithya-s-k/manim_skill` |
| **3D Graphics** | `threejs-world-generation` (OpenMontage semantic-world workflow), `threejs-animation`, `threejs-fundamentals`, `threejs-geometry`, `threejs-interaction`, `threejs-lighting`, `threejs-loaders`, `threejs-materials`, `threejs-postprocessing`, `threejs-shaders`, `threejs-textures` | Local OpenMontage skill + `cloudai-x/threejs-skills` |
| **Diagrams** | `beautiful-mermaid`, `d3-viz` | `intellectronica/agent-skills`, `davila7/claude-code-templates` |
| **Animation** | `framer-motion`, `lottie-bodymovin` | `pproenca/dot-skills`, `dylantarre/animation-principles` |
| **Design** | `tailwind-design-system`, `web-design-guidelines`, `vercel-react-best-practices`, `vercel-composition-patterns` | `wshobson/agents`, `vercel-labs/agent-skills` |
| **AI Video (HeyGen)** | `heygen`, `avatar-video`, `create-video`, `faceswap`, `ai-video-gen`, `video-download`, `video-edit`, `video-translate`, `video-understand`, `visual-style` | `heygen-com/skills` |
| **AI Video/Image/TTS/Avatar (Kling Official)** | `kling-official` - official direct API auth, Classic/Turbo/Omni task protocols, multi-reference Omni syntax, internal Elements/Account Usage helpers, callback notes, TTS voice parameters, avatar/lip-sync face selection, error handling, and cost governance for `kling_official_video` / `kling_official_image` / `kling_tts` / `kling_avatar` / `kling_lip_sync` | Local OpenMontage skill |
| **AI Video (Premium)** | `seedance-2-0` — preferred premium default (cinematic, trailer, multi-shot, lip-sync, synced audio); accessed via `seedance_video` (fal.ai) or `heygen_video` Avatar Shots; `seedance-2-5` — 4–30 s clips, 50 multimodal references, prompt contract (section order, `Hard cut` breakdown, continuity locks, asset method) | Local OpenMontage skill |
| **Infrastructure** | `acestep`, `ltx2`, `playwright-recording` | `digitalsamba/claude-code-video-toolkit` |
