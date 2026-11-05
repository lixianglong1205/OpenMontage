# /ink-art — 手绘墨水涂鸦动画

角色先自绘再行走/跳舞/挥手，或冷面 contraption 解说。矢量、确定性，经 HyperFrames 渲染为 MP4。

阅读 `skills/creative/ink-theater.md` 与 `ink-theater/README.md`，再按用户要求构建：

- **Ink Theater** 引擎（`ink-theater/ink-theater.js`）：可变宽度墨水笔触、seek-safe boil、闭式 spring eases、FABRIK IK、contraption grammar。
- 若要**会行走 / 跳舞 / 挥手 / 跳跃的角色**，使用 **Ink Puppet** mocap 系统：`InkPuppet.create` → `p.drawIn`（自绘显现）→ `InkPuppet.choreograph([{clip:'wave'},{clip:'twist'},…])`（动作名来自 `ink-theater/mocap/catalog.json`，12 个 CMU 来源动作）。**切勿手动微调动作**；通过 `node ink-theater/mocap/add-motion.mjs` 添加动作。
- 字幕 = **HTML overlay `<div>`**（HyperFrames 不会将 webfonts 应用到 SVG `<text>`）。
- 渲染前验证（`npx hyperframes lint` + `snapshot`）。
