# 场景导演（Scene Director）- 播客再利用流水线

## 何时使用

你需要根据实际的源素材模式，决定每个播客交付物应呈现何种视觉形态。在此阶段要避免「虚假丰富度」，并选择诚实、有效的呈现方式。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | 产物（Artifact）校验 |
| 前置产物 | `state.artifacts["script"]["script"]`, `state.artifacts["idea"]["brief"]` | 高光片段集合与源素材事实 |
| 工具 | `frame_sampler` | 可选：对视频播客源进行视觉检视 |
| Playbook | 当前启用的风格 Playbook | 品牌一致性 |

## 流程

### 1. 为每个交付物选择合适呈现方式

优先遵循「忠于源素材」的层级：

- 若存在视频播客素材，优先使用以讲者为主的场景；
- 若仅有音频，使用 audiogram 或以引用为主的版式；
- 若品牌资产有限，保持视觉系统简洁且可复用。

### 2. 避免伪复杂度

除非预算与工具支持，不要规划整集大量生成式主题图。简洁、带品牌标识的伴读版式，优于嘈杂、力有不逮的伪制作感。

### 3. 定义场景族（Scene Families）

Schema 中常用的场景类型：

- `talking_head`：源视频中的讲者镜头
- `text_card`：引用卡与章节卡
- `generated`：可选的主题艺术图
- `diagram`：讨论确实需要图示的少数情况
- `transition`：章节过渡

### 4. 用元数据描述版式策略

推荐的 `scene_plan.metadata` 键：

- `deliverable_layouts`
- `speaker_card_rules`
- `quote_card_rules`
- `audiogram_rules`
- `full_episode_companion_rules`

### 5. 规划安全区与署名

每种版式都应明确保留：

- 讲者署名（speaker attribution），
- 字幕区域，
- 节目品牌标识，
- 如有需要，CTA 或单集引用区域。

### 6. 质量门禁

- 每个交付物的呈现方式与实际源素材一致；
- 存在源视频时优先使用，而非用泛化图形掩盖；
- 纯音频资产在视觉上保持简洁、可读；
- 长形式伴读视觉方案可落地执行。

## 常见陷阱

- 对纯音频单集仍规划以讲者为中心的版式。
- 把每个片段都做成相同的波形加 logo 合成。
- 用生成图形掩盖薄弱的编辑决策。

---

## 门禁提醒（具有约束力）

本阶段需经人工审批（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 做 checkpoint，展示摘要（Backlot 看板会渲染该产物），并**结束本轮回复**。勿在同一回复中启动下一阶段。
审批按门禁逐项进行——此前说的「继续」不覆盖本门禁。
