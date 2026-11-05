# 资产导演 — Talking Head 流水线

## 何时使用

你已有场景规划与脚本。你的任务是为口播类视频生成配套资产：字幕、提取的音频、叠加图形（图表、文字卡片、数据揭示）以及任何补充画面。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | 产物校验 |
| 前置产物 | 场景规划、脚本 | 需要创建哪些资产 |
| 工具 | `subtitle_gen`、`audio_mixer` | 字幕与音频生成 |
| 工具 | `image_selector`（可选） | 叠加层用图库素材 |
| 工具 | `pixabay_music`（可选） | 免版税背景音乐 |

## 流程

### 步骤 0：主场景样片（必填）

在批量生成资产之前：
1. 确定主场景（视频的视觉高峰）
2. 为该场景生成**一份**样片资产（字幕样式、叠加层或背景）
3. 呈现给用户：「这是最重要场景的视觉方向。是否符合你的设想？确认后我会按此风格生成其余内容。」
4. 等待批准后再进入批量生成

这可避免最昂贵的错误：在用户不喜欢的方向上生成 10+ 份资产。

### 步骤 1：生成字幕

使用脚本阶段的转写数据创建：
- 带词级时间轴的 SRT 或 ASS 字幕文件
- 按 playbook 设定字幕样式（字体、大小、颜色、位置）

若场景规划包含 `corrections` 字典，将其传给 `subtitle_gen`：
```
subtitle_gen.execute({
    "segments": <transcript_segments>,
    "corrections": {"cloud": "Claude"},
    "max_words_per_line": 5,
    "output_path": "<project>/assets/subtitles/subtitles.srt"
})
```

### 步骤 2：提取并处理音频

- 从原始素材中提取音轨
- 如需要，通过 `audio_mixer` 做降噪
- 归一化音量电平

### 步骤 3：获取背景音乐

若场景规划包含背景音乐：

1. **检查本地 pixabay 音乐库** — 查找与情绪匹配的已下载 MP3
2. **使用 `pixabay_music` 工具** — 按场景规划中的情绪/流派关键词搜索
3. **对所选曲目运行 `audio_energy` 分析**，找到最佳起始偏移（跳过安静前奏）

在资产清单中记录音乐路径、偏移量以及是否需要循环。

### 步骤 4：生成叠加层资产

若场景规划包含叠加场景（来自 scene-director 的 Watch & Propose 步骤），为每个场景生成对应资产。

**Remotion 渲染的叠加层**（图表、对比、KPI 网格、数据卡片等）：

为每个叠加层创建一段 composition JSON。这些将由 compose-director 渲染。每个叠加层需要：

```json
{
  "overlay_id": "overlay_1",
  "remotion_cut": {
    "id": "term-agentic-ai",
    "type": "callout",
    "text": "Agentic AI: software that acts autonomously toward goals",
    "in_seconds": 0,
    "out_seconds": 4,
    "backgroundColor": "<theme_background>",
    "accentColor": "<theme_accent>",
    "icon": "💡"
  },
  "overlay_timestamp": 22.0,
  "position": "lower_third"
}
```

**叠加类型 → Remotion cut 映射：**

| 场景规划叠加 | Remotion `type` | 必填属性 |
|-------------------|-----------------|----------------|
| 关键术语定义 | `callout` | `text`、`icon`（可选） |
| 统计/数字 | `stat_card` | `stat`（数字）、`text`（标签） |
| 对比 | `comparison` | `leftLabel`、`rightLabel`、`leftValue`、`rightValue` |
| 数据柱状图 | `bar_chart` | `chartData`（`{label, value}` 数组） |
| 饼图 | `pie_chart` | `chartData`（`{label, value}` 数组） |
| 折线图 | `line_chart` | `chartSeries`（`{name, data: number[]}` 数组） |
| KPI 仪表盘 | `kpi_grid` | `chartData`（`{label, value}` 数组）— 数字宜小并带后缀（如 "2.4M"） |
| 进度指示 | `progress_bar` | `progress`（0-100）、`text` |
| 章节标题 | `hero_title` | `text`、`subtitle`（可选） |
| 引用/金句 | `callout` | `text`、`icon` |
| 下三分之一 | `text_card` | `text` |

**Remotion AnimatedBackground：**

Explainer composition 现包含 `AnimatedBackground` 组件，渲染动画渐变网格、浮动光球与 subtle 网格图案，观感远优于纯色平面背景。

- 场景背景应使用当前主题背景，使 AnimatedBackground 与叠加卡片形成统一体系。
- **不要**为背景使用任意纯色平面 — 由 AnimatedBackground 与主题驱动整体处理。
- 合成绿幕素材时，将 AnimatedBackground 作为替换背景渲染（见 compose-director 步骤 3c）。

