# Publish Director - Avatar 发言人管线

## 适用场景

将完成的 spokesperson 产出打包交付。本阶段应明确哪份文件是 hero 主片、哪些是衍生版本，以及各版本所服务的讯息或受众。

## 流程

### 1. 清晰标注交付物

区分：

- hero 主片，
- 竖版精简版（vertical cutdown），
- 方形精简版（square cutdown），
- 语言变体，
- 水印或审阅版本。

### 2. 以讯息为导向的元数据

建议的元数据键：

- `audience_segment`
- `cta_copy`
- `offer_name`
- `locale`
- `thumbnail_concept`

### 3. 打包审阅说明

若 avatar 路径存在局限（例如可见的口型同步风险），应在交付包中保留该说明，而非隐藏。

### 4. 质量门禁

- 导出文件命名清晰，
- 元数据与预期讯息一致，
- 海报帧或缩略图概念能清晰呈现主讲人，
- 审阅说明随交付包一并保留。

## 常见陷阱

- 未清晰命名即混放 hero 与衍生导出。
- 复用忽略 spokesperson offer 的通用元数据。
- 丢弃对下游发布团队重要的风险说明。

---

## 门禁提醒（具有约束力）

本阶段以人工审批为门禁（`human_approval_default: true`）。审阅通过后：
以 `status="awaiting_human"` 做 checkpoint，呈现摘要（Backlot 看板会渲染该 artifact），并**结束本轮**。勿在同一回复中启动下一阶段。
审批按门禁单独生效——此前「继续」的口头许可不覆盖本门禁。
