# OpenMontage - 共享项目上下文

本文档是项目架构与约定的唯一权威来源。各平台专用 Agent 文件（CLAUDE.md、CODEX.md、CURSOR.md、COPILOT.md）应指向此处，而非重复本内容。

## 身份

OpenMontage 是一个开源、由 AI 编排的视频生产平台。

## 架构：指令驱动（Agent 优先）

AI Agent 即智能核心。Python 仅用于工具与持久化。其余一切——编排、创意决策、审查、阶段流转——均存在于 Agent 遵循的指令中（YAML 清单 + Markdown 技能）。

```
Agent reads pipeline manifest (YAML) → reads stage director skill (MD)
→ uses tools (Python BaseTool) → self-reviews (meta skill)
→ checkpoints (Python utility) → presents to human for approval
```

**无 Python 编排器、无 Python 审查器、无 Python 处理器。** 由 Agent 驱动流水线。

## 权威来源

- **Agent 指南与契约：** `AGENT_GUIDE.md`（工具清单、流水线选择、阶段 Agent、协议）
- **技能索引：** `skills/INDEX.md`
- **工具注册表：** `tools/tool_registry.py`
- **流水线清单：** `pipeline_defs/`
- **制品模式：** `schemas/artifacts/`
- **风格手册：** `styles/*.yaml`（模式：`schemas/styles/playbook.schema.json`）
- **阶段导演技能：** `skills/pipelines/<pipeline>/<stage>-director.md`
- **元技能：** `skills/meta/*.md`（reviewer、checkpoint-protocol、skill-creator）
- **架构深度说明：** `docs/ARCHITECTURE.md`

## 知识架构（三层）

```
Layer 1: tools/tool_registry.py     → "What tools exist" (runtime capabilities, status, cost)
Layer 2: skills/                    → "How OpenMontage uses them" (project conventions)
Layer 3: .agents/skills/            → "How the technology works" (generic API rules, skills.sh)
```

各工具的 `agent_skills[]` 字段连接 Layer 1 → Layer 3。完整映射见 `skills/INDEX.md`。

## 关键模式

- **流水线状态机：** `idea -> script -> scene_plan -> assets -> edit -> compose -> publish`
- **指令驱动阶段：** 每个阶段有导演技能（MD），教 Agent 如何执行
- **流水线清单：** 声明式 YAML，定义阶段、技能、工具、审查重点、审批关卡
- **能力优先的工具设计：** 每个主要工具族应暴露选择器工具及明确的提供商工具
  - 示例：`tts_selector` + `elevenlabs_tts` / `google_tts` / `openai_tts` / `piper_tts`
  - 示例：`video_selector` + `heygen_video` / `wan_video` / `hunyuan_video` / `ltx_video_local` / `ltx_video_modal` / `cogvideo_video`
- **风格手册：** YAML 定义视觉语言、排版、动效、音频、资产生成约束
- **制品为权威数据（canonical）：** `brief`、`script`、`scene_plan`、`asset_manifest`、`edit_decisions`、`render_report`、`publish_log`
- **每个工具继承自 `tools/base_tool.py`**（ToolContract）
- **检查点策略** 位于流水线清单（每阶段 `human_approval_default`）+ `skills/meta/checkpoint-protocol.md`
- **Reviewer** 为元技能（`skills/meta/reviewer.md`），顾问式，最多 2 轮
- **成本追踪器**（`tools/cost_tracker.py`）管理预算：estimate -> reserve -> reconcile
- **权威制品** 对照 `schemas/artifacts/` 中的 JSON 模式校验

## 关键文件

