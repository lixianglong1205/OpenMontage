---
description: 手绘墨水涂鸦动画 — 角色自绘后行走/跳舞/挥手，或装置说明（vector → HyperFrames MP4）。
argument-hint: [要动画化的内容]
---

阅读 `skills/creative/ink-theater.md` 与 `ink-theater/README.md`，然后构建下述手绘墨水动画。

- **Ink Theater** 引擎（`ink-theater/ink-theater.js`）：可变宽度墨水笔触、可 seek 的 boil 效果、闭式 spring 缓动、FABRIK IK、装置语法（contraption grammar）。
- 若需 **行走 / 跳舞 / 挥手 / 跳跃的角色**，使用 **Ink Puppet** 动作捕捉系统：`InkPuppet.create` → `p.drawIn`（自绘揭示）→ `InkPuppet.choreograph([{clip:'wave'},{clip:'twist'},…])`（动作名来自 `ink-theater/mocap/catalog.json`，12 个源自 CMU 的动作）。**切勿手工调 motion**；通过 `node ink-theater/mocap/add-motion.mjs` 添加动作。
- 字幕 = **HTML overlay `<div>`**（HyperFrames 不会将 webfont 应用到 SVG `<text>`）。渲染前请校验（`npx hyperframes lint` + `snapshot`）。

请求：$ARGUMENTS
