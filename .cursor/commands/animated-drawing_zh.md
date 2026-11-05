# /animated-drawing — 使用真实动捕为提供的绘图制作动画

将用户提供的人形绘图/照片转换为该绘图运动的栅格 GIF/MP4（跳舞 / 行走 / 跳跃 / 挥手），通过 Meta 开源的 AnimatedDrawings 实现。若要*从零*创建会自行绘制的矢量涂鸦，请使用 `/ink-art`。

阅读 `skills/creative/animated-drawing.md`，然后使用所请求的动作为用户的绘图设置并运行 AnimatedDrawings。

- 仅适用于为*现有*的人形绘图/照片制作动画（单个角色，plain light 背景）。
- 输出为**栅格**（原绘图形变）— 非矢量，无绘制揭示效果。
- 优先使用开箱即用的 bundled-character 路径；auto-rig 需要 Docker 及约 670 MB 模型。