| 文件 | 用途 |
|------|------|
| `config.yaml` | 全局配置 |
| `lib/config_model.py` | 运行时配置加载器（Pydantic） |
| `lib/checkpoint.py` | 检查点写入/读取 |
| `lib/pipeline_loader.py` | 流水线清单加载器及辅助函数 |
| `lib/media_profiles.py` | 平台专用渲染配置 |
| `styles/playbook_loader.py` | 风格手册加载器、校验器及设计智能（色彩/字体/无障碍） |
| `tools/base_tool.py` | ToolContract 基类 |
| `tools/tool_registry.py` | 工具发现与报告 |
| `tools/cost_tracker.py` | 预算治理 |
| `tools/video/video_stitch.py` | 多片段组装（拼接、空间、校验、预览） |
| `tools/video/video_compose.py` | 运行时感知合成编排器——根据 `edit_decisions.render_runtime` 路由至 Remotion / HyperFrames / FFmpeg |
| `tools/video/hyperframes_compose.py` | HyperFrames 运行时——模板化工作区物化及 authored-workspace 统一 `check`/`render`、FFmpeg 底线检查 |
| `tools/graphics/threejs_world.py` | 本地语义 3D 世界创作，含显式 blockout/生产保真度层级、区域感知地形、诊断及 HyperFrames atelier 工作区 |
| `tools/graphics/threejs_asset_catalog.py` | CC0 GLTF/GLB 目录获取、清单与溯源，用于生产保真度世界构建 |
| `tools/graphics/atlas_3d.py` | Atlas Cloud Tripo H3.1 文本转 3D，生成独特纹理/PBR GLB 资产 |
| `tools/graphics/fal_3d.py` | fal.ai Hunyuan 3D 与 SAM 3D 路由，用于图像条件及多对象 GLB 生成 |
| `tools/graphics/blender_world.py` | Blender 4.5 LTS 生产世界组装、地形、光照、相机及 Eevee Next 渲染 |
| `tools/character/character_animation.py` | 本地角色动画工具——角色规格、SVG 绑定方案、姿势库、动作时间线、HyperFrames 包及 QA 报告 |
| `lib/hyperframes_style_bridge.py` | Playbook → CSS 自定义属性 + HyperFrames 工作区 `DESIGN.md` 桥接 |
| `remotion-composer/src/components/` | 8 个 Remotion 组件（TextCard、StatCard、ProgressBar、CalloutBox、ComparisonCard + charts/） |
| `.agents/skills/hyperframes*/` | 内嵌 HyperFrames Layer 3 技能（创作契约、CLI、registry、website-to-video） |
| `.agents/skills/threejs-world-generation/` | Layer 3 由粗到细的语义世界构建及渲染引导 refinement 工作流 |
| `skills/core/hyperframes.md` | Layer 2——OpenMontage 何时选择 HyperFrames 与 Remotion、制品 → 工作区映射 |
| `schemas/styles/playbook.schema.json` | Playbook 模式 v2，含设计令牌（chart_palette、scale_system、weight_matrix、color_rules） |
| `tests/qa/` | 逐工具输出检查的质量验证测试脚本 |

## 可用流水线

| 流水线 | 清单 | 类型 |
|----------|----------|------|
| `talking-head` | `pipeline_defs/talking-head.yaml` | 基于实拍素材 |
| `animated-explainer` | `pipeline_defs/animated-explainer.yaml` | AI 生成 |
| `screen-demo` | `pipeline_defs/screen-demo.yaml` | 屏幕录制 |
| `clip-factory` | `pipeline_defs/clip-factory.yaml` | 短视频批量提取 |
| `podcast-repurpose` | `pipeline_defs/podcast-repurpose.yaml` | 播客再利用 |
| `cinematic` | `pipeline_defs/cinematic.yaml` | 电影感剪辑 |
| `animation` | `pipeline_defs/animation.yaml` | 动画优先 |
| `character-animation` | `pipeline_defs/character-animation.yaml` | 本地绑定角色动画 |
| `hybrid` | `pipeline_defs/hybrid.yaml` | 源素材加辅助混合 |
| `avatar-spokesperson` | `pipeline_defs/avatar-spokesperson.yaml` | 虚拟形象出镜 |
| `localization-dub` | `pipeline_defs/localization-dub.yaml` | 本地化与配音 |
| `framework-smoke` | `pipeline_defs/framework-smoke.yaml` | 测试 harness |

## 构建新流水线时

1. 在 `pipeline_defs/` 创建 YAML 清单（由 `pipeline_manifest.schema.json` 校验）
2. 在 `skills/pipelines/<pipeline-name>/` 创建阶段导演技能（7 个技能：从 idea 到 publish）
3. 在清单中引用元技能（reviewer、checkpoint-protocol）
4. 向清单添加兼容的风格手册
5. 在 `tests/contracts/` 添加契约测试

## 构建新工具时

1. 继承 `tools/base_tool.py` 的 `BaseTool`
2. 将工具放入正确的能力包（`tools/audio/`、`tools/video/`、`tools/enhancement/`、`tools/analysis/`、`tools/graphics/`、`tools/avatar/`、`tools/subtitle/`）
3. 优先采用选择器加提供商模式：
   - 一个能力路由工具，便于 Agent 使用
   - 每个真实提供商/运行时路径一个具体工具
4. 设置全部契约字段（name、version、tier、capability、provider、supports、fallback_tools、agent_skills 等）
5. 实现返回 `ToolResult` 的 `execute()`
6. 通过 `tools/tool_registry.py` 发现；不要依赖临时 import
7. 若工具有复杂 I/O，在 `schemas/tools/` 添加 JSON 模式
8. 仅在运行时路径正确后再添加测试
