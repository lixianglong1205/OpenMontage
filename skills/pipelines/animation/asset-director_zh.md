# 资产导演 - 动画流水线

## 何时使用

本阶段准备实际的动画素材：旁白、示意图、数学渲染、动态背景、代码可视化，以及可复用的字体或版式系统。

## 动画创作 — 选择运行时

在创作动效组件之前，请阅读 **`skills/meta/animation-runtime-selector.md`** 以确定运行时路由。动画流水线最有可能需要 GSAP 插件 — 标志变形、曲线相机路径、 kinetic 文字、FLIP 过渡等。

常见动画流水线需求的快速路由：

| 动效类型 | 推荐做法 |
|---|---|
| 两个 SVG 形状之间的标志变形 | GSAP MorphSVG — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| SVG 描线 / 笔画揭示 | GSAP DrawSVG — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 沿曲线路径运动的对象 | GSAP MotionPath — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 逐字 / 逐词标题揭示 | GSAP SplitText — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 自定义贝塞尔或弹性缓动 | GSAP CustomEase — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 版式到版式的元素飞入（FLIP） | GSAP Flip — 阅读 `.agents/skills/gsap-plugins/SKILL.md` |
| 跨多元素的多步序列 | GSAP timeline — 阅读 `.agents/skills/gsap-timeline/SKILL.md` |
| 粒子叠加 / 背景动效 | Remotion `ParticleOverlay` 组件（已存在） |
| 数学动画（图表、公式） | Manim — 阅读 `.agents/skills/manim-composer`、`.agents/skills/manimce-best-practices` |
| 吉卜力 / 动漫风格静帧驱动场景 | Remotion `AnimeScene` 组件 + FLUX 图像生成 |

