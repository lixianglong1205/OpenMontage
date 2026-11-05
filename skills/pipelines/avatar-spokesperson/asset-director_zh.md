# 资产导演 - Avatar Spokesperson 流水线

## 何时使用

本阶段准备实际的代言人素材：旁白、数字人或口型同步镜头、字幕资产、品牌背景，以及完成剪辑所需的最小支持图形。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]`, `state.artifacts["idea"]["brief"]` | 主持人方案与旁白需求 |
| 工具 | `talking_head`, `lip_sync`, `tts_selector`, `subtitle_gen`, `image_selector`, `audio_enhance` — 选择器会从注册表自动发现所有可用提供商 | 数字人、旁白与支持资产选项 |
| Playbook | 当前启用的风格 playbook | 背景、字体与字幕规则 |

## 流程

### 1. 锁定数字人生成路径

选用一条主路径并明确记录：

- 由静态图加音频生成 `talking_head`，
- 由现有主持人底片加新音频做 `lip_sync`，
- 或在当前运行时之外已提供的外部数字人渲染。

不要隐瞒已阻塞的数字人路径。如实记录。

### 1b. 样片预览（避免浪费成本）

在批量生成资产之前，为每种高成本类型各做一份样片并展示给用户：

1. **TTS 样片**（若生成旁白）：生成一个段落。在批量生成其余内容前确认音色、语速与人设。
2. **数字人样片**（若使用 `talking_head`）：生成一段短测试片段。在投入完整生成前确认数字人质量可接受。

若被拒绝，调整参数并重试（最多 3 轮）。未获批准前不要批量生成。

### 2. 先解决旁白再处理支持图形

代言人视频依赖语音。明确旁白是：

- 已提供，
- 由 TTS 生成，
- 或已嵌入主持人底片。

若旁白缺失且没有可用的 TTS 工具，将项目标记为阻塞，而不是假装本阶段已成功。

### 3. 构建最小支持套件

仅准备场景计划实际所需：

- 字幕文件，
- 一套 lower-third 系统，
- CTA 卡片，
- 背景或底片资产，
- 可选的静态图或产品支持图。

### 4. 用元数据反映能力真相

推荐元数据键：

- `avatar_generation_path`
- `narration_assets`
- `subtitle_assets`
- `background_assets`
- `scene_asset_index`
- `blocked_assets`

### 5. 质量门

- 数字人路径明确，
- 旁白与数字人资产一致，
- 支持图形保持精简，
- 每个被引用的文件均存在。

## 无数字人路径

当 EP 已触发「旁白叠图形」转向（`talking_head` 与 `lip_sync` 均不可用）时，完全跳过数字人生成，改为产出图形驱动的资产套件：

### 需要产出：
1. **旁白音频** — 通过 `tts_selector`（必选；若 TTS 也不可用则阻塞项目）。
2. **场景画面** — 通过 `image_selector` 或 `video_selector`。每个场景一条主视觉，强化口播要点（示意图、插画、产品图或素材镜头）。
3. **字幕文件** — 与标准路径相同。
4. **文字卡片** — 要点叠加、数据卡片、结尾 CTA 卡片。
5. **背景** — 与 playbook 一致的一套背景族。

### 需要跳过：
- 不调用 `talking_head` 或 `lip_sync`。
- 不写入主持人构图元数据。
- `avatar_generation_path` 应设为 `"none — narration-over-graphics pivot"`。

### 此路径的元数据：
- `avatar_generation_path`: `"narration_over_graphics"`
- `pivot_reason`: 选择无数字人路径的原因
- 其余元数据键保持不变。

### 制作过程中的事实核查

若在资产生成中遇到不确定之处：
- 使用 `web_search` 核查主体视觉准确性（例如：该建筑实际长什么样？）
- 使用 `web_search` 在生成插画前查找参考图
- 在决策日志中记录：`category="visual_accuracy_check"`

视觉准确性很重要。若脚本提到具体地点、人物或物体，
在生成图像前先核实其真实外观。不要依赖
AI 模型的训练数据 — 可能错误或过时。

## 常见陷阱

- 在旁白路径未解决前就制作装饰性资产。
- 在一个简单的代言人视频中混用多种数字人生成策略。
- 核心主持人资产仍是假设状态时仍将本阶段标为完成。
- （无数字人路径）生成与旁白无关的填充视觉 — 每张图都必须强化口播要点。


## 当你不确定怎么做时

若遇到不确定的生成技法、提供商行为或提示模式：

1. **搜索网络** 获取当前最佳实践 — 模型与 API 变化频繁，智能体的训练数据可能已过时
2. **查阅 `.agents/skills/`** 中已有的 Layer 3 知识（提供商专用提示指南、API 模式）
3. **若仍无法解决**，在 `projects/<project-name>/skills/<name>.md` 编写项目范围技能，记录所学内容
4. **在技能中引用来源 URL**，使知识可追溯
5. **写入决策日志**：`category: "capability_extension"`, `subject: "learned technique: <name>"`

以下情况尤其重要：
- **视频生成提示** — 模型对特定词汇的响应随版本变化
- **图像模型参数** — FLUX、GPT Image、Imagen 等的最优设置各不相同且持续演进
- **音频提供商特性** — 声音克隆、音乐生成与 TTS 各有模型专用最佳实践
- **Remotion 组件模式** — 框架演进会带来新的合成技法

不要依赖过时知识。有疑问时，先搜索。

---

## 门控提醒（具有约束力）

本阶段需人工批准门控（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染
产物），并 **结束本轮**。不要在同一条回复中开始下一阶段。
批准按门控逐项进行 — 较早的「继续」不覆盖本门控。

## HeyGen Avatar V

对明确批准的 HeyGen 数字孪生使用 `heygen_avatar`。渲染前检查形象：`Avatar V` 要求 `supported_api_engines` 中包含 `digital_twin` 与 `avatar_v`。传入脚本加 voice_id，或单一提供的音频源。若轮询超时，保留返回的 resume_job/job_path；恢复该任务而不是再次提交。不符合条件的形象是阻塞项，绝不是改用 Avatar IV 的理由。请阅读 provider-model-refresh 技能。
