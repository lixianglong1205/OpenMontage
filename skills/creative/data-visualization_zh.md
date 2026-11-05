# 数据可视化策略技能

## 何时使用

当场景需要以视觉方式呈现数据时使用本技能：统计、对比、趋势、构成或关键指标。本技能指导图表类型选择、动画时序、标签布局、数据密度与配色，以产出在视频中清晰、准确且有效的图表。

## 工具

| 工具 | 角色 |
|------|------|
| `diagram_gen` | 通过 Mermaid 或 D3 生成图表 |
| `image_selector` | 生成风格化图表插图（FLUX/GPT Image） |
| Remotion | 动画图表组件（柱形生长、折线绘制、饼图填充） |
| Manim | 数学绘图、坐标系、函数图像 |

## 图表类型决策树

自上而下遵循此树。在第一个匹配处停止。

```
Is there data to visualize?
  NO  -> Use a text card or stat card instead
  YES -> How many data points?
           < 3 -> Use text or stat card (charts look empty with 1-2 points)
           3-9 -> Continue to "What story does the data tell?"
           > 12 -> Simplify first: aggregate into top-N + "Other", then continue

What story does the data tell?
  |
  |-- Comparing quantities across categories?
  |     -> BAR CHART (horizontal if labels are long)
  |
  |-- Showing a trend over time?
  |     -> LINE CHART (area chart if showing volume)
  |
  |-- Showing parts of a whole?
  |     -> PIE / DONUT CHART (max 5-6 slices)
  |     (If > 6 categories, aggregate smallest into "Other")
  |
  |-- Showing key metrics / KPIs?
  |     -> KPI GRID (3-6 stat cards in a grid layout)
  |
  |-- Showing ranking or ordered list?
  |     -> HORIZONTAL BAR CHART (sorted descending)
  |
  |-- Showing before/after or change?
  |     -> PAIRED BAR CHART or STAT CARD with delta arrow
  |
  |-- Showing correlation between two variables?
  |     -> LINE CHART with dual series (avoid scatter in video -- too dense)
  |
  |-- None of the above?
  |     -> Default to BAR CHART (most universally readable)
```

### 何时不要用图表

| 情况 | 改用 |
|-----------|----------------|
| 少于 3 个数据点 | 统计卡片或文字叠加：「Revenue grew 40% to $2.1M」 |
| 超过 12 个类别 | 聚合为前 5–7 项 +「Other」，再制图 |
| 只需强调单个数字 | 全屏统计卡片配合冲击型动画 |
| 定性对比 | 并排图片或文字表格 |
| 数据需 30 秒以上才能读完 | 拆成多个更简单的图表，分布在多个场景 |

## 动画时序

视频中的每张图表都应有动画。静态图表像幻灯片，不像视频。

### 模式：逐步构建（默认）

先显示空坐标轴/框架，再动画呈现数据。

```
Frame 0.0s: Empty chart frame (axes, title, gridlines visible)
Frame 0.3s: First data element begins animating in
Frame 2.0s: All data elements fully rendered
Frame 2.0-5.0s: Hold for readability
```

- **柱形图：** 柱从基线向上生长（从左到右错开，每项延迟 0.1s）
- **折线图：** 沿数据路径从左向右绘制
- **饼图/环形图：** 从 12 点方向顺时针填充扇区，最大扇区优先
- **KPI 网格：** 数字从 0 计数到最终值（里程表效果）

### 模式：叙事高亮

旁白提到某元素时，逐个高亮。

```
Frame 0.0s: Full chart visible but all elements at 30% opacity (desaturated)
Frame 0.5s: First highlighted element goes full color + slight scale-up
Frame 3.0s: First element returns to normal, second element highlights
...continue for each narrated point
```

旁白逐条讲解数据点时使用。使观众注意力与旁白同步。

### 模式：对比揭示

先显示基线，再动画呈现变化。

```
Frame 0.0s: Baseline data visible (e.g., "Before" bars)
Frame 2.0s: Hold baseline for comprehension
Frame 2.5s: Animate change (bars grow/shrink to "After" values)
Frame 3.5s: Delta labels appear (+40%, -15%, etc.)
Frame 3.5-7.0s: Hold for readability
```

用于前后对比、同比或 A/B 对比。

### 时序规则

| 元素 | 动画时长 | 保持时长 |
|---------|-------------------|---------------|
| 图表构建 | 2–4 秒 | 3–5 秒 |
| 单元素高亮 | 0.3–0.5 秒 | 2–3 秒 |
| 对比过渡 | 1–2 秒 | 3–5 秒 |
| KPI 计数 | 1.5–2 秒 | 2–3 秒 |
| 标签/标注出现 | 0.2–0.3 秒 | 保持在画面上 |

