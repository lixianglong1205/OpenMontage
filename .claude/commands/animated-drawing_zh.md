---
description: 使用真实动作捕捉（Meta AnimatedDrawings）为**提供的**角色手绘/照片添加动画 → 输出该手绘动起来后的栅格 GIF/MP4。若要从零**创建**矢量涂鸦，请使用 /ink-art。
argument-hint: [path to drawing] [motion: dance|walk|jump|wave]
---

读取 `skills/creative/animated-drawing.md`，然后设置并运行 Meta 开源的 **AnimatedDrawings**，按请求的动作类型为提供的手绘添加动画。

- 仅在用户**已有**可动画化的人形手绘/照片时使用。若要创建会自行绘制的矢量涂鸦 → 请改用 `/ink-art`。
- 输出为**栅格**（原图变形）——无矢量、无逐笔绘制揭示效果。请确认输入为纯色浅背景上的单个人形。
- 优先使用即装即用（turnkey）的 bundled-character 路径；auto-rig 路径需要 Docker 及约 670 MB 模型。

手绘与动作：$ARGUMENTS