**组件约束：**

| 组件 | 最小宽度 | 720px 竖屏？ | 值类型 |
|-----------|-----------|-----------------|------------|
| comparison | 900px | 否 → 改用 2 个 stat_card | string |
| kpi_grid | 720px | 是 | 仅 numeric（不可 "15+"） |
| bar_chart | 500px | 是 | numeric |
| stat_card | 300px | 是 | 可为 string |
| callout | 400px | 是 | string |
| hero_title | 400px | 是 | string |
| line_chart | 500px | 是 | numeric |
| progress_bar | 600px | 是 | numeric |
| stat_reveal | 300px | 是 | 可为 string |

关键规则：
- `comparison` 需要 900px 及以上宽度。720px 竖屏帧中，改为两个顺序播放的 `stat_card`。
- `kpi_grid` 的值**必须**为纯数字（如 `4.8`、`73`、`2400`）。形如 `"15+"`、`"$4.8B"` 或 `"2.4M"` 的格式化字符串会导致渲染错误。带格式的数字请用 `stat_card`。
- 选择组件前务必确认目标帧宽。竖屏（720px）不可用 `comparison`。

**叠加层主题规则** — 叠加层的背景、强调色与文字色应来自所选 playbook 或自定义视觉身份。仅在素材/主题需要时使用深色卡片；明亮编辑类口播在对比度足够时也可使用浅色卡片。

**简单文字叠加**（若 Remotion 过重）：

使用 FFmpeg 或 PIL 生成 PNG，保存于 `<project>/assets/overlays/overlay_<id>.png`。

### 步骤 5：构建资产清单

记录所有已生成资产的路径、类型与工具引用：

```json
{
  "subtitles": {
    "path": "assets/subtitles/subtitles.srt",
    "format": "srt",
    "word_count": 208
  },
  "music": {
    "path": "assets/audio/bg_music.mp3",
    "offset_seconds": 3.5,
    "needs_loop": true
  },
  "overlays": [
    {
      "overlay_id": "overlay_1",
      "type": "callout",
      "timestamp": 22.0,
      "duration": 4.0,
      "remotion_cut": { ... },
      "position": "lower_third"
    }
  ],
  "transcript_segments": "assets/audio/transcript.json"
}
```

### 步骤 6：自评

| 标准 | 问题 |
|-----------|----------|
| **字幕** | 字幕是否存在且与语音时间对齐？ |
| **音频** | 音频是否干净且已归一化？ |
| **音乐** | 是否对音乐运行了 audio_energy 以确定最佳偏移？ |
| **叠加层** | 场景规划中的每个叠加是否都有对应生成资产？ |
| **叠加内容** | 叠加中的数据是否与讲者实际表述一致？ |
| **文件** | 所有资产路径是否指向已存在的文件？ |

### 步骤 7：提交

对照 schema 校验 asset_manifest，并通过 checkpoint 持久化。

### 制作过程中的事实核查

若在资产生成中遇到不确定之处：
- 使用 `web_search` 核实主体视觉准确性（例如某建筑实际长什么样？）
- 使用 `web_search` 在生成插图前查找参考图
- 在决策日志中记录：`category="visual_accuracy_check"`

视觉准确性很重要。若脚本提到具体地点、人物或物体，生成图像前应先核实其真实外观。不要依赖 AI 模型的训练数据 — 可能错误或过时。

## 当你不确定如何做

若遇到不确定的生成手法、供应商行为或提示模式：

1. **搜索网络**获取当前最佳实践 — 模型与 API 更新频繁，训练数据可能过时
2. **查阅 `.agents/skills/`** 中的 Layer 3 知识（供应商专用提示指南、API 模式）
3. **若仍无法解决**，在 `projects/<project-name>/skills/<name>.md` 撰写项目级 skill，记录所学
4. **在 skill 中引用来源 URL**，便于追溯
5. **写入决策日志**：`category: "capability_extension"`，`subject: "learned technique: <name>"`

以下场景尤其重要：
- **视频生成提示** — 各版本模型对特定词汇响应不同
- **图像模型参数** — FLUX、GPT Image、Imagen 等最优设置各异且持续演进
- **音频供应商特性** — 声音克隆、音乐生成、TTS 各有模型级最佳实践
- **Remotion 组件模式** — 框架演进中不断出现新 composition 手法

勿依赖过时知识。有疑问时，先搜索。

---

## 关卡提醒（具约束力）

本阶段需人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染产物），并**结束本轮**。勿在同一回复中启动下一阶段。
批准按关卡单独生效 — 此前的「继续」不覆盖本关卡。
