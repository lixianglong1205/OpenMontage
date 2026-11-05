# Publish Director - 播客再利用流水线

## 适用场景

将播客衍生的片段与配套素材打包发布，使每条短视频都能指回整期节目，而不是作为孤立片段漂移流失。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["compose"]["render_report"]`、`state.artifacts["idea"]["brief"]`、`state.artifacts["script"]["script"]` | 输出、源真相、章节 |
| Playbook | 当前启用的风格 playbook | 品牌调性 |

## 流程

### 1. 将每条片段链回整期节目

每条短视频素材应包含以下引用信息：

- 节目名称，
- 单集标题或期号，
- 在相关时注明嘉宾姓名，
- 完整单集的落地页/收听入口。

### 2. 按平台定制文案

- Shorts / Reels / TikTok：以 hook 开头、简洁有力
- LinkedIn：以洞察为主、语境更完整
- YouTube 配套内容：章节丰富、利于搜索

### 3. 安排发布顺序

建议顺序：

1. 最强的官宣/预告类片段
2. 次优的洞察类片段
3. 金句或嘉宾主导的跟进片段
4. 其余支撑性片段

### 4. 在元数据中保存交叉链接信息

建议的元数据键：

- `episode_reference`
- `guest_tags`
- `posting_schedule`
- `clip_to_episode_map`

### 5. 质量门禁

- 每条片段都能指回整期节目，
- 嘉宾署名正确，
- 文案符合平台特性，
- 发布顺序反映片段实际强度。

## 常见陷阱

- 发布片段时缺少清晰的单集引用。
- 在受众关心嘉宾时忘记标注或提及嘉宾。
- 在所有平台复用同一套 caption 风格。

---

## 门禁提醒（具有约束力）

本阶段需经人工审批（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 创建 checkpoint，呈现摘要（Backlot 看板会渲染
对应产物），并**结束本轮**。不要在同一条回复中启动下一阶段。
审批按门禁单独生效——此前说的「继续」不覆盖本门禁。
