# 发布导演 - Screen Demo 流水线

## 何时使用

将完成的演示打包，使用户能快速发布，并使元数据反映实际任务、结果与所用工具。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["compose"]["render_report"]`, `state.artifacts["idea"]["brief"]`, `state.artifacts["script"]["script"]` | 视频、简报与章节 |
| Playbook | 当前启用的风格 playbook | 缩略图与文案调性 |

## 流程

### 1. 构建可检索元数据

Screen-demo 标题在组合以下要素时效果最好：

- 任务，
- 工具，
- 结果。

良好模式示例：

- `How to deploy on Vercel from Next.js`
- `Fix CORS in React + Express`
- `Set up GitHub Actions for Python tests`

从以下来源提取关键词：

- 软件名称，
- 框架，
- 命令，
- 精确错误文本，
- 结果类词汇，如 `deploy`、`fix`、`connect`、`publish`、`ship`。

### 2. 用章节标记作为导航

以脚本章节为章节标记与打包要点的基础。优质的 screen-demo 包装应让用户在未播放前即可快速浏览工作流。

### 3. 缩略图策略

若需要缩略图概念，应呈现：

- 结果状态，而非泛化的设置界面，
- 可识别的工具界面，
- 2–4 个字的 value 文案。

将概念存入 `publish_log.metadata.thumbnail_concepts`。

### 4. 按平台打包

准备：

- 视频文件，
- 标题与描述/说明文案，
- 适用的章节标记，
- 关键词列表，
- 缩略图概念说明。

针对开发者或产品演示内容，还需打包：

- 展示的命令，
- 软件/版本提及，
- 若为排障演示，则包含错误相关术语。

### 5. 质量门

- 元数据标明真实工具与任务，
- 章节与实际上屏流程一致，
- 导出目录整洁且可复用，
- 文案按平台定制，而非复制粘贴。

## 常见陷阱

- 使用泛化标题发布，未体现实际软件或任务。
- YouTube、LinkedIn 与短视频平台使用同一段说明文案。
- 仅依据脚本构建章节标记，未对照成片校验。

---

## 门控提醒（具约束力）

本阶段需人工审批（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 设置 checkpoint，呈现摘要（Backlot 看板会渲染产物），并**结束本轮**。勿在同一回复中启动下一阶段。
审批按门控逐项进行——此前「继续」的同意不覆盖本门控。
