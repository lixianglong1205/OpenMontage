---
name: manim-composer
description: |
  触发条件：(1) 用户想制作教育/讲解类视频，(2) 用户有一个需要可视化的模糊概念，(3) 用户提到「3b1b 风格」或「像 3Blue1Brown 那样讲解」，(4) 用户想规划 Manim 视频或动画序列，(5) 用户要求「编排」或「规划」数学/科学可视化。

  将模糊的视频想法转化为逐场景的详细计划（scenes.md）。开展调研、就受众/范围/重点向用户澄清问题，并输出可直接用于 ManimCE 或 ManimGL 实现的完整场景规格。

  在编写任何 Manim 代码之前使用本技能。本技能负责规划视频；实现阶段请使用 manimce-best-practices 或 manimgl-best-practices。
---

## 工作流

### 阶段 1：理解概念

1. **深入调研主题**，再向用户提问
   - 使用网页搜索理解核心概念
   - 找出让该主题有趣的关键洞见
   - 找到「顿悟时刻」——学习者何时会豁然开朗
   - 记录需要纠正的常见误解

2. **确定叙事钩子**
   - 本视频要回答什么问题？
   - 观众为何应该关心？
   - 令人惊讶或反直觉的点是什么？

### 阶段 2：与用户澄清

提出有针对性的问题（不要一次问完——根据回答灵活调整）：

**受众与范围**
- 应假定观众具备怎样的数学/科学背景？（例如「懂微积分」或「高中代数」）
- 目标视频时长？（短：5–10 分钟，中：15–20 分钟，长：30 分钟以上）
- 应是独立成片还是系列中的一集？

**重点与深度**
- 有哪些方面需要强调或跳过？
- 偏证明还是偏直觉？
- 是否包含现实应用？

**风格偏好**
- 配色偏好？
- 旁白风格？（随意、正式、活泼）
- 是否已有特定的视觉隐喻？

### 阶段 3：创建 scenes.md

输出结构完整的 `scenes.md` 文件：

```markdown
# [Video Title]

## Overview
- **Topic**: [Core concept]
- **Hook**: [Opening question/mystery]
- **Target Audience**: [Prerequisites]
- **Estimated Length**: [X minutes]
- **Key Insight**: [The "aha moment"]

## Narrative Arc
[2-3 sentences describing the journey from confusion to understanding]

---

## Scene 1: [Scene Name]
**Duration**: ~X seconds
**Purpose**: [What this scene accomplishes]

### Visual Elements
- [List of mobjects needed]
- [Animations to use]
- [Camera movements]

### Content
[Detailed description of what happens, what's shown, what's explained]

### Narration Notes
[Key points to convey, tone, pacing notes]

### Technical Notes
- [Specific Manim classes/methods to use]
- [Any tricky implementations to note]

---

## Scene 2: [Scene Name]
...

---

## Transitions & Flow
[Notes on how scenes connect, recurring visual motifs]

## Color Palette
- Primary: [color] - used for [purpose]
- Secondary: [color] - used for [purpose]
- Accent: [color] - used for [purpose]
- Background: [color]

## Mathematical Content
[List of equations, formulas, or mathematical objects that need to be rendered]

## Implementation Order
[Suggested order for implementing scenes, noting dependencies]
```

## 3b1b 风格原则

编排场景时遵循以下原则：

### 视觉叙事
- **展示，而非仅讲述**——每个概念都需要视觉呈现
- **渐进揭示**——逐步增加复杂度，不要一次展示全部
- **视觉连续性**——在可能时用变换而非替换对象

### 节奏与韵律
- **为洞见留白**——给观众时间消化关键瞬间
- **变化节奏**——快序列与慢讲解交替
- **场景有收束**——每个场景都应感觉完整

### 数学之美
- **强调优雅**——突出数学出人意料的简洁或美感
- **联结多种表征**——同一概念用代数、几何、直觉等多种方式呈现
- **逐步抽象**——从具体出发，再推广

### 参与感技巧
- **提出问题**——在揭晓答案前激发好奇
- **承认难度**——「一开始这可能有点绕……」
- **庆祝顿悟**——让「啊哈时刻」显得来之不易

## 参考

- [references/narrative-patterns.md](references/narrative-patterns.md) - 常见 3b1b 叙事结构
- [references/visual-techniques.md](references/visual-techniques.md) - 有效的可视化模式
- [references/scene-examples.md](references/scene-examples.md) - scenes.md 示例摘录

## 模板

- [templates/scenes-template.md](templates/scenes-template.md) - 空白 scenes.md 模板
