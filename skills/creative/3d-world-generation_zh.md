# 3D 世界生成

当动画或电影级项目需要真实、连续的 Three.js 环境，而非一堆静态图或生成视频片段时，使用本 Layer 2 技能。

## 能力路径

1. 在注册表中查询 `3d_world_generation`、`3d_asset_acquisition`、`3d_asset_generation` 和 `3d_world_rendering`。
2. 阅读所选工具的 `agent_skills`；生产工作需同时阅读 `.agents/skills/threejs-world-generation` 与 `.agents/skills/3d-asset-generation`。
3. 在提案阶段选定交付路径。需要可编辑、浏览器原生的 Three.js 交付物时，使用 `render_runtime="hyperframes"` 与 `composition_mode="atelier"`。需要 Blender 渲染的 PNG 序列及受控音/视频封装时，使用 `render_runtime="ffmpeg"`。后者仍是真实 3D 运动；FFmpeg 仅对 Blender 帧进行打包。
4. 使用 `animation` 或 `cinematic` 流水线均可。3D 世界是复用的生产能力，不是独立流水线。
5. 锁定保真度档位。`blockout` 仅用于语义布局与镜头迭代。英雄级/参考驱动输出需要 `production`、重复资产使用授权目录、在合适时用 Atlas/fal 生成独特资产，并用 `blender_world` 进行场景组装与渲染。

## 产物映射

| 阶段 | 约定 |
|---|---|
| proposal | 记录世界承诺、显式与推断策略、保真度档位，以及浏览器原生 Three.js/HyperFrames 路径或生产级 Blender/FFmpeg 路径。 |
| script | 使用节拍或稀疏标题；旁白可选。 |
| scene_plan | 在同一连续坐标系中定义全局、区域与步行级镜头节拍。 |
| assets | 用 `threejs_asset_catalog` 安装/盘点重复资产；用 `atlas_3d` 或 `fal_3d` 采样独特英雄资产；用 `blender_world` 组装并渲染全局/区域/步行静帧；将网格注册为 `type="3d_asset"`，将可编辑世界规格/`.blend` 注册为 `type="3d_world"`。 |
| assets review | 产出语义/线框诊断与代表性快照；记录有界 refinement 问题。 |
| edit | 携带镜头时间轴，且不改变区域 ID 或 seed。 |
| compose | 浏览器原生：在已编写的 HyperFrames 工作区上调用 `video_compose`。生产 Blender：启用 resume 渲染编号 PNG 序列，再由 `video_compose`/FFmpeg 封装帧与音频，勿将 FFmpeg 当作运动生成器。 |

## 必需资产元数据

记录：

- `source_tool: "threejs_world"`；
- `provider: "threejs"`；
- `quality_tier`、`seed` 及返回的 model identifier；
- catalog ID、源 URL、许可证、归档哈希、所选 model ID 与 PBR 材质贴图；
- workspace 路径与 `world.json` 路径；
- region、landmark、instance 与 terrain-triangle 数量；
- 诊断警告与 refinement 轮次；
- `layer3_skills_read: ["threejs-world-generation"]`。

## 审查重点

- 地形连续，并确立大尺度轮廓。
- 区域颜色、起伏、散布与地标与同一语义布局一致。
- 环境实例满足坡度与接触约束。
- 全局、区域与步行级画面在空间上保持连贯。
- 镜头不得穿入地形或裁切远平面。
- 最终渲染保持可编辑性：世界、区域、地标与镜头关键帧仍为结构化文件。
- 生产帧在前景、中景与背景深度使用带纹理的已创作模型；以原始体或 untextured 平地为主视为资产门禁失败。

勿将此路径用于孤立产品旋转展示、CSS 视差 landscape，或没有显式场景图的 AI 生成飞越镜头。
