# 第三方声明 — Ink Theater

Ink Theater 捆绑了两项第三方资源。二者均可免费用于任何用途（包括商业用途），仅需注明出处。

## Patrick Hand（手写字体）— SIL Open Font License 1.1

`assets/patrickhand.ttf`

Copyright (c) 2010-2012 Patrick Wagesreiter (mail@patrickwagesreiter.at)。
依据 SIL Open Font License（开放字体许可证）1.1 版授权。OFL 允许捆绑、嵌入与再分发（含商业用途）；仅禁止单独出售字体本身，并要求随附本声明及许可证全文。完整许可证：`assets/OFL.txt`。

## 动作捕捉片段 — CMU Graphics Lab Motion Capture Database

`mocap/clips/*.json`，并打包为 `mocap/clips.js`

二维动作片段源自 **CMU Graphics Lab Motion Capture Database**（http://mocap.cs.cmu.edu）中的 BVH 文件，经 `mocap/bvh2clip.mjs` 转换而来，数据来自 `una-dinosauria/cmu-mocap` 镜像。CMU 数据库**可免费用于一切用途**（"This data is free for use in research and commercial projects worldwide"）。各片段对应的源 trial ID 记录在 `mocap/catalog.json` 中（例如 `walk` = CMU 02_01，`wave` = CMU 141_16）。

未捆绑 Meta / FAIR（AnimatedDrawings）的动作捕捉数据。独立的 `/animated-drawing` 能力文档说明 Meta 的 AnimatedDrawings 工具，但本引擎的片段库完全来自 CMU。
