# 资产导演 - 电影管线（Cinematic Pipeline）

## 何时使用

本阶段为最终电影剪辑准备可用媒体：源素材选段、标题卡资产、可选辅助插入镜头、音乐、环境声，以及需要时的字幕资产。

## 电影标题与叠加层的动画创作

在创作标题卡、姓名条或 SVG 叠加层之前，请阅读 **`skills/meta/animation-runtime-selector.md`** 以了解运行时路由。电影类作品通常依赖少量高工艺动效模式：

| 电影需求 | 推荐做法 |
|---|---|
| 带 subtle 揭示的英雄标题 | Remotion `HeroTitle` 组件（已有） |
| SVG 上的 Logo 构建 / 电影 sting | GSAP DrawSVG + MotionPath — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 在宽幅静帧或叠加层上的曲线镜头运动 | GSAP MotionPath — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 逐字标题揭示（ prestige / 预告片风格） | GSAP SplitText — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 电影感缓动（Unreal 风格、顿挫、加权） | GSAP CustomEase / EasePack — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 带弹性 settle 的姓名条 lower-third | 通常 Remotion `spring()` 足够；若需顿挫则用 GSAP CustomEase |
| 胶片颗粒 / 粒子叠加 | Remotion `ParticleOverlay`（已有） |
| 调色 / LUT | `tools/enhancement/color_grade.py`（非动画范畴） |

