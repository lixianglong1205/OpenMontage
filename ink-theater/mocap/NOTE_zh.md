# 动作捕捉来源与许可

所有捆绑片段均来自 **CMU Graphics Lab Motion Capture Database**
(http://mocap.cs.cmu.edu)，该数据库 **可免费用于一切用途，包括研究与商业**。
BVH 文件从 `una-dinosauria/cmu-mocap` 镜像获取；`clips.js` /
`clips/*.json` 是由 `bvh2clip.mjs` 生成的二维衍生数据。各片段对应的源试验
ID 见 `catalog.json`（例如 `wave` = CMU 141_16，`shuffle` = CMU 77_29）。
完整归属说明见 `../THIRD_PARTY_NOTICES.md`。

## 添加动作（自扩展 — 无需改代码）

```
node add-motion.mjs <name> <cmu-id|url|path> [category] "[description]"
# e.g.  node add-motion.mjs backflip 90_01 dance "a backflip"
```

该流程会拉取 BVH、完成转换（自动映射 fair1 / CMU / Mixamo 骨骼）、
重新打包 `clips.js`，并更新 `catalog.json`。CMU 提供数千个片段
（walk、run、dance、wave、jump 等）。凡需随库分发的内容请优先选用 CMU，以保持
库的许可合规。不同骨骼可能需要在 `bvh2clip.mjs` 的 `ALIAS`
表中增加别名，并用 `--axis xy|zy` 选择投影平面。
