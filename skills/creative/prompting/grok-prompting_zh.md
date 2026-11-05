# Grok 提示词

当所选提供方为 `grok_image` 或 `grok_video` 时使用本文。

## 何时选用 Grok

- 需要编辑现有图像，而非从零生成
- 需要将多张源图合并为一张输出
- 需要受参考图影响、但不锁定首帧的短视频
- 希望用同一提供方、相近的提示语言完成图像与视频生成

## Grok 图像

### 最佳提示结构

```
[subject] + [action or change] + [setting] + [one style anchor] + [lighting]
```

### 编辑类提示

进行图像编辑时，直接描述期望的变换：

- 「将此图渲染为带细腻阴影的铅笔素描。」
- 「将 plain 白 T 恤替换为深绿色飞行员夹克。」
- 「将这两个人合成到同一处阳光公园场景中。」

除非必须保留未改部分，否则不必过度指定每一处不变细节。

### 多图合成

说明 Grok 应如何组合输入：

- 各元素来自哪张源图
- 哪些部分应保持独立
- 最终场景发生在何处

示例：

```
Place the person from image 1 and the person from image 2 on the same subway platform at dusk,
standing shoulder to shoulder, cinematic sodium-vapor lighting, realistic photography.
```

## Grok 视频

### 最佳提示结构

```
[shot] + [camera movement] + [subject] + [main motion beat] + [environment] + [lighting] + [tone]
```

### 参考图视频

Grok 支持在提示中使用 `<IMAGE_1>` 等占位符引用源图。
当你需要身份、服装或产品一致性时使用。

示例：

```
Medium full shot, slow push-in. The model from <IMAGE_1> walks onto a clean white runway wearing
the jacket from <IMAGE_2>. Soft studio lighting, premium fashion campaign, confident expression.
```

### 图生视频 vs 参考图生视频

- 当源图应作为开场帧时，使用图生视频（image-to-video）。
- 当源图应影响内容但不锁定构图时，使用参考图生视频（reference-to-video）。

## 常见错误

- 把 Grok 参考图当成严格分镜。它们是影响输入，而非精确帧锁定。
- 在一个片段请求里写多个场景切换。
- 堆叠过多风格标签、场景信息却过少。
- 使用「让它更好看」这类模糊编辑提示，而不是明确写出要改什么。

## OpenMontage 指引

- 图像编辑或合成时，优先 `grok_image`，而非选择器默认的主力工具。
- 参考条件视频、且简报要求把输入图中的人物、服装或产品带入运动时，优先 `grok_video`。
- 若交付物是纯电影感运动、无参考约束，在锁定提供方前将 Grok 与 Runway、Veo、Kling 对比。
