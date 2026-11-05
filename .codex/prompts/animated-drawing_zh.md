---
description: 使用真实动捕（Meta AnimatedDrawings）为「已有」绘画/照片生成动画 → 栅格 GIF/MP4。要从零绘制矢量涂鸦，请使用 /ink-art。
argument-hint: [绘画路径] [动作: dance|walk|jump|wave]
---

先阅读 `skills/creative/animated-drawing.md`，再配置并运行 Meta 开源的 AnimatedDrawings，按所选动作为提供的绘画生成动画。

- 仅用于为*已有*的人形绘画/照片做动画。要从零创建矢量涂鸦 → 使用 `/ink-art`。
- 输出为**栅格**（原图变形）——无矢量、无逐笔绘制揭示效果。
- 优先使用开箱即用的 bundled-character 路径；auto-rig 需要 Docker 及约 670 MB 模型。

绘画与动作：$ARGUMENTS