**Remotion 确定性规则：** Remotion 组件内每一处 GSAP 用法都必须由 `useCurrentFrame()` 驱动时间轴进度 — 切勿使用 `requestAnimationFrame`。模式示例见 `.agents/skills/gsap-react/SKILL.md`。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["scene_plan"]["scene_plan"]`、`state.artifacts["script"]["script"]`、`state.artifacts["proposal"]["proposal_packet"]` | 工具路径与节拍映射 |
| 工具 | `tts_selector`、`image_selector`、`video_selector`、`math_animate`、`diagram_gen`、`code_snippet`、`threejs_world`、`music_gen`、`fal_elevenlabs_music` — 选择器会从注册表自动发现所有可用提供商 | 资产生成选项 |
| Playbook | 当前风格 playbook | 视觉一致性 |

## 流程

### 1. 从确定性资产开始

优先选择方差最低且仍够用的路径：

- 结构化示意图优先用 `diagram_gen`，而非通用图像生成；
- 代码场景用 `code_snippet`；
- 真实数学动效用 `math_animate`；
- 已有素材优先于新生成。

若要真实 3D 环境，请阅读 `skills/creative/3d-world-generation.md` 以及该工具的 `threejs-world-generation` Layer 3 技能，再使用 `threejs_world`，而不是任何图像或视频生成器。构建电影级工作区以及语义或线框诊断通道。将可编辑工作区注册为 `type: "3d_world"`；快照属于资产审查，最终 MP4 属于合成阶段。

### 1b. 样片预览（避免浪费成本）

在批量生成资产之前，为每种昂贵类型各做一个样片并展示给用户：

1. **TTS 样片**（若以旁白为主）：在存在 `script.voice_performance.sample_section_id` 时生成该段；否则选择情绪或节奏变化最显著的段落。批量前确认音色、语速、停顿、重音与语气。
2. **视觉样片**：生成一个代表性场景画面（示意图、插画或动态背景）。批量前确认风格与质量。

若被拒绝，调整参数并重试（最多 3 轮）。未获批准前不要批量生成。

### 1c. 基于图像的动画的多图生成（方案 A）

当 `animation_mode == "image_animation"` 时，每个场景需要 **2–3 张图** 用于交叉淡入淡出动画。这是让静帧看起来像运动的关键。

**图像生成工作流：**

1. **定义视觉系统（VISUAL SYSTEM）** — 一套可在项目全部图像中复用的锚点，保证视觉连贯又不把每个镜头压成同一提示词。将其存为可复用元数据。
   ```
   Example: "Hand-painted nature fantasy, warm moss-and-amber palette,
   soft diffused light, painterly foliage textures, gentle wonder."
   ```
   再按场景调整：
   - 场景 1：广角 establishing 森林山谷，薄雾，日出
   - 场景 2：近景角色节拍，灯笼光，漂浮孢子
   - 场景 3：抽象魔法能量揭示，更亮的 accent 对比

2. **使用 seed 管理** — 每个场景的 A/B 变体使用相近 seed（如 100 与 101）。相同提示词 + 不同 seed = 构图相近、细节微差 = 自然的交叉淡入动效。

3. **先生成一张测试图** — 在 1920×1080 下渲染单场景，确认视觉系统效果良好，再批量生成全部图像。

4. **批量生成** — 生成所有场景图像。磁盘上已存在的跳过（幂等）。

5. **Composition JSON** — 每个场景为 `type: "anime_scene"`，含 `images: ["path/a.png", "path/b.png"]` 以及相机运动、粒子类型与光照配置。

**成本估算：** 每场景 2–3 张图 × 按提供商约 $0.03–0.13/张。

**参考：** 成熟批量模式见 `projects/mori-no-seishin/generate_images.py`。

6. **复制到 Remotion public 目录** — 生成全部图像后，复制到 `remotion-composer/public/<project-name>/`，以便 Remotion 通过 `staticFile()` 访问。composition JSON 中的图像路径相对于该目录：
   ```
   remotion-composer/public/<project-name>/scene1-a.png   ← Remotion reads from here
   remotion-composer/public/<project-name>/ambient-music.mp3  ← Music too
   ```
   **若跳过此步，渲染会因文件缺失而失败。** 这是新项目渲染失败的头号原因。

### 2. 构建可复用系统

一次性创建：

- 字体处理方案；
- 下三分之一或标签样式；
- 重复出现的 motif 资产；
- 背景容器。

### 3. 旁白可选，但计划必须明确

若项目以旁白为主，制作或获取旁白。阅读 `skills/meta/voice-performance-director.md`，再在构建 TTS 请求时应用 `script.voice_performance` 与各段的 `delivery_cues`。存在 `provider_text` 时使用它，将 cues 映射到提供商控件，并在每条旁白资产上记录所用设置。若以文字或音乐为主，在元数据中明确说明。

### 4. 用元数据记录可行性真相

推荐元数据键：

- `tool_path_map`
- `reusable_assets`
- `narration_assets`
- `voice_performance`：样片批准路径、提供商设置、是否应用了 delivery cues
- `scene_asset_index`
- `blocked_assets`

### 5. 质量门

- 每个场景的资产路径明确；
- 可复用资产确实被复用；
- 缺失能力如实暴露；
- 每个引用文件存在；
- 旁白主导的资产应用已批准的 voice-performance 设置。

### 制作过程中的事实核查

若在资产生成中遇到不确定之处：
- 使用 `web_search` 核实主体视觉准确性（例如某建筑实际长什么样？）
- 使用 `web_search` 在生成插画前查找参考图
- 在决策日志中记录：`category="visual_accuracy_check"`

视觉准确性很重要。若脚本提到具体地点、人物或物体，生成图像前先核实其真实外观。不要依赖 AI 模型的训练数据 — 可能错误或过时。

## 常见陷阱

- 在确定性资产更合适时仍使用高方差生成。
- 反复重建相同的标题或标签系统。
- 隐藏失败的资产路径而非上报。
- 把 TTS 当作纯文本转音频。旁白主导的动画需要停顿、重音与节奏 cues 从脚本进入生成的音频。
- 把「一致性」理解成「每次同一提示词」。好的动画保持可识别的世界，同时让每个节拍仍有新鲜感。

## 当你不确定时

若遇到不确定的生成技巧、提供商行为或提示模式：

1. **搜索网络** 获取当前最佳实践 — 模型与 API 变化频繁，智能体的训练数据可能过时
2. **查阅 `.agents/skills/`** 中已有的 Layer 3 知识（提供商专用提示指南、API 模式）
3. **若仍无解**，在项目范围技能 `projects/<project-name>/skills/<name>.md` 中记录所学
4. **在技能中引用来源 URL**，使知识可追溯
5. **写入决策日志**：`category: "capability_extension"`，`subject: "learned technique: <name>"`

以下尤其重要：
- **视频生成提示** — 模型对各版本有特定词汇响应
- **图像模型参数** — FLUX、GPT Image、Imagen 的最优设置不同且持续演进
- **音频提供商特性** — 声音克隆、音乐生成、TTS 各有模型级最佳实践
- **Remotion 组件模式** — 框架演进中不断出现新的合成技巧

不要依赖过时知识。有疑问时先搜索。

---

## 关卡提醒（具有约束力）

本阶段需人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染该产物），并 **结束本轮**。不要在同一条回复中开始下一阶段。
批准按关卡单独计算 — 更早的「继续」不覆盖本关卡。
