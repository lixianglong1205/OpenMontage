---
description: 手绘白底墨线涂鸦动画 — 角色先自绘再行走/跳舞/挥手，或一本正经的机械装置解说。矢量、确定性渲染，经 HyperFrames 输出 MP4。
argument-hint: [要动画化的内容]
---

请先阅读 `skills/creative/ink-theater.md`（隐喻方法、色彩语法、已挖掘的原型）和 `ink-theater/README.md`（引擎 API、确定性、SVG 文本字体注意事项），再按下方描述制作成片。

- 使用 **Ink Theater** 引擎（`ink-theater/ink-theater.js`）：可变宽度墨线笔触、可 seek 的 boil、闭式弹簧缓动、FABRIK IK、机械装置语法。
- 若需 **行走 / 跳舞 / 挥手 / 跳跃的角色**，使用 **Ink Puppet** 动作捕捉系统：`InkPuppet.create(...)` → `p.drawIn(tl, ...)` 完成自绘揭示 → `InkPuppet.choreograph(tl, p, [{clip:'wave'},{clip:'twist'},{clip:'walk'},...])`。片段名称见 `ink-theater/mocap/catalog.json`（12 个源自 CMU 的动作）。**切勿手工微调动作** — 用 `node ink-theater/mocap/add-motion.mjs <name> <cmu-id> …` 添加动作（免费 CMU 动捕含 walk/run/dance/…）。
- 字幕 = **HTML  overlay `<div>`**（HyperFrames 不会把 webfont 应用到 SVG `<text>`）。
- 用 `npx hyperframes lint` + `snapshot`（目视检查 contact sheet）验证，再渲染。

在 OpenMontage 中，这运行在 `animation` 管线（插画）或 `character-animation` 管线（动捕木偶）上 — 它是一种风格 + 引擎，不是独立管线。

请求：$ARGUMENTS
