---
name: flux-best-practices
description: BFL FLUX 图像生成模型综合指南。涵盖提示词编写、T2I、I2I、结构化 JSON、十六进制颜色、排版、多参考编辑，以及 FLUX.2 与 FLUX.1 系列模型的专项最佳实践。
metadata:
  author: Black Forest Labs
  version: "1.0.0"
  tags: flux, bfl, image-generation, prompting, t2i, i2i
---

# FLUX 最佳实践

在为任意 BFL FLUX 模型编写提示词时使用本技能，以获得最佳图像质量与准确的提示词理解。

> **扩展参考：** 本目录下的 [`AGENTS.md`](AGENTS.md) 是上游 FLUX 完整长文指南（来自 Black Forest Labs 的 vendored 版本）。它仅作为本技能的补充参考——`SKILL.md` 是可加载的入口与权威来源。它不会覆盖或扩展仓库根目录的 `AGENTS.md` / `AGENT_GUIDE.md`。

## 何时使用

- 为 FLUX.2 或 FLUX.1 模型创建提示词
- 文生图（Text-to-image，T2I）生成
- 使用 FLUX.2 模型进行图生图（Image-to-image，I2I）编辑
- 使用 JSON 的结构化场景生成
- 排版与文字渲染
- 多参考风格迁移
- 颜色精确的品牌化生成

## 快速参考

### 提示词结构公式

```
[Subject] + [Action/Pose] + [Style/Medium] + [Context/Setting] + [Lighting] + [Camera/Technical]
```

### 模型选择

| 使用场景       | 推荐模型          | 说明                                   |
| -------------- | ----------------- | -------------------------------------- |
| 最快生成       | FLUX.2 [klein]    | 4B 或 9B，亚秒级                       |
| 最高质量       | FLUX.2 [max]      | 最佳细节，支持 grounding search        |
| 生产级平衡     | FLUX.2 [pro]      | 质量与速度兼顾                         |
| 排版/文字      | FLUX.2 [flex]     | 最佳文字渲染                           |
| 本地/开发      | FLUX.2 [dev]      | 开放权重                               |
| 图像编辑       | FLUX.2 [pro/max]  | 将图像 URL 直接传入 input_image        |
| 局部重绘       | FLUX.1 Fill       | 物体移除/补全                          |
| 上下文编辑     | FLUX.1 Kontext    | 较旧模型，优先选用 FLUX.2              |

### 关键规则

1. **不使用负向提示词** - FLUX 不支持负向提示词；请描述你想要的内容
2. **要具体** - 模糊的提示词只会得到平庸结果
3. **使用自然语言** - 散文/叙事风格效果最佳
4. **指定光照** - 光照对质量影响最大
5. **引用文字** - 排版渲染时使用带引号的 `"quoted text"`
6. **十六进制颜色** - 使用 #RRGGBB 格式并附带颜色描述

## 相关

API 集成（端点、轮询、Webhook）请参阅 **bfl-api** 技能。

## 规则索引

阅读各规则文件以获取详细指导：

- [rules/core-principles.md](rules/core-principles.md) - 通用 FLUX 提示词原则
- [rules/flux2-models.md](rules/flux2-models.md) - FLUX.2 系列：klein、max、pro、flex、dev
- [rules/flux1-models.md](rules/flux1-models.md) - FLUX.1 系列：FLUX.2 的前一代——pro、Kontext、Fill
- [rules/t2i-prompting.md](rules/t2i-prompting.md) - 文生图提示词模式
- [rules/i2i-prompting.md](rules/i2i-prompting.md) - 使用 FLUX.2 的图生图编辑
- [rules/json-structured-prompting.md](rules/json-structured-prompting.md) - 复杂场景构图
- [rules/hex-color-prompting.md](rules/hex-color-prompting.md) - 精确颜色指定
- [rules/typography-text.md](rules/typography-text.md) - 文字渲染与排版
- [rules/multi-reference-editing.md](rules/multi-reference-editing.md) - 多图参考
- [rules/negative-prompt-alternatives.md](rules/negative-prompt-alternatives.md) - 正向替代写法
- [rules/model-selection-guide.md](rules/model-selection-guide.md) - 如何选择合适模型

## 示例提示词

```
A weathered fisherman in his 70s with deep wrinkles and a salt-and-pepper beard,
wearing a navy cable-knit sweater, standing at the helm of his wooden boat.
Golden hour sunlight from the left creates dramatic rim lighting on his profile.
Shot on Hasselblad with 85mm lens at f/2.8, shallow depth of field with harbor
lights creating soft bokeh in the background. Kodak Portra 400 color science.
```