**电影类是 GSAP 最常发挥价值的场景** — 该类型需要精细缓动与精确曲线运动，原生 `interpolate()` 往往难以干净表达。也不要过度使用：简单淡入标题时，Remotion `spring()` 仍优于引入整套 GSAP 依赖。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]`, `state.artifacts["proposal"]["proposal_packet"]` | 场景意图与节拍计划 |
| 工具 | `subtitle_gen`, `audio_enhance`, `image_selector`, `video_selector`, `pixabay_music`（免费，默认）, `freesound_music`（免费）, `music_gen`（ElevenLabs，付费） — 选择器会从 registry 自动发现所有可用 provider。**默认先用 `pixabay_music`，再考虑 `music_gen`。** | 可选辅助资产创建 |
| Playbook | 当前风格 playbook | 品牌与 typography 一致性 |

## 流程

### 显式 3D 世界路径

当已批准的交付承诺是连续、自由视点 3D 世界时，
`threejs_world` 满足语义规划与浏览器原生动效：它创建真实场景图与时间驱动的相机，而非静帧回退。阅读
`skills/creative/3d-world-generation.md` 与 `.agents/skills/threejs-world-generation/SKILL.md`，
构建到 `projects/<id>/hyperframes/`，并在资产关卡前审查全局、区域、步行、语义与线框视图。浏览器原生交付须锁定
`render_runtime="hyperframes"` 与 `composition_mode="atelier"`。参考级视频须锁定 Blender 为 3D
渲染器，且 `render_runtime="ffmpeg"` 仅作为图像序列/音频打包器。

英雄/参考驱动工作须强制 `quality_tier="production"`。用 `threejs_asset_catalog` 安装授权目录，在有用时用 Atlas/fal 生成唯一 mesh，在 Blender 中组装与渲染；若仍存在 dominant 基元、平坦无纹理地面、区域对象密度低或明显重复，则拒绝资产关卡。`blockout` 仅用于布局/相机批准。

### 1. 优先源素材选段

从以下开始：

- 源 footage 选段，
- 静帧，
- 标题卡背景，
- 任何已批准的提供音乐或环境 bed。

这些是主要材料。其余均为辅助。

若 `proposal_packet.metadata.motion_required = true`，则必须有真实运动 footage 或生成的视频片段。此时：

- 静帧仅可作为参考材料或更大运动合成内的衬底元素，
- 静帧不能替代已规划的运动镜头，
- 除非用户明确批准 animatic，否则静帧 teaser 不可接受。

### 1b. 样本预览（避免浪费支出）

在批量生成辅助资产之前，为每种昂贵的生成类型各做一个样本并展示给用户：

1. **生成插入样本**（若使用 `image_selector` 或 `video_selector`）：生成一个代表性视觉。在批量前确认其与源 footage 互补。
2. **音乐样本**（先试 `pixabay_music` — 免费，可按 mood/BPM 搜索；回退 `freesound_music` 做 cue 与环境；仅当搜索工具无法满足 brief 时才用 `music_gen`）：采样或检索短片段。确认 mood 与能量与节拍计划一致。

若 `motion_required = true`，代表性视觉必须是视频片段样本，而非静帧样本。

若被拒绝，调整参数并重试（最多 3 次）。未批准前不要批量。

在生成样本之前，向用户明确说明将使用的生成路径：

- tool，
- provider，
- model 或 variant，
- generation mode，
- 选择理由。

若该路径失败，在尝试不同 provider、model 或 generation mode 之前停止并询问。

### 2. 仅在需要处生成辅助资产

可选生成资产应填补明确缺口：

- 缺失的过渡 b-roll，
- 概念导向插入，
- 纹理或氛围卡，
- 简单纹理化运动背景。

对 motion-required 任务，生成镜头优先用 `video_selector`。`image_selector` 可支持 look development、概念帧或嵌入设计层，但本身不能满足 motion 要求。

### 3. 准备真实音频计划

存储：

- 所选音轨或 prompt，
- 环境层，
- impact 或转场音效，
- 若有对白或旁白则含字幕资产。

### 4. 用元数据记录权利与意图

推荐 metadata 键：

- `source_selects`
- `music_plan`
- `ambience_plan`
- `title_assets`
- `generated_support_assets`
- `rights_notes`

### 生成 Prompt 的前/后自审

> 在向任何图像或视频生成 tool 发送 prompt 之前，执行三步自审， modeled on CHAI oversight loop（「Building a Precise Video Language with Human-AI Oversight」，arXiv 2604.21718v2）。成本小（无额外 tool 调用）；收益大（避免浪费生成）。对电影类，这对 **hero-frame prompt** 最重要 — 一张坏 hero frame 会毁掉整片，且 hero frame 是最贵、最难重做的镜头。
>
> **Step 1 — Pre-caption pass。** 按你平时的方式写 prompt。不要过度编辑；目标是完整初稿。
>
> **Step 2 — Critique pass。** 用 5 方面清单（Subject / Subject Motion / Scene / Spatial Framing / Camera）给初稿打分。对每个方面：
> - 是否已指定？若否，是刻意省略（如「无主体 — 风景镜头」）还是疏漏？
> - 易混术语是否已消歧？（dolly vs zoom，pan vs truck，bird's-eye vs aerial，fisheye vs barrel，full shot vs close-up）
> - 情绪形容词（「epic」「moody」「cinematic」）是否替换为其视觉成因（low-key lighting、slow push-in、anamorphic flare、deep shadows）？
> - 对多镜头 prompt 与 identity 锚定的 hero frame：identity 是否在镜头间逐字锚定？
>
> **Step 3 — Post-caption pass。** 重写以补全缺失方面、修正易混术语、替换主观用语。post-caption 才是发给生成 tool 的版本。
>
> 在资产 metadata 中记录 (pre, critique, post) 三元组以便追溯。这与 CHAI 工作流一致，并为 reviewer 提供可审计记录。

### 5. 质量关卡

- 源与辅助资产区分清晰，
- 生成插入有限且有目的，
- 音频计划与 beat map 一致，
- 每个引用文件存在。
- 若需要 motion，资产集须包含 motion-led beat 的真实视频片段。

### 制作中事实核验

若在资产生成中遇到不确定：
- 用 `web_search` 核验主体视觉准确性（例如该建筑实际长什么样？）
- 用 `web_search` 在生成插画前找参考图
- 在 decision log 中记录：`category="visual_accuracy_check"`

视觉准确性很重要。若脚本提到具体地点、人物或物体，
在生成图像前核验其真实外观。不要依赖
AI model 的训练数据 — 可能错误或过时。

## 常见陷阱

- 在证明源剪辑可行之前就生成额外镜头。
- 把音乐当作单一 loop 而非 beat-aware 元素。
- 忘记 supplied 资产的权利或来源说明。
- 因某个 provider 或 renderer 失败而悄悄从视频片段降级为静帧。
- 在用户批准生成路径后悄悄切换 provider 或 model。


## 当你不确定如何做

若遇到不确定的生成技术、provider 行为或 prompting 模式：

1. **搜索网页** 获取当前最佳实践 — model 与 API 变化频繁，agent 训练数据可能过时
2. **查阅 `.agents/skills/`** 中已有 Layer 3 知识（provider 专用 prompting 指南、API 模式）
3. **若仍不够**，在 `projects/<project-name>/skills/<name>.md` 写项目范围 skill，记录所学
4. **在 skill 中引用来源 URL**，使知识可追溯
5. **记入 decision log**：`category: "capability_extension"`, `subject: "learned technique: <name>"`

以下尤其重要：
- **视频生成 prompting** — model 对特定词汇的响应随版本变化
- **图像 model 参数** — FLUX、GPT Image、Imagen 等最优设置不同且演进
- **音频 provider 特性** — 声音克隆、音乐生成、TTS 各有 model 专用最佳实践
- **Remotion 组件模式** — 框架演进中不断出现新合成技巧

不要依赖过时知识。有疑问时先搜索。

---

## 关卡提醒（具有约束力）

本阶段以人工批准为关卡（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` checkpoint，呈现摘要（Backlot board 渲染
产物），并 **结束本轮**。不要在同一回复中开始下一阶段。
批准按关卡计 — 较早的「继续」不覆盖本关卡。
