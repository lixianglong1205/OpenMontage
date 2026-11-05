---
description: 手绘白底墨水涂鸦动画 — 角色自绘后行走/跳舞/挥手，或一本正经的小装置解说。矢量、确定性、HyperFrames → MP4。
---

阅读 `skills/creative/ink-theater.md` 与 `ink-theater/README.md`，然后按用户要求构建手绘墨水动画。

- 使用 **Ink Theater** 引擎（`ink-theater/ink-theater.js`）：可变宽度墨水笔触、可 seek 的 boil 效果、闭式 spring 缓动、FABRIK IK、contraption 语法。
- 若需 **行走 / 跳舞 / 挥手 / 跳跃** 的角色，使用 **Ink Puppet** 动作捕捉系统：`InkPuppet.create` → `p.drawIn`（自绘揭示）→ `InkPuppet.choreograph([{clip:'wave'},{clip:'twist'},…])`（动作名来自 `ink-theater/mocap/catalog.json`，12 个 CMU 来源动作）。**切勿手工微调动作**；通过 `node ink-theater/mocap/add-motion.mjs` 添加新动作。
- 字幕 = **HTML overlay `<div>`**（HyperFrames 不会将 webfont 应用到 SVG `<text>`）。
- 渲染前请校验（`npx hyperframes lint` + `snapshot`）。
