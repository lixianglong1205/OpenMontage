# 发布总监（Publish Director）- Clip Factory 流水线

## 何时使用

本阶段将 clip 批次打包为分发计划。目标不只是导出文件，而是打造可用的内容引擎。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| 模式 | `schemas/artifacts/publish_log.schema.json` | 制品校验 |
| 前置制品 | `state.artifacts["compose"]["render_report"]`, `state.artifacts["idea"]["brief"]`, `state.artifacts["script"]["script"]` | 输出、排名与目标 |
| Playbook | 当前风格 playbook | 品牌调性 |

## 流程

### 1. 以最强 clip 打头阵

不要按时间顺序排期，应按排名排期。

首个发布的 clip 通常应为：

- 钩子最强的一条，
- 最干净、可独立成片的 clip，
- 与批次目标最对齐的 clip。

### 2. 按平台定制文案

各平台需要不同的语气与包装：

- TikTok / Reels：直接、快节奏、钩子先行
- Shorts：便于搜索、兼顾关键词
- LinkedIn：以洞察为主、更专业
- X：短、有力、适合观点表达

### 3. 清晰打包整批内容

按平台分组，并提供可直接粘贴的文本素材，而不仅是视频文件。

### 4. 保留批次事实

在 `publish_log.metadata` 中存储：

- `clip_catalog`
- `posting_order`
- `platform_copy_map`
- `schedule_notes`

### 5. 质量门禁

- 最强 clip 引领发布节奏，
- 字幕/说明文案按平台区分，
- 导出目录可直接使用、无需额外整理，
- 批次目录清晰关联排名、文件路径与发布意图。

## 常见陷阱

- 同一天发布整批内容。
- 所有平台共用同一条文案。
- 渲染完成后丢失排名/顺序逻辑。

---

## 门禁提醒（绑定）

本阶段需经人工审批（`human_approval_default: true`）。审核通过后：
以 `status="awaiting_human"` 设置检查点，呈现摘要（Backlot 看板会渲染该制品），并**结束本轮回复**。不要在同一条回复中启动下一阶段。
审批按门禁单独生效——此前说的「继续」不覆盖本门禁。
