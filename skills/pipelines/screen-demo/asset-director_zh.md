# 资产导演 - Screen Demo 流水线

## 适用场景

本阶段产出数量精简但杠杆高的资产，让屏幕演示更易跟随：字幕、音频清理、可复用叠加层、遮罩，以及可选的轻量辅助卡片。

## 两种制作模式 — 生成资产前先选定

**阅读 brief 中的 `production_mode` 字段。** 若 `idea` 阶段未设定，在此决定：

| 模式 | 适用情况 | 资产制作方式 |
|---|---|---|
| **`real_capture`** | 真实应用 UI（浏览器、设计工具、带插件的 IDE）；实时行为；用户要求录制自己的屏幕 | 在捕获的 MP4 上叠加：清理后的音频 + 字幕 + 标注叠加层（箭头、高亮遮罩） |
| **`synthetic_terminal`** | CLI、终端、安装流程、make 目标、git/npm 命令、`.env` 配置 — 一切可脚本化的内容 | **完全不录制。** 为 `video_compose`（Remotion）编写 `terminal_scene` 切片。命令逐字输入，输出滚动，药丸提示完成。见 `.agents/skills/synthetic-screen-recording/SKILL.md`。 |

**模式选择启发式：** *「我能否在拍摄前预测每条命令及其输出？」* 若是 → 合成。若否 → 真实录制。

合成模式下，资产阶段产出：
- **旁白（tts_selector）** 与每条命令应在视频时间轴上开始输入的时刻精确对齐
- **`steps` 列表**（cmd/out/pause/pill 原语）与旁白提示同步节奏
- **节奏校验** 通过 `lib.verify_scene_pacing.assert_alignment(...)` — 渲染前必须通过
- **不** 使用屏幕录制素材、标注箭头、缩放裁剪区域（这些属于真实录制概念）

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]`, `state.artifacts["idea"]["brief"]` | 制作内容依据 |
| 工具 | `subtitle_gen`, `audio_enhance`, `tts_selector`, `image_selector`, `diagram_gen` — 选择器从 registry 自动发现所有可用 provider | 生成能力 |
| Playbook | 当前风格 playbook | 字体与叠加层样式 |

## 流程

### 1. 实用优先于装饰

屏幕演示不需要大量资产堆叠，需要的是少数关键资产：

- 必选：字幕
- 通常必选：清理后的主音频
- 通常有帮助：可复用高亮框、箭头、步骤标签、模糊遮罩套件
- 可选：一张 intro 卡片、一张 outro 卡片、稀疏的示意图叠加
- 仅当 preflight 允许时可选：为无声录制生成旁白

### 1b. 英雄场景样片（必选）

批量生成资产之前：
1. 确定英雄场景（演示中最重要的一步或交互）
2. 为该场景生成 **一个** 样片资产（字幕样式、高亮叠加或 intro 卡片）
3. 呈现：「这是最重要步骤的视觉方向。是否符合你的想象？其余将按此风格生成。」
4. 等待批准后再进行批量生成

这可避免最昂贵的错误：在用户不认可的方向上生成 10+ 个资产。

### 2. 优先生成字幕

规则：

- 在未知 UI 背景上保持高对比度，
- 切勿遮挡观众需要阅读的文本，
- 除非逐词高亮有明显帮助，否则优先短语级分块，
- 在 `asset_manifest.metadata.subtitle_zones` 中准备位置覆盖说明。

### 3. 构建可复用叠加层套件

不要为每次点击单独生成资产。构建小型共享套件：

- `highlight_box_primary`
- `arrow_primary`
- `step_label_primary`
- `keystroke_badge_primary`
- `blur_mask_template`

这些应跨场景复用，时序与摆放由下游处理。

### 4. 务实清理或生成音频

目标：

- 去除干扰性键盘声与环境噪声，
- 归一化语音，
- 保持时序，
- 勿过度处理成机械感音频。

若录制无声：

- 仅当 TTS 通过 preflight 时才生成旁白，
- 否则保持资产计划以文本为主，并在 metadata 中注明限制。

### 5. 仅在物有所值时生成补充视觉

仅在以下情况使用 `image_selector` 或 `diagram_gen`：

- 简短开场卡片，
- 步骤过渡卡片，
- 澄清隐藏流程的简单示意图，
- outro 卡片。

不要为屏幕已能说明的工作流创建装饰性 artwork。

### 6. 整洁构建资产清单

每个资产须有有效的 schema 类型与 `scene_id`。

在 `asset_manifest.metadata` 中记录例如：

- `subtitle_zones`
- `overlay_kit`
- `audio_settings`
- `narration_mode`
- `sensitive_regions`

### 7. 质量门

**存在性检查：**
- [ ] 字幕文件存在于声明路径且解析无错误
- [ ] 清理后音频文件存在且时长符合预期
- [ ] 可复用叠加层套件存在且覆盖计划的标注类型
- [ ] 所有补充视觉存在于声明路径

**时序检查：**
- [ ] 字幕时间戳与 script 各 section 时间戳对齐
- [ ] 若已生成旁白，时序与 section 时长足够接近以便剪辑

**质量检查：**
- [ ] 字幕在输出分辨率下可读
- [ ] 清理后音频无残留干扰噪声
- [ ] 标注颜色对比度充足
- [ ] 模糊遮罩完全覆盖敏感内容

### 制作过程中的事实核验

若在资产生成中遇到不确定之处：
- 使用 `web_search` 核验主体视觉准确性（例如某建筑实际长什么样？）
- 使用 `web_search` 在生成插图前查找参考图
- 在决策日志中记录：`category="visual_accuracy_check"`

视觉准确性很重要。若脚本提到具体地点、人物或物体，
在生成图像前核验其真实外观。不要依赖
AI 模型的训练数据 — 可能错误或过时。

## 常见陷阱

- 为每次点击生成大量一次性叠加文件，而非可复用套件。
- 字幕直接压在终端输出或底部导航上。
- 假设无声录制会自动获得旁白而不检查 TTS。
- 把图像生成预算花在原始屏幕已能提供的视觉上。


## 当你不确定做法时

若遇到不确定的生成技巧、provider 行为或 prompting 模式：

1. **搜索网络** 获取当前最佳实践 — 模型与 API 变化频繁，agent 训练数据可能过时
2. **查阅 `.agents/skills/`** 中的 Layer 3 知识（provider 专用 prompting 指南、API 模式）
3. **若仍无法解决**，在项目范围技能 `projects/<project-name>/skills/<name>.md` 中记录所学
4. **在技能中引用来源 URL**，使知识可追溯
5. **记入决策日志**：`category: "capability_extension"`, `subject: "learned technique: <name>"`

以下情况尤其重要：
- **视频生成 prompting** — 模型对特定词汇的响应随版本变化
- **图像模型参数** — FLUX、GPT Image、Imagen 等的 optimal 设置各异且演进
- **音频 provider 特性** — 声音克隆、音乐生成、TTS 各有模型级最佳实践
- **Remotion 组件模式** — 框架演进中不断出现新的 composition 技巧

不要依赖过时知识。有疑问时，先搜索。

---

## 门控提醒（具有约束力）

本阶段需人工批准门控（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` checkpoint，呈现摘要（Backlot 看板渲染
产物），并 **结束本轮**。勿在同一回复中启动下一阶段。
批准按门控逐项进行 — 较早的「继续」不覆盖本门控。
