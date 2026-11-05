# 品味方向 - 元技能

## 何时使用

在确定视觉识别、情绪板、提案包、自定义 playbook、atelier 合成、图像参考批次或品牌导向较重的视频之前使用本技能。

本技能定义 OpenMontage 的视频品味配置（taste profile）契约。不要将其当作前端样式配方。输出是一份紧凑的视频品味配置，贯穿提案、场景规划、资产提示、剪辑、合成与审阅。

## 输出契约

当提案或 playbook 需要更强的创意契约时，编写 `taste_profile`：

```json
{
  "design_read": "Premium expert explainer: calm authority, high trust, low ornament.",
  "visual_variance": 4,
  "motion_intensity": 3,
  "information_density": 5,
  "palette_discipline": "Neutral base, one accent, no decorative gradients.",
  "layout_variation": "Alternate editorial split frames with data-forward full-frame scenes.",
  "reference_strategy": "One reference still per scene family before asset generation.",
  "anti_patterns": ["generic AI-purple gradient backgrounds"],
  "quality_gates": ["Every scene should carry the design read without explanatory labels."]
}
```

`visual_variance`、`motion_intensity` 与 `information_density` 为 1–10 的整数拨盘：

| 拨盘 | 低 | 中 | 高 |
|------|-----|-----|------|
| `visual_variance` | 紧凑体系，重复语法 | 有目的的场景族模式 | 每个节拍可采用不同视觉模式 |
| `motion_intensity` | 平静定格、小幅转场 | 清晰动效点缀与揭示 | 快速动感语言，频繁方向变化 |
| `information_density` | 每帧一个想法 | 主想法加支撑细节 | 密集仪表盘、图表或分层标注 |

## 流程

### 1. 做出设计解读（Design Read）

在选择 playbook 或色板之前，说明视频需要呈现何种感受及原因。与受众、承诺、平台与主题挂钩。

好的解读具体：

- 「面向投资者的 AI 发布：精确、克制、可信；避免浮夸视觉。」
- 「青少年科学短片：明亮、好奇、动感；让不可见的物理变得可触。」
- 「安全事件说明：紧张而精准；高对比、低装饰、证据可读。」

弱的解读只有形容词：

- 「现代且干净」
- 「电影感」
- 「专业」

### 2. 设定三个拨盘

在写概念之前选定 `visual_variance`、`motion_intensity` 与 `information_density`。这些数字应解释后续选择：

- 高动效加低信息密度意味着短促动感节拍，而非密集图表。
- 低动效加高信息密度意味着稳定画面、图表构建与较长可读定格。
- 高方差意味着场景族需要更强锚点：反复出现的字体、色板、构图或声音母题。

### 3. 选择风格路径

用拨盘在三条路径中选一：

| 路径 | 适用情形 | 产出物 |
|------|----------|--------|
| 现有 playbook | 某预设诚实匹配设计解读 | `production_plan.playbook` |
| 自定义 playbook | 主题自有视觉世界 | 生成的 `styles/<name>.yaml`，含 `taste_profile` |
| Atelier 艺术指导 | 重点作品需要一次性语言 | `production_plan.art_direction` 加 `taste_profile` |

不要让预设可用性压过设计解读。若内容需要自定义视觉世界，应编写自定义 playbook 或艺术指导。

### 4. 规划参考

若工作涉及 AI 图像/视频、情绪板、品牌资产或 atelier 合成，制定参考策略：

- 每个场景族或主要节拍使用一张参考静帧。
- 不要把整个方向压缩成一张情绪板图。
- 品牌/产品类工作，在资产生成前创建或检查 brand kit。
- 屏幕演示类，在样式化叠加层之前检查真实 UI 并撰写 redesign/audit 说明。

### 5. 将配置向下游传递

提案阶段：

- 添加 `production_plan.taste_profile`。
- 在 `decision_log` 中记录风格/playbook 选择。
- 说明拨盘如何影响时长、合成模式与资产生成。

场景规划阶段：

- 按 `visual_variance` 变化布局。
- 将屏上文字与标注控制在 `information_density` 范围内。
- 由 `motion_intensity` 设定转场族与镜头运动。

资产阶段：

- 在图像/视频提示中包含色板、质感、构图与参考策略。
- 当配置依赖视觉细微差别时，在全量批次前生成参考静帧。

剪辑/合成阶段：

- 将定格时长与切点节奏与动效拨盘对齐。
- 避免添加违反设计解读的装饰性叠加层。

## 反默认清单

继续推进前标记以下项：

- 无主题理由的通用 AI 紫色渐变或默认 corporate-blue 视觉。
- 当 `visual_variance` 为 4 或更高时，每个切点使用相同转场。
- 使旁白更难跟上的强动感动效。
- 当 `information_density` 为 4 或更低时仍使用密集标注。
- 除非设计解读刻意要求字体叙事，否则纯文字幻灯片。
- 好看但无法映射到具体场景族的情绪板。
- 从未展示或检查真实品牌/产品表面的品牌/产品视频。

## 审阅挂钩

审阅者应检查：

- `taste_profile.design_read` 是否解释了真实的创意选择？
- 场景规划与剪辑是否尊重三个拨盘？
- 反模式是否确实被避免？
- 当 AI 图像/视频或 atelier 工作依赖视觉细微差别时，参考策略是否存在？
- 换掉标题后，该视频是否仍可属于任意主题？若是，则品味方向过于泛化。
