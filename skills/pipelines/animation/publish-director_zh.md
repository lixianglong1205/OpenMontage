# 发布总监 — 动画流水线

## 何时使用

将动画打包，使元数据、缩略图概念与平台呈现方式能反映项目实际的视觉体系。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["compose"]["render_report"]`, `state.artifacts["proposal"]["proposal_packet"]`, `state.artifacts["research"]["research_brief"]`, `state.artifacts["script"]["script"]` | 最终输出与主题框架 |
| Playbook | 当前启用的风格 playbook | 视觉命名一致性 |

## 流程

### 1. 使包装与动画模式一致

示例：

- 图表为主的视频应呈现结构化、易读的外观，
- kinetic-type（动态文字）类作品应围绕强文案进行包装，
- 插画类动画应围绕主视觉画面进行包装。

### 2. 保持视觉体系的真实性

写入 `publish_log.metadata`：

- `animation_mode`
- `hero_frame_notes`
- `thumbnail_concept`
- `platform_notes`

### 3. 质量门禁

- 元数据与实际动画模式一致，
- 缩略图概念与最终视觉体系匹配，
- 导出文件按用途与平台清晰标注，
- 打包结果可直接使用，无需额外手工整理。

## 常见陷阱

- 撰写忽略动画风格的泛化元数据。
- 缩略图概念与最终帧画面无关。
- 混用各平台变体却未清晰标注。

---

## 门禁提醒（具有约束力）

本阶段需经人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 创建 checkpoint，呈现摘要（Backlot 看板会渲染该产物），并**结束本轮回复**。勿在同一轮回复中启动下一阶段。
批准按门禁单独生效——此前「继续」的口头许可不涵盖本门禁。
