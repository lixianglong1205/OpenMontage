# Publish Director — Explainer 流水线

## 何时使用

你是已生成讲解视频的发布负责人（Publisher）。你手头有一份包含最终视频文件的 `render_report`。你的任务是为分发做准备：生成 SEO 元数据、创建缩略图、打包导出，并记录发布事件。

这里是优质视频触达受众的环节。若没有合适的元数据与打包，再好的内容也会被埋没。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["compose"]["render_report"]`、`state.artifacts["proposal"]["proposal_packet"]`、`state.artifacts["research"]["research_brief"]` | 视频文件与原始提案 |
| Playbook | 当前启用的 style playbook | 缩略图视觉风格 |

## 流程

### 步骤 1：收集上下文

收集编写元数据所需的一切：
- **Proposal packet**：标题、钩子、要点、目标平台、调性
- **Render report**：输出路径、时长、分辨率
- **Script**：各章节摘要，用于描述/章节标记

### 步骤 2：生成 SEO 元数据

**标题**（YouTube 最长 60 字符）：
- 包含 proposal packet 中的主关键词
- 以钩子或数字开头
- 避免标题党，但要足够吸引点击
- 示例："Vector Databases Explained in 60 Seconds" 优于 "About Vector Databases"

**描述**（前 150 字符至关重要 — 会出现在搜索结果中）：
- 首行：用核心价值主张重述钩子
- 正文：涵盖的关键主题，自然融入相关关键词
- 章节：各主要段落的时间戳标记（来自 script sections）
- 行动号召（CTA）：订阅/点赞/关注
- 链接：视频中提到的相关资源

**标签/关键词**（因平台而异）：
- 从 proposal packet 的 key_points 衍生 5–10 个具体标签
- 宽词与窄词结合：如 "machine learning" + "vector database tutorial"
- 包含主题、形式（"explainer"）及相关术语

**话题标签**（面向社交平台）：
- 3–5 个相关 hashtag
- 热门与垂直领域兼顾

### 步骤 3：生成缩略图概念

描述一张缩略图，要求：
1. 采用 playbook 的视觉风格
2. 视觉上呈现视频核心概念
3. 包含 3–5 个字的文案（钩子或关键数据）
4. 高对比度，小尺寸下仍可读
5. 文案使用 playbook 的 accent colors

```json
{
  "thumbnail": {
    "concept": "Split screen: left side shows slow SQL query (red X), right shows fast vector search (green check). Large text: '100x FASTER'",
    "text_overlay": "100x FASTER",
    "style_notes": "Use playbook accent colors, bold Inter font, dark background"
  }
}
```

*注意：若可用 image_selector，则实际生成缩略图；否则仅为供手动制作的概念说明。*

### 步骤 4：创建章节标记

根据 script sections 生成 YouTube 风格章节：

```
0:00 - Introduction
0:15 - What are Vector Databases?
0:45 - How Embeddings Work
1:20 - The Search Algorithm
1:55 - Real-World Examples
2:30 - When to Use Vector DBs
```

每个章节对应某 script section 的 `start_seconds`。

### 步骤 5：打包导出

使用 `export_bundle` 工具（capability `publish`）以确定性方式完成打包 — 传入最终 `video_path`（来自 `render_report`）、`title`，以及你准备好的元数据（`description`、`tags`、`hashtags`、`chapters`，可选 `subtitles_path` 与 `thumbnail_path`/`thumbnail_concept`）。
它会布局导出目录、写入元数据文件，并在 `data["publish_log"]` 中返回符合 schema 的 `publish_log`（`status: "exported"`），你将其持久化为本阶段产物。

产出如下结构：

```
exports/
  <project_name>/
    video/
      output.mp4            # Final rendered video (subtitles.srt alongside if provided)
    metadata/
      metadata.json         # All SEO metadata
      chapters.txt          # Chapter markers
      description.txt       # Ready-to-paste description (+ chapters)
      tags.txt              # One tag per line
    thumbnails/
      concept.json          # Thumbnail concept (or the copied thumbnail image)
```

`export_bundle` 是本地离线打包器 — 不会上传。联网发布器（例如 YouTube uploader）将是独立的 `publish` capability 提供方。

### 步骤 6：构建 Publish Log

`export_bundle` 已在 `data["publish_log"]` 中返回符合 schema 的 `publish_log` — 直接持久化即可，勿手工拼装。不要添加额外 entry 字段（schema 设置 `additionalProperties: false`；仅允许 `platform`、`status`、`url`、`video_id`、`visibility`、`export_path`、`timestamp`、`metadata_used`、`error`）。其返回形态如下：

```json
{
  "version": "1.0",
  "entries": [
    {
      "platform": "youtube",
      "status": "exported",
      "export_path": "projects/vector-db-explainer/exports",
      "timestamp": "2026-01-15T10:30:00+00:00",
      "metadata_used": {
        "title": "Vector Databases Explained in 60 Seconds",
        "description": "What vector databases are and when to use them.",
        "hashtags": ["#ai", "#vectordb"],
        "chapters": [{ "start_seconds": 0, "title": "Introduction" }]
      }
    }
  ]
}
```

### 步骤 7：自评

打分（1–5）：

| 标准 | 问题 |
|-----------|----------|
| **SEO 质量** | 该标题与描述是否能在该主题下获得较好排名？ |
| **描述完整性** | 描述是否包含章节、CTA 与关键词？ |
| **缩略图概念** | 该缩略图在信息流中是否足够醒目？ |
| **导出包** | 导出目录是否包含创作者所需的一切？ |
| **平台适配** | 元数据是否针对目标平台定制？ |

任一维度低于 3 分则修订。

### 步骤 8：提交

对照 schema 校验 publish_log，并通过 checkpoint 持久化。

## 常见陷阱

- **泛泛的标题**：「关于 X 的视频」永远输给「X Explained in 60 Seconds」。要具体、有吸引力。
- **无章节**：YouTube 会奖励带章节的视频。务必包含。
- **描述关键词堆砌**：先为人写，再兼顾搜索。自然语言中融入关键词。
- **忘记 CTA**：每条描述都应以行动号召结尾。
- **平台格式错误**：YouTube 描述与 TikTok  caption 不同。按目标平台定制。

---

## 门禁提醒（具有约束力）

本阶段需人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染产物），并**结束本轮**。勿在同一回复中启动下一阶段。
批准按门禁单独生效 — 此前「继续」不覆盖本门禁。