**关键规则：** 场景切换前，图表必须完全构建完成并至少保持 3 秒。观众需要时间阅读。若旁白在图表可读之前已继续，要么延长场景，要么简化图表。

## 标签布局规则

### 柱形图

```
Vertical bars:
  - Value labels: ABOVE each bar (or INSIDE if bar is tall enough for legible text)
  - Category labels: Below on x-axis, horizontal text
  - If labels overlap: rotate 45 degrees or use horizontal bars instead
  - Y-axis: include gridlines, omit axis label if title makes it obvious

Horizontal bars:
  - Value labels: TO THE RIGHT of each bar
  - Category labels: Left-aligned on y-axis
  - Preferred when category names are longer than 2 words
```

### 折线图

```
  - Endpoint labels: Show value at the last data point (right end)
  - Start label: Show value at the first data point (left end) for context
  - Dense data (>7 points): Label only start, end, and notable peaks/valleys
  - Avoid: Labels on every point (creates clutter in video)
  - Legend: Top-right or inline (label next to the line) for multi-series
```

### 饼图 / 环形图

```
  - Large slices (>= 10%): Label INSIDE the slice (percentage + category)
  - Small slices (< 10%): Label OUTSIDE with leader line connecting to slice
  - Center of donut: Use for total value or key metric label
  - Maximum: 5-6 slices. Combine anything under 5% into "Other"
  - Always show percentages, not just raw values
```

### KPI 网格

```
  - Large number: Center of each card, using stat_card font (3-4x body size)
  - Label: Below the number, smaller font, describes the metric
  - Delta indicator: Small arrow + percentage showing change (green up, red down)
  - Grid: 2x2 or 3x2 layout, evenly spaced, consistent card sizing
```

### 通用标签规则

- **标题可见：** 每张图表必须有清晰标题（左上或顶部居中）
- **来源标注：** 若数据来自外部，在底部小字显示「Source: [name]」
- **单位：** 始终在标题或坐标轴上显示单位（%、$、秒等）
- **无孤立标签：** 每个视觉元素都需有标签或由旁白说明

## 数据密度与可读性

### 视频法则：少即是多

视频不是电子表格。观众无法暂停、滚动或缩放。每个数据点都在 5–7 秒窗口内争夺注意力。

```
Ideal data points per chart type:
  Bar chart:     5-7 bars (max 9)
  Line chart:    5-12 points (max 15, but label sparsely)
  Pie chart:     3-5 slices (max 6)
  KPI grid:      3-6 metrics (max 6)
```

### 简化策略

| 问题 | 解决方案 |
|---------|----------|
| 类别过多（>9） | 显示前 5–7 项，其余聚合为「Other」 |
| 时间点过多 | 聚合（月→季，日→周） |
| 需展示多个指标 | 拆成多个场景中的独立图表 |
| 数值范围跨度大 | 用归一化/百分比视图代替绝对值 |
| 小数精度 | 积极四舍五入：$1,234,567 -> $1.2M |

### 字号下限（1080p）

在含手机在内的屏幕上可读，以下为不可妥协的下限：

| 元素 | 最小字号 | 推荐 |
|---------|-------------|-------------|
| 图表标题 | 32px | 36–40px |
| 坐标轴标签 | 24px | 28px |
| 数值标签 | 24px | 28px |
| 标注 | 20px | 24px |
| 来源标注 | 16px | 18px |

**缩放规则：** 4K 输出乘以 2x。720p 仍适用上述最小值（作为底线）。

## 配色

### 从 Playbook 推导图表色

图表必须看起来属于该视频。始终从当前 style playbook 推导颜色。

```
Color derivation priority:
  1. playbook.visual_language.color_palette.chart_palette  (if the playbook defines one)
  2. Derive from primary + accent colors:
       - Bar/slice 1: primary[0]
       - Bar/slice 2: accent[0]
       - Bar/slice 3: primary[1]
       - Bar/slice 4: accent[1]
       - Bar/slice 5+: generate by adjusting lightness of primary[0]
  3. Background: use playbook background color
  4. Text/labels: use playbook text color
  5. Gridlines: use playbook muted color at 50% opacity
```

### 高亮与焦点

```
Highlighting strategy:
  - KEY data point:    Full saturation of accent[0], slight scale-up (1.05x)
  - FOCUS data points: Full saturation of their assigned color
  - NON-FOCUS points:  Desaturate to 30% opacity or use muted color
  - BASELINE/CONTEXT:  Dashed lines using muted color
```

### 无障碍规则

切勿仅靠颜色传达含义：

