---
description: 将用户提供的角色手绘/照片通过真实动捕（Meta AnimatedDrawings）动画化 → 输出栅格 GIF/MP4。若要从零创建矢量涂鸦，请使用 /ink-art。
---

Read `skills/creative/animated-drawing.md`，然后搭建并运行 Meta 开源的 **AnimatedDrawings**，将用户提供的 drawing 按所需动作（dance / walk / jump / wave）动画化。

- 仅适用于动画化*已有*的人形手绘/照片。若要从零创建会自行绘制的矢量涂鸦 → 使用 `/ink-art`。
- 输出为**栅格**（原图变形）—— 非矢量，无绘制显现效果。
- 优先使用开箱即用的 bundled-character 路径；auto-rig 路径需要 Docker 及约 670 MB 模型。
