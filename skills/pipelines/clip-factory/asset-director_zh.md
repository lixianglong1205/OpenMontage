# 资产导演 - Clip Factory 流水线

## 适用场景

本阶段为整批 clip 构建共享的视觉与音频套件。重点是复用，而非为每个 clip 单独定制设计。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["scene_plan"]["scene_plan"]`、`state.artifacts["script"]["script"]`、`state.artifacts["idea"]["brief"]` | Clip 计划与排序 |
| 工具 | `subtitle_gen`、`audio_enhance` | 可批量使用的字幕与音频清理 |
| Playbook | 当前启用的 style playbook | 字幕与叠加层一致性 |

## 流程

### 1. 优先构建共享资产

优先可复用资产，避免每个 clip 重新发明：

- 一套字幕样式系统，
- 一种 hook 文字处理，
- 一种 lower-third 处理，
- 一个水印 / 品牌框，
- 如需要，一种 CTA / 片尾处理。

### 1b. 主场景样片（必选）

在批量资产生成之前：
1. 确定主场景（整批 clip 的视觉高峰）
2. 为该场景生成 **一个** 样片级视觉资产
3. 展示给用户：「这是最重要 clip 的视觉方向。是否符合你的预期？我会按此风格生成其余内容。」
4. 在继续批量生成前等待批准

这可避免最昂贵的错误：在用户不喜欢的方向上生成 10+ 个资产。

### 2. 为每个 Clip 生成字幕

每个已批准的 clip 需要各自的字幕资产，时间轴从 clip 起点而非源素材起点对齐。**时间戳重基准**至关重要。

将 clip 相对时间细节存入 `asset_manifest.metadata.subtitle_map`。

### 3. 统一规范化音频

对整批 clip 使用 `audio_enhance`，使批次像同一系列：

- 相近响度，
- 相近噪底，
- 相近人声清晰度。

### 4. 保持 Hook 资产轻量

多数 hook 叠加层应以文字优先、基于模板。除非整批确实受益，否则不要为定制美术花费时间或预算。

### 5. 用元数据组织批次结构

推荐的 metadata 键：

- `shared_assets`
- `subtitle_map`
- `audio_profile`
- `clip_asset_index`
- `style_tokens`

### 6. 质量门

- 每个 clip 都有字幕，
- 每个 clip 都有干净的音频资产或已验证的源音频路径，
- 共享资产被一致引用，
- 资产数量与批次规模相匹配、切实可行。

### 制作过程中的事实核查

若在资产生成中遇到不确定之处：
- 使用 `web_search` 核实主体视觉准确性（例如：该建筑实际长什么样？）
- 在生成插画前用 `web_search` 查找参考图
- 在决策日志中记录：`category="visual_accuracy_check"`

视觉准确性很重要。若脚本提到具体地点、人物或物体，
在生成图像前先核实其真实外观。不要依赖
AI 模型的训练数据——可能错误或过时。

## 常见陷阱

- 忘记按 clip 重基准字幕时间。
- Hook 资产过度设计导致批次不一致。
- 只规范化部分 clip 而忽略其余。
- 把 10 个 clip 的批次当成 10 个互不相关的项目。

## 当你不确定怎么做时

若遇到不确定的生成技巧、提供商行为或 prompting 模式：

1. **搜索网络** 获取当前最佳实践——模型与 API 变化频繁，智能体的训练数据可能过时
2. **查阅 `.agents/skills/`** 中已有的 Layer 3 知识（提供商专用 prompting 指南、API 模式）
3. **若仍无法解决**，在 `projects/<project-name>/skills/<name>.md` 编写项目级 skill，记录所学
4. 在 skill 中 **引用来源 URL**，使知识可追溯
5. **记入决策日志**：`category: "capability_extension"`、`subject: "learned technique: <name>"`

以下场景尤其重要：
- **视频生成 prompting**——模型对特定词汇的响应随版本变化
- **图像模型参数**——FLUX、GPT Image、Imagen 等的最优设置各不相同且持续演进
- **音频提供商特性**——声音克隆、音乐生成、TTS 各有模型级最佳实践
- **Remotion 组件模式**——框架演进中不断出现新的合成技巧

不要依赖过时知识。有疑问时，先搜索。

---

## 门控提醒（具有约束力）

本阶段需人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染
产物），并 **结束本轮**。不要在同一回复中启动下一阶段。
批准按门控逐项进行——此前说的「继续」不覆盖本门控。
