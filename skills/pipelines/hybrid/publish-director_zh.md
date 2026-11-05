# 发布总监 - 混合流水线

## 何时使用

打包混合流水线的产出，使主片（hero cut）及其衍生版本保持有序，且源素材与支持素材的混合关系清晰可辨。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | 制品校验 |
| 前置制品 | `state.artifacts["compose"]["render_report"]`、`state.artifacts["idea"]["brief"]`、`state.artifacts["script"]["script"]` | 最终输出与混合框架 |
| Playbook | 当前启用的风格 playbook | 调性一致 |

## 流程

### 1. 区分主片与变体

将输出分组为：

- 主片（master cut），
- 短内容衍生版，
- 格式变体，
- 分章节或上下文变体。

### 2. 在打包中保留源素材真实性

若项目以访谈素材、录屏或产品实拍为锚点，元数据应如实反映这一点，而不是按纯生成内容的方式打包。

### 3. 存储跨输出说明

建议的元数据键：

- `master_output`
- `derivative_outputs`
- `source_mix_notes`
- `platform_copy_map`

### 4. 质量门

- 主片与变体标注清晰，
- 元数据与真实的源素材混合一致，
- 导出目录按用途组织，
- 整包可直接使用，无需手工整理。

## 常见陷阱

- 掩盖哪一条输出是主片（hero cut）。
- 将以源素材为主导的项目打包成泛化的生成资产。
- 在各变体之间丢失平台专属文案与标注。

---

## 门控提醒（强制）

本阶段需经人工审批（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做检查点，呈现摘要（Backlot 看板会渲染该制品），并**结束本轮回复**。勿在同一轮回复中启动下一阶段。
审批按门控逐项进行——此前「继续」的许可不覆盖本门控。
