# 场景导演 - 动画流水线

## 何时使用

你正在将剧本转化为可执行的动画计划。这一阶段决定项目是显得经过设计还是杂乱无章。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["script"]["script"]`, `state.artifacts["proposal"]["proposal_packet"]` | 节拍图与工具路径 |
| Playbook | 当前启用的风格 playbook | 调色、字体、动效一致性 |

## 流程

### 1. 制定以动态分镜为导向的计划

针对每个场景，定义：

- 首先出现什么，
- 发生什么变化，
- 保持什么，
- 场景如何退出。

### 2. 限制转场类型族

选择少量具有明确含义的转场：

- cut（硬切），
- fade（淡入淡出），
- slide（滑动），
- transform（变换）。

### 3. 将场景类型与工具路径对应

使用：

- `diagram` 场景用于结构化讲解，
- `animation` 场景用于以动效为主的序列，
- `text_card` 用于干净、高冲击力的文案时刻，
- `generated` 仅在必要时使用。

**对于 `image_animation` 方式（动漫/插画风格）：**

每个场景使用 `anime_scene` 类型。规划：

- **每场景图片数**：2–3 张，来自同一视觉体系且种子相近，以实现交叉淡入淡出
- **镜头运动**：从 `zoom-in`、`zoom-out`、`pan-left`、`pan-right`、`ken-burns`、`drift-up`、`drift-down`、`parallax`、`static` 中选择 — 各场景交替使用以避免单调
- **粒子类型**：从 `fireflies`、`petals`、`sparkles`、`mist`、`light-rays` 中选择 — 与场景情绪匹配
- **光照**：可选 `lightingFrom`/`lightingTo` 渐变，用于场景内的氛围变化
- **暗角**：电影感构图用 `true`（默认），明亮/open 场景用 `false`
- **场景时长**：每场景 4–7 秒。较长场景需要更多图片以丰富交叉淡入淡出

**image_animation 的场景多样性规则：**
- 连续场景不要使用相同的镜头运动
- 在暖色与冷色粒子类型之间交替
- 混合特写与广角建立镜头
- 使用叠加层（`hero_title`、`section_title`）增强叙事结构

**JSON 属性名映射**（在 composition JSON 中使用下列确切字段名）：

| 概念 | JSON 字段 | 示例值 |
|---------|-----------|----------------|
| 镜头运动 | `animation` | `"zoom-in"`, `"pan-right"`, `"ken-burns"` |
| 粒子效果 | `particles` | `"fireflies"`, `"sparkles"`, `"mist"` |
| 粒子颜色 | `particleColor` | `"#FFE082"` |
| 粒子密度 | `particleCount` | `20`（范围：1–50） |
| 粒子亮度 | `particleIntensity` | `0.5`（范围：0–1） |
| 光照起点 | `lightingFrom` | `"rgba(255,200,100,0.15)"` 或 `"transparent"` |
| 光照终点 | `lightingTo` | `"rgba(255,107,157,0.08)"` 或 `"transparent"` |
| 电影感边缘压暗 | `vignette` | `true` / `false` |
| 场景背景 | `backgroundColor` | 主题衍生值，如 `"#0A0A1A"` 或 `"#F6F1E8"` |

参考：`remotion-composer/public/demo-props/mori-no-seishin.json` — 6 个场景采用此模式。
参考：`remotion-composer/public/demo-props/deep-ocean.json` — 6 个水下场景，不同调色。

### 4. 用元数据定义时序规则

推荐的元数据键：

- `animatic_rules`
- `transition_rules`
- `hold_rules`
- `tool_path_map`
- `reusable_motifs`

### 5. 五维场景计划检查清单

> 每个场景必须明确全部五个维度，但各维度的权重随场景的 `animation_mode` 而变。Manim 及其他图表/程序化场景最关注 **主体（Subject）** 与 **空间构图（Spatial Framing）** — 电影意义上的镜头与主体运动常对应 N/A 或抽象等价物。AI 视频 / `image_animation` / `anime_scene` 场景需要五个维度齐全，行为类似电影镜头。允许将某维度标为 N/A，但须按场景显式标注；禁止静默省略。
>
> 1. **Subject（主体）** — 类型 + 关键视觉属性；Manim 中为突出的方程/对象/图形；`anime_scene` 中为焦点角色或环境。
> 2. **Subject Motion（主体运动）** — Manim 中为 `Create`/`Transform`/`FadeIn` 的顺序及每项动画传达的内容；AI 视频中为按时间顺序的动作与交互。
> 3. **Scene（场景）** — 叠加层（单独列出！）+ 视点 + 设定 + 时段 + 场景动态。Manim 中「设定」为画布背景 + 坐标轴样式；`anime_scene` 中为环境 + 光照渐变。
> 4. **Spatial Framing（空间构图）** — 景别 + 画内位置 + 景深（前景/中景/背景）+ 相对机位高度；以及这些如何变化。Manim 关注布局网格与元素位置；AI 视频关注完整电影构图。
> 5. **Camera（镜头）** — 播放速度 → 镜头畸变 → 高度 → 角度 → 对焦/景深 → 稳定性 → 运动。Manim 与纯 motion graphics 默认 N/A，除非使用虚拟镜头运动（`MoveCamera`、`self.frame`）。`anime_scene` 与 AI 视频须完整指定。
>
> 与场景元数据中的 `animation_mode` 对齐：Manim 场景若写满 Camera 则过度指定；AI 视频场景若省略 Camera 则指定不足。原始词汇见 `skills/creative/video-gen-prompting.md`。

> **叠加层说明。** 叠加层（标题、字幕、HUD、水印、框线图形、下三分之一、`hero_title`、`section_title`、`provider_chip`）不属于场景前景/中景/背景的景深轴。在场景元数据（`overlays: [...]`）中单独列出，含内容与位置。切勿将叠加层描述为「在前景中」 — 这会混淆下游工具以及任何重新分析输出的视频理解模型。

### 6. 质量门禁

- 每个场景有清晰的时序意图，
- 五维检查清单满足该场景 `animation_mode` 的要求（适当时显式 N/A），
- 叠加层位于 `overlays:` 下，不得写在构图描述内，
- 转场体系统一且有意义，
- 工具路径明确，
- 序列整体像一套统一设计。

## 常见陷阱

- 每个场景都引入新的转场创意。
- 规划没有现实制作路径的场景。
- 对文字密集场景过度动画化。

---

## 门禁提醒（具有约束力）

本阶段需人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染产物），并 **结束本轮回复**。勿在同一回复中开始下一阶段。
批准按门禁逐项进行 — 此前「继续」不覆盖本门禁。
