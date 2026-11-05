# 内部风格指南（House Style）

在未提供设计规范（`frame.md` 或 `design.md`）时，用于指导作品创意方向的默认准则。这些是起点——凡是不服务于内容的条目都可以覆盖。若已有设计规范，则以其中的品牌取值为准；内部风格指南用于填补空白。

## 编写 HTML 之前

1. **解读提示词。** 生成真实内容。食谱应列出真实配料；HUD 应有真实读数。
2. **选定配色。** 浅色还是深色？在写代码前先声明 bg、fg、accent。
3. **选定字体。** 运行 [references/typography.md](references/typography.md) 中的字体发现脚本——或选用你已熟悉、且契合主题的字体。脚本用于拓宽选择面，并非唯一来源。

## 需要质疑的「惰性默认」

以下模式是 AI 设计的典型痕迹——也是多数大模型会优先套用的套路。若你正要使用其中一项，先停一下问：这是针对**本**内容的有意选择，还是在走默认？

- 渐变文字（`background-clip: text` + 渐变）
- 卡片/标注左侧色条强调
- 深色底上的青色文字 / 紫到蓝渐变 / 霓虹强调色
- 纯 `#000` 或 `#fff`（中性色宜向你的 accent 色相微调）
- 完全相同的卡片网格（同尺寸卡片重复排列）
- 全部居中、权重均等（应引导视线落点）
- 禁用字体（完整列表见 [references/typography.md](references/typography.md)）

若内容确实需要其中某种——例如庄重收束用居中布局、真实产品 UI mockup 用卡片、或某禁用字体恰是主题最佳匹配——可以使用。目标是**有意图**，而非机械回避。

## 色彩

- 明暗与内容匹配：美食、康养、儿童向 → 浅色。科技、电影、金融 → 深色。
- 单一 accent 色相。所有场景背景一致。
- 中性色向 accent 微调（哪怕轻微冷暖也比死灰更好）。
- **对比度：** 由 `hyperframes validate` 强制执行（WCAG AA）。去掉装饰后文字仍须可读。
- 事先声明配色。不要按元素临时发明颜色。

## 背景层

每个场景都需要视觉纵深——在内容入场动画进行时仍保持可见的持久装饰元素。缺少这些时，入场错峰阶段会显得空洞。

思路（可混搭，每场景 2–5 种）：

- 径向光晕（accent 色调、低不透明度、呼吸式缩放）
- 幽灵文字（主题词 3–8% 不透明度、超大字号、缓慢漂移）
- accent 线条（发丝级规则线、轻微脉冲）
- 颗粒/噪点叠加、几何形、网格图案
- 主题装饰（太空用轨道环、音乐用沟槽纹、数据用网格线）

所有装饰应有缓慢的 GSAP 环境动画——呼吸、漂移、脉冲。静态装饰会显得「死」。

**装饰数量 vs 动效数量。** 「每场景 2–5 种」指装饰**元素**的数量。若项目设计规范写「每场景单一环境动效」，意指这些装饰共用一条循环动效（共享呼吸/漂移/脉冲）——而非整个场景只有一个元素。四个装饰共享一次呼吸动效是合理的；只有一个装饰则显得欠装饰。

## 动效

完整规则见 [references/motion-principles.md](references/motion-principles.md)。速记：0.3–0.6s、变化缓动、入场组合多种 transform、条目重叠。

## 排版

完整规则见 [references/typography.md](references/typography.md)。速记：标题 700–900 / 正文 300–400，衬线 + 无衬线（不要两个无衬线），标题 60px+ / 正文 20px+。

## 配色方案

写 HTML 前先声明一个 background、一个 foreground、一个 accent。

| 类别              | 适用场景                                       | 文件                                                       |
| ----------------- | ---------------------------------------------- | ---------------------------------------------------------- |
| 大胆 / 活力       | 产品发布、社交媒体、公告                         | [palettes/bold-energetic.md](palettes/bold-energetic.md)   |
| 温暖 / 编辑风     | 叙事、纪录片、案例研究                           | [palettes/warm-editorial.md](palettes/warm-editorial.md)   |
| 深色 / 高端       | 科技、金融、奢华、电影感                         | [palettes/dark-premium.md](palettes/dark-premium.md)       |
| 简洁 / 企业风     | 讲解、教程、演示                                 | [palettes/clean-corporate.md](palettes/clean-corporate.md) |
| 自然 / 大地       | 可持续、户外、有机                               | [palettes/nature-earth.md](palettes/nature-earth.md)       |
| 霓虹 / 电光       | 游戏、科技、夜生活                               | [palettes/neon-electric.md](palettes/neon-electric.md)     |
| 粉彩 / 柔和       | 时尚、美妆、生活方式、康养                       | [palettes/pastel-soft.md](palettes/pastel-soft.md)         |
| 宝石色 / 浓郁     | 奢华、活动、精致格调                             | [palettes/jewel-rich.md](palettes/jewel-rich.md)           |
| 单色              | 戏剧感、以排版为主                               | [palettes/monochrome.md](palettes/monochrome.md)           |

或从 OKLCH 推导——选定色相，在不同明度（lightness）上构建 bg/fg/accent，并将整体向该色相微调。