- **添加图案：** 柱/扇区除颜色外使用 hatch、点或条纹
- **添加标签：** 每根柱/每个扇区/每条线都需文字标签，不能仅靠图例
- **对比度：** 相邻图表元素至少 3:1 对比度
- **色盲友好：** 避免仅用红绿区分。表示正负时优先蓝橙或蓝黄配对

## 常见陷阱

### 误导性图表

| 陷阱 | 为何误导 | 修正 |
|---------|----------------|-----|
| 截断 y 轴（不从 0 起） | 小差异显得巨大 | 柱形图 y 轴始终从 0 开始 |
| 3D 图表 | 透视扭曲大小感知 | 始终使用 2D 平面图表 |
| 双 y 轴不同刻度 | 暗示虚假相关 | 并排两张独立图表 |
| 刻意选取的时间范围 | 隐藏更大背景 | 显示完整相关区间或注明截断 |
| 饼图扇区过多 | 小角度无法比较 | 最多 5–6 扇区，其余聚合 |

### 动画错误

| 陷阱 | 修正 |
|---------|-----|
| 动画过快（< 1.5s） | 观众跟不上出现内容。构建至少 2s |
| 动画后无保持 | 场景切走前图表不可读。至少保持 3–5s |
| 所有元素同时出现 | 失去叙事。错开元素入场 |
| 无意义弹跳/旋转 | 分散对数据的注意力。按 playbook 使用干净 ease-in-out |

### 设计错误

| 陷阱 | 修正 |
|---------|-----|
| 颜色过多（单图 >5） | 限制 4–5 种不同颜色。聚合或拆图 |
| 缺少标题 | 每张图都需要标题。观众无其他上下文 |
| 手机上字过小 | 强制下限：1080p 标题 32px、标签 24px |
| 装饰性网格线 | 用浅色网格或无。应辅助阅读，非装饰 |
| 深底深字 | 用 playbook 文字色与背景色。检查对比度 |

## 与 Scene Director 集成

当 Scene Director 识别到数据可视化需求时，按以下方式应用本技能：

1. **确定图表类型** — 使用上文决策树
2. **在场景的 `movement` 字段指定动画模式**（例如「build-up: bars grow from baseline over 2s, hold 4s」）
3. **在 `overlay_notes` 中包含标签规格**（例如「value labels above bars, title top-left, source bottom-right」）
4. **在 `required_assets` 描述中引用 playbook 颜色**（例如「bar chart using primary[0] #2563EB for main bars, accent[0] #F59E0B for highlight bar」）
5. **设置场景时长** 以容纳动画（2–4s）+ 保持（3–5s）= 每个图表场景至少 5s

### 场景规格示例

```json
{
  "id": "scene-7",
  "type": "animation",
  "description": "Horizontal bar chart comparing response times: Traditional DB 450ms, Vector DB 12ms, Cached 3ms. Bars grow left-to-right with stagger. Vector DB bar highlighted in accent color. Hold for readability.",
  "start_seconds": 32,
  "end_seconds": 40,
  "script_section_id": "s5",
  "framing": "full-screen chart, centered with generous padding",
  "movement": "build-up: bars grow from left over 2.5s with 0.3s stagger, hold 5s",
  "transition_in": "fade",
  "transition_out": "dissolve",
  "overlay_notes": "Title: 'Query Response Time Comparison'. Value labels right of bars (ms units). Source: 'Benchmark 2024' bottom-right 16px. Vector DB bar uses accent[0], others use primary[0] at 50% opacity.",
  "required_assets": [
    {
      "type": "chart_data",
      "description": "Horizontal bar chart data: Traditional DB 450ms, Vector DB 12ms, Cached 3ms. Use playbook primary #2563EB at 50% for context bars, accent #F59E0B for Vector DB highlight bar.",
      "source": "generate"
    }
  ]
}
```

## 质量检查清单

- [ ] 图表类型匹配数据故事（而非仅「默认柱形图」）
- [ ] 数据点在限制内：5–7 柱、3–5 饼扇区、5–12 折线点
- [ ] 动画时长：构建 2–4s，保持至少 3–5s
- [ ] 所有文字满足字号下限：1080p 标题 32px、标签 24px
- [ ] 颜色来自当前 playbook 调色板
- [ ] 关键数据点有视觉强调（高亮色、缩放或标注）
- [ ] 不单独依赖颜色传达含义（标签 + 图案以保障无障碍）
- [ ] 柱形图 y 轴从 0 开始
- [ ] 无 3D 效果或透视扭曲
- [ ] 标题可见且描述清楚
- [ ] 使用外部数据时注明来源
- [ ] 在保持期内任意帧暂停时图表仍可读
